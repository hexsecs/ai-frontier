---
uid: 7cac3645-4c23-4d52-be4b-d89a0b08d31b
title: "Browsentic"
summary: "Local browser extension and agent CLI integration exposing a signed-in browser through optional MCP."
type: project
created: 2026-11-24
updated: 2026-11-25
depth: full
sources:
  - https://github.com/imshaikot/browsentic
---

# Browsentic

**Source:** https://github.com/imshaikot/browsentic. **Date:** Repository discovery November 24; release date unverified.

## Mechanism

The README describes a browser side panel driven by existing local coding-agent CLIs and optional MCP access to the same browser. This reuses an authenticated browser context rather than creating a separate browser identity. See [[techniques/secure-agent-operations]] for the related mechanism and its evaluation boundaries.

## Evidence limits

Maintainer documentation, inspected November 25; original release date and access enforcement across routes remain unverified.

## Proposed experiment

Use an isolated browser profile and 20 mock-site tasks; compare direct and MCP routes for unauthorized effects, credential exposure and task completion. Not executed.
