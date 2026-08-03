# Clarity-behavior evaluation

This injected-behavior evaluation reports generation arms separately and blind-compares `178eaf8 vs e8138b051b4683a90dffc5e6f8ff6ea5360a82c7`. It is not automatic-routing evidence.
Frozen scenarios: `behavior-v1`; 5 repetitions per scenario and arm.

English, Japanese, and multilingual-core evidence is reported separately; there is no pooled headline score.

## English

Generations: 75; blind comparisons: 25.

### Deterministic evidence

Exact-literal checks provide preservation evidence only; they do not establish semantic correctness or clarity.

| Arm | Runs | Missing outputs | Protected | Facts | Numbers | Constraints | Conditions |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | 25 | 0 | 0 | 5 | 5 | 0 | 5 |
| 178eaf8 | 25 | 0 | 0 | 6 | 5 | 0 | 5 |
| e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 25 | 0 | 0 | 5 | 4 | 0 | 5 |

### GPT-judged evidence

Blind, seeded A/B judgments are model evidence and are separate from deterministic checks.

| Arm | Preservation | First-pass understanding | Core structure | Critical failures | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | n/a | n/a | n/a | 0 | 0 | 0 | 0 |
| 178eaf8 | 3.920 | 4.920 | 4.600 | 13 | 0 | 20 | 5 |
| e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5.000 | 5.000 | 5.000 | 0 | 20 | 0 | 5 |

## Japanese

Generations: 75; blind comparisons: 25.

### Deterministic evidence

Exact-literal checks provide preservation evidence only; they do not establish semantic correctness or clarity.

| Arm | Runs | Missing outputs | Protected | Facts | Numbers | Constraints | Conditions |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | 25 | 0 | 0 | 10 | 1 | 0 | 0 |
| 178eaf8 | 25 | 0 | 0 | 10 | 3 | 0 | 0 |
| e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 25 | 0 | 0 | 10 | 5 | 0 | 0 |

### GPT-judged evidence

Blind, seeded A/B judgments are model evidence and are separate from deterministic checks.

| Arm | Preservation | First-pass understanding | Core structure | Critical failures | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | n/a | n/a | n/a | 0 | 0 | 0 | 0 |
| 178eaf8 | 4.600 | 4.960 | 4.720 | 0 | 0 | 15 | 10 |
| e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5.000 | 5.000 | 5.000 | 0 | 15 | 0 | 10 |

## Multilingual core

Generations: 75; blind comparisons: 25.

### Deterministic evidence

Exact-literal checks provide preservation evidence only; they do not establish semantic correctness or clarity.

| Arm | Runs | Missing outputs | Protected | Facts | Numbers | Constraints | Conditions |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | 25 | 0 | 0 | 5 | 0 | 0 | 5 |
| 178eaf8 | 25 | 0 | 1 | 5 | 0 | 5 | 4 |
| e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 25 | 0 | 0 | 5 | 0 | 0 | 4 |

### GPT-judged evidence

Blind, seeded A/B judgments are model evidence and are separate from deterministic checks.

| Arm | Preservation | First-pass understanding | Core structure | Critical failures | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | n/a | n/a | n/a | 0 | 0 | 0 | 0 |
| 178eaf8 | 4.440 | n/a | 4.480 | 4 | 0 | 22 | 3 |
| e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5.000 | n/a | 5.000 | 0 | 22 | 0 | 3 |

Spanish, Simplified Chinese, Arabic, German, and mixed Japanese/English are assessed only for core structure and preservation. This report makes no native-naturalness claim and does not treat them as validated language profiles.

## Human-reviewed evidence

No human-reviewed evidence was collected for this baseline. Native-Japanese calibration is a later release step.

## Raw evidence

### Generations

| Scenario | Category | Arm | Repeat | Deterministic | Result | Trace |
|---|---|---|---:|---|---|---|
| en-ambiguous-referent | english | 178eaf8 | 1 | pass | [result](raw/generations/en-ambiguous-referent--178eaf8--r01.result.json) | [trace](raw/generations/en-ambiguous-referent--178eaf8--r01.trace.jsonl) |
| en-ambiguous-referent | english | 178eaf8 | 2 | pass | [result](raw/generations/en-ambiguous-referent--178eaf8--r02.result.json) | [trace](raw/generations/en-ambiguous-referent--178eaf8--r02.trace.jsonl) |
| en-ambiguous-referent | english | 178eaf8 | 3 | pass | [result](raw/generations/en-ambiguous-referent--178eaf8--r03.result.json) | [trace](raw/generations/en-ambiguous-referent--178eaf8--r03.trace.jsonl) |
| en-ambiguous-referent | english | 178eaf8 | 4 | fail | [result](raw/generations/en-ambiguous-referent--178eaf8--r04.result.json) | [trace](raw/generations/en-ambiguous-referent--178eaf8--r04.trace.jsonl) |
| en-ambiguous-referent | english | 178eaf8 | 5 | pass | [result](raw/generations/en-ambiguous-referent--178eaf8--r05.result.json) | [trace](raw/generations/en-ambiguous-referent--178eaf8--r05.trace.jsonl) |
| en-ambiguous-referent | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| en-ambiguous-referent | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| en-ambiguous-referent | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| en-ambiguous-referent | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| en-ambiguous-referent | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/en-ambiguous-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| en-ambiguous-referent | english | no-skill | 1 | pass | [result](raw/generations/en-ambiguous-referent--no-skill--r01.result.json) | [trace](raw/generations/en-ambiguous-referent--no-skill--r01.trace.jsonl) |
| en-ambiguous-referent | english | no-skill | 2 | pass | [result](raw/generations/en-ambiguous-referent--no-skill--r02.result.json) | [trace](raw/generations/en-ambiguous-referent--no-skill--r02.trace.jsonl) |
| en-ambiguous-referent | english | no-skill | 3 | pass | [result](raw/generations/en-ambiguous-referent--no-skill--r03.result.json) | [trace](raw/generations/en-ambiguous-referent--no-skill--r03.trace.jsonl) |
| en-ambiguous-referent | english | no-skill | 4 | pass | [result](raw/generations/en-ambiguous-referent--no-skill--r04.result.json) | [trace](raw/generations/en-ambiguous-referent--no-skill--r04.trace.jsonl) |
| en-ambiguous-referent | english | no-skill | 5 | pass | [result](raw/generations/en-ambiguous-referent--no-skill--r05.result.json) | [trace](raw/generations/en-ambiguous-referent--no-skill--r05.trace.jsonl) |
| en-buried-answer | english | 178eaf8 | 1 | pass | [result](raw/generations/en-buried-answer--178eaf8--r01.result.json) | [trace](raw/generations/en-buried-answer--178eaf8--r01.trace.jsonl) |
| en-buried-answer | english | 178eaf8 | 2 | pass | [result](raw/generations/en-buried-answer--178eaf8--r02.result.json) | [trace](raw/generations/en-buried-answer--178eaf8--r02.trace.jsonl) |
| en-buried-answer | english | 178eaf8 | 3 | pass | [result](raw/generations/en-buried-answer--178eaf8--r03.result.json) | [trace](raw/generations/en-buried-answer--178eaf8--r03.trace.jsonl) |
| en-buried-answer | english | 178eaf8 | 4 | pass | [result](raw/generations/en-buried-answer--178eaf8--r04.result.json) | [trace](raw/generations/en-buried-answer--178eaf8--r04.trace.jsonl) |
| en-buried-answer | english | 178eaf8 | 5 | pass | [result](raw/generations/en-buried-answer--178eaf8--r05.result.json) | [trace](raw/generations/en-buried-answer--178eaf8--r05.trace.jsonl) |
| en-buried-answer | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| en-buried-answer | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| en-buried-answer | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| en-buried-answer | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| en-buried-answer | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/en-buried-answer--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| en-buried-answer | english | no-skill | 1 | pass | [result](raw/generations/en-buried-answer--no-skill--r01.result.json) | [trace](raw/generations/en-buried-answer--no-skill--r01.trace.jsonl) |
| en-buried-answer | english | no-skill | 2 | pass | [result](raw/generations/en-buried-answer--no-skill--r02.result.json) | [trace](raw/generations/en-buried-answer--no-skill--r02.trace.jsonl) |
| en-buried-answer | english | no-skill | 3 | pass | [result](raw/generations/en-buried-answer--no-skill--r03.result.json) | [trace](raw/generations/en-buried-answer--no-skill--r03.trace.jsonl) |
| en-buried-answer | english | no-skill | 4 | pass | [result](raw/generations/en-buried-answer--no-skill--r04.result.json) | [trace](raw/generations/en-buried-answer--no-skill--r04.trace.jsonl) |
| en-buried-answer | english | no-skill | 5 | pass | [result](raw/generations/en-buried-answer--no-skill--r05.result.json) | [trace](raw/generations/en-buried-answer--no-skill--r05.trace.jsonl) |
| en-detached-qualification | english | 178eaf8 | 1 | fail | [result](raw/generations/en-detached-qualification--178eaf8--r01.result.json) | [trace](raw/generations/en-detached-qualification--178eaf8--r01.trace.jsonl) |
| en-detached-qualification | english | 178eaf8 | 2 | fail | [result](raw/generations/en-detached-qualification--178eaf8--r02.result.json) | [trace](raw/generations/en-detached-qualification--178eaf8--r02.trace.jsonl) |
| en-detached-qualification | english | 178eaf8 | 3 | fail | [result](raw/generations/en-detached-qualification--178eaf8--r03.result.json) | [trace](raw/generations/en-detached-qualification--178eaf8--r03.trace.jsonl) |
| en-detached-qualification | english | 178eaf8 | 4 | fail | [result](raw/generations/en-detached-qualification--178eaf8--r04.result.json) | [trace](raw/generations/en-detached-qualification--178eaf8--r04.trace.jsonl) |
| en-detached-qualification | english | 178eaf8 | 5 | fail | [result](raw/generations/en-detached-qualification--178eaf8--r05.result.json) | [trace](raw/generations/en-detached-qualification--178eaf8--r05.trace.jsonl) |
| en-detached-qualification | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | fail | [result](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| en-detached-qualification | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | fail | [result](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| en-detached-qualification | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | fail | [result](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| en-detached-qualification | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | fail | [result](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| en-detached-qualification | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | fail | [result](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/en-detached-qualification--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| en-detached-qualification | english | no-skill | 1 | fail | [result](raw/generations/en-detached-qualification--no-skill--r01.result.json) | [trace](raw/generations/en-detached-qualification--no-skill--r01.trace.jsonl) |
| en-detached-qualification | english | no-skill | 2 | fail | [result](raw/generations/en-detached-qualification--no-skill--r02.result.json) | [trace](raw/generations/en-detached-qualification--no-skill--r02.trace.jsonl) |
| en-detached-qualification | english | no-skill | 3 | fail | [result](raw/generations/en-detached-qualification--no-skill--r03.result.json) | [trace](raw/generations/en-detached-qualification--no-skill--r03.trace.jsonl) |
| en-detached-qualification | english | no-skill | 4 | fail | [result](raw/generations/en-detached-qualification--no-skill--r04.result.json) | [trace](raw/generations/en-detached-qualification--no-skill--r04.trace.jsonl) |
| en-detached-qualification | english | no-skill | 5 | fail | [result](raw/generations/en-detached-qualification--no-skill--r05.result.json) | [trace](raw/generations/en-detached-qualification--no-skill--r05.trace.jsonl) |
| en-register-certainty | english | 178eaf8 | 1 | fail | [result](raw/generations/en-register-certainty--178eaf8--r01.result.json) | [trace](raw/generations/en-register-certainty--178eaf8--r01.trace.jsonl) |
| en-register-certainty | english | 178eaf8 | 2 | fail | [result](raw/generations/en-register-certainty--178eaf8--r02.result.json) | [trace](raw/generations/en-register-certainty--178eaf8--r02.trace.jsonl) |
| en-register-certainty | english | 178eaf8 | 3 | fail | [result](raw/generations/en-register-certainty--178eaf8--r03.result.json) | [trace](raw/generations/en-register-certainty--178eaf8--r03.trace.jsonl) |
| en-register-certainty | english | 178eaf8 | 4 | fail | [result](raw/generations/en-register-certainty--178eaf8--r04.result.json) | [trace](raw/generations/en-register-certainty--178eaf8--r04.trace.jsonl) |
| en-register-certainty | english | 178eaf8 | 5 | fail | [result](raw/generations/en-register-certainty--178eaf8--r05.result.json) | [trace](raw/generations/en-register-certainty--178eaf8--r05.trace.jsonl) |
| en-register-certainty | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | fail | [result](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| en-register-certainty | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | fail | [result](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| en-register-certainty | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | fail | [result](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| en-register-certainty | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | fail | [result](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| en-register-certainty | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | fail | [result](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/en-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| en-register-certainty | english | no-skill | 1 | fail | [result](raw/generations/en-register-certainty--no-skill--r01.result.json) | [trace](raw/generations/en-register-certainty--no-skill--r01.trace.jsonl) |
| en-register-certainty | english | no-skill | 2 | fail | [result](raw/generations/en-register-certainty--no-skill--r02.result.json) | [trace](raw/generations/en-register-certainty--no-skill--r02.trace.jsonl) |
| en-register-certainty | english | no-skill | 3 | fail | [result](raw/generations/en-register-certainty--no-skill--r03.result.json) | [trace](raw/generations/en-register-certainty--no-skill--r03.trace.jsonl) |
| en-register-certainty | english | no-skill | 4 | fail | [result](raw/generations/en-register-certainty--no-skill--r04.result.json) | [trace](raw/generations/en-register-certainty--no-skill--r04.trace.jsonl) |
| en-register-certainty | english | no-skill | 5 | fail | [result](raw/generations/en-register-certainty--no-skill--r05.result.json) | [trace](raw/generations/en-register-certainty--no-skill--r05.trace.jsonl) |
| en-terminology-drift | english | 178eaf8 | 1 | pass | [result](raw/generations/en-terminology-drift--178eaf8--r01.result.json) | [trace](raw/generations/en-terminology-drift--178eaf8--r01.trace.jsonl) |
| en-terminology-drift | english | 178eaf8 | 2 | pass | [result](raw/generations/en-terminology-drift--178eaf8--r02.result.json) | [trace](raw/generations/en-terminology-drift--178eaf8--r02.trace.jsonl) |
| en-terminology-drift | english | 178eaf8 | 3 | pass | [result](raw/generations/en-terminology-drift--178eaf8--r03.result.json) | [trace](raw/generations/en-terminology-drift--178eaf8--r03.trace.jsonl) |
| en-terminology-drift | english | 178eaf8 | 4 | pass | [result](raw/generations/en-terminology-drift--178eaf8--r04.result.json) | [trace](raw/generations/en-terminology-drift--178eaf8--r04.trace.jsonl) |
| en-terminology-drift | english | 178eaf8 | 5 | pass | [result](raw/generations/en-terminology-drift--178eaf8--r05.result.json) | [trace](raw/generations/en-terminology-drift--178eaf8--r05.trace.jsonl) |
| en-terminology-drift | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| en-terminology-drift | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| en-terminology-drift | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| en-terminology-drift | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| en-terminology-drift | english | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/en-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| en-terminology-drift | english | no-skill | 1 | pass | [result](raw/generations/en-terminology-drift--no-skill--r01.result.json) | [trace](raw/generations/en-terminology-drift--no-skill--r01.trace.jsonl) |
| en-terminology-drift | english | no-skill | 2 | pass | [result](raw/generations/en-terminology-drift--no-skill--r02.result.json) | [trace](raw/generations/en-terminology-drift--no-skill--r02.trace.jsonl) |
| en-terminology-drift | english | no-skill | 3 | pass | [result](raw/generations/en-terminology-drift--no-skill--r03.result.json) | [trace](raw/generations/en-terminology-drift--no-skill--r03.trace.jsonl) |
| en-terminology-drift | english | no-skill | 4 | pass | [result](raw/generations/en-terminology-drift--no-skill--r04.result.json) | [trace](raw/generations/en-terminology-drift--no-skill--r04.trace.jsonl) |
| en-terminology-drift | english | no-skill | 5 | pass | [result](raw/generations/en-terminology-drift--no-skill--r05.result.json) | [trace](raw/generations/en-terminology-drift--no-skill--r05.trace.jsonl) |
| ja-ambiguous-subject | japanese | 178eaf8 | 1 | fail | [result](raw/generations/ja-ambiguous-subject--178eaf8--r01.result.json) | [trace](raw/generations/ja-ambiguous-subject--178eaf8--r01.trace.jsonl) |
| ja-ambiguous-subject | japanese | 178eaf8 | 2 | fail | [result](raw/generations/ja-ambiguous-subject--178eaf8--r02.result.json) | [trace](raw/generations/ja-ambiguous-subject--178eaf8--r02.trace.jsonl) |
| ja-ambiguous-subject | japanese | 178eaf8 | 3 | fail | [result](raw/generations/ja-ambiguous-subject--178eaf8--r03.result.json) | [trace](raw/generations/ja-ambiguous-subject--178eaf8--r03.trace.jsonl) |
| ja-ambiguous-subject | japanese | 178eaf8 | 4 | fail | [result](raw/generations/ja-ambiguous-subject--178eaf8--r04.result.json) | [trace](raw/generations/ja-ambiguous-subject--178eaf8--r04.trace.jsonl) |
| ja-ambiguous-subject | japanese | 178eaf8 | 5 | fail | [result](raw/generations/ja-ambiguous-subject--178eaf8--r05.result.json) | [trace](raw/generations/ja-ambiguous-subject--178eaf8--r05.trace.jsonl) |
| ja-ambiguous-subject | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | fail | [result](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| ja-ambiguous-subject | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | fail | [result](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| ja-ambiguous-subject | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | fail | [result](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| ja-ambiguous-subject | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | fail | [result](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| ja-ambiguous-subject | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | fail | [result](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/ja-ambiguous-subject--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| ja-ambiguous-subject | japanese | no-skill | 1 | fail | [result](raw/generations/ja-ambiguous-subject--no-skill--r01.result.json) | [trace](raw/generations/ja-ambiguous-subject--no-skill--r01.trace.jsonl) |
| ja-ambiguous-subject | japanese | no-skill | 2 | fail | [result](raw/generations/ja-ambiguous-subject--no-skill--r02.result.json) | [trace](raw/generations/ja-ambiguous-subject--no-skill--r02.trace.jsonl) |
| ja-ambiguous-subject | japanese | no-skill | 3 | fail | [result](raw/generations/ja-ambiguous-subject--no-skill--r03.result.json) | [trace](raw/generations/ja-ambiguous-subject--no-skill--r03.trace.jsonl) |
| ja-ambiguous-subject | japanese | no-skill | 4 | fail | [result](raw/generations/ja-ambiguous-subject--no-skill--r04.result.json) | [trace](raw/generations/ja-ambiguous-subject--no-skill--r04.trace.jsonl) |
| ja-ambiguous-subject | japanese | no-skill | 5 | fail | [result](raw/generations/ja-ambiguous-subject--no-skill--r05.result.json) | [trace](raw/generations/ja-ambiguous-subject--no-skill--r05.trace.jsonl) |
| ja-buried-action | japanese | 178eaf8 | 1 | pass | [result](raw/generations/ja-buried-action--178eaf8--r01.result.json) | [trace](raw/generations/ja-buried-action--178eaf8--r01.trace.jsonl) |
| ja-buried-action | japanese | 178eaf8 | 2 | pass | [result](raw/generations/ja-buried-action--178eaf8--r02.result.json) | [trace](raw/generations/ja-buried-action--178eaf8--r02.trace.jsonl) |
| ja-buried-action | japanese | 178eaf8 | 3 | pass | [result](raw/generations/ja-buried-action--178eaf8--r03.result.json) | [trace](raw/generations/ja-buried-action--178eaf8--r03.trace.jsonl) |
| ja-buried-action | japanese | 178eaf8 | 4 | pass | [result](raw/generations/ja-buried-action--178eaf8--r04.result.json) | [trace](raw/generations/ja-buried-action--178eaf8--r04.trace.jsonl) |
| ja-buried-action | japanese | 178eaf8 | 5 | pass | [result](raw/generations/ja-buried-action--178eaf8--r05.result.json) | [trace](raw/generations/ja-buried-action--178eaf8--r05.trace.jsonl) |
| ja-buried-action | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| ja-buried-action | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| ja-buried-action | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| ja-buried-action | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| ja-buried-action | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/ja-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| ja-buried-action | japanese | no-skill | 1 | pass | [result](raw/generations/ja-buried-action--no-skill--r01.result.json) | [trace](raw/generations/ja-buried-action--no-skill--r01.trace.jsonl) |
| ja-buried-action | japanese | no-skill | 2 | pass | [result](raw/generations/ja-buried-action--no-skill--r02.result.json) | [trace](raw/generations/ja-buried-action--no-skill--r02.trace.jsonl) |
| ja-buried-action | japanese | no-skill | 3 | pass | [result](raw/generations/ja-buried-action--no-skill--r03.result.json) | [trace](raw/generations/ja-buried-action--no-skill--r03.trace.jsonl) |
| ja-buried-action | japanese | no-skill | 4 | pass | [result](raw/generations/ja-buried-action--no-skill--r04.result.json) | [trace](raw/generations/ja-buried-action--no-skill--r04.trace.jsonl) |
| ja-buried-action | japanese | no-skill | 5 | pass | [result](raw/generations/ja-buried-action--no-skill--r05.result.json) | [trace](raw/generations/ja-buried-action--no-skill--r05.trace.jsonl) |
| ja-detached-condition | japanese | 178eaf8 | 1 | pass | [result](raw/generations/ja-detached-condition--178eaf8--r01.result.json) | [trace](raw/generations/ja-detached-condition--178eaf8--r01.trace.jsonl) |
| ja-detached-condition | japanese | 178eaf8 | 2 | pass | [result](raw/generations/ja-detached-condition--178eaf8--r02.result.json) | [trace](raw/generations/ja-detached-condition--178eaf8--r02.trace.jsonl) |
| ja-detached-condition | japanese | 178eaf8 | 3 | pass | [result](raw/generations/ja-detached-condition--178eaf8--r03.result.json) | [trace](raw/generations/ja-detached-condition--178eaf8--r03.trace.jsonl) |
| ja-detached-condition | japanese | 178eaf8 | 4 | pass | [result](raw/generations/ja-detached-condition--178eaf8--r04.result.json) | [trace](raw/generations/ja-detached-condition--178eaf8--r04.trace.jsonl) |
| ja-detached-condition | japanese | 178eaf8 | 5 | pass | [result](raw/generations/ja-detached-condition--178eaf8--r05.result.json) | [trace](raw/generations/ja-detached-condition--178eaf8--r05.trace.jsonl) |
| ja-detached-condition | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| ja-detached-condition | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| ja-detached-condition | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| ja-detached-condition | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| ja-detached-condition | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/ja-detached-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| ja-detached-condition | japanese | no-skill | 1 | pass | [result](raw/generations/ja-detached-condition--no-skill--r01.result.json) | [trace](raw/generations/ja-detached-condition--no-skill--r01.trace.jsonl) |
| ja-detached-condition | japanese | no-skill | 2 | pass | [result](raw/generations/ja-detached-condition--no-skill--r02.result.json) | [trace](raw/generations/ja-detached-condition--no-skill--r02.trace.jsonl) |
| ja-detached-condition | japanese | no-skill | 3 | pass | [result](raw/generations/ja-detached-condition--no-skill--r03.result.json) | [trace](raw/generations/ja-detached-condition--no-skill--r03.trace.jsonl) |
| ja-detached-condition | japanese | no-skill | 4 | pass | [result](raw/generations/ja-detached-condition--no-skill--r04.result.json) | [trace](raw/generations/ja-detached-condition--no-skill--r04.trace.jsonl) |
| ja-detached-condition | japanese | no-skill | 5 | pass | [result](raw/generations/ja-detached-condition--no-skill--r05.result.json) | [trace](raw/generations/ja-detached-condition--no-skill--r05.trace.jsonl) |
| ja-register-certainty | japanese | 178eaf8 | 1 | fail | [result](raw/generations/ja-register-certainty--178eaf8--r01.result.json) | [trace](raw/generations/ja-register-certainty--178eaf8--r01.trace.jsonl) |
| ja-register-certainty | japanese | 178eaf8 | 2 | fail | [result](raw/generations/ja-register-certainty--178eaf8--r02.result.json) | [trace](raw/generations/ja-register-certainty--178eaf8--r02.trace.jsonl) |
| ja-register-certainty | japanese | 178eaf8 | 3 | fail | [result](raw/generations/ja-register-certainty--178eaf8--r03.result.json) | [trace](raw/generations/ja-register-certainty--178eaf8--r03.trace.jsonl) |
| ja-register-certainty | japanese | 178eaf8 | 4 | fail | [result](raw/generations/ja-register-certainty--178eaf8--r04.result.json) | [trace](raw/generations/ja-register-certainty--178eaf8--r04.trace.jsonl) |
| ja-register-certainty | japanese | 178eaf8 | 5 | fail | [result](raw/generations/ja-register-certainty--178eaf8--r05.result.json) | [trace](raw/generations/ja-register-certainty--178eaf8--r05.trace.jsonl) |
| ja-register-certainty | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | fail | [result](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| ja-register-certainty | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | fail | [result](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| ja-register-certainty | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | fail | [result](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| ja-register-certainty | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | fail | [result](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| ja-register-certainty | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | fail | [result](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/ja-register-certainty--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| ja-register-certainty | japanese | no-skill | 1 | fail | [result](raw/generations/ja-register-certainty--no-skill--r01.result.json) | [trace](raw/generations/ja-register-certainty--no-skill--r01.trace.jsonl) |
| ja-register-certainty | japanese | no-skill | 2 | fail | [result](raw/generations/ja-register-certainty--no-skill--r02.result.json) | [trace](raw/generations/ja-register-certainty--no-skill--r02.trace.jsonl) |
| ja-register-certainty | japanese | no-skill | 3 | fail | [result](raw/generations/ja-register-certainty--no-skill--r03.result.json) | [trace](raw/generations/ja-register-certainty--no-skill--r03.trace.jsonl) |
| ja-register-certainty | japanese | no-skill | 4 | fail | [result](raw/generations/ja-register-certainty--no-skill--r04.result.json) | [trace](raw/generations/ja-register-certainty--no-skill--r04.trace.jsonl) |
| ja-register-certainty | japanese | no-skill | 5 | fail | [result](raw/generations/ja-register-certainty--no-skill--r05.result.json) | [trace](raw/generations/ja-register-certainty--no-skill--r05.trace.jsonl) |
| ja-terminology-drift | japanese | 178eaf8 | 1 | pass | [result](raw/generations/ja-terminology-drift--178eaf8--r01.result.json) | [trace](raw/generations/ja-terminology-drift--178eaf8--r01.trace.jsonl) |
| ja-terminology-drift | japanese | 178eaf8 | 2 | pass | [result](raw/generations/ja-terminology-drift--178eaf8--r02.result.json) | [trace](raw/generations/ja-terminology-drift--178eaf8--r02.trace.jsonl) |
| ja-terminology-drift | japanese | 178eaf8 | 3 | pass | [result](raw/generations/ja-terminology-drift--178eaf8--r03.result.json) | [trace](raw/generations/ja-terminology-drift--178eaf8--r03.trace.jsonl) |
| ja-terminology-drift | japanese | 178eaf8 | 4 | pass | [result](raw/generations/ja-terminology-drift--178eaf8--r04.result.json) | [trace](raw/generations/ja-terminology-drift--178eaf8--r04.trace.jsonl) |
| ja-terminology-drift | japanese | 178eaf8 | 5 | pass | [result](raw/generations/ja-terminology-drift--178eaf8--r05.result.json) | [trace](raw/generations/ja-terminology-drift--178eaf8--r05.trace.jsonl) |
| ja-terminology-drift | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| ja-terminology-drift | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| ja-terminology-drift | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| ja-terminology-drift | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| ja-terminology-drift | japanese | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/ja-terminology-drift--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| ja-terminology-drift | japanese | no-skill | 1 | pass | [result](raw/generations/ja-terminology-drift--no-skill--r01.result.json) | [trace](raw/generations/ja-terminology-drift--no-skill--r01.trace.jsonl) |
| ja-terminology-drift | japanese | no-skill | 2 | pass | [result](raw/generations/ja-terminology-drift--no-skill--r02.result.json) | [trace](raw/generations/ja-terminology-drift--no-skill--r02.trace.jsonl) |
| ja-terminology-drift | japanese | no-skill | 3 | pass | [result](raw/generations/ja-terminology-drift--no-skill--r03.result.json) | [trace](raw/generations/ja-terminology-drift--no-skill--r03.trace.jsonl) |
| ja-terminology-drift | japanese | no-skill | 4 | pass | [result](raw/generations/ja-terminology-drift--no-skill--r04.result.json) | [trace](raw/generations/ja-terminology-drift--no-skill--r04.trace.jsonl) |
| ja-terminology-drift | japanese | no-skill | 5 | pass | [result](raw/generations/ja-terminology-drift--no-skill--r05.result.json) | [trace](raw/generations/ja-terminology-drift--no-skill--r05.trace.jsonl) |
| multi-ar-condition | multilingual-core | 178eaf8 | 1 | pass | [result](raw/generations/multi-ar-condition--178eaf8--r01.result.json) | [trace](raw/generations/multi-ar-condition--178eaf8--r01.trace.jsonl) |
| multi-ar-condition | multilingual-core | 178eaf8 | 2 | pass | [result](raw/generations/multi-ar-condition--178eaf8--r02.result.json) | [trace](raw/generations/multi-ar-condition--178eaf8--r02.trace.jsonl) |
| multi-ar-condition | multilingual-core | 178eaf8 | 3 | pass | [result](raw/generations/multi-ar-condition--178eaf8--r03.result.json) | [trace](raw/generations/multi-ar-condition--178eaf8--r03.trace.jsonl) |
| multi-ar-condition | multilingual-core | 178eaf8 | 4 | pass | [result](raw/generations/multi-ar-condition--178eaf8--r04.result.json) | [trace](raw/generations/multi-ar-condition--178eaf8--r04.trace.jsonl) |
| multi-ar-condition | multilingual-core | 178eaf8 | 5 | pass | [result](raw/generations/multi-ar-condition--178eaf8--r05.result.json) | [trace](raw/generations/multi-ar-condition--178eaf8--r05.trace.jsonl) |
| multi-ar-condition | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| multi-ar-condition | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| multi-ar-condition | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| multi-ar-condition | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| multi-ar-condition | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/multi-ar-condition--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| multi-ar-condition | multilingual-core | no-skill | 1 | pass | [result](raw/generations/multi-ar-condition--no-skill--r01.result.json) | [trace](raw/generations/multi-ar-condition--no-skill--r01.trace.jsonl) |
| multi-ar-condition | multilingual-core | no-skill | 2 | pass | [result](raw/generations/multi-ar-condition--no-skill--r02.result.json) | [trace](raw/generations/multi-ar-condition--no-skill--r02.trace.jsonl) |
| multi-ar-condition | multilingual-core | no-skill | 3 | pass | [result](raw/generations/multi-ar-condition--no-skill--r03.result.json) | [trace](raw/generations/multi-ar-condition--no-skill--r03.trace.jsonl) |
| multi-ar-condition | multilingual-core | no-skill | 4 | pass | [result](raw/generations/multi-ar-condition--no-skill--r04.result.json) | [trace](raw/generations/multi-ar-condition--no-skill--r04.trace.jsonl) |
| multi-ar-condition | multilingual-core | no-skill | 5 | pass | [result](raw/generations/multi-ar-condition--no-skill--r05.result.json) | [trace](raw/generations/multi-ar-condition--no-skill--r05.trace.jsonl) |
| multi-de-terminology | multilingual-core | 178eaf8 | 1 | fail | [result](raw/generations/multi-de-terminology--178eaf8--r01.result.json) | [trace](raw/generations/multi-de-terminology--178eaf8--r01.trace.jsonl) |
| multi-de-terminology | multilingual-core | 178eaf8 | 2 | fail | [result](raw/generations/multi-de-terminology--178eaf8--r02.result.json) | [trace](raw/generations/multi-de-terminology--178eaf8--r02.trace.jsonl) |
| multi-de-terminology | multilingual-core | 178eaf8 | 3 | fail | [result](raw/generations/multi-de-terminology--178eaf8--r03.result.json) | [trace](raw/generations/multi-de-terminology--178eaf8--r03.trace.jsonl) |
| multi-de-terminology | multilingual-core | 178eaf8 | 4 | fail | [result](raw/generations/multi-de-terminology--178eaf8--r04.result.json) | [trace](raw/generations/multi-de-terminology--178eaf8--r04.trace.jsonl) |
| multi-de-terminology | multilingual-core | 178eaf8 | 5 | fail | [result](raw/generations/multi-de-terminology--178eaf8--r05.result.json) | [trace](raw/generations/multi-de-terminology--178eaf8--r05.trace.jsonl) |
| multi-de-terminology | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| multi-de-terminology | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| multi-de-terminology | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| multi-de-terminology | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| multi-de-terminology | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/multi-de-terminology--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 1 | pass | [result](raw/generations/multi-de-terminology--no-skill--r01.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r01.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 2 | pass | [result](raw/generations/multi-de-terminology--no-skill--r02.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r02.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 3 | pass | [result](raw/generations/multi-de-terminology--no-skill--r03.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r03.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 4 | pass | [result](raw/generations/multi-de-terminology--no-skill--r04.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r04.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 5 | pass | [result](raw/generations/multi-de-terminology--no-skill--r05.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r05.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 1 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r01.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r01.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 2 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r02.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r02.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 3 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r03.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r03.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 4 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r04.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r04.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 5 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r05.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r05.trace.jsonl) |
| multi-es-buried-action | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | pass | [result](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| multi-es-buried-action | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | pass | [result](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| multi-es-buried-action | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | pass | [result](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| multi-es-buried-action | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | pass | [result](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| multi-es-buried-action | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/multi-es-buried-action--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 1 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r01.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r01.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 2 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r02.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r02.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 3 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r03.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r03.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 4 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r04.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r04.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 5 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r05.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r05.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 1 | fail | [result](raw/generations/multi-mixed-ja-en--178eaf8--r01.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r01.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 2 | pass | [result](raw/generations/multi-mixed-ja-en--178eaf8--r02.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r02.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 3 | fail | [result](raw/generations/multi-mixed-ja-en--178eaf8--r03.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r03.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 4 | fail | [result](raw/generations/multi-mixed-ja-en--178eaf8--r04.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r04.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 5 | fail | [result](raw/generations/multi-mixed-ja-en--178eaf8--r05.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r05.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | fail | [result](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | fail | [result](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | fail | [result](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | fail | [result](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | pass | [result](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/multi-mixed-ja-en--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | no-skill | 1 | fail | [result](raw/generations/multi-mixed-ja-en--no-skill--r01.result.json) | [trace](raw/generations/multi-mixed-ja-en--no-skill--r01.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | no-skill | 2 | fail | [result](raw/generations/multi-mixed-ja-en--no-skill--r02.result.json) | [trace](raw/generations/multi-mixed-ja-en--no-skill--r02.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | no-skill | 3 | fail | [result](raw/generations/multi-mixed-ja-en--no-skill--r03.result.json) | [trace](raw/generations/multi-mixed-ja-en--no-skill--r03.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | no-skill | 4 | fail | [result](raw/generations/multi-mixed-ja-en--no-skill--r04.result.json) | [trace](raw/generations/multi-mixed-ja-en--no-skill--r04.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | no-skill | 5 | fail | [result](raw/generations/multi-mixed-ja-en--no-skill--r05.result.json) | [trace](raw/generations/multi-mixed-ja-en--no-skill--r05.trace.jsonl) |
| multi-zh-referent | multilingual-core | 178eaf8 | 1 | fail | [result](raw/generations/multi-zh-referent--178eaf8--r01.result.json) | [trace](raw/generations/multi-zh-referent--178eaf8--r01.trace.jsonl) |
| multi-zh-referent | multilingual-core | 178eaf8 | 2 | fail | [result](raw/generations/multi-zh-referent--178eaf8--r02.result.json) | [trace](raw/generations/multi-zh-referent--178eaf8--r02.trace.jsonl) |
| multi-zh-referent | multilingual-core | 178eaf8 | 3 | fail | [result](raw/generations/multi-zh-referent--178eaf8--r03.result.json) | [trace](raw/generations/multi-zh-referent--178eaf8--r03.trace.jsonl) |
| multi-zh-referent | multilingual-core | 178eaf8 | 4 | fail | [result](raw/generations/multi-zh-referent--178eaf8--r04.result.json) | [trace](raw/generations/multi-zh-referent--178eaf8--r04.trace.jsonl) |
| multi-zh-referent | multilingual-core | 178eaf8 | 5 | fail | [result](raw/generations/multi-zh-referent--178eaf8--r05.result.json) | [trace](raw/generations/multi-zh-referent--178eaf8--r05.trace.jsonl) |
| multi-zh-referent | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 1 | fail | [result](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.result.json) | [trace](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r01.trace.jsonl) |
| multi-zh-referent | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 2 | fail | [result](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.result.json) | [trace](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r02.trace.jsonl) |
| multi-zh-referent | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 3 | fail | [result](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.result.json) | [trace](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r03.trace.jsonl) |
| multi-zh-referent | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 4 | fail | [result](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.result.json) | [trace](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r04.trace.jsonl) |
| multi-zh-referent | multilingual-core | e8138b051b4683a90dffc5e6f8ff6ea5360a82c7 | 5 | fail | [result](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.result.json) | [trace](raw/generations/multi-zh-referent--e8138b051b4683a90dffc5e6f8ff6ea5360a82c7--r05.trace.jsonl) |
| multi-zh-referent | multilingual-core | no-skill | 1 | fail | [result](raw/generations/multi-zh-referent--no-skill--r01.result.json) | [trace](raw/generations/multi-zh-referent--no-skill--r01.trace.jsonl) |
| multi-zh-referent | multilingual-core | no-skill | 2 | fail | [result](raw/generations/multi-zh-referent--no-skill--r02.result.json) | [trace](raw/generations/multi-zh-referent--no-skill--r02.trace.jsonl) |
| multi-zh-referent | multilingual-core | no-skill | 3 | fail | [result](raw/generations/multi-zh-referent--no-skill--r03.result.json) | [trace](raw/generations/multi-zh-referent--no-skill--r03.trace.jsonl) |
| multi-zh-referent | multilingual-core | no-skill | 4 | fail | [result](raw/generations/multi-zh-referent--no-skill--r04.result.json) | [trace](raw/generations/multi-zh-referent--no-skill--r04.trace.jsonl) |
| multi-zh-referent | multilingual-core | no-skill | 5 | fail | [result](raw/generations/multi-zh-referent--no-skill--r05.result.json) | [trace](raw/generations/multi-zh-referent--no-skill--r05.trace.jsonl) |

### Blind GPT judgments

| Pair | Category | Presented | Preference | Result | Trace |
|---|---|---:|---|---|---|
| ja-ambiguous-subject--r03 | japanese | 1 | A | [result](raw/judgments/ja-ambiguous-subject--r03.result.json) | [trace](raw/judgments/ja-ambiguous-subject--r03.trace.jsonl) |
| multi-es-buried-action--r02 | multilingual-core | 2 | A | [result](raw/judgments/multi-es-buried-action--r02.result.json) | [trace](raw/judgments/multi-es-buried-action--r02.trace.jsonl) |
| ja-detached-condition--r03 | japanese | 3 | tie | [result](raw/judgments/ja-detached-condition--r03.result.json) | [trace](raw/judgments/ja-detached-condition--r03.trace.jsonl) |
| en-detached-qualification--r03 | english | 4 | B | [result](raw/judgments/en-detached-qualification--r03.result.json) | [trace](raw/judgments/en-detached-qualification--r03.trace.jsonl) |
| ja-buried-action--r01 | japanese | 5 | A | [result](raw/judgments/ja-buried-action--r01.result.json) | [trace](raw/judgments/ja-buried-action--r01.trace.jsonl) |
| en-ambiguous-referent--r03 | english | 6 | tie | [result](raw/judgments/en-ambiguous-referent--r03.result.json) | [trace](raw/judgments/en-ambiguous-referent--r03.trace.jsonl) |
| ja-register-certainty--r05 | japanese | 7 | B | [result](raw/judgments/ja-register-certainty--r05.result.json) | [trace](raw/judgments/ja-register-certainty--r05.trace.jsonl) |
| ja-register-certainty--r03 | japanese | 8 | A | [result](raw/judgments/ja-register-certainty--r03.result.json) | [trace](raw/judgments/ja-register-certainty--r03.trace.jsonl) |
| multi-zh-referent--r02 | multilingual-core | 9 | B | [result](raw/judgments/multi-zh-referent--r02.result.json) | [trace](raw/judgments/multi-zh-referent--r02.trace.jsonl) |
| en-terminology-drift--r02 | english | 10 | B | [result](raw/judgments/en-terminology-drift--r02.result.json) | [trace](raw/judgments/en-terminology-drift--r02.trace.jsonl) |
| ja-register-certainty--r04 | japanese | 11 | B | [result](raw/judgments/ja-register-certainty--r04.result.json) | [trace](raw/judgments/ja-register-certainty--r04.trace.jsonl) |
| ja-ambiguous-subject--r04 | japanese | 12 | A | [result](raw/judgments/ja-ambiguous-subject--r04.result.json) | [trace](raw/judgments/ja-ambiguous-subject--r04.trace.jsonl) |
| en-terminology-drift--r04 | english | 13 | A | [result](raw/judgments/en-terminology-drift--r04.result.json) | [trace](raw/judgments/en-terminology-drift--r04.trace.jsonl) |
| ja-register-certainty--r01 | japanese | 14 | B | [result](raw/judgments/ja-register-certainty--r01.result.json) | [trace](raw/judgments/ja-register-certainty--r01.trace.jsonl) |
| en-detached-qualification--r01 | english | 15 | B | [result](raw/judgments/en-detached-qualification--r01.result.json) | [trace](raw/judgments/en-detached-qualification--r01.trace.jsonl) |
| multi-ar-condition--r03 | multilingual-core | 16 | tie | [result](raw/judgments/multi-ar-condition--r03.result.json) | [trace](raw/judgments/multi-ar-condition--r03.trace.jsonl) |
| multi-mixed-ja-en--r05 | multilingual-core | 17 | B | [result](raw/judgments/multi-mixed-ja-en--r05.result.json) | [trace](raw/judgments/multi-mixed-ja-en--r05.trace.jsonl) |
| multi-mixed-ja-en--r01 | multilingual-core | 18 | B | [result](raw/judgments/multi-mixed-ja-en--r01.result.json) | [trace](raw/judgments/multi-mixed-ja-en--r01.trace.jsonl) |
| multi-ar-condition--r01 | multilingual-core | 19 | A | [result](raw/judgments/multi-ar-condition--r01.result.json) | [trace](raw/judgments/multi-ar-condition--r01.trace.jsonl) |
| en-terminology-drift--r01 | english | 20 | tie | [result](raw/judgments/en-terminology-drift--r01.result.json) | [trace](raw/judgments/en-terminology-drift--r01.trace.jsonl) |
| en-buried-answer--r03 | english | 21 | A | [result](raw/judgments/en-buried-answer--r03.result.json) | [trace](raw/judgments/en-buried-answer--r03.trace.jsonl) |
| multi-de-terminology--r03 | multilingual-core | 22 | A | [result](raw/judgments/multi-de-terminology--r03.result.json) | [trace](raw/judgments/multi-de-terminology--r03.trace.jsonl) |
| en-ambiguous-referent--r01 | english | 23 | B | [result](raw/judgments/en-ambiguous-referent--r01.result.json) | [trace](raw/judgments/en-ambiguous-referent--r01.trace.jsonl) |
| ja-buried-action--r03 | japanese | 24 | B | [result](raw/judgments/ja-buried-action--r03.result.json) | [trace](raw/judgments/ja-buried-action--r03.trace.jsonl) |
| ja-terminology-drift--r01 | japanese | 25 | tie | [result](raw/judgments/ja-terminology-drift--r01.result.json) | [trace](raw/judgments/ja-terminology-drift--r01.trace.jsonl) |
| ja-detached-condition--r01 | japanese | 26 | tie | [result](raw/judgments/ja-detached-condition--r01.result.json) | [trace](raw/judgments/ja-detached-condition--r01.trace.jsonl) |
| ja-terminology-drift--r03 | japanese | 27 | tie | [result](raw/judgments/ja-terminology-drift--r03.result.json) | [trace](raw/judgments/ja-terminology-drift--r03.trace.jsonl) |
| en-buried-answer--r04 | english | 28 | B | [result](raw/judgments/en-buried-answer--r04.result.json) | [trace](raw/judgments/en-buried-answer--r04.trace.jsonl) |
| ja-terminology-drift--r05 | japanese | 29 | tie | [result](raw/judgments/ja-terminology-drift--r05.result.json) | [trace](raw/judgments/ja-terminology-drift--r05.trace.jsonl) |
| multi-zh-referent--r03 | multilingual-core | 30 | B | [result](raw/judgments/multi-zh-referent--r03.result.json) | [trace](raw/judgments/multi-zh-referent--r03.trace.jsonl) |
| multi-ar-condition--r04 | multilingual-core | 31 | tie | [result](raw/judgments/multi-ar-condition--r04.result.json) | [trace](raw/judgments/multi-ar-condition--r04.trace.jsonl) |
| en-detached-qualification--r02 | english | 32 | B | [result](raw/judgments/en-detached-qualification--r02.result.json) | [trace](raw/judgments/en-detached-qualification--r02.trace.jsonl) |
| ja-buried-action--r02 | japanese | 33 | A | [result](raw/judgments/ja-buried-action--r02.result.json) | [trace](raw/judgments/ja-buried-action--r02.trace.jsonl) |
| en-register-certainty--r03 | english | 34 | B | [result](raw/judgments/en-register-certainty--r03.result.json) | [trace](raw/judgments/en-register-certainty--r03.trace.jsonl) |
| en-buried-answer--r02 | english | 35 | B | [result](raw/judgments/en-buried-answer--r02.result.json) | [trace](raw/judgments/en-buried-answer--r02.trace.jsonl) |
| en-ambiguous-referent--r05 | english | 36 | A | [result](raw/judgments/en-ambiguous-referent--r05.result.json) | [trace](raw/judgments/en-ambiguous-referent--r05.trace.jsonl) |
| ja-ambiguous-subject--r01 | japanese | 37 | B | [result](raw/judgments/ja-ambiguous-subject--r01.result.json) | [trace](raw/judgments/ja-ambiguous-subject--r01.trace.jsonl) |
| multi-es-buried-action--r04 | multilingual-core | 38 | B | [result](raw/judgments/multi-es-buried-action--r04.result.json) | [trace](raw/judgments/multi-es-buried-action--r04.trace.jsonl) |
| multi-ar-condition--r05 | multilingual-core | 39 | B | [result](raw/judgments/multi-ar-condition--r05.result.json) | [trace](raw/judgments/multi-ar-condition--r05.trace.jsonl) |
| ja-ambiguous-subject--r02 | japanese | 40 | A | [result](raw/judgments/ja-ambiguous-subject--r02.result.json) | [trace](raw/judgments/ja-ambiguous-subject--r02.trace.jsonl) |
| ja-buried-action--r04 | japanese | 41 | B | [result](raw/judgments/ja-buried-action--r04.result.json) | [trace](raw/judgments/ja-buried-action--r04.trace.jsonl) |
| en-register-certainty--r01 | english | 42 | tie | [result](raw/judgments/en-register-certainty--r01.result.json) | [trace](raw/judgments/en-register-certainty--r01.trace.jsonl) |
| multi-es-buried-action--r03 | multilingual-core | 43 | A | [result](raw/judgments/multi-es-buried-action--r03.result.json) | [trace](raw/judgments/multi-es-buried-action--r03.trace.jsonl) |
| ja-terminology-drift--r02 | japanese | 44 | tie | [result](raw/judgments/ja-terminology-drift--r02.result.json) | [trace](raw/judgments/ja-terminology-drift--r02.trace.jsonl) |
| en-register-certainty--r04 | english | 45 | B | [result](raw/judgments/en-register-certainty--r04.result.json) | [trace](raw/judgments/en-register-certainty--r04.trace.jsonl) |
| multi-de-terminology--r04 | multilingual-core | 46 | B | [result](raw/judgments/multi-de-terminology--r04.result.json) | [trace](raw/judgments/multi-de-terminology--r04.trace.jsonl) |
| ja-detached-condition--r05 | japanese | 47 | tie | [result](raw/judgments/ja-detached-condition--r05.result.json) | [trace](raw/judgments/ja-detached-condition--r05.trace.jsonl) |
| multi-zh-referent--r04 | multilingual-core | 48 | A | [result](raw/judgments/multi-zh-referent--r04.result.json) | [trace](raw/judgments/multi-zh-referent--r04.trace.jsonl) |
| en-register-certainty--r02 | english | 49 | B | [result](raw/judgments/en-register-certainty--r02.result.json) | [trace](raw/judgments/en-register-certainty--r02.trace.jsonl) |
| ja-detached-condition--r04 | japanese | 50 | tie | [result](raw/judgments/ja-detached-condition--r04.result.json) | [trace](raw/judgments/ja-detached-condition--r04.trace.jsonl) |
| ja-detached-condition--r02 | japanese | 51 | tie | [result](raw/judgments/ja-detached-condition--r02.result.json) | [trace](raw/judgments/ja-detached-condition--r02.trace.jsonl) |
| multi-mixed-ja-en--r04 | multilingual-core | 52 | B | [result](raw/judgments/multi-mixed-ja-en--r04.result.json) | [trace](raw/judgments/multi-mixed-ja-en--r04.trace.jsonl) |
| ja-ambiguous-subject--r05 | japanese | 53 | B | [result](raw/judgments/ja-ambiguous-subject--r05.result.json) | [trace](raw/judgments/ja-ambiguous-subject--r05.trace.jsonl) |
| multi-es-buried-action--r01 | multilingual-core | 54 | A | [result](raw/judgments/multi-es-buried-action--r01.result.json) | [trace](raw/judgments/multi-es-buried-action--r01.trace.jsonl) |
| multi-zh-referent--r05 | multilingual-core | 55 | A | [result](raw/judgments/multi-zh-referent--r05.result.json) | [trace](raw/judgments/multi-zh-referent--r05.trace.jsonl) |
| en-terminology-drift--r05 | english | 56 | A | [result](raw/judgments/en-terminology-drift--r05.result.json) | [trace](raw/judgments/en-terminology-drift--r05.trace.jsonl) |
| en-detached-qualification--r04 | english | 57 | B | [result](raw/judgments/en-detached-qualification--r04.result.json) | [trace](raw/judgments/en-detached-qualification--r04.trace.jsonl) |
| en-ambiguous-referent--r02 | english | 58 | tie | [result](raw/judgments/en-ambiguous-referent--r02.result.json) | [trace](raw/judgments/en-ambiguous-referent--r02.trace.jsonl) |
| en-detached-qualification--r05 | english | 59 | B | [result](raw/judgments/en-detached-qualification--r05.result.json) | [trace](raw/judgments/en-detached-qualification--r05.trace.jsonl) |
| ja-register-certainty--r02 | japanese | 60 | B | [result](raw/judgments/ja-register-certainty--r02.result.json) | [trace](raw/judgments/ja-register-certainty--r02.trace.jsonl) |
| en-ambiguous-referent--r04 | english | 61 | A | [result](raw/judgments/en-ambiguous-referent--r04.result.json) | [trace](raw/judgments/en-ambiguous-referent--r04.trace.jsonl) |
| ja-buried-action--r05 | japanese | 62 | A | [result](raw/judgments/ja-buried-action--r05.result.json) | [trace](raw/judgments/ja-buried-action--r05.trace.jsonl) |
| en-buried-answer--r05 | english | 63 | A | [result](raw/judgments/en-buried-answer--r05.result.json) | [trace](raw/judgments/en-buried-answer--r05.trace.jsonl) |
| multi-ar-condition--r02 | multilingual-core | 64 | A | [result](raw/judgments/multi-ar-condition--r02.result.json) | [trace](raw/judgments/multi-ar-condition--r02.trace.jsonl) |
| multi-zh-referent--r01 | multilingual-core | 65 | A | [result](raw/judgments/multi-zh-referent--r01.result.json) | [trace](raw/judgments/multi-zh-referent--r01.trace.jsonl) |
| en-buried-answer--r01 | english | 66 | B | [result](raw/judgments/en-buried-answer--r01.result.json) | [trace](raw/judgments/en-buried-answer--r01.trace.jsonl) |
| ja-terminology-drift--r04 | japanese | 67 | tie | [result](raw/judgments/ja-terminology-drift--r04.result.json) | [trace](raw/judgments/ja-terminology-drift--r04.trace.jsonl) |
| multi-mixed-ja-en--r03 | multilingual-core | 68 | A | [result](raw/judgments/multi-mixed-ja-en--r03.result.json) | [trace](raw/judgments/multi-mixed-ja-en--r03.trace.jsonl) |
| en-register-certainty--r05 | english | 69 | tie | [result](raw/judgments/en-register-certainty--r05.result.json) | [trace](raw/judgments/en-register-certainty--r05.trace.jsonl) |
| multi-de-terminology--r01 | multilingual-core | 70 | A | [result](raw/judgments/multi-de-terminology--r01.result.json) | [trace](raw/judgments/multi-de-terminology--r01.trace.jsonl) |
| multi-es-buried-action--r05 | multilingual-core | 71 | A | [result](raw/judgments/multi-es-buried-action--r05.result.json) | [trace](raw/judgments/multi-es-buried-action--r05.trace.jsonl) |
| multi-mixed-ja-en--r02 | multilingual-core | 72 | tie | [result](raw/judgments/multi-mixed-ja-en--r02.result.json) | [trace](raw/judgments/multi-mixed-ja-en--r02.trace.jsonl) |
| multi-de-terminology--r05 | multilingual-core | 73 | A | [result](raw/judgments/multi-de-terminology--r05.result.json) | [trace](raw/judgments/multi-de-terminology--r05.trace.jsonl) |
| multi-de-terminology--r02 | multilingual-core | 74 | B | [result](raw/judgments/multi-de-terminology--r02.result.json) | [trace](raw/judgments/multi-de-terminology--r02.trace.jsonl) |
| en-terminology-drift--r03 | english | 75 | A | [result](raw/judgments/en-terminology-drift--r03.result.json) | [trace](raw/judgments/en-terminology-drift--r03.trace.jsonl) |
