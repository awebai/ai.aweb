# Hosted Lifecycle Mutation Audit (AC-01)

**Status (2026-04-19)**: AC-02 (`2169640f`) resolved every bypass
exhibit below. EX-1/2 wrapper was renamed from `_archive_agent_tx`
to `_archive_agent_via_cascade` in ac `160b5604` and now funnels
through `apply_lifecycle_cascade`. This document is kept as
historical audit evidence; read it against the _via_cascade name
when cross-referencing current code.

Purpose: inventory every ac code path that mutates aweb coordination
state, identify where those mutations bypass OSS coordination cleanup
semantics, and surface the work AC-02 must do to route them through
the shared lifecycle cascade from AWEB-04 (aweb `6ac5e90`).

Scope (per
[`agent-lifetime-support-epic.md`](agent-lifetime-support-epic.md)
§AC-01):

- `{{tables.agents}}` (aweb schema)
- `{{tables.aweb.workspaces}}` / `{{tables.workspaces}}`
- task claims, locks, presence
- `{{tables.server.api_keys}}`
- hosted custody material (`{{tables.cloud_custodial_keys}}`, cert material)
- `{{tables.replacement_announcements}}`

Lifecycle operations covered: **archive**, **replace**, **delete**,
**retire**, **cleanup**. Bootstrap/create-only paths are listed in a
secondary table because they produce the state that lifecycle
operations must later clean, but they are not themselves cascade
sites.

## Security invariant this audit protects

An archived or replaced agent MUST NOT retain active coordination
state: task claims, locks, presence entries, waiting chat sessions,
inbound mail routing, or work-discovery reservations. Any code path
that soft-deletes / archives an aweb-schema row WITHOUT running the
coordination cascade violates this invariant.

---

## Primary exhibits (archive / replace paths)

### EX-1. `routers/agent_lifecycle.py::_archive_agent_tx` (lines 418–468)

**Called from**: `archive_agent` route handler, `replace_agent`
(retires the old agent before creating the replacement), and
embedded cascades.

**Actor type**: support/admin user, or team controller acting on a
specific agent.

**Authority checked**: `assert_team_access` upstream; namespace
controller key loaded for each managed address via `aajw.12`.

**Current mutations** (all direct SQL):

- `UPDATE {{tables.agents}} SET signing_key_enc = NULL, status = 'archived', deleted_at = NOW() WHERE agent_id = $1` — clears custody material and soft-deletes the agent row.
- `UPDATE {{tables.server.api_keys}} SET is_active = FALSE WHERE team_id = $2 AND metadata->>'workspace_id' = $1::text` — deactivates cloud API keys for the archived workspace.
- `UPDATE {{tables.aweb.workspaces}} SET deleted_at = NOW(), updated_at = NOW() WHERE workspace_id = $1` — soft-deletes the aweb workspace row.
- `delete_cloud_agent_certificate(tx, workspace_id=workspace_id)` — cloud-schema helper, removes cert record.
- `delete_cloud_custodial_key(tx, workspace_id=workspace_id)` — removes hosted custody key.

**Missing cascade side effects** (coordination invariants
violated — verify against `lifecycle_cascade` from
aweb `6ac5e90`):

- **Task claims not released.** The archived workspace may hold
  `task_claims` rows. No `DELETE FROM {{tables.task_claims}} WHERE
  workspace_id = $1` or equivalent call to
  `lifecycle_cascade.release_claims()`.
- **Locks not freed.** `{{tables.locks}}` rows held by the workspace
  remain active.
- **Presence not cleared.** `{{tables.workspace_presence}}` /
  Redis presence keys remain.
- **Waiting chat state orphaned.** The archived agent may be a
  party to an in-flight chat conversation (`chat_waiting` state);
  no close / NAK of those sessions.
- **Inbound mail routing.** Messages addressed to the archived
  agent's did_aw continue to be deliverable; no policy update.
- **Work-discovery reservations.** No cleanup of the agent's
  reservations in work/discovery tables.

**Classification**: **BYPASS**. Direct cross-schema writes into
aweb with zero invocation of the OSS cascade.

**Fix (AC-02)**:

- Replace the three direct `UPDATE`/`UPDATE`/`UPDATE` statements
  above with a single call to `lifecycle_cascade.archive(
  actor_identity, actor_type, agent_id, workspace_ids, operation,
  reason, dry_run, authority)`. The cascade returns planned/
  completed mutations including task unclaim counts, presence
  cleanup booleans, event ids, workspace lifecycle changes — all of
  which the cloud side can surface in dry-run output and write to
  the support audit (AC-04).
- Keep `delete_cloud_agent_certificate` and
  `delete_cloud_custodial_key` in the cloud sequence (cloud-owned
  concerns), but execute them AFTER the cascade completes so the
  cascade observes a valid identity while running its checks.
- Keep the multi-address iteration and `_rollback_reassigned_addresses`
  from `aajw.12` — that's cloud-owned concern (awid registry
  authority).

**Regression test to add** (initial FAIL before AC-02): in
`backend/tests/test_agent_lifecycle.py`, add
`test_archive_agent_releases_task_claims_via_cascade` that creates
a workspace, claims a task, archives the agent, and asserts the
claim is released and the release event was emitted. This will
fail against the current direct-SQL path and pass after AC-02
routes through the cascade.

### EX-2. `routers/agent_lifecycle.py::replace_agent` and new-agent INSERTs (lines 554, 582, 623, 675)

**Called from**: dashboard Replace flow, support replace-agent
endpoint (AC-12 will formalize this).

**Current behaviour**: calls `_archive_agent_tx` on the old agent
(inheriting EX-1's bypass), then:

- `INSERT INTO {{tables.agents}} (...)` — creates the replacement
  agent row.
- `INSERT INTO {{tables.aweb.workspaces}} (...)` — creates the
  replacement workspace.
- `INSERT INTO {{tables.server.api_keys}} (...)` — mints a new API
  key.
- Later: `UPDATE {{tables.agents}}` for identity publishing.
- `INSERT INTO {{tables.replacement_announcements}}` per managed
  address (from `aajw.12`).

**Missing cascade side effects**: same as EX-1 for the archive
side. The INSERT side doesn't itself bypass cascade (it's creation,
not lifecycle cleanup), but:

- No audit record (AC-04 will add this).
- Dry-run not supported (AC-12 will add this).
- Replacement announcement is recorded but not linked to an audit
  reason/ticket (AC-04 will add the link).

**Classification**: **BYPASS** (inherits from EX-1) + incomplete.

**Fix (AC-02 for archive side, AC-12 for replace orchestration)**:
same cascade call for the archive half. INSERT side stays cloud-
owned, but gains audit (AC-04) and dry-run (AC-12).

**Regression test**:
`test_replace_agent_releases_old_claims_and_records_audit` — assert
old workspace claims released, replacement announcement written,
audit record with actor+reason+old/new state.

### EX-3. `routers/teams.py` workspace-scoped archive (lines 247–270, 778–801)

**Called from**: two team-level archive sites (I haven't
disambiguated without reading — both blocks do
`UPDATE {{tables.aweb.workspaces}}` + `DELETE FROM {{tables.task_claims}}`).

**Current behaviour**: direct SQL soft-delete of the workspace row
AND a direct `DELETE FROM task_claims`. This is the only place in
the audit that explicitly releases task_claims — but it does it
bypassing any event emission or presence cleanup the cascade would
run.

**Classification**: **PARTIAL BYPASS**. Task claims released but no
cascade-level events emitted; locks, presence, chat state, and
work-discovery reservations still not touched.

**Fix (AC-02)**: replace the two-statement pattern with a cascade
call. The cascade's task-unclaim is equivalent SQL but emits the
proper events and handles the rest of the invariant state.

**Regression test**:
`test_team_archive_emits_cascade_events` asserting events table has
the expected unclaim events after team-level archive.

### EX-4. `embedded/workspaces.py::coordination_delete_workspace`

**Called from**: `routers/oss_workspaces.py` cloud overlay for hosted
workspace deletion.

**Finding**: this was a cloud-specific duplicate of the OSS lifecycle
primitive for stale ephemeral workspace deletion. It performed direct
`UPDATE {{tables.workspaces}}`, `DELETE FROM {{tables.task_claims}}`,
and `UPDATE {{tables.agents}}` mutations, then best-effort Redis
cleanup.

**Classification**: **DUPLICATE BYPASS, RESOLVED IN AC-02**.

**AC-02 action**: `coordination_delete_workspace` now keeps the cloud
access checks and stale-ephemeral preflight, then calls
`apply_lifecycle_cascade(operation="delete_ephemeral_workspace")`.
The OSS adapter owns the workspace soft-delete, task unclaim, agent
delete, reservation/chat/presence cleanup, and event emission.

### EX-5. `services/dashboard_identity.py` dashboard identity edits (lines 74, 174, 183)

**Called from**: dashboard routes for identity edit (name change,
reachability change, etc.).

**Current mutations**: `UPDATE {{tables.agents}}` (multiple sites) +
`UPDATE {{tables.workspaces}}`.

**Scope**: these look like edit-in-place, not archive/replace. If
the edits are strictly metadata (display name, reachability) with
no lifecycle implication, they are NOT bypass sites for AC-01's
archive/replace scope.

**Classification**: **OUT OF AC-01 SCOPE**. AC-02 verification found
the updates are dashboard identity creation/metadata repair and
failure rollback for a just-created dashboard identity. They do not
perform archive/replace/delete of an existing hosted agent. The
rollback remains local to the creation attempt and should be revisited
only if dashboard identity creation is later made user-visible as a
lifecycle operation.

---

## API-key lifecycle (auth paths)

### AK-1. `services/auth*.py` API key UPDATEs

`services/auth.py:135, 267`, `services/auth_password.py:487, 569,
640, 709` — API key mint / deactivate / rotate / revoke.

**Scope**: API key rows themselves, not agent lifecycle. Relevant
to archive/replace only insofar as EX-1 already deactivates API
keys via `is_active = FALSE`.

**Classification**: **OUT OF AC-01 SCOPE** for the bypass question.
However, **AC-05 (Normalize Hosted Custody/API-Key Cleanup
Reporting)** will consolidate reporting so that archive/replace
dry-runs can enumerate the API keys they are deactivating.

### AK-2. `embedded/auth.py:115, 158` — `UPDATE {{tables.api_keys}}`

**Called from**: embedded aweb server path for API-key state
transitions.

**Classification**: OUT OF SCOPE (aweb-owned path, not a cloud
bypass).

---

## Bootstrap / creation paths (for context only)

These are listed so AC-02 + AC-05 + AC-12/13 have a complete map
of where state is produced. They are NOT lifecycle-cleanup bypass
sites.

| Path | File:line | What it creates |
| --- | --- | --- |
| Workspace init | `services/workspace_init.py:145, 205` | workspace row update + insert |
| Workspace init | `services/identity_workspace.py:115, 137` | workspace row |
| Hosted init (API key) | `routers/init.py:769, 803` | agent update (address link) |
| Onboarding | `routers/onboarding.py:536` | agent update |
| Bootstrap | `embedded/bootstrap.py:122, 516, 560, 614, 650, 664` | workspace, agent, api_key, and deactivate |
| Team binding | `embedded/team_binding.py:156, 180, 233, 423` | agent/workspace creation |
| Team cert mint | `embedded/team_cert_mint.py:214` | agent (cert material) |
| Messaging | `routers/agent_messaging.py:103` | agent (last_seen / status touch) |

Archive/replace must cascade over all state these paths produce.
The cascade in AWEB-04 already owns the aweb-schema portion; cloud
must extend for custody/api_key (AC-05) and audit (AC-04).

---

## Background jobs

### BG-1. `jobs/retention.py::DELETE chat_messages` (lines 106, 183)

Scheduled retention sweep that deletes old chat messages. Scoped by
retention policy, not by lifecycle — an archived agent's messages
will be deleted by this job on the normal retention schedule.

**Classification**: OUT OF SCOPE for AC-01 bypass (not lifecycle-
triggered). No action.

---

## Summary table

| Exhibit | File | Category | Classification | AC-02 action |
| --- | --- | --- | --- | --- |
| EX-1 | `agent_lifecycle.py::_archive_agent_tx` | Archive | BYPASS | Route through `lifecycle_cascade.archive()` |
| EX-2 | `agent_lifecycle.py::replace_agent` | Replace | BYPASS (via EX-1) | Same fix as EX-1 for old-agent half |
| EX-3 | `teams.py` two sites | Team archive | PARTIAL BYPASS | Route through cascade for event emission |
| EX-4 | `embedded/workspaces.py::retire_workspace` | Unknown | UNKNOWN | Trace caller and diff against AWEB-04 adapter |
| EX-5 | `dashboard_identity.py` | Identity edit | OUT OF SCOPE if metadata-only | Verify; route only if lifecycle |
| AK-1 | `auth*.py` API key mutations | API key | OUT OF SCOPE | AC-05 reporting |
| AK-2 | `embedded/auth.py` API key | aweb-owned | OUT OF SCOPE | None |
| BG-1 | `jobs/retention.py` | Retention | OUT OF SCOPE | None |

Plus bootstrap/creation paths (not bypass sites; map only).

---

## Known bypasses → regression tests to add

As per AC-01 acceptance criteria, failing regression tests or TODO
markers for each known bypass:

- `backend/tests/test_agent_lifecycle.py::test_archive_agent_releases_task_claims_via_cascade` — **initially failing until AC-02 lands.**
- `backend/tests/test_agent_lifecycle.py::test_archive_agent_clears_presence` — **initially failing.**
- `backend/tests/test_agent_lifecycle.py::test_archive_agent_closes_waiting_chat` — **initially failing.**
- `backend/tests/test_agent_lifecycle.py::test_archive_agent_drops_reservations` — **initially failing.**
- `backend/tests/test_agent_lifecycle.py::test_replace_agent_releases_old_claims_and_records_audit` — **initially failing.**
- `backend/tests/test_team_archive.py::test_team_archive_emits_cascade_events` — **initially failing.**

These tests should be written as part of **AC-03** (hosted
lifecycle cascade tests) so they serve as both audit evidence and
regression guarantee. Until AC-02 lands, they stay pending or
marked `xfail` with a reference to this audit.

---

## What AC-02 must NOT change

- The multi-address iteration and rollback logic added in `aajw.12`
  (`state.managed_addresses`, `_rollback_reassigned_addresses`).
  That work is correct and stays.
- BYOD guardrails: address reassignment for BYOD namespaces is left
  untouched; the cascade only handles the aweb-schema coordination
  side, not registry authority.
- The multi-schema transaction boundary: the cascade call runs
  inside `multi_schema_transaction` so cloud+oss+aweb rollback
  remains atomic with the awid registry calls.

---

## Open question: `embedded/workspaces.py::retire_workspace`

See EX-4. If this function is cloud-duplicate of the AWEB-04
cascade, we need to delete it and use the cascade. If it's the
actual cascade helper (exposed at the embedded boundary by
AWEB-04), we need to document that and stop calling it from other
sites that should be using the high-level cascade API instead.

**Action owner**: Kate, as the first thing in AC-02. Result
documented here before AC-02's implementation lands.

---

## Traceability

- Source spec: [`agent-lifetime-support-epic.md`](agent-lifetime-support-epic.md) §AC-01.
- Epic task: `aweb-aaka.14`.
- Informed by prior audit: Alice's 2026-04-18 dashboard audit
  (`list_did_addresses[0]` sites, singular Replace/Archive fields).
- aweb side the cascade lives at: commit `6ac5e90` "feat: expose
  lifecycle coordination cascade" (AWEB-04), now on aweb main.
- Related recent cloud work to build on: aweb commit `1f51a31f`
  "Handle multi-address lifecycle operations" (aajw.12), already
  on ac main — provides the multi-address iteration AC-02 keeps.
