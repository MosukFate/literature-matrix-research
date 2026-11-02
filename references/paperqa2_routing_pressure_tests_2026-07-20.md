# PaperQA2 Routing Pressure Tests — 2026-07-20

## Baseline Failure

The prior workflow called discovery “PaperQA2-inspired” but had no executable PaperQA2 route. An agent could propose integration yet could not name a pinned runtime, stable handoff artifacts, evidence state, or fallback.

## Required Routing

- Ordinary paper discovery remains `paper-lookup` plus `discover_candidates.py`.
- Cross-PDF QA, citation spot checks, and contradiction candidates load `paperqa2-audit` only after source screening.
- PaperQA2 remains optional; its absence never blocks matrix, card, or PDF audit work.
- Outputs return to `audit-only` as candidate evidence and a manual PDF verification queue.
- PaperQA2 never promotes `source_status`, verifies numeric claims by itself, or directly rewrites a formal paper card.

## Regression Check

```powershell
rg -n "paperqa2-audit|cross-PDF|candidate evidence|must not promote|optional" SKILL.md references/skill_integration.md
```
