# Use-case recipes

Use this reference only when a substantial task needs genre-specific structure. Read only the matching recipe. The preservation gate, task-mode contract, target-language profile, and Crystal pass in `SKILL.md` still apply.

The sequences below are defaults, not reasons to invent missing content. Omit an unavailable element or label it as unknown when the genre requires that distinction.

## Direct answers

Default sequence: **answer → reason → limits → next action**.

- State the answer in the first useful sentence. If the answer depends on a condition, state the condition with it.
- Add only the reasoning needed to trust or use the answer.
- Name material limits, uncertainty, or exceptions before an action that depends on them.
- End with a next action only when the reader needs one.
- For a simple question, use the core alone; do not load this recipe merely to produce a short answer.

## Documentation and procedures

Default sequence: **purpose or result → prerequisites → ordered actions → expected result**.

- Tell readers what they will accomplish before giving setup details.
- Separate prerequisites from actions. Put warnings before the step that creates the risk.
- Give each action an observable result when verification matters.
- Keep commands, code, paths, identifiers, placeholders, and meaningful formatting exact unless the user asks to edit them.
- Do not turn an optional step into a requirement or silently fill in a missing prerequisite.

## Errors and support

Default sequence: **what happened → effect or known cause → recovery action**.

- Name the failed operation in user terms; include an error identifier when it helps support or diagnosis.
- Distinguish a known cause from a possible cause. Do not present diagnostic guesses as facts.
- Give the safest specific recovery action available. Say when retrying is unsafe or support is required.
- Remove apologies and filler only when they do not carry the requested tone or relationship.

## Incidents and status updates

Default sequence: **time and measured impact → cause and current status → next update**.

- Put the timestamp, affected system or users, and measured impact together.
- Separate confirmed cause, working hypothesis, mitigation, and unknowns.
- Preserve approximations and uncertainty markers such as “about,” “may,” and “not confirmed.”
- State the next-update time or trigger when one is known; do not invent an estimate.
- Keep the tone calm and factual. Do not minimize impact or imply resolution before confirmation.

## Proposals and decision memos

Default sequence: **recommendation → reasons → trade-offs → decision needed**.

- Make the recommendation and requested decision visible before background.
- Use reasons that bear directly on the decision. Separate evidence from inference.
- Expose material costs, risks, alternatives, and reversible versus irreversible consequences.
- Preserve approval gates, deadlines, dissent, and unresolved questions.
- If no recommendation was requested, present options neutrally rather than manufacturing one.

## Emails and requests

Default sequence: **requested action → owner and deadline → necessary context**.

- After any subject line or brief salutation, make the request explicit.
- Name the owner when ambiguity is possible. Attach the deadline and conditions to the action.
- Include only context the recipient needs to act or decide.
- Keep politeness appropriate to the relationship without burying the request.
- Do not create a deadline, commitment, or authority that the source does not provide.

## Japanese business prose

Default sequence: **結論・依頼 → 担当者・期限・条件 → 必要な背景**.

- 件名や短い挨拶の後に、結論または依頼を置く。
- 主語は、担当者や責任の所在が曖昧になる場合だけ明示する。英語にならって毎文の主語を補わない。
- 「です・ます」と「だ・である」を目的に合わせて統一する。
- 敬意を保ちつつ、重複する挨拶、過剰なクッション言葉、二重敬語で要点を遠ざけない。
- 期限、条件、承認前にしてはならないことを、対象の行動の近くに置く。

## Bilingual and localized text

Default sequence: **shared message map → natural target-language realization → cross-language alignment check**.

- Before drafting, map facts, numbers, names, product terms, constraints, and claim status across versions.
- Use one approved target-language term for each concept; keep protected product names unchanged.
- Write naturally for the target language and locale. Do not copy English subject frequency, word order, modifier placement, punctuation, idiom, or paragraph rhythm into Japanese or another language.
- Preserve deliberate differences required by audience or locale, and identify them when the user asks for an alignment audit.
- Match meaning and force, not sentence boundaries. Do not translate ambiguity away by guessing.

## Agent-facing instructions

Use this recipe for prompts, `AGENTS.md`, `SKILL.md`, tool rules, and evaluation rubrics.

Default sequence: **goal and output → executable conditions → required action → exceptions → priority → completion evidence**.

- Write conditions that an agent can observe: “when a command exits nonzero,” not “when appropriate.”
- Pair each condition with a concrete action. State exceptions beside the rule they limit.
- Use explicit priority language when instructions can compete: identify which rule wins and the scope of that priority. Do not rely on section order to imply precedence.
- Use one term for each tool, artifact, state, and completion status. Define a term before using aliases.
- Preserve every constraint, prohibition, permission, tool boundary, output contract, and acceptance threshold. A rewrite must not broaden authority or weaken `must`, `do not`, or `only`.
- Make completion testable with required evidence or observable output. Do not add workflow, tools, or escalation paths absent from the source.

## Voice-sensitive creative text

Default sequence: **intended effect → voice-bearing choices → clarity changes only where requested**.

- Identify the requested voice, rhythm, imagery, point of view, and degree of ambiguity before editing.
- Preserve fragments, repetition, unusual syntax, wordplay, and silence when they create the intended effect.
- Resolve only accidental confusion unless clarity itself is the explicit creative goal.
- Prefer a local repair over flattening the whole piece into explanatory prose.
- Do not normalize dialect, cultural expression, or brand language merely because a plainer alternative exists.
