# Coordinator aweb OSS (John) — Handoff

Last updated: 2026-04-22 (end of second cycle)

## Current state

aweb OSS is shipping aggressively. Since 2026-04-11 the repo landed
six server/CLI minors (1.11.0 → 1.16.0) plus awid 0.3.0–0.4.0. Current
cleanup: drift surfaced by the per-membership address model (1.16.0).

Current head: `05c46b2 fix(cli): prefer cert member address in
selection` on main. Only `beadhub-legacy` remains as a named archive
branch.

## My role (confirmed by Randy this cycle)

Full-review layer for aweb. Run a `code-reviewer` agent pass on every
significant commit Grace (or any dev) lands, not just a shape check.
Juan is explicit: **I'm responsible for the quality of the software.**

## Review protocol (corrected by Juan 2026-04-22)

- Grace commits locally on main (aweb AGENTS.md forbids WIP branches).
- The aweb/ symlink in this coord dir IS her working tree — I read
  her unpushed commits directly via `git -C aweb log`. No diff-paste
  needed.
- I chat go/no-go.
- She pushes on approval.
- Escalation: architecture → Randy; direction → Juan; bugs surfaced
  mid-review → file as aakq subtask or standalone aweb-aak bug.

I originally offered her a "feature branch PR" option and later a
"paste diff in chat" option — both wrong. Juan asked Randy to update
coord-aweb/CLAUDE.md and the dev-agent docs so this is codified and
future instances don't repeat the mistake.

## Active work: aweb-aakq (P1 epic)

**Shipping order:**
1. aakq.1 channel precedence flip — **landed fcbcc00**, closed.
2. aakq.2 Go CLI precedence flip — **landed 05c46b2**, closed.
3. aakq.3 drop workspace.yaml.active_team field — **landed e08b609**,
   closed.
4. aakq.4 migrate call sites — **bundled in e08b609**, closed.
5. aakq.5 remove applyTeamStateToWorkspaceCache — **reviewed GO as
   0b24ad1, push pending**. Code-reviewer clean. Pre-existing 4 e2e
   failures (from .3/.4's non-Go consumer regression, see aaku) not
   fault of .5.
6. aakq.6 doctor migration — **ready to claim**.
7. aakq.7 e2e switch-without-reinit in Phase 12d — blocked on .5
   (now .5-GO, unblockable on push).
8. aakq.8 release 1.17.0 — **now blocked on aaku** (see below) in
   addition to .5-.7 and .9.
9. aakq.9 silent cert-load error — **ready to claim**, no deps.
10. **aweb-aaku** (P1, standalone — see "Critical finding" below).

**Ready queue:** aaku (CRITICAL, new blocker), .6, .9.

## Critical finding 2026-04-23 — aweb-aaku filed

Ran `make test-e2e` as my new per-review discipline the moment Docker
was available. **Main has been e2e-broken for ~24h from aakq.3/.4**:
4 failures in Phase 21 and Phase 22 of
scripts/e2e-oss-user-journey.sh from bash reads of
`workspace.yaml.active_team` (removed by aakq.3).

**Grep for non-Go readers** (per Randy's hint) uncovered this is not
just the bash script — it's a NEW-USER BREAK in production code:

- `channel/src/config.ts:63` reads `workspace.active_team` at
  runtime. After 1.17.0 ships, new `aw init` writes workspace.yaml
  WITHOUT active_team (aakq.3's MarshalYAML strips it on save).
  Channel then throws "worktree workspace binding is missing
  aweb_url, active_team, or the active membership alias" at line
  67-68.  **Every new user after 1.17.0 breaks.** Existing users
  survive only because lazy migration doesn't rewrite workspace.yaml,
  so the legacy field stays on disk.
- Stale docs: aweb-sot.md:1013, identity.md:110, cli/go/README.md:151.

**Scope of aweb-aaku:**
1. scripts/e2e-oss-user-journey.sh lines 1147, 1195 → read from
   teams.yaml.
2. channel/src/config.ts:63-68 → load teams.yaml, derive activeTeam.
3. channel/test/config.test.ts fixtures (lines 68, 109, 140, 166) —
   update to post-1.17.0 shape.
4. Docs — aweb-sot.md ~1011-1044, identity.md:110, cli/go/README.md:151.
5. Regression test in channel: workspace.yaml WITHOUT active_team +
   teams.yaml WITH active_team + valid cert → resolveConfig succeeds.

**aaku is THE release blocker for aakq.8.** Without it 1.17.0
cannot ship.

## My review discipline (promoted to spec by Randy 2026-04-23)

- `make test-e2e` on EVERY subtask review, not just at .8. Randy is
  updating .5, .6, .7, .9 specs to include this as acceptance.
- Before .8 tag: formatted gate log per named gate to Randy
  (exact command, pass/fail/skipped with reason, duration). Both
  .7 regression pairs logged (pass-on-Shape-A + fail-on-1.16.0).
- Before .8 tag: SOT analysis walking user-facing surfaces against
  aweb-sot/awid-sot/trust-model. Mail findings to Randy.
- Migrations no-touch unless spec scopes them.
- Scope-creep watch: any file outside the task's Where list is
  flagged before anything else.
- After a field removal: grep across ALL file types (bash, TS,
  Python, docs), not just compilation consumers (my lesson + Randy's
  self-feedback from aaku).

## Code review findings this cycle

### fcbcc00 — aakq.1 (channel plugin) — pass-with-notes
- Precedence flip correct, `.trim()` symmetric, edge cases OK.
- Self-message detection in channel/src/index.ts:339 now correctly
  uses the team-presentation address.
- **Test gaps** (minor): no explicit identity-only-fallback assertion
  with cert present-but-empty; no whitespace-only member_address case.
  Randy's call: not worth a subtask on their own; roll into aakq.9 or
  drive-by on next touch. Not filing.

### 05c46b2 — aakq.2 (Go CLI) — pass-with-notes
- **Real finding, now aakq.9**: `if cert, err := LoadTeamCertificate;
  err == nil` silently swallows parse/load errors. Corrupt PEM →
  silent fallback to identity.Address. Inconsistent with
  `resolveCertificateClient` which surfaces errors. Fix: distinguish
  `os.ErrNotExist` (silent fallback OK) from parse/load errors
  (surface or debug-log).
- Bonus fix in `helpers.go` (return sanitized selection in
  identity-missing branch) is a genuine correctness bug — good.
- Test fixture `TestAwWhoamiJSONUsesActiveCertMemberAddress` is
  fragile: `writeSelectionFixtureForTest` writes identity with cert's
  address, then an explicit `writeIdentityForTest` overwrites it. One
  refactor of the helper and the discriminating power is lost. Worth
  a test comment; not a blocker.
- Missing-test cases (non-blocking): empty `CertPath`, cert with
  empty-string member_address.
- No `MemberAddress` cache on `WorktreeMembership`. ✓

### Scope-creep rule (added 2026-04-22 after Juan flagged)

**Migrations are no-touch unless the task spec explicitly scopes them.**
This covers both database/SQL migrations AND in-process client-side
migration helpers (e.g., `migrateTeamStateFromWorkspace` in
`cli/go/awconfig/team_state.go`, which lazily synthesizes teams.yaml
from a legacy workspace.yaml on first load). Removing an existing
backward-compat shim is the inverse of adding one and is equally
Juan-level — it needs explicit approval, not architectural-logic
justification.

Add this check to every future review: if the diff touches a file
whose existence is about bridging old → new on-disk or on-DB state,
confirm the task description scoped that work. If not → NO-GO with
scope-creep flag.

### e08b609 — aakq.3+.4 (Shape A refactor) — shipped

**Review history:** 0401d50 was the first attempt; got a NO-GO
from me (after reviewer-agent said GO, Randy and Grace independently
flagged the migration deletion, I flipped). Grace amended to e08b609
with the migration restored.

**Delta-review on e08b609: GO.** All four migration cases handled,
consume-once semantics with disk-persistence assertion, workspace.yaml
not rewritten on migration, `filepath.ToSlash` fix landed, no
regression of prior review items. 28 files touched, all flow from
the refactor; no scope creep.

**Soft items left non-blocking** (Grace's call for future touch):
- `workspaceMembershipForSelection` returns `(nil, nil)` when
  `sel.WorkingDir` empty. Unreachable in production but test-brittle.
- `runRoleNameSet` workspace-membership lookup path has no test.

### aweb-aakr filed (P4, standalone, not under aakq)

Surfaced during e08b609 delta review and Juan's "is workspace.yaml
really legacy?" pushback. After aakq removes active_team, the two
files STILL duplicate team_id/alias/cert_path/joined_at across their
memberships lists. Same cached-copy pattern, lower impact (fields
rarely mutate).

Per Randy: filed as P4 task-candidate (not epic), framed open with
two candidate framings (narrow teams.yaml vs. derive workspace.yaml
from teams.yaml for shared fields), no pre-commitment to direction.
Architectural commitment is Juan-level. Task-comment added on aakq
for lineage.

Scope: drops `WorktreeWorkspace.ActiveTeam` field, deletes
`WorktreeWorkspace.ActiveMembership()` method, replaces with package-
level `ActiveMembershipFor(ws, ts)`, new `LoadWorkspaceAndTeamState`,
deletes `migrateTeamStateFromWorkspace` path. 28 files, ~250 lines net.

All five invariant checks pass:
- `grep ws\.ActiveMembership|workspace\.ActiveTeam` → 0 hits.
- No new method on WorktreeWorkspace taking *TeamState.
- Legacy `active_team` parses-and-discards; workspace.yaml not rewritten.
- LoadWorkspaceAndTeamState does NOT synthesize from workspace.yaml.
- ActiveMembershipFor is package-level, not a method.

**Upgrade-break I was worried about: non-issue.** f51e178
(team_state.go + migration) is ancestor of server-v1.11.0. Every
active 1.11.0+ install auto-healed teams.yaml on first `aw init` /
`aw id team switch`. Blast radius: effectively zero.

**Pre-push fix (1 line, no architectural change):**
- `doctor_fix_local.go` teamStateRepairFromWorkspaceMemberships is
  missing `filepath.ToSlash` on CertPath. Deleted migration had it;
  new helper doesn't. Safe today (normalize runs on load) but
  fragile on Windows. Requested fix before push.

**Soft notes (Grace's call for this PR vs follow-up):**
- `workspaceMembershipForSelection` returns (nil, nil) when
  `sel.WorkingDir` empty. Unreachable in production but test-brittle.
- `runRoleNameSet` workspace-membership lookup now correctly passes
  sel but has no test coverage. Worth a minimal test.

**Release-notes-grade (not this PR):**
- Fresh checkouts with workspace.yaml but no teams.yaml yield raw
  `open .aw/teams.yaml: no such file or directory` on some paths
  (`aw id team list` has a friendlier message). Consolidate before
  1.17.0 tags.

**Test suite health:** Grace reported DNS-only failures in
`go test ./cmd/aw` (127.0.0.1.nip.io, _awid.myteam.aweb.ai).
Confirmed pre-existing flakes in `init_apikey_test.go`; that file
is not in 0401d50's changed-file list. Unrelated.

### Architectural verification: cross-namespace domain/address
- `aw whoami` after aakq.2: for cross-namespace members (bob at
  partner.com/bob in team backend:acme.com), `domain` and `address`
  now disagree. **This is designed-for**, not a bug.
- Confirmed in awid-sot.md §551–573 (cross-namespace membership is
  explicitly a supported case; member_address "is just a string and
  is not constrained to match the team's namespace").
- Confirmed in commit 3a9564a's `_require_member_address_owned_by_did_aw`:
  validation only checks that the address is owned by the member
  did:aw; no team-namespace check.
- Randy's original expectation (awid enforces namespace match) was
  slightly off. The semantics that actually hold: `Domain` = team
  namespace (where I'm a member), `Address` = my presentation address
  (which may legitimately be cross-namespace). Independent fields.
- No cross-namespace whoami test exists in `aw_test.go`. Low priority.

## Dev agents (live snapshot 2026-04-22)

| Alias | Status | Focus | Notes |
|-------|--------|-------|-------|
| grace | active | aweb-aakq | Finished .1/.2, picking up .3/.4 |
| kate  | offline 3d | aweb-aakj | Stale claim; presumed done |
| bob   | offline 6d | aweb-aakh | ac repo; not my scope |

Team.md's dev-agent roster (dave/henry/ivy) is aspirational. Real
flow: Grace drives aakq end-to-end; Randy architects; Juan owns
direction.

## SOT / code alignment

- `aweb/docs/aweb-sot.md` — per-membership address model documented
  (§458). **Lines 835–1040 still describe `workspace.yaml` carrying
  `active_team`.** That section goes stale when aakq.3 ships. Flag
  this in the aakq.8 release PR.
- `aweb/docs/awid-sot.md` — verified aligned with 0.4.0. Cross-
  namespace membership at §551–573 matches the code in
  `awid/src/awid_service/routes/teams.py`.

## What to check FIRST next wake-up

1. Has Grace's .3/.4 staged diff arrived in chat? If so, full
   code-reviewer pass. Explicit checks:
   - `grep -r 'ws\.ActiveMembership\b\|workspace\.ActiveTeam\b' aweb/cli/go`
     returns zero.
   - No new method on `WorktreeWorkspace` that takes `*TeamState`
     internally (that re-centralizes what we just split).
   - Legacy `active_team` in workspace.yaml parses and discards;
     no error, at most a one-time stderr line.
   - `LoadWorkspaceAndTeamState` does not synthesize a TeamState
     from legacy workspace.yaml; missing teams.yaml is an error.
2. Has aakq.9 (silent cert-load error) landed? Review when it does.
3. `git -C aweb log --oneline 05c46b2..HEAD` — what else shipped.
4. Who responded to my awid-sot verification mail to Randy.

## Release gate (Juan directive, this cycle)

Juan set policy: **no release of anything before the full e2e user
journey test passes, and Grace's tasks must be covered in that test.**

Full e2e is `scripts/e2e-oss-user-journey.sh` (run via `make test-e2e`),
1228 lines / 22 phases. Phase 12d "Per-membership addresses" (added
in 89449f1) covers per-membership mail but masks the aakn bug by
calling `aw init` after every `aw id team switch`.

**Resolution** (Randy applied 2026-04-22):

- `aweb-aakq.7` spec now requires extending Phase 12d (or a new
  Phase 12e) with team-switch-WITHOUT-reinit assertions for whoami,
  mail, chat, and channel-advertised address. Must fail on v1.16.0;
  must pass on full Shape A build. Cross-namespace coverage
  explicitly excluded (out of scope for this bug).
- `aweb-aakq.8` spec now lists `make test-e2e green against the
  release candidate` as the first acceptance item, with Juan's
  2026-04-22 policy cited so the gate survives past this epic.
- Randy will file a `ai.aweb/docs/decisions.md` entry capturing
  the release-gate policy as a standing rule. Not yet pushed; check
  next cycle.

## Messages sent this cycle

- mail → grace (workflow clarification + aakq.9 heads-up)
- mail → grace (initial review protocol draft — superseded by her
  reply that correctly invoked AGENTS.md)
- mail → randy (awid-sot verification: cross-namespace domain/address
  divergence is designed-for)
- mail → randy (Juan's release-gate directive mapped onto aakq.7/.8
  scope)
- mail → tom (ac release state: ac v0.5.3 shippable on its own
  against 1.16.0; do NOT bump aweb pin to 1.17.0 yet; release gate
  applies to ac too)
- chat send-and-wait → randy (ack of full-review role + findings)

## Open questions

- **beadhub-legacy** (aweb): 187 ahead / 1227 behind. Preserved
  pending Juan confirmation. Not my call.
- **Cross-namespace whoami test coverage**: low priority, no action
  filed, noted here for next time that file is touched.
- **Membership-field duplication between workspace.yaml and
  teams.yaml** (raised by me this cycle, flagged to Randy): Tom
  confirmed workspace.yaml is CLI-side only (ac doesn't read it),
  so not an ac concern. But team_id/alias/cert_path/joined_at exist
  in BOTH files' memberships lists, which is the same cached-copy
  pattern aakq just fixed for active_team. Proposed future cleanup
  (not this epic): teams.yaml.memberships becomes team-ids only;
  worktree-bound fields live in workspace.yaml.memberships;
  identity-level operations without a workspace need a separate
  mechanism. Waiting for Randy's read on whether to file as a
  future task.
- **"Legacy" language I was using imprecisely**: workspace.yaml is
  NOT legacy as a file. It's the CLI-side worktree↔aweb-server
  binding and owns aweb_url, workspace_id/role_name per membership,
  repo/host metadata. Only its team-state fields (active_team, and
  eventually the membership-list duplication above) are migrating
  out. I've noted this to Juan and will use sharper language going
  forward.
- **ac's own e2e journey**: Tom confirmed ac has its own full gates
  — test-backend + test-frontend + e2e journey — and will run all
  three before any ac tag. No aweb-side action needed on this.
- **Tom's pending audit** (expected reply): ac code paths that
  read/write `workspace.yaml.active_team`, and his decision on
  whether ac stays at v0.5.3 or cuts v0.5.4 pre-1.17.0 bump.

## Reference — invariant checks I applied

- fcbcc00 (aakq.1): ✓ Invariant #1 honored — eliminates
  identity.address coupling over per-membership address.
- 05c46b2 (aakq.2): ✓ No cached copy of MemberAddress introduced.
  Cert is single source of truth per membership.
- aakq epic framing: ✓ Catches the same-team-messaging-class mistake
  at the implementation layer (cached copy that claims to equal its
  source, but drifts).
- No new coupling between the four primitives observed across
  1.11.0–1.16.0. Address work is strictly inside the address
  primitive.
