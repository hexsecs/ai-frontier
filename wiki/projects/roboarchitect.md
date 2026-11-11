---
uid: b6a90302-a8d1-4d13-9a40-000000000002
title: "RoboArchitect"
summary: "A coding model evolves the control harness around a frozen robot policy, raising held-out manipulation success from 9.7% to 43.3% without weight updates."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
related: [capability-locus]
sources:
  - https://arxiv.org/abs/2610.42141
  - https://arxiv.org/abs/2610.42141
  - https://arxiv.org/html/2610.42141v1
---

# RoboArchitect

## What it is

RoboArchitect is a method for automatically designing and optimising the **agent harness** around a frozen robot policy, reported in the arXiv preprint "RoboArchitect: Automating the Design of Robotic Agents with Persistent Memory" (arXiv:2610.42141, cs.RO, v1 submitted 30 October 2026; preprint, no peer-reviewed venue claimed). The source lists six authors — Shengguang Wu, Suning Huang, Cherie Ho, Ria Doshi, Hao Zhu and Serena Yeung-Levy — all at Stanford University. The paper gives a project website (https://roboarchitect-ai.github.io/) and points to a codebase at https://github.com/roboarchitect-ai/RoboArchitect.

The premise it builds on is that "a frozen robot policy performs far better inside an agent harness, where control code decides when to query the policy, consult vision tools, or command the arm directly" — but that today's harnesses are built by hand and redesigned for each new robot or benchmark. RoboArchitect's claim is that harness design can be automated, offering "a strong alternative to finetuning on a novel setup". The unit of optimisation is therefore the surrounding program, not the weights: a coding model observes rollouts, diagnoses failures and revises the harness, and the paper's headline numbers are 4.5× and 3.2× gains in held-out success with no weight updates anywhere.

The paper is explicit that it is about transfer rather than about one benchmark: harnesses are evolved on one set of episodes and evaluated on held-out episodes under two protocols — *unseen scenes* (same tasks, different scene arrangements and layouts) and *unseen tasks* (held-out episodes containing entirely different tasks that require shared manipulation skills) — because "like a finetuned policy, a harness optimized on specific rollouts could overfit to them".

## Mechanism

**Harness interface.** A robotic agent harness is a program between environment observations and low-level robot execution commands. At each control step it receives the current observation — camera images, depth maps, gripper pose, gripper status — plus the natural-language task instruction, and outputs low-level action vectors for the robot controller. The starting harness is a pass-through of the bare VLA policy: it forwards observations and returns the policy's predicted actions directly. This pass-through is exactly the "Bare Policy" baseline column of the results.

**Auxiliary tools.** Beyond the policy, the harness may query pretrained auxiliary tools — language models, vision-language models, object detectors, segmentation models, pointing models and grasp pose generators — and has geometric utilities that project pixel-depth pairs into 3D robot base coordinates and generate relative trajectory primitives. In the reported configuration the auxiliary stack is Qwen3-30B-A3B-Instruct as the language model, Molmo2-8B or Qwen3-VL-8B-Instruct as the vision-language model, Grounding-DINO for object detection, SAM 3 for segmentation, Molmo2-8B for pointing, and GraspGen for grasp pose generation.

**Optimisation loop.** The loop follows the same trial-and-error sequence as a human engineer. Every evaluation logs complete trajectory traces — per-step camera frames, the robot's readings, and all model and tool outputs. A coding model reviews these traces from the current harness, diagnoses failure modes and proposes a candidate revision, in which it may follow the policy, invoke any tool, or command the arm programmatically. The candidate is re-evaluated on the same training set and **accepted only if its performance surpasses that of the current harness**, which guarantees a monotonic optimisation trajectory on the training set, capped at a maximum number of iterations. The coding model is `claude-opus-5`, invoked via the Claude Code client at maximum effort, with **at most 5 optimisation iterations**.

**Persistent memory.** The harness is also given a persistent memory mechanism carrying information across episodes and tasks. Crucially, "no schema or memory rules are specified; RoboArchitect is entirely free to decide what to store, in what form, and how to retrieve it", and the structure is evolved from accumulated rollout evidence rather than hand-crafted. These memories are data structures inside the designed robot agent, not the coding model's own context: they accumulate during the agent's rollouts and persist at execution time, and every evaluation starts with an empty memory to be accumulated.

**Evolved control routines.** The paper documents what the harness revisions look like in practice. *Detecting and clearing arm jams*: because the visual observation barely changes during a jam, the policy keeps issuing similar commands and tips objects over; the harness learns to monitor discrepancies between commanded and actual gripper movement and lifts the arm clear before re-querying the policy. *Synthesising missing motion primitives*: on VLABench the harness detects overhead obstructions via depth maps and computes horizontal approach vectors to reach beneath a shelf board; on RoboCerebra it adds a wrist-rotation primitive for pouring, and for cabinet opening it locates the cabinet with the pointing model, finds its handles in the depth image, then aligns and pulls. *Rescaling contact forces*: on RoboCasa-365 the toaster-oven door requires closure within 0.5% of its opening range, but RLDX-1 pushed too gently, so the harness rescales action magnitudes while preserving direction. *Tethering mobile bases*: it defines workspace anchors at locations where the last gripper activations occurred, gives the base a driving budget, and retraces to the latest anchor once the budget is spent. *Redirecting to target objects*: for spatially swapped scenes such as LIBERO-Pro, where policies overfit on the original LIBERO and reach for memorised locations, the harness queries the pointing model for the instructed item instead. *Replacing an unusable policy*: where the untuned X-VLA on SimplerEnv WidowX commands a fully open gripper at every step and produces no useful signal, the harness evolves into a complete vision-based code-as-policy agent — parsing instructions, detecting targets with open-vocabulary detectors, estimating 3D poses from depth maps, computing grasp vectors and executing trajectories directly. *Adapting to perception limitations*: where vision tools could not reliably distinguish mahjong tile faces, the harness maintains a ranked candidate list and works down it; where visual grasp checks caused premature release, it replaces the visual check with a depth check under the fingertips. *Per-robot control-rate independence*: each motion phase ends when the arm arrives or stops making progress, measured by distance to target rather than by elapsed time, because a fixed time budget expires while the arm is still in transit on a slower platform such as the 3 Hz Google robot.

**Evolved memories.** The discovered memory types fall into three families. *Execution parameters from experience*: on SimplerEnv WidowX the harness records the grasp heights that have successfully lifted an object as a function of measured object height; on LIBERO-Pro-10 the MolmoAct-2 harness averages the depth of successful grasps below the object top as a share of the object's height to parameterise fallback grasps; the OpenVLA-7B harness records the grip style — *pinch* or *spread* — that succeeds for each object. The paper stresses that these are indexed by measured physical properties or object identity rather than by task names, so they generalise to novel objects. *Implicit task and environment clues*: on RoboCasa-365 the harness associates instruction verbs with the need to *hold* an object, enabling an empty-grasp recovery routine for "picking" tasks while leaving it disabled for "pressing" tasks where a closed empty gripper is intentional; on RoboCerebra it discovers and stores the environment's 150-step scene-reset period so later episodes can take over a placement early enough to finish before the reset; inference outputs such as VLM/LLM parses of multi-step instructions are cached. *Embodiment-specific calibration*: in the unified harness the memory stores which way each robot's fingers close, learned by opening and closing the empty gripper and observing the motion in the depth image, plus the resting finger configuration as a reference for detecting empty grasps.

**Control division of labour.** The paper's most interesting claim about the division of labour is that it was never specified. In several setups the evolved harness bypasses the frozen policy entirely on benchmarks a general policy was never trained for, becoming a code-as-policy agent; around finetuned specialists it keeps the VLA in charge and intervenes only when it fails — taking over via the pointing tool late in an episode if the gripper has never approached the instructed object, and handing control back if the policy is already closing in on it. "We never instructed the coding model how to divide control; each harness arrived at its structure from rollout evidence alone."

## Evidence

All results are **author-reported** from this single preprint; none has been independently replicated. Metric definition matters here: on VLABench the authors use the official **progress score**, which assigns partial credit for grasping the right object and for each goal condition met; on all other benchmarks they report **success rate** averaged over tasks. The paper calls all of these "success rates (%)" in its own text, so the VLABench numbers are progress scores rather than binary success. All compared scores, including the finetuned references, use the same step limits, and on SimplerEnv WidowX and Google episodes always run to the limit and are scored on their final state.

**Benchmarks and policies.** LIBERO-Pro-10 (LIBERO-10 long-horizon with object locations swapped per the LIBERO-Pro protocol), RoboCerebra, VLABench, RoboCasa-365 and SimplerEnv WidowX, plus SimplerEnv Google for the unified harness. Policies: MolmoAct-2, OpenVLA-7B, π0.5, RLinf-π0.5, SmolVLA, X-VLA and RLDX-1. Each setup is characterised by the distance between the policy's training data and the evaluation benchmark: in-distribution, swapped, cross-benchmark or out-of-domain.

**Held-out results (Table 1).** "Harness (ours)" is the same frozen policy inside the evolved harness after a single design attempt (*One-Shot*, iteration 1) or after iterative refinement over up to 5 iterations (*Iterative*).

| Benchmark | Policy | Bare (scenes) | One-Shot | Iterative | Bare (tasks) | One-Shot | Iterative |
|---|---|---|---|---|---|---|---|
| LIBERO-Pro-10 | MolmoAct-2 | 10.0 | 12.0 | 32.0 | 2.5 | 2.5 | 15.0 |
| LIBERO-Pro-10 | OpenVLA-7B | 0.0 | 2.0 | 26.0 | 0.0 | 0.0 | 22.5 |
| LIBERO-Pro-10 | π0.5 | 8.0 | 4.0 | 24.0 | 0.0 | 0.0 | 2.5 |
| LIBERO-Pro-10 | RLinf-π0.5 | 2.0 | 2.0 | 40.0 | 0.0 | 0.0 | 10.0 |
| LIBERO-Pro-10 | SmolVLA | 0.0 | 0.0 | 38.0 | 0.0 | 10.0 | 27.5 |
| RoboCerebra | π0.5 | 22.0 | 20.0 | 55.3 | 24.0 | 12.0 | 28.0 |
| RoboCerebra | SmolVLA | 20.0 | 34.3 | 49.3 | 26.0 | 16.0 | 80.0 |
| VLABench | X-VLA (general) | 7.3 | 32.8 | 52.6 | 1.2 | – | 72.5 |
| VLABench | *X-VLA finetuned* | 35.2 | – | – | 32.1 | – | – |
| SimplerEnv WidowX | X-VLA (general) | 0.0 | 77.1 | 87.5 | 0.0 | – | 66.7 |
| SimplerEnv WidowX | *X-VLA finetuned* | 70.8 | – | – | 87.5 | – | – |
| RoboCasa-365 | RLDX-1 | 27.9 | 29.3 | 27.8 | 73.5 | 76.5 | 77.5 |
| **Mean (all setups)** | | **9.7** | **21.4** | **43.3** | **12.7** | **–** | **40.2** |
| **Mean (cross-benchmark and out-of-domain)** | | **7.3** | **32.5** | **58.4** | **6.3** | **–** | **48.7** |

The paper's headline figures are the all-setup means: **+345%** mean held-out success on unseen scenes (9.7 → 43.3) and **+216%** on unseen tasks (12.7 → 40.2); restricted to the setups furthest from the policy's training data, the means are 7.3 → 58.4 (+696%) on unseen scenes and 6.3 → 48.7 (+671%) on unseen tasks.

The comparison against finetuning is the sharpest part of the table: on VLABench under both protocols and on SimplerEnv WidowX under unseen scenes, the evolved harness around the general policy **outperforms the finetuned weights of the same model** (52.6 vs 35.2 on VLABench scenes; 72.5 vs 32.1 on VLABench tasks; 87.5 vs 70.8 on WidowX scenes), and falls short only on SimplerEnv WidowX under unseen tasks (66.7 vs 87.5). Two setups show no gain from the harness: RLDX-1 on RoboCasa-365 under unseen scenes (27.9 → 27.8, a −0.2 point change, where the paper notes the policy improved only on its optimisation episodes), and the π0.5 row on LIBERO-Pro-10 under unseen tasks (0.0 → 2.5).

**Iterative refinement.** The iteratively evolved harness outperforms the one-shot design on the training set in every setup and on the held-out sets except RLDX-1 on RoboCasa-365 under unseen scenes. The paper notes that while some one-shot designs fall below the bare VLA policy on held-out sets, the iterative harness surpasses it on nearly every one. The appendix trajectories show steady, mostly monotonic progression over iterations.

**Unified harness across embodiments (Table 2).** A single harness is evolved on a training pool of **2,201 procedurally generated episodes** and evaluated on the **2,160 standard benchmark episodes**. Around the *general* X-VLA checkpoint it raises the mean over benchmarks from 1.8 to 41.6 on the training pool (+2228%) and from 1.9 to 28.8 on held-out evaluation (+1417%), reaching 29.4 on LIBERO-Pro, 17.5 on VLABench, 68.3 on SimplerEnv WidowX and 51.2 on SimplerEnv Google (held-out). Around the *finetuned X-VLA specialists* the gains are small by design: 58.0 → 60.7 on the training pool (+5%) and 45.9 → 47.0 held-out (+2%), with individual benchmarks moving between −1.0 and +10.2 points — the harness preserves the specialists' competence rather than disturbing it. The unified harness reads everything that differs between robots at runtime from the action specification and proprioception, never hardcoding embodiment-specific constants.

**Memory behaviour (Table 3).**

| Setting | Memory entries | Reads per episode | Actionable reads |
|---|---|---|---|
| X-VLA on VLABench | finger depths that have been lifting objects | 3.4 | 98% |
| X-VLA on SimplerEnv WidowX | height at which to close the fingers, per measured object height | 3.5 | 96% |
| MolmoAct-2 on LIBERO-Pro-10 | average depth of successful grasps below an object's top | 9.9 | 99% |
| π0.5 on RoboCerebra | scene-reset period of this simulation | 13.0 | 95% |
| RLDX-1 on RoboCasa-365 | task instructions that need a grip | 11.0 | 92% |

"Actionable reads" is the share of memory reads that find a stored entry. A worked example from the figures: on SimplerEnv WidowX, closing the fingers at 18% of the carrot's height (floored at 0.8 cm) lifts nothing, whereas closing at 45% of the object height — 1.4 cm on the carrot, 3.9 cm on the eggplant — lifts both.

**Episode counts and cost.** Every task is run for the same number of trials per benchmark: 10 for LIBERO-Pro-10, RoboCerebra and VLABench, 24 for SimplerEnv WidowX and 50 for RoboCasa-365. The task split of a benchmark is shared by all policies evaluated on it. A complete evolution of 5 iterations "takes under 6 hours of coding-model time and stays under $150 on average, with no demonstrations collected and no model weights updated."

**A single worked trajectory.** For general X-VLA on SimplerEnv WidowX, where the policy is unusable, the evolved harness raised success from 0% to 100% on its optimisation episodes and achieved 87.5% on unseen scenes and 66.7% on unseen tasks. A separate revision that made the harness end moves on arrival rather than on a fixed time budget raised the agent's performance on the slower Google robot from 11.0% to 30.2% on the training pool.

## Limitations

**Stated by the authors.** Three limitations are given. *Scaling cap of iterations*: the work uses a fixed maximum of 5 optimisation iterations; more iterations may yield further gains, but the point at which returns saturate remains to be explored. *More complex manipulation*: extending to richer contact dynamics such as dexterous in-hand manipulation or tool use, where the space of failure modes is larger than in pick-and-place, is an open question. *Sim-to-real transfer*: all evaluations run in simulation. The authors argue the harness reads only the standard input space (camera images, depth, the robot's own readings), so its interface should carry over to a real robot, but testing simulation-evolved harnesses on real robots and investigating how many further improvement iterations a real deployment needs are future work.

**Assessed from the reporting.**

- **Single source, simulation only, no physical validation.** Everything rests on one arXiv preprint (v1, 30 October 2026). No sim-to-real experiment, no real-robot rollout and no safety evaluation appears; the paper's own framing is that sim-to-real is future work.
- **The baselines are author-run in one harness.** The bare-policy column is the authors' evaluation of each policy, and the finetuned reference rows are public checkpoints of the same policies evaluated on the same held-out set — but run by the authors, under the authors' harness and step limits. The central claim "often outperforms even the finetuned version" therefore rests on the authors' own harness configuration.
- **Small absolute counts in places.** With 10 trials per task on LIBERO-Pro-10, RoboCerebra and VLABench, one episode is 10 percentage points on a single task, and many of the table's values are multiples of 2.5. The paper reports no confidence intervals, no seed variation and no significance test for any of the table's differences.
- **The mean hides a failure.** The all-setup mean of 43.3% on unseen scenes includes a setup where the harness was flatly unhelpful (RLDX-1 on RoboCasa-365, −0.2 points) and one where the one-shot design fell below the bare policy (π0.5 on LIBERO-Pro-10, 8.0 → 4.0). The distributions matter more than the mean, and the paper does not report them beyond the table.
- **The optimiser can overfit the training episodes.** Acceptance is decided on the same training set used to generate the traces, so the monotonicity guarantee is a guarantee on the training set, not a generalisation guarantee. The held-out protocols mitigate this but do not eliminate it, and the RLDX-1 case is an instance of training-set improvement without held-out improvement.
- **The memory contribution is not isolated.** No ablation removes the persistent memory while keeping the harness, so the share of the gain attributable to memory is unknown; the memory statistics (reads per episode, actionable share) show use, not causation.
- **The code-as-policy escape hatch complicates the claim.** In several settings the evolved harness ignores the frozen policy entirely. The headline is then "a coding model can build a robot agent", not "a frozen policy can be made much better", and the paper does not separate how often each happens across the table.
- **Cost is per-evolution, not per-deployment.** "Under 6 hours and under $150 on average" describes harness evolution for one setup; it excludes the coding-model costs of the auxiliary tools, the simulator time, and any real-robot iteration, and it says nothing about the maintenance cost of a harness that is specialised to one robot.
- **The unified harness is evaluated on procedurally generated training data only.** Its training pool is synthetic-by-procedure episodes; the breadth of that generator, and whether a different generator would produce a different harness, is not tested.

## Competing approaches

Only approaches the source itself compares against or cites as related.

**Hand-written harnesses around frozen policies.** VoLo treats the policy as an interruptible tool, guiding it alongside vision models and programmatic motions; Harness VLA assigns high-level planning to an LLM agent and restricts the frozen policy to contact-level primitives. Other systems decompose tasks into subproblems with memory or verification mechanisms, and Hu et al. find that the planner, controllers and switching logic of hierarchical VLA architectures must be co-designed. The paper's distinction: these works establish that the interface around a VLA matters, but their agent architectures were specified manually in advance, whereas RoboArchitect automates harness design including the VLA/code division of labour and persistent memory.

**Inference-time adaptation without weight updates.** Retrieving demonstrations or successful action segments to condition the policy, and selecting among the policy's candidate actions with a learned value function, are cited as complementary; the paper's contrast is that RoboArchitect evolves complete agent interfaces from scratch, combining persistent memory, programmatic control and policy orchestration.

**Finetuning** is the main alternative the paper benchmarks against — RLinf-VLA's πRL online RL fine-tuning and the general practice of collecting demonstrations for every new task or hardware configuration. The paper notes that finetuned manipulation skills often fail to generalise beyond their initial training distributions, and that its held-out protocols test exactly this transfer. It also cites Berman et al. (2026) finding that frontier coding models are more capable with higher-level access to pretrained robot policies than when controlling low-level motion directly, "an arrangement RoboArchitect often evolves into on its own".

**Code-as-policy and coding agents for manipulation.** Code-as-policy uses executable programs as the primary robot control, with ProgPrompt, VoxPoser and recent coding agents extending it; CaP-X shows their success depends heavily on the hand-written primitives they are given. The paper argues that RoboArchitect unifies the code-as-policy and learned-VLA paradigms empirically, since in out-of-domain settings the evolved harness can replace the policy entirely.

**Automated code and harness optimisation.** ADAS (automated design of agentic systems), Darwin Gödel Machine, Self-Harness, Meta-Harness and Evo-Harness are cited as coding models that evaluate agent outputs, analyse execution traces and iteratively refine agent implementations; RoboArchitect's own monotonic acceptance rule follows "the empirical validation in prior work on self-improving agents". Within robotics, Eureka (reward design), ENPIRE (training configurations revised from execution logs) and EXIMO (VLM-decomposed exploration distilled into policies) all generate artifacts that train policy weights, and are therefore described as complementary, since RoboArchitect automates the agent built around a frozen policy.

**Skill libraries for control code.** ASPIRE, RHO, GaP, Playful Agentic Robot Learning and language-guided skill distillation are cited as systems that accumulate reusable control skills — with the key contrast that "these skill systems optimize programs that entirely replace the robot policy", whereas RoboArchitect develops the harness *around* a frozen policy.

Within this knowledge base, the related entry is [[projects/tinyastral]], which tests the same capability-locus question in a different domain; the connection is an analyst-level comparison, not a claim that the two projects cite or depend on each other.

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The most transferable engineering idea is that **the optimisation target is the harness, not the model**, and that the harness is a normal program that a coding model can edit. That reframes "can we adapt to a new robot?" from a data-collection problem into a code-generation problem, and the acceptance rule — accept a revision only if it beats the current harness on the optimisation set — is directly portable to any agent scaffolding. It also gives a concrete answer to [[concepts/capability-locus]]: for these setups the measurable capability lived in the surrounding control code, and the paper's own table shows the largest gains exactly where the policy contributed least, which is the boundary case that makes the point sharply.

Second, the paper's most useful negative result is the **monotonicity trap**. Optimisation progress is guaranteed on the training episodes by construction, and the held-out gain can lag or reverse — the RLDX-1 case is exactly that. Any team adopting an automated-harness loop needs a held-out gate, not a training-set gate, and needs to decide in advance what happens when the harness improves on what it sees but not on what it will meet. This is the same [[concepts/verified-completion-vs-apparent-success]] structure as elsewhere in this knowledge base: an accepted revision is a claim, not a verification.

Third, the **iterative refinement result** argues for budgeting more than one revision. The one-shot harness captures less than half the total gain on average (21.4 vs 43.3 on unseen scenes), and the paper attributes this to the agent generating its own new failure evidence after the first design — a mechanism that applies anywhere an agent's execution produces diagnostic data. The corollary is that a single-shot harness-design attempt is likely to be a badly chosen stopping point.

Fourth, the **memory design principle** is worth stealing in its negative form. The paper specifies no memory schema at all, and the useful memories that emerged are indexed by measured physical properties rather than by task identity, which is why they transfer. For agent-memory systems generally, the lesson is to index persistent state by measurable properties rather than by task labels, and to check whether an evolved memory still carries signal on held-out episodes (here: over 90% actionable reads).

Fifth, a caution about scope: in several rows the harness simply **discarded the policy**. Reporting "the frozen policy improved 4.5×" without also reporting how often the policy was bypassed would misrepresent what happened. Teams porting the pattern should log the fraction of episodes in which the base model is actually consulted, because that number determines whether they have an improved policy or a new system wearing its name.

Finally, the cost picture is encouraging but narrow: "under 6 hours and under $150 on average" per evolution is cheap enough to make this a routine step for every new robot setup, which is the paper's stated operational goal. That is a strong argument for treating harness redesign as a first-class, automatable engineering step rather than as bespoke integration work.

## Reproducible experiment

The codebase is public (https://github.com/roboarchitect-ai/RoboArchitect), so a reproduction is plausible, though it depends on simulation stacks, VLA checkpoints and a closed frontier coding model.

1. **Reproduce the two headline means on a single benchmark first.** Take one setup with a public policy — LIBERO-Pro-10 with OpenVLA-7B is the cleanest, since the bare policy scores 0.0 on both protocols and the claim is a large multiplicative gain — and run the loop: log traces, let a coding model propose revisions, accept only on improvement of the training set, cap at 5 iterations, then evaluate on the unseen-scene and unseen-task held-out splits. Pass criterion: the bare policy's near-zero baseline should rise to roughly the paper's 26.0% on unseen scenes and 22.5% on unseen tasks. A directional match on one setup is weak evidence but a null result would be decisive; note the paper's own one-shot numbers (2.0 and 0.0) show how much the iterative loop contributes, so a one-shot implementation failing to reproduce would not falsify the claim.
2. **Test the acceptance-rule hypothesis.** Add a variant in which revisions are accepted on the *held-out* split instead of the training split, and a third in which revisions are accepted on training score but a held-out regression vetoes acceptance. This tests the paper's most consequential implicit design choice — that training-set monotonicity is safe — and should be reported per setup, because the RLDX-1 result suggests it is not always safe.
3. **Isolate the memory contribution.** Add a condition with the persistent memory mechanism removed but the control routines intact, and a condition with the control routines removed but memory intact. The paper reports no such ablation, so this directly measures a claim the paper asserts without evidence, and the "actionable reads" statistic is the natural dependent variable alongside held-out success.
4. **Audit the bypass.** For every evolved harness, log the fraction of control steps in which the frozen policy was consulted, and split the reported success rates by whether the policy was used. The paper claims unification of code-as-policy and VLA paradigms; this measures how often each mode actually occurred, and whether the headline gains come from the modes the framing emphasises.
5. **Check the sim-to-real assumption, at least partially.** The paper's stated limitation is that everything is simulated. A minimal check is to run an evolved harness on a real arm with the same observation space, if one is available; failing that, at least report the control-rate sensitivity the paper identified (ending moves on arrival rather than on a fixed time budget) as an explicit hypothesis, since it changed the Google robot's training-pool success from 11.0% to 30.2% and would silently degrade on slower hardware.

Substituting an available coding model for `claude-opus-5` and available VLA checkpoints for the paper's is unavoidable; the substitutions, the simulator versions and the per-task trial counts should be reported with the results, since 10 trials per task means one episode is 10 percentage points.

## Evidence status

This page is grounded in a full read of the primary source on 2026-11-10: the arXiv abstract page (https://arxiv.org/abs/2610.42141) and the complete HTML full text including appendices A–C with the control-routine and memory detail, the benchmark table and the evolution trajectories (https://arxiv.org/html/2610.42141v1). Every quantitative result is **author-reported**; the baselines — the bare policies and the finetuned reference checkpoints — were run by the authors in the authors' harness; the paper is a single preprint (v1) with no peer-reviewed venue claimed; and all evaluation is in simulation. No independent replication is known. Claim types are separated in the text: the claim that harness design can be automated and the "substantial headroom in the harness" conclusion are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no simulator, policy or harness was run.

## Historical coverage

- [[briefings/2026/11/2026-11-03]] — finding 2, the dated report that first mined this source.
- [[evaluations/briefing-synthesis-2026-11-03-to-09]] — cross-briefing synthesis that includes this project.
