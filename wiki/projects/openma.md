---
uid: b6a90507-a8d1-4d13-9a40-000000000027
title: "OpenMA"
summary: "Canonical evidence record for OpenMA; source, mechanism, limitations and experiment from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://github.com/openma-ai/open-managed-agents
---

# OpenMA

**Origin:** [[briefings/2026/11/2026-11-05]] — finding 7. This is a canonical backfill of the archived briefing assessment, not an independent source re-review or benchmark replication.

## Archived evidence and assessment

**Date:** Repository active November 5, 2026; not necessarily launched today. **Source:** [openma-ai/open-managed-agents](https://github.com/openma-ai/open-managed-agents). **Verdict:** High operational relevance; claims need hands-on verification.

**Built/demonstrated:** OpenMA offers an open-source, self-hostable management layer for agent sessions, execution and recovery, with model, harness, sandbox and cloud-provider choices. The stated goal is to separate the lifecycle manager from the agent implementation.

**Agentic mechanism:** A control plane that tracks sessions and recovery while workers run in interchangeable sandboxes. This reduces coupling between orchestration policy and a specific model vendor.

**Why frontier / comparison:** Where Rivet's key abstraction is a durable process per agent, OpenMA emphasizes managed sessions and interchangeable execution substrates. Neither should be assumed to guarantee transactional side effects.

**Practical takeaway:** Compare a managed session against a custom cron-driven agent on restart, cancellation, tool timeout, sandbox cleanup and state restoration. Score the actual postconditions, not whether the process returned 'success'.

**Caveat:** The repository's feature description is not evidence of production-scale reliability, security or cross-provider compatibility. Test before adopting.

## Cross-briefing context

Compare the documented evidence tier and mechanism against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. These are analyst comparisons, not direct citations between projects. Further primary-source verification can deepen this record without changing its identity.
