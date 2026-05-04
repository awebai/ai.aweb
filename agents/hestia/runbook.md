# Operations Runbook

Hestia owns this. The runbook encodes how to carry a release across
the build/ship boundary without engineer assistance: pre-flight,
gates, tag, watch CI/CD, verify live, post evidence.

## Status of this document

**Seeded 2026-05-01 from prior-knowledge sources** — the banked
release decisions in `../../docs/decisions.md`, the Makefile survey
on this same day, and the standing release-discipline policies
(banked through 2026-04-26).

**First end-to-end exercise complete 2026-05-02** (ac v0.5.18 +
aw CLI 1.18.8, claim-human cli_signup orphan vector + BYOD username
contract). The chain ran solo end-to-end including a gate-failure
detour and recovery. Sections marked **[unvalidated]** below have
been removed where the exercise validated them; remaining
unvalidated markers are for shapes that the v0.5.18 release didn't
exercise (e.g., aweb-only releases, awid registry releases). Real
timing and failure-mode notes from the first exercise are folded
in below.

When validation discovers a gap, the runbook updates. When Athena
adds a new gate, the runbook updates. When a banked memory adds an
operational lesson, the runbook updates.

## Artifact map and release dependencies

Six distinct artifacts ship from two repos with five distribution
channels.

**aweb repo (5 artifacts):**

| Artifact | Tag pattern | Distribution | Pinned by |
|---|---|---|---|
| aweb server (Python) | `server-vX.Y.Z` | PyPI `aweb` | ac (`aweb>=…`) |
| aw CLI (Go) | `aw-vX.Y.Z` | GitHub Releases (goreleaser) + npm `@awebai/aw` | end-users |
| awid lib (Python) | `awid-service-vX.Y.Z` | PyPI `awid` | ac (`awid-service>=…`) |
| awid registry (Docker) | `awid-vX.Y.Z` | GHCR; Juan deploys manually; runs at `api.awid.ai` | (independent service) |
| @awebai/claude-channel (TS) | `channel-vX.Y.Z` | npm | end-users (Claude Code) |

The version field shared between `awid-vX.Y.Z` and `awid-service-vX.Y.Z`
points at the same `aweb/awid/pyproject.toml` — single source code, two
distribution channels (Docker image + PyPI library).

**ac repo (1 artifact):**

| Artifact | Tag pattern | Distribution | Live at |
|---|---|---|---|
| aweb-cloud (Docker) | `vX.Y.Z` | GHCR; Juan deploys manually from GHCR | `app.aweb.ai` |

ac pins `aweb` and `awid-service` in `backend/pyproject.toml`.

### Release-as-needed, not lockstep

Per Juan: artifacts ship as needed, not always together.

- **aweb server bump usually drags ac.** When the server changes
  contract or behavior that ac depends on, ac picks up the new pin
  in a follow-on release. `cross-repo-change` skill summary:
  OSS lands first → tag → CI publishes to PyPI → wait for
  propagation → bump ac pin (with `uv sync --refresh`) →
  `make release-ready` on ac → ac tag → GHA builds image →
  Juan deploys manually from GHCR → verify live.
- **awid tends to be more independent.** Both the Docker image
  (`awid-vX.Y.Z` → GHCR → api.awid.ai) and the PyPI lib
  (`awid-service-vX.Y.Z` → PyPI) can move on their own cadence
  unless ac needs the new client features.
- **aw CLI (Go) often moves in lockstep with aweb server** but
  isn't required to. The `release-all-tag` Makefile target cuts
  server + aw + channel + awid + awid-service from the same
  commit; that target exists for the all-together case, not as
  a default.

**Per-case rule:** which artifacts move and in what order is
discussed with Athena on each release. Her bless-and-run mail
names: target repo, expected SHA of clean main, change shape, the
code-reviewer-pass result, and which other artifacts (if any)
need to move in the same wave. If the wave touches aweb, she
also names whether ac needs to follow and in what order.

## What gets you to a release candidate (input)

A release candidate enters my surface as a mail from Athena:

- Subject: `release-handoff: <repo> <version-target>` (or shape).
- Body names: target repo (aweb / ac), expected SHA of clean main,
  release-notes draft, code-reviewer-subagent pass result on the
  gate-input commits (banked policy 13).

Until that mail lands, no candidate exists from my side. I do NOT
self-spawn a release on a bump commit I find sitting on main —
that would skip the build/ship boundary and decouple the gate from
engineering's signal.

**Bless-and-run mail shape (validated v0.5.18, 2026-05-02):**

Athena's release-handoff mail under the new role model includes:

- Subject `Bless-and-run: <one-line change summary> (<repos involved>)`.
- Repos and commits: each repo + commit SHA, with one-line
  description per commit. "Already on main" if pushed; flag
  otherwise.
- Cross-repo dependency check: which artifacts move together,
  which can ship independently, which decisions she leaves to
  Hestia.
- Compat-test invocation guidance: which compat scope applies to
  this release per the operational rule.
- Release notes draft: closes / does NOT close / code evidence
  (key commits + tests added) / affects / live verification
  (smoke probe + browser-verify if UI surface).
- Failure-mode pre-warning: any expected gate output that should
  be treated as "intentional break observed correctly" rather
  than regression.
- Bless-and-run signal: explicit "you own the release from here."

Hestia confirms gate-run readiness, runs the chain. Mails back
the failure shape if anything goes red; mails back verified-live
when the release is on `/health`.

## The chain (step-by-step)

### 1. Pre-bump check

```sh
git -C aweb pull   # or git -C ac pull
git -C <repo> rev-parse HEAD
```

Confirm head matches the SHA in Athena's handoff mail. If it
doesn't, stop and ask — never gate against a different commit than
what was reviewed.

### 2. Bump

The bump itself is a single commit on the target repo:

- `pyproject.toml`: version field bumped to the target version.
- `uv.lock`: regenerated minor (the next step's `uv sync` will
  produce the canonical lock).

For aweb (multi-component: server, awid, awid-service, channel,
cli), see "aweb-specific" below — multiple version fields move in
lockstep or independently per the release shape.

For ac (unified backend version), only `backend/pyproject.toml`
moves.

**[unvalidated]** Whether the bump commit is authored by Athena,
Mia, or me-as-Hestia — TBD by the first real handoff. Today's
bumps were Mia's. Prior decisions show CTO (Randy) authored bumps.
Not load-bearing for the gate run; load-bearing for attribution
in the verified-live mail.

### 3. Sync

```sh
uv sync --refresh   # ac
# or
uv sync --refresh   # aweb (run from each component's pyproject root)
```

`--refresh` matters. If the bump pins a downstream that was just
published to PyPI, the local cache may still hold the prior version.
Banked from awid prod cutover (2026-04-25) and earlier ac releases:
the PyPI cache-lag window can mask a stale resolution. Always
`--refresh` post-bump.

### 4. Gates (release-ready)

#### ac

```sh
cd ac && make release-ready
```

Composes (per `ac/Makefile`, post-commit `24cb7c68`):

- `release-verify-remote` — confirms remote state matches expectation.
- `release-verify-model` — model-side verification.
- `release-verify-migrations` — migrations are forward-only, ordered,
  checksum-clean.
- `test-backend` — pytest suite. ~1250 selected as of v0.5.17 (1263
  collected, 13 deselected).
- `test-frontend` — vitest suite. ~96 tests as of v0.5.5; ~25 files.
- `test-two-service` — Docker two-service stack (cloud + awid).
  ~9–10 tests depending on era.
- `test-cloud-user-journeys` — local-aw arm only as of `24cb7c68`
  (the chain previously composed local-aw + installed-aw; the
  installed-aw arm moved to the explicit `test-cloud-user-journeys-compat`
  target, ~233s saving on the default chain). Mia's per-Mia mail
  reports release-ready total of 244.56s under the new shape.

All must be green. Per banked policy 4, trust the Makefile's chain;
do not chase adjacent targets that aren't in `release-ready`.

**First-exercise timing (v0.5.18, 2026-05-02):**
- `make release-ready` end-to-end: 198s (3m18s)
- `make test-cloud-user-journeys-compat` (one prior binary): 57s
- Total ac gate run: ~4m15s

Faster than Mia's pre-runbook 244s baseline, possibly cache effects
from a back-to-back run earlier the same evening. Single-run baseline
expected ~225-250s.

##### When to also run `make test-cloud-user-journeys-compat`

Compat covers the installed-aw arm — i.e., it exercises ac against
the published `aw` package on PyPI rather than the sibling
checkout. The default chain skips it for speed; invoke it
explicitly when the release shape risks breaking installed users.

**[validated by Mia + Athena 2026-05-02; awaiting first real-release
exercise for empirical confirmation]**

**Always run compat when any of these apply:**

- A SQL migration touches a table read or written by aweb-server
  endpoints (schema changes that alter data shape returned over
  existing endpoints break installed-aw clients).
- An API endpoint contract changes (response shape, required
  fields, status semantics).
- Middleware / request-routing / header-validation /
  path-routing changes (the `Invalid team_id format` failure
  class).
- Auth / cert / identity flow changes.
- The `aweb` pin in `ac/backend/pyproject.toml` is bumped.

**Skip compat only when both apply:**

- Changes are strictly internal: admin tooling refactor,
  frontend layout / copy, internal Python refactor with NO SQL
  migration AND NO API change AND NO middleware/routing change.
- AND the `aweb` pin is unchanged.

**Practical separation:**

- *Local dev iteration*: default `make release-ready` (no
  compat). ~228s.
- *Ship-bound* (Hestia's surface): ALWAYS include
  `make test-cloud-user-journeys-compat` unless the release is
  strictly internal per the criterion above. Compat run is ~58s
  isolated — cheap insurance.

When in doubt, run compat. The cost of a missed installed-aw
regression (the iteration-class shape that drove
v0.5.13–v0.5.17) is much higher than ~58s.

**Underlying policy (Sofia ratified 2026-05-02 post-convergence):**
cloud tests against the current released `aw` plus the prior two
released versions — three binaries total. Definition: "whatever
the prior two released semver tags happen to be" — patches in
normal weeks, a mix during minor-bump cycles. Not strict
semver-minor.

Internal-test floor only; no public support-window promise.
Customer-facing answer to "what `aw` versions do you support"
stays implicit ("use current `aw`"). The operational criterion
above is what enforces the floor; the criterion itself doesn't
change with the scope.

A formal decision-record entry is deferred per Athena's defer-
pending-evidence discipline: bank from a real multi-version
bless-and-run after Mia wires the multi-version compat infra.
v0.5.18 (the first Hestia exercise) was bug-fix shape, not the
trigger.

**Compat infra status (2026-05-02):** today's
`make test-cloud-user-journeys-compat` exercises one prior binary
(~58s isolated). A multi-version variant is on Mia's plate; when
shipped, compat runs all three binaries (~150s extra in the gate
per Athena). Athena's bless-and-run mail will name which compat
scope is in flight on each release.

#### aweb

```sh
cd aweb && make ship
```

`make ship` is the canonical comprehensive pre-tag-push gate for
aweb. It composes:

- `make test` — `test-server` + `test-awid` + `test-cli` +
  `test-channel`
- `make release-server-check` — server build + tests + dist
  artifact verification
- `make release-channel-check` — channel test + build + npm
  pack dry-run + plugin-version match
- `make release-awid-check` — awid lock + tests + build + Docker
  build verification
- `make test-e2e` — full e2e user journey (banked 2026-04-22
  standing policy: no release cut before this passes green)

The Makefile comment explicitly says `make ship` is the canonical
pre-tag-push gate; do NOT substitute `make test` alone. Banked
discipline: 1.18.3 / 1.18.4 / 1.18.5 / 1.18.6 each ran `make test`
instead of the canonical comprehensive gate, and even though GHA
caught build failures downstream the local gate is supposed to be
authoritative before tag-push.

**`make ship` does NOT push.** It prints "Ready for tag-push" at
the end. Tag-push is always the explicit per-component sequence
(see step 7 below).

Per-component check / tag / push targets:

- `release-server-check` / `-tag` / `-push`
- `release-cli-tag` / `-push`
- `release-awid-check` / `-tag` / `-push` / `-pypi-tag` / `-pypi-push`
- `release-channel-check` / `-tag` / `-push`

`release-all-check` runs the check arms together. `release-all-tag`
+ `release-all-push` exist for the all-together case (aala-epic
shape) but are NOT the default. Most releases move only the
artifacts that need moving.

**First-exercise observation (aw CLI 1.18.8, 2026-05-02):**
- `make ship` end-to-end (test + 3 release-*-checks + test-e2e
  Phases 0-22): **7m6s baseline**. Anomaly threshold: future runs
  over 10 min are a signal worth investigating (test-e2e regressing
  in performance, Docker image build slowing, etc).
- aw CLI version coupling: the Makefile's `CLI_VERSION := SERVER_VERSION`
  is a stale assumption when CLI moves but server doesn't. For aw-only
  releases, tag directly with `git tag -a aw-vX.Y.Z <commit> -m "…"`
  bypassing `make release-cli-tag`. The tag is the source of truth
  for goreleaser; no in-tree version bump needed.
- aweb-side downstream chain: tag-push triggers `aw Sync and Release`
  workflow on awebai/aweb → syncs to awebai/aw repo → triggers
  `aw Release` on awebai/aw → goreleaser publishes GH Releases +
  npm. End-to-end aw-on-npm: ~3 min from tag push.

### 5. SOT analysis (when needed)

For releases that touch protocol surface, schema, or trust model,
walk:

- `aweb-sot.md` (in `aweb/docs/`) — protocol invariants
- `awid-sot.md` (in `aweb/docs/`) — registry invariants
- `trust-model.md` (in `aweb/docs/`) — trust + identity invariants
- `ac/sot.md` (in `ac/docs/`) — cloud-side invariants

If the release shape doesn't touch protocol/schema/trust (e.g.,
v0.5.17 layout-containment fix), SOT analysis is not needed.

When drift is found between the release content and the SOT docs,
mail Athena and work the fix together — code change lands with her;
gate re-runs with me.

### 6. Sofia framing review (only when needed)

**Default: skip.** Bug-fix releases without external-claim weight
tag through the gate chain without Sofia review. Confirmed in
Sofia's 2026-05-01 mail: "Bug-fix releases don't need Sofia in the
loop — tag through your gate chain. If at any point a release
carries external-claim weight (new public capability, behavior
change customers will notice, anything that affects value-prop
framing), mail me before tag; otherwise I read /health when you
post verified-live."

**Mail Sofia before tag when:** new public capability, customer-
visible behavior change, value-prop framing implications. Subject
shape: `framing-review: <release-target>`. Body: release-notes
draft + what's load-bearing for external claim.

### 7. Tag and push (per-tag, never batched)

Banked policy 7. GitHub coalesces same-commit tag pushes into a
single event; GHA workflows triggered by tag pushes do not fire
correctly when tags are batched. Always one `git push origin <tag>`
per tag, sequentially.

```sh
git tag -a vX.Y.Z -m "release: vX.Y.Z, <one-line summary>"
git push origin vX.Y.Z
```

For aweb multi-component releases, push each tag separately (in any
order — what matters is each push is its own event):

```sh
git push origin server-vX.Y.Z
git push origin aw-vX.Y.Z
git push origin awid-vX.Y.Z
git push origin awid-service-vX.Y.Z
# and channel-v* if it moved
```

The aweb 1.18.0 ghost-tag failure mode (banked 2026-04-25) is the
load-bearing reason for this rule. 1.18.0 was pushed as a single
batched `git push origin tag1 tag2 tag3 tag4` — all 4 GHA publish
workflows failed to fire (event-coalescing on same-commit batched
tags), nothing reached PyPI/npm. The 1.18.1 recovery pushed
individually and all 5 workflows fired.

### 8. Watch CI/CD and signal Juan for the deploy step

After each tag push, the corresponding GHA workflow fires. For ac,
that's the cloud CI/CD run (image build → GHCR publish). For aweb,
that's per-component (PyPI for server / cli / awid-service; npm for
channel; GHCR Docker for awid registry image).

Use `gh run list` and `gh run view <id> --log` (or the GHA web UI)
to watch the run. Confirm it fired (banked failure: workflow
silently doesn't fire when tag push is batched).

**Docker-image deploys are manual.** This applies to both:

- ac (`vX.Y.Z` → GHCR → live at `app.aweb.ai`)
- awid registry (`awid-vX.Y.Z` → GHCR → live at `api.awid.ai`)

Render does NOT auto-deploy from GHCR for either. When the GHA
build completes and the image is at GHCR, Juan deploys manually.
Mail or chat Juan when the image is ready:
"<service> v<version> image at GHCR — ready to deploy when you
are." Then wait for him to deploy before moving to verify-live.
Do not attempt to automate the deploy; stay in operations lane
(gates, signal, verify, post evidence).

**PyPI / npm / GitHub Releases publishes don't have a manual
deploy step** — once GHA finishes the publish workflow, the
artifact is "live" in the sense of available to consumers. The
remaining wait is just PyPI/npm propagation before downstream
`uv sync --refresh` / `npm install` resolves the new version.
Applies to: `server-vX.Y.Z` (PyPI `aweb`),
`awid-service-vX.Y.Z` (PyPI `awid`), `aw-vX.Y.Z` (GitHub
Releases + npm `@awebai/aw`), `channel-vX.Y.Z` (npm
`@awebai/claude-channel`).

### 9. Verify live

**[partly validated tonight via /health probe]** GHA green ≠ live.
Package published ≠ live. Tag pushed ≠ live. Image at GHCR ≠ live.
The release is live only after Juan has deployed AND the deployed
service reports the new version AND the changed surface behaves
correctly.

#### Step 9a: /health version match

```sh
curl -sS https://app.aweb.ai/health | jq .   # ac
curl -sS https://api.awid.ai/health | jq .   # awid
```

Assert:

- `release_tag` matches the tag you just pushed (ac only — aweb's
  surface is the OSS package, no `/health` endpoint per repo).
- `git_sha` matches the bump commit (ac).
- `aweb_version` and `awid_service_version` match the pin in
  `backend/pyproject.toml` post-bump.

If any field doesn't match, Juan hasn't deployed yet (or the
deploy is still rolling). Wait, re-check. If GHA is green and the
image is at GHCR but /health doesn't show the new version after
Juan signals "deployed," ask him to confirm the deploy completed.
Don't troubleshoot deploy infra — that's outside the operations
lane.

#### Step 9b: Smoke probe of the changed surface

For each release, exercise what actually changed:

- **New endpoint**: curl the endpoint with a real-shape request.
- **New CLI behavior**: run the command against a clean workspace.
- **UI change**: browser probe (Playwright MCP or manual). Banked
  policy 10. v0.5.17 (layout-containment) is exactly this shape —
  open the Add-Existing dialog and confirm the long fetch-cert
  command scrolls horizontally inside the modal instead of widening
  it.

#### Step 9c: Banked failure modes to check

- **Docker container clock-drift after macOS host sleep**: HTTP 401
  timestamp-skew on signed requests after laptop sleep. Resolved by
  `make test-two-service-down && make test-two-service-up` — not a
  code regression, just stack restart. Banked symptom; if smoke
  probe returns 401 timestamp errors, restart the local stack
  before suspecting the release.

### 9.5. Run pending migrations (when applicable)

**[banked from Athena's mail 2026-05-02]**

**SQL migrations in aweb-server do NOT run automatically when a
new aweb-cloud image deploys to Render.** This is filed as a bug
(task #13, auto-migration bug). Until it's fixed, every release
whose aweb pin includes new migration files requires a manual
migration run on the production aweb-cloud DB after Juan's
deploy completes.

If you skip this step on a release that has migrations: queries
against the new tables/columns fail in production. The release
shows healthy on `/health` because the API server starts fine,
but anything that touches the new schema breaks.

**When this step applies:**

- Athena's bless-and-run mail explicitly names migration files
  (going forward, she'll surface them when relevant), OR
- Git-log check at gate-run time: `git -C aweb log --diff-filter=A
  --name-only <prev-aweb-tag>..<this-aweb-tag> -- "**/migrations/**"`
  shows new files.

If either condition is true, sequence is:

1. Verify Juan has deployed (step 9 /health match).
2. Run the pending migration(s) against the prod aweb-cloud DB.
3. Verify migration applied (schema_migrations row added; new
   tables/columns exist).
4. Smoke probe of the changed schema (e.g., a query that
   exercises the new column or table).
5. THEN post verified-live mail (step 10).

**Apply mechanism — partially understood (Grace + Athena, 2026-05-02):**

OSS aweb-server applies bundled migrations automatically at
startup via `AsyncMigrationManager.apply_pending_migrations()`,
called from `DatabaseInfra.initialize(run_migrations=True)`
(`server/src/aweb/db.py`). So in theory the deploy SHOULD
auto-apply — the contradiction with Juan's "doesn't run
automatically on Render" is AC/Render/Neon-side: either the
deploy doesn't restart the aweb-server cleanly, OR initializes
without `run_migrations=True`, OR ac wraps the server in a way
that bypasses the auto-migration path. **Mia owns the AC-side
answer; pending her reply.**

Until that resolves: assume the migration is NOT auto-applied
and run it manually post-deploy. Pessimistic default; turning
out to be auto-applied means the manual run is a no-op
(idempotent) — turning out NOT to be means we caught a real
production-broken state.

**Concrete invocation (folded from Athena's bless-and-run mail
968d03a3, 2026-05-02):**

```sh
cd ac && make prod-migrate-direct PROD_ENV_FILE=.env.production
```

The Makefile target wraps the multi-schema migration runner against
the prod aweb-cloud DB. `.env.production` is the operational secret
file holding `AWEB_DATABASE_URL` / `DATABASE_URL` for prod (Juan's
machine; not in the repo). Mia/Grace confirmed this is the
canonical path until task #13 (auto-migration on Render deploy)
lands.

Runs both ac and aweb schemas — applies any pending migrations
in either schema. For an aame-shape ship, that's
`aweb/server/src/aweb/migrations/aweb/002_conversations.sql` and
`003_conversations_constraints.sql`. Idempotent — already-applied
migrations are no-ops; applies only the pending ones.

Grace recommended a more operator-friendly variant
(`aweb-prod-migrate` + `aweb-prod-pending` with
`AsyncMigrationManager.get_pending_migrations()` / dry-run
support) but `make prod-migrate-direct` is the working command
today.

**Pre-flight check for 003 specifically (and any future
constraint-adding migration):**

`003_conversations_constraints.sql` adds `CHECK` constraints via
`ALTER TABLE ADD CONSTRAINT`. PostgreSQL full-table-scans existing
rows at constraint-add time. If the prod aweb-cloud DB carries any
row that violates the new constraint, the migration fails at the
ALTER step — the constraint doesn't land, the schema-migrations
row doesn't land, the ship is blocked until data-repair clears the
offenders. Not destructive (retry is possible after fix-up), but
does halt verified-live.

Run these BEFORE applying 003 against an environment with
durable data (staging, prod):

```sql
-- Rows that would fail conversations_created_by_did_not_blank
SELECT COUNT(*) AS bad_created_by
FROM aweb.conversations
WHERE BTRIM(created_by_did) = '';

-- Rows that would fail conversation_participants_alias_not_blank
SELECT COUNT(*) AS bad_alias
FROM aweb.conversation_participants
WHERE BTRIM(alias) = '';

-- Rows that would fail conversation_participants_reachable
SELECT COUNT(*) AS bad_reachable
FROM aweb.conversation_participants
WHERE address IS NULL AND transport_hint IS NULL;
```

If any count is non-zero: flag the failure shape to Athena before
running the migration. Options are (a) a fix-up migration that
data-repairs first, or (b) accept the constraint failure and the
migration aborts. Athena's call.

For ephemeral test databases (fresh schema per run): this check
is a no-op; nothing to clean up. Only environments with durable
data from the 002-era state need the pre-check.

**[banked from Athena's mail 2026-05-03] NEVER edit a deployed
migration.** Once a migration file (e.g., 003) has even attempted
to apply, pgdbm records its checksum. Editing the file in place
to fix a failure trips the checksum guard on every future
deploy and forces a destructive dump-restore cutover (banked
from awid 0.3.1 → 0.5.1 prod cutover; same shape, same pain).

Recovery scenarios for any constraint-adding migration that
fails or partially applies:

- **Migration succeeds**: schema_migrations row records; done.
- **Migration fails at apply time** (e.g., 003 ALTER TABLE finds
  offending rows): file the next-numbered migration (004 for
  this case) as a data-repair-then-tighten. Pattern:
  1. UPDATE: data-repair offending rows (set sentinel value;
     populate fallback fields; or DELETE orphaned rows if
     appropriate per the data shape).
  2. ALTER TABLE: re-attempt the constraint that the prior
     migration couldn't apply.
  Apply 004 via the same prod-migrate command.
- **Migration partially applied** (DDL succeeded but row insert
  failed mid-way): same rule, file the next-numbered migration
  to complete the work. Don't edit the partially-applied file.

This applies forward forever: every constraint addition that
might fail on persistent data needs its successor data-repair
migration. Never edit a deployed migration.

**[banked 2026-05-04] Same rule applies to AC's embedded
migration copy.** AC bundles its own copy of the aweb migrations
under `backend/src/aweb_cloud/migrations/aweb/` (001_initial.sql,
002_conversations.sql, 003_conversations_constraints.sql, etc.).
Prod's `aweb.schema_migrations` records checksums of THESE files,
not of the OSS aweb-server wheel migrations. Today's prod failure
(`column "conversation_id" does not exist` on v0.5.19, then
checksum mismatch `3953210a…` vs prod `f0331940…`) traced to AC
commit `133a7d94` editing the embedded 001 in-place to make
`tasks.parent_task_id DEFERRABLE` instead of filing a successor
migration. Grace fixed it in AC `a93c69be`: restored 001 to the
`f0331940…` shape, kept 002 + 003, and filed
`004_tasks_parent_task_deferrable.sql` as the data-repair-shaped
successor for the deferrable change.

Operational consequence: when chasing a checksum mismatch, check
*both* the OSS aweb wheel migration AND the AC embedded copy.
The bytes that pgdbm hashes are AC's. Diff:

```bash
# AC embedded migrations (what prod actually applied):
ls ac/backend/src/aweb_cloud/migrations/aweb/
sha256sum ac/backend/src/aweb_cloud/migrations/aweb/001_initial.sql

# OSS aweb wheel migrations (the upstream source AC was built from):
ls aweb/server/src/aweb/migrations/aweb/

# History on the AC embedded copy (the one prod cares about):
git -C ac log -- backend/src/aweb_cloud/migrations/aweb/001_initial.sql
```

If `git log` on the AC embedded file shows commits AFTER the
deployed prod release, that's the drift. Recovery is the same
"file successor migration" rule — do NOT edit the embedded 001
back, file 004/005 instead.

**[banked 2026-05-04] Asymmetric compat-test gap is a real risk
the test matrix doesn't catch.** AC's
`make test-cloud-user-journeys-compat` covers (old client +
new server). It does NOT cover (new client + old server). In
24h we hit the missed direction three times:

1. v0.5.18 / aw-1.18.8 ship: claim-human BYOD-username — script
   gap masking the contract; e2e exercised the broken arm and
   passed.
2. aame ship (aweb 1.19.0 / aw 1.19.0): aw 1.19.0 sends
   `conversation_id` on mail/chat; cloud at 1.18.6 rejects as
   `extra_forbidden`.
3. v0.5.19 routing regression: aw 1.19.0 + cloud 1.19.0 used
   Grace's new guard rejecting unsigned-AWID-misses; cloud at
   v0.5.18 (aweb 1.18.6) didn't have the guard so probes worked
   from rolled-back state — confirming the regression was in the
   new-binary path.

Pre-release validation gate that closes this until the matrix
is fixed: run the new-client binary against the live (still
old) prod server before pushing tags. If `aw <new-version>
mail send --to <peer>` and `aw <new-version> chat send-and-wait`
both succeed against rolled-prod-version cloud, you've covered
the asymmetric direction. If either fails, the new client is
ahead of the server by a wire-incompat shape and the release
needs a coordinated bump. (This is a manual fallback. The
proper fix is engineering: add (new-client + old-server) to the
compat matrix.)

**Verify-applied query block (run AFTER apply, regardless of
mechanism):**

```sql
-- Migration metadata
SELECT filename, module_name, checksum, applied_at, applied_by, execution_time_ms
FROM aweb.schema_migrations
WHERE module_name = 'aweb-aweb'
ORDER BY filename;
-- Expect: 001_initial.sql, 002_conversations.sql, 003_conversations_constraints.sql
-- (and any subsequent aame migration files as Grace's epic progresses)

-- Object existence
SELECT to_regclass('aweb.conversations'),
       to_regclass('aweb.conversation_participants');

-- Constraints from 003 specifically
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

These probe both sides: schema_migrations records the filename
AND the actual schema objects exist. Catches partial-apply
states where the row landed but the DDL didn't. Run after the
migration step (whichever way it gets applied), before posting
verified-live.

**Pending migrations as of 2026-05-02:**

- aame.1 added `aweb/server/src/aweb/migrations/aweb/002_conversations.sql`
  on aweb main (commit 6b0f28e). Not yet released; will need
  attention when a future ac release bumps the aweb pin past
  this commit.
- aame consolidation commit (Grace landing soon) will add
  `003_conversations_constraints.sql`.

**Engineering follow-ups (not Hestia surface):**

- task #13: auto-migration bug (the Render contradiction). Sofia +
  Hestia on direction when bandwidth.
- New: add `aweb-prod-migrate` + `aweb-prod-pending` Makefile
  targets in aweb wrapping `AsyncMigrationManager`. Folds cleanly
  into task #13 as a stop-gap if the auto-migration fix takes
  longer (a single-command manual path is better than ad-hoc DB
  access regardless).

### 10. Post verified-live mail

Compose the release post mail:

```
To: athena, sofia, juan
Subject: verified-live: <repo> <version> <one-line summary>
Body:
  - What it fixes (and what nearby issue it does NOT fix)
  - What evidence proves the fix
  - What live check proves deployment (paste /health output snippet
    + smoke-probe result + browser-probe result for UI)
  - GHA run reference (workflow id + URL)
```

Banked rule (release discipline): every fix announcement states
(1) what it fixes, (2) what nearby issue it does NOT fix, (3) what
evidence proves the fix, (4) what live check proves deployment.

Also mail Iris when the release carries an external-claim
opportunity (new capability ready for distribution). Mail Aida when
the release changes a customer-facing surface that affects the
runbook.

## Verified-live probe pattern (compact reference)

| Surface          | Deploy step | Live check                                                   | Smoke probe                              |
|------------------|------------|---------------------------------------------------------------|------------------------------------------|
| ac (cloud)       | Juan manual | `app.aweb.ai/health` `release_tag` + `git_sha` match          | curl changed endpoint or browser-probe the UI |
| awid registry    | Juan manual | `api.awid.ai/health` `version` matches `awid-vX.Y.Z`          | endpoint smoke against `api.awid.ai`     |
| aweb server (PyPI)  | none (GHA publishes) | check on PyPI                                       | `pip install aweb==X.Y.Z` + import smoke |
| awid lib (PyPI)     | none (GHA publishes) | check on PyPI                                       | `pip install awid==X.Y.Z` + import smoke |
| aw CLI              | none (GHA publishes to GH Releases + npm) | check on GH Releases + npm | `aw --version` + smoke command           |
| @awebai/claude-channel | none (GHA publishes to npm) | check on npm                                | `npm install` smoke                      |

## Foot-guns and known failure modes

### PyPI cache-lag

When a downstream pin bumps to a just-published version, `uv sync`
without `--refresh` may resolve the prior cached version. Always
`uv sync --refresh` post-bump.

### make-export compose-interpolation

Bare `export VAR ?= default` lines in a Makefile expose VAR to
subprocess shell environment. `docker compose --env-file foo.env`
then has shell-env-wins precedence over the env-file. Result: env
file is silently overridden by Makefile defaults. If a test fails
because a setting "isn't being read from the env file," check
whether the Makefile is exporting an `?=` default.

### per-tag-not-batched push

See step 7 above. Banked from aweb 1.18.0 ghost-tag.

### Docker container clock-drift after macOS host sleep

See step 9c. Banked symptom: HTTP 401 timestamp errors on signed
requests after laptop sleep. Restart the stack.

### Gate failure in compat — script gaps masquerade as CLI bugs

**[banked from v0.5.18 first-exercise gate failure 2026-05-02]**

When `make test-cloud-user-journeys-compat` fails on what looks like
a CLI/contract regression, also check whether the e2e script's
invocation matches the new contract. Script gaps look like CLI bugs
because the failure surfaces from a CLI command, but the actual root
is in `scripts/e2e-cloud-user-journey.sh` not honoring the new
contract.

Diagnose by arm-pattern, not just exit code. When the compat target
fails, look at WHICH arm fails:

- **Only the installed-aw arm fails** (local-aw passes): real
  installed-aw regression OR an intentional break per the release
  shape. Check Athena's bless-and-run mail for whether the break
  was named.
- **Only the local-aw arm fails** (installed-aw passes): the new
  CLI commit broke a contract the prior CLI honored. Real
  CLI-side regression — failure shape goes to Athena.
- **BOTH arms fail identically**: the failure is in the e2e shell
  script (`scripts/e2e-cloud-user-journey.sh`) — both arms run the
  same script, just with different `$AW_INSTALLED_BINARY`. The
  script's expectations don't match the new server contract. Fix
  is in the script, not in the CLI. Failure shape still goes to
  Athena (script lives in ac, engineering surface).

The v0.5.18 case: A.18 claim-human assertion failed both arms with
empty status/email because the script didn't pass `--username`,
which the new contract required. `run_aw_json` redirected stderr
to stdout, so the CLI's usageError got captured into the JSON
parse and `jq_field` returned empty. Fixed by Athena in 1be46c42
adding `--username "$ORG_SLUG"` to the A.18 invocation.

### Migration file editing

When a project uses a single consolidated migration file (awid uses
this shape — `001_registry.sql`), every additive schema change goes
in a NEW ordered file (`002_<name>.sql`, `003_<name>.sql`, …).
Editing the existing consolidated file in place trips pgdbm's
checksum guard and forces a destructive dump-restore cutover.
Banked from awid 0.3.1 → 0.5.1 prod cutover.

### `make ship` semantics differ between repos

- **aweb `make ship`**: comprehensive pre-tag check. Runs
  `release-all-check` + `release-awid-check` + `test-e2e`. Does
  NOT tag and does NOT push. Prints "Ready for tag-push" at the
  end. Use it as the gate; tag and push manually per step 7.
- **ac `make ship`**: runs `release-ready` (via `ship-tag`'s
  dependency) AND tags + pushes the version from
  `scripts/get_release_version.py`. Auto-pushes the tag, which
  fires GHA immediately. Use this when you want one-shot
  gate-and-ship; use the explicit `make release-ready` →
  `git tag -a` → `git push origin <tag>` sequence when you want
  to inspect gate output before tag exists, or to control when
  GHA fires.

Default for production releases under the new role model: use the
explicit sequence in both repos. The runbook step 4 (gates) and
step 7 (tag and push) sit in separate boxes for a reason — they
deserve separate eyes-on. The auto-ship targets are convenient for
quick local iteration, not the standing release path.

## Standing policies (banked through 2026-04-26, Hestia enforces)

1. Release gate = full e2e + SOT + peer-review (mailed)
2. Review via shared working tree (not chat-pasted diffs)
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written decisions via mail (not in-conversation prose)
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate (no candidate fix ships without local
    end-to-end reproducer flipping pre-fix-failure to
    post-fix-pass) — surface-agnostic
13. Code-reviewer subagent for gate-input commits (Athena runs this
    before signaling Hestia)

## Working-agreement bank (peer-confirmed)

- **Sofia**: out of routing for bug-fix / no-external-claim-weight
  releases. Mail before tag only when external-claim weight applies
  (new public capability, customer-visible behavior change, value-
  prop framing). Otherwise reads /health on verified-live mail.
  (Sofia mail, 2026-05-01.)
- **Iris**: signal her when a release is verified-live and ready
  for external claim. Not yet exercised — Iris not yet online.
- **Aida**: mail when live-state changes affect support runbook.
  Not yet exercised — Aida not yet online.

## Open gaps in this runbook (collect on every exercise)

- First end-to-end exercise pending. The actual shape of an
  Athena release-handoff mail under the new role model needs to
  surface on first real handoff.
- Local reproducer state for the Add-Existing-Identity surface is
  unknown — pending Athena's read.
- Publishing-path timing (the 30+-min cycle Sofia flagged) needs
  to be timed on first ac release and decomposed (GHA build
  versus PyPI propagation versus image build versus deploy
  rollout versus health-check wait).
- Test-suite triage — which targets compose to the ~20-min run,
  which are critical-path for changes of various shapes — needs a
  data pass.
