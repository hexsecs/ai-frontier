---
uid: 2a4066e2-4b50-4af4-81ef-70e613a444ca
title: "Baya — Securing Web Agents with Compile-Then-Execute"
summary: "Compiles web tasks into bounded Python programs before exposing agents to untrusted website content."
type: project
created: 2026-11-12
updated: 2026-11-12
depth: brief
related: [fastbrowse]
sources:
  - https://arxiv.org/abs/2611.06039
---

# Baya — Securing Web Agents with Compile-Then-Execute

**Source:** https://arxiv.org/abs/2611.06039  
**Date:** 2026-11-04  
**Evidence status:** Author-reported research; not independently replicated.

## Mechanism

Baya compiles a user's web request into Python against a Trusted Website API before seeing the live page. The compiled program can consume website data and choose among precompiled branches, but untrusted page content cannot induce fresh model-planned operations.

**Technique:** Compile-then-execute; isolate the planner from untrusted observations and constrain actions to an ahead-of-time program.

## Evidence and bounds

Across 581 valid WebArena Verified tasks, the authors report 77.8% aggregate utility versus 55.1% browser-only ReAct and 66.7% API-enabled ReAct. On WASP, they report 0% attack success versus 25.5% and 16.2% respectively. These are author-reported benchmark results, not a universal security guarantee.

## Novelty and comparison

This is a stronger structural answer to prompt injection than merely instructing the agent to ignore malicious text. Compared with November 11's LLM-as-Code, it specifically blocks live webpage text from changing model-authored control flow.

## Reproducible experiment

Build ten synthetic web tasks with injected instructions in product descriptions and comments. Compare a ReAct agent with a precompiled task-specific API program, recording legitimate-task completion, unauthorized actions and tasks requiring unexpected branching.

## Verdict

High novelty and strong quantitative evidence, bounded by the tested API coverage, websites and attack suite.

## Related

- [[briefings/2026/11/2026-11-12]] — complete dated evidence and cross-project synthesis.
- [[projects/fastbrowse]] — analyst comparison, not a demonstrated head-to-head; source URLs and limitations in the briefing.
