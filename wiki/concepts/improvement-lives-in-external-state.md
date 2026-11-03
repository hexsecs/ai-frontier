---
uid: 9cafe10f-c05b-4127-8fd8-fc3ea28431e8
created: 2026-11-02
updated: 2026-11-02
type: concept
depth: full
title: "Improvement lives in external state"
summary: "Agents in this corpus improve by editing persistent external state (memory, knowledge modules, skills, team rules) while model weights stay frozen."
related: [filingloop, garden, hera, karma, molrsi, evoteam, github-copilot-fusion]
sources:
  - url: https://arxiv.org/abs/2610.39884
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39714
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.37926
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39074
    retrieved: 2026-11-02
---

# Improvement lives in external state

## What it is

The claim: across the systems this knowledge base has deepened, the thing
that improves is persistent state *around* a frozen model — a skill
document, a curated corpus, a reward program, a knowledge directory, a
team library — not the model's weights. The model is held fixed while
some external artifact is edited, accumulated, or selected, and the
measured gain is attributed to that artifact.

This candidate sits on the concept/technique boundary. The *methods* —
validation-gated knowledge editing, memory-conditioned search,
test-gated skill compilation — are techniques and belong to other pages.
As a concept, this entry is the empirical claim those methods jointly
support: in this corpus, the locus of improvement is external state.
Freezing the artifact is also what makes the improvement inspectable,
reversible, portable, and its transfer measurable, because the identical
artifact can be applied unchanged to cases it was not developed on.
(Mining pass 1 also recorded the alias *frozen-artifact-learning*.)

## Evidence for

**[[projects/karma]]** is the purest statement. "Model weights, business
tools, and all executable harness code stay frozen throughout; the only
thing that changes is a directory of typed knowledge modules that the
agent's prompt is rendered from." Six typed modules are edited in small,
schema-checked steps; a patch is kept only if it improves a fixed
validation set, and the initial and final knowledge states are each
evaluated on the untouched hold-out exactly once, at the end.

**[[projects/molrsi]]** improves a search policy, not a model. "The
backbone model — Claude Sonnet 5, via the Anthropic API — is frozen
throughout. Nothing is retrained, and the agent does not modify its own
code or architecture. What improves is the *effective search policy*."
The policy lives in three persistent memory stores — solution,
refinement, and execution memory — which record workflows and scores,
modifications and their outcomes, and failures and their repairs, and
condition later searches.

**SkillCompiler** (see [[projects/skillcompiler]]) compiles
well-specified operations of a skill into validated, deterministic
programs stored in a persistent Program Asset Bank, retrieved for reuse
across skills. Its page states the locus directly: "Model parameters
are never updated: all learning happens in the skill and program-bank
state," with candidate and bank states selected on validation
performance and frozen before test evaluation.

**[[projects/evoteam]]** evolves three levels of persistent knowledge —
team rosters and descriptions in a reusable team library, team-scoped
interaction rules, and individual agent skills — "with the underlying
LLM parameters held fixed". Because the evolved artifacts are external,
they can be ported: applied to other backbones, they stay "within 4.00
points of the corresponding same-backbone performance".

**[[projects/garden]]** makes the artifact a single reward program
written by an LLM reward engineer. The selected reward's "source is
frozen and hashed, and it is applied **unchanged** to held-out
scenarios" — the freeze is what turns transfer into a measurement
rather than an anecdote.

**[[projects/hera]]** supplies the controlled version: with the model
fixed, "a curated knowledge base is a *measurable* intervention in
agent quality, separable from the model". Removing the corpus collapsed
expert-verdict grades from 1.00 to 0.40 in the trial apparatus — the
quality was in the external state, not the weights.

**[[projects/filingloop]]** updates "written procedures … across cases
from requirement-level grading feedback while model weights stay
frozen"; its summary of what moves between cases is that "what
transfers is procedure, not facts".

The substrate itself is independently documented. Persistent text
files that an agent loads and carries across sessions are a real,
measurable channel: [[projects/security-impact-of-coding-agent-memory-files]]
studies them as an attack surface, and [[projects/exlabel]] is the
positive control that the same channel steers behavior when the stored
content is a curated experience bank — removing the bank costs up to
84.0% of F1 on a cell. One further supporting page,
[[projects/github-copilot-fusion]], is vendor material and counts only
as architectural description: its control layer sits outside any model,
the router choosing models and execution patterns.

## Evidence against and bounds

External state is a locus, not a guarantee. The memory-files study is
the null result this concept must carry: planted memory files changed
security outcomes by only −8 to +6 percentage points across three agent
configurations, with no consistent direction and every shift inside the
band the authors say cannot be told from chance. Persistent state was
present, loaded, and adversarially written — and did not reliably
steer. Stored text improves a system only when the channel actually
moves behavior, which is the separate question owned by the sibling
concept persistent-memory-steers-later-behavior.

The frozen reader bounds the artifact. [[projects/evoteam]] states the
dependence plainly: "effective use of the experience depends on the
base model's ability to correctly interpret and apply the stored
guidance". External state improves the system only as far as the frozen
model can read it — the artifact and the reader are complements, not
substitutes.

The individual exhibits are bounded too. [[projects/hera]]'s ablation
is not perfectly clean: "ablated sessions differed from full sessions
in the brief and output contract as well as the corpus", so part of the
collapse may belong to the contract, not the corpus. [[projects/garden]]'s
transfer is shown "across *related* scenarios of a family — the paper's
own scoped claim — not transfer to new tasks". [[projects/filingloop]]'s
artifact learned unevenly: the frozen skill improved revision behaviour
but not discovery. And stored experience can travel badly: transfer is
a per-source property to measure, not to assume — which sources
contributed experience changes the outcome ([[projects/molrsi]]), and
karma's transfer results likewise read per source domain. The sign of
travelling experience is the sibling concept
negative-transfer-of-experience; this entry is about where improvement
resides, that one is about whether it survives the trip.

Finally, the branding bound. [[projects/molrsi]]'s "recursive
self-improvement" names a memory-update loop around a frozen model; its
page insists the two not be conflated with the model improving itself.
Any citation of this concept that slides from "the system's external
state improved" to "the model improved itself" has left the evidence.

A neighbouring entry, accumulated-state-as-asset, concerns within-task
execution state and attempt history; this concept concerns cross-task
stored artifacts, and the two should not be merged.

## Relations

- [[projects/filingloop]] —shares-mechanism→ [[projects/garden]]:
  a frozen artifact, developed on some cases, applied unchanged to
  others — filingloop's updated guidance "applies only to later,
  unattempted tasks" with skills frozen per batch; garden's one program
  is applied unchanged to held-out scenarios of the family.
- [[projects/garden]] —shares-mechanism→ [[projects/hera]]:
  freeze-and-seal the artifact and the yardstick before measuring —
  garden's selected source "is frozen and hashed" under a rule fixed in
  advance; hera's corpus was "frozen under a git tag … before the first
  trial session", its conclusions sealed as hashes before each session.
- [[projects/evoteam]] —shares-mechanism→ [[projects/karma]]: both
  evolve persistent external knowledge from execution traces around a
  frozen model, then freeze and evaluate on untouched holdout.
- [[projects/molrsi]] —supports→ [[projects/karma]] and
  [[projects/molrsi]] —supports→ [[projects/evoteam]]: molrsi's
  pool-dependence ("transfer depends on which tasks contributed
  experience") supports the per-source reading of karma's transfer
  results and of evoteam's cross-context experience reuse.
- [[projects/hera]] —contradicts→ [[projects/agenticds]], on capability
  locus, each scoped to its own system: hera, model fixed, found the
  corpus carried quality; agenticds, scaffold fixed, found "a
  frontier-scale Critic is a prerequisite, not an optimization" — the
  model carried it. The contradiction is between the transferable
  lessons drawn, not the data, and it is the sharpest bound on this
  concept's generality.
- [[projects/molrsi]] —contradicts→ [[projects/evoteam]] is recorded
  with its typing disputed: the basis shows both pages *agreeing* on
  the underlying fact — improvement lives in stored guidance whose use
  depends on the frozen reader — so it stands as a mutual
  branding-bound rather than a factual contradiction.

## Open questions

- Does improvement in external state compound across repeated transfer
  steps — artifact carried to a second task family, improved there,
  carried again — or is every exhibit in this corpus a single
  develop-then-freeze cycle? No supporting page measures a second hop.
- Where is the reader threshold? EvoTeam's bound says the frozen model
  must be able to interpret the stored guidance, but no page varies the
  reader while holding the artifact fixed, so the minimum reader
  capability for a given artifact is unmeasured.
- The claimed side-benefits of the frozen locus — inspectability,
  reversibility, portability — are asserted by the systems' designs
  (karma's journaled edits and snapshot restore come closest) but never
  measured as outcomes in their own right. Whether they are real
  advantages or framing remains open.
- SkillCompiler's reuse claim rests on descriptive statistics, with no
  compile-fresh versus bank-reuse ablation; whether the *persistence*
  of program assets, as opposed to their validation, earns its keep is
  untested.

## Evidence status

This concept is the knowledge base's own analytical construct,
synthesized on 2026-11-02 in mining pass 1 from the KB's own deepened
project pages; it is not a term any single source paper uses for the
pattern. Mining pass 1 graded the candidate **strong**: seven
supporting pages, six of them non-vendor, spanning two clusters. Every
underlying result is author-reported from its source paper; none has
an independent replication recorded in this KB, and the one vendor
page (github-copilot-fusion) is weighted as architectural description
only. The bounds above — one null result, one disputed relation
typing, one capability-locus contradiction — are part of the concept's
record, not qualifications added later.
