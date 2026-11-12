#!/usr/bin/env python3
"""Fetch Artificial Analysis coding results and render a deterministic rating."""
import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
AA_URL = "https://artificialanalysis.ai/agents/coding-agents"
METHODOLOGY_URL = "https://artificialanalysis.ai/methodology/coding-agents-benchmarking"
DEFAULT_CACHE = ROOT / "runs" / "artificial-analysis" / "coding-agents.json"
DEFAULT_REPORTS = ROOT / "reports" / "actual"
DEFAULT_SESSION_MODELS = ROOT / "runs" / "session-stats" / "models.yml"
DEFAULT_MAPPING = ROOT / "aa-mapping.yml"


class _Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self._active = False
        self._buffer = []
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self._active = True
            self._buffer = []

    def handle_endtag(self, tag):
        if tag == "script" and self._active:
            self.scripts.append("".join(self._buffer))
            self._active = False

    def handle_data(self, data):
        if self._active:
            self._buffer.append(data)


def normalize_model(value):
    """Normalize spelling, not model versions or model families."""
    value = html.unescape(str(value)).strip().strip("`").replace("**", "")
    value = value.rsplit("/", 1)[-1].strip()
    value = re.sub(r":(?:batch|free)$", "", value, flags=re.I)
    value = re.sub(r"^free-", "", value, flags=re.I)
    value = value.casefold().replace("–", "-").replace("—", "-")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value)).strip("-")


def _next_text(html_text):
    parser = _Scripts()
    parser.feed(html_text)
    for script in parser.scripts:
        match = re.fullmatch(r"self\.__next_f\.push\((.*)\)", script, re.S)
        if not match:
            continue
        try:
            args = json.loads(match.group(1))
        except ValueError:
            continue
        if len(args) > 1 and isinstance(args[1], str):
            yield args[1]


def _benchmark_key(dataset_id):
    known = {
        "frontiercode-v1.1-main": "frontiercode",
        "terminal-bench-v4": "terminal_bench",
        "swe-atlas-qna": "swe_atlas_qna",
    }
    return known.get(dataset_id, normalize_model(dataset_id).replace("-", "_"))


def _score(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if not math.isfinite(value) or not 0 <= value <= 1:
        return None
    return round(value * 100, 4)


def parse_aa(html_text, fetched_at=None):
    """Extract model variants embedded in the public Next.js page."""
    rows = {}
    for text in _next_text(html_text):
        for match in re.finditer(r'\{\s*"id"\s*:\s*"[a-f0-9]{32}"', text):
            try:
                row, _ = json.JSONDecoder().raw_decode(text[match.start():])
            except ValueError:
                continue
            if "indexScore" in row:
                rows[row["id"]] = row
    if not rows:
        raise ValueError("Artificial Analysis benchmark rows not found; page format may have changed")

    variants = []
    for row in rows.values():
        model = row.get("model") or {}
        release = model.get("release") or {}
        name = release.get("name")
        slug = release.get("slug")
        score = _score(row.get("indexScore"))
        if not name or not slug or score is None:
            continue  # Router-only agents cannot be attributed to one model.
        evaluations = []
        for evaluation in row.get("evals") or []:
            component_score = _score((evaluation.get("mean") or {}).get("reward"))
            if component_score is None:
                continue
            evaluations.append({
                "id": evaluation.get("datasetIndexName"),
                "name": evaluation.get("evaluationDatasetSlug"),
                "key": _benchmark_key(evaluation.get("datasetIndexName", "")),
                "score": component_score,
                "weight": evaluation.get("weight"),
            })
        component_count = row.get("indexComponentCount")
        complete = (
            isinstance(component_count, int)
            and component_count >= 3
            and len(evaluations) == component_count
            and not row.get("isUnavailable", False)
        )
        effort = (model.get("effort") or {}).get("slug") or model.get("shortSuffix")
        mean = row.get("mean") or {}
        variants.append({
            "release_slug": slug,
            "model_key": normalize_model(slug),
            "model": name,
            "variant": model.get("name") or name,
            "effort": effort,
            "agent": row.get("agentName"),
            "index_score": score,
            "components": evaluations,
            "complete_index": complete,
            "cost_per_task_usd": mean.get("costUsd"),
            "time_per_task_seconds": mean.get("agentWallTimeSec"),
        })
    if not variants:
        raise ValueError("Artificial Analysis returned no attributable model results")

    best = {}
    for variant in variants:
        if not variant["complete_index"]:
            continue
        key = variant["model_key"]
        if key not in best or variant["index_score"] > best[key]["index_score"]:
            best[key] = variant
    if not best:
        raise ValueError("Artificial Analysis returned no complete model indexes")
    version = re.search(r"Artificial Analysis Coding Agent Index v([0-9.]+) incorporates", html_text)
    return {
        "schema_version": 1,
        "source": "Artificial Analysis",
        "url": AA_URL,
        "methodology_url": METHODOLOGY_URL,
        "fetched_at": fetched_at or dt.datetime.now().astimezone().isoformat(),
        "index": {
            "name": "Artificial Analysis Coding Agent Index",
            "version": version.group(1) if version else "unknown",
            "method": "AA composite; equal weight of its benchmark components",
        },
        "best_models": sorted(best.values(), key=lambda item: (-item["index_score"], item["model"])),
        "variants": sorted(variants, key=lambda item: (item["model"], -(item["index_score"]))),
    }


def empty_snapshot(reason="Снимок Artificial Analysis недоступен"):
    return {
        "schema_version": 1,
        "source": "Artificial Analysis",
        "url": AA_URL,
        "methodology_url": METHODOLOGY_URL,
        "fetched_at": dt.datetime.now().astimezone().isoformat(),
        "available": False,
        "error": reason,
        "index": {"name": "Artificial Analysis Coding Agent Index", "version": "unknown"},
        "best_models": [],
        "variants": [],
    }


def load_snapshot(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("best_models"), list) or not data["best_models"]:
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


def fetch_snapshot(output, cache=DEFAULT_CACHE, offline=False, timeout=60, url=AA_URL):
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
        request = urllib.request.Request(url, headers={"User-Agent": "ai-monitor/2.0"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(20_000_001)
        if len(body) > 20_000_000:
            raise ValueError("Artificial Analysis response exceeds 20 MB")
        data = parse_aa(body.decode("utf-8"))
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
        if not groups or groups[-1][0]["index_score"] - item["index_score"] >= 1:
            groups.append([item])
        else:
            groups[-1].append(item)
    return " > ".join(" ≈ ".join(item["model"] for item in group) for group in groups)


def render_rating(snapshot, reports_dir=DEFAULT_REPORTS, session_models=DEFAULT_SESSION_MODELS, mapping=DEFAULT_MAPPING):
    aliases, labels = _load_mapping(mapping)
    models = {item["model_key"]: item for item in snapshot["best_models"]}
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
        -(item["result"]["index_score"] if item["result"] else 0),
        item["name"].casefold(),
    ))
    index = snapshot.get("index", {})
    component_names = {}
    for model in snapshot["best_models"]:
        for component in model["components"]:
            component_names[component["key"]] = component["name"]
    benchmark_keys = ["frontiercode", "terminal_bench", "swe_atlas_qna"]
    if snapshot.get("available", True):
        description = (
            f"Данные Artificial Analysis от {snapshot['fetched_at']}. "
            f"Рейтинг основан на Coding Agent Index v{index.get('version', 'unknown')}: "
            "равный вес компонентов измеряет изменения кода, работу в терминале и понимание репозитория. "
            "Это не отдельный PHP/Vue-бенчмарк; цена, скорость и локальная популярность в оценку не входят."
        )
    else:
        description = snapshot.get("error", "Снимок Artificial Analysis недоступен") + "; все оценки — н/д."
    lines = [
        "# Рейтинг моделей",
        "",
        description,
        "",
        "Для каждой модели выбран лучший публичный вариант с полным индексом. "
        "Результат относится к указанным agent harness и режиму reasoning; оценки других версий не переносятся.",
        "",
    ]
    headers = ["Место", "Модель", "AA Index"] + [component_names.get(key, key) for key in benchmark_keys]
    headers += ["Измеренный вариант", "Уверенность"]
    lines += [
        "| " + " | ".join(headers) + " |",
        "| ---: | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    position = 0
    previous_score = None
    for order, entry in enumerate(entries, 1):
        result = entry["result"]
        if result is None:
            place = "—"
            scores = ["н/д"] * 4
            variant = "н/д"
            confidence = "Нет данных AA"
        else:
            score = result["index_score"]
            if previous_score is None or score < previous_score - 0.05:
                position = order
            previous_score = score
            place = str(position)
            components = {component["key"]: component["score"] for component in result["components"]}
            scores = [f"{score:.1f}"] + [
                f"{components[key]:.1f}" if key in components else "н/д" for key in benchmark_keys
            ]
            variant = f"{result['agent']}; {result['variant']}"
            confidence = (
                "Точная версия; в настройке указан fallback"
                if "default fallback" in result["variant"].casefold()
                else "Прямое измерение точной версии"
            )
        lines.append("| " + " | ".join([place, entry["name"]] + scores + [variant, confidence]) + " |")
    measured = [entry["result"] for entry in entries if entry["result"]]
    if measured:
        lines += [
            "",
            _comparison_groups(measured),
            "",
            "Обозначения: `>` — разница не менее 1 пункта AA Index; `≈` — разница меньше 1 пункта. "
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
