---
uid: b6a90601-a8d1-4d13-9a40-000000000031
title: "Late Autumn"
summary: "LLM coding agents specialize a general lifelong multi-robot planner to one modeled warehouse, raising throughput 22-60% with reviewable scored commits."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://arxiv.org/abs/2611.02391
  - https://arxiv.org/html/2611.02391v1
---

# Late Autumn

## What it is

Late Autumn is a case study in using LLM coding agents to specialize a general multi-robot planner for a single warehouse site. It is reported in the arXiv preprint "Late Autumn: LLM Agents Specialize a General Multi-Robot Planner for One Warehouse" (arXiv:2611.02391, submitted 2 November 2026, cs.RO and cs.AI). The paper lists six authors: Yimin Tang and Erdem Bıyık (Thomas Lord Department of Computer Science, University of Southern California), Han Zhang, Shao-Hung Chan and Jingkai Chen (Symbotic), and Sven Koenig (Department of Computer Science, University of California Irvine). The arXiv abstract page records no venue, comment or journal reference, so this is a preprint with no peer-reviewed venue claimed in the inspected text. An ancillary file, frontier_steps.csv, ships with the arXiv version.

The framing is an analogy with post-training: a pretrained model is adapted to one task by trading generality for fit, and the paper asks whether a general algorithm can be specialized the same way. The argument for trying is that warehouses differ in aisle geometry, fleet size, carry capacity, demand mix and service times, but each site runs the same layout every day, while operators keep one general planner across sites because experts cannot tune it for each one. The argument against naively applying coding agents is that a warehouse planner differs from the short programs and cheap deterministic scores that dominate the agent-for-algorithm-engineering literature in three ways: the agent edits a complete planner rather than one heuristic function; the score is a stochastic simulation in which many changes are smaller than the noise; and a change reaches physical robots only after an engineer understands and trusts it.

The paper asks four research questions: does throughput really improve (RQ1); what methods do the agents propose (RQ2); are those methods site-specific or general (RQ3); and how large is each improving change, and can an expert review it from first principles (RQ4).

## Mechanism

**Problem.** A 4-connected grid graph G = (V, E); N agents each carrying at most K tasks; tasks released online, each with a pickup vertex and a goal set. A plan is valid if no two agents occupy a vertex, no two swap vertices along an edge, and pickup and delivery dwell durations are respected. The objective is throughput — tasks completed within horizon H, divided by H — and each planner call has a 1 s wall-clock limit.

**Site and workload.** The floor models one existing automated warehouse: a 35 × 39 grid with 691 free cells, 19 one-wide storage aisles of 20 cells and 8 one-wide station lanes, with a wall splitting it into two halves joined by a single cell. An outbound task (probability 0.5) starts at a storage cell and may be delivered to any of 3 cells of one station lane; an inbound task starts at a station cell and may be delivered to any of 3 storage cells. New tasks are released so that 2N tasks stay unfinished, keeping the system saturated. Parameters: N = 100 robots, K = 2, H = 400, d_p = d_d = 4.

**Baseline planner.** The planner is a lifelong version of ITA-LaCAM. It replans after every pickup or delivery, or when the plan runs out. A Hungarian matching assigns each agent one goal option (a pickup, a goal cell of a carried case, or a costly wait), costed by distance plus service time with at most one agent per pickup or drop cell; the matching is repaired incrementally at each search node. LaCAM with FOCAL node selection then generates configurations with PIBT until some agent completes a service. The planner has 9.0k lines of C++ and needs 4.8 ms per call at the tuned site; its anytime refinement exits after the first solution, so over 99 % of the budget is unused. It reaches a hidden-seed throughput of 1.23.

**The agent loop.** The setup uses CORAL to run one autonomous coding agent per campaign in its own git worktree. The agent can read and edit all code, build, test, inspect traces and request evaluations. A natural-language task contract, given to the agents in Chinese and translated in Appendix C, fixes the rules: the agent may generally change planner, assignment or goal-candidate behaviour; it may not change the fixed official target, hard-code seed, task or map shortcuts, fabricate CSV, trace or schedule outputs, or optimise only the output format; a mean change smaller than 0.03 on public seeds is not a signal and trace-derived behaviour signals are preferred; and once a behaviour-changing candidate is finalised, builds and produces valid output, it must be committed and officially evaluated whether the self-test shows improvement, no change or regression. The contract also treats iteration time as a resource — a clearly higher runtime cost should be accepted only when the throughput evidence is strong (about 0.1 or more).

**Commit-and-evaluate lifecycle and isolated evaluation.** Every candidate that changes behaviour, builds and yields valid output must be committed and officially evaluated before the agent keeps, reverts or abandons it, which prevents silent cherry-picking and gives the complete record. CORAL adds periodic prompts to reflect (every 2 evaluations), consolidate (every 8) and pivot (on plateaus); a campaign stops after 100 official evaluations. Throughput depends on how much search fits into 1 s, so builds and benchmarks run on a separate host with pinned 10-core slots. A self-test runs public seeds 0–9 and returns per-seed traces; an official evaluation runs 10 hidden seeds and returns only aggregates. The same binary is reproducible on one slot, but contention can move the 10-seed mean by about 0.025, and six evaluations of the unmodified baseline spanned 1.198–1.249; the contract therefore treats mean changes below 0.03 as noise.

**Safety property.** The simulator validates every executed joint move for vertex and edge conflicts. As long as a patch leaves this validator unchanged — which review confirmed for all 102 new-best steps — a patch can lower throughput but cannot produce a collision in an executed plan.

**Knowledge settings.** In the paper-grounded setting every idea must cite one of 137 briefs of MAPF-related papers and competition reports; in the open setting any source is allowed and must be named; open+web additionally enables web search.

**Re-evaluation and transfer.** Because a campaign's best hidden score is a maximum over noisy evaluations, the baseline and each best commit were rebuilt and run on 20 fresh seeds for the tuned site and for seven held-out configurations, each changing one factor: an alternative layout (37 × 39 cells, 835 free cells, an open top corridor, no dividing wall, 13 station lanes), 60 or 150 robots, K = 1, an 80/20 outbound/inbound mix, and service durations of 2 or 8 — 1,120 episodes in total (7 builds, 8 configurations, 20 seeds). Gain is the paired throughput difference to the baseline on the same seeds, with a 95 % CI over seeds. A new-best step is an official evaluation that raises a campaign's best hidden score; its size counts changed lines of algorithm code only, excluding tests, tools and build files. Builds use GCC 10.5 -O3; re-evaluation used a 32-core AMD EPYC 9R14 host with 64 GB RAM.

## Evidence

All numbers in this section are **author-reported** from this single preprint; none has been independently replicated.

**The six campaigns (Table 1).** All campaigns started from the same commit at high reasoning effort. Hidden-best gain is relative to the baseline mean of 1.230; fresh-seed gain is the best commit re-evaluated on 20 unseen seeds; planner seconds are per 400-step episode.

| Model | Harness | Ideas | Evals | Hours | Hidden best TP | Gain | Fresh-seed TP | Fresh gain | Evals to 90 % gain | Planner s/episode |
|---|---|---|---|---|---|---|---|---|---|---|
| Unmodified baseline (6 evals) | – | – | – | – | 1.230 | – | 1.209 | – | – | 1.8–3.8 |
| Opus 5.5 | Claude Code | paper | 100 | 7 | 1.973 | +60 % | 1.968 | +63 % | 24 | 21.2 |
| Opus 5.5 | Claude Code | open | 100 | 12 | 1.875 | +52 % | 1.869 | +55 % | 73 | 189.9 |
| Fable 5.1 | Kiro | paper | 100 | 8 | 1.884 | +53 % | 1.861 | +54 % | 67 | 11.3 |
| Fable 5.1 | Kiro | open+web | 100 | 9 | 1.758 | +43 % | 1.746 | +44 % | 27 | 94.1 |
| GPT-6 Luna | Codex | paper | 100 | 22 | 1.500 | +22 % | 1.476 | +22 % | 83 | 2.9 |
| GPT-6.1 Sol | Codex | paper | 100 | 34 | 1.498 | +22 % | 1.497 | +24 % | 49 | 342.1 |

The best campaign reached 1.973 tasks per timestep, 60 % above the baseline mean. The four Claude-family campaigns gained 43–60 %; both GPT campaigns plateaued near 1.50 (+22 %). The table footnote records that web search was enabled but never used in the open+web campaign.

**Fresh seeds.** On 20 seeds no agent had seen, every best patch scores within 0.001–0.024 of its hidden best, and every best patch beats the baseline on all 20 seeds — for example the Opus/paper patch reaches 1.968 (+63 %). The paper's headline range is therefore 22–60 % on hidden seeds and up to 63 % on fresh seeds.

**Gains come early, and partly from compute.** The Claude-family campaigns reached 65–86 % of their final gain within 20 evaluations (0.6–1.9 hours). Only 27 of the 102 new-best steps exceed the 0.03 noise floor; the other 75 fall below it (27 of the 102 steps across the six campaigns change only constants). Relative to their baseline evaluation, the paper-grounded Claude patches use 4–10× more planner time and the open-setting patches 53–91× (mean calls of 0.3–0.6 s against the 1 s limit). GPT-6.1 Sol's last new best, worth +0.008, raised its planner time 87-fold (112× its baseline).

**Mechanisms (Table 2, gain contributed by the new-best steps that introduced or tuned each mechanism).**

| Mechanism (pipeline stage) | Opus/paper | Opus/open | Fable/paper | Fable/open+web | GPT-6 Luna | GPT-6.1 Sol |
|---|---|---|---|---|---|---|
| Corridor-exit priority (PIBT) | .10 | .14 | .09 | – | .03* | – |
| Corridor-blocking cost (assignment) | .12 | .28 | .20 | × | – | – |
| Local guidance (PIBT order) | .35 | .04 | – | – | × | × |
| Flow-aware distances / routes | – | .00 | .13 | – | .03 | .17 |
| Time-aware assignment | .13 | – | – | – | × | – |
| Rollouts / Monte-Carlo PIBT | .00 | .12 | .16 | .51 | .02 | – |
| K=2 insertion / pairing | .03 | – | .03 | – | .11 | .04 |
| Search-level changes | .05 | – | – | – | .02 | .01 |

× means tried but never a new best; * is around articulation cells only.

**Independent campaigns found the same bottleneck.** On this floor 470 of the 691 free cells lie in one-wide corridors, and a servicing robot blocks everyone behind it. Three Claude campaigns found this — from traces ("corridor entrances are occupied 89 % of the time") or from a cited paper — and converged on two rules. A *corridor-exit priority* gives a PIBT priority boost to a robot inside a corridor whose goal lies outside it, so priority inheritance pushes entering robots back instead of pushing the leaving robot deeper (+0.09 to +0.14; cf. PIBTTP). A *corridor-blocking cost* makes pickup and drop cells behind occupied corridor cells more expensive in the matching (+0.12 to +0.28; cf. idle-time-aware assignment). All three campaigns detected corridors generically, as connected components of degree-2 vertices. These rules provide 28–67 % of those campaigns' gains.

**Agents spent the idle budget.** Agents ported local guidance (+0.35 in Opus/paper), added flow-dependent edge weights (+0.13 in Fable/paper), and built rollout planners; Fable/open+web replaced LaCAM's search with the best of many noisy PIBT rollouts (+0.38 in one step).

**Sources and failures.** Paper-grounded campaigns cited a brief in 97–99 % of evaluations but used only 18–44 of the 137 briefs; 79 % of Opus/open candidates came from its own diagnosis. The paper gives two reasons for the GPT plateaus: they turned to the library instead of the traces and never built corridor rules for the aisles, and they followed CORAL's "hardest idea, three evaluations" prompt literally, with median attempts of 66 and 290 added lines (Claude: 4–16). The same local-guidance paper gave Opus +0.24 but GPT 0.98–1.30, because GPT used a 5-step window and no warm start.

**Code-level generality (Appendix D).** Every frontier step was graded G0 (generic features only), G1 (generic code, layout-tuned constants) or G2 (scenario facts). Of 77 Claude-family steps, 12 are G0, 59 G1 and 6 G2; none hard-codes seeds, coordinates or the map.

| Campaign | Steps | > 0.03 | Retunes | G0/G1/G2 | Patch (added/deleted lines) |
|---|---|---|---|---|---|
| Opus / paper | 24 | 6 | 7 | 5/15/4 | +1454 / −10 |
| Opus / open | 20 | 8 | 10 | 3/17/0 | +635 / −22 |
| Fable / paper | 21 | 5 | 4 | 3/16/2 | +824 / −20 |
| Fable / open+web | 12 | 2 | 6 | 1/11/0 | +558 / −101 |
| GPT-6 Luna / paper | 14 | 4 | 0 | 12/2/0 | +1264 / −28 |
| GPT-6.1 Sol / paper | 11 | 2 | 0 | 11/0/0 | +2372 / −57 |

**Transfer.** Applied unchanged to the seven held-out configurations, the patches gain significantly in 40 of 42 cells, with all 95 % CIs excluding zero. On the alternative layout the patches keep 57–91 % of their absolute gain, because its aisles are still one-wide. There is a clear trend with congestion: with 60 robots only 25–43 % of the absolute gain remains, whereas with 150 robots 64–110 % remains, because the discovered mechanisms target blocking in one-wide corridors, which grows with fleet size. Relative gains also stay close to the tuned ones for single-carry robots and for service durations of 2 and 8. The exception is the 80/20 outbound-heavy mix, which sends most deliveries to the 8 station lanes: the Claude patches keep only +3 to +10 %, and both GPT patches lose 6 %.

**Step and patch sizes.** The median improving step changes 27 lines, 27 of the 102 steps only retune a constant, and the largest gains came from 36–383-line mechanisms. The final patches (0.7k–1.5k lines for Claude, 1.3k–2.4k for GPT) are modest next to the 9k-line planner, and each is a chain of 13–49 officially scored commits that an expert can review one at a time. The chain also exposes dead code — 26 % of the lines added by Opus/paper.

**Review findings.** Of the 24 frontier steps of Opus/paper, 7 are constant retunes, 10 are local cost or priority rules an expert can verify from first principles, and 7 need careful review. Review found problems the score cannot reveal: (i) the Opus/open rollout stops at 880 ms and then starts the main solve with a fresh 1 s deadline, so the per-call limit holds only empirically; (ii) a Monte-Carlo step redraws PIBT's random tie-breaks, so the executed configuration can differ from the scored one; and (iii) dwell-sized constants and K = 2 formulas are hard-coded. Appendix E gives a worked example: the second evaluation of the Opus/open campaign (commit 3400f25f) added 45 lines and removed 2, raising the hidden score from 1.238 to 1.380, and the paper argues a reviewer can check its two claims — that corridors are connected components of vertices with degree at most 2, and that only unsatisfied agents whose goal lies outside their corridor are boosted — directly from the code.

## Limitations

**Stated by the authors.** This is a case study of one planner and one family of sites; all results come from simulation, and no agent-generated patch has been deployed on physical robots. One campaign was run per (model, harness, knowledge setting) combination, so differences between campaigns combine the effects of model, agent harness (Claude Code, Kiro, Codex), knowledge setting and run-to-run variance — the comparison is indicative, not causal. Each campaign's best hidden score is selected from up to 100 noisy evaluations and is therefore optimistic; the paper reports fresh-seed re-evaluations to correct for this. The reviewability analysis rests on diff statistics and on an LLM-assisted code reading whose key findings the authors checked against the source. The agents optimised throughput only; they could trade other operational metrics such as task latency, energy use or robot wear, which were not measured.

**Assessed from the reporting.**

- **Single source, one planner, one floor.** Everything rests on one arXiv preprint (v1, 2 November 2026) with no peer-reviewed venue claimed and no public artifact URL in the inspected text. The planner (ITA-LaCAM, Tang et al. 2026) is the authors' own line of work — the same Yimin Tang appears as first author of both — so "a general planner" here means one the authors also wrote.
- **The compute cost is the other half of the result and is not in the headline.** The best gains cost 4–10× more planner time (paper-grounded) and 53–91× (open setting); the GPT-6.1 Sol campaign used 342.1 planner seconds per 400-step episode against the baseline's 1.8–3.8, a roughly hundred-fold increase for a +22 % throughput gain. Since a real planner runs under a 1 s deadline in production, most of these patches are not deployable as scored.
- **The 1 s limit is respected only empirically, and only sometimes.** The paper's own review found a rollout that stops at 880 ms and then starts the main solve with a fresh deadline, and a Monte-Carlo step whose redrawn PIBT tie-breaks mean the executed configuration can differ from the scored one. A throughput score obtained under a wall-clock budget that the patch can reset is not comparable to the baseline's, and the paper does not report how the affected campaigns' scores behave under a strictly enforced budget.
- **The 42-cell transfer result is dominated by one family.** 40 of 42 cells gain significantly, but six of the seven held-out configurations keep the same one-wide corridor geometry that the discovered mechanisms target; only fleet size and the demand mix vary the structure. The one structural change, the alternative layout, still has one-wide aisles, so the "generalisation" measured is largely to the mechanism the agents found rather than to a different bottleneck.
- **Failure modes are under-reported.** The paper documents that the GPT campaigns plateaued and why, but the frontier contains 102 new-best steps and 27 of them clear the noise floor; no table reports how many candidate steps were rejected, how many times an agent produced a non-building candidate, or how many official evaluations ended in a crash or an abandoned commit. The commit-and-evaluate rule is described as preventing cherry-picking, but the size of the rejected population is not disclosed.
- **Review is human-adjacent but partly LLM-assisted.** The paper is explicit that the reviewability analysis used "an LLM-assisted code reading whose key findings we checked against the source" — that is, a language model read the diffs. The three specific review findings reported are real and specific, but they are the findings the authors' reading surfaced; the paper gives no measure of how many reviewer findings were missed.
- **Safety rests on an unchanged simulator.** The collision validator is the last line of defence, and the paper's claim that no patch can produce a collision is conditional on the patch leaving that validator unchanged — a property confirmed by review for all 102 new-best steps, which is a review, not a proof. Nothing was run on hardware.
- **Only throughput.** The paper says so explicitly, and it matters for deployment: a patch that raises throughput by shortening idle travel while raising tail latency, or by preferring cheap robots and wearing them out faster, is indistinguishable from a good patch under this metric.

## Competing approaches

**The MAPF field the paper positions against.** The baseline planner draws on PIBT (priority inheritance with backtracking) and LaCAM with FOCAL node selection, chosen over optimal CBS because large fleets need fast suboptimal planners; TAPF couples target assignment with path finding (ITA-CBS, ITA-ECBS), and lifelong variants model continuous task arrival in warehouses. Guidance-graph optimization (Zhang et al. 2024; Zang et al. 2024) and imitation learning (Jiang et al. 2024) raise throughput; learned planners and fleet foundation models such as RAILGUN serve many maps. The paper's claim is that these are designed by researchers for a class of instances and that it studies the remaining site-specific engineering.

**The two mechanisms the agents rediscovered.** Corridor-exit priority is compared to PIBTTP (Fujitani et al. 2022), a deadlock-free method for multi-agent pickup and delivery using priority inheritance with temporary priority; corridor-blocking cost in the assignment is compared to idle-time-aware assignment for sortation centres (Kou et al. 2019). Local guidance is ported from Arita and Okumura's 2025 and 2026 work on local guidance for configuration-based and lifelong MAPF; flow-dependent edge weights from the guidance-graph optimization line.

**The agentic algorithm-engineering line.** The paper contrasts itself with LLM-driven program search and agentic research loops (AlphaEvolve, AIDE, ShinkaEvolve, the AI Scientist, ReEvo, Evolution of heuristics) and with benchmarks for those systems (MLE-bench, MLAgentBench, SWE-bench, AlgoTune, ALE-Bench), noting that there programs are small and scores are cheap. It cites Chen et al. 2024, "Why solving multi-agent path finding with large language model has not succeeded yet", and distinguishes its own approach: the LLM writes planner code, so the planner remains a verifiable search algorithm, rather than planning MAPF paths directly. The agent harness is CORAL (Qu et al. 2026).

**Within this knowledge base.** Late Autumn is a research-side deployment of the same pattern as [[projects/auto-research]] — an agent pipeline that writes its own tools and reports only provenance-checked numbers — but against a simulated operational planner rather than scientific data; the auto_research page's finding that a declared failure is a legitimate outcome is the mirror image of Late Autumn's rule that every behaviour-changing candidate must be committed and officially evaluated. The choice of hidden seeds and a noise floor as an explicit contract is an instance of [[concepts/protocol-relative-scores]], and the reviewability analysis is a concrete instance of [[concepts/scoped-assurance]] applied to generated code rather than to a permission boundary.

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The most transferable idea is not that agents found corridor rules — a domain-expert could have found those too — but the *contract* that made the search honest: hidden seeds, a stated noise floor, mandatory commit-and-evaluate, and the refusal to accept a patch whose change is below the floor. That combination converts "the agent said it improved" into a number that a third party can recompute. It is the same move as auto_research's provenance rule, at the level of a scalar score rather than a scientific quantity, and it is why the paper can report a +22 % result that is only +22 %.

Second, the compute column is the real report. A patch that multiplies planner time by 100× for a 20 % throughput gain is, in a deployed system with a hard deadline, not an improvement but a different algorithm with different properties — and one the paper's own review shows may not even respect the deadline it was scored under. Any team adopting this pattern should treat the resource multiplier as a first-class acceptance criterion rather than a footnote, and should compare against a re-scored baseline under a strictly enforced budget, because the paper's own Table 1 shows the baselines themselves cost 1.8–3.8 planner seconds per episode while one campaign costs 342.

Third, the diagnosis of the GPT campaigns is more useful than the wins. The paper shows two mechanisms by which a coding agent fails to benefit from good literature: it reads the library instead of the traces, and it follows the harness's "try the hardest idea" prompt literally, producing 66- and 290-line diffs where the successful campaigns produced 4–16-line ones. This is a caution for anyone delegating algorithm work: an agent's willingness to consult the trace of the actual system is a stronger predictor of success than its willingness to read papers, and harness prompt wording can dominate the outcome.

Fourth, the reviewability result deserves more attention than it gets. A median improving step of 27 lines and a chain of 13–49 scored commits means the deliverable is a reviewable history rather than a patch — the expert reads decisions, not a diff. The paper's three review findings (a reset deadline, a Monte-Carlo step that decouples executed from scored behaviour, hard-coded dwell constants) are exactly the classes of defect a throughput metric cannot see, and they are visible precisely because each commit is small and independently scored. Compare the risk in [[concepts/verified-completion-vs-apparent-success]]: the score was a valid metric and the system still behaved differently in production.

Finally, the demand-mix result is the one that most constrains deployment. A campaign tuned for a balanced inbound/outbound mix retained only +3 to +10 % under an outbound-heavy mix, and the GPT patches regressed. Site specialization is therefore not a one-off per-site cost but a recurring cost whenever the demand mix drifts, which changes the business case: the paper's closing expectation — that experts shift toward designing insightful metrics and fast simulators that mirror the real problem — implies that the simulator, not the agent, becomes the principal artefact of the site.

## Reproducible experiment

No artifact URL for the planner repository, the campaigns or the traces is given in the inspected text, so a check means reimplementing the loop against a public lifelong MAPF planner (ITA-LaCAM or a LaCAM/PIBT combination). The protocol below is ordered so that the cheapest decisive test comes first.

1. **The noise-floor and hidden-seed protocol, on any planner.** Build the simulator, fix the site, run the unmodified baseline six times and report the spread of the 10-seed mean; then run 20 candidate patches that change only constants, to see how many "improvements" a search would harvest from noise alone. Pass criterion: the paper's numbers are the reference — six baseline evaluations spanning 1.198–1.249, contention moving the 10-seed mean by about 0.025, and a 0.03 floor below which changes are treated as noise. If your baseline spread is much wider, the paper's floor is not transferable and every gain claim must be re-derived.
2. **Hidden-seed generalisation of the mechanism.** Implement only the two rules the paper reports as rediscovered independently — a corridor-exit priority in the PIBT priority assignment for agents inside a one-wide corridor whose goal lies outside it, and a corridor-blocking cost in the Hungarian assignment for pickup and drop cells behind occupied corridor cells — and measure throughput on 20 seeds the search never saw. Pass criterion: a gain of roughly +0.09 to +0.28 in absolute throughput on the tuned site, and a *decrease* of the retained gain with a smaller fleet (paper: 25–43 % remaining at 60 robots) and an increase with a larger one (64–110 % at 150 robots). This tests the mechanism and the transfer claim without running a single agent.
3. **The compute-multiple experiment.** Score the same patch set under (a) the paper's wall-clock budget and (b) a strictly enforced per-call deadline that a patch cannot reset, and compare the two rankings. Pass criterion: if the ranking changes, the paper's headline numbers are budget artefacts for those patches, exactly as its own review finding (i) suggests; if it does not, the "100× compute" patches are merely expensive rather than unsound. Either outcome is informative and this is the experiment that most directly tests the paper's least-discussed claim.
4. **Reviewable-chain test.** Ask a coding agent to improve the same planner under the paper's contract, then review the commit chain rather than the final diff, and record how many review findings are of the three reported classes (reset deadline, executed-versus-scored divergence, hard-coded constants). Pass criterion: a majority of improving steps under ~30 changed lines, and at least one reviewer-caught defect that the score cannot show. A result with 1000-line steps and no reviewer-caught defects would indicate the reviewability claim does not hold for a different harness.
5. **Demand-mix drift.** Re-run the best patch under an outbound-heavy mix (the paper's 80/20). Pass criterion: a retained gain in the +3 to +10 % range rather than the tuned +43 to +60 %; a patch that keeps its gain under a changed demand mix would contradict the paper's own claim that a new demand mix calls for a new campaign.

Model and harness substitutions are unavoidable (the paper used Opus 5.5, Fable 5.1, GPT-6 Luna and GPT-6.1 Sol across Claude Code, Kiro and Codex), and the substitution, the host hardware and the exact simulator parameters should be reported alongside the results, since the paper's own comparison between campaigns explicitly cannot separate model from harness from run-to-run variance.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2611.02391) and the complete HTML full text including appendices A–F, all three tables and the reference list (https://arxiv.org/html/2611.02391v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; there is no peer-reviewed venue claimed in the inspected text; no code, planner repository or trace archive URL is given in the inspected text, and the only ancillary file is frontier_steps.csv with the per-step table. All results are from simulation on a modelled floor; the paper states that no agent-generated patch has been deployed on physical robots, and no such deployment is claimed here. Claim types are separated in the text: the "no algorithm is best on all problems" framing, the transfer conclusion and the recommendation to shift experts toward metrics and simulators are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-06]] — dated full-fidelity research and cross-project synthesis (this page supersedes that snapshot's assessment).
