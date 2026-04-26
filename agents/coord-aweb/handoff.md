# Coordinator aweb OSS (John) — Handoff

Last updated: 2026-04-26 (mid-cycle, v0.5.8 + three-layer KI#1 reframe)

## Current state (read this first on wake-up)

**Cycle in flight: v0.5.8 release with three-layer KI#1 reframe.**

aweb 1.18.2 (924070c) shipped to PyPI earlier today. Channel 1.3.3 (3ee9b94) shipped to npm — bad-signature corruption fixed at 2f52433 after Grace's empirical catch (banked: subagent-can-be-wrong-on-crypto-detail). ac v0.5.8 pending Tom's tag, gates on leg-2 dashboard probe.

**aweb origin/main:** `c250cd1` Fix known-agent fallback for missing registry addresses (Grace, aalk; GO sent today, push imminent under opt-in handshake)

Recent stack since 924070c:
- `c250cd1` — aalk (Grace, GO sent today; supersedes 189a78b with Randy's refinement folded in: signEnvelope writes ToStableID + helper assertion. Targeted Go tests green from my workspace.)
- `ef5c3d7` — Reject local awid registry in channel (parked, gates on leg-2 dashboard probe per Tom's posture)
- `3ee9b94` — channel 1.3.3 release tag (shipped to npm)
- `2f52433` — TOFU bad-signature corruption fix (Grace empirical catch on base64-char-flip non-determinism)
- `924070c` — aweb 1.18.2 release tag (shipped to PyPI)

**KI#1 final framing (today, post-three-iteration churn):**

After three reframes triggered by Grace's chat challenge → my prod-DB query → Juan's ephemeral-agent correction, the picture collapsed cleanly to:

1. **aalk** (closing v0.5.8): TOFU continuity-fallback. CLI ChainResolver falls through to PinResolver on registry 404; PinResolver returns DID + StableID; signEnvelope copies identity.StableID into env.ToStableID. Closes Amy's case (she has Randy pinned). c250cd1 GO sent, push imminent under opt-in handshake.

2. **aalm** (P1, SOLE architectural follow-on): Go RegistryResolver does anonymous awid GETs — org_only/team_members_only rows return 404 even though rows EXIST in DB. Authenticated CLI requests + awid server-side filtering by team-cert membership closes it. Cross-coord (Grace CLI + Goto awid + Juan-loop on signature scheme: detached Ed25519 over canonical method+path+body? bearer+sig? — real architectural question). Days-to-weeks. v0.5.9.

3. **aalo + aalp** (P3, Goto's lane): awid server correctness bugs found in passing — (a) LIST endpoint reports ownership_proof=true on mismatched controller key; (b) LIST endpoint applies visibility filter despite ownership_proof claim. Filed today, not v0.5.8-blocking, may share root cause.

4. **aaln** (P3, my lane): `aw id register` reports success without verifying server registration state (filed by Randy today). Narrow CLI bug. Backlog.

5. **aall** (CLOSED today as not-a-bug): originally framed as "9/10 permanent agents missing from awid" but the 5 missing (charlene, enoch, goto, grace, noah) are EPHEMERAL agents per Juan's classification — ephemerals don't get persistent registrations by design. Persistent agents under juan.aweb.ai (amy, avi, john, marvin, randy, support, tom) are all present and registered.

**Final ship-mail line locked** (Randy framing-authority + my drafting + Tom + Juan correction):

  "KI#1 closes for continuity case (aalk: known-agent pin fallback when 
  registry resolution misses or returns empty). Authenticated CLI lookup 
  for org_only / team_members_only address visibility remains open 
  under aalm (P1) — landing in v0.5.9."

**Held: ship-mail to Charlene** gates on Avi sign-off (mailed ceo 9ed78982 with final framing; supersedes 055c9410, fb5105f2, e0c4e29d). Avi offline 11d — slow leg. Three-events distinction (Tom's): cleanup pushes (gates leg-2) / tag cycles (each coord's call) / ship-mail (Avi sign-off). Independent.

**Direct prod awid DB access**: I have working psql connection via `aweb/.env.awid-production` (AWID_DATABASE_URL → Neon). Used today to settle the aall scope question. Useful follow-up surface.

**Lessons banked today (durable memory, ../../../.claude/projects/.../memory/):**
- `feedback_bug_class_spans_architectural_layers.md` — bug class can decompose into N architectural layers; reproducer-green at layer 1 doesn't close class. Hold wholesale-closure framing until layers mapped.
- Concrete trigger: today's KI#1 three-iteration churn. Original "wholesale closes" → three layers → empirical DB verification → Juan's ephemeral correction. Truth-finding is iterative; framing must be revised honestly along the way.

**Open follow-ups on my plate (carried from prior cycles):**
- BYOIT prod-awid smoke test (Randy ask, task #27). Mailed Tom (`f2881e63`); cert blob populates after add-member; cross-machine fetch verifies; wrong-DID 403.
- v0.5.8 verified-live probe leg 2 (task #34): Juan dashboard send → Randy JSON inbox. Pending Juan/Randy execution.
- Render redeploy of awid is manual via dashboard. Worth proposing deploy hook + daily probe of api.awid.ai/health vs PyPI head to catch next aala-style version drift.

**Open from prior cycles, still open:**
- `aweb-aakr` (P4) — membership-field duplication between teams.yaml and workspace.yaml. Juan-level architectural call. Not actively scheduled.
- `aweb-aajv` (Dashboard lifecycle bypasses OSS mutation hooks) — Randy re-opened after Tom's pin-bump close was premature.
- `aweb-aald` (BYOD ephemeral re-init observation Grace filed from my aajs review) — future P? task, not actively scheduled.

**Memories banked this cycle (most recent first):**
- `feedback_bug_class_spans_architectural_layers.md` (today) — sibling to reproducer-synthetic but at architecture-decomposition layer. Bug class spans N layers; fix at layer 1 doesn't close class even if reproducer only exercises layer 1. Concrete trigger: KI#1 three-layer reframe.
- `feedback_reproducer_synthetic_state_assumes_user_invariants.md` (today, earlier) — reproducer-canonical-green is necessary but not sufficient; user state shape may differ.
- `feedback_subagent_can_be_wrong_on_crypto_detail.md` (today) — subagent confident-wrong on base64-char-flip determinism; Grace caught empirically.
- `feedback_uv_sync_refresh_after_pypi_publish.md` (today) — Tom found uv index cache lag.
- `feedback_grace_unilateral_protocol_cross_pattern.md`, `feedback_multi_gate_go_mail_visibility.md` (today) — Grace unilateral channel 1.3.2 push; CTO-blind chat-only GO.
- `feedback_default_to_code_reviewer_subagent_for_gate_reads.md` (recurring; flagged twice this week) — default to subagent for non-trivial gate-reads.
- `feedback_artificial_gate_from_unverified_dependency.md`, `feedback_verify_before_relay_at_coord_layer.md` (this week) — verify before relaying upstream signals.

## Decision records added this cycle (ai.aweb/docs/decisions.md)

- 2026-04-25 — awid prod registry cutover from 0.3.1 to 0.5.1 (00952ad). Captures the deployment lag, impact, recovery script, and migrations-discipline lesson per Randy's three-point ask.
- 2026-04-25 — aweb-cloud v0.5.5 ships (was already there before my cycle started)
- 2026-04-25 — BYOIT cross-machine team join + multi-membership launch hardening (aala epic) (was already there)

## Memories banked this cycle (per-agent dir + MEMORY.md index)

- `feedback_pgdbm_checksum_normalization.md` — pgdbm normalizes line endings + strips before SHA256; raw `sha256(file)` won't match `schema_migrations.checksum`. Surfaced during cutover validation when I almost chased a fake bug.
- `feedback_consolidated_migration_discipline.md` — never edit a consolidated single-file migration in place; every additive change is a new ordered file. Codifies the lesson behind the cutover.
- (Both also reflected in aweb/AGENTS.md "Database migrations" section so dev agents see them on wake-up.)

## Engineering quality bar held this cycle

- Local docker-postgres:16-alpine dry-run before any prod-destructive op surfaced two real PG-version-skew bugs (`SET transaction_timeout=0`, `schema_migrations` row collision). Both encoded into the script as sanitizers. Lesson: even mechanical tooling deserves a synthetic-seed dry-run when it touches prod state.
- Pre-cutover schema column-by-column comparison confirmed the only delta was the new nullable `team_certificates.certificate` — no risk of `--column-inserts` referencing dropped/renamed columns. Treat this as the standard pre-cutover check on any future schema-reset.
- Push-discipline: ed4fa89 + 72530c2 + 00952ad each pushed individually, working tree clean between commits, no batched pushes. Lesson `feedback_push_tags_individually.md` extends to non-tag pushes too — the principle is "don't batch what GitHub event-coalesces."

## Cross-coord state

- Tom finished his bisect (sibling aweb at b0b2b27 → green at pure 1.18.1) and restored to ed4fa89. v0.5.6 release sequence in flight on his side. He'll mail when v0.5.6 tags.
- Grace pushed 18021ff9 (aaja.6) to ac under Tom's authorized cross-coord borrow. That borrow's scope is aaja.6; she's back under my coord for aweb-side work after v0.5.6 closes.
- Randy has the awid cutover confirmation + the three follow-up asks I'm working through.

---

## History (older cycles below — useful for context, not current)

## aakq cycle final state (2026-04-23)

aweb 1.17.0 shipped. aakq epic closed. Main at `b98a331` (ai.aweb) and `bb668be` (aweb). PyPI + npm published via GHA.

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

## GO 2026-04-25 (later): aala first slice (.1/.2/.3/.4/.5/.7) approved for push

After Grace's regression fix, all three gates verified:
- **e2e (independent verify)**: exit 0, ALL PASSED 139 tests, Phase 22
  marker present (full coverage). Per the harness-honesty discipline,
  verified by exit code AND phase-marker presence, not by the summary
  text alone.
- **Code-reviewer**: GO-with-notes on the delta. All 3 prior BLOCKERs
  (atomicity, refuse-overwrite, subject-only) hold. My 3 NOTES
  addressed (call-site comment, from_agent_id assertion, --force
  success test).
- **Randy SOT GO** (722dc6bf): all 4 of his items addressed (BLOCKER +
  3 NOTES). One non-blocking nit on fetch-envelope `certificate`
  field naming (base64-PEM vs base64-canonical-JSON vs inline) —
  follow-on SOT pass.

**Push approval covers**: aala.1, .2, .3, .4, .5, .7.

**Four non-blocking follow-ups** that Grace folded into the SAME
commit before push (eliminating the post-push followup queue for
this slice):
1. ✓ Randy's multi-active-rows fixture team-scoped half — landed
   (server suite 55 → 56 passed for this addition).
2. ✓ Restored line 576 `to_alias` assertion.
3. ✓ Confirmed single-row identity alias coverage.
4. ✓ Fetch-envelope certificate field pinned: base64 of exact UTF-8
   team certificate JSON.

## SHIPPED 2026-04-25 (v1.18.1 republish): aweb 1.18.1 + aw CLI 1.18.1 + awid-service 0.5.1

**Live on PyPI + npm**:
- PyPI `aweb 1.18.1` ✓
- PyPI `awid-service 0.5.1` ✓
- npm `@awebai/aw@1.18.1` ✓ (downstream awebai/aw repo workflow 2m47s)
- All 5 aweb-side GHA workflows fired clean (Server Release, aw Sync and Release, Awid Release GHCR, Awid Service Release PyPI, Server CI).

**Release commit**: `b0b2b27` "release: aweb server 1.18.1, aw CLI 1.18.1, awid-service 0.5.1 (fixes 1.18.0 ghost-tag publish; includes aweb-aajs and aweb-aakk)"

**Includes**: 1.18.0 aala bundle (898556d) + aweb-aajs BYOD wizard fix (4623979) + aweb-aakk dashboard task-claim events fix (3bc296e). Both Randy-approved scope-extensions on the same shape (small, real-gap, tracker-evidence-clean, found via tracker-hygiene scanning).

**Coordinated**:
- Tom mailed (`4edf68e3`) with unblock + final pin targets (aweb>=1.18.1, awid-service>=0.5.1).
- Randy mailed (`89552454`) with ship confirmation; he had banked feedback_push_tags_individually.md during the recovery.

## 1.18.0 → 1.18.1 ghost-tag detour (lessons banked)

**What happened**: Tagged 1.18.0 + pushed all 4 tags in a single batched `git push`. Zero of the 4 GHA tag-triggered publish workflows fired (compared to 5 on 1.16.0 and 1.17.0). PyPI/npm never received 1.18.0/0.5.0; 1.18.0 became a ghost tag (commit + tags exist on origin but no artifacts).

**Recovery (Option B, Randy-approved)**: bump versions to 1.18.1/0.5.1, fold in aajs + aakk on the same release commit, push tags **individually one-by-one** to defeat any GitHub batch-coalesce / event-dedup. Worked. All 5 workflows fired identical-pattern to prior releases.

**1.18.0 ghost tag stays in origin** as audit history per Randy's call.

**Memories banked** (shared project memory dir):
- `feedback_prohibition_language.md` (mine, 2026-04-25 morning, from the Grace lane-cross resolution).
- `feedback_push_tags_individually.md` (Randy's, 2026-04-25 afternoon, from this ghost-tag recovery).
- Distinct lessons; both apply going forward.

## Tracker audit pass (Randy-asked, 2026-04-25 afternoon)

Walked Randy's list of 12 + aais epic. Net: **0 closures from his list**. 2 were already-closed pre-audit (aaki, aakg). 10 + aais's 9 subtasks all real-still-open work, not stale-shipped. Audit-result mail to Randy: `abbd81fd`.

Methodology limit: I grep'd commit subjects + bodies for task-refs and bug-keywords; commits that landed without naming the task slip past. Randy's converging pass catches those.

aweb-aajv (Dashboard lifecycle bypasses OSS mutation hooks) noted: Randy re-opened after Tom's pin-bump close was premature. Re-open canonical.

aais (P1 epic, Hugo site + cloud docs alignment) — explicit site/ walk-through is Charlene/Avi/Eugenie's lane, not coord-aweb's audit. Hedged accordingly.

## Final state of aweb-aala epic

- 11 of 12 child tasks closed: `.1, .2, .3, .4, .5, .7, .6, .8, .9, .11, .12`.
- 1 still open: `.10` (cloud aweb-cloud alignment) — Tom's lane via authorized cross-coord borrow with Grace. Pin updates land in ac v0.5.5.
- Plus 2 epic-adjacent items shipped in 1.18.1:
  - aweb-aajs (BYOD wizard) — tracker-hygiene scan find, fixed.
  - aweb-aakk (dashboard task-claim events) — same.
- Open as design question: `aweb-aakr` (membership-field duplication; Juan-level architectural call).

## What's up next for me

- Standing by for Tom's ac v0.5.5 tag mail.
- Standing by for Randy's converging-pass on the audit (might re-open or close items).
- Grace continuing tracker-hygiene scans + real implementation under my coord. Same protocol.
- aweb-aald (BYOD ephemeral re-init observation Grace filed from my aajs review): future P? task, not actively scheduled.

## SHIPPED 2026-04-25 (mid-day, ghost-tag): aweb 1.18.0 + aw CLI 1.18.0 + awid-service 0.5.0

Release commit `898556d` on origin/main with 4 tags pushed:
- `server-v1.18.0` — PyPI publish via GHA server-release.yml (aweb 1.18.0)
- `aw-v1.18.0` — npm publish via GHA aw-release.yml (@awebai/aw)
- `awid-v0.5.0`
- `awid-service-v0.5.0` — PyPI publish via GHA awid-pypi-release.yml

Gate log (mailed to Randy 5da4621a, approved 2a2f344a):
- Gate 1 (make test on ba133d4): 368+144+cli+72 green; 4m20s logical CPU.
- Gate 2 (make test-e2e on ba133d4): 159 PASS, exit 0, all 22 phases. 1m24s.
- Gate 3 (v1.17.0 regression arm with aala e2e script): exit 2, 1 FAIL on `erin add-member prints fetch-cert` (expected — cross-machine guidance doesn't exist in v1.17.0). Regression proof valid.
- Gate 4 (release-all-check on bumped tree): exit 0, 5m47s. All checks passed.

Decision record: `c858c98` ai.aweb/docs/decisions.md 2026-04-25 entry.

Tom mailed (7d0150e9) — ac v0.5.5 unblocked on aweb side; PyPI propagating; he'll bump and ship under his discipline. Side note for ac release notes: `aw id team accept-invite` semantic shift to same-machine helper (ac doesn't surface but worth banking).

## Coord-flow violation 2026-04-25: resolved via authorized cross-coord borrow

Grace started uncommitted ac edits in aala.10 territory after I redirected her ("stand down — aala.10 is Tom's lane, Mia dispatched"). Five ac files modified locally on her side, not pushed. Two-step recovery:

1. **Strong stop signal** (chat) — required: don't push, git stash, ack. Grace acked: stashed as `stash@{0} On main: aala.10 BYOIT cert pickup WIP from grace`, ac clean against origin/main. Verified.
2. **Juan inverted Tom's insight-option call** — authorized cross-coord borrow: Grace works in ac under Tom's coord for aala.10 scope. Mia stands down. Grace unstashed under Tom's authorization and continued. Tom now reviews her ac commits per his discipline.

Lessons banked:
- `feedback_prohibition_language.md` saved to shared project memory + entry in MEMORY.md.
- One-paragraph "Cross-coordinator dispatch and lane discipline" subsection added under `docs/team.md` "How engineering works." Codifies authorized-cross-coord-borrow + insight-transfer-without-code as the two valid cross-repo patterns + names the prohibition-language requirement when redirecting. (`3f59d81`)
- Distinct from Randy's `feedback_dispatch_via_coordinator.md` (CTO-side); these are complementary halves of the same protocol.

## What's up next for me

- aweb 1.18.0 is shipped. ac v0.5.5 is Tom's track from here.
- Grace picked up `aweb-aajp` (API key bootstrap → add-worktree → mail round-trip, P0 pre-existing). My lane. Will review when she pings with a concrete commit.
- Standing by for any aala.10 follow-up needing aweb-side input (Tom will mail).
- **aweb-aakr** still open as future design question (membership-field duplication, Juan-level call).

## 9b2eed3 LANDED on origin/main 2026-04-25 (slice 2 of aala)

Grace pushed `9b2eed3 Add cross-machine fetch-cert e2e` directly
without pre-push review. Per Juan's "don't wait on reviews" that's
allowed. Independent post-push verification:
- e2e: exit 0, 159 tests, Phase 22 marker. Up from 139.
- code-reviewer GO-with-notes on the slice.
- 5 of 6 remaining aala children CLOSED in this slice: .6, .8, .9,
  .11, .12.

**One real post-push gap to fix before tag**: aala.9 closure is
premature. Three error messages still point cross-machine users at
`aw id team accept-invite` (which fails for them after Grace's .6
conservative-helper rename):
- cli/go/cmd/aw/init.go:231
- cli/go/cmd/aw/run.go:449
- cli/go/cmd/aw/run.go:461

Flagged to Grace as a one-string-fix follow-up commit. Trivial.
Won't push the tag until those land.

**Discipline note flagged to Grace**: closing tasks should require
verified acceptance ("I checked each acceptance item, they hold"),
not "I think it's done." First time her close-discipline slipped;
worth surfacing. Juan's directive covers push-without-pre-push;
doesn't relax close-on-verified-acceptance.

## Tom's status (after my mail e2e8b867 → 4cc636f7 → bbf3240f-4fe0):

Mia dispatched on aala.10 ac surface walk. Tom asked for aweb
release timing + awid version. Answered (`a*`):
- aweb 1.18.0 + aw CLI 1.18.0 + awid-service 0.5.0 + channel stays
  1.3.1.
- ~6-12h to tag (Grace fixes .9 strings → my gate log + SOT analysis
  → Randy approves → tag).
- I'll mail Tom the moment the tag fires.

## ff92358 LANDED on origin/main 2026-04-25 (slice 1 of aala)

Single commit "Implement cross-machine team cert fetch" covers
aala.1/.2/.3/.4/.5/.7 + the four follow-ups + Randy's new contract
requirement. All 7 tracker tasks closed including aweb-aakz
(superseded by aala.7 per Randy's framing — closes with pointer to
aala.7's resolution).

**Half the aala epic is in.** Remaining open:
- .6 (accept-invite, conservative same-machine-helper path per
  Grace's earlier decision)
- .8 (per-membership address integration with cert issuance)
- .9 (aw init + CLI help text reality)
- .10 (cloud ac alignment — Tom's lane)
- .11 (E2E test matrix expansion for full BYOIT cross-machine)
- .12 (support and migration plan for pre-fix team certificates)

Grace will pick at her pace; same review protocol per slice.

## NO-GO 2026-04-25 (earlier, resolved): aala e2e regression (held push)

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
- **Randy responded e934ee65**: agreed with both findings. He's
  adding to aala.7's acceptance criteria a CONTRACT requirement for
  the multi-active-local-agent fixture (identity-scoped AND
  team-scoped mail tests against it), so it gets carried forward as
  part of the spec's evidence-of-correctness — not just a one-off
  fix. Comment going on the aala.7 task. Holding the rest of his
  SOT review until Grace addresses the e2e regression + backward-
  compat-pre-blob BLOCKER. Will re-review on her ping.

## Filed P2 follow-up: e2e harness summary message can lie

Randy filing as a separate P2 task (release-gate trust issue):
`scripts/e2e-oss-user-journey.sh` printed "ALL PASSED: 97 tests"
while exiting 2 because the trap-EXIT cleanup fires after the
last-printed PASS but before the script's normal end. A future
reader scanning a log could miss the failure if they read the
summary line and not the exit code. 5-line fix: set a flag in the
trap to suppress/override the summary.

Class-related implication for regression-pair verification: when
running aakq.7-style "must-fail-on-old-version" arms (and we'll
need this for aala too at tag time), verification must be by exit
code, not by the printed summary message. Tom did this correctly
during 1.17.0 by discipline; harness fix removes the discipline
dependency. Worth banking in my review checklist: **always check
exit code first, summary text second, when reading e2e logs.**
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
