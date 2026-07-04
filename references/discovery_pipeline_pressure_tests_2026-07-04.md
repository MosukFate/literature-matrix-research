# Discovery Pipeline Pressure Tests - 2026-07-04

These pressure tests protect the online discovery and citation graph extension behavior.

## Test 1: Seed plus gap must produce ledgers

Prompt: "Use literature-matrix-research to expand a seed paper about long-tail factual knowledge and internal reasoning trajectories."

Expected behavior:

- Produce or request a `candidate_table.csv` style ledger.
- Include source IDs, source_status, failed searches, and inclusion/exclusion notes.
- Do not answer with only a prose list of papers.

Old failure:

- Keyword search only, no raw URLs, no failed-query ledger, no official source distinction.

## Test 2: Official venue beats aggregator metadata

Scenario: The same paper appears from arXiv, Semantic Scholar, OpenAlex, and PMLR.

Expected behavior:

- Deduplicate into one row.
- Preserve arXiv/S2/OpenAlex IDs.
- Use PMLR as `official_url`.
- Set `source_status` to `official:icml-pmlr`.

Old failure:

- Duplicate rows or arXiv treated as the canonical source despite an official proceedings page.

## Test 3: arXiv-only can be core but must stay labeled

Scenario: A 2025 arXiv paper directly studies the user's gap and has code, but no proceedings page.

Expected behavior:

- It may enter `core` or `bridge`.
- `source_status` remains `arxiv-only`.
- `why_core` explains why the paper is worth deep reading despite lower venue trust.

Old failure:

- Either discarding valuable arXiv papers entirely or silently treating them as official.

## Test 4: High citations do not override low relevance

Scenario: A highly cited generic neural-network survey appears in search results.

Expected behavior:

- High `citation_score` is allowed.
- Low `relevance_score` prevents `core`.
- The paper becomes `supplemental` or `matrix-only`.

Old failure:

- Highly cited but weakly relevant papers crowd out direct mechanism or benchmark papers.

## Test 5: Deep-card rules remain protected

Scenario: Discovery finds a strong candidate pool.

Expected behavior:

- The pipeline stops at candidate/source handoff.
- Formal `paper-card` writing still uses the existing 0-10 deep-read schema, original table evidence, GASP-style method reconstruction, and novice detail check.

Old failure:

- Discovery upgrades accidentally weaken deep-card constraints or create shallow formal cards.
