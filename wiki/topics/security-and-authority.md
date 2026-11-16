---
type: index
title: "Security and authority"
summary: "Locate enforcement boundaries and distinguish permission from instruction."
---

# Security and authority

Which actions may an agent take, where is that boundary enforced, and what happens when evidence is missing?

## Start here

[[concepts/delegated-authority-and-revocation]] introduces grant scope, ceilings and revocation. [[projects/sopguard]] concerns a separate cross-origin information-flow boundary. [[experiments/lifecycle-authority-and-retention]] specifies bounded fault injection.

1. [[concepts/structural-constraint-over-instruction]] — Distinguish model instructions from externally enforced limits.
2. [[techniques/secure-agent-operations]] — Compare concrete enforcement surfaces and their coverage.
3. [[techniques/gated-admission-and-revalidation]] — Separate tool admission from authorization of each use.

## Compare boundaries

| Boundary | Reading | Limitation to retain |
|---|---|---|
| Runtime action and network policy | [[projects/strands-box]], [[projects/openbot]] | Enforcement depends on mediated routes and configured policy. |
| Tool catalog and invocation | [[projects/toolguardian]], [[projects/a2ui-and-copilotkit]] | A trusted catalog does not prove every permitted operation is appropriate. |
| Planning before untrusted observations | [[projects/baya-compile-then-execute]] | Precompiled branches constrain adaptation as well as attacks. |
| Bounded browser actions | [[projects/fastbrowse]] | Developer-run comparisons are not independent security guarantees. |
| Measured harness behavior | [[projects/agenticbench]], [[projects/harness-matters-web-agent-security]] | Results are bounded by the tested harness stages and attacks. |

## Counterevidence and experiments

[[projects/security-impact-of-coding-agent-memory-files]] bounds broad claims about instruction-bearing memory. [[projects/assuring-ai-written-software]] illustrates why a named safeguard is insufficient without evidence it ran. [[topics/verification-and-evaluation]] covers checker reliability; [[topics/agent-execution-and-recovery]] covers fail-closed recovery.
