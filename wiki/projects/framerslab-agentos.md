---
uid: 019a5b21-21b2-7c91-8a42-18d90b5e11f6
title: "Framerslab AgentOS 0.18–0.19"
summary: "Agent memory deletion uses a forgotten-user ledger and tombstone copies designed to preserve deletion across store restoration."
type: project
created: 2026-11-16
updated: 2026-11-16
depth: brief
sources:
  - https://github.com/framerslab/agentos/releases/tag/v0.18.0
---

# Framerslab AgentOS 0.18–0.19

**Source and date:** https://github.com/framerslab/agentos/releases/tag/v0.18.0 (2026-11-14–15).

AgentOS 0.18 adds a forgotten-user ledger, tombstones persisted outside the main memory store, deletion of associated traces/chunks, SQLite secure_delete and retention choices for shared stores. Version 0.19 makes persistence, prompt profiles and date tools explicit host configuration rather than implicit runtime defaults.

**Mechanism:** Durable negative memory: enforce deletion/retention across restored databases and derived retrieval indexes, while making host authority explicit.

**Evidence and limits:** Many agent-memory projects optimize recall but under-specify deletion, provenance and consent. This release treats forgetting as a durable state transition that must survive backup restore. That is an engineering mechanism, not a measured privacy guarantee. Substantive implementation of memory governance; no independent reliability study. Release documentation does not independently establish measured reliability.

**Evaluation:** Create synthetic user memories, delete one subject, restore an older SQLite snapshot and attempt dense, exact and recency retrieval. Assert zero recovered content, inspect tombstone state and verify unrelated subjects remain accessible.

## Conceptual context

Compare memory operations, admission and reuse while retaining null and negative-transfer evidence. See [[techniques/agent-skills-and-memory]]. Distinguish assignment and connector identity from enforced action scope, inheritance ceilings and revocation. See [[concepts/delegated-authority-and-revocation]].
