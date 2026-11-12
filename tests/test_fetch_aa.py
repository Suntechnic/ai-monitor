import tempfile
import unittest
from pathlib import Path
from unittest import mock

import fetch_aa


def api_page(data, has_more):
    return {
        "tier": "free",
        "intelligence_index_version": 5,
        "pagination": {"page": 1, "page_size": 200, "total_pages": 2, "has_more": has_more},
        "data": data,
    }


def api_item(slug, name, index, creator="Creator", released="2026-08-18"):
    return {
        "slug": slug,
        "name": name,
        "model_creator": {"name": creator},
        "release_date": released,
        "evaluations": {"artificial_analysis_intelligence_index": index},
        "pricing": {"price_1m_input_tokens": 1.4, "price_1m_output_tokens": 4.4},
    }


FETCHED_AT = "2026-11-12T01:00:00+03:00"


class ArtificialAnalysisTests(unittest.TestCase):
    def setUp(self):
        pages = [
            api_page([api_item("new-model", "New Model", 70.0)], True),
            api_page([api_item("old-model", "Old Model", 40.0), api_item("unmeasured", "Unmeasured", None)], False),
        ]
        self.meta = pages[0]
        self.snapshot = fetch_aa.parse_api(
            [item for page in pages for item in page["data"]], pages[0], fetched_at=FETCHED_AT)

    def test_parse_api_builds_best_models_from_nonzero_indexes(self):
        self.assertEqual(self.snapshot["schema_version"], 2)
        self.assertEqual(self.snapshot["index"], {
            "name": "Artificial Analysis Intelligence Index",
            "version": "5",
            "method": "AA Intelligence Index over model catalog",
        })
        self.assertEqual(self.snapshot["tier"], "free")
        best = {item["slug"]: item["intelligence_index"] for item in self.snapshot["best_models"]}
        self.assertEqual(best, {"new-model": 70.0, "old-model": 40.0})
        self.assertEqual(len(self.snapshot["models"]), 3)
        self.assertIsNone(next(item for item in self.snapshot["models"] if item["slug"] == "unmeasured")["intelligence_index"])

    def test_load_api_key_prefers_environment_then_env_file(self):
        self.assertEqual(fetch_aa.load_api_key(environ={"AA_API_KEY": "  k1 "}), "k1")
        with tempfile.TemporaryDirectory() as temporary:
            key_file = Path(temporary) / ".env"
            key_file.write_text("# comment\nAA_API_KEY=\"k2\"\nOTHER=x\n", encoding="utf-8")
            self.assertEqual(fetch_aa.load_api_key(environ={}, path=key_file), "k2")
            key_file.write_text("", encoding="utf-8")
            self.assertIsNone(fetch_aa.load_api_key(environ={}, path=key_file))

    def test_fetch_models_requires_key_and_follows_pagination(self):
        with self.assertRaisesRegex(RuntimeError, "AA_API_KEY"):
            fetch_aa.fetch_models(None)
        responses = [
            api_page([api_item("a", "A", 10.0)], True),
            api_page([api_item("b", "B", 20.0)], False),
        ]
        calls = []

        def fake_request(url, key, timeout):
            calls.append(url)
            return responses[len(calls) - 1]

        with mock.patch.object(fetch_aa, "_api_request", fake_request):
            items, meta = fetch_aa.fetch_models("key", url="https://api.test/models")
        self.assertEqual(len(items), 2)
        self.assertEqual(meta["intelligence_index_version"], 5)
        self.assertEqual(calls, ["https://api.test/models?page=1", "https://api.test/models?page=2"])

    def test_rating_has_measured_models_and_explicit_no_data(self):
        with tempfile.TemporaryDirectory() as temporary:
            reports = Path(temporary) / "actual"
            reports.mkdir()
            (reports / "report.md").write_text(
                "| Задача | Модель |\n| --- | --- |\n| coding | New Model |\n", encoding="utf-8")
            (reports / "prices.md").write_text(
                "## Сравнение цен по моделям\n### Old Model\n### Missing Model\n", encoding="utf-8")
            text = fetch_aa.render_rating(self.snapshot, reports, Path(temporary) / "missing.yml")
            self.assertIn("Intelligence Index v5", text)
            self.assertIn(FETCHED_AT, text)
            self.assertIn("| 1 | New Model | 70.0 |", text)
            self.assertIn("| 2 | Old Model | 40.0 |", text)
            self.assertIn("| — | Missing Model | н/д |", text)
            self.assertIn("New Model > Old Model", text)
            self.assertNotIn("Missing Model >", text)
            self.assertIn("Методология", text)

    def test_comparison_does_not_chain_ties_beyond_one_point(self):
        rows = [
            {"model": "A", "intelligence_index": 10.0},
            {"model": "B", "intelligence_index": 9.5},
            {"model": "C", "intelligence_index": 9.0},
        ]
        self.assertEqual(fetch_aa._comparison_groups(rows), "A ≈ B > C")

    def test_session_candidates_exclude_free_and_local_but_keep_paid_aa_base(self):
        with tempfile.TemporaryDirectory() as temporary:
            reports = Path(temporary)
            (reports / "report.md").write_text("", encoding="utf-8")
            (reports / "prices.md").write_text("", encoding="utf-8")
            sessions = Path(temporary) / "models.yml"
            sessions.write_text(
                "opencode:\n  beam-free:\n    sessions: 1\n"
                "other:\n  free-new-model:\n    sessions: 1\n"
                "  free-unknown-model:\n    sessions: 1\n"
                "  old-model:\n    sessions: 1\n"
                "  auto:\n    sessions: 1\n"
                "ollama:\n  qwen3:14b:\n    sessions: 1\n",
                encoding="utf-8",
            )
            text = fetch_aa.render_rating(self.snapshot, reports, sessions)
            self.assertIn("| New Model |", text)
            self.assertIn("| Old Model |", text)
            self.assertNotIn("unknown-model", text)
            self.assertNotIn("beam-free", text)
            self.assertNotIn("qwen3", text)
            self.assertNotIn("| auto |", text)

    def test_offline_cache_and_network_fallback_preserve_snapshot(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary) / "cache.json"
            output = Path(temporary) / "new" / "aa.json"
            fetch_aa.write_json(cache, self.snapshot)
            _, cached = fetch_aa.fetch_snapshot(output, cache, offline=True)
            self.assertTrue(cached)
            models = {item["model"]: item for item in fetch_aa.load_snapshot(output)["best_models"]}
            self.assertEqual(models["New Model"]["intelligence_index"], 70.0)
            output.unlink()
            with mock.patch.object(fetch_aa, "fetch_models", side_effect=OSError("offline")):
                _, cached = fetch_aa.fetch_snapshot(output, cache)
            self.assertTrue(cached)
            self.assertEqual(fetch_aa.load_snapshot(output)["fetched_at"], FETCHED_AT)
            output.unlink()
            cache.unlink()
            with mock.patch.object(fetch_aa, "load_api_key", return_value=None):
                with self.assertRaises(RuntimeError) as raised:
                    fetch_aa.fetch_snapshot(output, cache)
            self.assertIn("fetch failed", str(raised.exception))
            self.assertIn("AA_API_KEY", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
