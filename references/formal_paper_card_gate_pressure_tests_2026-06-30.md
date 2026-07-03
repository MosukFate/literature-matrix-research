# Formal Paper-Card Gate Pressure Tests - 2026-06-30

## Scope

This file records the RED/GREEN check added after a commonsense long-tail entity matrix produced `type: paper-card` notes that were only source-level planning stubs.

## RED: Observed Failure

| Scenario | Expected behavior | Observed failure |
|---|---|---|
| User expects GASP-quality cards | Formal paper cards should contain layered method reconstruction, source evidence, result-table interpretation, limitations, and project fit | Cards averaged roughly 1.2k characters; method sections averaged roughly 100 characters |
| Package says `source-level ready` and `table-level pending` | Such notes should be `paper-stub` or `matrix-stub` until deep rewritten | Notes still used `type: paper-card`, making them look finished in Obsidian |
| Card has all required headings but almost no paper-specific substance | Validator should fail on depth and evidence gates | Existing validators passed a minimal fixture with headings, one-sentence summary, and a one-line method |
| No original result table was included | A formal paper card should include original result-table evidence or an explicit no-table statement | Cards had zero original tables and zero `结果解析 / Result interpretation` blocks |

## RED Fixture

`tmp_skill_tests/shallow_matrix/01_Test_Lane/O01_shallow.md` is a deliberately bad card:

- has valid frontmatter;
- has the one-sentence summary block;
- has the beginner section and all seven labels;
- has all legacy six-card headings;
- has a one-line `## 2` method section;
- has no original table, no result interpretation, and no no-table statement.

Before this update, both validators returned `EXIT=0` on that fixture.

## GREEN: Required Passing Behavior

Validators must now reject formal `type: paper-card` notes when they are actually stubs:

| Gate | Required behavior |
|---|---|
| Card type | `type: paper-card` means GASP-depth; source-level placeholders use `paper-stub` or `matrix-stub` |
| Method depth | `## 2` must contain layered how/why/effect reconstruction, not a one-line generic method |
| Evidence table | Include original result table plus immediate interpretation, or explicitly state no relevant extractable result table |
| Source status | `prior survey`, `source-level ready`, or `table-level pending` cannot silently pass as a finished paper card |
| Examples | Concrete examples or analogies must be embedded in analysis, not omitted or appended decoratively |

## Verification Commands

```powershell
python scripts\validate_structure.py tmp_skill_tests\shallow_matrix --require-beginner
python scripts\validate_structure.py <package-root> --require-beginner
```

Expected:

- the shallow fixture fails with `paper_card_too_short_for_deep_card`, `method_section_too_short_for_layered_reconstruction`, and missing table/interpretation gates;
- the commonsense package fails as a deep-card package until shallow notes are demoted or rewritten;
- lane indexes are not misclassified as paper cards.
