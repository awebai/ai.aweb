# Coordinator aweb OSS (John) — Handoff

Last updated: 2026-04-23 (end of aakq ship cycle)

## Current state

**aweb 1.17.0 shipped.** aakq epic closed. Main at `b98a331` (ai.aweb)
and `bb668be` (aweb). PyPI + npm published via GHA.

Tags out on github.com/awebai/aweb:
- `server-v1.17.0` (cb8f7f5) — pypi aweb 1.17.0 live
- `aw-v1.17.0` (cb8f7f5) — npm @awebai/aw@1.17.0 live
- `channel-v1.3.0` (bb668be) — npm @awebai/claude-channel@1.3.0 live

Tom confirmed all three published successfully.

## aakq epic — closed

All subtasks + follow-ups shipped in 1.17.0:

| Task | Commit | What |
|------|--------|------|
| aakq.1 | fcbcc00 | channel precedence flip |
| aakq.2 | 05c46b2 | Go CLI precedence flip |
| aakq.3+.4 | e08b609 | drop workspace.yaml.active_team + migrate call sites |
| aakq.5 | 0b24ad1 | remove applyTeamStateToWorkspaceCache |
| aaku | 4b15d3d | non-Go consumers (channel + e2e + docs) + anti-regression test |
| aakq.7 | d2d59a5 | e2e switch-without-reinit regression test |
| aakq.9 | f120888 | surface cert load errors |
| aakq.6 | 25cf3f5 | doctor migration to teams.yaml SoT |
| aaks | 58070ca | fix aw work active 500 (server-side tasks_service.py) |
| release server+CLI | cb8f7f5 | version bumps + tags |
| release channel | bb668be | version bump + tag |

aakn, aako, aaks, aaku, aakq.1-.9 all closed in tracker with
references. Decision record committed to ai.aweb/docs/decisions.md
at `b98a331`.

## Gate log summary (2026-04-23)

- **Gate 1** (make test on 58070ca): 3m15s green. 365 server + 140
  awid + cli ok + 72 channel tests.
- **Gate 2** (make test-e2e on 58070ca): 1m4s green. 139 PASS.
- **Gate 3** (make test-e2e on v1.16.0 worktree with release-
  candidate e2e script): 58s. 4 FAIL exactly the 4 new switch-
  without-reinit assertions + 135 PASS. Regression proof valid.
- **Gate 4** (make release-all-check on bumped tree): 4m13s green.
  Version parity + make test + release-server-check (uv build) +
  release-channel-check (npm test).

All logs preserved at `/tmp/gate2-maketest.log`, `/tmp/gate2-e2e-head.log`,
`/tmp/gate-e2e-v116.log`, `/tmp/gate4.log`.

## Open from this cycle — not blockers

- **aweb-aakr** (P4): membership-field duplication between teams.yaml
  and workspace.yaml. Filed open with two candidate framings;
  architectural commitment is Juan-level. Not in 1.17.0.
- **Tom's v0.5.4 side**: aakt + aakv (ac test-backend pollution + ac
  JWT test isolation) still need dev dispatch. Tom is awaiting an
  aweb-server dev to claim either. Randy/Juan own the dispatch
  escalation on that side. Not a 1.17.0 concern.

## Process lessons from this cycle

Captured in shared memory (already saved):

- `feedback_spec_scope_all_consumers.md` — after field removal, grep
  all file types not just Go (aaku near-miss).
- `feedback_gut_over_confident_agent.md` — trust raised-eyebrow over
  confident agent review on upgrade/compat questions (0401d50 flip).
- `feedback_review_via_symlink.md` — coord reads commits via shared
  working tree, no diff-paste.
- `feedback_dispatch_via_coordinator.md` — dev-agent dispatch routes
  through coordinator, not CTO-direct (Randy's self-feedback).

Session-local lesson for next cycle (not yet in memory — consider
adding if pattern recurs): **push-before-mail order** for any
message that references a commit. I mailed Tom about the decisions
record seconds before the push landed and he got a pull-miss. One
race, low cost, but symptomatic of when announcement timing matters.

## What's up next

- **aweb-aakz dispatched to Grace 2026-04-25** (multi-membership mail
  409). P1 per Randy. Surfaced by Amy 2026-04-24 — two-membership
  did:aw gets 409 on `aw mail send`, chat works. Latent bug newly
  reachable via the per-membership flow aakq enabled. Server-side
  analysis from Randy: `identity_auth_deps.py:126` raises on
  multi-row; `:130` has the disambiguating `get_messaging_auth` that
  chat uses but mail doesn't. Investigation order I gave Grace:
  (1) check if cli/go/cmd/aw/mail.go sends X-AWID-Team-Certificate
  the way chat does, (2) check which auth dep the mail handler uses,
  (3) pick fix shape A/B/CLI. Same release protocol as 1.17.0;
  Randy will signal whether ship is 1.17.1 (patch) or 1.18.0.
- **Grace**: dispatched to aakz via chat. Offline 2d; will see on
  return. No urgency (Amy on chat workaround).
- **aweb-aakr** sits as a future design task. No action unless Juan
  wants to revisit the architectural question.
- **Tom's v0.5.4 cycle**: still awaiting aakt/aakv dev dispatch
  (Randy → Juan in flight). Tom said he'd ping if 12h+ stalled; we're
  past that window now — worth a check-in if I see no progress.
- **Process check**: verify Randy's CLAUDE.md updates landed in
  coord-cloud, coord-awid, cto docs.

## Messages sent this cycle (retrospective)

- chat → grace (hold on aaks finding; close-the-loop norm; GO on
  .5/.6/.7/.9/aaks; ship confirmation)
- chat → randy (status + ack of gate-check protocol; correction on
  aakt/aakv scope; request unblock)
- chat → tom (workspace.yaml legacy framing check)
- mail → randy (SOT verification cross-namespace; aakq.8 scope Juan
  directive; aaku scope grew; gate log + SOT analysis x2; ship
  confirmation)
- mail → tom (aakq.8 coordination x2; cert validation no-change;
  ship notice; push-race correction)
- mail → grace (review protocol; aakq.9 heads-up x2)

## Files preserved outside the repo

- `/tmp/gate-maketest.log`, `/tmp/gate2-maketest.log` — Gate 1 logs.
- `/tmp/gate-e2e-head.log`, `/tmp/gate2-e2e-head.log` — Gate 2 logs.
- `/tmp/gate-e2e-v116.log` — Gate 3 regression-arm log.
- `/tmp/gate4.log` — Gate 4 log.
- `/tmp/aakq7-v116-arm.log`, `/tmp/aakq-aaku-shape-a-arm.log` —
  earlier arm logs from the pre-push reviews.
- `/tmp/aweb-v116-e2e/` — git worktree at server-v1.16.0 for the
  regression arm. Can delete if next cycle needs the space.
- `/tmp/randy-mail-body.md`, `/tmp/randy-mail-body-v2.md`,
  `/tmp/sot-analysis-draft.md`, `/tmp/release-commit-body.md`,
  `/tmp/channel-release-commit-body.md`, `/tmp/decision-record-draft.md`,
  `/tmp/decisions-new.md` — ceremony drafts.
