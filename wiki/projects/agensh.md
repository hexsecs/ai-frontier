---
uid: b6a90301-a8d1-4d13-9a40-000000000001
title: "Agensh"
summary: "Canonical evidence record for Agensh; mechanism, limitations, practical implications and source provenance from the November 3 briefing."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
sources:
  - https://github.com/microsoft/Agensh
  - https://arxiv.org/abs/2609.26781
---

# Agensh

**Origin:** [[briefings/2026/11/2026-11-03]] — finding 1. **Provenance:** This canonical record is backfilled from the archived research briefing. It is not a fresh independent source review or replication. Date and evidence limitations remain as reported in the snapshot.

## Archived evidence and assessment

**Date:** October 24, 2026 open-source release; October 29 expanded backend support. **Source:** [Microsoft Agensh repository](https://github.com/microsoft/Agensh); [paper](https://arxiv.org/abs/2609.26781). **Assessment:** High practical relevance; high infrastructure novelty; controlled benchmarks.

**What was built.** A multi-agent coding harness in which workers claim tasks, share context, message one another, check contributions, and integrate results without a single central planner. Gitea is the shared code workspace and Mattermost carries team communication. The release includes Docker Compose deployment and experiment scripts; the October 29 update adds Copilot, Codex, Claude Code, and Pi single-agent backends.

**Key technique.** Decentralized task discovery and asynchronous work claiming, backed by durable shared artifacts and peer coordination. Rather than one orchestrator routing every instruction, the coordination substrate allows team organization to emerge from worker behavior.

**Evidence.** On five difficult ProgramBench tasks with a six-hour budget and GPT-5.6-sol, the reported average final test-pass rate improved from **19.31% with one worker** to **28.78% with 128 workers** (a 9.47 percentage-point absolute increase). On Pandoc, one worker scored 33.89%, 128 workers 50.94%, and 1,024 workers 55.06%. A separate reported GPT-6.1-sol Pandoc experiment scored 56.19% with one worker versus 79.59% with 32 workers. These are task-specific, author-run results; the additional compute, coordination cost, and variance must be considered before generalizing.

```chart
{"type":"bar","title":"Agensh: Pandoc final test-pass rate under six-hour budget","caption":"Author-reported GPT-5.6-sol ProgramBench Pandoc results; worker counts differ, and inference expenditure is not normalized.","labels":["1 worker","128 workers","1,024 workers"],"datasets":[{"label":"Test-pass rate (%)","data":[33.89,50.94,55.06]}],"yAxis":{"min":0,"max":100,"title":"Test-pass rate (%)"}}
```

**Why frontier.** This tests the organizational structure of autonomous coding rather than simply prompting a larger model. It is directly relevant to a two-agent project that might eventually grow to many specialized agents.

**Practical takeaway / experiment.** Run the same bounded repository task with 1, 2, 4, and 8 workers; track acceptance-test pass rate, wall time, tokens, merge conflicts, duplicate work, and reviewer intervention. Add an atomic task-claim ledger and artifact ownership before adding more agents.

**Verdict:** Worth testing, not a claim that 1,024 workers are generally economical. Compared with [[techniques/multi-agent-orchestration]], Agensh provides an unusually concrete decentralized implementation and reproduction path.

## Knowledge-base synthesis

This entry preserves the finding as a reusable canonical reference rather than leaving it accessible only by briefing date. Compare its stated mechanism and evidence tier against [[concepts/scoped-assurance]], [[concepts/validation-tier-gap]], and the [November 3–9 cross-briefing synthesis](../evaluations/briefing-synthesis-2026-11-03-to-09.md). These are analyst-level thematic connections, not assertions that the original project cites or implements the linked concepts. Future source verification should replace this backfill with a deeper independently checked treatment while retaining this page identity.
