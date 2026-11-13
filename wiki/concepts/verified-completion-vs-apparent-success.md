---
uid: 0c17c078-693d-4eca-99fe-235e08f47719
title: "Verified completion versus apparent success"
summary: "Agent completion claims, user approval, tool acknowledgements and passing checks do not establish independently verified outcomes."
type: concept
created: 2026-11-09
updated: 2026-11-13
depth: full
sources:
  - https://arxiv.org/abs/2611.13246
  - https://arxiv.org/abs/2611.01484
  - https://arxiv.org/abs/2611.06841
  - https://arxiv.org/abs/2611.07464
  - https://arxiv.org/abs/2611.07947
  - https://arxiv.org/abs/2611.08321
  - https://arxiv.org/abs/2610.08651
  - https://arxiv.org/abs/2610.13361
  - https://github.com/BuilderIO/agent-native/pull/8670
  - https://raw.githubusercontent.com/OrchestratorInc/agent-orchestrator/main/docs/architecture.md
---

# Verified completion versus apparent success

## Claim and boundary

A task's apparent success is not equivalent to independent acceptance. This is an **analyst synthesis** across November 3–9 reports, not a claim that these projects share implementations. Distinguish five different observable outcomes: (1) agent declaration; (2) user approval; (3) tool acknowledgement; (4) executed validator result; and (5) independent, task-complete acceptance. A result at a lower tier cannot be silently promoted to a higher one.

## Supporting and limiting evidence

- **FINCOSMOS** ([[projects/fincosmos]], [paper](https://arxiv.org/abs/2611.07464)) reports **zero of 150** sessions satisfying its independent acceptance criteria, including user-approved sessions. Its hidden-intent, data-cutoff and metric-recomputation tests provide unusually concrete evidence of the gap. These are author-run benchmark results, not production failure rates.
- **ControlAnything** ([[projects/controlanything]], [paper](https://arxiv.org/abs/2611.08321)) reports 9/10 ready requests, but readiness establishes connector and transport acknowledgements, **not physical effects**. Acknowledgement is not actuation evidence.
- **ChemE-as-Code** ([[projects/cheme-as-code]], [paper](https://arxiv.org/abs/2611.07947)) versions engineering artifacts and checks dependency consistency; the illustrative ammonia design was **not independently engineer-reviewed**. Internal consistency is narrower than domain certification.
- **Production assurance case** ([[projects/assuring-ai-written-software]], [paper](https://arxiv.org/abs/2610.08651)) reports silently missing or proxy-based checks and an automated repair that disrupted operations. The check-execution record itself must be independently observable. Single-case qualitative evidence.
- **AgentSWE** ([[briefings/2026/11/2026-11-03]], [paper](https://arxiv.org/abs/2610.13361)) tests agents that construct other agents. Acceptance must cover the built agent's actual behavior rather than its self-description.

## Competing explanations and counterweights

A failed strict benchmark may reflect demanding or brittle acceptance criteria rather than an inherently useless agent. Conversely, user approval can be legitimate for subjective tasks. The synthesis concerns **claims of objective task completion**, where acceptance conditions can be operationalized; it does not imply every task needs an external oracle.

## Typed, evidence-scoped relations

- FINCOSMOS **evaluates** hidden-intent acceptance; ControlAnything **illustrates** a narrower transport-acknowledgement tier; ChemE-as-Code **implements** internal provenance checks. These are source-backed roles, not direct citations between projects.
- The production case **contradicts** the assumption that the presence of automated review implies that the review actually ran.
- **Extends** [[concepts/scoped-assurance]] and [[concepts/validation-tier-gap]] with an explicit acceptance-evidence ladder.

## Reproducible experiment

Create 30 repository-ingestion tasks with hidden acceptance rules and planted failures: missing source dates, fabricated metrics, skipped validators, unresolved canonical aliases and tools that acknowledge a write without persisting it. Compare agent self-verdict, user-style review, and independent checker verdict. Report full-acceptance rate, false acceptances, abstentions and checker execution coverage, not merely PR counts.

## Evidence status

Cross-paper inference assembled from the cited primary reports and existing canonical records; no experiment run for this synthesis. Published numbers remain author-reported.

## 2026-11-10 evidence connections

Two deepened project pages (sources re-read 2026-11-10) extend this concept from gap-**measurement** to gap-**closure**. Both links are analyst-level relations to KB project pages; neither source names the concept.

- **[[projects/builderio-agent-native]] — the concept implemented as infrastructure.** BuilderIO's observed-write classification replaces a position-derived completion verdict ("the handler started, so it might have written" → the run ends `write_tool_outcome_unknown` even for pre-save rejections) with an observation-derived one, fail-closed at every boundary: unknown SQL is a write, an unwrappable `fetch` counts every call as having sent a write, and a never-arrived result stays `unknown`. This is the acceptance-evidence ladder's discipline built into the call path rather than measured after the fact — the run-ending verdict becomes evidence-derived instead of control-flow-derived. Bounds, from the inspected PR record: the observation funnel sits *beneath* explicit author labels (`NoWriteError` / `retrySafe` take precedence over observed evidence), its completeness is the whole property (an unobserved write channel reads as retry-safe — the inverse of the failure being fixed), and three review findings were declined as documented risks rather than fixed. Mechanism inspected (PR threads and raw files at head commit `dec69e4c`); every verification number is author-reported.
- **[[projects/agent-orchestrator]] — the discipline applied to UI state and irreversible actions.** The architecture's context-boundary rule refuses to represent continuity it cannot prove ("Prior rows remain intact, but are not represented as context inherited by the new provider"), and session termination is fail-closed against the same error class: "Failed probes are NOT proof of death," with termination requiring both-dead evidence, no contradicting recent activity, and no merged-PR ownership. Vendor-documented mechanism with zero published outcome measurement — the instance shows the discipline *designed*, not its effect measured.

Typed relations: builderio-agent-native **implements** the acceptance-evidence discipline as call-path infrastructure; agent-orchestrator **applies** it to display status and irreversible actions. Neither is a benchmark measurement of the gap like the five instances above, so both rows extend the concept's evidence base rather than re-grade it.

## November 13 update: compositional acceptance

[[projects/expertcrowd-swe]] uses calibrated executable merge blockers (https://arxiv.org/abs/2611.13246); [[projects/crossswe]] rejects incomplete multi-repository fixes (https://arxiv.org/abs/2611.01484); [[projects/serverbench]] independently verifies optimized execution paths (https://arxiv.org/abs/2611.06841). These independently support the *need* for scoped postconditions, not proof that any single grader guarantees correctness. Counterexamples include superficial patches, partial repo changes, unexercised optimized paths and held-out grader opacity. Proposed experiment: 25 fixed tasks with hidden postconditions and adversarial no-op patches; compare apparent success with externally verified success and regression rate. All published performance numbers are author-reported and protocol-relative.
