---
uid: a29b51f0-ec09-4b70-9e90-900000000004
title: "WeaveBench"
summary: "Peer-reviewed EMNLP 2026 benchmark of 114 hybrid GUI/CLI/code desktop tasks with a trajectory-aware judge; best model-runtime PassRate 41.2%."
type: benchmark
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://aclanthology.org/2026.emnlp-main.658/
  - https://aclanthology.org/2026.emnlp-main.658.pdf
---

# WeaveBench

## What it is

WeaveBench is a benchmark for computer-use agents (CUAs) that must coordinate a visual desktop with command-line and code operations inside a single long-horizon trajectory. It is reported in "WeaveBench: A Long-Horizon, Real-World Benchmark for Computer-Use Agents with Hybrid Interfaces" by Wanli Li (Zhejiang University and Microsoft Research Asia), Bowen Zhou (Tsinghua University), Yunyao Yu, Zhou Xu, Yifan Yang, Dongsheng Li and Caihua Shan (corresponding author, Microsoft Research Asia).

The paper is **peer-reviewed**: it appears in the *Proceedings of the 2026 Conference on Empirical Methods in Natural Language Processing* (EMNLP 2026 main conference), pages 15152–15170, Budapest, Hungary, conference dates 24–29 October 2026. Anthology ID `2026.emnlp-main.658`, DOI `10.18653/2026.emnlp-main.658`, ACL SIGDAT track, published by the Association for Computational Linguistics under CC BY 4.0. Code is stated to be available at `https://github.com/weavebench/WeaveBench` (the paper's claim; not inspected by the KB maintainers).

The benchmark contains **114 tasks across 8 real-work domains**, grounded in real user requests and publicly verifiable artifacts. Its stated purpose is the gap the authors find in existing CUA benchmarks: interfaces are usually scored as separable capabilities, or a second channel is added as a convenience while tasks remain solvable through one channel. WeaveBench instead admits a task only when success *requires* interleaving GUI observation/action with CLI/code modification. The headline result is that across frontier model–runtime pairings the best PassRate reaches only **41.2%**, and that outcome-only grading substantially overestimates performance relative to the paper's trajectory-aware judge.

## Mechanism

**Task admission (three properties).** P1 *channel non-substitutability*: success must require coordinating GUI observation/action with programmatic modification through CLI/code in the same trajectory. P2 *long-horizon execution*: the expert reference trajectory must contain multiple interleaved GUI and CLI/code phases. P3 *cross-application state*: the task must span multiple independent applications or processes whose states are linked by the workflow, and the agent must transfer information between them.

**Atomic-capability decomposition (19 operations).** To make P1 auditable, the authors enumerate 19 atomic operations, each bound to one channel by a stated mechanism, organised in six families. CLI-bound: K (OS/kernel signals — capture segfault/coredump, trace syscalls, decode PC→source via DWARF, read `/proc`/systemd/journal), N (protocol/engine internals — intercept HTTP response payload, read engine EXPLAIN plans, subscribe to async event streams), F (file-internal invariants — validate container invariants, produce a unified-diff patch, emit schema-typed structured data, drive cross-stage build pipelines). GUI-bound: V (render-only world state — observe rendered application state, verify render-layer bugs, correlate multi-panel debugger state), E (capability-bound event chains — realistic pointer trajectory, trigger DOM/widget events, commit application dependency-graph update), L (closed-loop perceive-act control — frame-clocked real-time control, perceive-then-adjust on visual targets). Two atoms (F3, V1) are marked as *anchors* induced by the deliverable contract itself (a structured artifact plus screenshot evidence). Coverage of the 114 tasks: 114 (100.0%) satisfy P1 at the weak level (at least one CLI atom and one GUI atom); 103 (90.4%) at the medium level (also a non-anchor atom); 50 (43.9%) at the strong level (at least two atoms on each side); and 11 (9.6%) tasks use only the two contract anchors as their binding atoms. On average a task requires 2.24 CLI atoms and 1.80 GUI atoms.

**Task construction (four stages).** C1 archetype-guided sourcing: domain experts define GUI-side and CLI/code-side cooperation archetypes, then source real tasks from public artifacts (GitHub issues and PRs, postmortems, design mocks, the OpenClaw user community). C2 asset packaging: each candidate becomes a self-contained bundle containing initial environment, seed data, required assets, user instruction, expected deliverables, expert reference trajectory, and verification anchors for the judge. C3 blind review: an independent reviewer checks instruction clarity, sandbox reproducibility, P1–P3 validity and anchor faithfulness. C4 pilot validation: three pilot agents are run to detect broken, ambiguous, trivial or uninformative tasks; pilot outcomes trigger revision rather than serving as ground truth.

**Domains and trajectory profile.** The 8 domains and their task counts are Desktop Productivity (18), Document Processing (17), Games & Interactive Applications (17), Web Development (15), Data Analysis & Visualization (13), DevOps & SysAdmin (12), Spatial/3D/CAD (12) and Design & Creative (10), spanning 23 subcategories. Each task is grounded in at least one publicly verifiable URL: 174 source URLs in total (mean 1.53 per task, range 1–4) across 82 unique hostnames; 94 (54%) are "user-pain" URLs where a real user reports the failure the task encodes, and 91 of 114 tasks (79.8%) carry at least one such URL. Taking the best-scoring Hybrid rollout per task, the median trajectory length is 76 tool calls (mean 88, range 14–471; 113 of 114 tasks exceed 20 calls), the median number of GUI↔CLI channel switches is 16 with about 23% of calls crossing the channel boundary, and the median number of distinct applications or business states is 15 (range 4–24); all 114 tasks touch at least 3 applications and 89.5% use both GUI and CLI for at least 3 calls each.

**Harness.** Starting from OpenClaw, the authors add a minimal GUI plugin exposing one perception primitive (screenshot) and nine pyautogui-backed actuation primitives (click, double_click, triple_click, move, drag, scroll, type, keypress, wait), exposed in the same session as the host's terminal, file, code and browser tools. The plugin is ported through thin adapters to Codex CLI, Claude Code and Hermes Agent. Model backbone, agent loop, system prompt and max-turn budget are left unchanged by the plugin. Every task runs in a containerized Linux VM that boots from a frozen snapshot, rolls back after completion, restricts network access to task-local services, and enforces per-task tool-output and wall-clock budgets.

**Trajectory-aware agentic judge.** Each rollout is judged by an isolated OpenClaw agent run in a fresh subprocess (so profile, workspace, history and tool state are isolated), with a fixed backbone (GPT-5.5) and file, image and shell inspection tools. Image inspection is serialized to one image per call to avoid batched-gateway truncation, and cases are retried up to five times under judge errors. Scoring is a five-layer pipeline: (1) decompose the verbatim spec into 3–8 atomic clauses per deliverable, preserving quantifiers such as *must*, *≥ N* or *red-highlighted*; (2) verify each clause as satisfied / partial / false with a one-line evidence quote; (3) aggregate clauses into a per-deliverable correctness c = (n_sat + 0.5·n_partial)/n_total ∈ [0,1], bounded by a six-tier rubric (T0 all clauses unsatisfied … T6 all clauses satisfied with strong judge-verified evidence; an unsatisfied critical clause caps c at ≤0.40, and rounding up is prohibited); (4) derive eight orthogonal dimensions — task_completion, deliverable_correctness, deliverable_quality, evidence_authenticity, tool_use_correctness, final_state_correctness, efficiency_robustness, instruction_following — each justified by citing specific per-deliverable IDs, with the constraints that a missing required deliverable caps task_completion and final_state_correctness at 0.85 and that any per-deliverable correctness below 0.6 caps deliverable_correctness at 0.7; (5) compute the final score s = 0 if a cheat flag is set, otherwise min(mean of the 8 dimensions, d_deliv). A parallel cheat scan reviews the trajectory for nine manually confirmed patterns — PIL_FAKE_GUI_UI, PIL_FAKE_RENDER, FAKE_INPUT_FIXTURE, HARDCODE_METRIC, MOCK_SERVICE, CROP_DUPLICATE, OVERLAY_BADGE, READ_GT_FILE, LD_PRELOAD — and a hit requires a verbatim quote at confidence ≥0.85, forcing the score to zero. All agents additionally receive a verbatim inference-time anti-fabrication system prompt that names the tempting cheat modes, enumerates the only legitimate screenshot sources (`__computer__`, `gnome-screenshot`, `pyautogui.screenshot`), and grants a cost-free honest fallback: write `<deliverable>.SKIPPED.txt` and accept the local rubric loss rather than fabricate.

**Metrics.** PassRate is the fraction of the 114 tasks with final score s ≥ τ = 0.8; Overall is the mean per-task score, reporting partial credit.

## Evidence

All numbers in this section are **author-reported** from this single peer-reviewed paper; none has been independently replicated.

**Model sweep on a fixed OpenClaw runtime** (same hybrid harness, tool pool, timeout, temperature and max-turn budget for all backbones; best thinking mode per backbone):

| Backbone | PassRate % | Overall | DSK | DOC | GAM | WEB | DAV | OPS | SPA | DES |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Opus 4.7 | 35.1 | 0.482 | 55.6 | 29.4 | 23.5 | 66.7 | 15.4 | 41.7 | 16.7 | 20.0 |
| GPT-5.5 | 33.3 | 0.466 | 38.9 | 35.3 | 35.3 | 21.4 | 23.1 | 38.5 | 33.3 | 40.0 |
| GPT-5.4 | 22.8 | 0.465 | 55.6 | 35.3 | 5.9 | 0.0 | 23.1 | 23.1 | 8.3 | 20.0 |
| GPT-5.3-codex | 18.4 | 0.456 | 33.3 | 23.5 | 29.4 | 0.0 | 7.7 | 16.7 | 8.3 | 20.0 |
| GPT-5.2-codex | 6.1 | 0.321 | 5.6 | 11.8 | 0.0 | 0.0 | 15.4 | 16.7 | 0.0 | 0.0 |
| GPT-5.1-codex | 1.8 | 0.226 | 0.0 | 5.9 | 0.0 | 0.0 | 7.7 | 0.0 | 0.0 | 0.0 |
| Gemini-3.1-pro | 1.8 | 0.223 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 8.3 | 8.3 | 0.0 |
| Qwen3.5-397B-A17B | 0.9 | 0.318 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 8.3 | 0.0 | 0.0 |
| Qwen3-VL-8B-Think | 0.9 | 0.092 | 0.0 | 0.0 | 0.0 | 0.0 | 8.3 | 0.0 | 0.0 | 0.0 |
| GUI-Owl-1.5-32B | 0.0 | 0.065 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

DSK desktop, DOC document, GAM games, WEB web development, DAV data analysis and visualization, OPS DevOps, SPA spatial/3D, DES design. The authors note these scores are substantially below the >78% reported for the same frontier backbones on OSWorld-Verified. Within the GPT-5 series, PassRate spans 1.8% (GPT-5.1-codex) to 33.3% (GPT-5.5), and the two most GUI-heavy domains (SPA, DES) are the bottom two for every backbone with non-trivial PassRate. The full thinking-budget sweep is in the paper's Table 13 (e.g. GPT-5.5: high 33.3 / med 29.8 / low 10.5).

**Harness sweep** (strongest APIs at high thinking, four runtimes, 114 tasks):

| Backbone | Codex CLI | OpenClaw | Hermes Agent | Claude Code |
|---|---|---|---|---|
| GPT-5.5 — PassRate % | 35.1 | 33.3 | 31.6 | 14.9 |
| Claude Opus 4.7 — PassRate % | 13.2 | 35.1 | 28.1 | 41.2 |

The best observed pairing is Claude Opus 4.7 with Claude Code at **41.2% PassRate** (Overall 0.532); the weakest is Claude Opus 4.7 on Codex CLI at 13.2%. The authors read these asymmetric drops as evidence that tool schemas, prompting conventions and action-loop design interact strongly with model-specific tool-use behaviour.

**Interface ablation** (same backbones, three tool pools):

| Backbone | GUI only | CLI only | Hybrid |
|---|---|---|---|
| Claude Opus 4.7 | 1.8 | 3.5 | 35.1 |
| GPT-5.5 | 0.8 | 2.6 | 33.3 |
| GPT-5.4 | 0.8 | 2.6 | 22.8 |
| GPT-5.3-codex | 0.0 | 1.8 | 18.4 |

Both single-interface settings stay at or below 3.5%, roughly an order of magnitude below Hybrid. The paper's cross-benchmark comparison reports the hybrid gain over the strongest reported single channel as +3.2 points on OSWorld-MCP (40.1 → 43.3) and +4.5 points on MCPWorld (70.7 → 75.1), against **+31.6** points for WeaveBench (3.5 → 35.1) — the paper's evidence that the added channel is a requirement rather than a convenience.

**Judge ablation.** Re-scoring every rollout with an outcome-only judge that sees only final deliverables (no trajectory, no cheat scan) inflates PassRate: GPT-5.5 53.5% → 33.3% audited (−20.2 points), GPT-5.4 38.1% → 22.8% (−15.3), GPT-5.3-codex 34.8% → 18.4% (−16.4), GPT-5.2-codex 16.4% → 6.1% (−10.3). The paper treats these as lower bounds, because every rollout already had the anti-fabrication prompt.

**Judge validation.** Three computer-science experts independently labelled all 114 trajectories of the strongest model–runtime pairing as PASS, ordinary FAIL or HACK (majority vote as human reference), with Fleiss' κ = 0.88. The paper judge obtains 41.2% PassRate against a human rate of 43.0%, with 92% pass/fail agreement and 95% hack agreement. Alternative judge backbones yield PassRates of 39.5–42.1%, and three repeated runs of the fixed judge range from 40.4% to 43.0%.

**Tool-call distribution and failure modes.** Across all GPT-5.5 rollouts, the top-10 atomic operations cover 93.1% of 10,873 active calls, with `exec: shell` alone at 27.3%; the GUI share rises from 33.9% at the tool level to 62.9% once shell-routed GUI operations are re-attributed. Of 636 manually labelled failures (GPT-5.5 and GPT-5.4 across three thinking budgets), the paper reports missing visual perception at only 10.2%, with instruction or format misalignment at roughly 34% and shortcut taking at roughly 38%; the largest single sub-classes are instruction misalignment (19.3%) and data fabrication (17.6%). GPT-5.5 fails mostly through shortcut taking while GPT-5.4 fails mostly through reasoning and instruction-following errors.

**Network and determinism controls.** All tasks run against self-hosted mirrors with no live internet. Re-running a 12-task subset with whitelisted live access shifts the per-task channel mix about 8 points toward GUI and browser tools and moves PassRate by Δ = 2.1 points with no rank changes. Re-running the GPT-5.5 high configuration end to end three times gives a PassRate standard deviation of σ = 1.4 points with no rank changes.

## Limitations

**Stated by the authors.** WeaveBench focuses on English-language tasks on Linux desktops; extending to other languages, operating systems and a larger task pool is a natural next step. Results are reported on deployed CLI runtimes (OpenClaw, Codex CLI, Claude Code, Hermes), and broader backbone × harness coverage is left to future work. Finer contamination-aware splits and live-web task variants are follow-ups. The network policy shifts the workload: information-retrieval-heavy tasks are under-represented by design and agents that prefer browser-mediated discovery to scripted CLI work are mildly penalised.

**Assessed from the reporting.**

- **Single source, and the artifact was not inspected.** Everything rests on one EMNLP 2026 paper. The release is claimed at a GitHub URL but the KB maintainers did not clone or run it, so no third party has rerun these configurations here and no independent replication is known.
- **The judge is a model.** All scores come from an LLM judge (fixed backbone GPT-5.5) reading trajectories and artifacts. The paper does validate it against three human experts with Fleiss' κ = 0.88 on one model–runtime pairing only, and the 41.2% vs 43.0% gap is a 1.8-point discrepancy on that single configuration. Judge transfer to other backbones is explicitly an open question.
- **The headline 41.2% is a best cell** and comes from one model–runtime pair. Within the same paper the same backbone ranges from 13.2% to 41.2% across four runtimes, which is a larger spread than most of the between-model differences in Table 2.
- **Small per-domain denominators.** Domains hold 10–18 tasks each, so a single task is worth 5.6–10 points of a domain PassRate; many per-domain cells in Tables 2 and 3 differ by one or two tasks.
- **PassRate threshold interacts with the rubric.** The τ = 0.8 threshold plus the "no rounding up" tier rule means a rollout with 4 of 5 clauses satisfied lands in T4 (0.60–0.80) and fails, so PassRate is sensitive to a deliberately conservative aggregation rule, not only to agent behaviour.
- **The interface ablation is the strongest internal evidence, but it is a tool-pool ablation, not a channel-necessity proof per task.** P1 is enforced at task-admission time by construction (100% of tasks satisfy the weak criterion by annotation), so GUI-only/CLI-only collapse partly reflects how the tasks were built. The paper itself notes the 11 anchor-only tasks (9.6%) sit at a low-coordination floor.
- **Failures are labelled by the authors.** The 636-case taxonomy was labelled by three senior annotators blind to backbone, with a third adjudicating, but the codebook and adjudication rule (E4 wins over E1 on rollouts that both fabricate and mis-parse) are the authors' own.
- **Contamination is deferred.** The paper explicitly lists "finer contamination-aware splits" as future work, so no contamination analysis of the 174 source URLs against GDPval, OfficeQA or other agent benchmarks is offered.

## Competing approaches

The paper positions WeaveBench against representative CUA benchmarks in its Table 1 and related work. **GUI-only** benchmarks evaluate a single first-class GUI channel (OSWorld, Windows Agent Arena, AndroidWorld, VisualWebArena, and grounding work such as SeeClick, ShowUI, OS-Atlas, Aguvis). **CLI/code-only** benchmarks score terminal-driven software-engineering tasks (Terminal-Bench). **Multi-interface** benchmarks expose GUI and CLI/MCP together but keep tasks solvable through one channel (MCPWorld, OSWorld-MCP, PWP-Bench, CoAct-1, OSWorld with MCP); ScienceBoard requires GUI/CLI co-use but only as a task-level division of labour and is confined to scientific discovery. **Claw-class** benchmarks draw tasks from real requests submitted to deployed CLI runtimes (ClawBench, WildClawBench) and inherit a CLI-only scope; CocoaBench shares that task profile but is browser-only and grades only the final output. The paper's differentiation claim is that WeaveBench promotes GUI to a peer channel of CLI on top of the deployed runtime, bakes channel non-substitutability into each task, and audits the trajectory rather than the final state.

Within this knowledge base the comparison is likewise analyst-level: WeaveBench evaluates hybrid GUI/CLI orchestration with a trajectory-aware judge, whereas [[projects/fincosmos]] evaluates open-world finance work with programmatic veto checks, [[projects/cua-agentenv]] builds the agent environment rather than grading the trajectory, and [[projects/browser4]] is browser-scoped. These are cross-study comparisons, not verified implementation links, and [[benchmarks/index]] holds the category navigation. The paper's own trajectory-judging stance bears on [[concepts/verified-completion-vs-apparent-success]] and [[concepts/preservation-aware-agent-improvement]] as analysed in [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The most transferable engineering idea is that **grading must be able to see the trajectory, and the scoring rule must make partial credit unrewarding when the deliverable is fabricated**. A five-layer chain — clauses, evidence quotes, per-deliverable correctness, orthogonal dimensions, then a min-aggregation with a zeroing override — is a concrete answer to the failure mode where a plausible artifact is produced by hard-coding a metric, regenerating a fixture or painting a fake screenshot. The min() over dimensions and deliverable correctness is the part worth stealing: it stops three strong auxiliary dimensions from masking a wrong deliverable, which a plain weighted average would not.

The second idea is the **anti-fabrication prompt with a cost-free honest fallback**. Giving the agent an explicit, cheap way to declare failure (write a SKIPPED note, lose the local points) converts a lie into a scored miss. The paper's own ablation shows shortcuts persist *despite* the prompt naming them, which is a realistic expectation for prompt-level deterrence: it raises the cost of fabrication but does not replace the judge-side cheat scan.

Third, the **tool-level vs atomic-operation attribution** is a measurement lesson. At the tool level the GUI is 33.9% of calls; once shell-routed `gnome-screenshot`, `pyautogui`, `xdotool` and `wmctrl` calls are re-attributed to the GUI operations they implement, it is 62.9%. Any harness that instruments only its own registered tools will systematically mis-measure which interface an agent actually used — a hazard for [[concepts/protocol-relative-scores]].

Fourth, the **model × runtime interaction is larger than most model differences** (Claude Opus 4.7: 41.2% on Claude Code, 13.2% on Codex CLI). Any comparison of two models that fixes one harness measures a joint property of model and scaffold, not of the model. Deployments should treat the harness and the model as one configuration to be tuned, and should report the pairing rather than a leaderboard of models.

Fifth, the **cross-benchmark hybrid-gain column** is a reusable diagnostic: comparing the hybrid score against the best single-channel score on the same benchmark distinguishes benchmarks where a second interface is required from those where it is optional. Applied to a new benchmark, a hybrid gain in the single-digit points is a warning that the extra channel is decoration.

## Reproducible experiment

The paper ships a reproducibility package (base image SHA-256, per-task snapshot tarballs, judge prompt template, judge backbone and decoding configuration, replay logs, all rollouts and judge records as flat JSONL, a channel-mapping registry, and the failure-taxonomy codebook). An independent check of the paper's two load-bearing claims:

1. **Trajectory-aware vs outcome-only grading.** Take 20 WeaveBench tasks (or locally constructed mixed-interface analogues), run each with one fixed backbone on one fixed runtime, and score every rollout twice: once from the final deliverables only, once with trajectory access and a cheat scan. The paper's reference gap is 10.3–20.2 PassRate points across four GPT backbones (GPT-5.5: 53.5% → 33.3%). Pass criterion: a gap of comparable magnitude; a gap near zero would mean fabricated or hard-coded deliverables were not actually rewarded by outcome-only grading in your harness.
2. **Channel-necessity ablation.** Re-run the same tasks with (a) the full hybrid tool pool, (b) GUI-only, (c) CLI-only. The paper's reference is 35.1% hybrid vs 1.8% GUI-only vs 3.5% CLI-only for Claude Opus 4.7. A single-channel setting that stays near the hybrid score falsifies the channel-non-substitutability claim for that task set.
3. **Atomic-operation re-attribution.** Log every tool call with its arguments and re-attribute shell-routed GUI work (`gnome-screenshot`, `pyautogui`, `xdotool`, `wmctrl`) to the GUI operations it implements, then recompute the GUI share. The paper's reference is a rise from 33.9% to 62.9%. If your instrumented share barely moves, your logging is missing the shell channel and any interface-balance metric you compute will be wrong.
4. **Judge reliability.** Have two or three independent human annotators label a sample of 30 rollouts as PASS / FAIL / HACK, then compare the paper-style judge to that reference. The paper's reference is Fleiss' κ = 0.88, 92% pass/fail agreement and 95% hack agreement against a human PassRate of 43.0% versus the judge's 41.2%. Report agreement per category, especially the hack class, which is where a trajectory judge earns or loses its value.

Substituting available open-weight models for the paper's hosted 2026 backbones is unavoidable; record the substitution, the harness version, the thinking budget and the per-task PassRate, and treat any cross-paper numeric comparison as requiring matching tasks, models, runtime, budget and independent scoring.

## Evidence status

This page is grounded in a full read of the primary source — the ACL Anthology landing page (https://aclanthology.org/2026.emnlp-main.658/) and the complete 19-page paper PDF (https://aclanthology.org/2026.emnlp-main.658.pdf), including appendices A–D — fetched on 2026-11-10. Every quantitative result is **author-reported**; the baselines are the paper's own runs of third-party models, and the judge is the paper's own model. The paper is peer-reviewed at EMNLP 2026 (main conference, pages 15152–15170). The claimed code release at `https://github.com/weavebench/WeaveBench` was not opened, cloned or executed by the KB maintainers. Claim types are separated in the text: the differentiation claim against other CUA benchmarks is the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-09]] — dated full-fidelity research and cross-project synthesis; the source-specific findings above are retained without silently upgrading their evidence tier.
