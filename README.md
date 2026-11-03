# AI Frontier

An [OpenShelf](https://github.com/OpenNorms/openshelf) v1.7 knowledge base for evidence-backed agentic AI research.

## Organization

- `index.md` — discovery entry point (L1)
- `wiki/briefings/` — dated, immutable briefing snapshots
- `wiki/projects/` — one canonical page per project
- `wiki/techniques/` — reusable agentic patterns
- `wiki/signals/` — emerging patterns and hypotheses
- `wiki/experiments/` — reproducible experiments
- `wiki/evaluations/` — benchmark and evidence assessments
- `raw/` — optional locally preserved source evidence
- `automation/briefing-policy.yaml` — research and curation policy

## Validation

```sh
pip install 'openshelf>=1.7,<2'
openshelf lint .
```

Agent contributions should arrive as pull requests. See `AGENTS.md`.
