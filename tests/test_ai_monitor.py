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


if __name__ == "__main__":
    unittest.main()
