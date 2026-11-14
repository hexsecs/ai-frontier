---
uid: 2ca51a69-615a-4663-a329-e202645d4c1a
title: "KinoCut — Guardrailed Video-Editing MCP Tools"
summary: "Exposes local FFmpeg-based editing and repurposing operations to agents through bounded MCP tools."
type: project
created: 2026-11-12
updated: 2026-11-12
depth: brief
sources:
  - https://github.com/KyaniteLabs/kinocut
---

# KinoCut — Guardrailed Video-Editing MCP Tools

**Source:** https://github.com/KyaniteLabs/kinocut  
**Date:** 2026-11-12 (repository inspected; launch date unverified)  
**Evidence status:** Source repository inspected; release date and independent evaluation not verified.

## Mechanism

An open-source MCP server, Python client and CLI expose video editing, FFmpeg operations, subtitle work and repurposing workflows as agent-invocable operations with documented guardrails.

**Technique:** Tool-oriented creative production: an LLM plans edits while deterministic media tooling executes transforms and can be checked against file properties.

## Evidence and bounds

Public code, documentation and examples exist, but no independently validated quality, speed or cost comparison was established. Repository activity on November 12 does not establish a release date.

## Novelty and comparison

An exploration outside software-engineering research: it tests whether narrow, inspectable tools make creative work more reproducible than open-ended desktop automation.

## Reproducible experiment

Give a media agent a short rights-cleared clip and require a 30-second cut, captions and two aspect ratios. Verify durations, codec metadata, captions and absence of unintended edits before human quality review.

## Verdict

Practical domain-diversifying experiment; engineering implementation is more credible than any unverified marketing claim.

## Related

- [[briefings/2026/11/2026-11-12]] — complete dated evidence and cross-project synthesis.
