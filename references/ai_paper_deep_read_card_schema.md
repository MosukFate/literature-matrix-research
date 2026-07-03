# AI Paper Deep-Read Card Schema

Use this reference whenever writing or auditing a formal `type: paper-card` for AI, machine-learning, or deep-learning papers.

## Core Principle

Every formal paper card must help the reader understand the paper, not merely summarize it. The card must explain the algorithmic mechanism, key formulas or derivations, why the method may work, what the evidence actually supports, and how the paper maps to implementation.

## Hard Depth Gate

`type: paper-card` is only allowed when the card is source-grounded enough to replace a first serious reading of the paper. Do not use `paper-card` for metadata-only, abstract-only, source-level-only, prior-survey-only, or full-text/table-level-pending notes. Those must be `type: paper-stub` or `type: matrix-stub`.

A formal card must contain concrete source anchors: official paper URL, arXiv/OpenReview/CVF/ACL/proceedings page, PDF/HTML/conversion ledger, table/figure/section anchor, or equivalent local extraction evidence. A URL alone is not enough if the card content still says the full paper was not read.

## Novice Detail Check

Before finishing a formal card, include a short section named exactly:

```markdown
### 小白细节自检 / Novice detail check
```

Answer these checks from the viewpoint of a first-time reader:

1. Can I reconstruct the paper's actual pipeline from input to output?
2. Do I know the modules, objective/loss or scoring rule, training/inference path, evaluation setup, and baseline difference?
3. Do I know which claims are backed by tables/figures/sections and which details remain unknown?
4. If any answer is no, do one source-backed repair pass. After that single repair pass, if the card is still insufficient, demote it to `paper-stub` instead of padding.

The novice check must not be performative. If it says the reader still cannot reconstruct the method, the formal card fails validation.

If the paper does not specify a detail, write `论文未明确说明` or `我无法从当前内容确认`. Separate `论文明确给出的事实` from `基于论文内容作出的合理推断` when making important judgments.

## Required Card Skeleton

Keep frontmatter, source/evidence bullets, and the `one_sentence_summary` callout before the body. Then use exactly this body skeleton for formal deep cards:

```markdown
## 0. 总览摘要
## 1. 论文定位与核心痛点
## 2. 核心思想与逻辑链
## 3. 方法/模型/训练/推理拆解
## 4. 数学公式、推导与算法映射
## 5. 创新点与 baseline 本质差异
## 6. 实验、消融、效率与可信度
## 7. 优缺点、局限与过度宣传风险
## 8. 复现路径与落地适用性
## 9. 阅读建议与相关工作
## 10. 最终总结
```

Do not append the old six-section card skeleton as a second structure. Fold prior content into the new headings.

## Section Contract

| Section | Required content |
|---|---|
| `0. 总览摘要` | Global understanding, one-sentence summary, three-sentence summary, and why the method matters. |
| `1. 论文定位与核心痛点` | Problem, field, task family, core pain point, importance, performance/efficiency/cost/robustness/interpretability/generalization target, and 1-3 contribution sentences. |
| `2. 核心思想与逻辑链` | Beginner intuition, technical explanation, key components, and chain: observed problem -> hypothesis -> method -> why it may work -> experiments. |
| `3. 方法/模型/训练/推理拆解` | Input/output pipeline, modules, data flow, training data and supervision, objective/loss, inference path, extra search/retrieval/post-processing, and concrete baseline difference. |
| `4. 数学公式、推导与算法映射` | Explain each key formula's objective, variables, design motivation, relation to classic methods, model behavior effect, derivation assumptions, code/training-loop mapping, and complexity/cost. |
| `5. 创新点与 baseline 本质差异` | Separate core innovation from engineering enhancement, compare with classic or adjacent methods, and judge whether the innovation is substantive or a combination of known tricks. |
| `6. 实验、消融、效率与可信度` | Datasets, tasks, baselines, metrics, main results, ablations, efficiency, table evidence or explicit no-table statement, and whether experiments support the claims. |
| `7. 优缺点、局限与过度宣传风险` | Strongest algorithmic/engineering points, assumptions, failure scenarios, dependencies, sensitivity, and overclaim risks. |
| `8. 复现路径与落地适用性` | Minimum reproduction path, hardest parts, sensitive hyperparameters/tricks, missing implementation details, real deployment fit, and unsuitable scenarios. |
| `9. 阅读建议与相关工作` | Which sections to read carefully, what can be skimmed, prerequisites, and related papers only when source-grounded or clearly marked as inference. |
| `10. 最终总结` | One-sentence summary, three-sentence summary, and natural oral summary. |

## Formula Rules

- Do not only translate symbols. Explain the formula's goal, why it takes that form, what it encourages or penalizes, how it relates to known objectives, and how it changes training or inference.
- Map formulas back to implementation: which step computes them, whether they appear in the training loop or inference, and which variables are explicit versus learned implicitly.
- If the paper has no central formulas, say so and explain the algorithmic mechanism instead.

## Evidence Rules

- Keep original result tables or manually corrected source tables when they support method, benchmark, ablation, limitation, or project relation.
- Every included table must be followed by `结果解析 / Result interpretation`.
- If no relevant table exists or extraction fails, write an explicit source-grounded no-table statement.
- Benchmark wins, attention maps, or aggregate scores do not prove mechanisms unless paired with source-anchored intervention, ablation, probing, or representation analysis.

## Reproduction Rules

- Write from the viewpoint of implementing the paper: minimum modules, safe simplifications, likely blockers, sensitive hyperparameters, and unclear paper details.
- Do not invent training tricks, datasets, evaluation settings, or implementation details. Mark omissions explicitly.

## Anti-Patterns

- Keeping the legacy six-section body and appending the new 0-10 structure.
- Copying the long user prompt verbatim into every card.
- Treating `数学公式、推导与算法映射` as a symbol glossary only.
- Writing `baseline is worse` without identifying which part changed.
- Recommending related work not present in the paper or source set without marking it as a reasonable inference.
