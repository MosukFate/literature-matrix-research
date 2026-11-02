# Discovery Pipeline

Use this reference when `search-only`, seed-paper expansion, or novelty-risk discovery needs more than a one-off paper lookup.

## Goal

Turn a seed paper or research question into a traceable candidate pool before any Obsidian deep-card writing starts. The pipeline is PaperQA2-inspired in structure: candidate search, metadata-aware merge, citation/related-work expansion, relevance re-ranking, and source-grounded handoff. Do not require PaperQA2 as an installed dependency.

## Required Outputs

Run or emulate `scripts/discover_candidates.py` and preserve:

- `candidate_table.csv`
- `candidate_table.jsonl`
- `search_log.json`
- `failed_queries.md`

Never replace these ledgers with a prose-only literature list.

## Candidate Schema

Required fields:

`id`, `title`, `year`, `venue`, `sources`, `source_status`, `layer`, `overall_score`, `relevance_score`, `venue_score`, `citation_score`, `recency_score`, `novelty_risk_score`, `citation_count`, `graph_relation`, `doi`, `arxiv_id`, `openreview_id`, `acl_id`, `pmlr_url`, `cvf_url`, `semantic_scholar_id`, `openalex_id`, `official_url`, `pdf_url`, `code_url`, `data_url`, `why_relevant`, `why_core`, `query`, `abstract`.

## Source Adapters

Use these sources in parallel when network access is available:

- arXiv for recent preprints and arXiv IDs.
- Semantic Scholar for metadata, citations, references, related papers, and OA PDFs.
- OpenAlex for broad metadata, DOI, venue, and citation counts.
- OpenReview for ICLR/NeurIPS-style official forum pages.
- PMLR for ICML/AISTATS/COLT official proceedings.
- ACL Anthology for ACL/EMNLP/NAACL/COLM official pages.
- CVF Open Access for CVPR/ICCV/ECCV official pages.

If an adapter fails or times out, record it in `failed_queries.md`; do not silently drop it.

## Merge Policy

Deduplicate in this order:

1. DOI.
2. arXiv ID.
3. OpenReview ID.
4. Official venue URL.
5. Normalized exact title.

When sources conflict, official venue metadata wins over arXiv, and arXiv wins over aggregator metadata. Keep all IDs when possible.

## Source Status

Use conservative labels:

- `official:openreview`
- `official:icml-pmlr`
- `official:acl-anthology`
- `official:cvf`
- `official:neurips`
- `official:aaai`
- `arxiv-only`
- `project/code-only`
- `metadata-only`

An arXiv-only paper may be `core` or `bridge` only when it has direct value for the research gap, code/data, strong evidence, or novelty-risk relevance. It must keep `source_status: arxiv-only` and must include `why_core`.

## Scoring

The script emits these scores in `[0, 1]`:

- `relevance_score`: title/query/abstract overlap with the user gap and mechanism/failure terms.
- `venue_score`: official top venue > arXiv > project/code > metadata-only.
- `citation_score`: log-scaled citation count.
- `recency_score`: favors recent work without discarding older foundations.
- `novelty_risk_score`: citation graph relation plus direct method overlap.
- `overall_score`: weighted ranking, not a proof of importance.

Never let citation count alone promote a paper to `core`.

## Layer Assignment

- `core`: one deep read can start or materially advance a sub-work package: direct method, direct benchmark, mechanism tool, closest prior work, or direct novelty threat.
- `bridge`: connects two required areas, such as long-tail factual knowledge and activation patching.
- `supplemental`: useful background, lower-trust evidence, broad survey, or tool/system support.
- `matrix-only`: keep in the candidate map, but do not create a formal deep card yet.
- `excluded`: irrelevant or too weakly sourced.

Formal `paper-card` creation still follows the existing 0-10 deep-card schema and table evidence rules.

## Conference/Year Retrieval and Existing Notes

Use requested year bounds to choose proceedings indexes before fetching papers.
PMLR volumes and CVF conference pages must come from the official indexes rather
than a frozen volume/year list. With no bounds, the proceedings adapters use the
current calendar year and the previous two years; broader historical searches
need explicit bounds. `--proceedings-venue` narrows those proceedings adapters,
not every aggregator result in the candidate pool.

```powershell
python scripts/discover_candidates.py --query "visual hallucination" --year-from 2026 --year-to 2026 --proceedings-venue ICML --proceedings-venue CVPR --notes-root <reading-package-or-vault> --out-dir <discovery-output>
```

Read `source_coverage` in `search_log.json` together with `failed_queries.md`.
Report fetched indexes, requested years/venues, retrieval limits, missing
indexes, and any incomplete coverage. A failed or absent directory is missing
coverage, not evidence that no relevant paper exists. A bounded result list is
not an exhaustive conference survey. Publication/source verification and the
candidate ranking rules above still apply.
Keep the official event label in `venue`; PMLR workshop volumes and main
proceedings must remain distinguishable. `--proceedings-venue ICML` is a label
filter and can also find volumes labelled "at ICML"; it does not itself certify
main-track publication.

When the target package or vault is known, `--notes-root` scans its Markdown
notes without editing them and writes `existing_note_matches.jsonl` beside the
candidate table. The candidate CSV schema remains unchanged. Each sidecar row
preserves the candidate ID/title, match status/reason, and matched note path(s)
and declared note type.

- Match primary note metadata by normalized DOI, version-normalized arXiv ID,
  OpenReview ID, then normalized exact title. Related-work citations in the body
  are not the note's identity.
- Reuse a unique matched note's existing ID/path, read its contents, and update
  only the requested/generated material through the card-polish preservation
  recipe. Keep personal notes/questions, manually added evidence, and images.
- Review ambiguous matches and conflicting identifiers before selecting a note.
  A fuzzy title similarity is not an automatic identity match.
- Preserve the existing note's declared type and evidence state. A matched
  `paper-stub` remains a stub until the original deep-card gates are satisfied.
- Without `--notes-root`, discovery keeps its candidate outputs and removes any
  stale note-match sidecar from a previous run in the same output directory.

The matcher supports top-level scalar identity metadata in opening frontmatter;
unsupported multiline/list-only metadata can remain unmatched and should be
checked manually before creating a new card. See `card_polish_workflow.md` for
the preservation contract.
