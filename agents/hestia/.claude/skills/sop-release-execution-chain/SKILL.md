---
name: sop-release-execution-chain
description: Carry a release from a release-handoff mail to verified-live evidence — both aweb-side cuts (server/cli/awid/channel) and ac-side ships. Concrete commands, env vars, and gotchas inline. Invoke when a release-handoff mail names a target repo, target SHA, and release shape.
---

# Release execution chain

The complete release runbook. Discipline + executable mechanics in
one place. No "see architecture.md for the gate" hand-waves — every
command, every env var, every gotcha is inline.

## Run from MAIN, not a worktree

For both aweb and ac, run from the actual main checkout. Worktrees
cause env-file gaps (`.env.production` doesn't follow), break
`uv sync` against the right `.venv`, and break Playwright installs
(Chromium lives per-checkout). Worktree for code work is fine;
worktree for releases is not. Lighter alternative for a shared
checkout with a peer: `git stash push -m "non-release"` → release
work → `git stash pop`.

## Trigger

A release-handoff mail (subject contains `release-handoff`,
`Bless-and-run`, or `release:`) naming: target repo, expected
SHA of clean main, release-notes draft, what migrations / API
contract changes / aweb-pin bumps are in scope.

Until that mail lands, no candidate exists. Do NOT self-spawn a
release on a bump commit found sitting on main.

## Pre-flight (every release, before anything)

```sh
# In the target repo (aweb or ac):
git pull
git status                    # must be clean — no uncommitted bleed-in
git rev-parse HEAD            # confirm matches the SHA in handoff mail
git log --oneline -5          # sanity-check bump-commit IS HEAD, not stale
aw whoami                     # confirm identity is what you expect

# If migrations are in scope:
git log --diff-filter=A --name-only <prev-tag>..HEAD -- "**/migrations/**"
# Output must exactly match the migration set named in handoff mail
```

If any check fails: stop and ask. Never gate against a different
commit than what was reviewed.

---

## PHASE 1 — aweb cut (when in scope)

### When phase 1 runs

The cross-repo dependency: aweb server bump usually drags ac. If
the release-handoff mail names an aweb pin bump in ac, phase 1
runs first; ac waits for the PyPI publish.

### aweb gate

```sh
cd ~/prj/awebai/aweb     # actual checkout, not a worktree
make ship                # ~7 min
```

`make ship` is the canonical pre-tag gate. Composes
`release-all-check` + `release-awid-check`. Internally chains:
`test` (test-server + test-awid + test-cli + test-channel) +
`release-server-check` + `release-channel-check` +
`release-awid-check` + `test-e2e`.

Does NOT push. Prints `Ready for tag-push` at the end.

Never substitute `make test` alone — banked from 1.18.3–1.18.6
where `make test` passed but downstream build failed in CI.

### aweb tag + push (per-tag, never batched)

```sh
# Server cut (move only what's in scope):
make release-server-tag   # creates server-vX.Y.Z, enforces tag == pyproject
make release-server-push  # pushes ONE tag

# Same per-component pattern for aw / awid / channel:
make release-cli-tag      && make release-cli-push
make release-awid-check   && make release-awid-tag && make release-awid-push
make release-awid-pypi-tag && make release-awid-pypi-push
make release-channel-check && make release-channel-tag && make release-channel-push
```

Always one push per tag, sequentially. Batched same-commit tag
pushes coalesce on GitHub and silently skip GHA fires
(banked: 1.18.0 ghost-tag, all 4 GHA publish workflows silently
no-fired).

### Watch GHA fire WITHIN 30 seconds

```sh
gh run list --repo awebai/aweb --workflow "Server Release (PyPI)" --limit 5
gh run watch <run-id> --exit-status
```

If no workflow appears within 30s of `git push`: suspect
batched-coalesce even if pushed sequentially. Push the tag
again (idempotent at the registry; GHA will re-fire on the
second push event).

### Verify PyPI / npm publication

```sh
# PyPI (server, awid-service):
curl -sS https://pypi.org/pypi/aweb/<VERSION>/json | python3 -c "import sys,json; print(json.load(sys.stdin)['info']['version'])"

# npm (channel, @awebai/aw):
npm view @awebai/claude-channel version
npm view @awebai/aw version

# GitHub Releases (aw goreleaser):
gh release view aw-v<VERSION> --repo awebai/aw
```

Capture the GHA run URL in local notes BEFORE the next step.
Tabs close; the URL goes into the verified-live mail.

---

## PHASE 2 — ac cut

### Pre-bump preparation (after aweb is on PyPI)

```sh
cd ~/prj/awebai/ac     # actual checkout, not a worktree
git pull
git status             # clean

# Bump version manually in backend/pyproject.toml:
#   version = "X.Y.Z" (current + patch, e.g. 0.5.74 → 0.5.75)
#   aweb pin: aweb>=<new-aweb-version> (if aweb moved)

# Refresh lock against new PyPI:
cd backend
uv lock --refresh-package aweb    # updates uv.lock
uv sync --refresh                 # actually resolves .venv to new aweb
cd ..

# Commit the bump:
git add backend/pyproject.toml backend/uv.lock
git commit -m "release: vX.Y.Z (aweb pin to A.B.C)"
git push origin main
```

`uv lock --refresh-package` updates the file; `uv sync --refresh`
actually resolves `.venv` to use the new pin. Skipping sync
means `check_release_model` passes but the gate runs against
stale `.venv` — banked PyPI cache-lag class.

### Install Playwright BEFORE running tests

```sh
cd ~/prj/awebai/ac/backend
uv run playwright install chromium
cd ..
```

`cloud-user-journey` Phase C runs `playwright install chromium`
mid-run. Non-interactive sessions hang at the install prompt.
Pre-install once per checkout/env to skip the hang.

### ac gate: what `make release-ready` actually composes

```sh
cd ~/prj/awebai/ac
make release-ready          # ~3-5 min
```

**Only the 4 verify-* targets:**
- `release-verify-remote` — remote state matches expectation
- `release-verify-model` — model-side verification
- `release-verify-migrations` — forward-only, ordered, checksum-clean
- `release-verify-migration-immutability` — pgdbm-normalized
  checksum of every migration on disk == `schema_migrations.checksum`

It does NOT run `test-backend`, `test-frontend`,
`test-two-service`, or `test-cloud-user-journeys`. Those run via
PR CI before merge to main. The release-time gate is
**deploy-safety**, not test-correctness. Main is presumed clean.

### Compat — run when scope requires

```sh
make test-cloud-user-journeys-compat   # ~58s isolated
```

**Run compat when ANY apply:**
- `aweb` pin in `backend/pyproject.toml` bumped
- New SQL migration touches table read/written by aweb-server endpoints
- API endpoint contract change (response shape, required fields, status)
- Middleware / request-routing / header-validation / path-routing change
- Auth / cert / identity flow change

**Skip compat only when BOTH apply:**
- Strictly internal changes (frontend layout/copy, internal refactor, no migration, no API change)
- AND `aweb` pin unchanged

When in doubt: run. 58s is cheap insurance against installed-aw
regression.

### ac tag + push

```sh
git tag -a v<X.Y.Z> -m "release: v<X.Y.Z>, <one-line summary>"
git push origin v<X.Y.Z>
```

Watch GHA Cloud CI/CD within 30s:

```sh
gh run list --repo awebai/ac --limit 5
gh run watch <run-id> --exit-status
```

**The ac v* tag GHA only builds + pushes the image to GHCR.
It runs NO tests, NO e2e.** Local `make release-ready` from main
is THE quality bar at release time.

---

## DEPLOY

### Whether deploy is auto-pull or manual: VERIFY LIVE

```sh
# After GHA green + GHCR image is ready, watch /health for 2 min:
for i in {1..24}; do
  echo "$(date -u +%H:%M:%S) $(curl -sS https://app.aweb.ai/health | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('release_tag','?'), (d.get('git_sha','?') or '?')[:8])")"
  sleep 5
done
```

Outcomes:
- **release_tag flips to new vX.Y.Z within 2 min**: auto-deploy is
  configured (Render auto-pulls from GHCR on new tag matching the
  pin). Note for next time.
- **release_tag stuck on prior version after 2 min**: manual deploy
  needed. Render dashboard → ac service → Settings → Image URL →
  change `ghcr.io/awebai/aweb-cloud:<old>` → `:<new>` → Save.
  Or signal Juan: "ac v<X.Y.Z> image at GHCR — needs Image URL bump."

Don't assume which model is configured — the live behavior is the
authoritative answer. Banked from a2a-gw-v1.26.19 incident
2026-06-13: Manual Deploy redeploys the existing pin, doesn't pick
up new tags.

---

## MIGRATIONS

### `.env.production` lives in the instance home, NOT repo root

Path is `agents/instances/<instance-name>/.env.production`. For
hestia: `agents/hestia/.env.production` is NOT where it lives — it
lives at `~/prj/awebai/ac/agents/instances/ac-operations/.env.production`
(per-team-instance). When invoking `make prod-migrate-direct` from
ac root, pass:

```sh
make prod-migrate-direct PROD_ENV_FILE=agents/instances/<instance-name>/.env.production
```

The Makefile target does `cd backend && PROD_ENV_FILE="../$(PROD_ENV_FILE)"`,
so the path is taken relative to ac root.

### Migrations do NOT auto-apply on Render deploy (#109/#110/#284)

Apply manually after `/health` flips to the new release_tag.

### Pre-flight row-count check (for constraint-adding migrations)

```sh
PROD_ENV=agents/instances/<instance-name>/.env.production
DATABASE_URL=$(grep -E '^DATABASE_URL=' "$PROD_ENV" | sed -E 's/^DATABASE_URL="?(.*)"?$/\1/')

# For each table the migration adds constraints to:
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM <schema>.<table>;"

# For each new CHECK / FK constraint, count rows that would VIOLATE it:
psql "$DATABASE_URL" -c "SELECT COUNT(*) AS would_fail FROM <schema>.<table> WHERE <constraint-violation-predicate>;"
```

Non-zero `would_fail` → migration will abort at ALTER TABLE.
Flag the failure shape to the code owner before running. Options:
(a) file a fix-up migration that data-repairs first; (b) accept
the abort and roll back. Owner's call.

### Apply

```sh
cd ~/prj/awebai/ac
make prod-migrate-direct PROD_ENV_FILE=agents/instances/<instance-name>/.env.production
```

Target wraps: `cd backend && PROD_ENV_FILE="../<file>" uv run python -m aweb_cloud.cli migrate`.
Idempotent. Applies only pending. Runs both `aweb_cloud` and
`aweb` schema chains.

### Verify applied

```sh
DATABASE_URL=$(grep -E '^DATABASE_URL=' agents/instances/<instance-name>/.env.production | sed -E 's/^DATABASE_URL="?(.*)"?$/\1/')

# Schema-migrations rows:
psql "$DATABASE_URL" -c "
SELECT filename, applied_at, applied_by, execution_time_ms
FROM aweb_cloud.schema_migrations
WHERE filename ~ '^00[6-9]_|^010_'   -- adjust to scope
ORDER BY filename;
"

# Object existence:
psql "$DATABASE_URL" -c "SELECT to_regclass('aweb_cloud.<new_table>');"

# For each new column, CONFIRM queryable (to_regclass passes on partial apply):
psql "$DATABASE_URL" -c "SELECT 1 FROM aweb_cloud.<table> WHERE <new_column> IS NOT NULL LIMIT 1;"

# For each new constraint:
psql "$DATABASE_URL" -c "
SELECT conname FROM pg_constraint
WHERE connamespace = 'aweb_cloud'::regnamespace
  AND conname IN ('<expected-constraint-names>');
"
```

### Smoke against the migrated surface

```sh
cd backend
uv run python -m aweb_cloud.cli decomposition verify-fk-backfill --json
# Expect: gate_failures=0 AND fail_closed_failures=0
```

If either is non-zero: do NOT post verified-live. Flag the shape
to the code owner.

### Emergency metadata repair

If a migration was applied out-of-band (rare; the only known
case is the `_assert_coordination_schema_ready` startup-fail
loop), the `schema_migrations.checksum` MUST be the
**pgdbm-normalized** checksum, NOT a raw `sha256sum`. See the
sibling skill `sop-pgdbm-migration-apply` for the recipe.

---

## VERIFIED-LIVE MAIL

```
To: <coordinators>, <human-owner>
Subject: verified-live: <repo> <version> — <one-line summary>
Body:
  What it fixes: <scope>
  What it does NOT fix: <adjacent issues; "none" only if explicitly true>
  Evidence:
    - <aweb PyPI publication>: <URL or curl output>
    - <ac build>: paste /health JSON (release_tag, git_sha, aweb_version)
    - <migrations>: paste schema_migrations rows
    - <FK-backfill>: gate_failures=0, fail_closed_failures=0
  Live check:
    - /health: <release_tag value>
    - Smoke probe: <command + expected response>
  GHA runs:
    - aweb: <URL>
    - ac:   <URL>
```

**Four-point check** (constitution): (1) what fixed, (2) what NOT
fixed, (3) evidence, (4) live check. Item 2 is the recurring slip
(Sofia caught its absence on v0.5.47). Even when nothing nearby is
broken, write "no adjacent surface changes; no nearby issues to
disclaim" — explicit absence is the verified-live framing.

Keep body under 2KB. Larger bodies can trip edge HTTP 403 blocks.

---

## Gate-failure hand-back to code-owner

When the gate goes red and the failure is code-side (not gate-
harness drift, not flake):

```sh
aw mail send --to <code-owner> \
  --subject "gate-failure: <gate-name> on <repo> at <SHA>" \
  --body "$(cat <<EOF
Gate: <make target>
Repo + SHA: <repo> <SHA>
Failure shape: <test name / step name>
Output (last ~40 lines, paste VERBATIM):
<...>

My read: <what surface looks broken; what I'd guess is the cause>
Next: holding the release; re-run when you signal.
EOF
)"
```

The hand-back IS the right move. Per constitution: do NOT push
back on red as flake/known/baseline-accept. Red gate = no ship.

---

## Post-step hygiene

After verified-live mail lands:

```sh
# Update state:
cd ~/prj/awebai/ai.aweb/agents/<your-name>   # for hestia: /agents/hestia
# Edit handoff.md (live-matrix line + current focus)
# Append dated entry to logbook.md (release shape + evidence + GHA URLs)
# Edit ../../status/operations.md current-snapshot

# Commit + push:
git add handoff.md logbook.md ../../status/operations.md
git commit -m "<your-name>: <release> verified-live"
git push origin main
```

## What's NOT in this skill (and where to find it)

- Destructive cutover (DROP SCHEMA, restore, fresh consolidated 001):
  see `sop-destructive-cutover`. Juan-direct-authorization required.
- Standalone migration emergency unblock (Render startup-fail loop):
  see `sop-pgdbm-migration-apply`. Use when AC ships a new migration
  but Render didn't apply it on container start.
- Identity-discipline foot-guns: see `legacy.md` identity-discipline.
- Render Static Site stale-file retention: see `legacy.md`
  infra-render.
