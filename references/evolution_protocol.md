# Evolution Protocol

Use this reference whenever the user adds a new preference, corrects the workflow, or asks to make the literature-matrix skill easier to reuse later.

## Core Principle

Evolve additively. New rules should be layered as pressure-tested extensions unless the user explicitly says an older rule is superseded. Do not silently rewrite approved behavior.

## Protected Rules

These rules are protected because they came from explicit user corrections and successful verification:

- GASP-style method rewrite: each card's method section answers `怎么做 / How`, `为什么这么做 / Why`, and `这么做的效果是什么 / Effect`.
- Cards must summarize and analyze the paper as already-read synthesis, not tell the reader how to read the paper.
- Examples and analogies are embedded inside method, evidence, limitation, or project-relation sections.
- Original result tables should be pasted or manually corrected when extractable, then followed immediately by `结果解析 / Result interpretation`.
- Compact fallback tables are allowed only when original extraction fails and must be labeled as fallback.
- Source status, numeric claims, benchmark rankings, and mechanism claims stay conservative until verified.
- The only active literature-matrix skill entry on this machine is `literature-matrix-research`; do not recreate an overlapping duplicate skill entry.
- `type: paper-card` is a GASP-depth contract. Source-level planning notes must be `paper-stub` or `matrix-stub`, and validators must reject shallow formal paper cards.
- Formal `paper-card` notes use the AI paper deep-read 0-10 schema, not the old six-section body.
- Formal `paper-card` notes require a source-backed `小白细节自检 / Novice detail check`; if the card is still too shallow after one repair pass, demote it to a stub instead of padding.

## Additive Update Workflow

1. Capture the new user rule in plain language.
2. Identify whether it changes card content, source evidence, Obsidian structure, skill routing, validation, or sync behavior.
3. Add or update a pressure-test file under `references/` describing the old failure and the expected new behavior.
4. Patch the smallest relevant reference file. Update `SKILL.md` only for routing or top-level gate changes.
5. Preserve protected blocks unless the user explicitly asks to replace them.
6. Run validation: frontmatter/YAML parse, grep for banned patterns, protected-rule check, and any package-specific validators.
7. Record what changed and what remains unresolved in the package's compressed context or audit file when a package is being edited.

## Regression Checks

Use these checks after future edits:

```powershell
rg -n "## 11\. 示例|compact reconstructions|compact table-backed" <skill-root>
rg -n "读方法时|读实验时" <skill-root>\SKILL.md <skill-root>\references
rg -n "paper-stub|paper_card_too_short|method_section_too_short|missing_result_table|formula|baseline|reproduction" <skill-root>
Confirm the removed duplicate skill path is absent from the active namespace.
```

Expected interpretation:

- Hits inside pressure-test files or explicit anti-pattern sections are acceptable.
- Active instructions must not require separate examples sections, compact-table replacement, or reader-instruction prose.
- Active instructions must preserve the formal paper-card vs stub distinction and the deep-card validator gates.
- The removed duplicate skill path should remain absent from the active namespace.

## When to Split a Reference

Create a new reference file when an added rule exceeds roughly one screen, affects a distinct phase, or needs its own pressure tests. Otherwise add a short subsection to the closest existing reference.

Do not split protected rules just to make the file look tidy. Stability beats aesthetic refactoring.
