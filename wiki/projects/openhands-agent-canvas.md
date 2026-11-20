---
uid: 5dd00619-775e-4e40-aedd-ccde60fee7ab
title: "OpenHands Agent Canvas 1.42"
summary: "Authenticated trigger provenance and repository identity with source-grounded mechanisms and evidence limits."
type: project
created: 2026-11-20
updated: 2026-11-20
depth: full
sources:
  - https://github.com/OpenHands/OpenHands/releases/tag/v1.42.0
---

# OpenHands Agent Canvas 1.42

**Primary source:** https://github.com/OpenHands/OpenHands/releases/tag/v1.42.0. **Source date:** 2026-11-18.

## Demonstrated capability and mechanism

The release adds exact connected Git-provider selection, restores native webhook-source validation, and provides non-loopback HTTP origins for verification runs. Explicit provider resolution and webhook validation precede automation effects.

**Reusable concept:** Authenticated trigger provenance and repository identity. Incremental release, but consequential for security boundaries; no independent attack or reliability measurements.

## Boundaries and test

Simulate 20 valid/invalid webhook events against two mock providers; require correct target selection and zero unauthorized writes.

This is a proposed experiment, not an independently reproduced result. See [[briefings/2026/11/2026-11-20]] and [[concepts/verified-completion-vs-apparent-success]] for comparisons and acceptance limits.
