---
uid: b54b13d9-becf-4eec-a930-975759b1202a
depth: full
title: "Evidence-backed comparison of agent systems"
summary: "Compare agent systems by mechanisms, evidence scope and uncertainty rather than shared vocabulary."
type: evaluation
created: 2026-11-02
updated: 2026-11-14
sources: []
---

# Evidence-backed comparison of agent systems

## What constitutes a useful relationship

Shared words such as “memory,” “agent,” or “verification” establish topical similarity, not a shared implementation, measured benefit or dependency. A defensible comparison identifies the mechanism in each system, the evidence supporting it, and the boundary of the inference.

[[projects/evoteam]] stores reusable teams and team-scoped collaboration rules; [[projects/agenticds]] uses typed contracts between fixed roles. Both coordinate agents, but that shared purpose does not establish equivalent mechanisms or transferable performance. [[techniques/multi-agent-orchestration]] explains their different designs.

## Compare evidence as well as mechanisms

[[concepts/protocol-relative-scores]] explains why scores from different task sets, feedback conditions or acceptance rules cannot be treated as a common ranking. [[concepts/comparator-construction-shapes-margins]] addresses how adapted baselines and unequal budgets can shape reported margins. These are analyst interpretations of the cited studies, not additional measurements.

A verification result should be bounded by the cases actually checked ([[concepts/scoped-assurance]]). A grader that shares models or data with the system it evaluates can introduce [[concepts/evaluator-circularity]]; a different role name alone does not establish independent validation.

## Uncertainty and counterevidence

Record an untested architectural analogy as a hypothesis. Distinguish “implements,” “evaluates” and “depends on” from “can be compared with.” A directional dependency requires source evidence for that direction; reciprocal navigation does not establish a reciprocal dependency.

[[projects/security-impact-of-coding-agent-memory-files]] provides a limiting case for claims that persistent text reliably steers later behavior. [[concepts/improvement-lives-in-external-state]] discusses both supporting instances and this null result. A useful synthesis retains such counterexamples rather than treating every related project as supporting evidence.

## Evidence limits

The linked project and concept pages supply the underlying source references and author-reported findings. This comparison introduces no benchmark result and does not establish independent replication.
