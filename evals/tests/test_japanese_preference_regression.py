from __future__ import annotations

import unittest

from evals.run_japanese_preference_regression import (
    business_request_reasons,
    condition_scope_reasons,
    role_object_preference_reasons,
    status_certainty_reasons,
    terminology_style_reasons,
)


class JapanesePreferenceTests(unittest.TestCase):
    def test_business_request_avoids_redundant_deferential_frame(self) -> None:
        good = "先日の会議では、移行時期について複数の意見がございました。現行環境は7月末まで利用可能です。つきましては、田中様には6月20日までに移行案Aをご承認くださいますようお願いいたします。なお、ご承認前には作業を開始しないようお願いいたします。"
        bad = good.replace("田中様には6月20日", "田中様におかれましては、6月20日")
        paraphrase = "先日の会議では、移行時期についてさまざまな意見がございました。現行の環境は7月末まで使えます。つきましては、田中様には移行案Aを6月20日までにご承認いただきますようお願いいたします。なお、ご承認前には作業へ着手しないようお願いいたします。"
        self.assertEqual(business_request_reasons(good), [])
        self.assertEqual(business_request_reasons(paraphrase), [])
        self.assertIn("redundant-deferential-frame", business_request_reasons(bad))

    def test_business_request_rejects_reversed_or_missing_facts(self) -> None:
        outputs = (
            "先日の会議では移行時期について一つの意見が出ました。現行環境は7月末まで利用可能です。田中様には6月20日までに移行案Aをご承認ください。承認前に作業を開始しないでください。",
            "先日の会議では移行時期について複数の意見が出ました。現行環境は7月末まで利用できません。田中様には6月20日までに移行案Aをご承認ください。承認前に作業を開始しないでください。",
            "先日の会議では移行時期について複数の意見が出ました。現行環境は7月末まで利用可能です。田中様は6月20日以降に移行案Aを承認しました。承認前に作業を開始しないでください。",
            "先日の会議では移行時期について複数の意見が出ました。現行環境は7月末まで利用可能です。田中様には6月20日までに移行案Aをご承認ください。承認前に作業へ着手しないわけではありません。",
            "先日の会議では移行時期について複数の意見がございました。現行環境は7月末まで利用可能です。つきましては、田中様には6月20日までに移行案Aをご承認くださいますようお願いいたします。なお、ご承認前には作業を開始しないようお願いいたしますが、作業を開始してください。",
            "先日の会議では移行時期について複数の意見がございました。現行環境は7月末まで利用可能です。つきましては、田中様には6月20日までに移行案Aをご承認くださいますようお願いいたします。なお、ご承認前には作業を開始しないようお願いいたしますが、開始してください。",
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
        unquoted = "管理画面で共有スペースを作成します。共有スペースにメンバーを追加してください。共有スペースには外部ユーザーを招待できません。"
        quoted_later = "管理画面で共有スペース（以下「共有スペース」）を作成します。共有スペースにメンバーを追加してください。共有スペースには外部ユーザーを招待できません。"
        self.assertEqual(terminology_style_reasons(good), [])
        self.assertEqual(terminology_style_reasons(good.replace("。共有スペース", "。\n共有スペース")), [])
        self.assertIn("missing-initial-term-quote", terminology_style_reasons(unquoted))
        self.assertIn("missing-initial-term-quote", terminology_style_reasons(quoted_later))
        self.assertIn("repeated-term-quotes", terminology_style_reasons(bad))
        self.assertIn("invented-demonstrative-identity-or-missing-external-user-prohibition", terminology_style_reasons(good.replace("共有スペースには外部ユーザー", "この共有スペースには外部ユーザー")))
        self.assertIn("invented-demonstrative-identity-or-missing-external-user-prohibition", terminology_style_reasons(good.replace("共有スペースには外部ユーザー", "当該共有スペースには外部ユーザー")))
        adversaries = (
            good.replace("作成します", "作成しますが、実際には作成できません"),
            good.replace("共有スペースには外部ユーザーを招待できません", "外部ユーザーを招待できます。共有スペースには外部ユーザーを招待できません"),
            good.replace("共有スペースには", "このワーク\nスペースと同一の共有スペースには"),
        )
        for output in adversaries:
            with self.subTest(output=output):
                self.assertTrue(terminology_style_reasons(output))

    def test_role_object_makes_report_approval_explicit(self) -> None:
        good = "佐藤さんは鈴木さんに、『レビュー後に鈴木さんが案件ID JP-42の報告書を送る』と伝えました。佐藤さんは、その報告書の承認を担当します。"
        invalid = (
            good.replace("その報告書の承認", "承認"),
            good.replace("その報告書の承認を担当します", "その報告書を読み、承認を担当します"),
            good.replace("その報告書の承認", "その報告書ではなく申請書の承認"),
            good.replace("その報告書の承認を担当します", "その報告書の承認を担当しません"),
        )
        self.assertEqual(role_object_preference_reasons(good), [])
        for output in invalid:
            with self.subTest(output=output):
                self.assertIn("approval-object-left-implicit", role_object_preference_reasons(output))

    def test_status_keeps_fixed_update_time_definite(self) -> None:
        good = "現在、決済処理の遅延を調査しております。初期調査ではネットワーク障害の可能性が示されていますが、原因は確定しておりません。約12%のお客様に影響している可能性があります。次回更新は18時です。"
        definite_variant = good.replace("次回更新は18時です", "次回更新は18時となります")
        changed_cause_wording = (
            good.replace("原因は確定しておりません", "原因は特定されておりません"),
            good.replace("原因は確定しておりません", "原因は未確定です"),
            good.replace("原因は確定しておりません", "原因は確定していません"),
            good.replace("原因は確定しておりません", "原因は確定しておりませんでした"),
            good.replace("原因は確定しておりません", "原因は確定しておりませんが、現在は確定しています"),
        )
        weakened = (
            good.replace("次回更新は18時です", "次回更新は18時を予定しております"),
            good.replace("次回更新は18時です", "次回更新予定は18時です"),
            good.replace("次回更新は18時です", "次回更新は暫定的に18時です"),
        )
        self.assertEqual(status_certainty_reasons(good), [])
        self.assertEqual(status_certainty_reasons(definite_variant), [])
        for output in changed_cause_wording:
            with self.subTest(output=output):
                self.assertIn("cause-uncertainty-terminology-drift", status_certainty_reasons(output))
        for output in weakened:
            with self.subTest(output=output):
                self.assertIn("fixed-update-time-weakened", status_certainty_reasons(output))

    def test_status_rejects_fact_polarity_and_number_changes(self) -> None:
        outputs = (
            "現在、決済処理の遅延は調査しておりません。ネットワーク障害の可能性がありますが、原因は未確定です。約12%のお客様に影響している可能性があります。次回更新は18時です。",
            "現在、決済処理の遅延を調査しております。ネットワーク障害が原因で確定しています。約12%のお客様に影響している可能性があります。次回更新は18時です。",
            "現在、決済処理の遅延を調査しております。ネットワーク障害の可能性がありますが、原因は未確定です。約21%のお客様に影響している可能性があります。次回更新は18時です。",
            "現在、決済処理の遅延を調査しております。ネットワーク障害の可能性はありませんが、原因は未確定です。約12%のお客様に影響している可能性があります。次回更新は18時です。",
            "現在、決済処理の遅延を調査しております。ネットワーク障害の可能性がありますが、原因は未確定です。約12%ではなく約21%のお客様に影響している可能性があります。次回更新は18時です。",
            "現在、決済処理の遅延を調査しております。ネットワーク障害の可能性がありますが、原因は未確定です。約12%のお客様に影響していない可能性があります。次回更新は18時です。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(status_certainty_reasons(output))

    def test_defined_term_rejects_action_polarity_reversals(self) -> None:
        outputs = (
            "管理画面で共有スペースを作成しないでください。共有スペースにメンバーを追加してください。共有スペースには外部ユーザーを招待できません。",
            "管理画面で共有スペースを作成します。共有スペースにメンバーを追加しないでください。共有スペースには外部ユーザーを招待できません。",
            "管理画面で共有スペースを作成します。共有スペースにメンバーを追加してください。共有スペースには外部ユーザーを招待できないわけではありません。",
            "管理画面で「共有スペース」を作成します。共有スペースにメンバーを追加してください。この共有スペースには外部ユーザーを招待できませんでした。",
            "管理画面で「共有スペース」を作成します。共有スペースにメンバーを追加してください。この共有スペースには外部ユーザーを招待できませんが、招待できます。",
        )
        for output in outputs:
            with self.subTest(output=output):
                self.assertTrue(terminology_style_reasons(output))


if __name__ == "__main__":
    unittest.main()
