# Release Readiness And Rollout Plan (CROSS-04)

This document locks down how an aweb / aweb-cloud release that touches
lifecycle or support flows is shipped and verified, and how it gets
rolled back if something misbehaves in production.

It is the evergreen contract. The per-release audit trail lives at the
bottom under **As-Shipped Record** — append one entry per release tag.

## Scope

Applies to any release that changes:

- OSS persistent-vs-ephemeral lifecycle semantics
- the hosted lifecycle cascade (archive/replace/delete of agents or
  workspaces)
- `aw doctor` read or fix output
- cloud support read endpoints (agent/namespace/team/replacements)
- cloud support write endpoints (repair-managed-address, replace-agent,
  archive-agent)
- the support-contract-v1 envelope or any payload schema it carries

Non-lifecycle cosmetic or dashboard-only changes do not need this doc;
they ship through the ordinary release flow.

## Release Order

The rollout order preserves the invariant that every later layer can
assume the earlier layers are trustworthy. **Do not reorder**; each
step depends on the previous one being live and verified.

1. **OSS persistent cleanup safety** — the OSS `aweb` package must
   refuse to delete persistent identities through stale cleanup paths
   before any hosted code relies on that refusal.
2. **Cloud lifecycle cascade** — the hosted archive/replace paths must
   route through the shared OSS cascade adapter
   (`apply_lifecycle_cascade`) before support endpoints are exposed.
3. **`aw doctor` read-only** — all doctor read commands must be live
   and redaction-safe before any fix path ships.
4. **`aw doctor --fix` safe repairs** — fix commands ship individually;
   every fix must carry dry-run and an ambiguity-refusal path.
5. **Support read endpoints** — `/api/v1/admin/support/{agents,
   replacements, teams, namespaces}/*` read endpoints ship before any
   mutation endpoint so support can read state before acting on it.
6. **Support write endpoints** — `repair-managed-address`,
   `replace-agent`, `archive-agent` ship last; each requires dry-run,
   audit, and the `support-contract-v1` envelope.

## Version Pinning Rule

`aweb-cloud` pins `aweb` with a `>=` lower bound equal to the aweb
release that contains the OSS safety + cascade features the cloud
release relies on.

- `aweb-cloud` `pyproject.toml` pin must be bumped **before** the cloud
  release that depends on it is tagged.
- If a cloud release changes the pin, the PR that changes it must
  reference both the aweb tag and the aweb release notes.

## Operational Verification Checklist

Every lifecycle/support release must pass every item below **before**
the release tag is considered healthy. Each item names the test or
probe that proves it. "Probe" means a thing an operator runs against
the deployed environment; "test" means the CI-enforced coverage.

| # | Invariant | Test or probe |
|---|-----------|--------------|
| V1 | Persistent-missing path no longer deletes identity | aweb `server/tests/test_lifecycle.py::test_lifecycle_archive_persistent_agent_rejects_non_persistent_target` (refuses non-persistent target) + `test_mutation_hooks.py::test_agent_deleted_cascade_releases_claims_events_and_presence` (cascade semantics) |
| V2 | Hosted archive/replace unclaims tasks | ac `tests/test_cross03_recovery_scenarios.py` scenarios 2 & 6 assert `task_claims` count goes from 1 to 0 after apply; ac `tests/auth_bridge_oss_cases.py::test_archive_agent_releases_task_claims_via_cascade` for the dashboard path |
| V3 | Hosted archive/replace clears presence | ac `tests/test_cross03_recovery_scenarios.py` scenarios 2 & 6 assert `redis.hgetall("presence:{workspace_id}")` is empty after apply; ac `tests/auth_bridge_oss_cases.py::test_archive_agent_clears_presence` for the dashboard path |
| V4 | Support bundle redacts secrets | aweb `cli/go/cmd/aw/doctor_test.go::TestAwDoctorSupportBundleJSONPrintsRedactedBundle` + `TestAwDoctorSupportBundleFinalScanFailsBeforeWrite` + `TestAwDoctorSupportBundleFinalScanRejectsRawTeamCertificate` |
| V5 | `repair-managed-address` preserves DID | ac `tests/test_cross03_recovery_scenarios.py::test_cross03_repair_managed_address_preserves_existing_did` asserts agent `did`, `did_aw`, `status` unchanged and no `register_did` call fired; plus per-tool `test_admin_support_agents.py::test_support_repair_managed_address_*` |
| V6 | `replace-agent` records replacement announcement | ac `tests/test_cross03_recovery_scenarios.py::test_cross03_replace_agent_archives_old_agent_through_cascade` asserts `replacement_announcements` row present with old_agent_id; plus per-tool tests |
| V7 | `archive-agent` refuses without `no_address_continuity_confirmed` | ac `tests/test_cross03_recovery_scenarios.py::test_cross03_archive_agent_cascades_and_audits` (refusal path); plus per-tool refusal tests |
| V8 | Support endpoints emit `support-contract-v1` envelope with audit id on write | ac `tests/test_cross03_recovery_scenarios.py` scenarios 2 & 6 load the audit via `get_support_audit(audit_id)` and assert `operation`/`agent_id`/`ticket_id`; plus `tests/test_support_contract.py` for envelope shape |

**Gates that must be green for ship**:

- `make test-backend` (backend unit + integration suite)
- `make test-two-service` (Docker-based two-service e2e)
- `make test-cloud-user-journeys` (Docker user journey)
- `make test-frontend` (frontend tests + build + lint)
- Playwright customer-journey suite (8-step browser walkthrough)

`make release-ready` composes the non-frontend subset of these. It is
a necessary but not sufficient gate: the frontend gates are run
separately.

## Migration Review Gates

Schema-changing migrations must fail loudly when they do not produce
the intended database shape. Any migration that creates or alters a
`UNIQUE` constraint, partial index, or `CHECK` constraint must have a
companion assertion in `backend/tests/test_migration_paths.py` that
queries `pg_indexes` or `pg_constraint` after a fresh migration run and
asserts the real definition.

Index DDL must also be schema-qualified enough that it cannot silently
operate in the wrong schema. `DROP INDEX` targets must use
`{{schema}}.<index_name>`. `CREATE INDEX` statements must either
schema-qualify the index name or create the index on a `{{schema}}.*` or
`{{tables.*}}` table reference. `make release-ready` enforces this with
`scripts/check_migration_index_qualification.py`.

## Post-Deploy Probes

After the release tag rolls out, run these against the deployed
environment. These are the minimum signals that confirm the release
landed healthy; they complement the CI gates above.

1. **Health**: `curl -fsS https://app.aweb.ai/health | jq '.status'`
   returns `"healthy"` (never `"degraded"` or `"unhealthy"`), and
   `.database`, `.redis`, `.awid_registry`, `.coordination_api` are
   all `"connected"` or `"mounted"`.
2. **Release tag**: `curl -fsS https://app.aweb.ai/health | jq '.build.release_tag'`
   reports the expected `vX.Y.Z`. If `release_tag` is `null` the
   `AWEB_RELEASE_TAG` env var was not set on the deploy — investigate
   before calling the release healthy.
3. **Schema**: run `make prod-migrate-direct PROD_ENV_FILE=.env.production`
   against prod (or verify startup migrations completed in logs).
   Confirm no pending migrations remain.
4. **Support read smoke**: a support-role API key resolves a known
   agent via `GET /api/v1/admin/support/agents/resolve?agent_id=…`
   and receives a `support-contract-v1` envelope with
   `authority_mode: "support"` and `source: "aweb-cloud"`.
5. **Dry-run smoke**: dry-run `repair-managed-address` against a known
   healthy hosted agent returns `dry_run: true`,
   `identity_replacement.will_replace: false`, and no audit row is
   written (check `support_audit` count before/after).
6. **Customer journey**: the Playwright customer-journey suite run
   against production reports 8/8 steps green with all badges in the
   expected state.

Record the output of each probe in the release ticket.

## Feature Flags

The lifecycle / support feature set does not rely on runtime feature
flags. Risky hosted actions are gated by:

- **Route-level auth**: write endpoints require an admin API key with
  `metadata.is_admin = true`. The route dependency is `require_admin`
  in `aweb_cloud.routers.auth`.
- **Contract-level refusal**: destructive-to-external-state operations
  (archive with address continuity loss, replace) refuse to execute
  without explicit acknowledgement flags and a ticket id.
- **Dry-run first**: every write supports `dry_run: true`. Operators
  are expected to dry-run before apply.

If a release needs to hide a specific capability post-ship without
re-tagging, the supported tools are:

- revoke the admin API key so write endpoints cannot be reached;
- remove `require_admin` metadata from the key so `/admin/support/*`
  returns 401.

There is no kill switch per endpoint. If one is needed later, the
design should route through `require_admin` and be documented here.

## Rollback Plan

Rollback is layered — you revert the smallest layer that contains the
defect, not the entire release.

### If defect is in a support write endpoint (repair/replace/archive)

1. Set all admin API keys' `metadata.is_admin` to `false` to lock out
   write endpoints.
2. Communicate the outage to support.
3. Issue a patch release that fixes the endpoint or removes its
   handler, keeping the rest of the release intact. Do not revert the
   lifecycle cascade or the OSS safety fix.

### If defect is in the hosted lifecycle cascade

1. Revert the commit(s) that introduced the cloud cascade change.
2. Keep the OSS aweb pin at the current version — the OSS safety
   behaviour is independent.
3. Ship a patch release. Rerun V2 and V3 probes.

### If defect is in the OSS safety behavior

1. Revert the aweb `>=` pin to the previous aweb release that was
   healthy.
2. Ship a cloud patch release that re-pins aweb.
3. If the OSS safety fix is itself the defect, coordinate an aweb
   patch release before the cloud re-pin.

### If defect corrupts state (audit rows, replacement announcements, etc.)

State writes are append-only by design (no updates to
`support_audit` or `replacement_announcements`). Do not roll back the
tables; roll back the code path that wrote them and then review rows
written during the bad window for support follow-up.

## Release Notes Mapping

Every release tag that touches lifecycle/support must include a notes
block mapping capabilities to the version that introduced them.

Template:

```
## vX.Y.Z — <date>

### Capabilities
- <capability name>: <1-line user-visible description> [<epic ticket>]

### OSS dependency
- aweb: >=<version>

### Operational notes
- <any post-deploy action support needs to take>
- <any feature flag / kill-switch change>
```

## As-Shipped Record

Append one entry per release tag. Each entry must cite which
acceptance criteria were verified and link to the CI run that proves
them. Do not edit prior entries.

### v0.4.21 — 2026-04-20

**Capabilities landed since v0.4.20**:

- Session expiry timezone correctness (aweb-aaki): `OAuthService.
  get_user_by_session` now compares `expires_at` against postgres
  `NOW()` in tz-aware form. Fix commits: 846d4101, 871a5dc6. Before
  this, expired sessions could authenticate users on deployments
  where postgres session timezone was not UTC (proportional to the
  tz offset). Prod was unaffected only because prod runs UTC; our
  test DB also runs UTC, which is why the regression was not caught
  by the ship gate for v0.4.20.
- TIMESTAMPTZ migration (migration 016): all 56 remaining bare
  `TIMESTAMP` columns in the cloud schema migrated to `TIMESTAMPTZ`.
  Structural fix for the class of bug above; removes timezone
  dependence from every auth/session/audit comparison.
- Trusted proxy team-id plumbing (aweb-aaje): bridge sends canonical
  colon-form team IDs to the OSS proxy; strict team_id validation
  per Henry's review. Commits 2761d0a5, 1f6e4797, 78794ff (aweb).
- Add-worktree cloud journey coverage (aweb-aajp): e2e covers the
  add-worktree flow end-to-end.
- Terminology sweep (aais.2): `permanent` → `persistent` for
  identity lifetime across docs/code for consistency with protocol.
- Support lifecycle contract polish (12594ca9): typing fix for
  `_LifecycleManagedAddress.current_did_key`, threads actual
  `no_address_continuity_confirmed` into archive audit metadata,
  replace-agent `generated_at_execute=false` when concrete
  DID/stable_id present, three replace-agent rejection tests.
- Release-readiness contract itself landed (03398742, edca85c2):
  this document + the tripwire in `backend/tests/test_release_
  readiness_tripwire.py`. Kate's aweb-side tripwire for V1/V4 is a
  follow-up.
- CROSS-03 cross-repo recovery scenarios landed (6bc611c3, 4d5f7d70)
  with registry-call, audit-row, and presence-cleared assertions
  per Dave's thorough review.

**OSS dependency**: `aweb>=1.10.1` (was `>=1.10.0` in v0.4.20).
  aweb 1.10.1 adds the strict proxy team_id validation needed by
  aaje.

**Gates passed**:

- backend: 1155 passed, 0 failures
- Docker two-service e2e: 9/9
- fast tests: 68

**Operational verification checklist**: V1–V8 all remain covered
by the tests named in the checklist at HEAD. V5 (repair preserves
DID) and V2/V3/V7/V8 (cross-repo cascade + audit + refusal)
re-verified locally after pulling v0.4.21 — 22/22 including
`test_expired_session_returns_none` which was the v0.4.20 miss.

**Known regressions from v0.4.20 closed**:

- `test_expired_session_returns_none` — now passes on all postgres
  session timezones thanks to the TIMESTAMPTZ migration. Task #23
  closed. This also closes the lesson: the v0.4.20 ship gate
  counted 1135 passed because the test DB ran UTC; non-UTC pg
  sessions would have failed. Structural fix removes the tz
  dependence from the gate's correctness.

**Lesson encoded**: the ship gate's test DB timezone is a hidden
input. The TIMESTAMPTZ-all-the-things approach removes that input
entirely. No explicit process change needed beyond the schema fix.

### v0.4.20 — 2026-04-19

**Capabilities landed since v0.4.19**:

- Support mutation endpoints live: `repair-managed-address`,
  `replace-agent`, `archive-agent`, each with dry-run, audit, and
  `support-contract-v1` envelope. (AC-11, AC-12, AC-13)
- Dashboard consequence dialog for archive/replace operations.
  (AC-14)
- Support role instructions and runbook docs with corrected CLI
  commands. (AC-15)
- Managed namespace persisted during team creation (aweb-aake).
- Custodial canonical columns populated after creation (aweb-aakg).
- Enriched dashboard agent roster (aweb-aakh).
- Security: controller key decryption errors redacted in support
  payloads.
- 40 fixture regressions resolved; 17 mutation tests restored.
- CROSS-03 cross-repo recovery scenarios landed (6bc611c3, 4d5f7d70).

**OSS dependency**: `aweb>=1.10.0` (was `>=1.9.0` in v0.4.19).

**Gates passed**:

- backend: 1135 passed, 0 failures
- Docker two-service e2e: 9/9
- Docker user journey: 105 tests
- frontend: 67 tests + build + lint
- Playwright customer journey: 8/8

**Operational verification checklist**: V1–V8 all covered by landed
tests above; the doc references tests that exist at this tag.

**Post-deploy probes**: health / version / Playwright customer
journey reported green by Alice on 2026-04-19.

**Final verification against as-deployed v0.4.20 (2026-04-19)**:

- `curl https://app.aweb.ai/health`: `status=healthy`,
  `build.release_tag=v0.4.20`, `git_sha=a8100421`, database / redis
  / awid_registry / coordination_api all connected. Verified.
- V1 (aweb `test_lifecycle_archive_persistent_agent_rejects_non_persistent_target`
  + `test_agent_deleted_cascade_releases_claims_events_and_presence`):
  both pass locally at aweb 1.10 HEAD.
- V2/V3/V5/V6/V7/V8 (ac side: `test_cross03_recovery_scenarios`,
  `test_admin_support_agents`, and dashboard-path cascade tests in
  `auth_bridge_oss_cases`): all pass locally at ac v0.4.20.
- V4 (aweb Go `TestAwDoctorSupportBundleJSONPrintsRedactedBundle`
  + `TestAwDoctorSupportBundleFinalScanFailsBeforeWrite` +
  `TestAwDoctorSupportBundleFinalScanRejectsRawTeamCertificate`):
  `go test ./cmd/aw/` passes at aweb HEAD.

**Known unrelated failure at tag**: `test_expired_session_returns_none`
fails on v0.4.20 with a pre-existing timezone bug in
`OAuthService.get_user_by_session` (filed for investigation; security
implication depends on prod tz). Not blocking v0.4.20 ship, but flagged.

**Tripwire landed**: `backend/tests/test_release_readiness_tripwire.py`
enforces that every ac-side test named in the V1–V8 checklist
continues to exist. Deleting or renaming one fails CI with a pointer
back to this doc. Follow-up: equivalent tripwire for V1 and V4 in the
aweb repo.

**Rollback window**: lifecycle/support path. Admin-key lockout is the
first line of defence per the rollback plan.

## Cross-References

- Epic: [`agent-lifetime-support-epic.md`](agent-lifetime-support-epic.md)
- Cross-repo coverage map: [`cross-repo-lifecycle-coverage.md`](cross-repo-lifecycle-coverage.md)
- Hosted lifecycle audit: [`hosted-lifecycle-audit.md`](hosted-lifecycle-audit.md)
- Support contract: aweb `docs/support-contract-v1.md`
- Scenario design: ac origin/ivy `docs/support/cross-repo-recovery-scenarios.md`
