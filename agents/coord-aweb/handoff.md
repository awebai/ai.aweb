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

## Review protocol with Grace (set this cycle)

- Grace stages .3/.4 locally on main (aweb AGENTS.md forbids WIP
  branches).
- Pastes the `git diff main...HEAD` into chat to me.
- I respond go/no-go in chat.
- She pushes to main on approval.
- Escalation: architecture → Randy; direction → Juan; bugs surfaced
  mid-review → file as aakq subtask or standalone aweb-aak bug.

I had offered her a "feature branch PR" option — that was wrong; she
correctly flagged the AGENTS.md rule.

## Active work: aweb-aakq (P1 epic)

**Shipping order:**
1. Channel plugin precedence flip (aakq.1) — **landed fcbcc00**,
   reviewed, pass-with-notes.
2. Go CLI precedence flip (aakq.2) — **landed 05c46b2**, reviewed,
   pass-with-notes.
3. Drop `workspace.yaml.active_team` field (aakq.3) — **pending,
   awaiting Grace's diff**.
4. Migrate ~15 `ActiveMembership` / `ActiveTeam` call sites to
   `TeamState` / `ActiveMembershipFor` (aakq.4) — pending, paired
   with .3.
5. Remove `applyTeamStateToWorkspaceCache` from runTeamSwitch (aakq.5).
6. Doctor migration (aakq.6).
7. E2E regression for Amy's two-team scenario (aakq.7).
8. Release aweb 1.17.0 / CLI 1.17.0 / channel 1.3.0 + ac pin (aakq.8).
9. **Follow-up from my .2 review**: silent cert-load error swallow at
   `cli/go/awconfig/selection.go:161` — Randy is filing as aakq.9, P2.

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
