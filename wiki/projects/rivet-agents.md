---
uid: b6a90505-a8d1-4d13-9a40-000000000025
title: "Rivet Agents"
summary: "Canonical evidence record for Rivet Agents; source, mechanism, limitations and experiment from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://github.com/rivet-dev/agents
---

# Rivet Agents

**Origin:** [[briefings/2026/11/2026-11-05]] — finding 5. This is a canonical backfill of the archived briefing assessment, not an independent source re-review or benchmark replication.

## Archived evidence and assessment

**Date:** Repository active November 5, 2026 (not necessarily first released today). **Source:** [rivet-dev/agents](https://github.com/rivet-dev/agents). **Verdict:** High practical relevance; implementation exists, production claims unverified.

**Built/demonstrated:** An open-source TypeScript agent infrastructure project organized around a durable process for each agent, with state and memory intended to survive restarts. Its repository advertises sandbox integrations and coding-agent use cases.

**Agentic mechanism:** Model each long-running agent as a persistent actor/process rather than a one-shot prompt. The runtime owns lifecycle, resumability and isolation boundaries.

**Why frontier / comparison:** Complements November 3's AgentOS recovery concepts and November 4's uncertain-write analysis, but shifts the abstraction from an execution loop to a per-agent durable process. The key distinction to evaluate is whether state survives process failure *without* duplicating external effects.

**Practical takeaway:** Prototype a persistent research worker that stores its queue cursor, last verified artifact and tool-operation IDs. Kill it mid-task; restart and check that it resumes without replaying completed writes.

**Caveat:** The README's durability claim alone does not prove exactly-once execution or safe retries. Those properties require an application-level reconciliation test.

## Cross-briefing context

Compare the documented evidence tier and mechanism against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. These are analyst comparisons, not direct citations between projects. Further primary-source verification can deepen this record without changing its identity.
