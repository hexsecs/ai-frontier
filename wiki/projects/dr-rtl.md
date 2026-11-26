---
uid: 73f18c20-423b-4b9f-8c20-000000000002
title: "Dr. RTL"
summary: "Tool-grounded hardware optimization."
type: project
created: 2026-11-25
updated: 2026-11-26
depth: brief
sources:
  - https://arxiv.org/abs/2611.13713v1
---

# Dr. RTL

November 10, 2026 preprint. [Primary source](https://arxiv.org/abs/2611.13713v1).

## Mechanism and evidence

Agents analyze timing paths, rewrite RTL and evaluate implementation results while retaining reusable skills. Authors report mean WNS/TNS improvements of 21%/17% and area reduction of 6% across twenty designs relative to commercial synthesis.

## Limits

Timing and functional criteria do not establish side-channel or fault resistance. Section 4.4 and Table 2 report a separate eight-design synthesis experiment. The authors report 10.6% lower mean area and 9.1% lower mean delay than agent-tuned Yosys+ABC in that experiment. Results are author-reported; no independent replication is cited.

## Proposed experiment

Compare RTL changes under area, timing, equivalence and separate security tests. See [[concepts/verified-completion-vs-apparent-success]] for the distinction between observed checks and task acceptance.
