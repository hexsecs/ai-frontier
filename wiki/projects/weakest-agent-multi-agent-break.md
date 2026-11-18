---
uid: b9a7c1d2-4e61-4b0d-9e31-4b7e2d930118
title: "Only as Safe as the Weakest Agent"
summary: "Trust-boundary collapse across delegated readers: A stronger orchestrator delegates file retrieval to a cheaper reader; forge"
type: case-study
created: 2026-11-18
updated: 2026-11-18
depth: full
sources:
  - https://arxiv.org/abs/2611.17520
---

# Only as Safe as the Weakest Agent

**Primary source:** https://arxiv.org/abs/2611.17520 (published 2026-11-12). Engineering finding; evidence is author-reported unless otherwise noted.

## Implementation and general mechanism

Unmodified Claude Code, Codex and a reference harness were tested with planted forged records in a file store. Strong orchestrators reading directly made almost no harmful revisions in over 1,000 trials; delegated reading produced failures of 20/180, 44/180, 75/180 and 553/900 in different configurations. In a separate simulated delivery test, aggregators repeated a corrupted subagent error in 751/757 trials.

The general concept is **trust-boundary collapse across delegated readers**. A stronger orchestrator delegates file retrieval to a cheaper reader; forged disk records influence the reader, and the orchestrator propagates the corrupted result.

## Novelty and evidence boundary

A controlled change in who reads untrusted data reveals a system-level failure invisible in a strong-model-only safety evaluation. All figures are author-reported and configuration-specific, not general failure rates. The simulated delivery test is not a production deployment.

The failure mechanism bears on [[concepts/delegated-authority-and-revocation]] and [[techniques/multi-agent-orchestration]]: permission delegation and information trust are different boundaries.

## Practical implication and proposed test

Do not treat a high-capability orchestrator as a sanitizer for weaker worker output; verify evidence provenance and important facts at the integration boundary.

**Proposed, unexecuted:** Create 20 synthetic file-store queries with five forged records; compare direct orchestrator reading, weaker-worker reading, and worker reading with independent source verification. Count false assertions and harmful file edits; prohibit external writes.
