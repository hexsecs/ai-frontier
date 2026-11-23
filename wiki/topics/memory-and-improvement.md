---
type: index
title: "Memory and improvement"
summary: "Locate persistent capability and evaluate updates without hiding regressions."
---

# Memory and improvement

What persists between tasks, how is it updated, and which previous capabilities survive?

## Start here

The retention section of [[techniques/agent-skills-and-memory]] distinguishes recall from forbidden recall. [[projects/framerslab-agentos]] supplies one documented forgetting implementation; [[experiments/lifecycle-authority-and-retention]] tests restoration without claiming a measured privacy guarantee.

1. [[techniques/agent-skills-and-memory]] — Compare stored procedures, query-time history and learned file operations.
2. [[concepts/capability-locus]] — Separate contributions from weights, harness and external state.
3. [[concepts/preservation-aware-agent-improvement]] — Count lost as well as newly solved cases.
4. [[techniques/gated-admission-and-revalidation]] — Decide what may enter a reusable store.

## Compare mechanisms

| Mechanism | Reading | Question to ask |
|---|---|---|
| Preserve and retrieve history | [[projects/just-in-time-agent-memory]] | Can the answer be traced to the original record? |
| Consolidate persistent memory | [[projects/tigerless-agent-memory]] | Does consolidation preserve useful evidence? |
| Compile reusable operations | [[projects/skillcompiler]] | Are invocation conditions and validation records still applicable? |
| Update external knowledge | [[projects/karma]] | Does improvement transfer safely across domains? |
| Learn memory operations | [[projects/coding-agent-memory-post-training-ii]] | How much comes from training the policy rather than storing more text? |

## Counterevidence and tests

[[projects/security-impact-of-coding-agent-memory-files]] bounds claims that stored text reliably changes behavior. [[techniques/agent-skills-and-memory]] discusses negative transfer and missing gate ablations. Compare the two explicitly different ingestion protocols in [[experiments/index]]; both are proposed, not measured outcomes. See [[topics/verification-and-evaluation]] for acceptance criteria.


## When forgetting must survive old backups

[[projects/linera]] studies encrypted lineage keys that make derived memory unreadable after a source key is punctured, even when an attacker obtains old ciphertext and current keys ([primary paper](https://arxiv.org/abs/2611.18133)). Unlike [[projects/framerslab-agentos]]'s documented tombstone and deletion mechanism, this is a cryptographic erasure construction with an explicit threat model and a collateral-forgetting tradeoff. See [[techniques/agent-skills-and-memory]] for the fan-in effect and its evidence limits.

## Environment-shifted skills and self-improving harnesses

[[projects/when-agent-skills-go-stale]] shows why previously successful reusable procedures need current-environment replay checks and selective repair; [[techniques/agent-skills-and-memory]] distinguishes admission from later invalidation. [[projects/elite-evaluation-free-self-improvement]] integrates compatible harness mechanisms without downstream candidate scoring, while [[projects/values-shape-self-improving-coding-agents]] demonstrates that persistent value statements influence the optimization path. [[concepts/preservation-aware-agent-improvement]] requires independent regression accounting for both mechanisms.


[[projects/coding-agent-working-memory-evaluation]] compares object-aware compression and retrieval, finding that nominally equal token budgets do not ensure equal delivered context or task outcomes. See [[techniques/agent-skills-and-memory]] for the evidence and held-out evaluation boundary.
