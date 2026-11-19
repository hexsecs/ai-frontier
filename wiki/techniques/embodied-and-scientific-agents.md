---
uid: 1a836d84-71ba-4bc5-aedd-7caab288dda9
depth: deep
title: "Closed-loop instrument and simulation execution"
summary: "Agents acting on instruments and physical systems, where feedback arrives as measurement, actions carry real cost, and evidence tiers bound every claim."
type: technique
created: 2026-11-02
updated: 2026-11-19
related: [projects/auctopus, projects/hera, projects/bioagent, projects/molrsi, projects/tinyastral, concepts/validation-tier-gap, concepts/capability-locus, concepts/improvement-lives-in-external-state]
sources:
  - url: https://arxiv.org/abs/2610.40589
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39074
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.41383
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39714
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.41216
    retrieved: 2026-11-02
  - https://arxiv.org/abs/2611.19081
  - https://arxiv.org/abs/2611.21099
---

# Closed-loop instrument and simulation execution

## What it is

This technique concerns the observe–act–measure loop, including instrument feedback, execution constraints and the boundary between simulated and physical validation. Use [[domains/scientific-and-embodied]] to browse the application area. The comparison is architectural; it does not imply one shared implementation or transferable performance.

Embodied and scientific agents act through instruments, robots or computational research environments. Their shared engineering pressures include costly actions, measurement feedback, provenance and explicit validation boundaries.

The systems below do not share one implementation. [[projects/auctopus]] and [[projects/hera]] report instrument experiments; [[projects/bioagent]] reports physical robot runs; [[projects/molrsi]] combines computational search with wet-lab endpoints; [[projects/tinyastral]] reports quantitative simulation results and qualitative physical demonstrations. [[projects/garden]] is a comparison involving reward engineering for simulated reinforcement-learning policies.

## Mechanism variants

**Precommitted measurement campaigns on real instruments (Auctopus).** Six roles — proposers, a principal investigator, a computational researcher, an experimentalist, a manager, independent reviewers — plus a safety agent configured by humans with preset operating limits whose approval was required before experimentation. Generation and assessment are separated across agents holding distinct contexts; fresh reviewers saw only the manuscript. Predictions and acceptance criteria were committed to before results were judged, with three verdicts available — support, contradiction, or inconclusive. Raw photon counts never left the instrument computer: the PI and computational researcher judged measurements from the experimentalist's laboratory reports, so even inside the system, feedback travelled as reported measurement.

**Corpus-carried measurement practice (HERA).** The agent runs cryogenic transport measurements on quantum devices, writing code into live notebooks that drive the rig. What distinguishes it is the corpus it reads: 29 recipes, worked examples, forward models, and literature, governed by rules of evidence — every conclusion carries a confidence level from a fixed five-level vocabulary, and load-bearing claims must cite their source and its kind. Autonomy is graded (E0/E1) and gated by a read-only state check; the safety cell writes the device card's limits onto the instruments, so an out-of-range setting errors before hardware moves. After each session, a review agent proposes corpus revisions, which the operator accepts or rejects — the corpus is where the system improves.

**Audit-then-teach skill acquisition (BioAgent).** A dual-arm robot executes wet-lab protocols it has never run. An Analyzer derives ordered operation–object–outcome requirements (human-reviewed); a Planner matches them against a library of validated atomic skills; unmatched requirements become capability gaps, and only the gaps are closed — by choosing an implementation backend (a fine-tuned vision-language-action policy, reviewed trajectory replay, or direct instrument command) and requesting human teaching only where the tool-experience record says the unaided tool is unreliable. A candidate skill must reach 60% success in learning-stage trials and pass sequential package validation before joining the library. Acquisition happens in a learning stage that precedes evaluation: during evaluation the library is frozen, a Monitor checks preconditions before each operation and outcomes after it, recovery retries or restores preconditions from validated skills — and if recovery would need a capability the library lacks, the run terminates.

**Computational search with physical endpoints (MoLRSI).** An LLM agent searches over combinations of existing models, methods, and settings — the workflows that predict activity or rank binders — guided by a three-store memory (solution, refinement, execution) around a frozen backbone model. The loop's feedback is entirely computational development scores. The physical tier enters only at the end: the developed workflows are run prospectively in a wet lab (an antibiotic screen; a phage-display selection). Experimental outcomes do not feed back into the search — as the authors themselves note.

**Harness evolution in simulation (TinyAstral).** A frozen 180B teacher planner acts through a harness that owns perception, geometry, collision-free motion planning, and tool returns — tools "report what they measured rather than what they intended," and unmeasurable checks return unknown rather than a pass. Master agents propose harness edits against observed failure classes, accepted only through a pre-registered paired statistical gate. The final harness is then frozen and a small student distilled inside it. Every quantitative result is simulation; the physical arm appears only in qualitative trajectory figures.

**Reward-program engineering over a training process (GARDEN comparison).** An LLM reward engineer with shell access to environment and learner source code, training curves, and trajectories writes executable reward programs, tests them through bounded learning probes, and a fixed mechanical rule freezes and hashes one program for unchanged transfer to held-out scenarios. The system acted on is a learning process; its feedback is training metrics — measurement of a simulated process, which distinguishes it from physical experimental feedback.

## Co-evolving recovery code and learned control

[[projects/robocoevo]] ([November 14 study](https://arxiv.org/abs/2611.19081)) couples two capability loci: a multimodal agent writes executable failure detectors and recovery programs for failed robot-policy rollouts, then the corrected trajectories become training data for a vision-language-action policy. The updated policy's changed failure distribution determines which detectors and programs the agent revises next. Unlike [[projects/tinyastral]], which evolves a harness around a frozen policy before distilling a student, this loop repeatedly changes both recovery code and policy parameters. The relation is an architectural contrast, not a measured head-to-head result.

The authors report sustained task-success gains on BEHAVIOR-1K, RoboCasa and RoboTwin, all simulation benchmarks in the cited evaluation. That is stronger than an untested proposal but does not establish safe physical deployment. An important failure mode is moving-target validation: a detector calibrated to one policy may become stale after retraining, while an improvement on previously failed states can regress other tasks. Hold out evaluation seeds and preserve previous-policy success cases; compare frozen policy, script-only recovery and iterative script-plus-policy updates with identical simulation budgets. No such independent comparison is performed here.

## Evidence and measured effects

All results below are **author-reported**; none has an independent replication. They are ordered by evidence tier, because the tier is the point.

**Prospective physical tier.** Auctopus's revised acquisition collected 21,600 one-second records and passed all ten precommitted accuracy criteria and all controls: the target contrast was S = (40.0 ± 0.4)×10⁻³ against the locked prediction P = (39.7 ± 1.3)×10⁻³, where both interpolation baselines predicted exactly 0. BioAgent, over 50 runs per task per condition, achieved complete-task success of 66% (Task 1) and 58% (Task 2) with validity-aware recovery, against 54% and 40% with recovery disabled — worth +12 and +18 points. Its reuse economics are the domain's clearest cost result: Task 1 required 26 teaching requests and 360 human minutes; Task 2, built mostly by reuse (17 of 24 skill types carried over unchanged), required 9 requests and 114 minutes. MoLRSI's prospective antibiotic screen found 17 hits among 107 tested compounds, a 15.9% hit rate against 8.7% in the authors' previous expert-driven study — a cross-study comparison, not a controlled head-to-head — and its pMHC designs produced eight phage-display enrichment hits across two targets where the comparison agent and a no-ranking control produced none.

**Blinded-agreement tier.** HERA matched the expert's sealed conclusion on both trial devices, in stacking order and confidence level, with zero pre-conclusion interventions on one device and one — a safety concern HERA itself raised — on the other. The endpoint is agreement with a single expert on two devices — the paper itself states "the protocol reports this agreement rather than accuracy." HERA's corpus ablation is the strongest locus measurement here: with the corpus removed, verdict grades fell from 1.00 to 0.40 for both models and one model concluded a flatly wrong stacking order, while *decision* grades — what to measure and how — stayed high (0.71–0.96) in every session. The corpus changed inference quality, not measurement selection.

**Offline and simulation tiers.** HERA's replay study — 300 offline replays in which the fan is designed but never measured — found a pooled +0.43 P(call) gain from the full corpus: real evidence, at the design tier. TinyAstral's simulation results are the locus decomposition [[concepts/capability-locus]] rests on: harness evolution alone moved the frozen teacher from 33.4% to 63.6% strict success on RoboTwin; the same harness lifted a planner it was never evolved around by +30.6 points; distillation added +21.6 points within the final harness; and removing the teacher's reasoning text cost up to −19.3 points. GARDEN's frozen reward program transferred unchanged to held-out scenarios (+58.2% and +52.5% relative return in Overcooked; SMAX win rates 27.3% → 96.1% and 74.6% → 83.6%) — at the simulation tier throughout.

**Cross-cutting effect.** In every system here that ran the ablation, the gain lived in external state — HERA's corpus, BioAgent's skill library, TinyAstral's harness, MoLRSI's memory stores — with the model's weights frozen or incidental. That is [[concepts/improvement-lives-in-external-state]], and this domain supplies some of its strongest exhibits: physical settings force the artifact — a protocol, a library, a harness — to exist before the run starts.

## Failure modes and bounds

**Tier slippage is the characteristic failure.** TinyAstral is [[concepts/validation-tier-gap]]'s purest instance: robotics framing, every number simulated, physical evidence qualitative only — and its one physical-world metric (0.923 next-call accuracy) is an offline score that collapses to 0.235 without real-robot training data, which says nothing about closed-loop physical success. MoLRSI's bound is subtler: its wet-lab results validate the workflows it produced, not the self-improvement loop, whose evidence is computational ablation only (an enrichment factor going from 0.00 to 3.65 when memory is enabled). Citing either page at its framing tier overstates what was measured.

**Measurement feedback has its own pathologies.** Auctopus's first run met all ten accuracy criteria and was still rejected as inconclusive, because the global-phase and reference-pulse controls failed: the signal had drifted (a 7.6% rise over the morning and a 2.9% step the experimentalist attributed to room lights being switched on), and two controller programs sampling at different times turned drift into systematic offset. The fix kept the criteria and changed the acquisition. HERA shows the corpus-gap version: every tetralayer session initially misread a known physical feature (paired charge-neutrality resistance peaks) that no recipe covered, and in the transfer study HERA concluded, wrongly, that a device did not superconduct because it had surveyed too narrow a range — one operator message pointing at the unexhausted gate range fixed it, and the durable fix was a new corpus rule. Feedback as measurement fails by drift, by coverage gaps, and by unmodelled features, not by hallucinated text.

**Comparator construction bounds the head-to-head numbers.** BioAgent's atomic-skill advantage (96.9% average against 41.2–54.4% for three baselines) was measured on the skills BioAgent was purpose-taught, on its own platform, against the authors' own adaptations of the baselines — ports, not the original systems; and no baseline completes either full task, so the task-level numbers have no external reference point at all. GARDEN's margin over its controls is confounded by compute (155 LLM calls and 15.0M input tokens against 18 calls and ~3.5M for each control, never compute-matched). MoLRSI's headline hit-rate comparison is cross-study with differently constructed denominators and no hypothesis test.

**Self-grading is pervasive and only partly mitigated.** Auctopus's acceptance criteria were set and graded by agents of the same system, its "independence" is fresh conversations within one framework, and its prediction lock for the final run occurred after data collection (before any target mean was computed) — analysis-order discipline, weaker than pre-registration. MoLRSI's generation search optimized against its own learned ranking score; its mitigations (cross-scoring under a competitor's metric, the prospective screen, a no-ranking control arm) are the reason its physical hits still count. HERA's sealed conclusions, corpus, and grading all trace to the same laboratory and largely the same expert.

**Scale and human presence.** Every physical result here is one laboratory, one platform, one or two devices or protocols, at small n (66% at n = 50 spans roughly the low 50s to high 70s). None of these systems is human-free: humans assembled Auctopus's apparatus and set its safety limits, authored HERA's corpus and caught its false negative, reviewed BioAgent's requirements and supplied 360 minutes of teaching for its first protocol, and remain the accept/reject authority over HERA's self-improvement loop. The honest summary of the domain's autonomy claims is that the human moves — to apparatus, corpus, teaching, and adjudication — rather than disappears.

## Open questions

- **Replication.** No physical-tier result on this page has an independent replication. Which of them survives a second laboratory, a second platform, a second expert?
- **The locus question, factorially.** [[concepts/capability-locus]] records HERA (artifact-dominant) against AgenticDS (model-dominant) with neither testing the other's system. Does corpus quality × backbone strength, run factorially in a physical setting, decompose the way TinyAstral's simulation decomposition does?
- **Closing the loop with physical outcomes.** MoLRSI's authors note that experimental outcomes do not yet feed its policy updates. Does a loop that learns from wet-lab successes and failures outperform one fed only on computational scores — and at what cost per unit of physical feedback?
- **Teaching economics.** BioAgent's teaching cost fell roughly threefold from the first protocol to the second. Does that ratio hold across protocol families and platforms, or is it an artifact of two similar protocols on one robot?
- **Tier discipline as method.** The disciplined pages here (HERA's sealed protocol, BioAgent's learning/evaluation separation, Auctopus's unrelaxed criteria) suggest a transferable assessment template for physical agents. Whether adopting it changes results — or only their credibility — is unmeasured.

## Evidence status

Measurements are attributed to their authors or vendors at the point of use. The cross-project comparisons are analyst interpretations, not new experiments or evidence of a shared implementation. No independent replication is cited.

## Fast contact control below slow model planning

[[projects/forceharness]] ([November 16 paper](https://arxiv.org/abs/2611.21099)) makes a different intervention from policy learning: an API-only frozen multimodal model receives force-aware tools whose inner loop regulates contact locally and terminates at an observable event. A physics translation layer converts measured force traces into physical quantities with uncertainty, rather than asking the model to infer mechanics from a raw high-rate stream. The authors report real-arm success increasing from 3.3% to 90.0% in their tested zero-shot setting and simulation gains of 17.5 and 34.3 percentage points on ForceBench and HiddenPhys.

This distinguishes **controller time scale** from **planner time scale**. The model selects a bounded action; the local controller handles fast contact regulation and returns a measured outcome. Compared with [[projects/robocoevo]], which updates both external recovery programs and learned policy weights in simulation, ForceHarness keeps model weights frozen and reports a physical-arm test. The evidence tiers and tasks differ, so the comparison establishes a mechanism distinction rather than a superior general robotics result.

The calibration and local force limits are part of the trusted control boundary. A self-terminating primitive can still terminate on a misinterpreted contact event, and an accurate physical summary does not establish global task safety. Compare raw telemetry, physical summaries and locally regulated primitives under identical held-out contact conditions, logging force-limit violations, uncertainty calibration, latency and task completion. No combined experiment is reported.

