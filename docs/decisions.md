# Decisions

When the plan changes, record it here with the commit hash(es) that
mark the moment. Agents check this for entries newer than their last
handoff to detect that the world changed.

---

## 2026-04-25 — BYOIT cross-machine team join + multi-membership launch hardening (aala epic)

**Commits (aweb):**
- `ff92358` Implement cross-machine team cert fetch (aala.1 SOT + aala.2/.3/.4/.5/.7)
- `9b2eed3` Add cross-machine fetch-cert e2e (aala.6/.8/.9/.11/.12)
- `ba133d4` Fix BYOIT certificate pickup guidance (aala.9 follow-up)
- `898556d` release: aweb server 1.18.0, aw CLI 1.18.0, awid-service 0.5.0 (tagged `server-v1.18.0`, `aw-v1.18.0`, `awid-v0.5.0`, `awid-service-v0.5.0`)

**Decision maker:** Juan (architectural framing on awid storing signed public cert blobs; Grace executed the work breakdown end to end)

**Decision.** Pre-aala, BYOIT cross-machine team join was structurally broken: `aw id team add-member` signed a certificate in memory, registered metadata only at awid, and lost the blob. From a different machine, `aw id team fetch-cert` had nothing to fetch, and `aw id team accept-invite` required local controller state. aala makes the cert lifecycle truly cross-machine: awid stores the full signed cert blob, controller-side `add-member` uploads it after signing, invitee-side `fetch-cert` downloads + verifies + installs.

**What changed structurally:**

1. **awid persists full signed cert blobs.** `public_certificates` table gains a nullable `certificate TEXT` column (additive migration). RegisterCertificate now validates the blob's signature against the team public key + the caller's controller signature in one atomic transaction at INSERT time; either the whole record lands or none does. (aala.2)

2. **New authenticated awid fetch endpoint.** `GET /v1/namespaces/{domain}/teams/{name}/certificates/{cert_id}` returns the signed blob in a JSON envelope (base64 of exact UTF-8 team certificate JSON). Path-signature auth using the caller's identity DID key. Authorization is subject-only: caller must equal the cert's member_did_aw. Pre-blob records return 409 with reissue guidance. (aala.3)

3. **CLI add-member uploads the blob and prints fetch-cert.** No invitee-side state is written from the controller's machine. (aala.4)

4. **CLI fetch-cert is the cross-machine cert install path.** Verifies signature + member_did_aw + team_id locally before writing `.aw/team-certs/{team_id}/certificate.pem`. Refuses to overwrite an existing different cert by default; `--force` opt-in. Same-cert idempotent. (aala.5)

5. **accept-invite is a same-machine helper for the controller's own machine.** Conservative path per Grace's call: fork between "redesign" and "rename + clarify" resolved as the latter. Help text + error messages updated; cross-machine flows go through request → add-member → fetch-cert. (aala.6)

6. **Identity-scoped messaging tolerates multi-team DID membership.** `lookup_identity_agent_context` no longer raises 409 when an identity-scoped request finds multiple active local-agent rows for the same DID. Team-scoped (cert-auth alias-scoped) sends still reject ambiguity. test_messages_http carries a fixture with two active local-agent rows on the same DID exercising BOTH identity-scoped AND team-scoped paths (test contract Randy added during review). (aala.7, supersedes aweb-aakz)

7. **CLI help text + aw init reality.** Stale references to impossible certificate locations removed. Error strings on `aw init` and `aw run` point cross-machine users at `request → add-member → fetch-cert`, not at the accept-invite path that fails for invitees. (aala.9 + ba133d4 follow-up)

**Trust model preserved:**
- awid stores public cert blobs (signed offline by team controller; uploaded as inert bytes).
- awid never holds the team controller private key.
- awid validates blob signatures against the team public key it already has.
- DNS still anchors trust; crypto verifies it. Invariant #2 holds.

**User-visible changes for release notes:**
- New: `aw id team request` and `aw id team fetch-cert` commands; new awid fetch endpoint.
- Behavioral change: `aw id team accept-invite` is now a same-machine helper for the controller. Cross-machine flows use the new request/fetch-cert path.
- Fixed: `aw mail send` no longer 409s for persistent did:aw with multiple team memberships.
- Schema: awid `public_certificates` gains nullable `certificate TEXT`. Pre-1.18 rows return 409 with reissue guidance from the fetch endpoint (no silent reconstruction).

**Closes:**
- `aweb-aala` (epic — BYOIT cross-machine + multi-membership launch hardening)
- `aweb-aala.1` through `.9` + `.11` + `.12`
- `aweb-aakz` (multi-membership mail 409, superseded by aala.7)
- `aweb-aait` (fetch-cert from awid, superseded by aala.5)

**Open under aala:**
- `aweb-aala.10` — cloud `aweb-cloud` alignment (Tom's lane). ac v0.5.5 will pick up the new contract once aweb 1.18.0 tags. Mia is on the surface walk.

**Open as design question (not in scope for aala):**
- `aweb-aakr` (P4) — membership-field duplication between teams.yaml and workspace.yaml. Architectural commitment is Juan-level; deferred.

**Release mechanics:**
- aweb server: 1.17.0 → **1.18.0**
- aw CLI: 1.17.0 → **1.18.0** (lockstep with server)
- awid-service: 0.4.0 → **0.5.0** (cert blob storage + new fetch endpoint)
- @awebai/claude-channel: stays at **1.3.1** (channel not touched in aala)
- ac aweb pin: `aweb>=1.17.0` → `aweb>=1.18.0` + `awid-service>=0.4.0` → `awid-service>=0.5.0` (Tom handles in ac v0.5.5)

**Gate log + SOT analysis** mailed to Randy 2026-04-25 (5da4621a). All gates green (Gate 1 unit/integration 368+144+cli+72; Gate 2 e2e 159 PASS all 22 phases; Gate 3 v1.17.0 regression arm correctly fails on Phase 11a's `add-member prints fetch-cert` assertion). CTO approval recorded with the release commit.

---

## 2026-04-23 — aweb-cloud v0.5.4 ships; picks up aweb 1.17.0

**Commits (ac):**
- `feee297c` Align admin managed namespace env lookup (aweb-aakw)
- `14821e47` test(e2e): read active_team from teams.yaml, not workspace.yaml (aweb 1.17.0) (aweb-aakx)
- `33a4c089` release: v0.5.4, aweb 1.17.0 + awid-service 0.4.0 deps (tagged `v0.5.4`)

Two earlier fixes shipped on top of v0.5.3 before the v0.5.4 bump and
are also carried by this release:
- `2f0c42cc` Fix JWT revocation UTC handling (aweb-aakv)
- `2425cc7e` Stabilize backend tests under make env (aweb-aakt)

**Decision maker:** Randy (written tag-approval) + Tom (coord-cloud)

**Decision.** v0.5.4 is a dependency-alignment + test-infra release.
It picks up aweb 1.17.0 (aakq epic — active_team moved from
workspace.yaml to teams.yaml on the CLI side) and aweb 1.17.0's
server-side aaks fix (tasks_service.py no longer SELECTs the
nonexistent `w.current_branch` column, so `aw work active` at
app.aweb.ai stops 500-ing). awid-service pin is tightened from
`>=0.3.1` to `>=0.4.0` to match the version already resolving
transitively. Two ac-side corrections land alongside: aakw
consolidates admin.py to read the same env-var name pydantic
Settings reads (`MANAGED_NAMESPACE_BASE_DOMAIN`, unprefixed),
and aakx updates the two-service e2e fixtures to read active_team
from teams.yaml per 1.17.0. Zero customer-visible feature change;
prod behavior improves on the latent aaks 500.

**Release protocol exercised end-to-end for the first time:**
1. Per-gate log (one mail per gate) — ran all 6 release-ready
   gates (release-verify-remote, release-verify-model,
   release-verify-migrations, test-backend, test-frontend,
   test-two-service) against post-bump `.venv` (aweb==1.17.0,
   awid-service==0.4.0 resolved from PyPI). 1170 backend tests
   passed, 94 frontend tests passed, 9 two-service tests passed.
2. SOT analysis mail — walked aweb-sot, awid-sot, trust-model,
   ac/sot for drift. None found. Operator edge on aakw named
   honestly in release notes (anyone who had set only the
   AWEB_-prefixed env var form loses the override).
3. CTO written approval.
4. Manual `git push origin main` then `git tag -a v0.5.4 && git
   push origin v0.5.4` — explicitly NOT `make ship` because
   `ship-tag` auto-pushes the tag, which would short-circuit the
   approval step.

Two process-lesson memories got banked for future coord-cloud
instances during the run:
- Reproduce the exact invocation path (`make X` not the underlying
  tool directly); a simplified harness silently strips env-file
  loading, cwd, and fixture wiring.
- Trust the Makefile as the authoritative gate chain; a skill doc
  can list adjacent targets that are not in the `release-ready`
  chain (we chased `test-cloud-user-journeys-local-aw` for two
  hours when the actual gate was `test-two-service`).

**Closes:**
- `aweb-aakv` (test_user_revoke_before_rejected_with_db failed under
  non-UTC postgres sessions — naive datetime written to timestamptz)
- `aweb-aakt` (test suite not env-baseline-isolated from developer
  `.env.dev`; session-autouse scrub added)
- `aweb-aakw` (admin.py env-var consolidation — single source of
  truth with pydantic Settings)
- `aweb-aakx` (two-service e2e read active_team from teams.yaml
  per aweb 1.17.0)
- `aweb-aaks` (reaches hosted users via the aweb pin pickup — fix
  is internal to aweb server; ac gains it for free via >=1.17.0)

**Still open:**
- `aweb-aakr` (P4, teams.yaml/workspace.yaml memberships overlap —
  CLI architectural question, not ac-owned).

**GHA:** release tag push triggered aweb-cloud CI/CD run
`24859523654`. Image publish to GHCR follows on green.

---

## 2026-04-23 — Collapse duplicate SoT for active-team and active-address (aakq epic)

**Commits (aweb):**
- `fcbcc00` fix(channel): prefer cert member address (aakq.1)
- `05c46b2` fix(cli): prefer cert member address in selection (aakq.2)
- `e08b609` refactor(cli): move active team selection to teams state (aakq.3 + .4)
- `0b24ad1` fix(cli): stop syncing team switch to workspace cache (aakq.5)
- `4b15d3d` fix(channel): read active team from teams state (aweb-aaku)
- `d2d59a5` test(e2e): cover team switch without reinit (aakq.7)
- `f120888` fix(cli): surface active cert load errors (aakq.9)
- `25cf3f5` fix(cli): move doctor active team to teams state (aakq.6)
- `cb8f7f5` release: aweb server 1.17.0, aw CLI 1.17.0 (tagged `server-v1.17.0`, `aw-v1.17.0`)
- `bb668be` release: @awebai/claude-channel 1.3.0 (tagged `channel-v1.3.0`)

**Decision maker:** Juan (architectural framing from Randy, driven end-to-end by Grace + John)

**Decision.** `teams.yaml` is now the single source of truth for active-team and active-address selection. `workspace.yaml` is the aweb coordination binding only (aweb_url, workspace_id per membership, repo/host metadata). The previous arrangement — where both files carried `active_team` and some CLI paths read one while others read the other — created silent drift. Amy's 2026-04-21 two-team activation surfaced it as user-visible: `aw whoami` reported hybrid identity, `aw id team switch` left workspace.yaml stale, outbound `from_address` drifted, channel plugin advertised the wrong address.

**What changed structurally:**
1. `WorktreeWorkspace.ActiveTeam` field and `WorktreeWorkspace.ActiveMembership()` method removed (aakq.3 + .4). Call sites migrated to package-level `ActiveMembershipFor(ws, ts)` that forces callers to hold both.
2. `applyTeamStateToWorkspaceCache` helper removed (aakq.5). `aw id team switch` writes only teams.yaml.
3. Channel plugin reads `active_team` from teams.yaml (aaku). Anti-regression test locks the invariant.
4. `aw doctor` check id `local.workspace.active_team` renamed to `local.teams.active_team` (aakq.6). Fix writes teams.yaml.
5. E2E journey (`scripts/e2e-oss-user-journey.sh`) extended with switch-without-reinit assertions that fail on v1.16.0 and pass on Shape A (aakq.7). Release-gate regression coverage.
6. Active-cert load errors are now surfaced (aakq.9) instead of silently swallowed.

**Lazy-migration preserved.** A user upgrading from ≤ v1.10.3 who has workspace.yaml with `active_team` but no teams.yaml still works: `LoadTeamState` synthesizes teams.yaml from the legacy workspace.yaml on first read and saves it to disk. workspace.yaml is not rewritten; the legacy field stays on disk but is ignored by all post-1.17 consumers. Removing the migration path was attempted (0401d50) but flipped to NO-GO after Grace's and John's independent traces surfaced the dormant-install case; the restored path and a positive migration test are in e08b609.

**User-visible changes for release notes:**
- `aw doctor --json` check id rename `local.workspace.active_team` → `local.teams.active_team`. Covers the same failure class; consumers parsing the old id should update.
- `aw id team switch` now takes effect immediately for all coordination commands (mail, chat, whoami) without needing `aw init`. Matches how users already expected it to behave.
- Active-cert corruption now surfaces as a clear error instead of silent fallback to `identity.yaml.address`.

**Closes:**
- `aweb-aakq` (epic — collapse duplicate sources of truth)
- `aweb-aakn` (workspace.yaml.active_team drift after team switch)
- `aweb-aako` (identity.yaml.address preferred over cert.member_address)
- `aweb-aaku` (non-Go consumers — channel, e2e script, docs — broken by aakq.3's field removal)

**Still open (as design questions, not bugs):**
- `aweb-aakr` (P4): `team_id`, `alias`, `cert_path`, `joined_at` appear in both `teams.yaml.memberships` and `workspace.yaml.memberships` — same cached-copy pattern aakq just fixed for `active_team`, lower mutation rate. Two candidate framings (narrow teams.yaml vs. derive workspace.yaml for shared fields). Architectural commitment is Juan-level; not committed to a direction.

**Release mechanics:**
- aweb server + aw CLI: 1.16.0 → **1.17.0**
- @awebai/claude-channel: 1.2.0 → **1.3.0**
- ac aweb pin: `aweb>=1.16.0` → **`aweb>=1.17.0`** (Tom handles in ac v0.5.4 after aweb 1.17.0 tags)
- awid-service: stays at **0.4.0** (no aakq changes)

**Gate log + SOT analysis** mailed to Randy before tag per the 2026-04-22 + 2026-04-23 pre-ship protocols. `make test-e2e` green on Shape A (139 PASS); aakq.7 regression pair logged (PASS on Shape A, 4 FAIL on v1.16.0 — the 4 failing assertions are exactly the aakn drift surfaces, proving the test works). CTO approval in writing before tag; approval recorded with the release commits.

---

## 2026-04-22 — Release gate: full e2e user journey must pass

**Decision maker:** Juan (relayed via John / coord-aweb)

No release of anything (aweb server, aw CLI, awid-service,
@awebai/claude-channel, aweb-cloud) is cut before the full e2e user
journey test passes green. In the aweb repo, that's
`scripts/e2e-oss-user-journey.sh` run via `make test-e2e`. The full
phase suite must run clean — no skipped phases, no warnings-only
passes. In-flight tasks that change user-facing behavior must land
their coverage inside that journey, not alongside it as a separate
test file.

Why: two coordinated bugs (aweb-aakn, aweb-aako) shipped as part of
v1.16.0 without the multi-team flow being covered end-to-end. The
per-membership address phase (Phase 12d, commit 89449f1) called
`aw init` after every `aw id team switch`, which masked aakn by
rewriting workspace.yaml. A proper regression test has to exercise
what real users do, not what tests do for convenience.

Applies to: every release, every repo, every agent doing release
work. This is a standing rule, not a one-off for the aweb-aakq
epic that surfaced it.

Affects: `aweb-aakq.8` release acceptance criteria (explicit gate);
future release subtasks inherit the same gate. Coordinators (John,
Tom, Goto) enforce in their respective repos.

---

## 2026-04-21 — Amy gets a second address at aweb.ai/amy

**Decision maker:** Juan

Amy's persistent `did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ` now holds two
public addresses: the original `juan.aweb.ai/amy` and the new
`aweb.ai/amy`. Both have reachability `public`. Amy is the canonical
support address for aweb; routing `aweb.ai/amy` to her makes the
public-facing address match the company domain.

Steps taken (all on Juan's workstation, 2026-04-21 21:47 UTC):
1. Verified `aweb.ai` is BYOD at awid; controller `did:key:z6Mkgpop…EuVn`
   matches `_awid.aweb.ai` TXT.
2. Installed the controller seed from `ac/.env.production`
   (`AWEB_PARENT_CONTROLLER_KEY`) at
   `~/.config/aw/controllers/aweb.ai.key`, overwriting a stale key
   (backed up as `.bak-2026-04-21`).
3. `aw id namespace assign-address --domain aweb.ai --name amy
   --did-aw did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ --reachability public`
   → address_id `69c4346c-a2d6-4c0d-b626-359884467eff`.
4. Created team `aweb:aweb.ai` (team did:key `z6MkhSLsj1bk…NiH2`)
   and issued Amy a persistent cert with `member_address=aweb.ai/amy`
   (certificate_id `30324a6d-e8e3-432a-bc31-5943875bc51d`). Cert saved
   at `agents/support/.aw/team-certs/aweb__aweb.ai.pem`; membership
   added to `teams.yaml`.

Later the same day (2026-04-21 ~21:56 UTC), at Juan's direction,
activated outbound-as-`aweb.ai/amy`:
5. `aw id team switch aweb:aweb.ai`.
6. `aw init --aweb-url https://app.aweb.ai/api` → aweb auto-provisioned
   a second workspace for the new team, `workspace_id
   ad83997e-5380-49a8-9867-aea3b31ebbd2`. Both memberships now carry
   workspace_ids in `workspace.yaml`.

Active sender is now `aweb.ai/amy`. Inbound for both addresses
continues to reach Amy: mail is keyed by `did_aw` on the aweb side,
so `aw mail inbox` returns the same envelope list regardless of which
team is active. Switching is cosmetic (changes the cert the CLI
presents, and thus the `from_address` in outbound messages).

CLI gotcha surfaced during activation: `aw id team switch` updates
`.aw/teams.yaml` but not `.aw/workspace.yaml.active_team`, so
coordination commands continue using the old team until workspace.yaml
is edited. Reported to Randy; workaround in Amy's handoff.md.

Affects: support agent (`agents/support/`), `aw` CLI
(`runTeamSwitch` in `cli/go/cmd/aw/id_team.go`).

---

## 2026-04-18 — Idempotent address registration at awid

**Commits:**
- aweb: `3b264f0` (awid-sot §Addresses Idempotency); epic aweb-aajw,
  subtask aweb-aajw.15

**Decision maker:** Juan

Symmetric with the resume-from-partial decision on register_did:
`POST /v1/namespaces/{domain}/addresses` becomes idempotent on
exact (domain, name, did_aw, current_did_key) match. Any mismatch
stays 409. Dave surfaced the gap in his aajw.8 review — if awid
accepts an address but the cloud transaction commit then fails, the
retry driven by aajw.13's resume path would 409 without this
behavior, orphaning the address at awid.

Rejected alternatives:
- Server-side pre-check via GET before register — extra round-trip
  on every init, more code on the cloud side.
- Accept for pre-launch with operational cleanup later — reverses
  the parallel decision we took on register_did and leaves
  retry-after-failure unusable.

---

## 2026-04-18 — Resume-from-partial bootstrap, not awid DID cleanup

**Commits:**
- aweb: epic aweb-aajw, subtask aweb-aajw.13

**Decision maker:** Juan

On the API-key persistent bootstrap, awid registration now happens
BEFORE /workspaces/init (aajw.6). If /workspaces/init fails after
awid registration succeeds, a naive retry generates a fresh keypair
and orphans the first did:aw at awid. Dave surfaced this in his
review of 2b2e16f.

Chose option 2 of three: the CLI persists the signing key and
derived identity material to a local partial-init file BEFORE
calling awid, then reuses it on retry. Successful completion
removes the file. awid stays append-only — no cleanup endpoint.

Rejected alternatives:
- Accept the orphans for pre-launch and add operational cleanup
  later — leaves unbounded drift at awid.
- Add an awid endpoint to delete unbound did:aw entries — violates
  the append-only audit-log property and expands protocol surface
  for a problem the CLI can solve locally.

---

## 2026-04-18 — Replace/Archive multi-address policy

**Commits:**
- aweb: epic aweb-aajw, subtask aweb-aajw.12

**Decision maker:** Juan (on Jack's recommendation, from Alice's audit)

A persistent DID can hold multiple addresses across namespaces. The
cloud's Replace and Archive lifecycle flows must honor that:

- **Replace**: reassign every cloud-managed address for the old DID
  to the new DID, atomically. BYOD addresses are left untouched — the
  cloud does not hold the namespace controller key for those, so it
  has no authority to migrate them.
- **Archive**: delete every cloud-managed address for the DID. BYOD
  addresses are left untouched for the same reason.
- **Reachability** stays per-address. A DID can carry different
  reachability per address. The dashboard presents the team-managed
  address as primary for now.

Affects: `ac/backend/src/aweb_cloud/routers/agent_lifecycle.py` and
the six `list_did_addresses[0]` sites surfaced in Alice's audit
(agent_addressing.py, init.py, onboarding.py, agent_lifecycle.py).

---

## 2026-04-18 — Split awid identity registration from address binding

**Commits:**
- aweb: (pending) — `docs/awid-sot.md` Identity operations section,
  Addresses precondition, `did_aw_mappings` schema update;
  `docs/trust-model.md` identity vs address authority;
  `docs/identity-guide.md` two-step flow

**Decision maker:** Juan

awid's `POST /v1/did` bundled identity registration (`did_aw ↔ did_key`)
with an address claim into a single signed envelope. This forced a
cycle for managed addresses: a self-custodial identity holder had to
sign over an address they did not yet own, while the namespace
controller (the hosted operator) had no way to pre-register the
identity before assigning the address. Juan's 2026-04-17 precheck
`15aab802 "Require awid registration before managed addresses"` made
the invariant explicit on the server side but could not be satisfied
by the existing CLI flow — mechanically impossible.

Chosen resolution: split the awid protocol into two separately
authorized operations.

- `register_did` — identity holder signature only, binds
  `did_aw ↔ did_key`. No address in envelope or state hash.
- Address binding stays at `POST /v1/namespaces/{domain}/addresses`,
  namespace controller signature, with awid rejecting the call if
  `did_aw` is not already registered.

Rationale: identity and address are semantically independent facts
with different authorities. Bundling them collapses the authority
model, forces pre-launch protocol band-aids, and makes cross-namespace
memberships awkward. Splitting them makes the "identity before address"
invariant structural, gives each party the authority it legitimately
holds, and matches the log-based identity model already sketched in
`aweb/docs/vectors/identity-log-v1.json`.

Cost: awid schema migration (drop address/server/handle from
`did_aw_mappings`; drop denormalized `current_did_key` from
`public_addresses` and resolve via JOIN so a DID can hold multiple
addresses without rotation cascades), CLI two-step flow in
`aw id create` and the API-key bootstrap path, server-side obligation
for the hosted operator to submit the two ops in order. Estimated
3–5 days.

Alternatives rejected:
- Two-phase CLI "prepare" endpoint — a workaround for the coupling,
  not a fix; bakes the bug into the protocol.
- Server registers DID on behalf using the public key in the
  payload — requires extending awid to accept controller-authorized
  identity registrations, which breaks the authority model.
- Revert the precheck — loses the invariant (managed addresses
  pointing at DIDs awid doesn't know), which is foundational.

Affects: awid server and schema, `aw` CLI identity creation + bootstrap,
`ac` hosted operator init flow, identity-log conformance vectors.
Launch-blocker for the API-key persistent bootstrap; Juan's
2026-04-18 attempt to re-provision `juan.aweb.ai/avi` surfaced this.

Source of truth: [`aweb/docs/awid-sot.md` — Identity
operations](https://awid.ai/awid-sot.md#identity-operations).

---

## 2026-04-11 — Content publishing split

**Commits:**
- co.aweb: `fd59be4` — Add content strategy decision and publishing plan

**Decision makers:** Juan + Enoch (board)

Personal, story-driven posts publish on juanreyero.com. Technical and
protocol posts publish on aweb.ai/blog (to be set up in the Hugo site).

juanreyero.com has domain authority and a real person behind it —
personal stories land better from a person than a company. Technical
content on aweb.ai builds the domain's authority and keeps interested
readers on-site.

The linking pattern: juanreyero.com posts mention aweb and link to
aweb.ai. aweb.ai/blog posts link to the repo and docs.

Affects: CEO should use this split when approving content. Hugo site
needs a blog section. Content plan (content/plan.md) tracks what goes
where.

---

## 2026-04-06 — Migrate to full public-key cryptographic identity

**Commits:**
- aweb: `9212616` — Add team architecture SOT for aweb server and CLI
  (first migration commit; 15+ followed on same day: awid SOT rewrite,
  certificate auth, team CRUD, connect flow, middleware)
- ac: no commits until April 9 — migration reached cloud on `933d606`
  (Pin backend local dev to sibling aweb) and team certs arrived on
  April 9-10 starting with `1a7190f` (Mint real team certs for
  custodial API keys)

**Decision maker:** Juan

Replace bearer tokens and API keys with Ed25519 public-key
cryptographic identity (`did:aw`) and team certificates throughout
the stack (aweb, aweb-cloud, awid).

The old architecture worked for single-server coordination but can't
support cross-org agent communication, offline signature verification,
true agent ownership of identity, or external services built on the
identity layer.

Cost: full rewrite of auth paths, production database reset, ~1-2
weeks of engineering, delayed shipping and outreach. Accepted because
migrating after users are on the platform would be 10x harder.

Affects: everything — aweb OSS, aweb-cloud auth bridge, awid registry,
CLI flows, all agent identities.
