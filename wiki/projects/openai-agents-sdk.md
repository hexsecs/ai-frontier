---
uid: b782aa6f-f16d-445d-a7e2-690f61b4c321
title: "OpenAI Agents SDK alpha 0.24.0"
summary: "An alpha SDK release adds durable root sessions and stricter executor write policies."
type: project
created: 2026-11-21
updated: 2026-11-21
depth: full
sources:
  - https://github.com/openai/openai-agents-python/releases/tag/v0.24.0-alpha.7
---

# OpenAI Agents SDK alpha 0.24.0

**Primary source:** https://github.com/openai/openai-agents-python/releases/tag/v0.24.0-alpha.7. **Evidence:** inspected maintainer release/README; no independent reproduction.

## Implementation
The November 8, 2026 **pre-release** introduces root Sessions backed by caller-owned CustomStorage, alongside native execution and the retained classic runtime. The release instructs users to reconcile uncertain tool effects before resuming. Newly created Environments default to strict write policy, requiring a compatible executor; migration to legacy behavior is explicit. The SDK README documents sandbox agents that inspect files, run commands and apply patches.

## Mechanism and bounds
Session persistence concerns conversation/execution records; it is not proof of exactly-once effects. A strict write policy constrains filesystem destinations, not every network side effect. [[concepts/replay-idempotency-and-effect-semantics]] explains uncertain writes, [[concepts/agent-state-and-lifecycle]] separates session and workspace state, and [[techniques/durable-agent-execution]] compares recovery contracts. This is a vendor-maintained alpha release, not an independent reliability measurement.

## Proposed experiment
Run 20 disposable file-edit tasks with a mocked remote mutation, interrupt immediately before and after remote commit, restart from CustomStorage, and separately count duplicate effects, missing effects, unresolved outcomes and writes outside allowed roots. Compare strict versus legacy policy only in isolated test environments.
