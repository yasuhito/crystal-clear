#!/usr/bin/env python3
"""Run the live regression for Chinese role and ordering preservation."""
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

PROMPT = """改写 SOURCE，明确每个人的职责，不要添加事实。只返回消除指代歧义后的简体中文文本。保留编号、期限和必须条件。SOURCE: 李敏告诉王伟，她将在审核后关闭工单 CN-88。关闭工单的人是王伟；李敏负责最终确认。必须在周五之前完成。"""
MINIMAL_PROMPT = """改写 SOURCE，消除指代歧义，但不要补充未说明的角色或顺序。只返回改写后的简体中文。SOURCE: 李敏告诉王伟，她将在审核后关闭工单。关闭工单的人是王伟；李敏负责最终确认。"""


def role_and_order_change_reasons(output: str, *, require_ticket: bool) -> list[str]:
    text = "".join(output.split())
    ticket = "CN-88" if require_ticket else ""
    close = rf"关闭工单{ticket}"
    wang_closes = bool(
        re.search(rf"(?:^|[，,。；;：“”])(?:\d+[.、])?王伟[^，,。；;]{{0,24}}{close}", text)
        or re.search(rf"(?:审核(?:完成|通过)?后|经审核(?:通过)?后)[，,]?[^，,。；;]{{0,12}}(?:由)?王伟[^，,。；;]{{0,12}}{close}", text)
    )
    review_before_close = bool(
        re.search(rf"(?:审核(?:完成|通过)?后|经审核(?:通过)?后)[^。；;]{{0,30}}{close}", text)
        or re.search(rf"{close}[^。；;]{{0,20}}(?:须|要)在审核后", text)
    )
    reasons: list[str] = []
    if not wang_closes:
        reasons.append("missing-wang-closes-ticket")
    if not review_before_close:
        reasons.append("missing-review-before-close")
    if re.search(rf"(?:^|[，,。；;：“”])李敏[^，,。；;：“”]{{0,20}}{close}|由李敏[^，,。；;：“”]{{0,12}}{close}|李敏(?:告诉|告知|通知)王伟[：:]?[“\"]我[^”\"]{{0,20}}{close}", text):
        reasons.append("li-replaced-wang-as-closer")
    if re.search(
        r"审核人(?:是|为)(?!未|没有)[^，,。；;]{1,10}|"
        r"(?:由|让)[^，,。；;]{1,10}(?:负责|进行|执行)?(?:审核|审查)|"
        r"[^，,。；;]{1,8}(?:负责|进行|执行)(?:审核|审查)(?!结果)|"
        r"(?:李敏|王伟|审核团队|评审团队|团队)(?:审核|审查)(?:后|了|工单)",
        text,
    ):
        reasons.append("invented-reviewer-role")
    ordering_patterns = (
        r"只有李敏[^。；;]{0,20}最终确认[^。；;]{0,25}王伟[^。；;]{0,12}才[^。；;]{0,12}关闭",
        r"(?:待|经)李敏[^。；;]{0,20}最终确认(?:后|方可|才能)[^。；;]{0,30}关闭",
        r"王伟[^。；;]{0,20}(?:待|经|在)李敏[^。；;]{0,20}最终确认(?:后|方可|才能)?[^。；;]{0,15}关闭",
        r"李敏[^。；;]{0,15}最终确认后[^。；;]{0,30}王伟[^。；;]{0,15}关闭",
        r"(?:关闭[^。；;]{0,20}前提是|最终确认[^。；;]{0,15}是[^。；;]{0,15}关闭[^。；;]{0,10}前提)[^。；;]*李敏?",
    )
    if any(re.search(pattern, text) for pattern in ordering_patterns):
        reasons.append("invented-final-confirmation-order")
    return reasons


def _has_shared_friday_deadline(text: str) -> bool:
    completion = r"(?<!未)完成|办结"
    obligation = (
        r"(?:(?:必须|须|务必|需)(?:在)?周五(?:之前|前)[^。；;]{0,15}(?:" + completion + r")|"
        r"周五(?:之前|前)[^。；;]{0,10}(?:必须|须|务必|需)[^。；;]{0,10}(?:" + completion + r"))"
    )
    negated = bool(
        re.search(
            r"(?:不必|无需|不需要|不一定|未必)[^。；;]{0,18}(?:必须|须|务必|需)?[^。；;]{0,12}周五(?:之前|前)|"
            r"周五(?:之前|前)[^。；;]{0,18}(?:不必|无需|不需要|不一定|未必)|"
            r"并非[^。；;]{0,8}必须[^。；;]{0,12}周五(?:之前|前)|"
            r"周五(?:之前|前)[^。；;]{0,12}不得[^。；;]{0,12}(?:完成|办结)|"
            r"周五(?:之前|前)[^。；;]{0,15}(?:保持)?未完成",
            text,
        )
    )
    contradictory = bool(
        re.search(
            r"(?:关闭工单|最终确认)[^。；;]{0,20}(?:改为|延至|推迟到|可在)[^。；;]{0,12}"
            r"(?:下周一|周一|周末|周五之后|周五后)",
            text,
        )
    )
    if negated or contradictory:
        return False
    broad_prefix = (
        r"(?:(?:(?:上述|以上|这)(?:两项)?(?:事项|工作|任务)|"
        r"(?:所有|全部|相关)(?:事项|工作|任务)|(?:二者|两者))(?:均|都)?|(?:均|都))?"
    )
    coordinated = r"(?:关闭工单(?:和|及|与)最终确认|最终确认(?:和|及|与)关闭工单)(?:均|都)?"
    for sentence in re.split(r"[。；;]", text):
        sentence = re.sub(r"^\d+[.、)]", "", sentence)
        if not sentence:
            continue
        broad_subject = re.fullmatch(broad_prefix + obligation, sentence)
        explicit_both = re.search(coordinated + r"[^。；;]{0,6}" + obligation, sentence)
        if broad_subject or explicit_both:
            return True
    return False


def role_change_reasons(output: str) -> list[str]:
    """Return deterministic failures for the frozen Chinese role scenario."""
    text = "".join(output.split())
    reasons = role_and_order_change_reasons(output, require_ticket=True)
    required = {
        "missing-li-tells-wang": bool(re.search(r"李敏[^。；;]{0,20}(?:告诉|告知|通知)[^。；;]{0,10}王伟", text)),
        "missing-li-final-confirmation": bool(re.search(r"李敏[^。；;]{0,25}(?:负责)?最终确认|最终确认[^。；;]{0,15}由李敏负责", text)),
        "missing-shared-friday-must-condition": _has_shared_friday_deadline(text),
    }
    reasons.extend(name for name, passed in required.items() if not passed)
    return reasons


def minimal_role_change_reasons(output: str) -> list[str]:
    return role_and_order_change_reasons(output, require_ticket=False)


def run_once(repeat: int, model: str, *, minimal: bool) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="crystal-clear-chinese-role-regression-") as tmp:
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
            prompt=MINIMAL_PROMPT if minimal else PROMPT,
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
    parser.add_argument("--minimal", action="store_true")
    args = parser.parse_args()
    if args.repeats < 1:
        raise ValueError("--repeats must be positive")

    rows: list[tuple[int, str]] = []
    with ThreadPoolExecutor(max_workers=args.repeats) as executor:
        futures = [
            executor.submit(run_once, repeat, args.model, minimal=args.minimal)
            for repeat in range(1, args.repeats + 1)
        ]
        rows.extend(future.result() for future in as_completed(futures))

    regressions = 0
    for repeat, output in sorted(rows):
        reasons = minimal_role_change_reasons(output) if args.minimal else role_change_reasons(output)
        regressions += bool(reasons)
        suffix = f" ({', '.join(reasons)})" if reasons else ""
        print(f"[{repeat}] {'REGRESSION' if reasons else 'preserved'}{suffix}: {output}")
    print(f"Chinese role regressions: {regressions}/{args.repeats}")
    if regressions:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
