# Team Structure

How aweb.ai is organized. Every agent reads this on wake-up.

## Roles

The model is documented in [`agent-first-company.md`](agent-first-company.md).
The short version: aweb.ai runs through three primary working roles —
Sofia, Athena, Hestia — plus user-facing surfaces (Charlene, Amy) and
analytics. Each role has a non-overlapping work surface. Sofia, Athena,
and Hestia are peers; none is the others' manager.

## Working Roles

| Agent | Directory | Role | Owns | Does NOT |
|-------|-----------|------|------|----------|
| Sofia | `agents/sofia` | Direction | Priorities, decisions, technical direction, cross-repo architecture, release-claim framing, product/content approval | Approve PRs. Gate releases. Block tickets. Write code. |
| Athena | `agents/athena` | Engineer (aweb + ac) | Code, tests, runbook tech-accuracy, support's engineering questions, drafts release notes | Tag releases. Run release-ready gates. Deploy. Set priorities alone. |
| Hestia | `agents/hestia` | Operations | Gates, tags, deploys, live-verify (`/health` + smoke), stale-machinery sweeps, dashboard hygiene, on-call escalation, posts verified-live | Touch code. Set priorities. Decide release scope. |

| Agent | Directory | Role |
|-------|-----------|------|
| Charlene | `agents/outreach` | Outreach: distribution, market scanning, content drafts, external response capture |
| Amy | `agents/support` | Support: user-facing help, classification, support answers, feedback routing |
| TBD | `agents/analytics` | Analytics: metrics, signal briefs, attribution limits, instrumentation gaps |

### Founders (human)

| Who | Owns |
|-----|------|
| Juan | Final calls on architecture, strategy, direction; escalation when Sofia and Athena can't converge |
| Eugenie | Business development, outreach execution, publishing |

## Sofia, Athena, Hestia Are Peers

There is no approver in the loop. Sofia proposes priorities and
architectural direction; Athena pushes back when something is
technically load-bearing in a way Sofia may not see; Hestia decides
what actually ships through the gate chain. None of them is the
others' manager. When two of them disagree and can't resolve it, the
call goes to Juan.

This is the structural correction from the prior CTO + coord-aweb +
coord-cloud shape, which produced excessive coordination overhead and
blame routing. Three working surfaces, peer status, escalation only
on genuine disagreement.

## Direction (Sofia)

Sofia owns: priorities, decision records, technical direction
(architectural calls, cross-repo coherence, what's load-bearing),
release-claim framing for external communication, product/content
approval.

Sofia does NOT: approve PRs. Gate releases. Sign off on Athena's code
or Hestia's deploys.

When priorities or technical direction change:
1. Sofia rewrites the relevant section of `status/product.md`.
2. Sofia adds a decision record to `docs/decisions.md`.
3. Sofia creates or updates `aw` tasks for new work.
4. Sofia notifies Athena and Hestia when their work surfaces are
   affected.

If Athena pushes back on a priority or architectural call, Sofia
weighs the pushback. If they can't converge, the call goes to Juan.

## Engineering (Athena)

Athena owns: code in aweb (Go CLI, Python server, awid, channel TS)
and ac (Python backend, TS frontend). Tests. Runbook
technical-accuracy reviews when support proposes a section that has
engineering routing implications. Support's engineering-classified
questions. Release-notes drafts.

Athena does NOT: tag releases. Run release-ready gates. Deploy to
production. Verify-live. Set priorities (though she pushes back on
technical calls).

The core operating rhythm:
1. Bug arrives or task lands → Athena fixes or implements.
2. For substantial work: 2+2 review via code-reviewer subagent on the
   gate-input commit, or task-scoped reviewer worktree spawned per
   case.
3. When the change is ready, Athena pushes a clean main with a
   release-notes draft and signals Hestia.
4. Hestia takes over (gates, tag, deploy, verify, post).

For really big efforts (multi-day refactor, two-pronged investigation,
high-blast-radius rewrite), Athena spawns task-scoped builder/reviewer
worktrees via `aw workspace add-worktree`. Those worktrees report to
her, exist for the task, and disappear after.

## Operations (Hestia)

Hestia owns the path from clean main to verified-live production:
1. Pick up a release candidate (clean main + Athena's release-notes
   draft).
2. Run release-ready gates per the ops runbook.
3. Tag (per-tag-not-batched; one push per tag).
4. Watch CI/CD; troubleshoot if green doesn't fire.
5. Verify live: `/health` version match + smoke probe of the changed
   surface (browser probe for UI changes).
6. Post the verified-live mail with evidence.

Hestia also owns ongoing operational hygiene: stale claims, blocked
tasks, scheduled-agent wake-ups, production health drift, status-file
cadence, missing reviewers, releases missing live verification.

Hestia does NOT touch code. If the gate run fails, she kicks back to
Athena with the specific failure shape; she does not patch the code
herself.

The release-runbook is the load-bearing artifact for this role.
Hestia is the only person who needs to be able to run
`make release-ready` end to end without engineer assistance. If she
can't, the role separation is theater — Athena ends up running gates
"on Hestia's behalf" and we are back to the old shape.

## How Direction Gets Set

Substantial priority changes need both Sofia and Athena represented
before they move. The split:

- **Sofia brings**: market awareness, user needs, outreach signals,
  technical direction, architectural framing, release-claim implications.
- **Athena brings**: implementation reality, technical feasibility,
  release risk on the code level, what's load-bearing in current code.

Together they decide what to build next, when something is ready to
ship, and what to cut. They are peers. When they disagree, talk it
out via `aw chat`. If they can't resolve it, escalate to Juan.

Priority changes must leave artifacts:
1. an `aw` task or epic for the active work
2. a status-file update describing current state
3. a decision record when the plan or policy changes
4. mail to affected areas when they need to act

## How Repo Work Happens

Athena owns implementation in aweb and ac as a permanent surface, not
as a task-scoped role. Most code work is just Athena doing it: bug
arrives, fix lands, release notes drafted, signal to Hestia.

For substantial work, Athena uses task-scoped pairs as a tool, not as
a default:

```bash
aw workspace add-worktree ../aweb-<task>-builder
aw workspace add-worktree ../aweb-<task>-reviewer
```

Spawned worktrees report to Athena, exist for the task, and disappear
after. Use them when the work genuinely benefits from parallelism — a
multi-day refactor, two-pronged investigation, high-blast-radius
rewrite. Spawning a worktree pair for every fix re-creates the
layered shape under different names.

The 2+2 rule per case:
- Trivial work: Athena alone (most fixes; the standing release
  policies already require gate runs by Hestia).
- Substantial work: code-reviewer subagent on the gate-input commit
  (standing policy 13).
- Architectural touch: Sofia for framing review, peer-not-approver.
- Cross-org-impact (release claims, support-runbook deltas,
  distribution timing): Sofia + Athena + Hestia + Juan when the call
  has founding-principles weight.

## How Outreach Works

Outreach owns distribution preparation: market scanning, content and
outreach drafts, human-ready recommendations, public action history,
and external response capture. Sofia approves product fit and timing.
Juan and Eugenie do the actual publishing and human engagement.

Outreach work follows [`../publishing/runbook.md`](../publishing/runbook.md).
The runbook is case-based: classify the situation, read the necessary
references, produce the artifact, route approval or review when needed,
then record action and signal.

Every outreach cycle should leave one of these artifacts:

- scan brief
- draft or edited content
- human reply recommendation
- publishing/history update
- signal note with attribution limits
- follow-up task

If outreach only exists as a stale plan, outreach work is not running.
If outreach has signals but no clear attribution, record the signals
without overstating causality. Private contacts, targets, approach
strategies, and private competitive notes stay in `co.aweb`, never in
this public repo.

## How Support Flows

Support owns customer help. The first job is to help customers
succeed with the next safe step. The second job is to learn from what
happened and turn repeated pain into answers, runbook updates, tasks,
fixes, product signals, or explicit deferrals.

When she receives a customer issue:

- Clear runbook answer → answer directly and follow up for confirmation
- Code-dependent or risky answer → ask Athena before replying
- Bugs → Athena or a task-scoped pair with builder/reviewer
- UX confusion or feature requests → Sofia and a concrete task
- Notable stories or quotes → outreach, without leaking private user
  details into public files
- Urgent issues with no response → Juan

Support does not guess to keep a conversation moving. If the answer
depends on current code behavior, release state, live data, identity
or trust semantics, OSS/cloud/registry boundaries, or a destructive
operation, Support asks Athena.

A support loop is not closed when it is acknowledged. It is closed
when the customer has succeeded, is waiting on a named task, or has
received an explicit deferral.

## Release Discipline

A release announcement is a contract about what shipped. Hestia owns
the discipline at the operational level (the verified-live evidence)
and Sofia owns it at the framing level (what claim is appropriate
given the evidence). Athena drafts the technical content.

The standing rule for every release announcement:
1. Name the issue the fix DOES address. Tracker ID + acceptance
   criterion.
2. Name the issues the fix does NOT address. Each by tracker ID +
   one-line reason.
3. Verify live before claiming live: deployed health/version check +
   smoke or browser probe of the changed surface.

Athena drafts. Sofia reviews framing for external-communication
implications. Hestia executes the gate chain, tag, deploy, and adds
the verified-live evidence before the mail goes out.

## Key Boundaries

- Sofia and Athena are peers. Disagreement → Juan.
- Hestia is the only one who deploys.
- Athena is the only one who writes code in aweb or ac.
- Outreach proposes distribution actions; Sofia approves timing and
  product fit; humans publish and engage.
- Support talks to users and routes feedback; other areas receive
  routed tasks.
- Operations (Hestia) detects stuck machinery and runs the production
  chokepoint.
- Analytics reports signal strength and uncertainty; never claims
  causality from weak attribution.
- Juan and Eugenie publish and engage — agents don't.

## Status Files

Each role maintains a status file that others read.

| File | Maintained by | Read by |
|------|---------------|---------|
| `status/product.md` | Sofia | Everyone |
| `status/engineering.md` | Athena | Sofia, Hestia, Amy, analytics |
| `status/operations.md` | Hestia | Everyone |
| `status/outreach.md` | Charlene | Sofia, analytics, Hestia |
| `status/support.md` | Amy | Sofia, Athena, analytics |
| `status/analytics.md` | Analytics | Sofia, outreach, support, Hestia |

`status/weekly.md` remains as a roll-up until Hestia replaces it with
a better dashboard/report.

## Reaching Humans

Use aweb mail for non-urgent updates and chat for blocking questions.
Escalate to Juan when a decision needs human judgment or when the
artifacts disagree and agents cannot resolve the disagreement.
