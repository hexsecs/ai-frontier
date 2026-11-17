---
uid: 494e689b-f1c1-438e-859d-9ca55a6093b6
title: "Aligning AI Teams — System-level safety ownership"
summary: "Delegated responsibility and system-level acceptance: A designated safety lead checks whole-team objectives and a coordinator pub."
type: project
created: 2026-11-17
updated: 2026-11-17
depth: full
sources:
  - https://arxiv.org/abs/2611.17820
---

# Aligning AI Teams — System-level safety ownership

**Primary study:** [https://arxiv.org/abs/2611.17820](https://arxiv.org/abs/2611.17820), 2026-11-13. This is an author-reported research implementation; no independent replication is claimed.

## Mechanism and boundary

A designated safety lead checks whole-team objectives and a coordinator publishes a safety specification; researchers compare this with ordinary peer critique and group chat. The reusable distinction is **delegated responsibility and system-level acceptance**. [[techniques/multi-agent-orchestration]] and [[concepts/contracts-and-compositional-correctness]] explain the neighboring mechanism and its limits; similarity of vocabulary does not imply identical architecture.

## Evidence and novelty

In two software-engineering scenarios and ten consulting tasks across five models, authors find that team critique and group chat do not reliably close single-agent safety gaps; a designated safety lead and explicit safety specification perform better in their studied settings.

Demonstrates that individually aligned workers can collectively neglect a system-level invariant; role assignment alone is insufficient unless someone owns the invariant. **Boundary:** The evaluation intentionally constructs safety/business tradeoffs; it does not prove the same effect magnitude in routine repository teams or every safety domain.

## Practical engineering test

Use 12 seeded multi-agent coding tasks with cross-module safety invariants. Compare no lead, peer-review-only and safety-lead-plus-spec; score independently verified invariant violations, completion and cost.

**Engineering implication:** Assign one agent responsibility for cross-task invariants and require a signed-off acceptance artifact, not merely peer critique.
