# Literature Matrix Research Skill

A Codex skill for building source-grounded academic literature matrices, Obsidian reading systems, and deep per-paper cards.

## What It Does

- Builds paper matrices and staged reading orders from research topics or seed papers.
- Produces Obsidian-ready paper cards with source status, evidence anchors, wikilinks, and audit checks.
- Enforces deep AI paper-card structure for formal `type: paper-card` notes.
- Rejects shallow metadata-only, abstract-only, full-text-pending, or table-level-pending cards unless they are marked as stubs.
- Includes validators for structure and content-risk checks.

## Install

Clone this repository into your Codex skills directory:

```powershell
git clone https://github.com/<your-user>/<your-repo>.git "$env:USERPROFILE\.codex\skills\literature-matrix-research"
```

Or copy this folder to:

```text
~/.codex/skills/literature-matrix-research
```

## Usage

Ask Codex to use `$literature-matrix-research` for source-grounded literature matrices, Obsidian reading systems, or formal deep paper cards.

Default behavior:

- single-paper deep card: use this when you say `read this paper`, `精读这篇`, `analyze this paper`, or `做深度卡`. The skill should read PDF/full text/source evidence and create a formal `paper-card` with method pipeline, how/why/effect, formulas, original result-table evidence or a no-table statement, result interpretation, limitations, reproduction path, project fit, and novice detail check.
- matrix plus core deep cards: use this for a research question, paper corpus, or literature direction. The skill should build the literature matrix, split `core` / `bridge` / `supplemental` / `matrix-only`, then write formal deep cards for core papers after source review.
- full Obsidian package: use this when you need START, dashboard, staged reading order, matrices, formal paper-cards, source audit, and validation report.

Use search-only only when explicitly requested:

- search-only candidate table: say `search-only`, `candidate_table`, `找论文`, `seed expansion`, or `基础调查`. The skill should output `candidate_table.csv`, `candidate_table.jsonl`, `search_log.json`, `failed_queries.md`, `source_status`, `graph_relation`, and `layer`; it should not write deep cards yet.
- fast planning map: ask for a planning-stub research map. Entries should stay as `paper-stub` or `matrix-stub` until source evidence is sufficient for `paper-card` promotion.

Example prompts:

```text
Use literature-matrix-research to close-read this paper and create a formal paper-card from the PDF/full text.
```

```text
Use literature-matrix-research for this research question. Build the literature matrix, split core/bridge/supplemental/matrix-only, then write formal deep cards for the core papers after source review.
```

```text
Search-only / candidate_table / 找论文 / seed expansion / 基础调查 for this topic. Do not write deep cards yet.
```
## Validation

Validate the skill metadata:

```powershell
python <codex-home>\skills\.system\skill-creator\scripts\quick_validate.py <skill-root>
```

Validate an output paper-matrix package:

```powershell
python scripts\validate_structure.py <package-root> --require-beginner
python scripts\validate_content_risks.py <package-root>
```

## Public Repo Notes

This repository should contain only reusable skill instructions, references, and scripts. Do not commit private paper PDFs, converted full-text corpora, Obsidian vault outputs, local scratch packages, or personal machine paths.