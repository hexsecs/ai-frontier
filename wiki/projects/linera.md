---
uid: be3c76b3-d258-400b-85d4-20a6a2054bc8
title: "LinEra — Cryptographic erasure across agent-memory lineage"
summary: "Cryptographic erasure versus logical forgetting: Derive memory encryption keys from the keys of all input memories."
type: project
created: 2026-11-17
updated: 2026-11-17
depth: full
sources:
  - https://arxiv.org/abs/2611.18133
---

# LinEra — Cryptographic erasure across agent-memory lineage

**Primary study:** [https://arxiv.org/abs/2611.18133](https://arxiv.org/abs/2611.18133), 2026-11-13. This is an author-reported research implementation; no independent replication is claimed.

## Mechanism and boundary

Derive memory encryption keys from the keys of all input memories; puncture a source key in a pseudorandom-function tree so dependent summaries, embeddings and backups become unreadable. The reusable distinction is **cryptographic erasure versus logical forgetting**. [[techniques/agent-skills-and-memory]] and [[concepts/delegated-authority-and-revocation]] explain the neighboring mechanism and its limits; similarity of vocabulary does not imply identical architecture.

## Evidence and novelty

In the paper's largest-writer ten-conversation LoCoMo experiment, attacker recovery was 70/71 secrets after logical deletion, 67/71 with per-object/epoch keys, and 0/71 with LinEra. Forgetting 1% of turns made 73.0% of session-summary derivatives unreadable versus 3.8% with four-turn windows.

Adds a cryptographic security boundary to memory lineage, not just a tombstone or deletion API. Exposes a measurable privacy/utility tradeoff determined by summarizer fan-in. **Boundary:** Author-reported prototype and threat model; lineage completeness depends on recording everything the writer saw, protecting current keys and not leaking plaintext through other channels.

## Practical engineering test

On synthetic secrets in a local memory store, compare logical deletion, per-object encryption and lineage-key puncturing after snapshot restore; measure secret recovery, collateral memory loss and query quality.

**Engineering implication:** Treat derived memory as a dependency graph and keep summarization fan-in narrow; verify backup restoration under an attacker-with-storage-and-current-keys model.
