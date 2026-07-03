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

Ask Codex to use `$literature-matrix-research` for literature matrices, Obsidian paper-card packages, source-grounded reading orders, or deep card polishing.

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