---
uid: b6a90505-a8d1-4d13-9a40-000000000025
title: "Rivet Agents"
summary: "Canonical evidence record for Rivet Agents; source, mechanism, limitations and experiment from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
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

## Mechanism and boundary

The reusable mechanism is **Durable agents and stateful execution infrastructure**. Distinguish model reasoning, tool execution, persistent state, side effects, and the independently observed acceptance condition. The historical source summary above is the factual evidence base; the interpretation below is an analyst synthesis.

## Critical evidence assessment

**Failure mode / counterweight:** Crash recovery and external side effects require read-after-write and idempotency, not just resumed local state. The cited sources have not been independently reproduced in this mining pass. Report source-reported metrics as such, and do not equate a successful demo, publication, repository release or PR proposal with production readiness. Negative and missing results matter as much as successes.

## Directional relationships and comparative interpretation

Related evidence: [[projects/agentos]]; [[projects/builderio-agent-native]]. These are analyst-level **compares_with** links, not verified direct dependencies. Compare this mechanism against the simpler baseline, distinguish quality from throughput, and preserve task-level losses rather than averaging them away. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible evaluation

**Proposed, not executed:** Inject process crashes around writes and external acknowledgements; measure duplicates, missing writes and recovery. Hold model, prompts, inputs and budget constant; log task-level results, full tool receipts, source spans, failed attempts, checker execution, elapsed time and tokens. Evaluate unseen cases and require explicit evidence before promoting changes to a trusted workflow.

## Deployment considerations and open questions

Sandbox the initial integration. Specify the authority boundary, persistence model, rollback path and owner of independent acceptance. Open questions include transfer to unseen tasks, sensitivity to the evaluator, total operational cost and whether the same improvement survives adversarial failure injection.

## Provenance and depth

**Full analytical treatment based on the dated primary-source briefing; not an independent replication.** Historical claims are preserved above; comparisons, risks and tests in this section are proposed analyses.
