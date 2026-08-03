# Crystal Clear

An agent skill for writing and revising clear English and Japanese prose. It helps readers understand the intended meaning on the first pass.

Crystal Clear:

- leads with the answer or required action
- orders context around the reader's needs
- makes references, qualifications, and logical connections explicit
- preserves meaning, emphasis, constraints, and uncertainty while editing
- applies dedicated English and Japanese guidance
- uses a small *Elements of Style* index for targeted reference loading

## Install

Install into a project:

```sh
npx skills@latest add yasuhito/crystal-clear
```

Or install globally:

```sh
npx skills@latest add yasuhito/crystal-clear --global
```

The skill is model-invoked for explicit editing requests and complex communication-primary tasks such as documentation, reports, emails, prompts, and agent instructions. In Pi, direct invocation remains the guaranteed fallback:

```text
/skill:crystal-clear
```

The automatic-activation metadata comparison and raw Pi evidence are published in [`evals/results/routing/metadata-v1/`](evals/results/routing/metadata-v1/).

## Contents

- [`SKILL.md`](SKILL.md) — the writing and revision process
- [`language-guides.md`](language-guides.md) — concise guidance for clear English and natural Japanese
- [`references/use-cases.md`](references/use-cases.md) — focused, conditionally loaded recipes for substantial genre-specific tasks
- [`references/elements-of-style/index.md`](references/elements-of-style/index.md) — the task router and complete rule index
- [`references/elements-of-style/source.md`](references/elements-of-style/source.md) — the canonical public-domain source, with generated verbatim rule and word-usage files under the same directory; sourced from [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style)
- [`scripts/generate_elements_of_style.py`](scripts/generate_elements_of_style.py) — the deterministic reference generator (`--check` validates checked-in outputs)

## License

The original material in this repository is available under the [MIT License](LICENSE). *The Elements of Style* (1918) by William Strunk Jr. is public domain.
