#!/usr/bin/env python3
"""Run the live regression for relative timing and tense preservation."""
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

PROMPT = """Rewrite the SOURCE to remove the ambiguous referent without inventing facts. Return only the clarified text in two professional English sentences. Preserve identifiers, timing, and access distinctions. SOURCE: Maya told Priya that her access to ACCT-74 would end Friday. Priya must export the audit log before then; Maya retains access."""


def _sentences(text: str) -> list[str]:
    return [part.strip() for part in re.findall(r"[^.!?]+[.!?](?:\s|$)", text)]


def temporal_reasons(output: str) -> list[str]:
    """Return deterministic failures for the frozen ambiguous-referent scenario."""
    text = " ".join(output.split())
    sentences = _sentences(text)

    attribution = bool(re.search(r"\bMaya\s+(?:told|informed)\s+Priya\b", text, re.I)) and not bool(
        re.search(r"\bPriya\s+(?:told|informed)\s+Maya\b", text, re.I)
    )

    priya_access_ends = False
    for sentence in sentences:
        positive = bool(
            re.search(
                r"Priya(?:'s|’s) access[^.!?]{0,35}(?:end|expire)[^.!?]{0,18}Friday|"
                r"Priya[^.!?]{0,20}(?:lose|loses|lost)[^.!?]{0,15}access[^.!?]{0,18}Friday",
                sentence,
                re.I,
            )
        )
        negated = bool(
            re.search(
                r"Priya[^.!?]{0,45}\b(?:not|never|won't)\b[^.!?]{0,25}(?:end|expire|lose)|"
                r"Priya[^.!?]{0,35}(?:end|expire|lose)[^.!?]{0,12}\bnot\b",
                sentence,
                re.I,
            )
        )
        priya_access_ends |= positive and not negated

    export_duty = r"\bPriya\b[^.!?]{0,30}\bmust\s+export\s+the audit log\b"
    export_sentences = [
        sentence
        for sentence in sentences
        if re.search(export_duty, sentence, re.I)
        and not re.search(r"\bPriya\b[^.!?]{0,30}\bmust\s+not\s+export\b", sentence, re.I)
    ]
    relative = (
        r"(?:before then|(?:before|prior to)\s+(?:(?:her|Priya(?:'s|’s))\s+access\s+"
        r"(?:ends|expires)|Priya\s+losing\s+access|(?:losing|ending|expiring)\s+access)|"
        r"before (?:that|this) happens)"
    )
    relative_deadline = any(
        re.search(export_duty + r"[^.!?]{0,35}" + relative, sentence, re.I)
        or re.search(relative + r"[^.!?]{0,35}" + export_duty, sentence, re.I)
        for sentence in export_sentences
    )
    calendar_boundary = any(
        re.search(export_duty + r"[^.!?]{0,25}\bbefore Friday\b", sentence, re.I)
        or re.search(r"\bbefore Friday\b[^.!?]{0,25}" + export_duty, sentence, re.I)
        for sentence in export_sentences
    )

    maya_current_access = False
    for sentence in sentences:
        positive = bool(
            re.search(
                r"\bMaya\s+(?:(?:currently|still)\s+)?(?:retains|has|keeps) access\b|"
                r"\bMaya\s+continues to\s+(?:retain|have) access\b|"
                r"\bMaya(?:'s|’s) access\s+(?:continues|remains active)\b",
                sentence,
                re.I,
            )
        )
        changed = bool(
            re.search(
                r"\bMaya\b[^.!?]{0,25}\b(?:would|will|did|does not|no longer|won't)\b[^.!?]{0,25}access|"
                r"\bMaya\b[^.!?]{0,35}access[^.!?]{0,20}\b(?:after|starting|beginning|from)\b",
                sentence,
                re.I,
            )
        )
        maya_current_access |= positive and not changed

    required = {
        "wrong-sentence-count": len(sentences) == 2,
        "missing-account-id": "ACCT-74" in text,
        "missing-maya-to-priya-attribution": attribution,
        "missing-priya-access-ending": priya_access_ends,
        "missing-priya-export-duty": bool(export_sentences),
        "missing-relative-deadline": relative_deadline,
        "maya-access-tense-changed": maya_current_access,
    }
    reasons = [name for name, passed in required.items() if not passed]
    if calendar_boundary:
        reasons.append("relative-deadline-became-calendar-boundary")
    return reasons


def minimal_wording_reasons(output: str) -> list[str]:
    """Add the frozen preference for leaving an already-clear relative reference unchanged."""
    reasons = temporal_reasons(output)
    if not re.search(r"\bbefore then\b", output, re.I):
        reasons.append("unnecessary-relative-reference-expansion")
    return reasons


def run_once(repeat: int, model: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-temporal-regression-") as tmp:
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
    parser.add_argument("--minimal-wording", action="store_true")
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
        reasons = minimal_wording_reasons(output) if args.minimal_wording else temporal_reasons(output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"temporal regressions: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
