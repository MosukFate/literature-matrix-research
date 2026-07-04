# Skill Integration

Use this reference when a literature-matrix task needs capabilities already covered by other local skills. This skill is the orchestrator; do not reimplement the other skills' full workflows. Load the relevant supporting skill when its phase begins, then convert its output into the matrix/Obsidian package schema.

## Synchronous Skill Chaining Contract

Skills do not execute like APIs, but this skill can require the agent to load another skill before a phase begins. Treat this as synchronous orchestration: finish the supporting skill's phase, then hand its evidence back into the matrix package.

Use this decision rule:

| Trigger in user request | Load supporting skill | Handoff back into this skill |
|---|---|---|
| "update the skill", "merge skills", "make this reusable", "evolve this workflow" | `writing-skills`, then `superpowers:test-driven-development` | pressure-test file, protected-rule list, changed files, verification evidence |
| "find papers", "verify venue", "look up source", "official page" | `paper-lookup` | source ledger rows, identifiers, failed searches, source_status labels |
| "PDF", "table", "MarkItDown", "original results" | `pdf`, `markitdown` | local extraction path, table anchor, extraction status, manual-correction status |
| "Obsidian", "card", "Base", "Canvas", "wikilink" | `obsidian-markdown`, `obsidian-bases`, `json-canvas` as needed | valid frontmatter, links, Base/Canvas files, link-check result |
| "review claims", "novelty risk", "does this overclaim" | `academic-paper-reviewer` | findings with severity, evidence anchors, revision queue |
| "turn into proposal/paper" | `academic-paper` or `ml-paper-writing` | claim-evidence chain, citation plan, prose draft boundaries |
| "done", "sync", "final check" | `superpowers:verification-before-completion` | fresh command output and remaining gaps |

Keep the chain minimal. Loading three skills is justified only when the task actually spans three phases, for example: paper lookup -> PDF/table extraction -> Obsidian card rewrite.

## Protected Rule Preservation

When integrating another skill, do not let its style override this skill's approved matrix rules:

- `academic-paper` may polish prose, but it must not strengthen claims beyond source evidence.
- `deep-research` may suggest themes, but every paper-card claim still needs paper/source anchors.
- `markitdown` may convert tables, but broken extraction is not final evidence.
- `obsidian-markdown` may adjust syntax, but paper IDs, filenames, lane membership, and card schema remain stable unless the user asks for reorganization.
- `writing-skills` may refactor this skill, but previously approved rules are protected until a new pressure test and explicit user instruction supersede them.

## Routing Principle

Pick the smallest supporting skill set that covers the phase:

- Use `paper-lookup` for precise paper discovery, identifiers, metadata, citation graph, OA/PDF lookup, and raw database responses.
- Use `literature-review` for systematic search strategy, inclusion/exclusion criteria, multi-database search logs, screening counts, and PRISMA-style traceability.
- Use `deep-research` for broad field synthesis, research-question refinement, gap analysis, contradiction resolution, source verification, and devil's-advocate critique.
- Use `pdf` and `markitdown` for local PDF/TXT extraction, table extraction, and source material conversion.
- Use `academic-paper-reviewer` for critical review of claims, contribution/limitation balance, novelty risk, overgeneralization, and logic gaps.
- Use `academic-paper` or `ml-paper-writing` only when the user wants to turn the matrix into a proposal, related work, or manuscript text.
- Use `obsidian-markdown`, `json-canvas`, and `obsidian-bases` for Obsidian syntax, Canvas maps, and database-like views.
- Use `daily-paper-generator` or a monitoring workflow only when the user asks for recent-paper digests or ongoing updates.

## Phase Map

| Phase | Supporting skill | Required handoff into this skill |
|---|---|---|
| Research question is vague | `deep-research` or `brainstorming-research-ideas` | refined question, scope boundaries, in/out criteria |
| Skill or workflow maintenance | `writing-skills`, `superpowers:test-driven-development`, `superpowers:verification-before-completion` | pressure tests, protected rules, changed files, fresh validation evidence |
| Seed-paper expansion | `paper-lookup`, `deep-research` | candidate papers with official URLs, identifiers, why related |
| Systematic search | `literature-review`, `paper-lookup` | databases searched, search strings, date searched, raw results, screening log |
| Source verification | `paper-lookup`, `pdf`, `markitdown` | DOI/arXiv/OpenReview/venue identity, PDF/TXT path, table/figure anchors |
| Field synthesis | `deep-research` | themes, gaps, contradictions, closest prior work, novelty risks |
| Card critique | `academic-paper-reviewer` | factual errors, overclaims, missing limitations, revision queue |
| Obsidian packaging | `obsidian-markdown`, `json-canvas` | valid frontmatter, wikilinks, Markdown links, Canvas JSON |
| Proposal writing | `academic-paper`, `ml-paper-writing` | source-grounded related work, claim-evidence chains, citation plan |

## Mode Recipes

### `search-only`

Use `scripts/discover_candidates.py` or reproduce its output contract first for exact candidates, identifiers, citation graph signals, source_status, and ranking. Add `paper-lookup` for source verification and `literature-review` when the user needs systematic coverage rather than a quick candidate pool. Output:

- Query variants, databases, and official-source adapters.
- `candidate_table.csv` / JSONL rows with source_status, graph_relation, scores, and layer.
- Raw source URLs and identifiers.
- Inclusion/exclusion reason.
- Venue/source status.
- Preliminary mainline/supplement/matrix-only layer.

### `matrix`

Use `deep-research` for synthesis after candidate screening. Convert its themes into:

- Quicklook table.
- Venue trust split.
- Benchmark/results matrix.
- Research gap table.
- Similar-work/novelty-risk table.

### `obsidian-package`

Use `obsidian-markdown` for syntax and link conventions after the matrix is stable. Output:

- START and Dashboard.
- Stage indexes.
- Supplemental evidence pool index.
- Per-paper cards.
- Audit/source reports.
- Canvas or research map when useful.

### `audit-only`

Use `academic-paper-reviewer` for content judgment and `pdf`/`paper-lookup` for source checks. Output:

- Review matrix.
- Findings report.
- Evidence gaps.
- Broken-link and source-status checks.

### `card-polish`

Use `academic-paper-reviewer` to check overclaiming and `academic-paper` only for language polish when the user's goal is writing quality. Keep IDs, filenames, and links stable.

### `beginner-expansion`

Use the paper/card evidence first. Use `academic-paper-reviewer` for overclaim checks if the beginner layer adds formulas, mechanisms, or causal language.

## Handoff Contracts

When consuming another skill's output, preserve:

- Search date and source database.
- Raw URL or canonical identifier.
- Official PDF/proceedings URL when available.
- Local PDF/TXT path when extracted.
- Inclusion/exclusion reason.
- Evidence confidence and source_status.
- Any unresolved uncertainty.

Never collapse these into a fluent summary without keeping traceability.

## Search Expansion Heuristics

For an AI/ML field survey, run at least these query families unless the user narrows scope:

- Seed title and core method terms.
- Failure mode terms.
- Benchmark/dataset names.
- Mechanism terms: causal tracing, patching, attention head, neuron, SAE, steering, representation editing.
- Model family terms: LLaVA, Qwen-VL, InternVL, DeepSeek-VL, GPT-4V/4o, or the user's target models.
- Venue filters: ICLR, ICML, NeurIPS, CVPR, ICCV, ECCV, ACL, EMNLP, NAACL, AAAI, COLM, Findings, workshops, arXiv.

For each family, record what it found and what it failed to find. A failed query can be evidence that a niche is undercovered, but not proof of novelty.

## Novelty-Risk Audit

Use `deep-research` and `academic-paper-reviewer` together when a proposed idea is forming. Check:

- Same task and same benchmark.
- Same intervention level: decoding, attention, activation, training objective, data, evaluation protocol.
- Same model family.
- Same causal claim.
- Same math/objective.
- Same failure split.

The output should say whether the new work is:

- `distinct`: clear contribution margin.
- `adjacent`: related but separable.
- `high-risk`: must explicitly distinguish from prior work.
- `duplicate`: likely not novel enough without a new angle.

## Common Integration Mistakes

- Running `deep-research` and pasting its prose into cards without source anchors.
- Treating `paper-lookup` metadata as full-paper verification.
- Using `literature-review` systematic breadth but losing the Obsidian reading-order structure.
- Letting `academic-paper` polish make claims stronger than the evidence.
- Using `obsidian-markdown` links without verifying they resolve from each index's location.
- Creating a research map that shows every edge instead of only research-meaningful edges.
