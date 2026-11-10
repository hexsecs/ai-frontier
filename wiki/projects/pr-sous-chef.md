---
uid: b6a90604-a8d1-4d13-9a40-000000000034
title: "PR Sous Chef"
summary: "Canonical November 6 research finding: PR Sous Chef; documented mechanism, evidence limitations and next steps."
type: workflow
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://github.github.com/gh-aw/blog/2026-11-04-agent-of-the-day/
---

# PR Sous Chef

**Origin:** [[briefings/2026/11/2026-11-06]] — finding 4. This is a canonical backfill of the briefing's sourced assessment, not a new independent review or replication.

## Archived evidence and assessment

**Date:** November 4, 2026. **Source:** [Primary source](https://github.github.com/gh-aw/blog/2026-11-04-agent-of-the-day/). **Category:** Core / observed orchestration.

**What was built or demonstrated:** A five-minute scheduled workflow deterministically prefilters actionable PRs, then gives an agent a compact queue. The agent may dispatch PR Finisher, add limited comments, approve allowlisted runs, or escalate via an expiring issue.

**Agentic technique:** Deterministic prefilter + bounded agent decision + safe-output dispatch to another workflow.

**Evidence and limitations:** Four inspected runs included two successes and two failures; one successful run took 9.9 minutes and an audit estimated 249k tokens, with 72% of turns potentially reducible to deterministic data gathering. Two downstream PR Finisher runs reportedly succeeded.

**Why this matters / comparison:** A real multi-agent operations loop with explicitly bounded delegation and documented failure cases. This goes beyond yesterday's generic managed-agent control planes.

**Practical takeaway:** Build a queue prefilter for stale GitHub issues/PRs, then delegate only the ambiguous cases to a model. Use idempotent dispatch keys and a human escalation path; measure queue age and duplicate dispatches.

**Verdict:** High implementation relevance; reliability and cost remain significant concerns.

## Cross-briefing context

For independent acceptance, regression preservation, and source limits, see [[concepts/verified-completion-vs-apparent-success]], [[concepts/preservation-aware-agent-improvement]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. These are analytical comparisons, not direct project dependencies.
