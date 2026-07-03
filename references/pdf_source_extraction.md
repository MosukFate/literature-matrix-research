# PDF and Source Extraction

Use this reference when card claims need paper-level evidence.

## Extraction Order

1. Use existing local PDF/TXT/ledger if present.
2. Use official venue PDF.
3. Use arXiv PDF.
4. Use HTML full text when official PDF is unavailable.
5. Use abstract/project page only for metadata or explicitly stated abstract-level claims.

## Minimal Paper Evidence Record

For each deep card, record:

- Source URL.
- PDF URL or local PDF path.
- Extraction method.
- `source_status`.
- Unverified numbers, if any.
- Key table/figure/section anchors.
- Whether table-level verification is complete.

## Table and Figure Anchors

For benchmark or result claims, capture:

| Claim | Anchor | Extracted wording/value | Card wording | Status |
|---|---|---|---|---|

Anchor format examples:

- `Table 2, overall mitigation results`.
- `Figure 4, head intervention effect`.
- `Section 3.2, dataset construction`.
- `Appendix C, general ability check`.

## Extraction Methods

Use whichever is available:

- `pdftotext -layout paper.pdf -` for layout-preserving text.
- Python `pypdf` for simple text and metadata.
- Python `pdfplumber` for tables and layout when installed.
- MarkItDown or another converter for PDF -> Markdown when available.
- Manual browser/PDF inspection for tables that extraction garbles.

If extraction is poor, mark the claim `needs manual PDF check` rather than guessing.

## Numeric Claim Policy

Never copy a number into a card unless it has an anchor. This includes:

- Dataset size.
- Model count.
- Accuracy/score.
- Percentage.
- Rank.
- Number of heads/layers/tokens.
- Benchmark split.

If a number appears only in a secondary source, keep it out of the card or mark it as secondary metadata.

## Formula Policy

For important formulas:

- Quote or reconstruct only the relevant formula.
- Explain every symbol.
- State whether it is an original paper formula or a guide-level formalization.
- Anchor it to paper section/equation when possible.

If the paper does not give a formula but the method can be explained mathematically, label it as "导读层形式化".

## Source Status Upgrade Rules

Do not upgrade:

- `metadata verified` to `full paper verified` without reading the full paper.
- `full paper verified` to `table-level verified` without table/figure anchors.
- `arXiv-only` to venue verified because an abstract or comment says accepted.

Upgrade only when the official source and checked evidence support the stronger status.
