---
uid: d12d24de-6caf-423c-8b4c-bff192d3ce46
title: "Validation-tier gap"
summary: "A system's framing claims a higher validation tier — physical, production, independent — than the tier its evidence actually occupies."
type: concept
depth: full
created: 2026-11-02
updated: 2026-11-02
related: [tinyastral, openbot, context-as-infrastructure, github-contribution-check, karma, molrsi, pre-crime-for-agents]
sources:
  - url: https://arxiv.org/abs/2610.41216
    retrieved: 2026-11-02
  - url: https://arxiv.org/html/2610.41216v1
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39884
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39714
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.40588
    retrieved: 2026-11-02
---

# Validation-tier gap

## What it is

Every result sits at some tier of validation: a physical trial outranks a simulation, a production deployment outranks an offline replay of logged actions, an independent check outranks a design document, a measured verdict-quality study outranks operational telemetry. A validation-tier gap exists when a project's headline framing — its title, its genre words, the setting its presentation evokes — claims one of the higher tiers while its measurements actually occupy a lower one. The numbers may be perfectly valid *at their tier*; the gap is between the tier the framing invites the reader to assume and the tier the evidence earns.

The gap is a property of presentation, not of measurement quality, and it is only visible when both tiers are stated side by side: the framing tier ("industrial", "physical robotics", "forecasting", "enforced governance") against the measurement tier (offline agreement with logged actions, simulation, computational ablation, last-second detection, a design ledger, cost telemetry). Where a source discloses both, a careful reader can see the mismatch without any outside audit — which is why most instances below are documented in the pages' own words.

Two neighbouring concepts mark the boundary. Scoped assurance is about a specific check's result outrunning the set that check exercised; the tier gap is about a whole project's framing outrunning the tier of its evidence as a body. Claims-are-not-evidence is about assertions offered with no evidence behind them; here evidence exists and may be sound — it simply sits lower than the framing implies. Nor is this the proxy failure mode: the instruments in these pages generally measure the quantity they claim to measure. What they do not do is measure it where the framing says the system lives.

## Evidence for

**TinyAstral** is the purest form in the corpus. The framing tier is physical robotics — a self-evolving harness transferred to a real manipulation agent — but the KB page records that "**Physical evidence is qualitative only.** Despite the robotics framing, every number is simulated; the real SO-ARM101 runs … appear as trajectory figures with no success rates or trial counts." Every quantitative claim in the paper occupies the simulation tier; the physical tier is present only as pictures. It is the shape the register first found in KARMA, one tier further removed.

**OpenBot**'s gap is total, and the project states it itself. The framing tier is enforced governance — a policy gateway standing between an agent and the world — while the measurement tier is empty: "**There are no performance measurements to report, and that absence is the finding.**" There is no lower-tier evidence to mismatch; the tier where governance efficacy would be measured is simply unoccupied.

**Context-as-Infrastructure** frames itself as deployed compiled-context infrastructure. On its own deployment ledger, six of seven artifact families report *no measured effect* — for those families the measurement tier is a design document: the artifact is specified, its intended effect described, and the effect itself unmeasured.

**GitHub Contribution Check** is framed as compliance review — a checker rendering verdicts on contributions. Its evidence tier is operational telemetry: three runs of cost, turn, and API-call figures, with "no accuracy evaluation of the checker's verdicts against human judgment". Telemetry occupies the tier where verdict-quality evidence would sit; it shows the checker ran, not that its verdicts are right.

The three founding instances come from cluster D. **KARMA** carries "industrial" in its framing, but the word denotes "data provenance, not a deployment": "KARMA is a research system evaluated offline without executing actions", and every number is offline agreement with logged historical actions. **MoLRSI** shows both directions on one page: its wet-lab results are genuinely at the physical tier, but "those physical results validate the workflows MoLRSI produced; they do not, by themselves, validate the self-improvement loop — the RSI claim rests on computational ablations". The headline claim (recursive self-improvement) is evidenced a tier below the claim the physical results actually support. **Pre-Crime for Agents** claims forecasting in its title, against its own numbers: episode-level "will this episode ever leak" scores are 0.53 and 0.61 — "the last is near chance" — while the supported claim is per-call detection at the leaking call itself, a last-second measurement wearing a prediction's framing.

## Evidence against and bounds

The strongest bound is that the corpus also contains pages that practise tier discipline, so the gap is a per-page property, not a corpus habit. Cluster E supplied the counterweights. **AiSOC v21** labels its own evaluation suites tautological and marks its unmeasured configuration row "not measured" rather than letting a blank read as a result. **ANGLER** states plainly that "the nine websites are finite-state-machine-generated clones built on AutoWebWorld, not the real Coursera, Facebook, or other named services" — the framing tier is named and disclaimed in the same breath. **Prefix-executability** runs the transfer audit that downgrades its own intervention, publishing the setting where its headline effect weakens. **BlindToChange** states on its page that the evaluation ran against the live web, so exact numerical reproduction of its results table is not expected — the measurement tier's limits are declared where the numbers are. Cluster E's one nearby overreach, BioAgent's "self-directed" framing, sits on the autonomy axis, not the evidence-tier axis this concept defines. Pass 2's verdict on the cluster was explicit: E weakens the hypothesis that the gap is a corpus-wide presentation habit. The register's original counter-example makes the same point from cluster D: **EnvOS** "explicitly refuse[s] to pool its results into a model ranking" and scopes its claims to "within-configuration review-information effects, not the effect of making a static environment dynamic" — framing discipline is available, and some authors exercise it.

Second, no framing deception is required for the gap to exist. A gap is a mismatch between two tiers, and both can be fully disclosed: MoLRSI's page states the ablation basis of its loop claim in its own text; KARMA's offline scoping is author-acknowledged; OpenBot's missing measurements are the project's own headline admission. This is what separates the tier gap from claims-are-not-evidence: nothing here requires an assertion without support, and nothing here is cured by adding *more* evidence at the same lower tier.

Third, a gap is therefore not an accusation of overclaiming. Where the source itself discloses the tier — as several instances above do, in the source's own words — the mismatch is visible precisely because the disclosure exists. The concept names the distance between framing and evidence; whether that distance misleads depends on whether the reader is shown both ends of it, and in most instances here, they are.

## Relations

- [[projects/tinyastral]] —same-failure-mode→ [[projects/karma]] — the pass-2 miner maps TinyAstral directly onto KARMA's shape: a provenance word ("industrial") or genre framing (physical robotics) claims a tier the measurements do not occupy; TinyAstral sits one tier further removed, simulation standing in for physical runs where KARMA's offline replay at least replays real logged actions.
- [[projects/molrsi]] —bounds→ the concept from inside an instance: its page separates its own claims by tier, assigning the physical results to the workflows and the computational ablations to the loop — an instance that also demonstrates the disclosure that bounds the concept's force.
- [[projects/openbot]] —limiting case→ the concept: the measurement tier is not lower but empty, which the project itself reports; the gap's maximum extent, self-declared.
- [[projects/envos]] —counter-example→ the concept (named in text in the bounds section above): deliberate framing restraint, refusing the pooled ranking its results might have invited.
- Distinguish from scoped-assurance (a check outrunning its exercised set, not a framing outrunning an evidence tier) and from claims-are-not-evidence (no evidence, rather than evidence at a lower tier than the framing implies), both named here in text.

## Open questions

- Does the size of a page's tier gap predict how its numbers travel — are results from high-gap pages cited downstream at the framing tier rather than the measurement tier? Nothing in the corpus measures this.
- How much of a gap is the text's claim and how much is the reader's inference? Where the framing tier is set by a single word ("industrial", a title's "Pre-Crime"), the boundary between the author's framing and the reader's assumption is itself a judgment call.
- Would a stated-tier convention — every headline number tagged with its measurement tier — close these gaps, and would the authors of the disciplined pages (EnvOS, AiSOC) recognise it as a formalisation of what they already do?
- Is the gap stable across versions? TinyAstral's physical tier could be populated by later runs with trial counts; whether framing-first projects close the gap with measurements, or the framing simply becomes the record, is an empirical question the KB can revisit as these projects publish again.

## Evidence status

This concept is the KB's analytical construct, synthesised from the KB's own deepened project pages in mining passes 1 and 2 (2026-11-02); no paper names it, and every underlying result is author-reported. Its history inside the mining process is part of its status and is kept visible here deliberately: pass 1 graded it medium on three pages from a single cluster (cluster D) and deferred it, because the miner who proposed it flagged it as **the candidate closest to an editorial judgment rather than a domain phenomenon**. Pass 2 promoted it only when cluster F supplied four further instances, in the pages' own words and across multiple genres (preprint, vendor paper, open-source project, vendor workflow), while cluster E supplied counterweights showing the pattern is not universal. That promotion history does not retire the original warning. Assigning a tier to a framing is a reader's judgment in a way that, say, identifying a shared judge model is not; each instance on this page is anchored to the page's own words, including author-acknowledged scopings, but the construct sits one step nearer interpretation than the KB's other concepts, and it should be weighed accordingly.
