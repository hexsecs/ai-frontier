---
uid: b6a90501-a8d1-4d13-9a40-000000000021
title: "auto_research"
summary: "Multi-agent pipeline for X-ray polarimetry that writes its own analysis tools, gates them with checks and review, and admits only numbers with provenance."
type: project
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://arxiv.org/abs/2611.05251
  - https://arxiv.org/html/2611.05251v1
---

# auto_research

## What it is

auto_research is a semi-autonomous multi-agent pipeline that analyses X-ray polarimetry data from the Imaging X-ray Polarimetry Explorer (IXPE) and writes the analysis tools it needs. It is reported in the arXiv preprint "A semi-autonomous multi-agent pipeline for high-energy astrophysics research with enforced provenance and verifiable self-extension" (arXiv:2611.05251, submitted 3 November 2026, astro-ph.IM and astro-ph.HE). The paper lists a single author, Fang Zhou, of the Physics Department at Washington University in St. Louis. The arXiv abstract page records no journal reference and no venue; the HTML rendering carries a "Journal: Astroparticle Physics" line, so this is best treated as a preprint with no peer-reviewed venue claimed in the inspected text. The pipeline and toolkit code are public at github.com/tomthestuka/auto_research and github.com/tomthestuka/research_toolkit.

The problem the paper names is that LLM agents fabricate results and report numbers that did not come from the analysis they ran. The cited evidence is concrete: SciIntegrity-Bench (Yang et al.) found seven models produced synthetic data in 57.1% of runs and did not disclose it in 20.6% of runs; when failure reporting was allowed, undisclosed synthetic data fell to 3.2% but synthetic data still appeared in 55.6% of runs. ImpossibleBench found the strongest model tested still passed contradicting tests in 54.0% of tasks. Fei et al. found that in 82.5% of 800 agent trajectories the agent identified a flaw in its own self-review and still reported the unrevised conclusion.

auto_research's answer is to check the agents' products at two points rather than their reasoning: when a new tool enters the toolkit, and when a number appears in a report. A human remains responsible for the analysis and for promoting a tool to the trusted branch.

## Mechanism

**Team and infrastructure.** The pipeline is built on LangGraph with typed messages defined by Pydantic. Six roles follow the flow of an analysis: a **reviewer** that receives the request, dispatches literature and analysis tasks, and judges the returned result; **librarian agents** that query arXiv, NASA ADS and the web; **analyst workers** (two by default) that use models from different providers, analyse the data and then debate their results; an **analyst lead** that adjudicates between workers and decides when a new tool is needed; a **coder** that writes the tool from a brief; and a **co-lead** that reviews the new tool's code. A **status monitor** summarises progress for the human and takes no part in the analysis. Model-to-role assignment is set in a configuration file.

Each analyst worker runs its tool calls in a separate, restricted Python process with HEASoft, XSPEC and ixpeobssim available. A file-system allow-list enforced by an operating-system sandbox excludes the orchestration repository, so the agents can neither change the gate and review code nor reach the trusted branch of the toolkit.

**Two repositories and two halves per tool.** The repository auto_research holds orchestration code (agent graph, prompts, message schemas, sandbox, report generation); the running pipeline has no tool that writes to it. The repository research_toolkit holds the analysis tools; the pipeline writes to it only through the checked commit process. Each tool is committed as one atomic commit so that promoting or reverting it is a single operation. Each tool has a lib/ half holding analysis code a human can import and run, and a skills/ half holding a manifest and short wrappers telling agents how to call it. Choices that are easy to get wrong are hard-coded in the lib/ functions — the paper's example is that the IXPE reduction selects the response files of the epoch closest to the observation date.

**Provenance enforcement on reported numbers.** The reviewer, librarians and analysts can end a task only by submitting a report through the tool turn_end. Before the task ends, a validator checks that the report fills its required fields, that each cited figure file exists, and that each cited output matches its recorded hash. The validator admits a number only if it appears in a cited output of a toolkit tool, appears in the cited request, or the report gives its location in a cited paper — the last case without checking the number against the paper's text, because text extracted from PDF files is considered unreliable. Explicitly not supporting a number: shell output, files and web pages an agent read, and the output of a failed call or of a run on synthetic data, including anything computed from such an output. A rejected report returns to the agent with the reasons.

**The gate: seven automatic checks on a new tool.** (1) Determinism: the tool ships with a test that runs it twice on real data and checks the two outputs agree within a tolerance; the gate runs each of the tool's tests twice and requires the same pass-or-fail outcome both times. (2) Tool-local tests: the changed test files pass, with at least one passing test. (3) Banned vocabulary: the gate scans comments, docstrings, strings of changed code and changed text files for 35 phrases that typically accompany invented results (the list is given in Appendix E and includes "example data", "mock data", "placeholder", "TODO", "FIXME"). (4) Data-fabricating code: placeholder function bodies and binary data added to the toolkit are rejected; random-number generators and hard-coded arrays are passed to the co-lead as findings. (5) Parseability: the changed Python files parse. (6) Structure: the tool carries a description for the agents, the changes include a test file, and the changes lie on allowed paths. (7) Provenance: when tests call a new or changed tool, the figures it returns exist, the pipeline records the files it writes, and the numbers it returns appear in the recorded output.

**The co-lead: a cross-provider code review.** The co-lead receives the brief, the code changes and the gate report, can read the working copy of the toolkit, and judges whether the code follows the brief and whether the tests are adequate. It is always a model from a different provider than the coder's, because LLM evaluators favour their own output and a reviewer from the coder's family may share the coder's blind spots. The co-lead keeps no memory between submissions, because a claim of prior approval steers review agents towards approving vulnerable code. After a rejection the lead usually has the coder fix the code and resubmit, within a budget of five submissions by default; if the lead considers a rejection unfounded it can dispute it, and the co-lead reconsiders the same submission with the lead's reply as input. The code is committed only if both the gate and the co-lead approve, as one atomic commit. After a failed attempt the working branch resets to its base revision.

**Declared failure is an acceptable outcome.** The agent retries an error it can fix within a fixed budget; when it cannot complete the task it reports this to the human or ends the run in a failed or needs-human state. Following SciIntegrity-Bench, the prompts tell agents that a declared failure is not penalised. A tool-writing session likewise ends with a commit that passed all checks or with a declared failure.

**Scale.** auto_research has 34,289 lines of Python in 121 modules; the typed messages between agents are 35 Pydantic models; the deterministic test suite has 1,824 tests in 27,444 lines; the benchmark harnesses have 16,716 lines and 499 tests. On the working branch, research_toolkit holds three tool packages with 25 tools: 8,247 lines of lib/ code, 3,444 lines of skills/ code and 11,130 lines of toolkit tests.

## Evidence

All results in this section are **author-reported** from this single preprint; none has been independently replicated.

**The four analyses (Table 1).** Cost is the model-call cost at list prices.

| Analysis | Data | Tools | Cost (US$) | Time | External check |
|---|---|---|---|---|---|
| Cyg X-1 polarization reproduction | 2 ObsIDs | 7 | 55 | 7.0 h | published values |
| Polarization stability catalogue | 6 ObsIDs | 3 | 35 | 2.4 h | internal, literature |
| Polarization–hardness survey | 29 ObsIDs | 4 | 45 | — | Paper I, literature |
| qq–uu time-lag search | 45 ObsIDs | 3 | 377 | 12.0 h | none |

**Cyg X-1 reproduction (Table 2).** The agents were asked to reproduce the IXPE polarization degree (PD) and polarization angle (PA) of Cyg X-1 in the hard state, told to use the published values as a benchmark rather than tune toward them, and to report any discrepancy above 3σ. The pipeline wrote six tools and extended the data loader. All 14 compared quantities agree within 3σ. The PAs agree to better than 0.5σ and the PD-versus-energy slope to 0.24σ. However all 10 PD quantities, including the slope, lie below the published values, by 0.2–2.4σ, for both analysis methods and in all energy bands — for example May PD (2–8 keV, PCUBE) 3.37 ± 0.20 against 4.01 ± 0.20 (z = −2.29), and combined PD (2–8 keV) 3.46 ± 0.17 against 3.95 ± 0.17 (z = −2.09). The pipeline reported the offset as systematic but did not trace its cause; the paper's own earlier pipeline (Paper I) traced it to the event weighting.

**Polarization stability.** Six observations of four sources were split into 5 ks segments (effective exposures 1.1–4.9 ks). For five of six, (q, u) is consistent with being constant, with p between 0.75 and 0.98. The exception is Swift J1727.8−1613 observation 03006001 (χ² = 155.9 for 116 degrees of freedom, p = 0.0079), where no significant polarization was detected (PD = 0.05 ± 0.33 %); after accounting for the six trials the p-value is 0.046, so the variability is marginal. No observation shows significant PD variability.

**Polarization–hardness survey.** The pipeline correlated 2–8 keV PD with hardness for 29 observations of six black-hole X-ray binaries. PD exceeds MDP99 in 24 of 29 observations, from four sources; the five non-detections lie at the soft end of the hardness range. For the 24 detections, Spearman ρ = 0.947 with p = 2.5 × 10⁻¹². The paper notes the hardness ratios are not corrected for absorption, that the two heavily absorbed 4U 1630−47 observations therefore appear harder than they are and contribute to the combined correlation, and that the pipeline did not recognise this problem. Within single sources the correlation holds for Cyg X-1 and Swift J1727.8−1613 and is not significant within LMC X-3.

**qq–uu time lag.** The pipeline read 45 of 47 requested observations; the other two (SS 433 04004001 and GS 1354−64 05250399) are still proprietary and encrypted and were reported as not measured. Slices were cut to reach a minimum detectable polarization of 6 %, and significance came from shuffling the u values 1,000 times with q and timestamps fixed — a method the paper itself says can underestimate the chance probability of a DCF peak. Only 11 of 45 observations have enough events for at least eight slices, giving 12 segments from six sources. Eleven of 12 segments show no significant lagged correlation. Cyg X-3 observation 02250301 has a DCF peak at a lag of −57.7 ks with p = 0.0060, below the 0.01 threshold; after accounting for the 12 segments tested, p = 0.07, so the pipeline reported it as a candidate rather than a detection. Its 68 % flux-randomisation interval is [−100.94, −57.68] ks, and the paper notes that Peterson et al. combine flux randomisation with random-subset selection and that either method alone generally gives smaller uncertainties, so the interval is probably too narrow.

**Planted-defect benchmark (Table 4; co-lead gpt-5.6-sol).** The benchmark inserts each defect into a copy of the toolkit and passes the modified toolkit through the gate and the review. It contains 65 planted defects and 69 defect-free control changes.

| Class | Defects | Gate: scan | Gate: tests, structure | Co-lead | Reaching a commit |
|---|---|---|---|---|---|
| Fabrication, with a banned word | 8 | 6 | 1 | 1/1 | 0 |
| Fabrication, without a banned word | 6 | 0 | 1 | 5/5 | 0 |
| Wrong result, test exposes it | 4 | 0 | 4 | — | 0 |
| Wrong result, test misses it | 15 | 0 | 0 | 15/15 | 0 |
| Tests that check nothing | 9 | 0 | 2 | 6/7 | 1 |
| Hidden limit | 10 | 0 | 0 | 10/10 | 0 |
| Missing structure or manifest | 7 | 0 | 4 | 3/3 | 0 |
| Invisible to the gate | 6 | 0 | 0 | 6/6 | 0 |
| All planted defects | 65 | 6 | 12 | 46/47 | 1 |
| Control (defect-free change) | 69 | 0 | 0 | 40/69 | 29 |

An LLM checked whether each rejection reason named the planted defect: of the 46 defects the co-lead rejected, 44 were rejected for the planted defect. In the eight-model comparison, 295 of 308 rejections named the defect in the specific code. The eight models from five providers detect between 31 and 46 of the 47 defects that reach the review and falsely reject between 0 and 40 of the 69 controls; the three GPT models detect the most defects and also falsely reject the most. In all 113 false rejections the GPT models judged the tests inadequate. Six reviews returned no usable verdict (three by deepseek-v4-pro, two by qwen3.8-max, one by glm-5.3) and were counted as non-detection.

**Ablation of the checks (Table 5).** Defects reaching a commit: default 1/65; no scan 0/65; no tool-local tests 0/65; **no co-lead review 46/65**. In each run with a gate check disabled, the co-lead caught every defect that check had stopped in the default configuration.

**Reliability and cost of tool writing (Tables 6 and 7).** Over 386 gate runs in 252 logged coder sessions the gate rejected 68 submissions (17.6 %): banned vocabulary 52 (13.5 %), tool-local tests 10 (2.6 %), structure 6 (1.6 %), determinism 1, parseability 1. In the 25 trials of Table 7, banned vocabulary caused all 18 gate rejections, some of them false positives. With the lead (claude-opus-5) and co-lead (gpt-5.6-sol) held fixed and the coder varied:

| Coder | Trials | Committed | Gate rej./trial | Co-lead rej./trial | Median cost US$ | Median minutes |
|---|---|---|---|---|---|---|
| deepseek-v4-flash | 5 | 5 | 0.6 | 1.6 | 6.5 | 52 |
| glm-5.3 | 5 | 4 | 0.2 | 2.8 | 16.0 | 90 |
| claude-sonnet-5 | 10 | 7 | 1.4 | 2.2 | 82.0 | 116 |
| gpt-5.6-terra (same provider as co-lead) | 5 | 5 | 0.0 | 2.8 | 10.8 | 43 |

With claude-sonnet-5 the coder accounted for a median 89 % of trial cost. The paper notes the deepseek-v4-flash commits changed a smaller scope (no change to the reduction module), so its higher commit rate may reflect that, and that with so few trials the difference in commit rate is consistent with chance.

**Generality across model tiers (Table 9).** The coder (deepseek-v4-flash) and co-lead (gpt-5.6-sol) were held fixed while the analyst lead, reviewer and one analyst worker were switched between an "anchor" and a weaker "contrast" assignment; the Cyg X-1 request was run three times per assignment.

| Run | Assignment | Tools | Hours | US$ | k/14 | Mean abs z | Gate | Review |
|---|---|---|---|---|---|---|---|---|
| 1 | anchor | 0 | 3.5 | 38 | 8/14 | 1.12 | 0/5 | 5/5 |
| 2 | anchor | 6 | 21.5 | 121 | 14/14 | 1.24 | 1/20 | 13/19 |
| 3 | anchor | 7 | 7.2 | 95 | 14/14 | 1.29 | 1/18 | 11/18 |
| 4 | contrast | 8 | 9.5 | 60 | 12/14 | 1.23 | 3/25 | 14/22 |
| 5 | contrast | 3 | 6.6 | 102 | 12/14 | 1.23 | 42/49 | 4/7 |
| 6 | contrast | 3 | 3.1 | 51 | 12/14 | 1.23 | 2/8 | 3/6 |

All six runs reproduced the systematic PD offset of the main analysis. In run 5 one analyst worker computed the May PD and PA of the XSPEC fit with PyXspec in a shell session; the reviewer later instructed the analysts to record the two quantities as not measured if no toolkit tool could fit the model, and the lead did not carry the shell values forward because the fit lacked background subtraction. The final report records both quantities as not measured.

**Total cost.** The reported experiments cost about US$2,200 at list prices: the four analyses of Table 1, US$259 for the planted-defect benchmark, US$984 for the tool-writing trials and US$466 for the model-tier runs.

## Limitations

**Stated by the authors.** The design has three limitations. First, provenance enforcement establishes the origin of a number, not its correctness: a defective tool that passes the gate and the review yields numbers the validator admits. Second, the co-lead is a language model and therefore fallible — it let one of the 47 defects that passed the gate reach a commit and rejected 40 of the 69 defect-free controls. Third, the validator verifies that a number appears in a cited output, not that it was taken from the correct place in that output. Further stated limits: results are based on four analyses of similar data; the paper has not yet measured how often later runs revise earlier conclusions, how often later analyses reuse committed tools, or how much it costs a human to verify a tool. The q–u lag analysis has no published reference and no expected detection, so a false detection is its main risk; the paper notes its own reviewer accepted a report on the basis of a reference that does not support the claim made of it.

**Assessed from the reporting.**

- **Single source, single author.** Everything rests on one arXiv preprint (v1, 3 November 2026) written by one author, with no peer-reviewed venue claimed. Unlike [[projects/receipt]] or [[projects/late-autumn]], this is not a multi-author institutional result.
- **The headline defect number is the complement of a different number.** "47 of 65 planted defects pass the automatic checks" describes the gate alone; the paper's own Table 4 shows that with the full gate plus the co-lead review, 64 of 65 are stopped and one reaches a commit. The abstract foregrounds the weaker number, and the briefing-derived summary inherited it. Read against Table 5, the load-bearing number is that removing the co-lead review alone lets 46 of 65 reach a commit.
- **The false-rejection rate is the mirror image of the catch rate.** 40 of 69 defect-free control changes were rejected by the co-lead, and the eight-model sweep produced 113 false rejections. The paper argues these rejections mostly name real weaknesses in the tests or code, but for a pipeline that expects to promote tools, a 58 % false-rejection rate on correct changes is a heavy operational cost that the cost tables do not price separately.
- **The defect benchmark is author-built.** The paper states it knows of no established benchmark for how well checks catch defects in AI-written scientific code, so the 65 defects are the author's own construction and the class labels are theirs. The 69 controls are likewise author-written, which makes "false rejection" a comparison against the author's notion of a correct change.
- **The reproduction is a 3σ agreement, not a verification.** Agreement within 3σ on 14 quantities leaves room for a systematic offset of 0.2–2.4σ in every PD value, which is exactly what was observed and not traced. The comparison is also against a specific published table (Table S2 of Krawczynski et al., "PD sum") with a model the reference does not name, so part of the residual could be methodology rather than pipeline error.
- **Statistically thin inference.** The model-tier test uses three runs per assignment and the paper itself says three runs are too few to measure run-to-run consistency, citing Mustahsan et al. on intraclass correlation in agentic evaluations. Run 1 recovered 8/14 quantities with 0 tools; the contrast runs' 42/49 gate rejections in run 5 is a very different operating regime from run 6's 2/8. No confidence intervals accompany the k/14 or \|z\| figures.
- **The co-lead's verdict is unstable.** The paper counts unstable verdicts on 10 repeated submissions of the same defect-free package, and states that in both runs with a gate check disabled the co-lead's verdict on an unchanged package differed between runs. A single LLM verdict is therefore not a deterministic gate.
- **Scope is four analyses of one instrument's data.** The claim that the gate, validator, two-repository boundary and promotion rule contain no astronomy-specific code is an author claim about generality that is not tested on a second domain in the inspected text.
- **No cost accounting for human review.** The paper states that the cost of human verification of a tool is not yet measured, yet the pipeline requires a human to promote tools to the trusted branch and the co-lead rejects ~58 % of correct changes — both of which imply human cost.

## Competing approaches

**The paper's own comparisons.** The baseline it differentiates itself from is Paper I (Domine et al., arXiv:2610.14185), the author's earlier IXPE agentic pipeline, described as an AI-assisted analysis pipeline for IXPE observations of black hole X-ray binaries; auto_research differs in four stated ways — it takes project analysis ideas rather than developing its own, it focuses on a reviewed toolkit, it adds quantitative tests of new analysis tools, and it writes reports about the results. The cross-provider scripted-checks-plus-audit combination is credited to Dong and Chen's CrossAudit (arXiv:2608.28631). The paper notes that earlier tool libraries let the model that wrote a tool grade it, citing Voyager, or relied on tests and human review, citing ToolUniverse.

**Provenance mechanisms it distinguishes itself from.** Earlier systems link each number to a labelled output of the analysis code (Ifargan et al., NEJM AI), to logged tool calls (Liu, arXiv:2608.23623), or require that the named run has finished (Chen, EviBound, arXiv:2511.05524). Kosmos (arXiv:2511.02824) links each statement to its source notebook or paper, yet independent scientists judged only 79.4 % of 102 statements accurate. The paper's counterpoint is that those approaches do so for a fixed set of tools or for code written for a single task, whereas auto_research can extend its toolkit and still enforce provenance.

**Failure-mode literature it draws on.** SciIntegrity-Bench (arXiv:2605.10246), Collider-Bench (arXiv:2605.13950) and gwBenchmarks (arXiv:2605.11269) for fabricated results; ImpossibleBench (arXiv:2510.20270) for test gaming; the Darwin Gödel Machine (arXiv:2505.22954) for faked tool calls; Fei et al. (arXiv:2608.14905) for agents not acting on their own reviews; Kaliyev and Maryanskyy (arXiv:2604.00392), whose benchmark found 215 of 222 agent-written tools gave wrong results on every held-out input, for the argument that checks on results can miss a defective tool; Panickssery et al. (arXiv:2404.13076) for LLM evaluators favouring their own generations; Melo et al.'s SEVRA-BENCH (arXiv:2606.13757) for review agents being steerable by claims of prior approval.

**Other agentic science systems cited as related.** The AI Scientist (arXiv:2408.06292), Denario (arXiv:2510.26887), the AI Cosmologist (arXiv:2504.03424), an open-source planning and control system with language agents (arXiv:2507.07257), domain-specific agents for CTA and gamma-ray analysis (arXiv:2510.01299), and Gendreau-Distler et al.'s LLM-powered HEP data-analysis agents (arXiv:2512.07785), whose repeated-trial protocol the tool-writing benchmark follows.

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The transferable idea is the separation of *provenance* from *correctness*, made explicit and machine-checked. auto_research does not claim that a number is right; it claims that a number can be traced to a recorded tool output, to the request, or to a location in a cited paper. That is a weaker claim and a more implementable one, and it is exactly the distinction [[concepts/verified-completion-vs-apparent-success]] needs: the pipeline can certify that a figure came from an execution without certifying that the execution computed the intended quantity. The paper names the residual gap itself — the validator checks that a number appears in a cited output, not that it was taken from the correct place in it. A deployment that treats a provenance link as a correctness signal inherits [[concepts/evaluator-circularity]]: the tool that produced the number is also the tool the gate reviewed.

The second takeaway concerns the shape of the defence. The ablation in Table 5 is the sharpest result in the paper: removing the deterministic scan or the tool-local tests changes almost nothing about what reaches a commit (0/65 in both cases, because the co-lead catches what they would have caught), while removing the LLM reviewer lets 46 of 65 through. In other words the LLM review is doing the work that the cheap deterministic checks appear to do, and the deterministic checks are doing little that the reviewer does not also do. That is the opposite of the usual intuition that mechanical checks are the cheap safety net, and it argues for spending on review capacity rather than on expanding keyword lists. It also cuts the other way: the same reviewer is what produces 40 false rejections, so the paper's configuration trades a defect-free change being thrown away for a defect reaching a commit.

The third takeaway is about declared failure as a first-class outcome. The pipeline treats "not measured" as a correct answer and makes the shell-output exclusion work in practice: in run 5 a worker computed the missing values correctly and the pipeline still refused them because the fit lacked background subtraction and came from a shell. Systems that allow "no answer" as a verdict are the only ones that can also be audited afterwards; a pipeline where every request must produce a number will produce numbers, and provenance rules are what make that safe.

Fourth, the honesty of the cost accounting is worth copying. auto_research reports total list-price spend by experiment, reports the coder's share of trial cost, and reports the fraction of false rejections alongside the catch rate. That combination — catch rate, false-rejection rate, and money per trial — is a much better reporting template than the win-rate-on-benchmarks template that dominates the [[evaluations/briefing-synthesis-2026-11-03-to-09]] material, because it lets a reader estimate the operational cost of a gate rather than only its nominal effectiveness.

Finally, the two repositories plus the promotion rule is the part of the design most likely to transfer to other domains, since the paper states that the gate, the report validator, the repository boundary and the promotion rule contain no instrument-specific or astronomy-specific code. The pattern — orchestration repository the agents cannot write to, toolkit repository they can only write through a checked commit, trusted branch no agent can reach — is a concrete answer to [[concepts/scoped-assurance]] that does not depend on the science.

## Reproducible experiment

The pipeline and toolkit code are public, so a check does not have to be a from-scratch reimplementation, but running the authors' pipeline is not required to test the central claim; the defect benchmark is self-contained and is the load-bearing evidence.

1. **Replicate the defect benchmark with your own defects.** Take the published research_toolkit, write 30 correct tool changes and 30 defective ones in the same style as the paper's six classes (fabrication with and without a banned word; wrong result with a test that exposes it and with a test that misses it; tests that check nothing; hidden limits; missing structure). Run each through a gate you implement (determinism, tool-local tests, banned-vocabulary scan, parseability, structure, provenance) and then through a cross-provider LLM reviewer. Pass criterion: the review stage removes a large majority of the defects that the mechanical gate passes, matching the paper's direction — the paper's own Table 5 shows the reviewer catching everything the disabled checks had caught, and the gate alone letting 46 of 65 through.
2. **Measure the false-rejection rate explicitly.** Run the 30 correct changes through the same reviewer. The paper's reference point is 40 of 69 rejected (58 %), with the reviewer usually citing inadequate tests. A materially lower false-rejection rate at similar detection would show the co-lead configuration, not the idea, is the problem; a materially higher rate would show the paper understates the operational cost.
3. **Test the provenance validator, not the reviewer.** Construct reports in which a number appears in a cited output but is misattributed — the case the paper names as its third limitation — and confirm that the validator admits them. This is the cleanest test of the design's stated boundary: the validator should reject nothing here, and the point of the experiment is to document exactly that gap rather than to hope it is closed.
4. **Check the "not measured" path.** Give an agent a task whose only correct answer requires a computation the toolkit cannot perform, and verify the pipeline reports "not measured" instead of substituting a shell-computed value. The paper's run 5 is the reference; the pass criterion is that no unvalidated shell number reaches the report.

Any reproduction must substitute models available to the tester for the paper's 2026 hosted models (claude-opus-5, claude-sonnet-5, gpt-5.6-sol, deepseek-v4-flash, glm-5.3, gpt-5.6-terra) and should report the substitution, since the paper's own Table 8 shows the roles are sensitive to model choice.

## Evidence status

This page is grounded in a full read of the primary source — the arXiv abstract page (https://arxiv.org/abs/2611.05251) and the complete HTML full text including appendices A–E, all nine tables and the reference list (https://arxiv.org/html/2611.05251v1) — fetched on 2026-11-10. Every quantitative result is **author-reported**; the baselines and defect benchmark were run by the authors; the paper is a single preprint (v1, 3 November 2026) with no peer-reviewed venue claimed in the inspected text. The event logs and the planted defects and controls are stated to be available from the corresponding author on request, not from a public URL; the six model-tier reports are attached as ancillary files anc/run1.pdf–anc/run6.pdf. Claim types are separated in the text: the design's generality beyond astronomy, the adequacy of the checks, and the reviewer-cross-provider argument are the authors'; the items under "Assessed from the reporting" and the whole Implications section are analysis by the KB maintainers. Nothing on this page was reproduced, executed, cloned or tested by the KB maintainers, and no independent replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-05]] — dated full-fidelity research and cross-project synthesis (this page supersedes that snapshot's assessment).
