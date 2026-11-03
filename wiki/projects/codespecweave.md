---
uid: 958fdf8c-5bcd-44bb-a49f-be56f32c169e
depth: deep
title: "When Requirements Interact: Scaling Long-Horizon Coding via Interdependent Specifications"
summary: "Synthetic coding tasks with interdependent requirements, grounded in real-repo seeds; 73.9% of pilot candidates had flawed tests."
type: project
created: 2026-10-30
updated: 2026-11-02
related: [ground-truth-fallibility, comparator-construction-shapes-margins]
sources:
  - url: https://arxiv.org/abs/2610.40256
    retrieved: 2026-11-02
  - url: https://arxiv.org/html/2610.40256v1
    retrieved: 2026-11-02
---

# CodeSpecWeave

## What it is

CodeSpecWeave is a framework for synthesizing long-horizon coding tasks whose
requirements are *interdependent*: coupled so that satisfying one specification
constrains how the others can be satisfied, forcing a solver to reason about
requirements jointly rather than resolve them one at a time. It is described in
the preprint "When Requirements Interact: Scaling Long-Horizon Coding via
Interdependent Specifications" by Yishuo Cai, Minzheng Wang, Liang Zhao,
Linghao Zhang, Lei Li, Shicheng Li, Xu Sun, and Fuli Luo (arXiv:2610.40256,
cs.SE, v1, submitted 29 Oct 2026; the arXiv listing gives no venue or journal
reference, so it is a preprint as far as the listing shows). The framework
produces two artifacts: a training set of 4,670 tasks used for reinforcement
learning, and CodeSpecWeave-Bench, a 100-task benchmark.

The problem it addresses is that real coding work is specification-dense: a
patch to a real repository must simultaneously preserve interface
compatibility, state consistency, and error handling without breaking existing
dependencies. The authors' empirical analysis (their Figure 1) finds that
existing SWE training datasets carry few extracted specifications and few
distinct behavioral categories per task, so agents trained on them learn from
partial specifications and fail on the intricate interacting constraints of
real repositories. (The per-dataset values behind that comparison appear only
in Figure 1, not in the paper's text.)

Two synthesis difficulties follow. First, naively adding specifications does
not create difficulty: it either leaks solution paths or degrades the task
into a checklist of independent edits that a model can satisfy greedily, one
requirement at a time. Second, verifying interdependent specifications is
unreliable — tests can miss flaws that only appear when requirements interact
at runtime (false positives: a patch passes the tests while violating a
stated requirement) or can over-constrain the task to one implementation and
reject valid alternatives (false negatives). CodeSpecWeave's design is a
response to both: coupling as the difficulty lever, and an executed,
trajectory-audited verification loop as the quality gate. The work is
Xiaomi-adjacent in substance: all data-construction agents and both
RL-trained backbones are Xiaomi MiMo models, and an author footnote records
work done during an internship at Xiaomi. Every result reported on this page
is **author-reported**; the paper cites no independent replication of any of
its results.

## Mechanism

**Formulation.** A task is a tuple T = (R, Q, S, E): a repository R, a
natural-language request Q, a set of specifications S = {s₁…sₘ} embedded in
Q, and an execution environment E with a verifier V. A patch Δ is valid if
and only if sᵢ(Δ) = 1 for every i; in practice V checks this by executing
test suites.

**Interdependence as a design principle.** The paper distinguishes additive
specifications, where the feasible design space factorizes (F_d = ∏ⱼ Fⱼ) and
each design choice can be resolved greedily in isolation, from interdependent
specifications, where F_d ⊊ ∏ⱼ Fⱼ — choosing how to satisfy one requirement
strictly restricts the feasible choices for the others. The authors report
that their initial synthesis attempts confirmed spec-count alone yields
trivial tasks, because models satisfy each requirement in isolation.

**Task synthesis** proceeds in three steps:

1. *Specification seeds.* Candidate specification units are mined from real
   open-source development — commit histories, issue discussions, and pull
   requests. After filtering conversational chatter and raw code fragments,
   normalized deduplication yields **104,182 candidate specification units
   across six natural languages**. These seeds feed a compact "specification
   reference" (examples, definitions, boundary guidance) used during
   synthesis. This real-repository seed grounding is what distinguishes the
   tasks from specifications invented in a vacuum.
2. *Synthesis agent.* Given a repository, the seeds and reference, and
   prompts to construct interdependent specifications, an agent explores the
   codebase and combines complementary requirements, anchoring them to the
   same state transitions or core components so that satisfying one
   constrains the others. The paper's worked example couples input
   validation, transactional rollback, and backward compatibility so that
   satisfying any one in isolation still violates the broader contract.
3. *Joint iterative drafting.* The agent drafts the request Q, the
   fine-grained specifications S, and the test cases A together in a loop,
   executing the generated tests in the repository and refining from runtime
   feedback. Tests map to specifications many-to-many: several checks may
   validate one requirement, or one integration test may cover several.

**Validation and repair.** Static inspection is treated as insufficient,
because alignment flaws surface only when code runs. The pipeline collects
candidate patches and trajectories from independent coding models across
multiple attempts, filtering for tasks with *mixed solver success* —
challenging yet solvable. A review agent inspects the full tuple (Q, A, Δ, τ):
runs that violate multiple requirements expose missing checks (false
positives); valid runs that fail expose tests enforcing unintended
restrictions (false negatives). A repair agent revises the task request or
the verifier for selected flawed candidates; repaired pairs undergo execution
checks, fresh solver trials, and alignment review before acceptance. The
reported attrition for one batch is steep: **14,905 initial tasks →
difficulty filtering retained 3,275 candidates → review approved 766 verified
tasks**. The full pipeline output is **4,670 training tasks across 2,865
repositories**. The construction agents (Appendix A.1) are MiMo models —
synthesis and review use MiMo-V2.5-Pro; solvers use MiMo-V2.5-Pro and
MiMo-V2.5-Flash — all running in the Claude Code harness.

**CodeSpecWeave-Bench.** The benchmark contains **100 tasks from 100
repositories with 1,044 specifications (mean 10.44 per task)**, curated
through the same pipeline plus manual review by the authors, who examined
task descriptions, verifiers, model patches, and trajectories for realism,
requirement clarity and consistency, test coverage of stated requirements,
verifiers omitting required behavior or imposing unstated constraints, and
flaky tests or environment issues (Appendix A.2). The specification taxonomy
(Table 5) divides the 1,044 specifications into Functional Semantics (470 —
Parsing & Representation 182, Computation & Algorithms 145, Domain & Protocol
Rules 143), Errors & Recovery (187), State & Side Effects (181), Interface &
I/O Contracts (108), and Control Flow & Ordering (98); annotation was
human-in-the-loop, with MiMo-V2.5 proposing categories and rationales audited
by the authors. The training queries are also longer than prior datasets':
median length 2,131 characters (P10 1,414; P90 2,856), versus Scale-SWE
1,361, R2E-Gym 1,088, SWE-Lego 742, and SWE-rebench V2 731 (Appendix C.2).

## Evidence

All numbers in this section are **author-reported**. Evaluation settings for
the benchmark runs (Appendix B.2): 3 samples per task, a 512K context budget,
temperature 1.0, top-p 0.95. "Pass rate" means the fraction of tasks whose
patch passes the executable verifier — all specifications.

**Frontier models on CodeSpecWeave-Bench.** Ten models were evaluated across
three harnesses: GPT-5.4, GPT-5.5, GPT-5.6 Sol, and GPT-6 Astra (Codex);
Claude Opus 5, Kimi K3, and Qwen3.8-Max (Claude Code); MiMo-V2.5,
MiMo-V2.5-Pro, and MiMo-V2.6-Flash-SFT (MimoAgent). Pass rates **span 44.0%
to 74.0%** across the 100 tasks; the best is GPT-6 Astra at 74.0%, which
also had the lowest mean output length, 17.2k output tokens. Within Codex,
pass rate decreases monotonically as mean output length rises, from 74.0% at
17.2k tokens down to 66.0% at 31.8k tokens across the four GPT models.
Within Claude Code, Claude Opus 5 exceeds Qwen3.8-Max by 6.1 percentage
points while producing roughly 47% fewer output tokens. Per-model values for
the remaining models appear only in the paper's Figure 4 and are not stated
in the text. The authors interpret the extra output as largely unproductive
trial-and-error on interdependent specifications: higher success does not
require more output tokens.

**The test-alignment audit.** The paper's most consequential measurement may
be about its own pipeline. In a pilot generation of 3,067 candidate tasks,
the review process found false positives only in 1,548 tasks (50.5%), false
negatives only in 426 (13.9%), both in 293 (9.6%), and no observed issues in
800 (26.1%) — **2,267 tasks, 73.9%, had at least one alignment flaw**. In the
authors' words: "Our pilot generation reflects this difficulty: automated
reviews identified alignment flaws in 2,267 of 3,067 candidate tasks (73.9%;
Table 1), confirming that complex specifications make reliable test
generation exceedingly hard."

**RL training results.** GRPO (batch size 128, mini-batch 128, 16 samples
per task, temperature 1.0, top-p 0.97, prompt limit 8,192 tokens, response
limit 516,096 tokens; Appendix B.1) was applied to two MoE backbones —
MiMo-V2.5 and MiMo-V2.6-Flash-SFT, each 310B total / 15B active parameters —
trained on CodeSpecWeave's 4,670 tasks and compared against two training-data
baselines: SWE-PI (30,128 tasks; a mixture of Scale-SWE, SWE-Lego,
SWE-rebench V2, and Multi-SWE-RL) and MiMo Coding (size not stated in the
text). Evaluation covered CodeSpecWeave-Bench (100 tasks), DeepSWE-v1.1 (113
long-horizon tasks), SWE-bench Verified (500 tasks), and SWE-bench Pro (731
public tasks). Task success rates (%), author-reported:

| Backbone / training data | CSW-Bench | DeepSWE-v1.1 | SWE-bench Verified | SWE-bench Pro | Avg |
|---|---|---|---|---|---|
| MiMo-V2.5 Vanilla | 47.00 | 12.39 | 69.27 | 50.11 | 44.69 |
| MiMo-V2.5 + SWE-PI | 44.00 | 6.78 | 68.00 | 49.43 | 42.05 |
| MiMo-V2.5 + MiMo Coding | 50.00 | 18.62 | 73.63 | 53.81 | 49.01 |
| MiMo-V2.5 + CodeSpecWeave | 52.00 | 25.30 | 72.00 | 51.30 | **50.15** |
| MiMo-V2.6-Flash-SFT Vanilla | 59.00 | 54.42 | 74.20 | 54.54 | 60.54 |
| MiMo-V2.6-Flash-SFT + SWE-PI | 66.33 | 56.64 | 76.60 | 59.05 | 64.66 |
| MiMo-V2.6-Flash-SFT + MiMo Coding | 69.00 | 50.74 | 77.20 | 59.44 | 64.09 |
| MiMo-V2.6-Flash-SFT + CodeSpecWeave | 70.67 | 62.98 | 77.40 | 59.37 | **67.60** |

CodeSpecWeave training yields the highest four-benchmark average on both
backbones, and the best CodeSpecWeave-Bench and DeepSWE-v1.1 scores. The
largest single gain is MiMo-V2.5 on DeepSWE-v1.1, 12.39% → 25.30%. It does
not win every column: on MiMo-V2.5, the **MiMo Coding baseline is better on
SWE-bench Verified (73.63 vs 72.00) and SWE-bench Pro (53.81 vs 51.30)**.
SWE-PI shows negative transfer on MiMo-V2.5 DeepSWE (6.78 vs 12.39 vanilla).

**Behavior change after training.** Measured on CodeSpecWeave-Bench, RL on
CodeSpecWeave data changed how the models work, not just their scores.
Thinking tokens rose from 29.7k to 141.6k for MiMo-V2.5 (the authors report
4.8×) and from 22.8k to 69.5k for MiMo-V2.6-Flash-SFT (3.0×). Modified files
per trajectory rose 4.47 → 9.79 and 4.09 → 6.17 respectively; changed lines
rose 451 → 3,632 and 350 → 667; edit–test loops per trajectory rose 3.48 →
4.34 and 2.96 → 4.90, and trajectories with at least two loops rose 63.0% →
72.7% and 69.0% → 78.3%. The rate of editing and retesting after a failed
test rose 77.1% → 86.0% (MiMo-V2.5) and 77.7% → 87.1% (Flash-SFT). One
appendix nuance cuts the other way: within the first 40 turns, trajectories
with at least two loops *decreased* for Flash-SFT (47.7% → 45.7%) even as
they rose for MiMo-V2.5 (44.0% → 54.7%).

**Sliced gains and dynamics.** For MiMo-V2.6-Flash-SFT on the benchmark,
gains run 10.2–12.5 percentage points across specification-count groups
(largest in the 9–11 and 12–31 specification groups) and 9.5–14.9 points
across the seven specification categories. During training, task scores
rise steadily while policy entropy stays stable at 0.29–0.40; the backbones
adapt differently — MiMo-V2.5 more than doubles response length, Flash-SFT
nearly doubles agent turns.

**Failure analysis.** The paper names two qualitative patterns in failed
frontier attempts: *incomplete enforcement*, where a patch targets a
specification but its behavior still violates it in some settings (a SimpleX
case where a URL following "See(" remains plain text), and *interacting
requirements*, where a change satisfies one requirement while violating
another constraining the same state (an Iroha patch where a whole-state copy
shares transaction objects, so adding a required signature also mutates the
original, violating state isolation). The failure inspection itself was
performed by a frontier agent (Appendix F).

## Limitations

The authors state three limitations: using the synthesized tasks for RL
improvement requires substantial computational resources; each task carries
a container image and runs in a Kubernetes pod, so training and evaluation
require infrastructure to manage many containers concurrently; and producing
high-quality tasks relies on strong models and multiple rounds of filtering
that discard a large fraction of generated candidates.

Several further limitations are evident from the methods:

- **The same pipeline builds the training data and the benchmark.**
  CodeSpecWeave-Bench and the 4,670-task training set are products of the
  same synthesis framework, the same seed-grounding style, and the same
  MiMo-based construction agents, so part of the on-benchmark gain may
  reflect train/test distribution match rather than transferable capability.
  Improvements on the external benchmarks (DeepSWE-v1.1, SWE-bench) temper
  but do not eliminate this concern — and on SWE-bench Verified and Pro with
  the MiMo-V2.5 backbone, the CodeSpecWeave-trained model trails the MiMo
  Coding baseline outright.
- **Vendor adjacency throughout.** Synthesis, review, and solver agents are
  Xiaomi MiMo models; both trained backbones are Xiaomi MiMo models; an
  author footnote records an internship at Xiaomi. Difficulty filtering is
  keyed to MiMo solvers' mixed success, which could bias which tasks survive
  in ways favorable to MiMo-style solving.
- **Decontamination is not described.** The text does not state how overlap
  between the 100 benchmark tasks/repositories and the 4,670 training tasks
  across 2,865 repositories was excluded.
- **Most per-model benchmark numbers are figure-only.** Beyond the 44.0–74.0%
  span and the figures stated in the text, per-model pass rates appear only
  in Figure 4, and the Figure 1 dataset comparison (specifications per task)
  likewise rests on the authors' own extraction and taxonomy with values
  visible only in the figure.
- **Gains coincide with much larger test-time compute.** After training,
  models use 3.0–4.8× more thinking tokens and edit far more code; the paper
  reports no compute-matched control, so capability gain versus effort gain
  is not separated.
- **Small benchmark.** 100 tasks at 3 samples each: differences of a few
  points are a handful of tasks.
- **No independent replication.** Benchmark construction, frontier
  evaluation, and RL training were all performed by the author team; nothing
  in the paper is third-party verified.

## Competing approaches

The paper positions CodeSpecWeave against three bodies of prior work.

**Training-data baselines (head-to-head).** SWE-PI, the Prime Intellect
mixture of Scale-SWE, SWE-Lego, SWE-rebench V2, and Multi-SWE-RL (30,128
tasks), and Xiaomi's MiMo Coding dataset. These are the direct comparators in
the RL table above: both are outperformed on average, though MiMo Coding
retains the SWE-bench Verified and Pro edge on the MiMo-V2.5 backbone.

**Coding data synthesis (related work).** Magicoder and KodCode synthesize
at snippet level. R2E-Gym derives tasks from commits with test generation
and back-translation. SWE-smith breaks working code to create tasks;
SWE-Flow builds test/dependency-driven incremental tasks; SWE-Mirror
transfers issues across repositories; ADR recombines seed elements
combinatorially; TaskPilot and FrogNano refine tasks, patches, and tests
jointly with solver feedback; SWE-Gym mines issues and PRs. Against all of
these, CodeSpecWeave's claimed differentiator is that requirement coverage
and *interaction* are explicit synthesis objectives, grounded in real
developer specification seeds, rather than byproducts of task construction.

**Specification-centric work.** ArchCode, SpecRover, and REAgent extract or
use requirements from issues. CodeSpec (Wang et al. 2026, a different work
despite the similar name) builds cross-component functional chains and
executable specifications to guide feature development — the distinction the
paper draws is that CodeSpec uses specifications to guide development,
whereas CodeSpecWeave uses coupled specifications to construct the task
itself. DevAI builds requirement dependency graphs; SWE-AGI constructs tasks
from standards and RFCs; SpecCoder trains with specification-aware
generation. On the evaluation side, DeepSWE-v1.1, SWE-bench Verified, and
SWE-bench Pro serve as external benchmarks; CodeSpecWeave-Bench is
positioned as the benchmark that stresses interdependent constraints, where
the others emphasize issue resolution or long-horizon execution without
dense coupled specifications.

## Implications

For agent engineering and evaluation design, the paper's transferable claims
are mostly methodological:

- **Difficulty is a coupling property, not a count property.** Adding
  requirements produces checklists a model clears greedily; coupling them
  through shared state transitions and components is what forces joint
  reasoning. Benchmark and dataset designers should report and control
  interdependence, not just specification counts. See
  [[techniques/evaluation-and-simulation]].
- **Verifier quality is the bottleneck, and it is empirical.** That 73.9% of
  pilot candidates carried false-positive and/or false-negative test flaws
  means tests for coupled requirements cannot be validated by inspection.
  The pipeline's recipe — multi-model solver trials, trajectory-level
  review, repair, and revalidation — is a reusable auditing method for any
  generated verifier. See [[techniques/verification-and-evidence]].
- **Mixed-success filtering is a practical difficulty calibrator:** keep the
  tasks some solvers pass and others fail.
- **Behavioral telemetry is diagnostic.** Edit–test loop counts,
  retest-after-failure rates, modified-file counts, and thinking-token
  totals moved systematically with training and expose *how* an agent works,
  beyond pass rate.
- **Slice results by specification count and category.** Aggregate pass
  rates hide interaction failures; the per-count (10.2–12.5 points) and
  per-category (9.5–14.9 points) slices localize where training helps.
- **Output length is a warning sign, not a virtue.** Within a harness,
  longer frontier output tracked *lower* success — consistent with flailing
  against coupled constraints rather than solving them.
- **Training-task design shapes agent habits.** RL on interdependent-spec
  tasks shifted models toward cross-file refactoring and iterative verify
  loops rather than localized patches — a reminder that dataset design is
  behavior design.

## Reproducible experiment

The full pipeline is not reproducible at small scale — it assumes
Kubernetes-managed containers and GRPO training on 310B-parameter MoE
models — but the paper's central claims admit a small-scale replication:

1. Pick one mid-size open-source repository. Mine a few hundred
   specification seeds from its issues, PRs, and commits, and build a mini
   specification reference (examples plus boundary guidance) following the
   paper's Table 5 taxonomy.
2. Use a strong frontier model as the synthesis agent (the paper used
   MiMo-V2.5-Pro in Claude Code) to draft roughly 100 candidate tasks, each
   with 8–12 specifications deliberately anchored to shared state or
   components, plus executable tests, running the tests in-repo during
   drafting.
3. Run 3 solver models × 4 attempts per task in containers. Classify each
   task's tests: find patches that pass the tests but violate stated
   specifications (false positives) and patches that satisfy the
   specifications but fail the tests (false negatives), using an independent
   review model plus manual spot-checks. **Replication target: the Table 1
   alignment-flaw rate — about 73.9% of candidates with any flaw.**
4. Keep mixed-success tasks; repair a subset of the flawed ones and
   revalidate. **Replication targets:** frontier-model pass rates within the
   paper's 44–74% band on the kept tasks, and the within-harness
   anti-correlation between output tokens and pass rate.
5. Run the controlled ablation the paper implies but does not isolate: for
   about 20 tasks, author an *additive* twin — the same specifications,
   decoupled — and compare solver pass rates, testing the §2.2 claim that
   coupling, not count, drives difficulty.
6. Optionally, count edit–test loops and retest-after-failure rates in
   solver trajectories before and after any fine-tuning on the synthesized
   set; the Appendix E definitions make both directly computable from tool
   logs.

## Evidence status

Every quantitative claim on this page — the 104,182-seed pool, the 4,670
training tasks across 2,865 repositories, the benchmark's 100 tasks and
1,044 specifications and its taxonomy counts, the 73.9% alignment-flaw rate,
the 44.0–74.0% frontier pass-rate span, and all GRPO training and behavior
results — is **author-reported**: produced by the author team's own
pipeline, evaluation runs, and automated review process. The benchmark tasks
were manually reviewed by the authors themselves. No result is independently
replicated, and no result is a vendor claim in the paper's own presentation
(the evaluations were run by the author team, not by the model vendors; the
paper cites vendor system cards only as model references). This page was
revised on 2026-11-02 from a full read of the paper's arXiv HTML full text
(§§1–5, Limitations, References, Appendices A–F), superseding the earlier
import, whose metrics had not been reverified.

## Historical coverage

[Briefing 2026-10-30](../briefings/2026/10/2026-10-30.md)
