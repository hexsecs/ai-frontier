---
uid: 7ad46860-43c7-48c7-9a72-6c2e18c9d0f4
title: "Planning with Files"
summary: "Persistent Markdown plans and completion gates support coding-agent recovery after context loss."
type: project
created: 2026-11-21
updated: 2026-11-21
depth: full
sources:
  - https://github.com/OthmanAdi/planning-with-files
---

# Planning with Files

**Primary source:** https://github.com/OthmanAdi/planning-with-files. **Evidence:** inspected maintainer release/README; no independent reproduction.

## Implementation
The repository documents a skill that externalizes findings, progress and plans to Markdown, with hooks that reintroduce planning state across turns and after context clearing or compaction. The repository was active on November 20, 2026; that activity date is **not** a verified initial release date. Its cross-agent compatibility is maintainer-documented, not an independently tested matrix.

## Mechanism and bounds
The agent consults files rather than relying on a transient conversation window. Re-injection is a retrieval policy, not a guarantee that a plan reflects current repository state; a deterministic completion gate is only as sound as its declared conditions. [[concepts/agent-state-and-lifecycle]] separates plan state from external effects; [[techniques/agent-skills-and-memory]] explains retained guidance; [[concepts/verified-completion-vs-apparent-success]] bounds completion claims.

## Proposed experiment
Use 20 repository tasks with known hidden acceptance tests. Clear context halfway through, compare baseline, plan-only and plan-plus-reinjection, and score final tests, stale-plan errors, tokens and recovery time. Keep the same model and task order.
