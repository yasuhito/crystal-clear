from __future__ import annotations

import unittest

from evals.run_chinese_role_regression import minimal_role_change_reasons, role_change_reasons


class ChineseRolePreservationTests(unittest.TestCase):
    def test_accepts_roles_without_inventing_reviewer(self) -> None:
        output = "李敏告诉王伟，王伟将在审核后关闭工单 CN-88。王伟负责关闭工单；李敏负责最终确认。必须在周五之前完成。"
        self.assertEqual(role_change_reasons(output), [])

    def test_accepts_natural_role_paraphrases(self) -> None:
        outputs = (
            "李敏通知王伟，经审核通过后由王伟关闭工单 CN-88。最终确认由李敏负责。须在周五前完成。",
            "李敏告知王伟，审核完成后由王伟关闭工单 CN-88。李敏负责对审核结果进行最终确认。务必在周五之前完成。",
            "李敏告知王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。上述事项必须在周五前完成。",
            "李敏告知王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。关闭工单和最终确认均须在周五前完成。",
            "李敏告知王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。这两项工作都必须在周五前完成。",
            "李敏告知王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。二者均须在周五前完成。",
            "李敏告知王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。上述两项工作必须在周五前完成。",
            "李敏告知王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。上述事项须于周五前完成。",
            "1. 李敏告知王伟，审核后由王伟关闭工单 CN-88。2. 李敏负责最终确认。3. 以上事项必须在周五前完成。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertEqual(role_change_reasons(output), [])

    def test_rejects_invented_reviewer_roles(self) -> None:
        outputs = (
            "李敏告诉王伟，王伟将在李敏审核后关闭工单 CN-88。王伟负责关闭工单；李敏负责最终确认。必须在周五之前完成。",
            "李敏告诉王伟，审核人是李敏；审核后由王伟关闭工单 CN-88。李敏负责最终确认。必须在周五之前完成。",
            "李敏告诉王伟，王伟审核后关闭工单 CN-88。李敏负责最终确认。必须在周五之前完成。",
            "李敏告诉王伟，审核人是评审团队；审核后由王伟关闭工单 CN-88。李敏负责最终确认。必须在周五之前完成。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("invented-reviewer-role", role_change_reasons(output))

    def test_rejects_li_replacing_wang_as_closer(self) -> None:
        outputs = (
            "李敏告诉王伟，李敏将在审核后关闭工单 CN-88。李敏负责最终确认。必须在周五之前完成。",
            "李敏告诉王伟：“我将在审核后关闭工单 CN-88。”王伟负责关闭工单 CN-88；李敏负责最终确认。必须在周五之前完成。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("li-replaced-wang-as-closer", role_change_reasons(output))

    def test_rejects_invented_final_confirmation_precondition(self) -> None:
        outputs = (
            "李敏告诉王伟，李敏最终确认后，王伟关闭工单 CN-88。必须在周五之前完成。",
            "李敏告诉王伟，王伟须在李敏最终确认后关闭工单 CN-88。必须在周五之前完成。",
            "李敏告诉王伟，只有李敏最终确认，王伟才可关闭工单 CN-88。必须在周五之前完成。",
            "李敏告诉王伟，待李敏最终确认后，由王伟关闭工单 CN-88。必须在周五之前完成。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("invented-final-confirmation-order", role_change_reasons(output))

    def test_rejects_missing_required_roles_and_deadline(self) -> None:
        output = "王伟将在审核后处理工单。"
        reasons = role_change_reasons(output)
        self.assertIn("missing-li-tells-wang", reasons)
        self.assertIn("missing-wang-closes-ticket", reasons)
        self.assertIn("missing-li-final-confirmation", reasons)
        self.assertIn("missing-shared-friday-must-condition", reasons)

    def test_rejects_deadline_narrowed_to_one_responsibility(self) -> None:
        outputs = (
            "李敏告诉王伟，王伟将在审核后关闭工单 CN-88。李敏负责最终确认。工单必须在周五之前关闭。",
            "李敏告诉王伟，王伟将在审核后关闭工单 CN-88。李敏负责最终确认。王伟必须在周五前关闭工单。",
            "李敏告诉王伟，王伟将在审核后关闭工单 CN-88。李敏负责最终确认。李敏必须在周五前完成最终确认。",
            "李敏告诉王伟，王伟将在审核后关闭工单 CN-88，李敏负责最终确认，关闭工单必须在周五前完成。",
            "李敏告诉王伟，王伟将在审核后关闭工单 CN-88，李敏负责最终确认，最终确认必须在周五前完成。",
            "李敏告诉王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。上述事项必须在周五前完成；最终确认改为下周一前完成。",
            "李敏告诉王伟，审核后由王伟关闭工单 CN-88，李敏负责最终确认。上述事项必须在周五前完成；最终确认可在下周二完成。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertIn("missing-shared-friday-must-condition", role_change_reasons(output))

    def test_rejects_negated_deadline(self) -> None:
        endings = (
            "不必在周五之前完成，但必须最终完成。",
            "周五前无需完成，但必须最终完成。",
            "并非必须在周五前完成，但必须最终完成。",
            "关闭工单和最终确认不一定必须在周五前完成。",
            "关闭工单和最终确认在周五前不得完成，但周五前必须保持未完成状态。",
        )
        prefix = "李敏告诉王伟，审核后由王伟关闭工单 CN-88。李敏负责最终确认。"
        for ending in endings:
            with self.subTest(ending=ending):
                self.assertIn("missing-shared-friday-must-condition", role_change_reasons(prefix + ending))

    def test_minimal_oracle_isolates_roles_and_order(self) -> None:
        valid_outputs = (
            "李敏告诉王伟，审核后由王伟关闭工单。李敏负责最终确认。",
            "李敏告诉王伟，审核后王伟将关闭工单。李敏负责最终确认。",
        )
        for valid in valid_outputs:
            with self.subTest(valid=valid):
                self.assertEqual(minimal_role_change_reasons(valid), [])
        invalid = "李敏告诉王伟，待李敏最终确认后由王伟关闭工单。"
        self.assertIn("invented-final-confirmation-order", minimal_role_change_reasons(invalid))


if __name__ == "__main__":
    unittest.main()
