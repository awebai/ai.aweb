# Agent Identity Recovery Runbook

This runbook is for support agents and on-call engineers diagnosing broken
persistent agent identities on hosted `aweb-cloud`.

Use the canonical identity model in the OSS docs as the source of truth:

- `../aweb/docs/identity-guide.md`
- `../aweb/docs/trust-model.md`
- `../aweb/docs/awid-sot.md`

This document only covers hosted support triage and recovery.

## Support Goal

Recover the user's ability to use a persistent identity/address without
inventing ownership or silently changing custody.

Do not guess. Every recovery must preserve the correct authority boundary:

- awid owns DID and address state.
- Cloud owns managed namespace controller keys for hosted namespaces.
- Cloud owns hosted custodial identity keys.
- Local worktrees own self-custodial identity keys.
- BYOD namespace controller keys are owned by the customer unless explicitly
  hosted by cloud.

## Initial Triage

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
- Whether awid has the DID registered.
- Whether awid has an address for that DID.

If the identity is ephemeral, this runbook does not apply. Ephemeral identities
are not recoverable as durable identities; create a new identity.

## API-First Diagnostics

Prefer API/CLI checks first. Use SQL only when API state is insufficient or an
engineer is already involved.

### 1. Inspect Cloud Identity State

From the dashboard, capture:

- agent name and `agent_id`
- status: `active`, `retired`, `archived`, or `deleted`
- custody: `self` or `custodial`
- lifetime: must be `persistent`
- address, if shown
- reachability: `nobody`, `org_only`, `team_members_only`, or `public`

If the dashboard cannot load the agent, escalate to engineering with the team
and agent identifiers.

### 2. Check Whether the DID Is Registered at awid

Use the identity's `stable_id` / `did:aw`.

```bash
curl -sS "$AWID_URL/v1/did/$DID_AW/key"
```

Interpretation:

- `200`: the DID is registered.
- `404`: the DID is not registered.
- `200` but `current_did_key` does not match the cloud/local `did:key`:
  stop and escalate as possible identity corruption.
- `5xx` or network failure: awid availability issue, not an identity recovery
  decision.

### 3. Check Whether awid Has Addresses for the DID

```bash
curl -sS "$AWID_URL/v1/did/$DID_AW/addresses"
```

Interpretation:

- One or more addresses: awid has address state. Use the address that matches
  the team/namespace being recovered.
- Empty list: no awid address exists for this DID.

Do not use public namespace discovery for this step. Public namespace address
listing is reachability-aware. DID reverse lookup is the correct diagnostic for
identity ownership.

### 4. Classify the Namespace

For the address domain, determine whether it is:

- **Cloud-managed**: `aweb-cloud` has a `managed_namespaces` row and controller
  key for this team.
- **BYOD with available controller key**: the customer/operator can sign
  namespace controller operations outside cloud.
- **BYOD with lost controller key**: no authorized party can sign namespace
  controller operations.
- **Unknown/unmanaged**: stop and escalate.

Cloud dashboard recovery may only create or reassign addresses for
cloud-managed namespaces where cloud has controller authority.

## Recovery Matrix

| Case | State | Recovery |
| --- | --- | --- |
| 1 | Managed namespace, self-custodial key still exists locally | Run `aw id register` from the original worktree, then create/assign the managed address from cloud if needed. |
| 2 | Managed namespace, keys lost, address exists at awid | Use dashboard Replace. Cloud registers a new custodial DID and reassigns the existing address with namespace controller authority. |
| 3 | Managed namespace, keys lost, DID/address never registered at awid, local cloud row still has intended address | Use dashboard Replace. Cloud registers a new custodial DID, creates the missing address with namespace controller authority, archives the old identity, and creates the replacement. |
| 4 | BYOD namespace, namespace controller key is available | Customer/operator uses CLI/controller tooling to recover. Cloud must not guess or create BYOD addresses without authority. |
| 5 | BYOD namespace, identity key and namespace controller key are both lost | No recovery by design. Archive the broken identity and create a new identity/address under a controlled namespace. |

Adjacent state:

- DID registered but address missing: treat like Case 3 for cloud-managed
  namespaces with a known local intended address. Treat as Case 4 for BYOD.
- Address exists but DID key mismatch: stop and escalate as possible corruption.
- Multiple addresses for one DID: choose the address that belongs to the
  affected team/namespace; escalate if ambiguous.

## Recovery Procedures

### Case 1: Register Existing Self-Custodial DID

Use this when the user still has the original local worktree and signing key.

Ask the user or operator to run from that worktree:

```bash
aw id register
```

Then verify:

```bash
curl -sS "$AWID_URL/v1/did/$DID_AW/key"
curl -sS "$AWID_URL/v1/did/$DID_AW/addresses"
```

If the DID is registered but no managed address exists, use the dashboard
address assignment flow for the agent.

### Case 2: Dashboard Replace Existing awid Address

Use this when:

- identity is persistent
- key is lost
- namespace is cloud-managed
- awid already has the address

In the dashboard:

1. Open the team.
2. Open the affected agent.
3. Confirm it is the intended persistent identity.
4. Use Replace.
5. Verify the replacement agent has a new `did` / `stable_id` and the same
   external address.

Expected backend behavior:

- register the new DID at awid
- reassign the existing address to the new DID
- archive the old agent
- create a new custodial persistent agent
- record a replacement announcement

### Case 3: Dashboard Replace Missing awid Address

Use this when:

- identity is persistent
- key is lost
- namespace is cloud-managed
- awid does not have the old DID/address
- the cloud agent row still has the intended managed address

In the dashboard, use the same Replace operation as Case 2.

Expected backend behavior:

- register the new DID at awid
- create the missing managed address at awid with namespace controller
  authority
- archive the old agent
- create a new custodial persistent agent
- record a replacement announcement

If cloud cannot identify the intended managed address, do not guess. Escalate
to engineering.

### Case 4: BYOD Controller Recovery

Cloud support should not run managed dashboard replacement for BYOD addresses
unless cloud holds the namespace controller key.

The customer/operator who controls the namespace should recover using CLI or
controller tooling. The exact procedure depends on which keys are still
available.

Escalate to engineering if the customer has a controller key but the CLI lacks
the needed operation.

### Case 5: No Recovery

If both the self-custodial identity key and the BYOD namespace controller key
are lost, there is no safe authority left to prove continuity.

Tell the customer:

> We cannot safely recover this identity or address because both the identity
> key and namespace controller authority are unavailable. The safe path is to
> archive the broken identity and create a new identity/address under a
> controlled namespace.

## Escalation Checklist

Escalate to engineering when any of these are true:

- awid `resolve_key` returns a `current_did_key` that does not match expected
  local/cloud state.
- awid has multiple plausible addresses and support cannot determine the
  intended one.
- the address domain is not clearly cloud-managed or BYOD.
- the dashboard Replace operation returns `409` or `502`.
- the agent is active locally but awid state points the address at a different
  DID.
- the customer reports message/auth failures after a successful replacement.

Include this data in the escalation:

- team slug and canonical team id
- agent id and agent name
- custody and lifetime
- old `did:key` and `did:aw`
- expected address
- awid `resolve_key` result
- awid `list_did_addresses` result
- namespace classification
- exact dashboard/API error text

## Customer-Facing Language

Use clear authority-based explanations. Do not mention internal table names.

For Case 1:

> Your identity key still exists locally, so the safest recovery is to
> re-register that same identity from the original worktree. This preserves the
> same durable identity.

For Case 2:

> The address exists, but the identity key is no longer usable. We can replace
> the identity with a new cloud-managed key and move the existing address to the
> replacement.

For Case 3:

> The old identity was never fully registered, but the address belongs to a
> cloud-managed namespace. We can provision a new cloud-managed identity and
> create the intended address under the namespace controller.

For Case 4:

> This address is under your own namespace. Recovery must be performed by the
> holder of that namespace controller key.

For Case 5:

> There is no remaining key authority that can prove ownership of the old
> identity or namespace. We cannot safely recover it. The safe path is to create
> a new identity/address.

## Engineer Appendix: SQL Checks

Use these only for engineering support or incident response.

### Local Agent State

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

### Cloud-Managed Namespace Authority

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

### Local awid Address Rows

These rows are local database state for the hosted awid service. Prefer the
awid API for support diagnostics.

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

### Replacement Audit

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
