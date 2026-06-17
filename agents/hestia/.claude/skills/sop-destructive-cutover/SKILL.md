---
name: sop-destructive-cutover
description: Drive a destructive dump-restore schema cutover on aweb-cloud's aweb schema when forward-additive recovery is unsound. Six-phase chain with explicit Juan-go between each phase, safety-net dump separate from cutover dump, rollback paths per phase, post-cutover constraint-diff audit. Invoke only when Juan explicitly authorizes a cutover; routine schema work uses forward-additive successors per sop-pgdbm-migration-apply.
---

# Destructive cutover recovery (aweb-cloud)

The recovery shape for irrecoverable migration-history drift on
aweb-cloud's `aweb` schema (the embedded coordination schema in
AC). The pattern: dump prod data, drop the schema, apply a single
consolidated 001 representing the post-state, restore data with
required transforms. Drops migration history entirely and replaces
it with a single fresh row in `schema_migrations`.

## When to use this path

ONLY when forward-additive recovery via successor migrations is
unsound or has been rejected, e.g.:

- The additive chain itself triggers checksum mismatch on prod.
- Migration history is considered too fragile to leave intact.
- A `DROP SCHEMA X CASCADE` happened in an earlier cutover and
  CASCADE-dropped cross-schema FK constraints that the additive
  path cannot recreate without violating immutability (see
  `legacy.md` migration-discipline: cross-schema FK drift).

Routine schema work uses forward-additive successors per
`sop-pgdbm-migration-apply` "NEVER edit a deployed migration" rule.

## Authorization model

The destructive cutover is a **Juan-direct-authorization shape**.
Athena's relay carries strong signal but the schema-drop step is
irreversible-against-current-prod, so I hold for Juan's explicit
go on the day, after the AC patch carrying the routing fixes is
published in Render.

## Lane split

| Role | Owner |
|---|---|
| Author consolidated 001 + transformation script | Grace (dev team) |
| Architectural review (schema-equivalence + transformation enumeration) | Athena |
| Cutover execution | Hestia |
| Cutover authorization | Juan |

## Pre-cutover authoring (parallel, no prod risk)

These three artifacts must exist before Phase 0:

1. **Consolidated 001** representing post-cutover schema, with all
   historical edits baked in. Replaces existing 001 + 002 + 003 +
   004 in `ac/backend/src/aweb_cloud/migrations/aweb/`. The other
   files are deleted in the same commit.

2. **Transformation script** enumerating any data-shape changes
   needed during restore. List what does need transforming, with
   assertions baked in (every NOT NULL / CHECK / FK in the deltas
   vs. pre-state prod data).

3. **Schema-equivalence proof** (Athena's review): apply
   [old-001 + 002 + 003 + 004] to a clean local DB; apply [new
   consolidated-001] to a second clean local DB; pg_dump both
   schemas (--schema-only); diff. Identical diff = schema-
   equivalence proven. Different diff = consolidation has drift;
   reject and ask Grace to fix.

   Scripted scaffolding at
   `agents/hestia/scripts/cutover_schema_equivalence.sh`:

   ```bash
   ./agents/hestia/scripts/cutover_schema_equivalence.sh \
       main feature/aweb-consolidation
   ```

   Orchestrates: two AC git worktrees from each ref → `uv sync`
   each → `createdb` two scratch DBs → `aweb-db --env=development
   setup` against each → `pg_dump --schema-only` both → normalize
   (strip pg_dump headers, version-sensitive SETs,
   schema_migrations data blocks) → `diff -u`. Exits 0 with
   "IDENTICAL" on success, exits 1 leaving worktrees+DBs in
   `/tmp/cutover-schema-eq-<ts>/` for inspection on diff.

## Local roundtrip gate (mandatory before prod cutover)

`make verify-db-reset-roundtrip` against the new consolidation +
a real prod-shape data dump (sourced from a recent prod-dump kept
read-only):

1. `dropdb` + `createdb` for a fresh local DB.
2. Apply the new consolidated 001 via `aweb-db --env=development
   setup`.
3. Restore the filtered prod-shape dump (schema_migrations
   stripped per `_write_filtered_restore_dump`).
4. Verify expected clean-schema columns
   (`messages.from_address`, `chat_messages.from_address`,
   `chat_participants.address`).
5. Verify row counts per table match dump's COPY/INSERT counts.
6. Run `make test-backend` against the restored DB.

All steps must pass. Failure here means the cutover would fail
on prod the same way; **do not proceed**. Loop with Grace + Athena
on the failure shape.

## Pre-cutover safety net

Just-before-cutover (with prod still on the working binary):

```bash
# From ac/ root with .env.production loaded:
TS=$(date -u +%Y%m%dT%H%M%SZ)
make prod-dump PROD_ENV_FILE=.env.production \
    DB_RESET_DUMP=/tmp/aweb-cloud-safety-net-${TS}/full-data-dump.sql

ls -la /tmp/aweb-cloud-safety-net-${TS}/full-data-dump.sql
head -50 /tmp/aweb-cloud-safety-net-${TS}/full-data-dump.sql
```

**Separate operation from the cutover dump** (different filename,
different timestamp). Copy the safety-net dump off the machine
running cutover (workstation copy + Juan's machine if he can hold
one). The safety-net is the rollback artifact: if cutover goes
sideways, restore THIS dump onto a fresh re-migrated DB at the
prior-binary schema and re-deploy the prior binary.

**DO NOT compose the safety-net path with the cutover path.** Keep
them independent so a failure in one cannot corrupt the other.

## Execution chain

Each phase pauses for **explicit Juan-go** before the next runs.
No orchestrated single-shot reset: we step individually so we can
inspect between.

### Phase 0 — Pre-flight checks

```bash
# Confirm we're on the cutover commit:
git -C ac log --oneline -5

# Confirm /health is what the safety-net dump represents:
curl -sS https://app.aweb.ai/health | jq .build

# Confirm AWID is healthy (we're not touching it):
curl -sS https://api.awid.ai/health
```

**Pause. Juan goes on phase 1.**

### Phase 1 — Cutover dump (just before drop, fresh)

```bash
make prod-dump PROD_ENV_FILE=.env.production \
    DB_RESET_DUMP=/tmp/aweb-cloud-cutover-${TS}/full-data-dump.sql

grep -c '^COPY ' /tmp/aweb-cloud-cutover-${TS}/full-data-dump.sql || true
grep -c '^INSERT INTO ' /tmp/aweb-cloud-cutover-${TS}/full-data-dump.sql || true
```

**Pause.** Confirm dump file size is comparable to prior known-good
dumps. **Juan goes on phase 2.**

### Phase 2 — Drop schema aweb (IRREVERSIBLE)

Before running, verify:

- `/health` was just confirmed in phase 0.
- Phase 1 dump is on disk, readable, non-empty.
- Safety-net dump from earlier exists on at least one off-machine
  copy.

`aweb-db drop` drops the WHOLE database, not just schema aweb. To
keep `aweb_cloud` and `server` schemas intact (Athena confirmed
only `aweb` schema gets consolidated), use direct psql:

```bash
DATABASE_URL=$(grep -E '^DATABASE_URL=' ac/.env.production \
    | sed -E 's/^DATABASE_URL="?(.*)"?$/\1/')
psql -v ON_ERROR_STOP=1 "$DATABASE_URL" -c "DROP SCHEMA aweb CASCADE;"
```

Drops ONLY the `aweb` schema. The `aweb_cloud` and `server`
schemas remain. Their `schema_migrations` tables remain intact.
The `aweb.schema_migrations` row(s) for aweb's chain drop along
with the schema.

**Pause. Juan goes on phase 3.**

### Phase 3 — Apply consolidated 001 (clean migration baseline)

```bash
cd ac && make prod-migrate-direct PROD_ENV_FILE=.env.production
```

Without an existing `aweb.schema_migrations` table or rows for the
aweb chain, the migrate runner sees the chain as fresh and applies
the consolidated 001 from scratch. New checksum row gets recorded.

After it returns, run the verify-applied SQL block (sample for the
aame consolidation; adjust per consolidation shape):

```sql
-- Should be ONE row, the consolidated 001:
SELECT filename, module_name, checksum, applied_at, applied_by, execution_time_ms
FROM aweb.schema_migrations
WHERE module_name = 'aweb-aweb'
ORDER BY filename;

-- Object existence (post-state schema):
SELECT to_regclass('aweb.conversations'),
       to_regclass('aweb.conversation_participants'),
       to_regclass('aweb.messages'),
       to_regclass('aweb.tasks'),
       to_regclass('aweb.teams'),
       to_regclass('aweb.agents');

-- Constraints (sample from prior 003, now baked into consolidated 001):
SELECT conname FROM pg_constraint
WHERE connamespace = 'aweb'::regnamespace
  AND conname IN ('conversations_created_by_did_not_blank',
                  'conversation_participants_alias_not_blank',
                  'conversation_participants_reachable');

-- Updated_at trigger (sample from prior 003):
SELECT tgname FROM pg_trigger
WHERE tgrelid = 'aweb.conversations'::regclass
  AND tgname = 'trg_conversations_updated_at'
  AND NOT tgisinternal;

-- Deferrable FK shape (sample from prior 004):
SELECT conname, condeferrable, condeferred
FROM pg_constraint
WHERE conrelid = 'aweb.tasks'::regclass
  AND conname = 'tasks_parent_task_id_fkey';
```

Schema must be present and constraint shape must match what the
consolidation 001 declared. If anything is missing, **do NOT
proceed to restore** — the schema apply was incomplete.

**Pause. Juan goes on phase 4.**

### Phase 4 — Restore filtered dump

```bash
make prod-restore PROD_ENV_FILE=.env.production \
    DUMP=/tmp/aweb-cloud-cutover-${TS}/full-data-dump.sql
```

`prod_db_reset.py restore` does:
- TRUNCATE all tables in (aweb, aweb_cloud, server) RESTART
  IDENTITY CASCADE.
- Disable `users_create_principal` trigger.
- Apply filtered dump (schema_migrations COPY blocks stripped).
- Re-enable trigger.
- Verify row counts match dump's COPY/INSERT counts.

Watch for row-count mismatches in the verifier output. **Any
mismatch = ABORT, investigate.**

**Pause. Juan goes on phase 5.**

### Phase 5 — Re-deploy aame-aware binary

Juan deploys the AC patch carrying the consolidated 001 from GHCR
(manual deploy per existing pattern). Wait for `/health` to come
up:

```bash
# Loop until /health shows the new release_tag:
curl -sS https://app.aweb.ai/health | jq .build
```

### Phase-pacing SLO (banked from Athena 2026-05-04)

The cutover-irreversible phases (Phase 2 drop → Phase 5 deploy
live) are a window where some queries 5xx. **Sprint these phases
under explicit time targets** — do NOT take coffee-break-shaped
pauses between them.

| Phase transition | Target | Notes |
|---|---|---|
| Phase 1 (dump complete) → Phase 2 (drop start) | ≤ 2 min | quick file-size/head sanity |
| Phase 2 (drop) → Phase 3 (migrate) | ≤ 30 sec | psql DROP returns immediately |
| Phase 3 (migrate complete) → Phase 4 (restore start) | ≤ 2 min | verify-applied SQL block + sanity |
| Phase 4 (restore complete) → Phase 5 (deploy start) | ≤ 2 min | row-count verifier returns; signal Juan |
| Phase 5 (deploy live on /health) → Phase 6 (smoke probes complete) | ≤ 3 min | new binary up; mail/chat probes |
| **Phase 2 start → Phase 6 complete (TOTAL)** | **≤ 10 min** | hard ceiling worth pre-coordinating |

If any phase will overshoot, mail/chat Juan and Athena before
continuing. If total approaches 15 min, treat as an incident and
consider rollback to safety-net dump.

### Window-shape note (the why)

Between deploy and cutover-complete, the old binary's queries hit
the new schema (or vice versa) and 5xx for any path touching the
delta. Window length depends on phase pacing. Sprint phases 4→5
tightly so the window is minutes, not hours.

If the window concerns Juan operationally, a feature flag at
deploy time that returns 503 with structured body for all
delta-paths until cutover completes is the bigger-mitigation
option (not mandatory; named for awareness).

### Phase 6 — Live verification

```bash
# Schema verification still passes after deploy:
psql -v ON_ERROR_STOP=1 "$DATABASE_URL" -c "
SELECT to_regclass('aweb.conversations'),
       (SELECT count(*) FROM aweb.schema_migrations WHERE module_name='aweb-aweb');
"

# Smoke probes from new-binary CLI:
aw mail send --to athena --subject cutover-smoke-1 --body "..."
aw chat send-and-wait athena "cutover smoke probe"
aw mail send --to-did did:aw:<athena-did> --subject cutover-smoke-2 --body "..."
```

All probes succeed = cutover verified-live. Mail
Athena/Sofia/Iris/Juan with full evidence: dump filename + size,
drop SQL output, verify-applied SQL output, restore row-count
verification, post-deploy `/health`, smoke-probe message_ids.

## Rollback paths

The rollback target is the safety-net dump (taken pre-cutover).

| Failure at | Recovery shape |
|---|---|
| Phase 1 (cutover dump itself fails) | Nothing destructive happened. Standdown, investigate, retry next window. |
| Phase 2 (DROP SCHEMA fails) | Schema didn't drop cleanly; psql error halts. No data lost; investigate. |
| Phase 3 (consolidated 001 doesn't apply) | Schema is gone, no replacement. Two recovery shapes: (a) re-deploy prior binary which expects pre-cutover schema — needs old-001 file applied directly via psql, then safety-net dump restored, heavy. (b) Quicker: fix the consolidated 001 problem, retry phase 3 (no data restored yet, so phase 3 is idempotent against empty aweb schema). |
| Phase 4 (restore row-count mismatch or psql error) | Data partially restored. ABORT immediately. Recovery: drop schema again, re-apply consolidated 001, retry restore from same dump. If consistent fail: fall back to safety-net — drop schema, apply prior-era 001, restore safety-net dump, re-deploy prior binary. |
| Phase 5 (deploy fails) | Schema and data at post-cutover shape, binary still pre-cutover. App will misbehave. Recovery: get the AC patch deploying ASAP, or restore safety-net dump (TRUNCATE + restore) onto pre-cutover schema after dropping + re-applying prior-era 001. |

**Treat every failure mode as "stop, don't compose, escalate to
Juan + Athena."** The cutover is high-stakes and chained; don't
attempt clever recovery moves under pressure.

## Constraint-diff audit (BEFORE and AFTER, mandatory)

Banked from cutover #2 (2026-05-05). `DROP SCHEMA X CASCADE` can
CASCADE-drop FK constraints declared in OTHER schemas that
reference X. The drift is invisible to the migration chain.

Run BEFORE cutover (spin up clean local DB from current code,
snapshot pg_constraint, compare to prod). Document any pre-
existing drift that needs separate recovery.

Run AFTER cutover (same query against prod and clean local).
Assert ZERO drift in either direction.

### Query

```sql
SELECT n.nspname || '.' || c.relname || '.' || con.conname AS cstr,
       con.contype
FROM pg_constraint con
JOIN pg_class c ON c.oid = con.conrelid
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname IN ('aweb','aweb_cloud','server')
  AND con.contype IN ('f','c','p','u','x')
ORDER BY 1;
```

### Diff

```bash
comm -23 <(sort baseline.txt) <(sort prod.txt)  # in baseline, missing from prod
comm -13 <(sort baseline.txt) <(sort prod.txt)  # in prod, extra
```

Both must be empty for "zero drift" claim. Cutover #2 evidence:
prod=226 / baseline=226, both diffs empty → claim valid.

## Post-cutover hygiene

- Verified-live mail to Athena / Sofia / Iris / Juan with full
  evidence trail.
- Append dated entry to `logbook.md` with what worked + what
  failed.
- If a learning is general (not incident-specific), promote to
  `legacy.md`.
- Sweep stale aw work claims after the cycle.
- Update `../../status/operations.md` to reflect new live state.
- Decide whether the awid-shaped wrapper script
  (`scripts/cloud_aweb_schema_reset.py`) should land for next
  time. If we cutover more than once, the wrapper saves time.

## Worked example (cutover #2, 2026-05-05)

Two-cutover sequence (aweb-side first, then aweb_cloud-side) to
recover from 133a7d94's pre-Render-auto-deploy in-place edit of
TWO 001_initial.sql files. Cutover #1 (aweb) was urgent and took
the strictly-correct destructive shape. Cutover #2 (aweb_cloud)
was authored as forward-additive (Grace's 8fa36cd0: revert 001 +
additive 002) — initial recovery proposal was the corresponding
hotfix-style "UPDATE schema_migrations" path, but Juan rejected
for "strictly correct and clean" before launch.

Critical decision evidence: a constraint-diff audit on prod
revealed 6 cross-schema FKs missing (CASCADE-dropped during
cutover #1). The forward-additive path could neither recreate nor
detect those. Destructive cutover #2 was the only shape that
closed both the migration-chain-immutability concern AND the
silent FK drift in one pass.

End state: prod=226 constraints, clean baseline=226 constraints,
zero drift in either direction. Phase timings: drop=1s, migrate
(001+002)=917ms, restore=2min, total cutover ~3min (within banked
10-min SLO).

Full incident narrative in `logbook.md` under 2026-05-05.
