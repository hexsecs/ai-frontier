---
uid: c6ebb2a0-7beb-46e6-9025-7571992588d5
title: Replay, idempotency and effect semantics
summary: Distinguish rebuilding history, retrying an operation and repeating its intended effect safely.
type: concept
created: '2026-11-16'
updated: '2026-11-16'
depth: full
sources:
- https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2
- https://raw.githubusercontent.com/rivet-dev/agents/21c248b1d1d8c3a9d6c1cc7b85531a4a2d0e5c50/docs/content/guides/durable-ai-agents.mdx
- https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0
- https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/4aab69b4e6bcb53965ff5b1141d2f04a62a25c6c/CHANGELOG.md
---

# Replay, idempotency and effect semantics

## Definitions

**Replay** may mean reconstructing state from recorded events or executing a recorded procedure again. Those operations have different effect boundaries. **Retry** is another attempt at an operation whose earlier attempt failed or is uncertain. **Deduplication** recognizes repeated identities. **Idempotency** concerns the intended effect: [RFC 9110 section 9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) defines an HTTP method as idempotent when multiple identical requests have the same intended server effect as one request.

The RFC explicitly permits other per-request effects such as logging and warns against automatically retrying non-idempotent requests without knowing their semantics or whether the original was applied. HTTP method properties do not automatically establish the semantics of every agent tool.

## Three kinds of replay in this corpus

| Mechanism | Example | What it does not establish |
|---|---|---|
| Reconstruct client/session history | [[projects/agent-client-protocol]] documents a replay-complete event. | That an outstanding tool mutation completed or should run again. |
| Resume a persisted call | [[projects/rivet-agents]] distinguishes replay-safe reads, mutations using a persisted idempotency key honored by the destination, and calls not automatically rerun. | Exactly-once effects when the destination ignores the key or the tool's effect declaration is wrong. |
| Execute a saved workflow | [[projects/agent-browser]] tries direct HTTP, in-page requests and recorded browser commands. | Equivalent state, authorization or outcomes under a stale session. |

Sources: [ACP changelog](https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/4aab69b4e6bcb53965ff5b1141d2f04a62a25c6c/CHANGELOG.md), [Rivet guide](https://raw.githubusercontent.com/rivet-dev/agents/21c248b1d1d8c3a9d6c1cc7b85531a4a2d0e5c50/docs/content/guides/durable-ai-agents.mdx), [agent-browser v0.42 release](https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0). The comparison is architectural, not a shared performance result.

## The uncertain-effect interval

An operation can commit remotely before the caller records its result. A missing result therefore does not distinguish never-started, still-running and already-applied work. Stable operation identity can support deduplication; observing the resulting state can support reconciliation. Neither a persisted transcript nor a deterministic local procedure alone settles the remote outcome.

[[projects/builderio-agent-native]] supplies an adjacent record about observed-write classification; [[concepts/verified-completion-vs-apparent-success]] explains the evidence requirement. Use [[techniques/durable-agent-execution]] for recovery orchestration and [[techniques/deterministic-workflow-reuse]] for reusable procedure design.

## Limits and proposed test

Do not generalize HTTP idempotency into a guarantee about all mutations, irreversible actions or composed workflows. Compare replay mechanisms against a disposable endpoint with explicit operation IDs. Inject failures before mutation, after mutation and before result persistence; vary destination deduplication support and session freshness. Count duplicate effects, lost effects, unresolved outcomes and authorization violations separately. This is a proposed experiment; no measured reliability is introduced.
