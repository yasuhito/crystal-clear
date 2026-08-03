---
name: crystal-clear
description: "Write or improve text and instructions for first-pass understanding. Use for explicit requests to clarify, simplify, polish, rewrite, edit, or proofread, and when communication quality is primary in complex explanations, documentation, READMEs, procedures, reports, proposals, emails, UI and error messages, summaries, prompts, agent instructions, or localized and multilingual text. Apply core clarity rules in any language and validated English and Japanese guidance. Preserve facts, constraints, uncertainty, terminology, protected text, and requested voice."
---

# Crystal Clear

Make the reader understand the intended meaning on the first pass. Apply the core below in every language. English and Japanese are the validated language profiles; use the core on a best-effort basis in every other language.

Apply the skill silently. Do not announce that it ran or add editorial commentary the user did not request. An already-clear passage may remain unchanged. Make the smallest revision that resolves a real comprehension problem; visible change is not a goal.

## 1. Frame the task

Identify the reader, target language, requested register, and the user's main question or requested action. Classify the task as one mode:

- **Answer:** Formulate the main answer before drafting. Return the answer first, followed by any requested support. When the user does not specify what follows, include only reasons, limits, or a next action that helps the reader.
- **Draft:** Formulate the requested action or purpose before drafting. Return the requested artifact, led by that action or purpose and organized around the reader's needs.
- **Rewrite:** Return the revised text first. Add notes only when the user requests them or needs them to decide something. If the source is already clear, return it unchanged.
- **Audit:** For each material problem, return `issue → misreading risk → proposed revision`. Do not silently rewrite the whole source unless requested. If there is no material problem, say so directly.

Put the main answer or requested action first unless the genre requires a warning, subject line, or brief salutation before it. Move the whole claim, including its fact, inference, recommendation, or uncertainty marker: lead a recommendation with its recommendation marker (for example, “We recommend”), never with a bare imperative.

## 2. Pass the preservation gate

Before improving style, identify what the output must preserve. A candidate cannot pass if it invents or removes a fact, changes a constraint or instruction, strengthens or weakens uncertainty, corrupts protected text, or breaks the requested register.

Protect:

- facts, numbers, relationships, and essential emphasis;
- requirements, prohibitions, conditions, exceptions, and requested actions;
- the stated distinction between fact, inference, recommendation, and unknown;
- each speech act, its modality, speaker, addressee, and exact content: keep a report a report, a request a request, and an instruction an instruction; never recast what someone said as what they asked or ordered, and never move an adjacent fact into attributed speech—for example, preserve the Japanese distinction between `〜すると伝えた` and `〜するよう伝えた`;
- uncertainty, confidence, attribution, and evidential limits;
- quotations, code, commands, paths, identifiers, and formatting that carries meaning;
- names and domain terminology, including user-requested terms; and
- voice, politeness, formality, and intentional ambiguity appropriate to the audience and genre.

Treat quoted or technical strings as immutable unless the user explicitly asks to edit them. Before rewriting communication, transfer, approval, or causality, map each semantic role as `actor → action → object → recipient` and keep that map unchanged. When repeated concepts could drift, map each concept to one preferred term before drafting and use it consistently. If clarity conflicts with preservation, preserve the source and surface the ambiguity rather than guessing.

## 3. Build the clearest path

Use these language-independent composition rules:

- Give context in the order the reader needs it.
- Keep each reference recoverable and each condition, exception, reason, and uncertainty marker next to the claim it qualifies.
- Distinguish facts, inferences, recommendations, and unknowns in the wording.
- Give each paragraph one purpose and each sentence one main claim unless combining claims makes their relationship clearer.
- Use concrete nouns and verbs, consistent terms, and explicit chronology, causality, contrast, or dependency where the reader would otherwise have to infer it.
- Keep related words together. Use headings or lists only when they expose real structure.
- Retain examples that resolve ambiguity. Remove words only when their meaning, emphasis, rhythm, and register are genuinely redundant.

Completion criterion: the reader can recover the main point, every dependency, and every reference in one pass without losing an essential qualification.

## 4. Apply the language profile

The core is sufficient for short tasks. Do not load a reference merely because the output is prose.

For a substantial task whose genre materially affects its structure, read only the matching recipe in [`references/use-cases.md`](references/use-cases.md). The recipes cover direct answers, documentation and procedures, errors and support, incidents and status updates, proposals and decision memos, emails and requests, Japanese business prose, bilingual and localized text, agent-facing instructions, and voice-sensitive creative text. Treat agent-facing instructions with interacting conditions, exceptions, priorities, or constraints as substantial. Do not load the recipes for a short task that the core resolves.

For substantial or ambiguous drafting or revision, or when the user explicitly requests a language pass, read only the matching section of [`language-guides.md`](language-guides.md): **Clear English**, **明快な日本語**, or both for mixed English/Japanese text. Keep facts and terminology aligned across languages. These are the validated profiles.

For every other language, apply the core on a best-effort basis. Write naturally in the target language; do not treat English or Japanese grammar as universal.

### Load *The Elements of Style* only when needed

Short tasks use the core only. Do not load an Elements reference merely because the output is prose.

For substantial writing or revision where grammar, punctuation, usage, or composition materially matters, every language may consult the same [`Elements of Style` index](references/elements-of-style/index.md). Read the index, then at most two relevant rule or word-usage chunk files. Apply a rule only when it is natural and useful in the target language. Target-language grammar, convention, information structure, and the applicable language guide override the reference; avoid direct transplantation of English-specific forms.

For a comprehensive English copyedit, formal style pass, or explicit request for a full Strunk pass, read the canonical [`source.md`](references/elements-of-style/source.md). For comprehensive work in any other language, continue to use the index and targeted rules rather than blindly importing the full English grammar.

Treat the reference's 1918 usage advice as historical guidance. Current usage, audience needs, the preservation gate, and the user's house style take precedence.

## 5. Crystal pass

Read the candidate once as the intended reader. Check every item before returning it:

1. **Opening position:** After any required warning, subject line, or brief salutation, does the first line contain the main answer, action, or purpose?
2. **Unique referents:** Does every pronoun, demonstrative, omitted subject, and cross-reference have one recoverable meaning?
3. **Qualification scope:** Is every condition, exception, reason, modifier, and uncertainty marker attached to the claim it limits?
4. **Claim and speech-act status:** Can the reader distinguish fact, inference, recommendation, and unknown without guessing? Does every report, request, instruction, promise, confirmation, and permission remain the same kind of speech act as in the source?
5. **Terminology:** Does one concept keep one term, including across languages?
6. **Paragraph purpose:** Does each paragraph perform one clear job in the reader's path?
7. **Preservation:** Are all facts, constraints, instructions, quotations, protected strings, names, and essential emphasis intact?
8. **Register:** Are voice, politeness, formality, and intentional ambiguity preserved where requested?
9. **Output-first delivery:** Does the response follow its mode contract without an activation notice or unnecessary editorial preface?

If a check fails, revise and run the preservation gate again. Before returning a rewrite, preserve each speech act and who said what to whom: never turn a report about an action into a request, command, instruction, promise, confirmation, or permission. In Japanese, restore an omitted subject inside the reported proposition when the source clarifies it elsewhere; do not resolve it by swapping the speaker and addressee. For example, when later context says that `X` is B's action, preserve `AがBに、Xすると伝えた` as `AはBに「BがXする」と伝えた`; keep facts outside that reported proposition outside it, and do not invent their order. Explicitly check that `〜すると伝えた` has not become `〜するよう伝えた` and that `AはBに伝えた` has not become `BはAに伝えた`. Return the result only when every check passes.
