---
uid: b6a90405-a8d1-4d13-9a40-000000000015
title: "CrossSWE"
summary: "Canonical evidence record for CrossSWE; mechanism, limitations, practical implications and source provenance from the November 4 briefing."
type: benchmark
created: 2026-11-09
updated: 2026-11-09
depth: brief
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

## Knowledge-base synthesis

This entry preserves the finding as a reusable canonical reference rather than leaving it accessible only by briefing date. Compare its stated mechanism and evidence tier against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]], and the [November 3–9 cross-briefing synthesis](../evaluations/briefing-synthesis-2026-11-03-to-09.md). These are analyst-level thematic connections, not assertions that the original project cites or implements the linked concepts. Future source verification should replace this backfill with a deeper independently checked treatment while retaining this page identity.
