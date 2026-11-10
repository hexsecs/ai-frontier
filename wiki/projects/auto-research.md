---
uid: b6a90501-a8d1-4d13-9a40-000000000021
title: "auto_research"
summary: "Canonical evidence record for auto_research; mechanism, limitations, practical implications and source provenance from the November 5 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.05251
---

# auto_research

**Origin:** [[briefings/2026/11/2026-11-05]] — finding 1. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** November 3, 2026. **Source:** [primary paper](https://arxiv.org/abs/2611.05251). **Verdict:** High novelty; unusually concrete scientific deployment; early, author-reported validation.

**Built/demonstrated:** A semi-autonomous multi-agent pipeline that retrieves and analyzes raw High Energy Astrophysics Science Archive Research Center (HEASARC) data, writes new analysis tools as needed, and drafts reports about Imaging X-ray Polarimetry Explorer (IXPE) observations. The pipeline reproduced a published Cyg X-1 analysis, undertook a six-observation polarization-stability analysis, surveyed 29 observations for polarization–hardness relations, and searched for lag between Stokes parameters.

**Agentic mechanism:** Tool self-extension is staged. New tools undergo repeated automated runs, a fabricated-value-phrase scan, and cross-provider model review; a human approves promotion into the trusted branch. A reported number is allowed only if it appears in a recorded tool output, the request, or a located cited publication. The agent cannot merely narrate a plausible measurement.

**Evidence:** In a 65-defect injection study, 47 planted defects passed the automated checks and one passed the additional code review. The review also rejected 40 of 69 correct changes. The pipeline's 14 compared Cyg X-1 quantities agreed with published results within 3 sigma, although polarization-degree estimates were lower. With weaker main-role models, it recovered 12/14 quantities and explicitly marked two as unmeasured. These are the author's tests; the high false-rejection rate is material.

**Why frontier / comparison:** Unlike general self-improving coding agents, this explicitly connects generated code, scientific measurements and provenance. Compared with November 4's deterministic tool authorization, it addresses whether *results* are traceable to actual executions, not just whether a tool was permitted.

**Practical takeaway:** For automated research or knowledge-base ingestion, require every numeric assertion to carry a machine-checkable reference to a tool-output artifact or a cited source location. Keep human review for promotion of newly generated tools.

**Caveat:** Reproduction within 3 sigma is not proof of correct independent inference, and the review rejects many valid patches. Audit both false accepts and false rejects before deploying such a gate.

## Mechanism and boundary

The reusable mechanism is **Scientific tool generation with staged promotion and result provenance**. Distinguish model reasoning, tool execution, persistent state, side effects, and the independently observed acceptance condition. The historical source summary above is the factual evidence base; the interpretation below is an analyst synthesis.

## Critical evidence assessment

**Failure mode / counterweight:** 47 of 65 planted defects passed automated checks; review rejected 40 of 69 correct changes (author-reported). The cited sources have not been independently reproduced in this mining pass. Report source-reported metrics as such, and do not equate a successful demo, publication, repository release or PR proposal with production readiness. Negative and missing results matter as much as successes.

## Directional relationships and comparative interpretation

Related evidence: [[concepts/evaluator-circularity]]; [[concepts/verified-completion-vs-apparent-success]]. These are analyst-level **compares_with** links, not verified direct dependencies. Compare this mechanism against the simpler baseline, distinguish quality from throughput, and preserve task-level losses rather than averaging them away. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible evaluation

**Proposed, not executed:** Inject 30 incorrect data-analysis tools and 30 correct ones; measure false acceptance, false rejection and traceable measurements. Hold model, prompts, inputs and budget constant; log task-level results, full tool receipts, source spans, failed attempts, checker execution, elapsed time and tokens. Evaluate unseen cases and require explicit evidence before promoting changes to a trusted workflow.

## Deployment considerations and open questions

Sandbox the initial integration. Specify the authority boundary, persistence model, rollback path and owner of independent acceptance. Open questions include transfer to unseen tasks, sensitivity to the evaluator, total operational cost and whether the same improvement survives adversarial failure injection.

## Provenance and depth

**Full analytical treatment based on the dated primary-source briefing; not an independent replication.** Historical claims are preserved above; comparisons, risks and tests in this section are proposed analyses.
