# Literate Company Graph Pilot

## Status

Internal pilot brief. This is not a product commitment, customer-facing pitch,
or a plan to make Aweb Core depend on a graph database.

## One-line proposal

Pilot a read-only graph mirror for Aweb release-readiness and review/blessing
state, while keeping Aweb Core native and dependency-light.

## Thesis

Aweb Core remains the first-mile coordination product: tasks, claims, locks,
mail/chat, teams, roles, identity, verification, and raw message storage. A
graph should not be required for normal developer-team coordination.

The graph starts as a projection and intelligence layer: structured truth with
provenance, derived from Aweb coordination state, git commits, tests, reviews,
and human blessings.

This is a **literate company graph**: structured company state is queryable and
provenance-backed, while humans continue to understand and govern it through
narrative docs, messages, and review rituals.

## Why start with release readiness

Release readiness is where Aweb's current knowledge fragmentation hurts most.
During the hosted MCP/OAuth selected-org incident, the real state was
distributed across:

- Grace's patch summary
- Mia's design/blocker review
- Athena's blessing hold
- Hestia deployment gate
- chat/mail status updates
- test results
- commits/branches
- production smoke expectations

A graph mirror should answer:

> What is blessed, what is blocked, by whom, with what evidence, and what
> release includes it?

If it cannot answer that faster and more accurately than grep + inbox + status
docs, it is not yet useful.

## Source-of-truth boundary

### Native to Aweb Core

- task lifecycle
- claims and locks
- team membership
- mail/chat
- identity and verification
- raw message store
- first-mile CLI/MCP/API coordination UX

### Optional graph mirror

- derived dependencies
- review state
- blessing/release-gate state
- release-readiness state
- decision links
- service/doc impact
- evidence summaries
- generated status blocks

The graph must not introduce an ontology tax into the first-mile developer
workflow.

## Pilot mode: read-only first

The first pilot is mirror + query + generated status block only.

- Mirror canonical state from Aweb/git/test/deploy sources.
- Query that mirrored state for release readiness.
- Generate human-readable status blocks.
- Allow agents to draft proposed graph facts with confidence and provenance.
- Do not write back to Aweb Core or silently apply proposed facts.

Graph writeback, graph-authored canonical state, and branch-reviewed graph
mutations are later phases only after the pilot proves value.

## Minimum pilot ontology

Nodes:

- `Actor`
- `Team`
- `Repo`
- `Service`
- `Task`
- `Decision`
- `Blocker` / `Risk`
- `Review`
- `Blessing`
- `Release`
- `Evidence`
- `Document`

Relationships:

- `affects`
- `blocks`
- `depends_on`
- `evidence_for`
- `reviewed_by`
- `blessed_by`
- `supersedes`
- `implemented_by`

Defer deeper modeling of Customer, Capability, and Role until a concrete query
requires them.

### Review vs blessing

Do not collapse review and blessing.

- **Review** can approve, block, or comment on a diff, task, design, artifact,
  or test result.
- **Blessing** is a production-readiness or release-gate event. It says a
  reviewed change is cleared for a specific release/deploy/customer-facing
  claim.

A patch can have positive review evidence and still lack blessing.

## Provenance rules

Every graph fact should carry:

- `source_system`
- `source_id`
- evidence pointer
- `last_seen`
- `asserted_by` when asserted by a human/agent
- `reviewed_by` when reviewed
- `responsible_actor` when someone owns follow-up for the fact
- whether the fact is `mirrored`, `asserted`, or `proposed`
- review state when relevant
- confidence only for proposed/extracted facts

Mirrored facts are regenerated, not hand-edited. Human/agent edits should either
write back to the canonical source or create a separate asserted/proposed fact
with provenance and review state.

Evidence is truth-adjacent, not automatically truth. The graph stores structured
truth with provenance, not unsupported certainty.

## Evidence mirroring rules

Mirror message metadata broadly when messages are part of Aweb coordination:

- message id
- sender/recipient
- timestamp
- conversation id
- verification state
- subject/priority/waiting state
- linked task/review/blessing/release when known

Promote message bodies/snippets only by rule or human override when attached to
one of:

- blocker evidence
- review evidence
- blessing/release-gate evidence
- deploy evidence
- incident evidence
- explicit handoff evidence

Do not mirror every raw chat body into the graph by default. Raw bodies remain
in Aweb's message store unless promoted as evidence.

## Docs role

Docs remain essential, but their job changes.

Docs should explain:

- concepts
- architecture
- rationale
- playbooks
- onboarding paths
- human judgment

Docs should not manually own current operational state such as release
readiness, blessing status, active blockers, owners, or dependency status. Those
should be graph-backed/generated where possible.

Keep this sentence intact:

> Docs become an authoring surface for graph changes, not a parallel database.

Example: if a human writes, "This fix is not production-ready until stale
handoff fails closed," the system should offer to create a structured blocker
linked to the task/release, source message/doc, reviewer, and evidence.

## Human gates

Non-negotiable human gates:

- production readiness
- customer-facing claims
- policy/invariant changes
- ontology/schema changes
- security/identity semantics
- destructive graph mutations
- any decision that changes source-of-truth ownership

Agents can propose graph updates and generate summaries. Humans bless meaning
and high-impact state transitions.

## Concrete seed example

Use the hosted MCP/OAuth selected-org fix and Hestia gate cycle as seed data:

1. `Task`: hosted MCP OAuth selected-org fix.
2. `Blocker B1`: stale/invalid targeted handoff must fail closed.
3. `Evidence`: Athena mail marks current fix not production-ready.
4. `Evidence`: Mia review identifies Q2/Q1 blockers and missing tests.
5. `Commit`: Grace fix commit(s), once pushed.
6. `Review`: Mia approval or continued block on the commit set.
7. `Review`: Athena code/design review on the accessible branch.
8. `Blessing`: Athena production-readiness blessing, only after blockers/tests
   pass.
9. `Release`: Hestia gate includes the blessed commit set.
10. `Evidence`: live smoke result after deploy.

The graph should make it obvious whether the release is blocked,
reviewed-but-not-blessed, blessed-but-not-deployed, or deployed-and-smoked.

## Pilot inputs

- Aweb tasks and task comments
- aweb mail/chat metadata and rule-promoted evidence messages
- git commits/branches
- test run summaries
- review messages
- blessing messages
- Hestia deploy gates
- production smoke/check results
- relevant docs/decision records

## Pilot outputs

- readiness query: what is blocked/blessed/ready
- release query: what commits/tasks are included and what gates they passed
- evidence query: why a fix is or is not blessed
- generated status block for humans
- stale/inconsistent state warnings, e.g. "task says fixed but blessing is
  blocked"

## Anti-goals

- Do not replace Aweb tasks with a graph dependency.
- Do not require customers to understand graph schemas to coordinate work.
- Do not mirror every raw chat body into the graph by default.
- Do not make docs a second source of operational truth.
- Do not silently convert agent extraction into current truth.
- Do not add graph writeback in the first pilot.
- Do not pitch this externally before the architecture and source-of-truth
  boundaries are clear.

## Success metric

For a real release cycle, the pilot succeeds if it answers these questions
faster and more accurately than current practice:

1. What is included in the release?
2. What is blocked?
3. Who blocked or blessed it?
4. What evidence supports that state?
5. Which human gates remain?
6. Which docs/status blocks are stale?

## Suggested next step

Use the hosted MCP/OAuth selected-org fix and Hestia gate cycle as seed data.
Build the smallest read-only graph mirror that can answer the release-readiness
questions above. Keep Aweb Core unchanged.
