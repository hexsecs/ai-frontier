---
uid: 4e147fb5-357e-4b70-9ac2-f19f502cd4bb
title: "Durable agent execution"
summary: "Persist execution state, classify interrupted effects and reconcile retries without assuming exactly-once external actions."
type: technique
created: 2026-11-14
updated: 2026-11-23
depth: full
sources:
  - https://raw.githubusercontent.com/rivet-dev/agents/21c248b1d1d8c3a9d6c1cc7b85531a4a2d0e5c50/docs/content/guides/durable-ai-agents.mdx
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/d45d7dc194187130bbdd375261d2e6e3c064f812/README.md
  - https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/4aab69b4e6bcb53965ff5b1141d2f04a62a25c6c/CHANGELOG.md
  - https://raw.githubusercontent.com/compozy/compozy/8cbf8a5a4dcb343f349e2b47635a461bea0c9b24/CHANGELOG.md
  - https://raw.githubusercontent.com/paperclipai/paperclip/b4fa1c7fb1c9adafc6407bc46381a0ab89f4b4fd/releases/v2026.1005.0.md
  - https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0
---

# Durable agent execution

## Mechanism

Durable execution separates the record of an agent's work from the process currently running it. The practical question is which calls can be repeated after interruption, and which require observation or reconciliation first. [[projects/openai-agents-sdk]] adds a third storage boundary: its November 8 [alpha release](https://github.com/openai/openai-agents-python/releases/tag/v0.24.0-alpha.7) documents caller-owned CustomStorage for root Sessions while explicitly warning that uncertain tool effects must be reconciled on resume. This distinguishes **storage ownership** from **remote-effect deduplication**: persistence can restore context without proving a mutation occurred once. [[projects/planning-with-files]] persists task intent in Markdown across context clearing, a different layer again; its completion gate does not establish the external state of a remote write. A crash-injection comparison should separately observe recovered instructions, reconstructed calls and remote effects.

The comparison below is an analyst interpretation of documented designs, not a measured common implementation.

| Design | Persisted boundary | Recovery contract |
|---|---|---|
| [[projects/rivet-agents]] | Actor-owned SQLite records model calls, tool calls and plan state. | The guide marks replay-safe reads separately; mutating examples persist an idempotency key through `api.memo` and require the destination API to honor it. Tools without safe replay return an interrupted-call result rather than automatically repeating. |
| [[projects/openma]] | Session history survives independently of the harness and sandbox. | The README describes durable execution claims, renewable leases and fencing across replicas; replacement harnesses rebuild context from durable events after sandbox loss. Workspace restoration remains dependent on the configured resources. |

Sources: [Rivet durable-agent guide](https://raw.githubusercontent.com/rivet-dev/agents/21c248b1d1d8c3a9d6c1cc7b85531a4a2d0e5c50/docs/content/guides/durable-ai-agents.mdx), [OpenMA README](https://raw.githubusercontent.com/openma-ai/open-managed-agents/d45d7dc194187130bbdd375261d2e6e3c064f812/README.md). These describe mechanisms and contracts, not independently measured reliability.

## Session replay and delegated-work reconciliation

[[concepts/agent-state-and-lifecycle]] separates restored session history, live worker state and external effects. [[projects/agent-client-protocol]] documents an unstable replay-complete notification; [[projects/compozy]] documents deleted-child settlement, parent wake delivery and orphan reconciliation at boot. These are different lifecycle boundaries, not implementations of one recovery protocol ([ACP](https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/4aab69b4e6bcb53965ff5b1141d2f04a62a25c6c/CHANGELOG.md), [Compozy](https://raw.githubusercontent.com/compozy/compozy/8cbf8a5a4dcb343f349e2b47635a461bea0c9b24/CHANGELOG.md)).

[[projects/agent-browser]] adds another meaning of replay: rerunning a recorded browser flow through different execution tiers ([v0.42 release](https://github.com/vercel-labs/agent-browser/releases/tag/v0.42.0)). [[concepts/replay-idempotency-and-effect-semantics]] distinguishes that procedure from reconstructing history or safely repeating a remote effect. [[projects/paperclip]] documents cross-task files and human browser takeover, which improve continuity without establishing retry safety ([release](https://raw.githubusercontent.com/paperclipai/paperclip/b4fa1c7fb1c9adafc6407bc46381a0ab89f4b4fd/releases/v2026.1005.0.md)).

Extend crash tests to a waiting parent whose child disappears, a client reconstructing events, and a saved flow using stale credentials. Score each boundary separately; successful reconstruction is not evidence that outstanding mutations completed.

## Distinct responsibilities

Persist the call identity and relevant intent before dispatch. Preserve the returned result when available. After interruption, distinguish a known failure, a known effect and an unknown effect. A repeated request needs a stable identity; preventing duplicate effects additionally requires cooperation from the effecting system or a reconciliation procedure. Leases and fencing address competing workers, while idempotency addresses repeated operations. Neither replaces outcome observation.

[[concepts/verified-completion-vs-apparent-success]] explains why an acknowledgement or resumed conversation does not establish the intended external result. [[projects/builderio-agent-native]] and [[projects/agentos]] offer adjacent write-classification and recovery records; [[projects/receipt]] concerns process-state observation. These are further reading, not claims that the systems share the same recovery guarantee.

## Limits and counterexamples

A persisted transcript can coexist with an unrecorded remote mutation. A destination that ignores idempotency keys can duplicate effects even when the caller reuses the same key. An interrupted tool may have partially completed. Read-only replay is safe only within the declared effect model. The documented designs do not establish universal exactly-once execution or reliability across every tool integration. Use [[concepts/scoped-assurance]] when stating the tested boundary.

## Proposed experiment

Use a disposable endpoint that records unique operation IDs and supports an optional idempotency key. Compare naive retry, persisted identity with destination deduplication, and reconciliation before retry. Inject crashes before mutation, after mutation and before local result persistence. Repeat each point and record duplicate effects, lost effects, unknown outcomes, recovery time and concurrent-worker interference. A correctly recorded unknown is distinct from a verified successful effect. No experiment is reported here.

## Evidence status and reading path

The primary documents above were read on November 14, 2026; their mechanisms were not executed. No independent reliability measurement is introduced. Continue through [[topics/agent-execution-and-recovery]] and [[topics/security-and-authority]] for recovery authority and enforcement boundaries.


**Atomic internal state is not exactly-once external effects.** [[projects/microsoft-agent-framework-python-123]] ([Python 1.23 release](https://github.com/microsoft/agent-framework/releases)) documents atomic Memory/Todo writes, completion waits bound to execution identity, and cleanup of abandoned nested streams. These changes target distinct internal race and lifecycle boundaries. [[projects/novelmaker-agent-tool-message-repair]] ([1.7.0 release](https://github.com/wg-1337/NovelMaker/releases)) addresses a different layer: preserving the on-disk history while constructing a valid outgoing tool-call transcript after interruption. Neither establishes whether an external mutation was applied. Crash tests should distinguish durable state, outbound request validity, event ordering and independently observed effects; no cross-project benchmark is reported.
