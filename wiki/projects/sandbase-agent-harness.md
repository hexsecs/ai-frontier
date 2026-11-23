---
uid: 439f4fb6-4ad4-4199-aac1-deafbe05f8dd
title: "SandBase Agent Harness"
summary: "A vendor-described agent runtime with managed sessions, tools, approvals, sandboxing and replay."
type: project
created: 2026-11-23
updated: 2026-11-23
depth: full
sources:
  - https://github.com/sandbaseai
---

# SandBase Agent Harness

**Source:** https://github.com/sandbaseai. **Source date:** 2026-11-23. This is observed repository activity, not a confirmed original release date.

## Mechanism and demonstrated scope

Managed session lifecycle, sandbox execution, approval controls and replay/audit surfaces described in the project organization's documentation. The reusable boundary is [[concepts/delegated-authority-and-revocation]]; this implementation does not by itself establish that other systems share its results.

## Evidence and limits

Vendor claims; specific runtime source and release identity were not independently inspected, and 2026-11-23 is observed organization activity, not a verified release date. The described behavior should be treated as implementation documentation or author-reported findings, not independent replication.

## Proposed bounded experiment

On a sandbox test account, attempt 20 permitted and denied tool actions across resumed sessions, recording approval enforcement and replay fidelity. No experiment is reported as executed here.
