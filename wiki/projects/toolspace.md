---
uid: dd2c44b0-b381-4922-96a1-45231a4634eb
title: "ToolSpace — Execution-grounded tool environments"
summary: "Pipeline that mines data, state and retry dependencies from real MCP execution traces to synthesize replayable cross-environment agent tasks"
type: project
created: 2026-11-10
updated: 2026-11-10
depth: deep
related: [evaluator-circularity, protocol-relative-scores, preservation-aware-agent-improvement]
sources:
  - https://arxiv.org/abs/2611.05036
  - https://arxiv.org/html/2611.05036v1
---

# ToolSpace — Execution-grounded tool environments

## What it is

ToolSpace is a framework for synthesising long-horizon agent training environments and tasks from real tool-execution traces, reported in the arXiv preprint "ToolSpace: Scaling Tool-Centric Environment Synthesis for Long-Horizon Agents" (arXiv:2611.05036, submitted 3 November 2026, cs.CL; the arXiv comment field reads "Working in progress", and no peer-reviewed venue is claimed). The paper lists 25 authors led by Guanting Dong, with Zhicheng Dou and Tao Gui as corresponding authors, at Renmin University of China, Fudan University and Shanghai Jiao Tong University.

Its target is the family of MCP environment-scaling methods the paper calls *data-centric environment synthesis*: synthesize a database and a theme first, then derive tools and tasks from them. The authors identify three consequences of that ordering — tool interfaces that diverge from real ones because tools are reverse-synthesized from the fabricated database; tool-composition links that are built by random linking or shallow LLM judgment rather than by observed execution; and tasks confined to a single environment, because tools are locked inside their own sandboxes and no cross-environment reachability relation exists. ToolSpace reverses the dependency: the tool graph comes first, environments are derived from it, and databases are synthesized only where state actually has to change.

The paper's stated outputs are a typed tool-composition graph mined by deterministic rules from adjacent calls in real execution traces, environment clusters derived from that graph, a cross-environment task sampler that keeps only replay-verified chains, and two harder benchmark splits — AutomationBench Pro (300 tasks) and τ³-Bench Banking Pro (98 tasks) — on which seven frontier models drop by up to 38.2 points. The paper lists a project page (https://toolspace-agent.github.io/), a GitHub repository (https://github.com/dongguanting/ToolSpace) and a Hugging Face model collection (https://huggingface.co/collections/dongguanting/toolspace); these URLs are given in the paper's header and were not fetched for this page.

## Mechanism

ToolSpace has two stages: Tool Space Exploration, which reconstructs an explorable tool space from traces, and Cross-Environment Task Synthesis, which samples executable long-horizon chains over that space and decompiles them into auditable tasks. The stated design principle is *Trace-to-ENV*: do not mine a new environment ecosystem from scratch, but reconstruct a scalable tool space from execution traces first and synthesise tasks across the tool and environment clusters it connects.

**Trajectory collection.** The corpus is built from two source families and split by execution provenance into three levels. *MCP-ecosystem trajectories* come from a real tool catalog in an MCP registry, keeping only tasks whose tool definitions exactly match the real servers, then executing them with diverse agents against real MCP services and recording the complete call chains. *High* web-sourced trajectories are real-server interactions: Toucan-1.5M, covering 495 MCP servers, 2,000+ tools and 1.5M trajectories with synthetic instructions but real executions, and ToolBench/ToolLLM, covering 16,464 RapidAPI interfaces and roughly 469K API calls, with unavailable interfaces removed. *Medium* trajectories are real-workspace interactions collected from SWE-agent and OpenHands running in real containers and repositories, keeping only explicit tool calls and excluding shell wrappers such as `execute_bash`. *Low* trajectories are generated in synthetic environments, retained only where the tool name and schema format match a corresponding real tool. The paper states that over 200,000 agent–tool interaction trajectories were collected as raw material, with decontamination at both task and trajectory level against evaluation test sets.

**Graph modelling.** Every tool call becomes a node v = (n_f, α_f, β_f, x̃): tool name, input schema, output schema and a *normalised argument configuration*. Calls to the same canonical tool with different argument configurations are therefore distinct nodes, because they may carry different outputs and downstream dependencies. For adjacent calls in a trajectory the pipeline extracts three edge types by deterministic rules, with no LLM judgment: a **data dependency** when the next call's input uses a value from the previous output and field types match; a **state dependency** when the first call mutates an environment object and the second reads or further mutates the same object rather than merely coincidentally equal values; and a **retry dependency** when the first call returns an error, the trajectory switches tools, and the next call succeeds — the error is kept in the trajectory as a recoverable observation alongside the successful retry. Edges are weighted by observed transition frequency, w(v_i, v_j) = N_ij / N_i, and low-frequency edges are pruned. Candidate data edges must additionally show that downstream arguments are traceable to upstream output, which the paper says prevents false links caused by common constants such as `limit=10`.

**Environment materialisation.** The weighted undirected projection of the graph is clustered by connection density, giving K = 804 clusters; each cluster defines an environment e_k = (D_k, F_k) with a tool set and a database. Three cases are handled differently. *Operation environments* — those containing tools that create, modify or delete objects — get a synthesized database: a theme m_k is derived from the cluster, a research agent built on a policy model and research tools collects and aligns web data, and the database is iteratively expanded until unit tests and state-transition checks pass. *State-query environments*, whose tools return partial snapshots such as `google_drive.files.list` or `gmail.users.messages.get`, use those outputs as anchors to initialise the environment state, which becomes the initial snapshot s_0, instead of synthesizing a database. *Stateless environments* — web search, fixed-index lookup — replay cached tool results from the corpus as execution outputs, with no live API calls and no database.

**State-aware random walks with rollback.** A walk starts at a tool node bound to a database and a snapshot s_0. A neighbour is admissible only if its next-step inputs can be filled from earlier returns or the current snapshot — dependency reachability, state preconditions and parameter provenance, where every argument must be traceable to the task, s_0 or an earlier observation. Admissible neighbours are sampled in proportion to edge weight, so connections that recur in real traces are more likely to be extended. The walk runs until it reaches the target length L and covers K environments. If a selected tool fails, or the post-execution state is inconsistent with the data or state relation of the traversed edge, the step is discarded, the environment is restored to the previous snapshot and another neighbour is resampled; chains that still cannot proceed after repeated rollbacks are discarded. Every retained chain is finally replayed from s_0, which the paper calls Replay & Acceptance: re-executing the chain against the recorded snapshots guarantees state continuity and that every tool remains executable.

**Reverse verifiable task synthesis.** Each retained chain ω is reverse-synthesised: a language model writes a natural-language task q from the chain and its state changes, and q contains no tool names and no call order. Instead of a reference answer, the chain gets a verification set V = V_state ∪ V_trace ∪ V_out, where V_state checks the final state, V_trace checks key intermediate snapshots, and V_out checks fields that must appear in returned results. A sample is retained only if re-executing ω from s_0 passes every check in V. Difficulty is raised through L, the target number of environments, and the share of cross-environment edges. The dataset is X_TS = {(q, V, ω, s_0)}: task, verification script, tool chain and snapshot. Algorithm 1 closes the loop by deduplicating the dataset, generating teacher trajectories for the retained tasks, and keeping only those that pass V. Kimi K3 is used for both teacher-trajectory generation and reverse verifiable task synthesis.

**Scale of the produced space.** The graph contains 77,760 tool-call-pattern nodes derived from 2,042 distinct canonical tools, with mean and maximum out-degree of 2.3 and 56. Data, state and retry edges account for 69%, 25% and 6% of the edge mix. The 804 environments include Gmail, Google Sheets, Slack, Google Drive, Salesforce and Airtable; the largest domains are Communication & General Utilities (27.4% of environments), Finance & Markets (11.2%) and Document & Design (10.1%). The mean number of matched tools per environment is 10.86 with a maximum of 436; 453 tools (22.2%) are operational against 1,589 (77.8%), and 181 environments (22.5%) are operational against 623 (77.5%). In total the pipeline synthesizes 34,376 trajectories; the 21,385 with at least five tool calls average 18.86 tool calls and 2.29 environments each, with maxima of 209 tool calls, 22 environments and 855,386 tokens.

**Pro benchmark construction.** For a benchmark with original environment e_b = (D_b, F_b), the pipeline collects that benchmark's real tool calls, builds a tool graph with the same rules, and thereby links in tools from outside the benchmark that share data or state relations with benchmark tools — expanding a single environment into a cross-environment cluster. Databases and snapshots are then restored or synthesized, walks are run with larger L and K than the original benchmark, and tasks and verification scripts are reverse-generated and de-duplicated. Three doctoral-level experts independently reviewed all candidate tasks and their verification scripts over a two-day period, and only tasks approved by at least two experts were retained; the paper reports Fleiss' κ = 0.82 and observed agreement of 93.1%. The difficulty increase is measurable in tool calls: on AutomationBench the average rises from 26.8–43.6 calls under the standard split to 56.3–60.6 under Pro, and on τ³-Bench Banking from 23.1–32.2 to 27.3–36.3.

## Evidence

All numbers in this section are **author-reported** from this single preprint; none has been independently replicated.

**Setup.** Seven long-horizon tool-use benchmarks are used: AutomationBench, SkillsBench, JobBench, τ³-Bench Banking, BFCL V4, Harvey LAB and OfficeQA Pro. Three backbones are trained — Qwen3-8B, Qwen3.6-35B-A3B and GLM-5.2-744B-A40B (the resulting 744B model is named ToolSpace-744B-A40B). SFT uses one epoch on 16 GPUs for the 8B and 35B models and 256 GPUs for the 744B model. Agent RL uses the GRPO objective with clipping bounds 0.8 and 1.28, a binary execution-based verification reward, 48 steps, learning rate 2×10⁻⁶, total batch size 256, rollout group size 16, fully asynchronous with a maximum policy staleness of 4. The pipeline yields 34,376 SFT samples and 653 RL samples; RL candidates additionally undergo Pass@16 screening with the 35B model, keeping only candidates with one or two correct rollouts. Results are averaged over three independent runs.

**Main results (average over the seven benchmarks).**

| Model | Size | Avg. score |
|---|---|---|
| Claude Opus 5 | — | 56.6 |
| ToolSpace-744B-A40B | 744B | 56.6 |
| GLM 5.3 | 744B | 53.8 |
| Qwen 3.8 Max | 2.4T | 54.5 |
| DeepSeek-V4-Pro-0813 | 1.7T | 49.9 |
| Kimi K3 (teacher) | 2.8T | 49.7 |
| GPT 5.6 Sol | — | 48.9 |
| GLM 5.2 | 744B | 44.6 |
| ToolSpace-35B-A3B (+RL) | 35B | 43.2 |
| ToolSpace-35B-A3B | 35B | 41.0 |
| Qwen3.6-35B-A3B (backbone) | 35B | 23.0 |
| ToolSpace-8B (+RL) | 8B | 20.7 |
| ToolSpace-8B | 8B | 19.6 |
| Agent-Reflex-8B | 8B | 9.2 |
| Agent-World-8B | 8B | 8.9 |
| EnvScaler-8B | 8B | 8.4 |

Per benchmark, ToolSpace-35B-A3B scores 45.8 on AutomationBench, 42.4 on SkillsBench, 40.0 on JobBench, 34.0 on τ³-Bench Banking, 74.3 on BFCL V4, 1.7 on Harvey LAB and 48.9 on OfficeQA Pro. The 744B model scores 54.7, 67.8, 57.5, 43.3, 78.4, 27.5 and 67.1. SFT alone lifts the 35B model by 18.0 points over its backbone (23.0 → 41.0), with AutomationBench rising from 8.2 to 45.8; on-policy RL adds a further 2.2 points (41.0 → 43.2), the largest single gain being τ³-Bench Banking (34.0 → 42.3). The paper reads the 744B result as exceeding GLM 5.3, GPT 5.6 Sol and its own teacher Kimi K3 on average while matching Claude Opus 5.

**Pro splits (frontier models).**

| Frontier model | AutomationBench Std → Pro (Δ) | τ³-Bench Banking Std → Pro (Δ) |
|---|---|---|
| Claude Opus 5.5 | 59.2 → 26.3 (−32.9) | 51.5 → 35.7 (−15.8) |
| GPT 6.1 Sol | 50.8 → 24.7 (−26.1) | 46.4 → 29.6 (−16.8) |
| DeepSeek-V4.1-Flash-1017 | 60.5 → 22.3 (−38.2) | 51.3 → 36.9 (−14.4) |
| DeepSeek-V4.1-Flash | 54.8 → 20.0 (−34.8) | 50.3 → 35.7 (−14.6) |
| GLM 5.3 | 52.5 → 22.7 (−29.8) | 40.2 → 20.4 (−19.8) |
| Qwen 3.8 Max | 49.7 → 24.0 (−25.7) | 55.2 → 29.6 (−25.6) |
| GLM 5.2 | 29.3 → 18.0 (−11.3) | 37.1 → 12.2 (−24.9) |

Standard-split scores are taken from the Atria Dawn public leaderboard and DeepSeek-V4.1-Flash scores from its official release notes, as the paper states — they are not the authors' own runs.

**Component ablation (35B model).**

| Variant | AutomationBench | SkillsBench | BFCL V4 | τ³-Bench Banking | OfficeQA Pro |
|---|---|---|---|---|---|
| Full ToolSpace | 45.8 | 42.4 | 74.3 | 34.0 | 48.9 |
| w/o state edges | 36.5 | 38.0 | 70.1 | 21.5 | 44.0 |
| w/o data edges | 38.2 | 37.5 | 62.4 | 29.8 | 40.6 |
| w/o retry edges | 43.9 | 41.2 | 72.8 | 32.6 | 47.9 |
| w/o rollback | 41.0 | 39.8 | 71.5 | 30.1 | 46.3 |
| Uniform walk (no w) | 39.6 | 38.9 | 69.8 | 28.4 | 45.1 |
| LLM-judged edges | 37.8 | 36.4 | 66.9 | 26.7 | 43.5 |

Every removal degrades all five benchmarks. The two structural edge types divide the labour: state edges matter most on τ³-Bench Banking and AutomationBench, data edges on BFCL V4 and OfficeQA Pro, with comparable average drops of 7.1 and 7.4 points on disjoint benchmarks. Replacing rule-mined edges with LLM-judged ones degrades every benchmark almost as much as removing state edges. The paper's reading is that edges must be witnessed by execution rather than merely plausible, with rollback and edge-weighted sampling contributing in between and retry edges having the smallest effect.

**Scaling analyses.** Fine-tuning the 35B backbone on increasing fractions of the environment set (1/16, 1/8, 1/4, 1/2, full) improves overall, with AutomationBench jumping from 9.2 to 33.8 between 1/16 and 1/8 and gaining roughly +4 points per doubling beyond 1/8, while τ³-Bench Banking improves more slowly and shows its largest jump only at the full set (19.6 → 34.0). Scaling the training data fraction gives the same shape: AutomationBench rises from 25.2 at 1/16 to 45.8 at full, τ³-Bench Banking from 20.6 to 34.0, with a small SkillsBench dip (32.4 → 32.0) and the 1/16 fraction falling below the untuned backbone on BFCL V4 and OfficeQA Pro, which the paper attributes to interference from too small an SFT mixture.

**Environment relevance.** Ranking environments by benchmark relevance with BGE embeddings and comparing SFT on the full data, the top-50% most relevant environments and a random 50% gives a difference of at most 1.7 points on AutomationBench, SkillsBench, BFCL V4 and OfficeQA Pro, with both half-size conditions approaching full-data performance. The paper concludes the gains do not hinge on benchmark-aligned environments.

**Task diversity.** Sampling 2k questions from each of four SFT corpora and clustering BGE-M3 embeddings with t-SNE and DBSCAN, ToolSpace produces the largest number of question clusters (42) against EnvScaler (25), Agent-World (31) and Agent-Reflex (34).

**Environment synthesis cost.** Using the number of synthesized files as a proxy over 500 environments sampled from Agent-World's public library, Agent-World synthesizes all 2,724 files while ToolSpace synthesizes 1,218 — 1,506 fewer files, a 55.3% reduction, with JSON files falling from 2,643 to 1,205 and CSV from 42 to 7. The paper states the proxy does not directly measure token, wall-clock, API or compute cost.

## Limitations

**Stated by the authors.** The inspected text contains no limitations section and no future-work section for the method itself; the word "limitations" appears only in the paper's critique of the data-centric paradigm it is replacing. The threats that *are* stated are local: the cost figure is explicitly a file-count proxy that "does not directly measure token, wall-clock, API, or compute cost"; the diversity comparison is explicitly attributed to "edge-weighted sampling over observed tool compositions" as the authors' interpretation; and the data-scaling analysis notes interference when the SFT mixture is too small, with the trend stabilising as the fraction grows. Everything else below is assessment.

**Assessed from the reporting.**

- **Single source, in-progress preprint.** All evidence comes from one arXiv preprint whose comment field reads "Working in progress". The paper's own headline is a 38.2-point drop on a benchmark it built, and its training gains come from models trained on 16 to 256 GPUs; a third party without that budget can reproduce the pipeline but not the training curve.
- **Mixed score provenance in the main table.** The paper states its priority order — official leaderboard results, then provider-reported scores under the official protocol, then local reproduction with the official harness, split, metric, tool-call protocol and recommended inference settings — so the Table 1 column mixes three kinds of measurement. The Pro comparison mixes a third-party leaderboard (Atria Dawn) and vendor release notes with the paper's own Pro scores.
- **The environment-scaling result is not monotone.** AutomationBench gains are concentrated between 1/16 and 1/8 of the environment set, the paper itself notes a plateau between 1/4 and 1/2, and τ³-Bench Banking barely moves until the full set. A reading of "performance scales with breadth" therefore rests on a curve with a large early step and a late step, not on a smooth trend.
- **The diversity metric is method-dependent.** The claim that ToolSpace covers a wider task space is an embedding-cluster count (42 versus 25/31/34) from a specific embedding model, dimensionality reduction and clustering algorithm, with no sensitivity analysis over embedding or clustering choices reported in the inspected text.
- **Authenticity is inherited, not guaranteed.** The graph's edges are witnessed by real adjacent calls, but the underlying corpus includes "Low" provenance trajectories that are synthetic, admitted on name and schema matching rather than on execution. The graph is only as execution-grounded as the traces it was mined from.
- **The replay guarantee is about executability, not correctness.** A retained chain satisfies its own assertion set V when replayed from s_0; nothing in the inspected text shows that the decompiled natural-language task faithfully expresses what the chain does. Expert review (two-of-three doctoral-level approval, Fleiss' κ = 0.82) is the only check on that gap, and it is a human judgement on a two-day review.
- **No variance reported.** Results are averaged over three runs, but no standard deviations, confidence intervals or significance tests accompany the main table, so small differences (for example the 56.6-versus-56.6 match with Claude Opus 5) carry no stated uncertainty.
- **Training cost is not quantified.** The paper quantifies *environment synthesis* cost (files synthesized) but not the cost of the 200,000-trajectory collection, the 804 environment clusters, the 34,376 synthesized trajectories or the 653 RL rollouts, which is where the practical barrier for most teams sits.
- **Single-domain dependence of the headline.** The tool space is drawn from 2,042 canonical tools concentrated in office and communication services; the paper does not report which of the seven benchmarks the gains generalise to beyond the five shown in the ablation, and Harvey LAB remains very low in absolute terms for the smaller ToolSpace models (1.7 and 2.5).

## Competing approaches

The paper positions itself against two families it names explicitly, and its stated difference from each is about where the graph comes from and what it guarantees.

**Simulator-style environment scaling.** Simia and GenEnv treat the LLM as an implicit textual world model and generate simulated feedback from tool specifications and interaction histories. The paper's characterisation: inexpensive, but prone to hallucination, with state consistency difficult to guarantee.

**Executable-environment scaling.** EnvScaler, Agent-World, AWM, Agent World Model, Weft and Agent-Reflex synthesize databases, tools and verifiable tasks programmatically, with later variants evolving whole interaction stacks or repairing environments from execution feedback. The paper's difference claim is that in all of these the unit of scaling remains the environment, so which tools may compose is fixed before any task is drawn, whereas ToolSpace recovers composition structure witnessed by execution and synthesizes databases only on demand. ToolSpace also follows the *Trace-to-ENV* principle it attributes to Long et al. (arXiv:2610.06100) and Wu et al. (arXiv:2609.04148), and takes its environment-mining procedure and settings from Agent-World.

**Graph-based agentic data synthesis.** WebShaper builds knowledge graphs for search and knowledge agents; MAGNet translates function-signature or API-dependency graphs into multi-turn calls; APIGen-MT generates multi-turn data through simulated agent–human interplay; Tongui and WebDancer reverse-synthesise trajectories for GUI and web agents. ToolSpace's stated difference is that its edges are mined by deterministic rules from adjacent real calls across environments, typed as data, state or retry and weighted by witnessed frequency, and that a walk enters training only after replay from s_0 passes state, trace and output checks.

Within this knowledge base, ToolSpace is the counterpart to [[projects/envopt]] noted in the 10 November briefing: EnvOpt reorganises a persistent information environment so that a given agent performs better, whereas ToolSpace constructs the environment and the task. It also shares ground with [[projects/agent-r2]], which synthesises productivity tasks from occupational seeds and authentic web sources rather than from tool-composition graphs. Two concepts frame the general questions it raises: [[concepts/evaluator-circularity]] for environments whose tasks are verified by scripts generated alongside the trajectories, and [[concepts/preservation-aware-agent-improvement]] for whether gains on new harder splits preserve performance on the original ones. [[techniques/evaluation-and-simulation]] and [[techniques/verification-and-evidence]] cover the surrounding machinery.

## Implications

The following is analysis, not a claim of the authors.

The strongest transferable idea is not the pipeline but the *ordering*: derive the composition structure from observed behaviour first, and materialise state only where behaviour demands it. That ordering generalises well beyond MCP. The paper's own cost proxy — 55.3% fewer synthesized files than Agent-World on the same 500 environments — follows mechanically from the choice of not building databases for stateless and state-query environments, and the same argument applies to any synthetic-environment work whose ground truth is a database that most tasks never touch.

The ablation is the part worth borrowing methodologically. The finding that LLM-judged edges degrade performance almost as much as removing an entire edge type is a strong argument for rule-mined, execution-witnessed structure wherever such structure exists and can be extracted: the pipeline's value is not that an LLM writes tasks, but that the LLM's role is confined to the least load-bearing step (decompiling a verified chain into prose) while the relation structure is extracted deterministically. Where a graph cannot be mined, the paper's own results give a reason for caution rather than encouragement.

A second implication is about what a "harder benchmark" costs. The Pro splits raise difficulty by adding cross-environment tool calls, and every frontier model drops — but the drops are uneven (11.3 to 38.2 points on AutomationBench, 14.4 to 25.6 on τ³-Bench Banking), which means a Pro score is not directly comparable to a Standard score from a different model set. Any team adopting cross-environment difficulty should report the standard split alongside, and treat the delta, not the absolute number, as the comparable quantity. This is the same class of issue as [[concepts/protocol-relative-scores]].

Third, the training results raise a capability-locus question that the paper only partially addresses. The 8B model trained on this data reaches 19.6 average against 7.2 for its untuned backbone and 8.4–9.2 for other environment-scaling baselines at the same size, and the 35B model reaches 41.0. But the pipeline also builds the training environments, so part of what is measured is the interaction of one artifact with itself; the paper's own mitigation is the relevance analysis showing top-50% and random-50% environment sets differ by at most 1.7 points, which is a partial answer to the circularity question rather than a resolution of it. The independent-replication gap here is the important one: nobody has yet shown that ToolSpace-trained agents transfer to environments the pipeline never saw, and that is the claim a deployment would actually need.

Finally, the practical caveat: the replay-verification filter is what makes the data auditable, and it is also what makes the pipeline expensive. A pipeline that must execute every sampled chain and re-execute it for acceptance will not scale cheaply, and the paper's cost accounting covers environment synthesis but not this execution load. Anyone replicating should instrument the walk budget and acceptance rate from the start, because those two numbers determine whether the approach is affordable at their scale.

## Reproducible experiment

The paper states a GitHub repository, a project page with an interactive demo and a Hugging Face model collection; these URLs appear in the paper's header and were not fetched for this page, so their contents and completeness are unverified here. Assuming the pipeline is runnable, a check that would meaningfully probe the claims rather than restate them:

1. **Edge mining on a small, controlled corpus.** Take one real MCP server set (a handful of tools with a stateful object) plus a few hundred recorded call chains. Mine the three edge types with the stated rules — value-provenance for data edges, mutation/read identity for state edges, error-then-switch for retry edges — and check the two known failure modes by hand: a common constant such as `limit=10` appearing in both calls must not create a data edge, and two calls touching different objects with equal values must not create a state edge. A pass criterion is that the mined edge set matches a hand-labelled set on this sample; a failure would show the rules need more context than the paper describes.
2. **Witnessed vs judged edges at small scale.** Build the same graph twice — once from the deterministic rules, once by asking a model to propose adjacency — and run the pipeline from each. The paper's ablation reports a large gap (for example AutomationBench 45.8 vs 37.8, τ³-Bench Banking 34.0 vs 26.7) at 35B scale; at small scale the informative measurement is whether the *composition* of the two edge sets differs, i.e. whether the judged set contains edges the rules reject as coincidental.
3. **Replay acceptance and rollback behaviour.** Instrument the walker to report the acceptance rate of sampled chains, the number of rollbacks per retained chain, and the fraction of chains discarded after repeated rollbacks. The paper's interactive demo shows one walk of 28 tool calls across 6 environments completed after 2 rollbacks and kept after replay verification; a much larger rollback-to-retention ratio in your environment would mean the graph's edges do not hold under your services' real state behaviour.
4. **The difficulty claim on one model.** Evaluate a single model on a standard split and on the corresponding Pro split, and report both the absolute scores and the tool-call counts per task. The paper's Pro splits are the harder artifacts; what makes them useful as a benchmark is the tool-call growth (AutomationBench 26.8–43.6 → 56.3–60.6). If your own tasks grow in tool calls but the model's score does not drop correspondingly, the added difficulty is longer trajectories rather than harder decisions — a distinction the paper's aggregate drop figures do not separate.

If the released artifacts turn out not to contain the pipeline or the Pro task sets, reproduction falls back to reimplementation from Sections 4 and 5 and to the graph-level checks above; that limitation should be reported with any result.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2611.05036) and the complete HTML full text including all seven sections, the three tables, the algorithm and the reference list (https://arxiv.org/html/2611.05036v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; the Pro-split standard scores come from a third-party leaderboard and the DeepSeek scores from vendor release notes, as the paper states; the paper's comment field reads "Working in progress" and no peer-reviewed venue is claimed. The repository, project-page and model-collection URLs are quoted from the paper's header and were not fetched or inspected for this page. Claim types are separated in the text: the "execution-witnessed edges clearly outperform LLM-judged ones" reading, the beyond-teacher interpretation and the cost-saving framing are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or trained by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-10]] — dated full-fidelity research and cross-project synthesis.
