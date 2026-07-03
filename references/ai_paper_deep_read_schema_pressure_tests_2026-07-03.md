# AI Paper Deep-Read Schema Pressure Tests - 2026-07-03

## Scope

This file records the RED/GREEN checks for replacing the old six-section formal paper-card skeleton with the 0-10 AI paper deep-read schema.

## RED: Observed Failures Before Skill Edit

| Scenario | Expected behavior | Observed failure |
|---|---|---|
| User asks every card to follow the AI paper-reading requirements | Formal `paper-card` should include positioning, intuition, method, formula/derivation, baseline difference, experiments, reproduction, reading advice, and final summary | Existing validator required the old six headings and rejected a valid 0-10 card |
| User asks for whole-structure rebuild without repetition | The new schema should replace the legacy six-section body instead of being appended | Existing references told agents to preserve the legacy six-heading card body |
| Card contains `source-level verified` | Verified source status should not be treated as a stub | Existing `source-level` regex classified verified cards as stub-like |
| Only current entry remains installed | UI metadata and packaging should point to `literature-matrix-research` | Existing docs and metadata still referenced the removed duplicate trigger |

## GREEN: Required Passing Behavior

| Scenario | Passing rule now encoded |
|---|---|
| Formal AI paper card | Must contain 0-10 deep-read headings from `ai_paper_deep_read_card_schema.md` |
| Formula section | Must explain formulas or explicitly state the paper has no confirmable formula details, and map formulas to algorithm/implementation |
| Baseline section | Must state concrete baseline differences rather than only "better result" |
| Reproduction section | Must include minimum reproduction path, implementation blockers, or explicit missing-detail boundaries |
| Source status | `source-level verified` is allowed; `source-level ready`, `prior survey`, and `table-level pending` remain stub-like |
| Active entry | References point to `literature-matrix-research`, not the removed duplicate trigger |

## Verification Commands

Run after editing:

```powershell
python scripts\validate_structure.py tmp_skill_tests\new_schema_valid --require-beginner
python scripts\validate_content_risks.py tmp_skill_tests\new_schema_valid
rg -n "<legacy six-section phrase>|<removed duplicate trigger>|<legacy canonical wording>" <skill-root>
```

Expected:

- The new-schema fixture passes both validators.
- Search returns no active instruction pointing future users to the removed duplicate trigger. Hits in historical pressure-test files are acceptable only if clearly historical.
