---
uid: 4e147fb5-357e-4b70-9ac2-f19f502cd4bb
title: "Durable agent execution"
summary: "Persist execution state, classify interrupted effects and reconcile retries without assuming exactly-once external actions."
type: technique
created: 2026-11-14
updated: 2026-11-14
depth: full
sources:
  - https://raw.githubusercontent.com/rivet-dev/agents/21c248b1d1d8c3a9d6c1cc7b85531a4a2d0e5c50/docs/content/guides/durable-ai-agents.mdx
  - https://raw.githubusercontent.com/openma-ai/open-managed-agents/d45d7dc194187130bbdd375261d2e6e3c064f812/README.md
---

# Durable agent execution

## Mechanism

Durable execution separates the record of an agent's work from the process currently running it. The practical question is which calls can be repeated after interruption, and which require observation or reconciliation first. The comparison below is an analyst interpretation of documented designs, not a measured common implementation.

| Design | Persisted boundary | Recovery contract |
|---|---|---|
| [[projects/rivet-agents]] | Actor-owned SQLite records model calls, tool calls and plan state. | The guide marks replay-safe reads separately; mutating examples persist an idempotency key through `api.memo` and require the destination API to honor it. Tools without safe replay return an interrupted-call result rather than automatically repeating. |
| [[projects/openma]] | Session history survives independently of the harness and sandbox. | The README describes durable execution claims, renewable leases and fencing across replicas; replacement harnesses rebuild context from durable events after sandbox loss. Workspace restoration remains dependent on the configured resources. |

Sources: [Rivet durable-agent guide](https://raw.githubusercontent.com/rivet-dev/agents/21c248b1d1d8c3a9d6c1cc7b85531a4a2d0e5c50/docs/content/guides/durable-ai-agents.mdx), [OpenMA README](https://raw.githubusercontent.com/openma-ai/open-managed-agents/d45d7dc194187130bbdd375261d2e6e3c064f812/README.md). These describe mechanisms and contracts, not independently measured reliability.

## Distinct responsibilities

Persist the call identity and relevant intent before dispatch. Preserve the returned result when available. After interruption, distinguish a known failure, a known effect and an unknown effect. A repeated request needs a stable identity; preventing duplicate effects additionally requires cooperation from the effecting system or a reconciliation procedure. Leases and fencing address competing workers, while idempotency addresses repeated operations. Neither replaces outcome observation.

[[concepts/verified-completion-vs-apparent-success]] explains why an acknowledgement or resumed conversation does not establish the intended external result. [[projects/builderio-agent-native]] and [[projects/agentos]] offer adjacent write-classification and recovery records; [[projects/receipt]] concerns process-state observation. These are further reading, not claims that the systems share the same recovery guarantee.

## Limits and counterexamples

A persisted transcript can coexist with an unrecorded remote mutation. A destination that ignores idempotency keys can duplicate effects even when the caller reuses the same key. An interrupted tool may have partially completed. Read-only replay is safe only within the declared effect model. The documented designs do not establish universal exactly-once execution or reliability across every tool integration. Use [[concepts/scoped-assurance]] when stating the tested boundary.

## Proposed experiment

Use a disposable endpoint that records unique operation IDs and supports an optional idempotency key. Compare naive retry, persisted identity with destination deduplication, and reconciliation before retry. Inject crashes before mutation, after mutation and before local result persistence. Repeat each point and record duplicate effects, lost effects, unknown outcomes, recovery time and concurrent-worker interference. A correctly recorded unknown is distinct from a verified successful effect. No experiment is reported here.

## Evidence status and reading path

The primary documents above were read on November 14, 2026; their mechanisms were not executed. No independent reliability measurement is introduced. Continue through [[topics/agent-execution-and-recovery]] and [[topics/security-and-authority]] for recovery authority and enforcement boundaries.
