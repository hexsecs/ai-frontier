---
uid: b6a90605-a8d1-4d13-9a40-000000000035
title: "Browser4"
summary: "Canonical November 6 research finding: Browser4; documented mechanism, evidence limitations and next steps."
type: project
created: 2026-11-09
updated: 2026-11-09
depth: brief
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

## Cross-briefing context

For independent acceptance, regression preservation, and source limits, see [[concepts/verified-completion-vs-apparent-success]], [[concepts/preservation-aware-agent-improvement]] and [[evaluations/briefing-synthesis-2026-11-03-to-09]]. These are analytical comparisons, not direct project dependencies.
