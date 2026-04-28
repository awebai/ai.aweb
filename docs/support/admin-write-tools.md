# Admin Write Tools — Design (aweb-aakj)

`aweb-admin` has guarded write tools. This doc specifies the minimum write
surface needed so operators can retire squatting users, orgs, teams,
and release blocked slugs without raw SQL. It defines the command
shapes, safety gates, audit contract, and test expectations.

Target: `backend/src/aweb_cloud/admin.py`. New commands only; do not
alter existing read commands.

## Commands

Four new top-level commands, each declared on the existing `click`
group:

| Command | What it does | Target |
|---------|--------------|--------|
| `retire-user` | Soft-deletes a user, removes ephemeral auth state, and cascades to same-scope org/team cleanup when explicitly allowed | email, username, or UUID |
| `retire-org` | Soft-deletes an organization and its teams; removes ephemeral membership/invite state | slug or UUID |
| `retire-team` | Soft-deletes a single team and lifecycle-bearing scoped rows; removes ephemeral credentials/claims/tokens | slug or UUID |
| `release-slug` | Frees a blocked slug without deleting owned data — renames the existing occupant to `<slug>-released-<yyyymmdd-hhmmss>` | slug |

No command cascades across the above boundaries silently. `retire-user`
refuses if the user owns a team unless the operator runs `retire-team`
or `retire-org` first. `retire-org` refuses if it would orphan
addresses in a managed namespace unless namespace cleanup has been
done. Refusal messages name the specific blocker.

## Arguments and flags

```
aweb-admin <command> <IDENTIFIER>
  [--dry-run]            # default. Prints the plan, writes nothing.
  --confirm=<IDENTIFIER> # required to apply. Must match IDENTIFIER exactly.
  [--reason=<STRING>]    # optional free text, persisted to audit
  [--ticket=<STRING>]    # optional external ticket ref, persisted to audit
  [--cascade]            # opt-in to cross-boundary deletes (see below)
  [--json]               # machine-readable output on stdout
```

Contract details:

- **Default is dry-run.** The operator must explicitly pass
  `--confirm=<IDENTIFIER>` (string equality with the positional
  argument) to apply. Passing `--confirm` without a value or with a
  mismatch is a refusal, not a silent no-op.
- `--cascade` only applies where documented per-command. It is not a
  global "delete everything" switch.
- `--reason` and `--ticket` are optional but recommended; both are
  persisted verbatim to the audit row.
- `--json` produces structured output suitable for piping to `jq`;
  without it, output is rich-console human format.

## Dry-run output format (human)

```
Would {{retire|release}} <target-type>: <identifier>

Scope (would be affected):
  <schema>.<table>: <N> rows (<hard_delete|soft_delete|disable|revoke|expire>)
  <schema>.<table>: <N> rows
  ...

Cross-boundary blockers (refusing):
  - <blocker 1> — run `aweb-admin <fix-command>` first
  - <blocker 2> — run `aweb-admin <fix-command>` first

Audit (would write):
  operation: admin-<command>
  authority_subject: <from AWEB_ADMIN_ACTOR or local signing identity>
  ticket_id: <--ticket or null>
  reason: <--reason or null>

Re-run with --confirm=<IDENTIFIER> to apply.
```

If there are blockers, the command **exits non-zero** after printing
them, even in dry-run mode. An operator should not see "all green"
and then try `--confirm`.

If there are no blockers and no rows, exit zero and print "Nothing to
do."

## Dry-run output format (--json)

```json
{
  "command": "retire-user",
  "dry_run": true,
  "target": {"type": "user", "identifier": "juan@example.com", "id": "<uuid>"},
  "plan": {
    "deletes": [
      {"schema": "aweb_cloud", "table": "sessions", "kind": "hard_delete", "count": 3},
      {"schema": "aweb_cloud", "table": "mcp_oauth_grants", "kind": "revoke", "count": 1},
      {"schema": "aweb_cloud", "table": "users", "kind": "soft_delete", "count": 1}
    ],
    "renames": []
  },
  "blockers": [
    {"code": "owns_team", "detail": {"team_id": "<uuid>", "slug": "acme"}}
  ],
  "audit_preview": {
    "operation": "admin-retire-user",
    "authority_subject": "<actor>",
    "ticket_id": null,
    "reason": null
  }
}
```

Same shape on apply with `"dry_run": false` and an additional
`"audit": {"audit_id": "<uuid>"}` once the audit row is written.

## Transaction and connection model

- All write paths run in **one** `BEGIN ... COMMIT` per command.
- Flip read/write at the transaction level, not the session level:

  ```python
  async with conn.transaction():
      await conn.execute("SET LOCAL default_transaction_read_only = off")
      # apply declared mutations
      # insert audit row
  ```

  This keeps the existing session-level read-only default intact for
  everything that reuses the same connection. Do **not** flip
  `default_transaction_read_only` at the session level.

- The audit insert is the **last** statement before `COMMIT`. If any
  mutation fails, rollback leaves the audit unwritten too. We never
  have an audit row for a mutation that did not happen.

## Mutation policy

Default to soft-delete, not hard-delete. Hard-delete is reserved for
truly ephemeral state: sessions, one-time or bearer OAuth tokens,
spawn invite tokens, JWT revocations, OAuth states, password reset
tokens, email link tokens, task claims, reservations, and membership or
invite rows that are pure access state. Disable or revoke credentials
where the table has an active/revoked state instead of deleting them.

Always preserve forensic or externally referenceable history:

- `aweb.audit_log`
- `aweb.replacement_announcements`
- `aweb.messages`
- `aweb.chat_messages`
- `aweb_cloud.support_audit`

Mutation in FK-safe order. Do not rely on `ON DELETE CASCADE` — make
every row count visible so the dry-run can enumerate it.

For each command, document the ordered list of tables in the command
docstring. Example sketch for `retire-user`:

```
aweb_cloud.mcp_oauth_* token tables   hard_delete
aweb_cloud.mcp_oauth_grants           revoke
aweb_cloud.sessions                   hard_delete
aweb_cloud.jwt_token_revocations      hard_delete
aweb_cloud.oauth_states               hard_delete
aweb_cloud.password_reset_tokens      hard_delete
aweb_cloud.email_link_tokens          hard_delete
aweb_cloud.organization_members       hard_delete
aweb_cloud.team_members               hard_delete
aweb_cloud.users                      soft_delete
```

If a cross-boundary row exists (e.g., user is last owner of an
organization with active teams), refuse unless `--cascade` is passed,
and even then refuse with a clear error naming what needs to be
retired first. `--cascade` **is not** a license to retire organizations
outside the same scope inside `retire-user`; it only enables same-scope
cleanup (e.g., a personal-scope org that has the user as its only
member).

## Guard-vs-delete coverage invariant

Every row a mutation predicate can reach must be visible to a guard that
runs **before** the transaction opens. Guards may over-match (refuse on
rows the mutation would not touch); guards must never under-match. This is
the class of bug ceo's thorough review surfaced on the first cut.

Concrete requirements:

- **Both-column team scoping.** `aweb.agents` has `team_id` (aweb team
  id) and `server_team_id` (server team id). Either column may be NULL.
  If a mutation predicate uses either column, the guard must query both.
  For a retire-team plan: guard filter is
  `server_team_id = $server_id OR team_id = $aweb_team_id`, never just
  one.
- **dns_namespaces dual path.** A `dns_namespaces` row can be tied to a
  team two ways: `dn.scope_id = team_id`, or `dn.domain` matches a
  `managed_namespaces.domain` for the team. `dns_namespaces.scope_id`
  uses `ON DELETE SET NULL`, so deleting `server.teams` does not remove
  the namespace row. A guard that only joins through
  `managed_namespaces` misses BYOD or drifted `dns_namespaces` rows.
  Guards and explicit mutation predicates must walk both paths.
- **Every mutation predicate has a guard entry.** For each row added to
  `_retire_for_team` / `_retire_for_org` / etc., enumerate the
  corresponding guard check in the plan. Reviewers count mutation
  calls and guard calls and compare.

## Audit contract

One row per apply in `aweb_cloud.support_audit` using the existing
schema. Field choices:

- `operation` — stable string, new values introduced by aakj:
  - `admin-retire-user`
  - `admin-retire-org`
  - `admin-retire-team`
  - `admin-release-slug`
- `authority_mode` — `admin_cli` for support_audit provenance only.
  This value is internal to the admin CLI audit rows and is **not** part
  of the public `support-contract-v1` envelope vocabulary. Public
  envelope `authority_mode` continues to describe the authority exercised;
  if CLI invocation needs to become public later, add a separate
  `invocation_surface` field rather than overloading authority.
- `authority_subject` — resolved from, in order:
  1. `AWEB_ADMIN_ACTOR` env var if set (expected: the operator's email
     or did:aw).
  2. The signing identity in `~/.config/aw/identity.yaml` if the CLI
     is being run from a workspace with a persistent identity.
  3. `"cli-unknown"` as a last resort — but refuse write in this case
     unless `--force-unidentified-actor` is passed (another explicit
     opt-in, not a default).
- `target_type` — one of `user | organization | team | slug`.
- `target_identifier` — the resolved UUID of the target.
- `target_label` — human-readable: email for users, slug for orgs/
  teams.
- `mutations` — JSON array of `{kind: "hard_delete" | "soft_delete" |
  "disable" | "revoke" | "expire" | "rename", schema, table, count,
  details?}`.
- `new_state` — `{before_slug, after_slug}` for `release-slug`;
  `{status: "soft_deleted"}` for retire commands.
- `ticket_id` — from `--ticket`, nullable.
- `reason` — from `--reason`, nullable.
- `request_id` — generate a new UUID per invocation.

## Refusal semantics

Refusals are always:
- **Exit code non-zero.**
- **Human output** starts with `REFUSED:` on its own line, then the
  code, then the explanation, then the next command to run.
- **--json output** uses `{"status": "refused", "error": {"code": ..., "message": ..., "next_step": ...}}`.
- **No audit row is written on refusal.** Refusals happen before any
  state change, including the audit insert.

Initial refusal codes:

- `admin.refused.no_actor` — no `AWEB_ADMIN_ACTOR`, no local signing
  identity, and `--force-unidentified-actor` not passed.
- `admin.refused.target_not_found` — identifier resolves to zero rows.
- `admin.refused.target_ambiguous` — identifier resolves to more than
  one row (e.g., a substring search not anchored).
- `admin.refused.owns_team` — user owns teams; run `retire-team` or
  `retire-org` first.
- `admin.refused.has_active_namespace` — org has a managed namespace
  with addresses still registered at awid.
- `admin.refused.slug_free` — `release-slug` called on a slug that
  nobody owns; nothing to do.
- `admin.refused.confirm_mismatch` — `--confirm` value does not equal
  the positional identifier.
- `admin.refused.cascade_required` — the retirement would orphan rows the
  operator did not opt into; naming the class of rows.

## Test expectations

New test file: `backend/tests/test_admin_cli_write.py`. Use the
existing `aweb_cloud_db` fixture for a real Postgres schema.

Each command needs at minimum:

1. **Dry-run on a seeded target** — asserts expected mutation plan
   counts; asserts zero rows changed.
2. **Dry-run on a missing target** — asserts `admin.refused.target_not_found`;
   zero mutation.
3. **Dry-run on a blocker** — asserts `admin.refused.owns_team` or
   similar; zero mutation; exit non-zero.
4. **Apply with `--confirm` mismatch** — asserts `admin.refused.confirm_mismatch`;
   zero mutation.
5. **Apply with matching `--confirm`** — asserts exact rows affected per
   the dry-run plan; asserts `support_audit` row present with correct
   operation and target fields; asserts no rows in cross-boundary
   tables were touched.
6. **Apply same command twice** — second run exits with
   `admin.refused.target_not_found` (not a different error), zero
   mutation, no second audit row.
7. **Apply without actor** — asserts refusal; asserts
   `--force-unidentified-actor` flag lets it through and records
   `"cli-unknown"` in the audit.

Tests use click's `CliRunner` so they exercise the full CLI surface,
not just the underlying functions. Reuse the `support_audit` helper
from `aweb_cloud.services.support_audit` rather than reading the
table directly.

## Non-goals

- No HTTP endpoint. This is CLI-only. The support HTTP surface
  (`/api/v1/admin/support/*`) covers agent lifecycle; aakj covers
  user/org/team/slug cleanup which is an operator concern, not a
  support-ticket concern. If an HTTP version is ever needed it goes
  through a separate design.
- No bulk delete / batch mode. Each invocation targets exactly one
  user / org / team / slug.
- No undelete. The operator owns the backup.

## Implementation and review path

- **Kate**: implements.
- **Jack (me)**: first-pass review (file-level correctness, matches
  this doc, tests cover the refusal cases).
- **Ivy**: architectural review — this is contract-sensitive
  (introduces new `support_audit.operation` values, new
  `authority_mode`, new refusal codes). Ivy gates.
- **Alice**: final approval before merge.

## Open questions to close before implementing

1. Does Alice's squatter-cleanup SQL already enumerate the exact FK-safe
   order for `retire-user` + `retire-org`? If yes, Kate reuses it
   verbatim instead of reconstructing it. Ask Alice in mail.
2. Should `admin_cli` authority_mode be added to the support-contract
   payload vocabulary now, or is it strictly internal? **Confirmed:
   internal only.** `admin_cli` may appear in support_audit rows for CLI
   provenance, but not in `support-contract-v1`.
3. Does `support_audit` schema already allow the new operation values
   without a migration? **Confirmed: yes.** Migration 015 defines
   `operation TEXT NOT NULL` and `authority_mode TEXT NOT NULL` with
   no CHECK constraint. New string values are free to add without a
   migration.
