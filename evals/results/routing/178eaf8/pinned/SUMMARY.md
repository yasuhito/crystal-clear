# Automatic activation baseline — pinned

- Inventory role: **formal**
- Inventory snapshot: `pinned-routing-inventory-v1`
- Frozen scenarios: `routing-v1-frozen-2026-03-24` (40 scenarios; 12 held-out)
- Baseline skill revision: `178eaf8`
- Runs: 200
- Recall across expected-positive runs: 76.8% (96/125)
- Precision: 100.0%
- False-positive rate across all expected-negative runs: 0.0% (0/75)
- Unrelated-control false-positive rate: 0.0% (0/50)

This pinned inventory is the only result eligible for later pass/fail comparison.

## Category results

| Category | Runs | Recall | Precision | False-positive rate | Activation rate |
|---|---:|---:|---:|---:|---:|
| boundary | 50 | 80.0% | 100.0% | 0.0% | 40.0% |
| complex-communication | 50 | 100.0% | 100.0% | n/a | 100.0% |
| explicit-request | 50 | 52.0% | 100.0% | n/a | 52.0% |
| unrelated-control | 50 | n/a | n/a | 0.0% | 0.0% |

## Frozen split results

| Split | Runs | Recall | False-positive rate |
|---|---:|---:|---:|
| train | 140 | 70.0% | 0.0% |
| held-out | 60 | 94.3% | 0.0% |

## Selection outcomes

`not-selected` means Crystal Clear was not read. `selected-with-little-visible-change` means it was read but the final output was identical or at least 98% similar to the supplied source text. Generated outputs without a source text are reported as `selected-effect-not-deterministically-assessed`; the report does not infer a behavioral effect merely from selection.

- not-selected: 104
- selected-with-little-visible-change: 0
- selected-with-visible-change: 26
- selected-effect-not-deterministically-assessed: 70

## Raw runs

| Scenario | Category | Split | Repeat | Expected | Observed | Outcome | Trace | Result |
|---|---|---|---:|---|---|---|---|---|
| boundary-code-doc-held | boundary | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r01.trace.jsonl) | [result](raw/boundary-code-doc-held--r01.result.json) |
| boundary-code-doc-held | boundary | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r02.trace.jsonl) | [result](raw/boundary-code-doc-held--r02.result.json) |
| boundary-code-doc-held | boundary | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r03.trace.jsonl) | [result](raw/boundary-code-doc-held--r03.result.json) |
| boundary-code-doc-held | boundary | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r04.trace.jsonl) | [result](raw/boundary-code-doc-held--r04.result.json) |
| boundary-code-doc-held | boundary | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-code-doc-held--r05.trace.jsonl) | [result](raw/boundary-code-doc-held--r05.result.json) |
| boundary-code-only-held | boundary | held-out | 1 | false | false | not-selected | [trace](raw/boundary-code-only-held--r01.trace.jsonl) | [result](raw/boundary-code-only-held--r01.result.json) |
| boundary-code-only-held | boundary | held-out | 2 | false | false | not-selected | [trace](raw/boundary-code-only-held--r02.trace.jsonl) | [result](raw/boundary-code-only-held--r02.result.json) |
| boundary-code-only-held | boundary | held-out | 3 | false | false | not-selected | [trace](raw/boundary-code-only-held--r03.trace.jsonl) | [result](raw/boundary-code-only-held--r03.result.json) |
| boundary-code-only-held | boundary | held-out | 4 | false | false | not-selected | [trace](raw/boundary-code-only-held--r04.trace.jsonl) | [result](raw/boundary-code-only-held--r04.result.json) |
| boundary-code-only-held | boundary | held-out | 5 | false | false | not-selected | [trace](raw/boundary-code-only-held--r05.trace.jsonl) | [result](raw/boundary-code-only-held--r05.result.json) |
| boundary-creative-ambiguity-intentional | boundary | train | 1 | false | false | not-selected | [trace](raw/boundary-creative-ambiguity-intentional--r01.trace.jsonl) | [result](raw/boundary-creative-ambiguity-intentional--r01.result.json) |
| boundary-creative-ambiguity-intentional | boundary | train | 2 | false | false | not-selected | [trace](raw/boundary-creative-ambiguity-intentional--r02.trace.jsonl) | [result](raw/boundary-creative-ambiguity-intentional--r02.result.json) |
| boundary-creative-ambiguity-intentional | boundary | train | 3 | false | false | not-selected | [trace](raw/boundary-creative-ambiguity-intentional--r03.trace.jsonl) | [result](raw/boundary-creative-ambiguity-intentional--r03.result.json) |
| boundary-creative-ambiguity-intentional | boundary | train | 4 | false | false | not-selected | [trace](raw/boundary-creative-ambiguity-intentional--r04.trace.jsonl) | [result](raw/boundary-creative-ambiguity-intentional--r04.result.json) |
| boundary-creative-ambiguity-intentional | boundary | train | 5 | false | false | not-selected | [trace](raw/boundary-creative-ambiguity-intentional--r05.trace.jsonl) | [result](raw/boundary-creative-ambiguity-intentional--r05.result.json) |
| boundary-creative-clarity-primary | boundary | train | 1 | true | false | not-selected | [trace](raw/boundary-creative-clarity-primary--r01.trace.jsonl) | [result](raw/boundary-creative-clarity-primary--r01.result.json) |
| boundary-creative-clarity-primary | boundary | train | 2 | true | false | not-selected | [trace](raw/boundary-creative-clarity-primary--r02.trace.jsonl) | [result](raw/boundary-creative-clarity-primary--r02.result.json) |
| boundary-creative-clarity-primary | boundary | train | 3 | true | false | not-selected | [trace](raw/boundary-creative-clarity-primary--r03.trace.jsonl) | [result](raw/boundary-creative-clarity-primary--r03.result.json) |
| boundary-creative-clarity-primary | boundary | train | 4 | true | false | not-selected | [trace](raw/boundary-creative-clarity-primary--r04.trace.jsonl) | [result](raw/boundary-creative-clarity-primary--r04.result.json) |
| boundary-creative-clarity-primary | boundary | train | 5 | true | false | not-selected | [trace](raw/boundary-creative-clarity-primary--r05.trace.jsonl) | [result](raw/boundary-creative-clarity-primary--r05.result.json) |
| boundary-error-code-incidental | boundary | train | 1 | false | false | not-selected | [trace](raw/boundary-error-code-incidental--r01.trace.jsonl) | [result](raw/boundary-error-code-incidental--r01.result.json) |
| boundary-error-code-incidental | boundary | train | 2 | false | false | not-selected | [trace](raw/boundary-error-code-incidental--r02.trace.jsonl) | [result](raw/boundary-error-code-incidental--r02.result.json) |
| boundary-error-code-incidental | boundary | train | 3 | false | false | not-selected | [trace](raw/boundary-error-code-incidental--r03.trace.jsonl) | [result](raw/boundary-error-code-incidental--r03.result.json) |
| boundary-error-code-incidental | boundary | train | 4 | false | false | not-selected | [trace](raw/boundary-error-code-incidental--r04.trace.jsonl) | [result](raw/boundary-error-code-incidental--r04.result.json) |
| boundary-error-code-incidental | boundary | train | 5 | false | false | not-selected | [trace](raw/boundary-error-code-incidental--r05.trace.jsonl) | [result](raw/boundary-error-code-incidental--r05.result.json) |
| boundary-error-copy-primary | boundary | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-error-copy-primary--r01.trace.jsonl) | [result](raw/boundary-error-copy-primary--r01.result.json) |
| boundary-error-copy-primary | boundary | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-error-copy-primary--r02.trace.jsonl) | [result](raw/boundary-error-copy-primary--r02.result.json) |
| boundary-error-copy-primary | boundary | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-error-copy-primary--r03.trace.jsonl) | [result](raw/boundary-error-copy-primary--r03.result.json) |
| boundary-error-copy-primary | boundary | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-error-copy-primary--r04.trace.jsonl) | [result](raw/boundary-error-copy-primary--r04.result.json) |
| boundary-error-copy-primary | boundary | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-error-copy-primary--r05.trace.jsonl) | [result](raw/boundary-error-copy-primary--r05.result.json) |
| boundary-ja-data-held | boundary | held-out | 1 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r01.trace.jsonl) | [result](raw/boundary-ja-data-held--r01.result.json) |
| boundary-ja-data-held | boundary | held-out | 2 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r02.trace.jsonl) | [result](raw/boundary-ja-data-held--r02.result.json) |
| boundary-ja-data-held | boundary | held-out | 3 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r03.trace.jsonl) | [result](raw/boundary-ja-data-held--r03.result.json) |
| boundary-ja-data-held | boundary | held-out | 4 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r04.trace.jsonl) | [result](raw/boundary-ja-data-held--r04.result.json) |
| boundary-ja-data-held | boundary | held-out | 5 | false | false | not-selected | [trace](raw/boundary-ja-data-held--r05.trace.jsonl) | [result](raw/boundary-ja-data-held--r05.result.json) |
| boundary-ja-status-primary | boundary | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-ja-status-primary--r01.trace.jsonl) | [result](raw/boundary-ja-status-primary--r01.result.json) |
| boundary-ja-status-primary | boundary | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-ja-status-primary--r02.trace.jsonl) | [result](raw/boundary-ja-status-primary--r02.result.json) |
| boundary-ja-status-primary | boundary | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-ja-status-primary--r03.trace.jsonl) | [result](raw/boundary-ja-status-primary--r03.result.json) |
| boundary-ja-status-primary | boundary | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-ja-status-primary--r04.trace.jsonl) | [result](raw/boundary-ja-status-primary--r04.result.json) |
| boundary-ja-status-primary | boundary | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-ja-status-primary--r05.trace.jsonl) | [result](raw/boundary-ja-status-primary--r05.result.json) |
| boundary-research-data-incidental | boundary | train | 1 | false | false | not-selected | [trace](raw/boundary-research-data-incidental--r01.trace.jsonl) | [result](raw/boundary-research-data-incidental--r01.result.json) |
| boundary-research-data-incidental | boundary | train | 2 | false | false | not-selected | [trace](raw/boundary-research-data-incidental--r02.trace.jsonl) | [result](raw/boundary-research-data-incidental--r02.result.json) |
| boundary-research-data-incidental | boundary | train | 3 | false | false | not-selected | [trace](raw/boundary-research-data-incidental--r03.trace.jsonl) | [result](raw/boundary-research-data-incidental--r03.result.json) |
| boundary-research-data-incidental | boundary | train | 4 | false | false | not-selected | [trace](raw/boundary-research-data-incidental--r04.trace.jsonl) | [result](raw/boundary-research-data-incidental--r04.result.json) |
| boundary-research-data-incidental | boundary | train | 5 | false | false | not-selected | [trace](raw/boundary-research-data-incidental--r05.trace.jsonl) | [result](raw/boundary-research-data-incidental--r05.result.json) |
| boundary-research-summary-primary | boundary | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-research-summary-primary--r01.trace.jsonl) | [result](raw/boundary-research-summary-primary--r01.result.json) |
| boundary-research-summary-primary | boundary | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-research-summary-primary--r02.trace.jsonl) | [result](raw/boundary-research-summary-primary--r02.result.json) |
| boundary-research-summary-primary | boundary | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-research-summary-primary--r03.trace.jsonl) | [result](raw/boundary-research-summary-primary--r03.result.json) |
| boundary-research-summary-primary | boundary | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-research-summary-primary--r04.trace.jsonl) | [result](raw/boundary-research-summary-primary--r04.result.json) |
| boundary-research-summary-primary | boundary | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/boundary-research-summary-primary--r05.trace.jsonl) | [result](raw/boundary-research-summary-primary--r05.result.json) |
| complex-en-agent-instructions | complex-communication | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-agent-instructions--r01.trace.jsonl) | [result](raw/complex-en-agent-instructions--r01.result.json) |
| complex-en-agent-instructions | complex-communication | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-agent-instructions--r02.trace.jsonl) | [result](raw/complex-en-agent-instructions--r02.result.json) |
| complex-en-agent-instructions | complex-communication | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-agent-instructions--r03.trace.jsonl) | [result](raw/complex-en-agent-instructions--r03.result.json) |
| complex-en-agent-instructions | complex-communication | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-agent-instructions--r04.trace.jsonl) | [result](raw/complex-en-agent-instructions--r04.result.json) |
| complex-en-agent-instructions | complex-communication | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-agent-instructions--r05.trace.jsonl) | [result](raw/complex-en-agent-instructions--r05.result.json) |
| complex-en-procedure | complex-communication | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-procedure--r01.trace.jsonl) | [result](raw/complex-en-procedure--r01.result.json) |
| complex-en-procedure | complex-communication | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-procedure--r02.trace.jsonl) | [result](raw/complex-en-procedure--r02.result.json) |
| complex-en-procedure | complex-communication | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-procedure--r03.trace.jsonl) | [result](raw/complex-en-procedure--r03.result.json) |
| complex-en-procedure | complex-communication | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-procedure--r04.trace.jsonl) | [result](raw/complex-en-procedure--r04.result.json) |
| complex-en-procedure | complex-communication | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-procedure--r05.trace.jsonl) | [result](raw/complex-en-procedure--r05.result.json) |
| complex-en-proposal | complex-communication | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-proposal--r01.trace.jsonl) | [result](raw/complex-en-proposal--r01.result.json) |
| complex-en-proposal | complex-communication | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-proposal--r02.trace.jsonl) | [result](raw/complex-en-proposal--r02.result.json) |
| complex-en-proposal | complex-communication | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-proposal--r03.trace.jsonl) | [result](raw/complex-en-proposal--r03.result.json) |
| complex-en-proposal | complex-communication | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-proposal--r04.trace.jsonl) | [result](raw/complex-en-proposal--r04.result.json) |
| complex-en-proposal | complex-communication | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-proposal--r05.trace.jsonl) | [result](raw/complex-en-proposal--r05.result.json) |
| complex-en-readme | complex-communication | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-readme--r01.trace.jsonl) | [result](raw/complex-en-readme--r01.result.json) |
| complex-en-readme | complex-communication | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-readme--r02.trace.jsonl) | [result](raw/complex-en-readme--r02.result.json) |
| complex-en-readme | complex-communication | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-readme--r03.trace.jsonl) | [result](raw/complex-en-readme--r03.result.json) |
| complex-en-readme | complex-communication | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-readme--r04.trace.jsonl) | [result](raw/complex-en-readme--r04.result.json) |
| complex-en-readme | complex-communication | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-readme--r05.trace.jsonl) | [result](raw/complex-en-readme--r05.result.json) |
| complex-en-report-held | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r01.trace.jsonl) | [result](raw/complex-en-report-held--r01.result.json) |
| complex-en-report-held | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r02.trace.jsonl) | [result](raw/complex-en-report-held--r02.result.json) |
| complex-en-report-held | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r03.trace.jsonl) | [result](raw/complex-en-report-held--r03.result.json) |
| complex-en-report-held | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r04.trace.jsonl) | [result](raw/complex-en-report-held--r04.result.json) |
| complex-en-report-held | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-report-held--r05.trace.jsonl) | [result](raw/complex-en-report-held--r05.result.json) |
| complex-en-skill-held | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r01.trace.jsonl) | [result](raw/complex-en-skill-held--r01.result.json) |
| complex-en-skill-held | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r02.trace.jsonl) | [result](raw/complex-en-skill-held--r02.result.json) |
| complex-en-skill-held | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r03.trace.jsonl) | [result](raw/complex-en-skill-held--r03.result.json) |
| complex-en-skill-held | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r04.trace.jsonl) | [result](raw/complex-en-skill-held--r04.result.json) |
| complex-en-skill-held | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-skill-held--r05.trace.jsonl) | [result](raw/complex-en-skill-held--r05.result.json) |
| complex-en-ui-errors | complex-communication | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-ui-errors--r01.trace.jsonl) | [result](raw/complex-en-ui-errors--r01.result.json) |
| complex-en-ui-errors | complex-communication | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-ui-errors--r02.trace.jsonl) | [result](raw/complex-en-ui-errors--r02.result.json) |
| complex-en-ui-errors | complex-communication | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-ui-errors--r03.trace.jsonl) | [result](raw/complex-en-ui-errors--r03.result.json) |
| complex-en-ui-errors | complex-communication | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-ui-errors--r04.trace.jsonl) | [result](raw/complex-en-ui-errors--r04.result.json) |
| complex-en-ui-errors | complex-communication | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-en-ui-errors--r05.trace.jsonl) | [result](raw/complex-en-ui-errors--r05.result.json) |
| complex-ja-business-email | complex-communication | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-business-email--r01.trace.jsonl) | [result](raw/complex-ja-business-email--r01.result.json) |
| complex-ja-business-email | complex-communication | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-business-email--r02.trace.jsonl) | [result](raw/complex-ja-business-email--r02.result.json) |
| complex-ja-business-email | complex-communication | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-business-email--r03.trace.jsonl) | [result](raw/complex-ja-business-email--r03.result.json) |
| complex-ja-business-email | complex-communication | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-business-email--r04.trace.jsonl) | [result](raw/complex-ja-business-email--r04.result.json) |
| complex-ja-business-email | complex-communication | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-business-email--r05.trace.jsonl) | [result](raw/complex-ja-business-email--r05.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r01.trace.jsonl) | [result](raw/complex-ja-procedure-held--r01.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r02.trace.jsonl) | [result](raw/complex-ja-procedure-held--r02.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r03.trace.jsonl) | [result](raw/complex-ja-procedure-held--r03.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r04.trace.jsonl) | [result](raw/complex-ja-procedure-held--r04.result.json) |
| complex-ja-procedure-held | complex-communication | held-out | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-ja-procedure-held--r05.trace.jsonl) | [result](raw/complex-ja-procedure-held--r05.result.json) |
| complex-mixed-terminology | complex-communication | train | 1 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-mixed-terminology--r01.trace.jsonl) | [result](raw/complex-mixed-terminology--r01.result.json) |
| complex-mixed-terminology | complex-communication | train | 2 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-mixed-terminology--r02.trace.jsonl) | [result](raw/complex-mixed-terminology--r02.result.json) |
| complex-mixed-terminology | complex-communication | train | 3 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-mixed-terminology--r03.trace.jsonl) | [result](raw/complex-mixed-terminology--r03.result.json) |
| complex-mixed-terminology | complex-communication | train | 4 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-mixed-terminology--r04.trace.jsonl) | [result](raw/complex-mixed-terminology--r04.result.json) |
| complex-mixed-terminology | complex-communication | train | 5 | true | true | selected-effect-not-deterministically-assessed | [trace](raw/complex-mixed-terminology--r05.trace.jsonl) | [result](raw/complex-mixed-terminology--r05.result.json) |
| control-code-change | unrelated-control | train | 1 | false | false | not-selected | [trace](raw/control-code-change--r01.trace.jsonl) | [result](raw/control-code-change--r01.result.json) |
| control-code-change | unrelated-control | train | 2 | false | false | not-selected | [trace](raw/control-code-change--r02.trace.jsonl) | [result](raw/control-code-change--r02.result.json) |
| control-code-change | unrelated-control | train | 3 | false | false | not-selected | [trace](raw/control-code-change--r03.trace.jsonl) | [result](raw/control-code-change--r03.result.json) |
| control-code-change | unrelated-control | train | 4 | false | false | not-selected | [trace](raw/control-code-change--r04.trace.jsonl) | [result](raw/control-code-change--r04.result.json) |
| control-code-change | unrelated-control | train | 5 | false | false | not-selected | [trace](raw/control-code-change--r05.trace.jsonl) | [result](raw/control-code-change--r05.result.json) |
| control-code-held | unrelated-control | held-out | 1 | false | false | not-selected | [trace](raw/control-code-held--r01.trace.jsonl) | [result](raw/control-code-held--r01.result.json) |
| control-code-held | unrelated-control | held-out | 2 | false | false | not-selected | [trace](raw/control-code-held--r02.trace.jsonl) | [result](raw/control-code-held--r02.result.json) |
| control-code-held | unrelated-control | held-out | 3 | false | false | not-selected | [trace](raw/control-code-held--r03.trace.jsonl) | [result](raw/control-code-held--r03.result.json) |
| control-code-held | unrelated-control | held-out | 4 | false | false | not-selected | [trace](raw/control-code-held--r04.trace.jsonl) | [result](raw/control-code-held--r04.result.json) |
| control-code-held | unrelated-control | held-out | 5 | false | false | not-selected | [trace](raw/control-code-held--r05.trace.jsonl) | [result](raw/control-code-held--r05.result.json) |
| control-creative-poem | unrelated-control | train | 1 | false | false | not-selected | [trace](raw/control-creative-poem--r01.trace.jsonl) | [result](raw/control-creative-poem--r01.result.json) |
| control-creative-poem | unrelated-control | train | 2 | false | false | not-selected | [trace](raw/control-creative-poem--r02.trace.jsonl) | [result](raw/control-creative-poem--r02.result.json) |
| control-creative-poem | unrelated-control | train | 3 | false | false | not-selected | [trace](raw/control-creative-poem--r03.trace.jsonl) | [result](raw/control-creative-poem--r03.result.json) |
| control-creative-poem | unrelated-control | train | 4 | false | false | not-selected | [trace](raw/control-creative-poem--r04.trace.jsonl) | [result](raw/control-creative-poem--r04.result.json) |
| control-creative-poem | unrelated-control | train | 5 | false | false | not-selected | [trace](raw/control-creative-poem--r05.trace.jsonl) | [result](raw/control-creative-poem--r05.result.json) |
| control-debug | unrelated-control | train | 1 | false | false | not-selected | [trace](raw/control-debug--r01.trace.jsonl) | [result](raw/control-debug--r01.result.json) |
| control-debug | unrelated-control | train | 2 | false | false | not-selected | [trace](raw/control-debug--r02.trace.jsonl) | [result](raw/control-debug--r02.result.json) |
| control-debug | unrelated-control | train | 3 | false | false | not-selected | [trace](raw/control-debug--r03.trace.jsonl) | [result](raw/control-debug--r03.result.json) |
| control-debug | unrelated-control | train | 4 | false | false | not-selected | [trace](raw/control-debug--r04.trace.jsonl) | [result](raw/control-debug--r04.result.json) |
| control-debug | unrelated-control | train | 5 | false | false | not-selected | [trace](raw/control-debug--r05.trace.jsonl) | [result](raw/control-debug--r05.result.json) |
| control-debug-held | unrelated-control | held-out | 1 | false | false | not-selected | [trace](raw/control-debug-held--r01.trace.jsonl) | [result](raw/control-debug-held--r01.result.json) |
| control-debug-held | unrelated-control | held-out | 2 | false | false | not-selected | [trace](raw/control-debug-held--r02.trace.jsonl) | [result](raw/control-debug-held--r02.result.json) |
| control-debug-held | unrelated-control | held-out | 3 | false | false | not-selected | [trace](raw/control-debug-held--r03.trace.jsonl) | [result](raw/control-debug-held--r03.result.json) |
| control-debug-held | unrelated-control | held-out | 4 | false | false | not-selected | [trace](raw/control-debug-held--r04.trace.jsonl) | [result](raw/control-debug-held--r04.result.json) |
| control-debug-held | unrelated-control | held-out | 5 | false | false | not-selected | [trace](raw/control-debug-held--r05.trace.jsonl) | [result](raw/control-debug-held--r05.result.json) |
| control-factual-lookup | unrelated-control | train | 1 | false | false | not-selected | [trace](raw/control-factual-lookup--r01.trace.jsonl) | [result](raw/control-factual-lookup--r01.result.json) |
| control-factual-lookup | unrelated-control | train | 2 | false | false | not-selected | [trace](raw/control-factual-lookup--r02.trace.jsonl) | [result](raw/control-factual-lookup--r02.result.json) |
| control-factual-lookup | unrelated-control | train | 3 | false | false | not-selected | [trace](raw/control-factual-lookup--r03.trace.jsonl) | [result](raw/control-factual-lookup--r03.result.json) |
| control-factual-lookup | unrelated-control | train | 4 | false | false | not-selected | [trace](raw/control-factual-lookup--r04.trace.jsonl) | [result](raw/control-factual-lookup--r04.result.json) |
| control-factual-lookup | unrelated-control | train | 5 | false | false | not-selected | [trace](raw/control-factual-lookup--r05.trace.jsonl) | [result](raw/control-factual-lookup--r05.result.json) |
| control-ja-factual | unrelated-control | train | 1 | false | false | not-selected | [trace](raw/control-ja-factual--r01.trace.jsonl) | [result](raw/control-ja-factual--r01.result.json) |
| control-ja-factual | unrelated-control | train | 2 | false | false | not-selected | [trace](raw/control-ja-factual--r02.trace.jsonl) | [result](raw/control-ja-factual--r02.result.json) |
| control-ja-factual | unrelated-control | train | 3 | false | false | not-selected | [trace](raw/control-ja-factual--r03.trace.jsonl) | [result](raw/control-ja-factual--r03.result.json) |
| control-ja-factual | unrelated-control | train | 4 | false | false | not-selected | [trace](raw/control-ja-factual--r04.trace.jsonl) | [result](raw/control-ja-factual--r04.result.json) |
| control-ja-factual | unrelated-control | train | 5 | false | false | not-selected | [trace](raw/control-ja-factual--r05.trace.jsonl) | [result](raw/control-ja-factual--r05.result.json) |
| control-lookup-held | unrelated-control | held-out | 1 | false | false | not-selected | [trace](raw/control-lookup-held--r01.trace.jsonl) | [result](raw/control-lookup-held--r01.result.json) |
| control-lookup-held | unrelated-control | held-out | 2 | false | false | not-selected | [trace](raw/control-lookup-held--r02.trace.jsonl) | [result](raw/control-lookup-held--r02.result.json) |
| control-lookup-held | unrelated-control | held-out | 3 | false | false | not-selected | [trace](raw/control-lookup-held--r03.trace.jsonl) | [result](raw/control-lookup-held--r03.result.json) |
| control-lookup-held | unrelated-control | held-out | 4 | false | false | not-selected | [trace](raw/control-lookup-held--r04.trace.jsonl) | [result](raw/control-lookup-held--r04.result.json) |
| control-lookup-held | unrelated-control | held-out | 5 | false | false | not-selected | [trace](raw/control-lookup-held--r05.trace.jsonl) | [result](raw/control-lookup-held--r05.result.json) |
| control-math | unrelated-control | train | 1 | false | false | not-selected | [trace](raw/control-math--r01.trace.jsonl) | [result](raw/control-math--r01.result.json) |
| control-math | unrelated-control | train | 2 | false | false | not-selected | [trace](raw/control-math--r02.trace.jsonl) | [result](raw/control-math--r02.result.json) |
| control-math | unrelated-control | train | 3 | false | false | not-selected | [trace](raw/control-math--r03.trace.jsonl) | [result](raw/control-math--r03.result.json) |
| control-math | unrelated-control | train | 4 | false | false | not-selected | [trace](raw/control-math--r04.trace.jsonl) | [result](raw/control-math--r04.result.json) |
| control-math | unrelated-control | train | 5 | false | false | not-selected | [trace](raw/control-math--r05.trace.jsonl) | [result](raw/control-math--r05.result.json) |
| control-research | unrelated-control | train | 1 | false | false | not-selected | [trace](raw/control-research--r01.trace.jsonl) | [result](raw/control-research--r01.result.json) |
| control-research | unrelated-control | train | 2 | false | false | not-selected | [trace](raw/control-research--r02.trace.jsonl) | [result](raw/control-research--r02.result.json) |
| control-research | unrelated-control | train | 3 | false | false | not-selected | [trace](raw/control-research--r03.trace.jsonl) | [result](raw/control-research--r03.result.json) |
| control-research | unrelated-control | train | 4 | false | false | not-selected | [trace](raw/control-research--r04.trace.jsonl) | [result](raw/control-research--r04.result.json) |
| control-research | unrelated-control | train | 5 | false | false | not-selected | [trace](raw/control-research--r05.trace.jsonl) | [result](raw/control-research--r05.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 1 | true | false | not-selected | [trace](raw/explicit-en-clarify-status-held--r01.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r01.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r02.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r02.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 3 | true | false | not-selected | [trace](raw/explicit-en-clarify-status-held--r03.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r03.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r04.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r04.result.json) |
| explicit-en-clarify-status-held | explicit-request | held-out | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-en-clarify-status-held--r05.trace.jsonl) | [result](raw/explicit-en-clarify-status-held--r05.result.json) |
| explicit-en-clearer-status | explicit-request | train | 1 | true | false | not-selected | [trace](raw/explicit-en-clearer-status--r01.trace.jsonl) | [result](raw/explicit-en-clearer-status--r01.result.json) |
| explicit-en-clearer-status | explicit-request | train | 2 | true | false | not-selected | [trace](raw/explicit-en-clearer-status--r02.trace.jsonl) | [result](raw/explicit-en-clearer-status--r02.result.json) |
| explicit-en-clearer-status | explicit-request | train | 3 | true | false | not-selected | [trace](raw/explicit-en-clearer-status--r03.trace.jsonl) | [result](raw/explicit-en-clearer-status--r03.result.json) |
| explicit-en-clearer-status | explicit-request | train | 4 | true | false | not-selected | [trace](raw/explicit-en-clearer-status--r04.trace.jsonl) | [result](raw/explicit-en-clearer-status--r04.result.json) |
| explicit-en-clearer-status | explicit-request | train | 5 | true | false | not-selected | [trace](raw/explicit-en-clearer-status--r05.trace.jsonl) | [result](raw/explicit-en-clearer-status--r05.result.json) |
| explicit-en-polish-email | explicit-request | train | 1 | true | true | selected-with-visible-change | [trace](raw/explicit-en-polish-email--r01.trace.jsonl) | [result](raw/explicit-en-polish-email--r01.result.json) |
| explicit-en-polish-email | explicit-request | train | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-en-polish-email--r02.trace.jsonl) | [result](raw/explicit-en-polish-email--r02.result.json) |
| explicit-en-polish-email | explicit-request | train | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-en-polish-email--r03.trace.jsonl) | [result](raw/explicit-en-polish-email--r03.result.json) |
| explicit-en-polish-email | explicit-request | train | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-en-polish-email--r04.trace.jsonl) | [result](raw/explicit-en-polish-email--r04.result.json) |
| explicit-en-polish-email | explicit-request | train | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-en-polish-email--r05.trace.jsonl) | [result](raw/explicit-en-polish-email--r05.result.json) |
| explicit-en-proofread-readme | explicit-request | train | 1 | true | false | not-selected | [trace](raw/explicit-en-proofread-readme--r01.trace.jsonl) | [result](raw/explicit-en-proofread-readme--r01.result.json) |
| explicit-en-proofread-readme | explicit-request | train | 2 | true | false | not-selected | [trace](raw/explicit-en-proofread-readme--r02.trace.jsonl) | [result](raw/explicit-en-proofread-readme--r02.result.json) |
| explicit-en-proofread-readme | explicit-request | train | 3 | true | false | not-selected | [trace](raw/explicit-en-proofread-readme--r03.trace.jsonl) | [result](raw/explicit-en-proofread-readme--r03.result.json) |
| explicit-en-proofread-readme | explicit-request | train | 4 | true | false | not-selected | [trace](raw/explicit-en-proofread-readme--r04.trace.jsonl) | [result](raw/explicit-en-proofread-readme--r04.result.json) |
| explicit-en-proofread-readme | explicit-request | train | 5 | true | false | not-selected | [trace](raw/explicit-en-proofread-readme--r05.trace.jsonl) | [result](raw/explicit-en-proofread-readme--r05.result.json) |
| explicit-en-remove-ambiguity | explicit-request | train | 1 | true | false | not-selected | [trace](raw/explicit-en-remove-ambiguity--r01.trace.jsonl) | [result](raw/explicit-en-remove-ambiguity--r01.result.json) |
| explicit-en-remove-ambiguity | explicit-request | train | 2 | true | false | not-selected | [trace](raw/explicit-en-remove-ambiguity--r02.trace.jsonl) | [result](raw/explicit-en-remove-ambiguity--r02.result.json) |
| explicit-en-remove-ambiguity | explicit-request | train | 3 | true | false | not-selected | [trace](raw/explicit-en-remove-ambiguity--r03.trace.jsonl) | [result](raw/explicit-en-remove-ambiguity--r03.result.json) |
| explicit-en-remove-ambiguity | explicit-request | train | 4 | true | false | not-selected | [trace](raw/explicit-en-remove-ambiguity--r04.trace.jsonl) | [result](raw/explicit-en-remove-ambiguity--r04.result.json) |
| explicit-en-remove-ambiguity | explicit-request | train | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-en-remove-ambiguity--r05.trace.jsonl) | [result](raw/explicit-en-remove-ambiguity--r05.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 1 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r01.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r01.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r02.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r02.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r03.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r03.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r04.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r04.result.json) |
| explicit-ja-bunshou-held | explicit-request | held-out | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-bunshou-held--r05.trace.jsonl) | [result](raw/explicit-ja-bunshou-held--r05.result.json) |
| explicit-ja-meikakuni | explicit-request | train | 1 | true | false | not-selected | [trace](raw/explicit-ja-meikakuni--r01.trace.jsonl) | [result](raw/explicit-ja-meikakuni--r01.result.json) |
| explicit-ja-meikakuni | explicit-request | train | 2 | true | false | not-selected | [trace](raw/explicit-ja-meikakuni--r02.trace.jsonl) | [result](raw/explicit-ja-meikakuni--r02.result.json) |
| explicit-ja-meikakuni | explicit-request | train | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-meikakuni--r03.trace.jsonl) | [result](raw/explicit-ja-meikakuni--r03.result.json) |
| explicit-ja-meikakuni | explicit-request | train | 4 | true | false | not-selected | [trace](raw/explicit-ja-meikakuni--r04.trace.jsonl) | [result](raw/explicit-ja-meikakuni--r04.result.json) |
| explicit-ja-meikakuni | explicit-request | train | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-meikakuni--r05.trace.jsonl) | [result](raw/explicit-ja-meikakuni--r05.result.json) |
| explicit-ja-shizen | explicit-request | train | 1 | true | false | not-selected | [trace](raw/explicit-ja-shizen--r01.trace.jsonl) | [result](raw/explicit-ja-shizen--r01.result.json) |
| explicit-ja-shizen | explicit-request | train | 2 | true | false | not-selected | [trace](raw/explicit-ja-shizen--r02.trace.jsonl) | [result](raw/explicit-ja-shizen--r02.result.json) |
| explicit-ja-shizen | explicit-request | train | 3 | true | false | not-selected | [trace](raw/explicit-ja-shizen--r03.trace.jsonl) | [result](raw/explicit-ja-shizen--r03.result.json) |
| explicit-ja-shizen | explicit-request | train | 4 | true | false | not-selected | [trace](raw/explicit-ja-shizen--r04.trace.jsonl) | [result](raw/explicit-ja-shizen--r04.result.json) |
| explicit-ja-shizen | explicit-request | train | 5 | true | false | not-selected | [trace](raw/explicit-ja-shizen--r05.trace.jsonl) | [result](raw/explicit-ja-shizen--r05.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 1 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r01.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r01.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r02.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r02.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r03.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r03.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r04.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r04.result.json) |
| explicit-ja-suikou-held | explicit-request | held-out | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-suikou-held--r05.trace.jsonl) | [result](raw/explicit-ja-suikou-held--r05.result.json) |
| explicit-ja-wakariyasuku | explicit-request | train | 1 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-wakariyasuku--r01.trace.jsonl) | [result](raw/explicit-ja-wakariyasuku--r01.result.json) |
| explicit-ja-wakariyasuku | explicit-request | train | 2 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-wakariyasuku--r02.trace.jsonl) | [result](raw/explicit-ja-wakariyasuku--r02.result.json) |
| explicit-ja-wakariyasuku | explicit-request | train | 3 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-wakariyasuku--r03.trace.jsonl) | [result](raw/explicit-ja-wakariyasuku--r03.result.json) |
| explicit-ja-wakariyasuku | explicit-request | train | 4 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-wakariyasuku--r04.trace.jsonl) | [result](raw/explicit-ja-wakariyasuku--r04.result.json) |
| explicit-ja-wakariyasuku | explicit-request | train | 5 | true | true | selected-with-visible-change | [trace](raw/explicit-ja-wakariyasuku--r05.trace.jsonl) | [result](raw/explicit-ja-wakariyasuku--r05.result.json) |
