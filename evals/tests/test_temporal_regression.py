from __future__ import annotations

import unittest

from evals.run_temporal_regression import minimal_wording_reasons, temporal_reasons


class TemporalPreservationTests(unittest.TestCase):
    def test_accepts_relative_deadline_and_current_access(self) -> None:
        outputs = (
            "Maya told Priya that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya retains access.",
            "Maya told Priya that Priya's access to ACCT-74 would end Friday. Before her access ends, Priya must export the audit log; Maya still has access.",
            "Maya informed Priya that Priya will lose access to ACCT-74 Friday. Prior to losing access, Priya must export the audit log; Maya continues to retain access.",
            "Maya told Priya that Priya's access to ACCT-74 would end Friday. Prior to Priya losing access, Priya must export the audit log; Maya retains access.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(temporal_reasons(output), [])

    def test_minimal_wording_keeps_already_clear_relative_reference(self) -> None:
        minimal = "Maya told Priya that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya retains access."
        expanded = minimal.replace("before then", "before her access ends")
        self.assertEqual(minimal_wording_reasons(minimal), [])
        self.assertIn("unnecessary-relative-reference-expansion", minimal_wording_reasons(expanded))

    def test_rejects_observed_timing_and_tense_changes(self) -> None:
        output = "Maya told Priya that Priya’s access to ACCT-74 would end Friday, while Maya would retain access. Priya must export the audit log before Friday."
        self.assertIn("relative-deadline-became-calendar-boundary", temporal_reasons(output))
        self.assertIn("maya-access-tense-changed", temporal_reasons(output))

    def test_rejects_negated_or_rebound_facts(self) -> None:
        outputs = (
            "Maya told Priya that Maya’s access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya retains access.",
            "Priya told Maya that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya retains access.",
            "Maya told Priya that Priya’s access would end Friday. Priya must export the audit log before then; Maya retains access.",
            "Maya told Priya that Priya’s access to ACCT-74 would end Friday. Maya must export the audit log before then; Maya retains access.",
            "Maya told Priya that Priya’s access to ACCT-74 will not actually end Friday. Priya must export the audit log before then; Maya retains access.",
            "Maya told Priya that Priya’s access to ACCT-74 won't actually end Friday. Priya must export the audit log before then; Maya retains access.",
            "Maya told Priya that Priya’s access to ACCT-74 would end Friday. Priya must not export the audit log before then; Maya retains access.",
            "Maya told Priya before then that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log; Maya retains access.",
            "Before then, Maya told Priya that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log; Maya retains access.",
            "Maya told Priya that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya retains access starting Saturday.",
            "Maya told Priya that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya retains access after Friday.",
            "Maya told Priya that Priya’s access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya no longer has access.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(temporal_reasons(output))


if __name__ == "__main__":
    unittest.main()
