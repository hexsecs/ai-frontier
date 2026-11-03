---
uid: a408a95a-700b-4c86-bda0-66e818182da1
depth: deep
title: "Compile Away Uncertainty: Self-Evolving Agent Skills via Programmatic Compilation"
summary: "Self-evolving skill framework that selectively compiles well-specified skill operations into validated, reusable programs while LLM reasoning handles the rest."
type: project
created: 2026-10-31
updated: 2026-11-02
related: [information-content-dominance, scoped-assurance]
sources:
  - url: https://arxiv.org/abs/2610.39508
    retrieved: 2026-11-02
---

# SkillCompiler

## What it is

SkillCompiler is a self-evolving agent-skill framework from Chengyu Yang, Yunxiang Zheng, Zongzheng Li, and colleagues at East China Normal University and China University of Geoscience, reported in the arXiv preprint "Compile Away Uncertainty: Self-Evolving Agent Skills via Programmatic Compilation" (arXiv:2610.39508, submitted 29 October 2026; no peer-reviewed venue is claimed). It addresses a weakness of text-based agent skills: a skill stored as natural language must be re-interpreted by the model on every execution, so the same unchanged procedure can follow different reasoning paths and produce different outcomes across runs — what the authors call **execution uncertainty**. A second problem is **repeated capability construction**: executable procedures discovered during skill evolution are rebuilt for each skill or task instead of being kept for reuse.

The framework's answer operates at the level of individual operations, not whole skills. During skill evolution, a Task Analyzer decomposes a skill into fine-grained operations; operations that meet explicit executability criteria are turned into validated, deterministic programs, while operations involving unresolved inputs, context-dependent decisions, or open-ended semantic reasoning remain as LLM reasoning steps inside a hybrid Skill Skeleton. Validated programs are stored in a persistent **Program Asset Bank** and retrieved for reuse across skills. A trace-driven revision loop then improves skills locally, at operation level, from execution evidence. Model parameters are never updated: all learning happens in the skill and program-bank state. The authors claim — as an author claim, "to the best of our knowledge" — that SkillCompiler is the first self-evolving skill framework to combine operation-level selective compilation with persistent reuse of the compiled program assets.

## Mechanism

SkillCompiler has five components — Task Analyzer, Programmer, Executor, Skill Optimizer, and Program Asset Manager — and runs three phases: executability-aware compilation, program asset reuse, and skill optimization.

**Operation decomposition.** The Task Analyzer breaks a task and its relevant skill knowledge into operations, each expressed as an *operation contract* κ_i = ⟨I_i, O_i, pre_i, post_i, check_i, g_i⟩: required inputs, expected outputs, observable preconditions, expected local effects (postconditions), a check defining how those effects are verified, and reusable execution guidance. Task-specific entities and values are bound only at invocation time, so the same operation definition can serve across tasks.

**Executability analysis.** An operation is judged *programmatic* only when all of the following hold: its inputs and outputs can be explicitly represented; its execution procedure can be clearly specified; its preconditions can be observed from the current environment; its outputs and local effects can be independently verified; and available tool interfaces support a bounded implementation. Any operation failing a criterion stays *agent-guided* — executed by LLM reasoning. This per-operation decision is made before the skill is assembled, and it is the paper's central design move: compilation is selective by construction, never a whole-skill translation.

**Hybrid Skill Skeleton.** Operations are organized into a Skill Skeleton S_x = ⟨O_x, σ_x, E_x, β_x⟩: the operation occurrences for the task, their execution order, data and prerequisite relations between them, and current argument bindings. Programmatic and agent-guided operations coexist in the same skeleton; inputs unavailable at construction time remain unresolved in β_x and are instantiated from observations during execution.

**Programming and validation.** For each programmatic operation, the Programmer first queries the Program Asset Manager for an existing compatible implementation; only if none qualifies does it synthesize a new program from the operation contract, permitted tool interfaces, and execution evidence. Before use, the program is validated in an isolated environment: it must execute successfully, its inputs and outputs must conform to the contract's I_i/O_i, and its local effects must satisfy post_i as judged by check_i. Validation replays the source task and action prefix in a separate reset environment instance, checks required inputs against the declared schema (hidden answer fields and task-identity lookup tables are explicitly not program inputs), and compares file effects while retaining the original artifact hash. On failure, errors and check discrepancies return to the Programmer for repair; the loop continues until a qualified implementation exists or the operation reverts to agent-guided. Only validated programs enter the skeleton. The paper is careful about what this establishes: the tests are "evidence of local behavior, not exhaustive branch coverage or semantic equivalence on arbitrary inputs."

**Program Asset Bank.** Validated programs persist in the bank. Retrieval is compatibility-first, lexical-second: candidates are filtered by capability and contract compatibility, then ranked lexically — Skill Skeletons by lexical similarity, atomic skills by R(a,o) = 2|T(o) ∩ T(a)| / (|T(o)| + |T(a)|) + 0.1·u(a) + 0.05·1[active(a)], combining a Dice overlap term with historical utility and an active-status bonus. No embedding-based retrieval is used. A retrieved program may be reused only if arguments bind, preconditions hold, the environment provides the required interfaces, and its validation record still applies (Bind ∧ Pre ∧ Env ∧ Cert); automatic invocation requires a unique eligible or preferred implementation, otherwise the choice stays agent-guided. Operations, program realizations, and skeletons are versioned separately, and any change to an implementation, behavioral contract, or supported conditions requires revalidation of the affected realization before admission — a failed realization does not invalidate the operation definition.

**Skill optimization.** The Executor runs a candidate skill — invoking programs for programmatic operations, delegating the rest to the target agent — and records traces: actions, observations, argument bindings, program invocations, local check results, and task feedback. On failure, the Skill Optimizer revises *locally at operation level* rather than regenerating the skill: an operation that produced its expected output and satisfied its check is retained even when the task failed; an unsatisfied or overly broad invocation condition updates pre_i; wrong information passed between operations updates bindings and dependencies; incomplete guidance updates g_i; a program missing its postcondition effect goes back for repair and revalidation. Revised operations are compared against the skill bank and merged when they share capability semantics with compatible contracts under a parameter alignment; otherwise they stay separate. Candidate skill and bank states are selected on validation-set performance and frozen before test evaluation; test outcomes are used for reporting only, temporary programs synthesized during a test task are not added to the persistent bank, and no model parameters change at any point.

## Evidence

All results in this section are **author-reported** from the single preprint; none has been independently replicated.

**Setup.** Five benchmarks — SearchQA (open-domain QA), OfficeQA and DocVQA (document understanding), LiveMath (mathematical reasoning), and ALFWorld (long-horizon interactive tasks) — with train/validation/test partitions of 300/24/1,400, 120/24/102, 180/22/201, 60/17/100, and 120/24/134 respectively. Six model families: MiniMax-M3, Gemini-3.8-Flash, Qwen3.8-Flash, DeepSeek-V4.1-Flash, Kimi-K2.6, and GLM-5.3-Flash. Seven baselines: No Skill, Human Skill (fixed human-written skills released by the SkillOpt authors), Trace2Skill, EvoSkill, EmbodiSkill, GEPA, and SkillOpt. All methods share task partitions, tools, evaluators, and inference settings within each configuration; main results average three learning seeds (42, 43, 44), with learned states selected on validation and frozen for testing. Scores are exact match (%) on the four QA/reasoning benchmarks and success rate (SR) on ALFWorld; differences between percentage scores are reported here in points.

**Main results.** SkillCompiler is the top method for every one of the six model families on the four-benchmark average, outperforming each model's strongest baseline by **6.02–11.90 points**, while its own averages span only 79.78–84.63 — a 4.85-point spread across very different backbones:

| Model | SkillCompiler avg | Strongest baseline (avg) | Margin (points) |
|---|---|---|---|
| MiniMax-M3 | 79.78 | SkillOpt (71.68) | +8.10 |
| Gemini-3.8-Flash | 84.63 | GEPA (78.61) | +6.02 |
| Qwen3.8-Flash | 83.40 | EvoSkill (74.63) | +8.77 |
| DeepSeek-V4.1-Flash | 81.58 | GEPA (72.93) | +8.65 |
| Kimi-K2.6 | 83.13 | SkillOpt (71.23) | +11.90 |
| GLM-5.3-Flash | 82.16 | Trace2Skill (72.16) | +10.00 |

The gains are not uniform: they concentrate on LiveMath and OfficeQA, while SearchQA and DocVQA improvements are small (for Kimi-K2.6, +1.52 points on SearchQA and +0.50 on DocVQA against each benchmark's strongest baseline). The paper's advertised "up to 32.33%" improvement is the single largest cell — GLM-5.3-Flash on LiveMath, 77.00 vs 44.67 for the strongest baseline there — not a typical effect (see Limitations).

**ALFWorld.** On the long-horizon benchmark (DeepSeek-V4.1-Flash only, 134 test tasks), SkillCompiler reaches **98.26% SR vs 93.53%** for the best baseline (EmbodiSkill, +4.73 points), and +18.66 points over No Skill (79.60%). SkillOpt and GEPA score 88.06% and 86.82%.

**Execution uncertainty.** Reliability was measured with frozen seed-42 skill states, each test task executed three times under identical inputs and conditions; EIR@3 is the fraction of tasks with both successful and failed outcomes across the three repetitions. On LiveMath (Gemini-3.8-Flash), SkillCompiler cuts **EIR from 32.00% (SkillOpt) to 11.00%** — a 65.6% relative reduction — while raising EM to 78.67 vs SkillOpt's 64.67 in this repeated-execution protocol (distinct from the 78.00 main-protocol average above). On ALFWorld it records the lowest EIR (3.0%) with path-consistency scores APS 81.3%, success-conditioned APS 82.5%, and exact-path repetition 44.8%.

**Cost.** On LiveMath, SkillCompiler uses 2.695M learning tokens — 41.9% below SkillOpt (4.639M) and 52.1% below GEPA (5.631M) — and 0.450 model calls per test task, the lowest of any method (below 1 because a task executed entirely by programs makes no model requests). On ALFWorld, learning tokens (32.442M) are below SkillOpt (57.468M) and GEPA (52.970M), and inference tokens per task are 7.6% below SkillOpt's. The efficiency picture is mixed, however; see Limitations.

**Program execution and reuse (descriptive statistics, ALFWorld, mean over seeds 42–44).** Persistent Program Coverage is 100.00% — every test task invoked at least one banked program. Confirmed downstream consumption of program outputs (CPO, a trace-confirmed lower bound) is ≥48.36%; Program Invocation Success is 88.84%; programs account for 87.06% of canonical environment actions. Cross-Skill Reuse (CSR) is 54.85% — but on per-seed denominators of only 10–14 programs (6/11, 7/14, 6/10).

**Ablation — the load-bearing evidence.** On ALFWorld (DeepSeek-V4.1-Flash; each condition relearns from an empty bank with seed 42; intervention active in learning and testing):

| Condition | SR % | Test tokens (k/task) | EIR@3 % |
|---|---|---|---|
| Full SkillCompiler | 98.26 | 41.954 | 2.99 |
| w/o Skill Skeleton | 95.52 | 115.424 | 8.21 |
| w/o Programmer | 53.48 | 308.887 | 19.40 |
| w/o Skill Optimization | 95.52 | 103.858 | 4.48 |

Removing the **Programmer** — no program synthesis, qualification, or invocation, including no reuse of stored programs — collapses success from **98.26% to 53.48%** at **7.36×** the token cost. Removing the Skill Skeleton or Skill Optimization costs only **~2.7 points** each (95.52%), though both roughly double-to-triple token use and raise EIR. The ablation therefore attributes the headline effect primarily to executing validated programs in place of repeated LLM reasoning, with the skeleton structure and the revision loop contributing smaller, mostly efficiency- and stability-related gains.

## Limitations

**Stated by the authors.** Compilation reduces rather than eliminates uncertainty: the method relies on identifiable operation boundaries, observable preconditions, and independently checkable effects, and ambiguous or context-dependent decisions remain under LLM control. Local validation establishes correctness only under the tested inputs and environment states, without guaranteeing generalization to unseen conditions. Reuse benefits depend on contract compatibility and on enough reuse to amortize synthesis and validation costs. The evaluation covers controlled benchmark environments; effectiveness on broader task ranges and in dynamic web environments is untested.

**Assessed from the reporting.**

- **Single source, no artifacts.** Everything rests on one arXiv preprint (v1, October 2026). The paper contains no code or data URL — verified by full-text search — so no third party can rerun the authors' configurations, and no result has been independently replicated. The six backbones are 2026-era hosted models, which further limits exact reproduction.
- **The headline number is a best cell.** "Up to 32.33% improvement" is one model–benchmark cell (GLM-5.3-Flash on LiveMath), expressed in percentage points. Typical effects are the 6.02–11.90-point per-model average margins, and some cells are near-ties (DocVQA +0.50 for Kimi-K2.6).
- **Gains concentrate where test sets are smallest.** LiveMath (100 test tasks), OfficeQA (102), and ALFWorld (134) carry the largest improvements. No confidence intervals or significance results accompany the headline tables; the appendix describes bootstrap/McNemar machinery but states that no significance designation is inferred from the reported aggregate means.
- **Baselines are author-run.** The compared methods — mostly 2026 preprints themselves — were executed under the authors' harness and partitions rather than quoted from their original papers, so baseline quality rests on the authors' implementations. The appendix also discloses that development included inspection of held-out failure cases, a mild test-set-adjacent tuning caveat (frozen-bank rules did prohibit persistent updates from test outcomes).
- **The reuse contribution has no ablation.** There is no compile-always-fresh vs bank-reuse comparison. The claim that persistent program assets matter rests only on descriptive statistics: CSR of 54.85% computed on per-seed denominators of 10–14 programs, and CPO ≥48.36%. Retrieval is purely lexical (Dice overlap plus utility/active bonuses), so reuse quality depends on naming and description overlap between operations.
- **Validated is not the same as reliable at run time.** Program Invocation Success is 88.84% — roughly one in nine invocations of a validated program still fails — and confirmed consumption of program outputs (≥48.36%) is far below invocation coverage (100%).
- **Reliability evidence is narrow.** EIR and path metrics cover only two of the five benchmarks, one model each, one frozen bank (seed 42), with K=3 repetitions.
- **Efficiency is mixed.** On LiveMath, SkillCompiler's per-task inference tokens (13.984k) are about 2.1× SkillOpt's (6.672k); on ALFWorld its calls per task (14.868) are not the lowest (SkillOpt 14.674, Trace2Skill 14.085). The clean efficiency wins are learning-token cost and LiveMath call count.

## Competing approaches

The seven compared baselines define the immediate field. **SkillOpt** — the strongest recurring baseline — improves natural-language skills through validation-guided, bounded textual revision; skills remain text interpreted at run time. **GEPA** evolves prompts reflectively with Pareto selection. **Trace2Skill** distills trajectories into transferable skills, **EvoSkill** generates and refines skills from failure analysis, and **EmbodiSkill** uses skill-aware reflection that separates skill deficiencies from execution failures; **Human Skill** (the fixed skills released by the SkillOpt authors) and **No Skill** anchor the comparison.

In related work, the paper positions itself against experience-accumulation systems (Reflexion, ExpeL, Agent Workflow Memory, and Voyager — whose Minecraft skill library of executable code is the closest well-known precedent for stored programmatic skills) and against executable-representation approaches including FlowEvo, AutoTools, NSI (neuro-symbolic programmatic skill induction), SkillDisCo ("Distilling and Compiling Agent Traces into Reusable Procedural Skills"), and Agent Skill Induction. The authors' differentiation claim is that prior work attaches reusable workflows, tools, or executable artifacts to skill execution, whereas SkillCompiler analyzes executability at operation level *inside* the evolving skill and persists the resulting programs as reusable assets — an author claim, not an independently established distinction.

## Implications

For agent engineering, the paper's most transferable idea is executability analysis as an explicit design step: deciding, per operation and against stated criteria, whether a procedure is stable enough to become code — and gating that promotion with isolated validation against a declared contract — rather than treating "prompt vs program" as a whole-skill choice. The ablation asymmetry is instructive: on the authors' evidence, most of the gain comes from not re-deriving settled procedures through stochastic reasoning, while orchestration structure (the skeleton) and the revision loop add comparatively little accuracy, though they matter for cost and stability. Execution instability (EIR) is a metric worth borrowing: a skill system can post strong average scores while being unreliable run-to-run, and SkillCompiler's EIR reductions are as significant as its score gains.

The persistent asset bank is the least-proven part of the design. Its reuse statistics are descriptive, its denominators are small, and no ablation isolates its contribution; teams adopting the pattern should treat cross-skill program reuse as a hypothesis to instrument, not a demonstrated win. Finally, the ~11% failure rate among *validated* program invocations is a useful calibration point for anyone replacing reasoning with generated code: validation against a source task licenses the substitution, but runtime fallback to agent-guided execution remains necessary — a path the architecture itself retains.

## Reproducible experiment

No artifact release exists, so reproduction means reimplementation from the method section and appendices B–C, which do specify the protocol in usable detail (operation contracts, validation procedure, selection-on-validation with frozen test state, seeds 42–44, benchmark partitions). A feasible independent check of the core claims:

1. **Ablation-first replication on ALFWorld.** Implement the minimal pipeline — operation decomposition with contracts, a Programmer with isolated validation, hybrid skeleton execution — with an available backbone model, and run the paper's decisive comparison rather than the full benchmark suite: full system vs no-Programmer vs no-Skeleton, each relearned from an empty bank, on the 134-task test split. The paper predicts a ~45-point SR collapse without the Programmer and ~3-point costs for the other removals; even a directional match or mismatch would be informative.
2. **Instability measurement.** Freeze the learned skill state and execute each test task three times under identical inputs, reporting EIR@3 alongside mean success for both the compiled system and a text-skill baseline (e.g., a SkillOpt-style skill). This tests the paper's central reliability claim, not just its accuracy claim.
3. **The missing reuse ablation.** Add a compile-always-fresh condition — synthesis and validation permitted, bank persistence disabled — and compare success, total synthesis cost, and cost amortization across the task stream. This directly tests the contribution the paper asserts but does not isolate.
4. **Determinism spot-check.** For a sample of compiled operations, run each program repeatedly on its validation inputs and confirm byte-identical outputs and effects, contrasting with repeated LLM execution of the equivalent text procedure.

Substituting an available model for the paper's 2026 hosted backbones is unavoidable; the substitution and any partition differences should be reported with the results.

## Evidence status

This page is grounded in a full read of the primary source (arXiv:2610.39508 v1, including appendices) on 2026-11-02 for issue #2. Every quantitative result is **author-reported**; the paper links no code or data release (verified by full-text search), the baselines were run by the authors, and no independent replication is known. Claim types are separated in the text: the first-of-its-kind and differentiation claims are the authors'; the limitations marked as assessed are analysis of the paper's own reporting. Nothing here was reproduced or executed by the KB maintainers.

## Historical coverage

[Briefing 2026-10-31](../briefings/2026/10/2026-10-31.md)
