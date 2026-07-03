# Paper Lookup Playbook

Use this reference for paper discovery and metadata verification.

## Source Priority

Prefer official sources:

1. Conference/proceedings page: ICLR/OpenReview, NeurIPS, ICML/PMLR, CVF, ACL Anthology, AAAI, EMNLP/NAACL/COLM.
2. Official PDF from the venue page.
3. arXiv PDF and abstract page.
4. Author project page, GitHub, Hugging Face, Papers With Code.
5. Semantic Scholar, OpenAlex, Crossref, DOI, Google Scholar, publisher metadata.

Web summaries are search leads, not final evidence.

## Identifier Rules

Record all available identifiers:

- DOI: `10.xxxx/...`
- arXiv: `YYMM.NNNNN`
- OpenReview ID.
- ACL Anthology ID.
- CVF URL slug.
- PMLR volume/page URL.
- Semantic Scholar Corpus ID or paper ID.
- GitHub/HF/Papers With Code URL.

When two sources disagree, trust the official venue page for publication status and use the PDF for content claims.

## Search Families

For AI/ML research, run multiple query families:

- Seed title exact phrase.
- Core method terms.
- Failure mode terms.
- Dataset/benchmark names.
- Model family names.
- Mechanism terms: causal tracing, attention head, activation patching, SAE, steering, probing, representation editing.
- Intervention terms: contrastive decoding, DPO, RLHF, preference optimization, training-free, test-time.
- Venue/year filters.
- Closest-known work titles and citations.

Record failed searches too; they explain why coverage may be incomplete.

## Database Selection

| Need | Search where |
|---|---|
| CS/AI preprints | arXiv, Semantic Scholar, OpenAlex |
| Official ML venues | OpenReview, NeurIPS, ICML/PMLR, ICLR, CVF |
| NLP papers | ACL Anthology, OpenReview, arXiv |
| DOI/publisher metadata | Crossref, DOI resolver, publisher page |
| Citation graph | Semantic Scholar, OpenAlex |
| Code/artifact | GitHub, Hugging Face, Papers With Code |
| Broad discovery | web search with academic domains |

## Candidate Table

Maintain this table while searching:

| ID | Title | Year | Venue/source | DOI/arXiv/OpenReview | Official URL | PDF URL | Code/data | Why relevant | Initial layer |
|---|---|---:|---|---|---|---|---|---|---|

## Deduplication

Merge records when any of these match:

- DOI.
- arXiv ID.
- OpenReview ID.
- Exact normalized title.
- Same official venue page.

If titles differ slightly between arXiv and proceedings, keep proceedings title as canonical and record arXiv title as alias.

## Inclusion and Exclusion

Include papers that directly support:

- Problem definition.
- Benchmarks.
- Mechanism explanation.
- Intervention/baseline.
- Model architecture/infrastructure.
- Closest prior work or novelty risk.

Exclude or defer:

- Low-relevance papers with only keyword overlap.
- Papers with no accessible source and no reliable metadata.
- Blog-only claims without paper or artifact.
- Duplicated preprint when proceedings version is already included.

## Trust Layer Assignment

- `mainline`: top-conference main paper, CORE A/A*, or user-approved trusted venue.
- `supplemental`: arXiv, Findings, workshop, technical report, project page, artifact, or high-risk similar work without trusted venue.
- `matrix-only`: relevant but not deep-reviewed yet.
- `excluded`: not relevant enough or too weakly sourced.

Do not discard high-relevance arXiv work if it creates novelty risk; put it in supplemental.
