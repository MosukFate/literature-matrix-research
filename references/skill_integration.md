# Skill Integration

Use this reference when a literature-matrix task needs capabilities already covered by other local skills. This skill is the orchestrator; do not reimplement the other skills' full workflows. Load the relevant supporting skill when its phase begins, then convert its output into the matrix/Obsidian package schema.

## ARS-Codex Workflow Resolution

This skill reuses ARS research, reviewer, and writing support through the installed
`academic-research-suite` skill. Load that entry at the relevant phase boundary,
then load the selected internal workflow and the mode/role files it requires.
The ARS names below are internal workflows, not separately installed skills.

| Phrase in this reference | Load supporting skill | Select internal workflow |
|---|---|---|
| ARS research workflow | `academic-research-suite` | `deep-research` |
| ARS reviewer workflow | `academic-research-suite` | `academic-paper-reviewer` |
| ARS writing workflow | `academic-research-suite` | `academic-paper` |

The suite resolves workflow entries as `WORKFLOW.md`. Consume the installed
workflow's current rules rather than copying an ARS snapshot into this skill.
Missing legacy standalone entries do not mean ARS is unavailable. If the suite
itself is absent, use `end_to_end_research_workflow.md` and disclose the missing
support; if an installed suite's selected workflow cannot be loaded, report that
loading failure rather than pretending the handoff ran.

Keep `literature-matrix-research` as the orchestrator for matrix/card requests.
Pass the exact phase goal, source coverage, evidence anchors, and requested
handoff to ARS. For card-level critique, use scoped reviewer support (such as
`quick` or `methodology-focus`) rather than defaulting to full manuscript review.
Return findings, severity, anchors, and uncertainties to the matrix schema.
For card-only language polish, keep `card-polish` in charge and consult ARS
writing-quality guidance as a reference. Select a writing mode only if the
installed workflow declares one for the requested task.
Select writing, a full research-to-paper pipeline, or `sr-screener` only when the
user requests that work. For an explicit full manuscript review, let the current
ARS mode enforce its review and claim-check contracts; matrix critique headings
alone do not constitute an ARS review panel or independent executions.

## Synchronous Skill Chaining Contract

Skills do not execute like APIs, but this skill can require the agent to load another skill before a phase begins. Treat this as synchronous orchestration: finish the supporting skill's phase, then hand its evidence back into the matrix package.

Use this decision rule:

| Trigger in user request | Load supporting skill | Handoff back into this skill |
|---|---|---|
| "update the skill", "merge skills", "make this reusable", "evolve this workflow" | `writing-skills`, then `superpowers:test-driven-development` | pressure-test file, protected-rule list, changed files, verification evidence |
| "find papers", "verify venue", "look up source", "official page" | `paper-lookup` | source ledger rows, identifiers, failed searches, source_status labels |
| "PDF", "table", "MarkItDown", "original results" | `pdf`, `markitdown` | local extraction path, table anchor, extraction status, manual-correction status |
| "Obsidian", "card", "Base", "Canvas", "wikilink" | `obsidian-markdown`, `obsidian-bases`, `json-canvas` as needed | valid frontmatter, links, Base/Canvas files, link-check result |
| "review claims", "novelty risk", "does this overclaim" | the ARS reviewer workflow | findings with severity, evidence anchors, revision queue |
| "cross-PDF question", "citation spot check", "find contradictions in these PDFs" | `paperqa2-audit` | candidate evidence JSONL, context locators, manual PDF verification queue |
| "keep asking about this paper", "talk to this paper", "persistent paper Q&A" | `paper2agent`, selecting Paper2Skill | matching source-bundle entry, version and verification state, precise source-backed answers |
| "run this paper's code", "apply its method to new data" | `paper2agent`, selecting Paper2MCP | tested source-bound tools/results, runtime requirements and actual execution limits |
| "turn into proposal/paper" | the ARS writing workflow or `ml-paper-writing` | claim-evidence chain, citation plan, prose draft boundaries |
| "done", "sync", "final check" | `superpowers:verification-before-completion` | fresh command output and remaining gaps |

Keep the chain minimal. Loading three skills is justified only when the task actually spans three phases, for example: paper lookup -> PDF/table extraction -> Obsidian card rewrite.

## Protected Rule Preservation

When integrating another skill, do not let its style override this skill's approved matrix rules:

- The ARS writing workflow may polish prose, but it must not strengthen claims beyond source evidence.
- The ARS research workflow may suggest themes, but every paper-card claim still needs paper/source anchors.
- `markitdown` may convert tables, but broken extraction is not final evidence.
- `obsidian-markdown` may adjust syntax, but paper IDs, filenames, lane membership, and card schema remain stable unless the user asks for reorganization.
- `writing-skills` may refactor this skill, but previously approved rules are protected until a new pressure test and explicit user instruction supersede them.
- Paper2Skill supplies reusable source material, not a replacement card or a scientific-verification verdict. Keep card IDs/files, formal depth, original-table interpretation and source-status gates intact.

## Routing Principle

Pick the smallest supporting skill set that covers the phase:

- Use `paper-lookup` for precise paper discovery, identifiers, metadata, citation graph, OA/PDF lookup, and raw database responses.
- Use `literature-review` for systematic search strategy, inclusion/exclusion criteria, multi-database search logs, screening counts, and PRISMA-style traceability.
- Use the ARS research workflow for broad field synthesis, research-question refinement, gap analysis, contradiction resolution, source verification, and devil's-advocate critique.
- Use `pdf` and `markitdown` for local PDF/TXT extraction, table extraction, and source material conversion.
- Use the ARS reviewer workflow for critical review of claims, contribution/limitation balance, novelty risk, overgeneralization, and logic gaps.
- Use the ARS writing workflow or `ml-paper-writing` only when the user wants to turn the matrix into a proposal, related work, or manuscript text.
- Use `obsidian-markdown`, `json-canvas`, and `obsidian-bases` for Obsidian syntax, Canvas maps, and database-like views.
- Use `daily-paper-generator` or a monitoring workflow only when the user asks for recent-paper digests or ongoing updates.
- Use `paperqa2-audit` only after a local corpus has passed source screening. It is an optional RAG audit layer, not a discovery replacement or source authority.
- Use `paper2agent` for the selected paper's reusable source bundle and continued dialogue; use its Paper2MCP route only for requested research-code execution. Follow `paper_dialogue.md` for the handoff and answer boundaries.

## Phase Map

| Phase | Supporting skill | Required handoff into this skill |
|---|---|---|
| Research question is vague | the ARS research workflow or `brainstorming-research-ideas` | refined question, scope boundaries, in/out criteria |
| Skill or workflow maintenance | `writing-skills`, `superpowers:test-driven-development`, `superpowers:verification-before-completion` | pressure tests, protected rules, changed files, fresh validation evidence |
| Seed-paper expansion | `paper-lookup`, the ARS research workflow | candidate papers with official URLs, identifiers, why related |
| Systematic search | `literature-review`, `paper-lookup` | databases searched, search strings, date searched, raw results, screening log |
| Source verification | `paper-lookup`, `pdf`, `markitdown` | DOI/arXiv/OpenReview/venue identity, PDF/TXT path, table/figure anchors |
| Cross-PDF evidence audit | `paperqa2-audit` | manifest fingerprint, candidate answers, context locators, unresolved verification queue |
| Persistent single-paper dialogue | `paper2agent`, selecting Paper2Skill | paper/card identity, bundle path/version, verification report/status, limitations and source anchors |
| Field synthesis | the ARS research workflow | themes, gaps, contradictions, closest prior work, novelty risks |
| Card critique | the ARS reviewer workflow | factual errors, overclaims, missing limitations, revision queue |
| Obsidian packaging | `obsidian-markdown`, `json-canvas` | valid frontmatter, wikilinks, Markdown links, Canvas JSON |
| Proposal writing | the ARS writing workflow, `ml-paper-writing` | source-grounded related work, claim-evidence chains, citation plan |

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

Use the ARS research workflow for synthesis after candidate screening. Convert its themes into:

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

Use the ARS reviewer workflow for content judgment and `pdf`/`paper-lookup` for source checks. Output:

- Review matrix.
- Findings report.
- Evidence gaps.
- Broken-link and source-status checks.

Load `paperqa2-audit` inside this mode only when the request needs cross-PDF semantic retrieval, citation spot checks, or contradiction candidates. Preserve its `candidate evidence` label. Confirm page, section, table, or figure anchors against the original PDF before accepting a finding.

### `card-polish`

Keep this skill's card-polish recipe in charge. Use the ARS reviewer workflow to check overclaiming and consult ARS writing-quality guidance when the user's goal is language polish. Keep IDs, filenames, and links stable.

### `paper-dialogue`

Follow `paper_dialogue.md`. Keep the existing card as the explanatory layer and build or reuse a matching Paper2Skill bundle as the source layer. Answer from the relevant source passage, figure or table. Persist only reusable checked findings and unresolved questions in the selected paper's existing evidence area; do not rewrite the card from every chat response.

### `beginner-expansion`

Use the paper/card evidence first. Use the ARS reviewer workflow for overclaim checks if the beginner layer adds formulas, mechanisms, or causal language.

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

Use the ARS research workflow and the ARS reviewer workflow together when a proposed idea is forming. Check:

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

- Running the ARS research workflow and pasting its prose into cards without source anchors.
- Treating `paper-lookup` metadata as full-paper verification.
- Using `literature-review` systematic breadth but losing the Obsidian reading-order structure.
- Letting the ARS writing workflow polish make claims stronger than the evidence.
- Using `obsidian-markdown` links without verifying they resolve from each index's location.
- Letting PaperQA2 answers directly update cards, source status, numbers, or contradiction claims without original-source verification.
- Creating a research map that shows every edge instead of only research-meaningful edges.
