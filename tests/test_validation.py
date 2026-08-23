from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_configs import DEFAULT_BASELINE, validate
from scripts.validate_docs import validate as validate_docs
from soc.triage_syslog import triage


class ConfigValidationTests(unittest.TestCase):
    def test_evidence_baseline_has_no_static_failures(self):
        checks = validate(json.loads(DEFAULT_BASELINE.read_text(encoding="utf-8")))
        self.assertFalse([check for check in checks if check.level == "FAIL"])
        self.assertTrue([check for check in checks if check.level == "WARN"])

    def test_overlapping_networks_fail(self):
        data = json.loads(DEFAULT_BASELINE.read_text(encoding="utf-8"))
        data["vlans"][1]["subnet"] = data["vlans"][0]["subnet"]
        checks = validate(data)
        self.assertTrue(any(check.level == "FAIL" and check.name == "non-overlapping subnets" for check in checks))


class SyslogTriageTests(unittest.TestCase):
    def test_synthetic_fixture_is_deterministic(self):
        fixture = Path(__file__).resolve().parents[1] / "soc" / "fixtures" / "synthetic-ios-syslog.log"
        result = triage(fixture.read_text(encoding="utf-8").splitlines())
        self.assertEqual(len(result["events"]), 4)
        self.assertEqual(result["summary"]["acl_deny"], 1)
        self.assertEqual(result["summary"]["login_failure"], 1)
        self.assertEqual(result["unmatched_lines"], 0)

    def test_unknown_lines_are_not_misclassified(self):
        result = triage(["unstructured message with secret=redacted"])
        self.assertEqual(result["events"], [])
        self.assertEqual(result["unmatched_lines"], 1)


class DocumentationTests(unittest.TestCase):
    def test_relative_links_and_mermaid_fences(self):
        self.assertEqual(validate_docs(), [])


if __name__ == "__main__":
    unittest.main()
