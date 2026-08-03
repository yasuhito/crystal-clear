#!/usr/bin/env python3
"""Run the live regression for meta-instruction/content separation."""
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

PROMPT = """Rewrite the SOURCE using one consistent product term. Return only the revised three-sentence help text in English. Preserve the limitation. SOURCE: Enable Secure Review in Settings. The protected review feature checks new uploads, but this scanner does not inspect existing files. Keep the product term Secure Review throughout."""

TEAM_SYNC_PROMPT = """SOURCEを用語と条件が明確になるように書き直してください。日本語の説明文だけを返し、英語の製品名は変更しないでください。対象外の条件を保持してください。SOURCE: 管理者はTeam Syncを有効にしてください。この同期機能は新規メンバーを同期します。既存メンバーは対象外です。UI上の名称はTeam Syncのままにしてください。"""


def instruction_leak_reasons(output: str) -> list[str]:
    """Return deterministic failures for the frozen terminology scenario."""
    text = " ".join(output.split())
    sentence_count = len(re.findall(r"[^.!?]+[.!?](?:\s|$)", text))
    enable_action = bool(
        re.search(r"\benable\s+Secure Review\s+in\s+Settings\b", text, re.I)
        or re.search(r"\bopen\s+Settings[.!?]\s+Enable\s+Secure Review\b", text, re.I)
    ) and not bool(
        re.search(
            r"\b(?:do not|don't|never)\s+(?:open\s+Settings|enable\s+Secure Review)|"
            r"\bdisable\s+Secure Review\b",
            text,
            re.I,
        )
    )
    new_upload_scope = bool(
        re.search(r"Secure Review[^.!?]{0,25}\bchecks?\b[^.!?]{0,20}\bnew uploads\b", text, re.I)
    ) and not bool(re.search(r"\b(?:not|does not|doesn't)\b[^.!?]{0,20}\bnew uploads\b", text, re.I))
    existing_file_limitation = bool(
        re.search(r"\bdoes not inspect existing files\b", text, re.I)
    ) and not bool(
        re.search(
            r"\bchecks?\s+existing files\b|(?<!not )\binspects?\s+existing files\b|"
            r"\bchecks?\s+new uploads\s+(?:and|as well as)\s+existing files\b",
            text,
            re.I,
        )
    )
    required = {
        "wrong-sentence-count": sentence_count == 3,
        "missing-enable-action": enable_action,
        "missing-new-upload-scope": new_upload_scope,
        "missing-existing-file-limitation": existing_file_limitation,
    }
    reasons = [name for name, passed in required.items() if not passed]
    if re.search(
        r"\b(?:keep|leave|ensure)\b[^.!?]{0,25}\bSecure Review\b[^.!?]{0,25}\b(?:enabled|remain enabled|stays? enabled)\b|"
        r"\bSecure Review\b[^.!?]{0,25}\b(?:must|should)\s+(?:remain|stay|be kept)\s+enabled\b|"
        r"\bkeep\s+the\s+product\s+term\s+Secure Review\s+throughout\b",
        text,
        re.I,
    ):
        reasons.append("terminology-instruction-became-product-instruction")
    return reasons


def ui_name_constraint_reasons(output: str) -> list[str]:
    """Return deterministic failures for the frozen mixed-Japanese UI-name scenario."""
    text = " ".join(output.split())
    enable_action = bool(re.search(r"Team Sync[^。.!?]{0,20}(?:有効|オン)", text, re.I)) and not bool(
        re.search(
            r"Team Sync[^。.!?]{0,20}(?:無効|オフ|オン(?:に)?しない|有効(?:化)?に?しない|有効(?:化)?しません)",
            text,
            re.I,
        )
    )
    new_member_scope = bool(
        re.search(r"新規メンバー[^。.!?]{0,30}同期|同期[^。.!?]{0,30}新規メンバー", text)
    ) and not bool(
        re.search(
            r"新規メンバー[^、,。.!?]{0,20}(?:対象外|同期しない|同期しません|同期されない|同期されません|同期対象にしない|同期対象にしません)",
            text,
        )
    )
    existing_member_exclusion = bool(
        re.search(r"既存メンバー[^。.!?]{0,25}(?:対象外|同期しない|同期されない)", text)
    ) and not bool(
        re.search(
            r"既存メンバー[^。.!?]{0,25}(?:対象外では(?:ありません|ない)|対象外にしない|対象外にしません|同期する|同期します|同期されます)",
            text,
        )
    )
    ui_name_constraint = any(
        re.search(r"UI|ユーザーインターフェース", sentence, re.I)
        and re.search(r"Team Sync", sentence, re.I)
        and re.search(r"まま|変更しない|変えない|維持|使用", sentence)
        and not re.search(
            r"(?:使用|維持)しない|(?:使用|維持)しません|変更しても|変更でき|変えても|"
            r"(?:名称|名前)では(?:ありません|ない)",
            sentence,
        )
        for sentence in re.split(r"[。.!?]", text)
    )
    required = {
        "missing-enable-action": enable_action,
        "missing-new-member-scope": new_member_scope,
        "missing-existing-member-exclusion": existing_member_exclusion,
        "missing-ui-name-constraint": ui_name_constraint,
    }
    return [name for name, passed in required.items() if not passed]


def run_once(repeat: int, model: str, prompt: str = PROMPT) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-terminology-regression-") as tmp:
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
            prompt=prompt,
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
    parser.add_argument("--team-sync", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1:
        raise ValueError("--repeats must be positive")

    rows: list[tuple[int, str]] = []
    with ThreadPoolExecutor(max_workers=args.repeats) as executor:
        futures = [
            executor.submit(
                run_once,
                repeat,
                args.model,
                TEAM_SYNC_PROMPT if args.team_sync else PROMPT,
            )
            for repeat in range(1, args.repeats + 1)
        ]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for repeat, output in sorted(rows):
        reasons = ui_name_constraint_reasons(output) if args.team_sync else instruction_leak_reasons(output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    label = "UI-name regressions" if args.team_sync else "instruction-leak regressions"
    print(f"{label}: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
