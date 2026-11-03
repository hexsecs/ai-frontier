---
uid: 5382fb5c-e4e2-4a65-9d54-1fd496822bda
depth: deep
title: "GARDEN: Generalist Autonomous Reward Design Through Evidence Navigation for Cooperative Multi-Agent Reinforcement Learning"
summary: "One LLM-engineered reward program for a cooperative MARL task family, frozen and transferred unchanged to held-out scenarios."
type: project
created: 2026-10-31
updated: 2026-11-02
sources:
  - url: https://arxiv.org/abs/2610.37926
    retrieved: 2026-11-02
  - url: https://github.com/DoganUrgun/GARDEN
    retrieved: 2026-11-02
---

# GARDEN

## What it is

GARDEN (Dogan Urgun, Karabuk University; single-author arXiv preprint, submitted 27 October 2026) is a method for automated reward design in cooperative multi-agent reinforcement learning (MARL). Its central move is to design rewards at the level of a **task family** — a set of scenarios that share task semantics and interaction mechanics but differ in structure (layout, team size, unit composition) — rather than for one scenario at a time.

The designer is not the RL agents and not a human engineer. It is a tool-using LLM acting as a **reward engineer**: it inspects environment and learner source code, training artifacts, and behavioral evidence of its own choosing; writes draft reward programs as executable code; tests drafts through bounded learning probes; and iterates over generations of candidates. A fixed, mechanical selection rule — not the LLM — then picks one program based on development-scenario results. That program's source is frozen and hashed, and it is applied **unchanged** to held-out scenarios of the family, where new policies are trained from random initialization. Because no policy parameters are transferred, what the experiments measure is the generalization of a learning signal: whether a shaping reward engineered on some scenarios of a family still teaches well on scenarios it was never designed for.

In the reported experiments, the reward engineer is gpt-6.1-sol at maximum reasoning effort; the learner is MAPPO, held fixed across all conditions; and the two task families are Overcooked and SMAX from the JaxMARL library. Evaluation performance is always the sparse task reward alone, irrespective of the shaping used during training. The paper is explicit that the family objective is approached through development search and a predetermined selection rule, and that **no transfer guarantee is implied**.

## Mechanism

**Formulation.** Each scenario is a Dec-POMDP; a family F is partitioned into a development set D and a held-out set H. A reward program R is a deterministic executable function mapping (s_t, a_t, s_{t+1}, r^task_t, h_t) to a per-agent shaping vector ρ_t and an updated bounded memory h_t, reset at episode boundaries. No scenario identifier is supplied to the program — though the paper concedes identity may be inferred from geometry or team composition, so generalization is assessed empirically rather than enforced. The training reward is `task + native shaping` in the native condition and `task + λ_F · ρ` in the generated condition, with family weights λ_F = 0.1 (Overcooked) and 0.01 (SMAX). Native shaping code may be inspected as source but is never added to, imported by, or called from a generated program.

**Evidence navigation.** The protocol fixes the objective, the information boundary, the reward interface, and the learner; everything about *which evidence to examine* is delegated to the engineer. Through a constrained shell, the engineer can access environment and learner source code, native reward logic, training configurations, trajectories, losses, learning curves, checkpoints, and completed design records. No diagnostic checklist or fixed set of statistics is prescribed, and the engineer may write and run custom analysis programs. It may also request a bounded number of **learning probes**: a draft reward trained on a chosen development scenario with the learner, budget, and seed of the formal assessment. Each committed program is accompanied by a short design report recording the evidence examined, the proposed mechanism, and its limitations.

**Candidates and shared evidence.** A search runs G = 3 generations × P = 2 candidates — six candidate programs per family — with at most 2 learning probes per candidate session. Candidates within a generation are developed in independent sessions: siblings' programs, reports, probes, and assessments are withheld, while all completed evidence from earlier generations is shared. After commitment, each candidate is assessed on every development scenario; probes and development assessments use a single training seed.

**Selection and transfer.** After all candidates are assessed, one program is selected by the fixed score S(R) = (1/|D|) Σ_m (J_m(R) − J^nat_m) / max(|J^nat_m|, 1) — relative improvement over native shaping where |J^nat_m| ≥ 1, absolute improvement otherwise (as for win rates). Ties break by worst-scenario normalized improvement, then mean sparse return, then a deterministic identifier, so that neither LLM preference nor held-out results enter the selection. The selected source is frozen and hashed; interface compliance, admissible dependencies, and finite execution are verified before any training, and the information boundary is protected by sanitized workspaces, restricted commands, and logged actions. Transfer then means training native and generated-reward policies from scratch on the held-out scenarios under identical settings.

**Learner.** MAPPO with centralized training and decentralized execution and actor parameters shared across agents: a feedforward actor (three convolutional layers, two dense layers) over the full-grid observation in Overcooked, and a recurrent GRU actor with action masking in SMAX. Each training run uses ≈5M environment steps (exactly 4,997,120), with 305 updates, 4 PPO epochs, discount 0.99, GAE λ 0.95, and clip 0.20 shared across families. Final policies are evaluated with sampled actions, and held-out results were not used for checkpoint selection. All runs used a single NVIDIA RTX 6000 Ada GPU.

## Evidence

All results below are **author-reported** from a single-author preprint; no independent replication exists. Each reward was developed once, and every held-out condition was then trained with **10 matched policy seeds** (the same seeds for every reward); reported values are mean ± standard error over those seeds.

*Held-out transfer versus native shaping.* The development/held-out split was: Overcooked — development on Cramped Room, Bottleneck, and Coordination Ring; held-out on Forced Coordination and Counter Circuit. SMAX — development on 3s5z vs 3s6z, SMACv2 with 5 units, and 5m vs 6m; held-out on 10m vs 11m and SMACv2 with 10 units. A separate reward program was developed for each family. Overcooked's native reward pays 20 points per delivered dish, with shaping of +3/+3/+5 for pot-loading, dish pickup, and soup pickup; SMAX's task reward is a win (all enemies eliminated with at least one ally surviving), with native shaping on reductions in enemy health.

| Held-out scenario | Native | GARDEN | Gain |
|---|---|---|---|
| Overcooked — Forced Coordination (return, % of native) | 100.0 ± 3.4 | 158.2 ± 6.8 | +58.2% (relative) |
| Overcooked — Counter Circuit (return, % of native) | 100.0 ± 4.3 | 152.5 ± 15.8 | +52.5% (relative) |
| SMAX — 10m vs 11m (win rate) | 27.3 ± 0.96% | 96.1 ± 0.90% | +68.8 pp |
| SMAX — SMACv2 10 units (win rate) | 74.6 ± 1.80% | 83.6 ± 0.86% | +9.0 pp |

The Overcooked gains are relative improvements over the native mean; the SMAX gains are percentage-point differences. The same frozen program was used on both held-out layouts within each family, and all held-out policies were trained from scratch — in the paper's words, "these results measure the transfer of the reward itself rather than of a trained policy." Note the asymmetry: the largest gain (+68.8 pp) occurs where native shaping was weakest (27.3% win rate); where native shaping was already strong (74.6%), the gain is +9.0 pp. The SMAX mean held-out win rate rises from 51.0% to 89.9%.

*Controls.* Two reward-design controls were run on SMAX only, with the same permitted initial source context, candidate and probe budgets, learner, and selection rule; only the evidence available to the engineer (and the use of reward history) differed. **Fixed diagnostics** restricted training evidence to standardized reports (returns, learning curves, episode lengths, losses, entropy, shaping statistics), with shell access and custom analyses disabled. **Eureka-inspired reflection** refined the previous generation's best reward using standardized task and reward-component feedback, without initial native diagnostics. Mean held-out SMAX win rates: GARDEN 89.9%, fixed diagnostics 84.2%, Eureka-inspired reflection 79.2% — margins of +5.7 pp and +10.7 pp. Per scenario, GARDEN led on both (96.1% and 83.6%, vs 91.2%/77.1% for fixed diagnostics and 87.6%/70.8% for reflection); on SMACv2 10 units, the reflection control's reward fell *below* native shaping (70.8% vs 74.6%).

*Development case studies.* Two worked examples illustrate the search process; both concern development drafts, not the programs selected for transfer. In Overcooked's Bottleneck layout, a custom trajectory analysis found that the second pot remained empty throughout eight recorded 400-step native-policy episodes; a candidate adding demand-aware shaping, wall-respecting routing, and partly shared production credits used both pots, raising mean deliveries from 9 to 12 and mean task return by 33.5% in a separate 64-episode evaluation — with the author's caveat that the observations do not identify which component produced the change. In SMAX's 5m vs 6m, an initial draft achieved 22 wins in 256 evaluation episodes (8.6%); after the engineer examined combat traces and missed firing opportunities and revised the survival, offensive, evasion, and terminal terms, the revised draft achieved 238 wins in 256 episodes (93.0%) under the same training budget and seed.

## Limitations

- **Inference compute was not matched in the control comparison.** Candidate and probe budgets were matched, but the paper's Table V shows the GARDEN search consumed 155 LLM calls and 15.0M input tokens, versus 18 calls and ~3.5M / ~3.3M input tokens for each control — roughly 8.6× the calls and 4.3–4.5× the tokens. The paper discloses these figures but runs no compute-matched control, so part or all of the 5.7–10.7 pp advantage over the controls could reflect the much larger inference budget rather than autonomous evidence navigation as such. The paper also states the controls differ from GARDEN in evidence access, history use, and inference effort **jointly rather than as isolated factors**, so the design cannot attribute the gap to evidence navigation alone. *(The confound framing is analyst-assessed; the underlying figures are the paper's.)*
- **Search-level variance is unmeasured (paper-stated).** Each condition ran only **one** reward search — one selected program per family per condition. The 10 matched policy seeds capture variation in policy training under that one reward, not variation across reward searches, so the headline margins over the controls each rest on a single search and could move substantially if the search were re-run.
- **Single-seed search.** Probes and development assessments used one training seed, so candidate ranking during search is based on a single seed per assessment.
- **Pilot-informed evaluation (paper-stated).** The scenario split and training budget were fixed after pilot calibration, and one held-out SMAX scenario had been examined in pilots; the study is, in the author's words, "a pilot-informed rather than a researcher-blind evaluation."
- **Very small held-out sets.** Two held-out scenarios per family. Overcooked transfer is across layouts of the same two-agent task; SMAX transfer is largely scale and composition transfer within the same game. The evidence supports reuse across *related* scenarios of a family — the paper's own scoped claim — not transfer to new tasks.
- **Weak-baseline headroom.** The flagship +68.8 pp gain occurs where native shaping achieves only 27.3%; the mean win-rate improvement averages that near-ceiling jump with a +9.0 pp gain where the baseline was already strong.
- **Reporting conventions.** The Counter Circuit result carries a wide standard error (152.5 ± 15.8, as % of native). Overcooked percentages treat the observed native mean as a fixed scale, so native sampling error (±3.4 / ±4.3) is not propagated into the GARDEN standard errors, and gains are point estimates of differences between means.
- **Non-stock native baseline.** The native Overcooked baseline applies shaping with a constant weight throughout training, whereas the JaxMARL reference configuration decays shaping; the comparison is against the default reward under GARDEN's constant schedule, not the stock JaxMARL recipe.
- **Strongest external baselines were not run.** The controls are internal variants of GARDEN's own evidence access. ARBO — which the paper calls "the closest approach" — Eureka proper, Text2Reward, RF-Agent, and the author's own incentive-aware method are compared only qualitatively, not experimentally.
- **Single stack.** All results use one reward-engineer model (gpt-6.1-sol at maximum reasoning effort), one learner (MAPPO), and one environment library (JaxMARL). Nothing separates the method's contribution from the engineer model's capability.

## Competing approaches

The paper situates GARDEN among LLM-based reward-design systems. **Text2Reward** generates reward code from environment abstractions plus human feedback (single-agent). **Eureka** evolves reward code via reflection on reward-component statistics from training (single-agent); it is the basis of the paper's reflection control and of the R* follow-up, which adds reward-structure evolution and parameter alignment. **Self-alignment** learns rewards from comparisons of behavior under candidate rewards. **RF-Agent** runs a language-agent tree search over earlier designs and training feedback. The **Reward Design Agent** assesses trajectories with a vision-language model. **ARBO**, an agentic black-box optimizer with source inspection, tool access, and persistent evaluation records, is identified by the paper as the closest approach; it differs in that its records are limited to candidate scores, per-term training curves, and error tracebacks, and each of its rewards is evaluated in the task it was searched for. **PCRD** applies fixed code-analysis questions in cooperative platooning. The author's own prior **incentive-aware reward design** also synthesizes executable reward programs for cooperative MARL and selects by sparse return, but returns a fixed set of incentive diagnostics to the LLM and evaluates each reward in its design scenario; it is discussed in the paper but not run as a control. Classical alternatives the paper contrasts against include potential-based reward shaping, inverse RL, preference-based RL, meta-learned potential functions over a task distribution, and learner-internal credit assignment (COMA counterfactual baselines, QMIX value factorization). GARDEN's differentiator, per the paper: the learner is left unchanged, and an executable reward program is synthesized once and reused across a family. The only experimental comparisons actually run are the two internal controls above and native shaping.

## Implications

If the transfer result holds up, reward programs become reusable engineering artifacts: a learning signal can be designed once per task family and carried across layouts, team sizes, and compositions, instead of being hand-tuned per scenario. That reframes reward design from per-task craft to per-family infrastructure, and it is the part of the result most relevant to the KB's multi-agent coverage ([[techniques/multi-agent-orchestration]]).

The control comparison — subject to the compute caveat in Limitations — points at a broader agent-design lesson: the winning condition is the one where the designing agent could inspect raw source and training artifacts and build its own analyses, rather than consume standardized diagnostic reports. Instruments over dashboards, for agents as for engineers. GARDEN's protocol also offers a reproducibility template for machine-authored training signals: the objective, interface, and selection rule are fixed in advance; selection is mechanical; the chosen artifact is frozen and hashed; and each candidate ships with a design report. That audit trail is what makes a one-shot automated search result inspectable at all.

The sober reading is narrower: this is one search, by one model, on two held-out scenarios per family, against internal controls with a fraction of its inference budget. GARDEN is best read as a well-instrumented existence proof that family-level reward transfer *can* work, and as a concrete protocol others can replicate — not yet as evidence that autonomous evidence navigation beats simpler feedback loops at equal compute.

## Reproducible experiment

A reader with a JAX-capable GPU can replicate the core claim and test the paper's open confound:

1. **Setup.** Install JaxMARL; take the Overcooked family with development layouts Cramped Room, Bottleneck, Coordination Ring and held-out layouts Forced Coordination, Counter Circuit. Implement MAPPO per the paper's configuration (≈5M steps per run; feedforward actor; λ_F = 0.1), with native shaping held at constant weight.
2. **Minimal GARDEN loop.** Give a tool-using LLM shell access to the environment and learner source, native reward logic, configurations, and training artifacts. Run 3 generations × 2 candidates, at most 2 learning probes per candidate (each a full training run, single seed), candidates within a generation isolated from each other. Score candidates by the paper's mechanical selection rule over the development layouts; freeze and hash the winner.
3. **Transfer test.** Train native-shaped and generated-reward policies from scratch on both held-out layouts with 10 matched seeds; report mean ± SE of sparse task return. The paper's benchmark values are 158.2 ± 6.8 and 152.5 ± 15.8 (% of native).
4. **Compute-matched control (the extension the paper lacks).** Run the fixed-diagnostics control but let it spend the same LLM budget as the GARDEN search (~155 calls / 15M input tokens — e.g., more generations and candidates) before comparing held-out means. This separates evidence navigation from inference effort.
5. **Search replication.** Repeat each condition's entire search at least three times and report the spread of selected-program performance, to measure the search-level variance the paper leaves unquantified.

Logging model calls and input tokens per condition (as the paper's Table V does) is essential; without that accounting, step 4's comparison is uninterpretable.

## Evidence status

This page is based on a full read of the primary source — arXiv:2610.37926v1, HTML full text (Sections I–VI, Tables I–V, Algorithm 1, references; the HTML rendering has no appendices) — on 2026-11-02, for issue #2. All quantitative results are **author-reported** (single-author preprint; no conference or journal venue stated), and no independent replication is known. The code repository URL is recorded **as stated in the paper**; the repository was **not inspected** for this page, and no code was executed. Environment and data availability follow the paper: Overcooked and SMAX are part of the public JaxMARL library; other supporting data are available from the author on reasonable request, per the paper. This page replaces an import stub whose contents were explicitly unverified.

## Historical coverage

[Briefing 2026-10-31](../briefings/2026/10/2026-10-31.md)
