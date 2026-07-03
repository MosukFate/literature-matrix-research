# Obsidian Markdown Playbook

Use this reference when creating or editing the Obsidian reading package without an Obsidian-specific helper skill.

## Link Policy

- Use Markdown links for paths with directories: `[Title](../01_stage/card.md)`.
- Use wikilinks for same-vault note references when the note stem is stable: `[[card_stem|Display]]`.
- Use heading links only when headings are stable.
- Do not use path-style wikilinks for directory paths if they break in the target environment.

## Frontmatter

Paper cards should start with YAML frontmatter:

```yaml
---
paper_id: O01
title: "Paper Title"
cluster: "01_stage_name"
method_type: "mechanism"
result_type: "benchmark_and_intervention"
benchmarks: ["Benchmark"]
models: ["Model"]
source_status: "source-level verified; table-level ledger pending"
priority: P1
tags: ["topic"]
---
```

Use conservative `source_status`.

## Callouts

Use callouts for high-signal blocks:

```markdown
> [!abstract] 一句话理解
> **一句话**：...
```

Avoid nesting too many callouts inside cards; cards should remain readable in plain Markdown.

## Required Card Skeleton

Formal `type: paper-card` notes use the AI paper deep-read schema. Keep frontmatter and source/evidence bullets before the body, then use this skeleton:

```markdown
<!-- one_sentence_summary:start -->
> [!abstract] 一句话理解
> **一句话**：...
>
> **例子**：...
> **用处**：...
<!-- one_sentence_summary:end -->

- 核验来源: ...
- 核验状态: ...
- 未核验数字: ...

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

## Stage Index Pattern

Each stage index should include:

- Reading goal.
- Mainline reading list with one-sentence explanation after every link.
- Supplemental evidence links when relevant.
- Strong cross-paper relations and why they matter.
- Warnings for source-trust limits.

## Supplemental Pool Pattern

Supplemental entries must not be shorthand-only. Use:

```markdown
- [[card_stem|O01. Full Paper Title]]：一句话说明这篇论文在做什么，以及为什么作为补充证据有用。
```

## Canvas and Maps

Research maps should be readable and purposeful:

- Show research-relevant relations, not every possible edge.
- Use relation labels: baseline, benchmark, mechanism bridge, novelty risk, counterexample, infrastructure, extension.
- Split dense maps into groups or layers.

If writing `.canvas`, validate JSON before completion.
