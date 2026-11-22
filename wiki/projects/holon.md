---
uid: 92b8b42d-3c7e-4ad9-a2c2-892a55d4231a
title: "Holon runtime"
summary: "Durable agent runtime with bounded event pagination, recovery-before-dispatch and serialized-writer relief."
type: project
created: 2026-11-22
updated: 2026-11-22
depth: full
sources:
  - https://github.com/holon-run/holon/releases/tag/v0.60.0
---

# Holon runtime

**Primary release:** [November 21, 2026](https://github.com/holon-run/holon/releases/tag/v0.60.0).

The November 21 v0.60.0 release describes moving pure reads and probes away from a serialized shared writer, bounded event pagination and per-round tool/payload admission, deterministic startup recovery ordering, and isolation of rollback-safe agent startup faults. These are implementation and maintainer claims, not measured throughput or correctness improvements.

**Mechanism.** Separating reads from the mutation serialization queue reduces unnecessary contention; dispatch is gated until recovery completes so fresh work cannot race unfinished restoration. [[concepts/agent-state-and-lifecycle]] distinguishes worker, session and external-effect state; [[techniques/durable-agent-execution]] explains why a recovered task record still needs effect reconciliation.

**Novelty.** A concrete runtime-reliability release addressing ordering and boundedness, not a novel planning model. Moving reads off a writer queue may improve latency but does not automatically guarantee snapshot consistency or exactly-once effects.

**Proposed experiment.** Replay 50 read-heavy tasks while injecting restart at five recovery phases. Compare old/new pinned tags for read latency, writer wait, duplicate dispatch, unresolved writes and accepted task results. No benchmark was reproduced.
