---
uid: 201f9dbb-ee7c-4079-9ceb-7e9d3b00b089
depth: deep
title: "KARMA: Training-Free Knowledge-Atomic Harness Evolution for Industrial Advertising Agents"
summary: "Training-free evolution of six typed knowledge modules for an Alibaba advertising agent, gated by validation with snapshot rollback; offline log replay."
type: project
created: 2026-11-01
updated: 2026-11-02
related: [improvement-lives-in-external-state, scoped-assurance, validation-tier-gap]
sources:
  - url: https://arxiv.org/abs/2610.39884
    retrieved: 2026-11-02
---

# KARMA: Training-Free Knowledge-Atomic Harness Evolution for Industrial Advertising Agents

## What it is

KARMA (Knowledge-Atomic, Regression-Gated Modular Adaptation) is a training-free framework, from a team at Alibaba International Digital Commerce Group, for improving an advertising decision agent by evolving its external knowledge only. Model weights, business tools, and all executable harness code stay frozen throughout; the only thing that changes is a directory of typed knowledge modules that the agent's prompt is rendered from. The name's three load-bearing words are each literal: edits are *atomic* (small, schema-checked, individually journaled), retention is *regression-gated* (a candidate patch must improve a fixed validation set before it is kept), and the knowledge state is *modular* (six typed modules, each editable through a narrow interface).

The agent under improvement reads merchant and campaign telemetry through read-only tools and emits one structured advertising decision per case: an action type (budget, bid, or item), a direction (increase or decrease for budget and bid; add or stop for item), a rationale, and evidence identifiers. The evaluation data is real merchant data from AliExpress — roughly half a million July 2026 operation logs — but the word "industrial" in the title describes that data provenance, not a deployment. The paper states plainly that no advertising action is ever executed: the whole study is offline replay of logged merchant operations, and KARMA is "a research system evaluated offline without executing actions." There is no A/B test, no online metric, and no production KPI anywhere in the paper; deployment with guardrails and human oversight is named as future work. The work is an arXiv preprint (submitted 29 October 2026); no venue is established.

## Mechanism

The system has a frozen inner agent and an outer evolution loop that edits only the knowledge directory.

**Frozen inner agent.** A context builder renders the current knowledge state K into a prompt and a response schema — "(π_K, 𝒴_K) = Render(K)" — fixed within each trajectory. The agent follows a bounded two-stage protocol: it first collects evidence through whitelisted read-only business tools, then must make a standalone `finish_analysis` call before producing structured output. Traces record the knowledge fingerprint, tool queries and observations, the decision, the termination reason, and protocol-error codes; evidence identifiers must refer to successful tool responses.

**Typed modular knowledge.** K is a directory of six modules. Three are typed text modules: `role` (identity, objective, stance), `domain` (advertising products and operating semantics), and `output_protocol` (termination and structured-submission rules). Two are ordered rule lists of (stable rule id, source, text) triples: `experience` (reusable decision heuristics) and `constraints` (evidence, comparison, and safety requirements). The sixth, `action_descriptions`, holds field-level schema and local-tool descriptions and parameterizes both the response schema and the finish tool.

**Atomic, schema-checked edits.** An edit is a tuple (operator, module, optional rule id, value), with operators create, update, delete, and replace. A registry is the only write boundary: a `Valid` predicate schema-checks all six modules before anything is written, valid changes are written atomically and journaled with before/after values, and a fingerprint fp(K) identifies the resulting state. A cycle permits at most three mutations, evaluated together as one candidate patch.

**Deterministic trace verifier.** A non-LLM verifier partitions each batch's scored trajectories into full-credit successes, semantic failures, and infrastructure errors (errors score zero and are reported separately). Semantic failure classes are `no_action`, `wrong_action_type`, and `wrong_direction`. Two fixed, hand-written mappings route failures to candidate modules: wrong action type routes to {domain, experience}, wrong direction to {experience, constraints}, and a missing decision to {output_protocol, role}; a second mapping routes protocol codes (for example, malformed fields to `action_descriptions`). Failures are clustered by (reference operation, error class, candidate modules, protocol codes), successes by (operation, reference type, direction), and all batch records — successes and failures alike — are passed to the Critic.

**Critic and Evolver.** The Critic (an LLM) receives the verifier report plus compact trajectories and returns proposals of (failure mode, diagnosis, proposed change, target module, generality argument), comparing failures against successes from four perspectives: missing knowledge, conflicting rules, protocol timing, and ambiguous wording. It has no direct access to the knowledge. The Evolver (also an LLM, tool-constrained) turns the report and proposals into a patch of at most three atomic edits using CRUD tools only; it must inspect the current knowledge first, must avoid sample-specific identifiers, and is instructed to prefer no edit under uncertainty. It has no access to business tools, a shell, or the gate.

**Validation gate and rollback.** Before editing, the outer loop snapshots the entire knowledge directory. A cycle is gate-eligible only if semantic failures exist, the patch is non-empty, and the fingerprint changed. The candidate gain g_t is measured on a fixed validation set V, and the patch is retained if and only if g_t ≥ θ, with θ = 0.01 (one point on the paper's ×100 score scale); otherwise the pre-edit snapshot is restored — "on rejection or error, restoration returns the six-module knowledge directory to its pre-edit snapshot for subsequent batches." Validation scores are cached, so a run needs at most T+1 full passes over V instead of 2T. The hold-out set H is never exposed to diagnosis, mutation, or selection, and the initial and final knowledge states are each evaluated on H exactly once, at the end.

**Scoring metric.** The score is strict action agreement against the logged reference action: s = ½·𝟙[action type matches] + ½·𝟙[type matches ∧ direction matches]. Execution failures score zero and stay in the denominator. The paper is explicit about the metric's scope: "The metric measures agreement in action type and direction; it does not assess item-identifier accuracy, adjustment magnitude, rationale quality, or downstream business utility."

## Evidence

All results below are author-reported, from the authors' own runs on their proprietary, unreleased data. The evaluation setup is constant across them: offline replay; 800 cases sampled per domain from the ~500k-log corpus, split with seed 42 into 480 training cases in six batches of 80, 160 validation cases, and 160 untouched hold-out cases. There are six domains (Home & Living, Fashion & Apparel, Long-tail/Others, Automotive, Electronics & Office, Beauty & Health) and four reference operations (ADD_OFFER, DELETE_OFFER, UPDATE_BUDGET, UPDATE_PRICE). Three model families — Qwen3.8-Max, GLM-5.3, and Kimi-K3 — each fill all three roles (inner agent, Critic, Evolver) in their settings. Each main setting is run once from shared initial knowledge K_0, with θ = 0.01 and at most three mutations per cycle. No confidence intervals, error bars, or significance tests are reported anywhere.

**Main result.** Across the 18 domain–model settings, KARMA raised the average hold-out score from 30.19 to 39.15 (+8.96 points, +29.7% relative), improving 16 of 18 settings. Per-family average hold-out gains were +12.08 for Qwen3.8-Max (31.56 → 43.65), +8.91 for GLM-5.3 (28.85 → 37.76), and +5.89 for Kimi-K3 (30.16 → 36.04). Qwen3.8-Max and GLM-5.3 improved in every domain; Kimi-K3 improved in four of six. Note the absolute level: even after evolution, the agent's weighted agreement with the logged reference action is well under half.

**The gate does not guarantee hold-out improvement.** Kimi-K3 regressed on hold-out in two settings despite the gate — Automotive 40.31 → 37.19 (−3.13) and Electronics & Office 32.81 → 30.94 (−1.88) — each after a single early patch. The paper concedes the point directly: "The gate selects patches using observed validation scores and does not guarantee hold-out improvement." The gate screens regressions on a fixed 160-case validation set; it is not regression-proofing.

**Evidence ablation.** Using Qwen3.8-Max on three domains (Home & Living, Beauty & Health, Long-tail/Others), removing either evidence channel more than halved the average hold-out gain relative to the common base: +16.67 for full KARMA, versus +8.23 without successes and +6.56 without failures. Success-only consolidation still produced positive hold-out gains in all three domains — both channels carry signal, and neither alone recovers the full effect.

**Engine comparison.** Against alternative evolution engines — GEPA, AHE, and Self-Harness, all re-implemented by the KARMA authors on KARMA's own knowledge directory, mutation interface, and outer gate — KARMA gained more on both domains tested (Qwen3.8-Max only; Home & Living and Beauty & Health). On Home & Living its hold-out gain was +15.94, versus +9.06 for GEPA and +8.75 for AHE; on Beauty & Health it gained +18.13 while the strongest alternative, AHE, gained +6.56. GEPA and Self-Harness each showed a hold-out regression in one domain. Costs were comparable across engines: KARMA used 41.48M mean total LLM tokens per cycle and 4.53 hours per cycle, versus 42.15M / 4.58 h (GEPA), 40.74M / 3.40 h (AHE), and 40.72M / 3.60 h (Self-Harness).

**Cross-domain transfer.** With Qwen3.8-Max, the final knowledge evolved in each source domain was frozen and evaluated on the other five domains with no further mutation. The 30 source–target pairs averaged +8.54 points, about 71% of the average in-domain gain (+12.08); 23 pairs were positive and nine exceeded the target domain's own in-domain gain. Knowledge from Long-tail/Others transferred best, averaging +15.38 to every other domain — including +23.13 on Beauty & Health, against +18.13 from that domain's own evolution. The negative entries are concentrated: all seven involve Automotive. Automotive's evolved knowledge lowered the score of every other domain, while Automotive itself benefited more from several other sources than from its own evolution. Excluding Automotive as source or target leaves 20 positive entries averaging +12.73.

**Robustness checks.** On data seeds (Qwen3.8-Max, Electronics & Office only; seeds 42–46 controlling case selection, partition, and batch order — not LLM sampling), all five hold-out gains were positive, ranging +0.94 to +11.25 with mean +6.06; the headline seed 42 sat toward the upper end of that range. On gate thresholds (Qwen3.8-Max on three domains; θ ∈ {0.005, 0.01, 0.02}), five of six alternative domain–threshold combinations retained the default gains; raising θ to 0.02 cut Long-tail/Others' hold-out gain from +15.94 to +12.50, but every gain remained positive. The shared default θ = 0.01 was not selected using hold-out results.

**Rollback, demonstrated at the case level.** Across all runs there were 108 gated cycles. The paper works two of them in detail: an accepted Qwen3.8-Max cycle on Electronics & Office, where validation improved from 36.88 to 48.75 (+11.88) and the gate retained the patch; and a rejected Kimi-K3 cycle on the same domain, where the Evolver deleted rules E06 and E12 and rewrote E07, validation fell from 41.25 to 34.38 (−6.88), and restoration was triggered — "the rejected patch is never evaluated on H, so its hold-out effect is unknown." Rollback is therefore genuinely demonstrated as a mechanism; what is not reported is any aggregate accept/reject statistics across the 108 cycles — only these two case studies and gate-dynamics extremes.

## Limitations

Author-acknowledged limitations come first, then analyst-assessed ones; the two groups are labelled as such.

**Author-acknowledged:**

- The metric's scope is narrow by construction: agreement with logged actions "does not assess item-identifier accuracy, adjustment magnitude, rationale quality, or downstream business utility."
- "Logged actions may encode historical policy biases; agreement does not establish gains in revenue, welfare, or fairness."
- "KARMA is a research system evaluated offline without executing actions. Future work will consider deployment with business guardrails, monitoring, human oversight, and prospective evaluation."
- "Deterministic attribution may miss complex interactions, and repeated selection on a fixed validation set can favor changes that do not carry over to hold-out or transfer evaluation."
- "Each main configuration is run once; additional seed, threshold, and comparison studies cover selected settings."
- "Generalization beyond the sampled cases, period, and platform remains open."
- "The framework addresses external knowledge adaptation and cannot repair faulty tools or orchestration code."
- Because each model family fills the inner-agent, Critic, and Evolver roles, family differences "combine decision, diagnosis, and editing ability" — the design cannot separate them.
- Merchant and campaign identifiers are not released, and experiments rely on access controls and anonymized reporting.

**Analyst-assessed:**

- "Industrial" is provenance, not production evidence. There is no live deployment, A/B test, online metric, or business KPI in the paper; every number is offline agreement with logged historical actions.
- The half-million-log corpus is a sampling frame, not the evaluation size. Each setting is decided by 800 sampled cases, and every hold-out number rests on n = 160. Scores are per-case 0, 0.5, or 1, so a one-point (×100) difference is roughly 1.6 cases' worth of score; several reported effects (for example, Qwen3.8-Max on Automotive, +0.63 hold-out) sit at that granularity, and no uncertainty estimates are given.
- Single runs with uncontrolled LLM sampling. Each main configuration ran once, and even the seed study varies only data selection, partition, and order — explicitly not LLM sampling — with the headline seed toward the upper end of the one domain checked. Run-to-run variance of the headline +8.96 is unknown.
- The baselines are author re-implementations. GEPA, AHE, and Self-Harness were rebuilt by the KARMA authors on KARMA's own interface and gate, and GEPA's retention rule inside that harness differs from its published form; the comparison covers one model family and two of six domains.
- Rollback is well-evidenced as a mechanism (journaling, snapshots, gate-dynamics curves, one worked rejected cycle) but thinly evidenced as a statistic: no aggregate accept/reject rates across the 108 gated cycles are reported beyond the two case studies.
- Attribution is a fixed hand-written routing table, not a learned or validated diagnoser, and no experiment measures attribution accuracy itself. Diagnosis quality is likewise never independently measured — although the gate's scorer is the deterministic agreement metric, so there is no LLM-judge circularity in scoring.
- The improvement is fragile to the evidence pipeline: removing either evidence channel more than halves the average hold-out gain (+16.67 for full KARMA versus +8.23 without successes and +6.56 without failures in the ablation), so the headline effect depends on full ingestion of both successes and failures, not on either signal alone.
- Absolute performance stays low: the post-evolution average hold-out agreement of 39.15/100 means the evolved agent still disagrees with the logged reference on the majority of the weighted score. The +29.7% relative framing is accurate, but the absolute level is what an "industrial" reading should be judged against.

## Competing approaches

The paper compares KARMA head-to-head against three alternative evolution engines run as drop-in replacements under KARMA's own gate: GEPA (reflective prompt evolution), AHE (agentic harness engineering), and Self-Harness. At the framing level, it positions knowledge evolution against repeated fine-tuning (which changes weights rather than external knowledge), manual prompt maintenance, and whole-prompt rewriting by prompt optimizers such as ProTeGi, OPRO, and GEPA in its original form, as well as broad harness-code editing approaches such as ADAS, AFlow, and Meta-Harness, which KARMA deliberately forgoes by freezing all code. Named related work spans verbal-feedback and experience-accumulation methods (Reflexion, Self-Refine, ExpeL, Voyager), agentic context engineering (ACE), skill-evolution systems (RHO, RSIAgent, MetaSkill-Evolve), and gradient-free optimization frameworks (DSPy, TextGrad), plus harness-maintenance work (RHI, HarnessCompass, StarHarness, HarnessFix, HarnessBank). In the advertising domain specifically, the closest prior is RTBAgent for real-time bidding, while HAT and TaoLive represent the weight-training approach to live-commerce agents that KARMA's training-free stance is defined against.

## Implications

The strongest claim the evidence supports is a design claim: an agent's behaviour can be improved substantially — roughly nine points of action agreement on average, in these conditions — by editing only external, human-readable knowledge, with weights and code untouched. That matters operationally because knowledge edits are inspectable, journaled, and reversible in a way weight updates are not: the snapshot-and-restore gate gives an operator a concrete undo story for every accepted change, and the worked rejected cycle shows the undo actually firing. The typed-module structure also localizes blame: because failures are routed to specific modules and edits are atomic, the system produces an audit trail of what changed, why, and what it scored.

The transfer results add a second, more tentative implication: evolved knowledge is not purely local. Knowledge from the heterogeneous Long-tail/Others domain transferred better than several domains' own evolution, which suggests evolved heuristics partly encode general advertising decision structure rather than domain trivia — but the Automotive pattern cuts the other way, showing that one domain's evolved knowledge can be actively harmful everywhere else. Transfer is a property to measure per source domain, not to assume.

The caveats travel with the claims. The gate's failure to prevent two hold-out regressions, the more-than-halved gains when either evidence channel is removed, and the single-run, small-hold-out design together mean the headline numbers should be read as evidence that the mechanism works in this setting, not as a calibrated estimate of how much it helps. And because the score is agreement with historical logged actions, nothing here speaks to whether the evolved agent would make more money, or better decisions, than the policy that produced the logs. The verification discipline around the evolution loop is the transferable idea — see [[techniques/verification-and-evidence]] — more than the advertising results themselves.

## Reproducible experiment

A full reproduction is not possible from public artifacts: the paper gives no code URL anywhere in its text, references, or appendices, and the data is proprietary AliExpress merchant data that is not released. What can be reproduced is the *protocol*, on any logged decision corpus with a deterministic agreement-style metric:

1. Freeze an inner agent whose prompt is rendered entirely from a versioned knowledge directory; snapshot the directory before every edit cycle.
2. Run the agent over training batches; score each case with a strict, non-LLM metric (here, half credit for action-type match, full credit only when direction also matches; execution failures score zero).
3. Partition failures deterministically and route them to knowledge modules with a fixed mapping; have an LLM Critic propose module-targeted changes and an LLM Evolver emit at most three schema-checked atomic edits per cycle.
4. Accept the patch only if a fixed validation set improves by at least θ = 0.01; otherwise restore the snapshot. Keep a hold-out set untouched by every part of the loop and evaluate the initial and final knowledge on it exactly once.
5. Ablate the evidence channels (successes only, failures only, both) and sweep θ; the paper's signature results to check are that removing either channel more than halves the gain, and that validation-gated acceptance still permits occasional hold-out regressions.

The run artifacts the paper describes recording — split membership, traces, scores, knowledge states, mutation journals, fingerprints, gate decisions — are the right checklist for an independent implementation, but the paper states that identifiers, proprietary tool responses, and credentials are excluded from public reporting, and no artifacts were available to inspect for this page.

## Evidence status

Every result on this page is author-reported. All numbers come from the authors' own runs, on their own proprietary and unreleased data, against baselines the authors themselves re-implemented; no independent replication is mentioned in the paper, and none is possible from public artifacts, since neither code nor data is available. Internal validity is comparatively careful for an unreplicated preprint — an untouched hold-out evaluated exactly once, a full-ingestion ablation over both evidence channels, an engine comparison under a shared gate, a full cross-domain transfer matrix, and seed and threshold sensitivity checks — but all of it is single-team, single-platform, single-month (July 2026 logs) evidence, with each main configuration run once and no uncertainty estimates reported. The venue status is unestablished: this is an arXiv preprint whose HTML rendering still carries an unedited conference-template placeholder.

## Historical coverage

[Briefing 2026-11-01](../briefings/2026/11/2026-11-01.md)
