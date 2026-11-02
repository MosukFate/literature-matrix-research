# Literature Matrix Skill Merge Pressure Tests - 2026-06-30

## Scope

This file records the RED/GREEN checks for merging the overlapping literature-matrix entries and correcting deep card table enrichment behavior.

Subagent pressure testing was not used in this Codex run because the available multi-agent tool forbids spawning subagents unless the user explicitly asks for delegation. Instead, the RED phase is grounded in the observed pre-change skill text and package failures.

## RED: Observed Failures Before Skill Edit

| Scenario | Expected behavior | Observed failure |
|---|---|---|
| User asks for examples and analogies inside method/analysis | Skill should require examples to be integrated into explanatory sections | Both skills required a separate `## 7. 示例、比喻与汇报讲法` |
| User asks for original paper result tables via MarkItDown | Skill should require pasted original result tables plus interpretation | Both skills allowed `compact reconstructions` and compact table-backed conclusions |
| User asks to keep only one literature matrix skill | Only one canonical active skill should remain | Two overlapping active literature-matrix skill entries existed |

## GREEN: Required Passing Behavior

| Scenario | Passing rule now encoded |
|---|---|
| Examples/analogies | Must be embedded in `## 0`, `## 2`, `## 3`, `## 5`, or `## 6`; no separate examples section |
| Result tables | Paste original result tables as Markdown when extractable, then add `结果解析 / Result interpretation` |
| Compact fallback | Allowed only when extraction fails and labeled `fallback summary; verify original table before citation` |
| Skill duplication | one literature-matrix entry is canonical; the overlapping legacy directory is backed up and moved out of the active skill namespace |

## Verification Commands

Run after editing:

```powershell
$skillRoot = (Resolve-Path .).Path
rg -n "## 7\. 示例|compact reconstructions|compact table-backed" "$skillRoot"
Test-Path "$skillRoot"
```

Expected:

- `rg` returns no active instruction requiring separate `## 7` or compact replacement tables.
- `Test-Path` returns `False` for the legacy active skill directory.
