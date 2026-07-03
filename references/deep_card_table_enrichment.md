# Deep Card Table Enrichment

Use this reference when paper cards must be detailed enough for a reader who has not read the paper and when the user asks for detailed methods, original paper result tables, fuller conclusions, examples, analogies, or presentation-ready explanations.

## Core Principle

Deep enrichment is not "add more sections". It is paper-original synthesis. The agent must read the source evidence, then explain what the paper does, why it does it, what effect it reports, and where the evidence stops.

A deep card should feel like the analyst already read the paper for the user. It should not say "read the method like this" or "look at the table this way" unless the deliverable is explicitly a reading guide.

## Correct Card Shape

Every enriched formal `paper-card` must preserve the frontmatter, source/evidence bullets, and one-sentence summary block, then use the AI paper deep-read schema in `references/ai_paper_deep_read_card_schema.md`.

Required body headings:

1. `## 0. 总览摘要`
2. `## 1. 论文定位与核心痛点`
3. `## 2. 核心思想与逻辑链`
4. `## 3. 方法/模型/训练/推理拆解`
5. `## 4. 数学公式、推导与算法映射`
6. `## 5. 创新点与 baseline 本质差异`
7. `## 6. 实验、消融、效率与可信度`
8. `## 7. 优缺点、局限与过度宣传风险`
9. `## 8. 复现路径与落地适用性`
10. `## 9. 阅读建议与相关工作`
11. `## 10. 最终总结`

Do not append the old six-section skeleton as a duplicate structure. Do not append a separate examples/analogies section. Do not append a compact table-summary section as a replacement for original result evidence.

## Paper-Card vs Stub Contract

`type: paper-card` is reserved for GASP-depth notes. It means the paper has been read or extracted deeply enough that the card can stand in for a first serious reading.

Use these labels instead when the evidence is still shallow:

| Label | Use when | Must not claim |
|---|---|---|
| `type: paper-stub` | one paper is useful for planning, but only source-level metadata or prior-survey notes are available | finished paper-card quality |
| `type: matrix-stub` | an item belongs in a matrix/background row but does not deserve a full card yet | paper-original synthesis |

If a note says `source-level ready`, `prior survey`, or `table-level pending`, it is normally a stub unless the card still contains paper-original method reconstruction, source anchors, and explicit no-table evidence boundaries. Do not let a stub inherit `type: paper-card` merely because it sits in a lane folder.

A card that says `metadata verified`, `abstract only`, `full-text pending`, `table-level pending`, `source-level only`, or equivalent wording is not a formal card. Rewrite it from source evidence or demote it to a stub. A `No extractable result table` statement is valid only after the source evidence has actually been checked; it cannot mean `I did not read the full paper yet`.

Every enriched formal card must include `### 小白细节自检 / Novice detail check`. If this check reveals that a beginner still cannot reconstruct the pipeline, run one repair pass using paper/PDF/HTML/table evidence. Stop after one repair pass: either the card becomes source-grounded enough to pass, or it is demoted to `paper-stub`.

## Method Detail Requirements

`## 3. 方法/模型/训练/推理拆解` must answer three questions:

| Question | What to include |
|---|---|
| `怎么做 / How` | workflow, data source, task or model construction, inputs/outputs, modules, training or inference path, loss/objective/metric, and enough reproduction-level detail to know the approximate pipeline |
| `为什么这么做 / Why` | the failure of prior approaches, the assumption behind the design, why each module/loss/control exists, and what ambiguity it removes |
| `这么做的效果是什么 / Effect` | representation change, benchmark/task result, ablation, trade-off, downstream effect, and source-scoped boundary |

Use paper-type specifics:

| Paper type | Required method details |
|---|---|
| Benchmark/evaluation | data source, task construction, prompt/answer format, scoring metric, controlled variables, what is not controlled |
| Architecture/model | input/output, modules, token flow, training stages, inference path, objective/loss where available |
| Representation/probing | probed variable, probe target, controls, causal vs correlational status, intervention if any |
| Geometry model | camera/depth/point/register outputs, coordinate assumptions, multi-view or temporal handling |
| Action/video method | temporal state, memory, geometry cue, policy/action interface, segmentation or reward objective |

Examples and analogies belong inside this explanation when they clarify the mechanism. For example, a correspondence head can be explained as a temporary training calibration tool that is removed at inference, not as a decorative analogy at the end.


## Layered Method Reconstruction

A deep card's method section should be a layered explanation, not three disconnected answers. The target is the GASP-style pattern: first show the whole pipeline, then walk through the method step by step, and for every major step explain how it works, why the authors needed it, and what effect the paper reports or does not prove.

Use this checklist when rewriting `## 3`:

| Layer | Required content |
|---|---|
| Pipeline sketch | Ordered steps from input to output; enough for the reader to know the paper's overall workflow |
| Step mechanics | For each step: data/object/module, input/output, transformation, training/inference/scoring detail |
| Step rationale | Why this step is needed; what prior ambiguity, shortcut, or failure it tries to remove |
| Step effect | Table/ablation/qualitative evidence tied to the step, or an explicit boundary that the paper does not isolate this effect |
| Embedded example | A concrete example or analogy placed inside the relevant step to clarify mechanism |
| Reproduction boundary | What details are omitted by the paper and cannot be reconstructed safely |

For benchmark papers, organize the ladder as: data/scene source -> query/task generation -> control variables -> prompt/answer format -> scoring -> observed failure surface.

For method/model papers, organize the ladder as: input representation -> backbone/encoder -> bridge module or geometric/temporal/memory operation -> objective/loss or inference rule -> output -> evaluation/ablation.

Avoid these failures:

- writing a generic paragraph that could fit any VLM paper;
- writing a one-sentence method such as "the paper generates knowledge and feeds it back into the model";
- separating all `why` from the concrete steps so the method becomes hard to reproduce;
- adding examples only at the end;
- claiming a component causes improvement when the paper only reports aggregate performance.
## Original Result Table Rules

Prefer this extraction order:

1. Official HTML/table or arXiv HTML table.
2. Original PDF visual inspection or manual correction from PDF text.
3. Existing local converted Markdown/PDF extraction.
4. MarkItDown conversion from PDF to Markdown.
5. `pdftotext -layout`, `pdfplumber`, or another parser fallback.
6. Compact fallback only if the original table is unavailable or unreadable.

For every table used in a card, record or include:

| Field | Meaning |
|---|---|
| `Table anchor` | Table number/name and section/page if available |
| `Extraction status` | official/arXiv HTML, manual correction from PDF/source text, MarkItDown, pdfplumber, or incomplete |
| `Original role` | What the paper uses the table to show |
| `Markdown table` | Original result table converted to Markdown, preserving labels, metrics, units, and numbers as faithfully as possible |
| `结果解析 / Result interpretation` | What the table shows, what it means, what it does not prove, and why it matters for the project |
| `Evidence boundary` | Which claims remain unsupported or require manual verification |

If MarkItDown/pdfplumber breaks headers, merged cells, or row groups, do not paste the broken table as final evidence. Reconstruct the relevant table manually from the paper source and label it:

`manually corrected from source text/PDF; numeric cells require PDF check before formal citation`

Do not copy all tables mechanically. Include the tables that support the card's method comparison, benchmark design, main result, ablation, limitation, or project relation.

If there is no extractable or relevant result table, write an explicit statement in `## 6`:

`No extractable result table relevant to this card / 无可提取且与本卡相关的原文结果表`

Then explain which source sections, figures, proofs, qualitative examples, or dataset documentation replace table evidence. Do not leave a formal paper-card silent about table evidence.

## Fallback Policy

A compact table is allowed only when original extraction fails or the original table is unreadable. It must be labeled:

`fallback summary; verify original table before citation`

This fallback cannot be used as a substitute when the user explicitly asks for the original result table and the PDF/HTML is available.

## Conclusion Rules

A complete conclusion section must separate:

- `Paper reports`: what the authors report.
- `Table-backed evidence`: what specific tables or figures support.
- `Project inference`: how this affects the user's diagnostic matrix.
- `Boundary`: what remains unproven.

Never turn a benchmark table into mechanism proof unless the paper includes a source-anchored intervention, ablation, probing result, or causal analysis.

## Embedded Examples and Analogies

Each enriched card should include:

- one everyday analogy for the core problem or mechanism;
- one concrete task example;
- one failure example;
- one presentation-ready sentence when useful.

These must be embedded in the relevant section. They should clarify source-grounded claims, not replace them. If an analogy does not help explain the method, evidence, limitation, or project relation, remove it.

## Audit Output

After enrichment, write an audit row per card:

| paper_id | original_tables_added | table_extraction_status | method_detail_status | embedded_examples_status | source_level | remaining_followup |
|---|---:|---|---|---|---|---|

Use `original_tables_added = 0` only if the paper has no relevant extractable result table or extraction failed. Explain the reason and next verification step.

## Pressure-Tested Failure Pattern

This rule was added after a GASP card failed in three ways:

1. It described how the reader should read the method instead of explaining the paper's actual workflow.
2. It misidentified the paper as an attention/gaze probing paper instead of a geometric-prior intervention method.
3. It pasted a malformed pdfplumber table even though source text could restore Table 1 and Table 3.

The corrected pattern is: verify identity first, rewrite method as how/why/effect, manually correct relevant original tables, then add immediate result interpretation.
