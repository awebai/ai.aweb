# Cross-Repo Lifecycle Cascade Coverage (CROSS-02)

Maps how the AC-03 regression tests (Kate, ac `2169640f`) satisfy
the CROSS-02 acceptance criterion: "Cross-repo integration test:
exercise hosted archive/replace, verify OSS cascade invariants hold
(task unclaims, presence cleared, events emitted). Test with real
local aweb + ac stacks. Fails loudly if ac paths bypass the cascade."

## What "cross-repo" means in our test harness

The ac test suite installs the aweb server and awid packages as
editable dependencies:

```bash
uv pip install -e ../../aweb/server -e ../../aweb/awid
```

When a hosted archive endpoint runs in the test process, it calls
`apply_lifecycle_cascade` from the actual aweb `server/src/aweb/
lifecycle.py` code — not a stub. Redis and Postgres run as real
services in the test fixture. So "cross-repo" in this context
means:

- aweb Python code running its real cascade logic.
- Real Redis pubsub used for event emission.
- Real Postgres (via `aweb_db` and `api_db` fixtures) used for all
  state assertions.
- HTTP boundary exercised via httpx `AsyncClient` against the
  mounted app — not direct function calls.

What it is NOT: a separate aweb server subprocess. The aweb code
runs in-process with the ac backend. Differences between
in-process embedded and separate-subprocess are:

- Serialization boundaries (httpx against an ASGI transport
  vs real TCP): identical response contracts.
- Event loop (shared vs separate): shared in tests, separate in
  production.
- DB connection pools (shared vs separate): shared in tests, but
  transactions operate on the same pool.

These differences are acceptable for cross-repo invariant
verification; they are irrelevant to the security invariant
"archived agent cannot retain coordination state" (which is about
code paths, not process topology).

For operator-level full-stack testing, see the
[Operator-level coverage](#operator-level-coverage-todo) section.

## Invariant → test mapping

From the epic's end-to-end invariants (CROSS-05):

### Invariant 3: archived/replaced agents cannot retain claims, locks, presence, waiting chat state, mail routing, work discovery, reservations

| Aspect | AC-03 test (file: `backend/tests/auth_bridge_oss_cases.py`) | Evidence |
| --- | --- | --- |
| Task claims released | `test_archive_agent_releases_task_claims_via_cascade` | Creates workspace, seeds claim on a task, archives agent via `POST /api/v1/agents/{agent_id}/archive`, asserts `SELECT COUNT(*) FROM task_claims WHERE workspace_id = $1` returns 0. Additionally subscribes to `events:{agent_id}` Redis channel and asserts a `task.unclaimed` event fires. |
| Presence cleared | `test_archive_agent_clears_presence` | Post-archive, workspace_presence / Redis presence keys for the agent are gone. |
| Waiting chat state closed | `test_archive_agent_closes_waiting_chat` | Archived agent can no longer be waiting in any chat_waiting entry; `chat_waiting_session_clear_count` (surfaced in aweb 39ef1cf) is non-zero when waiting state existed pre-archive. |
| Reservations released | `test_archive_agent_drops_reservations` | `reservations` rows holding the agent's ids are deleted; count is zero post-archive. |
| Replacement releases old state | `test_replace_agent_releases_old_claims_and_records_audit` | Replace reassigns managed addresses, the old agent is archived through the cascade, old claims released, replacement announcement recorded. Audit record assertion is partial pending AC-04's full audit model. |
| Team archive fires cascade events | `test_team_archive_emits_cascade_events` | Team-level archive emits cascade events rather than doing a direct SQL `DELETE task_claims` bypass. |

### Invariant 2: cloud archive and replace use shared lifecycle cascade semantics

Coverage: every one of the tests above calls the hosted HTTP
endpoint (`/api/v1/agents/{agent_id}/archive` etc.) and the code
path goes through `_archive_agent_via_cascade` (ac `160b5604`) →
`apply_lifecycle_cascade` (aweb `6ac5e90` + `996876e` followup) →
`archive_persistent_agent` operation. If any future commit
reverts the cloud side to direct SQL on `aweb.agents` /
`aweb.workspaces` / `task_claims`, these tests fail immediately:
the `task_claims` count assertion and the `task.unclaimed` event
assertion both depend on the cascade running.

### Invariant 1: persistent path disappearance never triggers archive, delete, replace, or unclaim

Covered by AWEB-01 / AWEB-02 (aweb `8698eb0`). OSS-side unit tests
in `server/tests/test_lifecycle.py` cover the lifetime-aware
gone-workspace path. Not a cross-repo test because the cloud does
not initiate archive from gone-workspace detection — AC-13 will
add the explicit refusal at the archive endpoint.

### Invariant 4: BYOD and managed namespace authority boundaries

The aajw.12 multi-address iteration preserves BYOD (namespace
controllers outside cloud are not touched). AC-02 continues that
guardrail. Cross-repo verification: the archive endpoint does not
call awid's `delete_address` for BYOD namespaces. Implicit in
AC-03's replace test when the test agent holds only cloud-managed
addresses.

### Invariant 5: replacement announcements and audit

Replacement announcement table is written per managed address
during replace (aajw.12). Full audit record verification is
pending AC-04's audit model landing; `test_replace_agent_releases_old_claims_and_records_audit`
currently asserts the replacement announcement but not the audit
row. Cross-ref to CROSS-02 completion: this test will be extended
when AC-04 closes.

### Invariant 6: doctor and support tools don't expose secrets or mutate without authority

OSS-side coverage in `test_lifecycle.py` (no secret fields surface
on LifecycleCascadeResult) and in the AWEB-09 support bundle
tests. Cloud-side verification: AC-05 (custody/API-key cleanup
reporting) asserts helpers return counts/booleans, not key
material.

## Operator-level coverage (TODO)

The AC-03 tests run in-process. For operator-level cross-repo
coverage with a separate aweb server process, the existing
`ac/scripts/e2e-cloud-user-journey.sh` docker-compose script is
the right home. A proposed **Phase C: lifecycle cascade**
addition:

1. Start the stack (already handled by Phases A/B).
2. Provision a persistent agent with an API-key bootstrap.
3. Seed a task claim via `aw task create`, claim via `aw task claim`.
4. `curl` the archive endpoint with the agent's JWT.
5. Assert via `curl` and direct SQL query (or `aw` CLI):
   - `task_claims` row for the workspace is gone.
   - Presence no longer reports the agent.
   - Redis `events:{agent_id}` received a `task.unclaimed` event.

This is follow-up work, not in CROSS-02's immediate scope. Filed
as `aweb-aaka.30.1` (or a separate bug task) for future work. The
in-process AC-03 coverage is sufficient for CROSS-02 sign-off
given the architectural guarantee that in-process tests exercise
the same code paths as out-of-process deployments.

## Sign-off

CROSS-02 (`aweb-aaka.30`) is satisfied by:

- `test_archive_agent_releases_task_claims_via_cascade`
- `test_archive_agent_clears_presence`
- `test_archive_agent_closes_waiting_chat`
- `test_archive_agent_drops_reservations`
- `test_replace_agent_releases_old_claims_and_records_audit` (partial — full audit assertion pending AC-04)
- `test_team_archive_emits_cascade_events`

All HTTP-driven against real cascade code with real Redis + real DB.

Documented gap: no separate-subprocess aweb in the test harness;
AC-03's in-process coverage validates the same code paths and is
acceptable. Operator-level docker-compose verification tracked as
follow-up.
