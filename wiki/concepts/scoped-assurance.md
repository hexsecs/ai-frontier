---
uid: e23e48f4-2e1c-4f72-a00c-0a33c4f233f7
title: "Scoped assurance"
summary: "A verification result holds only inside the scope actually exercised; its headline number routinely outruns that scope and gets read as a guarantee."
type: concept
depth: full
created: 2026-11-02
updated: 2026-11-02
related: [skillcompiler, intent-loss-in-smart-contract-synthesis, webanything, dynarev, clingex, karma, envos, pre-crime-for-agents, aisoc-v21, prefix-executability, openbot]
sources:
  - url: https://arxiv.org/abs/2610.39508
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.37830
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.37786
    retrieved: 2026-11-02
  - url: https://arxiv.org/abs/2610.39884
    retrieved: 2026-11-02
---

# Scoped assurance

## What it is

Scoped assurance is the discipline of reading every verification result as a claim about exactly the set that was exercised — and nothing beyond it. A check never tests "the system"; it tests a specific, enumerable scope, and the result's warrant ends at that scope's edge. The scope dimensions recur across the KB's project pages:

- **Exposed mistakes** — the planted errors a test sequence actually surfaced, as opposed to all errors planted.
- **Tested inputs** — the cases a program or procedure was validated on, as opposed to arbitrary inputs it may later meet.
- **Reviewed instances** — the sites, cases, or artifacts actually inspected, as opposed to the full inventory a headline counts.
- **Validated judges** — whether the instrument issuing the verdict was itself ever checked against a human or ground-truth reference.
- **The checked set a gate selected on** — the validation set an acceptance gate optimized against, as opposed to the untouched hold-out it never saw.
- **Declared checks and calibration episodes** — the obligations a certification actually ran, and the episodes a detection threshold was tuned on, as opposed to future trajectories and fresh episodes.

The failure mode is rarely fabrication. The number is usually real *inside* its scope. The overclaim happens in the retelling: the scope qualifier drops away, and "passed the checks that were run" is silently read as a guarantee about unseen instances — unexposed mistakes, untested inputs, unreviewed sites, unvalidated judges, unobserved hold-outs. Scoped assurance names the habit of refusing that upgrade: the qualifier is part of the result, and a result quoted without it is a different, stronger claim than the one that was earned.

## Evidence for

**SkillCompiler — validated programs, untested inputs.** SkillCompiler compiles skill operations into programs that must pass validation before admission, and its own text bounds what that means: validation tests are "evidence of local behavior, not exhaustive branch coverage or semantic equivalence on arbitrary inputs". The bound is measurable: "Program Invocation Success is 88.84% — roughly one in nine invocations of a validated program still fails". "Validated" certifies behaviour on the exercised inputs; the remaining one-in-nine failure rate is what the word does not cover.

**Intent-loss — rates over exposed mistakes only.** The smart-contract synthesis study plants 279 mistakes and measures how often an oracle catches them — but a mistake can only be caught if some test sequence exposes it. Quoted over exposed mistakes, the best oracle scores 87.5%; "counting mistakes no sequence exposes, the best oracle's rate over all 279 planted mistakes is 65.2%, not 87.5%." Both numbers are correct; they differ only in scope, and the headline form is the larger one.

**WebAnything — inventory versus validated quality.** WebAnything's headline count is 244 reconstructed website artifacts, but the deep quality evidence covers a small matched subset. The register's phrasing: "The headline '244 artifacts' is an inventory count, not a validated-quality count". The scope that was exercised is the reviewed subset; the number that circulates is the inventory.

**DynaRev — headline metrics on unvalidated judges.** DynaRev's results rest on two instruments: a constraint-verification judge and a WRA judge. "No human-agreement study is reported for the constraint-verification judge or the WRA judge, which carry all headline metrics." Here the unexercised scope is the judge itself: the verdicts are only as warranted as an instrument that was never validated against human agreement.

**ClinGeX — a home-field benchmark.** ClinGeX's benchmark cases are drawn "from exactly the five resources whose procedures the skill library was purpose-built to encode". Passing inside that scope shows the library handles the resources it was built from; it says little, without further evidence, about cases sourced from elsewhere.

**KARMA — the gate that does not guarantee.** KARMA's acceptance gate retains knowledge patches that improve a fixed validation set. The paper states the bound itself: "The gate selects patches using observed validation scores and does not guarantee hold-out improvement." The bound is not hypothetical — two of 18 settings regressed on hold-out despite passing the gate. (The register records this page's alias for the concept: gate-is-not-a-guarantee.)

**EnvOS — certification as admission, not proof.** EnvOS certifies environments before agents run in them, and is explicit that certification is admission on the declared checks, "not a proof that every future model trajectory will be correctly handled". The caution proved concrete: the certified pipeline had already issued scored verdicts under defective code, inside a process whose whole purpose is pre-run assurance.

**Pre-Crime — thresholds that fail to transfer.** The disclosure probe's decision threshold was calibrated on training episodes. "Thresholds also fail to transfer: a threshold set on training episodes flags 29% of refusing test episodes instead of about one in twenty." A threshold is a verification result too, and its warrant is scoped to its calibration set.

## Evidence against and bounds

The concept is a discipline with good and bad instances, not a universal accusation — several pages in the same corpus use the discipline correctly, and some of the pages above also resist the failure they name.

**MoLRSI is the disciplined counter-design.** Its search never consumed the outcomes it was later judged on: "Test outcomes were not used in search", and its central ablation holds "library, backbone and budget fixed and toggles only memory access" — the claim scoped to exactly what the untouched set can show. Nothing in the result invites a reading beyond the exercised scope, because the scope was protected by construction.

**KARMA partly resists its own failure mode.** Its hold-out "is never exposed to diagnosis, mutation, or selection"; the gate overclaims only when a reader upgrades "passed validation" to "will generalize". The paper does not make that upgrade — it states the non-guarantee in its own text.

**Honest scoping is on-page, and praised.** WebAnything's counting discipline and intent-loss's coverage reporting were both flagged by their own miners as templates: intent-loss publishes the 65.2% figure alongside the 87.5% figure, and webanything separates its inventory count from its validated subset. The concept, as the register puts it, is that the scope qualifier is load-bearing — not that verification is fake.

## Relations

Typed relations recorded in the mining register (pass 1, Part 2) that bear on this concept:

- [[projects/clingex]] —shares-mechanism→ [[projects/skillcompiler]] — test-gated admission of reusable components: only skills passing all frozen tests entered ClinGeX's deployed library; SkillCompiler requires revalidation of an affected realization "before admission" on any change. The gate is the shared mechanism whose warrant this concept scopes.
- [[projects/intent-loss-in-smart-contract-synthesis]] —shares-mechanism→ [[projects/webanything]] — a checker separated from the producer: intent-loss's reference models flag disagreements and never score; WebAnything's candidate is frozen and examined by an Independent Verifier that cannot edit candidate code. Separation widens what a check can credibly cover, but does not widen the exercised set.
- [[projects/envos]] —supports→ [[projects/pre-crime-for-agents]] — EnvOS's grader-audit results support Pre-Crime's premise that the measurement instrument must itself be validated before its verdicts are used; both pages treat judge validation as part of the exercised scope, not an assumption.
- [[projects/clingex]] —same-failure-mode→ [[projects/dynarev]] — the judge is the contestant's own model family, in construction, judging, and evaluation; the validated-judges scope dimension fails on both sides of the pair.
- [[projects/intent-loss-in-smart-contract-synthesis]] —same-failure-mode→ [[projects/clingex]] — self-grading inside the evaluated loop: intent-loss's original pipeline "grades itself with an LLM rubric judge"; ClinGeX's ablation items were generated and scored within the evaluated core's own model family.
- [[projects/karma]] —same-failure-mode→ [[projects/skillcompiler]] — both anchor this concept from the gate side (KARMA's gate non-guarantee; SkillCompiler's 88.84% invocation success after validation). The register records this pair as *suspected — unverified*, inferred from shared concept membership across clusters, and it is carried here with that flag.

Sibling concepts, named in plain text: this entry is distinct from **precommitment**, which concerns locking the yardstick *before* outcomes exist — scoped assurance concerns the warrant of a result *after* the check ran, however well it was locked. It is also distinct from **validation-tier-gap**, which concerns a project's framing inviting a stronger evidence tier than its measurements occupy; scoped assurance concerns a specific check's result quoted beyond the set it exercised. ClinGeX's home-field benchmark also appears under **construct-validity-leakage**, and the unvalidated-judge cases border on **evaluator-circularity**.

## Open questions

- What reporting convention would make the scope travel with the number — denominators, exposure rates, and validated-subset counts stated wherever the headline appears — and would readers actually discount headlines that lack them?
- KARMA's gate reports its threshold; should acceptance gates also be expected to report the size and provenance of the checked set they selected on, as part of the result?
- Pre-Crime's threshold degradation (29% flagged versus roughly one in twenty expected) was found empirically, after the fact. Is transfer failure of a calibrated threshold predictable from properties of the calibration set, or only discoverable by re-exercising scope on fresh episodes?
- Within this KB, is there a project whose headline number is scope-complete — stated over the full set it appears to describe — or is some degree of scope shrinkage present in every headline the corpus contains?

## Evidence status

This concept is the KB's own analytical construct. No paper in the corpus names it. It was synthesized on 2026-11-02 in mining pass 1 from the KB's deepened project pages, and graded strong in the register (8 supporting pages across 2 clusters) on the strength of the quoted passages above. Every underlying result is author-reported in the source papers; the concept asserts no new measurements, only a reading discipline over results the pages themselves publish. The one relation flagged *suspected — unverified* in the Relations section is carried with the register's own flag and is not asserted here.
