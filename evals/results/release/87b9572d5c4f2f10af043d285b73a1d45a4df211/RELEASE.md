# Release-candidate decision

Decision: **fail**

Candidate revision: `87b9572d5c4f2f10af043d285b73a1d45a4df211`
Core matrix: 425 generations (routing and behavior only).

English, Japanese, and multilingual-core results are kept separate. Failed and non-gating checks remain visible.

| Gate | Group | Result | Actual | Threshold | Gating |
|---|---|---|---|---|---|
| core-generation-matrix | provenance | pass | 425 | exactly 200 routing + 225 behavior = 425 | yes |
| routing-explicit-recall | routing | fail | 0.92 | >= 0.95 | yes |
| routing-complex-recall | routing | pass | 1.0 | >= 0.85 | yes |
| routing-unrelated-fpr | routing | pass | 0.0 | <= 0.10 | yes |
| behavior-arm-provenance | provenance | pass | ['no-skill', '178eaf8', '87b9572d5c4f2f10af043d285b73a1d45a4df211'] | exact release arms and comparison | yes |
| english-mean-noncritical-preservation | behavior | pass | 4.96 | >= 4.5 | yes |
| english-critical-failures | behavior | pass | 0 | = 0 | yes |
| english-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| english-candidate-win-rate | behavior | pass | 0.76 | >= 0.50 | yes |
| english-candidate-loss-rate | behavior | pass | 0.08 | <= 0.10 | yes |
| japanese-mean-noncritical-preservation | behavior | pass | 5 | >= 4.5 | yes |
| japanese-critical-failures | behavior | pass | 0 | = 0 | yes |
| japanese-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| japanese-candidate-win-rate | behavior | pass | 0.64 | >= 0.50 | yes |
| japanese-candidate-loss-rate | behavior | fail | 0.16 | <= 0.10 | yes |
| multilingual-core-mean-noncritical-preservation | behavior | pass | 5 | >= 4.5 | yes |
| multilingual-core-critical-failures | behavior | pass | 0 | = 0 | yes |
| multilingual-core-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| multilingual-core-candidate-win-rate | behavior | pass | 0.76 | >= 0.50 | yes |
| multilingual-core-candidate-loss-rate | behavior | pass | 0.08 | <= 0.10 | yes |
| boundary-en-equivalent | boundary | pass | 1.0 | >= 0.90 | yes |
| boundary-en-critical-changes | boundary | pass | 0 | = 0 | yes |
| boundary-ja-equivalent | boundary | pass | 1.0 | >= 0.90 | yes |
| boundary-ja-critical-changes | boundary | pass | 0 | = 0 | yes |
| boundary-post-candidate-disclosure | boundary | pass | True | must disclose post-candidate fixture | yes |

The already-clear fixture was designed after candidate authorship and is supplemental; it is excluded from the 425-generation matrix.

Removed GPT rubric items: none.
