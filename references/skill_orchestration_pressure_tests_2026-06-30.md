# Skill Orchestration Pressure Tests - 2026-06-30

## Scope

This file records pressure tests for the cross-skill orchestration and additive evolution refactor. It protects the user's requirement that future improvements may be added without disturbing the already-approved GASP-style literature-matrix rules.

## RED: Failure Modes To Prevent

| Scenario | Expected behavior | Failure to prevent |
|---|---|---|
| User asks whether this skill can call other skills | Explain phase-based skill chaining and encode routing rules | Treat the literature-matrix skill as a silo or paste other skills' full workflows into it |
| User asks to improve the skill after approving GASP-style cards | Preserve approved Paper-Original and Deep-Table rules | Rewrite those sections and accidentally weaken the GASP-style requirements |
| User later adds a new preference | Append through an evolution protocol and pressure test | Edit scattered files without recording what changed or why |
| Task needs PDF table extraction and Obsidian packaging | Load only the relevant supporting skills at the phase boundary | Force-load many skills or use absolute `@` references that bloat context |
| Another skill proposes polished prose | Keep evidence boundaries and source_status conservative | Let writing polish turn benchmark behavior into mechanism proof |

## GREEN: Required Passing Behavior

| Rule | Passing behavior |
|---|---|
| Skill chaining | `SKILL.md` points to `skill_integration.md`; the integration reference maps triggers to supporting skills and handoff artifacts |
| Additive evolution | `evolution_protocol.md` defines protected rules, update steps, and regression checks |
| Protected rules | The existing `Paper-Original Rewrite Rules` and `Deep-Table Rules` blocks remain byte-identical during this refactor |
| Minimal context | The skill names supporting skills instead of force-loading their file paths |
| Validation | Post-edit checks parse frontmatter/YAML, confirm active duplicate absence, verify protected blocks, and scan for banned active instructions |

## Verification Commands

```powershell
python scripts\package_skill.py <skill-root>
rg -n "Synchronous Skill Chaining Contract|Evolution Protocol|Skill Chaining and Evolution" <skill-root>
Test-Path <skill-root>
```

Expected:

- Package validation succeeds or reports only known non-blocking warnings.
- The new routing/evolution sections are discoverable.
- No overlapping active `literature-matrix-research` skill exists.
