import datetime as dt
import os
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import ai_monitor


class SessionStatsRefreshTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.stats = self.root / "runs" / "session-stats" / "models.yml"
        self.stats.parent.mkdir(parents=True)
        self.patch_root = mock.patch.object(ai_monitor, "ROOT", self.root)
        self.patch_root.start()
        self.addCleanup(self.patch_root.stop)
        self.addCleanup(self.temporary.cleanup)

    def write_stats(self, age_hours):
        self.stats.write_text("{}\n", encoding="utf-8")
        old = time.time() - age_hours * 3600
        os.utime(self.stats, (old, old))

    def test_missing_or_old_stats_are_stale(self):
        self.assertTrue(ai_monitor.stats_are_stale(self.stats))
        self.write_stats(3)
        self.assertTrue(ai_monitor.stats_are_stale(self.stats))

    def test_fresh_stats_are_not_stale(self):
        self.write_stats(1)
        self.assertFalse(ai_monitor.stats_are_stale(self.stats))

    def test_stale_stats_run_collect_with_current_interpreter(self):
        self.write_stats(3)
        profiles = self.root / "profiles.yml"
        with mock.patch.object(ai_monitor.subprocess, "run",
                               return_value=SimpleNamespace(returncode=0)) as run:
            refreshed = ai_monitor.refresh_session_stats(profiles)
        self.assertTrue(refreshed)
        command = run.call_args.args[0]
        self.assertEqual(command[:2], [ai_monitor.sys.executable,
                                       str(self.root / "session_stats.py")])
        self.assertEqual(command[2:], ["--profiles", str(profiles), "collect"])
        self.assertEqual(run.call_args.kwargs["cwd"], self.root)
        self.assertEqual(run.call_args.kwargs["timeout"], ai_monitor.STATS_TIMEOUT)

    def test_fresh_stats_skip_collect(self):
        self.write_stats(1)
        with mock.patch.object(ai_monitor.subprocess, "run") as run:
            refreshed = ai_monitor.refresh_session_stats(self.root / "profiles.yml")
        self.assertFalse(refreshed)
        run.assert_not_called()

    def test_collect_failure_does_not_raise(self):
        self.write_stats(3)
        with mock.patch.object(ai_monitor.subprocess, "run",
                               side_effect=OSError("no ssh")):
            refreshed = ai_monitor.refresh_session_stats(self.root / "profiles.yml")
        self.assertFalse(refreshed)

    def test_partial_collect_is_reported_but_not_fatal(self):
        self.write_stats(3)
        with mock.patch.object(ai_monitor.subprocess, "run",
                               return_value=SimpleNamespace(returncode=1)):
            refreshed = ai_monitor.refresh_session_stats(self.root / "profiles.yml")
        self.assertFalse(refreshed)


class StaleThresholdTests(unittest.TestCase):
    def test_default_threshold_is_two_hours(self):
        self.assertEqual(ai_monitor.STATS_MAX_AGE, dt.timedelta(hours=2))


class RepositoryProfilesTests(unittest.TestCase):
    def test_repository_profiles_define_right_sizing_policy(self):
        profiles = ai_monitor.load_profiles(ai_monitor.ROOT / "profiles.yml")
        for key, profile in profiles.items():
            with self.subTest(key):
                self.assertIn("policy", profile)
                self.assertGreaterEqual(
                    profile["policy"]["main_min_index"],
                    profile["policy"]["budget_min_index"],
                )


class ProfilePolicyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.addCleanup(self.temporary.cleanup)

    def load(self, policy):
        path = self.root / "profiles.yml"
        path.write_text(
            "task:\n"
            "  title: Задача\n"
            "  input: 100\n"
            "  output: 10\n"
            "  cache_read: 0\n"
            + policy,
            encoding="utf-8",
        )
        return ai_monitor.load_profiles(path)

    def test_policy_is_optional(self):
        profiles = self.load("")
        self.assertNotIn("policy", profiles["task"])

    def test_valid_policy_is_loaded(self):
        profiles = self.load(
            "  policy:\n"
            "    main_min_index: 40\n"
            "    budget_min_index: 30\n"
            "    max_premium: 2.5\n"
        )
        self.assertEqual(profiles["task"]["policy"], {
            "main_min_index": 40,
            "budget_min_index": 30,
            "max_premium": 2.5,
        })

    def test_budget_floor_above_main_floor_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "budget_min_index exceeds main_min_index"):
            self.load(
                "  policy:\n"
                "    main_min_index: 40\n"
                "    budget_min_index: 45\n"
                "    max_premium: 2.0\n"
            )

    def test_invalid_policy_values_are_rejected(self):
        cases = {
            "missing main floor": (
                "  policy:\n"
                "    budget_min_index: 30\n"
                "    max_premium: 2.0\n"
            ),
            "premium below one": (
                "  policy:\n"
                "    main_min_index: 40\n"
                "    budget_min_index: 30\n"
                "    max_premium: 0.5\n"
            ),
            "unknown field": (
                "  policy:\n"
                "    main_min_index: 40\n"
                "    budget_min_index: 30\n"
                "    max_premium: 2.0\n"
                "    max_index: 60\n"
            ),
            "not a mapping": "  policy: right-sizing\n",
        }
        for name, policy in cases.items():
            with self.subTest(name):
                with self.assertRaises(ValueError):
                    self.load(policy)


if __name__ == "__main__":
    unittest.main()
