---
uid: 9fe52e42-4239-4831-9a13-f54119bff842
title: "Ground-truth fallibility"
summary: "The reference standards benchmarks score against contain measurable errors of their own, so agreement with a standard bounds a score differently than assumed."
type: concept
depth: full
created: 2026-11-02
updated: 2026-11-02
related: [vericua, codespecweave, exlabel, explorerepair]
sources:
  - url: https://arxiv.org/abs/2610.40578
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.40256
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39417
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39899
    retrieved: 2026-11-02
---

# Ground-truth fallibility

## What it is

Ground-truth fallibility is the property that the reference standard an
agent evaluation is scored against — gold labels, benchmark test suites,
human annotations — is itself an artifact with a measurable error and
misalignment rate, so agreement with it is a noisy target rather than
correctness itself. The error runs in both directions: a standard can
certify behavior that violates the stated requirement, and it can reject
behavior that satisfies it. A score reported against such a standard is
therefore bounded twice over — by the system's performance and by the
standard's own accuracy — and the two contributions are not separable
from the score alone.

The practical consequence is about comparison, not just calibration. A
score difference between two systems is only interpretable if it
exceeds the noise the standard itself contributes; below that, ranking
by agreement with the standard can rank systems by their fit to the
standard's idiosyncrasies. Fallibility therefore has to be budgeted
like any other measurement error — estimated, reported, and compared
against the differences the score is asked to support.

The concept is deliberately provenance-blind. It is distinct from the
sibling concept generated-oracles-inherit-generator-error, which
concerns verification artifacts a system manufactures for its own
checking; that failure mode requires a generation step. Fallibility
requires none. The gold labels [[projects/vericua]] caught contradicting
its verifier were the official evaluators' own verdicts, and the
annotations behind [[projects/exlabel]]'s benchmark are human work,
agreement-filtered. A standard can be entirely hand-made, carefully
reviewed, and still wrong at a rate an audit can measure — that is the
claim here, and it is what separates fallibility from complaints about
machine-generated tests specifically.

## Evidence for

**[[projects/vericua]]** supplies the most direct measurement. VeriCUA's
verdicts contradicted the official gold on a set of flagged cases, and
the authors submitted those contradictions to an adjudicator from a
different model family. The adjudicator "confirms 51 of 81 flagged
verdict–gold contradictions" — it "supports VeriCUA on 63%". In other
words, within the flagged subset, the reference side of the disagreement
was the wrong side roughly two times in three. The procedure cuts both
ways — in the remaining 30 cases the adjudicator did not confirm
VeriCUA's contradiction — which is what makes the 63% a measurement
rather than a rhetorical win: the checker was held to the same audit as
the gold. The page's conclusion is
the concept in one line: "Agreement with official evaluators is a noisy
target." Note the scope: 63% is a rate within cases already flagged as
contradictions, not an estimate of gold error overall — but it shows
that where a strong checker disagrees with gold, gold is not the safe
default.

**[[projects/codespecweave]]** measured fallibility at construction
scale. Auditing the candidate tasks for its synthetic coding benchmark,
the authors found that "2,267 tasks, 73.9%, had at least one alignment
flaw" out of 3,067 pilot candidates. The flaws ran in both directions
the definition predicts: "a patch passes the tests while violating a
stated requirement" — the suite certifies wrong behavior — or the tests
"reject valid alternatives" — the suite condemns right behavior. A
solver scored against the unfiltered suite would have been graded by a
standard that was misaligned with its own stated requirements in nearly
three quarters of tasks, before any question of solver competence
arises.

**[[projects/exlabel]]** shows two quieter failure shapes in a
human-built standard. First, the reference labels are agreement-filtered
annotation: "only instances where **all annotators agree** on the
binarized labels are retained". Filtering on unanimity does not remove
error so much as remove the instances where error was visible, and it
changes the measured population toward cases humans find unambiguous.
Second, the standard's provenance is entangled with the method scored
against it: "The benchmark was cleaned by the authors around the failure
modes ExLabel targets." Neither shape involves a careless benchmark —
both arise from reasonable curation choices whose effect on the score's
meaning is easy to miss.

## Evidence against and bounds

The strongest bound is that fallibility is **correctable in one
direction**. VeriCUA's adjudication did not merely expose gold error; it
resolved most of the flagged contradictions, assigning the error to one
side or the other. Noisy gold degrades the precision of a measurement;
it does not void measurement. The corrections differ in shape, though.
ExLabel's benchmark was repaired by *deletion* — instances removed,
population changed — whereas CodeSpecWeave's flaw was in tests
*retained* in the candidate set. One response shrinks what is measured;
the other ships the misalignment.

**[[projects/explorerepair]]** is a bounding instance rather than a
fourth support. Its success criterion is "the benchmark's hidden PoV
test", whose coverage determines what "success" can mean, and the page
itself flags success-by-own-PoV as "weaker evidence". This is
fallibility with its limits made explicit and priced in: the standard
is known to be partial, and claims are hedged accordingly. It bounds
the concept by showing that a fallible standard, openly treated as one,
still supports usable — if weaker — conclusions.

What fallibility does **not** imply: that benchmark scores are
meaningless, or that all standards err at CodeSpecWeave's pilot rate.
The 73.9% figure measures unfiltered candidate tasks in one synthesis
pipeline, caught precisely because the authors audited before release.
The claim is narrower: any score's interpretation must budget for the
standard's error, audits can measure that error, and until one is run,
agreement with the standard and correctness are different quantities
that happen to share a number.

## Relations

- **[[projects/codespecweave]] —supports→ [[projects/vericua]]** —
  CodeSpecWeave's audit is large-scale evidence for VeriCUA's founding
  premise that fixed or generated verification is unreliable:
  "automated reviews identified alignment flaws in 2,267 of 3,067
  candidate tasks (73.9%)". The support is for the premise, not the
  method — and it is the same measurement that anchors this concept.
- **[[projects/exlabel]] —shares-benchmark→ [[projects/codespecweave]]**
  — both report results on SWE-bench Verified: ExLabel's fine-tuned
  model was "evaluated on SWE-bench Verified" at "66.2% resolved", and
  CodeSpecWeave's RL table reports SWE-bench Verified for every
  training-data arm. The shared standard plays different roles —
  endpoint metric for ExLabel's data filter, one of four evaluation
  columns for CodeSpecWeave — so its fallibility propagates into both
  pages' numbers along different paths.
- **[[projects/vericua]] —shares-mechanism→ [[projects/explorerepair]]**
  — both replace text judgment with synthesized executable checks:
  VeriCUA can "synthesize a *checker*: a sequence of permitted reads
  paired with a predicate", and ExploreRepair's executable agent
  constructs and runs its own PoV test. The relation matters here
  because an executable check inherits the standing of the standard it
  encodes — mechanism does not launder fallibility.
- **[[projects/explorerepair]] —shares-mechanism→ [[projects/exlabel]]**
  — both distill prior trajectories and outcomes into compact,
  retrievable guidance that steers later judgments: ExploreRepair's
  "short, role-specific lesson" distillates, and ExLabel's curated
  experience items. Judgments steered by distilled experience are only
  as sound as the — fallible — outcomes they were distilled from.

## Open questions

- VeriCUA's 63% is conditional on flagged contradictions. What fraction
  of unflagged gold verdicts would fail the same adjudication? No page
  in the KB measures a base rate.
- Agreement-filtering (ExLabel) trades visible annotator disagreement
  for population shift. Can the resulting bias toward unambiguous
  instances be quantified, and does it inflate scores comparably across
  systems?
- Repair-by-deletion and repair-by-correction have different effects on
  what a benchmark measures. Is there a reporting convention that makes
  which repairs were applied — and to how many instances — a standard
  part of a benchmark score?
- When a system's error rate approaches its standard's error rate,
  rankings should become unstable. Does any KB page report scores close
  enough to its standard's measured error for this to bite? None of the
  four pages here puts the two rates side by side.

## Evidence status

This concept is the KB's analytical construct, synthesized 2026-11-02
in mining pass 1 from the KB's own deepened project pages; the label is
not a term the underlying papers use for themselves. Mining grade:
medium — three full supports ([[projects/vericua]],
[[projects/codespecweave]], [[projects/exlabel]]) plus one bounding
instance ([[projects/explorerepair]]), all from a single cluster of the
corpus. Every underlying result is author-reported: the adjudication
rate, the alignment-flaw audit, and the annotation protocol are as
reported by each paper's own authors, with no independent replication
in the KB.
