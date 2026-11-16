---
uid: 019a5b21-21b1-7c91-8a42-18d90b5e11f6
title: "Agent Client Protocol 1.18"
summary: "Experimental ACP session replay, subagent events and fork configuration; protocol surfaces do not establish runtime recovery guarantees."
type: project
created: 2026-11-16
updated: 2026-11-16
depth: brief
sources:
  - https://github.com/agentclientprotocol/agent-client-protocol/blob/main/CHANGELOG.md
  - https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/4aab69b4e6bcb53965ff5b1141d2f04a62a25c6c/CHANGELOG.md
---

# Agent Client Protocol 1.18

**Source and date:** https://github.com/agentclientprotocol/agent-client-protocol/blob/main/CHANGELOG.md (2026-11-14).

ACP 1.18.0 adds unstable-v2 skill commands and content blocks, subagents without the earlier unstable_subagents feature, a replay_complete session update, prompt suggestions, and initial configuration on forked sessions. These are schema/protocol changes, not evidence that every editor and agent implements them.

**Mechanism:** Explicit session lifecycle and interoperable subagent/skill event surfaces instead of proprietary orchestration state.

**Evidence and limits:** It extends the agent-to-editor interface toward persistent, replayable delegated work. Compared with earlier ACP provenance coverage, the meaningful delta is richer subagent, replay and skill semantics; all cited features are marked unstable. High architectural relevance; mostly experimental protocol evolution. Release documentation does not independently establish measured reliability.

**Evaluation:** Build a minimal ACP v2 adapter between two CLI agents; fork a session, dispatch a subagent, replay a saved event sequence and check whether the client can reconstruct final status without inventing tool results.

## Conceptual context

Separate reconstructed session state, live delegated work and independently observed external effects. See [[concepts/agent-state-and-lifecycle]]. Compare persistence, interrupted work and reconciliation without assuming exactly-once external effects. See [[techniques/durable-agent-execution]].
