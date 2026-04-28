# Decisions

When the plan changes, record it here with the commit hash(es) that
mark the moment. Agents check this for entries newer than their last
handoff to detect that the world changed.

---

## 2026-04-28 — Task work contracts become the queryability bridge

**Commit:** `c4eac9a` Add queryable work contract and dashboard inventory

**Decision maker:** Avi

**Decision.** Until `aw` has native task fields for builder, reviewer,
feedback signal, evidence, signal strength, and next check,
substantial tasks should include a parseable `Work contract:` block in
their description or notes. Operations should treat missing or malformed
contract fields as operational discrepancies.

`docs/company-dashboard.md` defines the dashboard/signal inventory:
active tasks, claims, workspaces, area-specific signals, dashboard
views, and query limits.

**Why.** The narrowed permanent-area model is legible in docs, but not
yet queryable enough through `aw`. Encoding the work contract in a
standard block gives operations something enforceable today and makes
the product gap explicit: these fields should become native task
metadata.

**Affects.** `docs/agent-first-company.md`,
`docs/company-dashboard.md`, `docs/team.md`, operations/engineering
instructions, and `aweb-aals.*` tasks.

---

## 2026-04-28 — Permanent agents narrowed; repo work moves to task-scoped pairs

**Commit:** `f002b50` Refine permanent agent areas and repo work pairs

**Decision maker:** Juan + Avi

**Decision.** The permanent company agents are direction, engineering,
outreach, support, operations, and analytics. Engineering absorbs
identity/protocol integrity. Permanent repo-manager agents are removed
from the active company model.

Significant repo work should use task-scoped builder/reviewer agents
created with `aw workspace add-worktree`. The task names the builder,
reviewer, repo/worktree, acceptance criteria, and feedback signal.
Engineering participates when the task has architecture, protocol,
release, identity, or cross-repo risk.

Operations watches the company machinery: stale claims, blocked tasks,
agent wake-ups, production health, missing reviewers, and live
verification. Analytics looks for signal, states attribution limits,
and files instrumentation gaps.

**Why.** A permanent global verification/accountability agent is too
broad and overlaps with the reviewer in each pair. Permanent repo
agents also pull the organization back toward coordination-by-role.
The useful split is: permanent agents own surfaces and feedback loops;
task-scoped pairs do substantial work and review.

**Affects.** `agents/`, `docs/team.md`,
`docs/agent-first-company.md`, status files, `AGENTS.md`, and
`README.md`.

---

## 2026-04-28 — Company agents move to responsibility areas

**Commit:** `f7a8701` Reorganize agents by responsibility area

**Decision maker:** Juan + Avi

**Decision.** aweb.ai agents are organized by responsibility areas
instead of management titles. Current areas are direction, engineering,
outreach, support, operations, and analytics.

Substantial work must flow through artifacts: `aw` tasks/claims,
handoffs, status files, and decision records. The default shape for
substantial work is builder plus reviewer. Agents should always look
for feedback and prefer close/verifiable feedback, but weak signals
must be recorded as signals rather than treated as proof of causality.

**Why.** Title-shaped organization creates too much coordination and
not enough work for agents. Responsibility areas make the work surface,
evidence, and review path explicit without pretending the company has a
human management hierarchy. Some loops are directly verifiable
(code -> test -> fix). Others, such as social media posts followed by
signup movement, are useful but ambiguous. The operating model should
exploit strong loops and still preserve weak signal with uncertainty.

**Affects.** `AGENTS.md`, `README.md`, `docs/team.md`,
`docs/agent-first-company.md`, `status/*`, `publishing/plan.md`, and
agent directories under `agents/`.

---

## 2026-04-25 — aweb-cloud v0.5.6 ships; closes aaja.6 (P0 launch blocker)

**Commits (ac):**
- `18021ff9` Add hosted MCP OAuth signed mail e2e (aweb-aaja.6, custody.py canonical_payload swap + cross-repo Docker e2e)
- `e5f58ce5` release: v0.5.6, aweb-aaja.6 hosted MCP OAuth verified mail (tagged `v0.5.6`)

**Decision maker:** Randy (written tag-approval) + Tom (coord-cloud)

**Decision.** v0.5.6 closes `aweb-aaja.6` (P0 launch blocker — cross-repo
Docker e2e for hosted MCP OAuth verified mail). Single-commit functional
delta from v0.5.5. Pin unchanged (`aweb>=1.18.1`, `awid-service>=0.5.1`).
Implementation track: Grace authored `18021ff9` under Tom's continuing
coord-borrow (same shape as aala.10 yesterday/today). Tom committed the
bump after a pre-bump bisect against pure aweb 1.18.1 sibling confirmed
the canonical_payload swap is sufficient by itself — no aweb 1.18.2
cycle required for the ac side.

**What changed in custody.py (the product fix).** `sign_hosted_mcp_message`
now computes `signed_payload = canonical_payload(dict(payload))` instead
of `canonical_json_bytes(dict(payload))`. The two functions live in
`awid.signing`; `canonical_payload` filters to the awid-defined
`SIGNED_FIELDS` set (the message fields that participate in
cryptographic identity), `canonical_json_bytes` serializes the entire
dict. Receivers (awid + aweb verifiers) reconstruct against
`canonical_payload`, so the prior implementation produced signatures
that didn't verify when the input dict carried any non-SIGNED-FIELDS
key (e.g. transport-only routing metadata). After the swap, hosted
MCP OAuth-routed mail produces `signed_payload` bytes that verify
correctly end to end.

**What the new e2e covers** (TestHostedMCPOAuth in
`backend/tests/test_two_service_e2e.py`): full OAuth code+PKCE
handshake against `/oauth/{register,authorize,token}` (asserts the
`mcpa_` access-token prefix), `/mcp/` initialize, `tools/call`
send_mail + check_inbox, message lookup by subject, and
`verify_did_key_signature` against the received `signed_payload` —
asserts `verified=True`. Real cloud + real mounted aweb + real awid
(Docker two-service stack).

**Pre-bump bisect.** `make test-two-service` executed twice:
1. Against aweb sibling at `b0b2b27` (pure 1.18.1 release commit;
   `2e6156b` "Harden hosted MCP proxy signing" / aajg + `ed4fa89`
   awid-prod-tooling intentionally dropped from worktree): 10 passed
   in 4.28s, including TestHostedMCPOAuth.
2. Against aweb sibling at main (post-aajg): 10 passed in 4.24s.
Both green. The aajg `canonical_signed_payload` alignment is a real
fix and will land in aweb 1.18.2 on John's timeline, but ac's hosted
MCP signing path doesn't depend on it. Worth banking — symmetric
canonicalization on either side of the wire is convergent: cleaning
up either end alone converges, both is just earlier.

**Trust model + invariants check:**
- DNS anchors trust → unchanged. Signature still authenticates the
  custodial sender's `did:key`.
- Custody choice → unchanged. Hosted MCP OAuth is custodial; v0.5.6
  makes that signature USEFUL, not nearly-correct.
- Coordination is the product → direct positive. Hosted-MCP-routed
  mail is now provably verifiable on the receiving end.
- Progressive disclosure / distribution / open+portable → unchanged.

**Verified-live discipline established** (banked from the awid 0.3.1
cutover-by-surprise earlier today). For v0.5.6 and every release from
here on:
1. GHA green ≠ feature live.
2. After auto-deploy, curl `app.aweb.ai/health` and assert
   `release_tag` matches the just-tagged version + `git_sha` matches
   the bump commit.
3. Run a one-shot smoke against the deployed surface that the
   release actually changes (for v0.5.6: hosted MCP OAuth + send_mail
   path + signature verification).
4. Only after both confirm — then mail "fully live."

**Release protocol exercised again** (3rd time this week — v0.5.4 +
v0.5.5 + v0.5.6 all under the same shape):
1. Pre-bump bisect to settle pin requirements (new step this release;
   bisect against pure 1.18.1 confirmed no 1.18.2 dependency).
2. Bump commit (pyproject.toml only this time; uv.lock minor change).
3. uv sync.
4. make release-ready against post-bump `.venv`. 6 gates green:
   release-verify-remote/model/migrations + test-backend
   (1170 passed/10 deselected) + test-frontend (25 files/96 tests)
   + test-two-service (10 passed including new TestHostedMCPOAuth).
5. SOT analysis mailed.
6. CTO written-and-mailed approval.
7. Manual `git push origin main` + `git tag -a v0.5.6` + `git push
   origin v0.5.6`.
8. Verified-live (pending — GHA in flight, prod auto-roll after).

**Closes:**
- `aweb-aaja.6` (P0 launch blocker, cross-repo Docker e2e for hosted
  MCP OAuth verified mail).

**Open under aaja epic:**
- `aweb-aaja.7` and other aaja subtasks (signing-path unification,
  trusted-proxy header restoration in ../aweb MCP auth, shared
  hosted-custodial signing hook). aaja parent stays open. Tom's
  audit comment from earlier today still stands.

**GHA:** release tag push triggered aweb-cloud CI/CD run
`24937821668`. Verified-live mail to Randy + Juan + John follows
on GHA-green + prod-roll + smoke-test pass.

---

## 2026-04-25 — awid prod registry cutover from 0.3.1 to 0.5.1

**Commits (aweb):**
- `ed4fa89` Add awid prod DB lifecycle script and Makefile targets

**Decision maker:** Juan (cutover authorization) + John (coord-aweb, executed)

**Decision.** Cut the awid registry production database (Neon Postgres,
api.awid.ai) from schema-version 0.3.1 to 0.5.1 by dumping data,
dropping the schema, re-applying the bundled `001_registry.sql` from
0.5.1, and restoring data. Once the schema was at 0.5.1 form, Juan
triggered a Render redeploy of the awid:0.5.1 image; pgdbm computed
the matching checksum on boot, skipped migration, and api.awid.ai
began reporting `version=0.5.1` with db+redis healthy.

**Why a destructive cutover and not an additive migration.** awid uses
a single consolidated migration file (`001_registry.sql`, since 0.3.0
in commit `cd01fac`). The aala epic (1.18.0/1.18.1, 0.5.0/0.5.1) added
the `team_certificates.certificate TEXT` column for BYOIT cross-machine
cert-blob persistence by editing 001 in place. pgdbm hashes migration
files (line-endings normalized + stripped, then SHA-256) and refuses
to boot when the bundled-file checksum disagrees with the
`schema_migrations.checksum` row from the prior apply. So a 0.5.1 pod
booting against a 0.3.1-checksum-pinned database would have hit
`MigrationError: Migration 001_registry.sql has been modified after
being applied!` and refused to start.

**The deployment lag that surfaced this.** awid 0.4.0 published to
PyPI on 2026-04-21 but the Render-deployed pod stayed on 0.3.1 — the
deploy is manual-only (no API key in `.env.awid-production`, no
deploy hook configured) and version drift on `api.awid.ai/health` was
not being monitored. When aala BYOIT tagged 2026-04-25 as aweb 1.18.0
(ghost) and then 1.18.1 (published), prod awid was still on 0.3.1.
Result: aala BYOIT had no production awid backend for the window
between the aala tag and this fix (~hours; aala tagged earlier 2026-04-25,
cutover completed 18:13:53 UTC the same day). The new
`/v1/namespaces/{domain}/teams/{name}/certificates/{cert_id}` fetch
endpoint and the `certificate` blob upload path were not actually
serving in prod during that window.

**Recovery encoded as a reusable artifact.** `aweb/awid/scripts/prod_db_reset.py`
with subcommands `dump`, `drop-schema`, `migrate`, `restore`, `verify`,
`reset` (orchestrator). Default `--env-file` is
`aweb/.env.awid-production`; destructive paths gated on `--yes`.
Wrapper Makefile targets: `awid-prod-verify`, `awid-prod-dump`,
`awid-prod-restore DUMP=...`, `awid-prod-migrate`,
`awid-prod-drop CONFIRM=yes`, `awid-prod-reset CONFIRM=yes`.

Two PG-version-skew sanitizers are baked into the script and would
have broken the cutover blind otherwise (host operator's `pg_dump` is
17.x, Neon prod is PG 16):
- Strip `SET transaction_timeout = 0;` from the dump (PG-17-only
  parameter; PG 16 servers reject it as unknown).
- Strip `schema_migrations` DML from the dump so the freshly-applied
  migration row stays canonical instead of either colliding on the
  primary key or restoring the stale 0.3.1 checksum.

Both were caught in a local docker-postgres:16-alpine dry-run with a
synthetic seed across all seven awid tables before going to prod.

**Cutover verification:**
- Pre/post row counts identical: 74/74/14/20/0/8/3 across
  did_aw_mappings / did_aw_log / dns_namespaces / public_addresses /
  replacement_announcements / teams / team_certificates.
- New `team_certificates.certificate` column present and nullable.
  Three pre-existing certs from the 0.3.x era have `certificate IS NULL`
  (consistent — they predate the BYOIT blob).
- `schema_migrations` reset to a single fresh row; checksum
  `e6ea1d1b…` matches the bundled `001_registry.sql` under pgdbm's
  normalization (raw `sha256(file)` is `eac20306…` and does NOT match;
  pgdbm normalizes line endings + strips first).
- `GET /v1/did/<did_aw>/head` returns real DID records from migrated
  data. `GET /v1/namespaces/<domain>/addresses/<name>` resolves
  verified+public addresses. Reachability gating still rejects
  `org_only` to anonymous callers.
- Dump preserved at `/tmp/awid-awid-reset-20260425T181335Z.sql` as
  rollback safety net.

**Migrations discipline lesson banked.** When a project uses a single
consolidated migration file, every additive schema change goes in a
NEW ordered file (`002_<name>.sql`, `003_<name>.sql`, …). Editing the
existing consolidated file in place trips pgdbm's checksum guard and
forces a destructive dump-restore cutover. Coordinators (John, Goto)
flag PRs that touch the existing 001 file for anything other than
comments/whitespace. Rule banked at the code-time-visible layer:
`aweb/AGENTS.md` (added in this same coord cycle, separate aweb
commit).

**Open follow-ups:**
- Smoke test of aala BYOIT cross-machine cert lifecycle against prod
  awid (controller add-member uploads blob → joining agent fetches
  via authenticated GET). Phase 11a passed against sibling 0.5.1 in
  dev; prod was never exercised. Grace to run after pushing aaja.6;
  John mails Randy with result.
- awid prod redeploy is still manual via Render dashboard. No deploy
  hook URL in repo; no API key in `.env.awid-production`. Worth a
  Juan-level decision on whether to set up a deploy hook + version-drift
  monitoring (e.g., a daily probe of api.awid.ai/health vs PyPI head
  awid-service version) so the next aala-style mismatch is caught
  before it becomes a launch-day cutover.

**Closes:** none — this is operational recovery, not a tracker item.

---

## 2026-04-25 — aweb-cloud v0.5.5 ships; picks up aweb 1.18.1 + completes aala.10

**Commits (ac):**
- `eb8e388d` Document BYOIT certificate pickup (aweb-aala.10, dashboard copy + sot.md custodial-shortcut framing + landing-and-onboarding flow)
- `343f40f8` Test BYOIT fetch-cert in split stack (aweb-aala.10, three-HOME e2e + bonus self-seed fix on TestDataMigration order-dependence)
- `bc35ce5a` release: v0.5.5, aweb 1.18.1 + awid-service 0.5.1 deps (tagged `v0.5.5`)

**Decision maker:** Randy (written tag-approval) + Tom (coord-cloud)

**Decision.** v0.5.5 closes aweb-aala.10 (cloud alignment with the aala
BYOIT cross-machine certificate contract) and picks up aweb 1.18.1 plus
awid-service 0.5.1 via the dependency pin bump. Three-commit delta
above v0.5.4. Implementation track: Grace authored eb8e388d + 343f40f8
under Tom's coord-borrow (Juan-greenlit cross-coord borrow after the
unauthorized-incursion incident earlier in the day — see process notes
below). Tom committed bc35ce5a after PyPI propagation of 1.18.1.

**aala.10 acceptance criteria coverage:**
1. Hosted onboarding can explain or initiate the BYOIT request →
   add-member → fetch-cert flow — `eb8e388d`. Dashboard
   `ByoitIdentitySetupFlow.tsx` corrects `aw team request` to
   `aw id team request` and adds the fetch-cert step. New tests in
   `ByoitIdentitySetupFlow.test.tsx` cover the flow strings and the
   empty-team-id fallback.
2. Auth bridge tests cover a fresh BYOIT user obtaining/installing a
   cert after approval — `343f40f8`. Split-stack e2e with separate
   owner/member/wrong HOMEs; member uses ephemeral signing key;
   controller add-member; wrong-DID fetch returns 403; correct fetch
   installs cert; aw init binds to the cloud /api endpoint; mail
   self-roundtrip + claim-human succeed. `/api/v1/connect` is
   intentionally in `_TEAM_CERTIFICATE_BYPASS_PATHS` and tested by
   `test_connect_route_bypasses_cloud_team_certificate_bridge`; no
   redundant pure-cloud bridge test added.
3. Split-origin deployments (onboarding, aweb server, registry)
   continue to work — `343f40f8` runs against split cloud + awid
   Docker stack and passes 9/9.
4. Any cloud-only custodial shortcut is documented as custodial —
   `eb8e388d` `docs/sot.md` adds `/api/v1/onboarding/cli-signup`
   under "Onboarding DIDKey authority" and explicitly names it as
   custodial/managed (cloud is the team controller for hosted teams).
   New "BYOIT Certificate Pickup" subsection clarifies cloud is NOT
   the BYOIT controller. `accept-invite` is named as a same-machine
   helper.

**What aweb 1.18.1 brings to ac via the pin:**
- aala epic (BYOIT cross-machine cert lifecycle; awid stores full
  signed cert blobs at registration; authenticated GET fetch endpoint
  at `/v1/namespaces/{domain}/teams/{name}/certificates/{cert_id}`;
  identity-scoped mail tolerates multi-team DID membership).
- aweb-aajs (BYOD wizard identity lifetime prompt fix). User-facing
  CLI surface only; ac doesn't surface `aw init` wizard directly so
  ac product impact is zero.
- aweb-aakk (task-claim dashboard event publishing). Server-side fix
  for silent-loss of `TeamTaskClaimedEvent`/`TeamTaskUnclaimedEvent`
  on direct task.claimed/task.unclaimed inputs. ac mounts the
  dashboard event feed; this is a positive fix that ac inherits via
  the pin bump.

**Bonus fix in 343f40f8:** `TestDataMigration::test_json_export_and_verification`
was order-dependent under pytest-randomly (asserted `public_addresses
>= 1` without seeding). Now self-seeds a permanent-custodial identity
via `/api/v1/identities/create-permanent-custodial` before calling
`export_identity_data`.

**Trust model + invariants check:**
- awid stores public cert artifacts only; never the team controller
  private key.
- Cert fetch is subject-only authorized (caller must equal
  `cert.member_did_aw`).
- All seven invariants (independent primitives, DNS-anchored trust,
  custody choice, coordination primacy, progressive disclosure,
  distribution > features, open/portable) hold unchanged.

**Release protocol exercised end-to-end again:**
1. Per-gate log against post-bump `.venv` (aweb 1.18.1 + awid-service
   0.5.1 from PyPI). All 6 release-ready gates green: 1170 backend
   tests (same as v0.5.4 — no regression), 96 frontend tests
   (+2 from Grace's BYOIT flow tests), 9 two-service tests including
   the rewritten split-stack BYOIT e2e under aweb 1.18.1.
2. SOT analysis mailed.
3. CTO written-and-mailed approval.
4. Manual `git push origin main` + `git tag -a v0.5.5` + `git push
   origin v0.5.5`. Did not use `make ship` (auto-pushes tag,
   short-circuits approval step).

**Process notes from this release:**
- aweb-aala.10 implementation involved a coord-borrow: Grace
  (John's dev) was authorized by Juan to work in ac under Tom's
  coord, after she crossed the lane unsupervised earlier in the day.
  Insight-option was the first call (have her mail observations);
  Juan reversed to "let her do the work, you review"; Randy
  concurred ("authorized cross-coord borrow is not what the
  dispatch-via-coord memory was banked against"). The protocol
  worked: Grace's commits went through Tom's delta-review and gate
  discipline; v0.5.5 ships clean.
- aweb 1.18.0 ghost-tag stays in aweb history. 1.18.1 is the
  published recovery release. ac pins against 1.18.1 directly.

**Closes:**
- `aweb-aala.10` (P1, ac alignment with BYOIT cert contract). John
  closed in tracker on receipt of tag mail; aala epic close pending
  Tom's "GHA green + prod rolled" confirmation.

**GHA:** release tag push triggered aweb-cloud CI/CD run
`24933534665`. Image publish to GHCR follows on green.

---

## 2026-04-25 — BYOIT cross-machine team join + multi-membership launch hardening (aala epic)

**Commits (aweb):**
- `ff92358` Implement cross-machine team cert fetch (aala.1 SOT + aala.2/.3/.4/.5/.7)
- `9b2eed3` Add cross-machine fetch-cert e2e (aala.6/.8/.9/.11/.12)
- `ba133d4` Fix BYOIT certificate pickup guidance (aala.9 follow-up)
- `898556d` release: aweb server 1.18.0, aw CLI 1.18.0, awid-service 0.5.0 — **GHOST TAG**. Tags `server-v1.18.0`, `aw-v1.18.0`, `awid-v0.5.0`, `awid-service-v0.5.0` were pushed to origin in a single batched `git push` command. All 4 tag-triggered GHA publish workflows failed to fire (likely event-coalescing on same-commit batched tags). PyPI/npm never received 1.18.0/0.5.0. Tags remain in origin as audit history; no actual publish.
- `4623979` Fix BYOIT certificate pickup guidance (aweb-aajs follow-up): three stale CLI error strings in init.go/run.go pointing cross-machine users at accept-invite (which fails after the aala.6 conservative-helper rename) updated to point at the request → fetch-cert path.
- `3bc296e` Publish task claim dashboard events (aweb-aakk): `_translate_team_event` and `_translate` now map task.claimed/task.unclaimed events to dashboard team-events and workspace events. Closes silent-loss of dashboard team-events for claim/unclaim.
- `b0b2b27` release: aweb server 1.18.1, aw CLI 1.18.1, awid-service 0.5.1 — **PUBLISHED** (re-publish of 1.18.0 content + aajs + aakk; tags pushed individually one-by-one; all 5 GHA workflows fired). Tagged `server-v1.18.1`, `aw-v1.18.1`, `awid-v0.5.1`, `awid-service-v0.5.1`.

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
