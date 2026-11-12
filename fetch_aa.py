#!/usr/bin/env python3
"""Fetch Artificial Analysis coding results and render a deterministic rating."""
import argparse
import datetime as dt
import html
import json
import math
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
AA_URL = "https://artificialanalysis.ai/agents/coding-agents"
METHODOLOGY_URL = "https://artificialanalysis.ai/methodology/coding-agents-benchmarking"
API_URL = "https://artificialanalysis.ai/api/v2/language/models/free"
KEY_ENV = "AA_API_KEY"
DEFAULT_KEY_FILE = ROOT / ".env"
DEFAULT_CACHE = ROOT / "runs" / "artificial-analysis" / "models-free.json"
DEFAULT_REPORTS = ROOT / "reports" / "actual"
DEFAULT_SESSION_MODELS = ROOT / "runs" / "session-stats" / "models.yml"
DEFAULT_MAPPING = ROOT / "aa-mapping.yml"


def normalize_model(value):
    """Normalize spelling, not model versions or model families."""
    value = html.unescape(str(value)).strip().strip("`").replace("**", "")
    value = value.rsplit("/", 1)[-1].strip()
    value = re.sub(r":(?:batch|free)$", "", value, flags=re.I)
    value = re.sub(r"^free-", "", value, flags=re.I)
    value = value.casefold().replace("–", "-").replace("—", "-")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def load_api_key(environ=None, path=DEFAULT_KEY_FILE):
    """Return the AA API key from the environment or a .env file, else None."""
    env = os.environ if environ is None else environ
    key = env.get(KEY_ENV)
    if key and key.strip():
        return key.strip()
    if Path(path).is_file():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            if name.strip() == KEY_ENV:
                value = value.strip().strip('"').strip("'").strip()
                if value:
                    return value
    return None


def _api_request(url, key, timeout):
    request = urllib.request.Request(url, headers={"User-Agent": "ai-monitor/2.0", "x-api-key": key})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(20_000_001)
    except urllib.error.HTTPError as exc:
        details = {
            "401": "invalid or missing API key",
            "403": "subscription tier does not cover this endpoint",
            "429": "rate limit exceeded",
        }.get(str(exc.code), exc.reason)
        if exc.code == 429 and exc.headers:
            retry_after = exc.headers.get("Retry-After")
            if retry_after:
                details += f"; retry after {retry_after}s"
        raise RuntimeError(f"Artificial Analysis API error {exc.code}: {details}") from exc
    if len(body) > 20_000_000:
        raise ValueError("Artificial Analysis API response exceeds 20 MB")
    return json.loads(body.decode("utf-8"))


def fetch_models(key, timeout=60, url=API_URL):
    """Return (items, meta) for every page of the free model catalog."""
    if key is None:
        raise RuntimeError("AA_API_KEY is not set; add it to the environment or .env")
    items = []
    meta = None
    for page in range(1, 21):
        payload = _api_request(f"{url}?page={page}", key, timeout)
        if not isinstance(payload.get("data"), list):
            raise ValueError("Artificial Analysis API response has no data list")
        if meta is None:
            meta = payload
        elif payload.get("tier") != meta.get("tier") or payload.get(
            "intelligence_index_version"
        ) != meta.get("intelligence_index_version"):
            raise ValueError("Artificial Analysis API pages disagree on tier or index version")
        items.extend(payload["data"])
        if not (payload.get("pagination") or {}).get("has_more"):
            return items, meta
    raise ValueError("Artificial Analysis API pagination does not end within 20 pages")


def parse_api(items, meta, fetched_at=None):
    """Build a schema_version 2 snapshot from the free model catalog."""
    version = meta.get("intelligence_index_version")
    if version is None or not items:
        raise ValueError("Artificial Analysis returned no model catalog or index version")
    models = []
    for item in items:
        evaluations = item.get("evaluations") or {}
        pricing = item.get("pricing") or {}
        creator = item.get("model_creator") or {}
        index = evaluations.get("artificial_analysis_intelligence_index")
        if isinstance(index, bool) or not isinstance(index, (int, float)) or not math.isfinite(index):
            index = None
        else:
            index = round(float(index), 4)
        models.append({
            "slug": item.get("slug"),
            "model": item.get("name"),
            "creator": creator.get("name"),
            "release_date": item.get("release_date"),
            "intelligence_index": index,
            "pricing": {
                "input": pricing.get("price_1m_input_tokens"),
                "output": pricing.get("price_1m_output_tokens"),
            },
        })
    models.sort(key=lambda item: (
        item["intelligence_index"] is None,
        -(item["intelligence_index"] or 0),
        item["model"] or "",
    ))
    best = [model for model in models if model["intelligence_index"]]
    if not best:
        raise ValueError("Artificial Analysis returned no models with an Intelligence Index")
    return {
        "schema_version": 2,
        "source": "Artificial Analysis",
        "url": API_URL,
        "methodology_url": METHODOLOGY_URL,
        "api_url": API_URL,
        "fetched_at": fetched_at or dt.datetime.now().astimezone().isoformat(),
        "index": {
            "name": "Artificial Analysis Intelligence Index",
            "version": str(version),
            "method": "AA Intelligence Index over model catalog",
        },
        "tier": meta.get("tier"),
        "models": models,
        "best_models": best,
    }


def empty_snapshot(reason="Снимок Artificial Analysis недоступен"):
    return {
        "schema_version": 2,
        "source": "Artificial Analysis",
        "url": API_URL,
        "methodology_url": METHODOLOGY_URL,
        "api_url": API_URL,
        "fetched_at": dt.datetime.now().astimezone().isoformat(),
        "available": False,
        "error": reason,
        "index": {"name": "Artificial Analysis Intelligence Index", "version": "unknown"},
        "tier": None,
        "models": [],
        "best_models": [],
    }


def load_snapshot(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != 2 or not isinstance(data.get("best_models"), list) or not data["best_models"]:
        raise ValueError(f"Invalid or empty Artificial Analysis snapshot: {path}")
    if not data.get("fetched_at"):
        raise ValueError(f"Artificial Analysis snapshot has no fetch date: {path}")
    return data


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def fetch_snapshot(output, cache=DEFAULT_CACHE, offline=False, timeout=60, url=API_URL):
    """Write a snapshot; on network failure use the cache without hiding its age."""
    output = Path(output)
    cache = Path(cache)
    cached = output if output.exists() else cache
    if offline:
        data = load_snapshot(cached)
        if output != cached:
            write_json(output, data)
        return data, True
    try:
        data = parse_api(*fetch_models(load_api_key(), timeout=timeout, url=url))
        write_json(output, data)
        if cache != output:
            write_json(cache, data)
        return data, False
    except Exception as fetch_error:
        try:
            data = load_snapshot(cached)
        except Exception as cache_error:
            raise RuntimeError(
                f"Artificial Analysis fetch failed ({fetch_error}); cache unavailable ({cache_error})"
            ) from fetch_error
        if output != cached:
            write_json(output, data)
        return data, True


def _model_names_from_markdown(path):
    if not Path(path).is_file():
        return []
    names = []
    model_column = None
    in_comparison = False
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            in_comparison = line.strip() == "## Сравнение цен по моделям"
        if in_comparison and line.startswith("### "):
            names.append(line[4:].strip())
        if not line.lstrip().startswith("|"):
            model_column = None
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if "Модель" in cells:
            model_column = cells.index("Модель")
            continue
        if model_column is not None and len(cells) > model_column and not set(cells[0]) <= {"-", ":", " "}:
            names.append(cells[model_column])
    return names


def collect_candidates(reports_dir=DEFAULT_REPORTS, session_models=DEFAULT_SESSION_MODELS):
    reports_dir = Path(reports_dir)
    names = []
    for filename in ("report.md", "prices.md"):
        names.extend(_model_names_from_markdown(reports_dir / filename))
    if Path(session_models).is_file():
        import yaml
        raw = yaml.safe_load(Path(session_models).read_text(encoding="utf-8")) or {}
        for provider, provider_models in raw.items():
            if provider == "ollama" or not isinstance(provider_models, dict):
                continue
            for model_id in provider_models:
                tail = model_id.rsplit("/", 1)[-1].casefold()
                if tail == "auto" or tail.endswith("-free"):
                    continue
                # A free-prefix route can identify an underlying paid model too.
                # It is retained only below when that exact model has an AA result.
                names.append(model_id)
    return list(dict.fromkeys(name for name in names if name and not name.startswith("---")))


def _load_mapping(path=DEFAULT_MAPPING):
    if not Path(path).is_file():
        return {}, {}
    import yaml
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    aliases = {normalize_model(key): normalize_model(value) for key, value in (data.get("aliases") or {}).items()}
    labels = {normalize_model(key): value for key, value in (data.get("labels") or {}).items()}
    return aliases, labels


def _comparison_groups(measured):
    groups = []
    for item in measured:
        if not groups or groups[-1][0]["intelligence_index"] - item["intelligence_index"] >= 1:
            groups.append([item])
        else:
            groups[-1].append(item)
    return " > ".join(" ≈ ".join(item["model"] for item in group) for group in groups)


def render_rating(snapshot, reports_dir=DEFAULT_REPORTS, session_models=DEFAULT_SESSION_MODELS, mapping=DEFAULT_MAPPING):
    aliases, labels = _load_mapping(mapping)
    models = {normalize_model(item["slug"]): item for item in snapshot["best_models"] if item.get("slug")}
    candidates = {}
    for raw in collect_candidates(reports_dir, session_models):
        key = normalize_model(raw)
        if not key or key == "auto":
            continue
        if str(raw).rsplit("/", 1)[-1].casefold().startswith("free-") and key not in models:
            continue
        key = aliases.get(key, key)
        candidates.setdefault(key, raw)
    entries = []
    for key, raw in candidates.items():
        result = models.get(key)
        entries.append({
            "key": key,
            "name": result["model"] if result else labels.get(key, str(raw).strip("`")),
            "result": result,
        })
    entries.sort(key=lambda item: (
        item["result"] is None,
        -(item["result"]["intelligence_index"] if item["result"] else 0),
        item["name"].casefold(),
    ))
    index = snapshot.get("index", {})
    if snapshot.get("available", True):
        description = (
            f"Данные Artificial Analysis от {snapshot['fetched_at']}. "
            f"Рейтинг основан на Intelligence Index v{index.get('version', 'unknown')}: "
            "сводная оценка 0–100 по бенчмаркам Artificial Analysis. "
            "Это не отдельный PHP/Vue-бенчмарк; цена и локальная популярность в оценку не входят."
        )
    else:
        description = snapshot.get("error", "Снимок Artificial Analysis недоступен") + "; все оценки — н/д."
    lines = [
        "# Рейтинг моделей",
        "",
        description,
        "",
        "Оценка относится к конкретной версии модели в каталоге Artificial Analysis; "
        "результаты родственной модели или другой версии не переносятся.",
        "",
    ]
    lines += [
        "| Место | Модель | Intelligence Index |",
        "| ---: | --- | ---: |",
    ]
    position = 0
    previous_score = None
    for order, entry in enumerate(entries, 1):
        result = entry["result"]
        if result is None:
            place = "—"
            score = "н/д"
        else:
            value = result["intelligence_index"]
            if previous_score is None or value < previous_score - 0.05:
                position = order
            previous_score = value
            place = str(position)
            score = f"{value:.1f}"
        lines.append(f"| {place} | {entry['name']} | {score} |")
    measured = [entry["result"] for entry in entries if entry["result"]]
    if measured:
        lines += [
            "",
            _comparison_groups(measured),
            "",
            "Обозначения: `>` — разница не менее 1 пункта Intelligence Index; `≈` — разница меньше 1 пункта. "
            "Это правило представления сырых результатов, а не проверка статистической значимости. "
            "Модели с «н/д» в сравнение не входят.",
        ]
    else:
        lines += ["", "Ни у одной модели из пула нет данных Artificial Analysis; сравнение не построено."]
    lines += [
        "",
        f"Источник: {snapshot['url']} · [Методология]({snapshot['methodology_url']}).",
        "",
    ]
    return "\n".join(lines)


def refresh_rating(snapshot, reports_dir=DEFAULT_REPORTS, session_models=DEFAULT_SESSION_MODELS, mapping=DEFAULT_MAPPING):
    reports_dir = Path(reports_dir)
    text = render_rating(snapshot, reports_dir, session_models, mapping)
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / "rating.md"
    path.write_text(text, encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser(description="Artificial Analysis coding data and deterministic rating")
    parser.add_argument("--output", type=Path, default=DEFAULT_CACHE, help="Snapshot destination")
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE, help="Fallback and shared cache")
    parser.add_argument("--offline", action="store_true", help="Use cache without network access")
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--refresh-rating", action="store_true", help="Rebuild only reports/actual/rating.md")
    parser.add_argument("--reports", type=Path, default=DEFAULT_REPORTS)
    parser.add_argument("--session-models", type=Path, default=DEFAULT_SESSION_MODELS)
    parser.add_argument("--mapping", type=Path, default=DEFAULT_MAPPING)
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be positive")
    data, cached = fetch_snapshot(args.output, args.cache, args.offline, args.timeout)
    print(f"Artificial Analysis: {args.output} ({len(data['best_models'])} models, cached={cached})")
    if args.refresh_rating:
        path = refresh_rating(data, args.reports, args.session_models, args.mapping)
        print(f"Rating: {path}")


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
