# Hestia Handoff

Last updated: 2026-05-04 12:30 CEST (post aame rollback + diagnosis;
ff5f2ec + a93c69be queued, awaiting Athena review verdict)

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between. Today (2026-05-04)
was a hard cycle: the aame OSS ship landed on PyPI/npm cleanly
(aweb 1.19.0, aw 1.19.0, awid 0.5.4, channel 1.4.0), but the cloud
uptake (ac v0.5.19) broke same-team mail/chat routing in production
and Juan rolled back to v0.5.18. Diagnosis is complete; both fixes
are on respective mains awaiting release coordination. Banked
learnings folded into runbook.md.

The team:

- **Sofia**: direction. Out of routing for bug-fix releases by
  default; mail before tag only for external-claim weight.
- **Athena**: code in aweb and ac. Briefs you with bless-and-run
  mail after running code-reviewer subagent on gate-input commits.
  Currently reviewing Grace's `ff5f2ec` architecturally.
- **Mia / Noah / Grace / Kate**: dev team (`aweb:juan.aweb.ai`,
  separate cryptographic team). Author feature work, Athena reviews.
- **Aida / Iris / Metis**: pending Hetzner deploy. Not yet online.

## Identity (live since 2026-05-01 21:05 UTC)

- did: `did:key:z6MkebRpF7qEFNt5vAYa5BWjegFk1igt6mRESqWb5r3kp9AK`
- stable: `did:aw:3fC4cfvFuVAxZCWyJNRCoUxHVAim`
- address: `aweb.ai/hestia` (registered with reachability=nobody;
  see "Open follow-ups" — does not break cloud-mediated routing)
- active team: `default:aweb.ai`
- workspace_id: `8ae26888-ee11-4e1f-beff-aaab79b44b58`
- registry: registered at `https://api.awid.ai`

## What's live (verified 2026-05-04 ~10:00 UTC)

- ac: **rolled back to v0.5.18** at `app.aweb.ai`, git_sha
  `4ace97702077a43e7067f296848145c40204444a`, aweb_version 1.18.6,
  awid_service_version 0.5.3. Started 2026-05-04 09:49 UTC.
- aw CLI: 1.19.0 published on npm (`@awebai/aw`) and GH Releases.
  My local CLI sends mail/chat fine against rolled-back cloud.
- aweb server: 1.19.0 on PyPI; **NOT** in the running cloud (rolled
  back).
- awid registry: 0.5.4 at `api.awid.ai`. Healthy.
- channel: 1.4.0 on npm. Unchanged in cloud.
- Mail/chat (verified 2026-05-04): both alias and DID-direct paths
  work from my CLI; chat threads with Athena round-tripped clean.

## Today's cycle (2026-05-03 → 2026-05-04)

1. **aame OSS ship** (2026-05-03): tagged + published aweb 1.19.0,
   aw 1.19.0, awid 0.5.4, channel 1.4.0. Make ship green. PyPI +
   npm publish confirmed.
2. **ac v0.5.19** bumped pin to aweb 1.19.0, ac gates ran with a
   pre-existing test-DB-fixture limitation (gate-failure on
   `column "conversation_id" does not exist` — ac test fixture
   doesn't apply aweb migrations on ephemeral test DB). Juan
   authorized gate override given the diagnosis.
3. **Manual deploy**: Juan deployed v0.5.19 from GHCR to Render.
4. **Migration apply** via `make prod-migrate-direct
   PROD_ENV_FILE=.env.production` failed: 001 checksum mismatch
   `3953210a…` vs prod `f0331940…`. 002 + 003 not applied.
5. **Mail/chat broke in prod** post-deploy (with v0.5.19 + aweb
   1.19.0): same-team-private routing 404'd on the new guard
   Grace had added to `aweb/messaging/...` for unsigned-AWID-miss
   protection.
6. **Rollback**: Juan rolled cloud back to v0.5.18 manually at
   09:49 UTC.
7. **Awid investigation chase**: probed reachability/listing
   endpoints; concluded the public-namespace 404 is cosmetic and
   has been there since April. Cloud-mediated routing uses a
   different path. NO awid reset required.
8. **Grace's diagnosis** (relayed via Athena):
   - **Issue 1** (checksum): the `3953210a…` was AC's embedded
     `backend/src/aweb_cloud/migrations/aweb/001_initial.sql`,
     edited in place by AC commit `133a7d94` (made
     `tasks.parent_task_id` DEFERRABLE). Fix on AC main:
     `a93c69be` restored 001 to `f0331940…`, kept 002 + 003,
     filed `004_tasks_parent_task_deferrable.sql` as the
     successor migration. Tests green.
   - **Issue 2** (routing): the v0.5.19 guard rejected local
     persistent address fallback when
     `registry_client.resolve_address` returned None. The cloud's
     unsigned AWID lookup misses private/team-scoped (nobody-
     reachability) records → guard 404s. Fix on aweb main:
     `ff5f2ec` allows same-team private routing if (a) authenticated
     sender is in same local coordination team OR (b) signed
     payload binds. Validation: 6 focused + 120 messaging + 33
     MCP + 427 full pytest passed.
9. **Probes from rolled-back state** (Hestia, 2026-05-04): mail
   alias-path + DID-direct + chat all 200. Confirms v0.5.18 routing
   is healthy and Grace's diagnosis is consistent.

## Pivot to destructive-cutover recovery (2026-05-04 ~13:30)

Juan authorized PREP work for a destructive-cutover recovery:
dump prod, drop the `aweb` schema, apply a single consolidated
new 001 representing post-aame state, restore data with any
needed transforms. Same shape as the awid 0.3.1→0.5.1 cutover
of record. Drop is GATED on Juan's explicit go on the day,
after Athena's fixes ship in the AC patch published in Render.

**Lane split**: Grace authors consolidated 001 + transformation
script. Hestia executes cutover phases. Athena reviews
consolidation (schema-equivalence proof) + transformation
(explicit enumeration of every NOT NULL/CHECK/FK delta). Juan
authorizes.

**Banked operational gates** (cutover playbook now in
`runbook.md` § "Destructive-cutover recovery (aweb-cloud)"):

1. Schema-equivalence proof: consolidated 001 produces same
   end-state as `[old-001 + 002 + 003 + 004]` applied to a
   clean local DB. Diffed schema-only pg_dumps must be identical.
2. Transformation enumeration: explicit list of every additive-
   chain delta that affects existing prod-data shape (for the
   aame chain: all additive on existing data shape, transform
   should be empty/trivial — but Grace asserts that explicitly).
3. Local `verify_db_reset_roundtrip.py` green against new
   consolidation + real prod-shape dump + target binary.
4. Pre-cutover safety-net dump (from current v0.5.18 prod), kept
   independent of cutover dump, copied off the cutover machine.
5. Cutover phases step-gated; each pauses for explicit Juan-go
   between phases (no orchestrated single-shot reset).
6. Verify-applied SQL block AFTER consolidated 001 applies,
   BEFORE restore data goes in.
7. Post-cutover smoke probes (mail/chat alias + DID-direct +
   send-and-wait) before posting verified-live.

**Schema delta the consolidation must capture** (mapped from
AC's embedded `backend/src/aweb_cloud/migrations/aweb/`):

- 002_conversations.sql: new tables `aweb.conversations`,
  `aweb.conversation_participants`; new nullable column
  `aweb.messages.conversation_id` with FK; 5 indexes.
- 003_conversations_constraints.sql: DROP DEFAULTs on
  conversations.created_by_did + conversation_participants.alias,
  add 3 CHECK constraints (not-blank x2, reachable), trigger
  + function for updated_at.
- 004_tasks_parent_task_deferrable.sql: tasks.parent_task_id
  FK becomes DEFERRABLE INITIALLY IMMEDIATE.
- All deltas additive on existing-row data shape; no destructive
  transforms expected.

**No prod-state changes performed during prep**. Only reads
(`make awid-prod-verify` already ran read-only; cloud equivalent
not yet exercised). Local prereqs confirmed: postgres@17 +
redis running, uv 0.11.7, psql/pg_dump from PG17 (script handles
PG16-server compat via `_INCOMPATIBLE_SET_PREFIXES` strip).

## Queued (waiting on Grace's next ff5f2ec iteration → Athena re-review)

**2026-05-04 ~12:30: Athena kicked `ff5f2ec` back to Grace.** Two
security gaps in the implementation:

- `_local_recipient_visible_to_auth` includes a DID-overlap branch
  outside the spec — any sender whose did_aw or did_key matches the
  recipient's passes the guard (self-send case + any
  key-collision-by-mistake = bypass).
- `_signed_payload_matches_address_binding` doesn't actually verify
  the cryptographic signature; it only parses JSON and compares
  fields. Anyone can craft a JSON blob claiming any address binding
  and route to any private recipient.

Architectural framing of the fix is right; implementation legs are
unsafe. Shipping as-is would replace a "regression rejecting
legitimate same-team traffic" with a "regression accepting spoofed
same-team-claimed traffic" — worse posture. Grace iterates: remove
DID-overlap branch, add real signature verification, add
cross-team / spoof / bad-signature rejection tests. Athena will
mail when next iteration is reviewable.

AC's `a93c69be` migration restoration is independent but releasing
AC without the aweb routing fix is also unsafe (both needed to
unblock the v0.5.19 regression cleanly).

Once Athena greenlights the next iteration:

1. aweb patch tag (1.19.x) + aw CLI patch tag
   individually (banked policy 7) → PyPI + npm publish.
3. ac release: bump `aweb` pin to the new patch + uv.lock
   refresh + bundle Grace's `a93c69be` (migration restore + 004)
   → `make ship` → tag → push → CI/CD → Juan deploys.
4. Apply migrations to prod via `make prod-migrate-direct
   PROD_ENV_FILE=.env.production`. Expect the
   `f0331940…` 001 checksum to verify, AND 002 + 003 + 004 to apply
   clean.
5. Verify-applied SQL block per runbook §"Verify-applied query
   block".
6. Smoke probe (mail send + chat send) from new-binary CLI
   against new-binary cloud — closes the loop.
7. Verified-live mail to Athena/Sofia/Iris/Juan (this is the
   verified-live mail owed for the aame epic; #16 task).

## Banked into runbook today (2026-05-04)

- **NEVER edit a deployed migration — applies to AC's embedded
  copy too.** AC bundles its own copies of aweb migrations under
  `backend/src/aweb_cloud/migrations/aweb/`; pgdbm hashes those,
  not the OSS wheel. When chasing a checksum mismatch, check
  `git log` on the AC embedded file. Diff commands documented in
  runbook.
- **Asymmetric compat-test gap.** AC's
  `make test-cloud-user-journeys-compat` covers (old-client +
  new-server) only. (new-client + old-server) is uncovered. Hit
  three times in 24h: BYOD-username script gap, mail
  conversation_id payload mismatch, signed-vs-unsigned AWID
  resolve. Manual workaround documented (smoke-probe new client
  against rolled prod before pushing tags); real fix is
  engineering — add the missed direction to compat matrix.

## Open follow-ups (Hestia's lane)

1. **Verified-live mail for aame epic** — owed once `ff5f2ec`-based
   re-ship lands and cloud uptake completes. Task #16.
2. **Hold for Juan's go on Makefile edit** — remove
   `awid-prod-drop` / `awid-prod-reset` from `aweb/Makefile`. Diff
   drafted; Athena green; awaiting Juan. Task #19.
3. **Asymmetric compat-test gap** — flagged to Athena; engineering
   decides countermeasure. Manual smoke-probe workaround used in
   meantime.
4. **AWID reachability=nobody on hestia/sofia/athena** — cosmetic,
   not blocking. Public-namespace listing 404s; cloud-mediated
   routing fine. If external resolvers ever start needing public
   visibility, file an UPDATE to flip those rows to
   `team_members_only`. Not urgent.
5. **Publishing-path timing breakdown** for Sofia (long-standing
   from v0.5.18 cycle).
6. **Test-suite triage** in ac/Makefile (deferred from v0.5.18
   cycle).

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — Athena's verdict on
   `ff5f2ec` review is the unblocker.
2. `curl https://app.aweb.ai/health` and `curl https://api.awid.ai/health`
   — confirm v0.5.18 still in place.
3. `aw work active` and `aw work blocked` — sweep stale claims
   (clean as of last check).
4. If Athena's mail says `ff5f2ec` accepted: run aweb patch ship
   chain per "Queued" steps 2–7 above.
5. If Juan greenlights Makefile edit: apply diff (lines 4, 36–37,
   108–114 of `aweb/Makefile`); decide also whether to strip
   `drop-schema` / `reset` subcommands from
   `awid/scripts/prod_db_reset.py`.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (run gates here for aweb releases)
- `ac` → `../../../ac` (run gates here for ac releases)

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos. Read sibling repos to run gates and
verify what shipped; do NOT edit code there (Athena's surface)
without explicit Juan-instruction-or-Athena-coordination.

## Note on git author attribution

Commits authored by dev-team members (Mia / Grace et al.) appear
as "Juan Reyero" in `git log`. The actual agent identity is
carried via the aweb cert. Cross-check author with Athena when
attribution matters; she routes to the actual author. Today's
`a93c69be` (AC) and `ff5f2ec` (aweb) are Grace's work.
