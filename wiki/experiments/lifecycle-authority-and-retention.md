---
uid: cc47d592-9e36-4e22-b800-9ab592b280cb
title: Lifecycle, authority and retention fault injection
summary: A proposed controlled test of delegated work, unknown effects, authority revocation and deleted data after restoration.
type: experiment
created: '2026-11-16'
updated: '2026-11-16'
depth: full
sources:
- https://raw.githubusercontent.com/agentclientprotocol/agent-client-protocol/4aab69b4e6bcb53965ff5b1141d2f04a62a25c6c/CHANGELOG.md
- https://raw.githubusercontent.com/compozy/compozy/8cbf8a5a4dcb343f349e2b47635a461bea0c9b24/CHANGELOG.md
- https://github.com/framerslab/agentos/releases/tag/v0.18.0
- https://raw.githubusercontent.com/rivet-dev/agents/21c248b1d1d8c3a9d6c1cc7b85531a4a2d0e5c50/docs/content/guides/durable-ai-agents.mdx
---

# Lifecycle, authority and retention fault injection

**Status: proposed; not executed.** The source documents motivate separate failure cases; they do not jointly validate this experiment.

## Hypotheses and controls

Explicit effect identities and reconciliation may reduce duplicate actions, while authority ceilings and retention tombstones may prevent specific post-restart failures. Test these as separate factors rather than assuming one combined reliability score proves all mechanisms.

Use 20 fixed disposable tasks with parent/child workers, a synthetic state-changing endpoint, a retrieval store and a versioned output. Freeze the task set, model, acceptance checker and resource budget. Compare a baseline, baseline plus durable reconciliation, and reconciliation plus explicit authority/retention enforcement. Repeat with randomized fault order and retain per-task outcomes.

## Faults and observations

| Fault | Required observation |
|---|---|
| Crash after an endpoint mutation but before local result persistence | Independently count effects and inspect the recorded unknown outcome; a missing result is not a failed effect. |
| Cancel or delete a child while the parent waits | Inspect parent terminal state, descendant activity and retained tool grants. |
| Revoke authority during a pending call, then restart | Distinguish effects committed before revocation from subsequent unauthorized effects. |
| Delete a synthetic subject, then restore an older store | Probe active rows, derived retrieval data and preserved tombstone state; verify unrelated subjects remain accessible. |
| Replay a history or saved flow | Check reconstructed state separately from remote postconditions and session freshness. |

## Metrics and acceptance

Report verified task completion, stranded parents, duplicate/lost effects, truthfully unknown effects, surviving unauthorized grants, recovered deleted content, rollback mismatches, cost and elapsed time. Publish counts and denominators for each fault. A critical authorization or retention violation cannot be hidden by an average success increase. Audit the independent checker with planted false completions and absent receipts.

The test distinguishes mechanism conformance from broader security or privacy guarantees. Synthetic tasks cannot establish every real deployment boundary. No success rate or gain is asserted.

## Reading path

[[concepts/agent-state-and-lifecycle]], [[concepts/replay-idempotency-and-effect-semantics]], [[concepts/delegated-authority-and-revocation]], [[techniques/durable-agent-execution]] and [[techniques/agent-skills-and-memory]] explain the conceptual boundaries. The independent ingestion experiments remain separate protocols with different task objectives.
