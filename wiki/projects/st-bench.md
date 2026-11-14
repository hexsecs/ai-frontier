---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c04
title: "ST-Bench"
summary: "Benchmark of 100 Earth-science analysis tasks and 2,067 queries measuring whether multi-agent systems beat a single agent, and at what cost."
type: benchmark
created: 2026-11-08
updated: 2026-11-10
depth: deep
related: [preservation-aware-agent-improvement, verified-completion-vs-apparent-success, protocol-relative-scores]
sources:
  - https://arxiv.org/abs/2610.07763
  - https://arxiv.org/html/2610.07763v1
---

# ST-Bench

## What it is

ST-Bench is a benchmark and evaluation framework for **multi-agent system (MAS) generation** on scientific data-analysis tasks. It is reported in the arXiv preprint "ST-Bench: A Spatial-Temporal Benchmark for Multi-Agent System Generation on Scientific Research Tasks" (arXiv:2610.07763, submitted 6 October 2026, cs.AI; preprint, no peer-reviewed venue claimed). The paper lists eleven authors — Qi Cheng, Rongchao Dong, Shengyu Chen, Licheng Liu, Dan Lu, Zhengzhang Chen, Wei Cheng, Yiqun Xie, Haifeng Chen, Xiaowei Jia and Haoyu Wang — with affiliations at Rutgers University, the University of Pittsburgh, the University of Minnesota, Oak Ridge National Laboratory, NEC Labs America and the University of Maryland.

The question it poses is narrow and testable: **do multi-agent systems outperform single agents on real scientific data analysis, and if so by how much and at what additional cost?** The premise is that the MAS advantage reported on coding, math and QA benchmarks rests on those tasks offering a binary oracle — executable unit tests, a single numeric answer — which is exactly the feedback signal inner-loop workflow optimizers were designed to consume. Real scientific data analysis offers no such oracle: a clustering task admits many valid clusterings, a forecasting task can be partially correct along several numerical axes, a gap-filling task can produce a usable answer matching no reference. The paper's claim is that no existing benchmark supports the test: scientific-agent benchmarks such as BLADE, DiscoveryBench and ScienceAgentBench evaluate a single agent on a single attempt per task and therefore lack the within-task pool of samples an MAS optimizer needs, while spatial-temporal benchmarks provide the right data but the wrong prompt and metric.

ST-Bench contains **100 tasks adapted from published Earth-science studies**, expanded into **2,067 paper-grounded queries** and validated by domain experts.

## Mechanism

**Construction, four stages.** The suite is built top-down. First, **16 task categories** are fixed spanning the standard data-science pipeline: Clustering, Cross-Dataset Evaluation, Data Augmentation, Exploratory Data Analysis, Feature Analysis, Feature and Label Correlation Checking, Forecasting Modeling, Missing Value Imputation, Model Comparison, Model Distillation, Novel Evaluation Metrics, Performance Stratification, Prediction Modeling, Sampling Strategies, Transfer Learning, and Up/Downscaling. Second, each (category, domain) cell is populated with one or more peer-reviewed publications that operationalized that analytical skill on that domain's data; a few cells had no natural fit and are not represented. Third, each task is expanded into approximately twenty queries. Fourth, the queries are stratified into train / validation / test splits.

**Domains and counts.** Hydrology uses CAMELS (25 tasks), agriculture uses a compiled "CropBench" from two crop-yield sources (24 tasks), wetland methane uses X-MethaneWet / FLUXNET-CH4 (40 tasks), plus 11 general-control tasks on synthetic or general tabular data. The general set is explicitly *not* counted as a fourth domain: it is a negative control, so a system that scores high on General but low on the three Earth-science domains is failing the spatial-temporal task rather than the data-science task. Per-category task counts range from 4 (Model Distillation) to 11 (Feature and Label Correlation Checking).

**The four components of a query.** A *task prompt* phrases each task as a concise scientific objective without prescribing an algorithm, so a generated MAS must decompose the task and select tools rather than retrieve a memorised solution; each prompt also contains a block specifying the subset of data to use. *Dataset files* are converted to a uniform Parquet representation and staged into the working directory, so file-format handling is not the variable under test. *Defined metrics* are named numeric metrics each paired with an inequality target such as ">0.3" or "lower is better" — chosen over gold answers because many valid scientific solutions clear the same bar, and because the reported numeric value (not merely pass/fail) is the continuous quantity an inner-loop fitness function needs. A *reference* field cites the source publication, stored only for expert validation and coverage analysis and **not exposed** to the MAS methods or the single-agent baseline.

**Query scopes.** Each query attaches a *scope record* to the task's data — a named geographic, temporal or sample-size slice, a short description, a numeric size and a citation to the publication that defined it. The processed files are identical across queries within a task; the scope changes which subset the system must operate on, so train/test scope variation forces the optimizer toward workflows that generalize across data samples rather than ones tuned to a subset. The 2,067 queries are split into **1,184 train, 391 validation and 492 test** queries, stratified by task so every task has at least three test queries and a non-trivial train and validation pool.

**Evaluation metrics.** For each task the score is `score_t = success_rate_t × mean_pass_rate_t`, where pass rate is averaged over *realistic* test queries and set to zero when no realistic output is produced. A query counts as realistic only if it reports parsable finite metrics, includes at least one strictly positive numeric value and does not use a −1 sentinel. The system-level score is the sum over all 100 tasks, with a maximum of 100. Six comparative metrics sit alongside it: win rate and mean score gain against the single-agent baseline; cost ratios ρ_time and ρ_token (mean per-query wall-clock time and token consumption relative to the baseline); efficiency η = Δ_perf / max(ρ_time − 1, 0.1), the denominator clipped at 0.1 to avoid instability near a ratio of one; and generalizability gen(M) = mean over tasks of (score of the per-task variant − score of the per-category variant), where positive values mean narrow task-specific optimization helps.

**Training-time reward.** Because a binary oracle does not transfer to scientific analysis, the benchmark supplies a continuous reference-aware verifier used in place of each method's usual training scoring hook, while leaving the prompt the candidate sees unchanged: `s = 0.10·s_sanity + 0.40·s_target + 0.50·s_reference`. `s_sanity` is 1 for a finite numeric value, `s_target` is 1 if the value satisfies the metric's inequality target, and `s_reference` is the proportion of the cached single-agent reference value the candidate reaches, clipped to [0,1] and polarity-flipped for lower-is-better metrics. A single override removes the defensive-zero attractor: a zero value against a non-zero reference scores zero regardless of the other components. For approximately seven percent of queries where the single-agent reference is missing, the reference term is dropped and the remaining weights renormalized to 0.40 and 0.60. The per-query reward is the average of s across the query's metrics. The reward is wired evaluator-side, mirroring how each method consumes a binary oracle on coding benchmarks, so that any improvement is attributable to better candidate selection rather than to leaking reference information into the prompt.

**Two training protocols.** Under the per-task protocol a method optimizes separately on each of the 100 tasks using only that task's train and validation queries, producing 100 task-specific instances. Under the per-category protocol it optimizes on the union of train and validation queries of all tasks in a category, producing 16 category-level instances. Both are evaluated on the same 492 held-out test queries.

**Task annotation axes.** Each task carries a difficulty label (17 Easy, 49 Medium, 34 Hard) and four orthogonal tag axes recording the capability dimension (Modeling 31, Discovery 28, Optimization 23, Robustness 18), the pipeline stage (Modeling 33, Data Analysis 25, Evaluation 23, Data Preparation 19), the cognitive skill (Predictive 39, Diagnostic 33, Prescriptive 16, Descriptive 12) and the MAS-specific challenge (Synthesis 35, Parallel Search 23, Long-horizon Planning 23, Error Recovery 14, Decomposition 5). The difficulty mix is deliberately weighted toward Medium and Hard because MAS generation methods are unlikely to add value where a single agent already succeeds.

## Evidence

All results are **author-reported** from this single preprint; none has been independently replicated.

**Setup.** All MAS generation methods and the primary single-agent baseline use GPT-5 with identical max-token and temperature settings, so any difference is attributed to the workflow rather than the model; baselines on GPT-5.2 and GPT-4o are additionally reported but their scores are not disclosed in the inspected text. Five MAS generation methods are evaluated: task-level AFlow (Monte Carlo tree search over operator graphs), GPTSwarm (REINFORCE-style edge realization) and MetaAgent (one-shot finite-state-machine generation); query-level W4S (low-compute reinforcement-learned meta-agent) and AutoAgents (prompting-only Explorer baseline).

**Training budgets.** The per-task inner-loop budgets differ by method and are part of the comparison:

| Method | Inner loop | Per-task budget |
|---|---|---|
| MetaAgent | one-shot FSM generation | 1 round (no iterative selection) |
| AutoAgents | per-query Explorer | 1 round, 3 test-query cap |
| GPTSwarm | edge-realization optimization | 3 realizations × 2 validation queries |
| AFlow | MCTS over operator graphs | 2 rounds, 2 validation samples, 1 validation round |
| W4S | iterative meta-agent proposals | 3 iterations × 2 validation queries |

**Absolute performance on the 492 held-out test queries.** The GPT-5 single-agent baseline scores **11.0** out of 100. Nine of the ten MAS configurations (five methods under two training protocols) exceed it. The paper's text names the five highest-scoring configurations and the one that falls below the baseline; the remaining four per-task and per-category scores are not disclosed in the inspected text:

| MAS configuration | Absolute score |
|---|---|
| GPTSwarm per-category | 32.0 |
| GPTSwarm per-task | 30.3 |
| W4S per-task | 29.4 |
| AFlow per-task | 26.6 |
| W4S per-category | 26.0 |
| AutoAgents per-category | 8.2 |

The single exception, AutoAgents per-category, scores 8.2 — the paper attributes this primarily to a per-category test-query cap (stated as five test queries per category in the results section and as a three-test-query cap in the budget table) leaving most queries unreached.

**Coverage, not quality.** Conditional on producing realistic output, the strongest MAS configurations clear a similar share of inequality targets as the single-agent baseline, typically **50–58%**; realistic output rates vary much more widely across methods, with W4S per-task the highest at **38.2%**, GPTSwarm and AFlow configurations at intermediate rates, and AutoAgents per-category the lowest. The decomposition is the paper's central finding: the MAS advantage comes from more often reaching the point where scientific metrics can be computed at all, not from producing better metrics once there.

**Cost-performance.** The MAS configurations that beat the baseline pay between roughly **1.85× and 4.5×** the single-agent inference time. GPTSwarm per-category gains **+21.1 percentage points** over the baseline at about **4.5×** the inference time; GPTSwarm per-task has the highest task win rate (**51%**) at a similar cost ratio; W4S per-task is the most efficient point on the frontier, gaining **+18.4 percentage points** at **1.85×** the inference time and yielding the highest gain per unit of additional compute, with AFlow per-task next most efficient. AutoAgents per-category is dominated, with a negative mean improvement. No single configuration dominates on both axes.

**Training-granularity generalization.** GPTSwarm and MetaAgent sit near or below zero on the per-task minus per-category gap, meaning their category-level workflows transfer cleanly to held-out sibling tasks. AFlow and AutoAgents gain strongly from per-task specialization, suggesting their workflows overfit or dilute on a broader category pool. W4S sits between the two regimes. The paper's reading: broader training pools help only when the induced workflow is abstract enough to transfer.

**Stratified results.** By domain, MAS improves all three but not uniformly: on MethaneWet the GPT-5 score is 8.2 on average while GPTSwarm reaches 40.1 per-category and 40.7 per-task; on CAMELS, GPTSwarm per-category and AFlow per-task are both near 29; CropBench is the weakest MAS domain, with GPTSwarm per-category at 23.6 and W4S per-task at 21.5. By task tag, the best MAS configuration per group is selected and compared with the group's GPT-5 mean:

| Tag axis | Tag value | Tasks | GPT-5 | Best MAS | Gain (pp) | Win rate |
|---|---|---|---|---|---|---|
| Capability | Discovery | 28 | 11.2 | GPTSwarm cat 38.6 | 27.4 | 57.1% |
| Capability | Modeling | 31 | 9.9 | W4S cat 32.4 | 22.5 | 54.8% |
| Capability | Optimization | 23 | 18.0 | GPTSwarm task 41.1 | 23.1 | 56.5% |
| Capability | Robustness | 18 | 3.5 | W4S task 38.2 | 34.7 | 61.1% |
| Cognitive | Descriptive | 12 | 10.0 | GPTSwarm cat 41.7 | 31.7 | 58.3% |
| Cognitive | Diagnostic | 33 | 10.2 | W4S task 35.5 | 25.3 | 57.6% |
| Cognitive | Predictive | 39 | 8.7 | W4S cat 38.5 | 29.8 | 59.0% |
| Cognitive | Prescriptive | 16 | 19.0 | W4S task 44.0 | 25.1 | 68.8% |
| MAS challenge | Decomposition | 5 | 6.0 | AFlow task 40.0 | 34.0 | 40.0% |
| MAS challenge | Error recovery | 14 | 8.0 | MetaAgent cat 25.1 | 17.1 | 57.1% |
| MAS challenge | Long-horizon planning | 23 | 16.2 | W4S cat 47.2 | 31.0 | 60.9% |
| MAS challenge | Parallel search | 23 | 6.1 | GPTSwarm task 39.1 | 33.0 | 60.9% |
| MAS challenge | Synthesis | 35 | 12.7 | W4S task 33.0 | 20.3 | 57.1% |
| Pipeline | Data analysis | 25 | 11.7 | GPTSwarm cat 42.4 | 30.7 | 60.0% |
| Pipeline | Data preparation | 19 | 7.0 | W4S task 42.2 | 35.2 | 73.7% |
| Pipeline | Evaluation | 23 | 7.1 | W4S cat 35.9 | 28.8 | 60.9% |
| Pipeline | Modeling | 33 | 15.4 | GPTSwarm task 34.4 | 19.0 | 51.5% |

By difficulty, MAS improves Easy, Medium and Hard alike by roughly 22 pp under the best configuration, and the best per-category MAS is slightly stronger than the best per-task MAS at every difficulty level. The declared difficulty labels are not monotonic with baseline performance — Easy tasks have the lowest GPT-5 score at 4.3 and Hard the highest at 17.4 — which the paper attributes to the one-turn baseline being dominated by execution brittleness rather than scientific complexity.

## Limitations

**Stated by the authors.** The paper's conclusion is explicitly cautious: its contribution is "not a claim that current MAS methods solve scientific data analysis, but a benchmark and evaluation framework together with empirical findings." The benefit is described as "conditional rather than universal". The token axis is explicitly partial: token accounting is consistently available for the single-agent baseline but not for every MAS adapter in the current release, so ρ_token is reported only where available and treated as a partially measured axis. The parallelism axis reports only a wall-clock proxy (wall-clock cost relative to summed agent time); a full audit of internal subtask parallelization is left to future work. The generalizability axis is defined as a mean per-task minus per-category score gap.

**Assessed from the reporting.**

- **Single source, no public artifact located.** Everything rests on arXiv:2610.07763 v1 (6 October 2026). A full-text search of the inspected HTML for a code or benchmark-release URL found none; the external links that do appear point to the upstream *source datasets* (CAMELS at Zenodo, CY-Bench at agml.org, the DOIs of the adapted publications), not to a release of the tasks, Parquet files, reward function or evaluation code. The paper's phrase "the current release" for token accounting and parallelism therefore refers to a release whose location is not given in the inspected text, and no independent replication is known.
- **The baseline is weak in absolute terms.** GPT-5 scores 11.0 out of 100, and the difficulty breakdown shows Easy tasks at 4.3. A large part of the measured gain may be recovering from execution brittleness — parsing, data loading, exception handling — rather than from any coordination advantage the multi-agent structure provides.
- **The score is a product, and the product structure rewards coverage.** `score_t = success_rate × pass_rate` means a system that never produces realistic output scores zero regardless of potential quality, and a system that produces realistic output on a few queries scores near zero. This is a deliberate anti-defensive-default design, but it makes the headline number sensitive to the realistic-output filter's threshold (at least one strictly positive numeric value, no −1 sentinel) — a threshold not ablated in the paper.
- **The training reward is partly circular.** `s_reference` measures closeness to a cached *single-agent* reference value, so 50% of the training reward is similarity to the baseline the MAS is being compared against, and the same cached reference is used to penalize zero outputs. That is a sensible way to suppress defensive defaults, but it means the optimization target is not independent of the comparison baseline; the paper does not report an ablation with the reference term removed.
- **Ten configurations, no repetitions.** No seeds, repeated runs, confidence intervals or significance tests are reported for the headline scores, and the 100 tasks are averaged into one number per system.
- **The best configuration is not uniformly best.** GPTSwarm per-category wins on absolute score and GPTSwarm per-task on win rate, while W4S per-task wins on efficiency, and the granularity split (GPTSwarm/MetaAgent transfer well, AFlow/AutoAgents do not) means a "best method" does not exist across axes. Any summary that names one winner is choosing an axis.
- **Domain coverage is narrow.** Three Earth-science domains plus a synthetic control set, all from the same data families (CAMELS, crop yield, wetland methane flux); the benchmark does not test chemistry, biology or physics data analysis even though the related-work section surveys agents for those domains.
- **Metric targets are inequality thresholds, not correctness.** A metric "clears" when it passes a bar such as ">0.3", so a configuration can score a pass rate of 50–58% while producing numbers far from any published result; the reference-aware reward partly compensates during training, but the test-time score does not measure closeness to the paper's value.
- **The stratified tables select the best configuration per group**, which is a favourable presentation; the unselected configurations' per-group numbers are not disclosed in the inspected text.
- **No code, so the framework cannot be re-run as specified.** Even the reward function's caching of single-agent references and the "current release" mentioned for token accounting imply an internal codebase that is not linked.

## Competing approaches

**MAS generation methods evaluated head-to-head** are AFlow, GPTSwarm, MetaAgent, W4S and AutoAgents — the two families the paper distinguishes (task-level optimizers that produce one workflow per problem, and query-level methods that produce a fresh workflow per query through a meta-agent or in-context controller), with AutoAgents included as a prompting-only Explorer baseline.

**Benchmarks the paper compares itself against** (Table 1): SWE-Bench, AgentBench, TaskBench and MLAgentBench all lack within-task query pools and multi-axis evaluation, with binary reward signals except MLAgentBench (continuous); BLADE, DiscoveryBench and ScienceAgentBench draw on publications but provide no MAS-optimization pool, with BLADE and DiscoveryBench binary and ScienceAgentBench mixed, and only ScienceAgentBench having partial multi-axis evaluation.

**Domain scientific agents** cited as related but not compared: single-agent chemistry systems Coscientist and ChemCrow; multi-agent systems AI Co-Scientist, OmniScientist, ProtAgents, GenoMAS, The AI Scientist and The AI Scientist-v2. The paper's point is that each is evaluated on narrow case studies, leaving the relative contribution of multi-agent coordination unmeasured in any standardized way.

**General MAS framework lineage** in the introduction: hand-crafted role decompositions and communication protocols (CAMEL, AutoGen, MetaGPT, AgentVerse, Self-Refine) and the later line treating the workflow itself as an optimizable object (GPTSwarm, AFlow, MetaAgent, ADAS, FlowReasoner, and multi-agent architecture search via an agentic supernet). The paper's stated contribution is to make agent construction and optimization the *object of evaluation* rather than a method.

Within this knowledge base, [[projects/masbench]] and [[projects/tandembench]] cover multi-agent system evaluation from a different angle, and [[projects/auto-research]] covers research-automation pipelines; the specific contrast here is coverage versus conditional quality, which the paper makes explicit. The page also belongs to [[benchmarks/index]] and to the cross-briefing layer recorded in [[evaluations/briefing-synthesis-2026-11-03-to-09]], and its realistic-output filter feeds [[concepts/verified-completion-vs-apparent-success]].

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The first takeaway is a measurement lesson that generalizes past multi-agent systems: **report coverage and conditional quality separately**. ST-Bench's most useful contribution is arguably the decomposition, because a single composite score can be lifted by either "answered more questions" or "answered the ones it answered better", and those have completely different engineering consequences. The paper shows both that the two can move together (a stronger workflow may answer more queries *and* be right more often) and that a gain can come almost entirely from the first. Any evaluation of a multi-component system — a research pipeline, a multi-stage code generator, a multi-agent team — should carry the same two-axis plot. It is also directly the [[concepts/preservation-aware-agent-improvement]] question in a new setting: does the improved system preserve quality while extending coverage?

Second, the anti-defensive-default machinery is directly transferable engineering. The realistic-output filter, the −1 sentinel ban, and the "zero against a non-zero reference scores zero" override are cheap rules that defeat a whole family of failure modes in which an agent returns a well-formed answer that computes nothing. Teams running agents against scientific or analytical pipelines should adopt that filter before they adopt any agent framework.

Third, the cost result is the one most likely to be quoted out of context. "Multi-agent systems nearly triple the composite score" is true at 4.5× the inference time; the economically interesting configuration is W4S per-task at +18.4 points for 1.85× the time. Any decision to adopt multi-agent generation should be taken at the efficient point of the frontier, not the absolute-score point — and the paper is unusually clear that no configuration dominates both.

Fourth, the granularity result is a design rule for MAS builders: a workflow trained on a broader pool transfers only if it is abstract enough to transfer. AFlow and AutoAgents degrade when trained per-category; GPTSwarm and MetaAgent do not. If you are investing in specialized roles, the training-pool breadth has to be matched to how abstract the induced workflow is, and the paper gives a cheap way to check it: train at both granularities and measure the gap.

Fifth, the design of the training reward deserves scrutiny by anyone copying it. Anchoring 50% of the reward to closeness to a single-agent reference is a clever way to get a continuous signal out of an open-ended task, but it optimizes the workflow toward the baseline's numbers, which is a conservative target: it can reward "do it like the single agent, but further" and penalize a genuinely better method that lands on a different, more accurate value. The paper reports no ablation without the reference term, so the contribution of that anchoring is unmeasured.

Sixth, a caution on generality. Three Earth-science domains, one backbone family and a baseline scoring 11 out of 100 mean the "conditional rather than universal" conclusion should be read as being about *this* setting. What transfers is the evaluation framework, not the ranking.

## Reproducible experiment

No artifact release was located in the inspected text, so a check means reimplementing the framework from the paper. A feasible independent test of the central decomposition claim:

1. **Coverage versus quality, on your own tasks.** Take 20–30 of your own analysis tasks with numeric outputs, define one inequality target per metric, and compute for each system two numbers: the rate of realistic outputs (parsable, finite, at least one strictly positive value, no −1 sentinel) and the mean pass rate conditional on realistic output. The paper's reference pattern is a narrow conditional band of 50–58% against widely varying realistic-output rates (38.2% for the best configuration, lower for others). A reproduction in which the conditional band also varies widely would falsify the claim that the MAS gain is primarily a coverage gain.
2. **The coverage-only ablation.** Add a single-agent baseline condition with the same backbone, the same prompts and the same per-query budget, and compare coverage rates directly rather than the composite score. If the single agent's coverage is close to the MAS coverage, the multi-agent structure is not what produces the gain.
3. **Defensive-default stress test.** Build a small set of adversarial queries where the easy answer is a sentinel (-1) or a zero with a passing-looking output, and measure how often each system falls into it. The paper does not report per-system sentinel rates, so this is an unmeasured dimension; a system with a high composite score but a high sentinel rate would show that the anti-default machinery, not the workflow, is doing the work.
4. **Cost frontier.** Measure wall-clock inference time per query for both single-agent and MAS configurations and plot mean score gain against cost ratio. The paper's claim is that the ordering of methods changes when cost is considered (GPTSwarm per-category is best on score, W4S per-task best on efficiency). A reproduction in which one method dominates on both axes would contradict the paper's cost-performance conclusion.

Substituting an available backbone for GPT-5 is unavoidable, and the substitution, budget and per-query cost accounting should be reported with the results.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2610.07763) and the complete HTML full text including the technical appendices A–D and the reference list (https://arxiv.org/html/2610.07763v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; the five MAS methods and the single-agent baselines were run by the authors on one GPT-5 backbone; the paper is a single preprint (v1) with no peer-reviewed venue claimed. A full-text search of the inspected HTML for a code or benchmark-release URL found none — the external links in the text point to upstream source datasets and publications — so no artifact is publicly linked in the inspected text. The scores for the GPT-5.2 and GPT-4o baselines, the per-configuration realistic-output rates other than W4S per-task's 38.2%, the token cost ratios, and the per-task values behind Figures 2–6 are not disclosed in the inspected text and are not reported here. Claim types are separated in the text: the "first scientific benchmark with signals fine-grained enough to drive MAS workflow optimization" claim and the "conditional rather than universal" conclusion are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed or tested by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-08]] — dated full-fidelity research briefing that created this canonical record.
