---
uid: 18f9178b-41ac-4d02-aa15-4e510348467f
title: "RECEIPT — Process-aware tool execution"
summary: "A tool-execution protocol and process inspector that detects programs waiting for input, then exposes that state to othe"
type: project
created: 2026-11-10
updated: 2026-11-10
depth: full
sources:
  - https://arxiv.org/abs/2611.01930
---

# RECEIPT — Process-aware tool execution

**Source and date:** https://arxiv.org/abs/2611.01930 (2026-11-01).

## Mechanism

A tool-execution protocol and process inspector that detects programs waiting for input, then exposes that state to otherwise unchanged agents. Its Litmus catalog covers 158 checked command invocations; Tripwire has 25 paired tasks with and without an interactive question. Observe syscall-level wait states and explicitly represent incomplete operations instead of treating exit code zero as proof of task completion.

## Evidence and novelty

Authors analyze 91,469 production tool calls and 89,047 public agent trajectories. They report 11.5% false-success status-zero invocations with closed input, 2.9× token use for an unanswered terminal question, and a 73.5% reduction in false-success claims across five LLMs with RECEIPT. High: a concrete, measured harness-level failure mode that cannot be repaired by prompt wording alone.

## Comparison

Complements the Nov 9 production-assurance case and ProcGrep: those examine governance and trajectories; RECEIPT identifies a specific unobserved execution state.

## Limitations

Author-reported evaluation; not independently replicated here. Results depend on commands, operating systems and harness input wiring.

## Reproducible next step

Instrument ten common deployment commands, including confirmation prompts, password requests and editor invocations; assert both process completion and target-state postconditions.

## Related

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
