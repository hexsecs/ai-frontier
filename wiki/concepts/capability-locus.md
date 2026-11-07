---
uid: a71e85c9-126e-4580-a88e-d26333d0357f
created: 2026-11-02
updated: 2026-11-07
type: concept
depth: full
title: "Capability locus"
summary: "When an agent system improves, where does capability live — weights, harness, external state, or their interaction? One system now measures the decomposition."
related: [hera, agenticds, garden, tinyastral, dittany, strategist]
sources:
  - url: https://arxiv.org/abs/2610.41216
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39074
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39608
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.42144
    retrieved: 2026-11-02
---

# Capability locus

## What it is

The locus question: when an agent system performs well, where does the
capability live — in the model's weights, in the harness or scaffold
around it, in the external state it reads and writes, or in the
interaction between them? The question is answerable only by ablation:
hold one side fixed, vary the other, and watch what the quality follows.
A claim that never runs that ablation is under-specified — "the system
works" does not say what is doing the work.

This entry was deferred in mining pass 1, deliberately. Two deepened
pages answer the question in opposite directions, and pass 1 refused to
pick a winner. [[projects/hera]] ablates its curated corpus and finds
the artifact dominant; [[projects/agenticds]] holds its scaffold fixed,
swaps the backbone, and finds the model dominant at the critical
component. Neither page tests the other's system, so the disagreement
is genuine. A third page, [[projects/garden]], never separates its
method's contribution from its engineer model's capability at all —
the question gone unasked.

Pass 2 promotes the entry in a changed form: not a phenomenon with a
verdict, but a *measured-decomposition* entry. What changed is that one
corpus system now measures both loci inside a single system and
reports the split ([[projects/tinyastral]]), and a second cluster
supplies another half-measurement ([[projects/dittany]]). The concept
is the question, plus the discipline of decomposing it per system —
and the corpus's record of how rarely that is done. Pass 2 also
lengthened the list of candidate loci: alongside weights, harness, and
external state, the newer pages add an interaction term and a
behavioral-policy term — the propensity to verify — that is neither
weights-as-capability nor artifact content.

## Evidence for

**The decomposition, measured once.** TinyAstral evolves a robot
manipulation harness around frozen models, then distills the result
into small students — and, unusually, ablates each side with the other
held fixed:

- *Harness, isolated.* The untrained Qwen3.5-4B initialization gains
  +26.6 pp "from the harness alone" (14.6% → 41.2%) with its weights
  untouched. A planner the harness was never evolved around gains
  +30.6 pp from it, so the harness contribution is not fitted to one
  model's quirks. In the teacher loop, the identical frozen model
  moves 33.4% → 63.6% by harness change alone.
- *Weights, isolated.* Within the final harness, distillation adds
  +21.6 pp over the untrained 4B initialization (62.8% vs. 41.2%).
  The weights term is real, and separately priced.
- *The harness stays load-bearing.* Distillation does not retire the
  harness: the student runs inside the final harness, so the deployed
  system's quality is a combination of both terms and their
  interaction, not a transfer of the harness's gains into weights.
- *The interaction term.* The 0.8B student nearly matches the 4B on
  RoboTwin (61.8% vs. 62.8%) and Guava (93.8% vs. 93.6%) but falls to
  54.7% on LIBERO-PRO against the 4B's 78.3% — in the paper's words,
  "the effect of model size is therefore most pronounced on
  LIBERO-PRO." Model size bites only where the task demands it; on
  the other benchmarks the harness carries the quality almost
  regardless of student size.

**Half-measurements elsewhere.** Dittany decomposes its scaffold's
contribution precisely — action scope alone is −5.47 pp; graph scope
adds +32.21 pp over action-only — while the model locus goes entirely
unmeasured: "Nothing in the paper shows the gains transfer to other
backbones." That is GARDEN's support-by-absence repeated in a second
cluster: one side priced, the other assumed.

**The original instances.** HERA: "removing the corpus dropped
verdict grades from 1.00 to 0.40 and produced a flatly wrong
conclusion," while decision quality barely moved — the intervention
that mattered was context, not the model. AgenticDS, scaffold fixed:
"a weaker backbone (GLM-4-9B) drops the full system to 0.4706, level
with plain BM25," and "a frontier-scale Critic is a prerequisite, not
an optimization." GARDEN: "Nothing separates the method's contribution
from the engineer model's capability."

**The widening.** Four more pages each isolate a different slice of
the question. [[projects/prefix-executability]] shows a factorial
pattern: architecture moves prefix reliability enormously within one
model (TER 0.47 → 0.94), yet "the gap widens under weaker models" —
neither side alone carries the effect; the interaction does.
[[projects/angler]] varies the backbone under a fixed scaffold and
gets a clean model-side effect (9.7%–41.2% attack success across
backbones), with the scaffold's share unmeasured by design.
[[projects/bioagent]] is a scaffold-side claim around a conventional
policy: "What BioAgent adds is the layer around the policy" —
requirement decomposition, gap-targeted acquisition, a validation
gate, execution-time monitoring, recovery. [[projects/blindtochange]]
names the third locus: models that search score near a common ceiling
(~79–82%) regardless of family, and the differentiator is the
decision to verify — "how rarely it searches, not how well it uses
what it finds."

## Evidence against and bounds

The HERA–AgenticDS contradiction is **not resolved** by any of this,
and this section leads with that because the evidence above could
mislead. TinyAstral decomposes TinyAstral; Dittany half-measures
Dittany. No pass-2 page runs HERA's corpus ablation with a swapped
backbone, or AgenticDS's backbone ablation over a degraded corpus —
so both pages' opposed answers stand, each internally valid on its
own system.

The full decomposition exists for exactly one system, and that system
is a simulated robotics benchmark suite: every TinyAstral number is
simulated. Whether a weights/harness split of this shape appears in a
dataset-search agent or a device-measurement agent is unknown.

The deeper bound: the decomposition may dissolve the question rather
than answer it. TinyAstral's answer is per-benchmark (harness on
RoboTwin, model on LIBERO-PRO); Prefix Executability's is an
interaction; BlindToChange's differentiator is a propensity that sits
awkwardly in both the weights and the artifact columns. If the routine
answer is "interaction, plus a behavioral-policy term," then "which
locus?" was under-specified as a corpus-level question — its value is
as a per-system measurement demand, not as a question expecting one
answer. That is the live possibility this entry records.

Finally, decomposition remains the exception. Of the pages touching
the question, most measure one side (Dittany, ANGLER) or neither
(GARDEN). The corpus's center of mass is still single-locus claims.

## Relations

[[concepts/improvement-lives-in-external-state]] is this question
answered for one locus: in the frozen-weights generation of systems,
it establishes that stored artifacts carry the improvement. Capability
locus is the wider attribution question — it also covers systems
where weights *do* change (TinyAstral's distillation term) and
components where the model is the load-bearing part (AgenticDS's
Critic). HERA sits on both sides of the pair: its corpus is external
state, and its ablation is the corpus's strongest artifact-dominant
locus measurement.

Distinguish from *accumulated-state-as-asset* (a held candidate,
named here without a page): that candidate concerns stored state as a
compounding, transferable asset, whereas capability locus concerns
attribution of measured quality, whether or not anything accumulates.
Distinguish also from *verification-is-load-bearing*: that entry is
one recurring answer — a verification component carries the load —
where this one is the general question of which component does. The
register records the typed relation hera —contradicts→ agenticds;
this page is where that contradiction is curated rather than settled.

## Open questions

- Will any system run the HERA/AgenticDS experiment factorially —
  corpus quality × backbone strength in one design — so the
  contradiction becomes a measurement?
- Is verification propensity a locus of its own, or a property of
  weights expressed only through behavior? BlindToChange's ceiling
  result suggests model rankings partly rank propensity, not
  capability.
- Does the TinyAstral decomposition shape — both terms positive, the
  interaction benchmark-dependent — replicate outside simulation and
  outside robotics?
- When both sides are measured, how often is the interaction term the
  largest of the three? Prefix Executability suggests it may be the
  common case, which would make single-locus ablations systematically
  misleading.

## Evidence status

This concept is the KB's analytical construct, synthesized in mining
pass 2 (2026-11-02) from the KB's own deepened project pages; no
paper names it. It was deferred in pass 1 because its two strongest
instances contradicted each other with no verdict earned, and it is
promoted here as a measured-decomposition entry on the strength of
TinyAstral's both-sides ablation and Dittany's second-cluster
half-measurement. The original HERA–AgenticDS disagreement remains
explicitly unresolved. Every underlying result is author-reported;
TinyAstral's are simulation-only, and no locus measurement in the
corpus has an independent replication.


## 2026-11-07 evidence connections

- [[projects/strategist]]: newly linked primary-source project; see its dated briefing and evidence limitations before treating this relationship as a universal mechanism.
