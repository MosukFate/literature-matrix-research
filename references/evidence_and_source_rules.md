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

### Precise Claim Records and Experiment Context

For the card's important numerical, comparative, and implementation claims, retain an object-level record in the existing evidence ledger. Use one row per distinct claim or experimental context; this is not a requirement to catalog every sentence in the paper.

| Claim | Source/version and object | Direct locator | Experiment context | Reported value / derivation | Verification and boundary |
|---|---|---|---|---|---|
| Source-scoped statement | Section, equation, table row or figure; fixed code commit when relevant | Clickable PDF `#page=N` plus printed page if present, HTML anchor, or code file and lines | Model/size, data/split, metric/unit, baseline/decoding, relevant settings and runs | Separate author-reported mean/SD from calculated delta, ratio or explanatory example | Original-source checked / pending / static code only / reproduced; what remains unknown |

- Check attribution as well as arithmetic: a correct number located in a result table must not be described as appearing in the abstract unless it actually does. Split links when named objects occupy different pages. A reachable link alone does not verify its semantic target.
- Preserve units: percentage points versus relative percent, subset total versus full benchmark, maximum versus average, mean/SD versus significance. Distinguish static code correspondence from executed reproduction.
- Link implementation claims to the fixed commit and relevant line range when available; label incomplete snapshots and missing adaptation files. Retain paper, supplement, evaluation-entry, and shell defaults separately when they differ.
- A chapter-wide default is a reported instruction, not confirmation of a particular table's actual run. If broad defaults conflict and the table does not specify the setting, retain both source statements and mark the actual setting unconfirmed instead of choosing one by inference.
- For key evidence actually reused in the card, compare contexts before combining results. Check main-versus-ablation defaults, displayed component/total consistency when additive, and suspiciously identical cross-model/scale rows including SDs. Match metric definitions and overlapping subsets before adding values. This is a scoped source check, not an automatic audit of every table.
- Mark an unexplained inconsistency or duplication next to the affected claim and in the ledger; preserve reported values, state the two anchors, and avoid combining their increments. Do not silently repair source tables, allege misconduct, or discard unrelated evidence. If the comparison cannot be checked, record it as pending.

An acceptable compact record is: `author-reported F1 74.84±0.34→82.23±0.22; derived +7.39 pp; Qwen-VL/GQA/Popular/direct sampling vs VCD; Table 1, formal PDF p.6; five runs; source checked, not reproduced`. The locator and context carry the evidence; a subjective quality score does not.

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
