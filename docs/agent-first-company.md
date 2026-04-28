# Agent-First Company Model

This is the operating model for aweb.ai.

The company is organized around a small set of permanent responsibility
areas, task-scoped builder/reviewer pairs, and feedback loops. Permanent
agents own surfaces and keep work legible. They are not a management
hierarchy.

Epic: `aweb-aals` — Reorganize company agents around responsibility
areas.

## First Principles

### 1. Work Needs Artifacts

If work matters, it needs a durable artifact:

- an `aw` task for active work
- a claim for who is working on it
- a named reviewer for substantial work
- a handoff for context that must survive agent restarts
- a status file for the current published state
- a decision record when direction changes
- a release, support, outreach, operations, or analytics note when an
  external claim changes

Conversation is not enough. Handoff prose is not enough. A status file
is not a work queue.

### 2. Substantial Work Needs Two Agents

Every substantial effort needs at least:

- **Builder**: produces the artifact, implementation, draft, answer,
  instrumentation, or plan
- **Reviewer**: checks it against the goal, invariants, evidence, and
  acceptance criteria

For code, spawn task-scoped builder and reviewer agents in repo
worktrees with `aw workspace add-worktree`. For company work, the pair
may be outreach plus direction, support plus engineering, analytics
plus direction, or operations plus the area owner.

The reviewer belongs to the task. There is no permanent review agent
for everything.

### 3. Permanent Agents Own Surfaces

The permanent areas are:

| Area | Agent | Owns |
| --- | --- | --- |
| Direction | Avi | Product direction, priorities, task shaping, product/content approval |
| Engineering | Randy | Engineering integrity, architecture, release discipline, identity/protocol correctness |
| Outreach | Charlene | Distribution work, market scanning, content/outreach drafts, external response capture |
| Support | Amy | User-facing help, issue classification, support answers, feedback routing |
| Operations | Enoch | Company machinery: health checks, stale work, schedules, task hygiene, dashboard/runbook |
| Analytics | TBD | Metrics, signal briefs, attribution limits, instrumentation gaps |

Ownership means:

- know what state must stay current
- know what feedback loop belongs to the surface
- create or update tasks when work appears
- identify builder and reviewer for substantial work
- route decisions to the right human or agent
- say when evidence is weak or missing

### 4. Repo Work Is Task-Scoped

There are no permanent repo-manager agents for normal code work.
Significant repo work gets a task-scoped pair:

```text
Task: implement or fix X in aweb/ac/awid
Builder: spawned worktree agent
Reviewer: separate spawned worktree agent
Engineering: involved for architecture, protocol, release, or cross-repo risk
Feedback signal: tests, CI, health check, smoke/browser probe, user/support confirmation
```

Use `aw workspace add-worktree` to create isolated repo workspaces for
builder and reviewer agents. The pair owns the local correctness of the
task. Engineering owns systemic risk, release discipline, and protocol
integrity.

### 5. Shared State Beats Status Routing

The company should be queryable through shared state:

- tasks and claims show active work
- mail/chat capture coordination and decisions in motion
- status files publish current state
- handoffs preserve area-specific memory
- decision records preserve changes in direction
- release gates, support confirmations, operations checks, and
  analytics briefs prove or qualify claims against reality

The standard is not perfect attribution. The standard is that any fresh
agent can inspect the artifacts and understand what is happening, what
is blocked, what was decided, what needs review, and what signal exists.

### 6. Look For Feedback, Grade Its Strength

Every agent archetype must look for feedback as part of its task. The
loop differs by area:

| Area | Loop |
| --- | --- |
| Engineering | code -> tests/CI -> fix; release -> health/smoke/browser probe |
| Direction | priority -> shipped artifact/action -> user/support/outreach/analytics signal |
| Outreach | draft/action -> human publish/engage -> replies/clicks/traffic/signups signal |
| Support | user issue -> answer/fix/task -> user confirms or issue remains open |
| Operations | check -> discrepancy -> routed task -> recheck |
| Analytics | question -> data/query/instrumentation -> signal brief -> next task or no-op |

Some feedback is strong enough to close a task. Some is only weak
signal. A social post followed by more signups might matter, but it is
not clean proof that the post caused the signups. Capture the signal,
note the uncertainty, and use it to shape the next task.

When evidence is ambiguous, the correct artifact is often an open
question or a task with explicit uncertainty, not a confident plan.

## Operating Rules

### Use `aw task` For Active Work

Every non-trivial active company effort gets an `aw` task. If the
effort has multiple parts, create an epic and subtasks.

Tasks should include:

- the desired result
- acceptance criteria
- the strongest available feedback signal
- the expected builder
- the expected reviewer or approver
- open uncertainty
- labels that make the work discoverable

### Use Claims To Prevent Duplicate Work

Agents should claim substantial work before doing it. Before claiming,
check:

```bash
aw workspace status
aw work ready
aw work active
```

If work is already claimed, coordinate rather than starting a parallel
version from memory.

### Keep Handoffs As Memory, Not Queues

Handoffs should answer:

- what changed since the last wake-up
- what context is not obvious from tasks/status/decisions
- what to check first next time
- what conversations or risks are in progress

They should not be the only place active work exists.

### Keep Status Files As Published State

Status files are what other agents read to understand current state.
They should be current, concrete, and short enough to scan. If a status
file says something is blocked or live, that claim should point to the
artifact that supports it: task, commit, health check, attestation,
analytics brief, operations check, or decision record.

When the evidence is weak, say that directly. "Post got traffic but no
attributable signups yet" is useful. "Post worked" is not.

### Use Decision Records For Direction Changes

When the operating model, product priority, release policy, or public
claim changes, write a decision record. Status files describe current
state; decision records explain how and why state changed.

## Work To Do

### Make Active Work Queryable

- Convert current company priorities into `aw` tasks/subtasks.
- Require current-focus status sections to reference active task refs
  where appropriate.
- Define the builder, reviewer, and feedback signal for each active
  task.

### Keep Permanent Areas Operational

- Keep `agents/<area>/AGENTS.md` focused on that area's work surface,
  artifacts, feedback loop, and review expectations.
- Keep `agents/<area>/handoff.md` focused on area memory and next
  checks.
- Route implementation work through task-scoped builder/reviewer pairs.

### Build The Company Dashboard

The dashboard should show:

- active tasks and claims
- stale claims
- tasks missing reviewers
- tasks closed without feedback evidence
- release gates and live versions
- production health checks
- support issues needing routing
- outreach actions and observed signals
- analytics briefs and instrumentation gaps
- agent liveness

This is not an executive dashboard. It is the company's shared
coordination state.

## Operating Standard

The operating standard is high-throughput verified work: useful
artifacts per unit of time and money, with enough shared context,
review, and feedback to correct course quickly when the evidence is
incomplete or misleading.
