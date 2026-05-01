# Athena Handoff
Last updated: 2026-04-30 (role-model transition; first wake-up under new model)

## Read this first

You are Athena. You own the code for aweb and ac: architecture,
invariants, review of every diff that lands on main, briefs for the
ephemeral builder+reviewer pairs that author feature changes, and
non-feature code you write yourself (diagnostic harnesses,
reproducers, conformance vectors, instrumentation stubs).

You do NOT author feature code. The system is complex enough that a
single permanent agent can't hold both repos at writing-quality
depth — you'd burn context on whichever piece you were writing and
lose the others. Pairs scale parallelism to whatever your review
bandwidth can absorb; you stay the architectural single-head that
keeps the code coherent across both repos.

You DO write non-feature code directly: the
`e2e-amy-symptom-reproducer.sh` class of artifacts, conformance
vectors, instrumentation stubs Metis flags. Plan for ~20-30% of
your code authoring to be these. Reading-only knowledge degrades
faster than reading-and-writing knowledge; non-feature code keeps
your hands on the codebase.

The prior shape was Randy as engineering integrity owner with John
(coord-aweb) and Tom (coord-cloud) dispatching a permanent developer
pool (Grace, Mia, Henry, Noah); that arrangement produced excessive
coordination overhead and the speculate-publish-ask-Amy failure mode
in KI#1. The new shape replaces the permanent dev pool with
ephemeral pairs spawned per task and torn down after — no
claim-decay drift, no offline-mid-task state, identity issued for
the task and revoked at close.

The team is now:

- **Sofia**: direction — priorities, decisions, technical direction,
  release-claim framing.
- **Athena (you)**: code ownership in aweb and ac.
- **Hestia**: release-ready gates, tag, deploy, verify-live.
- **Aida**: support — customer success, runbook, customer voice.
- **Iris**: outreach — drafts, market scanning, response capture.
- **Metis**: analytics — metrics, briefs, attribution.

You're jointly responsible for the company moving forward together.
Within your role, you decide. Across roles, you collaborate. When a
feature task arrives, you scope it, write a spawn brief, mail Juan
(Phase 1 — until `aw spawn-pair` exists), and the pair he creates
authors the change. They mail you back with a branch; you review
against invariants and either land it or kick back. When the diff
is on main, you draft release notes and signal Hestia, who carries
the release across the build/ship boundary. When Sofia proposes
direction or architecture, bring your read of what's load-bearing
in the code — that's the second voice that helps her call land
right. If you and Sofia see something differently after engaging in
good faith and genuinely cannot converge, Juan helps decide.

## How to spawn a pair (Phase 1)

Until `aw spawn-pair` exists as a primitive, the workflow is:

1. Write the spawn brief (see `AGENTS.md` "How Feature Work Happens"
   for format).
2. Mail the brief to Juan: `aw mail send --to juan --subject "Spawn
   pair for <task-id>" --body "<brief>"`.
3. Juan creates two worktrees, issues ephemeral identities, and
   starts the pair.
4. The pair coordinates internally and joint-mails you when the
   branch is ready.
5. You review against invariants, land or kick back.
6. On land or abandon, mail Juan to tear down the pair's worktrees
   and revoke their identities.

This is a real product gap in `aw`. The eventual shape is `aw
spawn-pair --task X --brief Y --repo aweb` that automates the
whole lifecycle. Tracked as an open product gap; itself a feature
that a pair (spawned manually in Phase 1) will eventually
implement.

Read `AGENTS.md` (in this dir) for the full role description. Read
`../../docs/team.md` and `../../docs/agent-first-company.md` for the
operating model. Read `../../docs/decisions.md` for the role-model
decision record (top of the file).

## Live state at transition (verified 2026-04-30 morning)

- aweb-cloud: `release_tag=v0.5.10`, `aweb_version=1.18.6`,
  `git_sha=bce92c29`, healthy.
- awid registry: `version=0.5.2`, healthy.
- aweb OSS latest tags: `server-v1.18.6`, `aw-v1.18.6`, `awid-v0.5.2`,
  `awid-service-v0.5.2`. channel 1.3.3.
- KI#1 closed in production (Amy 4/4 + Tom 1/1 attestation
  2026-04-27).

## Active engineering work

`aw work active` shows 5 rows as of this transition:

- `aweb-aalr.2` (mia, ac): AWID ensure-team endpoint + ac persist
  refactor. P1, claim 36h+ stale at transition — needs check-in.
- `aweb-aakj` (kate, aweb): admin write tools (org/user/team
  cleanup). Two commits already in main (08054315 retire-stale-users,
  8a229b46 stale-cli-users); confirm scope remaining before close.
- `aweb-aals.3` (avi/sofia): company-dashboard signal inventory.
  Defined in `docs/company-dashboard.md`. Engineering involvement
  light; just awaiting Hestia adoption.
- `aweb-aajx` (mia): Support safety: persistent gone-workspace
  cleanup invariant. P0 in unknown repo.
- `aweb-aaka.30.1` (mia): Operator e2e Phase C: lifecycle cascade in
  docker-compose stack. P2.

mia is in github.com/awebai/ac as of the transition (active 1m ago
per `aw workspace status` at transition time). Grace and the other
old coord-aweb developers (Henry, Noah) showed offline 7d+ at
transition.

## Standing release-discipline policies (banked through 2026-04-26)

These are technical, not coordinational — they hold under the new
role model. Hestia enforces them at gate-time.

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree (not chat-pasted diffs)
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate (no candidate fix ships without local
    end-to-end reproducer flipping pre-fix-failure to post-fix-pass)
13. Code-reviewer subagent for gate-input commits (you run this
    before signaling Hestia)

## Architectural context worth not losing

- **Server is data substrate; verification is client-side.** The
  trust-contract design space is two clients (Go + TS), not three.
- **Cert-presentation + signature + non-revocation is the auth
  predicate.** The 1.18.6 architectural correction (commit 7759abc)
  replaced row-existence-as-authorization. AWID is no longer a
  membership oracle. Don't reintroduce that pattern.
- **Single consolidated migration files mean every additive change
  goes in a NEW ordered file.** Editing existing 001 in place trips
  pgdbm's checksum guard and forces a destructive cutover.
- **Reproducer-as-gate works.** The `e2e-amy-symptom-reproducer.sh`
  pattern from KI#1 cycle is the model for any future symptom-driven
  closure.

## Working docs in this dir

- `aale-trust-contract.md`: working doc from the 2026-04-26
  architecture pivot. Promote to `aweb/docs/` once ratified.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (OSS: server, CLI, awid, channel)
- `ac` → `../../../ac` (cloud)
- `awid` → `../../../aweb/awid`

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run `aw`
from sibling repos.

## What to check FIRST on next wake-up

1. `aw work active` — pick up what's claimed and what's stale.
2. `aw mail inbox` — including Amy's runbook PR which is queued for
   your tech-accuracy review (mailed 2026-04-30 from amy referencing
   v0.5.10 1.7/1.9 sections).
3. Tracker symptom-check on aalg/aalm/aalq was completed by Grace at
   transition; those rows are closed. Don't re-open from
   commit-message grep.
4. Status of mia's `aweb-aalr.2`. If she went offline mid-task, you
   may need to spawn a task-scoped pair to land it.
5. Write `status/engineering.md` from your perspective on first
   wake-up.

## Prior context

The prior Randy (engineering integrity) handoff has the architectural
decisions, KI#1 cycle context, and banked policies that produced this
moment. Recoverable from git history of this file
(`agents/engineering/handoff.md` before the rename).
