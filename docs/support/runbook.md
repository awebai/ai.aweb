# Support Runbook

> **Status: DRAFT (v0).** Initial unified runbook scoped 2026-04-28.
> Pending Tom (coord-cloud) GO. Common operations section uses the
> 7-bullet template; rename is the filled-in model. Other operations
> marked PLANNED. Recovery cases (1-5) carried over from the prior
> agent-identity-recovery.md and will be conformed to the same template
> as we iterate.

## Scope

This is THE runbook for Amy as support agent. Single file, single
entry point. Customers find aweb via the cloud product and don't
distinguish "OSS vs cloud" — neither does this doc.

Self-hosted (OSS, BYOIT) operator workflows are out of scope here and
will be handled by a separate agent in the future, with its own
runbook.

Source-of-truth docs in aweb (read these for the underlying model when
a customer goes deep):

- `../../../aweb/docs/identity-guide.md`
- `../../../aweb/docs/trust-model.md`
- `../../../aweb/docs/awid-sot.md`

## How to use this doc

Two kinds of entries:

**Common operations** (Section 1) — customer wants to do something.
Each operation has a 7-bullet structure:

- **What the customer sees** — plain customer-facing description.
- **Dashboard path** — UI navigation.
- **Backend endpoint(s)** — for support reference; not customer-facing.
- **What happens under the hood** — for support reference; brief.
- **Edge cases & error conditions** — known failure modes + status codes.
- **What this is NOT** — boundary statements that disambiguate from
  adjacent operations.
- **Related operations** — links to sibling sections.

**Recovery scenarios** (Section 2) — customer's identity is broken
(key lost, address missing, dashboard fails). Different shape:
triage facts → matrix → per-case procedure → customer-facing language.

Customer-facing parts are **What the customer sees**, **What this is
NOT**, and the **Customer-facing language** quotes in recovery
sections. Quote those verbatim. The rest is support-agent reference.

## Maintenance contract

When a dashboard or cloud-CLI feature ships that touches anything
covered here, the PR description must include a "Support runbook
impact:" line — either "no update needed" or "update section X". Tom
(coord-cloud) enforces at GO. This makes runbook updates a release-gate
item rather than backlog cleanup.

The recovery section's content (Section 2) is currently synced from
`ac` via `make docs-sync` against the legacy file
`agent-identity-recovery.md`. **Sync target needs to redirect to this
file's Section 2** as a follow-up infra item with Mia. Until that
lands, the legacy file may transiently diverge from this one; this
file is authoritative.

---

# Section 1 — Common operations

## 1.1 Rename a hosted agent's public address

### What the customer sees

The agent's public address (the part the world types to reach them,
e.g. `juan.aweb.ai/avi`) is changed to a new name in the same
namespace (e.g., `juan.aweb.ai/sofia`). The agent keeps the same
identity, the same chat / mail history, the same coordination state,
the same credentials. Only the public address record changes.

This is what most customers mean when they ask "can I rename my agent."

### Dashboard path

Identities → click the agent → scroll to **External address** →
**Change or reassign address** → pick the same namespace, type the
new name → **Update address**.

For agents whose identity is hosted (custodial), the team owner must
perform this action. Other team members do not have authority — refer
the requester to their team owner, or escalate the team-ownership
question separately if no clear owner exists.

### Backend endpoint(s)

`PUT /api/v1/agents/{agent_id}/addressing`

Payload:
```json
{
  "namespace_id": "<managed_namespace_id>",
  "name": "<new-name>",
  "reassign": false
}
```

Returns 200 with the updated address record on success. Pass
`"reassign": true` to take a name currently bound to a different agent
(see Edge Cases).

### What happens under the hood

The cloud asks the identity registry to delete the old
`domain/old-name` row and register a new `domain/new-name` row pointing
at the same durable identity (`did_aw`). Two registry calls in
sequence; both signed by the namespace controller. The agent's local
rows (alias, did_aw, did_key, OSS team membership) are untouched.

The reachability setting (`public` / `org_only` / `team_members_only`
/ `nobody`) carries over to the new address.

### Edge cases & error conditions

- **`409 address_in_use`**: the new name is already bound to a
  different agent in the same namespace. Response payload includes
  `conflict_agent_id`. Two paths:
  - Customer picks a different name and retries.
  - Customer uses **Reassign existing address** in the same UI section
    — same endpoint with `reassign=true`. This MOVES the name off the
    conflicting agent (which is left without that address, addressable
    only via its other addresses if any). Destructive on the
    conflicting agent. Dashboard requires explicit confirmation;
    surface this clearly to the customer before they click.
- **`403 Namespace is not attached to this team`**: the customer
  picked a `namespace_id` that doesn't belong to their team. Almost
  certainly UI / state-staleness. Ask them to refresh and retry.
- **`403 manage external agent addresses`**: the customer is not the
  team owner. Refer them to whoever owns the team, or escalate the
  team-ownership question separately.
- **`400` from registry**: registry rejected the request (e.g., name
  validation failed, controller key mismatch). The error message
  includes the registry-side detail; surface it to the customer.
- **Registry transiently unavailable**: customer sees the dashboard
  request hang or fail. The endpoint is not transactional across
  registry calls; if the delete-old-address succeeds and the
  register-new-name fails, the cloud attempts a rollback to restore
  the old address. If the rollback also fails, the customer's address
  is in a degenerate state — escalate to engineering with the agent
  ID, intended new name, and the timestamp of the attempt. Recovery
  procedure for that state lives in a separate playbook (TBD).
- **BYOD-domain agents**: the dashboard shows "this address is
  managed outside this team" and the rename UI is disabled for these
  agents. Customers with BYOD addresses must rename via their
  namespace controller key on the CLI (`aw id` commands), not the
  dashboard. (UI disabled-state pending browser verification.)

### What this is NOT

- This does NOT change the agent's internal alias (the
  `agent.alias` field used for team-internal coordination). There is
  no dashboard endpoint to change just the alias today; if the
  customer specifically wants the internal alias changed without
  changing the public address, the only path is "archive + create new
  with the desired alias" (see Related Operations).
- This does NOT rotate the agent's keys, did_key, or did_aw. Identity
  continuity is preserved end-to-end. Open mail/chat threads, contact
  pins, message-acceptance settings, coordination role — all unchanged.
- This does NOT migrate the agent across namespaces. If the customer
  wants to move from `acme.com/avi` to `personal.example.com/avi`,
  that's a different operation: same endpoint accepts a different
  `namespace_id`, but they need to own / be attached to the target
  namespace first. Treat as adjacent operation, not rename.

### Related operations

- **Archive + create new with chosen name** (PLANNED 1.2): customer
  wants a fresh identity (new keys, new did_aw) under a new public
  name.
- **Replace agent identity** (Section 2 Cases 2-3): customer wants a
  fresh identity (new keys, new did_aw) but at the SAME public address.
  Useful for key rotation or recovery from compromised custody.
- **Change reachability** (PLANNED 1.4): if customer wants their agent
  visible to a different audience without renaming, that's the
  reachability dropdown above the address editor, not this operation.

## 1.2 Archive a hosted agent

PLANNED. Lifecycle terminal action; alias becomes reusable; no restore.

## 1.3 Reassign an address from one agent to another

PLANNED. Covered inline in Rename Edge Cases under `409 address_in_use`;
may extract if customer questions concentrate here.

## 1.4 Change an agent's reachability (visibility)

PLANNED. `public` / `org_only` / `team_members_only` / `nobody`.

## 1.5 Change an agent's coordination role / access mode / messaging policy

PLANNED.

## 1.6 Create a new hosted agent

PLANNED. CliIdentitySetupFlow + create-permanent-custodial endpoint.

## 1.7 Manage team API keys (CLI bootstrap)

PLANNED. createTeamKey / aw_sk_ tokens.

---

# Section 2 — Recovery scenarios

<!-- BEGIN: synced-from-ac/docs/support/agent-identity-recovery.md -->
<!-- DO NOT EDIT BETWEEN THESE MARKERS — content auto-synced via `make docs-sync`. -->
<!-- Edit the source in ac/docs/support/agent-identity-recovery.md instead. -->
<!-- The H1 from the source file is dropped on splice; this section's H1 above is provided by runbook.md. -->

This section recovers a customer's ability to use a persistent
identity/address without inventing ownership or silently changing
custody.

Do not guess. Every recovery must preserve the correct authority
boundary:

- The identity registry owns DID and address state.
- Cloud owns managed namespace controller keys for hosted namespaces.
- Cloud owns hosted custodial identity keys.
- Local worktrees own self-custodial identity keys.
- BYOD namespace controller keys are owned by the customer unless
  explicitly hosted by cloud.

## 2.1 Initial triage

Collect these facts before choosing a recovery path:

- `team_id` or team slug.
- `agent_id` or visible agent name.
- Expected address, for example `support:acme.aweb.ai` team or
  `acme.aweb.ai/support` identity address.
- Whether the identity is persistent or ephemeral.
- Whether the identity is custodial or self-custodial.
- Whether the user still has access to the original local worktree and
  `.aw/signing.key`.
- Whether the namespace is cloud-managed or BYOD.
- Whether the registry has the DID registered.
- Whether the registry has an address for that DID.

If the identity is ephemeral, recovery does not apply. Ephemeral
identities are not recoverable as durable identities; create a new
identity.

## 2.2 API-first diagnostics

Prefer API/CLI checks first. Use SQL only when API state is
insufficient or an engineer is already involved.

### Inspect cloud identity state

From the dashboard, capture:

- agent name and `agent_id`
- status: `active`, `retired`, `archived`, or `deleted`
- custody: `self` or `custodial`
- lifetime: must be `persistent`
- address, if shown
- reachability: `nobody`, `org_only`, `team_members_only`, or `public`

If the dashboard cannot load the agent, escalate to engineering with
the team and agent identifiers.

### Check whether the DID is registered

Use the identity's `stable_id` / `did:aw`:

```bash
curl -sS "$AWID_URL/v1/did/$DID_AW/key"
```

Interpretation:

- `200`: the DID is registered.
- `404`: the DID is not registered.
- `200` but `current_did_key` does not match the cloud/local
  `did:key`: stop and escalate as possible identity corruption.
- `5xx` or network failure: registry availability issue, not an
  identity recovery decision.

### Check whether the registry has addresses for the DID

```bash
curl -sS "$AWID_URL/v1/did/$DID_AW/addresses"
```

Interpretation:

- One or more addresses: registry has address state. Use the address
  that matches the team/namespace being recovered.
- Empty list: no registry address exists for this DID.

Do not use public namespace discovery for this step. Public namespace
address listing is reachability-aware. DID reverse lookup is the
correct diagnostic for identity ownership.

### Classify the namespace

For the address domain, determine whether it is:

- **Cloud-managed**: cloud has a `managed_namespaces` row and
  controller key for this team.
- **BYOD with available controller key**: the customer/operator can
  sign namespace controller operations outside cloud.
- **BYOD with lost controller key**: no authorized party can sign
  namespace controller operations.
- **Unknown/unmanaged**: stop and escalate.

Cloud dashboard recovery may only create or reassign addresses for
cloud-managed namespaces where cloud has controller authority.

## 2.3 Recovery matrix

| Case | State | Recovery |
| --- | --- | --- |
| 1 | Managed namespace, self-custodial key still exists locally | Run `aw id register` from the original worktree, then create/assign the managed address from cloud if needed. |
| 2 | Managed namespace, keys lost, address exists at registry | Use dashboard Replace. Cloud registers a new custodial DID and reassigns the existing address with namespace controller authority. |
| 3 | Managed namespace, keys lost, DID/address never registered, local cloud row still has intended address | Use dashboard Replace. Cloud registers a new custodial DID, creates the missing address with namespace controller authority, archives the old identity, and creates the replacement. |
| 4 | BYOD namespace, namespace controller key is available | Customer/operator uses CLI/controller tooling to recover. Cloud must not guess or create BYOD addresses without authority. |
| 5 | BYOD namespace, identity key and namespace controller key are both lost | No recovery by design. Archive the broken identity and create a new identity/address under a controlled namespace. |

Adjacent state:

- DID registered but address missing: treat like Case 3 for
  cloud-managed namespaces with a known local intended address. Treat
  as Case 4 for BYOD.
- Address exists but DID key mismatch: stop and escalate as possible
  corruption.
- Multiple addresses for one DID: choose the address that belongs to
  the affected team/namespace; escalate if ambiguous.

## 2.4 Recovery procedures

### Case 1: register existing self-custodial DID

Use this when the user still has the original local worktree and
signing key.

Ask the user or operator to run from that worktree:

```bash
aw id register
```

Then verify:

```bash
curl -sS "$AWID_URL/v1/did/$DID_AW/key"
curl -sS "$AWID_URL/v1/did/$DID_AW/addresses"
```

If the DID is registered but no managed address exists, use the
dashboard address assignment flow for the agent.

### Case 2: dashboard Replace (existing address)

Use this when:

- identity is persistent
- key is lost
- namespace is cloud-managed
- registry already has the address

In the dashboard:

1. Open the team.
2. Open the affected agent.
3. Confirm it is the intended persistent identity.
4. Use Replace.
5. Verify the replacement agent has a new `did` / `stable_id` and the
   same external address.

Expected backend behavior:

- register the new DID at the registry
- reassign the existing address to the new DID
- archive the old agent
- create a new custodial persistent agent
- record a replacement announcement

### Case 3: dashboard Replace (missing address)

Use this when:

- identity is persistent
- key is lost
- namespace is cloud-managed
- registry does not have the old DID/address
- the cloud agent row still has the intended managed address

In the dashboard, use the same Replace operation as Case 2.

Expected backend behavior:

- register the new DID at the registry
- create the missing managed address at the registry with namespace
  controller authority
- archive the old agent
- create a new custodial persistent agent
- record a replacement announcement

If cloud cannot identify the intended managed address, do not guess.
Escalate to engineering.

### Case 4: BYOD controller recovery

Cloud support should not run managed dashboard replacement for BYOD
addresses unless cloud holds the namespace controller key.

The customer/operator who controls the namespace should recover using
CLI or controller tooling. The exact procedure depends on which keys
are still available.

Escalate to engineering if the customer has a controller key but the
CLI lacks the needed operation.

### Case 5: no recovery

If both the self-custodial identity key and the BYOD namespace
controller key are lost, there is no safe authority left to prove
continuity.

Tell the customer:

> We cannot safely recover this identity or address because both the
> identity key and namespace controller authority are unavailable.
> The safe path is to archive the broken identity and create a new
> identity/address under a controlled namespace.

## 2.5 Customer-facing language

Use clear authority-based explanations. Do not mention internal table
names.

For Case 1:

> Your identity key still exists locally, so the safest recovery is
> to re-register that same identity from the original worktree. This
> preserves the same durable identity.

For Case 2:

> The address exists, but the identity key is no longer usable. We
> can replace the identity with a new cloud-managed key and move the
> existing address to the replacement.

For Case 3:

> The old identity was never fully registered, but the address
> belongs to a cloud-managed namespace. We can provision a new
> cloud-managed identity and create the intended address under the
> namespace controller.

For Case 4:

> This address is under your own namespace. Recovery must be
> performed by the holder of that namespace controller key.

For Case 5:

> There is no remaining key authority that can prove ownership of
> the old identity or namespace. We cannot safely recover it. The
> safe path is to create a new identity/address.

<!-- END: synced-from-ac/docs/support/agent-identity-recovery.md -->

---

# Section 3 — Escalation

Escalate to engineering when any of these are true:

- The registry's `resolve_key` returns a `current_did_key` that does
  not match expected local/cloud state.
- The registry has multiple plausible addresses and support cannot
  determine the intended one.
- The address domain is not clearly cloud-managed or BYOD.
- A dashboard Replace operation returns `409` or `502`.
- The agent is active locally but registry state points the address at
  a different DID.
- The customer reports message/auth failures after a successful
  replacement.

Include this data in the escalation:

- team slug and canonical team id
- agent id and agent name
- custody and lifetime
- old `did:key` and `did:aw`
- expected address
- registry `resolve_key` result
- registry `list_did_addresses` result
- namespace classification
- exact dashboard/API error text

---

# Engineer Appendix — SQL checks

For engineering support or incident response only.

### Local agent state

```sql
SELECT
    a.agent_id,
    a.team_id,
    a.alias,
    a.status,
    a.lifetime,
    a.custody,
    COALESCE(NULLIF(a.did, ''), NULLIF(a.did_key, '')) AS did_key,
    COALESCE(NULLIF(a.stable_id, ''), NULLIF(a.did_aw, '')) AS did_aw,
    NULLIF(a.address, '') AS local_address,
    a.deleted_at
FROM aweb.agents a
WHERE a.agent_id = '<agent_uuid>';
```

### Cloud-managed namespace authority

```sql
SELECT
    id,
    team_id,
    namespace_slug,
    domain,
    controller_did,
    controller_private_key_ciphertext IS NOT NULL AS has_controller_key,
    registration_status,
    deleted_at
FROM aweb_cloud.managed_namespaces
WHERE domain = '<address_domain>'
  AND team_id = '<server_team_uuid>'
  AND deleted_at IS NULL;
```

### Local registry address rows

These rows are local database state for the hosted identity registry
service. Prefer the registry API for support diagnostics.

```sql
SELECT
    ns.domain,
    pa.name,
    pa.did_aw,
    pa.current_did_key,
    pa.reachability,
    pa.visible_to_team_id,
    pa.deleted_at
FROM aweb.public_addresses pa
JOIN aweb.dns_namespaces ns ON ns.namespace_id = pa.namespace_id
WHERE ns.domain = '<address_domain>'
  AND pa.name = '<address_name>';
```

### Replacement audit

```sql
SELECT
    old_agent_id,
    new_agent_id,
    address_name,
    old_did,
    new_did,
    controller_did,
    replacement_timestamp,
    authorized_by,
    created_at
FROM aweb.replacement_announcements
WHERE old_agent_id = '<old_agent_uuid>'
ORDER BY created_at DESC;
```
