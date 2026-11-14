---
uid: a29b51f0-ec09-4b70-9e90-900000000001
title: "EnvOpt"
summary: "Automated pipeline that optimizes a shared agent environment for lower cost and better pass rate, training without verifiers."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
related: [verified-completion-vs-apparent-success, preservation-aware-agent-improvement, protocol-relative-scores]
sources:
  - https://arxiv.org/abs/2611.07372
  - https://arxiv.org/html/2611.07372v1
---

# EnvOpt

## What it is

EnvOpt is an automated optimization pipeline for the *environment* an LLM agent works in, reported in the arXiv preprint "EnvOpt: Automated Optimization for Agent Environments" (arXiv:2611.07372, submitted 5 November 2026, cs.AI; preprint, no peer-reviewed venue claimed; CC BY 4.0 licence). The paper lists six authors — Mingxuan Li, Huanzhi Mao, Qiuyang Mang, Hanchen Li, Joseph E. Gonzalez and Alex Dimakis — and the acknowledgements name a collaboration between the University of Chicago, the UC Berkeley Sky Computing Lab and Bespoke Labs.

The framing: an agent's cost and success depend on three things — model parameters, the harness, and the environment — and the first two are actively optimized (parameter tuning, harness optimization) while the environment is usually treated as immutable. EnvOpt proposes environment optimization as a third axis. Its object of optimization is what the paper calls a **stationary environment**: a large collection of artifacts that stays the same, or similar, across many tasks — a company's Slack workspace, a set of enterprise data sources, a code repository. The paper's novelty claim is that "environment optimization itself as the third direction of agent optimization remains underexplored", citing earlier work on RL environments, hand-designed agent interfaces, PREPING and Corpus2Skill as adjacent but different.

The method is automated end-to-end: a coding research agent edits the environment on the basis of target-agent trajectories, without any grader or reference answer for the training tasks.

## Mechanism

EnvOpt writes the underlying information as *I* and its representation as *E(I)*; the same Slack history can live behind an MCP server or in plain-text files that `grep` can search. The target agent is *T*, the research agent is *R* (a coding agent such as Codex). The objective is stated as an explicit minimization of the target agent's cost:

> E\* = arg min over E of E_{x~X}[cost(T, E(I), x)]

**Algorithm 1 (Environment Evolution).** The inputs are the initial environment E₀(I), the target agent T, the research agent R, training tasks X_train *without verifiers*, validation tasks X_val *with verifiers*, a number of steps N, a per-step budget B and an accuracy tolerance δ. X_train is partitioned into disjoint subsets X₁…X_N — disjointness is to prevent overfitting, and only a subset is given per step because "too much context for LLM-based optimization has been shown to be harmful". The loop for k = 1…N spawns R in a sandbox with X_k, the environment from step k−1, access to run T and budget B. Inside the step, R runs T on X_k, analyses the trajectories τ, edits the environment into a candidate E′, and re-runs T to get τ′. **The candidate is accepted only if the cost of τ′ is lower than the cost of τ and R judges accuracy preserved** — judged by R itself using proxies or answer consistency, because no verifier exists for the training tasks. Failing candidates are discarded. The inner loop runs until the budget is exhausted or R terminates. At the end of the step the best environment found is kept and **any changes R made to T's harness are discarded**, which is what makes the direction orthogonal to harness optimization. Then cost c_k and accuracy a_k are measured on X_val; if c_k > c_{k−1} or a_k < a_{k−1} − δ, the evolution stops and E_{k−1} is returned; otherwise the loop continues and the final E_N is returned.

**Training with no verifiers.** Verifiers are hidden for training tasks specifically to stop the research agent from reward-hacking, the example given being writing down the answers to the training tasks to lower cost directly. This also mitigates task scarcity: in-distribution queries can be synthesized without synthesizing verifiers. A separate validation set with verifiers is kept for the stopping rule, which is the only place in the method where a verifier-backed score is consulted.

**What the research agent is allowed to do.** It has freedom over design: it can restructure a directory into per-domain subdirectories, write cheatsheets, build a small database, add new tool endpoints, or — when environments are highly similar but not identical — write a converter program for the next environment.

**Accepted optimizations (§4.1), as reported.** On AutomationBench, a program retrieves Gmail information directly and presents sender, subject, message ID and chunks of the email as plain text, so the agent reads text instead of spending tokens on large tool calls; on Workspace-Bench, `.xlsx` files are converted to `.txt`. A cheatsheet on AutomationBench stores the API endpoints needed to create Jira issues, post Slack messages and record a Xero payment, so the agent need not call `api_search`/`api_fetch`; on Bleve, a cheatsheet stores template commands for complex tool calls. On Workspace-Bench an index file records the paths, sizes and types of all files so the agent searches the index instead of the filesystem. On Data-Eng-Bench the agent builds an SQLite database of table locations, which file each script writes to, and what each table holds. For Bleve, a program takes a bug report and outputs the eight `.go` files most likely to be affected, by keyword matching. For tenacity, `validate_tenacity.py` fetches the target agent's code change, finds relevant test files, runs them and returns verdicts.

**Rejected optimizations (§4.2), as reported.** A single large file holding all possible values of all database columns (Data-Eng-Bench) *increased* cost: one tool result revealed that a great deal of unexplored information existed, so the agent made more tool calls. A search tool that returned too many files (Workspace-Bench) cut the cost of finding files but increased reading, so cost rose. And in step 2 on Bleve, a check was added to a test script that scans for a particular bug-fix code snippet and fails if it is present; it worked on X₂, but on X₃ some correct fixes were rejected and the agent spent much more time trying to bypass the check.

**Research-agent behaviour (§4.6).** The authors report four observations. An unreliable verification proxy hurt: on Workspace-Bench the research agent sometimes used answer length and keyword matching to confirm answer quality, and this "often turns out to hurt performance on heldout tasks"; the instruction was changed after observing the validation set. Validation cost reduction correlates with how much tool-call patterns change during a step: Pearson 0.75 on AutomationBench between validation cost reduction and the per-task difference in tool-call counts before and after a step. Looking instead at the fraction of training tasks receiving more than 30% cost reduction in a step, the Pearson correlation with validation cost reduction is 0.82 for AutomationBench, 0.70 for Workspace-Bench and 0.56 for Data-Eng-Bench. The research agent also failed to follow instructions: on Workspace-Bench it tried to change Codex's reasoning effort during step 6; the change was discarded because only the environment directory is kept, but it could have affected that step's optimizations. Finally, running three steps without a validation set is described as "generally safe" — explicitly labelled by the authors as an empirical claim only — while the validation set with real verifiers remains important for auditable optimization.

## Evidence

All results in this section are **author-reported** from the single preprint; none has been independently replicated. The paper's headline numbers are percentages of token cost and of pass rate as stated in the abstract and prose; the units of the pass-rate figures are as printed by the authors and are not described as percentage points.

**Setup.** Five benchmarks over three task types: workspace tasks (AutomationBench, Workspace-Bench), data engineering (Data-Eng-Bench), and software engineering (Bleve repository tasks as used in gskill; SWE Agent Efficiency tasks on the tenacity library as used by advisor models).

| Benchmark | Split | Target agent | Research agent | Author-reported outcome |
|---|---|---|---|---|
| AutomationBench | 200 test, 96 val, remainder training pool, from 600 public tasks | Claude Code + Claude Haiku 4.5 | Claude Code + Claude Opus 4.8 | cost −72.7%, pass rate +14.34% |
| Workspace-Bench | 80 test, 20 val, from the 100 public leaderboard tasks | Codex + GPT-5.4-mini | Claude Code + Claude Opus 4.8 | cost −47.65%, pass rate +3.3% |
| Data-Eng-Bench | 73 test, 19 val | Codex + GPT-5.6-luna | Codex + GPT-5.6-Sol | cost −53.44%, "without hurting the performance" |
| Bleve (gskill splits) | as provided by gskill | as provided by gskill | — | near-perfect score at 56.9% of gskill's completion time |
| tenacity (advisor-model splits) | as provided by advisor models | as provided by advisor models | — | +8.9% pass rate over Advisor Models, fewer steps |

AutomationBench training used 20 tasks per step and stopped at step 5, "where results on X_val begin to saturate". On Workspace-Bench and Data-Eng-Bench the training queries were synthesized without verifiers, 20 distinct tasks per step. On Workspace-Bench, Claude Code with Sonnet 5 was the judge agent for evaluation on both X_test and X_val, so that benchmark's pass rates are judge-scored.

**Aggregate.** Across the five benchmarks the paper reports an average **48% cost reduction** on unseen test sets with "higher or similar pass rates", and "substantial cost reduction up to 88%".

**Comparisons on AutomationBench.** GEPA and Meta-Harness were run by the authors with the same training task pool, the same research agent or proposer, the same target agent and the same X_test; EnvOpt "achieves significantly better outcomes on both cost and pass rate, even without verifiers for training tasks". The introduction states EnvOpt outperforms Meta-Harness by **9.67% pass rate with only 15% of its cost**.

**Transfer to other models and harnesses.**

| Condition | Author-reported outcome |
|---|---|
| AutomationBench → other models/harnesses | average cost reduction 75.7%, generally higher pass rates |
| AutomationBench → Claude Code + Claude Opus 5 | cost −68.1%, pass rate +1.34% |
| AutomationBench → Claude Code + Claude Haiku 5.5 | pass rate higher than Opus 4.8's and "even close to Opus 5" |
| Workspace-Bench → Codex + GPT-5.6-Sol and Claude Code + Opus 5 | average cost reduction 56.7%, steady pass rates |
| Data-Eng-Bench → non-target agents | average cost reduction 53.54% |

**Stacking with harness optimization.** On top of Meta-Harness's optimized harness for Haiku 4.5, EnvOpt lowers cost "by a further 83.4% and adds 11.17% accuracy over Meta-Harness alone" (abstract); the introduction describes the same experiment as "16% improvement in pass rate" on top of Meta-Harness, outperforming either alone. When transferring to Opus 5, Meta-Harness alone shows no pass-rate gain, but EnvOpt on top of Meta-Harness still improves pass rate at much lower cost. Figure 1's caption states that the offline optimization of the AutomationBench environment costs around **USD $150** and saves the cost of running Claude Opus 4.8 by **77.5%** — a different agent from the 72.7% headline.

**Where the savings come from (§4.3).** Token counts are broken into categories (tool calls, tool execution results, thinking tokens, agent history). The most significant reduction is in the *environment feedback* categories on the input side, with further savings on the tool-call categories on the output side.

**Ablation — tool optimization only (§4.4).** Claude Code with Haiku 4.5 was run on the original environment E₀ with only the *tools* from E₅. Tool optimization alone improves both token efficiency and pass rate, but "is significantly lower than optimizing both the tools and the environment". The paper reads this as evidence that EnvOpt offers headroom beyond harness engineering. No numbers for this ablation appear in the HTML text; the result is presented in a figure.

**Training cost and time (§4.5).** Cumulative training cost, including the target-agent runs the research agent launches, is compared with the cost saved by running different agents on 1,000 unseen tasks; for frontier agents deployed at scale the paper claims savings "more than 10 times" the cost of running EnvOpt.

## Limitations

**Stated by the authors.** The paper has no dedicated limitations section; the relevant caveats appear in the discussion. The no-validation-set guidance is explicitly an empirical claim only. The research agent's use of unreliable proxies is acknowledged as harmful to held-out performance and was corrected only after looking at the validation set. The instruction-following failure (attempting to change Codex's reasoning effort) is acknowledged as capable of harming a step even though the change was discarded. The Data-Eng-Bench SQL splitter introduced at step 1 parsed on semicolons and broke when the semicolon was inside quoted text; the paper notes this bug stayed uncovered until step 5, inflating cost across four steps because the target agent could not tell its query had been corrupted and attributed the failure to itself. The tool-only ablation and the token-category breakdown are reported without numbers in the inspected HTML text, and the per-step and per-model result tables are figures rather than text.

**Assessed from the reporting.**

- **Single source, no artifact.** Everything rests on one arXiv preprint (v1, 5 November 2026). A search of the inspected HTML for a code or data link finds only third-party URLs (the Snowflake-Labs/data-eng-bench repository, arXiv's own infrastructure) and no EnvOpt artifact, so no third party can rerun the authors' configurations as written and no result has been independently replicated.
- **Most of the result detail is in images.** The per-step curves, the per-model transfer table, the tool-only ablation and the token-category breakdown are figures; the HTML full text exposes only the aggregates quoted above. Anyone checking the numbers beyond the abstract would need the PDF.
- **Cost is agent token cost, not total cost.** The reported savings measure the target agent's token cost; the optimization itself consumes research-agent tokens, target-agent runs and wall-clock time, and the paper's own amortization argument needs 1,000 tasks before the saving dominates.
- **Stop selection is a validation-set selection.** The environment returned to the reader is chosen by a rule evaluated on X_val, and the training tasks are synthesized without verifiers on two of the five benchmarks, so the selection pressure differs from a fully supervised setting.
- **Small and heterogeneous effects.** The Workspace-Bench pass-rate gain is 3.3% on a judge-scored benchmark, and the transfer pass-rate gain to Opus 5 is 1.34%. The paper reports no confidence intervals or significance tests in the inspected text, so a 3.3-point difference on 80 test tasks should not be read as a reliable improvement.
- **The research agent is an uncontrolled component.** It proposes the edits, judges its own accuracy preservation, and is instructed not to touch the model or harness; the paper documents one case where that instruction was violated. Whether a cheaper or more constrained proposer would find the same environments is not tested.
- **Optimization can produce artifacts that only fit the task distribution.** The rejected-optimization section shows the failure mode is concrete and recurring: an index, a search tool or a test check that helped on one step's tasks could mislead on the next. The paper's evidence that this is caught is the validation set, not a guarantee.
- **Benchmark-specific.** All five benchmarks are agentic task environments the authors chose; no human-facing environment (a wiki a person reads, a support inbox) is evaluated, and the paper gives no evidence about how an optimized environment changes the experience of human consumers of the same artifacts.

## Competing approaches

**Compared directly, on the same tasks and target agent.** *GEPA* (Agrawal et al., 2026b) evolves prompts reflectively; *Meta-Harness* (Lee et al., 2026) optimizes the harness end to end. Both were run by the authors on AutomationBench with the same training pool, proposer, target agent and test set. *gskill* (Agrawal et al., 2026a) optimizes coding-agent skills using tasks with verifiers from the same repository, and is the comparison point for the Bleve result (EnvOpt at 56.9% of gskill's completion time). *Advisor Models* (Asawa et al., 2026) trains an advisor model to steer a black-box agent, and is the comparison point for tenacity (EnvOpt +8.9% pass rate).

**Cited as related in the introduction.** *SWE-agent* (Yang et al., 2024) and "The devil is in the interface" (Xu et al., 2026) show that a better repository interface changes what the same model can do — but the interfaces were manually designed. *EnvHarness* (Huang et al., 2026) and "Don't just fine-tune the agent, tune the environment" (Lu et al., 2026) reshape environments to create RL training signal rather than to improve deployed-agent execution efficiency. *PREPING* (Choi et al., 2026) and *Corpus2Skill* (Sun et al., 2026) distill environment information into agent memory and skills instead of reorganizing the environment. *Mak et al.* (2026) supply the motivating measurement that the tool interface alone changes how much work an agent must do. *Combee* (Li et al., 2026) is cited for the context-scaling result that motivates giving the optimizer only a subset of tasks per step.

The authors' differentiation claim is that prior work attaches reusable workflows or executable artifacts to skill execution or improves training-time environments, whereas EnvOpt optimizes the stationary environment itself for deployed execution. That is an author claim about positioning, not a demonstrated head-to-head result beyond the benchmarks above. Within this knowledge base, the closest neighbour is [[projects/context-as-infrastructure]], which changes retrieved representations rather than searching the environment end to end; [[projects/strategist]] and [[projects/tigerless-agent-memory]] are analyst-level comparison points recorded in [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The transferable idea is to treat environment layout as a measured, optimizable variable rather than an inherited constraint. The paper's own evidence is that representation choices moved token cost by 48–88% on the same agent and harness, and the largest single contributor was environment feedback tokens — that is, what the environment hands back per action. Any team with an expensive agent and a fixed corpus should be able to test this hypothesis cheaply, and the paper's cost-reduction breakdown suggests where to look first.

The second, less obvious takeaway is that an optimizer without ground truth is a design constraint worth taking seriously, but only with a separate scored set. The authors' refusal to expose training verifiers is a real defence against reward hacking, and the fact that they still needed a verifier-backed validation set to decide when to stop suggests that "no graders" applies to the *training* loop, not to the whole method. A deployment that has no verifier-backed validation set has no equivalent stopping rule, and the paper's own "three steps is generally safe" claim is explicitly empirical, not principled.

Third, the rejected-optimization results are the most reusable part of the paper and are qualitative rather than numeric: a large consolidated file invites more exploration, a search tool that returns too much invites more reading, and a check that fits only the current task distribution causes the agent to spend time defeating the check rather than doing the task. Each of those is a failure mode that also appears when a knowledge base is restructured for agent consumption — a single index that reveals there is more to explore, a retrieval tool that returns everything, a validation script tuned to one task family. This is a concrete link to [[concepts/preservation-aware-agent-improvement]]: the environment changes that help agents must be evaluated for their effect on the humans and tools that share them.

Fourth, on the defence side the paper's claims are about cost and pass rate, not safety, and the evaluation would not have caught a degraded human experience, an environment that quietly drops information a person needs, or a research agent that writes the answers into the environment. The pass-rate check is a verifier-backed measurement on the target agent's task distribution; it says nothing about other consumers of the same artifacts, and it cannot distinguish a genuinely cheaper interaction from one that merely looks cheaper — the [[concepts/verified-completion-vs-apparent-success]] problem in a new setting. An environment optimized for one agent is not thereby optimized for everyone, and the paper reports no human-facing evaluation at all.

## Reproducible experiment

No artifact is linked in the inspected text, so any check means reimplementing the pipeline from §2 and Algorithm 1. A feasible independent test:

1. **Two-condition A/B on a shared corpus.** Take a fixed corpus of documents and a fixed set of held-out tasks with verifiers. Run the target agent on (a) the corpus as-is and (b) a corpus restructured by a research agent that is given training tasks *without* verifiers, an explicit budget, and a separate verifier-backed validation split for the stopping rule. Use the same model, harness, temperature and task set in both conditions. The paper predicts a large token-cost reduction with pass rate maintained or improved; the reference figures are −72.7% cost and +14.34% pass rate on AutomationBench, −47.65% and +3.3% on Workspace-Bench.
2. **Run the stopping rule.** Reproduce the accept/reject rule (cost of the candidate trajectory must be lower than the incumbent's *and* accuracy must be judged preserved) and the validation-triggered rollback (revert when validation cost rises or validation accuracy falls by more than δ). The informative output is the per-step trajectory: does the environment keep improving, plateau, and then regress the way the Data-Eng-Bench splitter bug did? A run that never regresses on your corpus is a stronger result than the paper's own.
3. **Transfer test.** Apply the optimized environment to a *different* model and a *different* harness with nothing changed, and measure cost and pass rate against the unoptimized corpus. The paper's transfer figures (75.7% average cost reduction on AutomationBench, 56.7% on Workspace-Bench, 53.54% on Data-Eng-Bench) are the reference. If the savings collapse under transfer, the finding does not generalize.
4. **Tool-only ablation.** Repeat condition (b) but hand the target agent only the *new tools* from the optimized environment, keeping the original corpus layout. The paper finds tool optimization alone helps but is "significantly lower" than optimizing both; this is the cheapest way to check whether the headline effect is really about the environment or about the tooling.
5. **Negative controls.** Record the costs of the three rejected patterns — a single consolidated file, a search tool with a generous result limit, and a task-specific validation check — and verify they raise cost rather than lower it. These are the paper's own qualitative claims and are the easiest results to falsify.

The paper's 2026-era hosted backbones (Claude Haiku 4.5, Opus 4.8/5, GPT-5.4-mini, GPT-5.6-Sol/luna) are not reproducible as such; substitutions, partition differences and judge differences should be reported alongside the results.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2611.07372) and the complete HTML full text including §4's discussion, the reference list and Appendix A (https://arxiv.org/html/2611.07372v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; the baselines (GEPA, Meta-Harness, gskill, Advisor Models) were run by the authors, and no independent replication is known. A full-text search for a code or data link found only the third-party data-eng-bench repository and arXiv's own infrastructure, so no EnvOpt artifact is publicly linked in the inspected text. Several result tables and figures are images and are therefore not verifiable from the HTML text alone; the numbers quoted here are the ones stated in prose or in the abstract. Claim types are separated in the text: the third-axis, first-of-its-kind and transfer claims are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no attack code from the source was run.

## Historical coverage

- [[briefings/2026/11/2026-11-09]] — dated full-fidelity research and cross-project synthesis; this page is the deep-depth grounding of the EnvOpt finding.
