# Evidence and Source Rules

Use this reference whenever a matrix, card, or audit makes claims about paper content, venue, benchmark, model, table results, formulas, or novelty.

## Source Hierarchy

Prefer sources in this order:

1. Official conference/proceedings page.
2. Official PDF from proceedings, OpenReview, ACL Anthology, CVF, NeurIPS, ICML, ICLR, AAAI, EMNLP, or publisher site.
3. arXiv PDF when no proceedings version is available or when checking preprints.
4. Author project page, GitHub, Hugging Face, Papers With Code for artifacts and model/data availability.
5. Semantic Scholar, Crossref, OpenAlex, DOI metadata for discovery and cross-checking.
6. Web summaries only for leads, never for final technical claims.

Use local PDF/TXT/ledger first when available. Use network lookup only to fill missing official metadata, DOI/arXiv/OpenReview identity, or source anchors.

## Source Status Vocabulary

Use conservative labels:

- `official proceedings verified`.
- `full paper verified`.
- `table-level primary PDF verified`.
- `source-level verified; table-level ledger pending`.
- `metadata verified; full-text pending`.
- `arXiv-only; no venue verification`.
- `venue pending`.
- `matrix-only; no deep card`.

Do not strengthen source_status unless the card has corresponding evidence.

## Numeric and Table Claims

Any claim involving a number, rank, dataset size, benchmark score, model count, percentage, or table comparison must have an anchor:

- Paper section.
- Table or figure number.
- Ledger path.
- Official abstract/page when it explicitly states the number.
- Local PDF/TXT extraction path.

If no anchor exists, write:

- `未核验数字`.
- `需回原文`.
- `source-level only`.

## Formulas

Formula rules:

- Include important formulas when the paper's method depends on them.
- Explain every symbol.
- Distinguish original paper formulas from explanatory formalizations.
- Do not invent formulas to decorate a note.
- If a formula is reconstructed from prose, mark it as "导读层形式化" or "可读化表达".

## Venue Trust Split

Default trust split:

- Mainline: top-conference main paper, strong CORE A/A* source, or user-approved trusted venue.
- Supplemental: arXiv, Findings, workshop, technical report, project page, pending proceedings, or lower-trust but high-relevance work.
- Matrix-only: relevant but not yet deep-reviewed.

Venue trust is not the same as content truth. A top venue can still have an overread card; an arXiv paper can still be useful as a hypothesis or baseline.

## Claim Strength

Use cautious language unless causal or table-level evidence supports stronger claims:

- `supports`, `suggests`, `reports`, `shows in this setup`, `can be used as a hypothesis`.
- Avoid `proves`, `must`, `always`, `fully`, `only`, `SOTA`, or `directly proves` without exact source-scoped support.

## Similar-Idea and Novelty Audit

For a proposed research direction:

- Identify closest prior work first.
- State overlap in task, method, model, benchmark, and intervention level.
- State required novelty margin.
- Put high-overlap arXiv or pending work in supplemental if venue trust is low but novelty risk is high.

## Docling and External Extraction

Do not default to unapproved candidate tools. Use existing PDF extraction first. Use Docling or other supplemental extraction only when existing extraction is insufficient and the tool is installed or approved.
