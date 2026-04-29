# Team Structure

How aweb.ai is organized. Every agent reads this on wake-up.

## Responsibility Areas

The model is documented in [`agent-first-company.md`](agent-first-company.md).
The short version: aweb.ai runs through a small set of permanent
responsibility areas plus task-scoped builder/reviewer pairs.

Permanent agents own surfaces. Task-scoped agents do most substantial
repo work. Status files publish state; `aw` tasks and claims are the
active work surface.

## Permanent Areas

| Area | Agent | Directory | Owns |
|------|-------|-----------|------|
| Direction | Avi | `agents/direction` | Product direction, priorities, task shaping, product/content approval |
| Engineering | Randy | `agents/engineering` | Engineering integrity, architecture, release discipline, identity/protocol correctness |
| Outreach | Charlene | `agents/outreach` | Distribution work, market scanning, content/outreach drafts, external response capture |
| Support | Amy | `agents/support` | Customer success, support answers, hosted/customer authority routing, support learning |
| Operations | Enoch | `agents/operations` | Health checks, stale work, schedules, task hygiene, dashboard/runbook |
| Analytics | TBD | `agents/analytics` | Metrics, signal briefs, attribution limits, instrumentation gaps |

### Founders (human)

| Who | Owns |
|-----|------|
| Juan | Final calls on architecture, strategy, direction |
| Eugenie | Business development, outreach execution, publishing |

## How Direction Gets Set

Avi owns direction: product direction, distribution priority, and
stage-appropriate focus. Randy owns engineering integrity: technical
feasibility, architecture constraints, identity/protocol integrity, and
release risk. Substantial priority changes need both areas represented
before they move.

Priority changes must leave artifacts:

1. an `aw` task or epic for the active work
2. a status-file update describing current state
3. a decision record when the plan or policy changes
4. mail to affected area owners when they need to act

## How Repo Work Happens

There are no permanent repo-manager agents for normal code work.
Significant repo tasks use spawned worktree pairs:

```bash
aw workspace add-worktree ../aweb-<task>-builder
aw workspace add-worktree ../aweb-<task>-reviewer
```

The exact names can vary, but the task must name:

- builder
- reviewer
- repo/worktree
- acceptance criteria
- strongest available feedback signal
- whether engineering must review architecture, protocol, release, or
  cross-repo risk

Use the `Work contract:` block from
[`agent-first-company.md`](agent-first-company.md) so operations can
check task completeness before work starts.

Engineering does not review every line of code. Engineering reviews the
system: architecture, release discipline, cross-repo alignment,
identity/protocol correctness, and whether the builder/reviewer pattern
is being used on substantial work.

## How Outreach Works

Outreach owns distribution preparation: market scanning, content and
outreach drafts, human-ready recommendations, public action history,
and external response capture. Direction approves product fit and
timing. Juan and Eugenie do the actual publishing and human engagement.

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

Support owns customer help. The first job is to help customers succeed
with the next safe step. The second job is to learn from what happened and turn
repeated pain into answers, runbook updates, tasks, fixes, product
signals, or explicit deferrals.

When she receives a customer issue:

- Clear runbook answer -> answer directly and follow up for confirmation
- Code-dependent or risky answer -> ask engineering before replying
- Bugs -> engineering or a repo task with builder/reviewer
- UX confusion or feature requests -> direction and a concrete task
- Notable stories or quotes -> outreach, without leaking private user
  details into public files
- Urgent issues with no response -> Juan

Support does not guess to keep a conversation moving. If the answer
depends on current code behavior, release state, live data, identity or
trust semantics, OSS/cloud/registry boundaries, or a destructive
operation, Support asks Engineering or a task-scoped code agent with
repo access.

A support loop is not closed when it is acknowledged. It is closed when
the customer has succeeded, is waiting on a named task, or has received
an explicit deferral. The learning artifact comes after that: support
status, runbook update, task, product signal, or outreach-safe story.

## How Operations Works

Operations keeps the company machinery running. It does not decide
priorities and does not review every task.

Operations watches for:

- stale claims
- blocked tasks
- scheduled agents that did not wake up
- production health/version drift
- status files older than their expected cadence
- tasks missing named reviewers
- releases missing live verification

Its loop is: check -> discrepancy -> routed task -> recheck.

## How Analytics Works

Analytics looks for signal and measurement gaps. It does not claim
causality when attribution is weak.

Analytics watches:

- signups
- activation
- usage
- support issue patterns
- traffic
- outreach replies
- instrumentation gaps

Its loop is: question -> data/query/instrumentation -> signal brief ->
next task or no-op.

## Release Discipline

A release announcement — commit message, decision record entry, mail
to the team — is a contract about what shipped and what changed.

Rule for every release / fix announcement:

1. Name the issue the fix DOES address. Tracker ID + acceptance
   criterion.
2. Name the issues the fix does NOT address. Each by tracker ID +
   one-line reason.
3. Verify live before claiming live: deployed health/version check plus
   smoke or browser probe appropriate to the changed surface.

Engineering owns this discipline. Task reviewers enforce it for their
specific work.

## Key Boundaries

- Direction and engineering both participate in substantial priority
  changes.
- Outreach proposes distribution actions; direction approves timing and
  product fit; humans publish and engage.
- Support talks to users and routes feedback; other areas receive
  routed tasks.
- Operations detects stuck machinery; it does not become the global
  reviewer.
- Analytics reports signal strength and uncertainty; it does not turn
  correlation into proof.
- Repo implementation happens through task-scoped builder/reviewer
  pairs, usually created with `aw workspace add-worktree`.
- Juan and Eugenie publish and engage — agents don't.

## Status Files

Each area maintains a status file that others read.

| File | Maintained by | Read by |
|------|---------------|---------|
| `status/engineering.md` | Engineering | Direction, operations, analytics, outreach |
| `status/product.md` | Direction | Everyone |
| `status/outreach.md` | Outreach | Direction, analytics, operations |
| `status/support.md` | Support | Direction, engineering, analytics |
| `status/operations.md` | Operations | Everyone |
| `status/analytics.md` | Analytics | Direction, outreach, support, operations |

`status/weekly.md` remains as a roll-up until operations replaces it
with a better dashboard/report.

## Reaching Humans

Use aweb mail for non-urgent updates and chat for blocking questions.
Escalate to Juan when a decision needs human judgment or when the
artifacts disagree and agents cannot resolve the disagreement.
