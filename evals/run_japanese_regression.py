#!/usr/bin/env python3
"""Run the live regression for Japanese report and attribution preservation."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from evals.evaluation import observe_trace
from evals.run_behavior import _materialize_skill
from evals.run_smoke import execute_pi

PROMPT = """曖昧さをなくし、自然な日本語に書き直してください。

出力条件：曖昧さをなくした自然な日本語だけを返してください。

佐藤さんが鈴木さんに、レビュー後に報告書を送ると伝えました。報告書を送るのは鈴木さんで、佐藤さんは承認を担当します。案件IDはJP-42です。"""

INSTRUCTION_MARKERS = ("送るよう", "送ってください")
SATO_TO_SUZUKI = re.compile(r"佐藤さん(?:は|が)[、 ]*鈴木さんに|佐藤さんから鈴木さんに")
SUZUKI_SENDS = re.compile(r"鈴木さんが[^。]*(?:送る|送り|送付)|送付は鈴木さんが")
SATO_APPROVES = re.compile(r"佐藤さん(?:は|が|による)[^。]*承認|承認(?:は|を)[^。]*佐藤さん")
REVERSED_ATTRIBUTION = re.compile(r"鈴木さん(?:は|が)[、 ]*佐藤さんに")
EXPANDED_REPORTED_CONTENT = re.compile(r"承認[^。]*と[、 ]*佐藤さん.*伝えました|承認[^。]*と伝えました|[「『].*承認.*[」』]と伝えました")


def meaning_change_reasons(output: str) -> list[str]:
    """Return deterministic reasons the rewrite violates this scenario's contract."""
    reasons = []
    required = {
        "missing-case-id": "JP-42" in output,
        "missing-review-timing": bool(re.search(r"レビュー[^。]*後", output)),
        "missing-report": "報告書" in output,
        "missing-reporting-speech-act": "伝えました" in output,
        "missing-sato-to-suzuki-attribution": bool(SATO_TO_SUZUKI.search(output)),
        "missing-suzuki-sends-role": bool(SUZUKI_SENDS.search(output)),
        "missing-sato-approves-role": bool(SATO_APPROVES.search(output)),
    }
    reasons.extend(name for name, passed in required.items() if not passed)
    if any(marker in output for marker in INSTRUCTION_MARKERS):
        reasons.append("report-became-instruction")
    if "承認後に" in output:
        reasons.append("invented-approval-order")
    if REVERSED_ATTRIBUTION.search(output):
        reasons.append("reversed-speaker-addressee")
    if EXPANDED_REPORTED_CONTENT.search(output):
        reasons.append("expanded-attributed-content")
    return reasons


def has_meaning_change(output: str) -> bool:
    return bool(meaning_change_reasons(output))


def run_once(repeat: int, model: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-ja-regression-") as tmp:
        root = Path(tmp)
        session_root = root / "pi"
        skill, _ = _materialize_skill("worktree", session_root / "work")
        instructions = root / "instructions.md"
        instructions.write_text(
            "Apply the following writing skill silently to the user's task. "
            "Its relative references are available in the working directory.\n\n"
            + skill.read_text()
        )
        live_trace = execute_pi(
            prompt=PROMPT,
            model=model,
            session_root=session_root,
            appended_instructions=instructions,
        )
        saved_trace = root / "trace.jsonl"
        shutil.copy2(live_trace, saved_trace)
        output = observe_trace(saved_trace, Path("/__regression__/SKILL.md")).final_output
    return repeat, output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="openai-codex/gpt-5.6-sol")
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if args.repeats < 1:
        raise ValueError("--repeats must be positive")

    rows: list[tuple[int, str]] = []
    with ThreadPoolExecutor(max_workers=args.repeats) as executor:
        futures = [
            executor.submit(run_once, repeat, args.model)
            for repeat in range(1, args.repeats + 1)
        ]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for repeat, output in sorted(rows):
        reasons = meaning_change_reasons(output)
        failed = bool(reasons)
        regressions += failed
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if failed else 'preserved'}{suffix}: {output}")
    print(f"meaning-change regressions: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
