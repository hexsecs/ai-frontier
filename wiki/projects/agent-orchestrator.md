---
uid: 4b76268a-826f-47b3-87ad-7bbf95f72c05
title: "Agent Orchestrator (OrchestratorInc)"
summary: "Go-based fleet orchestrator running parallel coding agents in isolated worktrees with CI-repair and review escalation."
type: project
created: 2026-11-08
updated: 2026-11-10
depth: deep
sources:
  - https://github.com/OrchestratorInc/agent-orchestrator
  - https://raw.githubusercontent.com/OrchestratorInc/agent-orchestrator/main/README.md
  - https://raw.githubusercontent.com/OrchestratorInc/agent-orchestrator/main/docs/STATUS.md
  - https://raw.githubusercontent.com/OrchestratorInc/agent-orchestrator/main/docs/architecture.md
  - https://raw.githubusercontent.com/OrchestratorInc/agent-orchestrator/main/LICENSE
  - https://orchestrator.inc
  - https://docs.orchestrator.inc
  - https://github.com/OrchestratorInc/agent-orchestrator/releases/latest
---

# Agent Orchestrator (OrchestratorInc)

## What it is

Orchestrator.inc is a local desktop fleet manager for parallel coding agents — "from task to merged PR: plan, run and supervise" — whose README tagline is "Stop babysitting agents. Start merging real work." The repository `OrchestratorInc/agent-orchestrator` ships an Electron/React desktop workspace for macOS, Windows and Linux, an `ao` CLI, a Go backend daemon, and companion iPhone and Android apps. The README's framing of the problem: "One coding agent can handle a task. Running several means splitting the work, keeping branches from colliding, and following every change through CI, review, and merge."

**Product surfaces (README).** An orchestrator plans work and starts one worker per piece, each in its own worktree; a Kanban board sorts sessions into lanes ("Working, Needs you, In review, and Ready to merge") from the agent's own PR, CI and review state; failed checks, review comments and merge conflicts route back to the worker that owns the branch "until the PR is approved", with "a reviewer agent can read every PR before a person does"; the agent and model are chosen per task ("Use the agent you already trust"); and each worker gets a browser to preview and test its app. The README's supported-agents table names 36 harnesses (Claude Code, Codex, Cursor, opencode, Aider, GitHub Copilot, Grok, Kimi, Pi, Amp, Auggie, Droid, Crush, Cline, Goose, Qwen, Continue, Devin, Kiro, Kilo Code, Vibe, Muse, Agy, Autohand, Kimchi, Prime Agent, OMP, fx, Unreal Agent, MiMo Code, Gemini CLI, DeepSeek, OpenCode 2, Codewhale, Command Code, OpenHands), with "Worker, Chat, and reviewer support differ by agent". Mobile apps pair via QR code over home Wi-Fi or away from home, and "Cloud Agents" run workers in hosted workspaces ("Nothing on your machine. The code, worktrees, and agents all live in the cloud").

**Identity and maintenance.** Repository created 2026-02-13, public, primarily Go; Apache-2.0 licence; 14,407 stars, 1,960 forks, 3,989 commits as read on 2026-11-10. The latest published release is v0.14.10 (2026-11-06). Installers: macOS `.dmg` (arm64/x64), Windows `.exe`, Linux AppImage/`.deb`/`.rpm`; "The app updates itself." The README also documents its own bug-report hygiene: a local coding agent can help gather evidence with a `bug-triage` skill, "keep its logs and notes in attachments, and review the draft before submitting it yourself. Please don't have a bot file issues for you."

**Maturity (docs/STATUS.md).** "Current `main` ships a working single-user local loop: the Go daemon and the Electron/React frontend both drive a live daemon over HTTP/SSE/WebSocket. The core GitHub flow works end-to-end: add project → spawn session/orchestrator → attach terminal → observe PR → merge." The local gate is `go build ./... && go test -race ./...` plus frontend typecheck/build, with OpenAPI generated from Go DTOs and frontend TypeScript types drift-checked in CI.

## Mechanism

Read from `docs/architecture.md` and `docs/STATUS.md` on 2026-11-10. The architecture doc states its own key insight as a rule: "Display status is never stored. It is computed at read time from durable facts."

**The three-stage pipeline.** OBSERVE (external facts) → UPDATE (durable facts) → DERIVE (display status / act). The SCM observer polls GitHub/GitLab PRs every 30 seconds with lazy/non-blocking auth, per-PR ETag guards and semantic diffing; the runtime reaper polls every 5 seconds and, per the architecture doc, treats its results conservatively: "Failed probes are NOT proof of death. A session is only terminated when the runtime and process are **both** clearly dead and recent activity doesn't contradict that" — plus no merged-PR ownership. Termination fails closed.

**Workspaces and controllers.** Project sessions own isolated Git worktrees (created at `worktrees/<project-id>/<session-id>` on a temporary `ao/<session-id>/root` branch, later renamed to `ao/<slug>/root` with slugs capped at 24 characters and a four-call naming limit, falling back to the session ID); projectless standalone workers own AO-managed plain directories. Every session uses exactly one interface mode at a time: TUI sessions run agents in native PTY/ConPTY runtimes (tmux as legacy/fallback), Chat sessions run runtime-less native controllers. Codex and ACP Chat processes live in detached per-session hosts so "replacing the daemon or desktop app does not stop an in-flight turn"; a durable, capability-gated drain/interrupt handoff moves the same Claude Code or Codex native conversation between TUI and Chat "without changing the AO session/worktree", fenced by controller generations, a transition message outbox and SQLite projection. STATUS names the Chat driver set explicitly, including "Claude Code (claude-agent-acp)" — this project is a consumer of [[projects/claude-agent-acp]] — plus per-harness version requirements (Qwen Code 0.16.0+ with approval modes "verified live"; Copilot CLI 1.0.93+; OMP 15.0.0+; MiMo Code 0.1.14+ as TUI-only).

**Durable facts and the status ladder.** Only minimal facts persist (`activity_state`, `hibernated_at`, `is_terminated`, `session_mode` plus controller generation, interface transitions, and PR facts in `pr`/`pr_checks`/`pr_comment` tables). Display status derives at read time with an explicit precedence: terminated → merged; waiting/blocked → `needs_input`; then the PR pipeline (`ci_failed`, `draft`, `changes_requested`, `merge_conflict`, `mergeable`, `approved`, `review_pending`, `pr_open`); then `working`; then `no_signal`/`idle`. Chat hibernation is a process boundary with its own decision table (idle-after-settled-turn with no Chat view hibernates if Developer Mode enables it; a 10-second view lease renews, a 30-second sweep catches late-finishing turns; "Hibernation records a process boundary, not a display status").

**Chat durability.** Chat queues every message in SQLite while a provider turn is active; "Completion claims the waiting messages in enqueue order and sends them as one provider input. A steer claims the same waiting queue and appends its guidance to one active turn input"; and "An uncertain provider result closes the claimed receipts without automatically replaying input that the provider may already have accepted." Conversation authentication is projected into explicit `authenticationState` facts (`unknown`/`required`/`authenticated`), and recovery "requires an authoritative completed provider turn with no error... started and completed after the outstanding demand/account-change barrier" — imported history, process readiness or local CLI login "cannot clear a demand".

**Persistence and events.** SQLite with goose migrations and sqlc-generated queries; DB-trigger-based change-data-capture into a `change_log` table; a CDC poller and broadcaster fan out to in-process subscribers and the SSE stream at `GET /api/v1/events` with `Last-Event-ID` replay. The lifecycle manager is the canonical write path for all session facts, and PR actions are explicit API commands (`POST /prs/{id}/merge`, `POST /prs/{id}/resolve-comments`); review routes (`GET /reviews`, `POST /reviews/execute`, `POST /reviews/{id}/send`) sit behind "Interactive reviewer adapters" — 22 named in STATUS — with "Experimental reviewer selection must be explicit; native modes and prompts are not OS or network isolation."

**Security boundaries.** The daemon runs two listeners sharing one router: loopback `127.0.0.1:3001` with no authentication (all existing daemon operations), and an opt-in LAN listener on `0.0.0.0:3011` with bearer-password middleware, "only when explicitly enabled through desktop settings", its rotating password persisted mode-`0600` at `~/.ao/data/mobile/config.json`; exactly `GET /api/v1/identity` is public on LAN. Browser automation runs over a dedicated local socket (`browser.sock` / `ao-browser` named pipe) in which "The daemon owns command authorization/correlation; Electron owns the actual browser targets"; requests accept "only the exact configured renderer origins", and network capture is "off by default, bound to the active tab..., limited to 200 in-memory metadata entries, and automatically expires within at most five minutes", never bodies. The architecture doc closes with ten "load-bearing rules" (never store display status; never treat failed probes as death; never force-delete dirty worktrees; keep app state under `~/.ao`; keep the primary daemon on loopback; keep the CLI thin; CDC as the source of truth for events; adapters as leaves; hooks gitignored; never change migrations).

**Telemetry.** The README states the product "collects limited usage and reliability telemetry, never your code, prompts, agent conversations, or credentials", comprising an installation ID and GitHub username (plus AO Cloud identity if signed in), with an opt-out in Settings.

## Evidence

Inspected on 2026-11-10 over HTTPS: the repository page, README, docs/STATUS.md, docs/architecture.md, LICENSE (Apache-2.0) and the releases API (v0.14.10, published 2026-11-06).

- **Checkable from the inspected files:** every mechanism statement above — the pipeline shape, the durable-fact list, the status ladder, the observer cadences (30s SCM, 5s reaper), the listener addresses and their auth model, the worktree and branch-naming lifecycle, the Chat queue semantics, the reviewer/Chat adapter lists with version requirements, the load-bearing rules, the telemetry description — is present in those documents and checkable by any reader.
- **Vendor-stated, unverified:** all working-behaviour claims ("the core GitHub flow works end-to-end", "replacing the daemon or desktop app does not stop an in-flight turn", the Qwen approval-mode verification "verified live"). These are the project's own claims about its own software.
- **Absent from all inspected material:** any benchmark, throughput, reliability or cost result; any measure of merge rate, CI-repair success rate, parallel speedup, or reviewer-agent quality; any third-party evaluation. The repo has 14.4k stars and 1.96k forks — adoption signals, not effectiveness evidence.

## Limitations

**Stated by the project (docs/STATUS.md, "In flight / not yet a runtime feature").** Cloud availability "is gated by build configuration, account entitlement, and a reachable control plane... not unconditional availability in every desktop release"; browser-automation acceptance is partial ("macOS/Linux packaging and manual lifecycle acceptance remain release verification work"); cross-interface raw terminal history import fails closed for resume-only agents ("ACP `session/resume` preserves model context but does not replay history, so a TUI→Chat handoff fails closed for resume-only agents", and AO "deliberately does not reconstruct PTY scrollback as messages/tool cards"); "no common provider protocol serializes a currently executing tool call or detached background process for adoption by another controller"; tracker mirroring remains read-only toward issues; and full raw PR/tracker fact surfacing stays open.

**Assessed by the KB maintainers:**

- **Documentation-depth without outcome-depth.** The architecture doc is unusually rigorous for its genre, but nothing measures whether the design achieves its goal — no parallel-speedup, CI-repair success or intervention-rate figure exists anywhere in the inspected files.
- **The 35+-harness surface is a compatibility liability.** STATUS itself enumerates per-harness caveats (Qwen's approval modes, Pi's missing approval channel requiring bypass-permissions, Unreal Agent's "no interactive approval channel", experimental reviewer adapters "not OS or network isolation"). Depth of integration varies per harness and is only partially documented.
- **Two issue namespaces.** STATUS and architecture link issues and the tracking milestone to a `Untrivial-ai/agent-orchestrator` organization while the repository lives under `OrchestratorInc` — a rename or transfer the docs do not explain, and a small but real signal that documentation drift exists in the operational docs.
- **Single-user, local-first.** STATUS scopes the shipped loop to "single-user local" mode; multi-user and cloud behaviours are gated or in flight.
- **Direct-LAN plaintext.** The architecture doc is explicit that "Direct LAN transport remains plaintext" (with managed cloudflared/Tailscale wrapping optional) — the trust model leans on "trusted networks", stated as such.

## Competing approaches

The inspected sources name no alternative orchestration framework or competitor product. What they do name as contrasts:

- **An always-running supervising model versus event-driven reactions.** The architecture's feedback routing reacts to observed CI failures, review comments and merge conflicts rather than supervising continuously — the README's "Stop babysitting agents" is the positioning against constant human (or model) supervision.
- **One interface mode versus multi-interface sessions.** "Every session uses one interface mode at a time" with durable handoffs, versus designs that keep terminal and chat controllers live simultaneously — the architecture doc says both controllers are "never live at once".
- **Cloud execution versus local execution.** The README's Cloud Agents section presents hosted workspaces as the alternative to "your code stays on your machine".

Analyst-level comparisons within this KB — [[projects/agensh]] and [[projects/github-agentic-workflows]] — exist in [[evaluations/briefing-synthesis-2026-11-03-to-09]]; the completion problem it manages is covered by [[concepts/verified-completion-vs-apparent-success]], its improvement posture by [[concepts/preservation-aware-agent-improvement]], and the wider workflow corpus is [[workflows/index]]. These are analyst-selected comparisons, not source-verified dependencies.

## Implications

The following is analysis by the KB maintainers, not a claim of the authors.

The transferable core is the **durable-facts/derived-status split with a fail-closed termination rule**. Persistence is minimal and append-oriented; everything a user sees is computed; and the two dangerous transitions — terminating a session and treating a failed probe as death — are both made structurally conservative ("Failed probes are NOT proof of death"; terminate only on runtime-and-process dead with no contradicting activity and no merged-PR ownership). This is [[concepts/structural-constraint-over-instruction]] applied to fleet supervision: the system is designed so its most irreversible action (killing a worker) has the highest evidential bar.

The second lesson is **interface handoff as controller replacement with fencing**. Moving a Claude Code conversation between terminal and chat without losing the worktree, the PR or the in-flight turn requires exactly the machinery this project documents: controller generations to fence stale events, a durable outbox for messages arriving during the no-controller gap, and a "context boundary" publication that refuses to claim continuity it cannot prove ("Prior rows remain intact, but are not represented as context inherited by the new provider"). That last honesty rule — do not represent inherited context you did not verify — is the [[concepts/verified-completion-vs-apparent-success]] discipline applied to UI state.

Third, **the queue semantics for steering** (completion claims waiting messages in enqueue order; a steer appends to the active turn; an uncertain result closes receipts without replay) are a concrete answer to double-delivery under provider uncertainty — the failure mode where a retried message becomes a duplicated instruction.

The counterweight: this is a well-documented mechanism with zero published outcome measurement, and its genre — desktop fleet orchestration — is exactly where anecdotes substitute for evidence. The project's own STATUS honesty ("what currently ships on `main` and what remains in flight") is the right epistemic posture; nothing here says the fleet *merges real work* faster than one well-driven agent would.

## Reproducible experiment

Proposed, not executed; all arms need a test repository with CI and at least two installed harnesses.

1. **CI-repair routing.** Seed a failing check on a worker's PR and record the nudge path (SCM observer → lifecycle → mode-aware messenger). Pass criteria: the owning worker receives the failure within one 30-second poll; a session whose PR has no failure receives nothing; a PR owned by no session generates no nudge.
2. **Termination guardrail.** Kill a runtime process out-of-band and verify the session is not marked terminated while the process supervisor still reports liveness, and vice versa: a failed probe must not terminate. Pass criterion: termination requires both dead-runtime evidence and no recent activity, per the architecture's guardrail chart.
3. **Handoff fidelity.** Start a Claude Code TUI session mid-task, switch to Chat, and compare the native conversation id, worktree, PR ownership and branch before and after. Pass criteria: same session row, same PR, no controller-generation regression (old Chat events fenced), and the context boundary published rather than claimed continuity.
4. **Parallel speedup.** Author a small task set; run one agent versus a fleet of three on the same project, with a two-retry CI-repair cap. Track merge-ready PRs per dollar and human interventions per PR. Pass criterion: the fleet matches or beats the single agent without worktree conflicts or repair loops; a fleet that loses on interventions falsifies the product's premise.
5. **Status derivation conformance.** Construct sessions hitting each ladder rung (waiting_input, ci_failed, changes_requested, merge_conflict, mergeable, approved, working, idle) and assert the board lane matches the documented precedence. A stored status or an out-of-order precedence fails.

## Evidence status

Grounded in HTTPS reads on 2026-11-10 of the repository page, README, docs/STATUS.md, docs/architecture.md, LICENSE and the releases API; no code was executed, installed, cloned or benchmarked by the KB maintainers. **Inspected and checkable:** all mechanism statements above, which any reader can verify against the same public documents. **Vendor-stated:** every working-behaviour claim (the end-to-end GitHub flow, in-flight-turn survival across daemon replacement, the Qwen approval-mode verification, hibernation behaviour). **Not present anywhere in the inspected material:** benchmarks, throughput, reliability, cost, merge-rate or reviewer-quality results, or any independent evaluation. The Implications and assessed-Limitations sections are analysis by the KB maintainers; the reproducible experiment is proposed and not executed.

## Historical coverage

- [[briefings/2026/11/2026-11-08]] — the dated full-fidelity research and cross-project synthesis briefing that first ingested this repository.
- [[projects/claude-agent-acp]] — the Chat driver this project names for Claude Code sessions (source-verified dependency direction: agent-orchestrator documents consuming claude-agent-acp).
