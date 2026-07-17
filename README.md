# Crystal Clear

An agent skill for writing and revising clear English and Japanese prose. It helps readers understand the intended meaning on the first pass.

Crystal Clear:

- leads with the answer or required action
- orders context around the reader's needs
- makes references, qualifications, and logical connections explicit
- preserves meaning, emphasis, constraints, and uncertainty while editing
- applies dedicated English and Japanese guidance
- loads the 12,000-token *Elements of Style* reference only when the task needs it

## Install

Install into a project:

```sh
npx skills@latest add yasuhito/crystal-clear
```

Or install globally:

```sh
npx skills@latest add yasuhito/crystal-clear --global
```

The skill is model-invoked when answering complex questions, explaining a subject, drafting user-facing prose, or revising text for clarity. You can also invoke `crystal-clear` directly.

## Contents

- [`SKILL.md`](SKILL.md) — the writing and revision process
- [`language-guides.md`](language-guides.md) — concise guidance for clear English and natural Japanese
- [`elements-of-style.md`](elements-of-style.md) — the public-domain reference for detailed English usage and composition, sourced from [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style)

## License

The original material in this repository is available under the [MIT License](LICENSE). *The Elements of Style* (1918) by William Strunk Jr. is public domain.
