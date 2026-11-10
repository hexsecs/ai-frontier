---
uid: b6a90506-a8d1-4d13-9a40-000000000026
title: "tigerless agent-memory"
summary: "Canonical evidence record for tigerless agent-memory; source, mechanism, limitations and experiment from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
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

## Mechanism and boundary

The reusable mechanism is **Persistent agent memory and retrieval**. Distinguish model reasoning, tool execution, persistent state, side effects, and the independently observed acceptance condition. The historical source summary above is the factual evidence base; the interpretation below is an analyst synthesis.

## Critical evidence assessment

**Failure mode / counterweight:** Summaries may discard critical provenance, amplify outdated information or contaminate later tasks. The cited sources have not been independently reproduced in this mining pass. Report source-reported metrics as such, and do not equate a successful demo, publication, repository release or PR proposal with production readiness. Negative and missing results matter as much as successes.

## Directional relationships and comparative interpretation

Related evidence: [[concepts/preservation-aware-agent-improvement]]; [[projects/envopt]]. These are analyst-level **compares_with** links, not verified direct dependencies. Compare this mechanism against the simpler baseline, distinguish quality from throughput, and preserve task-level losses rather than averaging them away. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible evaluation

**Proposed, not executed:** Compare memory-free, raw-event and compressed memory across 30 held-out tasks; score traceability and regressions. Hold model, prompts, inputs and budget constant; log task-level results, full tool receipts, source spans, failed attempts, checker execution, elapsed time and tokens. Evaluate unseen cases and require explicit evidence before promoting changes to a trusted workflow.

## Deployment considerations and open questions

Sandbox the initial integration. Specify the authority boundary, persistence model, rollback path and owner of independent acceptance. Open questions include transfer to unseen tasks, sensitivity to the evaluator, total operational cost and whether the same improvement survives adversarial failure injection.

## Provenance and depth

**Full analytical treatment based on the dated primary-source briefing; not an independent replication.** Historical claims are preserved above; comparisons, risks and tests in this section are proposed analyses.
