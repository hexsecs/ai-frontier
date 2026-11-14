---
uid: b6a90405-a8d1-4d13-9a40-000000000015
title: "CrossSWE"
summary: "Benchmark of 171 real-world cross-repository joint-development tasks where only coordinated changes across interdependent repositories pass."
type: benchmark
created: 2026-11-09
updated: 2026-11-13
depth: deep
related: [expertcrowd-swe, geofaham, protocol-relative-scores, capability-locus, verified-completion-vs-apparent-success]
sources:
  - https://arxiv.org/abs/2611.01484
  - https://arxiv.org/html/2611.01484v1
  - https://huggingface.co/datasets/CrossSWE/CrossSWE-Bench
---

# CrossSWE

## What it is

CrossSWE is a benchmark for **cross-repository joint development** — software-engineering tasks whose solution requires coordinated changes in two or more interdependent repositories. It is reported in the arXiv preprint "CrossSWE: Benchmarking Cross-Repository Joint Development for Coding Agents" (arXiv:2611.01484, submitted 1 November 2026, cs.SE; preprint, no peer-reviewed venue claimed). The paper lists seven authors — Silin Chen, Yuling Shi, Heng Lian, Zihan Zhang, Xiaodong Gu, Haotian Lin and Zhensu Sun — with affiliations at Shanghai Jiao Tong University, Xidian University and Singapore Management University.

The benchmark contains **171 real-world instances** spanning **165 repositories**, **20 technical domains** and **13 programming languages**. 165 instances involve two repositories, five involve three and one involves five. The argument is that single-repository benchmarks have saturated and that the remaining complexity is not more files or longer horizons inside one repository but the coordination *across* repository boundaries: dependency reasoning, change propagation and interface consistency. A second line of argument targets the multi-repository benchmarks that already exist — BeyondSWE and DepBench — where the additional repositories are only *context* to read, while the patch and the tests stay inside one repository.

The distinguishing methodological commitment is **joint-necessity verification**: each instance is kept only if partial repository modifications provably fail and the full coordinated patch provably passes. The dataset is **released** at https://huggingface.co/datasets/CrossSWE/CrossSWE-Bench.

## Mechanism

**Instance anatomy.** Each instance has four parts: (1) a pre-configured execution environment holding two or more participating repositories at their base commits with all dependencies installed; (2) a problem statement describing one software-engineering task spanning those repositories; (3) a test suite validating the target cross-repository behaviour plus required existing behaviour; (4) repository-specific gold patches recording the original developers' coordinated solution. An instance counts as resolved only if the joint repository state satisfies the complete evaluation suite.

**Construction pipeline, four stages.** *Stage 1 — candidate collection*: the GitHub API is used to find active repositories and search their development histories from January 2025 through September 2026 for candidate cross-repository changes, mining merged pull requests, issues with reconstructable changes, commits and release or compatibility discussions, using cross-repository cues such as API evolution, dependency migration, provider–consumer and client–server relations, plus explicit references to issues, pull requests, commits or repositories in other codebases. The discovery stage is explicitly designed for high recall. *Stage 2 — human screening*: each candidate is inspected with its source pull request or issue, development timeline, referenced repositories and commits; a candidate is retained only when the source evidence identifies a concrete change and at least two repositories contain substantive implementation changes that are causally, dependently or coordinately related to the same task. Candidates whose extra involvement is documentation, release notes or changelogs are excluded, as are candidates with insufficient or ambiguous evidence. *Stage 3 — environment construction and joint-necessity verification*: a dedicated Docker image holds all repositories at their verified base commits with build and execution dependencies installed, every checkout in a clean Git state, with fixed checkouts, gold patches, hidden tests and artifacts of the fixed versions excluded from the agent-facing image. *Stage 4 — problem statement construction*: following SWE-Bench ProMax, each verified candidate is turned into a self-contained natural-language specification describing the observable failure, the expected behaviour and the cross-repository requirements from the pre-fix perspective, without prescribing implementation details; gold patches, fixed commits and evaluator metadata are stripped, and consistency between statement, source evidence and tests is manually verified.

**The joint-necessity test.** For an instance involving N repositories, each repository is in one of two states — original base or gold-patched — and all 2^N mixed-version configurations are enumerated inside the same Docker environment. The target FAIL_TO_PASS tests are executed in every configuration. A candidate satisfies the criterion only if the behaviour fails in the all-base configuration **and** in every partially patched configuration, and succeeds only when all required repository patches are applied together. For a two-repository instance (A, B): (A₀,B₀), (A₁,B₀) and (A₀,B₁) must fail and (A₁,B₁) must pass. This is what separates tasks whose solution merely *mentions* several repositories from tasks whose repository changes are jointly necessary.

**Composition.** Task intents are classified into eight mutually exclusive high-level categories covering all 171 instances: feature development (54), API / schema / protocol evolution (43), bug fixing (22), security, identity and observability coordination (21), deployment, platform and runtime coordination (14), migration, upgrade and refactoring (9), test, benchmark and conformance adaptation (7) and transitive change propagation (1). Reference-patch size is broader than in SWE-bench Pro and SWE-Bench ProMax: 56.1% of instances modify more than ten files (against 6% and 30%) and 66.7% change more than 200 lines (against 13% and 32%).

**Worked example.** The paper's Figure 2 uses oauth2-proxy and Higress: during session refresh, multiple cookies are merged into a single HTTP header, causing authentication failures. Resolving it requires oauth2-proxy to preserve cookies as a list *and* Higress to process and emit each cookie separately; modifying either repository alone leaves the shared interface inconsistent.

**Task-intent taxonomy.** The eight categories and their instance counts, covering all 171 instances of the formal evaluation subset:

| Category | Instances |
|---|---|
| Feature development | 54 |
| API / schema / protocol evolution | 43 |
| Bug fixing | 22 |
| Security, identity and observability coordination | 21 |
| Deployment, platform and runtime coordination | 14 |
| Migration, upgrade and refactoring | 9 |
| Test, benchmark and conformance adaptation | 7 |
| Transitive change propagation | 1 |

The last category covers a required change propagated through a multi-step dependency chain involving more than two repositories; the paper does not state in the inspected text which instance sits in it.

**Experimental setup.** All experiments use mini-SWE-agent v2.4.6 as a common scaffold, five frontier models — GPT-6.1 Sol, Claude Sonnet 5.5, DeepSeek V4.1 Flash, GLM-5.3 Flash and Qwen3.8-Flash-Next — at high reasoning effort with a fixed agent configuration, at most 300 interaction steps and a maximum model cost of $10 per instance. The primary metric is Pass@1: an instance counts as resolved only when the final repository state satisfies the complete evaluation suite.

## Evidence

All numbers in this section are **author-reported** from this single preprint; none has been independently replicated.

**Main results.** Same instance set for all five models:

| Model | Pass@1 % | Single-lang % | Multi-lang % | Avg. input tok. | Avg. output tok. | Avg. steps | Avg. cost ($) |
|---|---|---|---|---|---|---|---|
| GPT-6.1 Sol | 58.48 | 60.34 | 54.55 | 0.97M | 12.5K | 32.9 | 0.3496 |
| Claude Sonnet 5.5 | 50.29 | 52.59 | 43.64 | 1.31M | 16.3K | 29.2 | 0.5217 |
| DeepSeek V4.1 Flash | 52.63 | 52.59 | 52.73 | 17.54M | 88.73K | 152.7 | 0.2881 |
| GLM-5.3 Flash | 43.86 | 45.69 | 40.00 | 9.74M | 55.21K | 141.7 | 0.3411 |
| Qwen3.8-Flash-Next | 45.03 | 45.61 | 43.86 | 13.31M | 75.68K | 182.1 | 0.2939 |

The paper contrasts GPT-6.1 Sol's 58.48% on CrossSWE with its reported 75.2% on DeepSWE v1.1, reading the gap as evidence that cross-repository joint development adds difficulty beyond conventional repository-level work. GPT-6.1 Sol leads on single-language tasks (60.34% vs 54.55% multi-language); DeepSeek V4.1 Flash stays competitive across the language boundary (52.73% multi-language). On cost, the closed-source leaders pay for their shorter trajectories: GPT-6.1 Sol and Claude Sonnet 5.5 average 32.9 and 29.2 steps against 152.7, 141.7 and 182.1 for the three open-weight models, and GPT-6.1 Sol's $0.3496 per instance is close to GLM-5.3 Flash's $0.3411 and above DeepSeek V4.1 Flash's $0.2881 and Qwen3.8-Flash-Next's $0.2939.

**Joint vs single-side development.** From the 165 two-repository instances the authors derive **330 single-side modification tasks** that keep both repositories in the environment but permit modification of only one, isolating the effect of joint modification from the effect of having cross-repository context:

| Model | Joint Pass@1 % | Single-side Pass@1 % | Joint steps | Single-side steps |
|---|---|---|---|---|
| GPT-6.1 Sol | 58.48 | 64.55 (+6.07) | 32.90 | 18.54 (−14.36) |
| DeepSeek V4.1 Flash | 52.63 | 61.81 (+9.18) | 152.70 | 126.94 (−25.76) |

**Licensing and release.** The benchmark is constructed from public GitHub repositories and development histories and is hosted on Hugging Face with source references and patch provenance preserved for attribution. The upstream licenses of all 165 repositories were reviewed and their applicable terms documented in the release; original non-code benchmark materials are licensed CC-BY-4.0 while third-party source-code contributions remain under their respective upstream licenses; for instances involving commercially licensed MUI X components, official licensing documentation permits qualifying non-production benchmark use. An appendix also records that AI assistants were used to draft basic code and refine the manuscript language, with all experimental designs, data analyses and conclusions conducted and verified by the authors.

**Behavioural observations.** GPT-6.1 Sol and Claude Sonnet 5.5 reach relevant code locations and begin editing earlier with larger, more concentrated edits; DeepSeek V4.1 Flash and GLM-5.3 Flash spend more interactions exploring repository structure and dependencies before alternating between incremental edits and testing. The difference in final source lines changed is much smaller than the difference in interaction length, so the shorter trajectories are not simply smaller patches.

**Failure patterns.** The authors manually classify unsuccessful trajectories into five categories: cross-repository inconsistency (incompatible interfaces, protocols or artifacts across repositories, including related compilation and build failures), incomplete implementation, compatibility regression, logic/state errors, and boundary handling. Cross-repository inconsistency is the most prevalent category for every model: 44.2% of GPT's unsuccessful trajectories, 41.2% of Claude's, 29.2% of DeepSeek's and 40.7% of GLM's. Incomplete implementation is the second-largest for Claude (29.4%), DeepSeek (25.0%) and GLM (25.4%). DeepSeek has the most distributed profile, with higher compatibility-regression (18.8%) and boundary-handling (14.6%) shares. The per-model percentage for Qwen3.8-Flash-Next is not disclosed in the inspected text.

## Limitations

**Stated by the authors.** Three limitations are given. *Coverage*: although the benchmark has 171 instances across 165 repositories and 20 domains, coverage of large-scale multi-repository development remains limited — 165 instances involve two repositories and only six involve three or more; extending to larger networks of interdependent repositories is future work. *Repository discovery*: the participating repositories are handed to the agent, so evaluation focuses on dependency reasoning and coordinated modification rather than on identifying relevant repositories in a broader ecosystem; introducing irrelevant repositories to test discovery and selection is proposed as an extension. *Scaffold*: a unified mini-SWE-agent scaffold and consistent configuration were adopted for fair model comparison; because mini-SWE-agent relies on Bash-based interactions that are widely supported by coding-agent harnesses, the findings may carry over to other shell-based frameworks — "although direct validation remains necessary". The step and cost limits (300 interaction steps, $10 per instance) are stated as imposed conditions. The ethical section notes that the benchmark is built from public GitHub repositories and development histories, that artifacts were reviewed for personal identifiers, sensitive information and objectionable content, that licensing terms for all 165 repositories are documented in the release, and that evaluation incurs substantial computational and monetary cost.

**Assessed from the reporting.**

- **Single source, author-run baselines.** Everything rests on arXiv:2611.01484 v1 (1 November 2026). All five models were run by the authors under one scaffold; no independent replication is known. The comparison against the same model's 75.2% on DeepSWE v1.1 is a *reported* figure from another work, not a measurement in this paper.
- **The joint-vs-single-side contrast is the load-bearing experiment, and it covers two of five models.** +6.07 and +9.18 percentage points for GPT-6.1 Sol and DeepSeek V4.1 Flash; no single-side number is reported for Claude, GLM or Qwen, so the size of the coordination penalty is established for two models only.
- **Failure classification is manual and the denominator is unpublished.** The five failure categories and their per-model shares come from manual analysis of unsuccessful trajectories; the paper does not state how many failed runs were classified, so 44.2% cannot be turned into a count, and no inter-annotator agreement is reported.
- **Pass@1 with a single run per instance.** No repetitions, seeds, confidence intervals or significance tests are reported, and no indication of run-to-run variance across the 171 instances.
- **Cost comparisons are confounded by trajectory length.** Claude Sonnet 5.5 uses the fewest steps (29.2) and is the most expensive model per instance ($0.5217), while GPT-6.1 Sol is second on both (32.9 steps, $0.3496); per-token price, steps and total cost move together, so "cost-effective" is a statement about the whole configuration rather than about efficiency.
- **The $10 cost cap and 300-step cap can bind differently across models.** DeepSeek V4.1 Flash averages 152.7 steps and Qwen3.8-Flash-Next 182.1, far above the 32.9 and 29.2 of the closed-source pair, so a step-capped run is more likely to truncate the open-weight models' trajectories; the paper does not report how often the cap binds.
- **Selection of jointly necessary tasks is a filter, not a neutral sample.** By construction the suite over-represents changes where coordination is verifiable; its Pass@1 numbers are therefore not comparable with single-repository benchmarks, as the archived briefing noted.
- **The dataset is released; the paper links no separate harness repository.** The paper points only at a Hugging Face dataset. The dataset card fetched on 2026-11-10 documents per-instance evaluation entry points, container images pinned by digest and inspection/download scripts, and states that the 171 delivered environments carry recorded public-test, editable-source rebuild, image-audit and formal endpoint evidence — but the construction-time 2^N joint-necessity verification script and the failure-analysis tooling are not linked in the inspected text, so third parties must rebuild the necessity verification themselves to re-derive the suite.
- **Instance difficulty skews large.** 66.7% of instances change more than 200 lines and 56.1% modify more than ten files, which raises the bar for every model relative to ordinary repository repair.
- **Scaling is untested.** The one five-repository instance cannot support claims about coordination among large repository networks.

## Competing approaches

The paper's own related work separates two lines. **Repository-level SWE benchmarks** grow complexity inside a single repository: SWE-Bench established issue resolution against a reference patch or test suite; SWE-bench Pro targets longer-horizon tasks with substantial multi-file reasoning; SWE-Bench ProMax extends to expert-curated multilingual refactoring; FEA-Bench and FeatureBench construct tasks from real pull requests and complex multi-commit features. The paper's claim is that these leave cross-repository coordination unexplored. **Multi-repository SWE** work includes BeyondSWE (arXiv:2603.03194), which broadens resolution scope and knowledge scope to cross-repository reasoning, dependency-driven migration and full-repository generation, and DepBench (Yang et al., 2026; the cited entry is "DepRepair: llm-based source-code repair for dependency breaking changes", arXiv:2607.17957), which studies dependency breaking changes where upstream release notes and API changes are evidence for repairing a downstream consumer — in both cases the upstream repository is a source of evidence or context while the generated patch and executable validation remain confined to one repository. The paper's differentiation claim is that CrossSWE verifies the joint necessity of repository changes rather than merely requiring agents to *reason about* cross-repository dependencies. Methodologically it follows SWE-Bench ProMax's procedure for writing self-contained natural-language task specifications from source artefacts. The five evaluated models are themselves named with their own source papers in the references (OpenAI 2026, Anthropic 2026, DeepSeek-AI 2026, GLM 2026, Qwen Team 2026), and mini-SWE-agent is the scaffold.

Within this knowledge base, [[projects/weavebench]] is the nearest neighbour on evaluation design, and the "the agent is given the repositories, so it must find the change" framing distinguishes CrossSWE from benchmarks that test discovery — a [[concepts/protocol-relative-scores]] distinction rather than a difficulty ranking. It also belongs to [[benchmarks/index]] and to the cross-briefing layer recorded in [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The most transferable technique here is the **joint-necessity test**: enumerate the 2^N patch configurations of a multi-repository change and keep the task only if every partial configuration fails. It converts "this change spans repositories" into a verified property, and it is reusable wherever a claim of irreducibility is made — a data migration that "must" touch two services, a protocol change that "cannot" be done in one place. Without such a check, a benchmark of "multi-repo tasks" silently becomes a benchmark of tasks that mention two repositories.

Second, the derived single-side comparison is the experimental move worth copying. Holding the environment, the context and the scaffold fixed while removing only the requirement to modify the second repository isolates the coordination cost from the cost of *having* more context. The paper's numbers say that context is not the hard part — a model that can read both repositories does noticeably better when it is allowed to change only one. That has a direct consequence for how multi-repo tooling should be evaluated: coverage of the dependency graph is cheap, propagation of a change across it is the expensive capability.

Third, the failure taxonomy says something useful about where the remaining error lives. Incompatibility across repositories dominates every model, and it is a *consistency* problem rather than a *correctness* problem: the agent produces locally reasonable patches that do not jointly satisfy a shared contract. That points engineering effort at interface-level artifacts (shared schemas, contract tests, cross-repo conformance suites) rather than at per-repository code generation.

Fourth, the trajectory-length observation is a caution about efficiency claims. Interaction steps range from 29.2 (Claude Sonnet 5.5) to 182.1 (Qwen3.8-Flash-Next) — a spread of more than six times — while the difference in final lines changed is much smaller, so step count alone is a poor proxy for work done, and a benchmark that reports only Pass@1 hides a large cost spread between configurations that are otherwise comparable in outcome. Reporting cost next to the score is not a nicety here; the paper's own conclusion that different models occupy different points on the effectiveness–cost frontier depends on it.

Fifth, a caveat on generality: the joint-necessity filter makes the suite a curated sample of the hardest multi-repo changes. For anyone using it to compare models, that is a feature, but it means the absolute Pass@1 numbers carry no meaning outside the suite, and a model that "solves" CrossSWE has demonstrated exactly one thing — that it can coordinate edits across repos under verifiable joint necessity.

## Reproducible experiment

The instance dataset is released, so an independent check of the central claim is feasible without reimplementing the benchmark.

1. **Re-derive joint necessity on a sample.** Take 10–20 released instances and reproduce the 2^N verification: check out each repository at its base commit, apply each repository's gold patch in every combination, run the FAIL_TO_PASS tests, and confirm that all-base and every partial configuration fail while the fully patched configuration passes. A sample in which partial configurations pass would show that the necessity filter is weaker than claimed — the most consequential possible check, because the whole difficulty story rests on it.
2. **Joint versus single-side on your own models.** For each sampled two-repository instance, construct the single-side variant (one repository frozen at base) and run the same model, scaffold, step budget and cost cap on both. Report Pass@1 and average steps for both conditions. The paper's reference is +6.07 and +9.18 percentage points for GPT-6.1 Sol and DeepSeek V4.1 Flash on the full 165-instance derivation; a materially smaller gap would weaken the claim that coordination, not context, is the bottleneck.
3. **Categorise your own failures.** On the failed runs, apply the paper's five categories manually (cross-repository inconsistency, incomplete implementation, compatibility regression, logic/state errors, boundary handling) and report the per-model shares with the underlying counts. The paper's reference is cross-repository inconsistency at 44.2% for GPT and 29–41% for the others; if your failures cluster in incomplete implementation instead, the taxonomy is a property of the model population rather than of the task.
4. **A consistency-only metric.** Score every instance twice: once with the existing suite, once with a check that only verifies cross-repository interface agreement (schema and protocol compatibility) rather than task behaviour. If the two scores separate sharply, interface consistency is a distinct, cheaper-to-measure capability that could be used as an acceptance gate inside a team's own CI.

Model substitutions for the paper's 2026 hosted models are unavoidable; the substitution, scaffold version, and step and cost caps should be reported with the results.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2611.01484) and the complete HTML full text including appendices A–C and the reference list (https://arxiv.org/html/2611.01484v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; the five models were run by the authors under a single mini-SWE-agent scaffold; the paper is a single preprint (v1) with no peer-reviewed venue claimed. The dataset is publicly released at https://huggingface.co/datasets/CrossSWE/CrossSWE-Bench (dataset card fetched 2026-11-10: 171 rows, 350 repository entries across 165 distinct upstream repositories, container images pinned by immutable digest, per-instance evaluation contracts); a full-text search of the inspected paper HTML found no linked harness or evaluation-code repository beyond that dataset. The per-model failure percentages for Qwen3.8-Flash-Next, the absolute failure counts behind the classification, and the contents of Figures 5–7 are not disclosed in the inspected text and are not reported here. Claim types are separated in the text: the novelty and differentiation claims are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-04]] — dated full-fidelity research briefing; finding 5 selected CrossSWE.

## November 13 comparison update

[[projects/expertcrowd-swe]] (https://arxiv.org/abs/2611.13246) tests expert-authored merge blockers in individual codebases; CrossSWE tests cross-repository consistency (https://arxiv.org/abs/2611.01484). Scores are protocol-relative, not head-to-head. [[projects/geofaham]] (https://arxiv.org/abs/2611.04977) similarly coordinates artifacts across tools, but geospatial metadata correctness is not the same as repository interface consistency. Proposed experiment: paired repository changes with independent integration postconditions.
