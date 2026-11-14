---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c03
depth: deep
title: "MASBench"
summary: "Multi-agent collaboration benchmark that isolates protocol, memory and routing effects under deliberately partial observability."
type: benchmark
created: 2026-11-08
updated: 2026-11-10
related: [protocol-relative-scores, capability-locus, evaluator-circularity]
sources:
  - url: https://arxiv.org/abs/2610.04672
    retrieved: 2026-11-10
  - url: https://arxiv.org/html/2610.04672v1
    retrieved: 2026-11-10
  - url: https://arxiv.org/html/2610.04672v2
    retrieved: 2026-11-10
---

# MASBench

## What it is

MASBench is a multi-agent collaboration benchmark built under **partial observability**: each agent sees only its own slice of the world and must exchange information with teammates to finish the task. It is reported in the arXiv preprint "MASBench: Benchmarking LLM-based Multi-Agent Collaboration under Partial Observability" (arXiv:2610.04672, v1 submitted 3 October 2026; the abstract page lists a v2 of 4 November 2026 as the current version — preprint, no peer-reviewed venue claimed). The paper lists eight authors — Qizhi Chu, Zekai Yu, Sijie Wen, Yang Liu, Chen Qian, Cheng Yang, Chuan Shi and Zhiyuan Liu — at Beijing University of Posts and Telecommunications, Shanghai Jiao Tong University and Tsinghua University. The paper states that code is available at https://github.com/BUPT-GAMMA/MASBench.

The problem the authors name is that multi-agent benchmarks generally assume **global observability**, which trivializes the difficulty of real teams, and that benchmarks using LLM-as-a-judge are prompt-sensitive and biased. MASBench's design bet is that partial observability can be turned into a controlled instrument: construct tasks so that a *specific* collaboration mechanism is necessary to close an information gap, then score the outcome and the communication cost deterministically. Its three task categories — Reasoning, Scheduling, Game — are ordered by mechanism demand (Protocol; Memory + Protocol; Memory + Protocol + Routing), and each category exercises only the mechanism subset that its interaction structure makes meaningful.

## Mechanism

The system is formalized as a goal **G**, a set of agents **A**, and a shared environment **E**. Each agent is a tuple ⟨O_i, m_i, M_i, D_i, C_i⟩: an observation function over its local view plus received messages, a memory, a memory-management function, a decision function over the environment, and a communication function over other agents. Three mechanisms are operationalized: **memory** (record, summarize and retain state across rounds), **routing** (decide who talks to whom and when), and **protocol** (constrain messages to schemas and interaction rules).

**Task families and sizes (Table 1 of the paper).**

| Category | Agents | Instances | Mechanisms exercised |
|---|---|---|---|
| Reasoning | 2 | 300 (200 Simple / 100 Complex) | Protocol |
| Scheduling | 5 | 200 (100 / 100) | Memory, Protocol |
| Game | 4–8 | 100 maps (50 / 50) | Memory, Protocol, Routing |

**Reasoning.** Multi-hop HotpotQA instances are adapted: the evidence chain is decomposed and split across two agents, so neither can answer alone. Each instance passes a four-part quality filter whose composite score s ∈ [0,4] sums a format check (JSON schema integrity plus a soft supporting-fact coverage score, each agent's coverage = assigned supporting facts / 5, capped at 1, averaged over the two agents), a question-validity check verified via Gemini-Flash (the question must be unanswerable without the provided context), a sufficiency check (the referenced supporting-fact sentences alone must recover the ground-truth answer), and an irrelevance check (after removing all supporting facts the remaining context must be insufficient, so no shortcut exists). Generation retries up to 5 times per seed until s ≥ 3.5. Difficulty is a heuristic — Difficulty = 10·N_f + L_c/500 + L_a/5 over supporting-fact count, context length and answer length — used only for splitting Simple from Complex. Agents converse for up to 10 rounds; the answer is parsed from `<A>…</A>` (last occurrence) or `\boxed{…}` (first occurrence), and scored by word-level F1 against the reference answer, scaled to [0,100]. The AI-use statement says generative AI assisted instance generation and validation for this task; Scheduling instances were generated programmatically and Game maps were hand-specified.

**Scheduling.** Five members each hold a private five-day calendar; they must agree a continuous 20-minute window. The timeline is discretized at m = 10 minutes over T = 5 × 24 × 60 / m units. Each calendar starts with fixed "Rest" blocks (sleep 00:00–07:00, lunch 12:00–14:00) that are strictly BUSY; the rest is filled stochastically with random activities of 10–60 minutes until each agent's busy ratio reaches ρ_i ∈ [0.3, 0.6]. All common feasible windows are then enumerated, and a **candidate-pruning** algorithm fixes difficulty: a protection set of K valid windows is sampled, non-protected windows are invalidated by inserting minimum-unit BUSY blocks, and the process repeats until exactly K valid windows remain. Simple instances have K ∈ {4,5}, Complex K ∈ {2,3} — more feasible windows means easier, since more candidates can be proposed. Scoring is strict exact match against the surviving solution set; partial overlaps count as failures. Communication follows a broadcast-style chat, so routing is not exercised.

**Game.** A cooperative Dec-POMDP-style grid world in which 4–8 agents explore, collect resources and deposit them into warehouses within 50 rounds. Each agent sees a local window centred on itself (4×4 on the 15×15 Simple map, 5×5 on the 18×18 Complex map); communication is point-to-point, so all three mechanisms matter. An agent may carry multiple units but only one resource type. Warehouses impose a total capacity C_i and per-type caps L_{i,k}; a deposit counts only if neither is violated, and the effective deposited amount for type k is c_k = Σ_i min(n_{i,k}, L_{i,k}), giving score S = Σ_k min(c_k, T_k) over quotas for wood, sand and stone. Resources left on cells or beyond the caps add nothing. Actions are one discrete call per round (movement, `PICK_UP [QTY] [TYPE]`, `PUT_DOWN [QTY]`); an explicit quantity that violates capacity *fails* rather than being silently repaired. The per-round loop delivers messages generated in round t−1, lets each agent observe and act, allows at most one point-to-point message per agent from the same pre-update observation, then resolves movement conflicts, executes pickups and deposits and updates the score. Each map is run five times; per-map means are averaged first, then aggregated across maps.

**Metrics.** Three, all deterministic and judge-free. *Performance score* is on [0,100]: F1 × 100 for Reasoning, success rate × 100 for Scheduling, and for Game the raw score normalized by a map-specific heuristic reference score U_m computed offline by a non-LLM planner (BFS shortest paths, greedy task-allocation heuristics under global and round-robin allocation, best plan taken as U_m), reported as min(100, 100·S_m/U_m). *Communication cost* (Tok) counts only tokens generated for inter-agent messages; local reasoning tokens are excluded. *Communication efficiency* (Eff) is the performance score per 1,000 tokens of communication cost.

**Mechanism configurations.** Reasoning: Base = free-form dialogue; Protocol = typed messages for information requests, evidence sharing and final answers. Scheduling: Base = unconstrained natural-language negotiation; Memory = structured availability and negotiation state (candidate and rejected slots) across rounds; Memory + Protocol = multi-phase interaction (coarse search → candidate proposal → voting). Game: Base = inter-agent communication disabled; Memory = stores discovered world state from local observations and received messages; Routing = point-to-point messaging with two recipient-selection modes, Random (sample a teammate) and Gate (first decide whether communication is needed, then select the recipient); Protocol = transmits grounded fields (agent state, observations, current plans).

## Evidence

All numbers below are **author-reported** from this preprint; none has been independently replicated. Scoring protocols differ per category, so figures are not comparable across rows of different tables.

**Setup.** Five backbones spanning capability–cost regimes: Llama-3.1-8B-Instruct, GPT-5-nano, Gemini-2.5-Flash-Lite, DeepSeek-v3.2 and Qwen-Plus. Llama-3.1-8B is included only in Reasoning because it has a high failure rate in Scheduling and Game. Game results are averaged over five runs per map and configuration. The framework-level evaluation uses a shared 30% subset sampled without replacement within difficulty strata with seed 42 — 90 Reasoning instances (60/30), 60 Scheduling (30/30) and 30 Game maps (15/15) — with identical instance manifests across systems.

**Reasoning (Overall column: score, message tokens, efficiency).**

| Backbone | Base score | Protocol score | Base Tok | Protocol Tok | Base Eff | Protocol Eff |
|---|---|---|---|---|---|---|
| Llama-3.1-8B | 26.06 | 33.45 | 1,261 | 530 | 20.67 | 63.09 |
| GPT-5-nano | 43.36 | 49.66 | 567 | 155 | 76.48 | 319.97 |
| Gemini-2.5-Flash-Lite | 50.92 | 55.53 | 589 | 324 | 86.39 | 171.21 |
| DeepSeek-v3.2 | 54.41 | 55.23 | 716 | 208 | 76.04 | 265.61 |
| Qwen-Plus | 55.81 | 59.24 | 382 | 161 | 145.91 | 367.71 |

The authors' summary of this table: Protocol raises score by +1.5% to +28.4% while cutting message tokens by 45.0% to 72.7%, a 2.0×–4.2× efficiency gain. The mechanism is legible in the transcripts: in a matched case, Base commits at turn 1 to an answer the private context does not support (word-level F1 = 0), while the Protocol run asks the partner for the missing evidence, receives it and answers correctly (F1 = 1).

**Scheduling (Overall: success rate %, message tokens, efficiency).**

| Backbone | Base | Memory | Memory + Protocol |
|---|---|---|---|
| GPT-5-nano | 1 | 2 | 42 |
| Gemini-2.5-Flash-Lite | 17 | 36.5 | 62.5 |
| DeepSeek-v3.2 | 22.5 | 38 | 63 |
| Qwen-Plus | 13.5 | 40 | 63.5 |

Token costs move the other way for the strongest protocols: Gemini's Memory + Protocol spends 933 tokens at 62.5% success, versus 999 tokens at 17% for Base, and GPT-5-nano spends 2,942 tokens at 42% versus 1,116 at 1%. Protocol buys agreement at a communication premium; memory alone is comparatively cheap and weak. The cross-round memory ablation (Appendix B.5, Overall score) separates state retention from availability preprocessing: Base → Cross-round Memory → full Memory gives GPT-5-nano 1 → 2 → 2, Gemini 17 → 27 → 36.5, DeepSeek 22.5 → 36.5 → 38, Qwen-Plus 13.5 → 39.5 → 40. Cross-round retention beats Base in all 12 backbone–split comparisons; full Memory adds further gains in 9 of 12, ties one, and is lower in two.

**Game (Overall: score, message tokens, efficiency).**

| Backbone / setting | GPT-5-nano | Gemini-2.5-Flash-Lite | DeepSeek-v3.2 | Qwen-Plus |
|---|---|---|---|---|
| Base | 42.61 | 23.85 | 18.59 | 38.73 |
| Memory | 50.65 | 25.75 | 50.12 | 53.39 |
| Memory + Random | 53.85 | 26.29 | 54.23 | 53.20 |
| Memory + Gate | 58.98 | 28.64 | 58.95 | 59.77 |
| Memory + Random + Protocol | 56.41 | 27.48 | 56.40 | 57.43 |
| Memory + Gate + Protocol | 60.71 | 30.41 | 60.07 | 62.05 |

The authors report that Gate beats Random by 2.35 to 6.57 score points while cutting message tokens by 28.0% to 35.6%, and that adding Protocol to a routing variant yields a 1.12×–1.91× efficiency gain — but that Memory + Random + Protocol still trails Memory + Gate in score, which the authors read as evidence that routing quality matters more than message schema. Token accounting is sensitive to what is counted: Appendix B.4 re-runs Game counting all completion tokens in the message phase, and under that accounting Memory + Gate costs *more* than Memory + Random for GPT-5-nano (10,016 vs 8,674) because of routing-decision overhead, while Gate + Protocol is cheaper for every backbone. A worked case shows the mechanism end to end: Agent_0 reports a warehouse at (3,15) that Agent_1 cannot see; Agent_1 verifies the sand capacity locally and deposits 4 units in round 19, and the team score moves from 8 to 12.

**Framework-level evaluation (30% subset, four backbones).** CAMEL and AgentVerse were run on the same instances under the same observation boundaries, against a controlled reference scaffold (Protocol for Reasoning, Memory + Protocol for Scheduling, Memory + Gate + Protocol for Game). Selected Overall cells: with Qwen-Plus, Game score is 26.11 for CAMEL, 29.61 for AgentVerse and 57.32 for the reference; Scheduling is 21.67, 23.33 and 58.33. With GPT-5-nano, Reasoning is 38.15 (CAMEL), 43.31 (AgentVerse) and 52.07 (reference). The authors' reading is that the frameworks are close on Reasoning but fall far behind as collaboration demands rise, and that they behave differently per task — AgentVerse communicates more compactly and is stronger in Scheduling, CAMEL is stronger in most Game settings.

**Error analysis (n = 40 sampled failure cases per task, diagnostic only).** Runs were ranked within each Simple/Complex subset per backbone and setting, the bottom 30% pooled, and 40 cases sampled per task. Reasoning: Incomplete Answer 40.0% (16/40), Incorrect Answer 27.5%, Format Violation 27.5%, Instruction Drift 5.0%. Scheduling: Exploration Failure 42.5%, Misjudgment 37.5%, Output Failure 10.0%, Memory Failure 10.0%. Game: Low Efficiency 47.5%, Low Exploration 27.5%, Navigation Failure 20.0%, Mixed 5.0%.

**Fairness statistic.** A normalized contribution entropy H_norm = −(1/log₂N)·Σ p_i log₂ p_i over deposited contributions (zero-contribution agents included, runs with no positive contribution excluded) is reported to measure participation balance; adding Protocol gives higher entropy and tighter distributions than memory or routing alone.

## Limitations

**Stated by the authors.** The Game reference score U_m is a heuristic, not a guaranteed global optimum or strict upper bound — it assumes no inter-agent collisions and only equals the theoretical maximum when the quota is met; the clipping operation did not affect the reported results because no run exceeded U_m. The Complex subset does not necessarily score lower, since it also has more agents and more resources. The error-analysis percentages describe the selected failures, not failure rates over the benchmark, and the qualitative cases illustrate interaction patterns rather than their frequency. For the framework comparison, differences may reflect preprocessing, conversation management, interaction control and message construction together, and the results do not isolate the causal effect of replacing only the framework library. The Tok metric measures communication volume rather than end-to-end inference cost, so it should not be read as API spend or wall-clock time.

**Assessed from the reporting.**

- **Single source, no independent replication.** Everything rests on one arXiv preprint. The evaluation code is linked from the paper, but no result here has been reproduced by a third party.
- **No error bars anywhere.** The Game runner is configured at temperature 0, top-p 1 and seed 42, and the paper states plainly that only averaged results were retained, so run-to-run standard deviations cannot be recovered; no confidence intervals or significance tests accompany any table. The five Game repetitions are averaged per map before aggregation, so the repeat structure is invisible in the reported numbers.
- **Small and unequal instance counts.** 300 Reasoning instances, 200 Scheduling instances and 100 Game maps (50 per difficulty level) are small for a benchmark; the framework-level evaluation drops to 90, 60 and 30 items, where a single instance moves a score by several points and a single agent's behaviour can dominate a mean.
- **Difficulty labels are heuristic, not calibrated.** Reasoning difficulty is a formula over supporting-fact count and lengths; Scheduling difficulty is the count of feasible windows; Game difficulty is essentially map size. The paper calls the source levels "recipe-complexity labels, not calibrated item difficulties" in the TandemBench sense — here the analogous point is that the strata are proxies.
- **The Game environment is small and closed.** 15×15 and 18×18 grids, three resource types, one warehouse in each published example, a 50-round horizon and a 4-unit carrying capacity. Nothing in the design probes realistic heterogeneity of tools, latency or failure modes.
- **The framework comparison is not a like-for-like architecture comparison.** The adapters replace parts of the reference implementation (for example, deterministic availability extraction instead of LLM-based extraction), the frameworks use their own history windows (CAMEL 32 message entries, AgentVerse the last 16 model outputs, "approximately eight action–message rounds", explicitly not equal token budgets), and the reference scaffold carries extra state and control machinery. Differences are therefore confounded by design, as the authors concede.
- **Baseline mechanics differ per category, so "Base" is not one thing.** In Reasoning, Base is free-form dialogue within a 10-round dialogue budget; in Scheduling, Base is unconstrained natural-language negotiation in a broadcast-style chat (the reference run in the qualitative case ends after five rounds, and the framework adapter in Appendix C.3 also ends after five rounds or when its stateless transcript checker reports completion); in Game, Base has communication *disabled entirely*. The Game comparison therefore mixes a communication-capable system against a non-communicating one, and the reported Game gains cannot be read as a controlled communication ablation without noticing this.
- **The Scheduling score is all-or-nothing.** A single feasible 20-minute window must be proposed and every one of five private calendars must accept it; partial overlap scores 0. The 80% of sampled Scheduling failures split between "never surfaced a feasible window" and "misjudged a candidate" suggests the metric is sensitive to a small number of negotiation pathologies that a majority-vote or partial-credit score would absorb.
- **A qualitative failure case shows a safety-relevant failure mode the scores do not capture.** An agent that trusts a teammate's stale capacity message over its own current per-type observation attempts a deposit that fails with no score change — an instance of the [[concepts/verified-completion-vs-apparent-success]] pattern inside the benchmark's own traces.

## Competing approaches

The paper positions itself against three families. **General-purpose multi-agent benchmarks** — GAIA and AgentBench for outcome-oriented task completion under loose interaction conditions, SOTOPIA for social interaction, plus collaborative suites such as MultiAgentBench, Collab-Overcooked and PARTNR. **Partially observable multi-agent benchmarks** — Zhou et al. (SOTOPIA), Yu et al. (MineLand), Zhu et al. (MultiAgentBench) and Ruan et al. (swarm intelligence); the authors say these focus on end-to-end task performance rather than mechanism-level analysis, so MASBench is complementary rather than a replacement. **Domain-specific MAS benchmarks** — VillagerAgent, LegalAgentBench, AI Hospital, TeamCraft, MindAgent — which the authors describe as prioritizing environment-specific adaptation of individual agents over the collaboration mechanism itself.

Within mechanism design, the paper cites **CAMEL** (ChatAgent with conversation memory), **AutoGen**, **MetaGPT**, **ChatDev** and **AgentVerse** as general orchestration frameworks, and **DyLAN** as a system that dynamically optimizes the interaction graph (the closest thing to MASBench's routing). It also cites **OPTIMA**, which optimizes inter-agent communication against task performance *and* token efficiency jointly, and the decision-optimization line of multi-agent debate, reflexion and voting. It cites **LLM-as-a-judge** evaluation (Zheng et al.; JudgeLM) and the position-bias study of Shi et al. as the practice it deliberately avoids, and it cites **HotpotQA** as the substrate for Reasoning.

Within this knowledge base, MASBench is the partial-observability counterpart to [[projects/tandembench]] (which grants complete global information and asks only for a plan choice) and to [[projects/st-bench]] and [[projects/agensh]]; the design lesson on making an evaluation deterministic and judge-free belongs with [[techniques/evaluation-and-simulation]] and [[concepts/evaluator-circularity]]. It is also the entry point from [[benchmarks/index]] and contributes evidence to [[evaluations/briefing-synthesis-2026-11-03-to-09]] and to [[concepts/preservation-aware-agent-improvement]], in the sense that improving a team's shared state must not be bought by degrading the checks that would catch a bad change.

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The most transferable idea is that **partial observability can be used as a variable rather than a difficulty setting**. MASBench does not merely hide information; it hides the specific information a chosen mechanism must supply. Reasoning hides the evidence chain that protocolized request-and-answer messages must carry; Scheduling hides the availability intervals that cross-round state must retain; Game hides the warehouse locations and capacities that routing and protocol must move. That is why the three categories are worth more than their three task types: each one is a separate test of whether a mechanism works when it is load-bearing, which is a much better experimental design than adding agents to a shared task and watching the aggregate.

The second lesson is about **how to measure communication honestly**. Splitting "cost" into transmitted tokens, message-phase generation tokens and end-to-end inference cost, and publishing both the first and the second, exposes a real engineering tension: Gate routing spends fewer transmitted tokens than Random but more generation tokens per instance, so a routing policy can look cheap or expensive depending on what you count. Any team building agent teams should decide which of those it is optimizing before it starts comparing systems.

Third, **mechanism ablations of this shape are the right template for internal agent evaluation**. The cross-round memory ablation is the model to copy: introduce a minimal variant (retain state across rounds, change nothing else) and a full variant (retain state *and* preprocess), and report both. It converts an unexplained improvement into two attributable ones, and it did so here without adding any new task.

Fourth, and most cautionary: **the Base condition is doing a lot of hidden work**. In Game, Base cannot talk at all; in Reasoning and Scheduling it can. The reported per-category gains therefore do not compose into a single statement about "collaboration mechanisms help". Internal evaluations should state, per condition, what the system is allowed to do — not just what component it has.

Finally, the error analysis is a reminder to instrument the *kind* of failure, not just the rate: "Exploration Failure" and "Misjudgment" in Scheduling point at different fixes (broader candidate generation versus better feasibility checking), and only a per-category taxonomy tells you which one to build. That is a concrete instance of [[concepts/comparator-construction-shapes-margins]] and [[concepts/ground-truth-fallibility]] — the difficulty strata are proxies, so a small regression on one stratum may be a composition artifact rather than a capability change.

## Reproducible experiment

The paper links its code, so a replication is possible; the model substitutions below are unavoidable for anyone without the 2026 hosted backbones. A feasible independent check:

1. **Replicate the cheapest decisive comparison.** Take the Reasoning category only (300 instances, two agents, HotpotQA-derived) and run Base versus Protocol on two available backbones, fixed at temperature 0, with the four cyclic option-format mechanics irrelevant here since Reasoning has no options. Measure score (word-level F1 × 100) and message tokens separately. The paper's prediction is that Protocol improves score modestly (+1.5% to +28.4% relative) while cutting tokens by 45.0%–72.7% and multiplying efficiency by 2.0×–4.2×. A directionally matching token reduction with a much smaller score gain would be informative; no token reduction at all would falsify the paper's central mechanism claim on the cheapest category.
2. **Test the Base-condition confound directly.** Re-run the Game category with a third condition: Base plus *unstructured* point-to-point communication (communication allowed, no memory, no protocol, random recipient). If the Game gains are really about information exchange, this condition should land well above Base (which cannot communicate) and below Memory + Gate + Protocol. If it lands at Base level, the mechanism story is wrong and the gain is coming from elsewhere. Run at least 5 seeds per map, keep the per-map values, and report run-to-run variance — the paper could not, because it retained only averages.
3. **Measure the accuracy/efficiency trade-off in Scheduling with a partial-credit metric.** Score the Scheduling task three ways: the paper's strict exact match, a partial-overlap credit, and the fraction of members who accept the proposed window. The paper's own error analysis attributes 42.5% of sampled Scheduling failures to Exploration Failure and 37.5% to Misjudgment; if partial credit lifts the Base score far more than the Memory + Protocol score, the strict metric is overstating the mechanism's contribution and the reported 1% → 62.5% jump should be read as a threshold effect rather than a capability gap.
4. **Reproduce one qualitative case end to end.** Reconstruct the Game case where a teammate's warehouse location enables a deposit that raises the team score, and the companion failure where a stale capacity message causes a rejected deposit. Instrument per-agent observed state, transmitted messages and action success. A pass means the mechanism-level story (share the location → verify locally → deposit) reproduces; a failure means information transfer alone does not produce the outcome, and the benchmark's Game score is measuring something else.

Report the substituted models, the exact harness settings and any partition differences alongside the results; a difference in score between a local run and the paper is not evidence about the paper unless the protocol matches.

## Evidence status

This page is grounded in a full read of the primary source on 2026-11-10: the arXiv abstract page (https://arxiv.org/abs/2610.04672), the complete HTML full text of v1 including appendices A–E (https://arxiv.org/html/2610.04672v1), and the v2 HTML (https://arxiv.org/html/2610.04672v2) for comparison of the main tables, whose numbers match v1. Every quantitative result is **author-reported**; no result here was reproduced, executed or cloned by the KB maintainers, and no independent replication is known. Claim types are separated in the text: the design rationale and the mechanism-effect readings are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. The paper is a preprint with no peer-reviewed venue claimed; the abstract page records a v2 revision dated 4 November 2026, and this page's numbers are those printed in v1 and v2.

## Historical coverage

- [[briefings/2026/11/2026-11-08]] — the dated briefing that introduced MASBench as an October gap-fill.
