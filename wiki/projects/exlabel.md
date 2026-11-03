---
uid: 2bbd433f-e987-4668-bc89-9edbef1aad0e
depth: full
title: "Well-Specified and Well-Tested? Assessing SWE-bench-Style Datasets with a Self-Evolving Agent"
summary: "Self-evolving experience-bank evaluator labeling SWE-bench-style dataset instances for task clarity and test coverage (suite adequacy)."
type: project
created: 2026-10-30
updated: 2026-11-02
sources:
  - url: https://arxiv.org/abs/2610.39417
    retrieved: 2026-11-02
  - url: https://github.com/ZJU-CTAG/ExLabel
    retrieved: 2026-11-02
---

# ExLabel

## What it is

ExLabel is an LLM-based automated assessor for the quality of SWE-bench-style dataset instances, presented in the paper "Well-Specified and Well-Tested? Assessing SWE-bench-Style Datasets with a Self-Evolving Agent" by Zhonghao Jiang, Xuyang Zheng, Yanfu Yan, Zhongxin Liu, Lingfeng Bao, and Shuiguang Deng, all of the College of Computer Science and Technology, Zhejiang University (most also of the State Key Laboratory of Blockchain and Data Security at ZJU). The paper appeared as arXiv:2610.39417 [cs.SE], submitted 29 October 2026; the abstract page states no publication venue, so it is a preprint.

A SWE-bench-style instance bundles a natural-language task description, a golden patch, a test patch (test suite), and a sandboxed environment. Such datasets are used both to benchmark coding agents and to train them, but they contain quality defects of two kinds: task descriptions that are underspecified, making the instance unsolvable as stated, and test suites that are inadequate, making the instance unverifiable — correct solutions can fail the tests while wrong ones pass. The incumbent fix is human verification, which the paper reports (citing SPICE) at roughly $100 per instance and 1.05 person-hours per instance; SWE-bench Verified, for comparison, used 93 professional Python engineers with each instance annotated three times.

ExLabel performs the two assessments defined in §2.1 of the paper. Each outputs a Boolean label plus an explanatory note, with "positive" denoting the defective class:

- **Task Clarity** — True means the task is *underspecified*; False means well-specified. The golden and test patches serve as references, but if information needed to solve the task can only be inferred from the patches and is absent from the description, the task still counts as underspecified. External discussions and linked resources are excluded from the assessment.
- **Test Coverage** — the paper's own term for judging test-suite *adequacy*: True means the suite is *inadequate*; False means adequate, judged mainly from the test patch. The canonical failure mode is a test that pins down an implementation detail the task never specified — for example, asserting an exact error or warning message — so that valid alternative solutions fail.

The distinguishing component is a self-evolving **experience bank**: a store of structured experience items distilled from previously annotated instances, functioning as a learned, adaptive judgment rubric, explicitly positioned against the static, hand-written rubrics of prior automated annotation. The system is designed both for fully automated annotation and as a preliminary-assessment assistant to human annotators.

## Mechanism

ExLabel works in two phases: experience accumulation, which requires gold-annotated historical instances, and experience reuse against the frozen bank.

**Experience accumulation** runs a three-stage loop per historical instance:

1. **Rollout.** (I) The LLM summarizes the instance along three dimensions — **Task Type** (a generalized category), **Task Explanation** (the cause, trigger, and scenario in natural language), and **Test Explanation** (the test patch's logic and its correspondence to the task) — converting code plus text into natural language; the concatenated summary is the retrieval key of an experience item. (II) Hybrid retrieval over the current bank combines BM25 (sparse) with dense embeddings (Qwen3-Embedding-8B), scores normalized and averaged to a Top-K (K=10), after which an LLM reranking step selects Top-N (N=3). (III) The LLM predicts the label and notes, conditioned on the retrieved items.
2. **Reflection.** The LLM compares its prediction against the gold annotation and self-reflects, distilling a new experience item whose value has three fields: **Understanding** (an abstract cross-instance pattern), **Successes** (transferable strategies from this instance), and **Mistakes** (recurring error patterns, populated only for failed predictions). Items carry unique IDs for deduplication.
3. **Experience update.** An LLM-driven maintenance procedure emits an ordered operation sequence over the bank — **Insert** (new item, allocate an ID), **Modify** (ID plus revised value), **Delete** (ID). If the operation list contains a Modify but no Insert, the fresh reflection item is also inserted, so that new experience stays anchored to the current instance. The bank starts empty: a cold start in which early predictions use no experience and their reflections seed the bank.

**Experience reuse.** For an unlabeled instance, the same summarize → retrieve (Top-10 → rerank Top-3) → predict pipeline runs against the frozen accumulated bank, outputting the label and explanatory notes.

## Evidence

Every result in this section is **author-reported** from the single paper above; the paper cites no independent replication of ExLabel, and baseline numbers are as run by the authors.

### Benchmark: SWE-TQ

Because no public benchmark existed for these judgments, the authors built SWE-TQ from human annotations in two subsets spanning **8 languages**. SWE-TQ-Python derives from OpenAI's annotation release for SWE-bench Verified (1,699 instances × 3 annotators); SWE-TQ-Multilingual derives from Multi-SWE-bench (2,456 candidate instances × 2 annotators; C, C++, Go, Java, JavaScript, Rust, TypeScript). Two construction choices condition all downstream numbers. First, only instances where **all annotators agree** on the binarized labels are retained. Second, two authors **manually cleaned** the data, removing instances matching two known annotation-error patterns — well-specified labels where key information sits behind excluded external links, and adequate labels where tests assume an exact error message the task never specified — removing 34 of 148 (Python) and 136 of 384 (Multilingual) clarity/coverage instances, plus non-consensus instances; the cleaners' inter-rater agreement was Cohen's κ = 0.928. Splits also differ by task: test coverage uses a temporal split (most recent 20% as test), while task clarity uses a random 30% test split, because a temporal 20% split would have left only 10/24 underspecified positives in test.

Final sizes (accumulation/test combined): clarity — Python 1,076 (test 300, with 18 underspecified), Multilingual 1,907 (test 573, 26 underspecified); coverage — Python 833 (test 165, 56 inadequate), Multilingual 1,739 (test 348, 62 inadequate). Positive (defective) rates in test are low for clarity (6.0% Python, 4.5% Multilingual) and higher for coverage (33.9%, 17.8%), and single surface features such as description length or patch size separate the classes only weakly (AUC 0.50–0.77), so the judgments are not trivially recoverable from metadata. Test-set sizes exceed the authors' computed minima (88/91 for clarity, 86/91 for coverage, at 95% confidence and 10% margin).

### RQ1 — effectiveness on SWE-TQ

The RQ1–RQ3 setup uses three backbone LLMs — Qwen3.8-27B, DeepSeek-V4-Flash, and GPT-5.6 Luna — accessed via official APIs at temperature 0, with Qwen3-Embedding-8B embeddings for both ExLabel and the SimpleRAG baseline; ExLabel accumulates on the merged historical data of both subsets per task, the same pool that serves as SimpleRAG's retrieval corpus. The primary metric is F1 on the defective class, alongside FPR (the share of valid instances wrongly discarded) and per-instance token and dollar cost.

Author-reported, ExLabel achieves the **best F1 in all 12 combinations** (2 tasks × 2 subsets × 3 backbones). The relative improvement in average F1 over the best baseline is **+44.2% (clarity, Python), +49.9% (clarity, Multilingual), +24.0% (coverage, Python), and +18.4% (coverage, Multilingual)**. ExLabel's own absolute F1 values are more modest than the relative gains suggest, particularly on Multilingual clarity: clarity F1 is 64.7 / 51.9 / 61.1 on Python and 37.5 / 25.4 / 26.9 on Multilingual (Qwen / DeepSeek / GPT-5.6 Luna); coverage F1 is 76.5 / 73.0 / 79.4 on Python and 36.9 / 34.9 / 40.0 on Multilingual. ExLabel's average FPR is 3.3% for clarity (per-cell range 0.7–6.6%) and 15.1% for coverage (6.4–30.1%). Against the closest prior system, ExLabel beats SPICE on F1 in all 12 cells and on FPR in 11; SPICE's FPR reaches 47.6% in one cell (coverage, Multilingual, GPT-5.6 Luna). General-purpose agents Codex and Claude Code, despite autonomous repository exploration, reach at most 52.6% F1, at much higher cost: ExLabel uses 6.0k–21.0k tokens per instance versus 25.6k–265.5k for the agents. In the appendix precision/recall figures, ExLabel has the highest average precision (52.7%) and the second-highest average recall (52.0%, behind SPICE's 67.4% at only 30.8% average precision).

### RQ2 — ablations

Ablations were run with GPT-5.6 Luna only. Removing the **experience bank** is the largest single effect: F1 drops by 25.5–35.7% on clarity and 49.3–84.0% on coverage (the paper's §6.2 summary puts the average cost at 48.6% of F1), with the extreme cell being coverage on Python, where F1 falls from 79.4 to 12.7. Removing reranking costs 20.1–34.2% F1 on clarity and 4.3–6.7% on coverage. Removing individual reflection fields is smaller but consistent: without Successes, −12.1–17.5% (clarity) and −4.3% (coverage); without Mistakes, −23.9–24.9% (clarity) and −3.1–5.0% (coverage); without both, −26.5–29.7% (clarity) and −7.3–9.3% (coverage). A separate historical-data-size study (Appendix B, GPT-5.6 Luna) reports that accumulating on just 20% of the historical data (≈400 annotated instances) already improves F1 by 2.7–67.3 points over the no-bank variant in all four task/subset cells; clarity saturates early with no clear gain beyond 20%, while coverage keeps improving from 40% to 100% of history (F1 77.5→79.4 Python; 37.3→40.0 Multilingual).

### RQ3 — downstream training value

The downstream test asks whether ExLabel's labels improve agent training data. The authors sampled 5,000 SWE-rebench instances, sampled trajectories with DeepSeek-V4-Flash, and applied each filter with GPT-5.6 Luna (ExLabel reusing its RQ1 banks); instances predicted underspecified *or* inadequate are dropped. Qwen3.5-9B-Base was then fine-tuned (SFT) on the *resolved* trajectories of retained instances and evaluated on SWE-bench Verified. Author-reported, the ExLabel filter gives the best result: **66.2% resolved**, from 1,087 retained resolved trajectories after filtering out 3,276 instances, at an annotation cost of $35.21 — **$0.46 per resolved trajectory**. Reference points under identical conditions: no filtering (Full Data) reaches 54.4% with 2,309 trajectories at $0.73 per trajectory; the best baseline filter, SimpleRAG, reaches 57.8% (1,390 trajectories, $0.64 each); SPICE reaches 57.6% but keeps only 582 trajectories (filtering 4,124 of 5,000) at $0.45 each; the base model without fine-tuning scores 2.0%. The paper's headline "+14.5%" (versus the best baseline filter) and "+21.7%" (versus unfiltered) are **relative** improvements (66.2/57.8 ≈ 1.145; 66.2/54.4 ≈ 1.217), not percentage points.

### Case studies

Two cases illustrate the mechanism. In django-15869, the task asks to deprecate `length_is` in favor of `length`, but the test patch asserts the golden patch's exact warning message, which the task never specifies; the Vanilla, SimpleRAG, SPICE, Codex, and Claude Code assessors all miss the defect (repository exploration even finds other tests asserting exact messages and concludes the practice is intended), while ExLabel catches it via a retrieved experience item: "Avoid over-specification that could reject reasonable alternative implementations." In astropy-13477 (Appendix D), the test depends on the exact error string "Can only compare SkyCoord to Frame with data," and ablated variants fail it in instructive ways — for instance, the variant without the Mistakes field lacks the prior-error lesson and misses the dependency.

## Limitations

**Stated by the authors (§7.2, Threats to Validity).** Internally, human annotations may still contain errors; the authors mitigate this by retaining only unanimous-agreement instances and by their criteria-based cleaning (κ = 0.928). Externally, the evaluation is confined to issue resolution; the authors argue SWE-TQ still spans bug fixing, feature implementation, and optimization, and assert — without demonstrating — that ExLabel's general interfaces and adaptable prompts extend to other task settings.

**Evident from the methods (analyst assessment, not author claims):**

- **Agreement-filtered ground truth excludes contested instances.** SWE-TQ contains only instances all annotators already agreed on — by construction the least ambiguous cases. Performance on contested instances, where automated assessment would be most valuable, is unmeasured. Combined with the low clarity positive rates (4.5–6.0% of test), absolute Multilingual clarity F1 remains low (25.4–37.5), so the large relative gains sit on small bases.
- **The benchmark was cleaned by the authors around the failure modes ExLabel targets.** SWE-TQ is constructed and cleaned by the same team, and the two cleaning patterns (information behind excluded external links; tests assuming an exact error message) closely match the failure modes the experience bank is designed to catch. Flagged items were *removed* rather than relabeled, shaping both the accumulation pool and the test labels.
- **No variance or significance reporting.** Results are single runs at temperature 0 over API-served models; the paper reports no repeated runs, confidence intervals, or significance tests.
- **Single-backbone ablations.** RQ2 and Appendix B use GPT-5.6 Luna only, so component contributions may not transfer across backbones — RQ1 already shows backbone-dependent precision/recall trade-offs.
- **Downstream evidence is one configuration.** One 5,000-instance sample, one trajectory sampler, one 9B base model, one benchmark endpoint, and no seed variation reported.
- **Annotation cost is amortized, not eliminated.** Accumulation presupposes a gold-annotated history (≈400 instances minimum for the bank to bite, per Appendix B), and bank maintenance is itself LLM-driven — Insert/Modify/Delete operations issued by the assessing model family — with no reported human audit of the final bank's contents.

## Competing approaches

As positioned by the paper, the alternatives fall into five groups:

- **Human annotation** — SWE-bench Verified (OpenAI; 93 professional engineers), Multi-SWE-bench, and Doc2Feat-bench: high quality at roughly $100 per instance, and unable to scale to large synthetic corpora. This is the incumbent ExLabel aims to augment or replace.
- **SPICE** — the closest prior automated annotator and the main baseline. It assesses clarity via developer-provided reasoning-pattern rubrics and test coverage via Aider-based repository exploration. It is static and per-instance rather than cumulative; in these experiments it achieves the highest recall but the lowest precision, with FPR up to 47.6%, and its human-annotated evaluation set is closed (only its auto-annotated SPICE-Bench is public).
- **Vanilla prompting** — zero-shot assessment, the lower bound — and **SimpleRAG**, which retrieves the top-3 raw historical instances as few-shot examples. Together they isolate what ExLabel's distilled, evolving bank adds over raw instance retrieval.
- **General-purpose coding agents** — Codex and Claude Code with autonomous repository exploration. They test whether exploration alone substitutes for explicit judgment criteria; in these experiments it does not (at most 52.6% F1, at 4–40× ExLabel's token cost).
- **Adjacent lines of work** — fixed-rubric LLM evaluators (e.g., LLM-Rubric), self-reflection methods, and earlier automated artifact labeling (e.g., SATD detection) form the pre-history of automated quality assessment against which the paper situates the experience bank.

## Implications

For agent engineering, the paper's results — all author-reported, under the conditions in the Evidence section — support several transferable lessons:

- **Curated experience beats raw memory and static rubrics.** Distilling annotated outcomes into retrievable Understanding/Successes/Mistakes items outperforms both injecting similar raw instances into context (SimpleRAG) and hand-written rubrics (SPICE). Evaluator and judge agents may be better served by maintaining explicit, evolving experience-bank artifacts than by relying on prompts or trajectory logs.
- **Record mistakes as first-class data.** Removing the Mistakes field alone costs roughly 24–25% F1 on clarity (GPT-5.6 Luna ablation): error patterns generalize at least as well as success patterns.
- **The retrieval stack matters.** Hybrid BM25 + dense retrieval with an LLM rerank (Top-10 → Top-3) is load-bearing; dropping the rerank costs up to ~34% F1 on clarity.
- **Memory is cheaper than re-derivation.** Repository-exploring agents spent 25.6k–265.5k tokens per instance and still lost to a 6–21k-token memory-guided assessor.
- **Filter training data rather than only scaling it.** Quality filtering produced a better coding model from fewer than half the trajectories (1,087 vs. 2,309), and filtering *before* trajectory sampling also cuts sampling spend.
- **Cold-start budgets can be modest.** Roughly 400 gold examples sufficed to saturate the clarity bank, making experience-guided evaluators viable with a modest seed annotation — though test-adequacy-type judgments keep benefiting from more history.
- **Benchmark hygiene transfers.** Unanimous-agreement filtering, targeted removal of known label-error patterns, and temporal splits for test-related judgments are reusable practices for building evaluator benchmarks — subject to the caveats in Limitations about what those same choices exclude.

## Reproducible experiment

The paper's replication package (github.com/ZJU-CTAG/ExLabel) ships SWE-TQ, prompt templates, and the appendix, so a reproduction can follow the authors' route:

1. Load the SWE-TQ accumulation/test splits from the package; verify split sizes (clarity 1,076 / 1,907; coverage 833 / 1,739) and test positive rates.
2. Implement the accumulation loop: three-dimension summarization → BM25 + Qwen3-Embedding-8B hybrid retrieval (Top-10) → LLM rerank (Top-3) → prediction → reflection (Understanding/Successes/Mistakes) → Insert/Modify/Delete updates; temperature 0; start from an empty bank.
3. Run the RQ1 grid with one backbone (GPT-5.6 Luna, for comparability with the paper's ablation tables) and compare per-cell F1/FPR against Table 3; then run the without-bank ablation, expecting the largest drop (≈48.6% of F1 on average).
4. Downstream check: sample 5,000 SWE-rebench instances, sample trajectories with DeepSeek-V4-Flash, filter with the accumulated banks, fine-tune Qwen3.5-9B-Base per Appendix C (full-parameter SFT, LLaMA-Factory, 4×H100, batch 8, learning rate 5×10⁻⁵, ≤3 epochs, 131,072-token context, cosine schedule, warmup 0.1), and evaluate on SWE-bench Verified (author-reported target: 66.2%).

Caveats: two backbones are API-served 2026 models (GPT-5.6 Luna, DeepSeek-V4-Flash), so exact replication depends on API availability and version stability; costs and token counts will drift with pricing and model revisions.

## Evidence status

Single-source evidence. All quantitative claims on this page are **author-reported** results from one preprint (arXiv:2610.39417, submitted 29 October 2026, no stated venue), with baselines as run by the authors; the paper cites no independent replication of ExLabel, and none is recorded here. The SWE-TQ benchmark was constructed and cleaned by the same team (see Limitations). The authors' replication package is linked from the paper's Data Availability statement; its contents were not independently inspected for this page. This page replaces an earlier brief imported from a retained briefing summary whose metrics had not been reverified; the upgrade is based on a full reading of the arXiv HTML v1 (all sections, Tables 2–7, Appendices A–D) on 2026-11-02, cross-checked against the abstract page.

## Historical coverage

[Briefing 2026-10-30](../briefings/2026/10/2026-10-30.md)
