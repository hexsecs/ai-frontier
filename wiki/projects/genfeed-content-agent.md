---
uid: b9913950-beb7-4dc6-9a11-9500cf58b185
title: "Genfeed Content Agent"
summary: "Self-hostable content automation with MCP, background queues and human approval before publishing."
type: project
created: 2026-11-23
updated: 2026-11-23
depth: full
sources:
  - https://github.com/genfeedai/genfeed.ai
---

# Genfeed Content Agent

**Source:** https://github.com/genfeedai/genfeed.ai. **Source date:** 2026-11-23. This is observed repository activity, not a confirmed original release date.

## Mechanism and demonstrated scope

MCP tools and REST/CLI interfaces submit drafts into Redis/BullMQ-backed workflows; the documented standard preset requires human approval for publication. The reusable boundary is [[concepts/delegated-authority-and-revocation]]; this implementation does not by itself establish that other systems share its results.

## Evidence and limits

Maintainer documentation and seeded demonstration; no independent proof that all alternate publishing paths enforce approval. Date is observed repository activity, not initial publication. The described behavior should be treated as implementation documentation or author-reported findings, not independent replication.

## Proposed bounded experiment

Use a disposable account to create ten drafts, test approval and denial through UI/MCP/REST, and verify no unauthorized posts appear at a mock destination. No experiment is reported as executed here.
