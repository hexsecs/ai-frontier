---
uid: b6a90404-a8d1-4d13-9a40-000000000014
title: "Claude Agent ACP"
summary: "Canonical evidence record for Claude Agent ACP; mechanism, limitations, practical implications and source provenance from the November 4 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
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

## Knowledge-base synthesis

This entry preserves the finding as a reusable canonical reference rather than leaving it accessible only by briefing date. Compare its stated mechanism and evidence tier against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]], and the [November 3–9 cross-briefing synthesis](../evaluations/briefing-synthesis-2026-11-03-to-09.md). These are analyst-level thematic connections, not assertions that the original project cites or implements the linked concepts. Future source verification should replace this backfill with a deeper independently checked treatment while retaining this page identity.
