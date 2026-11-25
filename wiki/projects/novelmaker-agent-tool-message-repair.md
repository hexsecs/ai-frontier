---
uid: 8f5b34ba-4d87-4271-a3de-0c8b7f57f378
title: "NovelMaker 1.7.0 Agent Message Repair"
summary: "A writing-agent release repairs dangling tool-call histories and confines project-file access."
type: project
created: 2026-11-23
updated: 2026-11-23
depth: full
sources:
  - https://github.com/wg-1337/NovelMaker/releases
---

# NovelMaker 1.7.0 Agent Message Repair

**Source:** https://github.com/wg-1337/NovelMaker/releases. **Source date:** 2026-10-11. 

## Mechanism and demonstrated scope

Sanitize outgoing request message sequences without destructively rewriting stored history; clean incomplete tool-call chains after interruption and normalize project-file paths. The reusable boundary is [[concepts/replay-idempotency-and-effect-semantics]]; this implementation does not by itself establish that other systems share its results.

## Evidence and limits

Maintainer release notes; repository archived November 22, 2026; no independent adversarial testing or reliability benchmark. The described behavior should be treated as implementation documentation or author-reported findings, not independent replication.

## Proposed bounded experiment

Generate 30 malformed tool-call transcripts and 20 traversal attempts in a disposable project; compare preserved disk history, API acceptance and out-of-root access. No experiment is reported as executed here.
