---
uid: 5215fd36-3f72-4fc9-8452-b9967999fd1c
title: SOPGuard and SOPBench
summary: Study and constrain agent-mediated cross-origin information flows in browser automation.
type: project
created: '2026-11-16'
updated: '2026-11-16'
depth: full
sources:
- https://arxiv.org/html/2606.14027
- https://github.com/wxl-lxw/BrowserOS-SOPGuard
---

# SOPGuard and SOPBench

## Mechanism and evidence

[SOPGuard](https://arxiv.org/html/2606.14027) studies an agent acting as an automated channel between browser origins. The paper introduces SOPBench and an enforcement mechanism implemented in BrowserOS. It distinguishes restrictions on page scripts from information the agent itself can read on one page and write to another.

This is an information-flow boundary, not merely a list of permitted browser tools. [[concepts/delegated-authority-and-revocation]] distinguishes action authority from allowed data movement; [[techniques/secure-agent-operations]] compares enforcement surfaces. The relation to [[projects/harness-matters-web-agent-security]] is an analyst comparison of different security questions, not a shared benchmark.

## Limits and proposed test

The paper's results are author-reported. They do not establish universal prevention of every exfiltration route or equivalent enforcement across browser harnesses. No benchmark was reproduced here.

Use local origins and synthetic canary data. Attempt benign transfers and injected transfers, and separately record leaks, blocked legitimate work and policy decisions. Test agent-mediated actions as well as script-level requests. The protocol is proposed and must not use real credentials.

## Provenance

Historical discovery: [[briefings/2026/11/2026-11-14]], where the June paper was explicitly labeled older exploratory evidence. SOPBench is described with its implementing system rather than duplicated as a second canonical record.
