---
uid: 6c3d97b4-2543-431c-98e9-a97423da87e5
title: "Protocol-relative scores"
summary: "A reported gap — and sometimes the ranking itself — is a property of the measurement convention chosen, not only of the system measured."
type: concept
depth: full
created: 2026-11-02
updated: 2026-11-02
related: [intent-loss-in-smart-contract-synthesis, seq-k, dynarev, clingex, webanything, prefix-executability, angler]
sources:
  - url: https://arxiv.org/abs/2610.37830
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.37859
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.40133
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.37786
    retrieved: 2026-11-02
---

# Protocol-relative scores

## What it is

A reported score is a property of the full measurement convention —
scoring rule, feedback mode, denominators, coverage — not of the system
alone. Change the convention and the measured gap, the pass rate, and
sometimes the ranking change with it, while the system under test has not
changed at all. A benchmark number is therefore a joint property of two
things: the system measured and the protocol that measured it. Quoting
the number without the convention is quoting half the result.

The convention has several independent dials, and the supporting pages
each isolate a different one. The scoring rule decides what counts as
success on a fixed set of outputs. The feedback mode decides what a
system is allowed to learn between attempts. The denominator decides
which cases a percentage is taken over. Coverage decides which parts of
a system's behavior the metric can see at all.

This concept is distinct from three neighbours it is easily confused
with. Comparator-construction shapes margins by varying how the
*opponent* was built — which baseline, trained on what, at what budget.
Evaluator-identity-relativity varies *who* evaluates — which model sits
in the judge's seat. Construct-validity leakage is a number crediting
the wrong cause under a *fixed* convention. Protocol-relativity is none
of these: the opponent, the judge, and the causal story can all stay
fixed while the number still moves, purely because the convention that
produces it changed.

## Evidence for

**[[projects/seq-k]]** makes the strongest form of the claim, because
its subject is the convention itself. A Seq@K value "is well-defined
only after specifying feedback mode alongside the benchmark task split,
verifier, prompt builder, decoding hyperparameters, and attempt budget."
The paper shows the two natural protocols measure different things: how
much a model gains from more independent samples says little about how
much it gains from feedback (the gains correlate at −0.08). The
consequence is practical, not philosophical. In a controlled selection
study, calibrating model choice with Pass@5 picked actors whose
held-out Seq@5 reached 70.8% and 90.2%; calibrating with Seq@3 picked
actors reaching 96.8% and 98.4% — choosing under the wrong protocol
left 8–26 points of held-out sequential success on the table. Feedback
mode is a dial of the same kind: rubric-aware critics repaired 73.8% of
failed criteria, binary feedback 34.4%, and plain resampling 36.5% — the
"sequential" number is mostly a number about the feedback convention.

**[[projects/intent-loss-in-smart-contract-synthesis]]** isolates the
scoring-rule dial on fixed outputs. Scoring the same 500 output sets
four ways: under a shared-interface metric — only the functions all
systems implement, on contracts where all build — the elicitation-first
pipeline leads by 19 points on 364 contracts; under a fixed required
interface the gap is 35 points on 499 contracts; under exact replay, 34.
The shared-interface convention silently erased 16 points of a real gap
by discarding exactly the functions the weaker system omitted: the
metric's coverage decided what the gap was allowed to be. The authors'
own previous scorer makes the same point from the other side — it
passed 43.9% of the pipeline's contracts, but 162 of those 219 passes
had an unobserved value or a missing or mismatched function.

**[[projects/dynarev]]** shows the ordering itself flipping across
metric families within one study: "Qwen3.8-Flash has a lower Score than
Claude-Opus-5-5 (0.604 vs 0.681) but a higher success rate (39.2% vs
36.5%)". Mean constraint satisfaction, strict success, and
revision-responsiveness rank the same five models differently, so which
system "won" DynaRev depends on which of its own headline metrics the
reader picks up.

**[[projects/webanything]]** contributes two dials. Its largest
fidelity gap sits on a metric computed under a disclosed asymmetry:
"the source side is frozen HTML *replayed with JavaScript disabled*
while mirror text comes from JavaScript-enabled captures" — the Text F1
gap is partly a property of the replay convention. And when strict
scoring penalized the fine-tuned model's format deviations, the authors
rescored its outputs under a format-relaxed rule (Retrieve passes rise
from 12.00% to 32.31%) — applied only to that model's outputs, with no
relaxed baseline, so the relaxed number cannot be compared against
anything. The page also notes the denominator form: "Accepted counts
describe accepted outputs, not the success rate of all proposals or
attempts."

**[[projects/clingex]]** is the denominator case in clinical dress. Its
headline concordance figures are not on common denominators:
actionability concordance is computed over 65 of 78 cases, gene–disease
scoring uses each system's own parsable-output subset, and the SNV
sensitivity and specificity exclude VUS references. The same paper
shows how easily headline numbers detach from their denominators — the
abstract's MRMC triple is the DeepSeek arm only, not routine practice.
Nothing here is hidden; the percentages simply do not mean what a
reader comparing them across tasks would assume.

## Evidence against and bounds

The concept has a live internal tension, and it is a bound, not a
refutation. In [[projects/intent-loss-in-smart-contract-synthesis]],
rankings survived: "Rankings are stable across every scoring rule
tried; absolute fidelity values, gap sizes, and pass rates are not."
Re-scoring fixed outputs under four conventions moved the gap by 16
points and changed pass rates, but never reordered the systems. Against
that, [[projects/seq-k]] and [[projects/dynarev]] show orderings that do
flip — but note what kind of convention change flips them. In Seq@K,
the change is to the attempt structure itself (independent samples vs
feedback-conditioned revision), which changes what behavior is being
elicited, not merely how it is scored. In DynaRev, the flip is across
metric families that weight different outcome dimensions. The precise
claim the evidence supports is therefore asymmetric: **magnitudes and
pass rates are always protocol-relative; rankings are
protocol-relative often** — when the convention changes what is
attempted or which outcome dimension headlines, and not, on this
evidence, when identical outputs are merely re-scored. The concept also
does not claim scores are arbitrary: in every supporting study the
convention is named, fixed in advance, and applied uniformly, which is
exactly what makes the movement attributable to it.

## Relations

- [[projects/dynarev]] —supports→ [[projects/seq-k]]: independent
  designs converging on this concept's core claim — dynarev finds that
  "delivering identical final requirements progressively changes
  outcomes in model-dependent directions, so single-turn scores do not
  predict performance under revision," which is seq-k's central
  measurement arrived at from a different benchmark.
- [[projects/intent-loss-in-smart-contract-synthesis]]
  —contradicts (apparent)→ [[projects/seq-k]]: intent-loss finds
  post-generation stages worth at most about one point, seq-k finds
  post-failure revision repairing 73.8% of failed criteria. The
  register resolves the apparent contradiction by information content —
  and information content is itself one of seq-k's protocol variables
  (feedback mode), so the resolution reinforces rather than weakens
  this concept.
- Boundary markers, recorded under other concepts and deliberately not
  claimed here: [[projects/clingex]] —same-failure-mode→
  [[projects/dynarev]] and
  [[projects/intent-loss-in-smart-contract-synthesis]]
  —same-failure-mode→ [[projects/clingex]] both concern the judge being
  the contestant's own model — evaluator-identity-relativity, not
  protocol-relativity, even where the same pages are involved.

## Open questions

- Intent-loss's ranking stability under re-scoring rests on a single
  study with one pipeline family. Does it generalize — is re-scoring
  alone ever enough to flip a ranking between close systems, or is an
  attempt-structure change always required?
- Which convention elements should be mandatory disclosures for a
  headline number to be quotable: interface coverage and denominators
  (intent-loss, clingex), feedback mode and attempt budget (seq-k), or
  the metric family (dynarev)? The pages agree the convention must be
  reported; none proposes the checklist.
- If benchmarks published both an independent-attempt and a sequential
  protocol by default, would seq-k's 8–26-point selection losses shrink
  in practice, or do practitioners select on whichever number is
  headline regardless?

## Evidence status

This concept is the knowledge base's own analytical construct,
synthesized 2026-11-02 in mining pass 1 from the KB's deepened project
pages listed above — it is not a term any of the underlying papers use
for their own results. Every underlying result is author-reported from
a single-team preprint, with no independent replication in the set; the
register grades the concept medium (five supporting pages). The
concept asserts exactly what those pages jointly support — magnitudes
and pass rates always, rankings often — and its bound comes from inside
the evidence, not from caution applied after the fact.
