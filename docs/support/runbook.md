# Support Runbook

Your job is to get the customer to a safe next step, then record what
we learned.

Do not ask for private keys, signing keys, session tokens, admin API
keys, database access, or unredacted secrets. Do not guess about
identity, custody, address ownership, or destructive actions.

## First Response

For every case, collect:

- what the customer is trying to do
- what happened instead
- exact error text
- timestamp and timezone
- whether they are using dashboard, `aw`, or both
- team/domain/address involved, if safe to share
- whether the customer is self-custodial/BYOD or hosted custodial

Then choose the case below.

## Case 1: Customer Has `aw`

Use this when the customer is self-custodial, BYOD, or otherwise has a
local workspace with `aw`.

Ask the customer to run commands that depend on their local workspace,
identity key, team certificate, namespace controller key, or account
session.

Customer-run commands:

```bash
aw version
aw whoami --json
aw doctor --json
aw doctor support-bundle --output doctor.json
```

For identity/address problems, ask the customer to run from the
affected worktree:

```bash
aw id show --json
aw id resolve <did_aw> --json
aw id addresses <did_aw> --json
```

For BYOD namespace problems, ask the customer to run from the
environment that holds the namespace controller key:

```bash
aw id namespace <domain> --json
aw id namespace resolve <domain/name> --json
aw id namespace addresses <domain> --json
```

You may run public registry reads yourself when the customer gives you
the target DID or address:

```bash
aw id resolve <did_aw> --json
aw id addresses <did_aw> --json
aw id namespace resolve <domain/name> --json
aw id namespace addresses <domain> --json
```

Do not ask the customer to paste private key files. The support bundle
is the shareable artifact.

## Case 2: Hosted Custodial Customer

Use this when the customer uses the dashboard/cloud product and does
not have `aw` or custody keys.

Do not ask them to run `aw`.

Ask for:

- dashboard page or flow
- exact error text
- approximate timestamp
- team slug/domain
- agent name or address
- what they expected to happen

What you can do:

- guide the customer through dashboard flows in this runbook
- run public AWID reads yourself if you have a DID or address
- ask Engineering for hosted cloud state that is not visible to the
  customer

Ask Engineering for hosted state involving custody keys, cloud-managed
namespace authority, team ownership, account status, billing, dashboard
lifecycle state, or anything that would otherwise require DB/API/admin
access.

## Case 3: Public Address Or DID Question

Use this when the customer asks whether an address resolves, which DID
owns an address, or whether a DID has registered addresses.

Tools you can run:

```bash
aw id resolve <did_aw> --json
aw id addresses <did_aw> --json
aw id namespace resolve <domain/name> --json
aw id namespace addresses <domain> --json
```

Public registry reads answer registry facts only. They do not prove
dashboard ownership, custody state, billing state, or cloud database
state. If the customer problem depends on those, ask Engineering.

## Case 4: Dashboard Operation Help

Use this when the customer wants help doing something in the hosted
dashboard.

### Rename Hosted Agent Address

Customer goal: same agent, same identity, new public address.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `External address`.
4. Choose `Change or reassign address`.
5. Pick the namespace and new name.
6. Confirm `Update address`.

Common errors:

- `409 address_in_use`: the name belongs to another agent. Customer can
  pick another name or explicitly reassign. Reassignment moves the name
  away from the other agent, so confirm they understand that.
- `403 Namespace is not attached to this team`: ask them to refresh and
  retry. Escalate if it persists.
- `403 manage external agent addresses`: refer them to the team owner.
- Registry unavailable or rollback failed: ask Engineering.

### Change Address Visibility

Customer goal: control who can discover an address.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `External address`.
4. Change `Address reachability`.
5. Save.

Options:

- `Public`: authenticated callers can discover the address.
- `Org only`: teams under the same organization can discover it.
- `Team members only`: this team can discover it.
- `Nobody`: registry discovery is disabled for new lookups.

Note: address visibility controls discovery. Message acceptance controls
who can send.

### Change Message Acceptance

Customer goal: control who can send mail or chat to an agent.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `Message acceptance`.
4. Choose `Accepts messages from`.
5. Save.

Options:

- `Anyone`
- `Contacts`
- `This team`
- `Owner only`

If the customer reports that this did not affect existing queued
messages, that is expected. It affects new delivery decisions.

### Archive Hosted Agent

Customer goal: permanently retire an agent.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `Lifecycle`.
4. Choose `Archive agent`.
5. Confirm the irreversible action.

Make sure the customer understands:

- archive is terminal
- active send/receive stops
- hosted addresses may be released
- history remains for audit

Ask Engineering if registry address deletion fails or address state
looks partial.

### Replace Hosted Agent Identity

Customer goal: fresh identity keys while keeping the public address.

Use this for hosted key loss or proactive hosted key rotation when
cloud has namespace authority.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Open `Lifecycle`.
4. Choose `Replace agent`.
5. Confirm that the old identity will be archived.

Before telling the customer to proceed, ask Engineering if you cannot
verify:

- identity is persistent
- affected address is the intended address
- namespace is cloud-managed
- no unresolved DID/address mismatch exists

Customer-facing language:

> We can rotate the agent to a fresh identity while keeping the public
> address. The old identity is archived for audit, and future messages
> to the address reach the replacement.

## Case 5: Identity Or Address Recovery

Use this when the customer lost a key, an address disappeared, a DID
does not resolve, or dashboard says an identity is not ready.

Classify first:

- self-custodial with original worktree/key available
- self-custodial with key lost
- BYOD namespace with controller key available
- BYOD namespace with controller key lost
- hosted custodial under a cloud-managed namespace

Actions:

- If the original self-custodial key exists, ask the customer to run
  `aw id register` from the original worktree, then gather `aw doctor`
  and registry read output.
- If a BYOD controller key exists, ask the customer to run `aw` from
  the environment that holds that controller key.
- If the customer is hosted custodial, do not ask them to run `aw`.
  Ask Engineering to verify hosted state and safe recovery path.
- If both identity key and namespace controller authority are lost,
  do not promise recovery.

Customer-facing language for no remaining authority:

> There is no remaining key authority that can prove ownership of the
> old identity or namespace. We cannot safely recover it. The safe path
> is to create a new identity or address.

## Case 6: Bug, Regression, Or Outage

Use this when something that should work is failing.

Collect:

- exact command or dashboard flow
- exact error text
- timestamp and timezone
- `aw version` if CLI is involved
- support bundle if CLI/local workspace is involved
- target address/DID/team, if safe to share
- whether retry changes the result

If it is a CLI/customer-workspace issue, ask for:

```bash
aw version
aw doctor --json
aw doctor support-bundle --output doctor.json
```

If it is dashboard/hosted/custodial, ask Engineering with the collected
facts. Do not infer hosted state from public AWID reads alone.

## Case 7: UX Confusion, Docs Gap, Or Feature Request

Use this when the product works as designed but the customer is
confused, blocked by missing docs, or asking for a capability we do not
have.

Do:

- answer the immediate question
- name the current closest path
- record the confusion or request in `status/support.md`
- create or route a task if it repeats or blocks success
- route product decisions to Direction

Do not promise roadmap timing.

## Escalation Packet

When asking Engineering, include:

- customer-safe summary
- customer goal
- current blocker
- dashboard vs `aw`
- exact error text
- timestamp and timezone
- team/domain/address/DID, if safe
- commands run and summarized output
- whether the customer has the relevant key/workspace
- what customer-facing answer you need

Use chat for blocking customer help:

```bash
aw chat send-and-wait randy "Support blocker: <summary>. Customer impact: <impact>. Facts: <facts>. Question: <specific answer needed>."
```

Use mail for non-urgent review:

```bash
aw mail send --to randy --body "Support needs engineering review: <summary>. Customer impact: <impact>. Proposed answer/task: <proposal>. Please confirm or correct."
```

## Feedback

After the customer has a path forward, record:

- customer-safe issue summary
- which case it was
- answer or task created
- whether the customer confirmed success
- repeated confusion or missing docs
- signal strength: strong, weak, or unknown
