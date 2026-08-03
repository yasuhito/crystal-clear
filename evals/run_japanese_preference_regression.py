#!/usr/bin/env python3
"""Run focused live checks for the remaining Japanese preference regressions."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import observe_trace
from evals.run_behavior import _materialize_skill
from evals.run_smoke import execute_pi

SCENARIOS: dict[str, str] = {
    "business": "SOURCEを一読で依頼内容が分かるように書き直してください。丁寧なビジネス日本語の依頼文だけを返してください。事実、期限、制約、固有表現を保持してください。SOURCE: 先日の会議では移行時期について複数の意見が出ました。現行環境は7月末まで利用できます。つきましては、田中様に6月20日までに移行案Aの承認をお願いいたします。承認前に作業を開始しないでください。",
    "condition": "SOURCEの条件を対象となる説明の近くに置いて書き直してください。条件が明確な案内文だけを日本語で返してください。可能性を確定表現に変えないでください。SOURCE: バックアップからデータを復元できます。対象はProプランで、障害発生から30日以内に申請した場合に限ります。復元には最大72時間かかる可能性があります。",
    "terminology": "SOURCEの製品用語を統一して書き直してください。用語を統一した3文の操作説明だけを返してください。制約を保持してください。SOURCE: 管理画面で「共有スペース」を作成します。共同エリアにメンバーを追加してください。このワークスペースでは外部ユーザーを招待できません。用語は「共有スペース」に統一してください。",
    "status": "SOURCEをお客様向けに書き直してください。丁寧で落ち着いた障害報告だけを日本語で返してください。不確実性と数値を保持してください。SOURCE: 現在、決済処理の遅延を調査しております。初期調査ではネットワーク障害の可能性が示されていますが、原因は未確定です。約12%のお客様に影響している可能性があります。次回更新は18時です。",
}


def business_request_reasons(output: str) -> list[str]:
    meeting_context = bool(
        re.search(r"会議[^。]{0,35}移行時期[^。]{0,25}(?:複数|さまざま)[^。]{0,15}意見", output)
    ) and not bool(re.search(r"会議[^。]{0,50}(?:一つ|1つ)[^。]{0,10}意見", output))
    environment_available = bool(
        re.search(
            r"現行(?:の)?環境[^。]{0,30}7月末[^。]{0,25}(?:利用可能|利用できます|使えます|ご利用いただけます)|"
            r"現行(?:の)?環境[^。]{0,30}(?:利用可能|利用できます|使えます|ご利用いただけます)[^。]{0,25}7月末",
            output,
        )
    ) and not bool(re.search(r"現行(?:の)?環境[^。]{0,40}(?:利用できません|使えません|利用不可)", output))
    approval_request = bool(
        re.search(
            r"田中様[^。]{0,55}(?:"
            r"6月20日まで[^。]{0,25}移行案A|移行案A[^。]{0,25}6月20日まで"
            r")[^。]{0,25}ご?承認[^。]{0,20}(?:お願|ください)",
            output,
        )
    ) and not bool(re.search(r"6月20日(?:以降|より後|を過ぎ)[^。]{0,30}(?:承認|ご承認)", output))
    preapproval_prohibition = bool(
        re.search(r"承認前[^。]{0,25}作業[^。]{0,20}(?:開始|着手)しない(?:でください|よう|こと)?", output)
    ) and not bool(re.search(r"承認前[^。]{0,30}(?:開始|着手)しないわけでは", output))
    required = {
        "missing-meeting-context": meeting_context,
        "missing-current-environment-deadline": environment_available,
        "missing-approval-request": approval_request,
        "missing-preapproval-prohibition": preapproval_prohibition,
    }
    reasons = [name for name, passed in required.items() if not passed]
    if "におかれましては" in output:
        reasons.append("redundant-deferential-frame")
    return reasons


def condition_scope_reasons(output: str) -> list[str]:
    plan = "Proプラン" in output and not bool(re.search(r"Proプラン(?:以外|ではない|でない)", output))
    timely_limiter = bool(
        re.search(
            r"障害発生[^。]{0,20}30日以内[^。]{0,20}申請[^。]{0,15}(?:場合に限|に限|のみ)|"
            r"障害発生[^。]{0,20}30日以内の申請(?:に限|のみ)",
            output,
        )
    )
    restoration = bool(
        re.search(r"バックアップ[^。]{0,30}復元[^。]{0,15}(?:できます|可能|することができます)", output)
    ) and not bool(re.search(r"バックアップ[^。]{0,30}復元[^。]{0,10}(?:できません|不可能)", output))
    duration = bool(
        re.search(r"(?:最大|最長)72時間[^。]{0,25}(?:かかる|要する)[^。]{0,20}(?:可能性|ことがあります|場合があります)", output)
        or re.search(r"(?:かかる|要する)[^。]{0,20}(?:可能性|ことがあります)[^。]{0,20}(?:最大|最長)72時間", output)
    ) and not bool(re.search(r"(?:最大|最長)72時間[^。]{0,20}(?:かからない|要しない)", output))
    required = {
        "missing-pro-plan": plan,
        "limiter-moved-from-filing-condition": timely_limiter,
        "missing-restoration": restoration,
        "missing-uncertain-72-hour-duration": duration,
    }
    return [name for name, passed in required.items() if not passed]


def terminology_style_reasons(output: str) -> list[str]:
    sentences = [part for part in re.findall(r"[^。]+。", output) if part.strip()]
    create_action = bool(re.search(r"共有スペース[^。]{0,20}作成(?:します|してください)", output)) and not bool(
        re.search(r"共有スペース[^。]{0,20}作成しない", output)
    )
    add_member_action = bool(
        re.search(r"共有スペース[^。]{0,25}メンバー[^。]{0,15}追加(?:します|してください)", output)
    ) and not bool(re.search(r"メンバー[^。]{0,15}追加しない", output))
    external_user_prohibition = bool(
        re.search(r"共有スペース[^。]{0,25}外部ユーザー[^。]{0,20}招待でき(?:ません|ない)", output)
    ) and not bool(re.search(r"招待できないわけでは(?:ありません|ない)", output))
    required = {
        "wrong-sentence-count": len(sentences) == 3,
        "missing-preferred-term": output.count("共有スペース") >= 3,
        "missing-create-action": create_action,
        "missing-add-member-action": add_member_action,
        "missing-external-user-prohibition": external_user_prohibition,
    }
    reasons = [name for name, passed in required.items() if not passed]
    quoted_mentions = len(re.findall(r"「共有スペース」", output))
    first_term = output.find("共有スペース")
    first_term_is_quoted = (
        first_term > 0
        and output[first_term - 1] == "「"
        and output[first_term + len("共有スペース"):first_term + len("共有スペース") + 1] == "」"
    )
    if not first_term_is_quoted:
        reasons.append("missing-initial-term-quote")
    if quoted_mentions > 1:
        reasons.append("repeated-term-quotes")
    if "共同エリア" in output or "ワークスペース" in output:
        reasons.append("terminology-drift")
    return reasons


def status_certainty_reasons(output: str) -> list[str]:
    investigation = bool(re.search(r"決済処理[^。]{0,20}遅延[^。]{0,20}調査|調査[^。]{0,20}決済処理[^。]{0,20}遅延", output)) and not bool(
        re.search(r"(?:調査して|調査をして|調査はして)(?:いません|おりません)", output)
    )
    uncertain_cause = bool(re.search(r"ネットワーク障害[^。]{0,20}可能性", output)) and not bool(
        re.search(r"ネットワーク障害[^。]{0,20}可能性(?:は|が)?(?:ありません|ない)", output)
    ) and bool(
        re.search(r"原因[^。]{0,15}(?:未確定|確定して(?:いません|おりません)|特定(?:できて|されて)(?:いません|おりません)|確認できて(?:いません|おりません))", output)
    )
    uncertain_impact = bool(re.search(r"(?:約)?12[%％][^。]{0,25}影響[^。]{0,20}可能性|影響[^。]{0,20}可能性[^。]{0,15}(?:約)?12[%％]", output)) and not bool(
        re.search(r"12[%％](?:ではなく|でなく)|21[%％]|影響(?:して|が生じて|が及んで)(?:いない|おりません)[^。]{0,10}可能性", output)
    )
    fixed_update = bool(
        re.search(
            r"次回(?:の更新|更新)?(?:は)?[^。]{0,12}18時(?:です|となります|に[^。]{0,15}(?:更新|お知らせ)[^。]{0,8}(?:ます|いたします))",
            output,
        )
    ) and not bool(
        re.search(
            r"次回[^。]{0,25}(?:予定|暫定|見込み|目安|可能性)[^。]{0,15}18時|"
            r"次回[^。]{0,15}18時[^。]{0,15}(?:予定|暫定|見込み|目安|可能性)|"
            r"18時[^。]{0,12}(?:予定|暫定|見込み|目安)",
            output,
        )
    )
    required = {
        "missing-delay-investigation": investigation,
        "missing-uncertain-cause": uncertain_cause,
        "missing-uncertain-impact": uncertain_impact,
        "fixed-update-time-weakened": fixed_update,
    }
    return [name for name, passed in required.items() if not passed]


CHECKERS: dict[str, Callable[[str], list[str]]] = {
    "business": business_request_reasons,
    "condition": condition_scope_reasons,
    "terminology": terminology_style_reasons,
    "status": status_certainty_reasons,
}


def run_once(scenario: str, repeat: int, model: str) -> tuple[str, int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-japanese-preference-") as tmp:
        root = Path(tmp)
        session_root = root / "pi"
        skill, _ = _materialize_skill("worktree", session_root / "work")
        instructions = root / "instructions.md"
        instructions.write_text(
            "Apply the following writing skill silently to the user's task. "
            "Its relative references are available in the working directory.\n\n"
            + skill.read_text()
        )
        trace = execute_pi(
            prompt=SCENARIOS[scenario], model=model, session_root=session_root, appended_instructions=instructions
        )
        saved_trace = root / "trace.jsonl"
        shutil.copy2(trace, saved_trace)
        output = observe_trace(saved_trace, Path("/__regression__/SKILL.md")).final_output
    return scenario, repeat, output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--scenario", choices=["all", *SCENARIOS], default="all")
    args = parser.parse_args()
    names = list(SCENARIOS) if args.scenario == "all" else [args.scenario]
    if args.repeats < 1:
        raise ValueError("--repeats must be positive")

    rows: list[tuple[str, int, str]] = []
    with ThreadPoolExecutor(max_workers=len(names) * args.repeats) as executor:
        futures = [
            executor.submit(run_once, name, repeat, args.model)
            for name in names
            for repeat in range(1, args.repeats + 1)
        ]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for name, repeat, output in sorted(rows):
        reasons = CHECKERS[name](output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{name} {repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"Japanese preference regressions: {regressions}/{len(rows)}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
