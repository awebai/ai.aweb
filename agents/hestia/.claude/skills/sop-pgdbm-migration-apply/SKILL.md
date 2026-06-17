---
name: sop-pgdbm-migration-apply
description: Apply pending pgdbm SQL migrations against prod aweb-cloud DB, with constraint-add pre-flight, verify-applied query block, and emergency-metadata-repair guardrails. Invoke as step 9.5 of sop-release-execution-chain when a release adds migration files; also invoke standalone for manual unblocks (e.g., #109/#284 startup-fail loops).
---

# pgdbm migration apply

The procedure for running aweb's pgdbm-managed migrations against
the prod aweb-cloud DB outside the auto-deploy path. Two invocation
shapes:

1. **In-release** (step 9.5 of `sop-release-execution-chain`):
   release shipped migration files, Render auto-apply may not have
   run, we apply explicitly post-deploy.
2. **Standalone emergency unblock**: AC container startup-fail loop
   on `_assert_coordination_schema_ready` because a migration in the
   new image's bundle didn't apply at deploy time (the open
   #109/#284 root-cause).

The mechanics are the same; the trigger and the surrounding
sequence differ.

## Why this skill exists

**SQL migrations in aweb-server do NOT reliably run automatically
when a new aweb-cloud image deploys to Render.** This is filed as
#109/#284. Until those close, every release whose aweb pin includes
new migration files needs a manual migration run after Juan's
deploy completes.

If skipped: queries against the new tables/columns fail in
production. The release shows healthy on `/health` because the API
server starts fine, but anything that touches the new schema
breaks.

## When this skill applies

- Athena's bless-and-run mail explicitly names migration files, OR
- Git-log check at gate-run time shows new files:

  ```sh
  git -C aweb log --diff-filter=A --name-only <prev-aweb-tag>..<this-aweb-tag> \
      -- "**/migrations/**"
  ```

If either condition is true, apply migrations after step 9 (verify
live) and before step 10 (verified-live mail).

## Sequence

1. Verify Juan has deployed (step 9 `/health` match).
2. (Constraint-adding migrations only) Run the pre-flight check
   block below.
3. Apply pending migration(s) against prod aweb-cloud DB.
4. Run verify-applied SQL block.
5. Smoke probe of the changed schema (a query that exercises the
   new column or table).
6. THEN post verified-live mail.

## Pre-flight check for constraint-adding migrations

`003_conversations_constraints.sql` and any future
constraint-adding migration adds `CHECK` / `FK` constraints via
`ALTER TABLE ADD CONSTRAINT`. PostgreSQL full-table-scans existing
rows at constraint-add time. If prod carries any row that violates
the new constraint, the migration fails — constraint doesn't land,
`schema_migrations` row doesn't land, ship is blocked until data
repair clears the offenders.

Not destructive (retry is possible after fix-up), but halts
verified-live.

Run BEFORE applying against an environment with durable data
(staging, prod):

```sql
-- Pattern: for each new constraint, count rows that would fail it
SELECT COUNT(*) AS bad_created_by
FROM aweb.conversations
WHERE BTRIM(created_by_did) = '';

SELECT COUNT(*) AS bad_alias
FROM aweb.conversation_participants
WHERE BTRIM(alias) = '';

SELECT COUNT(*) AS bad_reachable
FROM aweb.conversation_participants
WHERE address IS NULL AND transport_hint IS NULL;
```

If any count is non-zero: flag the failure shape to Athena before
running the migration. Options:

(a) A fix-up migration that data-repairs first, then the
    constraint-adding migration applies cleanly.
(b) Accept the constraint failure; migration aborts. Athena's call.

For ephemeral test databases (fresh schema per run): the check is a
no-op. Only environments with durable data from prior-era state
need the pre-check.

## Apply mechanism (preferred path)

```sh
cd ac && make prod-migrate-direct PROD_ENV_FILE=.env.production
```

The Makefile target wraps the multi-schema migration runner against
the prod aweb-cloud DB. `.env.production` is the operational secret
file holding `AWEB_DATABASE_URL` / `DATABASE_URL` for prod (Juan's
machine; not in the repo).

Runs both ac and aweb schemas — applies any pending migrations in
either schema. **Idempotent** — already-applied migrations are
no-ops; only pending ones apply.

## Verify-applied query block (run AFTER apply, regardless of mechanism)

```sql
-- Migration metadata
SELECT filename, module_name, checksum, applied_at, applied_by, execution_time_ms
FROM aweb.schema_migrations
WHERE module_name = 'aweb-aweb'
ORDER BY filename;

-- Object existence
SELECT to_regclass('aweb.conversations'),
       to_regclass('aweb.conversation_participants');

-- Constraints (sample from 003)
SELECT conname
FROM pg_constraint
WHERE connamespace = 'aweb'::regnamespace
  AND conname IN ('conversations_created_by_did_not_blank',
                  'conversation_participants_alias_not_blank',
                  'conversation_participants_reachable');

-- updated_at trigger from 003
SELECT tgname
FROM pg_trigger
WHERE tgrelid = 'aweb.conversations'::regclass
  AND tgname = 'trg_conversations_updated_at'
  AND NOT tgisinternal;
```

These probe both sides: `schema_migrations` records the filename
AND the actual schema objects exist. Catches partial-apply states
where the row landed but the DDL didn't. Run after the migration
step, before posting verified-live.

## NEVER edit a deployed migration

Banked from awid 0.3.1 → 0.5.1 prod cutover + AC 133a7d94 + the
v0.5.71 / v0.5.72 incident.

Once a migration file has even attempted to apply, pgdbm records
its checksum. Editing the file in place to fix a failure trips the
checksum guard on every future deploy and forces a destructive
dump-restore cutover.

If a migration fails or partially applies, file the next-numbered
migration as a successor:

- **Apply-failed (e.g., 003 ALTER TABLE finds offending rows)**:
  file 004 as data-repair-then-tighten. Pattern:
  1. UPDATE: data-repair offending rows.
  2. ALTER TABLE: re-attempt the constraint.
- **Partially applied** (DDL succeeded but row insert failed
  mid-way): same rule, file the successor.

This applies forward forever. Never edit a deployed migration.

## AC embedded copy vs OSS wheel migrations

AC bundles its own copy of the aweb migrations under
`backend/src/aweb_cloud/migrations/aweb/`. Prod's
`aweb.schema_migrations` records checksums of THESE files, not of
the OSS aweb-server wheel migrations.

When chasing a checksum mismatch, check **both**:

```bash
# AC embedded migrations (what prod actually applied):
ls ac/backend/src/aweb_cloud/migrations/aweb/
sha256sum ac/backend/src/aweb_cloud/migrations/aweb/001_initial.sql

# OSS aweb wheel migrations (the upstream source AC was built from):
ls aweb/server/src/aweb/migrations/aweb/

# History on the AC embedded copy:
git -C ac log -- backend/src/aweb_cloud/migrations/aweb/001_initial.sql
```

If `git log` on the AC embedded file shows commits AFTER the
deployed prod release, that's the drift. Recovery is "file
successor migration" — do NOT edit the embedded file back, file
004/005 instead.

## Emergency metadata repair (one-off only)

Banked from v0.5.71/v0.5.72 incident 2026-06-12. **NOT a release
step, NOT a process to rehearse, NOT something to fold into a
checklist.** This pattern exists only because v0.5.71 happened; the
guard below prevents the next occurrence.

When an emergency unblock requires applying a migration's DDL
out-of-band (currently-known case: `_assert_coordination_schema_ready`
startup-fail loop on Render when AC ships a new migration), the
`schema_migrations` row you insert MUST carry the checksum that
pgdbm will compute at the NEXT deploy — otherwise pgdbm's integrity
check rejects the next container start with a recorded-vs-on-disk
mismatch.

### pgdbm's exact normalization

`pgdbm.migrations.AsyncMigrationManager._calculate_checksum`:

```python
def _calculate_checksum(self, content: str) -> str:
    normalized_content = content.replace("\r\n", "\n").strip()
    return hashlib.sha256(normalized_content.encode("utf-8")).hexdigest()
```

**Raw `sha256sum file.sql` is WRONG for `schema_migrations.checksum`.**
The CRLF→LF normalization is usually a no-op on macOS/Linux working
trees, but the trailing `.strip()` is load-bearing: it removes the
trailing newline that almost every editor adds. In the v0.5.71
incident, the trailing strip changed the checksum because the file
had a trailing newline.

### Two acceptable shapes for an emergency manual unblock

**1. (Preferred)** Run AC's product migration command, which
constructs the migration manager correctly and records the
pgdbm-computed checksum by construction:

```sh
python -m aweb_cloud.cli migrate
```

Or programmatically via the existing helpers in
`aweb_cloud.migration_paths`: `create_cloud_migration_manager(db)`
and `apply_cloud_migrations(db=api_db)`. Both construct
`AsyncMigrationManager` with `module_name=CLOUD_MODULE`
("aweb_cloud") and `migrations_table="schema_migrations"`. The
pgdbm `apply_pending_migrations()` call inside substitutes the
`{{schema}}` template, executes DDL, and inserts the
`schema_migrations` row with the pgdbm-computed checksum in one
transaction per migration. No room for a checksum drift.

**2. (Only if #1 is not possible)** Hand-rolled apply + insert MUST
recompute the checksum using the exact pgdbm normalization above:

```python
content = open(migration_path).read()
normalized = content.replace("\r\n", "\n").strip()
checksum = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
# then INSERT with this checksum, NOT hashlib.sha256(content.encode()).hexdigest()
```

### Why the gate catches this

The AC `make release-ready` chain includes
`release-verify-migration-immutability`, which calls
`backend/scripts/verify_migration_immutability.py`. That script
computes the pgdbm-normalized checksum for every migration on disk
and compares against the `schema_migrations.checksum` column for
every applied row, refusing to ship if any pair disagrees.

The gate caught the v0.5.71 manual-unblock checksum drift on the
very next AC ship (v0.5.72 release-ready, 2026-06-12).

**Trust the gate. Fix the manual path.**

### Incident shape (2026-06-12, banked verbatim)

- v0.5.71 manual unblock used
  `hashlib.sha256(body.encode()).hexdigest()` — raw SHA of file
  bytes.
- DB recorded `fe0bd0aa…` for migration 005; pgdbm at next deploy
  would compute `735b07e7…` for the same file.
- v0.5.72 release-ready caught the mismatch pre-deploy.
- Recovery (Juan-ratified): one guarded `UPDATE
  aweb_cloud.schema_migrations SET checksum=<pgdbm-normalized>
  WHERE id=5 AND checksum=<raw>` — treated as audited emergency
  metadata repair, NOT represented as a migration. The migration
  file body and applied DDL were unchanged; only the recorded
  fingerprint was corrected.

## Asymmetric compat-test gap

Banked 2026-05-04. AC's
`make test-cloud-user-journeys-compat` covers (old client + new
server). It does NOT cover (new client + old server). In 24h
2026-05-04 we hit the missed direction three times.

Pre-release manual gate that closes this until the matrix is fixed
in CI: run the new-client binary against the live (still old) prod
server before pushing tags. If
`aw <new-version> mail send --to <peer>` and
`aw <new-version> chat send-and-wait` both succeed against
rolled-prod-version cloud, the asymmetric direction is covered. If
either fails, the new client is ahead of the server by a
wire-incompat shape and the release needs a coordinated bump.
