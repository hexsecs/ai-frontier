---
uid: 48bc81ce-4e5b-4e21-8f7b-261114000001
title: AlphaProof Code
summary: Multi-agent Lean proof generation for selected Signal libsignal machine-code security properties.
type: project
created: 2026-11-14
updated: 2026-11-14
depth: full
sources:
  - https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf
---

# AlphaProof Code

Google DeepMind describes a human-guided agent that prepares approved Lean specifications and autonomous prover agents that generate kernel-checked proofs of selected AArch64 `libsignal` properties. The November 10, 2026 paper reports approximately 6.5 million lines of checked proof code based on 26,000 lines of trusted specification and semantics. This is author-reported scope, not independent replication.

The separation between specification approval and autonomous proof search makes the proof kernel an independent acceptance boundary. It implements a concrete instance of [[projects/spec-first-verification-agents|spec-first verification]] at machine-code level. The reported coverage includes PQXDH and Triple Ratchet properties, not every Signal component or all possible security threats.

**Experiment:** Pin a small embedded cryptographic routine and formally specify one invariant; evaluate generated proofs with a trusted checker and track specification changes separately from proof generation.

Source: https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf
