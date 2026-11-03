---
uid: 691885e5-23e2-47f7-a50a-82963d896cfa
depth: deep
title: "BlindToChange: AI Agents Can Find Changes When Asked But Do They Look When Needed?"
summary: "Search agents find recent changes when asked directly but usually never look when a recommendation request doesn't mention them."
type: project
created: 2026-11-02
updated: 2026-11-02
sources:
  - url: https://arxiv.org/abs/2610.41435
    retrieved: 2026-11-02
  - url: https://arxiv.org/html/2610.41435v1
    retrieved: 2026-11-02
  - url: https://github.com/Anirudh-Phukan/blind-to-change
    retrieved: 2026-11-02
  - url: https://huggingface.co/datasets/Anirudh-Phukan/blind-to-change
    retrieved: 2026-11-02
---

# BlindToChange

## What it is

BlindToChange is a benchmark that measures whether search agents *proactively discover* recent real-world changes that affect their answers, when the user's request never mentions the change. It is by Anirudh Phukan (Indian Institute of Science), Tanya Goyal (Cornell University), and Danish Pruthi (Indian Institute of Science), published as an arXiv preprint (arXiv:2610.41435, v1, 30 October 2026, cs.CL); no peer-reviewed venue is stated. The paper's motivating observation is that popular agentic search benchmarks such as BrowseComp "cannot expose failures wherein agents do not recognize their own assumptions that should be verified, since these benchmarks explicitly state what needs to be found." BlindToChange removes the statement: each item is a recommendation request in which an obvious candidate has been disqualified by a recent real-world event the request does not mention.

The benchmark's central contrast is between two probe types for the same event. A **direct probe** asks explicitly which of the old and new facts holds ("Is Tony Hoare, the British computer scientist, alive?") and isolates the difficulty of *finding* the update. An **indirect probe** is a recommendation request that never names the affected entity: the entity was a natural candidate before the event and is disqualified after it. Accuracy on the pair separates "can find a change when asked" from "looks for a change when needed."

> **Correction to this page's earlier framing.** The imported stub summarised the paper as "agents fail to verify indirectly changed facts" and named a "key technique: trigger verification for implicit environment changes." Both are wrong, and the distinction matters. In this paper "indirect" describes the **probe**, not the change: the changes are discrete, directly recorded events, and nothing in the evaluated dataset involves a fact changing as a side effect of another change. Nor does the paper implement any verification-triggering technique — it is a benchmark paper. Its discussion section only *proposes* remedy directions (selective verification; continual learning) and explicitly labels the one concrete prompt it considers — "Before finalizing your answer, verify the facts it relies on" — as speculation: "we speculate that it would help."

The evaluated dataset is also narrower than the framing suggests. It covers **only two event types, both about people**: deaths ("demises") and ends of official tenures, drawn from Wikidata for events dated February–June 2026, all postdating the most recent reported knowledge cutoff among the evaluated models (January 2026). The paper's emblematic Figure 1 example — the Bayeux Tapestry Museum being closed for renovations — is illustrative only; closures and every other non-person event type are never evaluated.

## Mechanism

**Event and probe construction (§3).** The pipeline starts from Wikidata updates of the two event types: 2,078 demise events and 751 tenure events. Each entity must have a linked English Wikipedia article — a choice the authors note "favors people that agents are likely to know well enough to recommend without search," which the filtering step requires — and, for tenures, the person must not currently hold the position again. A frontier model (Gemini-3.1-Pro, high effort) receives the update plus the entity's Wikipedia article and proposes five candidate indirect probes per event (10,390 demise and 3,755 tenure candidates in total): shortlist-style recommendation requests that admit several plausible candidates without naming the disqualified entity. Category constraints shape the requests — demise probes must call for *future participation*; tenure probes must require *authority only the current officeholder has*.

**Per-agent filtering (Design Decision 3).** Candidate probes are then filtered *per agent*: three responses are sampled with search disabled at low reasoning effort, and a probe is retained for an agent only if **all three** responses recommend the disqualified entity. An LLM judge (Gemini-3.5-Flash-Lite) decides whether a response recommends the entity, penalising recommendations rather than mere mentions. As Appendix B states, "the agent's no-search accuracy on its retained probes is therefore zero by construction" — so if the agent still recommends the entity once search is enabled, the failure is attributable to discovery, not chance. Retained sets differ by agent (on demises, from 530 probes for MiMo-V2.5-Pro to 3,092 for Gemini-3.1-Pro). Paired direct probes are generated from templates only for retained probes ("Is [name], the [short identifying description], alive?" / "Is [name] currently serving as [position]?").

**Scoring.** A direct response is correct only if it explicitly states the new fact; affirming the old fact, expressing uncertainty, or evading counts as incorrect. An indirect response scores 0 if it recommends the disqualified entity in a way that relies on the outdated fact, and 1 otherwise — mentioning the entity while acknowledging the update is accepted, and the response need not state the update.

**Evaluation setup (§4).** Eight frontier models are evaluated: Claude-Opus-4.7, GPT-5.4, Gemini-3.1-Pro, Qwen3.7-Max, DeepSeek-V4-Pro, Kimi-K2.6, MiMo-V2.5-Pro, and GLM-5.1, each at a low and a high reasoning-effort setting. Two harnesses are used. The **native harness** uses each provider's own search tool and default system instructions, as users actually encounter the systems. The **shared harness** is a common scaffold built on Inspect AI with a single web-search tool backed by Exa (returning titles, URLs, publication dates, and text highlights); models write their own queries, may search repeatedly, and every query and result is logged. Notably, the shared harness's system prompt states the evaluation date and the model's knowledge cutoff and instructs: "If a fact may have changed after the model knowledge cutoff, or is otherwise time-sensitive, call the web_search tool before answering." Results in the main table are computed on model-specific samples of 200 probes per category per model (all retained probes where fewer survive); a second table re-runs five models on a common probe set (demises n = 200, tenures n = 172) so cross-model comparisons share identical questions.

**Judge validation.** One author blind-labelled a stratified sample of 200 responses per category per probe type. Judge–human agreement is 99.5% (demises) and 98.5% (tenures) on indirect probes, and 99.0% and 100% on direct probes. For the error analysis, failures are assigned to the first matching of four mutually exclusive modes — reasoning error (the update is in context but the answer still recommends the entity), ineffective but explicit search, indirect search, and no/unrelated search — by a classifier whose agreement with author labels is 98.1% (Cohen's κ = 0.97) on demises and 81.2% (κ = 0.74) on tenures.

## Evidence

All results below are author-reported; no independent replication is cited in the paper.

**The direct/indirect gap.** The abstract reports "a big gap — as high as 27.5 points, even at high reasoning effort." Agents "almost always find the change when asked directly at high effort, reaching at least 96.5% direct accuracy on demises in nearly all configurations. Yet when queried with indirect probes for demises, the accuracy falls by a median 40.5 points at low effort and 27.5 points at high effort under the native harness; agents routinely recommend people who have passed away." Median direct→indirect gaps on demises are 42.5 points (low) and 21.8 (high) under the shared harness, versus 40.5 / 27.5 native. Tenure gaps are smaller — medians of 18.7 (low) and 15.0 (high) native, 13.0 / 8.2 shared — and the gap is larger on demises than tenures in 23 of 27 configurations. Indirect accuracy is below direct accuracy in every configuration with one exception (discussed under Limitations). The largest single gap is Claude-Opus-4.7 under the shared harness on demises at low effort: **70.0 points** (96.5% direct vs. 26.5% indirect). The paper pointedly notes that Claude-Opus-4.7, "a model at the frontier of other agentic search benchmarks, shows the largest gap" and has the lowest indirect demise accuracy under the shared harness at both effort levels.

**The failure is not searching, not searching badly.** The abstract attributes the failures directly: "more than half of the failures can be attributed to the fact that agents do not directly search to verify whether a relevant fact has changed." Under the shared harness, "failures with no/unrelated search make up at least 75% of failures in 13 of the 15 configurations" on demises; on tenures, indirect and no/unrelated search together account for a median of 50% of failures, and in 14 of 15 configurations no/unrelated search accounts for *all* of the additional demise failures relative to tenures.

The Claude-Opus-4.7 analysis isolates propensity from quality. Grouped by number of searches issued, on probes where it searches at least twice it answers 79% (low effort) and 78% (high) correctly — close to the 82% median across the other shared-harness configurations. But "it issues no search on 68% of demise probes at low effort and 23% at high effort, while no other model exceeds 8% at high effort. Its larger gap reflects how rarely it searches, not how well it uses what it finds."

**Reasoning effort helps only by inducing search.** The paper runs no dedicated mitigation arm — no re-verification prompt condition, no verification tool; the low/high effort contrast is the only intervention-like comparison. Higher effort improves indirect accuracy in 12 of 13 model–harness pairs on demises (median gain 31.5 points) and in all 13 pairs on tenures (median 9.0). The decomposition in §6 is the paper's crispest result: moving from low to high effort "reduces failures with no/unrelated search by 28.9 points on average, nearly matching the average gain in indirect accuracy of 28.1 points. … No other failure mode changes by more than 5.0 points for any model." The authors conclude that "higher effort therefore improves accuracy almost entirely by getting models to search for the update on probes where they previously did not." Kimi-K2.6, flat at 78.5% across efforts on demises, is the exception that fits the rule: it already had few no-search failures at low effort.

**On a common question set, open-weights models win at low effort — by searching more.** On the shared common set (Table 3), low-effort indirect accuracy on demises is 26.0% for GPT-5.4 and 35.5% for Gemini-3.1-Pro, against 65.0% (DeepSeek-V4-Pro), 78.5% (Kimi-K2.6), and 60.0% (GLM-5.1): "the three open-weights models are more accurate than the two closed ones on both categories" at low effort. The mechanism is again propensity — GPT-5.4 and Gemini-3.1-Pro issue no search on 58.5% and 56.5% of demise probes, versus at most 30.0% for the open-weights models — while Gemini-3.1-Pro answers 80.5% correctly when it does search. At high effort the ordering inverts: GPT-5.4 reaches 90.5% on demises, issuing a median of 16 queries per probe and searching on 97.5% of them, more than any other model.

**Harness effects are secondary but real.** At high effort, shared-harness indirect accuracy exceeds native in 9 of 12 model–category pairs and is at most 12.0 points lower in the rest. At low effort the shared harness trails the native one on demises for the three closed models by up to 32.0 points, "possibly because with reduced or no reasoning these models use a generic search tool less effectively than their provider's own." One cell is missing entirely: MiMo-V2.5-Pro under the shared harness at low effort "kept calling tools without giving a final answer."

## Limitations

**Stated by the authors** (scattered through the paper; there is no dedicated limitations section):

- The two event types are explicitly proofs of concept, chosen "because both have enough support in Wikidata since frontier models' knowledge cutoffs, although our conceptual framework applies to other event types." Whether the gap generalises to other kinds of change is untested.
- Events must postdate model knowledge cutoffs, and four of the eight providers report no cutoff; January 2026 is substituted for those models in the shared-harness prompt.
- Entity selection requires a linked English Wikipedia article, favouring well-known people.
- Only *direct* consequences of an update are considered (§7): "real-world updates often have far reaching consequences." The paper's own example: an agent that verifies a safari reserve is open may still miss that a drought has driven the animals elsewhere — "verifying the answer's own assumptions is therefore not enough."
- The exhaustive-verification remedy is untested speculation, and the authors themselves note it "scales poorly," since the agent "must therefore first enumerate what it has implicitly assumed, and then check each assumption for every candidate it considers."
- Tenure failure-mode labels are noisier than demise labels (classifier–author agreement 81.2% vs. 98.1%), so the tenure conclusions rest on two failure modes taken together.

**Evident on inspection** (not the authors' claims):

- The evaluated categories — alive/dead, in/out of office — are binary person-status changes that are unusually easy to verify with a single targeted query once suspected. The benchmark therefore measures the *decision to check* under near-ideal checkability; magnitudes may not transfer to changes that are gradual, contested, or expensive to verify.
- Generator and judge sit in one model family: indirect probes are generated by Gemini-3.1-Pro and all responses are judged by Gemini-3.5-Flash-Lite, while Gemini-3.1-Pro is itself an evaluated model. Judge validation against human labels is strong (98.5–100%), but generator-side bias — probes phrased in ways Gemini-family systems handle unusually well or badly — is not examined.
- Retained-probe conditioning cuts both ways: results describe behaviour toward entities each model *reliably* recommends without search, which is the right population for the discovery question, but the main table's model-specific samples mean cross-model comparisons there are not on identical question sets; the common-set table mitigates this for only five of the eight models.
- There is no cost accounting. Search counts are reported, but no latency, token, or dollar cost of the extra searching that closes the gap — even though the paper's proposed remedy (selective verification) is motivated precisely by cost, and no cost curve is measured.
- The shared-harness system prompt already instructs models to search before answering time-sensitive questions, and the full gap persists under it (e.g., the 70.0-point Opus-4.7 gap is under that prompt). But the paper runs no prompt-less shared-harness arm, so the prompt's own marginal effect is never isolated — it cannot be credited or blamed from this data.
- One anomaly is flagged but never analysed: Qwen3.7-Max's native-harness *direct* accuracy on demises at low effort is 21.0% — far below its shared-harness score and every other native direct score, and the sole configuration in which indirect accuracy (30.0%) exceeds direct.

## Competing approaches

The paper positions BlindToChange against benchmark families that state what needs to be found; the comparisons are qualitative — it reports no competitor scores, so no external numbers are available from this paper.

- **Agentic search benchmarks** (BrowseComp, DeepSearchQA, InfoDeepSeek, Mind2Web 2, LiveBrowseComp, LiveNewsBench) pose hard or recent search problems, but "all the constraints that need to be satisfied are clearly specified." The paper's transfer claim is pointed: "strong performance on existing agentic benchmarks does not carry over to BlindToChange," with the frontier BrowseComp-class model showing the *lowest* indirect demise accuracy under the shared harness.
- **Temporal freshness benchmarks** (RealTimeQA, FreshQA, PAT-Questions, EvolvingQA, GrowOVER, EvoWiki, DynaQuest, DailyQA) likewise "explicitly state what information needs to be found," and some "even include temporal markers (e.g., current) that suggest that facts may have changed" — cues BlindToChange deliberately withholds.
- **Implicit-constraint benchmarks** (Implicit Intelligence, DeepPlanning, MapSatisfyBench) hide constraints in an environment reachable by tool calls and similarly "find that agents rarely probe for the missing information"; BlindToChange extends the phenomenon to web search over a changing world.
- **Li & Goyal (2025)** is the direct predecessor: the recommendation-request construction of indirect probes is borrowed from it. The paper distinguishes its own contribution on scale and realism — the predecessor "was manually curated" and evaluates "only on a small retrieval corpus of synthetically generated events," where the update is *provided* to the model.
- **Update-provided paradigms** — knowledge editing (MQuAKE, RippleEdits), in-context updates (TRACK), stale-memory interaction histories (STALE, HorizonBench) — all give the model the update in context or weights, so "the only research question is whether the response changes. In our setting the update is not provided, so the agent must first suspect that what it recalls may be outdated and then search for the change." Of the paper's failure categories, only reasoning errors correspond to the failure this line of work studies.

The remedy directions the paper proposes — not evaluates — belong to [[techniques/verification-and-evidence]]: **selective verification** ("a good verification strategy should therefore weigh both how likely an assumption is to be outdated and how much the answer depends on it"), ideally trained against an accuracy-vs.-test-time-cost objective, combined with **continual learning** to keep parametric memory current so fewer assumptions are stale. The benchmark-construction technique itself — paired direct/indirect probes with per-agent pre-event filtering — is a contribution to [[techniques/evaluation-and-simulation]].

## Implications

For benchmark design, the paper is an existence proof that a capability can be invisible to an entire benchmark family: every evaluated model can find these changes when asked (≥96.5% direct accuracy on demises in nearly all high-effort configurations), yet the same models fail the same facts at median rates of 27.5–42.5 points when the request does not mention them. Evaluations that state their target measure retrieval and reasoning; they do not measure whether a system notices that a premise needs checking.

For deployed agents, the failure mode is concrete and user-facing: systems "routinely recommend people who have passed away" in response to ordinary recommendation requests, and the dominant cause is not poor search quality but the absence of any search — a propensity problem that prompt-level instructions to check time-sensitive facts (already present in the shared harness) did not eliminate. The effort result cuts the other way optimistically: the gap is largely closable by behaviour change rather than capability gains, since models that search score near a common ceiling (~78–82%) regardless of family, and higher reasoning effort closes most of the gap precisely by inducing searches.

For verification research, the paper reframes the problem as an economic one: exhaustive verification of every assumption "scales poorly," so the open problem is a policy — which assumptions to check, weighted by staleness likelihood and answer-dependence — evaluated against test-time cost. Until such a policy exists, "search more" is the only demonstrated lever, and its price is unmeasured.

## Reproducible experiment

A small paired-probe spot check is extractable from the released artifacts in about an afternoon:

1. Take ~20 demise entries from the released data (the repository's `data/main_table/`, or the Hugging Face dataset), choosing a model whose retained probe set is published, and keep each indirect probe's paired direct probe.
2. Ask the model the **indirect** probe with its native web search enabled. Record whether the final answer recommends the deceased person, how many searches were issued, and whether any query asked whether the person is alive.
3. Ask the paired **direct** probe ("Is [name], the [description], alive?").
4. Expected pattern per the paper: direct probes are answered correctly almost always; indirect failures occur predominantly with zero verification searches. Even n = 20 should show the qualitative gap and the no/unrelated-search failure signature.

A full-pipeline variant is also documented: the repository README gives the end-to-end commands (Wikidata event pull for a date range → context → probe generation → no-search filtering → direct probes → shared-harness evaluation → judging → failure classification), requiring Gemini, OpenAI, and Exa API keys. Because events must postdate the target model's knowledge cutoff, a fresh run should use a recent event window.

## Evidence status

All benchmark results on this page are **author-reported**; the paper cites no independent replication, and none is claimed here. The evaluation ran against the **live web** (providers' native tools and Exa), so exact numerical reproduction of the main results table is not expected — the same probe set will not produce identical trajectories later; the authors' answer to drift is that the pipeline can regenerate probes from newer events. Availability is this paper's strength: the full pipeline code is public under the MIT license and the dataset under CC BY 4.0 (GitHub and Hugging Face, linked in the sources), including per-model probe tables, prompts, judging, and failure-classification scripts. The paper's full text was read for this page; the repository was inspected but not executed. This page also corrects the imported stub's framing (see the correction note in *What it is*): "indirect" describes the probe, the evaluated changes are deaths and ended tenures only, and the paper proposes — but does not implement or evaluate — any verification technique; its one concrete prompt suggestion is labelled speculation by the authors themselves.

## Historical coverage

[Briefing 2026-11-02](../briefings/2026/11/2026-11-02.md)
