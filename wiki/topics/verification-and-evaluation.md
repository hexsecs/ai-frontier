---
type: index
title: "Verification and evaluation"
summary: "Establish success and compare evidence under explicit measurement conditions."
---

# Verification and evaluation

What establishes task success, how reliable is the grader, and when can scores be compared?

## Start here

[[concepts/contracts-and-compositional-correctness]] distinguishes local checks from integrated obligations. [[projects/alphaproof-code]] supplies a formal-checking example bounded by specification trust in [[concepts/scoped-assurance]].

1. [[concepts/verified-completion-vs-apparent-success]] — Ask what outcome was independently checked.
2. [[concepts/scoped-assurance]] — Bound the result by the scope exercised.
3. [[concepts/protocol-relative-scores]] — Match feedback, attempts, budgets and scoring rules.
4. [[techniques/verification-and-evidence]] — Select concrete checking mechanisms.

## Choose the right evidence question

| Question | Reading |
|---|---|
| Is the judge inside the system being graded? | [[concepts/evaluator-circularity]] |
| Is the reference itself reliable? | [[concepts/ground-truth-fallibility]] |
| Was the comparator faithfully constructed? | [[concepts/comparator-construction-shapes-margins]] |
| Does the framing exceed the evidence tier? | [[concepts/validation-tier-gap]] |
| Can the output be traced to its origins? | [[techniques/artifact-and-claim-provenance]] |
| What should happen when evidence is insufficient? | [[concepts/abstention-as-first-class-verdict]] |

## Instruments, counterexamples and tests

[[benchmarks/index]] groups instruments by what they measure. [[projects/assuring-ai-written-software]] provides a field case about the gap between declared and executed safeguards; it is not a population estimate. [[experiments/independent-acceptance-regression-ingestion]] specifies a proposed blind acceptance test. [[topics/coordination-and-orchestration]] explains additional controls needed when evaluating teams.

## Execution behavior and real-world acceptance

[[projects/coding-agent-behavioral-trajectories]] makes normalized agent actions observable without treating them as proof of success; compare [[projects/procgrep]] for a distinct fingerprinting method. [[projects/abc-bench-backend-coding]] moves acceptance to deployed services and external API tests, while [[projects/agenticdatabench]] evaluates coverage across data-workflow skill combinations. These are different measurement constructs, not comparable leaderboard scores.
