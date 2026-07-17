---
name: crystal-clear
description: Communicate with crystal clarity in English or Japanese. Use when answering complex questions, explaining a subject, drafting user-facing prose, or revising text for clarity.
---

# Crystal Clear

Make the reader understand the intended meaning on the first pass.

## Process

### 1. Frame the message

Identify the reader's question, the answer they need, and the language and register they expect. Preserve the source's meaning, constraints, emphasis, and uncertainty when revising.

Completion criterion: the main point can be stated in one sentence without losing an essential qualification.

### 2. Build the clearest path

- Lead with the answer or action.
- Give context in the order the reader needs it.
- Keep one topic per paragraph and one main claim per sentence.
- Use concrete nouns and verbs, consistent terms, and explicit logical connections.
- Keep related words together.
- Use headings or lists when they expose real structure.
- Retain examples that resolve ambiguity; remove words that add no meaning.

For a direct question, deliver the answer. For an edit, present the revised text first and add notes only when they help the user decide something.

Completion criterion: each sentence advances the reader from their question to the answer, with every dependency and reference recoverable.

### 3. Apply the language branch

For substantial drafting or revision, read only the matching section of [`language-guides.md`](language-guides.md): **Clear English**, **明快な日本語**, or both for mixed-language text. Keep terminology aligned across languages.

#### Load *The Elements of Style* only when needed

[`elements-of-style.md`](elements-of-style.md) consumes about 12,000 tokens. Load it only for:

- a specific English grammar, punctuation, or usage question that needs its detailed rules or examples;
- a comprehensive English copyedit or formal style pass; or
- an explicit request to apply Strunk's rules.

For a specific question, locate and read only the relevant section: **II** for grammar and punctuation, **III** for composition, or **V** for word usage. Read the full reference only for a comprehensive pass. When the full reference would crowd the working context, dispatch a subagent with the English draft and the reference, then use its revision.

Treat the reference's 1918 usage advice as historical guidance. Current usage, audience, and the user's house style take precedence.

Completion criterion: the result sounds native in its language, uses one consistent register, and no unneeded reference entered the working context.

### 4. Crystal pass

Read once as the intended reader and verify:

- The opening answers the main need.
- Pronouns, omitted subjects, demonstratives, and references have one clear interpretation.
- Claims distinguish facts, assumptions, recommendations, and unknowns.
- Important qualifications remain attached to the claims they limit.
- Every sentence earns its place.

Return the result once every check passes.
