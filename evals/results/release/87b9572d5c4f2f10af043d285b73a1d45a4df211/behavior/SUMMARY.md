# Clarity-behavior evaluation

This injected-behavior evaluation reports generation arms separately and blind-compares `178eaf8 vs 87b9572d5c4f2f10af043d285b73a1d45a4df211`. It is not automatic-routing evidence.
Frozen scenarios: `behavior-v1`; 5 repetitions per scenario and arm.

English, Japanese, and multilingual-core evidence is reported separately; there is no pooled headline score.

## English

Generations: 75; blind comparisons: 25.

### Deterministic evidence

Exact-literal checks provide preservation evidence only; they do not establish semantic correctness or clarity.

| Arm | Runs | Missing outputs | Protected | Facts | Numbers | Constraints | Conditions |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | 25 | 0 | 0 | 5 | 5 | 0 | 5 |
| 178eaf8 | 25 | 0 | 0 | 5 | 5 | 0 | 5 |
| 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 25 | 0 | 0 | 5 | 5 | 0 | 5 |

### GPT-judged evidence

Blind, seeded A/B judgments are model evidence and are separate from deterministic checks.

| Arm | Preservation | First-pass understanding | Core structure | Critical failures | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | n/a | n/a | n/a | 0 | 0 | 0 | 0 |
| 178eaf8 | 3.920 | 4.960 | 4.640 | 13 | 2 | 19 | 4 |
| 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4.960 | 5.000 | 4.960 | 0 | 19 | 2 | 4 |

## Japanese

Generations: 75; blind comparisons: 25.

### Deterministic evidence

Exact-literal checks provide preservation evidence only; they do not establish semantic correctness or clarity.

| Arm | Runs | Missing outputs | Protected | Facts | Numbers | Constraints | Conditions |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | 25 | 0 | 0 | 10 | 2 | 0 | 0 |
| 178eaf8 | 25 | 0 | 0 | 10 | 3 | 0 | 0 |
| 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 25 | 0 | 0 | 10 | 4 | 0 | 0 |

### GPT-judged evidence

Blind, seeded A/B judgments are model evidence and are separate from deterministic checks.

| Arm | Preservation | First-pass understanding | Core structure | Critical failures | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | n/a | n/a | n/a | 0 | 0 | 0 | 0 |
| 178eaf8 | 4.400 | 5.000 | 4.840 | 3 | 4 | 16 | 5 |
| 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5.000 | 5.000 | 5.000 | 0 | 16 | 4 | 5 |

## Multilingual core

Generations: 75; blind comparisons: 25.

### Deterministic evidence

Exact-literal checks provide preservation evidence only; they do not establish semantic correctness or clarity.

| Arm | Runs | Missing outputs | Protected | Facts | Numbers | Constraints | Conditions |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | 25 | 0 | 0 | 5 | 0 | 3 | 5 |
| 178eaf8 | 25 | 0 | 1 | 5 | 0 | 5 | 2 |
| 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 25 | 0 | 0 | 5 | 0 | 0 | 5 |

### GPT-judged evidence

Blind, seeded A/B judgments are model evidence and are separate from deterministic checks.

| Arm | Preservation | First-pass understanding | Core structure | Critical failures | Wins | Losses | Ties |
|---|---:|---:|---:|---:|---:|---:|---:|
| no-skill | n/a | n/a | n/a | 0 | 0 | 0 | 0 |
| 178eaf8 | 4.400 | n/a | 4.480 | 5 | 2 | 19 | 4 |
| 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5.000 | n/a | 4.920 | 0 | 19 | 2 | 4 |

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
| en-ambiguous-referent | english | 178eaf8 | 4 | pass | [result](raw/generations/en-ambiguous-referent--178eaf8--r04.result.json) | [trace](raw/generations/en-ambiguous-referent--178eaf8--r04.trace.jsonl) |
| en-ambiguous-referent | english | 178eaf8 | 5 | pass | [result](raw/generations/en-ambiguous-referent--178eaf8--r05.result.json) | [trace](raw/generations/en-ambiguous-referent--178eaf8--r05.trace.jsonl) |
| en-ambiguous-referent | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| en-ambiguous-referent | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| en-ambiguous-referent | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| en-ambiguous-referent | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| en-ambiguous-referent | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/en-ambiguous-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| en-buried-answer | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| en-buried-answer | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| en-buried-answer | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| en-buried-answer | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| en-buried-answer | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/en-buried-answer--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| en-detached-qualification | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | fail | [result](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| en-detached-qualification | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | fail | [result](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| en-detached-qualification | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | fail | [result](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| en-detached-qualification | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | fail | [result](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| en-detached-qualification | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | fail | [result](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/en-detached-qualification--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| en-register-certainty | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | fail | [result](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| en-register-certainty | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | fail | [result](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| en-register-certainty | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | fail | [result](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| en-register-certainty | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | fail | [result](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| en-register-certainty | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | fail | [result](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/en-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| en-terminology-drift | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| en-terminology-drift | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| en-terminology-drift | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| en-terminology-drift | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| en-terminology-drift | english | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/en-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| ja-ambiguous-subject | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | fail | [result](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| ja-ambiguous-subject | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | fail | [result](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| ja-ambiguous-subject | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | fail | [result](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| ja-ambiguous-subject | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | fail | [result](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| ja-ambiguous-subject | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | fail | [result](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/ja-ambiguous-subject--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| ja-buried-action | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| ja-buried-action | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| ja-buried-action | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| ja-buried-action | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| ja-buried-action | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/ja-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| ja-detached-condition | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| ja-detached-condition | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| ja-detached-condition | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| ja-detached-condition | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| ja-detached-condition | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/ja-detached-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| ja-register-certainty | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | fail | [result](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| ja-register-certainty | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | fail | [result](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| ja-register-certainty | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | fail | [result](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| ja-register-certainty | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | fail | [result](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| ja-register-certainty | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | fail | [result](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/ja-register-certainty--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| ja-terminology-drift | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| ja-terminology-drift | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| ja-terminology-drift | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| ja-terminology-drift | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| ja-terminology-drift | japanese | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/ja-terminology-drift--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| multi-ar-condition | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| multi-ar-condition | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| multi-ar-condition | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| multi-ar-condition | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| multi-ar-condition | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/multi-ar-condition--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| multi-de-terminology | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| multi-de-terminology | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| multi-de-terminology | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| multi-de-terminology | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| multi-de-terminology | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/multi-de-terminology--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 1 | pass | [result](raw/generations/multi-de-terminology--no-skill--r01.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r01.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 2 | fail | [result](raw/generations/multi-de-terminology--no-skill--r02.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r02.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 3 | pass | [result](raw/generations/multi-de-terminology--no-skill--r03.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r03.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 4 | fail | [result](raw/generations/multi-de-terminology--no-skill--r04.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r04.trace.jsonl) |
| multi-de-terminology | multilingual-core | no-skill | 5 | fail | [result](raw/generations/multi-de-terminology--no-skill--r05.result.json) | [trace](raw/generations/multi-de-terminology--no-skill--r05.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 1 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r01.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r01.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 2 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r02.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r02.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 3 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r03.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r03.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 4 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r04.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r04.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 178eaf8 | 5 | pass | [result](raw/generations/multi-es-buried-action--178eaf8--r05.result.json) | [trace](raw/generations/multi-es-buried-action--178eaf8--r05.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | pass | [result](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | pass | [result](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | pass | [result](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | pass | [result](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| multi-es-buried-action | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | pass | [result](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/multi-es-buried-action--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 1 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r01.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r01.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 2 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r02.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r02.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 3 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r03.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r03.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 4 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r04.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r04.trace.jsonl) |
| multi-es-buried-action | multilingual-core | no-skill | 5 | pass | [result](raw/generations/multi-es-buried-action--no-skill--r05.result.json) | [trace](raw/generations/multi-es-buried-action--no-skill--r05.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 1 | fail | [result](raw/generations/multi-mixed-ja-en--178eaf8--r01.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r01.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 2 | fail | [result](raw/generations/multi-mixed-ja-en--178eaf8--r02.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r02.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 3 | pass | [result](raw/generations/multi-mixed-ja-en--178eaf8--r03.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r03.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 4 | pass | [result](raw/generations/multi-mixed-ja-en--178eaf8--r04.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r04.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 178eaf8 | 5 | pass | [result](raw/generations/multi-mixed-ja-en--178eaf8--r05.result.json) | [trace](raw/generations/multi-mixed-ja-en--178eaf8--r05.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | fail | [result](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | fail | [result](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | fail | [result](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | fail | [result](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| multi-mixed-ja-en | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | fail | [result](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/multi-mixed-ja-en--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| multi-zh-referent | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 1 | fail | [result](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.result.json) | [trace](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r01.trace.jsonl) |
| multi-zh-referent | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 2 | fail | [result](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.result.json) | [trace](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r02.trace.jsonl) |
| multi-zh-referent | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 3 | fail | [result](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.result.json) | [trace](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r03.trace.jsonl) |
| multi-zh-referent | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 4 | fail | [result](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.result.json) | [trace](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r04.trace.jsonl) |
| multi-zh-referent | multilingual-core | 87b9572d5c4f2f10af043d285b73a1d45a4df211 | 5 | fail | [result](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.result.json) | [trace](raw/generations/multi-zh-referent--87b9572d5c4f2f10af043d285b73a1d45a4df211--r05.trace.jsonl) |
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
| en-terminology-drift--r01 | english | 20 | B | [result](raw/judgments/en-terminology-drift--r01.result.json) | [trace](raw/judgments/en-terminology-drift--r01.trace.jsonl) |
| en-buried-answer--r03 | english | 21 | A | [result](raw/judgments/en-buried-answer--r03.result.json) | [trace](raw/judgments/en-buried-answer--r03.trace.jsonl) |
| multi-de-terminology--r03 | multilingual-core | 22 | A | [result](raw/judgments/multi-de-terminology--r03.result.json) | [trace](raw/judgments/multi-de-terminology--r03.trace.jsonl) |
| en-ambiguous-referent--r01 | english | 23 | B | [result](raw/judgments/en-ambiguous-referent--r01.result.json) | [trace](raw/judgments/en-ambiguous-referent--r01.trace.jsonl) |
| ja-buried-action--r03 | japanese | 24 | A | [result](raw/judgments/ja-buried-action--r03.result.json) | [trace](raw/judgments/ja-buried-action--r03.trace.jsonl) |
| ja-terminology-drift--r01 | japanese | 25 | B | [result](raw/judgments/ja-terminology-drift--r01.result.json) | [trace](raw/judgments/ja-terminology-drift--r01.trace.jsonl) |
| ja-detached-condition--r01 | japanese | 26 | tie | [result](raw/judgments/ja-detached-condition--r01.result.json) | [trace](raw/judgments/ja-detached-condition--r01.trace.jsonl) |
| ja-terminology-drift--r03 | japanese | 27 | A | [result](raw/judgments/ja-terminology-drift--r03.result.json) | [trace](raw/judgments/ja-terminology-drift--r03.trace.jsonl) |
| en-buried-answer--r04 | english | 28 | B | [result](raw/judgments/en-buried-answer--r04.result.json) | [trace](raw/judgments/en-buried-answer--r04.trace.jsonl) |
| ja-terminology-drift--r05 | japanese | 29 | B | [result](raw/judgments/ja-terminology-drift--r05.result.json) | [trace](raw/judgments/ja-terminology-drift--r05.trace.jsonl) |
| multi-zh-referent--r03 | multilingual-core | 30 | A | [result](raw/judgments/multi-zh-referent--r03.result.json) | [trace](raw/judgments/multi-zh-referent--r03.trace.jsonl) |
| multi-ar-condition--r04 | multilingual-core | 31 | A | [result](raw/judgments/multi-ar-condition--r04.result.json) | [trace](raw/judgments/multi-ar-condition--r04.trace.jsonl) |
| en-detached-qualification--r02 | english | 32 | B | [result](raw/judgments/en-detached-qualification--r02.result.json) | [trace](raw/judgments/en-detached-qualification--r02.trace.jsonl) |
| ja-buried-action--r02 | japanese | 33 | B | [result](raw/judgments/ja-buried-action--r02.result.json) | [trace](raw/judgments/ja-buried-action--r02.trace.jsonl) |
| en-register-certainty--r03 | english | 34 | tie | [result](raw/judgments/en-register-certainty--r03.result.json) | [trace](raw/judgments/en-register-certainty--r03.trace.jsonl) |
| en-buried-answer--r02 | english | 35 | B | [result](raw/judgments/en-buried-answer--r02.result.json) | [trace](raw/judgments/en-buried-answer--r02.trace.jsonl) |
| en-ambiguous-referent--r05 | english | 36 | B | [result](raw/judgments/en-ambiguous-referent--r05.result.json) | [trace](raw/judgments/en-ambiguous-referent--r05.trace.jsonl) |
| ja-ambiguous-subject--r01 | japanese | 37 | B | [result](raw/judgments/ja-ambiguous-subject--r01.result.json) | [trace](raw/judgments/ja-ambiguous-subject--r01.trace.jsonl) |
| multi-es-buried-action--r04 | multilingual-core | 38 | A | [result](raw/judgments/multi-es-buried-action--r04.result.json) | [trace](raw/judgments/multi-es-buried-action--r04.trace.jsonl) |
| multi-ar-condition--r05 | multilingual-core | 39 | tie | [result](raw/judgments/multi-ar-condition--r05.result.json) | [trace](raw/judgments/multi-ar-condition--r05.trace.jsonl) |
| ja-ambiguous-subject--r02 | japanese | 40 | A | [result](raw/judgments/ja-ambiguous-subject--r02.result.json) | [trace](raw/judgments/ja-ambiguous-subject--r02.trace.jsonl) |
| ja-buried-action--r04 | japanese | 41 | A | [result](raw/judgments/ja-buried-action--r04.result.json) | [trace](raw/judgments/ja-buried-action--r04.trace.jsonl) |
| en-register-certainty--r01 | english | 42 | B | [result](raw/judgments/en-register-certainty--r01.result.json) | [trace](raw/judgments/en-register-certainty--r01.trace.jsonl) |
| multi-es-buried-action--r03 | multilingual-core | 43 | A | [result](raw/judgments/multi-es-buried-action--r03.result.json) | [trace](raw/judgments/multi-es-buried-action--r03.trace.jsonl) |
| ja-terminology-drift--r02 | japanese | 44 | A | [result](raw/judgments/ja-terminology-drift--r02.result.json) | [trace](raw/judgments/ja-terminology-drift--r02.trace.jsonl) |
| en-register-certainty--r04 | english | 45 | B | [result](raw/judgments/en-register-certainty--r04.result.json) | [trace](raw/judgments/en-register-certainty--r04.trace.jsonl) |
| multi-de-terminology--r04 | multilingual-core | 46 | B | [result](raw/judgments/multi-de-terminology--r04.result.json) | [trace](raw/judgments/multi-de-terminology--r04.trace.jsonl) |
| ja-detached-condition--r05 | japanese | 47 | tie | [result](raw/judgments/ja-detached-condition--r05.result.json) | [trace](raw/judgments/ja-detached-condition--r05.trace.jsonl) |
| multi-zh-referent--r04 | multilingual-core | 48 | A | [result](raw/judgments/multi-zh-referent--r04.result.json) | [trace](raw/judgments/multi-zh-referent--r04.trace.jsonl) |
| en-register-certainty--r02 | english | 49 | A | [result](raw/judgments/en-register-certainty--r02.result.json) | [trace](raw/judgments/en-register-certainty--r02.trace.jsonl) |
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
| multi-ar-condition--r02 | multilingual-core | 64 | tie | [result](raw/judgments/multi-ar-condition--r02.result.json) | [trace](raw/judgments/multi-ar-condition--r02.trace.jsonl) |
| multi-zh-referent--r01 | multilingual-core | 65 | A | [result](raw/judgments/multi-zh-referent--r01.result.json) | [trace](raw/judgments/multi-zh-referent--r01.trace.jsonl) |
| en-buried-answer--r01 | english | 66 | B | [result](raw/judgments/en-buried-answer--r01.result.json) | [trace](raw/judgments/en-buried-answer--r01.trace.jsonl) |
| ja-terminology-drift--r04 | japanese | 67 | A | [result](raw/judgments/ja-terminology-drift--r04.result.json) | [trace](raw/judgments/ja-terminology-drift--r04.trace.jsonl) |
| multi-mixed-ja-en--r03 | multilingual-core | 68 | tie | [result](raw/judgments/multi-mixed-ja-en--r03.result.json) | [trace](raw/judgments/multi-mixed-ja-en--r03.trace.jsonl) |
| en-register-certainty--r05 | english | 69 | tie | [result](raw/judgments/en-register-certainty--r05.result.json) | [trace](raw/judgments/en-register-certainty--r05.trace.jsonl) |
| multi-de-terminology--r01 | multilingual-core | 70 | A | [result](raw/judgments/multi-de-terminology--r01.result.json) | [trace](raw/judgments/multi-de-terminology--r01.trace.jsonl) |
| multi-es-buried-action--r05 | multilingual-core | 71 | A | [result](raw/judgments/multi-es-buried-action--r05.result.json) | [trace](raw/judgments/multi-es-buried-action--r05.trace.jsonl) |
| multi-mixed-ja-en--r02 | multilingual-core | 72 | B | [result](raw/judgments/multi-mixed-ja-en--r02.result.json) | [trace](raw/judgments/multi-mixed-ja-en--r02.trace.jsonl) |
| multi-de-terminology--r05 | multilingual-core | 73 | A | [result](raw/judgments/multi-de-terminology--r05.result.json) | [trace](raw/judgments/multi-de-terminology--r05.trace.jsonl) |
| multi-de-terminology--r02 | multilingual-core | 74 | B | [result](raw/judgments/multi-de-terminology--r02.result.json) | [trace](raw/judgments/multi-de-terminology--r02.trace.jsonl) |
| en-terminology-drift--r03 | english | 75 | A | [result](raw/judgments/en-terminology-drift--r03.result.json) | [trace](raw/judgments/en-terminology-drift--r03.trace.jsonl) |
