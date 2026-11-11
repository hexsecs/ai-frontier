---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c02
depth: deep
title: "TandemBench"
summary: "Benchmark that asks decision models to pick optimal two-agent cooking plans and to notice when every supplied plan is suboptimal."
type: benchmark
created: 2026-11-08
updated: 2026-11-10
related: [protocol-relative-scores, capability-locus, comparator-construction-shapes-margins]
sources:
  - url: https://arxiv.org/abs/2611.05827
    retrieved: 2026-11-10
  - url: https://arxiv.org/html/2611.05827v1
    retrieved: 2026-11-10
---

# TandemBench

## What it is

TandemBench is a benchmark of 1,200 questions that tests decision models on **team plans** — a single choice that specifies what two collaborating agents each do and in what order — in multi-agent cooking scenarios. It is reported in the arXiv preprint "TandemBench: Benchmarking Decision Models for Multi-Agent Collaboration" (arXiv:2611.05827, v1 submitted 4 November 2026, cs.CL; preprint, no peer-reviewed venue claimed). The paper lists three authors — Baohang Li, Xiaocheng Feng and Bing Qin — at the Harbin Institute of Technology, with Feng also affiliated to Peng Cheng Laboratory. The paper states that the dataset and evaluation code are publicly available at https://github.com/lililibaohang/TandemBench, and names the public dataset release `tandembench-en-v1.0.0`.

The gap it targets: a decision model can pick the best option in a set, and be right, while having no idea whether the set contained the best possible option at all. The paper measures these as two separate scores — **decision accuracy (DA)** for choosing an optimal plan and **verification accuracy (VA)** for judging whether a better arrangement exists beyond the supplied options — and its headline result is that the two come apart sharply.

The benchmark is deliberately *not* a collaboration benchmark in the deployed sense. Models receive complete global information and a set of candidate plans; nothing is hidden and no model has to communicate. The task is the decision, not the coordination. That makes it a controlled probe of plan judgement rather than an evaluation of multi-agent systems, which is exactly how the paper positions it.

## Mechanism

**Environment.** 30 recipe tasks from Collab-Overcooked (Sun et al., 2025), in which a chef and an assistant work in separate kitchen regions with asymmetric access to ingredients, appliances and counters. Asymmetric access is what forces coordination: some actions depend on materials only the other member can supply, and recipe dependencies constrain order. Automatic processing lets preparation overlap with cooking; carrying limits and shared-counter availability constrain where and when a handoff can happen.

**Execution semantics.** Each joint step resolves chef interaction, assistant interaction, movement, then appliance processing; processing includes its start step and finished products await retrieval; waits are checked at step boundaries. An assistant interaction can retrieve an item the chef placed in the same step, but an explicit wait cannot. Domains define role permissions, retrieval and counter access. A candidate plan may cover the full task or prescribe a stage that ends before the final goal.

**Two goal settings.** *Short-horizon* questions count joint steps until a specified intermediate milestone is first reached. *Long-horizon* questions count steps until the final goal; if the prescribed stage ends before completion, the cost is the stage's executed steps plus the minimum remaining steps from the resulting state. Both settings are applied to both task types, and a long-horizon cost is ∞ for a plan that cannot complete under the protocol even if abandoning it would permit recovery.

**The reference answers.** The state optimum V*_g(s, D) is the minimum completion cost of *any* legal joint execution from the given state under the specified goal and domain. Candidate outcomes are established by execution, and the optimum by exact search — including the optimal continuation needed for long-horizon evaluation. Matching candidate costs to the state optimum identifies the correct base answer; among the four supplied candidates the optimum is unique.

**Scenario selection.** States are drawn from verified optimal delivery trajectories at events that change available materials, processing status or handoff opportunities, and reachability is established by executing trajectory prefixes. At each state the paper compares alternative orders of two required events by one member, or alternative locations for a required handoff; exact search gives the minimum delivery cost subject to each choice with all remaining actions optimized. A state qualifies only when two feasible choices are proven: one attains the state optimum (Δ = 0) and the other costs at least three additional joint steps (Δ ≥ 3). The screening algorithm caps comparison families at K = 8 and allocates a budget of B = 200 scenarios, using greedy coverage over event orderings, handoff directions, comparison families and material stages, with source levels L1–L6 contributing 10, 5, 40, 35, 50 and 60 scenarios respectively. The paper notes these source levels are recipe-complexity labels, not calibrated item difficulties.

**Question construction.** Each base question offers four plans — variations in work order, handoff location, preparation scope, work overlap or waiting conditions — of which at least three are feasible and exactly one attains the state optimum. Each verified base question then yields a **verification pair**: one variant removes the optimal plan, the other removes a predetermined nonoptimal plan, and both add the same fourth option stating that a feasible plan can reach the goal in fewer joint steps than all three retained plans. State, goal, execution rules and retained programs are unchanged across the pair. The better-plan statement is therefore true exactly when no retained plan attains the state optimum — false when the optimum is retained, true when it is removed. Because state and goal are held fixed, a model that reports "a better plan exists" in both variants is making a *false alarm*, and one that picks a concrete plan in both variants is *missing* a genuine improvement.

**Metrics.** DA compares the selected candidate ID with the gold ID over questions, four cyclic option rotations and samples; uniform selection or a fixed display letter yields 25%. VA averages the correct-detection rate when the optimum is removed with the correct-rejection rate when it is retained; uniform selection, always reporting a better plan, or always choosing a concrete plan yields 50%. Any valid concrete-plan choice counts as rejection — TN does not require picking the optimal retained plan. Truncated, missing-choice, multiple-choice and infrastructure-failure outputs count as incorrect for both metrics.

**A concrete case.** In the paper's long-horizon example point024 (a taro–bean–bell-pepper pie), the four candidate programs have stage costs and optimal continuations that yield totals of 21, 13, 15 and 15 joint steps; the 13-step plan is the optimum, while the plan with the shortest stage (7 steps) needs 15 steps in total. This is the shape of the stage/total rank reversal the paper counts 15 times.

**Dataset composition.**

| Unit or property | Count |
|---|---|
| Recipe tasks | 30 |
| Decision scenarios | 200 |
| Short-/long-horizon question pairs | 200 |
| Total evaluation questions | 1,200 |
| Base team-plan decision questions | 400 |
| Optimality-verification variants | 800 |
| Base candidate plans | 1,600 |
| Base questions with 3 / 4 feasible plans | 246 / 154 |
| Normalized question structures | 181 |
| Normalized paired-scenario structures | 97 |
| Pairs with identical candidate programs | 64 |
| Long-horizon questions with stage/total rank reversals | 15 |

## Evidence

All results are **author-reported** from this single preprint; none has been independently replicated. English inputs throughout.

**Setup.** 40 native decision models (models with purpose-built decision interfaces) and 10 general-purpose language models. Each question is evaluated under four cyclic option rotations so each candidate appears once in each position. Native models produce one response per rotation, and general-purpose models produce four; the paper states that each model contributes 1,600 native or 6,400 general-model base outputs, and that each general-purpose model contributes 19,200 outputs across questions, option rotations and samples. Each response is scored separately without voting. Models use their native interfaces: Tacit inference, Decision-2 for Vega/Lux/Kai/Nox, CLM's prediction head with last-token pooling, Laya state inputs with short labels, KnowLine's `read_twice`, GLiDE's non-causal text interface, with calibration retained for Mammoth, PPLX and D3 and Instant inference for StartLux. Weights are BF16 for H2O-Lightning-31B and deck31b, FP8 dequantized to BF16 for René. Muse-Glimmer-30B uses low reasoning; the evaluated Qwen conditions disable thinking.

**Native decision models — top and bottom by DA.**

| Rank | Model | Params (B) | DA % | VA % |
|---|---|---|---|---|
| 1 | KnowLine-31B-Gen1 | 31 | 62.50 | 51.44 |
| 2 | Basal-Omni-1.0-Ultra | 31 | 60.75 | 51.97 |
| 3 | Quyet-1.0-Large | 31 | 60.75 | 52.06 |
| 5 | PPLX-Decider-v1.2 | 27 | 60.38 | 55.31 |
| 13 | PPLX-Decider-Flash-v1.2 | 4 | 52.94 | 53.19 |
| 21 | D3-Ultra | 27 | 47.50 | 56.28 |
| 30 | Clef | 27 | 40.94 | 52.91 |
| 39 | Kai-0.6B | 0.6 | 21.81 | 50.00 |
| 40 | CLM-8B | 8 | 15.44 | 45.94 |

Native DA spans **15.44% to 62.50%**; VA spans **45.94% to 56.28%**, i.e. near the 50% chance line throughout. The paper's key observation is that the DA leader does not lead VA: D3-Ultra has the best native VA (56.28%) with a middling DA of 47.50%, so plan-selection quality and optimality judgement are not the same competence.

**General-purpose language models.**

| Rank | Model | Avg. output tokens | DA % | VA % |
|---|---|---|---|---|
| 1 | Qwen3.8-27B | 8,652 | 82.80 | 71.88 |
| 2 | Gemma4-31B | 1,072 | 73.11 | 57.03 |
| 3 | Gemma4-26B-A4B | 1,516 | 60.58 | 53.66 |
| 4 | Muse-Glimmer-30B | 1,415 | 59.64 | 60.35 |
| 5 | Qwen3-32B | 925 | 46.33 | 49.45 |
| 9 | Llama3.3-70B | 661 | 39.50 | 48.92 |
| 10 | Qwen3-0.6B | 25 | 17.19 | 40.61 |

The best general-purpose model, Qwen3.8-27B, is far ahead of the best native model on DA (82.80 vs 62.50) and has by far the highest VA of any evaluated model (71.88) — it also produced the longest outputs among the ten general-purpose models (8,652 average output tokens, against 2,564 for the next longest and 25 for Qwen3-0.6B).

**Verification behaviour.** Detection and false-alarm rates barely separate. Tacit-2B detects 98.38% of cases where the optimum is absent but raises false alarms in 97.88% of cases where the optimum is present. Over the 128,000 outputs the probability analysis uses (40 models, 400 pairs, four rotations), the AUROC that ranks removed-optimum against retained-optimum examples by better-plan probability has a median of 0.537 and a maximum of 0.598 (GLiDE); Basal scores 0.520. For models that report a better plan in both variants, the mean shift in better-plan probability between removed and retained conditions is +3.26 points for Basal (240 pairs), +2.05 for PPLX (504) and +0.55 for Tacit-2B (1,557) — a few points of movement against a condition difference that should have produced a much larger swing.

**Goal sensitivity.** Over the 64 matched pairs that share the initial state, candidate programs and optimal choice but differ in goal and execution rules, mean DA falls from **49.58% (short) to 46.75% (long)** across native models; for general-purpose models it falls from **56.68% to 48.04%**. The paper also identifies a disjoint set of 15 long-horizon questions where a feasible alternative finishes its prescribed stage sooner but needs more total steps — a stage/total rank reversal. On those, Basal selects the earlier-finishing but costlier alternative in 22 of 60 presentations and CLM in 66.67% of cases, while KnowLine selects it 0.00% of the time; the same disagreement appears in the conflict-DA column, which ranges from 0.00 (CLM) to 73.33 (Torchcast-4B-v1.2).

**Position sensitivity and consistency.** The median range between a native model's best and worst accuracy across the four rotations is **10.38 percentage points**. Choice consistency — selecting the same underlying plan across all four rotations — reaches **92.00% for CLM-8B, whose DA is 15.44%**: stable answers can be consistently wrong. For general-purpose models the median DA range is 7.34 points, or 8.47 points when averaging within-sample ranges.

**Execution consequences of the selected plan.** Among feasible selections, regret is the excess joint steps over the state optimum: KnowLine 1.68, Basal 1.44, Quyet 1.22, PPLX-Decider-v1.1-27B 1.74, Torchcast-4B-v1.2 1.25, CLM-8B 4.50. Feasibility rates are high for all but CLM: KnowLine 99.94% feasible and 0.06% noncompleting, Basal 99.75% / 0.25%, Quyet 98.75% / 1.25%, PPLX 100.00% / 0.00%, Torchcast 95.69% / 4.31%, CLM 78.56% / 21.44%. The 246 questions with non-completing candidates expose 984 native outputs (or 3,936 general-model outputs).

**Weighting and uncertainty.** Under task-macro weighting (task-level accuracies averaged equally) rather than item weighting, KnowLine rises from 62.50% to 66.96% and Basal from 60.75% to 65.45%, while CLM falls from 15.44% to 10.52%. Bootstrapping the 200 scenarios with both goals retained (10,000 replications, seed 20261027) puts the KnowLine-minus-Basal DA gap at 1.75 points with a 95% percentile interval of [−1.56, 5.00], or [−2.10, 5.56] when resampling the 30 tasks. The top two native models are therefore not separated by the benchmark's own uncertainty procedure.

**Coordination groups.** Questions are tagged by the coordination contrast they exercise: work order (processing/supply order) 300 questions across 156 scenarios, handoffs (transfer locations and conditions) 376 across 188, parallel work (productive overlap) 355 across 182, and resource constraints (carrying and counter capacity) 141 across 77. Groups overlap and differ in task and goal composition, so the paper is careful to describe these as performance on subsets rather than isolated mechanism effects.

## Limitations

**Stated by the authors.** The findings concern team-plan decisions for two agents in one kitchen with global information. Questions share scenarios, and inference budgets vary across models. The benchmark evaluates centralized plan decisions from complete global information; it does not test communication or adaptation to independent partners. Option rotations balance answer positions, but program length and waiting patterns remain observable cues. Models use their native interfaces and inference budgets, so results compare evaluated systems under their respective protocols.

**Assessed from the reporting.**

- **Single source, no independent replication.** Everything rests on one arXiv preprint (v1, 4 November 2026). The dataset and evaluation code are publicly linked, which makes replication feasible, but no third-party replication is known.
- **The headline gap between DA and VA is real but shallow.** Native VA spans 45.94%–56.28% around a 50% chance line, so "verification accuracy stays near chance" is accurate for native models but hides a spread: several models sit measurably above chance, and one (D3-Ultra, 56.28%) is meaningfully better at verification than at selection. The AUROC analysis (median 0.537, max 0.598) is the sharper statement of the same weakness.
- **The VA metric is easy to score well by accident.** A model that always picks a concrete plan scores exactly 50% VA by definition, and TN does not require picking the optimal retained plan. VA therefore has a large degenerate basin, and "near chance" partly means "no better than the degenerate policy". Any adoption of VA as a gate should compare against the always-pick-a-plan baseline and against the per-model detection/false-alarm split, not against the pooled 50%.
- **Inference budgets are wildly unequal and partly confounded.** Qwen3.8-27B emits 8,652 average output tokens against Qwen3-0.6B's 25. The highest-DA general model is also the one that reasons longest, so the paper cannot separate "better plan judgement" from "more deliberation". Native models keep native interfaces, which is faithful to their design but means the comparison is between systems, not between architectures.
- **200 scenarios, 30 tasks, 1,600 base candidate plans.** A single scenario can move a task-macro score by several points, and the bootstrap shows the top two native models are inside each other's confidence interval. Items are not independent either: 200 scenarios produce 400 base questions and 800 verification variants, so the effective sample size is far below 1,200.
- **The domain is narrow and the mechanics are toy-like.** Two agents, one kitchen, three resource types by analogy with 30 recipes, a discrete joint-step clock, and no partial credit or uncertainty in the environment. Whether a plan that is cost-optimal in this simulator is also robust in a live kitchen is untested.
- **Reference answers come from one search procedure.** The optimum is "exact search" under the paper's domain rules; any mismatch between that model and the true optimum (or between the model and reality) propagates into every label. The paper notes unresolved searches do not supply labels, and that a non-completing plan is scored as ∞ even when abandonment would recover — a defensible but strict convention that mechanically depresses DA for models whose plans are merely badly ordered.
- **The "wrong" answer in a verification question is not weighted.** Because any concrete plan counts as rejection, a model can be scored correct for rejecting a better plan while having selected the worst of the three feasible options. The benchmark measures the *presence* of a better arrangement, not the quality of the model's fallback choice.
- **Position sensitivity is reported but not corrected.** A median 10.38-point range across rotations for native models means single-position scores are unreliable; the headline tables average four rotations, but any user who quotes a single rotation should not treat it as a capability measurement.

## Competing approaches

The paper groups related work in three areas. **Decision-model evaluation:** JEVal and OpenDecisions (accuracy, calibration, inference efficiency), DecisionRobust (adversarial robustness), DecisionPivot (controlled input changes), AgentBench and AgentBoard (sequential decisions via task success and progress), and AgentDecisionBench (tool and action choices across isolated choices, recorded agent states and online control). TandemBench's stated difference is the decision unit: a *joint team plan* rather than an isolated choice.

**Multi-agent collaboration:** CoELA and RoCo (communication and coordinated execution), MultiAgentBench and PARTNR (interactive collaboration), CoordQA and RoCoBench-Text (coordination choices as static questions), ParaCook (CP-SAT optimal references for abstract scheduling) and CoCoBench (coordination against optimal makespan under a skill abstraction). The base environment is Collab-Overcooked's asymmetric cooking setup.

**Planning and verification:** PlanBench, ACPBench and TravelPlanner for plan generation and reasoning; Lin et al. (2024) on the computational complexity of plan-optimality verification; Dold et al. (2025) on optimality certificates as independently checkable evidence; DecisionPivot's controlled contrasts. TandemBench's stated difference is that it asks whether *any* supplied joint plan attains the state optimum, and tests whether model judgments track the optimum's presence via paired variants.

Within this knowledge base, TandemBench sits opposite [[projects/masbench]] on the observability axis — complete global information and no communication, against partial observability and mandatory exchange — while sharing the multi-agent-collaboration subject matter; it also shares the "a good choice can hide a bad set" concern with [[projects/st-bench]] and [[projects/agensh]]. The scoring lesson — that a selector score and a selector-set score are different measurements — belongs with [[concepts/comparator-construction-shapes-margins]] and [[techniques/evaluation-and-simulation]], and its pairing of an agent's own account with an independent record belongs with [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]]. It is listed from [[benchmarks/index]] and contributes to [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The transferable finding is that **"which option is best" and "is the option set sufficient" are separate capabilities, and a single leaderboard can hide the second one entirely**. Any internal evaluation that scores a router, a scheduler or a plan-selector on accuracy alone is measuring half the problem. The cheap fix is a paired design: hold the state fixed, present the same options with and without the optimum, and check whether the model's verdict tracks the optimum's presence. TandemBench's AUROC analysis is the right diagnostic for this — the better-plan probability should separate the two conditions, and a median AUROC of 0.537 says the signal is almost absent.

Second, **VA's degenerate basin should be priced into any adoption of it**. If always-picking-a-plan scores 50%, then VA near 50% may mean "no information" rather than "weak but real competence", and a team adopting a verification score needs the always-pick baseline and the detection/false-alarm split reported separately. The paper's own Tacit-2B numbers — 98.38% detection and 97.88% false alarms — are the clearest illustration of what a near-chance pooled number can hide.

Third, **the stage-versus-total distinction is the more interesting engineering finding**. A plan that finishes its assigned stage earlier can still be the worse plan for the team overall. The 15 rank-reversal questions and the Fast-stage choice column show models splitting their answers on exactly this: KnowLine never picks the earlier-stage option, CLM picks it two thirds of the time. For any scheduler that bills or bills against per-agent milestones, this is a trap with a measurable size.

Fourth, **a benchmark that mixes decision quality with output length cannot separate them**. The best general-purpose model also writes 8,652 tokens on average; the worst writes 25. For an evaluation meant to guide procurement, the two-factor version (judgement quality × deliberation cost) would be the more useful table, and the paper's mean-output-token column is the raw material for it.

Finally, the design itself is worth borrowing: **generate reference answers by execution and exact search rather than by annotation**, and construct the verification contrast by removing the optimal option while holding everything else fixed. That is a general recipe for testing any selector, and it needs no domain beyond one where optimality can be computed.

## Reproducible experiment

The dataset and evaluation code are linked publicly, so a replication is possible; substituting available models for the 2026-native decision models is unavoidable. A feasible independent check:

1. **Reproduce the DA/VA decoupling on the public release.** Run one available general-purpose model (the paper's own Qwen3.8-27B, if the weights and inference stack are accessible, otherwise an open 30B-class model) over the 1,200 questions with four cyclic option rotations, and score DA and VA with the published formulas. The reference numbers are DA 82.80% and VA 71.88% for Qwen3.8-27B. The paper's claim is not that these numbers replicate exactly but that **VA stays far below what DA would suggest** — for native models, DA up to 62.50% with VA at 51.44%. Report both scores and the per-model detection and false-alarm rates.
2. **Test the degenerate-policy floor explicitly.** Score the always-pick-a-concrete-plan policy and the always-report-a-better-plan policy on the same release. Both must produce DA 25% and VA 50% by construction; if the released scorer does not reproduce those floors, the scoring code and the paper's description disagree, which is itself the finding.
3. **Measure position sensitivity on your own stack.** For the same model, report the per-rotation DA rather than the four-rotation average. The paper's native median range is 10.38 points; if your model's range is of that order, treat any single-run leaderboard score as noise. Also report choice consistency (the fraction of questions where the same underlying plan is chosen in all four rotations) alongside DA — CLM's 92.00% consistency at 15.44% DA is the pattern to look for.
4. **Test the stage/total distinction.** Take the 15 long-horizon questions with stage/total rank reversals and check whether a model prefers the plan that finishes its stage sooner even when it costs more in total. Report the fast-stage selection rate against the paper's per-model values (KnowLine 0.00%, CLM 66.67%, Basal 22/60 presentations). A model with high DA but a high fast-stage rate is optimizing its own milestone rather than the team's goal — a failure mode that a DA-only evaluation will not surface.
5. **Stress the option-set design.** Construct a variant where the candidate set is replaced by a set containing a clearly inferior plan only (no optimum and no near-optimum). If the model's better-plan probability does not rise sharply, its apparent VA is coming from a stylistic bias rather than from detecting the optimum.

Report the substituted model, its inference settings and any dataset-version differences alongside the results.

## Evidence status

This page is grounded in a full read of the primary source on 2026-11-10: the arXiv abstract page (https://arxiv.org/abs/2611.05827) and the complete HTML full text of v1 including appendices A–H and the reference list (https://arxiv.org/html/2611.05827v1). Every quantitative result is **author-reported**; the paper links its dataset and evaluation code publicly, the models were run by the authors under their own protocols, and no independent replication is known. Claim types are separated in the text: the DA/VA decoupling, the stage-versus-total analysis and the interpretation of position sensitivity are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. The paper is a preprint (v1, 4 November 2026) with no peer-reviewed venue claimed. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers.

## Historical coverage

- [[briefings/2026/11/2026-11-08]] — the dated briefing that introduced TandemBench.
