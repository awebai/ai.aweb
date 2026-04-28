# Agent-First Company Model

This is the operating model for aweb.ai.

The company is organized around responsibility areas, shared artifacts,
and review contracts. Agents should not need a management hierarchy to
know what to work on, what evidence matters, who reviews the work, or
when a human decision is required.

Epic: `aweb-aals` — Reorganize company agents around responsibility
areas.

## First Principles

### 1. Work Needs Artifacts

If work matters, it needs a durable artifact:

- an `aw` task for active work
- a claim for who is working on it
- a handoff for context that must survive agent restarts
- a status file for the current published state
- a decision record when direction changes
- a release, support, or outreach note when an external claim changes

Conversation is not enough. Handoff prose is not enough. A status file
is not a work queue.

### 2. Substantial Work Needs Two Agents

Every substantial effort needs at least:

- **Builder**: produces the artifact, implementation, draft, or plan
- **Reviewer**: checks it against the goal, invariants, evidence, and
  acceptance criteria

For code this means builder plus code/release reviewer. For company
work it means proposer plus approver, writer plus reviewer, or support
classifier plus product reviewer. The point is the same: agents working
alone produce plausible wrong things.

Trivial work can skip the full two-agent path, but the default should
be two-agent verification whenever the work changes product direction,
external messaging, release framing, customer support language, or
shared process.

### 3. Responsibility Areas Own Surfaces

An agent owns a responsibility area when it owns the surface where
problems appear and the artifacts that keep that surface legible.

Ownership means:

- know what state must stay current
- know what evidence is relevant
- create or update tasks when work appears
- identify the builder and reviewer for substantial work
- route decisions to the right human or agent
- say when the evidence is incomplete

Ownership does not mean proving clean cause and effect. In many company
systems, cause and effect will be ambiguous. The job is to keep the
surface legible enough for good judgment and fast correction.

### 4. Shared State Beats Status Routing

The company should be queryable through shared state:

- tasks and claims show active work
- mail/chat capture coordination and decisions in motion
- status files publish current state
- handoffs preserve area-specific memory
- decision records preserve changes in direction
- release gates and support attestations prove specific claims against
  reality

The standard is not perfect attribution. The standard is that any fresh
agent can inspect the artifacts and understand what is happening, what
is blocked, what was decided, and what needs review.

### 5. Look For Feedback, Grade Its Strength

Sales calls, support messages, outreach replies, live health checks,
git history, task claims, and user behavior are signals. Agents should
capture and route them, but not pretend they settle causality by
themselves.

Always look for feedback. Prefer feedback that is verifiable and close
to the work:

- code change -> test result -> fix
- release -> deployed health/version check -> smoke test
- support answer -> requester confirms it worked
- outreach action -> recorded reply/no-reply/traffic/signup signal

Some feedback is strong enough to close a claim. Some is only weak
signal. A social post followed by more signups might matter, but it is
not clean proof that the post caused the signups. Capture the signal,
note the uncertainty, and use it to shape the next task.

When evidence is ambiguous, the correct artifact is often an open
question or a task with explicit uncertainty, not a confident plan.

## Operating Rules

### Use `aw task` For Active Work

Every non-trivial active company effort gets an `aw` task. If the
effort has multiple parts, create an epic and subtasks.

Use tasks for product, docs, outreach, support, release, and process
work. Engineering is not special here; it is just the most obvious case.

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
artifact that supports it: task, commit, health check, attestation, or
decision record.

When the evidence is weak, say that directly. "Post got traffic but no
attributable signups yet" is useful. "Post worked" is not.

### Use Decision Records For Direction Changes

When the operating model, product priority, release policy, or public
claim changes, write a decision record. Status files describe current
state; decision records explain how and why state changed.

## Responsibility Areas

| Area | Agent | Owns |
| --- | --- | --- |
| Direction | Avi | Product direction, distribution priority, user-stage focus, company-level product tasks |
| Engineering integrity | Randy | Architecture quality, release discipline, cross-repo engineering alignment |
| Attention | Charlene | Content pipeline, outreach monitoring, market signal capture |
| User feedback | Amy | User support, support language, feedback routing |
| Accountability | Enoch | Reality checks against status claims, stale-work detection, hard questions |
| OSS repo integrity | John | aweb code review, invariant enforcement, release readiness |
| Cloud repo integrity | Tom | ac code review, hosted/OSS alignment, release readiness |
| Identity integrity | Goto/John | awid protocol and registry correctness |

## Work To Do

### Make Active Work Queryable

- Convert current company priorities into `aw` tasks/subtasks.
- Require every status file's current focus to reference active task
  refs where appropriate.
- Define the reviewer/approver for each active task.

### Keep Responsibility Areas Operational

- Keep `agents/<area>/AGENTS.md` focused on that area's work surface,
  artifacts, and review expectations.
- Keep `agents/<area>/handoff.md` focused on area memory and next
  checks.
- Route work through artifacts and reviewers.

### Build The Company Dashboard

The dashboard should show:

- active tasks and claims
- stale claims
- release gates and live versions
- unanswered decision questions
- user feedback needing routing
- outreach briefs/actions and observed signals
- agent liveness

This is not an executive dashboard. It is the company's shared
coordination state.

## Operating Standard

The operating standard is high-throughput verified work: useful
artifacts per unit of time and money, with enough shared context and
review to correct course quickly when the evidence is incomplete or
misleading.
