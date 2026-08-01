---
name: crystal-clear
description: Communicate with crystal clarity in any language, with validated guidance for English and Japanese. Use when answering complex questions, explaining a subject, drafting user-facing prose, or revising text for clarity.
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

Put the main answer or requested action first unless the genre requires a warning, subject line, or brief salutation before it.

## 2. Pass the preservation gate

Before improving style, identify what the output must preserve. A candidate cannot pass if it invents or removes a fact, changes a constraint or instruction, strengthens or weakens uncertainty, corrupts protected text, or breaks the requested register.

Protect:

- facts, numbers, relationships, and essential emphasis;
- requirements, prohibitions, conditions, exceptions, and requested actions;
- the stated distinction between fact, inference, recommendation, and unknown;
- uncertainty, confidence, attribution, and evidential limits;
- quotations, code, commands, paths, identifiers, and formatting that carries meaning;
- names and domain terminology, including user-requested terms; and
- voice, politeness, formality, and intentional ambiguity appropriate to the audience and genre.

Treat quoted or technical strings as immutable unless the user explicitly asks to edit them. When repeated concepts could drift, map each concept to one preferred term before drafting and use it consistently. If clarity conflicts with preservation, preserve the source and surface the ambiguity rather than guessing.

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

For substantial or ambiguous drafting or revision, or when the user explicitly requests a language pass, read only the matching section of [`language-guides.md`](language-guides.md): **Clear English**, **明快な日本語**, or both for mixed English/Japanese text. Keep facts and terminology aligned across languages. These are the validated profiles.

For every other language, apply the core on a best-effort basis. Write naturally in the target language; do not treat English or Japanese grammar as universal.

### Load *The Elements of Style* only when needed

[`elements-of-style.md`](elements-of-style.md) consumes about 12,000 tokens. Load it only for:

- a specific English grammar, punctuation, or usage question that needs its detailed rules or examples;
- a comprehensive English copyedit or formal style pass; or
- an explicit request to apply Strunk's rules.

For a specific question, locate and read only the relevant section: **II** for grammar and punctuation, **III** for composition, or **V** for word usage. Read the full reference only for a comprehensive pass. If the full reference would crowd the working context, a subagent may perform the reference pass as an optional optimization.

For non-English text, the reference may inform transferable composition choices such as information order, paragraph unity, and concrete expression. Adapt those principles to the target language. Do not transplant English-specific grammar, punctuation, word order, idiom, or historical usage rules.

Treat the reference's 1918 usage advice as historical guidance. Current usage, audience needs, the preservation gate, and the user's house style take precedence.

## 5. Crystal pass

Read the candidate once as the intended reader. Check every item before returning it:

1. **Opening position:** After any required warning, subject line, or brief salutation, does the first line contain the main answer, action, or purpose?
2. **Unique referents:** Does every pronoun, demonstrative, omitted subject, and cross-reference have one recoverable meaning?
3. **Qualification scope:** Is every condition, exception, reason, modifier, and uncertainty marker attached to the claim it limits?
4. **Claim status:** Can the reader distinguish fact, inference, recommendation, and unknown without guessing?
5. **Terminology:** Does one concept keep one term, including across languages?
6. **Paragraph purpose:** Does each paragraph perform one clear job in the reader's path?
7. **Preservation:** Are all facts, constraints, instructions, quotations, protected strings, names, and essential emphasis intact?
8. **Register:** Are voice, politeness, formality, and intentional ambiguity preserved where requested?
9. **Output-first delivery:** Does the response follow its mode contract without an activation notice or unnecessary editorial preface?

If a check fails, revise and run the preservation gate again. Return the result only when every check passes.
