# Operations Status

Last updated: 2026-05-04 12:10 CEST (Hestia, post aame rollback + diagnosis)

## Current focus

**aame ship rolled back. Diagnosis complete.** v0.5.19 deploy with
aweb 1.19.0 broke same-team mail/chat routing. Juan rolled cloud
back to v0.5.18 (aweb 1.18.6) at 09:49 UTC. Mail and chat verified
working from my Hestia CLI on rolled-back state (alias and
DID-direct paths both 200). Standing down from awid-side
investigation; awaiting Athena's architectural review of Grace's
fix `ff5f2ec` on aweb main.

Two distinct issues identified, both with code-side fixes ready
on branches:

- **AC embedded 001 checksum drift** (separate from any aame work):
  AC commit `133a7d94` had edited `backend/src/aweb_cloud/migrations/aweb/001_initial.sql`
  in-place (DEFERRABLE on `tasks.parent_task_id`). Grace fixed AC
  main in `a93c69be` — restored 001 to the `f0331940…` checksum,
  kept 002 + 003, added `004_tasks_parent_task_deferrable.sql`.
  Tests green.
- **Routing regression in aweb 1.19.0**: Grace added a guard that
  rejected local persistent address fallback when
  `registry_client.resolve_address` returned None. The cloud's
  unsigned AWID lookup misses private/team-scoped (nobody-
  reachability) records, so the new guard 404s same-team-private
  routing. Candidate fix on aweb main as `ff5f2ec` (allows
  same-team private routing when authenticated sender is in the
  local coordination team OR signed payload binds). 6 focused +
  120 messaging + 33 MCP + 427 full pytest passed.

Neither fix is released. **Update 2026-05-04 ~12:30: Athena kicked
`ff5f2ec` back to Grace** — two security gaps (DID-overlap bypass
branch outside the spec; "signed-payload-binding" path doesn't
actually verify signatures, just parses JSON + compares fields).
Architectural framing is right; implementation is unsafe; would
replace one regression with a worse spoofing posture. Grace
iterates.

**Update 2026-05-04 ~13:30: Pivot to destructive-cutover recovery.**
Juan authorized PREP work for the awid-style cutover shape applied
to aweb-cloud's `aweb` schema: dump prod, drop schema, apply
consolidated single 001 representing post-aame state, restore data.
Cutover playbook drafted in runbook.md §"Destructive-cutover
recovery (aweb-cloud)" with phased execution chain (each phase
pauses for explicit Juan-go), schema-equivalence proof gate,
transformation-enumeration gate, local-roundtrip-green gate,
safety-net dump as separate pre-cutover artifact, and rollback
shapes per phase. **Drop is GATED on Juan's explicit go on the
day, after the AC patch carrying Athena's fixes ships in Render.**
Grace authors consolidated 001 + transforms in parallel; Athena
reviews schema-equivalence + transformation correctness; Hestia
executes the cutover phases under direct authorization.

## Live state (verified 2026-05-04 ~10:00 UTC)

- `app.aweb.ai/health`: `release_tag=v0.5.18`,
  `aweb_version=1.18.6`, `awid_service_version=0.5.3`,
  `git_sha=4ace97702077a43e7067f296848145c40204444a`. db / redis /
  awid_registry / coordination_api healthy. Started 2026-05-04
  09:49:41 UTC.
- `api.awid.ai/health`: `version=0.5.4`, redis / db / schema
  healthy.
- aweb OSS published tags include `server-v1.19.0`, `aw-v1.19.0`,
  `awid-v0.5.4`, `channel@1.4.0` — published to PyPI/npm but
  aweb 1.19.0 NOT in the running cloud (rolled back).
- ac main has `a93c69be` (Grace's migration restore + 004); not tagged.
- aweb main has `ff5f2ec` (Grace's routing fix); not tagged.
- Mail/chat probes 2026-05-04: `mail --to athena` (alias) →
  message_id `ba670e73…` arrived verified; `mail --to-did
  did:aw:yumP9TQf…` (DID-direct) → message_id `806b34f0…` arrived
  verified.

## Release pipeline

- **aame OSS ship (2026-05-03–04): partial.** PyPI/npm publish
  succeeded for aweb 1.19.0, aw 1.19.0, awid 0.5.4, channel 1.4.0.
  Verified-live mail NOT posted; cloud uptake (v0.5.19) was
  rolled back. Will re-ship cloud after Athena greenlights
  `ff5f2ec` and Grace's fix bundles into a new aweb patch +
  aw patch + ac release.
- **Queued (waiting on Athena's `ff5f2ec` review):**
  1. Athena reviews `ff5f2ec` architecturally.
  2. If accepted: aweb patch tag (1.19.x) + aw CLI patch tag
     individually (banked policy 7) → PyPI + npm publish.
  3. ac release: bump `aweb` pin to the new patch + uv.lock
     refresh + bundle Grace's `a93c69be` (the migration restore
     + 004) → `make ship` → tag → push → CI/CD → Juan deploys.
  4. Apply migrations to prod via `make prod-migrate-direct
     PROD_ENV_FILE=.env.production`. Expect the
     `f0331940…` 001 to keep its checksum AND 002 + 003 + 004
     to apply clean.
  5. Verify-applied SQL block per runbook §"Verify-applied query
     block".
  6. Smoke probe (mail send + chat send) from new-binary CLI
     against new-binary cloud — closes the loop.
  7. Verified-live mail to Athena/Sofia/Iris/Juan.

## Operational discrepancies

- **Asymmetric compat-test gap (third strike in 24h).** Compat
  covers (old-client + new-server). Doesn't cover (new-client +
  old-server). Manifestations: BYOD-username script gap, mail
  conversation_id payload mismatch, signed-vs-unsigned AWID
  resolve. Banked into runbook §"Asymmetric compat-test gap";
  manual workaround documented (run new-client probes against
  rolled prod before pushing tags). Real fix is engineering —
  add the missed direction to the compat matrix. Logged in
  Athena's lane.
- **AC embedded migration drift discoverability.** AC's embedded
  copy of aweb migrations at `backend/src/aweb_cloud/migrations/aweb/`
  is what prod hashes — not the OSS wheel. Today's chase wasted
  cycles because I assumed the OSS wheel was authoritative.
  Banked into runbook §"NEVER edit a deployed migration —
  applies to AC embedded copy too" with diff commands.
- **`awid-prod-drop` / `awid-prod-reset` Makefile targets are too
  ergonomic for destructive ops.** Juan asked to remove them.
  Holding on the Makefile edit pending his explicit "go". Will
  also propose stripping the corresponding subcommands from
  `awid/scripts/prod_db_reset.py` if he agrees.
- **AWID public-namespace 404 for nobody-reachability addresses
  is cosmetic.** sofia/athena/hestia rows are intact in
  `awid.public_addresses` with `reachability=nobody`. The
  unauthenticated namespace listing endpoint filters them out
  (has been filtering since April commits 100ecac/3dc19ea/7c016ec).
  Cloud-mediated mail/chat does NOT use this endpoint, so the
  404 doesn't break routing. Not blocking; track if external
  resolvers ever start needing public visibility.
- **Verified-live mail for aame OSS publish is owed** when the
  full aame chain (re-ship via `ff5f2ec` patch) lands.

## Active claims

`aw work active`: zero rows. `aw work blocked`: zero rows.

## Workspace status (company team, default:aweb.ai)

- hestia (me): online, no claims/locks, monitoring.
- athena: online, reviewing `ff5f2ec` architecturally.
- sofia: status unknown; she's on the eventual external-claim-
  framing path for the aame re-ship.
- aida/iris/metis: not yet online.

Dev team (`aweb:juan.aweb.ai`) members not visible from my
workspace — Athena is the cross-team bridge.

## Next checks

1. Watch for Athena's mail with verdict on `ff5f2ec` review.
2. When greenlit: run aweb gate chain (`make ship`), tag aweb
   patch + aw CLI patch individually, push, watch GHA, signal
   Juan when image at GHCR.
3. Next ac release picks up Grace's `a93c69be` AND the new aweb
   pin in one shot — single ship, single deploy, one apply of
   002 + 003 + 004 on prod.
4. Daily `/health` on `app.aweb.ai` and `api.awid.ai`. Compare
   to claims; flag drift.
5. On verified-live: post mail with full evidence + close out
   the aame ship cycle (verified-live mail still owed for the
   aame epic).

## Standing release-discipline (banked through 2026-04-26 + 2026-05-04, Hestia enforces)

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate
13. Code-reviewer subagent for gate-input commits (Athena runs
    before signaling Hestia)
14. Migration-checksum chase covers BOTH OSS wheel and AC
    embedded copy; AC is what prod hashes (banked 2026-05-04)
15. Run new-client smoke probes against rolled prod server
    before pushing patch tags (manual workaround for
    asymmetric compat-test gap; banked 2026-05-04)

`status/weekly.md` continues as a roll-up until replaced by a
proper dashboard.
