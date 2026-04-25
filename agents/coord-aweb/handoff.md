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

- **aweb-aala P0 launch epic filed by Grace 2026-04-25** (12 child
  tasks, BYOIT cross-machine team join + multi-membership hardening).
  Design from Juan per Grace: awid stores full signed public cert
  blobs. New awid endpoint + schema change + CLI add-member redesign
  + accept-invite redesign + ac cloud alignment + E2E matrix + migration
  plan. Beyond my approval lane; needs Randy's architectural review
  on aala.1 (SOT) before .2-.5 implement. **Held off escalating to
  Randy/Juan/Tom until Grace answers 5 clarifying questions** in my
  mail e7d2a6cf — superseding aakz, sequencing, Juan-scope-known,
  aakr-overlap, time-shape.
- **aweb-aakz** (multi-membership mail 409, dispatched to Grace
  earlier today): aala.7 explicitly says "Fix the aweb-aakz class of
  failures" — pending Grace's confirmation that aala.7 supersedes
  it and aakz can close as duplicate.
- **Grace**: working on invite/add-member/bootstrap survey for Juan
  (her direct dispatch); filed aala epic from that survey. Currently
  reading the aakr context I forwarded earlier today.
- **aweb-aakr** sits as a future design task. No action unless Juan
  wants to revisit the architectural question.
- **Tom's v0.5.4 cycle: shipped and deployed.** Tag `33a4c089`
  landed 2026-04-23 21:34 UTC, GHA green in 12m13s, auto-deploy hit
  prod 2026-04-24 06:01 UTC, running ~25h healthy. aakt/aakv/aakw/aakx
  all closed. aaks reached hosted users via the aweb pin pickup. No
  pending follow-up on the ac side. Confirmed via direct chat with
  Tom 2026-04-25 (he acknowledged he should have pinged me when the
  tag landed; banking the lesson on his side as a feedback memory).
- **GHA Node 20→24 deprecation forward item** (Tom flagged): aweb-cloud
  workflow uses actions/checkout@v4 + docker/* actions still on Node
  20. Forced bump by 2026-06-02. Tom owns; not aweb's lane unless
  aweb's own GHAs have the same pattern (worth a check next cycle).
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
