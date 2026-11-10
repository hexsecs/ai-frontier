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

The reusable mechanism is **Persistent agent execution and coordination across tasks**. Distinguish model reasoning, tool execution, persistent state, side effects, and the independently observed acceptance condition. The historical source summary above is the factual evidence base; the interpretation below is an analyst synthesis.

## Critical evidence assessment

**Failure mode / counterweight:** State persistence does not ensure side-effect consistency; retry semantics and stale state can corrupt outcomes. The cited sources have not been independently reproduced in this mining pass. Report source-reported metrics as such, and do not equate a successful demo, publication, repository release or PR proposal with production readiness. Negative and missing results matter as much as successes.

## Directional relationships and comparative interpretation

Related evidence: [[projects/agentos]]; [[concepts/preservation-aware-agent-improvement]]. These are analyst-level **compares_with** links, not verified direct dependencies. Compare this mechanism against the simpler baseline, distinguish quality from throughput, and preserve task-level losses rather than averaging them away. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible evaluation

**Proposed, not executed:** Run interrupted multi-step workflows; compare checkpoint correctness, duplicate actions and verified end states. Hold model, prompts, inputs and budget constant; log task-level results, full tool receipts, source spans, failed attempts, checker execution, elapsed time and tokens. Evaluate unseen cases and require explicit evidence before promoting changes to a trusted workflow.

## Deployment considerations and open questions

Sandbox the initial integration. Specify the authority boundary, persistence model, rollback path and owner of independent acceptance. Open questions include transfer to unseen tasks, sensitivity to the evaluator, total operational cost and whether the same improvement survives adversarial failure injection.

## Provenance and depth

**Full analytical treatment based on the dated primary-source briefing; not an independent replication.** Historical claims are preserved above; comparisons, risks and tests in this section are proposed analyses.
