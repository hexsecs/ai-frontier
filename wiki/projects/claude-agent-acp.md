---
uid: b6a90404-a8d1-4d13-9a40-000000000014
title: "Claude Agent ACP"
summary: "Canonical evidence record for Claude Agent ACP; mechanism, limitations, practical implications and source provenance from the November 4 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://github.com/agentclientprotocol/claude-agent-acp/pull/1516
---

# Claude Agent ACP

**Origin:** [[briefings/2026/11/2026-11-04]] — finding 4. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** November 2, 2026 release PR. **Primary source:** [agentclientprotocol/claude-agent-acp PR #1516](https://github.com/agentclientprotocol/claude-agent-acp/pull/1516). **Verdict:** Incremental implementation, strategically useful interoperability signal.

**What was proposed.** The ACP adapter's release activity includes exposing explicit subagent role metadata. Rather than treating every agent message as an undifferentiated stream, clients can present or process information about which delegated role produced it.

**Key technique:** Typed role provenance across the agent-to-client boundary. This can support audit logs, UI grouping, and specialized handling of delegated work.

**Why interesting:** For multi-agent systems, attribution is a prerequisite for assessing individual contributions and failures. Compared with Agensh's decentralized work claiming, this is a smaller protocol-interface feature; it does not itself solve task scheduling or conflict resolution.

**Practical takeaway:** Add `agent_id`, `role`, `parent_task`, `artifact_id`, and `verification_status` to every agent result. Keep role metadata descriptive, not an authorization source.

**Limitations:** No evidence here of cross-client compatibility or measured improvement. The release PR is not proof of a stable deployment.

## Mechanism and system boundary

The primary reusable mechanism is **Agent Client Protocol interoperability and session exchange**. Treat the agent model, orchestration state, tool authority, persistent artifacts and independent checker as separate components. The archived evidence above establishes what the authors or maintainers reported; it does not establish cross-domain transfer or a successful local deployment.

## Evidence interpretation and counterevidence

**Key failure mode:** Protocol compatibility does not imply preservation of decision provenance or secure authorization. The evidence tier is limited to the dated source assessment above. Do not interpret a repository release, simulated benchmark, user survey or PR proposal as independently reproduced production reliability. A null or missing validator result is an unknown, not a pass.

## Comparative synthesis and relationships

Relevant canonical context: [[projects/tracybot]]; [[concepts/scoped-assurance]]. These are analyst-selected **compares_with** or thematic relationships; none implies that the linked projects directly depend on one another. Cross-cutting questions include what state is persisted, what is observable, which actors have authority, and what independently proves the requested outcome. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible validation protocol

**Proposed, not executed:** Exchange 20 sessions between clients; audit tool permissions, resumability, task identity and action attribution. Freeze the model/runtime version, dataset and prompts; preserve raw traces, tool receipts, source excerpts, checker outputs and failed attempts. Report numerator/denominator, uncertainty and cost, with a baseline and a held-out transfer set. Never promote a performance claim without the actual independent acceptance record.

## Operational adoption and open questions

Adopt as an isolated prototype before production use. Require explicit ownership of side effects, auditability and rollback. Open questions: does the result survive a new task distribution; does a simpler baseline achieve similar quality; can failure be detected without consulting the producing agent; and what happens when an external write's outcome is unknown?

## Provenance and depth assessment

**Depth: full analytical synthesis of the archived briefing, not independently replicated research.** This page preserves original author-reported numbers and source URLs; the new threat model, comparisons and experiment are editorial analysis. Deeper source inspection and reproduction are separate future work.
