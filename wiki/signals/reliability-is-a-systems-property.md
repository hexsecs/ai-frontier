---
uid: e5293fb7-2647-4963-b610-9fe02204e08b
depth: full
title: "Agent reliability is a systems property"
summary: "Reliability as a loop of verification, scoped recovery, and gated memory survives only in scoped form; its evaluation link grades itself."
type: signal
created: 2026-11-02
updated: 2026-11-02
sources: []
---

# Agent reliability is a systems property

## The hypothesis

The original page claimed that the imported projects suggest an engineering loop:

> plan → execute → verify → recover selectively → update skills and memory after regression checks → evaluate,

with orchestration and security constraining each stage. Its status line was explicit:

> **Hypothesis, not validated architecture:** these connections were mined from prior summaries and require source-level verification.

That source-level verification has now happened for the project corpus. This page tests the loop against the deepened project pages and the concepts mined from them in pass 1. The verdict is not a clean confirmation: most links have real evidence behind them, several survive only in a narrower form than the loop states, and one link — evaluation — is compromised in a way the original formulation did not anticipate.

## The loop, link by link

**Plan → execute.** The corpus does not test planning as such, but it tests what a plan-stage delivers. [[concepts/information-content-dominance]] records that information obtained *before* generation dominates everything after it: in [[projects/intent-loss-in-smart-contract-synthesis]], elicited answers were worth roughly twenty points of fidelity while post-generation stages added at most about one. [[projects/prefix-executability]] complicates this: plan-conditioned agents reached the highest final success while their trajectories were executable only about half the time — a plan can buy outcomes without buying clean execution. Supported, in the form: *what reaches the agent before it acts matters more than the loop around it.*

**Execute → verify.** This is the loop's best-evidenced transition, held in the register as verification-is-load-bearing. In [[projects/agenticds]], every configuration that removes the Critic falls below both agent baselines, and unchecked expansion actively lowers ranking quality. In [[projects/auctopus]], a run that met all ten precommitted accuracy criteria was still classified **inconclusive** because its controls failed — the verdict layer, not the result layer, decided. In [[projects/filingloop]], gains concentrated in the one role whose output is verifiable against a filing. The bound is [[concepts/scoped-assurance]]: a check warrants only the scope it exercised — [[projects/skillcompiler]]'s validated programs still fail roughly one invocation in nine (88.84% success), and [[projects/karma]]'s gate, below, passed patches that later regressed. Verification is load-bearing; it is not a guarantee.

**Verify → recover selectively.** Dittany and prefix-executability jointly support a verdict-triggered, scope-decided recovery step. [[projects/dittany]]'s runtime checkers label contributions satisfied, violated, or unestablished against a contract-derived contribution graph, and only violated or unestablished conditions trigger repair. [[projects/prefix-executability]] shows why the recovery step must be scored separately from success: its Recovery Rate measures success *conditional on* an invalid prefix, and on BFCL plain ReAct recovered at 0.00 while plan-conditioned variants recovered at 0.73–0.90 — the same final-success number can hide opposite recovery behaviour.

**Recovery itself.** This link survives only at graph scope. [[projects/dittany]]'s ablation is decisive: native execution scores 58.01%, action-level repair alone scores **52.54% — below doing nothing** — graph-level repair alone scores 69.17%, and the full system scores 84.76%. Adding graph scope to action-only repair is worth 32.21 points; the action scope's demonstrated value inside the combination is efficiency (374.9M vs 451.4M tokens), not standalone accuracy. "Recover selectively" therefore has a precise meaning the original page did not have: *scope decided by the dependency graph of contributions, not by where the failure surfaced.* Local retry is the weakest form of the link and can be net-negative.

**Recover → update skills and memory, after regression checks.** Two halves must be separated. The update half is [[concepts/improvement-lives-in-external-state]]: across [[projects/karma]], [[projects/molrsi]], [[projects/skillcompiler]], [[projects/evoteam]], [[projects/garden]], [[projects/hera]] and [[projects/filingloop]], improvement resides in edited external state around frozen weights. The regression-check half has a concrete mechanism in [[projects/karma]]: a patch "is retained if and only if" its validation gain clears a threshold, otherwise the pre-edit snapshot is restored, and the hold-out is never exposed to diagnosis, mutation or selection. [[projects/filingloop]]'s validate-or-keep and the test-gated admission of [[projects/clingex]] and [[projects/skillcompiler]] are the same shape. The gate is demonstrated — and, per [[concepts/scoped-assurance]], it "does not guarantee hold-out improvement": two of KARMA's eighteen settings regressed on hold-out after passing it.

**Update → evaluate.** This is the loop's weak point, and [[concepts/evaluator-circularity]] is why. The evaluate stage is not outside the system looking in; in much of the corpus it is inside it. [[projects/filingloop]]'s backbone is simultaneously its grader, matcher and skill editor; [[projects/dynarev]]'s constructor model is also its judge and its top strict-success scorer; [[projects/agenticds]]'s benchmark shares a graph with its retrieval engine. A loop that updates itself and then grades itself partly measures self-agreement. The escapes are narrow: KARMA's deterministic, non-LLM gate scorer avoids judge circularity (trading it for selection bias), and the one demonstrated remedy is a genuinely external audit — [[projects/intent-loss-in-smart-contract-synthesis]]'s previous scorer flaw surfaced through "four counterexamples an external audit found."

**Orchestration and security as constraints.** Supported as design, unmeasured as effect. [[projects/openbot]] makes the constraint architectural: a single policy gateway writes the audit row *before* any action runs — "there is no path that acts without the record existing first" — fails closed on a broken policy, and routes human takeover as the fallback; its shipped default, however, is allow-all until an operator writes policy, and it publishes no measurements. [[projects/dittany]]'s contribution graph is the orchestration-side instance: multi-agent contributions become checkable because their dependencies are explicit. Against both stands correlated-error-defeats-redundancy: in [[projects/explorerepair]], both intermediate aggregators adopted the same wrong assumption and the final aggregator followed them, discarding the correct fix — orchestration that merely aggregates ratifies shared error, and [[projects/vericua]]'s typed arbitration (20 wrong majority-vote fails against the arbiter's 2) is the counter-design.

## Evidence for

- Verification carries quality where it is ablated: removing AgenticDS's Critic drops every such configuration below both baselines; Auctopus's checker overruled a passing result on control evidence.
- Recovery at the right scope is worth a large margin: Dittany's graph scope is +32.21 points over action-only repair; the combined system reaches 84.76% against 58.01% native.
- Updates live in external state and can be gated: KARMA's snapshot-and-restore gate, FilingLoop's validate-or-keep, and test-gated admission in ClinGeX and SkillCompiler are working instances of regression-checked updating, with an untouched hold-out as the discipline that makes the check mean anything.
- Precommitment (register) supports the loop's credibility conditions: [[projects/hera]] sealed conclusions as hashes before each session and froze its corpus and grader in advance; [[projects/filingloop]] fixed denominators before execution.
- The constraint layer exists in buildable form: OpenBot's audit-before-act gateway and Dittany's contribution graph show orchestration and security as mechanisms, not slogans.

## Evidence against and bounds

- **Verification fails too.** [[projects/hera]] built the corpus's most complete verification apparatus — sealing, blinding, a frozen grader — and its blinded second-expert check still failed its own pre-sealed prediction: 65% exact agreement, κ = 0.38, against a predicted ≥0.70. Declaring a mitigation is not the mitigation working.
- **Recovery harms in its local form.** Dittany's action-only repair scores below no repair at all. The register's net-negative-interventions entry generalises the warning: [[projects/intent-loss-in-smart-contract-synthesis]]'s security-and-refinement loop *cost* 12.8 points of fidelity; DeepSeek assistance in [[projects/clingex]] scored below unassisted clinicians in two of three scenarios; [[projects/dynarev]]'s Reset + Rewrite strategy was the worst of all (0.525). An added stage is not evidence of improvement, and the no-intervention baseline is a required control.
- **Updates do not reliably steer.** [[projects/security-impact-of-coding-agent-memory-files]] is the null the loop must carry: planted memory files changed secure-completion rates by −8 to +6 percentage points, no consistent direction, inside the band the authors cannot distinguish from chance. Persistent state was present, loaded and adversarially written — and did not reliably move behaviour. Transfer can also be actively negative: KARMA's Automotive knowledge lowered every other domain's score.
- **Evaluation grades itself.** Per [[concepts/evaluator-circularity]], the loop's final stage is, in the limiting instances, the system scoring its own output with its own model against its own substrate. Any version of this loop that treats evaluation as an external verdict overstates what the corpus supports.
- **Scores are protocol-relative and standards are fallible.** Per [[concepts/protocol-relative-scores]] and [[concepts/ground-truth-fallibility]], the numbers each link rests on move with the measurement convention and are bounded by the standard's own error rate — magnitudes always, rankings often.

The hypothesis therefore survives only in a scoped form, stated precisely: **reliability is a systems property when each stage's warrant is kept inside its exercised scope — verification with diagnostic content and an independent-enough grader, recovery scoped by the contribution graph rather than the failure's location, updates admitted by a regression gate against an untouched hold-out, and evaluation treated as part of the system under test, not as an external judge. The unscoped loop — verify somehow, retry locally, update freely, self-grade — is contradicted: parts of it are inert and parts are net-negative.**

## What would settle it

The original page proposed: compare workflows with and without independent verification, contribution-level recovery, and regression-gated memory updates, measuring accuracy, wasted calls, recovery latency, and preserved work. The corpus sharpens that design in four ways, and records that **no page in the corpus runs it** — every link above is evidenced inside a different system, never in one loop with the stages independently toggled.

1. **Make it factorial and include the negative controls the corpus earned:** verification on/off, recovery at action scope vs graph scope vs none, updates gated vs ungated — with the no-intervention arm mandatory, because two of the corpus's interventions score below it.
2. **Fix the yardstick before outcomes exist** (precommitment): criteria, denominators and the grader frozen and sealed in advance, with the grader outside the system's own model family, so the evaluate stage does not reintroduce circularity into the experiment itself.
3. **Keep an untouched hold-out for the update arm,** evaluated once at the end, and report gate pass rates alongside hold-out regressions — KARMA shows the gate and the hold-out can disagree, and that disagreement is a result, not an embarrassment.
4. **Measure the original four quantities plus preserved work at contribution granularity** (Dittany's accepted-result retention is the model), so "recover selectively" is tested as scope selection, not as effort.

## Status

- **Plan → execute:** evidence-backed in its information form (pre-generation information dominates); planning as a stage in itself untested.
- **Execute → verify:** evidence-backed, with [[concepts/scoped-assurance]] as its standing bound.
- **Verify → recover:** evidence-backed as a trigger discipline (verdict-labelled contributions; recovery scored conditionally, not folded into success).
- **Recovery:** evidence-backed at graph scope; **contradicted in its strong form at action scope** (below the no-repair baseline).
- **Update after regression checks:** the update locus is evidence-backed ([[concepts/improvement-lives-in-external-state]]); the gate mechanism is demonstrated, its guarantee is not — and adversarially planted updates are a measured null.
- **Evaluate:** plausible as a stage, **compromised as practised** — [[concepts/evaluator-circularity]] makes it the loop's weakest link, escapable by deterministic scorers or genuinely external audit, neither of which is the corpus's default.
- **Orchestration / security constraints:** architecturally demonstrated ([[projects/openbot]], [[projects/dittany]]), effect unmeasured; aggregation without diversity is a documented failure mode, not a safeguard.

Overall: **hypothesis, link-tested, not validated architecture** — the original status line stands, narrowed: five of seven links now rest on named, deepened evidence, one is contradicted in its unscoped form, and the settling experiment remains unrun.
