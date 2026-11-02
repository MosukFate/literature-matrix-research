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

## Original Figure Assets and Provenance

For figures from the selected paper/version, reuse the existing `pdf` skill for rendering and visual inspection; no separate extraction dependency is required. This asset workflow does not change the source hierarchy above.

1. Check official HTML/source assets first (including arXiv HTML for an arXiv source). Match the asset to the original figure label and full caption in that version; a filename or PDF image-object index is not a Figure number.
2. If the asset is absent or incomplete, render the relevant PDF page(s) with the PDF skill's available renderer, then crop the rendered page if needed. This preserves vector diagrams and multipanel layouts. Keep the full page render as a comparison reference.
3. Save the complete original figure, including every panel, label, axis and legend, plus access to the full original caption. The exact caption may be adjacent text linked from the ledger rather than inside the crop. For a shared export, link to the full caption on the identified official PDF page/HTML figure instead of repeating a long textual quotation. Keep the original number and a short source-faithful description beside the image. Do not present a redraw as an original figure.
4. Compare the saved asset and caption visually against the source HTML/PDF. Confirm the number, version, panels and caption completeness before marking the visual check `verified`; retain `unknown` or `needs manual PDF check` when correspondence cannot be confirmed.
5. Embed or link the asset beside the claim it supports and keep this ledger with the paper's evidence record. An extracted file is candidate evidence: it neither verifies the supported claim nor promotes `source_status`. Preserve the existing numeric, formula and table-verification rules.

At the reading position, provide the original number, clickable original PDF page/HTML figure, caption access, and a short explanation of what the figure supports and does not establish. For dense tables or multipanel examples, also link the full-resolution master. More embedded images do not establish a better explanation.

Treat incomplete image-object extraction as a trigger for the page-render fallback above, not as evidence that the paper lacks a diagram. Keep the full-page comparison render during checking. In the final export, bundle that render with a package-relative path, or omit its workspace-only pointer and supply an anchored official source page for rechecking. Do not label the official PDF URL as a saved render path.

Run `python scripts/validate_evidence_links.py path/to/final-export` after copying/exporting. It checks local Markdown/image links and ledger asset/render pointers for missing or out-of-package targets. Correct figure/page correspondence, caption completeness and scientific support still require original-source inspection; a packaging pass cannot mark them verified.

Use one ledger entry per figure; write `unknown` for unconfirmed fields:

```yaml
original_figure: "Figure 3 | unknown"
full_caption: "Exact full caption, path#anchor to adjacent exact text, or official locator to the identified full caption | unknown"
source_and_version: "Source URL/local PDF and exact version | unknown"
pdf_page: "1-based PDF page(s) | not applicable (HTML-only) | unknown"
printed_page: "Printed label(s) | unnumbered | unknown"
asset_path: "Saved original asset/render/crop path | unknown"
extraction_method: "official-source-asset | PDF-page-render | rendered-page-crop | PDF-image-object-candidate | unknown"
source_page_render: "Full page render path for PDF comparison | not applicable"
source_page_url: "Anchored official PDF page/HTML figure for portable rechecking | unknown"
crop_bbox: "Optional [x0, y0, x1, y1], with coordinate units and origin"
supported_claim: "Source-anchored claim and what the figure does not establish | unknown"
visual_check_status: "pending | verified | needs manual PDF check | unknown"
```
