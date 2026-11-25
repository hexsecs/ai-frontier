---
uid: d0a5f1a0-6f83-4c8e-9c1f-4e142aa21b10
title: "deja-vu"
summary: "Coding-agent memory and lineage CLI with fast recall, parallel-edit detection and subagent parent briefs."
type: project
created: 2026-11-22
updated: 2026-11-22
depth: full
sources:
  - https://github.com/vshulcz/deja-vu/releases/tag/v0.25.0
---

# deja-vu

**Primary release:** [November 21, 2026](https://github.com/vshulcz/deja-vu/releases/tag/v0.25.0).

The November 21 v0.25.0 maintainer release describes three new agent readers, bringing its supported coding-agent readers to 52, a composite GitHub Action, sub-second cold recall, 2.3 MB synced manifests, parallel edit radar, subagent parent briefs, two-strike fix gating and pass-rate ranking of verification commands. The stated latency and size are vendor-reported, not independently measured.

**Mechanism.** Persistent manifest and lineage indexes support retrieval of prior work; a subagent can carry a compact parent brief rather than assume shared transcript continuity. Parallel edit detection identifies possible conflicting workspace mutations. These are distinct from correctness of remembered conclusions. [[techniques/agent-skills-and-memory]] discusses admission and retrieval; [[concepts/contracts-and-compositional-correctness]] bounds cross-agent integration.

**Novelty.** The release joins fast retrieval and concurrent-edit awareness in one developer workflow, but is incremental. A memory hit or pass-rate-ranked command is not proof that the present repository is equivalent to the historical state.

**Proposed experiment.** Run 20 disposable multi-agent code tasks with and without lineage recall; force concurrent edits to five shared files. Score missed conflicts, false conflicts, accepted patches, recall latency and stale references against fixed independent tests. No experiment was run.
