# AI Frontier

**[Browse the AI Frontier knowledge base on GitHub Pages](https://hexsecs.github.io/ai-frontier/)**

An [OpenShelf](https://github.com/OpenNorms/openshelf) v1.7 knowledge base for evidence-backed agentic AI research.

## Organization

- `index.md` — discovery entry point (L1)
- `wiki/topics/` — question-led reading paths using the existing index type
- `wiki/briefings/` — dated, immutable briefing snapshots
- `wiki/projects/` — one canonical page per project
- `wiki/techniques/` — reusable agentic patterns
- `wiki/concepts/` — bounded cross-project claims and counterevidence
- `wiki/benchmarks/`, `wiki/workflows/`, `wiki/case-studies/` — indexes by entity type; canonical records retain their URLs
- `wiki/domains/` — application-area navigation
- `wiki/signals/` — emerging patterns and hypotheses
- `wiki/experiments/` — reproducible experiments
- `wiki/evaluations/` — benchmark and evidence assessments
- `raw/` — optional locally preserved source evidence
- `automation/briefing-policy.yaml` — research and curation policy

## Validation

```sh
pip install 'openshelf>=1.7,<2'
openshelf lint .
python scripts/check_frontmatter.py
python scripts/check_article_prose.py
python scripts/check_briefing_mining.py
python scripts/check_links.py
```

For the site build, navigation tests and optional editorial report, see [`docs/README.md`](docs/README.md).

Agent contributions should arrive as pull requests. See `AGENTS.md`.
