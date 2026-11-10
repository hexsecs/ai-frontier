---
uid: b6a90602-a8d1-4d13-9a40-000000000032
title: "Matt Pocock Skills Reviewer"
summary: "Canonical November 6 research finding: Matt Pocock Skills Reviewer; documented mechanism, evidence limitations and next steps."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://github.github.com/gh-aw/blog/2026-11-06-agent-of-the-day/
---

# Matt Pocock Skills Reviewer

**Origin:** [[briefings/2026/11/2026-11-06]] — finding 2. This is a canonical backfill of the briefing's sourced assessment, not a new independent review or replication.

## Archived evidence and assessment

**Date:** November 6, 2026. **Source:** [Primary source](https://github.github.com/gh-aw/blog/2026-11-06-agent-of-the-day/). **Category:** Core / observed workflow.

**What was built or demonstrated:** A GitHub Agentic Workflows PR reviewer imports a shared review base, selects engineering skills based on change type, uses economy-oriented model routing, and leaves a signed review linked to its run.

**Agentic technique:** Task-adaptive reviewer specialization with narrow, auditable write permissions and traceable review authorship.

**Evidence and limitations:** GitHub's published audit cites three successful PR-triggered runs lasting 13.1, 11.4, and 18.1 minutes, with 58,142, 51,209, and 103,570 log-summary tokens. One inspected run produced one inline comment and one review. The audit flagged high token use and a declared subagent not observed in requests.

**Why this matters / comparison:** A real, instrumented PR-review pipeline; the skill selection itself is incremental, but the run-level evidence makes it actionable.

**Practical takeaway:** Try a specialized reviewer on OpenShelf PRs that checks provenance, OpenShelf metadata, link validity, and unsupported depth promotions. Cap review comments and measure actionable findings per 10k tokens.

**Verdict:** Practical, observable; cost effectiveness remains unproven.

## Cross-briefing context

For independent acceptance, regression preservation, and source limits, see [[concepts/verified-completion-vs-apparent-success]], [[concepts/preservation-aware-agent-improvement]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. These are analytical comparisons, not direct project dependencies.
