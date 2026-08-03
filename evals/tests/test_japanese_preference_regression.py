from __future__ import annotations

import unittest

from evals.run_japanese_preference_regression import (
    business_request_reasons,
    condition_scope_reasons,
    terminology_style_reasons,
)


class JapanesePreferenceTests(unittest.TestCase):
    def test_business_request_avoids_redundant_deferential_frame(self) -> None:
        good = "先日の会議では、移行時期について複数の意見がございました。現行環境は7月末まで利用可能です。つきましては、田中様に6月20日までに移行案Aをご承認くださいますようお願いいたします。なお、承認前に作業を開始しないでください。"
        bad = good.replace("田中様に6月20日", "田中様におかれましては、6月20日")
        paraphrase = "先日の会議では、移行時期についてさまざまな意見が出ました。現行の環境は7月末まで使えます。田中様には、移行案Aを6月20日までにご承認いただきますようお願いいたします。承認前に作業へ着手しないでください。"
        self.assertEqual(business_request_reasons(good), [])
        self.assertEqual(business_request_reasons(paraphrase), [])
        self.assertIn("redundant-deferential-frame", business_request_reasons(bad))

    def test_business_request_rejects_reversed_or_missing_facts(self) -> None:
        outputs = (
            "先日の会議では移行時期について一つの意見が出ました。現行環境は7月末まで利用可能です。田中様には6月20日までに移行案Aをご承認ください。承認前に作業を開始しないでください。",
            "先日の会議では移行時期について複数の意見が出ました。現行環境は7月末まで利用できません。田中様には6月20日までに移行案Aをご承認ください。承認前に作業を開始しないでください。",
            "先日の会議では移行時期について複数の意見が出ました。現行環境は7月末まで利用可能です。田中様は6月20日以降に移行案Aを承認しました。承認前に作業を開始しないでください。",
            "先日の会議では移行時期について複数の意見が出ました。現行環境は7月末まで利用可能です。田中様には6月20日までに移行案Aをご承認ください。承認前に作業へ着手しないわけではありません。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(business_request_reasons(output))

    def test_condition_marker_stays_on_thirty_day_filing_condition(self) -> None:
        good = "Proプランでは、障害発生から30日以内に申請した場合に限り、バックアップからデータを復元できます。復元には最大72時間かかる可能性があります。"
        bad = "Proプランをご利用の場合に限り、障害発生から30日以内に申請すると、バックアップからデータを復元できます。復元には最大72時間かかる可能性があります。"
        paraphrase = "Proプランでは、障害発生から30日以内の申請のみ、バックアップからデータを復元可能です。復元には最長72時間を要することがあります。"
        self.assertEqual(condition_scope_reasons(good), [])
        self.assertEqual(condition_scope_reasons(paraphrase), [])
        self.assertIn("limiter-moved-from-filing-condition", condition_scope_reasons(bad))

    def test_condition_scope_rejects_polarity_and_omissions(self) -> None:
        outputs = (
            "Proプラン以外では、障害発生から30日以内に申請した場合に限り、バックアップからデータを復元できます。復元には最大72時間かかる可能性があります。",
            "Proプランでは、30日以内に限り、バックアップからデータを復元できます。復元には最大72時間かかる可能性があります。",
            "Proプランでは、障害発生から30日以内に申請した場合に限り、バックアップからデータを復元できません。復元には最大72時間かかる可能性があります。",
            "Proプランでは、障害発生から30日以内に申請した場合に限り、バックアップからデータを復元できます。復元には最大72時間かからない可能性があります。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(condition_scope_reasons(output))

    def test_defined_term_does_not_repeat_visual_quotes(self) -> None:
        good = "管理画面で「共有スペース」を作成します。共有スペースにメンバーを追加してください。共有スペースには外部ユーザーを招待できません。"
        bad = "管理画面で「共有スペース」を作成します。「共有スペース」にメンバーを追加してください。「共有スペース」には外部ユーザーを招待できません。"
        self.assertEqual(terminology_style_reasons(good), [])
        self.assertIn("repeated-term-quotes", terminology_style_reasons(bad))

    def test_defined_term_rejects_action_polarity_reversals(self) -> None:
        outputs = (
            "管理画面で共有スペースを作成しないでください。共有スペースにメンバーを追加してください。共有スペースには外部ユーザーを招待できません。",
            "管理画面で共有スペースを作成します。共有スペースにメンバーを追加しないでください。共有スペースには外部ユーザーを招待できません。",
            "管理画面で共有スペースを作成します。共有スペースにメンバーを追加してください。共有スペースには外部ユーザーを招待できないわけではありません。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(terminology_style_reasons(output))


if __name__ == "__main__":
    unittest.main()
