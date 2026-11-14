---
uid: 9482f8cf-50f7-423f-95f4-0cf875d34fdf
title: "Abstention as a first-class verdict"
summary: "When a verdict is forced, systems invent one; making insufficient evidence an explicit, accounted outcome changes the failure shape of the decision."
type: concept
depth: full
created: 2026-11-02
updated: 2026-11-10
related: [vericua, github-contribution-check, dittany, aisoc-v21, fa-agent, code-simplifier, matt-pocock-skills-reviewer]
sources:
  - url: https://arxiv.org/abs/2610.40578
    retrieved: 2026-11-02
  - url: https://github.com/github/gh-aw/blob/main/.github/workflows/contribution-check.md
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.42144
    retrieved: 2026-11-02
  - url: https://github.com/beenuar/AiSOC/releases/tag/v21.0.0
    retrieved: 2026-11-02
  - url: https://raw.githubusercontent.com/github/gh-aw/main/.github/workflows/code-simplifier.md
    retrieved: 2026-11-10
  - url: https://raw.githubusercontent.com/github/gh-aw/main/.github/workflows/mattpocock-skills-reviewer.md
    retrieved: 2026-11-10
---

# Abstention as a first-class verdict

## What it is

Most systems that return verdicts have a closed outcome space: pass or
fail, satisfied or violated, malicious or benign. When the evidence in
hand does not settle the question, a closed space forces a choice the
evidence does not support — the system invents a verdict, and the
invention is indistinguishable downstream from a verdict the evidence
did support. Abstention as a first-class verdict is the design move
that opens the space: "insufficient evidence" becomes an explicit,
named outcome of the decision itself, with its own accounting, rather
than an error, an omission, or a silent default to one side.

The concept is worth naming separately from ordinary error handling
because of the accounting. A first-class abstention is *counted*: the
system reports how often it abstained (coverage) separately from how
often its decided verdicts were right (decided accuracy), so the
abstention rate is visible and priced rather than hidden inside an
accuracy figure. Without that accounting, an abstaining system is
indistinguishable from a broken one — and a system can quietly trade
coverage for accuracy by deciding only the easy cases.

The corpus shows the move at two levels. At the **verdict level**, a
decision procedure gains a terminal "cannot decide" outcome. At the
**condition level**, each individual check inside a larger decision
gains a third state — neither satisfied nor violated, but
unestablished — which persists until its inputs arrive. The two levels
compose: a verdict-level abstention is what a system issues when too
many of its condition-level checks remain unestablished.

## Evidence for

**[[projects/vericua]] — the origin: abstention with priced
coverage.** VeriCUA's verifier returns a ternary verdict — success,
fail, or abstain — when it actively verifies a computer-using agent's
claimed task completion. The register's one-line form of the instance:
"insufficient evidence yields an explicit abstain outcome with
decided-accuracy/coverage accounting, rather than a forced binary
call." The accounting is the substance. Reporting accuracy over
decided cases alongside the abstention rate means the verifier cannot
inflate its reliability by abstaining on everything hard: the coverage
figure falls as the decided-accuracy figure rises, and both are on the
record. This is the only instance in the corpus where abstention is
fully priced.

**[[projects/github-contribution-check]] — abstention as a designed
terminal state.** The gh-aw contribution checker reviews pull requests
against a repository's contribution guidelines from metadata and
pre-fetched patches alone — a deliberately narrow evidence base, which
makes the missing-evidence case routine rather than exceptional. The
workflow's mechanism enforces the verdict: "if evidence is missing or
invalid, the checker must return verdict ❓, quality `triage:error`, an
empty comment, and an error — 'Do not retry tools or invent checklist
results'." The page's implications name the pattern directly: make "I
don't know" a structured, terminal output (❓ / `triage:error`) instead
of an invitation to improvise. Terminal is load-bearing: `triage:error`
results are never redispatched and never commented on, so the
abstention ends the matter auditable-as-error rather than looping the
checker until it produces something.

**[[projects/dittany]] — abstention as a state, not an exit.**
Dittany's repair framework judges each contract condition with a
three-valued label: "each condition is labelled **satisfied**,
**violated**, or **unestablished**, and pending checks resume when
their inputs arrive." Unestablished is never silently read as
satisfied — the failure this prevents is the quietest form of the
forced verdict, where an unchecked condition defaults to pass. And
because the label is a state in a running system rather than a
terminal verdict, abstention here is *revisable*: the check resumes
when the missing inputs land, and the label can resolve either way.
This is the condition-level form of the concept, and it shows the
verdict-level version is a special case — a decision that stays
unestablished forever because nothing will resume it.

**[[projects/aisoc-v21]] — abstention as measured behaviour.**
AiSOC's triage models abstain in practice: in the verdict eval,
Mistral abstained on 30.6% of items. AiSOC did not design that
abstention as a verdict class; what the project did design is the
accounting around it — "the replay scorer keeps abstentions and
failures in the malicious denominator rather than letting them drop
out of the recall figure." An abstention therefore costs exactly as
much as a miss in the headline number. The instance matters because
it closes the gaming path from the measurement side: a model whose
abstentions vanished from the denominator would post a higher recall
for deciding less.

## Evidence against and bounds

**Abstention can be gamed, and only one instance prices it.** A system
that abstains on everything is safe and useless. The defence is
coverage accounting — abstention must appear in the reported numbers
as a cost — and across the four instances only VeriCUA's carries the
full decided-accuracy/coverage pair. Contribution Check's `triage:error`
is terminal and visible, but the page reports no coverage rate for it;
Dittany's unestablished is a state whose eventual resolution is
tracked by the repair loop, not summarised as a rate. The concept as
practised is therefore uneven: the strongest instance prices
abstention, the others mostly make it *legible*. A reader should not
credit every three-valued outcome space with the discipline — the
accounting is the discipline.

**AiSOC's instance is behaviour observed, not a verdict designed.**
The pass-2 E brush is explicit: abstentions exist in AiSOC as measured
behaviour, and the scorer's denominator discipline is real, but
"abstention is not a designed verdict class with decided-accuracy/
coverage accounting in AiSOC." The instance supports the concept's
measurement half — abstention must stay in the denominator — and not
its design half. It is included as a brush that corroborates the
accounting point from an independent genre (security triage), not as
a fourth designed instance.

**No instance prices the downstream cost.** Every instance answers
"what does the system output when it cannot decide?" None answers
"what happens next, and who pays?" A terminal ❓ ends the checker's
obligation but not the contributor's problem; an unestablished
condition resumes only if inputs actually arrive; an abstained
verification leaves the trajectory unjudged. Who retries, who
escalates, who decides on the strength of an abstention — the
user-facing cost model — is absent from all four sources. The concept
redistributes failure from wrong-verdict to no-verdict; whether that
trade is net-positive depends on machinery none of these pages
describes.

**Scope of the evidence.** Three designed instances and one measured
brush, across two mining clusters — enough to promote the concept from
its pass-1 single-source hold, not enough to claim the pattern is
general practice. All four sources are from the same 2026 preprint and
project cohort the rest of the KB covers.

## Relations

The nearest built neighbour is [[concepts/scoped-assurance]]: a
verification result holds only inside the scope actually exercised.
Abstention is how a system *acts* on that limit at decision time —
scoped assurance describes the epistemic position, abstention is the
behavioural response when the position is reached mid-decision. A
system can fully understand its scope limits and still force verdicts
outside them; conversely, an abstention outcome without scope
discipline is just indecision. The register also carries a technique
seed, gated admission (held in plain text here, its page not yet
built): gated admission decides what may *enter* a system — accepted
or rejected at a boundary — where abstention decides what a system
may *conclude*. Admission gates act on artifacts; abstention acts on
judgments. The four supporting pages relate as instances, not as a
chain: [[projects/vericua]] (verdict-level, priced),
[[projects/github-contribution-check]] (verdict-level, terminal),
[[projects/dittany]] (condition-level, revisable),
[[projects/aisoc-v21]] (measured behaviour, denominator discipline).

## Open questions

- What coverage rate makes an abstaining verifier net-negative? None
  of the instances states a threshold at which abstention stops being
  honesty and starts being uselessness; VeriCUA's accounting makes the
  trade visible but does not price the exchange rate.
- Does a terminal abstention (`triage:error`) produce better
  downstream behaviour than a revisable one (unestablished)? The
  corpus contains both designs and no comparison.
- Who should own the retry? If an abstention is routed to a human, the
  concept is a triage mechanism; if it is routed to a stronger model,
  it is a cascade mechanism. The instances do not say, and the
  economics differ completely.

## Evidence status

This concept is the KB's analytical construct, synthesised in mining
pass 2 (2026-11-02) from the KB's own deepened project pages. It began
as a pass-1 single-source hold on [[projects/vericua]] and was
promoted when pass 2 found a second and third designed source in
cluster F ([[projects/github-contribution-check]],
[[projects/dittany]]) plus a measured-behaviour brush in cluster E
([[projects/aisoc-v21]]). No source paper or project names the
concept. Every instance is author-reported or author-documented — the
two preprints report their own designs, the workflow's behaviour is
specified in its own source file, and AiSOC's abstention figures come
from its own published eval — with no independent replication of any
instance.


## 2026-11-07 evidence connections

- [[projects/fa-agent]]: newly linked primary-source project; see its dated briefing and evidence limitations before treating this relationship as a universal mechanism.

## 2026-11-10 evidence connections

Two further instances from the depth pass over the gh-aw workflow pages (analyst-level links; the sources do not name the concept):

- **[[projects/code-simplifier]] — abstention before the model runs, and typed endings.** A sub-class none of the four instances above has: a skip-if-decision gate that abstains (skips agent execution entirely, at zero model turns) only on *conclusive* no-candidate evidence — "Abstain if either dataset is invalid, incomplete, inconsistent, or contains an eligible candidate," so uncertain evidence preserves execution, the conservative direction. Above the gate, three verbatim `noop` messages name *why* nothing was done (no recent changes, no worthwhile simplifications, budget ceiling), and the output contract forbids finishing without one of six typed endings, three of which are abstentions — a run cannot end in vague success text. This makes abstention structural but not *priced*: the vendor's telemetry reports "0 safe-output items" across the published window, yet no decided-accuracy/coverage pair exists, so VeriCUA's accounting discipline still has no second instance. Bound carried from the page: the published window contains zero write-path runs, so the abstention discipline is evidenced only on the cheap half of the design.
- **[[projects/matt-pocock-skills-reviewer]] — the disclosure cousin, not a designed abstain verdict.** Its triage fallback degrades to a deterministic heuristic, retries at most once, and must "mention in the Step 6 review body that skill selection used the fallback heuristic" — the concept's accounting made mandatory in prose, without the abstention itself. Its `noop`-instead-of-generic-praise success criterion is abstention at the comment level. Recorded as a brush corroborating the disclosure half of the discipline, not as a designed instance.

The designed-instance count rises to five; the coverage-accounting gap flagged in the bounds section is unchanged — still only VeriCUA prices abstention.
