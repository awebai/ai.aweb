# Company Dashboard Signal Inventory

This defines the queryable surface operations and analytics need. It is
not a visual design. It is the data contract for seeing whether the
company is working.

## Core Objects

### Active Task

Source of truth: `aw task`, `aw work active`, task notes/descriptions.

Fields:

- task ref
- title
- area
- status
- priority
- builder
- reviewer
- repo/worktree
- acceptance criteria
- feedback signal
- evidence
- signal strength: `strong`, `weak`, or `unknown`
- open uncertainty
- next check
- last updated

Operational checks:

- substantial task has builder and reviewer
- task has a feedback signal
- task has a next check when evidence is not yet available
- closed task has evidence

### Claim

Source of truth: `aw workspace status`, `aw work active`.

Fields:

- task ref
- claimant alias
- workspace path
- repo
- claim age
- stale flag
- liveness

Operational checks:

- stale claims older than the task's expected cadence
- claims on tasks with no recent artifact change
- duplicate claims without explicit builder/reviewer split

### Workspace

Source of truth: `aw workspace status`.

Fields:

- alias
- area or runtime role
- path
- repo
- status
- last seen
- focus
- active claims

Operational checks:

- permanent areas have the expected active paths
- obsolete workspace records are ignored, retired, or explicitly
  tracked as legacy
- expected always-on agents have recent heartbeat

## Area Signals

### Engineering

Sources: `status/engineering.md`, repo git history, CI, release tags,
health endpoints, smoke/browser probes.

Strong signals:

- test/CI result
- deployed health/version check
- smoke or browser probe
- support/user confirmation
- conformance vectors passing across implementations

Weak signals:

- "should fix" release language without live verification
- local-only success for a deployed-service claim

### Direction

Sources: `status/product.md`, decision records, active epics/tasks,
support/outreach/analytics reports.

Signals:

- priorities mapped to active tasks
- accepted/rejected distribution or product choices
- decisions with current rationale
- task outcomes tied back to user-stage focus

### Outreach

Sources: `status/outreach.md`, `publishing/`, private outreach history,
analytics briefs.

Strong signals:

- recorded human action
- direct reply
- attributed click or signup
- practitioner conversation

Weak signals:

- traffic or signup movement with unclear attribution
- social engagement that does not convert to a conversation or product
  use

### Support

Sources: `status/support.md`, support handoff, support runbooks, user
messages.

Strong signals:

- user confirms answer worked
- issue reproduced and turned into a task
- fix shipped and user/support confirms

Weak signals:

- internal speculation about support pain
- one-off confusion without follow-up

### Operations

Sources: `status/operations.md`, `aw` status/task commands, production
health checks.

Signals:

- stale claim found and routed
- missing reviewer found and routed
- failed health check routed
- scheduled agent wake-up missed and routed
- recheck confirms discrepancy resolved

### Analytics

Sources: `status/analytics.md`, product analytics, traffic, signup,
activation, support, and outreach data.

Signals:

- measured change with clear attribution
- measured change with weak attribution
- no measurable movement after action
- missing instrumentation converted to a task

## Dashboard Views

### Operations View

- active work missing work contract fields
- stale claims
- blocked tasks
- tasks closed without evidence
- expected agents not recently seen
- live services with version/health drift

### Direction View

- current priorities and task refs
- blocked or unreviewed priority work
- distribution actions and signals
- support patterns needing product decision
- analytics questions needing a decision

### Engineering View

- release-bound tasks
- tasks requiring engineering review
- tests/CI/live checks per release
- protocol/identity tasks
- cross-repo risk

### Analytics View

- current questions
- available signals
- attribution strength
- instrumentation gaps
- recommended next measurement task

## Query Limits

The current `aw task` schema does not have native fields for builder,
reviewer, feedback signal, evidence, or signal strength. Until it does,
operations should parse the `Work contract:` block and file tasks for
missing or malformed contracts.

Long-term product implication: these fields should become first-class
task metadata so `aw` can answer queries like:

- tasks missing reviewer
- tasks closed without evidence
- active work with weak or unknown feedback signal
- stale claims by area
- release tasks missing live verification
