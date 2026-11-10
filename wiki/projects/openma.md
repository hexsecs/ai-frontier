---
uid: b6a90507-a8d1-4d13-9a40-000000000027
title: "OpenMA"
summary: "Canonical evidence record for OpenMA; source, mechanism, limitations and experiment from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
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

## Mechanism and boundary

The reusable mechanism is **Multi-agent system design and reusable orchestration**. Distinguish model reasoning, tool execution, persistent state, side effects, and the independently observed acceptance condition. The historical source summary above is the factual evidence base; the interpretation below is an analyst synthesis.

## Critical evidence assessment

**Failure mode / counterweight:** Claims of generality require matched-task comparisons; routing overhead may erase gains. The cited sources have not been independently reproduced in this mining pass. Report source-reported metrics as such, and do not equate a successful demo, publication, repository release or PR proposal with production readiness. Negative and missing results matter as much as successes.

## Directional relationships and comparative interpretation

Related evidence: [[techniques/multi-agent-orchestration]]; [[projects/agensh]]. These are analyst-level **compares_with** links, not verified direct dependencies. Compare this mechanism against the simpler baseline, distinguish quality from throughput, and preserve task-level losses rather than averaging them away. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible evaluation

**Proposed, not executed:** Compare centralized, decentralized and role-specialized teams under identical task and budget constraints. Hold model, prompts, inputs and budget constant; log task-level results, full tool receipts, source spans, failed attempts, checker execution, elapsed time and tokens. Evaluate unseen cases and require explicit evidence before promoting changes to a trusted workflow.

## Deployment considerations and open questions

Sandbox the initial integration. Specify the authority boundary, persistence model, rollback path and owner of independent acceptance. Open questions include transfer to unseen tasks, sensitivity to the evaluator, total operational cost and whether the same improvement survives adversarial failure injection.

## Provenance and depth

**Full analytical treatment based on the dated primary-source briefing; not an independent replication.** Historical claims are preserved above; comparisons, risks and tests in this section are proposed analyses.
