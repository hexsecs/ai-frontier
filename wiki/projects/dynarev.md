---
uid: d01a9540-9153-4b9a-9463-07c0618570cd
depth: deep
title: "DynaRev: Benchmarking Web Agents under Dynamic Goal Revision"
summary: "DynaRev: 181-task web-agent benchmark delivering additive and override goal revisions at semantic milestones, scored for correctness, responsiveness, and cost."
type: project
created: 2026-11-01
updated: 2026-11-02
sources:
  - url: https://arxiv.org/abs/2610.40133
    retrieved: 2026-11-02
  - url: https://github.com/zsq259/DynaRev
    retrieved: 2026-11-02
---

# DynaRev

## What it is

DynaRev is a **benchmark**, not an agent or a technique: 181 web tasks that test whether a browser agent can cope when the user changes the goal partway through execution. It was built by Shiqi Zhang, Guochen Zhou, Zesheng Wei, Hai Zhao, and Zhisong Zhang (City University of Hong Kong and Shanghai Jiao Tong University) and released as an arXiv preprint in October 2026; no peer-reviewed venue is stated.

The motivation is a gap in static web-agent benchmarks such as Online-Mind2Web and Mind2Web 2 (the two seed sources DynaRev is built from): their tasks "generally specify the complete user objective before execution and keep it unchanged throughout the interaction." Real users do not behave that way — they add requirements, change their minds, and state contingencies once they see intermediate results. DynaRev delivers such revisions mid-execution, at **semantic milestones** in the task rather than at fixed step counts, and scores agents on three distinct axes: correctness against the final revised goal, responsiveness immediately after each revision, and cost-aware efficiency.

Five models were evaluated by the authors — DeepSeek-V4.1-Flash, GPT-6.1-Sol, Gemini-3.8-Flash, Qwen3.8-Flash, and Claude-Opus-5-5 (identifiers as printed in the paper). The headline result is that mid-task goal revision is far from solved: the best strict task success rate is 43.1%, so no evaluated agent completes even half the tasks fully once goals start changing. Code and data are public at [github.com/zsq259/DynaRev](https://github.com/zsq259/DynaRev); the repository's three data files (76 additive, 62 unconditional-override, 43 conditional-override tasks) sum to the paper's 181 tasks.

## Mechanism

**Task form.** A task is $T=(I_0,\{(M_k,I_k)\}_{k=1}^{n})$: an initial instruction $I_0$, plus revisions $I_k$, each delivered when its milestone $M_k$ fires. Every instruction decomposes into **atomic constraints** — "each describing an independently verifiable requirement" — and constraints are the unit of both construction and scoring: a revision updates which constraints are active.

**Semantic milestones.** A milestone is "an *inevitable semantic stage* of the goal that has already been specified before revision $I_k$" — for example, "the initial search for daytime flights from New York to Los Angeles has been completed and the search results have been observed." Crucially, a milestone is derived from the previously specified goal, never from the revision that follows it, and any successful execution path must pass through it regardless of the UI actions used. An LLM-based semantic judge evaluates the trigger against the current web state; when it fires, the revision is delivered before the agent's next step. This is the design's answer to fixed-step or fixed-relative-position injection, which exposes different agents to the same revision at different task stages (the paper's timing analysis, under Evidence, quantifies how large that confound is).

**Revision types.** Three kinds, illustrated with the paper's running flight example:

1. **Additive** — a new constraint is added while previously active constraints are preserved: "Only consider nonstop flights."
2. **Unconditional override** — a previously active constraint is replaced outright: "Actually, choose an overnight flight instead."
3. **Conditional override (runtime-conditioned override)** — a constraint is replaced only if a runtime condition, verifiable from the web state, holds: "If daytime flights cost more than $150 extra, overnight flights are acceptable." The agent must resolve the branch itself: "In a conditional override, the agent must determine the applicable branch and corresponding active constraints from the web state, rather than receiving them from the revision." Conditions are numerical thresholds over observable quantities (price or rating differences, distance) or existence conditions (an item in stock, a direct flight exists).

One scoping decision matters for interpreting results: override revisions are constructed **only from preference constraints** (colour, price range, rating, ranking) — never from core constraints that define the task object itself (product category, destination). The paper's rationale is that preferences are what users naturally revise; the consequence, noted under Limitations, is that override difficulty here is a lower bound on real revision difficulty.

**Construction.** The pipeline runs in five stages: decompose each seed task's goal into atomic constraints; build a coherent initial instruction from the *required* constraints; organise the remaining constraints into revisions in a natural interaction order, each paired with a semantic milestone; quality-control for structural validity and interaction naturalness (milestones implied by preceding goals and independent of any reference trajectory, conditional triggers observable at runtime, revision–constraint consistency), regenerating or excluding failures; and finally, as a deliberately separate post-processing stage, bind each constraint to the instruction that introduces or modifies it — the authors keep binding separate so revisions are not "constructed merely to correspond to a convenient subset of constraints." From 70 sampled seed tasks per source (140 total), 99 seeds contribute at least one retained task, yielding the 181 tasks. Mind2Web 2 tasks carry roughly double the constraints of Online-Mind2Web tasks (≈9.7–10.0 vs ≈4.6–5.7 per task) and longer revision sequences (average 3.22 rounds overall).

**Execution harness.** All agents run in BrowserGym with Playwright-controlled headless Chromium, viewport-restricted accessibility-tree observations, a **100-step budget, and temperature 0**, identically configured. The agent receives the accumulated instructions and full action history, but complete web observations are retained only for the five most recent steps (earlier ones are replaced by a fixed placeholder). If an agent declares completion while revisions are still pending and budget remains, the declaration is intercepted, the next revision is delivered, and execution continues.

**Evaluation.** Scoring is trajectory-grounded, in the agent-as-a-judge paradigm. Each constraint is decomposed into independently verifiable claims — *simple* claims checked against the agent's final response, and *page* claims requiring evidence retrieved from recorded web states in the trajectory — and a constraint counts as satisfied only if **all** its claims verify. Constraints belonging to revisions that were never delivered count as unsatisfied. Four metric families result: **Score** (mean fraction of constraints satisfied), **task success** (the strict all-constraints rate), **MFFR** (mean first failure round — how many revision rounds an agent survives before first failing a revision's constraints), **WRA** (Window Response Accuracy — an LLM judge examines at most the three actions following each delivered revision and decides whether behaviour is consistent with the revised intent), and a cost-aware efficiency measure **CE**, which the appendix proves equals the normalised area under the cumulative constraint-satisfaction curve over steps or tokens.

## Evidence

All results below are **author-reported** from the single preprint; conditions are stated with each result, and no independent replication exists (see Evidence status).

**Main results (all 181 tasks, BrowserGym, 100-step budget, temperature 0).** Gemini-3.8-Flash achieves the best mean constraint satisfaction, **Score 0.735**, the best MFFR (2.28 rounds), and the best cost efficiency under both step and token costs. DeepSeek-V4.1-Flash achieves the best **strict task success, 43.1%** — meaning even the leader fully satisfies every constraint on fewer than half the tasks, while its mean Score (0.698) ranks second. The two rankings genuinely diverge: Qwen3.8-Flash has a lower Score than Claude-Opus-5-5 (0.604 vs 0.681) but a higher success rate (39.2% vs 36.5%). GPT-6.1-Sol uses the fewest steps (24.9 on average) yet posts the lowest Score (0.598) and the earliest first failures (MFFR 1.91); it accumulates performance quickly under small budgets but plateaus early, whereas Gemini and DeepSeek keep improving as budget grows. The paper's own summary: "agents often satisfy only part of the task requirements."

**Breakdown by source and revision type.** Mind2Web 2 yields lower scores for every model and revision type — consistent with its higher constraint counts and longer revision sequences — and generally costs more steps. The best single cell is Gemini on Online-Mind2Web conditional tasks (Score 0.898); the worst is Qwen on Mind2Web 2 conditional tasks (0.275, at 80.0 average steps, close to the budget ceiling). Conditional tasks are not uniformly hardest: on Online-Mind2Web they are not the weakest subset for four of five models, though on Mind2Web 2 they are lowest for three of five. The authors conclude that task complexity produces a consistent gap, while differences among revision types vary by source and agent.

**Responsiveness is not satisfaction.** WRA is narrow across all five models (66.8% for DeepSeek to 69.4% for Gemini), and its ordering does not track final correctness. Revisions an agent responds to immediately (WRA = 1) do end with higher final satisfaction than ones it ignores — for all five models — but the gap is modest for most (DeepSeek 0.683 vs 0.644; Gemini 0.720 vs 0.696; the largest gap is GPT's 0.587 vs 0.465), and "many responsive revisions remain unsatisfied." Immediate behavioural adaptation and eventual constraint satisfaction measure different things, and an agent can visibly pivot to a revised goal yet still fail it. Round-wise diagnostics reinforce this: constraint satisfaction declines with revision-round depth for most models (e.g. GPT falls from 63.1% at the initial instruction to 28.5% at round 4+), while WRA shows no comparable collapse.

**Dynamic vs static delivery.** On 30 additive tasks paired with single-turn counterparts carrying identical final requirements and budget, progressive delivery improves the outcome in 32.0% of model–task pairs, worsens it in 28.0%, and leaves 40.0% unchanged — "no uniform effect on correctness: GPT and Qwen improve on both sources, Claude declines on both, while Gemini shows opposite trends across the two sources." Dynamic delivery typically costs more actions. The authors' interpretation: progressive delivery can proceed through intermediate stages, but also introduces "rework, interface loops, and budget exhaustion," exposing model-dependent execution behaviour that static evaluation does not reveal.

**Revision-handling strategies — the actionable result, with narrow conditions.** In a separate study on **one model only (DeepSeek-V4.1-Flash)** and an unspecified subset of benchmark tasks, the authors varied how a delivered revision is handled. The winning strategy has **two** halves, and the page this replaces kept only one of them:

- **Rewrite + preserve state:** when a revision arrives, consolidate the accumulated instructions into a rewritten current goal *and* continue from the current browser state. This raised Score from 0.647 to **0.718** while *reducing* steps (50.3 → 44.9) and token usage (806.7k → 658.8k). "Rewriting the accumulated instructions while preserving the ongoing execution gives the best overall trade-off."
- **Browser reset is harmful:** resetting the browser on revision lowered Score to 0.586 with more steps (59.7), and Reset + Rewrite was worst of all (0.525, 61.5 steps, 843.6k tokens) — rewriting cannot recover discarded execution progress. Clearing interaction history alone was roughly neutral for quality (0.648) with fewer tokens but more steps.

The authors' conclusion: "the results favor reorganizing the accumulated goal while continuing from the current execution, rather than treating each revision as a new task." The case studies name the matching failure modes: resets discarding progress until budget exhaustion; immediate adaptation without eventual satisfaction; and correct condition resolution without corresponding action (the agent identifies a newly eligible cheaper option, then selects a more expensive one).

**Milestone timing.** The justification for semantic delivery is measured, not asserted: across agents executing only the initial instruction, the first milestone's relative position averages 56.8% of the trajectory with a standard deviation of 28.5 percentage points, and the per-task spread between the earliest and latest agent has a median of 36.4 points (70.0% of tasks exceed 20). A fixed relative position would therefore deliver the same revision at substantially different task stages to different agents.

## Limitations

The authors state three limitations: the benchmark is constructed from static web tasks and "may not capture the full diversity of real-world goal changes"; milestone triggering and evaluation "rely on imperfect LLM-based semantic judgments"; and semantic milestones assume identifiable intermediate task stages, "which may be harder for tasks with highly diverse successful trajectories."

The following are **analyst-assessed** — they follow from the method as described and are not stated by the authors. The first is load-bearing for reading every number on this page:

- **Constructor–judge–contestant circularity.** Per §6.1 of the paper, **DeepSeek-V4.1-Flash is used for data construction, milestone judging, and offline evaluation** — it helps build the tasks, decides when milestones fire during runs, and judges constraint satisfaction and responsiveness offline. The same model is also one of the five evaluated agents, and it is the one that posts the **highest strict success rate (43.1%)**. This does not invalidate the results — DeepSeek ranks only second on mean Score, behind Gemini — but its success-rate lead is obtained under its own model as trigger and judge. Self-preference and shared-blind-spot risks are unmeasured: the paper reports no cross-judge replication (for example, re-scoring all trajectories with a different judge model).
- **The strategy result is single-model and subset-unspecified.** The rewrite-and-preserve finding — the paper's most actionable claim — is evaluated only with DeepSeek-V4.1-Flash, on "the same subset of benchmark tasks" whose size and selection §7.2 does not state. Generalisation to other agents is asserted by framing, not demonstrated.
- **Small, derived sample; no uncertainty estimates.** 181 tasks derive from 99 contributing seed tasks in one domain family (web navigation and agentic search). The Mind2Web 2 conditional cell contains only 12 tasks, so per-cell figures such as Qwen's 0.275 rest on very small n. No confidence intervals or significance tests are reported for any headline table.
- **Judge validation is thin.** The only human validation reported covers milestone-trigger timing on 30 sampled cases (three-way agreement 83.3%, Cohen's κ = 0.438; the Q1 κ prints as a degenerate 0.000). No human-agreement study is reported for the constraint-verification judge or the WRA judge, which carry all headline metrics. Relatedly, scoring undelivered revisions' constraints as unsatisfied conflates trigger failure — partly a property of the harness and its judge — with agent failure.
- **WRA is immediate-window responsiveness only.** The response window is at most three actions; an agent that adapts on the fourth action scores as unresponsive. "Responsiveness" on this page and in the paper means adaptation within that window.
- **Revision realism is bounded by construction.** Overrides touch only preference constraints, so core-goal reversals (change the destination, change the product) are untested; there is no retraction type; and because revisions are synthesised by decomposing a static final goal, every revision is consistent with a coherent final goal known to the constructors. Real mid-task revisions can be contradictory, mistaken, or withdrawn without leaving a clean constraint set — none of that is exercised here.
- **Reproducibility caveats.** Temperature 0 with a single run per configuration, as described, reports no run-to-run variance; and because seed tasks descend from live-website benchmarks, site drift means exact numbers may not reproduce over time even with the released code and data.

## Competing approaches

DynaRev positions itself against a first generation of dynamic-goal benchmarks, each missing at least one of its three contributions (semantic-aligned delivery, conditional revisions, revision-level evaluation):

- **InterruptBench** (Zou et al. 2026) — the closest relative per the paper: user additions, revisions, and retractions during long-horizon web navigation, scored on post-interruption success and execution cost. DynaRev's stated deltas are task-semantic alignment of delivery and conditional revisions. Note the trade: InterruptBench includes **retractions**, which DynaRev lacks.
- **AgentChangeBench** (Rana et al. 2025) — goal shifts and recovery in conversational tool-using agents, not web tasks.
- **DeskCraft** (Wang et al. 2026) — interruptions and corrections in desktop GUI workflows rather than the web.
- **IntentFlux** (Zhang et al. 2026), **COMPASS** (Qin et al. 2026), **RECAP** (Mitra et al. 2026) — intent drift and evolving constraints in multi-turn interaction.
- **ReInAgent** (Jia et al. 2025) — context-aware GUI agent with human-in-the-loop mobile navigation.

The static predecessors are the seed benchmarks themselves (Online-Mind2Web, Mind2Web 2) and the broader static web-agent suite the paper surveys — Mind2Web, WebArena, VisualWebArena, WorkArena/WorkArena++, WebVoyager — plus multi-turn predecessors MT-Mind2Web and WebLINX, and fine-grained evaluation predecessors (Mind2Web 2's criterion decomposition, ProBench). Two alternatives are evaluated *within* the paper rather than merely cited: fixed relative-position revision injection, rejected on the timing-variance evidence; and revision-handling strategies — browser reset, history clearing, instruction rewriting — of which direct continuation with rewriting wins and reset loses (see Evidence).

## Implications

**For agent builders**, the strategy study is the takeaway, within its single-model limits: treat a goal revision as an edit to a living specification, not a new task. Maintain one consolidated, rewritten statement of the current goal (initial instruction plus all revisions applied), and continue executing from the current browser state — progress already made is an asset that restarts throw away. The failure-mode catalogue adds a subtler warning: visibly adapting to a revision is not the same as satisfying it, so self-checks should verify revised constraints against the final state, not against the pivot.

**For evaluation practice**, DynaRev demonstrates that three quantities static benchmarks conflate — partial correctness (Score), strict completion (success), and immediate responsiveness (WRA) — can rank the same five models differently and respond differently to delivery timing. Reporting only task success would hide both the partial-credit picture (a 0.735 mean Score alongside a 43.1% best success rate) and the responsiveness–satisfaction gap. The static-vs-dynamic comparison cuts the other way as well: delivering identical final requirements progressively changes outcomes in model-dependent directions, so single-turn scores do not predict performance under revision.

**For benchmark design**, revision *timing* is an experimental confound that semantic milestones control and fixed positions do not — the measured 36.4-point median cross-agent spread in milestone position is the concrete evidence. The circularity caveat generalises too: when one model constructs tasks, triggers events, and judges outcomes, its own ranking under that benchmark deserves discounted confidence until a cross-judge replication exists. Related synthesis lives at [[techniques/evaluation-and-simulation]] and [[techniques/adaptive-recovery]].

## Reproducible experiment

The authors release code and data at [github.com/zsq259/DynaRev](https://github.com/zsq259/DynaRev). For this page the repository was verified live via its README on 2026-11-02 — the three JSONL data files' task counts (76 + 62 + 43 = 181) match Table 1 — but the code was **not cloned or executed**, per this KB's policy on untrusted code.

A faithful replication needs: the released task data; BrowserGym with Playwright-driven headless Chromium; viewport-restricted accessibility-tree observations; a 100-step budget at temperature 0; the milestone judge and the trajectory-grounded constraint/WRA evaluators; and API access to the evaluated models (the seed datasets, Online-Mind2Web and Mind2Web 2, are on Hugging Face). Two extensions would test this page's open questions directly:

1. **Cross-judge replication.** Re-score the released (or freshly collected) trajectories with a judge model other than DeepSeek-V4.1-Flash, and re-run milestone triggering under a different judge. If DeepSeek's success-rate lead survives an independent judge, the circularity concern is answered; if it inverts, the headline ranking was partly an artefact.
2. **Strategy study, generalised.** Repeat the §7.2 comparison (baseline / rewrite / clear / reset and combinations) on at least two additional models over a stated, fixed subset, with run variance reported. This tests whether "rewrite the accumulated goal, preserve the browser state" is a general agent-design rule or a DeepSeek-specific result.

Exact numerical reproduction should not be expected over time: the tasks descend from live-website benchmarks, and site drift moves the target.

## Evidence status

The primary source (arXiv:2610.40133, HTML full text including appendices and all tables) was read in full on 2026-11-02 for issue #2, and the code/data repository's existence and task counts were verified against its README the same day; the code was not run and the benchmark was not re-executed. Every quantitative result on this page is **author-reported** from that single preprint: no independent replication was located, and the authors claim none. Model identifiers (GPT-6.1-Sol, Gemini-3.8-Flash, Qwen3.8-Flash, Claude-Opus-5-5, DeepSeek-V4.1-Flash) are reproduced as printed in the paper and have not been silently "corrected" to other releases. Items labelled analyst-assessed under Limitations are inferences from the paper's stated method, not claims made by the authors. This page replaces the earlier import, whose own label — metrics "not independently reverified" — was accurate; the contents have now been verified against the source text, which is a weaker claim than independent reproduction of the benchmark.

## Historical coverage

[Briefing 2026-11-01](../briefings/2026/11/2026-11-01.md)
