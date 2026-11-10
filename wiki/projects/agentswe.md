---
uid: b6a90304-a8d1-4d13-9a40-000000000004
title: "AgentSWE"
summary: "Canonical evidence record for AgentSWE; mechanism, limitations, practical implications and source provenance from the November 3 briefing."
type: benchmark
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2610.13361
---

# AgentSWE

**Origin:** [[briefings/2026/11/2026-11-03]] — finding 4. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** October 9, 2026 (older paper newly selected for its direct relevance). **Source:** [AgentSWE paper](https://arxiv.org/abs/2610.13361). **Assessment:** High evaluation relevance; not a newly released system this week.

**What was built.** A 25-task benchmark covering the creation, editing, and optimization of agent software. Each task gives the builder a natural-language commission and a few illustrative examples, then evaluates the frozen submission on held-out cases against requirement-derived rubrics and hard acceptance gates.

**Key technique.** Separate the examples the builder can see from the full behavior the user commissioned. The benchmark exposes overfitting to demonstrations, plausible-looking but hollow runtimes, and unsupported claims of completion.

**Why frontier.** Agentic software development is moving from generating ordinary code to generating autonomous systems. The failure mode changes: an agent can build a polished interface while omitting the actual persistent loop, safety boundaries, or integration behavior.

**Practical takeaway / experiment.** For every new agent skill, write a hidden acceptance suite that tests actual side effects, restart behavior, denied permissions, and task completion. Require a machine-verifiable trace before declaring an implementation complete. This is a natural acceptance gate for autonomous agents maintaining the AI Frontier repository itself.

**Verdict:** High-value benchmark design. Its small task count limits universal claims, but the evaluation structure is directly reusable. It complements [[projects/seq-k]] by measuring commissioned behavioral fidelity rather than only iterative improvement.

## Mechanism and system boundary

The primary reusable mechanism is **Evaluation of agents that construct other agents**. Treat the agent model, orchestration state, tool authority, persistent artifacts and independent checker as separate components. The archived evidence above establishes what the authors or maintainers reported; it does not establish cross-domain transfer or a successful local deployment.

## Evidence interpretation and counterevidence

**Key failure mode:** A generated agent can pass a local build while failing hidden tasks or permission boundaries. The evidence tier is limited to the dated source assessment above. Do not interpret a repository release, simulated benchmark, user survey or PR proposal as independently reproduced production reliability. A null or missing validator result is an unknown, not a pass.

## Comparative synthesis and relationships

Relevant canonical context: [[concepts/verified-completion-vs-apparent-success]]; [[benchmarks/index]]. These are analyst-selected **compares_with** or thematic relationships; none implies that the linked projects directly depend on one another. Cross-cutting questions include what state is persisted, what is observable, which actors have authority, and what independently proves the requested outcome. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible validation protocol

**Proposed, not executed:** Build 20 small agents with withheld behavioral tests; compare self-reported completion with independent pass and tool-policy compliance. Freeze the model/runtime version, dataset and prompts; preserve raw traces, tool receipts, source excerpts, checker outputs and failed attempts. Report numerator/denominator, uncertainty and cost, with a baseline and a held-out transfer set. Never promote a performance claim without the actual independent acceptance record.

## Operational adoption and open questions

Adopt as an isolated prototype before production use. Require explicit ownership of side effects, auditability and rollback. Open questions: does the result survive a new task distribution; does a simpler baseline achieve similar quality; can failure be detected without consulting the producing agent; and what happens when an external write's outcome is unknown?

## Provenance and depth assessment

**Depth: full analytical synthesis of the archived briefing, not independently replicated research.** This page preserves original author-reported numbers and source URLs; the new threat model, comparisons and experiment are editorial analysis. Deeper source inspection and reproduction are separate future work.
