# Support Status
Last updated: 2026-04-30 (post v0.5.10 deploy)

## Current focus

Support owns customer success first and learning second. The immediate
operating standard is: get the customer to a safe next step, ask
engineering before guessing on code-dependent answers, then record the
feedback signal or task that came out of the support case. Tracking
task: `aweb-aals.8`.

Cloud rolled forward to **v0.5.10 / aweb 1.18.6** on 2026-04-30 05:54 UTC
(release_tag=v0.5.10, git_sha=bce92c29). Per Randy's commit-traced
review (mail 320be732), v0.5.10 layered auth-gate + personal-org
invariants + admin write tools. Three customer-visible runbook deltas
to land in the next runbook PR:

1. **1.9 NOT-boundary**: pre-v0.5.10 personal teams may need
   operator-run AWID backfill. If a customer hits cross-team-cert
   weirdness on a pre-v0.5.10 account, route to engineering — do NOT
   tell them to retry from the dashboard.
2. **New login-failure section** (1.6 or 1.12): cover the new
   `email_unverified` and `account_inactive` error codes users now see
   distinctly at login (substance commit 20872ccf).
3. **Namespace-claim collision messaging**: AWID controller conflicts
   are now HTTP 409 + structured body (commits 3f9938d0 + 668a9dbd),
   surfaced in CreateOrganizationDialog.tsx and OwnerSelector.tsx. If
   1.9 covers org/namespace creation, cite the 409 shape.

Sections 1.7 (conversation policy) and 1.9 (create-new-agent) happy
paths fill from the existing plan unchanged per Randy's verdict.

## Open customer blockers

- No new external user issues are recorded in this public status.
- Existing support-runbook work remains in the support handoff and
  `docs/support/`.

## Waiting on engineering

- Hosted custodial cases that require cloud state are Engineering
  escalations until Engineering provides a support-facing procedure.

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
  they hold the keys for keyed/local operations. Support can run
  non-keyed public `aw` reads on the customer's behalf when the
  customer provides the target DID or address. Do not ask hosted
  custodial customers to run `aw`; they usually do not have it.
