# Card Polish Workflow

Use this reference for `card-polish` work on existing paper cards. The goal is clearer, more accurate research notes without changing the package interface.

## Stable Interface Rules

Do not change unless explicitly requested:

- Filename.
- `paper_id`.
- Stage index order.
- Existing wikilink targets.
- `source_status` strength.
- Historical audit report text.
- Archive or zip files.

Only update index text if card edits make existing navigation misleading.

## Section-Level Polish Rules

### `one_sentence_summary`

Use the compact pattern:

- Problem: what failure, task, or research question.
- Example: one concrete scenario.
- Use: why this paper is in the matrix.

Remove duplicated template traces such as "这篇的用处是这篇的用处".

### `0. 总览摘要` and `1. 论文定位与核心痛点`

- Preserve the paper's actual claim.
- Avoid turning benchmark performance into mechanism proof.
- Keep the conclusion source-scoped: "在该设置下显示", "结果提示", "论文报告".

### `2. 核心思想与逻辑链` and `3. 方法/模型/训练/推理拆解`

Clarify:

- Failure mode.
- Data flow.
- Intervention or training point.
- Model/benchmark relationship.
- What is controlled and what is only observed.

### `6. 实验、消融、效率与可信度`

- Keep only numbers supported by source_status, ledger, PDF, table, figure, or official page.
- Downgrade unsupported details to "需回原文".
- Distinguish benchmark, diagnostic set, ablation, and mechanism experiment.

### `4. 数学公式、推导与算法映射`

- Explain formula objective, variables, motivation, relation to known methods, model-behavior effect, and implementation/training-loop mapping.
- If the paper has no central formula or the source is insufficient, write the boundary explicitly.

### `5. 创新点与 baseline 本质差异` and `7. 优缺点、局限与过度宣传风险`

Balance them as a pair:

- Contribution should say what the paper makes possible.
- Limitation should say where the evidence stops, not just generic caveats.

### `8. 复现路径与落地适用性`

Make it implementation-facing:

- Minimum reproduction path.
- First modules to implement.
- Safe simplifications.
- Hardest blockers.
- Sensitive hyperparameters or unclear paper details.
- Deployment suitability.

### `9. 阅读建议与相关工作` and `10. 最终总结`

Make it useful after the card is closed:

- Identify sections worth close reading.
- Name prerequisites only when they are actually needed.
- Recommend related work only when source-grounded or clearly marked as inference.
- Keep one-sentence, three-sentence, and oral summaries aligned with the evidence above.

## Strong Claim Review

Scan and review:

`证明`, `直接证明`, `必须`, `一定`, `完全`, `唯一`, `SOTA`, `state-of-the-art`, `best`.

Prefer source-scoped wording:

- `支持`.
- `提示`.
- `在该设置下显示`.
- `可作为假设`.
- `论文报告`.
- `需要回原文确认`.

## Template Residue Scan

Remove or rewrite:

- `主控阅读补充`.
- `主控最终补充`.
- `主 agent`.
- `????`.
- `TODO`.
- `TBD`.
- Generic "如果要把它接到 Instruction Anchor..." paragraphs that do not say anything paper-specific.

## Report

Write a concise polish report with one row per touched card:

- `paper_id`.
- `path`.
- `edit_type`: summary / positioning / method / formula / baseline / evidence / limitations / reproduction / reading_advice / format.
- `claims_changed`: yes/no.
- `source_checked`: ledger / PDF / official page / not needed.
- `manual_followup`.
