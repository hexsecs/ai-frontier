---
uid: b6a90304-a8d1-4d13-9a40-000000000004
title: "AgentSWE"
summary: "Canonical evidence record for AgentSWE; mechanism, limitations, practical implications and source provenance from the November 3 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
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

## Knowledge-base synthesis

This entry preserves the finding as a reusable canonical reference rather than leaving it accessible only by briefing date. Compare its stated mechanism and evidence tier against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]], and the [November 3–9 cross-briefing synthesis](../evaluations/briefing-synthesis-2026-11-03-to-09.md). These are analyst-level thematic connections, not assertions that the original project cites or implements the linked concepts. Future source verification should replace this backfill with a deeper independently checked treatment while retaining this page identity.
