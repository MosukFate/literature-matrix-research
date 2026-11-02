# Review and Synthesis Rubric

Use this reference for critical review, cross-paper synthesis, gap finding, and novelty-risk checks.

## Per-Paper Review

For each important paper, check:

- Does the card state the real research question?
- Does it distinguish method, benchmark, and conclusion?
- Are experiments described as evidence, not proof?
- Are contributions paired with limitations?
- Are assumptions, model scope, and evaluation scope visible?
- Does the research relationship say how to use the paper?

## Overclaim Checklist

Flag wording that implies too much:

- Benchmark win -> mechanism proof.
- Correlation -> causality.
- Attention heatmap -> causal pathway.
- One model family -> universal model behavior.
- One dataset -> general robustness.
- arXiv claim -> established venue consensus.
- Smooth prose -> source-grounded evidence.

Use cautious replacements:

- `supports`.
- `suggests`.
- `in this setup`.
- `the authors report`.
- `can serve as a hypothesis`.
- `requires source verification`.

## Cross-Paper Synthesis

Group papers by research function:

- Problem framing.
- Benchmark/evaluation.
- Mechanism evidence.
- Training-time mitigation.
- Decoding/test-time mitigation.
- Architecture/infrastructure.
- Representation/latent analysis.
- Closest similar work.
- Counterexample or limitation.

For each group, write:

- What the group agrees on.
- Where papers conflict.
- Which evidence is strongest.
- Which assumptions remain untested.
- Which paper should be cited first.

## Gap Analysis

A good gap has:

- Observable failure mode.
- Clear mechanism hypothesis.
- Available baselines.
- Available benchmarks or constructible evaluation set.
- Falsifiable success criteria.
- Closest prior work and difference.

Weak gap statements:

- "No one has studied X" without search evidence.
- "We combine A and B" without explaining why the combination answers a new question.
- "Improve performance" without a mechanism or evaluation target.

## Novelty-Risk Levels

| Level | Meaning | Action |
|---|---|---|
| `distinct` | clear new task/mechanism/evidence path | proceed |
| `adjacent` | related but separable | cite and distinguish |
| `high-risk` | same task or method level | add a stronger differentiator |
| `duplicate` | likely same idea | change direction or scope |

## Novelty-Risk Questions

Compare against closest work:

- Same problem?
- Same model family?
- Same benchmark?
- Same intervention level?
- Same causal variable?
- Same formula/objective?
- Same evaluation protocol?
- Same practical claim?

The matrix should include a `novelty risk` column or table for high-overlap work.

## Research Target Template

For each proposed target:

- Phenomenon: what fails and in which setting.
- Mechanism hypothesis: what internal or training factor causes it.
- Method: how to test or intervene.
- Baselines: what to compare against.
- Benchmarks: where to evaluate.
- Success criteria: measurable result and preserved ability.
- Risk: closest prior work and failure mode.

## Reviewer-Style Final Check

Before finalizing a package or proposal, apply three scoped critique perspectives:

- Method reviewer: controls, baselines, reproducibility, metrics.
- Domain reviewer: missing related work, venue trust, evidence scope.
- Devil's advocate: strongest alternative explanation and novelty attack.

Convert their objections into the findings report or proposal risk section. These perspectives are matrix-level critique, not a full ARS review panel or evidence of independent execution. When the user explicitly requests full manuscript review, hand off through `academic-research-suite` and follow the installed reviewer workflow's current mode contracts.
