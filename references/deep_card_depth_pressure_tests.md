# Deep Card Depth Pressure Tests

Use this reference when evolving or auditing the literature-matrix skill's deep-card behavior.

## Regression: long shallow card passed

Old failure: a formal `type: paper-card` could pass validation even when it was only metadata/abstract-level. The card had all 0-10 headings, enough characters, generic method language, a formula paragraph, a baseline paragraph, and a no-table statement. It also admitted that full-text/table-level deep reading was pending.

Expected behavior: this must fail. A formal card cannot pass when it contains any of these evidence states:

- `metadata verified`
- `metadata-only`
- `abstract only` or `abstract-level`
- `source-level only` or `source-level ready`
- `prior survey`
- `full-text pending`
- `table-level pending`
- `deep reading pending`
- statements that the full paper/PDF/HTML was not read

Use `type: paper-stub` or `type: matrix-stub` until the card is source-grounded enough to replace a first serious reading.

## Novice Detail Check

Every formal `paper-card` must include:

```markdown
### 小白细节自检 / Novice detail check
```

The check asks whether a first-time reader can reconstruct:

- the paper's input and output;
- the actual pipeline and modules;
- objective/loss/scoring rule;
- training or inference path;
- evaluation setup and table/figure/section anchors;
- baseline difference at mechanism level;
- reproduction blockers and unknown details.

If the answer is insufficient, run one source-backed repair pass. After that one pass, either the card is good enough or it is demoted to `paper-stub`. Do not loop forever and do not pad with generic prose.

## Positive Control

A good formal card does not need to be perfect, but it must be auditable:

- source status says the paper/PDF/HTML or converted full text was checked;
- method section lets a novice rebuild the pipeline in their head;
- formulas are mapped to implementation or explicitly marked as absent;
- experiments include table/figure/section anchors or a source-grounded no-table statement;
- claims are scoped to what the source evidence supports;
- the novice check says what is now reconstructable and what remains unknown.
