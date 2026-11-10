---
uid: b6a90401-a8d1-4d13-9a40-000000000011
title: "GitHub Octoverse 2026"
summary: "Canonical evidence record for GitHub Octoverse 2026; mechanism, limitations, practical implications and source provenance from the November 4 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/
---

# GitHub Octoverse 2026

**Origin:** [[briefings/2026/11/2026-11-04]] — finding 1. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** October 28, 2026. **Primary source:** [GitHub's 2026 Octoverse report](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/). **Verdict:** High relevance, strong platform-scale observational evidence, low algorithmic novelty.

**What was measured.** GitHub reports that more than 40% of pull requests started with an agent in September 2026, up from 17% in March, with 110 million agent-started PRs in September. The share of agent-involved PRs merged within two weeks reportedly reached 90% in September, compared with about 86% without detected agent involvement. The annual report also identifies repositories with agent configuration files as having eight times as many commits *on average* as new repositories without them. These figures measure activity and association, not agent-caused productivity or correctness.

**Key technique:** Task-level delegation into cloud coding agents, followed by human or automated review gates. The important shift is from chat-assisted editing to PR-centric work units with observable acceptance and merge outcomes.

**Why interesting:** Unlike another model benchmark, this is real workflow telemetry at platform scale. It suggests engineering bottlenecks increasingly move toward review, test infrastructure and coordination. GitHub also reports 61% of model-selecting Copilot users chose multiple models in September, supporting model-routing as an observed practice rather than merely a design proposal.

**Practical takeaway:** For an autonomous repository maintenance agent, track PR creation-to-merge latency, review iterations, CI retries, revert rate and regression escapes, not commit volume. Compare agent-originated and human-originated changes on matched tasks.

**Limitations:** Vendor-defined agent detection, selection effects, and non-equivalent PR complexity preclude a causal claim. The report's observation window ends September 30.

```chart
{"type":"bar","title":"Agent-started share of GitHub pull requests","caption":"GitHub Octoverse 2026: platform-reported shares, March vs September 2026; observational and not causal.","labels":["March 2026","September 2026"],"datasets":[{"label":"Share (%)","data":[17,40]}],"yAxis":{"min":0,"max":100,"title":"Share of PRs (%)"}}
```

*Note: September is reported as **more than** 40%; 40 is the conservative lower bound used for the chart, not a precise estimate.*

## Knowledge-base synthesis

This entry preserves the finding as a reusable canonical reference rather than leaving it accessible only by briefing date. Compare its stated mechanism and evidence tier against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]], and the [November 3–9 cross-briefing synthesis](../evaluations/briefing-synthesis-2026-11-03-to-09.md). These are analyst-level thematic connections, not assertions that the original project cites or implements the linked concepts. Future source verification should replace this backfill with a deeper independently checked treatment while retaining this page identity.
