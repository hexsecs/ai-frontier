---
uid: 2d0dfc8e-71df-42d3-bdd8-79d4f881f372
title: "ExploreRepair: Evidence-Specialized Agents for Vulnerability Repair under Information Constraints"
summary: "Three evidence-specialized agents repair vulnerabilities with no provided proof-of-vulnerability test — one builds its own — given only a function-level hint."
type: project
depth: deep
created: 2026-10-30
updated: 2026-11-02
sources:
  - url: https://arxiv.org/abs/2610.39899
    retrieved: 2026-11-02
  - url: https://arxiv.org/html/2610.39899v1
    retrieved: 2026-11-02
---

# ExploreRepair

## What it is

ExploreRepair is a multi-agent system for automated vulnerability repair (AVR) in the setting where the artifacts repair tools usually depend on — a vulnerability description or classification and a developer-written proof-of-vulnerability (PoV) test — are missing. It is presented in the arXiv preprint "ExploreRepair: Evidence-Specialized Agents for Vulnerability Repair under Information Constraints" (arXiv:2610.39899, cs.SE, submitted 29 October 2026; CC BY 4.0) by Duc Manh Tran, Ratnadira Widyasari, Ivana Clairine Irsan, Huihui Huang, Ting Zhang, David Lo, Rahul Gopinath, and Hong Jin Kang (University of Sydney, University of Victoria, Singapore Management University, and Monash University). The paper states no venue; as presented, it is a preprint.

The motivation is empirical: citing Householder et al. (2020), the authors note that only 4.1% of 75,807 CVEs had a public PoV within one year of disclosure — a method requiring a developer PoV cannot even start on most real vulnerabilities.

The formal setting is precise about what the system does and does not receive. Let C be the repository at its vulnerable revision and ℓ a function-level localization hint (one or more file/line ranges). Prior methods may also receive extra artifacts F — CWE labels, developer PoV tests, benchmark-oracle feedback. ExploreRepair receives **only (C, ℓ)**: it may inspect code and run the repository's test suites, has no access to F, and must output a single patch — ideal if it eliminates the vulnerability as judged by the benchmark's hidden PoV test while preserving functionality as judged by the unit tests. Two qualifications scope every claim on this page. First, the system is not localization-free: the hint ℓ is a substantial input. Second, "without a PoV" means without a *provided* PoV — one agent exists precisely to construct and execute its own PoV test, and success is still graded against the hidden benchmark PoV.

The problem is hard, the paper argues, because an agent without F must explore for evidence while avoiding premature commitment to a wrong repair hypothesis, and each evidence type it needs is incomplete alone. Structural evidence (the code graph around the localized function) does not show how inputs reach the code, and parallel repair sites may lie elsewhere. Semantic evidence (the API contract, intended behavior) must be reconstructed from code, comments, and tests. Executable evidence (a test demonstrating the vulnerable behavior) does not exist until someone builds it.

## Mechanism

ExploreRepair runs in two phases: exploration by three independent, evidence-specialized agents, then hierarchical aggregation. No agent or aggregator receives benchmark feedback at any point.

### Exploration: three evidence-specialized agents

All three agents use the same ReAct scaffold, run independently on the same vulnerable revision with the same (C, ℓ), at medium reasoning effort, with a 1,800-second limit per phase. Each can inspect files, run shell commands and repository tests, and edit production code beyond the localized function; each returns a trajectory and a candidate patch.

The **structural agent** works over a code knowledge graph built per vulnerability from the vulnerable revision: Tree-sitter ASTs give file and symbol nodes (functions, methods, classes) with qualified names and locations; call and import edges resolve to repository-local symbols and files; shared-commit edges link files changed in the same commit (up to the vulnerable revision only, weighted by co-change count). Node text is embedded with bge-large-en-v1.5 in a per-vulnerability vector store. Its tools are `search_code` (semantic retrieval, k = 5 by default) and `graph_neighbors` (default limit 20 per direction), and its prompt requires reading code via the shell before relying on retrieved content. It traces how external inputs reach the localized function, examines helpers and validators, compares sibling paths, and can conclude that a guard belongs in a shared helper or that a fix must cover another branch.

The **semantic (Intent) agent** reconstructs developer intent before repairing, answering four questions adapted from IntentFix: what specification or API contract governs the code; who can reach it and control its inputs; what resources it protects; and what constraints should hold for untrusted data. It seeks evidence in documentation, comments, tests, constants, error messages, and sibling-path conventions, and infers at most five security constraints on untrusted input — each naming values or operations, when it applies, and where it should be enforced — with file/line references, recording uncertainty where the repository establishes nothing. It then diagnoses where the implementation violates the constraints and patches.

The **executable (PoV) agent** constructs its own PoV test: it traces attacker-controlled input from a public API, CLI, or endpoint to the localized code; writes and executes a test against the vulnerable revision; revises it until the observed behavior demonstrates the suspected violation; then repairs the root cause and reruns the same test. It has no access to the developer-written benchmark PoV. Its prompt prohibits weakening the generated test or special-casing its input, and asks it to address every site sharing the weakness. Generated tests are saved in recognizable test paths so the harness can exclude them from the submitted production-code diff. Passing its own PoV supports the diagnosis but does not guarantee passing the hidden benchmark PoV.

### Aggregation: hierarchical, without benchmark feedback

Aggregation proceeds in three steps. First, **distillation**: a separate LLM call compresses each trajectory and candidate patch into a short, role-specific lesson — suspected vulnerability, supporting code locations or execution observations, proposed change, unresolved claims — since raw trajectories are long and oversized contexts degrade reasoning. Second, **separate synthesis**, in parallel: the Lesson Aggregator synthesizes a repair from the three lessons (the agents' observations and diagnoses), while the Patch Aggregator synthesizes one from the three candidate diffs (the concrete implementations, preserving details distillation may omit). Both may inspect the repository and are instructed to check the supplied attempts, since any may be incorrect. Third, **reconciliation**: each aggregator's trajectory is distilled into a lesson, and the final Aggregator receives the two lessons and two patches, checks their claims against the repository, and produces the final patch — adopting one repair, combining compatible changes, rejecting shared assumptions, or constructing a new patch.

## Evidence

All quantitative results here are **author-reported**: the ExploreRepair authors' own benchmark measurements, with no independent replication cited in the paper. Baseline scores are as measured — and, importantly, as adapted — by the ExploreRepair authors, not the baselines' published numbers; the adaptation caveats are detailed under Limitations.

### Setup

The authors evaluate with two models, OpenAI GPT-5.6-Luna and DeepSeek-V4.1-Flash, accessed through OpenRouter (names as reported by the authors), three runs at sampling temperature 1; repair counts varied by at most one across runs. Agents run in isolated, network-disabled Docker containers at the vulnerable commit; benchmark PoVs, reference patches, and grading scripts are removed, repository tests remain available, and agents never see evaluation code or results. Hardware: Ubuntu 22.04.5, AMD EPYC 7763, 251 GB RAM.

Two benchmarks are used. **PatchEval** (Wei et al. 2025) contains 230 CVEs across Python, JavaScript, and Go with runnable test artifacts and prebuilt Docker images. Of the 176 instances having both a PoV and a unit-test suite, 7 are excluded because their benchmark test patches do not compile against the vulnerable repository, leaving **N = 169** evaluated (64 Python, 49 JavaScript, 56 Go). The most common CWEs are path traversal (CWE-22, 27), code injection (CWE-94, 26), external file path control (CWE-73, 25), command injection (CWE-77, 24), and OS command injection (CWE-78, 23), with 27 further types grouped as "Other". **VulnLoc+** (Ye et al. 2026, the LoopRepair benchmark) contributes **N = 35 of 40** vulnerabilities, excluding ones whose PoV tests already pass on the vulnerable version; C/C++ across 9 projects, dominated by buffer overflows (23), with integer overflow (3), divide by zero (3), null-pointer dereference (2), data-type overflow (2), and use after free (2).

Metrics: on PatchEval a patch is *plausible* if it passes the benchmark PoV test and *successful* if it also passes the repository's unit tests. RSR (repair success rate) is S/N × 100 for S successful of N evaluated; OFR (overfitting rate) is (P − S)/N × 100, the fraction of all evaluated CVEs whose patch passes the PoV but fails unit tests. On VulnLoc+, RSR is measured with the benchmark PoV alone and OFR is not reported, there being no unit tests.

### PatchEval results (N = 169)

RSR in percent, with OFR in parentheses; all figures author-reported.

| Approach | GPT-5.6-Luna | DeepSeek-V4.1-Flash |
|---|---|---|
| IntentFix | 4.7 (1.2) | 9.5 (1.2) |
| EvoRepair (adapted: no ground-truth PoV, no benchmark feedback) | 23.7 (3.0) | 46.2 (1.8) |
| LLM (single response, no tools) | 10.7 (1.2) | 23.7 (2.4) |
| Multi-Agent (generic subagent delegation) | 30.2 (1.2) | 55.6 (1.2) |
| Single Agent (ReAct + shell) | 32.5 (0.6) | 57.4 (0.6) |
| Codex (general-purpose coding agent) | 34.3 (0.6) | 43.8 (0.6) |
| Structural (Graph) agent alone | 36.1 (1.2) | 55.6 (0.0) |
| Semantic (Intent) agent alone | 29.6 (0.0) | 59.8 (0.0) |
| Executable (PoV) agent alone | 33.7 (0.0) | 58.0 (0.6) |
| 3-in-1 Agent (all three mechanisms in one agent) | 30.8 (1.2) | 53.3 (0.6) |
| **ExploreRepair (full)** | **39.6 (0.0)** | **71.6 (0.6)** |

The authors' derived comparisons (all author-reported): against the adapted EvoRepair, ExploreRepair gains +16.0 points of RSR with GPT-5.6-Luna and +25.4 with DeepSeek-V4.1-Flash, with OFR of 0.0%/0.6% against EvoRepair's 3.0%/1.8%. Against the Single Agent it gains +7.1 and +14.2 points; against IntentFix, +34.9 and +62.1; against the 3-in-1 Agent — all three mechanisms combined in one trajectory — +8.9 and +18.3, which the authors read as evidence that independent exploration plus aggregation beats mechanism-stacking in one agent. Against Codex (same hint and repository, external capabilities disabled, medium reasoning effort): 39.6% versus 34.3% (+5.3, Luna) and 71.6% versus 43.8% (+27.8, DeepSeek). No single explorer is best on both models: the Graph agent leads with Luna (36.1%), the Intent agent with DeepSeek (59.8%).

The aggregation ablation locates where the gains come from. The Lesson Aggregator alone reaches 39.1% (OFR 0.6) with Luna and 63.9% (0.6) with DeepSeek; the Patch Aggregator alone, 37.3% (1.2) and 69.2% (1.2); handing one agent both lessons and patches directly, 37.3% (0.6) and 67.5% (0.6) — never beating the stronger separate aggregator. The full system's final Aggregator adds only +0.6 points (one extra vulnerability, Luna) and +2.4 points (four extra, DeepSeek) over the stronger intermediate aggregator, which itself flips by model (Lesson for Luna, Patch for DeepSeek). Most aggregation value is in the separate syntheses, not the final reconciliation.

The overlap analysis reinforces the division-of-labour story. With Luna the explorers' union covers 40.8% of the 169 instances, 4.7 points beyond the strongest single agent, with unique-to-one-agent repairs of 5.3% (Graph), 0.6% (Intent), and 3.0% (PoV). With DeepSeek the union covers 72.2% against the strongest agent's 59.8%, with unique contributions of 2.4%, 7.7%, and 4.7%. Most strikingly, the authors report that ExploreRepair repairs 11 vulnerabilities with DeepSeek and 3 with Luna that **none** of the three exploration agents repaired individually — repairs created by aggregation, not merely selected by it.

### VulnLoc+ results (N = 35)

RSR in percent, measured by the benchmark PoV alone; author-reported. Because VulnLoc+ has no unit tests, these scores carry no functionality or overfitting check (see Limitations).

| Approach | GPT-5.6-Luna | DeepSeek-V4.1-Flash |
|---|---|---|
| LoopRepair + PoV (ground-truth PoV given) | 48.6 | 51.4 |
| LoopRepair (no-PoV variant, authors' construction) | 31.4 | 45.7 |
| Single Agent | 48.6 | 57.1 |
| **ExploreRepair (no PoV)** | **51.4** | **62.9** |

Against the authors' no-PoV LoopRepair variant, ExploreRepair gains +20.0 points (Luna) and +17.1 (DeepSeek). Against LoopRepair *given* the ground-truth PoV it still scores higher, by +2.9 and +11.4 points — the narrower, fairer comparison, since the no-PoV comparator is a deliberately minimal configuration (see Limitations).

## Limitations

**Baselines were adapted and weakened by the authors, not run as published.** This is the most important caveat on every comparison above. EvoRepair — the principal PatchEval comparator and the source of the +16.0/+25.4-point headline — is designed to be guided by a ground-truth PoV and benchmark-oracle feedback; here it receives neither, **and** its refinement loop is cut from the original 15 turns to up to 3. The LoopRepair "no-PoV" comparator on VulnLoc+ is a variant the authors constructed for this paper: PoV-based localization is replaced by the given crash location, and the **first generated patch that compiles** is selected, with no PoV validation and no iterative refinement. The +20.0/+17.1-point VulnLoc+ headline is thus against a minimal configuration of a system designed around PoVs; comparison against LoopRepair with its PoV intact narrows the margin to +2.9/+11.4 points. The authors concede in their own Limitations that this "transforms the setting for which the baseline approaches were designed," though original code was preserved where possible. IntentFix's very low scores (4.7%/9.5%) carry a further asterisk: the authors found an evaluation flaw in IntentFix's replication package, confirmed by IntentFix's authors.

**VulnLoc+ success is PoV-only.** With no unit tests in that benchmark, RSR means only that the patch passes the benchmark PoV; functionality preservation and overfitting are unmeasured and OFR cannot be computed. The 51.4%/62.9% figures are therefore weaker evidence than the PatchEval numbers, where success also requires passing unit tests.

**The "without PoV" framing is scoped.** The system still receives a function-level localization hint — a substantial input that removes the localization problem entirely — and one agent constructs and executes its own PoV test; success on PatchEval is still defined by the hidden benchmark PoV plus unit tests. What is absent is a *provided* PoV, CWE label, and oracle feedback, not PoV-style evidence altogether.

**The evaluation sets are small and filtered.** PatchEval contributes 169 of 230 CVEs after requiring both a PoV and a unit-test suite and dropping 7 non-compiling cases; VulnLoc+ contributes 35 of 40 after excluding items whose PoV already passes. The exclusions shape the denominators, and no confidence intervals or significance tests are reported; margins of a few points (+2.9 on VulnLoc+ with Luna; the final Aggregator's +0.6) rest on one to a handful of instances.

**Cost is unreported.** A full run executes three explorers, two intermediate aggregators, a final aggregator, and multiple distillation calls per vulnerability, each phase allowed up to 1,800 seconds, with no token, dollar, or wall-clock comparison against the single-agent baselines — the accuracy-per-cost trade-off cannot be assessed from the paper.

**Aggregation can destroy correct repairs when errors correlate.** In the paper's Appendix C.2 case (CVE-2021-39163, Synapse), the Graph agent alone produced a passing repair, but both intermediate aggregators adopted the same incorrect group-membership authorization assumption and the final Aggregator followed them, discarding the correct fix. Hierarchical reconciliation is not a correctness guarantee; it amplifies shared misinterpretations.

**Results are model-dependent.** Only two models were evaluated, both via OpenRouter under the names the authors report; the strongest explorer and the stronger intermediate aggregator both flip between them, so component rankings are not stable across models. The authors state that results "are likely to vary with other models, prompts, or sampling seeds"; their mitigation is three runs at temperature 1 with repair counts varying by at most one. Pretraining exposure of the models to these public CVEs and fixes is not addressed; container hygiene controls in-run leakage but says nothing about training-data familiarity. The authors also flag the ethical risk that an incorrect patch may give developers unwarranted confidence, and that repair research can reveal exploitable behavior.

## Competing approaches

ExploreRepair positions itself against several lines of prior work, all as characterized by its authors. **EvoRepair** (Hu et al. 2026) retrieves experiences from prior repair trajectories, guided by ground-truth PoV tests and oracle feedback; it is the principal PatchEval comparator, run here in adapted form (see Limitations). **IntentFix** (Heo et al. 2026) infers developer intent to generate and refine patches; it is both a baseline and the source of the Intent agent's four questions. **LoopRepair** (Ye et al. 2026) performs C/C++ repair requiring a PoV, using its execution and taint traces to rank and refine patches; it originates the VulnLoc+ benchmark and runs in both PoV-assisted and authors-constructed no-PoV forms. **ContraFix** (Liu et al. 2026), which mutates the PoV to contrast runtime behavior, is cited as state of the art but excluded from evaluation because it requires a PoV test. **KeaRepair** (Cao et al. 2026) and **AgenticRepair** (Fu et al. 2026) — verified program facts plus historical-fix knowledge, and multi-agent context examination — are discussed but not evaluated (no public replication packages at evaluation time); the paper's stated distinction from AgenticRepair-style exploration is that prior systems "do not prevent premature commitment to an incorrect repair." **APPATCH** (Nong et al. 2025) was attempted, but the authors could not run its released implementation. Training-based AVR (SeCuRepair/SecurePair, VulMaster, VulKey) is excluded by design — ExploreRepair is inference-time; those systems learn from reference fixes — and program-analysis AVR (SAVER and successors) is set aside as typically needing language-specific analyses or a flaw demonstration. Among generic multi-agent and memory systems, the paper contrasts role-specialized frameworks (MetaGPT, ChatDev, CodeAgent), organized around discussion of a shared task, with its own independent per-evidence-type exploration; cites Reflexion, ReasoningBank, and workflow-memory work as precedents for lesson distillation; and cites evidence that multi-agent setups do not automatically improve diversity or correctness and that an incorrect initial analysis can mislead other agents — its stated reason for keeping explorers independent.

## Implications

Read as agent engineering, the paper supports several design claims, each tied to its own measurements. **Specialize by evidence type, not by subtask chatter.** The generic Multi-Agent baseline (30.2%/55.6%) underperforms even a lone Single Agent (32.5%/57.4%), while three independent evidence-specialized explorers plus aggregation top the table; what mattered was what each agent is responsible for *knowing*, not how much the agents talk. **Independence before aggregation.** The explorers never see each other's work, and the overlap analysis shows each role uniquely repairs items the others miss; independence is the stated defense against one wrong early analysis anchoring the rest. **Aggregate diagnoses and artifacts separately.** Lessons (why) and patches (how) carry different information; synthesizing each separately and reconciling last beat handing everything to one agent — though the final reconciliation's marginal gain is small (+0.6/+2.4 points over the better intermediate aggregator), so most of the value sits in the separate syntheses. **Distill trajectories before reuse.** Compressing long trajectories into short role-typed lessons — suspected flaw, evidence, proposed change, open claims — makes multi-agent output consumable without exhausting the context budget. **Manufacture your own executable evidence.** When the needed oracle or test does not exist, an agent that writes and runs its own PoV converts an unverifiable diagnosis into checkable evidence, with guardrails (no weakening the test, no input-specific fixes) doing real work. **Portfolios beat picking a winner.** Which explorer and which intermediate aggregator is strongest flips with the model, so running the diverse set and reconciling is more robust than selecting the best component on one model. **Correlated error is the residual risk.** When both intermediate syntheses share a wrong assumption, the final stage ratifies it and can discard a correct candidate; diversity must be maintained through the aggregation layers, not only at exploration.

## Reproducible experiment

The paper states that its replication package contains the repair infrastructure and public benchmark outputs (excluding credentials and previously undisclosed vulnerabilities), so a partial reproduction is feasible:

1. Take PatchEval's Docker images; select instances with both a PoV and a unit-test suite; drop instances whose benchmark test patches do not compile (expect approximately 169).
2. For each instance, run a network-disabled container at the vulnerable commit; delete benchmark PoVs, reference patches, and grading scripts; keep repository tests; supply only the function-level localization hint.
3. Implement the three ReAct explorers (medium reasoning effort, 1,800-second limit per phase): the Graph agent over a Tree-sitter-built code knowledge graph (call, import, shared-commit edges) embedded with bge-large-en-v1.5, exposing `search_code` (k = 5) and `graph_neighbors`; the Intent agent prompted with the four intent questions and an at-most-five-constraint output; the PoV agent prompted to build and execute its own PoV under the anti-weakening constraints.
4. Run the three-step aggregation — lesson distillation, parallel Lesson and Patch Aggregators, final Aggregator — with the same base model (GPT-5.6-Luna or DeepSeek-V4.1-Flash via OpenRouter), temperature 1, three runs.
5. Score externally: plausible means the hidden benchmark PoV passes; successful means PoV plus unit tests pass; report RSR and OFR with the run-to-run spread (the authors observed repair-count variation of at most one).
6. Reproduce the controls on identical budgets: the Single Agent, the 3-in-1 Agent, and the aggregation ablations, since those isolate the architecture's contribution from the base model's.

Fidelity caveat: exact prompts are not reproduced in the paper text (agent guidance is described functionally), so a from-scratch reimplementation would approximate, not replicate, the authors' prompts unless the replication package supplies them.

## Evidence status

Every quantitative result on this page is **author-reported**: the ExploreRepair authors' own benchmark measurements under the conditions documented above, including the adapted-baseline caveats under Limitations. The paper cites no independent replication of its results, and none of the headline numbers are vendor claims. Baseline scores (EvoRepair, IntentFix, LoopRepair, Codex) are as measured and adapted by the ExploreRepair authors, not those systems' published numbers. The 4.1%-of-CVEs statistic is a cited third-party result (Householder et al. 2020), reported rather than measured by the authors. This page is based on a full reading of the paper's arXiv HTML full text (v1), including tables, Limitations, and appendices; no part of the system was run or independently reproduced for this page.

## Historical coverage

[Briefing 2026-10-30](../briefings/2026/10/2026-10-30.md)
