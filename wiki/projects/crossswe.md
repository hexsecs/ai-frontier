---
uid: b6a90405-a8d1-4d13-9a40-000000000015
title: "CrossSWE"
summary: "Canonical evidence record for CrossSWE; mechanism, limitations, practical implications and source provenance from the November 4 briefing."
type: benchmark
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://arxiv.org/abs/2611.01484
---

# CrossSWE

**Origin:** [[briefings/2026/11/2026-11-04]] — finding 5. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** November 1, 2026. **Primary source:** [CrossSWE paper](https://arxiv.org/abs/2611.01484). **Verdict:** High relevance for real-world agent evaluation; author-reported benchmark results, not independently reproduced here.

**What was built.** A benchmark for cross-repository joint development: 171 real-world instances spanning 165 repositories, 20 technical domains, and 13 programming languages. Each instance is constructed so that a partial, single-repository change is insufficient — the intended behavior requires coordinated changes across interdependent repositories.

**Key technique:** Verify the necessity of coordinated changes by testing whether partial repository modifications fail to achieve the intended behavior, rather than inferring coordination from diff size alone.

**Evidence:** Across the five LLMs the authors evaluated, the strongest model (GPT-6.1 Sol) achieved only 58.48% Pass@1, and cross-repository inconsistencies were the most prevalent failure mode (44.2%).

**Why interesting:** Most coding-agent benchmarks still score work inside one repository. Real maintenance increasingly spans a service, its client libraries, and its fixtures — exactly where dependency reasoning, change propagation, and interface consistency break down. This connects directly to today's delegation findings: coordinating *changes* across repositories is as measurable a bottleneck as coordinating *agents* within one.

**Practical takeaway:** Evaluate agents on at least one task that requires synchronized changes in two repositories with a shared interface; score interface consistency explicitly, and treat a passing single-repository test suite as insufficient evidence of completion.

**Limitations:** A single benchmark with author-run evaluations of five models; its instance construction favors tasks where coordination is verifiably necessary, so its scores are not comparable to single-repository benchmarks.

## Mechanism and system boundary

The primary reusable mechanism is **Cross-environment software engineering evaluation**. Treat the agent model, orchestration state, tool authority, persistent artifacts and independent checker as separate components. The archived evidence above establishes what the authors or maintainers reported; it does not establish cross-domain transfer or a successful local deployment.

## Evidence interpretation and counterevidence

**Key failure mode:** Headline pass rates may conflate environment setup, tool selection and code correctness. The evidence tier is limited to the dated source assessment above. Do not interpret a repository release, simulated benchmark, user survey or PR proposal as independently reproduced production reliability. A null or missing validator result is an unknown, not a pass.

## Comparative synthesis and relationships

Relevant canonical context: [[benchmarks/index]]; [[projects/weavebench]]. These are analyst-selected **compares_with** or thematic relationships; none implies that the linked projects directly depend on one another. Cross-cutting questions include what state is persisted, what is observable, which actors have authority, and what independently proves the requested outcome. See [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Reproducible validation protocol

**Proposed, not executed:** Run matched patches in isolated environments; separate setup failure, test execution and hidden acceptance. Freeze the model/runtime version, dataset and prompts; preserve raw traces, tool receipts, source excerpts, checker outputs and failed attempts. Report numerator/denominator, uncertainty and cost, with a baseline and a held-out transfer set. Never promote a performance claim without the actual independent acceptance record.

## Operational adoption and open questions

Adopt as an isolated prototype before production use. Require explicit ownership of side effects, auditability and rollback. Open questions: does the result survive a new task distribution; does a simpler baseline achieve similar quality; can failure be detected without consulting the producing agent; and what happens when an external write's outcome is unknown?

## Provenance and depth assessment

**Depth: full analytical synthesis of the archived briefing, not independently replicated research.** This page preserves original author-reported numbers and source URLs; the new threat model, comparisons and experiment are editorial analysis. Deeper source inspection and reproduction are separate future work.
