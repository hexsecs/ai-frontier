---
uid: d3609232-2209-4b5e-aa0c-49f844eb49d0
depth: deep
title: "MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery"
summary: "Improves its molecular workflow-search policy across tasks via persistent memory; wet-lab validated: 15.9% antibiotic hit rate, 8 pMHC binder hits."
type: project
created: 2026-11-01
updated: 2026-11-02
sources:
  - url: https://arxiv.org/abs/2610.39714
    retrieved: 2026-11-02
---

# MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery

## What it is

MoLRSI is an LLM-agent system that develops computational workflows for molecular discovery. Its primary act is not generating molecules: it searches over combinations of existing models, methods and settings — the pipelines that predict activity, rank candidates or design binders — and assembles the best-performing combination for a given task. The paper, by Yikun Zhang, Xiwei Cheng and 16 co-authors (co-corresponding: Tianyu Liu, Yuanqi Du, Nir Hacohen, James J. Collins, Wengong Jin) across Northeastern University, the Broad Institute of MIT and Harvard, and twelve further institutions, applies the system in two domains: antibacterial activity prediction followed by a prospective antibiotic screen, and peptide–MHC (pMHC) binder ranking followed by prospective binder design.

The "recursive self-improvement" (RSI) in the title needs immediate qualification, because the term invites a stronger reading than the system supports. The backbone model — Claude Sonnet 5, via the Anthropic API — is frozen throughout. Nothing is retrained, and the agent does not modify its own code or architecture. What improves is the *effective search policy*: a persistent, structured memory of past workflow searches conditions which workflow families get explored, which modifications get proposed, and how execution failures get repaired.

The paper's other distinction is that both campaigns end in prospective wet-lab experiments rather than benchmark scores alone: an antibiotic screen with measured minimum inhibitory concentrations (MICs), and a phage-display selection for designed pMHC binders. Those physical results validate the workflows MoLRSI produced; they do not, by themselves, validate the self-improvement loop — the RSI claim rests on computational ablations, and the two claims should not be conflated.

## Mechanism

MoLRSI has three components: a resource library of executable skills, an experience-guided Monte Carlo tree search (MCTS) over workflows, and a persistent cross-task memory with three stores.

**Resource library.** An Explore Agent searches scientific papers and associated code repositories, tools, benchmarks and algorithms, converting each resource into a reusable, executable "skill" specifying purpose, dependencies, input/output requirements and execution steps. Each skill is execution-validated in an isolated environment on first use; failures are repaired from error messages or removed. The small-molecule study used a library of 110 skills (55 models, 48 methods, 7 tools/resources); the protein study used 65 skills (28 models, 37 registered scoring terms).

**Experience-guided MCTS.** Workflows are nodes in trees, grouped into families sharing a common model or approach. Each iteration: (1) selects a family using the current task's best development score, an exploration bonus for less-visited families, and a *historical transfer score* from solution memory; (2) samples a parent workflow, favouring better development performance, penalizing prolific parents, and incorporating transfer scores; (3) proposes a modification guided by refinement memory — replace a method, change a component combination, adjust parameters — subject to format, duplication and feasibility checks; (4) executes and evaluates the child, repairing execution failures using execution memory within bounded attempts; (5) writes the workflow, score, modification outcome, runtime, errors and repairs back to memory. Search stops at the task's attempt or compute limit and returns the best-development-score workflow.

**Persistent memory, three stores.** *Solution memory* holds each workflow's executable code, configuration, execution status and development scores, tagged with task, dataset, metric, split and seed identifiers. *Refinement memory* holds original and revised workflows, the changes, their rationales, and before/after scores — retained whether a revision improved, degraded or left performance unchanged, plus failed revisions with failure status. *Execution memory* holds compute requirements (runtime, GPU time/memory, dataset size, hardware, environment) and, on failure, the failing stage, error logs, identified cause, attempted repairs and whether each succeeded.

**The RSI loop.** Formally, the effective search policy is π_t(a|s) = π(a|s; M_t): each attempt's experience E_t updates memory (M_{t+1} = Update(M_t, E_t)), yielding π_{t+1}. In the paper's words, "the updated policy guides further searches, whose results supply experience for the next memory update. This feedback loop implements recursive self-improvement of the effective search policy." The loop runs within a task (current-task results update memory during search) and across tasks (pooled prior-task memory initializes and guides later searches). The LLM supplying π never changes; only M does.

**Zero-search transfer.** MoLRSI can instead retrieve the best-development-score workflow from the best-matching prior task — matched on task type, evaluation metric, dataset size and description similarity — and apply it with no workflow search; model parameters are still fitted on the new task's training data and evaluation on its validation data is retained.

**Budgets and conditions.** Antibacterial benchmark: up to 20 attempted workflow evaluations per task, each candidate fitted and evaluated across all five similarity-based splits (Tanimoto 0.40, 8:1:1 ratio, five seeds); mean validation AUPRC guides search and selection, test AUPRC is reported post hoc — test outcomes were not used to guide search. Protein benchmark: 300 A100 GPU-hours and 20 attempted evaluations per task. Prospective pMHC generation search: up to 30 rounds and 1,000 A100 GPU-hours per target. Baselines retained their native tools; local baselines received one NVIDIA L40S GPU plus 20 CPU threads (antibacterial), with no hard wall-clock limit.

## Evidence

Everything below is author-reported. Results are marked **in-silico** (computational scores on held-out data) or **physical** (prospective wet-lab measurement), because the paper's two headline claims rest on different tiers.

### Antibacterial workflow benchmark (in-silico)

Across six antibacterial activity-prediction tasks (S. aureus, P. aeruginosa, A. baumannii, E. coli, K. pneumoniae, N. gonorrhoeae; ~35k train/validation and ~3.9k test compounds per task, five similarity splits, metric = held-out test AUPRC), MoLRSI — evaluated *without* RSI, i.e. with no prior-task experience — achieved the highest mean test AUPRC among the evaluated agents, ranking first on four tasks and second on two. Baselines were the scientific agents Biomni, Claude Science and STELLA and the coding agents Codex and Claude Code. Per-task AUPRC values appear only in a figure, not tabulated in the text.

**RSI ablation (in-silico).** With memory pooled from 25 source tasks (22 Therapeutics Data Commons ADMET tasks plus 3 cytotoxicity tasks; the six antibacterial targets excluded), and the same initial resource library, backbone model and search budget as the no-memory condition, RSI improved mean test AUPRC on all six antibacterial tasks. On E. coli and N. gonorrhoeae, its first evaluated workflow already outperformed every baseline agent's final workflow after 20 search iterations.

**Zero-search transfer (in-silico).** With no search at all, transfer outperformed search without RSI on S. aureus, A. baumannii and K. pneumoniae, and took the highest mean test AUPRC of the three conditions on K. pneumoniae.

**Experience scaling (in-silico).** In a retrospective pool analysis over all subsets (2,000 sampled orderings per pool size), the mean test AUPRC of transferred workflows rose from approximately 0.32 with two source tasks to approximately 0.37 with all 25; with all 25, transferred performance exceeded the 0.361 mean AUPRC of search without RSI after 20 iterations. (The analysis is retrospective — see Limitations.)

### Antibiotic virtual screening and experimental validation (physical)

The RSI-developed workflow screened the same ~12.1M-compound library and training datasets as the authors' previous expert-driven study (Wong et al., Nature 2024). After structural filters (excluding Tanimoto ≥0.40 similarity to known antibacterials, PAINS/Brenk alerts, specified antibiotic cores), cytotoxicity predictors for HepG2, HSkMC and IMR-90 cells (threshold 0.40), ranking by a weighted ensemble (0.55/0.30/0.15) and Butina clustering, 107 compounds were purchased and tested. A hit was an MSSA MIC ≤ 32 µg/mL (assays against MSSA RN4220 and MRSA USA300; MIC = lowest concentration with ≥90% growth inhibition; technical replicates n=2–3, single experiment, higher replicate value reported).

Experimental validation identified 17 compounds at or below the threshold: "The 17 hits among 107 tested compounds correspond to an experimental hit rate of 15.9%, compared with 8.7% (21 of 241 compounds) in the previous expert-driven study at the same MSSA MIC threshold… an approximately 82% relative increase in observed hit rate." Two characterized hits, C3 and C32, also showed potent activity against MRSA (MICs of 1 and 8 µg/mL respectively), with CC₅₀ ranges of 6.4–17.5 µg/mL (C3) and 24.2–54.7 µg/mL (C32) across the tested cell lines.

This is a cross-study comparison, not a controlled head-to-head: the supplement states that hit proportions carry 95% Wilson confidence intervals, that "no between-group hypothesis tests were reported," and that "the numerical MIC threshold was aligned across studies, without assuming identical experimental protocols"; the expert comparator's denominator also excluded low-predicted-activity and known-antibiotic-class controls.

On a shared held-out set of experimentally labelled compounds (in-silico — the previous study's 271-compound S. aureus set: 241 candidates plus 30 low-activity controls, 12 known-antibiotic positive controls excluded), MoLRSI's predictor achieved AUROC 0.828 against 0.590 for the previous predictor, and AUPRC 0.300 against 0.090.

### Miniprotein binder ranking (in-silico)

On 14 experimentally annotated de novo miniprotein-binder targets from three published studies (1,565 positive designs retained, up to 10 negatives sampled per positive, 17,215 designs total; leave-one-target-out evaluation; metric = Enrichment Factor at top 1%/2%, where random ranking gives EF = 1), MoLRSI without prior-task memory achieved the highest macro EF at both cutoffs: 8.01 at 1% against 7.62 for the next-best agent, and 7.29 at 2% against 6.71. Labels come from prior experiments; the evaluation itself is computational.

### pMHC ranking on held-out MART-1 (in-silico)

A ranking workflow was developed and validated on two gp100 pMHC datasets, with MART-1 reserved as an unseen target. MoLRSI achieved the highest MART-1 test enrichment, EF@1% = 3.65 and EF@2% = 5.55. No comparison agent found an experimentally confirmed binder in its top-ranked 1%; the highest baseline EF@2% was 1.85.

**RSI ablation.** Against an otherwise identical MoLRSI workflow search without access to accumulated experience from the 14 miniprotein tasks, the same system achieved an EF of 0.00 at both cutoffs; with that experience, 3.65 and 5.55. This is the paper's sharpest cross-task result and its coarsest: EF 0.00 is a floor outcome — no confirmed binder in the top-ranked fractions, on a target with few positives — so the contrast is real but the metric coarse.

### Prospective pMHC design (in-silico optimization, then physical screening)

With the ranking procedure held fixed, a 30-round search over generation methods and settings (RFDiffusion3, Proteina-Complexa, PXDesign, BoltzGen, MOSAIC APGM) optimized the mean score of the top-ranked 5% of candidates *under MoLRSI's own ranking score*. The best observed objective reached 6.76 for MART-1 and 7.56 for SARS-CoV-1, improvements of 66% and 28% over the initial configurations. Note the circularity surface: the search was tuned against the system's own scorer, so score inflation without binding gains would be invisible at this stage; the mitigations are cross-scoring and the prospective screen below. Under cross-scoring, MoLRSI designs beat Claude Science designs on median on-target score for both targets under *both* measures — MoLRSI's own score and Claude Science's ipSAE-based score — guarding against pure home-metric bias, though still a computational comparison.

In the prospective experimental screen (physical), designs were synthesized by Twist Biosciences, cloned into engineered M13 phage, and put through two rounds of in vitro phage-display selection against MART-1 (ELAGIGILTV) and SARS-CoV-1 (GLMWLSYFV) pMHCs (HLA-A*02:01), with positive/negative selection circuits for on- versus peptide-swapped off-target binding and sequencing-based enrichment readout. A hit required on-target log2FC > 4, exceeding the highest measurable off-target enrichment. MoLRSI yielded five MART-1 hits among 251 evaluable designs and three SARS-CoV-1 hits among 266; Claude Science yielded none among 288 and 267 respectively. Removing the learned ranking procedure likewise yielded no hits among 479 evaluable designs across both targets. Ranked together, all five MART-1 hits fell within the highest-scoring 9% of 767 designs, the three SARS-CoV-1 hits within approximately the highest-scoring quarter of 784.

These eight hits — the source of the abstract's "eight experimentally validated hits" — are genuine experimental measurements, but they are phage-display enrichment hits: an in vitro selection assay, not purified-protein binding constants or cellular or functional validation.

## Limitations

### Author-acknowledged

- **Experimental outcomes do not feed the improvement loop (yet).** "Biological validation remains necessary to establish whether better computational scores lead to more effective molecular candidates. Future systems could incorporate experimental outcomes into policy updates, allowing laboratory successes and failures to influence which workflows receive further exploration." The loop's feedback is entirely computational development scores; no experiment compares wet-lab outcomes with versus without RSI.
- **Transfer depends on which tasks contributed experience.** "Further progress depends on whether policy updates remain useful as biological targets and evaluation criteria change. The variation among experience pools highlights the importance of the contributing tasks, while current-task evaluation provides a way to reassess priorities inherited from earlier searches." The percentile bands on the experience-scaling analysis are wide — pool composition matters a lot.
- **No optimality or regret guarantees.** The supplement states that "the bounded transfer scores serve as empirical selection priors; their boundedness alone does not establish a standard target-task or node-level regret guarantee," and that the returned workflow "is the best evaluated workflow under the stated criterion and budget, rather than a global optimum."
- **The hit-rate comparison is cross-study, not a controlled head-to-head** (see Evidence): no hypothesis tests reported; MIC threshold aligned "without assuming identical experimental protocols"; the comparator (the authors' own previous study) used a differently constructed denominator.
- **Selection exceptions.** The 107 tested antibiotic compounds include supplier substitutions and stated exceptions to the cytotoxicity criterion.
- **Biomni baseline not independently reproduced.** The supplement notes Biomni "ran on its own platform… Its outputs were not independently reproduced outside that platform."
- **No limitations section as such.** The word "limitation" does not appear in the paper; these caveats are distributed across the Discussion, Methods and supplement. There is no discussion of cost in dollars, failure modes of the RSI loop, or negative-transfer risk beyond pool-composition variation.

### Analyst-assessed

- **Self-evaluation structure in the design loop.** The pMHC generation search optimized the mean of MoLRSI's own ranking score among top-5% candidates, and the same learned ranking selected the final candidates — the generator was tuned against the system's own scorer, a reward-hacking surface. The mitigations are real (cross-scoring under Claude Science's metric still favoured MoLRSI designs; the prospective screen is decisive), and the no-ranking arm's zero hits support the ranker's value under this assay — but the in-silico design gains (66% and 28%) are gains on a self-defined objective.
- **The RSI evidence is one pool deep in each domain.** Compounding improvement over many successive task generations is the branding; the demonstration is a single transfer step per domain (25 source tasks → 6 antibacterial targets; 14 miniprotein tasks → 1 pMHC ranking target plus 2 design targets). Experience from one antibacterial target was deliberately not passed to the others, so the cross-task claim rests on source-pool → target transfer. No experiment shows compounding over a long task sequence, nor degradation or forgetting.
- **Backbone asymmetry in the headline comparison.** In the prospective design comparison, Claude Science used Claude Opus 5 while MoLRSI used Claude Sonnet 5 — this cuts against MoLRSI, so it does not inflate the headline. But baselines retained their native tools throughout, so agent comparisons confound system design with tooling/harness differences, as usual for agent benchmarks.
- **Small physical denominators.** The pMHC result is 5/251 and 3/266 versus 0/288 and 0/267 — directionally strong (zero-hit control arms help), but eight total hits, with thresholds and "evaluable design" definitions set by the authors. The antibiotic hit rate (17/107) is a single prospective batch in a single experiment with technical replicates only.
- **Retrospective element in the scaling curve.** The pool-size analysis is retrospective; prospective deployment cannot pick the best subset, so realized gains at a given pool size would sit closer to the variance-averaged mean than the plotted curve suggests.
- **Held-out discipline is good but author-run.** Test outcomes were not used in search, prompts prohibited baselines from using held-out labels, and splits are similarity-based (Tanimoto 0.40) rather than random — stronger than typical. All of it is nonetheless self-administered by the team that also built the expert-workflow comparator, their own prior paper.

## Competing approaches

**Agent baselines benchmarked in the paper.** Biomni (a biomedical agent with a unified tool/database environment), Claude Science (Anthropic's scientific workflow system, previously reported to produce experimentally validated binders from expert-written protocols), STELLA (a self-evolving agent, run in self-evolve mode), and the coding agents Codex (GPT-5.5) and Claude Code, the last two on the antibacterial benchmark only.

**Expert-driven workflows — the real bar for the physical results.** The antibiotic comparator is the authors' previous Chemprop-ensemble virtual-screening workflow (Wong et al., Nature 2024), which discovered a new structural class of antibiotics and produced the 8.7% hit rate MoLRSI's 15.9% is compared against, on the same training data and screening library. The pMHC design predecessor is the expert RFdiffusion + ProteinMPNN + pMHC-specialized AlphaFold2 workflow (Liu et al., Science 2025).

**Component-level alternatives** sit inside MoLRSI's own library rather than competing with it head-to-head: Chemprop GNNs, MiniMol embeddings and LANTERN–RADR (predictors); RFDiffusion3, Proteina-Complexa, PXDesign, BoltzGen and MOSAIC APGM (generation); SolubleMPNN (sequence design).

The framing contrast the paper itself draws: prior agents automate expert-defined protocols, but "the reported studies do not establish how this experience improves workflow development in subsequent problems." MoLRSI's claimed delta is the cross-task memory/policy layer — not a new generator or predictor — which is why the matched memory on/off ablations, rather than the leaderboard margins, carry its central claim.

## Implications

For agent-system design, MoLRSI is evidence that a frozen frontier model plus a disciplined, structured experience memory can yield measurable cross-task improvement in search behaviour — attributable improvement, because the ablation holds library, backbone and budget fixed and toggles only memory access. That is a cleaner causal design than most self-improvement claims in the agent literature; the EF 0.00 → 3.65 contrast on MART-1 shows the effect can be the difference between finding nothing and finding something, albeit on a coarse metric at a floor.

For scientific agents specifically, the paper sets a useful evidentiary norm: end the pipeline in a prospective physical experiment. The 15.9% versus 8.7% hit rates and the 8-versus-0 pMHC hits are the numbers most likely to be quoted; both are physical, but both validate the produced workflows, not the loop. Citing MoLRSI as proof that recursive self-improvement works in the wet lab over-claims relative to what was measured; the loop's contribution is established only in-silico, over one transfer step per domain.

For evaluation practice, the paper illustrates the failure mode to watch in self-referential design loops: when a system optimizes candidates against its own learned score, in-silico gains are partly self-fulfilling by construction. MoLRSI's mitigations — cross-scoring under a competitor's metric, and a prospective screen with a no-ranking control arm — are a template for keeping such loops honest; the zero hits in both control arms convert the pMHC result from a self-scored claim into experimental evidence.

## Reproducible experiment

MoLRSI's code is **not released**. The paper contains a Data Availability section but no Code Availability section and no repository URL for MoLRSI itself; the only GitHub URLs in the paper point to third-party tools (a component method and a baseline). Reproducing MoLRSI therefore requires reimplementation from the Methods and supplement — the search procedure, memory schemas and budgets are specified in enough detail to attempt it, but no reference implementation exists to check against.

Per the Data Availability section, the benchmark datasets are publicly available: Therapeutics Data Commons (molecular property tasks); the authors' previous study (antibacterial activity, cytotoxicity, the 271-compound held-out S. aureus set); Cao et al. and Bennett et al. (miniprotein binders). The pMHC binder datasets from Liu et al. are available from the corresponding authors upon reasonable request. No new dataset DOI or repository is given for the prospective experimental results (the 107-compound MIC data and phage-display enrichment data).

The decisive experiment to reproduce is the paper's own RSI ablation — the load-bearing claim, and the cheapest to check: rebuild the workflow search over a fixed resource library with a frozen backbone, run matched searches with and without access to a pooled cross-task memory (same library, backbone and budget), and compare held-out performance — test AUPRC across similarity splits on antibacterial-style tasks, or EF at top 1%/2% on a leave-one-target-out binder-ranking task with a reserved unseen target. Reported expectations: memory improves mean test AUPRC on all six antibacterial tasks, and turns a 0.00 EF floor outcome into EF@1% = 3.65 on the held-out pMHC target. A replication finding no memory effect under matched conditions would directly undercut the central claim; one finding the effect only with retrospective best-subset pool selection would narrow it.

## Evidence status

All results are **author-reported** from a single-team preprint (arXiv:2610.39714; this page is based on v1, read in full including Methods and Supplementary Information S1–S4; arXiv also lists a v2, revised 2026-10-30). No independent replication is mentioned anywhere in the paper.

Within that tier, the evidence is unusually well-constructed for an agent paper: matched budgets, libraries and backbones for the RSI ablation; test sets excluded from search; similarity-based rather than random splits; a shared held-out set for the predictor comparison; cross-metric scoring for the design comparison; and two prospective wet-lab validations. The physical results validate the end workflows; the self-improvement claim rests on computational ablations only — both statements should travel together.

## Historical coverage

[Briefing 2026-11-01](../briefings/2026/11/2026-11-01.md)
