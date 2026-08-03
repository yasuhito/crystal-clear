from __future__ import annotations

import unittest

from evals.run_terminology_regression import instruction_leak_reasons, ui_name_constraint_reasons


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


class UiNameConstraintTests(unittest.TestCase):
    def test_accepts_ui_name_constraint_as_artifact_content(self) -> None:
        outputs = (
            "管理者はTeam Syncを有効にしてください。Team Syncは新規メンバーのみを同期し、既存メンバーは対象外です。UI上の名称は「Team Sync」のままにしてください。",
            "管理者はTeam Syncを有効にしてください。新規メンバーのみが同期され、既存メンバーは対象外です。UIでは引き続き「Team Sync」という名称を使用してください。",
            "管理者はTeam Syncを有効にしてください。新規メンバーのみが同期され、既存メンバーは対象外です。ユーザーインターフェース上では名称を「Team Sync」から変えないでください。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(ui_name_constraint_reasons(output), [])

    def test_rejects_omitted_or_reversed_ui_name_constraint(self) -> None:
        outputs = (
            "管理者はTeam Syncを有効にしてください。Team Syncは新規メンバーのみを同期し、既存メンバーは対象外です。",
            "管理者はTeam Syncを有効にしてください。新規メンバーのみが同期され、既存メンバーは対象外です。UI上の名称はTeam Syncから変更しても構いません。",
            "管理者はTeam Syncを有効にしてください。新規メンバーのみが同期され、既存メンバーは対象外です。Team SyncはUI上の名称ではありません。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("missing-ui-name-constraint", ui_name_constraint_reasons(output))

    def test_ui_name_oracle_rejects_common_japanese_reversals(self) -> None:
        outputs = (
            (
                "管理者はTeam Syncを有効にしないでください。新規メンバーのみを同期し、既存メンバーは対象外です。UI上の名称は「Team Sync」のままにしてください。",
                "missing-enable-action",
            ),
            (
                "管理者はTeam Syncをオンにしないでください。新規メンバーのみを同期し、既存メンバーは対象外です。UI上の名称は「Team Sync」のままにしてください。",
                "missing-enable-action",
            ),
            (
                "管理者はTeam Syncを有効にしてください。新規メンバーは同期しません。既存メンバーは対象外です。UI上の名称は「Team Sync」のままにしてください。",
                "missing-new-member-scope",
            ),
            (
                "管理者はTeam Syncを有効にしてください。新規メンバーを同期対象にしません。既存メンバーは対象外です。UI上の名称は「Team Sync」のままにしてください。",
                "missing-new-member-scope",
            ),
            (
                "管理者はTeam Syncを有効にしてください。新規メンバーのみを同期します。既存メンバーは対象外ではありません。UI上の名称は「Team Sync」のままにしてください。",
                "missing-existing-member-exclusion",
            ),
            (
                "管理者はTeam Syncを有効にしてください。新規メンバーのみを同期します。既存メンバーを対象外にしません。UI上の名称は「Team Sync」のままにしてください。",
                "missing-existing-member-exclusion",
            ),
            (
                "管理者はTeam Syncを有効にしてください。新規メンバーのみを同期し、既存メンバーは対象外です。UIでは「Team Sync」という名称を使用しないでください。",
                "missing-ui-name-constraint",
            ),
        )
        for output, expected in outputs:
            with self.subTest(output=output):
                self.assertIn(expected, ui_name_constraint_reasons(output))

    def test_ui_name_oracle_still_requires_behavior_and_scope(self) -> None:
        output = "管理者はTeam Syncを無効にしてください。既存メンバーのみを同期します。UI上の名称は「Team Sync」のままにしてください。"
        self.assertEqual(
            set(ui_name_constraint_reasons(output)),
            {"missing-enable-action", "missing-new-member-scope", "missing-existing-member-exclusion"},
        )


if __name__ == "__main__":
    unittest.main()
