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

- **aweb-aala P0 launch epic — IN FLIGHT, time-shape ~2 days per
  Juan 2026-04-25.** 12 child tasks, BYOIT cross-machine team join +
  multi-membership hardening. Design (awid stores full signed public
  cert blobs) approved by Juan directly with Grace. Quality bar: no
  regression, no tech debt. Implementation protocol: Grace implements
  without waiting on reviews per Juan's directive; my pre-push
  GO/NO-GO leverage is gone. Compensating with explicit BLOCKER vs
  NOTE classification on review concerns.
- **My 3 BLOCKERs filed with Grace** (must resolve in spec/SOT before
  the affected child pushes to main):
  - **A**: aala.1 (SOT) blocks aala.2 (awid schema push). Dep graph
    didn't have this edge; I've told Grace to gate .2's push on .1
    being reviewed-and-agreed by me + Randy. Asked Randy to confirm.
  - **B**: aala.2 atomicity — blob upload + metadata + signature
    validation is one atomic transaction at awid. No orphan blobs.
  - **D**: aala.5 fetch-cert refuses to overwrite an existing local
    cert by default; `--force` opt-in. Prevents stale awid blob from
    silently kicking out a working local install.
- **5 NOTEs sent to Grace** (fix during review, not push-blocking):
  C narrow .3 to subject-only fetch; E heads-up Tom on .10; F resolve
  .6 redesign-vs-rename fork before impl; G clarify aakm vs aala.8
  scope; H aakr touch-during-aala.4 logged as observations not silent
  fold.
- **aakz framing accepted** — aala.7 is a SUPERSET of aakz, both stay
  open until aala.7 ships, then aakz closes as covered.
- **aakr is orthogonal to aala** per Grace; no Shape choice forced.
- **Grace state 2026-04-25 (per her mail 3e73c9f1):** code in-tree
  for aala.2/.3/.4/.5/.7 plus SOT/docs updates in
  `docs/awid-sot.md`, `docs/identity.md`, `docs/aweb-sot.md`. **NOT
  PUSHED** — she's holding push on .2 per the dep edge until .1 SOT
  is reviewed and any changes folded back. Focused Python + Go test
  suites green so far. Addressing all 3 BLOCKERs before SOT review
  ping:
  - A: SOT draft already in 3 docs; folding overwrite rule + one
    wording pass before ping.
  - B: confirmed awid registration is single-INSERT (blob + metadata
    + signature validation in one transaction, no split write path).
    She'll make this explicit in SOT wording.
  - D: had refuse-overwrite wrong (was overwriting); fixing to
    refuse-by-default with --force opt-in now.
- **NOTEs status (C/E/F/G/H):** Grace didn't mention these in her
  status update. Likely fine — F (aala.6 redesign-vs-rename fork)
  hasn't started yet so the fork decision isn't bypassed. Others are
  during-review-fixable. Watch for them when each child surfaces for
  review.

## NO-GO 2026-04-25: aala e2e regression (held push)

After review of Grace's aala slice working tree (.1 SOT + .2/.3/.4/.5/.7),
gates ran:
- `make test`: GREEN. server 367 (+2), awid 143 (+3 her new tests),
  cli ok, channel 72. 4m20s.
- `make test-e2e`: **EXIT 2**. Script dies silently mid-Phase-12d
  between line 1045 (last PASS "alice restored whoami address after
  switch") and line 1051 (next assertion "alice restored primary-team
  mail exit"). Log says "ALL PASSED: 97 tests" but that's misleading —
  it's the count to the death point, after which trap-EXIT cleanup
  fires and 42 assertions in Phases 13-22 never run. exit=2 from make.

Most likely cause: aala.7's auth-path change on multi-team-alice mail
send. Phase 12d sets up alice with two active team memberships
(devteam:test.local + main:partner.local) for the aakq.7 switch-
without-reinit assertions. Line 1046's `aw mail send` to bob runs
against multi-team alice — exactly the scenario aala.7 is supposed
to fix. Unit tests passed (no fixture exercises multi-active-local-
agent state); e2e is the only integration gate that catches this.

Same class of miss as aakq.3 / aaku — focused tests green, integration
regresses.

Held actions:
- .2 push gated. No push of any aala child until aala.7 regression
  resolved AND make test-e2e green to 22-phase completion.
- Grace investigating; she'll re-ping once fixed.
- Code-reviewer earlier passed all 3 BLOCKERs in static review; the
  bug is in test-coverage-of-the-fix, not in the architectural
  contracts. aala.7 unit fix shape is correct; the wiring through to
  the specific Phase-12d path is the gap.
- Mailed Randy the finding (74c1b733) — relevant to his SOT review
  of the aala.7 auth contract: test_messages_http needs a fixture
  with two active local-agent rows on the same DID before this slice
  ships. Otherwise the next auth-path touch reintroduces the bug.
- **Randy mailed**: technical review summary + ask to review aala.1
  SOT when it lands + confirm the .1→.2 dep edge.
- **Tom mailed**: aala.10 (ac alignment) heads-up; suggested he scope
  ac sub-tasks in parallel with the aweb side.
- **Time-shape risk**: aala.11 (E2E matrix) sits at the bottom of the
  dep graph. If it doesn't run green by launch-minus-12h, the call
  to slip-launch vs ship-partial is Juan's. I'll surface ~24h before
  launch with data.

## Recent unscheduled hotfixes

- `5b6a5ce` channel 1.3.1 — fixed `.mcp.json` `mcpServers` wrapper
  shape (broken in 1.1.0-1.3.0; Juan landed directly).
- `be0dfdb` release-channel skill: bump marketplace.json on release
  (silent-update bug fix; Juan landed directly).
- **Gap surfaced for follow-up**: `make test-e2e` doesn't validate
  channel/.mcp.json shape against the Claude Code plugin schema.
  Worth a 5-line CI check so 3 broken minors don't ship in a row
  again. Filed mention in Randy mail.
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
