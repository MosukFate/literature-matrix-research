# Workflow Upgrade Pressure Checks - 2026-11-01

## Figure workflow: before-edit baseline

Recorded before changing `pdf_source_extraction.md`. The original file SHA-256 is `47daf57b3ee1bec30d8052401b27e41e1a09b17a07606dcf548b58ae9d810893`.

Scenario: A rushed card update has `image-007.png` from a PDF extractor, an unverified label "Figure 3", and a vector/multipanel diagram. The PDF version is unspecified; a cover page may offset printed page numbers and the caption may continue outside the image. Only the filename is supplied. Produce a safe asset handoff and say whether it verifies a mechanism claim.

This baseline is a static contract-gap check, not a claimed agent failure or a measured extraction run. All four agent slots were occupied. The old reference requests source URL/path, extraction method, source status and generic figure anchors; it also already forbids unsupported status upgrades. It does not specify how an image file is mapped to an original figure, how full panels/captions are preserved, how PDF/printed pages and versions are separated, or a visual-check state.

| Required handoff element | Before-edit instruction coverage |
|---|---|
| Source URL/PDF path and method | Explicit |
| Anchor and no unsupported source-status upgrade | Explicit |
| Original figure number tied to the saved asset | No asset-mapping recipe |
| Complete panels/labels and exact full caption | No completeness check |
| Version; PDF page vs printed page | No separate fields |
| Saved asset path; optional crop coordinates | No figure ledger |
| Visual comparison state and unknown mapping | No figure-specific state |

## Forward scenario and acceptance checks

Use a fresh read-only agent when a slot is available. Give it the staged skill plus `references/pdf_source_extraction.md` and the same scenario above. Ask for a concrete extraction/verification plan and a figure-ledger row, without executing extraction or changing files.

Pass if it (1) checks official HTML/source assets first, then renders/crops the source PDF with the existing PDF skill; (2) preserves complete vector/multipanel content and full caption; (3) records original number, source/version, both page notions, asset path, method, optional bounding-box coordinates, supported claim and visual-check status; (4) leaves unconfirmed mapping/version/page/caption unknown; and (5) does not promote source status or treat a filename/extracted file as claim verification.

Forward result: a fresh read-only agent followed the staged workflow, kept the supplied Figure3 label/caption/version/pages unconfirmed, selected source assets then PDF render/crop, and separated visual correspondence from mechanism verification. A second scenario kept conflicting note identities unresolved and preserved personal annotations, images, IDs, and stub/card evidence gates. The check suggested making the image-object candidate method explicit in the ledger; that value is now included. No substantive workflow gap remained.

No paper input was supplied, so no original figure was extracted, mapped or visually verified in this upgrade. A scenario pass establishes instruction coverage only, not extraction quality or speed.

## Conference/Year Retrieval Checks

Observed RED: requested new-year proceedings were not fetched from the old fixed
volume/page lists. Additional failing regressions covered historical CVF `.py`
indexes, PMLR reissues, and lost workshop/main-event labels. GREEN resolves
official indexes using requested years, keeps event labels, and records failed,
unparsed, missing, partial and truncated coverage without claiming completeness.

Fourteen offline conference tests pass. The current official PMLR/CVF HTML
snapshots were also parsed successfully, including ICML/CVPR 2026; snapshots stay
outside the installed skill. Unknown-year PMLR entries remain skipped and
reported. A main-conference label filter is not a venue-quality verdict.

## Existing-Note Reuse Checks

Observed RED: the helper was absent, and discovery rejected `--notes-root`.
Fourteen matcher tests now cover primary identities, URL/version/case
normalization, Unicode titles, conflicting IDs, ambiguity, recursion and byte
preservation of existing notes/images. Four CLI tests cover the optional sidecar,
unchanged candidate CSV schema, missing roots, and reruns. A stale sidecar after
a later run without lookup was reproduced and fixed; old match decisions are
removed when that output directory is reused without `--notes-root`.

Matching remains read-only and carries declared note types without promoting
verification or stub/card status. Identity is read from supported opening
frontmatter, not related-work citations in the body.

Independent review found and verified fixes for stale sidecars and discarded
event labels. The original twelve function-style tests remain part of the
regression run alongside the thirty-two unittest cases. Protected card schema,
rewrite/table/quality-gate blocks, candidate schema and ranking/status logic are
compared with the pre-update installation before deployment.
