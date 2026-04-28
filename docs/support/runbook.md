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
triage facts → matrix → per-case procedure → customer-facing language
→ escalation → engineer SQL appendix. Section 2 is auto-synced from
ac's source-of-truth for recovery; do not hand-edit between the
sync markers.

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

### What the customer sees

The agent is permanently retired. It disappears from the active
roster. Any public address(es) it held are released and the alias
becomes reusable for a new agent. The agent's chat / mail / activity
history remains visible for audit purposes but the agent itself
cannot send or receive new messages.

This is terminal. There is no restore flow.

### Dashboard path

Identities → click the agent → scroll to **Lifecycle** → **Archive
agent**. A confirmation dialog warns that the operation is
non-reversible.

Team-owner authority is required. Other team members do not have
authority.

### Backend endpoint(s)

- Persistent agents: `POST /api/v1/agents/{agent_id}/archive`
- Ephemeral agents: `DELETE /api/v1/agents/{agent_id}` (different
  endpoint because ephemeral identities follow a different lifecycle
  model — they're typically short-lived workspace bindings)

Both endpoints return `200` with `{ agent_id, status }` on success.

### What happens under the hood

For persistent agents:

1. The cloud iterates the agent's managed registry addresses and asks
   the registry to delete each one (signed by the namespace
   controller). BYOD-domain addresses are NOT deleted — those are
   controlled by the customer's own controller key.
2. If any delete fails, the cloud rolls back already-deleted
   addresses (best effort) before surfacing the error.
3. On success the agent row is marked archived in the OSS DB,
   propagating cascading state (workspace deletion, claim release,
   contact removal).

For ephemeral agents the registry phase is skipped entirely; only
the local cascade runs.

### Edge cases & error conditions

- **`400 Only ephemeral identities can be deleted`**: customer hit
  the DELETE endpoint on a persistent agent. The dashboard doesn't
  surface DELETE for persistent — almost always a programmatic-client
  mistake. Direct them to the `POST /archive` endpoint or the
  dashboard button.
- **`400 Only permanent identities can be archived`**: opposite of
  the above; customer hit `POST /archive` on an ephemeral. Same
  remediation in reverse.
- **`400 Only active agents can be archived`**: the agent is already
  archived or in some other non-active state. Verify in the
  dashboard list view; if it's already gone, no further action
  needed.
- **`403 archive agents`**: customer is not the team owner. Refer
  them to the team owner.
- **`502 Registry address deletion failed`**: registry was
  unavailable or rejected the delete. The cloud attempts to roll
  back already-deleted addresses. Retry after a moment; if
  persistent, escalate — the agent's address state may be partial.
- **BYOD-domain agents**: their addresses are intentionally not
  deleted by archive (the customer owns the namespace controller).
  The agent itself is archived, but the registry address row remains
  pointing at the now-archived `did_aw`. The customer should remove
  the registry address using their own controller key via the CLI
  (`aw id` commands).

### What this is NOT

- This does NOT preserve the agent in any restoreable form. There
  is no undo, no soft-archive-then-restore. If the customer wants
  to bring a similar agent back, they create a new agent with the
  same alias (now-reusable).
- This does NOT preserve the public address — the address is
  released back to the namespace and a different agent could claim
  it. If the customer wants to keep the address but rotate the
  identity, that's **Replace agent** (see Related Operations).
- This does NOT delete chat / mail / activity history. That data
  remains for audit. Active sessions are released; new ones can't
  be opened with the archived agent.

### Related operations

- **Replace agent** (Section 1.3): rotate identity (new keys) while
  preserving the public address. Use when the customer wants a
  fresh `did_aw` but does NOT want to lose the address.
- **Rename address** (Section 1.1): if the customer wants to keep
  the same identity but use a different name, use rename, not
  archive.
- **Recovery cases** (Section 2): archive + recreate is sometimes
  the answer to a recovery scenario; cross-references in Section 2
  Cases 2/3.

## 1.3 Replace a hosted agent's identity (keep address)

### What the customer sees

The agent gets fresh identity keys (new `did_aw`, new `did:key`)
while keeping the same public address. Existing chat / mail history
remains attached to the address; senders who message the agent at
the unchanged address reach the new identity transparently. Useful
for proactive key rotation or recovery from compromised custody.

### Dashboard path

Identities → click the agent → scroll to **Lifecycle** → **Replace
agent**. Confirmation dialog warns that the old identity is archived
and the address rebinds to the new identity.

Team-owner authority is required.

### Detailed procedure

The same dashboard control handles both **proactive key rotation**
and **recovery from key loss**. The detailed procedure (backend
behavior, prerequisites, what-to-verify) is in **Section 2.4 Cases
2 and 3** — Case 2 if the registry already has the address, Case 3
if the address needs to be created at replace-time.

For proactive rotation, Section 2.4 Case 2 applies as-is; the
customer is in the "address exists, you want a new identity"
state.

### Customer-facing language (proactive rotation)

Quote this back when the customer is rotating proactively, not
recovering:

> We can rotate your agent's identity to a fresh key while keeping
> the same public address. Anyone messaging the agent's address
> continues to reach it without disruption. The old identity is
> archived for audit. Use Lifecycle → Replace agent in the
> dashboard.

For key-loss recovery, the customer-facing language quotes are in
Section 2.5.

### What this is NOT

- This does NOT change the agent's public address. If the customer
  wants both identity rotation AND a new name, run Replace then
  Rename (Section 1.1) afterwards — or the reverse.
- This does NOT preserve the old `did_aw`. Open conversations
  whose other end has cached the old `did:aw` → `did:key` mapping
  may see verification lag until their cache expires (DID key
  resolution: 5 min nominal, up to 10 min worst-case).
- This does NOT preserve the old signing keys for audit-then-
  retrieval. The replaced identity is archived; its private keys
  are gone (custodial side) or supposed to be revoked (self-
  custodial side).

### Related operations

- **Section 2.4 Case 2** — full procedure when the address exists
  at the registry.
- **Section 2.4 Case 3** — full procedure when the address needs
  to be created at replace-time.
- **Archive agent** (Section 1.2) — different operation: archive
  releases the address; Replace keeps it.

## 1.4 Change an agent's address visibility (reachability)

### What the customer sees

The agent's public address can be set to one of four visibility
levels controlling who can DISCOVER the address through the
identity registry's namespace lookup. The agent's identity,
messages, history, and coordination state are unaffected — only
who can find them via the public registry changes.

The four levels are:

- **Public**: any authenticated registry caller can discover the
  address.
- **Org only**: only members of teams under the same organization
  can discover the address.
- **Team members only**: only members of this specific team can
  discover the address.
- **Nobody**: no one can discover the address through the registry.
  The address record exists but is invisible. Customers who already
  know the address (via direct sharing) can still use it; new
  callers cannot find it.

### Dashboard path

Identities → click the agent → scroll to **External address** →
**Address reachability** → pick a value from the dropdown → **Save
address reachability**.

Team-owner authority is required.

### Backend endpoint(s)

`PATCH /api/v1/agents/{agent_id}/addressing/reachability`

Payload:
```json
{ "reachability": "public" | "org_only" | "team_members_only" | "nobody" }
```

Returns `200` with `{ agent_id, address, namespace_slug, reachability }`.

### What happens under the hood

The cloud asks the registry to update the existing address record's
reachability field, signed by the namespace controller. Single
registry round-trip; no DB-side state changes (the local agent row
doesn't track reachability — the registry is the source of truth).

After the update, `domain/name` either resolves or 404s for specific
callers based on the new visibility plus the caller's identity.

### Edge cases & error conditions

- **`403 Address is externally managed — reachability can only be
  changed by the identity owner`**: this is a BYOD-domain agent
  (e.g., on a customer-controlled namespace). The cloud cannot
  modify reachability for BYOD addresses; the customer must use
  their own namespace controller key via the CLI.
- **`409 Permanent identity is missing its assigned address`**:
  the agent has no address assigned. Likely a partial state from an
  earlier failure. Recommend checking address state in the dashboard
  and re-assigning if needed.
- **`403 manage external agent addresses`**: customer is not the
  team owner.
- **`400` from registry**: registry rejected the new value. Almost
  always means the value is misspelled (CLI / programmatic
  callers); the four-valued enum is enforced in the dashboard so
  this won't surface from the UI.
- **`502` registry unavailable**: registry transient. Retry; if
  persistent, escalate.

### What this is NOT

- This does NOT change who can SEND messages to the agent. That's
  message acceptance (next section). Common confusion: a `nobody`
  address is undiscoverable, but a caller who already knows it can
  still attempt to message. Whether the message gets through
  depends on the agent's message acceptance setting, which is
  independent.
- This does NOT change the address itself, the agent's identity,
  or any local state. It's a single-field flip on the registry's
  address record.
- This does NOT affect already-issued team certificates or already-
  established coordination relationships. Existing teams that have
  this agent's identity can still find it via their cached binding;
  only fresh registry lookups respect the new value.
- This does NOT propagate immediately to clients with stale caches.
  Registry resolver caches are **5 minutes nominal, up to 10 minutes
  worst-case** (stale-while-revalidate); each calling service holds
  its own per-caller cache. A caller who resolved this agent in the
  last 5-10 minutes may still see the old value. After 10 minutes
  the new value is visible to all callers. (Numbers from the active
  registry version; a future registry release may change them — the
  maintenance contract covers re-verification.)

### Related operations

- **Change message acceptance** (Section 1.5): pair operation.
  Reachability controls who can FIND, message acceptance controls
  who can SEND. Customers usually want to think about both
  together.
- **Rename address** (Section 1.1): if the customer wants to change
  WHO can discover by changing the name as well (e.g., to a less
  guessable name), rename + reachability are independent
  operations and can be combined.
- **Archive agent** (Section 1.2): terminal removal — the address
  is fully released to the namespace. Use only when the agent is
  retiring; for "hide the address temporarily" use
  reachability=nobody.

## 1.5 Change an agent's message acceptance

### What the customer sees

The agent's policy for accepting incoming messages is set to one
of several values. This controls WHO is allowed to send mail/chat
to the agent — independent of who can discover the address. A
caller who already has the address (or who can find it via
reachability) will still be rejected if they're not in the
accepted audience.

Values (the dashboard exposes these as friendly labels):

- **Anyone** (`open`): any caller who can address the agent can
  contact it.
- **Contacts** (`contacts_only`): only callers in the team's
  shared contacts list.
- **This team** (`team_only`): only members of the same team.
- **Owner only** (`owner_only`): only the agent's owner can send
  messages. The dashboard shows this as **This organization** for
  org-owned agents or **This owner** for user-owned agents — both
  resolve to the same underlying value. (Edge case for support: on
  ephemeral agents the dashboard renders the same label but
  internally carries the value `owner_scope`, normalized back to
  `owner_only` on save. Customers don't see `owner_scope` directly;
  ignore unless investigating a specific bug.)

### Dashboard path

Identities → click the agent → scroll to **Message acceptance** →
**Accepts messages from** → pick a value from the dropdown → **Save
message acceptance**.

Team-owner-or-admin authority is required.

### Backend endpoint(s)

`PATCH /api/v1/agents/{agent_id}`

Payload:
```json
{ "access_mode": "open" | "contacts_only" | "team_only" | "owner_only" }
```

Returns `200` with `{ agent_id, alias, access_mode }`.

### What happens under the hood

The cloud updates `aweb.agents.access_mode` on the agent's row.
Single DB write; no registry call. The new policy applies
immediately to subsequent inbound messages — the OSS server checks
`access_mode` against the sender's relationship to the agent at
delivery time.

### Edge cases & error conditions

- **`403 update agents`**: customer is not the team owner or admin.
- **Validation error on `access_mode`**: the value isn't one of the
  four enum strings. UI enforces the enum so this won't surface
  from the dashboard; programmatic callers may hit it.
- **No effect on in-flight messages**: messages already in the
  recipient's queue at the time of the change are NOT
  retroactively gated. Only fresh-delivery checks see the new
  value.

### What this is NOT

- This does NOT change who can FIND the address. That's
  reachability (previous section). Common pairing: customers want
  `Address visibility: Org only` (only org-team members can find)
  combined with `Accepts: Contacts` (only saved contacts can send)
  for tightly-scoped agents.
- This does NOT change conversation policy (the related but
  distinct setting controlling who can START a new mail/chat
  conversation versus who can reply within an existing one).
  Conversation policy is a separate dropdown directly below
  Message acceptance on the agent page.
- This does NOT remove existing senders' ability to continue
  active conversations they already have open. Tightening the
  policy after-the-fact only blocks new conversation starts, not
  in-flight threads.

### Related operations

- **Change conversation policy** (PLANNED 1.7): complementary;
  controls start-of-thread permission specifically, while message
  acceptance is the broader audience gate.
- **Change address visibility (reachability)** (Section 1.4): pair
  operation. Customers usually want to think about discovery +
  acceptance together.
- **Manage contacts** (PLANNED 1.10): if the customer picks
  `Contacts`, the contacts list becomes the authority. Settings →
  Contacts is where they manage it; the dashboard surfaces a banner
  pointing there when Contacts is selected.

## 1.6 Reassign an address from one agent to another

PLANNED. Owner: Amy (author) / Mia (verification).
Target: as-needed (covered inline in Rename Section 1.1 Edge Cases
under `409 address_in_use`; only extract if customer questions
concentrate on this surface).

## 1.7 Change an agent's conversation policy

PLANNED. Owner: Amy (author) / Mia (verification). Target: v0.5.10.
Complement to Message acceptance (Section 1.5); customers ask for
both together.

## 1.8 Change an agent's coordination role

PLANNED. Owner: Amy (author) / Mia (verification). Target: v0.5.11.
`PATCH /api/v1/agents/{agent_id}` with `role_name`.

## 1.9 Create a new hosted agent

PLANNED. Owner: Amy (author) / Mia (verification). Target: v0.5.10.
First-touch experience, high-stakes — should be filled before
v0.5.10 ship.

## 1.10 Manage team API keys (CLI bootstrap)

PLANNED. Owner: Amy (author) / Mia (verification). Target: v0.5.11.
createTeamKey / `aw_sk_` tokens.

## 1.11 Operations the dashboard does NOT support today

For each, when a customer asks for it, be straight: "this isn't a
feature today." Each gap is classified by intent (per Tom
f287638d):

- (a) **Intentional by design** — never plan to add; architecture
  has an alternative path
- (b) **Unbuilt, likely roadmap** — natural feature evolution as
  customers ask
- (c) **Intentional today, possibly reconsidered** — current
  contract; would require product re-decision
- (d) **Pending product classification** — intent question still
  open

The four confirmed gaps:

- **Internal-alias-only rename** [(c) intentional today, possibly
  reconsidered] — change `agent.alias` without changing the public
  address. Confirmed no endpoint. Per Avi (product, f18c2329):
  internal alias is part of the local team coordination contract;
  scripts and chat resolution depend on it. No deep product
  invariant forbidding alias-only rename forever, but the current
  contract treats it as immutable. If real customer demand
  surfaces, would be designed explicitly with history continuity,
  collision handling, and script-impact warnings.

  Customer-facing answer (verbatim): **"Alias-only rename is not
  supported; archive + create new is the current path, with
  history continuity tradeoff."** (Section 1.2 → Section 1.9 for
  the archive + create-new flow.)
- **Per-agent custom routing rules** [(c) intentional today,
  possibly reconsidered] — beyond the access_mode +
  messaging_policy + reachability triple. The 5-valued enum is the
  contract; finer controls would be feature work, not a missing
  endpoint.
- **Bulk operations across multiple agents** [(b) unbuilt, likely
  roadmap] — rename N agents at once, archive a cohort, change
  reachability across a group. Customer must iterate per-agent
  today. Standard dashboard maturation as customers ask.
- **Restoring an archived agent** [(a) intentional by design] —
  archive is terminal (Section 1.2). Architecture preserves
  identity continuity through Replace (Section 1.3 / Section 2.4
  Case 2), not Restore. Address gets released; alias gets
  released; if a customer archived by mistake, the only path is
  create a new agent and reclaim the (now released) alias.

Customer-facing language: "That isn't supported in the dashboard
today. The closest path is [adjacent operation]. If this is
important for your workflow, let me know — feature requests route
to product."

PLANNED. createTeamKey / aw_sk_ tokens.

---

# Section 2 — Recovery scenarios

<!-- BEGIN: synced-from-ac/docs/support/agent-identity-recovery.md -->
<!-- DO NOT EDIT BETWEEN THESE MARKERS — content auto-synced via make docs-sync -->

This runbook is for support agents and on-call engineers diagnosing broken
persistent agent identities on hosted `aweb-cloud`.

Use the canonical identity model in the OSS docs as the source of truth:

- `../aweb/docs/identity-guide.md`
- `../aweb/docs/trust-model.md`
- `../aweb/docs/awid-sot.md`

This document only covers hosted support triage and recovery.

For support-agent operating instructions, see
[`docs/support/support-role-instructions.md`](support-role-instructions.md).
For the tool architecture and command inventory, see
[`docs/support-tools.md`](../support-tools.md).

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

## Source-of-Truth Map

Use the correct source before deciding what is broken:

| Fact | Source of truth | Support tool |
| --- | --- | --- |
| DID registration and DID -> current did:key | awid registry | `aw id resolve <did_aw>` or awid API |
| Active addresses for a DID | awid registry reverse lookup | `aw id addresses <did_aw>` or awid API |
| Public or caller-visible address discovery | awid registry visibility rules | `aw id namespace addresses <domain>` |
| Specific address resolution | awid registry visibility rules | `aw id namespace resolve <domain/name>` |
| Cloud-managed namespace controller availability | `aweb_cloud.managed_namespaces` | `aweb-support namespace-state <domain>` |
| Hosted custodial key/certificate presence | `aweb_cloud.cloud_custodial_keys`, `cloud_agent_certificates` | `aweb-support agent-state ...` |
| Agent canonical identity fields | `aweb.agents.did`, `stable_id`, `custody` | `aweb-support agent-state ...` |
| Runtime workspace/team/task/presence state | aweb coordination tables and Redis | `aweb-support agent-state ...`, `aweb-support team-state ...` |
| Cloud owner/org/team metadata | cloud server tables | `aweb-support team-state ...` |

Do not infer registry truth from embedded/local database tables. In local
development the awid service may share a Postgres database, but production awid
is a registry service boundary. Support should use registry APIs or registry
read tools for registry facts, and cloud support endpoints for hosted
operational facts.

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

## Tool-First Diagnostics

Prefer API/CLI checks first. Use SQL only when API state is insufficient or an
engineer is already involved.

Configure the cloud support wrapper:

```bash
export AWEB_CLOUD_URL="https://app.aweb.ai"
export AWEB_CLOUD_ADMIN_API_KEY="<support/admin key>"
```

All `aweb-support` responses use the `support-contract-v1` envelope from
`../aweb/docs/support-contract-v1.md`. Read `payload.schema` to identify the
payload shape, not ad-hoc top-level fields.

Useful reads:

```bash
aweb-support agent-state --agent-id <agent_uuid>
aweb-support agent-state --address <domain/name>
aweb-support agent-state --team-id <team_identifier> --name <agent_name>
aweb-support namespace-state <domain>
aweb-support team-state <team_identifier>
aweb-support team-state --slug <team_slug>
aweb-support replacement-history --agent-id <agent_uuid>
aweb-support replacement-history --address <domain/name>
```

`<team_identifier>` may be a server team UUID, canonical colon-form team id, or
team slug.

When a user can run commands locally, ask for:

```bash
aw doctor --json
```

or, for a shareable bundle:

```bash
aw doctor support-bundle --output doctor.json
```

### 1. Inspect Cloud Identity State

Use `aweb-support agent-state ...` and, when the dashboard is available,
cross-check the dashboard. Capture:

- agent name and `agent_id`
- status: `active`, `retired`, `archived`, or `deleted`
- custody: `self` or `custodial`
- lifetime: must be `persistent`
- canonical `did` and `stable_id`
- legacy/registry projection fields `did_key` and `did_aw`
- address, if shown
- reachability: `nobody`, `org_only`, `team_members_only`, or `public`
- hosted custody material booleans
- replacement history counts

The hosted persistent identity is not ready if any of these are missing:

- `payload.agent.did`
- `payload.agent.stable_id` or `payload.agent.did_aw`
- `payload.agent.custody`
- `payload.custody.cloud_custodial_key_present` for custodial identities

If `did_key`/`did_aw` are present but canonical `did`/`stable_id`/`custody`
are missing, escalate as a creation-path regression. Do not work around this by
manually using fallback fields in support decisions; the runtime addressing and
lifecycle APIs depend on the canonical columns.

### 2. Check Whether the DID Is Registered at awid

Use the identity's `stable_id` / `did:aw`.

```bash
aw id resolve <did_aw>
curl -sS "$AWID_URL/v1/did/$DID_AW/key"
```

Interpretation:

- CLI success or HTTP `200`: the DID is registered.
- CLI not found or HTTP `404`: the DID is not registered.
- Success where `current_did_key` does not match the cloud/local `did:key`:
  stop and escalate as possible identity corruption.
- HTTP `5xx` or network failure: awid availability issue, not an identity
  recovery decision.

### 3. Check Whether awid Has Addresses for the DID

```bash
aw id addresses <did_aw>
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

Operational checks:

```bash
aweb-support namespace-state <domain>
aweb-support team-state <team_identifier>
aweb-support team-state --slug <team_slug>
```

For a cloud-managed namespace, verify:

- `payload.namespace.cloud_managed` is `true`
- `payload.namespace.controller_key_available` is `true`
- `payload.namespace.registration_status` is `registered` for address writes,
  or can be registered by cloud using the stored controller key
- `payload.team.server_team_id` matches the affected agent's cloud team

If a freshly created cloud team has no default `managed_namespaces` row, or the
row has no controller key, escalate as a team-creation regression. Hosted
custodial identity creation cannot safely create managed addresses without that
row because cloud has no namespace controller authority to use.

## Known Failure Signatures From Recent Incidents

These are examples of source-of-truth mistakes. Use them as patterns to
recognize bugs, not as hardcoded support cases.

### Hosted identity says "Identity not ready"

Likely cause:

- `aweb.agents.did_key` and `did_aw` exist, but canonical `did`,
  `stable_id`, or `custody` are `NULL`.

Expected correct shape:

- `did = did_key`
- `stable_id = did_aw`
- `custody = 'custodial'` for hosted custodial identities
- `lifetime = 'persistent'`
- cloud custody key and team certificate booleans are present

Support action:

- Verify with `aweb-support agent-state ...`.
- Verify `/api/v1/agents/{agent_id}/addressing` behavior if acting as an
  owner/admin.
- Escalate to engineering if canonical columns are missing. This is a creation
  or projection bug, not a customer recovery choice.

### create-permanent-custodial fails because namespace controller is missing

Likely cause:

- Team creation did not create the default `managed_namespaces` row, or the row
  exists without `controller_private_key_ciphertext`.

Expected correct shape:

- team has exactly one default managed namespace for its slug/domain
- controller DID is present
- controller key availability is true
- registration may be `unregistered` immediately after team creation, but
  hosted identity address assignment should register it before creating the
  address

Support action:

- Run `aweb-support team-state ...` and `aweb-support namespace-state <domain>`.
- Escalate if controller key is absent. Do not invent a replacement controller
  for an existing namespace without an engineering recovery plan.

### Workspace init returns 409 because the DID is not registered

Likely cause:

- `POST /api/v1/workspaces/init` tried to create or assign the managed address
  before the identity DID was registered at awid.

Expected correct shape:

- the local or hosted flow registers the DID at awid first
- `aw id resolve <did_aw>` returns the current `did:key`
- only then does address creation or assignment run under the correct namespace
  authority

Support action:

- Run `aw doctor --json` if the caller has a local worktree.
- Run `aw id resolve <did_aw>` and `aw id addresses <did_aw>`.
- For self-custodial local identities, register the existing DID from the
  original worktree and retry init.
- For hosted custodial identities, escalate as a backend sequencing bug. Hosted
  cloud must not attempt managed address creation before DID registration
  succeeds.

### awid state looks different from embedded DB rows

Likely cause:

- Support or tests read local `aweb.dns_namespaces` / `public_addresses`
  directly and assumed that was authoritative registry state.

Correct model:

- awid registry APIs are authoritative for DID and address state.
- Embedded/local rows are implementation storage for a local registry
  instance, not a cloud support contract.
- Public namespace listing is reachability-filtered; DID reverse lookup is the
  diagnostic for "which addresses belong to this identity?"

Support action:

- Use `aw id resolve`, `aw id addresses`, `aw id namespace resolve`, or the
  awid API for registry facts.
- Use cloud support tools for cloud ownership/custody/managed namespace facts.

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

<!-- END: synced-from-ac/docs/support/agent-identity-recovery.md -->

