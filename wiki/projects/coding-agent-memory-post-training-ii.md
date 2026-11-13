---
uid: 0f51e12c-1f8d-4e64-93a8-c8202799fe4b
title: "Coding Agent Memory Post-Training II (CAMP-II)"
summary: "CAMG-II spans Shop, Coding, AutoResearch, General and Visual long-horizon environments, giving agents ordinary Bash and persistent workspaces. CA"
type: project
created: 2026-11-13
updated: 2026-11-13
depth: brief
related: [agent-skills-and-memory]
sources:
  - https://arxiv.org/abs/2611.14009
---

# Coding Agent Memory Post-Training II (CAMP-II)

**Source:** https://arxiv.org/abs/2611.14009. **Publication:** 2026-11-10; revised 2026-11-12. **Evidence status:** author-reported, no independent replication.

## Mechanism
CAMG-II spans Shop, Coding, AutoResearch, General and Visual long-horizon environments, giving agents ordinary Bash and persistent workspaces. CAMP-II uses asynchronous on-policy distillation from a frozen teacher to learn when to write, revise, search and reuse files across context replacements.

**Technique:** Train memory operations through familiar filesystem tools, rather than introducing an unfamiliar memory API.

## Evidence and limits
Authors report 2.97× the gain of the strongest on-policy-distillation baseline on CAMG-II, with improvements on Terminal-Bench 2.1 and SWE-Bench Pro V2. This is an author-reported relative gain, not 2.97× task success.

Training apparatus and gains are not independently replicated here; no production deployment established.

## Comparison and relation
Substantive new training approach to file-based long-horizon memory. Contrasts with JAM's query-time retrieval and materials-memory's reusable guards: CAMP-II changes the policy's learned file-operation behavior.

Related: [[techniques/agent-skills-and-memory]]. The comparison is analytical, not a demonstrated integration.

## Proposed experiment
On 20 interrupted coding tasks, compare raw transcript compaction, file-based memory with explicit prompts, and learned/file-operation policies. Measure task success, memory read/write count, context resets, token cost, and negative transfer.

## Provenance
[[briefings/2026/11/2026-11-13]] — full dated narrative and source-scoped relation audit.
