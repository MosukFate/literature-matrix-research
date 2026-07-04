---
name: literature-matrix-research
description: Use when independently turning a research topic, seed paper, or paper corpus into a source-grounded paper matrix, Obsidian reading order, per-paper cards, venue trust split, benchmark table, evidence audit, original-result-table extraction, or beginner-readable paper notes.
---

# Literature Matrix Research

## Overview

Use this skill to turn academic research into a source-grounded Obsidian paper matrix and reading system. It is the only active literature-matrix workflow on this machine.

The default output is an Obsidian package with a START page, dashboard, staged reading order, mainline/supplemental split, quicklook matrix, venue trust split, benchmark/failure matrix, per-paper cards, original-result-table evidence, and audit reports.

## When to Use

Use this skill when the user asks for:

- a paper matrix, literature map, evidence pool, or field survey;
- a reading order around a seed paper or research direction;
- Obsidian-ready paper cards with frontmatter, wikilinks, Bases, and indexes;
- venue trust splitting between official proceedings, arXiv-only, workshop, project/code-only, and unverified sources;
- source-grounded quality checks for benchmark claims, formulas, tables, or per-paper summaries;
- beginner-readable paper notes that explain positioning, intuition, method, formulas, baseline differences, experiments, reproduction, limits, and project fit;
- detailed method rewrites or original result tables converted from PDF/HTML/MarkItDown into Markdown.

Do not use it for a one-off paper lookup, a generic APA literature review, or a manuscript review unless the deliverable is a matrix/Obsidian corpus.

## Modes

Default to `matrix` plus formal deep cards for paper-reading or research-synthesis requests. Use `search-only` only when the user explicitly asks for basic survey, candidate discovery, `candidate_table`, finding papers, or seed expansion.

| Mode | Use when | Output |
|---|---|---|
| `search-only` | building a candidate pool or expanding a seed paper/research gap | discovery pipeline outputs, candidate table, inclusion/exclusion notes, venue/source status, citation graph signals |
| `matrix` | organizing known papers | quicklook table, venue trust split, benchmark/results matrix |
| `obsidian-package` | creating a full reading system | START, dashboard, staged indexes, cards, matrices, audits |
| `audit-only` | checking an existing package | review matrix, findings report, link/source checks |
| `card-polish` | improving existing cards | edited cards plus polish report |
| `beginner-expansion` | making cards readable for non-readers | `## 0. 总览摘要` plus formula/metric explanation |
| `deep-table-enrichment` | making cards method-complete and table-grounded | detailed methods, embedded examples, original result tables, result interpretation |
| `paper-original-rewrite` | fixing shallow or templated cards | paper-specific how/why/effect method rewrite, manually corrected tables, source-scoped conclusions |
| `planning-stub` | making a lightweight research-planning map when full papers are not yet read | `type: paper-stub` or `type: matrix-stub`; never `type: paper-card` |

## Mode Router

Default route: use `matrix + formal deep cards` for normal paper-reading, single-paper close reading, and research-synthesis requests. Do not stop at `candidate_table` unless the user explicitly asks for `search-only`, `candidate_table`, finding papers, seed expansion, or a basic survey.

- Single-paper close reading: if the user asks to read, explain, summarize deeply, analyze, or make notes for one paper, create a formal `paper-card` after source/PDF/full-text review. If evidence is insufficient, create `paper-stub` and record what source is missing; do not downgrade to `search-only` just because there is one paper.
- Research topic or paper corpus: build a `matrix` first, then write formal deep cards for core papers after source review. Keep bridge/supplemental/matrix-only layers visible.
- `search-only`: use only when the user explicitly asks for `search-only`, `candidate_table`, candidate discovery, finding papers, seed expansion, novelty-risk scanning, citation graph expansion, or basic survey. Run `scripts/discover_candidates.py` when local execution is available, then preserve `candidate_table.csv`, `candidate_table.jsonl`, `search_log.json`, and `failed_queries.md`. Do not create `paper-card` notes from discovery rows.
- `matrix`: use when papers are known or after search screening when the user needs organization, trust splitting, benchmark comparison, relevance layering, or reading order. A matrix can hand off core papers to formal deep-card writing.
- `obsidian-package`: use when the user wants the complete reading system with START, dashboards, indexes, cards, matrices, and audits.
- `audit-only`: use when reviewing an existing package or checking source status, links, tables, claims, and validator findings.
- `card-polish`, `beginner-expansion`, `deep-table-enrichment`, and `paper-original-rewrite`: use only after cards already exist or paper sources have been read deeply enough for formal `paper-card` work.
- `planning-stub`: use when the user needs a fast research map before full source reading. Keep outputs as `paper-stub` or `matrix-stub` until validation supports promotion.
## Usage Examples

Use these prompt patterns to choose the right route:

- Default single-paper deep card: `Use literature-matrix-research to close-read this paper and create a formal paper-card from the PDF/full text. Include method pipeline, how/why/effect, formulas, original result-table evidence or a no-table statement, result interpretation, limitations, reproduction path, project fit, and novice detail check.`
- Default research matrix plus core deep cards: `Use literature-matrix-research for this research question. Build the literature matrix, split core/bridge/supplemental/matrix-only, then write formal deep cards for the core papers after source review.`
- Full Obsidian package: `Use literature-matrix-research to create the complete Obsidian package with START, dashboard, staged reading order, matrices, formal paper-cards, source audit, and validation report.`
- search-only candidate table: `Search-only / candidate_table / 找论文 / seed expansion / 基础调查 for this topic. Output candidate_table.csv/jsonl, search_log.json, failed_queries.md, source_status, graph_relation, and layer; do not write deep cards yet.`
- Fast planning map: `Create a planning-stub research map only. Use paper-stub or matrix-stub labels, and do not promote entries to paper-card until source evidence is sufficient.`

If the user says only `read this paper`, `精读这篇`, `analyze this paper`, or `做深度卡`, treat it as the default single-paper deep-card route, not as `search-only`.
## Skill Chaining and Evolution

This skill is the canonical orchestrator for literature-matrix work, not a silo. When a phase needs a capability already covered by another skill, load the smallest relevant supporting skill at that phase boundary and preserve its evidence in this matrix schema.

**Required routing rules:**

- For skill edits, use `writing-skills` plus `superpowers:test-driven-development`; write or update pressure tests before changing deployed instructions.
- For paper discovery and identifiers, use `paper-lookup`; keep raw URLs, IDs, failed searches, and source dates.
- For PDF, table, and conversion work, use `pdf` and `markitdown`; treat extraction as evidence candidates until source/PDF correction is done.
- For Obsidian syntax, Bases, Canvas, and link conventions, use `obsidian-markdown`, `obsidian-bases`, and `json-canvas` as needed.
- For claim critique, novelty risk, and overclaim checks, use `academic-paper-reviewer`; use `academic-paper` only when the deliverable turns into proposal/manuscript prose.
- Before claiming completion, use `superpowers:verification-before-completion` and report the command evidence.

Do not force-load other skills with file paths or `@` links in the skill body. Name the skill and the phase where it should be loaded. This keeps future runs modular and prevents context bloat.

When the user adds a new rule, append it through the evolution protocol rather than overwriting existing rules. Previously approved rules, especially the GASP-style card rewrite and original-table interpretation rules, must stay semantically intact unless the user explicitly supersedes them.
## Core Workflow

1. Establish the research question, seed papers, date range, venue policy, package root, mirror/sync target, and deliverable mode.
2. Search and screen papers. For online discovery or seed expansion, run `scripts/discover_candidates.py` or reproduce its candidate-table contract; record raw URLs, official identifiers, failed searches, citation graph signals, and source status.
3. Deduplicate by title, DOI, arXiv ID, OpenReview ID, and official venue page.
4. Split papers into core, core-support, bridge, supplemental, matrix-only, and excluded.
5. Build matrices before deep cards so coverage gaps are visible early.
6. Write or update per-paper cards with source status, evidence anchors, one-sentence summary, and the AI paper deep-read schema.
7. Treat `type: paper-card` as a formal deep card by default. A source-level planning note, prior-survey stub, or table-level-pending placeholder must use `type: paper-stub` or `type: matrix-stub`, not `type: paper-card`.
8. When writing any formal `paper-card`, use the AI paper deep-read schema plus `deep-table-enrichment` / `paper-original-rewrite`: extract paper-original evidence, explain the paper as already-read synthesis, explain formulas and derivations where central, paste or manually correct relevant result tables when extractable, add immediate `结果解析 / Result interpretation`, and integrate examples inside the relevant analysis.
9. If the user explicitly asks for a fast planning map, produce stubs honestly: label them as stubs, put them in the matrix or reading queue, and do not let them pass the paper-card validator.
10. Audit structure, links, source status, strong claims, benchmark numbers, formulas, original tables, method detail, embedded examples, and overclaiming before claiming completion.

## Paper-Original Rewrite Rules

- `type: paper-card` is a contract, not a folder label. It means the paper has been read or source-extracted deeply enough to explain the paper through the AI paper deep-read schema: positioning, core logic, method, formulas, innovation, evidence, limitations, reproduction, reading advice, and final summary.
- Lightweight planning notes must be named honestly: use `type: paper-stub` for one-paper placeholders and `type: matrix-stub` for matrix-only/background entries. Do not promote them to `paper-card` until the source evidence has been read and the card passes the deep-card validator.
- Write as the analyst who already read the paper. Do not tell the user how to read the paper, for example `读实验时...` or `读方法时...`, unless the file is explicitly a reading guide.
- `## 3. 方法/模型/训练/推理拆解` must answer three questions in paper-specific prose:
  - **How / 怎么做**: workflow, data flow, modules, training or benchmark construction, inputs/outputs, objective/loss/metric, and enough reproduction-level detail to know the approximate pipeline.
  - **Why / 为什么这么做**: what prior approach failed, what assumption the design encodes, and why each module/loss/control matters.
  - **Effect / 这么做的效果是什么**: internal representation change, benchmark/task change, ablation evidence, trade-off, and what remains unproven.
- Examples and analogies are explanatory instruments, not decorative endings. Embed them directly inside method, evidence, limitation, or project-relation paragraphs.
- Preserve paper identity. If title, task type, or method family conflicts with the card, fix the card and related matrices before polishing prose.


### Layered Method Reconstruction

When improving `## 3. 方法/模型/训练/推理拆解`, do not stop at three flat paragraphs. Reconstruct the method as a stepwise ladder that lets a reader rebuild the paper's pipeline in their head.

Required shape for method cards:

1. **One-screen pipeline first**: state the input, intermediate objects, model/benchmark modules, supervision or scoring signal, and output in 3-6 ordered steps.
2. **Layer-by-layer expansion**: expand each step with what the paper actually does, why that step exists, what ambiguity or failure it removes, and what evidence/result shows its effect.
3. **How/why/effect coupling**: do not put all `why` in one distant paragraph. For each major step, pair `how it is done` with `why it is done` and `what changes because of it`.
4. **Reproduction-level granularity**: include data source, preprocessing/task construction, model inputs/outputs, training/inference path, objective/loss/metric, and evaluation protocol when the paper provides them. If the paper omits a detail, say it is not specified instead of inventing it.
5. **Progressive examples**: embed examples or analogies inside the relevant step. Use them to make the mechanism easier to follow, like GASP's calibration-tool explanation, not as a final decorative section.
6. **Effect ladder when possible**: if the paper reports ablations, complexity sweeps, table comparisons, or qualitative examples, align them with the method steps so the reader sees which design choice caused which observed change. If the paper only reports aggregate performance, state that the step-to-effect mapping is not causally proven.
7. **No reader-instruction prose**: avoid `read this section as...` or `the reader should notice...`; write the synthesis directly.

For benchmark papers, the ladder is usually: source data or scene generator -> task/query construction -> controlled variable or split -> model prompting/answer format -> scoring metric -> failure surface.
For model papers, the ladder is usually: input representation -> backbone/encoder -> geometric, temporal, memory, or language bridge -> training objective or inference procedure -> output -> evaluation/ablation.
## Deep-Table Rules

- Do not create a separate examples/analogies section such as `## 11. 示例、比喻与汇报讲法`.
- Do not create a separate compact conclusion table to replace original evidence.
- Do not paste broken MarkItDown/pdfplumber tables without correction when the source text or PDF is available.
- Prefer original result evidence in this order: official HTML/table, arXiv HTML, PDF visual/manual correction, local converted Markdown, pdfplumber/MarkItDown candidate.
- If extraction mangles headers or merged cells, manually reconstruct the relevant table from the original PDF/HTML/source text and label it `manually corrected from source text/PDF; numeric cells require PDF check before formal citation`.
- Include only tables that support the card's method, benchmark design, main result, ablation, limitation, or project relation.
- Every table must be followed immediately by `结果解析 / Result interpretation`: what the table shows, what it means, what it does not prove, and why it matters for the project.
- If a paper has no extractable or relevant result table, the card must say so explicitly with a source-grounded reason, for example `No extractable result table relevant to this card` / `无可提取且与本卡相关的原文结果表`. Silence is not acceptable for a formal `paper-card`.
- Compact fallback is allowed only when extraction fails and must be labeled `fallback summary; verify original table before citation`.
- Never invent benchmark scores, dataset sizes, model counts, rankings, or SOTA claims.
- Benchmark results define failure surfaces; they do not prove mechanisms unless paired with source-anchored intervention, ablation, probing, or representation analysis.

## Reference Routing

Read only the reference needed for the current mode:

- End-to-end workflow: `references/end_to_end_research_workflow.md`.
- Formal paper-card structure: `references/ai_paper_deep_read_card_schema.md`.
- Deep-card pressure tests and novice repair gate: `references/deep_card_depth_pressure_tests.md`.
- Paper lookup, identifiers, official sources, query expansion: `references/paper_lookup_playbook.md`.
- Online discovery, candidate-table schema, citation graph expansion, scoring, and arXiv policy: `references/discovery_pipeline.md`.
- PDF/TXT/table extraction and source anchors: `references/pdf_source_extraction.md`.
- Synthesis, novelty-risk audit, reviewer-style critique: `references/review_synthesis_rubric.md`.
- Obsidian Markdown, wikilinks, callouts, Canvas/Bases: `references/obsidian_markdown_playbook.md`.
- Package layout, staged indexes, START/Dashboard: `references/matrix_and_reading_order.md`.
- Source hierarchy, venue trust, table claims, ledger rules: `references/evidence_and_source_rules.md`.
- Existing-card review and actionable findings: `references/card_quality_audit.md`.
- Card polishing without changing IDs/links: `references/card_polish_workflow.md`.
- Beginner-readable explanation layer and formula explanations: `references/beginner_guide_layer.md`.
- Detailed methods, embedded examples, original result tables, MarkItDown/PDF conversion: `references/deep_card_table_enrichment.md`.
- Cross-skill orchestration and phase handoffs: `references/skill_integration.md`.
- Additive skill evolution, protected rules, and regression checks: `references/evolution_protocol.md`.

## Validation

Use bundled scripts when working on a local Obsidian package:

```bash
python scripts/validate_structure.py path/to/obsidian_reading_order --require-beginner
python scripts/validate_content_risks.py path/to/obsidian_reading_order
python scripts/package_skill.py path/to/literature-matrix-research
```

The scripts are heuristics, not substitutes for paper-level source review. Treat reported issues as a review queue until checked against the paper, source ledger, PDF, or converted table. For packages with lane `index.md` files, also run a custom `type: paper-card` filter so lane indexes are not misclassified as paper cards.

## Quality Gates

- Never promote `source_status` without official paper, PDF, table ledger, project page, or source report support.
- Do not introduce unverified numbers, benchmark rankings, model names, or table conclusions.
- Keep paper IDs, filenames, wikilink targets, and staged order stable unless the user asks to reorganize.
- Mainline/supplement/matrix-only distinctions must be visible from START and lane indexes.
- Every actionable finding should include a card path, evidence path or source URL, issue, severity, and suggested fix.
- When a mirror/sync target is specified, update it after the canonical package changes and verify source/target consistency.
- A formal `paper-card` that is only source-level, table-level pending, or prior-survey based must fail validation. Demote it to `paper-stub` or rewrite it at GASP-card depth.
- A formal `paper-card` must not pass with a tiny `## 3` method section. The method section needs a pipeline sketch plus layered how/why/effect reconstruction.
- A formal `paper-card` must include `## 4. 数学公式、推导与算法映射`, `## 5. 创新点与 baseline 本质差异`, and `## 8. 复现路径与落地适用性`, with explicit unknown boundaries when the paper does not provide details.
- A formal `paper-card` must include original result-table evidence plus immediate interpretation, or an explicit source-grounded no-table statement.
- A formal `paper-card` cannot be metadata-only, abstract-only, source-level-only, prior-survey-only, or full-text/table-level-pending. If that is the evidence state, use `type: paper-stub` or `type: matrix-stub`.
- Before finishing each formal `paper-card`, add `### 小白细节自检 / Novice detail check`. Ask whether a first-time reader can reconstruct the paper's actual input/output, modules, objective, training or inference path, evaluation, baseline difference, source anchors, and unknown boundaries.
- If the novice check says the detail is insufficient, do exactly one source-backed repair pass. If the card still cannot support a first serious reading after that one pass, demote it to `paper-stub`; do not pad it with generic prose.

## Common Mistakes

- Writing a generic literature review instead of a navigable matrix package.
- Letting arXiv-only or workshop papers silently mix into the verified mainline.
- Letting `source-level ready` stubs masquerade as finished `type: paper-card` notes.
- Writing fluent beginner explanations that add claims not supported by the card, ledger, or original paper.
- Telling the reader how to read the paper instead of summarizing what the paper does and what its evidence means.
- Using a reusable paragraph such as `input visual evidence or video frames...` without paper-specific workflow detail.
- Counting matrix-only entries as fully verified deep cards.
- Treating benchmark wins, attention heatmaps, or abstract claims as causal mechanism evidence.
- Adding examples at the end as decorative content instead of using them to explain method or evidence.
- Replacing original result tables with compact summary tables when the user asked for paper-original tables.
- Trusting a mangled extraction table when source text/PDF can be used to restore the header and rows.


