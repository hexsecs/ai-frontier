---
uid: 9f4f43d3-ae31-4c7c-912c-fb9e97e05c11
title: "sqz context compression"
summary: "Deterministic tool-output compression and repeat references reduce coding-agent context consumption."
type: project
created: 2026-11-21
updated: 2026-11-21
depth: full
sources:
  - https://github.com/ojuschugh1/sqz
---

# sqz context compression

**Primary source:** https://github.com/ojuschugh1/sqz. **Evidence:** inspected maintainer release/README; no independent reproduction.

## Implementation
The Rust CLI and MCP integration transform command output before it reaches an agent. The maintainer describes command-specific formatters, unchanged source-code and stack-trace handling, and short references for already-seen outputs with byte-exact expansion for cached items. The repository was active November 12, 2026; this is an **older discovery**, not a newly released benchmark.

The README reports 3,003 compressions, 178,442 tokens saved and 24.7% average reduction in a developer's usage. These are maintainer-reported measurements, not independent task-success evidence; compression rates vary with output type and repetition. The source also warns that identical full-file rereads were uncommon in one external sample.

## Mechanism and bounds
Compression changes the *delivered context* without changing the underlying task. A reference is useful only if the previous content remains accessible and relevant; dropped diagnostic detail can affect downstream repairs. [[concepts/information-content-dominance]] cautions against equating fewer tokens with equal useful information; [[techniques/evaluation-and-simulation]] distinguishes token accounting from task acceptance.

## Proposed experiment
Replay 30 fixed coding traces with raw output, formatter-only compression and compression-plus-reference deduplication. Measure model-visible tokens, missing diagnostic facts, repair correctness, reference expansion failures and latency. Use identical model seeds where available.
