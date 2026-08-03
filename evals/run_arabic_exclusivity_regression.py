#!/usr/bin/env python3
"""Run the live regression for Arabic plan-exclusivity preservation."""
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

PROMPT = """أعد كتابة SOURCE بحيث تكون الشروط بجوار الادعاء الذي تقيده. أعد النص العربي الواضح فقط. لا تحوّل الاحتمال إلى يقين. SOURCE: يمكن استعادة الملفات المحذوفة. ينطبق ذلك فقط على خطة Pro إذا قُدِّم الطلب خلال 14 يومًا. قد تستغرق الاستعادة حتى 24 ساعة."""


def exclusivity_reasons(output: str) -> list[str]:
    """Return deterministic failures for the frozen Arabic condition scenario."""
    text = " ".join(output.split())
    sentences = [part.strip() for part in re.split(r"[.؟!]", text) if part.strip()]
    restoration_phrase = r"استعادة[^.؟!]{0,25}الملفات المحذوفة"
    restoration = any(
        (
            re.search(r"(?:يمكن[^.؟!]{0,20}|تتوفر\s+|إمكانية\s+|تقتصر\s+)" + restoration_phrase, sentence)
            or re.search(r"لا\s+(?:يمكن[^.؟!]{0,20}|تتوفر\s+)" + restoration_phrase + r"[^.؟!]{0,30}إلا", sentence)
        )
        and not re.search(r"لا\s+(?:يمكن[^.؟!]{0,20}|تتوفر\s+)" + restoration_phrase + r"(?![^.؟!]{0,30}إلا)", sentence)
        for sentence in sentences
    )
    exclusive = any(
        re.search(restoration_phrase, sentence)
        and re.search(r"(?:خطة\s+)?Pro", sentence, re.I)
        and (
            re.search(r"(?:فقط[^.؟!]{0,35}(?:خطة\s+)?Pro|(?:خطة\s+)?Pro[^.؟!]{0,12}فقط)", sentence, re.I)
            or re.search(r"لا\s+(?:يمكن|تتوفر)[^.؟!]{0,55}إلا[^.؟!]{0,20}(?:خطة\s+)?Pro", sentence, re.I)
            or re.search(r"تقتصر[^.؟!]{0,45}على\s+(?:خطة\s+)?Pro", sentence, re.I)
        )
        for sentence in sentences
    ) and not bool(
        re.search(
            r"ليس(?:ت)?\s+فقط[^.؟!]{0,30}(?:خطة\s+)?Pro|"
            r"(?:خطة\s+)?Pro[^.؟!]{0,20}(?:وغيرها|وخطط|أو\s+خطة)|"
            r"(?:Enterprise|Basic|خطة\s+أخرى)",
            text,
            re.I,
        )
    )
    submission = r"(?:ق[^\s]{0,6}م\s+الطلب|تقديم\s+الطلب|ي[^\s]{0,6}م\s+الطلب)"
    deadline = any(
        re.search(r"(?:إذا|بشرط)[^.؟!]{0,35}" + submission + r"[^.؟!]{0,20}خلال\s+14\s+يوم", sentence)
        or re.search(r"(?:إذا|بشرط)[^.؟!]{0,20}خلال\s+14\s+يوم[^.؟!]{0,35}" + submission, sentence)
        for sentence in sentences
    ) and not bool(
        re.search(r"(?:إذا|بشرط)[^.؟!]{0,15}(?:لم|لا)[^.؟!]{0,20}" + submission, text)
        or re.search(r"بعد\s+14\s+يوم", text)
    )
    uncertain_duration = any(
        (
            re.search(r"قد[^.؟!]{0,25}تستغرق[^.؟!]{0,20}(?:الاستعادة|عملية\s+الاستعادة|العملية)[^.؟!]{0,20}حتى\s+24\s+ساعة", sentence)
            or re.search(r"قد[^.؟!]{0,15}(?:تصل\s+)?مدة\s+الاستعادة[^.؟!]{0,20}(?:إلى|حتى)\s+24\s+ساعة", sentence)
            or re.search(r"قد[^.؟!]{0,15}(?:تستغرق)\s+(?:الاستعادة|عملية\s+الاستعادة|العملية)\s+حتى\s+24\s+ساعة", sentence)
        )
        and not re.search(r"(?:أكثر\s+من|ما\s+يزيد\s+عن|ستستغرق|بالتأكيد)[^.؟!]{0,15}24\s+ساعة", sentence)
        for sentence in sentences
    )
    required = {
        "missing-restoration-fact": restoration,
        "missing-pro-plan-exclusivity": exclusive,
        "missing-14-day-condition": deadline,
        "missing-uncertain-24-hour-duration": uncertain_duration,
    }
    reasons = [name for name, passed in required.items() if not passed]
    if re.search(
        r"(?:مشتركي|مستخدمي)\s+(?:خطة\s+)?Pro|(?:للمشتركين|للمستخدمين|المشتركين|المستخدمين)\s+في\s+(?:خطة\s+)?Pro",
        text,
        re.I,
    ):
        reasons.append("plan-recast-as-subscribers")
    return reasons


def run_once(repeat: int, model: str) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-arabic-exclusivity-") as tmp:
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
        futures = [executor.submit(run_once, repeat, args.model) for repeat in range(1, args.repeats + 1)]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for repeat, output in sorted(rows):
        reasons = exclusivity_reasons(output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"Arabic exclusivity regressions: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
