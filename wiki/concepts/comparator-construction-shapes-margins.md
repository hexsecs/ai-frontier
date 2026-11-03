---
uid: be154225-e331-4dae-bb1f-44eeaeec872d
title: "Comparator construction shapes margins"
summary: "A reported margin partly measures how its comparator was built — reimplementation fidelity, baseline selection policy, or literature numbers instead of re-runs."
type: concept
depth: full
created: 2026-11-02
updated: 2026-11-02
related: [explorerepair, vericua, repairs-for-whom, codespecweave, angler, bioagent, dittany, tinyastral, context-as-infrastructure]
sources:
  - url: https://arxiv.org/abs/2610.40578
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39899
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.42144
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.41383
    retrieved: 2026-11-02
---

# Comparator construction shapes margins

## What it is

A margin is a difference between two numbers, and in this literature one
of those numbers is usually manufactured by the claimant. The comparator
a method is measured against is rarely the published system running as
designed: it is a re-implementation by the method's own authors, the
original run outside its designed conditions, a search policy chosen to
stand in for a whole class of alternatives, a row copied from another
paper, or — at the limit — no measurement at all, only citations. The
concept is that the reported margin is therefore a joint property of the
method and of how its comparator was produced: change the construction —
restore a cut loop, re-run instead of transcribing, swap a random policy
for a real competitor — and the margin moves, sometimes by more than the
effect the paper is claiming.

This is distinct from the neighbouring phenomena. Protocol-relative
scores vary the *measurement convention* — scoring rule, denominators,
attempt structure — over a fixed set of comparators; this concept varies
how the comparator itself was *produced*, before any scoring convention
is applied. Evaluator-identity-relativity varies *who grades* the
outputs; here the grader can be perfectly neutral and the margin still
inherits the construction, because what is being graded against was
built by one side. It is also distinct from the unmatched-effort
confound: construction alters the comparator itself — its form, its
guidance, its provenance — whereas the effort confound leaves both
methods in their designed form and varies only the spend. The
EvoRepair turn cut below is claimed here, not under effort, because the
cut removes the baseline's designed guidance loop rather than merely
shrinking a budget both sides shared.

## Evidence for

**(a) Author-adapted re-implementations as baselines.** The most common
mode: the comparator exists only as the claimant's own rebuild of
someone else's system. [[projects/bioagent]] is the cleanest statement
of the shape: "The 25 skills are precisely the skills BioAgent was
purpose-taught for these protocols, on its own platform, scored with its
own success criteria. The three baselines are the authors' own
adaptations of other systems to that platform" — an adapted
re-implementation is not the original system, and the baselines' extreme
lows "are at least as consistent with adaptation disadvantage as with
the original methods' ability". [[projects/vericua]]: "Baselines are
the authors' re-implementations, two of them reduced" — CUAJudge's
four-stage pipeline "collapsed into one call", OS-Themis "cut from six
milestones and twelve frames to four and eight". [[projects/explorerepair]]
ran its principal comparator weakened: EvoRepair "is designed to be
guided by a ground-truth PoV and benchmark-oracle feedback; here it
receives neither", and "its refinement loop is cut from the original 15
turns to up to 3" — a transformation the authors concede "transforms the
setting for which the baseline approaches were designed".
[[projects/repairs-for-whom]] compares published methods that "appear
only as re-implemented verification steps inside this fixed-candidate
protocol, not as full reproductions of pipelines", so the recorded
losses "attach to the rules in isolation, not to the deployed methods".
[[projects/dittany]] repeats the mode inside its strongest-baseline row:
"even Reflexion here is the authors' MAS-level adaptation of a
single-agent method, not the original design".

**(b) Baseline selection policy.** Sometimes nothing is re-implemented;
the construction is the choice of *which* comparator stands in for the
alternative. [[projects/angler]]'s sole experimental comparator "selects
one of the remaining candidates uniformly at random" — "a deliberately
weak search policy". Its headline therefore "measures adaptivity against
random selection, not against the best alternative attacker", and
competing adaptive systems appear only in a feature matrix: "no
quantitative comparison numbers against any competing attacker or
benchmark". A margin over a random policy is a true number about a
constructed opponent.

**(c) Literature numbers vs re-runs.** [[projects/dittany]]'s two named
baselines were "re-executed under matched conditions on only five of the
30 applications; their other 25 results are 'the reported configurations
and assessments' from those systems' own papers, on potentially
different task instances and assessments". The page's own verdict:
"Margins over SupervisorAgent and AgentTether rest partly on
non-comparable rows." Five rows of the comparison are measurements; the
other twenty-five are provenance of a different kind wearing the same
table formatting.

**(d) Reduced-settings harnesses and citation-only comparison.**
[[projects/tinyastral]]'s competitor-harness headline gaps were produced
against a comparator run at reduced settings, and a second comparator is
disadvantaged by construction: PyRUA-Lean is "trained and self-evaluated
with a per-step environment success signal; without this signal, which
our protocol withholds, it often declares success prematurely" — the
explorerepair shape, a baseline run outside its designed conditions,
recurring in a second cluster. [[projects/context-as-infrastructure]]
constructs its comparison set by citation rather than measurement:
against dense retrieval "it offers only the unquantified assertion
discussed above, plus cited related work", and query-time compression
"is contrasted by construction rather than by experiment: … no
head-to-head numbers are reported".

**(e) Benchmark provenance.** [[projects/codespecweave]] constructs the
yardstick itself: "The same pipeline builds the training data and the
benchmark", with the same vendor's models as construction agents,
solvers, and trained backbones — the comparator is not a baseline system
but the evaluation set, produced by the method's own supply chain.

## Evidence against and bounds

The concept claims margins are *partly* construction, not that they are
wholly artefact, and the corpus itself supplies the bounds. First,
construction-dependence is a matter of degree: repairs-for-whom's
margins survive its construction better than most, because its
comparators are evaluators inside its own protocol by design and its
fresh-rollout mechanism checks replicate — when the re-implementation
*is* the object of study, the construction objection largely dissolves.
Second, the effect is measurable and partly correctable inside a study:
in vericua, restoring budget measurably raised a baseline's score, so a
reader given the construction details can estimate the direction and
rough size of the distortion rather than merely suspecting it. Third,
disclosure quality varies informatively — explorerepair and
repairs-for-whom state the construction plainly in their own
limitations, while vericua's reductions are "evident from the methods,
not author-flagged" — which means the phenomenon is detectable where
authors disclose, and the worst cases are exactly the undisclosed ones.
Finally, the hard bound: no page in the corpus re-runs an original
system in its original form alongside its re-implementation, so the
*share* of any headline margin attributable to construction is nowhere
quantified. The concept licenses discounting and demanding the
construction statement; it does not license dismissing any particular
margin outright. One instance is also dual-coded: tinyastral's
reduced-settings comparator is simultaneously an effort confound, and
the register counts it once, here.

## Relations

The supporting pages divide by construction mode rather than by topic:
adaptation ([[projects/bioagent]], [[projects/vericua]],
[[projects/explorerepair]], [[projects/repairs-for-whom]]), selection
policy ([[projects/angler]]), provenance of the numbers themselves
([[projects/dittany]], [[projects/context-as-infrastructure]]),
re-conditioned harnesses ([[projects/tinyastral]]), and benchmark
provenance ([[projects/codespecweave]]). TinyAstral and ExploreRepair
are the same failure shape in two clusters — a baseline run outside its
designed conditions — which is what carried this entry across the
single-cluster line. Angler and BioAgent also anchor
protocol-relative-scores, and the two concepts compose: a score can be
protocol-relative *and* measured against a constructed comparator, and
the discounts multiply rather than substitute. Codespecweave's
benchmark-provenance mode borders evaluator-circularity, where the
evaluation is partly produced by the thing evaluated; the difference is
that here the distortion enters through the comparison set's
construction, whether or not any judging is self-referential.

## Open questions

- How much of each headline margin survives a faithful re-run? Only
  vericua's budget-restoration result even gestures at a magnitude; a
  single study running an original system beside its re-implementation
  would price the phenomenon.
- Should a random or otherwise deliberately weak selection policy be
  labelled a *baseline* at all, or reported as a lower bound on the
  alternative class?
- Do literature rows belong in headline comparison tables, or only in
  clearly-marked context rows, given that table formatting erases the
  provenance difference?
- Would a standard construction statement — who built the comparator,
  what was changed, what was re-run — change which margins get claimed,
  the way precommitment changed what Auctopus could claim?

## Evidence status

This concept is the KB's analytical construct, synthesized in mining
passes 1–2 (2026-11-02) from the KB's own deepened project pages; no
paper names it. It was **deferred in pass 1** — graded medium on four
pages, all in one cluster — and **promoted in pass 2** when clusters E
and F widened its base to nine pages across three clusters and at least
five construction modes; that deferral and promotion are the register
discipline working as intended, recorded here rather than smoothed over.
Every underlying result is author-reported, and several of the strongest
instances are known only because the claimant's own page disclosed the
construction — the evidence base is therefore biased toward honest
papers, and the true prevalence of the phenomenon in the corpus is
likely higher than these nine pages show.
