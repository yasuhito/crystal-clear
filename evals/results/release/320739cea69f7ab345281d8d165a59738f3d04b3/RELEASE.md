# Release-candidate decision

Decision: **fail**

Candidate revision: `320739cea69f7ab345281d8d165a59738f3d04b3`
Core matrix: 425 generations (routing and behavior only).

English, Japanese, and multilingual-core results are kept separate. Failed and non-gating checks remain visible.

| Gate | Group | Result | Actual | Threshold | Gating |
|---|---|---|---|---|---|
| core-generation-matrix | provenance | pass | 425 | exactly 200 routing + 225 behavior = 425 | yes |
| routing-explicit-recall | routing | pass | 0.98 | >= 0.95 | yes |
| routing-complex-recall | routing | pass | 1.0 | >= 0.85 | yes |
| routing-unrelated-fpr | routing | pass | 0.0 | <= 0.10 | yes |
| behavior-arm-provenance | provenance | pass | ['no-skill', '178eaf8', '320739cea69f7ab345281d8d165a59738f3d04b3'] | exact release arms and comparison | yes |
| english-mean-noncritical-preservation | behavior | pass | 4.95 | >= 4.5 | yes |
| english-critical-failures | behavior | fail | 5 | = 0 | yes |
| english-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| english-candidate-win-rate | behavior | fail | 0.32 | >= 0.50 | yes |
| english-candidate-loss-rate | behavior | fail | 0.24 | <= 0.10 | yes |
| japanese-mean-noncritical-preservation | behavior | pass | 4.88 | >= 4.5 | yes |
| japanese-critical-failures | behavior | pass | 0 | = 0 | yes |
| japanese-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| japanese-candidate-win-rate | behavior | fail | 0.44 | >= 0.50 | yes |
| japanese-candidate-loss-rate | behavior | fail | 0.44 | <= 0.10 | yes |
| multilingual-core-mean-noncritical-preservation | behavior | pass | 4.773 | >= 4.5 | yes |
| multilingual-core-critical-failures | behavior | fail | 3 | = 0 | yes |
| multilingual-core-protected-string-changes | behavior | pass | 0 | = 0 | yes |
| multilingual-core-candidate-win-rate | behavior | fail | 0.24 | >= 0.50 | yes |
| multilingual-core-candidate-loss-rate | behavior | fail | 0.36 | <= 0.10 | yes |
| boundary-en-equivalent | boundary | pass | 0.9 | >= 0.90 | yes |
| boundary-en-critical-changes | boundary | fail | 1 | = 0 | yes |
| boundary-ja-equivalent | boundary | pass | 1.0 | >= 0.90 | yes |
| boundary-ja-critical-changes | boundary | pass | 0 | = 0 | yes |
| boundary-post-candidate-disclosure | boundary | pass | True | must disclose post-candidate fixture | yes |

The already-clear fixture was designed after candidate authorship and is supplemental; it is excluded from the 425-generation matrix.

Removed GPT rubric items: none.
