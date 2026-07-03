# Standalone Research Workflow

Use this reference when no separate literature-review, deep-research, paper-lookup, PDF, reviewer, or Obsidian skills are available. It compresses those capabilities into one workflow, with traceability preserved for every paper and claim.

## Mode Selection

| User need | Mode | Minimal output |
|---|---|---|
| Candidate papers only | `search-only` | source table, inclusion/exclusion, trust layer |
| Known paper set needs structure | `matrix` | quicklook, venue split, benchmark/results matrix |
| Full reading system | `obsidian-package` | START, dashboard, stage indexes, cards, audits |
| Existing package check | `audit-only` | review matrix, findings report, link/source checks |
| Existing card improvement | `card-polish` | edited cards, polish report |
| Make cards understandable | `beginner-expansion` | beginner-readable `## 0` and `## 2` plus formula/limit checks |

Default to `obsidian-package`.

## End-to-End Pipeline

1. **Intake**: capture seed paper/topic, target field, target venue, date range, must-include papers, excluded areas, language, and output mode.
2. **Question shaping**: define the core phenomenon, mechanism hypothesis, target tasks, failure modes, baseline families, and expected contribution type.
3. **Search plan**: create 5-8 query families covering seed title, method terms, failure terms, benchmark names, model families, mechanism terms, and venue filters.
4. **Source collection**: search official pages and broad databases; record raw URL, title, authors, venue/source, year, DOI/arXiv/OpenReview ID, PDF URL, code/data URL.
5. **Screening**: classify as include-mainline, include-supplemental, matrix-only, defer, or exclude. Record reason.
6. **Deduplication**: merge by DOI, arXiv ID, OpenReview ID, exact title, official venue page, and author/year/title similarity.
7. **Trust split**: assign mainline/supplement/matrix-only status; do not mix venue trust with content correctness.
8. **Matrix construction**: build quicklook, venue trust split, benchmark/results, method taxonomy, and novelty-risk table.
9. **Deep cards**: write cards only after matrix gaps are visible; each formal `paper-card` needs source_status, one-sentence summary, the AI paper deep-read schema, and evidence anchors.
10. **Synthesis**: build reading rounds by conceptual dependency, not just venue or chronology.
11. **Audit**: run structure and content risk checks; manually verify major findings against sources.
12. **Package**: produce START/Dashboard/stage indexes/supplemental index; expose counts and mainline/supplement distinction.

## Multi-Agent Roles Without External Skills

If subagents are available, split them by output boundary:

- Search scout: query families, source URLs, identifiers, candidate pool.
- Source auditor: official source, PDF, table/figure anchors, source_status.
- Matrix architect: categories, rounds, mainline/supplement split.
- Card writer: per-paper cards using the AI paper deep-read schema.
- Reviewer: overclaiming, limitations, novelty risk, logic gaps.
- Coordinator: counts, links, consistency, final reports.

If subagents are not available, run the same roles sequentially and keep a short handoff note after each phase.

## Deliverable Contract

Every final package should state:

- Total matrix entries.
- Deep-card count.
- Mainline count.
- Supplemental count.
- Matrix-only count.
- Source-level verified count.
- Table/PDF-level verified count when available.
- Known limitations and unresolved verification queue.

## Stop Conditions

Do not finalize if:

- Main navigation links are broken.
- Deep card counts and stage indexes disagree.
- Critical/major findings lack evidence anchors.
- Matrix-only papers are treated as deep-reviewed.
- A proposed novelty claim has not been checked against closest similar work.
