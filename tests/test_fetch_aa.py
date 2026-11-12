import tempfile
import unittest
from pathlib import Path
from unittest import mock

import fetch_aa


def aa_row(row_id, slug, name, score, effort="max"):
    components = [
        ("frontiercode-v1.1-main", "FrontierCode v1.1 Main", score - 0.02),
        ("terminal-bench-v4", "Terminal-Bench v4", score),
        ("swe-atlas-qna", "SWE-Atlas-QnA", score + 0.02),
    ]
    return {
        "id": row_id,
        "agentName": "Test Harness",
        "isUnavailable": False,
        "indexComponentCount": 3,
        "indexScore": score,
        "model": {
            "name": f"{name} ({effort.title()})",
            "shortSuffix": effort,
            "release": {"slug": slug, "name": name},
            "effort": {"slug": effort},
        },
        "evals": [
            {
                "datasetIndexName": dataset_id,
                "evaluationDatasetSlug": label,
                "mean": {"reward": component_score},
                "weight": 1 / 3,
            }
            for dataset_id, label, component_score in components
        ],
        "mean": {"costUsd": 1.25, "agentWallTimeSec": 100},
    }


class ArtificialAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            aa_row("a" * 32, "new-model", "New Model", 0.60),
            aa_row("b" * 32, "new-model", "New Model", 0.70, "high"),
            aa_row("c" * 32, "old-model", "Old Model", 0.40),
            aa_row("d" * 32, "non-reasoning-model", "Non-reasoning Model", 0.90, "none"),
        ]
        self.snapshot = {
            "schema_version": 1,
            "source": "Artificial Analysis",
            "url": fetch_aa.AA_URL,
            "methodology_url": fetch_aa.METHODOLOGY_URL,
            "fetched_at": "2026-11-12T01:00:00+03:00",
            "index": {"name": "Artificial Analysis Coding Agent Index", "version": "2.0"},
        }
        # Parsing a tiny synthetic page keeps tests independent of the live website.
        import json
        rsc = "31:" + json.dumps({"rows": self.rows})
        html = "Artificial Analysis Coding Agent Index v2.0 incorporates 3 benchmarks"
        html += "<script>self.__next_f.push(" + json.dumps([1, rsc]) + ")</script>"
        self.snapshot.update({
            "best_models": fetch_aa.parse_aa(html)["best_models"],
            "variants": fetch_aa.parse_aa(html)["variants"],
        })

    def test_parser_selects_best_exact_model_without_merging_versions(self):
        models = {item["model_key"]: item for item in self.snapshot["best_models"]}
        self.assertEqual(models["new-model"]["effort"], "high")
        self.assertEqual(models["new-model"]["index_score"], 70)
        self.assertEqual(models["old-model"]["index_score"], 40)
        self.assertEqual(models["non-reasoning-model"]["release_slug"], "non-reasoning-model")
        self.assertNotIn("model", models)

    def test_rating_has_measured_models_and_explicit_no_data(self):
        with tempfile.TemporaryDirectory() as temporary:
            reports = Path(temporary) / "actual"
            reports.mkdir()
            (reports / "report.md").write_text(
                "| Задача | Модель |\n| --- | --- |\n| coding | New Model |\n", encoding="utf-8")
            (reports / "prices.md").write_text(
                "## Сравнение цен по моделям\n### Old Model\n### Missing Model\n", encoding="utf-8")
            text = fetch_aa.render_rating(self.snapshot, reports, Path(temporary) / "missing.yml")
            self.assertIn("Coding Agent Index v2.0", text)
            self.assertIn("| 1 | New Model | 70.0 | 68.0 | 70.0 | 72.0 |", text)
            self.assertIn("| 2 | Old Model | 40.0 |", text)
            self.assertIn("| — | Missing Model | н/д | н/д | н/д | н/д | н/д | Нет данных AA |", text)
            self.assertIn("New Model > Old Model", text)
            self.assertNotIn("Missing Model >", text)

    def test_comparison_does_not_chain_ties_beyond_one_point(self):
        rows = [
            {"model": "A", "index_score": 10.0},
            {"model": "B", "index_score": 9.5},
            {"model": "C", "index_score": 9.0},
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
            self.assertEqual(models["New Model"]["index_score"], 70)
            output.unlink()
            with mock.patch("urllib.request.urlopen", side_effect=OSError("offline")):
                _, cached = fetch_aa.fetch_snapshot(output, cache)
            self.assertTrue(cached)
            self.assertEqual(fetch_aa.load_snapshot(output)["fetched_at"], self.snapshot["fetched_at"])


if __name__ == "__main__":
    unittest.main()
