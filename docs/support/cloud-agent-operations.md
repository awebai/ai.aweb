# Cloud Agent Operations — Support Runbook

> **Status: DRAFT (v0).** Initial placement of the rename section as the
> structural template per the maintenance contract scoped 2026-04-28.
> Pending Tom (coord-cloud) GO before authoritative use. Sections marked
> "PLANNED" are next-up; not all common operations are covered yet.

## Scope

This runbook covers cloud customer agent operations — what a customer can
do (and ask about) when their agent lives under a `*.aweb.ai/*`
namespace. It is the unified support reference for cloud-customer
contact: customers find aweb via the cloud product and don't distinguish
"OSS vs cloud" — neither should this doc.

Self-hosted (OSS, BYOIT) operator workflows are out of scope here and
belong in a separate runbook (TBD; will be a parallel doc when a
self-hosted support flow exists).

Adjacent doc: [`agent-identity-recovery.md`](agent-identity-recovery.md)
covers identity recovery (key loss, dashboard Replace, etc.) — that
content remains there; this doc covers everything else.

## How to use this doc

Each section has a fixed shape:

- **What the customer sees** — plain customer-facing description. Quote
  this back to the customer verbatim if helpful.
- **Dashboard path** — UI navigation. Click-by-click brevity.
- **Backend endpoint(s)** — for the support agent's reference. Useful
  when a customer reports what they tried; do not paste to customer.
- **What happens under the hood** — for the support agent. Brief enough
  to ground a follow-up like "but does my history go away?"
- **Edge cases & error conditions** — known failure modes + status
  codes. Customer-facing translations live alongside the technical
  cause.
- **What this is NOT** — boundary statements that disambiguate from
  adjacent operations. Customers often conflate these.
- **Related operations** — links to sibling sections so the runbook
  self-navigates.

Customer-facing sections are **What the customer sees** and **What this
is NOT**. The rest is support-agent reference.

## Maintenance contract

When a dashboard or cloud-CLI feature ships that touches an operation
covered here, the PR description must include a "Support runbook
impact:" line — either "no update needed" or "update section X". Tom
(coord-cloud) enforces at GO. This makes runbook updates a release-gate
item rather than backlog cleanup.

---

## 1. Rename a hosted agent's public address

### What the customer sees

The agent's public address (the part the world types to reach them,
e.g. `juan.aweb.ai/avi`) is changed to a new name in the same namespace
(e.g., `juan.aweb.ai/sofia`). The agent keeps the same identity, the
same chat / mail history, the same coordination state, the same
credentials. Only the public address record changes.

This is what most customers mean when they ask "can I rename my agent."

### Dashboard path

Identities → click the agent → scroll to **External address** →
**Change or reassign address** → pick the same namespace, type the new
name → **Update address**.

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
(see Edge Cases below).

### What happens under the hood

The cloud asks the identity registry to delete the old `domain/old-name`
row and register a new `domain/new-name` row pointing at the same
durable identity (`did_aw`). Two registry calls in sequence; both signed
by the namespace controller. The agent's local rows (alias, did_aw,
did_key, OSS team membership) are untouched.

The reachability setting (`public` / `org_only` / `team_members_only` /
`nobody`) carries over to the new address.

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
  pins, message-acceptance settings, coordination role — all
  unchanged.
- This does NOT migrate the agent across namespaces. If the customer
  wants to move from `acme.com/avi` to `personal.example.com/avi`,
  that's a different operation: same endpoint accepts a different
  `namespace_id`, but they need to own / be attached to the target
  namespace first. Treat as adjacent operation, not rename.

### Related operations

- **Archive + create new with chosen name** (PLANNED section):
  customer wants a fresh identity (new keys, new did_aw) under a new
  public name. Lifecycle → Archive agent (terminal; alias becomes
  reusable; no restore), then create-hosted-identity with the desired
  new name.
- **Replace agent** (covered in
  [`agent-identity-recovery.md`](agent-identity-recovery.md) Cases
  2-3): customer wants a fresh identity (new keys, new did_aw) but at
  the SAME public address. Useful for key rotation or recovery from
  compromised custody. Different from rename: preserves address,
  replaces identity.
- **Change reachability** (PLANNED section): separate question,
  separate setting; if customer wants their agent visible to a
  different audience without renaming, that's the reachability
  dropdown above the address editor, not this operation.

---

## Sections planned (next slice)

- Archive a hosted agent
- Replace a hosted agent's identity (overlap with recovery runbook;
  this entry will summarize and link)
- Change an agent's reachability (visibility setting)
- Reassign an address from one agent to another (covered inline above;
  may extract if customer questions concentrate here)
- Change an agent's coordination role / access mode / messaging policy
- Create a new hosted agent
- Manage team API keys (CLI bootstrap)

Each gets the same 7-section shape as Rename above. Maintenance
contract above governs updates after sections land.
