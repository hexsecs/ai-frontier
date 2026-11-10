---
uid: b6a90506-a8d1-4d13-9a40-000000000026
title: "tigerless agent-memory"
summary: "Canonical evidence record for tigerless agent-memory; source, mechanism, limitations and experiment from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://github.com/tigerless-labs/agent-memory
---

# tigerless agent-memory

**Origin:** [[briefings/2026/11/2026-11-05]] — finding 6. This is a canonical backfill of the archived briefing assessment, not an independent source re-review or benchmark replication.

## Archived evidence and assessment

**Date:** Repository active November 3–5, 2026; original launch date not verified. **Source:** [tigerless-labs/agent-memory](https://github.com/tigerless-labs/agent-memory). **Verdict:** Highly relevant to personal agent stacks; concrete architecture, effectiveness unbenchmarked here.

**Built/demonstrated:** A local-first memory runtime using plain Markdown as its source of truth, ranked retrieval, and a separate sleep-time Manage layer. Its project description says Claude Code and Codex can share the same memory store without an API key.

**Agentic mechanism:** Separate online memory retrieval from offline memory maintenance. The independent consolidation step can update durable knowledge between agent sessions rather than relying on each active task to summarize itself.

**Why frontier / comparison:** The distinctive pattern is a shared, user-owned, inspectable memory corpus across multiple agent harnesses. It overlaps with existing memory techniques, but the independent management phase offers a concrete experiment in reducing repeated context and stale assumptions.

**Practical takeaway:** Compare no memory, append-only memory and offline-managed memory on 20 repeated repository tasks. Measure relevant-fact recall, stale-memory errors, tokens injected and manual correction rate. Version the Markdown so a bad consolidation can be rolled back.

**Caveat:** Shared memory can also spread incorrect conclusions and secrets across agents. Do not equate local storage with safe isolation; add namespaces, provenance and retention controls.

## Cross-briefing context

Compare the documented evidence tier and mechanism against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. These are analyst comparisons, not direct citations between projects. Further primary-source verification can deepen this record without changing its identity.
