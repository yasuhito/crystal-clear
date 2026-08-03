#!/usr/bin/env python3
"""Run a focused live regression for recommendation modality preservation."""
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

PROMPT = """Rewrite the SOURCE for first-pass understanding. Return only one concise decision memo paragraph in professional English. Preserve every fact, condition, constraint, number, and protected string exactly in meaning. SOURCE: The migration has been discussed for several weeks. The legacy exporter remains available. After reviewing the risks, we recommend approving Project Northstar by 14 June. The rollout must not begin before security signs off."""


def modality_change_reasons(output: str) -> list[str]:
    """Return deterministic failures for the frozen recommendation scenario."""
    text = " ".join(output.split())
    lower = text.lower()
    negation = re.compile(
        r"\b(?:no|not|never|cannot|can't|dont|don't|doesn't|didn't|hasn't|hadn't|won't|wouldn't|shouldn't|couldn't)\b",
        re.I,
    )

    def positive_match(pattern: str, *, radius: int = 35) -> bool:
        match = re.search(pattern, text, re.I)
        if match is None:
            return False
        window = text[max(0, match.start() - radius) : match.end()]
        return negation.search(window) is None

    recommendation = positive_match(
        r"\b(?:recommend(?:ed|ing)?(?:\s+that\s+\w+)?\s+(?:the\s+)?approv(?:e|al|ing)|"
        r"recommendation\s+(?:is\s+)?(?:to\s+)?approv(?:e|al)|"
        r"advice\s+is\s+to\s+approv(?:e|al)|"
        r"propos(?:e|al\s+is\s+to)\s+(?:the\s+)?approv(?:e|al))\b"
    )
    discussion_preserved = "several weeks" in lower and positive_match(
        r"\b(?:discuss(?:ed|ion)|under discussion)\b"
    )
    risk_review_preserved = positive_match(
        r"\brisk review\b|\breview(?:ed|ing)?\s+(?:the\s+)?risks?\b|\brisks?\s+(?:were\s+)?reviewed\b"
    )
    exporter_available = bool(
        re.search(r"legacy exporter[^.!?]{0,35}\b(?:remains?|is|will be|stays?)\b[^.!?]{0,20}\bavailable\b", text, re.I)
        or re.search(r"\bavailable\b[^.!?]{0,35}\blegacy exporter\b", text, re.I)
    ) and not bool(
        re.search(r"\b(?:no|not an?)\s+legacy exporter\b|legacy exporter[^.!?]{0,35}\b(?:unavailable|not available|no longer available)\b", text, re.I)
    )
    positive_security_signoff = bool(
        re.search(r"security\s+signs? off|security(?:'s)?\s+approval|approval\s+from\s+security", text, re.I)
    ) and not bool(
        re.search(r"security[^.!?]{0,20}(?:refuses?|declines?|fails?|does not|doesn't|must not|cannot|can't)[^.!?]{0,15}(?:sign off|approv)", text, re.I)
    )
    security_condition = positive_security_signoff and bool(
        re.search(
            r"(?:rollout[^.!?]{0,45}(?:must not|cannot|can't)[^.!?]{0,25}(?:before|until)[^.!?]{0,35}(?:security|approval)|"
            r"(?:do not|don't)[^.!?]{0,20}(?:begin|start)[^.!?]{0,20}rollout[^.!?]{0,20}until[^.!?]{0,35}(?:security|approval)|"
            r"rollout[^.!?]{0,35}(?:may|can)[^.!?]{0,15}(?:begin|start)[^.!?]{0,15}only after[^.!?]{0,35}(?:security|approval))",
            text,
            re.I,
        )
    )
    required = {
        "missing-positive-approval-recommendation": recommendation,
        "missing-project": "Project Northstar" in text,
        "missing-deadline": "14 June" in text,
        "missing-discussion-duration": discussion_preserved,
        "missing-risk-review": risk_review_preserved,
        "legacy-exporter-not-available": exporter_available,
        "missing-rollout-security-condition": security_condition,
    }
    reasons = [name for name, passed in required.items() if not passed]
    if re.search(r"(?:^|[.!?]\s+)(?:Decision:\s*)?Approve\b", text, re.I):
        reasons.append("recommendation-became-directive")
    return reasons


def run_once(repeat: int, model: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-semantic-regression-") as tmp:
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
        reasons = modality_change_reasons(output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"modality regressions: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
