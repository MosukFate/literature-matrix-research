# Card Quality Audit

Use this reference for `audit-only` work on an existing Obsidian paper-card package.

## Scope Setup

Create an audit inventory before judging content:

- Identify the package root, START page, dashboard, stage indexes, supplemental index, matrices, audit/source folders, and deep-card directories.
- Count deep cards separately from matrix-only entries.
- Record total Markdown files, table claim ledgers, local PDFs/TXTs, and source reports when present.
- Preserve historical audit files; do not treat old unresolved notes as current unresolved issues without checking the latest ledger or final report.

## Multi-Agent Split

Use independent agents only when their write/read scopes are separable:

- Structure agent: frontmatter, IDs, source_status fields, stage indexes, wikilinks, callouts, heading templates, priority fields, and Obsidian readability.
- Evidence agent: card claim -> result table -> source_status -> ledger/report -> PDF/TXT/full paper.
- Content reviewer: contribution/limitation balance, overclaiming, logic jumps, and whether claims match the paper.
- Synthesis reviewer: cross-card map, gap coverage, redundancy, missing themes, and reading order sufficiency.
- Coordinator: merge findings by severity and deduplicate repeated template issues.

## Review Matrix Fields

Produce one row per deep card:

| Field | Meaning |
|---|---|
| `paper_id` | ID from frontmatter or filename |
| `path` | relative path from package root |
| `stage` | reading stage or supplemental pool |
| `structure_status` | pass / minor / major |
| `evidence_status` | verified / partial / missing / not sampled |
| `content_sufficiency` | sufficient / needs detail / overclaim / unclear |
| `severity` | critical / major / minor / format-only / none |
| `recommended_action` | concrete next edit or verification step |

## Findings Report

List only actionable issues. Every item must include:

- Severity: `critical`, `major`, `minor`, or `format-only`.
- Card path and, when applicable, line/heading.
- Evidence path: ledger, PDF, source report, official URL, or card source_status.
- Issue statement: what is wrong or unsupported.
- Suggested fix: exact wording direction, source to check, or structural edit.

## Severity Rules

- `critical`: factual error, wrong paper identity, broken main navigation, unsupported numeric/table claim likely to be cited, or a missing source for a major conclusion.
- `major`: evidence is partial, method is misrepresented, benchmark result is overread as mechanism proof, or contribution/limitation framing is materially unbalanced.
- `minor`: unclear wording, weak example, missing research relation, or minor heading inconsistency.
- `format-only`: Obsidian formatting, callout syntax, link style, table alignment, or metadata cleanup.

## Content Sufficiency Checklist

Each deep card should cover:

- Overview summary and paper positioning.
- Beginner intuition plus technical logic chain.
- Method/model/training/inference workflow.
- Important formulas, derivations, metrics, or mechanisms when central to the paper.
- Innovation and concrete baseline differences.
- Experimental design, ablations, efficiency, and evidence.
- Strengths, limitations, overclaim risks, reproduction path, landing fit, reading advice, and final summary.

## Formal Paper-Card Gate

Audit `type: paper-card` as a finished deep card, not as a general note. A formal card fails if any of these are true:

- it is only `source-level ready`, `prior survey`, or `table-level pending`;
- `## 3. 方法/模型/训练/推理拆解` is a short generic paragraph instead of a layered how/why/effect pipeline;
- `## 4. 数学公式、推导与算法映射` is missing, only translates symbols, or does not map math back to algorithm/implementation;
- `## 5. 创新点与 baseline 本质差异` only says the method is better without naming the changed component;
- `## 8. 复现路径与落地适用性` is missing or gives generic implementation advice unrelated to the paper;
- it has no original result-table evidence and no explicit no-table statement;
- it lacks embedded examples or concrete task/failure cases;
- it could be understood only by someone who already read the paper.

When a note is useful but shallow, recommend demotion to `type: paper-stub` or `type: matrix-stub` instead of polishing the wording around an empty core.

## Acceptance Criteria

- All deep cards are registered in the review matrix.
- Stage indexes match actual linked cards.
- Broken links are recorded.
- All `critical` and `major` findings have traceable evidence.
- Matrix-only entries are explicitly separated from deep cards.
