---
uid: b6a90401-a8d1-4d13-9a40-000000000011
title: "GitHub Octoverse 2026"
summary: "GitHub's 2026 platform report: agent-started PRs pass 40% of pull requests; all figures are vendor-reported and observational, not audited."
type: case-study
created: 2026-11-09
updated: 2026-11-10
depth: deep
sources:
  - https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/
  - https://github.blog/news-insights/octoverse/
  - https://docs.github.com/copilot/concepts/models/auto-model-selection
  - https://docs.github.com/pull-requests/how-tos/stacked-pull-requests
---

# GitHub Octoverse 2026

**Origin:** [[briefings/2026/11/2026-11-04]] — finding 1. **Date of report:** October 28, 2026, updated November 6, 2026. **Primary source:** [GitHub's 2026 Octoverse report](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/). **Status:** a vendor annual report, published by GitHub Staff about GitHub's own platform. It is not peer reviewed, not audited, and not independently verifiable.

## What it is

Octoverse is GitHub's yearly report on activity across its platform. The 2026 edition, "Commits, pushes, reach new highs in 2026 as developers build with agents", is published under the Octoverse tag by "GitHub Staff" on 28 October 2026 and edited on 6 November 2026 "to clarify the methodology language for open source rankings". The post is a summary of a larger report; a glossary and a **Methodology** section are published in the same post, and the post links onward to product documentation (for example the auto model selection page and the stacked pull requests documentation) rather than to a separate downloadable dataset.

The report's own measurement window is stated in the methodology: **the Octoverse year runs 1 October 2025 to 30 September 2026, inclusive**. Unless noted, metrics include public and private repositories; industry, open-source contribution and open-source project figures are public only. Prior years' figures are recalculated on the same definitions and window, so 2024 and 2025 numbers here may differ from earlier reports, which covered public activity on a September-to-August window.

The subject matter closest to this knowledge base's concerns is a set of platform telemetry figures about agent involvement in software delivery, plus a set about model choice. The figures are observational: they measure that agent-associated activity happened and how it correlated with other activity, not that agents caused any outcome.

## Mechanism

**How the numbers are produced.** The methodology section describes the collection and classification rules; it does not publish queries, code, or the underlying records.

- *Scope and window.* Octoverse year = 1 Oct 2025 – 30 Sep 2026 inclusive. Public and private repositories unless stated; industry, open-source contribution and open-source project figures are public only. 2024 and 2025 are recalculated on the same definitions and window.
- *Counting rules.* A push sends one or more commits and counts once toward contributions, so commit totals can exceed contribution totals; Actions are counted in jobs, not minutes.
- *Filtering.* Contributor and contribution counts exclude spam-flagged accounts, staff, and bots where identifiable.
- *Geography.* Developers are mapped to countries by self-reported location with a 100-developer publication threshold. The "top countries by pushes" table is adjusted for VPN bias by using LLM classification to extract each contributor's ISO 3166-1 alpha-2 code from their profile, then weighting pushes by the ratio of profile-location to IP-address country codes.
- *Industry.* Public repositories created 2022–2026 were sorted into NAICS sectors by a fine-tuned multilingual embedding model over name, description, topics and README, from random samples per year. AI mentions and agent-opened pull requests are flagged as separate signals; the methodology notes explicitly that "sector and AI-mention shares can be related because both read the same text" and that "shares are estimates".
- *Model choice.* Figures cover GitHub Copilot and count **developer-selected requests only**, excluding auto model selection, staff usage, duplicate monitoring requests, background utility models, and requests made with a developer's own API key. A model counts only with at least 1,000 weekly active users. Models are grouped by what they are built for. Request share is the share of qualifying requests per group in a 7-day period ending 13 October 2026; trend observations use weekly data from 14 July to 13 October 2026.
- *Forecasts.* 43 time-series and regression models over historical GitHub data, sign-ups, product usage and market sizing, projecting developer counts to September 2031 relative to September 2026, grouped as 3× or more (21 models), 2× to under 3× (19), and under 2× (3). Octoverse 2025 used five models.
- *Agent detection.* The glossary defines an **agent configuration file** as "a repository file that sets up or directs an AI coding agent", an **agent signal** as "an observed sign of agent involvement in telemetry, such as an agent-opened pull request", and an **agent-started pull request** as "a pull request whose first draft came from a coding agent that we can detect". The signal is described as **a floor, since not all agent use may be detected**.

**What is not disclosed.** The methodology does not describe the classifier or heuristic that decides "this PR's first draft came from an agent", so the denominator of the headline agent-share figures is not reproducible. It does not give sampling rates for the industry classifier beyond "random samples per year", does not publish the per-year sample sizes, and does not state uncertainty intervals for any share, count or correlation. It does not provide an audit, an external verification, or a way to request the underlying records. Two figures in the report are explicitly forecast rather than measured, and are marked as such.

## Evidence

**Every figure in this section is vendor-reported by GitHub about its own platform and has not been independently audited.** The post's own Methodology section is the only methodological disclosure; it establishes definitions, filters and windows, but not measurement procedures that a third party could rerun.

**Activity in the Octoverse year (12 months ending 30 September 2026, public and private unless noted).**

| Measure | Reported value | Denominator / period |
|---|---|---|
| Pushes | 17.9 billion | 12 months ending 30 Sep 2026; post states this exceeds 2024 and 2025 combined |
| Commits | 34.3 billion | same window; reported as more than 3× two years earlier |
| Merged pull requests | 1.3 billion | same window; reported as averaging 3.5 million a day |
| Actions jobs | 45.4 billion | same window (total reported only in the post's chart; the narrative gives 1,440 jobs per second and 124 million per day) |
| Dependabot PRs merged | more than 30 million | "about double 2025's pace" |
| Push protection scans | 5.8 billion | "nearly four times 2025's pace" |
| Developers on GitHub | more than 225 million | as of the report date; United States 38.3 M, India 32.0 M, China 12.4 M |
| Public contributions | 2.5 billion | 2026; more than double last year's 1.12 billion |
| New repos' share of commits | about 55% | commits from brand-new repositories, from June onwards |

**Agent involvement in pull requests.** By September 2026, **more than 40% of pull requests on GitHub started with an agent's first draft, up from 17% in March**; the report gives this as 110 million agent-started PRs in September alone, "about 6x March's volume". Because the September figure is stated as *more than* 40%, the report's own figures do not fix an exact value.

```chart
{"type":"bar","title":"Agent-started share of GitHub pull requests","caption":"GitHub Octoverse 2026: platform-reported shares, March vs September 2026; observational and not causal.","labels":["March 2026","September 2026"],"datasets":[{"label":"Share (%)","data":[17,40]}],"yAxis":{"min":0,"max":100,"title":"Share of PRs (%)"}}
```

*Note: September is reported as **more than** 40%; 40 is the conservative lower bound used for the chart, not a precise estimate.*

The report's comparison against PRs **without detected agent involvement**:

| Condition | Agent-involved PRs | PRs without detected agent involvement |
|---|---|---|
| Changed multiple files | about 87% | 79% |
| Merged within two weeks, February 2026 | 83% | roughly 86% |
| Merged within two weeks, September 2026 | 90% | about 86% |

So the agent-involved cohort is described as merging at a higher rate by September than the comparison cohort, having started behind it in February. This is a difference between two observational cohorts that differ in composition, not a controlled comparison.

**Adoption and delegation.** Among GitHub Copilot's monthly active users, 55% now use agentic features, up from 35% a year earlier. Copilot cloud agent grew 230% year over year, against 85% for agent chat — the report's framing is that developers are moving from asking agents questions to handing over whole tasks. Public repositories mentioning interoperability or reverse engineering rose more than 300% year over year, from about 30,000 created in 2025 to more than 130,000 in 2026.

**The "eight times" commit claim.** "Among repositories created this year, the average repo with an agent configuration file logged eight times as many commits as the average new repo without one." The report presents this as a sign that "individuals and teams building with agents from day one are moving at a markedly different pace". It is a comparison of two averages over new repositories; no control for repository purpose, team size or age is offered.

**Model choice (developer-selected requests only).** In September 2026, 61% of Copilot users who selected a model themselves used more than one model across their sessions, up from 50% four months earlier. Developers on paid Copilot plans used 29 distinct models in May and 47 in September, and no single model carried more than 25% of requests that month. Of every 100 developer-selected requests, 38 went to general-purpose models, 37 to deep reasoning and planning models, and 25 to fast and lightweight models; the report notes percentages are rounded. In September 2026, 63% of paying Copilot developers used auto model selection at least once. Project HydraFusion, a research preview of model orchestration now generally available as GitHub Copilot Fusion, "routed almost 60,000 sessions" in the CLI and the Copilot app.

**Industry and language.** More than four in ten public repositories in administrative and support services, mining, health care and agriculture mention AI, yet agent-opened pull requests there are rare, "less than 3 percent". Construction breaks the pattern: about a quarter of its repositories mention AI and about 9 percent have agent-opened pull requests, the highest share of any sector. The bubble chart of language growth against detected AI involvement is reported in the post's chart with TypeScript at 134% growth and 44.1% AI involvement, Python at 118% and 41.1%, Rust at 162% and 40.4%, and Java at 30% and 21.2%; these values appear only in the chart. Among repositories created in 2026, TypeScript was the primary language in 35% of those with an observed agent signal against 24% without one; for repositories created before 2026, 27% against 17%.

**Forecasts (explicitly estimates).** 43 models were run forward to September 2031: 21 project 3× or more growth, 19 project 2× to under 3×, and 3 project under 2×. The post's chart image is captioned as showing 43 forecasts with those groupings; the chart is the source of the per-model distribution. The post itself cautions that "forecasts are estimates" and that Octoverse 2025 used five models.

## Limitations

**Stated by the source.** The methodology discloses that agent signals are "a floor, since not all agent use may be detected"; that industry and AI-mention shares "can be related because both read the same text" and "are estimates"; that prior-year figures are recalculated and may differ from earlier reports; that model-choice figures count developer-selected requests only, excluding auto selection, staff usage, duplicate monitoring, background utility models and own-key requests; that a model needs at least 1,000 weekly active users to count; and that "no forecast is perfectly accurate". The glossary defines "contributions" as activity events, with each push counted once however many commits it holds.

**Assessed by the KB maintainers.**

- **Vendor-reported and unaudited.** Every figure is GitHub reporting on GitHub. There is no third-party audit, no published dataset, no query, and no means to recompute any share from public data.
- **The detection method is the load-bearing undisclosed detail.** "Started with an agent" is defined operationally as detectable by GitHub, but the classifier is not described. Because the report's own glossary calls the signal a floor, both the numerator and the denominator of the headline share are uncertain, and the direction of the error is not recoverable: undetected agent use inflates the share, and misclassification of human PRs as agent-started deflates it.
- **Cohort comparison, not a control.** The agent-involved and "without detected agent involvement" groups differ in size, authorship and task mix. A 90% versus 86% two-week merge rate, and 87% versus 79% multi-file share, describe two populations rather than an effect of agent involvement. Nothing in the report adjusts for repository size, language, or whether the agent wrote the whole PR or only a first draft.
- **"Eight times as many commits" is a ratio of averages over selected new repositories.** Repositories with an agent configuration file are self-selected; the report offers no matching on project type, team size or repository age, and the comparison group is new repositories only, so it says nothing about established repositories.
- **Chart-only figures.** The language growth/AI-involvement bubble values, the 43-model forecast distribution, the monthly-activity multiples from September 2025, the industry share bars and the progress-toward-2030 percentages exist in the post as images with descriptive alt text; the post's narrative text gives only the headline summary of each. This page reports those values as chart captions and does not treat them as table-grade numbers.
- **Detected-AI-involvement share is a lower bound by construction**, and the report's own industry analysis shows the two signals diverging sharply — "more than four in 10 repositories mention AI" alongside "less than 3 percent" with agent-opened PRs in the same sectors — which is evidence that AI-mention and agent-activity are measuring different things.
- **Forecasts and the growth-narrative framing are separate from measurement.** The "every country closed at least a fifth of its distance to 2030" and "43 models, about half call for extreme growth" claims are model projections from a vendor's own data, and the post's framing that the 2026 surge "widened what is plausible" is an interpretation, not a measurement.
- **No defect, quality or outcome dimension.** The report measures activity: commits, pushes, PRs, jobs, scans, model selections. It contains no measure of code quality, review burden, defect rate, revert rate, or whether agent-started PRs are more or less acceptable to maintainers — the questions that would matter for whether the shift is beneficial.

## Competing approaches

The report names few alternatives, and they are named as context rather than as comparisons.

- **Chat versus delegation.** The report contrasts Copilot cloud agent, where a developer assigns a task and an agent works on it independently (230% year-over-year growth), with agent chat (85%), framing the trend as developers handing over whole tasks rather than asking questions.
- **Explicit model selection versus auto model selection.** 61% of model-selecting users chose more than one model themselves in September 2026 while 63% of paying developers used auto model selection at least once; the report presents the two as complementary, with auto selection and Project HydraFusion / GitHub Copilot Fusion routing models per step behind the scenes.
- **Model categories as alternatives.** Deep reasoning and planning (Claude Opus 5.5, GPT 5.5), general purpose (Claude Sonnet 5, Grok 4.7, GPT 6.1 Sol) and fast and lightweight (Claude Haiku 5.5, Gemini 3.8 Flash, GPT 6 Luna) are the three buckets the report groups models into for the request-share analysis.
- **Community-governed versus single-vendor projects.** The growth and engagement rankings are split into foundation-governed or independently run projects and single-vendor, product-led projects, with the methodology stating the split "describes governance and hosting, not funding or who employs maintainers".

The report names no competing measurement approach and offers no head-to-head comparison against another platform, a different telemetry method, or a controlled study.

Within this knowledge base, the report is the platform-scale observational counterpart to [[case-studies/index]] and to [[concepts/verified-completion-vs-apparent-success]]: it establishes that agent-started work is now a large share of pull requests, and establishes nothing about whether those pull requests are correct, reviewed or wanted. It is an analyst-level **compares_with** companion to [[projects/github-agentic-workflows]], which is the mechanism GitHub offers for putting agents into a repository's CI, and to [[projects/github-copilot-fusion]], which is the routing product the report names. See also [[evaluations/briefing-synthesis-2026-11-03-to-09]].

## Implications

The following is analysis by the KB maintainers, not a claim of GitHub's.

The durable lesson from this report is what it does *not* measure, and how that shapes measurement practice. Everything in it is an activity count — commits, pushes, PRs, jobs, scans — and none of it is an outcome count. A platform can report 110 million agent-started PRs in a month and say nothing about whether those PRs were accepted, reverted, or needed more review effort. The engineering consequence is that "agents did more" must never be read as "agents did better", and any team drawing conclusions from Octoverse-style telemetry should pair volume figures with acceptance, revert and cycle-time figures on the same population.

Second, the report's own glossary contains the most useful line for anyone building telemetry: an agent signal is **a floor**. The same logic applies to internal agent-detection heuristics. A detection rule produces a lower bound on agent involvement, so downstream ratios built on it inherit an unknown bias in both directions. Any internal metric of this kind should be reported with its detection coverage stated, and treated as a floor rather than a rate.

Third, the cohort comparison illustrates the selection problem that [[concepts/protocol-relative-scores]] names from another angle: the report compares agent-involved PRs to "PRs without detected agent involvement", which is not a matched control. Since "without detected involvement" includes both human-only PRs and agent PRs the detector missed, the comparison group's composition is itself uncertain. For a team running its own measurement, the fix is the same one the report applies to geography — match on observable properties (repository, size, language, task type) and report the matched result, not the aggregate.

Fourth, the "eight times as many commits" figure is a useful warning about self-selection. Repositories that adopt an agent configuration file from creation are a selected population; the ratio of averages is a description of that population, and the post's own wording ("a sign that… individuals and teams building with agents from day one are moving at a markedly different pace") stops at association. Treating it as an effect would be the exact substitution this knowledge base's [[concepts/scoped-assurance]] warns about.

Finally, the model-choice data points at a real engineering transition with a real cost structure: 47 distinct models in use among paying users, no model above 25% of requests, and 63% of paying developers letting the platform choose. The engineering consequence is that model routing becomes a first-class component with its own failure modes — a misrouted task is a silent quality regression — and it is worth instrumenting per-model outcomes rather than tracking request share alone.

## Reproducible experiment

The report is not reproducible and does not claim to be; no artifact is published. What *can* be tested independently is the report's implicit causal claim — that agent-started pull requests are being merged at least as successfully as the rest — and the claim that agent involvement concentrates in the repositories that create more.

1. **Matched-cohort merge and review-outcome comparison (the report's central claim).** Fix a cohort of repositories. Within each repository, stratify pull requests by agent-detection signal and match on size, file count, author, language and base branch. Record time-to-merge, number of review rounds, revert rate, and reviewer comment count per PR. The report's observational expectation is that agent-started PRs merge at least as fast as the rest (90% within two weeks versus about 86% in September 2026) and touch more files (87% versus 79%). The pass criterion is directional: if agent-started PRs in a matched comparison show materially *worse* merge, revert or review-comment rates, the report's favourable reading of the telemetry does not hold and the aggregate figures are confounded by composition. Pre-register the matching variables and report unmatched results alongside.
2. **Agent-signal detection coverage (the undisclosed method).** For a sample of pull requests in your own repository, hand-label which were agent-started and compare with your platform's detector. Report precision and recall, and report every downstream metric computed on the signal as a floor. A detector with materially below-complete recall makes the platform's headline shares unusable as rates; quantifying that gap is the only way to interpret such a share honestly.
3. **The "eight times" claim, matched.** Within one organisation, compare repositories that adopted an agent configuration file with matched repositories that did not, matched on age, primary language, team size and repo purpose, over the same period. The report's expectation is a large positive gap in commits. A matched gap of near zero would show that the octoverse-style ratio is selection, not pace — and would be equally informative.
4. **Review-burden measurement.** For the same cohorts, record maintainer time per PR (review duration, number of iterations, comment volume per changed file). Neither the report nor any vendor source measures this, so a first independent measurement is itself a contribution; a finding that agent-started PRs raise reviewer effort per merged change would qualify the favourable reading of the merge-rate figures.

Every result should be reported with numerator, denominator, matched-pair count, uncertainty interval, and the negative cases preserved. Substituting your own repository population for GitHub's is unavoidable and should be stated with the results.

## Evidence status

This page is grounded in a full read of the primary source — the GitHub blog post [Octoverse: Commits, pushes, reach new highs in 2026 as developers build with agents](https://github.blog/news-insights/octoverse/octoverse-commits-pushes-reach-new-highs-in-2026-as-developers-build-with-agents/), including its Glossary and Methodology sections, fetched on 2026-11-10 — together with the Octoverse index page (https://github.blog/news-insights/octoverse/) and the two product documentation pages the post links for its model-selection and stacked-PR material (https://docs.github.com/copilot/concepts/models/auto-model-selection and https://docs.github.com/pull-requests/how-tos/stacked-pull-requests), both fetched on 2026-11-10. Every quantitative result is **vendor-reported by GitHub about its own platform**: no figure was independently audited, the post publishes no dataset, query or code, and the agent-detection method that defines the headline numerator is not described in the Methodology section. Figures that exist only as chart images are reported here as chart captions, and no value has been invented for them. Claim types are separated in the text: the activity figures, the definitions, the explicit caveats and the forecast groupings are the source's; the items under "Assessed by the KB maintainers" and the whole Implications section are analysis by the KB maintainers, and the reproducible experiment is proposed and not executed. Nothing on this page was reproduced, executed or tested by the KB maintainers, and no independent audit or replication is known.

## Historical coverage

- [[briefings/2026/11/2026-11-04]] — dated full-fidelity research briefing; finding 1 selected this report.
