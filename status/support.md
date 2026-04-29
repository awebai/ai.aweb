# Support Status
Last updated: 2026-04-29 09:06 CEST

## Current focus

Support owns customer success first and learning second. The immediate
operating standard is: get the customer to a safe next step, ask
engineering before guessing on code-dependent answers, then record the
feedback signal or task that came out of the support case. Tracking
task: `aweb-aals.8`.

## Open customer blockers

- No new external user issues are recorded in this public status.
- Existing support-runbook work remains in the support handoff and
  `docs/support/`.

## Waiting on engineering

- `aweb-aaka.34`: decide and implement hosted/custodial support
  tooling outside customer `aw`. `aw` must remain a customer/key-holder
  CLI, not an admin support surface. Until the hosted support surface is
  clear, Support asks Engineering for cloud state that the customer or
  support agent cannot inspect with their own authority.

## Closed customer loops

- KI#1 was marked closed in recent support/cloud handoffs after
  empirical attestation. Engineering should keep release evidence
  current in `status/engineering.md`.

## Learnings and patterns

- Support should route every repeated user pain into a task with an
  owner, reviewer, and feedback signal, but only after the customer has
  a path forward or is explicitly waiting on a named task.
- If the safe customer-facing answer depends on current code behavior,
  release state, live data, identity/trust semantics, or a destructive
  operation, Support asks Engineering before replying.
- Ask self-custodial/BYOD customers to run `aw` themselves because
  they hold the keys. Do not ask hosted custodial customers to run
  `aw`; they usually do not have it.
