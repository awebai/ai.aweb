# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-26 (post-v0.5.8 ship; v0.5.9 cleanup held +
test-infra fix landed)

## Current state

**ac main:** 2 commits ahead of origin/main, both unpushed:
- `4f31e116` — test-infra fix (compose port-collision + bootstrap script)
- `b5b1ee1f` — Grace's v0.5.9 architectural cleanup (parallel-registry
  dead-code removal)
- on top of `0336a2c4` (v0.5.8 release tag, shipped)

**aweb (Grace's side):** `ef5c3d7` local, unpushed. Amend chain:
`ee72ee3` → `32bb7c6` (John's N1+N2 wording fold, GO'd) → `ef5c3d7`
(substance change post-Juan's Chesterton-fence challenge: removed the
unused `_baseURL` parameter from `resolveRegistryFallbackURL`,
simplified the call site, updated 4 tests). Channel npm test still
green: 81 passed. **John's GO on ef5c3d7 still pending** — flagged
to him via mail (f1cca8d4) and to Grace via chat to route to him.

**Production:** v0.5.8 live since 2026-04-26 ship. Verified-live leg 1
(/health flip + git_sha) confirmed at ship. Legs 2-3 pending (see below).

## Held push state — three commits, all coord-GO'd

| Commit | Repo | Author-coord | Reviewer-coord | Status |
|--------|------|--------------|----------------|--------|
| ef5c3d7 | aweb | Grace | John GO + Tom ack | **on origin/main** (piggybacked on c250cd1 push, fed3774b coord-miss; gate now at channel re-tag, not main-push) |
| b5b1ee1f | ac | Grace | Tom | GO, holding |
| 4f31e116 | ac | Tom (auto) | n/a (test infra) | self-merged, holding |

**Coord-miss note (fed3774b → c099930e)**: ef5c3d7 reached aweb origin/main inadvertently when Grace pushed c250cd1 (aalk, authorized) — they were stacked locally and `git push` carried both. John's GO message didn't explicitly carve out ef5c3d7 as still-gated, so reasonable read on Grace's side. Picked option (b): leave on main, gate remains at channel re-tag layer (npm consumers don't see ef5c3d7 until next tag fires). ac cleanup-push gate (b5b1ee1f + 4f31e116) is unaffected — those stay local until leg-2 green. Lesson banked for joint coord-protocol amendment to Randy: "GO on stacked commits must explicitly carve scope" — pairs with opt-in handshake.

All three are parked pending verified-live legs 2-3 per Randy's
ship-discipline. Coord-GO chain is complete; waiting only on production
verification.

## What's blocking push: verified-live leg 2 only (legs reframed)

Original framing was wholesale-KI#1-closure attestation across both
legs. **Reframed 2026-04-26 afternoon** after leg 3 came back red on
Amy's CLI re-test:

**Leg 3 RED → architecturally simplified to aalk (continuity) +
aalm (authenticated-lookup, scope-pending-re-query). Earlier "rows
missing for 9/10 agents" framing was built on a false premise.**

Juan corrected (verbal, late-day): the "missing rows" are ALL
ephemeral identities — by design, ephemerals don't get persistent
awid registrations. Only permanent identities do. The
juan.aweb.ai cohort's permanent-only count (randy + Amy) is the
correct state, not a coverage gap. Relayed to Randy (cea16d13) +
John (3cf9d56c).

(Parallel awid server-side bug discovered by Grace: LIST endpoint
accepted ownership_proof=true with a non-matching controller_did
key — Goto's lane to fix; orthogonal to the cohort-framing
correction.)

Updated picture:

1. **aalk (c250cd1, GO sent, push imminent)**: TOFU
   continuity-fallback when registry address row is missing OR
   anonymous-filtered. Closes Amy's empirical case because she has
   Randy pinned.
2. **aalm (P1, scope-pending-cohort-re-query)**: CLI Go
   RegistryResolver does anonymous awid lookups; permanent
   identities with org_only/team_members_only reachability return
   404 to anonymous callers even though rows exist. Authenticated
   requests + awid server-side visibility filtering closes it.
   Cross-coord: Grace (CLI signing) + Goto (awid server filter) +
   Juan (architectural call on request-signing scheme). Scope
   contingent on re-query bounded to permanent identities; if the
   cohort is small (just randy), aalm closes a known-narrow gap.
3. **aall**: **close-as-no-action**. Nothing to backfill —
   ephemerals correctly have no awid rows; permanents do.

**Final ship-mail line LOCKED** (per John 59b31a27, after Avi
briefing 9ed78982 superseded three prior drafts):
"KI#1 closes for continuity case (aalk: known-agent pin fallback).
Authenticated CLI lookup for org_only / team_members_only address
visibility remains open under aalm (P1) — landing in v0.5.9."

**Tracker state** (per John 59b31a27):
- aweb-aall: CLOSED as not-a-bug.
- aweb-aalo + aweb-aalp: filed P3 in Goto's lane (awid server-side
  correctness bugs surfaced during the cohort investigation —
  ownership_proof acceptance + visibility-filter consistency).
- aalk c250cd1: Grace push pending opt-in handshake; John GO sent.
- Avi sign-off: pending (11d offline; expected slow leg).

**Brief Randy-escalation false-alarm on ac dashboard persistence path
(f5ea2abf → 17c364ec)**: I investigated for ~30 min before reframe.
Findings worth carrying: ac write paths
(`services/permanent_addresses.py:assign_permanent_team_address`,
`routers/agent_addressing.py:update_agent_address_reachability`) DO
call `registry_client.register_address` / `update_address`. Read
paths (dashboard.py, agent_lifecycle.py) DO read via
`list_did_addresses`. Both interact with aalm: when aalm fix lands,
ac must use the authenticated client so preconditions read true row
state, not visibility-filtered state. Flagged to Randy
(f6742f14) + John (7c574f2d) for aalm fix-shape scoping.

**ac parallel-address-authority concern returns to v0.5.9 scope** (not
launch-blocking, per Randy's reframe). Two-reachability-fields UX
confusion in dashboard is real but v0.5.9-pace.

**Ship-mail-to-Charlene call** is Randy's authority (with Avi sign-off
— Avi 11d offline, expected slow leg). I deferred when John pinged
me (0bcc8d02 → John; 729ecf18 → Randy).

**Leg 2 still load-bearing for aalf empirical attestation.** Juan
triggers dashboard send from app.aweb.ai → Randy reads JSON inbox →
confirms `verification_status=verified`. This is the gate for v0.5.8
ship-mail and for the v0.5.9 cleanup pushes.

**v0.5.9 cleanup pushes are surface-independent of aalk** (mailed to
John 4e742bfe + Randy 8009090b, parallel multi-gate-mail-visibility):
- ac b5b1ee1f: cloud-side parallel-registry dead-code removal — zero
  overlap with aalk's CLI Go resolver-init surface.
- ac 4f31e116: ac/scripts/ test-infra fix — no protocol surface.
- aweb ef5c3d7: channel TS package error message + dead-arg cleanup —
  zero overlap with CLI Go resolver-init.

So: **pushes proceed when leg 2 lands green**. Do not wait for aalk
ship. Bundling would couple unrelated work and slow Grace's
RCA-first cadence on aalk.

When leg 2 green — **v0.5.9 ship sequence** (revised after aweb 1.18.3
publish per John 1031f72a, my plan 546bca16):

1. Bump `aweb>=1.18.3` (was 1.18.2) in backend/pyproject.toml + `uv sync
   --refresh` (banked: feedback_uv_sync_refresh_after_pypi_publish.md).
2. Bump version 0.5.8 → 0.5.9 + `uv lock`.
3. Commit pin-bump + version-bump (single commit or two; doesn't
   matter — both ride v0.5.9 tag).
4. Run release-ready gate chain (per banked
   feedback_makefile_is_authoritative_gate_chain.md): make release-ready
   covers test-backend + test-frontend + test-two-service + verify-remote/model/migrations.
5. Tag v0.5.9 + `git push origin v0.5.9` individually (banked:
   feedback_push_tags_individually.md).
6. GHA fires; verified-live legs 2-3 re-run against v0.5.9 substance
   (leg-2 dashboard probe = aalf attestation on v0.5.9; leg-3 CLI =
   aalm attestation if user has 1.18.3 CLI).
7. Randy mails ship-framing to Charlene with locked single-gap line.

**v0.5.9 commit set on ac main when tag fires**:
- b5b1ee1f (parallel-registry dead-code cleanup)
- 4f31e116 (test-infra fix: compose port + bootstrap script)
- 5844ffba (Mia's UX fix: Reachability/Message-acceptance disambiguation;
  pending her push, GO'd)
- NEW: pin-bump 1.18.2 → 1.18.3 + version-bump 0.5.8 → 0.5.9

## Test-infra fix (4f31e116) — context

Today (2026-04-26), Juan asked "are all the docker-backed e2e user
journey scripts working?" + "we have to test all... never say again
that something requires manual-running anything." Surveyed the full
Makefile gate matrix and ran all 7. Outcome:

| Gate | Result |
|------|--------|
| test-backend (full) | 1170 passed |
| test-frontend | 96 passed |
| test-two-service | 11 passed |
| test-cloud-user-journeys-local-aw | 138 passed + 4 Playwright |
| test-cloud-user-journeys-installed-aw | 138 passed + 4 Playwright |
| test-frontend-e2e | 4 Playwright passed |

**Bug 1 (script-fix in 4f31e116)**: `make test-cloud-user-journeys-local-aw`
was broken under make. Root cause: ac/Makefile:16 has bare `export`
which leaks Make's `?=` defaults (`AWEB_CLOUD_PORT=8001`) into the
script's shell. Docker Compose's variable interpolation puts shell-env
> --env-file, so `.env.e2e`'s random-port value was silently ignored;
api bound to 8001, host curl to random port timed out. Direct-run
(no make) was green. Fix: `compose_local()` now explicitly exports
the random ports on every `docker compose` invocation. Banked memory:
`feedback_compose_var_interpolation_make_export.md`.

**Bug 2 (new bootstrap script in 4f31e116)**: `make local-container`
needed a `.env.local-container` that the repo doesn't ship — only
`.env.local-container.example` with `REPLACE_WITH_*` placeholders that
fail config validators. Added `scripts/bootstrap-local-container-env.sh`
which generates a working file: random secrets, blanked optional
secrets (OAuth/Stripe/AWS/Sentry), plus `AWEB_PARENT_CONTROLLER_KEY`
and `AWEB_CUSTODY_KEY` for hosted-identity flows.

**Follow-up not done yet**: `make local-container` still doesn't
auto-bootstrap the AWID parent namespace (the journey script does this
internally via `bootstrap_awid_parent_namespace`). Worth folding into
the Makefile target so frontend-e2e is one command from a fresh
checkout. P3.

## Lane state

- **Grace**: holding push on aweb ef5c3d7 + ac b5b1ee1f (already
  GO'd). aalk c250cd1 GO sent and push imminent on aweb side (a
  separate substance commit, not the v0.5.9 cleanup parking lot).
  Likely also picks up CLI-side of aalm if Juan ratifies the
  request-signing scheme.
- **John**: aalk dispatched + GO'd; reframed KI#1 closure into the
  three-layer picture (aalk continuity / aall first-contact / aalm
  authenticated-lookup). Pinged me on ship-mail framing call;
  I deferred to Randy.
- **Randy**: holds ship-mail-to-Charlene call. Dual gate now: leg 2
  green AND ship-mail framing accepted (under restricted-three-layer
  framing). Banked
  feedback_reproducer_synthetic_state_assumes_user_invariants.md.
- **Goto**: aall (controller-key backfill) + awid server-side aalm
  in his lane. Cross-coord with John for CLI-side aalm.
- **Juan**: owns architectural call on aalm request-signing scheme.
  Plus controller-key authority for aall backfill.
- **Amy**: standing down for aalk publish (post-1.18.3). aale render
  attestation green on her stack — KI#3 closed independently.
- **Mia**: still offline; earlier stand-down moot.
- **Tom (me)**: dormant pending leg 2 (Juan dashboard probe).

## URGENT: prod observably broken — hotfix v0.5.8.1 in flight

**Symptom**: Any CLI on aweb 1.18.3+ trying to mail a hosted-custodial
identity gets HTTP 422 "to_address must match the to_stable_id
recipient." Reproduced by me + Amy. Population-level on the cohort,
not target-specific.

**Root cause**: aweb 1.18.2 server (running in v0.5.8 prod) has the
strict pre-d4fb982 matcher that requires same-agent_id between
to_stable_id-resolved and to_address-resolved rows. aalm in 1.18.3
CLI started populating to_stable_id properly via authenticated awid
lookups, exposing pre-existing data inconsistency in cloud's mounted
aweb DB (multiple agent rows for same identity, likely from
replacement history).

**Three layers of fix**:

1. **Mode 1 (server, d4fb982 in aweb 1.18.4)**: `_recipient_identity_matches`
   accepts agent_id OR did_aw OR did_key match. Lands in prod via ac
   v0.5.8.1 hotfix (awaiting Juan auth).
2. **Mode 2 (CLI, 7a770c8 in aweb main, future 1.18.5)**: signEnvelope
   was fail-opening on AWID 404 for direct address targets; now
   fail-closes. Prevents silent unverifiable chat wires.
3. **Underlying registry-sync gap**: local certs exist for
   juan.aweb.ai/<members> but AWID has no team row + no member rows.
   Data-layer issue not solvable by code; needs controller-key +
   data-owner coord (Goto's lane + Juan's authority for
   juan.aweb.ai). Per Grace a77930c2: `aweb:juan.aweb.ai` local cert
   exists, AWID can't authorize it. Registry-sync/data repair OR
   reachability policy change required.

## Hotfix v0.5.8.1 plan (pending Juan auth)

1. Branch `hotfix/v0.5.8.1` from `origin/main` (= 0336a2c4 v0.5.8 tag).
2. Apply ONLY: aweb pin 1.18.2 → 1.18.4 in backend/pyproject.toml +
   `uv sync --refresh` + `uv lock` + version bump 0.5.8 → 0.5.8.1.
   No other substance.
3. Commit on the hotfix branch (single commit).
4. Run `make release-ready` (banked discipline:
   feedback_makefile_is_authoritative_gate_chain.md).
5. Tag `v0.5.8.1` on the branch tip.
6. **Push tag only**, NOT main, to avoid piggybacking the
   held v0.5.9 cleanup commits (b5b1ee1f + 4f31e116 + 5844ffba).
   Same coord-miss class as fed3774b on aweb side.
7. Render auto-deploys.
8. Empirical attestation: I rerun mail probe → expect HTTP 200 +
   verification_status=verified. Amy reruns her probe.

After hotfix: cleanup commits stay parked. v0.5.9 plan unchanged
(cleanup + Mia UX + Mia tests + version bump 0.5.8.1 → 0.5.9). Pin
target stays aweb>=1.18.4 (pin already bumped in v0.5.8.1, no further
bump needed for v0.5.9 unless 1.18.5 is preferable).

## v0.5.9 release-readiness — substance done, holding on aweb 1.18.6

**v0.5.8.1 LIVE in production** (release_tag=v0.5.8.1, aweb 1.18.4,
deployed 2026-04-26 21:12Z). Mode 1 strict-matcher 422 closed
empirically per Amy's fb258854 attestation
(verification_status=verified on Tom→Amy probe 3175b394).

**aweb 1.18.5 PUBLISHED** (PyPI 21:08:58Z, npm 21:11:31Z).
Server-side substance includes Grace's d4fb982 (Mode 1 server fix)
+ aalq audit + identity-messaging-contract + sub-binding cleanup
+ hosted-custodial e2e matrix.

**v0.5.9 substance complete on origin/main**:
- b5b1ee1f (parallel-registry cleanup)
- 4f31e116 (test-infra fix)
- 5844ffba + d1511867 (UX disambiguation: Reachability vs Message
  acceptance vs Address visibility)
- f3145b14 + 479411cf (Mia's auth_bridge alias-classifier fix per
  contract L73-75)

**release/v0.5.9 @ 38d047d5** in `/tmp/ac-v059-workdir/ac-v059`
(branch off origin/main + pin bump aweb>=1.18.5 + version 0.5.9).
**ALL test gates GREEN per Juan's "ALL tests pass" directive**:
- backend full: 1174 passed
- frontend: 96 passed (1 lint warning)
- two-service: 11 passed
- journey-local-aw: 138 + 4 Playwright passed
- journey-installed-aw: 138 + 4 Playwright passed
- frontend-e2e (via local-container): 4 Playwright passed
- release-verify-remote/model/migrations: pass

**Tag/push HELD per John 2ff836b9** until aweb 1.18.6 ships. Reason:
1.18.5 CLI selector misclassifies slash-prefixed hosted-team labels
(e.g. juan.aweb.ai/randy) as direct AWID addresses — fail-closes
correctly but blocks every 1.18.5 user's outbound to hosted-custodial
team members. Workaround: plain alias (`aw mail send --to randy`).
Real fix: Grace's CLI classifier fix in 1.18.6 (RCA in flight +
2 more bugs in 1.18.6 scope per John ff2ec457).

**v0.5.9 pin bumps to aweb>=1.18.6 once shipped**, then re-run all
gates + tag + push.

**Architectural option B endorsed** (per Juan-direct, Tom 69e35c50,
John 0a4573fb): hosted-team auth via aweb server using local cert
data + CLI classifier fix. Preserves my v0.5.9 substance as-is.
Option A (ac team-sync to AWID for personal-owned hosted teams)
filed as Task #29 v0.5.10+ ticket — long-term cleanup independent
of v0.5.9 path.

## What to check FIRST on next wake-up

1. Mail/chat for Juan signaling leg 2 (dashboard send executed).
2. Mail from Randy: ship-framing-to-Charlene trigger (he'll mail
   when leg 2 + framing accepted).
3. Mail from John: Grace's aalk RCA determination + reproduce-locally
   signal (timing: hours-to-days; not on critical path for v0.5.9
   cleanup push).
4. `aw workspace status` — broad situational awareness.
5. Time-bound carry: GHA Node 20 actions deprecation by 2026-06-02
   (~5 weeks out).

## Open ac branches

- `main` at `4f31e116` (local) / `0336a2c4` (origin) — see "ac main"
  above for the 2-commit gap.
- `aaga-archive` — remote-only; preserved per Randy's note.

## Memory file count

20 memories indexed in MEMORY.md (was 19; added
`feedback_compose_var_interpolation_make_export.md` today).

## Joint coord-protocol amendment to Randy (still parked)

Tom + John convergence on the two-layer canonical+degraded coord-borrow
protocol: opt-in handshake + 60s opt-out floor. Plan unchanged: submit
after v0.5.8 + v0.5.9 wholesale close. Anchor: now 4 coord-borrows
(aala.10, aaja.6, aalf, plus the Grace v0.5.9 cleanup which followed
the same shape).
