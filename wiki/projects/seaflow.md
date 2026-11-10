---
uid: b6a90502-a8d1-4d13-9a40-000000000022
title: "SeaFlow"
summary: "Canonical evidence record for SeaFlow; mechanism, limitations, practical implications and source provenance from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.01840
  - https://github.com/Applied-Machine-Learning-Lab/NeurIPS2026_SeaFlow
---

# SeaFlow

**Origin:** [[briefings/2026/11/2026-11-05]] — finding 2. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** November 1, 2026 paper; repository inspected November 5. **Sources:** [paper](https://arxiv.org/abs/2611.01840), [implementation](https://github.com/Applied-Machine-Learning-Lab/NeurIPS2026_SeaFlow). **Verdict:** High relevance and actionable; author-reported competition evidence.

**Built/demonstrated:** A framework for decomposing complex tasks into procedures with explicit applicability conditions. Procedures either execute code or call a model; execution feedback refines the decomposition and procedure selection. The authors evaluated bargaining, negotiation and persuasion in the GLEE competition and report first overall in the competition in the repository description.

**Agentic mechanism:** Turn repeatable decision segments into code while reserving LLM reasoning for uncertain or context-dependent steps. This is *selective compilation of behavior*, not blind conversion of every agent thought into a script.

**Evidence:** The paper reports that most observed final-decision procedures are implemented as code. The repository contains an implementation, but the competition result and efficiency claims are author-reported here; no controlled local cost or accuracy comparison was performed.

**Why frontier / comparison:** Builds on the pattern in SkillCompiler already cataloged in the KB: the novel emphasis is semantic task decomposition with explicit applicability conditions and feedback-driven evolution in interactive strategic tasks. It suggests a useful optimization objective: replace repeated model calls with stable procedures without losing adaptability.

**Practical takeaway:** Instrument a recurring agent workflow and classify each decision as deterministic, bounded-choice, or genuinely open-ended. Compile only the first two classes, then measure cost, success and fallback frequency.

**Caveat:** Success in negotiation games does not establish performance in repository engineering or browser automation; applicability-condition errors may silently route work to an unsuitable procedure.

## Mechanism and boundary

**SeaFlow decomposes complex interactive tasks into applicability-conditioned procedures.** A procedure may execute deterministic code or call a model; execution feedback can refine the decomposition, applicability conditions and procedure choice. The optimization target is selective reuse of stable decision logic while retaining model calls where reasoning is needed. The documented contribution is not durable checkpoint recovery or generic stateful orchestration.

## Critical evidence assessment

**Key risk:** An overly broad applicability condition may route a task to inappropriate deterministic code; an overly narrow one may increase fallback model calls and erase efficiency gains. Competition performance in bargaining, negotiation and persuasion does not independently establish transfer to coding or browser automation. Report both wrong-procedure selection and unnecessary model invocation, as well as final-task success and cost. The briefing's competition and efficiency claims remain author-reported.

## Directional relationships and comparative interpretation

Compare with [[projects/skillcompiler]] as a related but distinct method for replacing model decisions with executable code; SeaFlow emphasizes semantic decomposition, applicability conditions and feedback-based refinement. Compare with [[projects/agentos]] only to contrast procedural selection against durable task execution; they are not the same mechanism. These are analyst-level **compares_with** links, not direct dependency claims. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible evaluation

**Proposed, not executed:** Select 30 recurring, held-out workflow tasks spanning deterministic, bounded-choice and open-ended decisions. Compare (A) all-model execution, (B) fixed manually written procedures and (C) SeaFlow-style applicability-conditioned code/model procedures with execution-feedback refinement. Freeze models, task set, budgets and scoring. Measure applicability precision/recall, wrong-procedure selections, model-call reduction, fallback frequency, tokens, latency, total cost and independently accepted task success. Evaluate transfer to shifted task conditions and log every refinement and regression. Do not infer successful cost savings if accepted-task rate declines.

## Deployment considerations and open questions

Prototype in a sandbox with explicit fallback to the model when applicability is uncertain. Review generated code before promotion, version applicability predicates, and test distribution shifts. Open questions: how stable are applicability boundaries, how costly is procedure refinement, and which decision segments truly benefit from compilation?

## Provenance and depth

**Full evidence-scoped analytical synthesis of the archived paper/repository briefing, not independent reproduction.** The proposed ablations and comparisons are analyst experiments, not reported SeaFlow results.
