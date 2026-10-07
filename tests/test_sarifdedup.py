import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sarifdedup import core

RAW = {"ruleId": "R1", "uri": "a.c", "line": 10, "level": "warning", "message": "x"}


class SarifDedupTest(unittest.TestCase):
    def test_single_result(self):
        report = core.dedup([dict(RAW)], set(), set(), core.Counter())
        self.assertEqual(len(report.results), 1)

    def test_result_fields(self):
        report = core.dedup([dict(RAW)], set(), set(), core.Counter())
        self.assertEqual((report.results[0].rule_id, report.results[0].level), ("R1", "warning"))

    def test_no_baseline_no_suppression(self):
        report = core.dedup([dict(RAW)], set(), set(), core.Counter())
        self.assertEqual(len(report.suppressed), 0)

    def test_baseline_suppresses(self):
        report = core.dedup([dict(RAW)], {"R1|a.c", "R1|a.c|10"}, set(), core.Counter())
        self.assertEqual(len(report.suppressed), 1)

    def test_lookup_missing(self):
        report = core.dedup([dict(RAW)], set(), set(), core.Counter())
        self.assertIsNone(core.lookup(report, "nope", core.Counter()))

    def test_counter_counts(self):
        counter = core.Counter()
        core.dedup([dict(RAW)], set(), set(), counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
