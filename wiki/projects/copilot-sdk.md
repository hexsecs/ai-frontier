---
uid: e3e2e8f5-bfa6-43f6-8e3d-0f8a622abda7
title: "Microsoft Copilot SDK"
summary: "Preview SDK exposing command operations, compaction attribution and corrected background-subagent event ordering."
type: project
created: 2026-11-22
updated: 2026-11-22
depth: full
sources:
  - https://github.com/microsoft/copilot-sdk/releases/tag/v2.0.2-preview.4
---

# Microsoft Copilot SDK

**Primary release:** [November 21, 2026](https://github.com/microsoft/copilot-sdk/releases/tag/v2.0.2-preview.4).

The November 21 v2.0.2-preview.4 notes describe shared command operations and caller-specific SDK settings, experimental fusion attribution on session compaction, a change to reasoning ciphertext representation, and a fix for session.idle arriving before assistant.idle when a parent resumed after background subagent completion. They also describe registry distribution improvements. This is a preview release, not a measured correctness study.

**Mechanism.** Distinct event types describe assistant, session and delegated-worker lifecycle. Event ordering matters because consumers may otherwise infer terminal status from a premature idle signal. [[concepts/agent-state-and-lifecycle]] provides the state vocabulary; [[concepts/verified-completion-vs-apparent-success]] explains why correct idle ordering is not equivalent to task acceptance.

**Novelty.** A specific event-order race fix and attribution fields, not a new multi-agent algorithm. Downstream SDK clients may have different compatibility and event-consumption assumptions.

**Proposed experiment.** Launch 30 mock background subagent jobs, deliberately vary completion and parent-resume timing, compare preview versions and assert event partial order and independent output acceptance. No SDK test was executed.
