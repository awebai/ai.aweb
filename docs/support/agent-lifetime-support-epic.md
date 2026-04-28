# Epic: Agent Lifetime Management And Support Tools

This epic turns the support tooling architecture in
[`docs/support-tools.md`](../support-tools.md) into an implementation plan.

The work is split by owning repository:

- `[aweb]`: OSS `aweb` repo. Owns CLI behavior, awid-facing tools, canonical
  coordination/lifecycle semantics, and local/user-agent self-service.
- `[ac]`: `aweb-cloud` / hosted app repo. Owns dashboard/support APIs,
  hosted custody and managed namespace state, cloud lifecycle routes, support
  audit, and hosted UI.
- `[cross]`: work that requires contract alignment or tests across both repos.

## Epic Outcome

Agents and users can diagnose and repair ordinary identity/workspace problems
without support when they have the needed authority, while hosted support and
dashboard flows can perform high-impact lifecycle operations without bypassing
OSS coordination semantics.

The completed epic must guarantee:

- persistent identities are never deleted, archived, replaced, or otherwise
  mutated merely because a local `.aw` directory or workspace path disappeared
- ephemeral gone-workspace cleanup remains possible, but only after explicit
  lifetime checks and through normal cleanup/cascade semantics
- dashboard, support, and user-admin lifecycle mutations share one tested
  lifecycle path for task unclaims, presence cleanup, events, API key cleanup,
  custody cleanup, replacement announcements, and audit
- `aw doctor` diagnoses by default and can apply only narrow, obvious,
  caller-authorized repairs through `aw doctor --fix`
- high-impact operations remain explicit commands or UI actions with dry-run,
  authority labels, consequence explanations, and audit
- support tools distinguish source of truth and authority in every response

## Milestones

1. **Safety first**: fix persistent cleanup and hosted lifecycle cascade gaps.
2. **Self-service diagnosis**: implement `aw doctor` read-only checks and
   support bundle output.
3. **Self-service safe repair**: implement bounded `aw doctor --fix`.
4. **Registry and cloud read primitives**: add awid read commands and cloud
   support read endpoints.
5. **Privileged action tools**: add audited dry-run repair, replace, and
   archive flows.
6. **End-to-end validation**: cross-repo tests, docs, role updates, and release
   readiness.

## Task Index

| ID | Repo | Title | Blocks |
| --- | --- | --- | --- |
| AWEB-01 | aweb | Fix persistent gone-workspace cleanup invariant | AWEB-02, AWEB-03 |
| AWEB-02 | aweb | Harden workspace delete route and client cleanup semantics | AWEB-03 |
| AWEB-03 | aweb | Add lifecycle cascade regression coverage | AC-02, CROSS-02 |
| AWEB-04 | aweb | Expose canonical lifecycle cascade service/adapter | AC-02 |
| AWEB-05 | aweb | Define `aw doctor` check/output contract in CLI code | AWEB-06, AWEB-07, AWEB-08, AWEB-09 |
| AWEB-06 | aweb | Implement local state and certificate doctor checks | AWEB-09, AWEB-10 |
| AWEB-07 | aweb | Implement identity and awid doctor checks | AWEB-09, AWEB-10, AWEB-11 |
| AWEB-08 | aweb | Implement server, workspace, coordination, and messaging doctor checks | AWEB-09, AWEB-10 |
| AWEB-09 | aweb | Implement redacted support bundle output | CROSS-03 |
| AWEB-10 | aweb | Implement bounded `aw doctor --fix` framework | AWEB-11, AWEB-12 |
| AWEB-11 | aweb | Add safe local/caller-authorized doctor fixes | CROSS-03 |
| AWEB-12 | aweb | Add high-impact action handoff messages | AC-11, AC-12, AC-13 |
| AWEB-13 | aweb | Add awid read commands | AC-06, AC-11 |
| AWEB-14 | aweb | Document OSS doctor and lifecycle semantics | CROSS-04 |
| AC-01 | ac | Audit hosted lifecycle mutation paths | AC-02 |
| AC-02 | ac | Route hosted archive/replace through shared lifecycle cascade | AC-03, AC-04, AC-05 |
| AC-03 | ac | Add hosted lifecycle cascade tests | CROSS-02 |
| AC-04 | ac | Add support audit model and write helpers | AC-11, AC-12, AC-13 |
| AC-05 | ac | Normalize hosted custody/API-key cleanup reporting | AC-12, AC-13 |
| AC-06 | ac | Add read-only support agent resolve endpoint | AC-10, AC-11, AC-12 |
| AC-07 | ac | Add read-only support namespace endpoint | AC-10, AC-11, AC-12 |
| AC-08 | ac | Add read-only support team endpoint | AC-10 |
| AC-09 | ac | Add read-only support replacement history endpoint | AC-10, AC-12 |
| AC-10 | ac | Add support CLI/API wrappers and response schemas | AC-11, AC-12, AC-13 |
| AC-11 | ac | Implement audited `repair-managed-address` | CROSS-03 |
| AC-12 | ac | Implement dry-run/consequence-aware `replace-agent` | CROSS-03 |
| AC-13 | ac | Implement audited `archive-agent` | CROSS-03 |
| AC-14 | ac | Update dashboard UI for dry-runs and consequence prompts | CROSS-04 |
| AC-15 | ac | Update support role, runbook, and operational docs | CROSS-04 |
| CROSS-01 | cross | Agree on source/authority/status JSON vocabulary | AWEB-05, AC-10 |
| CROSS-02 | cross | Validate cloud lifecycle uses OSS cascade semantics | AC-02 |
| CROSS-03 | cross | End-to-end doctor/support recovery scenarios | CROSS-04 |
| CROSS-04 | cross | Release readiness and rollout plan | none |

## Detailed Tasks

### AWEB-01 `[aweb]` Fix Persistent Gone-Workspace Cleanup Invariant

Priority: P0

Problem:

The OSS workspace cleanup path can observe a missing workspace path and treat
that as gone-workspace cleanup input. Persistent identities may move to another
directory or machine, so missing local paths must not participate in cleanup
decisions for persistent identities.

Implementation:

- Locate all code paths that detect missing workspace paths or `.aw`
  directories, including CLI status/cleanup helpers and any server route they
  call.
- Load or query identity lifetime before any destructive cleanup decision.
- If lifetime is `persistent`, report the missing path as operational
  information only.
- If lifetime is `persistent`, do not delete workspace rows, identity rows,
  `identity.yaml`, `signing.key`, task claims, addresses, DID registrations, or
  replacement state.
- If lifetime is `ephemeral`, preserve the existing cleanup behavior, but make
  the lifetime precondition explicit in code and response output.
- Make the command output distinguish:
  - `gone_ephemeral_cleanup_candidate`
  - `gone_persistent_path_only`
  - `unknown_lifetime_no_cleanup`

Acceptance criteria:

- A persistent identity with a missing workspace path is reported but no
  lifecycle mutation occurs.
- An ephemeral identity with a missing workspace path still follows the
  expected cleanup path.
- Unknown lifetime fails closed and does not cleanup.
- CLI output tells the user why persistent cleanup was skipped.
- No cleanup path touches `identity.yaml` or `signing.key` for a persistent
  identity.

Validation:

- Add or update OSS CLI tests for persistent path disappearance.
- Add or update OSS CLI tests for ephemeral cleanup still working.
- Run the focused `go test` package that owns workspace cleanup.
- Run broader OSS tests affected by workspace cleanup.

### AWEB-02 `[aweb]` Harden Workspace Delete Route And Client Cleanup Semantics

Priority: P0

Problem:

The server delete route already rejects non-ephemeral identities, but the
client cleanup path and server response contract should make that invariant
unambiguous and testable.

Implementation:

- Review `DELETE /v1/workspaces/{workspace_id}` and any equivalent internal
  delete helpers.
- Ensure the server checks identity lifetime from authoritative server state,
  not only caller-provided state.
- Return a structured error for persistent delete attempts:
  - stable error code, for example `persistent_identity_not_cleanup_eligible`
  - workspace id
  - identity id when safe
  - lifetime
  - recommended next step
- Ensure the CLI treats this response as expected protective behavior, not as
  an unexpected failure.
- Ensure client cleanup never retries persistent delete through another route.

Acceptance criteria:

- Persistent workspace delete attempts are rejected consistently.
- The CLI displays a clear protective message instead of a stack trace.
- Ephemeral workspace delete behavior remains unchanged.
- Tests prove the client cannot cleanup persistent identities through the route.

Validation:

- Add server route tests for persistent rejection and ephemeral success.
- Add CLI tests for response handling.
- Run the relevant OSS server and CLI test packages.

### AWEB-03 `[aweb]` Add Lifecycle Cascade Regression Coverage

Priority: P0

Problem:

Cloud needs a canonical cascade to call or mirror. OSS must have regression
tests that define what lifecycle cleanup means for coordination state.

Implementation:

- Identify the canonical OSS lifecycle hook or service used when an agent is
  deleted, archived, or replaced.
- Add tests that establish required side effects:
  - workspace soft-delete/retirement
  - task claims released
  - task/team unclaim events emitted
  - Redis or presence state cleared where applicable
  - no persistent DID/address mutation unless explicitly requested by a higher
    authority
- Include a test that persistent path disappearance is not a lifecycle event.
- Include a test that ephemeral cleanup does run the cleanup cascade.

Acceptance criteria:

- The test suite documents the minimum lifecycle cascade contract.
- Future changes that skip task unclaims or presence cleanup fail tests.
- Persistent path disappearance remains separate from lifecycle deletion.

Validation:

- Run OSS lifecycle/mutation hook tests.
- Run any coordination route tests affected by task claims and presence.

### AWEB-04 `[aweb]` Expose Canonical Lifecycle Cascade Service/Adapter

Priority: P0

Problem:

Hosted cloud currently has direct DB mutation paths. Cloud needs a stable way
to run the same cascade semantics as OSS without reaching into incidental
implementation details.

Implementation:

- Define a reusable lifecycle entry point for agent archive/delete/retire
  semantics.
- Inputs must include:
  - actor identity and actor type
  - target agent id
  - target workspace ids when scoped
  - requested lifecycle operation
  - reason/ticket id when supplied
  - dry-run flag when supported
  - authority label
- Output must include:
  - planned or completed mutations
  - task unclaim count
  - event ids or event counts
  - presence cleanup status
  - workspace lifecycle changes
  - errors with stable codes
- Keep registry/DID/address reassignment out of this service unless the
  operation explicitly requests it and supplies registry authority.
- Provide a small adapter boundary that hosted cloud can call from embedded
  aweb or from the cloud integration layer.

Acceptance criteria:

- Cloud can call a documented lifecycle entry point instead of duplicating the
  cascade.
- The service supports dry-run or exposes enough planning data for cloud
  dry-runs.
- Existing OSS behavior is unchanged except for improved structure/tests.
- Errors are stable enough for cloud/support UI display.

Validation:

- Unit tests for service input/output.
- Integration test proving the route and service produce equivalent side
  effects.

### AWEB-05 `[aweb]` Define `aw doctor` Check/Output Contract In CLI Code

Priority: P1

Problem:

`aw doctor` needs a stable machine-readable contract so other agents and hosted
support can consume its output.

Implementation:

- Add `aw doctor` command group with:
  - `aw doctor`
  - `aw doctor --json`
  - `aw doctor --verbose`
  - `aw doctor --offline`
  - `aw doctor --online`
  - `aw doctor --fix`
  - `aw doctor --fix --dry-run`
  - `aw doctor --fix <check-id>`
  - `aw doctor local`
  - `aw doctor identity`
  - `aw doctor workspace`
  - `aw doctor team`
  - `aw doctor registry`
  - `aw doctor messaging`
  - `aw doctor support-bundle --output doctor.json`
- Define stable output fields:
  - `status`: `ok`, `info`, `warn`, `fail`, `unknown`, `blocked`
  - `generated_at`
  - `subject`
  - `checks`
  - `redactions`
  - `version`
- Define per-check fields:
  - `id`
  - `status`
  - `source`
  - `authority`
  - `target`
  - `authoritative`
  - `message`
  - `detail`
  - `next_step`
  - `fix`
- Keep human output concise but ensure JSON has enough detail for support.

Acceptance criteria:

- `aw doctor --json` emits valid JSON for an empty/new workspace, an ephemeral
  workspace, and a persistent workspace.
- Unknown network state is reported as `unknown`, not as failure or identity
  corruption.
- Authorization gaps are reported as `blocked`.
- Check ids are stable and documented.

Validation:

- CLI snapshot/golden tests for human output.
- JSON schema or struct validation tests.
- Tests for offline and online mode behavior.

### AWEB-06 `[aweb]` Implement Local State And Certificate Doctor Checks

Priority: P1

Problem:

Many failures are local config or certificate mismatches. The affected agent
should diagnose them without support.

Implementation:

- Add local checks for:
  - `.aw/workspace.yaml` existence and parse validity
  - active team selection
  - active membership existence
  - team certificate path existence
  - `.aw/signing.key` existence and parse validity
  - local signing key matching certificate member DID
  - server URL and registry URL coherence
  - workspace id coherence
  - lifetime and custody consistency
  - persistent `.aw/identity.yaml` presence and parse validity
  - ephemeral identity not requiring `.aw/identity.yaml`
- Add certificate checks for:
  - certificate decodes
  - lifetime is valid
  - team id matches selected team
  - alias/name matches local selection
  - signature verifies when team public key is available
  - revocation status is checked when reachable
- Avoid printing secret material.

Acceptance criteria:

- Corrupt local files produce actionable `fail` checks.
- Missing optional online data produces `unknown`, not false failure.
- Secret values are never emitted in human or JSON output.
- Persistent vs ephemeral identity expectations are different and explicit.

Validation:

- Tests with fixture `.aw` directories for valid, missing, and corrupt states.
- Tests verifying redaction of key material and tokens.

### AWEB-07 `[aweb]` Implement Identity And awid Doctor Checks

Priority: P1

Problem:

The affected agent should be able to explain whether its DID/key/address state
is registered and coherent at awid under its own authority.

Implementation:

- For persistent identities, check:
  - local `did:aw` and stable id are present
  - local signing key matches current DID key when awid can resolve it
  - `aw id verify <did_aw>` equivalent passes
  - registered key matches local key or reports mismatch
  - local address resolves to expected `did:aw` when visible
  - reverse address listing for DID returns expected address or reports none
- For ephemeral identities, check:
  - no public address is expected
  - identity-only commands explain that the current identity is ephemeral
- Distinguish:
  - DID not found
  - address not found
  - key mismatch
  - awid unavailable
  - caller lacks visibility
- Do not use public namespace discovery as proof of missing identity ownership.

Acceptance criteria:

- DID registered/address missing is reported as a repairable registry
  inconsistency, not as automatic replacement.
- DID key mismatch is a hard failure with escalation guidance.
- awid network failure is `unknown`.
- BYOD and managed namespaces are not conflated.

Validation:

- Tests against mocked awid responses.
- Tests for registered, missing, mismatch, and unavailable cases.

### AWEB-08 `[aweb]` Implement Server, Workspace, Coordination, And Messaging Doctor Checks

Priority: P1

Problem:

Users need one command to determine whether the local agent can talk to the
server, see its workspace, coordinate, and use identity-signed messaging.

Implementation:

- Add server checks for:
  - aweb server reachability
  - awid registry reachability
  - hosted cloud base URL vs mounted `/api` runtime URL confusion
  - compatible version headers when available
  - caller-authenticated team reads
  - caller-authenticated workspace/status reads
- Add coordination checks for:
  - server workspace row exists for current workspace id
  - server workspace team/alias match local config
  - workspace is not marked deleted
  - current task claims are visible and coherent
  - presence can be refreshed by normal activity
- Add messaging checks for:
  - identity-only signing works locally
  - own DID can be resolved when persistent
  - own inbox can be read under current credentials
  - messaging policy is readable when authorized
  - self-send dry-run validates payload shape without sending real mail unless
    explicitly requested

Acceptance criteria:

- Offline mode skips network checks and labels them skipped/unknown.
- Online mode attempts network checks and labels failures precisely.
- Messaging checks do not send real messages by default.
- URL confusion produces a specific check id and next step.

Validation:

- CLI tests with mocked server responses.
- Integration test against local server if available.

### AWEB-09 `[aweb]` Implement Redacted Support Bundle Output

Priority: P1

Problem:

Support needs a shareable artifact produced by the affected agent without
receiving secrets.

Implementation:

- Add `aw doctor support-bundle --output doctor.json`.
- Include:
  - command version
  - timestamp
  - platform and hostname only when useful
  - parsed non-secret `.aw` metadata
  - team id, alias/name, workspace id
  - DID, stable id, address, lifetime, custody
  - registry lookup results
  - server response statuses and request ids
  - check ids, statuses, messages, next steps
  - redaction list
- Exclude:
  - private signing keys
  - API keys
  - bearer tokens
  - cookies
  - full auth headers
  - encrypted key ciphertext
  - raw team certificate material unless explicitly requested and safe
- Optionally sign the bundle with the local identity key for persistent
  identities. If signing is not implemented in v1, include a future field and
  document that it is absent.

Acceptance criteria:

- Bundle is valid JSON.
- Bundle can be generated offline with local checks only.
- Bundle includes request ids for failed server calls when available.
- Redaction tests prove no known secret pattern is emitted.

Validation:

- Golden JSON tests.
- Redaction tests with synthetic secrets.

### AWEB-10 `[aweb]` Implement Bounded `aw doctor --fix` Framework

Priority: P1

Problem:

Some issues are safe for the affected agent to repair itself, but `doctor`
must not become an authority-blind automation path.

Implementation:

- Add fix planning model:
  - check id
  - source
  - authority
  - target
  - planned mutation
  - dry-run/apply mode
  - rollback guidance when possible
  - reason why fix is refused when not allowed
- Make `aw doctor` diagnostic only.
- Make `aw doctor --fix` the explicit apply mode for safe repairs.
- Make `aw doctor --fix --dry-run` show the plan without applying.
- Allow `aw doctor --fix <check-id>` to target one fix.
- Refuse fixes when:
  - caller lacks authority
  - state is ambiguous
  - the action is high-impact
  - multiple plausible repairs exist
  - persistent identity lifecycle would be mutated
- Log local or server-side fixes where appropriate.

Acceptance criteria:

- `aw doctor` never mutates.
- `aw doctor --fix --dry-run` never mutates.
- `aw doctor --fix` applies only checks that advertise `fix.safe=true`.
- Refused fixes explain the explicit command or UI action to use instead.

Validation:

- Tests proving no mutation in diagnostic or dry-run mode.
- Tests proving high-impact checks are refused even when mocked authority
  exists.

### AWEB-11 `[aweb]` Add Safe Local/Caller-Authorized Doctor Fixes

Priority: P2

Problem:

The first fix set should handle boring, unambiguous repairs that are useful in
the field.

Implementation:

- Implement fixes for:
  - stale local selected team derived from existing non-secret `.aw` metadata
  - stale workspace metadata derived from authoritative caller-visible server
    state
  - local server or registry URL normalization when the correct value is
    already present elsewhere in local config
  - non-secret local cache refresh
  - unambiguous broken local `.aw` symlink repair
  - caller-authorized DID self-registration retry after non-fatal init failure,
    when the local key proves the DID and no address or namespace-controller
    authority is involved
  - caller-authorized reconnect/rebind when the local identity key proves the
    identity
  - caller-authorized ephemeral cleanup through existing OSS cleanup semantics,
    with lifetime checked first
- Do not implement:
  - managed address registration/reassignment
  - controller key rotation
  - persistent archive/replace/delete/retire
  - task unclaims outside existing lifecycle endpoints
  - workspace cleanup that touches `identity.yaml` or `signing.key`

Acceptance criteria:

- Each fix has dry-run output and apply output.
- Each fix is idempotent or refuses when state changed unexpectedly.
- DID self-registration retry cannot register addresses.
- Ephemeral cleanup cannot run if lifetime is persistent or unknown.

Validation:

- Per-fix unit tests.
- End-to-end dry-run/apply tests with temporary `.aw` fixtures.

### AWEB-12 `[aweb]` Add High-Impact Action Handoff Messages

Priority: P2

Problem:

When `doctor` finds a problem requiring a significant operation, it should be
useful without performing the operation automatically.

Implementation:

- For each forbidden automatic fix, add a handoff message:
  - required authority
  - whether caller appears to have that authority
  - expected explicit command or dashboard action
  - dry-run command when available
  - consequences
  - why `doctor --fix` refused
- Cover:
  - persistent archive
  - persistent replacement
  - managed address registration/reassignment
  - namespace controller key rotation
  - BYOD recovery with external controller authority
  - suspected DID key mismatch/corruption

Acceptance criteria:

- High-impact findings have actionable next steps.
- Messages do not instruct users to run support-only commands unless they hold
  the authority.
- Replacement guidance says address repair is preferred when existing DID key
  is valid.

Validation:

- Snapshot tests for handoff messages.
- Review messages against support runbook.

### AWEB-13 `[aweb]` Add awid Read Commands

Priority: P1

Problem:

Both users and support agents need registry facts without ad hoc curl commands.

Implementation:

Extend the existing `aw id` command group rather than introducing a
parallel `aw awid` top-level group. `aw id resolve` and
`aw id namespace` already perform registry inspection against awid;
a separate top-level group would duplicate surface and make the
"when do I use `aw id` vs `aw awid`?" question ambiguous.

Commands under `aw id`:

- `aw id resolve <did_aw>` — existing. Already returns the current
  did:key. Extend only if a new flag is needed for AWEB-13 scope.
- `aw id addresses <did_aw>` — **new**. Lists awid-registered
  addresses for a DID.
- `aw id namespace state <domain>` — extend the existing
  `aw id namespace` subcommand with a `state` verb if needed;
  otherwise the current `aw id namespace` surface is sufficient.
- `aw id namespace addresses <domain> --authority anonymous|did|namespace-controller` — **new**.
- `aw id namespace resolve <domain>/<name> --authority anonymous|did|namespace-controller` — **new**.

Response fields (output envelope is `support-contract-v1` from
CROSS-01; payload schema is `awid_read.v1`):

- `source: awid`
- `authority_mode`
- caller/controller DID when signed
- target
- not found vs transport failure
- raw registry fields

Keep registry namespace state distinct from cloud managed-namespace state.

Acceptance criteria:

- Commands work outside hosted cloud.
- JSON output is available.
- Authority modes are explicit in both command input and output.
- Public listing cannot be misread as proof of ownership.

Validation:

- Registry client tests.
- CLI tests with mocked awid server.

### AWEB-14 `[aweb]` Document OSS Doctor And Lifecycle Semantics

Priority: P2

Problem:

The OSS repo must document the behavior that cloud and users rely on.

Implementation:

- Update OSS docs to describe:
  - persistent identity lifetime vs workspace path lifetime
  - ephemeral cleanup rules
  - `aw doctor` commands and statuses
  - `aw doctor --fix` limits
  - awid read commands
  - support bundle redaction
  - explicit commands for high-impact actions
- Link back to cloud support tooling docs where appropriate without making OSS
  docs depend on hosted-only behavior.

Acceptance criteria:

- New users can understand why persistent identities are not cleanup
  candidates.
- Support can link users to `aw doctor` docs.
- Hosted-only support actions are labeled as hosted-only.

Validation:

- Docs review by cloud/support owner.

### AC-01 `[ac]` Audit Hosted Lifecycle Mutation Paths

Priority: P0

Problem:

Hosted archive/replace paths directly mutate local aweb tables in places and
can bypass OSS lifecycle side effects.

Implementation:

- Audit all hosted routes/services/jobs that mutate:
  - `aweb.agents`
  - `aweb.workspaces`
  - task claims
  - presence
  - API keys
  - hosted custody material
  - replacement announcements
- Include dashboard routes, support/admin routes, background jobs, and tests.
- For each path, document:
  - actor type
  - authority checked
  - target
  - current mutations
  - missing cascade side effects
  - whether the operation is archive, replace, delete, retire, or cleanup
- Add failing regression tests or TODO markers for any known bypass.

Acceptance criteria:

- A short audit table exists in code comments, test names, or a design note.
- All lifecycle mutation entry points are known.
- Direct DB mutations that bypass cascade are identified.
- The archive/replace path discussed in this investigation is covered.

Validation:

- Run backend tests that import lifecycle routes.
- Review `agent_lifecycle` and embedded aweb integration paths.

### AC-02 `[ac]` Route Hosted Archive/Replace Through Shared Lifecycle Cascade

Priority: P0

Problem:

Dashboard/support archive and replacement must not bypass OSS coordination
cleanup.

Implementation:

- Integrate the lifecycle service/adapter from `[aweb]` AWEB-04.
- Refactor hosted archive and replace paths to call the shared lifecycle path
  for local aweb lifecycle changes.
- Keep cloud-specific operations in cloud, but execute them in a controlled
  sequence:
  - registry operations when applicable
  - local lifecycle cascade
  - API key/custody cleanup
  - replacement announcement
  - support/dashboard audit
- Ensure failures are transactional or compensating:
  - do not reassign address and then fail silently before recording replacement
  - do not archive locally before required registry preconditions are proven
  - make retry idempotent where possible
- Preserve BYOD guardrails.

Acceptance criteria:

- Hosted archive releases task claims and clears presence.
- Hosted replacement releases old task claims, clears old presence, and records
  replacement announcement.
- Hosted lifecycle writes no longer contain partial direct table mutation
  sequences outside the shared path.
- Dry-run output names every planned mutation by source of truth.

Validation:

- Backend integration tests with tasks claimed by the target workspace.
- Tests that presence is cleared.
- Tests that BYOD replacement without authority is refused.

### AC-03 `[ac]` Add Hosted Lifecycle Cascade Tests

Priority: P0

Problem:

Cloud needs tests that prove it cannot regress to partial direct mutation.

Implementation:

- Add tests for hosted archive:
  - active agent with workspace
  - claimed tasks
  - presence
  - API key
  - custody/cert material when applicable
- Add tests for hosted replace:
  - old agent archived/retired
  - new agent created
  - address continuity handled only with authority
  - replacement announcement recorded
  - old tasks unclaimed
  - old presence cleared
  - audit recorded
- Add negative tests:
  - missing namespace controller authority
  - BYOD without cloud-held controller key
  - persistent path missing alone does not trigger archive/replace

Acceptance criteria:

- Tests fail if task unclaim or presence cleanup is removed.
- Tests fail if direct cloud route can archive persistent identity solely from
  missing path.
- Tests cover both dashboard and support/admin entry points when both exist.

Validation:

- Run cloud backend lifecycle test package.
- Run embedded aweb protocol tests affected by lifecycle changes.

### AC-04 `[ac]` Add Support Audit Model And Write Helpers

Priority: P1

Problem:

Every significant support/user-admin write needs durable audit with authority
and before/after state.

Implementation:

- Define support audit schema or extend existing admin activity schema.
- Required fields:
  - actor id
  - actor type
  - actor auth method
  - ticket id or reason
  - target team
  - target agent
  - target address
  - old DID/address/lifecycle state
  - new DID/address/lifecycle state
  - authority used
  - awid operation result
  - cloud operation result
  - lifecycle cascade result
  - timestamp
  - request id
- Add helper APIs for writing audit records from action tools.
- Ensure audit never stores secrets.

Acceptance criteria:

- All write tools can call one audit helper.
- Audit records are queryable by agent id, address, team, actor, and ticket id.
- Missing reason/ticket id is rejected for production writes.

Validation:

- Migration tests if schema changes.
- Unit tests for audit helper redaction.

### AC-05 `[ac]` Normalize Hosted Custody/API-Key Cleanup Reporting

Priority: P1

Problem:

Lifecycle dry-runs and audit records must report hosted custody and API-key
cleanup without returning secrets.

Implementation:

- Identify hosted custody key, certificate, and API-key records associated with
  agents/workspaces.
- Add cleanup helpers that return counts/booleans, never key material.
- Ensure archive/replace dry-runs report planned cleanup:
  - API keys to revoke
  - hosted identity key material to delete/detach
  - cert material to delete/detach
- Ensure execute paths report completed cleanup counts.

Acceptance criteria:

- Support APIs never return private keys, encrypted key ciphertext, API keys,
  bearer tokens, or cookies.
- Dry-run and audit show cleanup happened or why it was skipped.
- Cleanup helpers are idempotent.

Validation:

- Backend tests for redaction.
- Backend tests for repeated cleanup calls.

### AC-06 `[ac]` Add Read-Only Support Agent Resolve Endpoint

Priority: P1

Problem:

Support and authorized user-admin flows need a single read endpoint for hosted
agent state before acting.

Implementation:

- Add `GET /api/v1/admin/support/agents/resolve`.
- Inputs:
  - `agent_id`, or
  - `address`, or
  - `team_id` plus `name`
- Auth:
  - support/admin auth, or
  - equivalent user-held authority over the team/agent where product policy
    allows
- Return:
  - `source: aweb-cloud`
  - authority label
  - cloud/embedded agent row summary
  - lifecycle state
  - custody/lifetime
  - local DID/address fields
  - server team UUID
  - canonical team id
  - workspace metadata if present
  - hosted custody material presence as booleans
  - replacement history summary
  - optional awid join results when explicitly requested
- Do not return secrets.

Acceptance criteria:

- Endpoint resolves by all supported identifiers.
- Unauthorized callers receive stable `blocked`/403-style responses.
- Response distinguishes not found from unauthorized.
- Optional awid join failures do not hide cloud state.

Validation:

- Backend route tests for each identifier.
- Auth tests for support, authorized user, and unauthorized user.

### AC-07 `[ac]` Add Read-Only Support Namespace Endpoint

Priority: P1

Problem:

Recovery decisions require knowing whether cloud holds namespace controller
authority.

Implementation:

- Add `GET /api/v1/admin/support/namespaces/{domain}`.
- Auth:
  - support/admin auth, or
  - equivalent user-held namespace/team authority where allowed
- Return:
  - `source: aweb-cloud`
  - authority label
  - whether domain is cloud-managed
  - owning cloud team if managed
  - namespace slug
  - awid registration status known to cloud
  - controller DID
  - controller key availability as boolean
  - whether cloud can perform controller-authorized operations
- Never return controller private key material.

Acceptance criteria:

- Managed, BYOD, unknown, and unauthorized namespaces are distinguishable.
- Controller key availability is boolean only.
- The endpoint can support `repair-managed-address` preflight.

Validation:

- Backend route/auth/redaction tests.

### AC-08 `[ac]` Add Read-Only Support Team Endpoint

Priority: P2

Problem:

Support needs a safe team overview to correlate server UUIDs, canonical team
ids, slugs, managed namespaces, and agent counts.

Implementation:

- Add `GET /api/v1/admin/support/teams/resolve`.
- Inputs:
  - server team UUID
  - canonical colon-form team id
  - slug
- Return:
  - server team UUID
  - canonical colon-form team id
  - slug/name
  - owner organization
  - managed namespaces
  - active/archived/deleted agent counts
  - authority label
- Respect user-held authority boundaries.

Acceptance criteria:

- Team identifiers resolve consistently.
- Unauthorized callers cannot enumerate unrelated teams.
- Counts match backend state.

Validation:

- Backend route/auth tests.

### AC-09 `[ac]` Add Read-Only Support Replacement History Endpoint

Priority: P2

Problem:

Support needs to see replacement continuity without direct SQL.

Implementation:

- Add `GET /api/v1/admin/support/replacements`.
- Inputs:
  - `agent_id`, or
  - `address`
- Return:
  - replacement announcements
  - old/new agent ids
  - old/new DID keys
  - address
  - timestamp
  - actor/authorized_by
  - authority label
  - request/audit ids when available
- Redact secrets.

Acceptance criteria:

- Replacement history can be queried without SQL.
- Address lookup returns the continuity chain when available.
- Unauthorized callers are blocked.

Validation:

- Backend route/auth tests.

### AC-10 `[ac]` Add Support CLI/API Wrappers And Response Schemas

Priority: P2

Problem:

Agents and operators need consistent command/API contracts around support read
tools.

Implementation:

- Define response schemas for all support read endpoints.
- Add thin wrappers if this repo has a support CLI/admin script surface.
- Ensure every response includes:
  - source
  - authority
  - target
  - authoritative vs operational label
  - request id
  - redaction marker when relevant
- Make wrappers emit JSON suitable for support agents.

Acceptance criteria:

- Support docs can cite stable commands or endpoint examples.
- Schemas are tested or validated.
- Wrappers do not embed direct SQL.

Validation:

- Schema tests.
- CLI wrapper tests if wrappers exist.

### AC-11 `[ac]` Implement Audited `repair-managed-address`

Priority: P1

Problem:

When the existing DID/key is valid and only the managed address is missing or
inconsistent, replacement is too destructive.

Implementation:

- Add high-level action endpoint/command `repair-managed-address`.
- Inputs:
  - target agent id or address
  - target DID/stable id
  - expected address
  - reason/ticket id
  - dry-run flag
- Preconditions:
  - authorized actor
  - cloud-managed namespace
  - namespace controller key available
  - local cloud row identifies intended address
  - existing DID key is valid or intentionally preserved
  - no conflicting address ownership
- Dry-run output:
  - observed cloud state
  - observed awid state
  - planned registry mutations
  - planned audit record
  - explicit statement that no identity replacement will occur
- Execute:
  - register DID only if safe and intended
  - register or repair managed address under namespace controller authority
  - verify address resolves to existing DID
  - write audit

Acceptance criteria:

- DID registered/address missing repairs without replacement.
- Existing DID/key continuity is preserved.
- Conflicting address ownership fails closed.
- BYOD without cloud controller authority is refused.
- Dry-run is available and accurate.

Validation:

- Backend tests with mocked awid.
- Integration tests for dry-run and execute.

### AC-12 `[ac]` Implement Dry-Run/Consequence-Aware `replace-agent`

Priority: P1

Problem:

Replacement is valid only when existing identity key/custody is lost or
unusable and address continuity must move to a fresh identity.

Implementation:

- Add or update `replace-agent` endpoint/command.
- Require:
  - authorized actor
  - reason/ticket id
  - dry-run support
  - explicit explanation of why address repair is insufficient
  - authority over namespace/address
  - BYOD guardrails
- Dry-run output must list:
  - new DID registration
  - address reassignment
  - old agent lifecycle cascade
  - new custodial agent creation when applicable
  - replacement announcement
  - task unclaims and presence cleanup
  - API key/custody cleanup
  - audit
  - consequences and continuity changes
- Execute through shared lifecycle cascade.

Acceptance criteria:

- Replacement refuses when address repair is sufficient.
- Replacement refuses without namespace/address authority.
- Replacement dry-run names every source of truth it will mutate.
- Execute records replacement announcement and audit.
- Old workspace claims/presence are cleaned up through the shared cascade.

Validation:

- Backend tests for dry-run.
- Backend integration tests for execute.
- Negative tests for repair-sufficient and missing-authority cases.

### AC-13 `[ac]` Implement Audited `archive-agent`

Priority: P1

Problem:

Persistent archive is destructive and must be deliberate, audited, and cascade
through coordination cleanup.

Implementation:

- Add or update `archive-agent` endpoint/command.
- Require:
  - authorized actor
  - reason/ticket id
  - dry-run support
  - explicit confirmation that no address continuity is being claimed
  - optional second approval if policy requires
- Dry-run output must list:
  - agent/workspace lifecycle changes
  - task unclaims
  - presence cleanup
  - API key/custody cleanup
  - managed address detach/delete if requested and authorized
  - audit record
- Execute through shared lifecycle cascade.
- Refuse archive if the only evidence is a missing workspace path.

Acceptance criteria:

- Archive never triggers from gone-workspace detection alone.
- Archive releases tasks and clears presence.
- Archive redacts custody/API-key material.
- Archive writes audit.

Validation:

- Backend route tests.
- Integration tests with claimed tasks and presence.

### AC-14 `[ac]` Update Dashboard UI For Dry-Runs And Consequence Prompts

Priority: P2

Problem:

Human users with authority may initiate significant actions from the dashboard.
The UI must make consequences explicit rather than relying on support-only
flows.

Implementation:

- Update replace/archive UI to call dry-run before execute.
- Display:
  - required authority
  - authority the current user is using
  - planned mutations by source of truth
  - address/DID continuity impact
  - task/presence cleanup impact
  - API key/custody cleanup impact
  - BYOD guardrail status
  - audit reason/ticket field
- Require explicit confirmation for archive and replace.
- Where address repair is sufficient, guide the user to repair rather than
  replacement.

Acceptance criteria:

- Users can see exactly what will change before archive/replace.
- UI blocks execute if dry-run reports missing authority or ambiguous state.
- UI distinguishes support actor and user-held authority.
- UI does not expose secrets.

Validation:

- Frontend tests for modal/flow state.
- Backend contract tests for dry-run responses.
- Manual local dashboard verification.

### AC-15 `[ac]` Update Support Role, Runbook, And Operational Docs

Priority: P2

Problem:

Support agents need instructions that match the new tools and authority model.

Implementation:

- Update support role guidance to include:
  - trust chain
  - source-of-truth split
  - user-held authority vs support authority
  - `aw doctor` first where possible
  - inspect before acting
  - prove authority before recovery
  - no authority means no recovery
  - preserve identity when address repair is enough
  - persistent missing path is not identity death
  - dry-run before writes
- Update recovery runbook examples to prefer:
  - `aw doctor support-bundle`
  - support read endpoints
  - `repair-managed-address` before `replace-agent`
- Remove or demote direct SQL from normal flows.

Acceptance criteria:

- Runbook matches implemented commands/endpoints.
- Support agents can triage without memorizing case numbers.
- Docs clearly mark hosted-only tools.

Validation:

- Docs review with support/cloud owner.

### CROSS-01 `[cross]` Agree On Source/Authority/Status JSON Vocabulary

Priority: P0

Problem:

OSS doctor output, awid read tools, and cloud support tools must use compatible
terms so agents can compose them.

Implementation:

- Define shared vocabulary:
  - statuses: `ok`, `info`, `warn`, `fail`, `unknown`, `blocked`
  - sources: `local`, `aweb`, `awid`, `aweb-cloud`, `dashboard`
  - authority modes: `anonymous`, `caller`, `team-admin`, `org-admin`,
    `namespace-controller`, `support`, `service`
  - target formats for DID, address, team, agent, workspace
  - redaction markers
- Add examples for doctor output and cloud support output.
- Decide whether this lives in OSS docs, cloud docs, or both.

Acceptance criteria:

- `aw doctor --json` and support endpoints use the same status words.
- Authority labels are not support-specific.
- User-held authority is representable.

Validation:

- Contract review by OSS and cloud owners.

### CROSS-02 `[cross]` Validate Cloud Lifecycle Uses OSS Cascade Semantics

Priority: P0

Problem:

The highest-risk bug is cloud lifecycle mutation bypassing OSS route logic and
coordination cleanup.

Implementation:

- Build an integration scenario with:
  - active persistent agent
  - workspace
  - claimed task
  - presence
  - API key
  - optional hosted custody material
- Execute hosted archive and replacement paths.
- Assert the same side effects as OSS lifecycle cascade tests:
  - tasks unclaimed
  - events emitted
  - presence cleared
  - workspace retired/deleted according to operation
  - API keys revoked
  - custody cleaned
  - replacement announcement recorded when applicable
  - audit written
- Include a negative scenario where only workspace path disappearance exists.

Acceptance criteria:

- Cloud and OSS cascade expectations are aligned.
- A direct DB-only lifecycle mutation would fail tests.
- The persistent missing-path negative case passes without mutation.

Validation:

- Run OSS lifecycle tests.
- Run cloud embedded aweb integration tests.

### CROSS-03 `[cross]` End-To-End Doctor/Support Recovery Scenarios

Priority: P1

Problem:

The full product needs scenario coverage across local doctor output, registry
state, cloud support reads, and action tools.

Scenarios:

1. Persistent self-custodial identity, DID valid, managed address missing:
   - `aw doctor` reports address missing
   - support/user-admin reads cloud namespace state
   - `repair-managed-address --dry-run` plans repair
   - execute preserves DID and registers address
2. Persistent identity key lost, managed address exists:
   - `aw doctor` cannot prove local key
   - support/user-admin validates namespace authority
   - `replace-agent --dry-run` explains consequences
   - execute creates replacement and archives old agent through cascade
3. Persistent workspace path moved:
   - `aw doctor workspace` reports missing path
   - no cleanup occurs
   - support tools do not recommend archive/replace solely from path
4. Ephemeral workspace gone:
   - `aw doctor` reports cleanup candidate
   - `aw doctor --fix --dry-run` plans ephemeral cleanup
   - execute cleanup uses existing lifecycle semantics
5. BYOD namespace without cloud controller authority:
   - cloud support reads report no authority
   - repair/replace are refused
   - doctor handoff explains customer-controller action

Acceptance criteria:

- All scenarios have automated tests or documented manual verification.
- Every write path has dry-run coverage.
- Support bundle contains enough data to continue the investigation without
  secrets.

Validation:

- Cross-repo scenario tests where practical.
- Manual runbook exercise for any scenario not yet automated.

### CROSS-04 `[cross]` Release Readiness And Rollout Plan

Priority: P2

Status: landed — [`release-readiness.md`](release-readiness.md) is the
binding contract; append a per-release entry under "As-Shipped Record"
for every lifecycle/support release.

Problem:

This work changes lifecycle semantics and support flows. It needs staged
rollout and clear verification.

Implementation:

- Define release order:
  1. OSS persistent cleanup safety fix.
  2. Cloud lifecycle cascade fix.
  3. `aw doctor` read-only release.
  4. `aw doctor --fix` safe repairs.
  5. Support read endpoints.
  6. High-level write tools.
- Add migration plan for audit tables if needed.
- Add feature flags for risky hosted actions if appropriate.
- Add operational verification checklist:
  - persistent missing path no longer deletes identity
  - hosted archive/replace unclaims tasks
  - hosted archive/replace clears presence
  - support bundle redacts secrets
  - repair-managed-address preserves DID
  - replace-agent records replacement announcement
- Update release notes for both repos.

Acceptance criteria:

- Release order is documented and followed.
- Rollback plan exists for cloud lifecycle changes.
- Support knows which version contains which capability.

Validation:

- Run repo-specific release readiness commands before shipping.
- Verify deployed cloud behavior against the operational checklist.

## Dependency Notes

- AWEB-01 through AWEB-03 and AC-01 through AC-03 are the safety-critical
  foundation. Do not wait for the doctor UX before fixing these.
- `repair-managed-address` should ship before support-authority replacement
  improvements so valid identities are not replaced just because an address is
  missing.
- `aw doctor --fix` may ship incrementally, but every fix must have dry-run
  coverage and a refusal path for ambiguity.
- Low-level registry writes should remain internal or expert-only until
  high-level repair/replace/archive tools exist.

## Done Definition

The epic is done when:

- all P0 tasks are implemented, tested, and released in the relevant repo
- `aw doctor` can produce a redacted support bundle for persistent and
  ephemeral identities
- `aw doctor --fix` can safely apply at least the v1 local/caller-authorized
  repairs
- cloud archive/replace uses shared lifecycle cascade behavior
- support/user-admin read endpoints exist for agent, namespace, team, and
  replacement state
- audited dry-run action tools exist for repair, replace, and archive
- docs and runbooks reflect the implemented commands
- cross-repo scenario validation has passed
