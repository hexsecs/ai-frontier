---
uid: b6a90605-a8d1-4d13-9a40-000000000035
title: "Browser4"
summary: "Canonical November 6 research finding: Browser4; documented mechanism, evidence limitations and next steps."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: full
sources:
  - https://github.com/platonai/browser4
---

# Browser4

**Origin:** [[briefings/2026/11/2026-11-06]] — finding 5. This is a canonical backfill of the briefing's sourced assessment, not a new independent review or replication.

## Archived evidence and assessment

**Date:** Repository inspected November 6, 2026; launch date not verified. **Source:** [Primary source](https://github.com/platonai/browser4). **Category:** Exploration / infrastructure.

**What was built or demonstrated:** An open-source browser engine exposing CDP-native browser automation via CLI and MCP, interactive element snapshots, batch actions, deterministic X-SQL/CSS extraction, crawl jobs, reusable selector experience, and a programming-agent tool kernel.

**Agentic technique:** Hybridize expensive model-guided navigation with deterministic selectors and reusable browser knowledge, keeping stateful browser sessions available to agents.

**Evidence and limitations:** The README documents the CLI, MCP, snapshot and extraction interfaces, and claims 100k–200k complex page visits per machine per day. This throughput is a project claim, not independently benchmarked here. The repository was not executed.

**Why this matters / comparison:** More operationally interesting than another chat-driven browser: its zero-token extraction and experience-store pattern could reduce repeated perception calls. Compared with November 4's macOS VM computer-use work, this optimizes the browser interface rather than environment isolation.

**Practical takeaway:** Benchmark browser4 against Playwright on 20 recurring source-ingestion tasks, measuring successful extraction, tokens, selector breakage, network safety, and recovery after DOM changes.

**Verdict:** Promising concrete infrastructure, but launch date and performance claims require verification.

## Mechanism and system boundary

Browser agent execution and interaction span perception, tool authority, navigation state and observable task effects. The historical report above supplies source-reported evidence; the following is analytical synthesis, not independent source inspection.

## Critical evidence and counterexamples

Dynamic content, UI drift, session persistence and hidden effects can invalidate replay or produce misleading success. Browser actions are not equivalent to independently verified target state. Require a frozen task definition and external acceptance checks.

## Comparative synthesis

Compare [[domains/computer-and-device-use]], [[projects/weavebench]], and [[concepts/verified-completion-vs-apparent-success]]. These are analyst comparisons, not direct dependencies. A browser-only success measure may miss terminal and filesystem failures.

## Proposed experiment

Replay 20 stateful browser tasks from controlled snapshots. Measure success, wrong-side-effect rate, trace coverage, state drift, tokens, time and recoverability after interruptions. Keep a non-agent baseline and held-out tasks; do not claim the experiment was run.

## Provenance and deployment

Full analytical treatment of the archived briefing, not independently reproduced research. Use sandboxed browser sessions and least-privilege credentials.
