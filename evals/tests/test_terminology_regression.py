from __future__ import annotations

import unittest

from evals.run_terminology_regression import instruction_leak_reasons


class TerminologyInstructionTests(unittest.TestCase):
    def test_accepts_consistent_term_without_meta_instruction(self) -> None:
        output = (
            "Enable Secure Review in Settings. Secure Review checks new uploads. "
            "Secure Review does not inspect existing files."
        )
        self.assertEqual(instruction_leak_reasons(output), [])

    def test_accepts_split_settings_action(self) -> None:
        output = "Open Settings. Enable Secure Review. Secure Review checks new uploads but does not inspect existing files."
        self.assertEqual(instruction_leak_reasons(output), [])

    def test_rejects_negated_settings_action(self) -> None:
        outputs = (
            "Do not open Settings. Enable Secure Review. Secure Review checks new uploads but does not inspect existing files.",
            "Never open Settings. Enable Secure Review. Secure Review checks new uploads but does not inspect existing files.",
            "Do not enable Secure Review in Settings. Secure Review checks new uploads. Secure Review does not inspect existing files.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("missing-enable-action", instruction_leak_reasons(output))

    def test_rejects_observed_keep_enabled_instruction(self) -> None:
        output = (
            "Enable Secure Review in Settings. Secure Review checks new uploads but does not inspect existing files. "
            "Keep Secure Review enabled."
        )
        self.assertIn(
            "terminology-instruction-became-product-instruction",
            instruction_leak_reasons(output),
        )

    def test_rejects_equivalent_invented_product_instructions(self) -> None:
        endings = (
            "Leave Secure Review enabled.",
            "Ensure Secure Review remains enabled.",
            "Secure Review must remain enabled.",
            "Secure Review should stay enabled.",
            "Keep the product term Secure Review throughout.",
        )
        prefix = (
            "Enable Secure Review in Settings. Secure Review checks new uploads. "
            "Secure Review does not inspect existing files. "
        )
        for ending in endings:
            with self.subTest(ending=ending):
                self.assertIn(
                    "terminology-instruction-became-product-instruction",
                    instruction_leak_reasons(prefix + ending),
                )

    def test_rejects_reversed_or_missing_scan_scope(self) -> None:
        outputs = (
            (
                "Enable Secure Review in Settings. Secure Review checks existing files, not new uploads. Secure Review does not inspect existing files.",
                {"missing-new-upload-scope", "missing-existing-file-limitation"},
            ),
            (
                "Enable Secure Review in Settings. Secure Review checks new uploads and existing files. Secure Review does not inspect existing files.",
                {"missing-existing-file-limitation"},
            ),
        )
        for output, expected in outputs:
            with self.subTest(output=output):
                self.assertTrue(expected.issubset(instruction_leak_reasons(output)))

    def test_rejects_wrong_sentence_count(self) -> None:
        outputs = (
            "Enable Secure Review in Settings. Secure Review checks new uploads but does not inspect existing files.",
            "Enable Secure Review in Settings. Secure Review checks new uploads. Secure Review does not inspect existing files. Secure Review is available now.",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("wrong-sentence-count", instruction_leak_reasons(output))


if __name__ == "__main__":
    unittest.main()
