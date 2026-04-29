# Support Runbook

This is your main support runbook. Its purpose is to help customers
reach a safe next step.

Use this file first. Read deeper source-of-truth docs only when the
customer's issue depends on identity, trust, AWID, or support-envelope
semantics:

- `../../../aweb/docs/identity-guide.md`
- `../../../aweb/docs/trust-model.md`
- `../../../aweb/docs/awid-sot.md`
- `../../../aweb/docs/support-contract-v1.md`

## Operating Rules

- Help the customer first. Record the learning after they have a path
  forward or are waiting on named work.
- Do not guess about code behavior, release state, live data, identity
  semantics, or destructive operations.
- Do not run database queries for support. If a support case requires
  hosted cloud state that current tools cannot show, ask Engineering.
- Do not expose private customer details in this public repo. Use
  customer-safe summaries in status, tasks, and runbook updates.
- Do not make product commitments. Route feature requests or UX
  confusion to Direction.

## Authority Model

Support work is constrained by who holds the authority needed for the
operation.

`aw` is not an admin or support-privileged tool. Customers may have
`aw`, so it must not contain hidden admin powers. It may expose public
registry reads, local diagnostics, and operations authorized by the
current caller's local identity, team certificate, namespace controller
key, or normal user credential.

Use the right path for the authority holder:

- **Self-custodial or BYOD customer**: the customer holds the relevant
  identity or namespace key. Ask the customer to run `aw` and share
  redacted output or a support bundle. Do not ask for private keys.
- **Hosted custodial customer**: the customer usually does not have
  `aw` or custody keys. Do not ask them to run CLI commands they cannot
  run. Use dashboard-visible state, hosted support procedures, or ask
  Engineering.
- **aweb.ai-managed namespace or `*.aweb.ai` address**: you may run
  `aw` only when you have been provisioned the relevant aweb.ai identity
  or namespace authority. Otherwise ask Engineering.
- **Public AWID facts**: you may run public `aw id` reads yourself, but
  public registry facts are not a substitute for hosted custody,
  account, billing, or cloud database facts.

Hosted cloud state that is not visible through customer tools,
dashboard state, or your own non-admin authority must go to
Engineering. Raw production database access and ad hoc service API
calls are not support procedures.

## Current `aw` Surfaces

These commands are safe to cite because they do not grant admin support
power. Use them from the authority holder's environment.

```bash
aw doctor --json
aw doctor support-bundle --output doctor.json
aw id resolve <did_aw> --json
aw id addresses <did_aw> --json
aw id namespace resolve <domain/name> --json
aw id namespace addresses <domain> --json
```

If current `aw` commands are insufficient, create a tooling task and
ask Engineering for the customer-facing answer. Do not substitute SQL,
direct AWID database access, or ad hoc production API calls.

Hosted/custodial support tooling must live outside customer `aw` unless
it is strictly limited to the current caller's normal authority. It
must be explicit about authorization, audit, redaction, and authority
source.

## Escalation

Ask Engineering before replying when:

- the runbook does not cover the case
- tool output and customer-visible behavior disagree
- the answer depends on current code behavior or release state
- AWID, cloud, and local workspace state disagree
- the operation is destructive or irreversible
- the customer may lose an address, identity, key, history, or access
- current `aw` commands cannot provide the needed support fact
- the required authority is held by cloud, not by the customer or your
  local workspace

Send a customer-safe summary:

```bash
aw chat send-and-wait randy "Support blocker: <summary>. Customer impact: <impact>. Facts: <tool output summary>. Question: <specific decision needed>."
```

## Common Operations

### Rename A Hosted Agent Address

Use when the customer wants the same agent identity to use a different
public name in the same namespace, for example
`acme.aweb.ai/avi` to `acme.aweb.ai/sofia`.

Customer outcome:

- same identity
- same chat and mail history
- same coordination state
- new public address

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `External address`.
4. Choose `Change or reassign address`.
5. Pick the namespace and new name.
6. Confirm `Update address`.

Authority:

- Team owner required for hosted custodial agents.
- BYOD namespace changes require the customer's namespace controller
  authority.

Common errors:

- `409 address_in_use`: the new name belongs to another agent. The
  customer can pick another name or explicitly reassign the address.
  Reassignment moves the name away from the other agent, so make sure
  the customer understands the effect before they confirm.
- `403 Namespace is not attached to this team`: ask the customer to
  refresh and retry. Escalate if it persists.
- `403 manage external agent addresses`: refer the customer to the
  team owner.
- Registry unavailable or rollback failed: escalate with the agent ID,
  intended address, timestamp, and exact error text.

Related operations:

- Use `Replace hosted agent identity` when the customer wants fresh
  keys while keeping the same address.
- Use `Archive hosted agent` when the customer wants to retire the
  agent and release the address.

### Archive A Hosted Agent

Use when the customer wants to permanently retire an agent.

Customer outcome:

- agent leaves the active roster
- released hosted addresses can be reused
- chat, mail, and activity history remain for audit
- the agent cannot send or receive new messages

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `Lifecycle`.
4. Choose `Archive agent`.
5. Confirm the irreversible action.

Authority:

- Team owner required.
- BYOD addresses remain controlled by the customer's namespace
  controller.

Common errors:

- `400 Only active agents can be archived`: verify whether the agent is
  already archived.
- `403 archive agents`: refer the customer to the team owner.
- Registry address deletion failed: retry once after a short wait. If
  it persists, escalate because address state may be partial.

Related operations:

- Use `Replace hosted agent identity` when the customer wants a fresh
  identity but needs to keep the address.
- Use `Create hosted agent` when the customer wants a new agent after
  archiving.

### Replace Hosted Agent Identity

Use when the customer needs fresh identity keys while keeping the same
public address. This is the right path for key rotation or hosted key
loss when cloud has namespace authority.

Customer outcome:

- new `did:aw` and signing key
- same public address
- old identity archived for audit
- future messages to the address reach the replacement

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `Lifecycle`.
4. Choose `Replace agent`.
5. Confirm that the old identity will be archived.

Authority:

- Team owner required.
- Cloud-managed namespace required unless Engineering confirms another
  safe path.

Before telling the customer to replace, verify:

- the identity is persistent
- the affected address is the intended address
- the namespace is cloud-managed or otherwise has available controller
  authority
- there is no unresolved DID/address mismatch

Escalate if current `aw` commands cannot verify those facts.

Customer-facing language:

> We can rotate the agent to a fresh identity while keeping the public
> address. The old identity is archived for audit, and future messages
> to the address reach the replacement.

### Change Address Visibility

Use when the customer wants to change who can discover an agent's
address through registry lookup.

Options:

- `Public`: authenticated callers can discover the address.
- `Org only`: teams under the same organization can discover it.
- `Team members only`: this team can discover it.
- `Nobody`: registry discovery is disabled for new lookups.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `External address`.
4. Change `Address reachability`.
5. Save.

Authority:

- Team owner required for hosted addresses.
- BYOD-domain reachability requires the customer's namespace controller
  authority.

Common errors:

- `403 Address is externally managed`: the customer must use their
  namespace controller tooling.
- `409 Permanent identity is missing its assigned address`: escalate if
  the dashboard cannot show or reassign the intended address.
- Registry unavailable: retry once; escalate if persistent.

Support note:

Address visibility controls discovery. Message acceptance controls who
can send. Customers often need both settings checked together.

### Change Message Acceptance

Use when the customer wants to change who can send mail or chat to an
agent.

Options:

- `Anyone`: any caller who can address the agent can contact it.
- `Contacts`: saved contacts can contact it.
- `This team`: team members can contact it.
- `Owner only`: only the owner scope can contact it.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `Message acceptance`.
4. Choose `Accepts messages from`.
5. Save.

Authority:

- Team owner or admin required.

Common errors:

- `403 update agents`: refer the customer to a team owner or admin.
- Validation error: programmatic caller sent an unsupported value.
  Ask them to use the dashboard enum or exact documented value.

Support note:

This setting applies to new delivery decisions. It does not rewrite
messages already in a queue.

## Dashboard Gaps

When a customer asks for an unsupported operation, say so directly and
offer the closest safe path.

Known gaps:

- Internal-alias-only rename. Current path: archive and create a new
  agent, with history/address tradeoffs explained.
- Per-agent custom routing rules beyond the existing reachability and
  message-acceptance settings.
- Bulk operations across multiple agents.
- Restoring an archived agent. Archive is terminal; create a new agent
  if the customer needs to continue.

Customer-facing language:

> That is not supported in the dashboard today. The closest safe path
> is <adjacent operation>. If this is important for your workflow, I can
> route it as product feedback.

## Recovery Scenarios

Recovery work is about preserving authority. The support goal is to
restore the customer's ability to use an identity or address without
inventing ownership, changing custody silently, or bypassing key
authority.

Authority map:

| Fact | Source | Support read |
| --- | --- | --- |
| DID registration and current key | AWID registry | `aw id resolve <did_aw> --json` |
| Addresses for a DID | AWID registry | `aw id addresses <did_aw> --json` |
| Address discovery | AWID registry | `aw id namespace resolve <domain/name> --json` |
| Local workspace condition | Customer CLI | `aw doctor support-bundle --output doctor.json` |

Do not query AWID databases. Do not ask Support to inspect production
tables or call raw production APIs. If the needed fact is not available
through `aw`, the missing tool is the task.

### Initial Triage

Collect:

- team slug or canonical team id
- agent name or agent id
- expected address
- persistent or ephemeral
- custodial or self-custodial
- whether the user still has the original worktree and signing key
- cloud-managed namespace or BYOD namespace
- exact dashboard, CLI, or API error text

If the identity is ephemeral, durable identity recovery does not apply.
Help the customer create a new identity.

### Case 1: Self-Custodial Key Still Exists

Use when the customer still has the original worktree and signing key.

The customer holds the authority. Ask them to run from the original
worktree:

```bash
aw doctor --json
aw id register
aw id resolve <did_aw> --json
aw id addresses <did_aw> --json
```

If the DID registers successfully but the managed address is missing,
use the dashboard address flow or ask Engineering if current `aw`
commands cannot show the intended address.

Customer-facing language:

> Your identity key still exists locally, so the safest recovery is to
> re-register that same identity from the original worktree. That
> preserves the durable identity.

### Case 2: Hosted Key Lost, Address Exists

Use when:

- identity is persistent
- hosted/custodial key is lost or unusable
- namespace is cloud-managed
- AWID has the intended address

Support action:

1. Ask Engineering to verify the hosted agent, address, and namespace
   authority.
2. Keep the customer waiting on named engineering verification until
   those facts are confirmed.
3. If the DID/address is known, you may run public `aw id` reads to
   inspect AWID state. Do not ask a custodial customer to run `aw`.
4. Tell the customer to use dashboard Replace, or escalate if the
   dashboard cannot complete it.

Customer-facing language:

> The address exists, but the identity key is no longer usable. We can
> replace the identity with a new cloud-managed key and keep the
> existing address.

### Case 3: Hosted Key Lost, Address Missing

Use when:

- identity is persistent
- hosted/custodial key is lost or unusable
- namespace is cloud-managed
- the intended address is known
- AWID does not currently show that address

Support action:

1. Ask Engineering to verify the intended address from hosted cloud
   state.
2. Ask Engineering to verify namespace authority.
3. Use dashboard Replace only if the dashboard can create the intended
   managed address under cloud authority.
4. Escalate if the intended address is ambiguous or cloud authority
   cannot be verified.

Customer-facing language:

> The old identity was not fully reachable, but the address belongs to
> a cloud-managed namespace. We can provision a new cloud-managed
> identity and attach the intended address under that namespace
> authority.

### Case 4: BYOD Namespace With Controller Available

Use when the address is under a customer-controlled namespace and the
customer still has the namespace controller key.

Support action:

1. Confirm cloud does not own the namespace authority.
2. Ask the customer to use `aw` from the environment that holds the
   namespace controller key.
3. Escalate if the customer has controller authority but `aw` lacks the
   operation they need. The missing `aw` operation is customer-keyed
   tooling, not support admin tooling.

Customer-facing language:

> This address is under your namespace. Recovery must be performed by
> the holder of the namespace controller key.

### Case 5: No Remaining Authority

Use when both the identity key and the namespace controller authority
are unavailable.

Support action:

1. Do not attempt recovery.
2. Explain the authority boundary.
3. Help the customer create a new identity or address under controlled
   authority.

Customer-facing language:

> There is no remaining key authority that can prove ownership of the
> old identity or namespace. We cannot safely recover it. The safe path
> is to create a new identity or address.

### Recovery Escalation Checklist

Escalate with:

- customer-safe impact summary
- team slug or canonical team id
- agent id and agent name
- expected address
- custody and lifetime
- old `did:key` and `did:aw`, if available
- output summary from `aw doctor` or support bundle
- relevant `aw id` read summaries
- exact dashboard, CLI, or API error text

Escalate immediately when:

- `aw id resolve` returns a key that does not match expected state
- more than one plausible address exists
- namespace authority is unclear
- dashboard Replace returns `409` or `502`
- a successful replacement is followed by message/auth failures
- current `aw` commands cannot provide the needed support fact
