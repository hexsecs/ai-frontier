---
uid: 6ef323df-97a9-449e-8852-16465523f8a6
depth: deep
title: "ANGLER: Verifier-Grounded Benchmarking with an Adaptive Attacker for Web Agents"
summary: "REEF benchmarks web-agent prompt-injection vulnerability on nine executable sites; ANGLER, an adaptive attacker, raises attack success from 15.24% to 20.36%."
type: project
created: 2026-11-02
updated: 2026-11-02
related: [comparator-construction-shapes-margins, improvement-lives-in-external-state, protocol-relative-scores]
sources:
  - url: https://arxiv.org/abs/2610.41272
    retrieved: 2026-11-02
  - url: https://arxiv.org/html/2610.41272v1
    retrieved: 2026-11-02
---

# ANGLER

## What it is

This is an arXiv preprint (arXiv:2610.41272, submitted 30 October 2026; no peer-reviewed venue stated) by Yini Huang, Aiwen Lu, Zhen Sun, Yi Han, Yuzhi Zhao, and Jiaheng Wei, from the Hong Kong University of Science and Technology (Guangzhou) and Huazhong University of Science and Technology. It makes two paired contributions, and the page treats them separately because several headline properties belong to one or the other: **REEF**, a benchmark of executable websites for measuring web-agent security, and **ANGLER**, an adaptive prompt-injection attacker evaluated inside REEF.

The paper's framing is that web agents increasingly complete tasks autonomously on real websites, where adversarially injected content can induce them to perform unauthorized actions — sending an unauthorized message, modifying an account setting, completing an unauthorized transaction. Existing evaluations, the authors argue, primarily use fixed attacks or a single attack type, and evaluate attacks at the text level rather than through real state changes, thus underestimating vulnerability. REEF (a benchmark of "Red-teaming Executable Environments with Faithful Verification") addresses the measurement half: 9 verifier-grounded websites, 8,316 executable cases, and 326 instantiated malicious objectives (from 72 templates), with success read from programmatic state-based verifiers rather than text matching or LLM judging. ANGLER (an "Adaptive Near-miss-Guided Lure Evolution framework for Red-teaming") addresses the attack half: instead of a fixed attack set, it mutates attacks with an LLM and selects among candidates with a contextual bandit, using verifier feedback from prior rollouts and prioritising *near-miss* seeds — attacks that achieved their malicious effect transiently but not at termination.

The pairing is deliberate. The paper argues that simply adding an adaptive attacker to existing benchmarks is insufficient, because newly generated attack plans must be validated against specific constraints and evaluated under consistent task contexts, objective definitions, and verifier rules. REEF therefore supplies a fixed benchmark specification with a site compiler that enforces plan validity, and ANGLER supplies adaptive search inside that specification.

The dual-use framing is the paper's own and is recorded here as stated. The work is presented throughout as benchmarking and red-teaming for measuring vulnerabilities, and containment is by construction: all experiments run in isolated and resettable benchmark environments using synthetic accounts, entities, and malicious objectives, with — in the words of the ethics and privacy statement — "no attacks directed at public services, real users, or real accounts," and no personal data collected. The nine "websites" are synthetic clones, and the attacker's action space is restricted to a predefined feasible space enforced by the site compiler. The paper contains no discussion of release gating, misuse risk beyond that ethics statement, or defensive recommendations.

## Mechanism

**REEF: environments and tasks.** The 9 stateful, resettable websites are built on AutoWebWorld and span five domains (travel, commerce, productivity, media, communication): Coursera, Facebook, GitHub, Headspace, JD, Skyscanner, Slack, Walmart, and YouTube (site names as printed in the paper). Sites run isolated with synthetic users and content, enabling state-changing interactions without affecting public services. Each site's workflows are modelled as a finite-state machine; breadth-first search from the reset state enumerates valid paths to goal states, and those paths become parameterised benign-task templates instantiated with site entities. Each benign task receives a programmatic user verifier. The 326 malicious objectives fall into five effect categories: browsing/navigation (108; 33.1%), content publishing (70; 21.5%), transactional commit (55; 16.9%), account configuration (51; 15.6%), and lightweight action (42; 12.9%), with estimated minimum action horizons split roughly evenly across short (≤6 actions), medium (7–9), and long (≥10). One objective instance can pair with multiple compatible benign tasks and attack configurations, which is how 326 objectives generate 8,316 executable cases.

**Attack plans and types.** An attack plan is a tuple of attack type, malicious objective, delivery specification, optional injection surface, injection timing, and site-valid content/presentation parameters. There are five attack types. One is user-level: *direct prompt injection*, where an adversarial payload is appended to the authentic user instruction and the website is unchanged. Four are environment-level, leaving the instruction unchanged and injecting content into the webpage: *indirect prompt injection* (payload embedded in ordinary page content such as a post or support message, in native presentation), *pop-up injection* (a modal overlay framing a call-to-action as a required verification, security check, or workflow prerequisite), *distraction injection* (a non-modal notice or banner claiming the page state is outdated or needs synchronisation), and *ad injection* (payload in an advertising or sponsored surface with promotional framing). Environment-level attacks use two-phase delivery: an initial-phase injection presents a call-to-action (CTA) intended to make the agent navigate to a target page, and a continuation-phase injection on the destination page then pushes completion of the malicious objective.

**Compilation and verification.** A site compiler instantiates templates with registered site parameters and builds the verifier specifications; static validation rejects undefined templates, entities or surfaces, incompatible task–objective pairs, invalid timing or payloads, and payload–objective inconsistencies. Only validated cases are eligible for rollout — this compiler check is also ANGLER's plan-validation step. Outcomes are determined "directly from recorded website states rather than relying on agent self-reports or LLM-as-a-judge scoring." Three programmatic verifiers score each case: a user verifier (benign objective achieved), an attacker verifier (malicious objective achieved *and still satisfied at termination*), and a recovery verifier (a malicious effect seen earlier is absent at termination), which together separate never-successful, recovered, and successful-at-termination attacks. A pre-check requires the attacker verifier to be false in the reset state, so a pre-existing effect cannot count as success. A separate CTA metric records, for environment-level rollouts, the fraction in which the agent activates the registered CTA, taken from the interaction event and page transition rather than self-reports; CTA captures an intermediate stage, while attack success requires the final state.

**Threat model.** The adversary's goal is to induce a malicious objective not authorised by the authentic user goal. The attacker may vary payload, delivery configuration, injection surface, timing, and presentation within the predefined feasible attack space, and objectives must be site-supported. After each rollout the attacker receives execution-level feedback — verifier outcomes and attack-progress signals — but has no access to the target model's parameters, hidden states, or private reasoning, and cannot modify the agent implementation, website logic, verifiers, or reset procedure.

**Target agents.** All targets run the VisualWebArena agent scaffold with an identical observation interface (multimodal accessibility tree plus viewport screenshot), action space (10 ID-based browser actions), prompt structure, and interaction horizon; only the vision-language backbone varies. Eight backbones are evaluated, with model names as the paper prints them: GPT-4o, GPT-6.1 Sol, Claude Sonnet 4.5, Claude Sonnet 5.5, Qwen3-VL, Qwen3.7-Flash, GLM-4.6V-Flash, and GLM-5V-Turbo. Browser state is cleared and the site reloaded before each rollout.

**ANGLER: scheduling, mutation, selection.** A two-stage scheduler runs the search. In the *coverage stage*, with an empty experience pool, ANGLER systematically evaluates feasible benign-task-template × attack-type pairings, prioritising pairings below their coverage quota and least-used instruction instances — forced exploration intended to mitigate cold-start bias. In the *adaptive stage*, the benign template is chosen uniformly and scheduling is independent of past outcomes, so budget cannot concentrate on easy contexts; within the assigned attack level, the bandit picks the attack type and delivery configuration.

After each rollout, a record (plan, verifier outcomes, benign completion, funnel signals) enters an experience pool under one of four categories: *Success* (objective satisfied at termination); *Near-miss, benign incomplete* (objective achieved transiently, not at termination; benign task incomplete); *Near-miss, benign complete* (transient achievement; benign task completed); and *Blocked* (objective never achieved). The rationale is that near-misses show an attack induced its effect at least transiently and so locate the remaining bottleneck. Seed sampling retrieves records for the same benign instruction (else the same template) and switches weightings by evidence: a low-evidence regime (few records or low running success) favours verified successes, while a refinement regime prioritises near-misses, weighting benign-incomplete near-misses highest because they best evidence that the attack diverted the agent from its task. All weights stay positive, so any category can be sampled.

Mutation is performed by an LLM — Qwen3.5-9B, fixed across all target agents. The program assigns each candidate slot a catalog malicious objective with its parameters; the LLM decides only how the objective is expressed and delivered. A mutation router directs revisions by failure stage: for user-level failures, revise the injected instruction; for environment-level failures, revise placement or timing if the injection was not observed, CTA wording or visual salience if it was observed but not engaged, and continuation instructions if the malicious path was reached but the objective not completed. Output is a constrained JSON schema — payload overrides, catalog-supported delivery parameters, an integer display delay, whitelisted surface styles. The model may not introduce new objective parameters, entity identifiers, routes, verifier rules, rendering logic, HTML, or arbitrary CSS. Invalid, duplicate, or uncompilable mutations are dropped; unfilled slots receive catalog candidates passing the same compiler validation.

Selection is a contextual bandit over a fixed-dimensional feature vector encoding website, benign instruction and template, seed category, objective, attack type, delivery configuration, and mutation provenance (plus timing and phase surfaces for environment-level candidates), with signed feature hashing so outcomes update weights shared by overlapping candidates. User-level selection uses logistic Thompson sampling with a Laplace-approximated posterior. Environment-level selection is *funnel-aware*: two logistic Thompson-sampling models, a gate model (will the agent engage the initial CTA?) and a completion model (will the objective succeed?), score candidates by the product of the two probabilities over phase-specific feature views. The gate posterior updates on every environment-level rollout; the completion posterior updates only when the CTA was engaged — so engagement without success is positive for the gate model but negative for the completion model, and a rollout with no engagement leaves the completion model unchanged.

**Baseline.** The non-adaptive comparator constructs candidate attacks supported by the current website, filters them through the same compiler, and "selects one of the remaining candidates uniformly at random," with matched task contexts and identical rollout budgets (100 rollouts per website per backbone). This matters for reading the results: the comparison isolates adaptivity against random selection from the same validated candidate pool, not against another adaptive attacker.

## Evidence

All results in this section are author-reported from the single paper; the main evaluation is 100 rollouts × 9 websites × 8 backbones = 7,200 rollouts per attacker condition.

**Headline.** ANGLER achieves an average attack success rate (ASR) of 20.36%, against 15.24% for the non-adaptive baseline — an absolute improvement of 5.12 percentage points, a 33.6% relative improvement. Because the baseline selects uniformly at random among compiler-valid candidates under matched budgets, this contrast measures adaptivity versus random search within REEF's feasible attack space; it is not a comparison against the strongest alternative attacker (see Limitations and Competing approaches).

**Per-backbone results** (average ASR across the 9 websites, non-adaptive → ANGLER; ANGLER CTA rate also shown):

| Backbone | Non-adaptive ASR | ANGLER ASR | ANGLER CTA |
|---|---|---|---|
| GPT-4o | 25.4% | 41.2% | 74.6% |
| GPT-6.1 Sol | 6.9% | 9.7% | 4.1% |
| Claude Sonnet 4.5 | 13.1% | 17.2% | 69.1% |
| Claude Sonnet 5.5 | 8.0% | 15.2% | 1.9% |
| Qwen3-VL | 11.6% | 14.6% | 41.1% |
| Qwen3.7-Flash | 16.4% | 17.0% | 47.4% |
| GLM-4.6V-Flash | 8.8% | 10.1% | 50.1% |
| GLM-5V-Turbo | 31.7% | 37.9% | 59.5% |

The largest backbone-level gain is GPT-4o's, from 25.4% to 41.2%. At the website level, the largest average gains are on Coursera (+8.6 points), Facebook (+8.3), and YouTube (+7.0). The paper's claim that ANGLER "improves the average ASR for all 8 backbones and all 9 websites" is an averages claim: individual site × backbone cells sometimes regress — GPT-6.1 Sol on Headspace falls from 10.0% to 4.0% and on JD from 20.0% to 14.0%; Claude Sonnet 4.5 on Coursera falls from 22.0% to 17.0%.

**Discovery efficiency.** At a budget of 50 rollouts per site–backbone pair, ANGLER discovers 713 successful attacks against the baseline's 545 — 168 more, a 30.8% relative gain. The methods are close at small budgets and the gap widens as verifier feedback accumulates, which is the paper's evidence that cross-rollout learning, not just candidate volume, drives the improvement.

**Effect on benign tasks.** Adversarial content damages the agent's actual job. The attack-free condition achieves an average benign success rate (BSR) of 61.9%; this falls to 46.4% under the non-adaptive baseline and 44.4% under ANGLER — reductions of 15.5 and 17.5 percentage points respectively. (Two backbones, Claude Sonnet 4.5 and Qwen3-VL, show slightly *higher* BSR under ANGLER than under the non-adaptive baseline.)

**Engagement is not success.** ANGLER's average CTA rate is 43.5%, but the range across backbones is extreme: 74.6% for GPT-4o down to 1.9% for Claude Sonnet 5.5. By attack type, direct prompt injection achieves the highest ASR at 31.5%. Among environment-level types, pop-up injection achieves the highest CTA rate (52.4%) yet converts that engagement into the final state less effectively than its engagement rank suggests, at 17.1% ASR — below distraction injection's 17.8% ASR on a 47.0% CTA rate; indirect prompt injection records 15.9% ASR / 25.8% CTA, and ad injection 13.9% / 34.6%. The per-model extremes sharpen the point. GPT-4o is highly susceptible to environment-level attacks (pop-up CTA 83.3% with 42.3% ASR; distraction CTA 89.3% with 39.3% ASR), while CTA never exceeds 5.4% for GPT-6.1 Sol or 2.3% for Claude Sonnet 5.5 across the four environment-level types — yet direct prompt injection still achieves a 32.5% ASR against GPT-6.1 Sol, so low engagement with injected webpage content does not imply general robustness. GPT-4o's direct-injection ASR of 56.6% is the highest single cell reported.

**Ablations.** On Qwen3-VL across all 9 websites, the full method achieves 14.6% ASR. Removing bandit selection reduces ASR by 4.3 points, removing experience feedback by 3.3 points, and removing online mutation by 2.6 points — all three components contribute, with bandit selection the largest individual gain. CTA stays in a narrow 39.4–41.2% band across ablations, indicating the adaptive components improve downstream attack success rather than the frequency of initial engagement.

**Stability and cost.** Metrics fluctuate at small sample sizes but stabilise after roughly 75 rollouts per website–backbone pair; reported results use the full 100-rollout budget. Across three complete ANGLER runs on Qwen3-VL with configuration held fixed, the standard deviation stays below two percentage points on all three metrics (ASR 12.6 ± 1.8). Wall-clock cost per valid rollout ranges from 63.9 seconds (Qwen3.7-Flash) to 299.7 seconds (Qwen3-VL); no monetary cost figures are reported.

## Limitations

The paper contains **no limitations section** — the word does not appear in the full text — and no future-work section. The scope limits below are recovered from caveats the authors state elsewhere in the paper, followed by issues evident on inspection.

Stated by the authors, in effect if not under that heading:

- All eight targets share one scaffold (VisualWebArena), one observation preset, and one action space, so — in the paper's own words — "reported results therefore characterize the complete target-agent configuration rather than the backbone model alone." Backbone rankings should not be read as properties of the models in other harnesses.
- CTA "should be interpreted as a meaningful indicator of attack exposure and engagement," not of attack success; the paper itself documents large CTA–ASR gaps.
- Runtime figures mix local-GPU and remote-API serving, so they "represent practical rollout latency under our evaluation setup rather than controlled model-serving throughput."
- Quality control (automated consistency checks plus manual audits, with invalid cases corrected and rerun) is described, but no residual error rate for the tasks or verifiers is reported.

Evident on inspection:

- **An unresolved internal inconsistency.** The §6.5 text states that direct prompt injection achieves an ASR of 32.9% against Claude Sonnet 5.5; Table 11 reports Claude Sonnet 5.5's direct-injection ASR as 39.8%. The paired figure for GPT-6.1 Sol (32.5%) agrees between text and table. One of the two Sonnet 5.5 numbers is wrong, and the paper does not resolve which.
- **No head-to-head comparison with other adaptive attackers.** Systems such as MUZZLE, AgentVigil, SIR, AdvWeb, and WebInject are compared only qualitatively, in a feature matrix. The sole experimental comparator is the non-adaptive baseline, which selects uniformly at random among compiler-valid candidates — a deliberately weak search policy. The +5.12-point headline therefore measures adaptivity against random selection, not against the best alternative attacker.
- **Ablations and repeatability use a single backbone** (Qwen3-VL), which sits mid-pack in vulnerability; component contributions are not shown for the most or least vulnerable backbones.
- **Synthetic environments.** The nine websites are finite-state-machine-generated clones built on AutoWebWorld, not the real Coursera, Facebook, or other named services. Transfer of the measured success rates to real websites or other agent scaffolds is untested within the paper.
- **Fixed proposal model.** Mutation quality depends on Qwen3.5-9B, held fixed throughout; no sensitivity analysis over the proposal model is reported.
- **Bounded attack space by design.** Mutation can only edit whitelisted payload, delivery, timing, and style fields of catalog objectives; ANGLER cannot discover attack types or objectives outside REEF's catalog, so all success rates are relative to this feasible space.
- **No defenses evaluated.** The paper measures attack success only; no mitigation — detection, instruction hierarchy, guardrails — is tested against ANGLER.

## Competing approaches

The paper positions itself against two families. Fixed-case security benchmarks — WASP, RedAgentBench, SecureWebArena, VWA-Adv, RedTeamCUA — "evaluate agents using fixed and static attack cases or trajectories" and do not adapt attack generation or selection based on outcomes from previous rollouts. Adaptive predecessors exist but are narrower: MUZZLE uses execution feedback to adapt attacks but focuses specifically on indirect prompt injection; AgentVigil and SIR are likewise single-type (indirect injection) systems; pop-up and ad-injection studies each target one delivery channel; WebInject optimises pixel perturbations; AdvWeb trains a black-box adversarial prompter. General capability benchmarks (WebArena, VisualWebArena, Mind2Web, WebLINX, BrowserGym, AutoWebWorld) primarily measure benign task completion rather than security.

The paper's Table 1 feature matrix makes the positioning concrete: across number of web environments, user-level and environment-level coverage, attack types, online generation, adaptive search, cross-rollout learning, failure-guided refinement, plan validation, and execution oracle, ANGLER/REEF is the only row with every feature — 9 environments, both delivery levels, 5 attack types, and all of the adaptivity and validation features. The closest adaptive systems (MUZZLE, SIR) lack plan validation and cover fewer environments and a single attack type; SecureWebArena covers 6 environments and 6 attack types across both levels but has no online generation, adaptive search, or execution oracle.

There are, however, no quantitative comparison numbers against any competing attacker or benchmark: Table 1 is a feature matrix, and the only numeric comparison in the paper is ANGLER against its own non-adaptive baseline. Claims of superiority over MUZZLE-class systems are therefore feature claims, not measured ones.

## Implications

If the author-reported results hold, fixed attack suites systematically underestimate web-agent vulnerability: an attacker that learns from verifier feedback across rollouts finds substantially more successful attacks than random selection from the same validated candidate pool, and the advantage grows with budget. Evaluation harnesses that score attacks at the text level, or that use a single attack type, will miss both the adaptivity effect and most of the delivery surface.

The engagement results carry a measurement lesson. CTA rates and final-state success rates diverge sharply — pop-ups engage the most and convert comparatively poorly, and the two backbones that almost never engage with injected page content are still compromised by direct injection at rates comparable to the field. Any security metric that stops at "did the agent click / follow the lure" will overstate compromise for environment-level attacks and understate it for user-level ones. REEF's three-verifier design — separating never-successful, transiently successful (recovered), and successful-at-termination outcomes — is the paper's answer, and it is reusable independently of ANGLER: [[projects/webanything]] addresses the complementary problem of constructing resettable web environments for agent evaluation at all.

The benign-task results reframe prompt injection as a reliability problem as well as a security one: under attack, benign success falls by up to 17.5 points even when the malicious objective is not completed, because diverted agents abandon or botch the user's task. The near-miss taxonomy is relevant here — attacks that transiently succeed and then recover are invisible to final-state-only scoring of the *malicious* objective while still damaging the benign one.

What the paper does not support is any conclusion about defenses: no mitigation is evaluated, so whether instruction hierarchies, injection detectors, or action gating would blunt ANGLER specifically is untested. It also does not support transferring the absolute success rates to real websites, production agent stacks, or other scaffolds — those transfers are plausible directions for follow-up work, not findings.

## Reproducible experiment

A full replication is not extractable from the paper: no code or data is released (see Evidence status), and the environments and verifiers are artifacts of the authors' AutoWebWorld-based pipeline, so REEF and ANGLER cannot be re-run from the paper alone.

The smallest check a reader can run is an internal-consistency audit of the published tables. Performed during the preparation of this page, it reproduces the headline arithmetic exactly: the Table 3 backbone averages follow from the site-level cells (e.g., GPT-4o under ANGLER: (58+59+42+31+54+20+42+22+43)/9 = 41.2); the headline figures are the means of the eight backbone averages (20.36 and 15.24); the benign-success averages (61.9 / 46.4 / 44.4) and derived deltas check; the discovery gain (168/545 = 30.8%), relative ASR gain (5.12/15.24 = 33.6%), ablation deltas (4.3 / 3.3 / 2.6), and mean CTA (43.5%) all recompute correctly. The same audit surfaces the single failure: the §6.5 versus Table 11 discrepancy for Claude Sonnet 5.5 direct-injection ASR disclosed under Limitations.

A conceptual mini-replication of the central qualitative claim — engagement is not success — is possible on any open WebArena-style environment: implement a two-phase pop-up injection, log CTA activations and final-state verifier outcomes separately, and compare the two rates. That is a re-implementation of the design, however, not an extraction from this paper.

## Evidence status

Every result on this page is **author-reported** from a single arXiv preprint; there is no independent replication in the paper or cited here, and no claim on this page should be read as independently verified. The full text (arXiv HTML v1) was read for this page, and the internal-consistency audit described under Reproducible experiment reproduced the headline arithmetic exactly, with the one discrepancy disclosed under Limitations — arithmetic consistency is not experimental replication.

**No code or data is released.** No repository, project page, dataset URL, or release statement appears anywhere in the paper ("GitHub" occurs only as the name of one of the nine benchmark websites). The environments are built on AutoWebWorld (Wu et al., 2026) and the target scaffold is VisualWebArena (Koh et al., 2024); neither is this paper's artifact. Corresponding-author emails are the only contact channel given. Model names (GPT-6.1 Sol, Claude Sonnet 5.5, Qwen3.7-Flash, GLM-5V-Turbo, and the Qwen3.5-9B mutation model) are recorded exactly as the paper prints them, not normalised.

## Historical coverage

[Briefing 2026-11-02](../briefings/2026/11/2026-11-02.md)
