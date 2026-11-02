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
$skillRoot = (Resolve-Path .).Path
python scripts\package_skill.py "$skillRoot"
rg -n "Synchronous Skill Chaining Contract|Evolution Protocol|Skill Chaining and Evolution" "$skillRoot"
Test-Path "$skillRoot"
```

Expected:

- Package validation succeeds or reports only known non-blocking warnings.
- The new routing/evolution sections are discoverable.
- No overlapping active `literature-matrix-research` skill exists.

## ARS-Codex Unified Entry Migration - 2026-11-01

Baseline environment: ARS-Codex 3.24.0 exposes `academic-research-suite`; the
standalone `deep-research`, `academic-paper-reviewer`, `academic-paper`, and
`academic-pipeline` entries are absent.

Observed RED: a matrix-plus-critique request followed the current integration
reference to nonexistent `deep-research/SKILL.md` and
`academic-paper-reviewer/SKILL.md`. The installed suite already contained both
internal `WORKFLOW.md` files, but the matrix skill supplied no route to them.

| Scenario | Required GREEN behavior |
|---|---|
| Known AI papers need a matrix, novelty-risk check, and overclaim critique; no manuscript requested | Keep this skill as orchestrator; load `academic-research-suite` and its research/reviewer workflows only for scoped support; return anchored findings to the matrix |
| Matrix cards need language polish only | Keep card-polish in charge, consult current ARS writing-quality guidance as needed, and use only declared modes; preserve evidence and card schema |
| User explicitly requests full manuscript review | Let the installed ARS reviewer mode enforce its current checks; do not present the matrix's three critique perspectives as a full ARS panel |
| Only legacy standalone entries are missing | Resolve through the installed suite; do not reinstall duplicates or claim ARS support is unavailable |
| The suite itself is absent | Use the local standalone workflow and disclose unavailable ARS support |
| Routing changes are deployed | Existing card-depth, original-table, interpretation, stub, and source-status rules remain intact; Python helpers and UI metadata remain unchanged |

Verification: re-run the matrix-plus-critique scenario against the updated skill,
verify selected suite workflow files exist, run the existing four test scripts,
validate frontmatter and references, and compare protected sections with the
pre-update installed skill before deployment.
