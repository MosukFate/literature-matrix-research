# Beginner Guide Layer

Use this reference for `beginner-expansion` work. The target reader understands basic AI terms such as attention, token, loss, benchmark, steering, and retrieval, but does not know the specific paper.

## Placement

For the current AI paper deep-read schema, the beginner-readable layer is folded into:

```markdown
## 0. 总览摘要
## 2. 核心思想与逻辑链
```

Keep existing frontmatter, `one_sentence_summary`, source_status, and the required 0-10 deep-read body. Do not recreate the old beginner-guide heading as a duplicate.

## Required Labels

The beginner-readable material must still answer these seven questions, but it can express them as prose inside `## 0` and `## 2` instead of as mandatory labels:

- `背景问题`: the concrete pain point or failure mode.
- `为什么要做`: why existing models, benchmarks, or methods are insufficient.
- `怎么做`: workflow-level method explanation, not only method names.
- `方法独特点`: how this paper differs from adjacent work.
- `为什么这个方法有优势`: whether the advantage comes from data, structure, objective, intervention point, evaluation protocol, or system design.
- `数学/机制/评价原理`: readable explanation of objective, loss, probe, steering, metric, causal comparison, or data flow.
- `读这篇别误会`: what not to overgeneralize.

## Length Guidance

- P0/P1 cards: about 1200-1800 Chinese characters.
- P2 cards: about 900-1400 Chinese characters.
- Short LLM extension cards should be expanded to P1-style depth when they are part of the mainline.

## Math and Mechanism Rules

Add formulas only when the paper's core method or metric requires them:

- Loss or objective.
- Probability/logit ratio.
- Steering vector.
- Retrieval trigger.
- Attention/head contribution.
- JEPA latent prediction objective.
- Benchmark scoring metric.

Every formula must explain each symbol in plain Chinese. If the formula is a pedagogical formalization rather than a paper formula, say so explicitly.

## Paper-Type Guidance

| Paper type | Explain |
|---|---|
| Benchmark/evaluation | data construction, scoring, failure type, why metric measures the target |
| Architecture/model | module roles, token/latent flow, visual/text pathway, training stages |
| Mechanism/intervention | probe, knockout, patching, steering, causal comparison, controls |
| JEPA/representation | prediction objective, latent target, masking/conditioning, collapse prevention |
| LLM extension | pretraining objective, alignment objective, context/retrieval/preference mechanism |

## Evidence Rules

- Do not add unverified numbers.
- Model names, benchmark names, table conclusions, and numeric results must trace to source_status, ledger, PDF, official page, or a card evidence anchor.
- If local evidence is insufficient, write "论文声称", "结果提示", or "正式引用前需回原文", not a strong conclusion.
- Do not use web summaries as evidence for new technical conclusions.

## Misreading Guards

Include boundaries such as:

- Benchmark improvement is not mechanism proof.
- Attention visualization is not causal evidence unless paired with intervention.
- arXiv or workshop status should not be cited as top-conference authority.
- A method shown on one model family may not be universal.
- A training-free decoding trick may reduce one hallucination type while hurting general ability.
