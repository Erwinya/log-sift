import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import log_sift  # noqa: E402


SAMPLE = """\
127.0.0.1 - - [17/Sep/2026:08:00:01 +0000] "GET /health HTTP/1.1" 200 12
127.0.0.1 - - [17/Sep/2026:08:00:04 +0000] "GET /missing HTTP/1.1" 404 19
2026-09-17T08:00:06Z ERROR database connection timed out
2026-09-17T08:00:07Z WARN retrying upstream /api/v1/users
"""


class AnalyzeTests(unittest.TestCase):
    def test_status_and_paths(self) -> None:
        report = log_sift.analyze(SAMPLE)
        self.assertEqual(report["lines"], 4)
        self.assertEqual(report["status_counts"]["200"], 1)
        self.assertEqual(report["status_counts"]["404"], 1)
        self.assertIn(("GET /health", 1), report["top_paths"])

    def test_levels_and_error_samples(self) -> None:
        report = log_sift.analyze(SAMPLE)
        self.assertEqual(report["levels"]["ERROR"], 1)
        self.assertEqual(report["levels"]["WARN"], 1)
        self.assertTrue(any("database connection" in s for s in report["error_samples"]))

    def test_cli_json(self) -> None:
        sample = ROOT / "samples" / "app.log"
        code = log_sift.main(["--file", str(sample), "--json"])
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
