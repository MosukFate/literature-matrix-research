# Matrix and Reading Order

Use this reference when building `matrix` or `obsidian-package` outputs.

## Package Structure

Default Obsidian package layout:

```text
obsidian_reading_order/
  00_START_HERE.md
  00_综述与索引/
  01_<stage>/
  02_<stage>/
  ...
  07_补充证据池_非顶会与非COREA_<N>篇/
  90_附录与历史版本/
  99_审计与来源/
```

Keep per-paper cards as independent Markdown files. Do not merge them into a monolithic review unless the user explicitly asks.

## Core Outputs

- START page: entry point, counts, mainline/supplement split, links to matrices and audits.
- Dashboard: current reading map and practical navigation.
- Stage indexes: reading goal, mainline list, one-sentence explanation after every link, strong cross-paper relations.
- Supplemental index: same quality as mainline list; include full paper title and one-sentence explanation.
- Quicklook table: one row per matrix paper with what it does, benchmark/example, method feature, and evidence note.
- Venue trust split: mainline/top-tier versus supplemental/non-CORE or pending.
- Results/benchmarks matrix: datasets, metrics, models, reported results, and evidence anchors.
- Research map/canvas: readable, research-relevant relations rather than dense all-to-all graphs.
- Audit/source reports: source status and remaining verification queue.

## Paper Layers

Use three layers:

- `mainline`: top-conference/main conference, CORE A/A* or otherwise explicitly trusted by the user's venue policy.
- `supplemental`: arXiv, Findings, workshop, technical report, artifact paper, or high-relevance lower-trust source.
- `matrix-only`: useful for the map but no deep card yet.

Counts must state the difference between total matrix entries, deep cards, mainline cards, supplemental cards, and matrix-only entries.

## Stage Index Requirements

Each stage index should include:

- Reading goal.
- Mainline reading list with full title and one-sentence explanation.
- Supplemental links when relevant.
- `强交叉/相关论文` section directly under reading goal or near the reading list.
- Reason for each strong cross-link: shared failure mode, baseline relation, mechanism relation, benchmark relation, novelty risk, or counterexample.

Good one-sentence explanations say what the paper does and why it is in the round. Avoid venue-only entries like "O01 — arXiv; Seed / L4".

## Research Relation Types

Use explicit relation labels:

- `baseline`: method to compare against.
- `benchmark`: evaluation set or metric source.
- `mechanism bridge`: explains internal pathway or causal variable.
- `novelty risk`: closest similar idea.
- `counterexample`: paper that weakens a proposed claim.
- `infrastructure`: model, toolkit, data, or reproducibility support.
- `extension`: transfers the idea to another modality, model, or task.

## Mainline/Supplement Policy

Do not hide supplemental evidence. START and stage indexes must expose it clearly, but writing should distinguish trust:

- Mainline evidence can carry the central argument.
- Supplemental evidence can motivate hypotheses, baselines, ablations, and risk checks.
- Matrix-only entries should not be cited as if fully reviewed.

## Navigation Checks

- Prefer Markdown links for file paths with directory segments.
- Use wikilinks for same-vault note references when names are stable.
- Every index link should resolve from its own file location.
- Canvas JSON must parse if a `.canvas` file is present.
