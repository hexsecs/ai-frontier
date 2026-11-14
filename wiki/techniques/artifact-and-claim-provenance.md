---
uid: f02fee3a-f844-4f63-8b73-216da09ff08f
title: "Artifact and claim provenance"
summary: "Trace artifacts and reported claims to prompts, tool outputs and executed checks while keeping provenance distinct from correctness."
type: technique
created: 2026-11-14
updated: 2026-11-14
depth: full
sources:
  - https://arxiv.org/html/2611.09395v1
  - https://arxiv.org/html/2611.05251v1
---

# Artifact and claim provenance

## Mechanism and comparison

Provenance records how an artifact or reported claim came to exist. Different mechanisms preserve different portions of that chain; capturing an origin is not the same as validating the result.

| Mechanism | Evidence record | What it preserves |
|---|---|---|
| Source-line attribution | [[projects/tracybot]] | Tasklets associate planning/build prompts with agent-generated code changes; a Tasklet can be exported as a decision record. |
| Scientific report admission | [[projects/auto-research]] | Report validation checks required fields, cited figure existence and output hashes. Reported numbers must occur in an accepted toolkit output or request, or have a stated location in a cited paper. |

Sources: [Tracybot, abstract and architecture](https://arxiv.org/html/2611.09395v1); [auto_research, section 3.1](https://arxiv.org/html/2611.05251v1). The table is an analyst comparison of distinct mechanisms, not a head-to-head evaluation.

## A useful evidence chain

For an auditable result, preserve the requirement or request, the relevant input snapshot, the action/tool invocation, the resulting artifact identity, the claim made about it, and the check that actually ran. Record versions or hashes where later changes would alter interpretation. This chain is a proposed engineering composition of the two designs, not a system evaluated by either study.

Trace capture, artifact identity and claim support answer different questions. A line-to-prompt mapping explains an origin; it does not show that the prompt was correct. An output hash establishes identity relative to recorded bytes; it does not establish scientific validity. A validator-execution receipt establishes that a check ran; the check's adequacy remains a separate question.

## Limits and counterevidence

auto_research explicitly does not check paper-sourced numbers against extracted paper text. Its provenance rule therefore retains an evidentiary gap for that admission route. Tracybot's attribution mechanism does not establish correctness of the attributed code. These limits motivate [[concepts/scoped-assurance]] and [[concepts/ground-truth-fallibility]], rather than a universal claim that complete provenance yields true conclusions.

[[projects/cheme-as-code]] provides further reading on engineering artifacts, while [[projects/procgrep]] concerns behavioral procedure fingerprints. A fingerprint is not automatically a complete causal lineage record. [[projects/just-in-time-agent-memory]] addresses retrieving relevant historical evidence after capture.

## Proposed experiment

Audit 50 claims or changed code spans from fixed tasks. Require a request/input snapshot, originating action, artifact identity, source span where relevant, executed checker identity and final verdict. Inject missing traces, mismatched output hashes, unsupported citations and skipped checks. Score provenance completeness separately from factual or functional correctness. Blind the auditor to the treatment and report false acceptance as well as missing evidence. This is a proposed test; no audit result is asserted.

## Evidence status and reading path

The two primary papers were read on November 14, 2026. The comparison introduces no new performance result or independent replication. Continue through [[topics/verification-and-evaluation]] and [[techniques/verification-and-evidence]].
