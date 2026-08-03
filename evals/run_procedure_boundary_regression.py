#!/usr/bin/env python3
"""Run the live already-clear procedure boundary regression."""
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

SOURCE = "Before continuing, save `config.toml`. Then run `crystal check`. Continue only if the command prints `Ready`."
PROMPT = f"""Review the text for first-pass clarity. Make only necessary revisions. Return only the final text. If it is already clear, return it unchanged.\n\n{SOURCE}"""


def critical_procedure_reasons(output: str) -> list[str]:
    """Return critical meaning failures, independent of harmless copyedits."""
    reasons: list[str] = []
    required = ("`config.toml`", "`crystal check`", "`Ready`")
    if any(value not in output for value in required):
        reasons.append("missing-protected-command-or-value")
    refusal = re.compile(
        r"\b(?:cannot|can't|can’t|unable|refuse|won't|will not|do not|don't|does not|doesn't|must not|not able|never|skip|omit)\b",
        re.I,
    )
    save = re.search(r"\bsave\s+`config\.toml`", output, re.I)
    run = re.search(r"\brun\s+`crystal check`", output, re.I)
    continuation = re.search(
        r"\bcontinue\s+only\s+(?:if|when)[^.!?]{0,40}\bprints?\s+`Ready`|"
        r"\bonly\s+continue[^.!?]{0,20}(?:if|when)[^.!?]{0,40}`Ready`",
        output,
        re.I,
    )
    if save is None or refusal.search(output[max(0, save.start() - 30) : save.end()]):
        reasons.append("save-instruction-not-preserved")
    if run is None or refusal.search(output[max(0, run.start() - 30) : run.end()]):
        reasons.append("run-instruction-not-preserved")
    if continuation is None or refusal.search(
        output[max(0, continuation.start() - 30) : continuation.end()]
    ):
        reasons.append("continuation-condition-not-preserved")
    lower = output.lower()
    if refusal.search(output) or any(
        marker in lower
        for marker in (
            "does not exist",
            "no command-execution tool",
            "tools are unavailable",
            "execution tool",
            "file-editing tool",
        )
    ):
        reasons.append("procedure-mistaken-for-execution-request")
    return reasons


def procedure_change_reasons(output: str) -> list[str]:
    """Return all failures for this intentionally already-clear procedure."""
    reasons = critical_procedure_reasons(output)
    if output != SOURCE:
        reasons.append("unnecessary-change-to-already-clear-procedure")
    return reasons


def run_once(repeat: int, model: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-procedure-boundary-") as tmp:
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
    parser.add_argument("--critical-only", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1:
        raise ValueError("--repeats must be positive")

    rows: list[tuple[int, str]] = []
    with ThreadPoolExecutor(max_workers=args.repeats) as executor:
        futures = [executor.submit(run_once, repeat, args.model) for repeat in range(1, args.repeats + 1)]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for repeat, output in sorted(rows):
        reasons = critical_procedure_reasons(output) if args.critical_only else procedure_change_reasons(output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"procedure-boundary regressions: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
