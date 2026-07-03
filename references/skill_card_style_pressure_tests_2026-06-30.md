# Paper-Original Card Rewrite Pressure Tests - 2026-06-30

## Scope

This file records the RED/GREEN checks for the approved GASP-style card rewrite pattern. It extends the earlier skill merge pressure tests.

Subagent pressure testing was not used in this Codex run because the available multi-agent tool forbids spawning subagents unless the user explicitly asks for delegation. The RED phase is grounded in an observed real card failure: the GASP card before correction.

## RED: Observed Failure Before Skill Edit

| Scenario | Expected behavior | Observed failure |
|---|---|---|
| User asks for method detail | Explain what the paper does, why it does it, and what effect it reports | The card said "读方法时要区分..." and gave a generic data-flow reading instruction instead of paper-specific synthesis |
| Paper identity conflicts with card | Verify title/task/method against source and repair matrix metadata | GASP was described as gaze/attention subspace probing, while the arXiv paper is geometric-aware spatial priors injected into VLMs |
| Extracted table is malformed | Reconstruct the relevant original table from PDF/source text and label the correction status | The card pasted a broken pdfplumber table with missing headers and row groups |
| User asks for examples | Embed examples inside method/evidence/limitation where they explain the mechanism | Examples risk becoming a decorative final section or generic analogy |

## GREEN: Required Passing Behavior

| Scenario | Passing rule now encoded |
|---|---|
| Method rewrite | `## 2` must answer `怎么做 / How`, `为什么这么做 / Why`, and `这么做的效果是什么 / Effect` with source-grounded workflow/module details |
| Identity verification | Title, method family, and matrix role must be checked against source before prose polishing |
| Table extraction | Broken MarkItDown/pdfplumber output must be corrected from source text/PDF when possible; every table gets immediate `结果解析` |
| Examples | Analogies/examples must be embedded directly in method, evidence, limitation, or project relation |

## Verification Commands

```powershell
rg -n "读方法时|读实验时|attention/gaze|Gaze Attention|Attention Subspace" path\to\package -g "*.md" -g "!90_Audit_and_Sources/converted_markdown/**" -g "!90_Audit_and_Sources/table_extracts/**"
rg -n "结果解析 / Result interpretation" path\to\package -g "*.md"
```

Expected:

- No active card uses generic reader-instruction language as a substitute for paper-specific method synthesis.
- No card keeps a known-wrong paper identity after source verification.
- Every relevant result table is followed by result interpretation.