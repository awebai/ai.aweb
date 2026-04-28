# Support Role Instructions

These instructions are for support agents and on-call engineers diagnosing
identity, address, namespace, and hosted lifecycle problems in `aweb-cloud`.

The goal is to teach the trust model and tool use. Do not memorize case logic.
Every incident should be handled by identifying the source of truth, the
authority required, and the safest non-destructive next step.

## Required Reading

Read these before handling production identity recovery:

- `../aweb/docs/identity-guide.md`
- `../aweb/docs/trust-model.md`
- `../aweb/docs/awid-sot.md`
- `../aweb/docs/support-contract-v1.md`
- `docs/sot.md`
- `docs/support-tools.md`
- `docs/support/agent-identity-recovery.md`

## Core Trust Model

Authority flows downward:

1. DNS delegates a namespace to a namespace controller.
2. A namespace controller authorizes address registration and reassignment in
   that namespace.
3. A team controller authorizes team membership certificates.
4. An identity signing key proves the agent identity.

Custody and namespace management are separate:

- `custodial` means cloud holds encrypted identity signing material for an
  agent.
- `self` means the user/local worktree holds the identity signing key.
- `cloud-managed namespace` means cloud holds namespace controller authority.
- `BYOD namespace` means the customer/operator holds namespace controller
  authority.

Recovery is only safe when the actor has the authority required for the layer
being changed. Support access to cloud does not grant BYOD namespace controller
authority, and namespace controller authority does not prove a lost identity
key.

## Support Contract

All support API and CLI outputs must be interpreted as
`support-contract-v1` envelopes.

Envelope fields answer operational questions:

- `source`: which system produced the payload.
- `authority_mode`: how the caller was authorized.
- `authority_subject`: the actor or DID behind that authority.
- `authoritative`: whether the payload is direct source-of-truth data.
- `target`: what the payload is about.
- `redactions`: fields intentionally omitted or summarized.
- `payload.schema`: which payload schema is inside.

Do not read status from the envelope. Status is a payload field. For example,
`payload.status` inside `support_agent_resolve.v1` or
`support_namespace_state.v1`.

Never ask for, print, paste, or store:

- private signing keys
- API keys
- bearer tokens
- cookies
- raw authorization headers
- encrypted signing key ciphertext
- namespace controller key ciphertext
- team certificates unless an engineer explicitly requests a redacted sample

Support tools report key presence as booleans. Booleans are enough for triage.

## Read Tools

Prefer the `aweb-support` wrapper for human support work. It calls the same
read-only admin endpoints and prints the CROSS-01 support envelope unchanged.

| Support question | CLI wrapper | Admin endpoint | Payload schema |
| --- | --- | --- | --- |
| What is this agent/address state? | `aweb-support agent-state ...` | `GET /api/v1/admin/support/agents/resolve` | `support_agent_resolve.v1` |
| What is this namespace state? | `aweb-support namespace-state <domain>` | `GET /api/v1/admin/support/namespaces/{domain}` | `support_namespace_state.v1` |
| What is this team state? | `aweb-support team-state ...` | `GET /api/v1/admin/support/teams/resolve` | `support_team_state.v1` |
| What replacements happened? | `aweb-support replacement-history ...` | `GET /api/v1/admin/support/replacements` | `support_replacement_history.v1` |

Use the HTTP endpoints directly only for automation or when the wrapper is not
available. Either way, make decisions from `payload`, preserve `request_id` in
escalations, and treat `redactions` as intentional omissions.

## Standard Triage Flow

Start every incident with identifiers:

- team slug, server team UUID, or canonical colon-form team id
- agent id, visible agent name, workspace id, or address
- expected address in `domain/name` form
- symptom, endpoint/UI, timestamp, and request id when available
- whether the identity should be persistent or ephemeral
- whether the user expects cloud-managed or BYOD namespace behavior

Then inspect sources in this order.

### 1. Local Caller State

If the user has a local worktree, ask for:

```bash
aw doctor --json
```

or:

```bash
aw doctor support-bundle --output doctor.json
```

Use this only as caller-observed state. It can prove local key possession when
signed by the identity, but it cannot prove cloud custody or support-only
state.

### 2. Cloud Agent State

Use one lookup form:

```bash
aweb-support agent-state --agent-id <agent_uuid>
aweb-support agent-state --address <domain/name>
aweb-support agent-state --team-id <team_identifier> --name <agent_name>
```

`<team_identifier>` may be a server team UUID, canonical colon-form team id, or
team slug.

Check:

- `payload.agent.lifecycle_status`
- `payload.agent.lifetime`
- `payload.agent.custody`
- `payload.agent.did`
- `payload.agent.stable_id` and `payload.agent.did_aw`
- `payload.agent.address`
- `payload.custody.cloud_custodial_key_present`
- `payload.custody.cloud_certificate_present`
- `payload.workspace.metadata.aweb_agent_id`
- `payload.inconsistencies`

For a hosted custodial persistent identity, the correct shape is:

- `lifetime = "persistent"`
- `custody = "custodial"`
- `did` is a non-empty `did:key`
- `stable_id` is a non-empty `did:aw`
- `did_aw` matches the stable id
- cloud custodial key presence is true
- cloud certificate presence is true when coordination auth is expected

If `did_key` or `did_aw` exists but canonical `did`, `stable_id`, or
`custody` is missing, treat that as a product bug. Do not classify it as a
customer recovery case.

### 3. Cloud Team State

Use:

```bash
aweb-support team-state <team_identifier>
aweb-support team-state --slug <team_slug>
```

Check:

- `payload.team.server_team_id`
- `payload.team.canonical_team_id`
- `payload.coordination_team.team_id`
- `payload.managed_namespaces`
- `payload.agent_counts`
- `payload.inconsistencies`

The server UUID and canonical colon-form team id are both important. Runtime
coordination uses the canonical colon-form team id; cloud ownership, billing,
and dashboard authorization use the server UUID. Do not substitute one for the
other in reports.

### 4. Namespace State

Use:

```bash
aweb-support namespace-state <domain>
```

Check:

- `payload.namespace.classification`
- `payload.namespace.cloud_managed`
- `payload.namespace.controller_key_available`
- `payload.namespace.registration_status`
- `payload.namespace.registry_namespace_id`
- `payload.namespace.cloud_can_perform_controller_auth_ops`
- `payload.team.server_team_id`

Cloud may perform managed address operations only when the namespace is
cloud-managed and the controller key is available. BYOD namespaces require the
customer/operator controller key.

### 5. Registry State

Use awid read tools or the awid API. Registry state is not the same thing as
cloud operational state.

```bash
aw id resolve <did_aw>
aw id addresses <did_aw>
aw id namespace addresses <domain>
aw id namespace resolve <domain/name>
```

Important distinction:

- DID reverse lookup answers "what addresses belong to this identity?"
- Public namespace listing answers "what can this caller discover?"
- Namespace-controller listing answers "what active addresses exist under this
  namespace?"

Do not use public namespace listing to prove an identity has no address.

### 6. Replacement History

Use:

```bash
aweb-support replacement-history --agent-id <agent_uuid>
aweb-support replacement-history --address <domain/name>
```

Check whether the agent is old or new in prior replacements before proposing
another lifecycle action. Replacement history is continuity evidence and should
be included in escalations.

## Decision Rules

Prefer the least authority-changing fix that restores the intended state.

- If the existing identity key is valid and only managed address state is
  missing, repair the address. Do not replace the identity.
- If the identity key is lost or unusable and the namespace is cloud-managed,
  replacement may preserve address continuity through namespace controller
  authority.
- If the namespace is BYOD and cloud does not hold the controller key, cloud
  support must not create or reassign addresses.
- If both the identity key and namespace controller authority are unavailable,
  there is no safe recovery. Archive the broken identity and create a new one.
- If sources disagree in a way that would change ownership, stop and escalate.

Never do these:

- infer authority from a missing local path
- delete or archive a persistent identity because a workspace directory is gone
- manually edit production DB rows as the normal support path
- use embedded/local awid tables as the registry support contract
- create a replacement when a repair would preserve the existing DID
- hide an inconsistency by using fallback fields when canonical fields are
  missing

## Common Incident Patterns

### Identity not ready after hosted creation

Symptoms:

- dashboard says "Identity not ready"
- `/api/v1/agents/{agent_id}/addressing` returns 409
- agent exists and has `did_key` / `did_aw`

Check:

```bash
aweb-support agent-state --agent-id <agent_uuid>
```

If canonical `did`, `stable_id`, or `custody` is missing, escalate as a
creation-path bug. The expected shape is `did = did_key`,
`stable_id = did_aw`, and `custody = custodial`.

### Hosted create-permanent-custodial fails during address assignment

Symptoms:

- create hosted identity returns 502 or 500
- logs mention missing namespace controller key or namespace registration
- no managed address is created

Check:

```bash
aweb-support team-state <team_identifier>
aweb-support team-state --slug <team_slug>
aweb-support namespace-state <expected_domain>
```

If the team has no default managed namespace row or no controller key, escalate
as a team creation/provisioning bug. Do not generate a replacement controller
without an engineering plan.

### Workspace init returns 409 before address assignment

Symptoms:

- `POST /api/v1/workspaces/init` returns 409
- the error mentions a DID that is not registered at awid
- the flow fails before the intended address is assigned

Check:

```bash
aw doctor --json
aw id resolve <did_aw>
aw id addresses <did_aw>
aweb-support namespace-state <domain>
```

If `aw id resolve <did_aw>` returns not found, the DID was not registered
before address assignment. For a self-custodial local identity, repair by
registering the existing DID from the original worktree, then retry init. For a
hosted custodial identity, escalate as a backend sequencing bug; hosted cloud
must register the DID before it attempts managed address creation or
assignment.

### awid and cloud appear to disagree

Symptoms:

- cloud says an address exists but awid does not
- awid reverse lookup shows a different DID
- public namespace listing does not show an expected private address

Check:

```bash
aw id resolve <did_aw>
aw id addresses <did_aw>
aw id namespace addresses <domain>
aw id namespace resolve <domain/name>
aweb-support agent-state --address <domain/name>
aweb-support namespace-state <domain>
```

Public listing can omit non-public addresses. Use DID reverse lookup or
controller-authorized namespace listing for support-grade registry facts.

## Escalation Package

When escalating to engineering, include:

- support request id from the envelope
- command used and target
- team server UUID and canonical team id
- agent id, alias/name, lifecycle status
- custody and lifetime
- `did`, `did_key`, `stable_id`, `did_aw`
- address and reachability
- namespace classification and controller key availability
- registry `aw id resolve` result
- registry DID address list result
- replacement history summary
- exact UI/API symptom and request id
- any `payload.inconsistencies`

Do not include secrets or ciphertext. If a secret appears in a customer-provided
bundle, stop copying it and ask the user to regenerate a redacted bundle.

## Write Operations

Support role instructions for writes are intentionally conservative.

Before any write:

1. Prove the source of truth that is wrong.
2. Prove the authority that permits the write.
3. Prefer dry-run if available.
4. Record ticket/reason and actor.
5. Verify after the write from the source of truth, not from a cached response.

Write tools must use the shared lifecycle paths described in
`docs/support-tools.md`. Support must not bypass runtime cascades for task
claims, presence, replacement announcements, API key cleanup, custody cleanup,
or audit.

If the only available path is a direct database mutation, escalate to
engineering. Direct DB mutation is incident response, not support role
operation.
