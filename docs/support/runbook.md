# Support Runbook

Your job is to get the customer to a safe next step, then record what
we learned.

Do not ask for private keys, signing keys, session tokens, admin API
keys, database access, or unredacted secrets. Do not guess about
identity, custody, address ownership, or destructive actions.

## Invariants

- Customer success first. Learning comes after the customer has a path
  forward or is waiting on named work.
- Authority decides who acts. The customer runs commands that require
  their key, workspace, certificate, namespace controller, or account
  session.
- You may run public registry reads when the customer gives you a DID
  or address.
- Hosted custodial customers usually do not have `aw`; do not ask them
  to run it.
- Public AWID state is not cloud account, custody, billing, or dashboard
  state.
- If the answer depends on hosted cloud state, current code behavior,
  release state, or an irreversible operation, ask Engineering before
  replying.
- Name the answer, not the internal team-set. Tell customers "we are
  routing this to engineering," not which agents or teams handled it.
  Internal coordination shape (company team vs dev team, who bridges)
  is not customer-facing context.

## Case Router

| Customer says | Use | First action |
| --- | --- | --- |
| "I have a CLI/worktree error" | Case 1 or 6 | Ask for `aw version`, `aw doctor`, and support bundle. |
| "I use the dashboard and do not have `aw`" | Case 2 or 4 | Ask for page/flow, error, timestamp, team, agent/address. |
| "Does this DID/address exist?" | Case 3 | Run public `aw id` reads if you have the target. |
| "I want to rename/archive/replace/change visibility" | Case 4 | Guide through dashboard flow; escalate risky state. |
| "I lost a key/address/identity" | Case 5 | Classify custody and namespace authority first. |
| "Something that worked is broken" | Case 6 | Collect exact command/flow, error, time, version/bundle. |
| "This is confusing / missing / unsupported" | Case 7 | Answer current path, record learning, route if repeated. |

## Tool Matrix

| Tool | Who runs it | Use for | Does not prove |
| --- | --- | --- | --- |
| `aw doctor --json` | Customer | Local workspace, identity, team, messaging diagnostics | Hosted custody or cloud account state |
| `aw doctor support-bundle --output doctor.json` | Customer | Shareable redacted local diagnostics | Secrets, hosted custody, billing |
| `aw id resolve <did_aw> --json` | You or customer | Public DID -> current key registry fact | Cloud ownership or account authority |
| `aw id addresses <did_aw> --json` | You or customer | Public addresses registered to a DID | Dashboard state or billing |
| `aw id namespace resolve <domain/name> --json` | You or customer | Public address resolution | Hosted custody or team ownership |
| Dashboard | Customer | Hosted account-visible actions | BYOD controller authority |
| `aw chat` / `aw mail` to Engineering | You | Code/cloud/release/authority questions | Customer confirmation |

## Reference Map

Read deeper docs only when the case needs them:

| Doc | Use when | How to treat it |
| --- | --- | --- |
| `support-role-instructions.md` | You need the trust model, source-of-truth map, or support envelope vocabulary | Reference only; the runbook decides support actions. |
| `agent-identity-recovery.md` | Identity/address recovery is subtle or Engineering asks for a structured escalation | Do not run SQL or DB procedures from it. Use it to understand authority and shape the escalation. |
| `release-readiness.md` | A case depends on a lifecycle/support release or rollout state | Check shipped state and verification expectations. |
| `admin-write-tools.md` | Engineering asks about admin write review | Engineering background, not a support procedure. |
| `agent-lifetime-support-epic.md` and coverage/audit docs | You need task history or invariants behind support capabilities | Background only. Active work belongs in `aw` tasks. |
| `../../../aweb/docs/identity-guide.md`, `trust-model.md`, `awid-sot.md` | You need identity, namespace, team, DID, or AWID semantics | Source-of-truth model docs. |

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

## Known Errors

A symptom-keyed lookup. If a customer's exact error string matches an
entry here, route the corresponding answer directly. If the symptom is
close but not exact, escalate per the case rules above rather than
guessing.

### `aw claim-human` returns 422 on a BYOD domain

**When this applies.** Customer runs `aw claim-human --email <email>`
against a BYOD domain (a non-`.aweb.ai` namespace) and gets HTTP 422.
The error body matches one of:

```json
{"detail": [{"type": "missing", "loc": ["body", "username"], "msg": "Field required", ...}]}
```

```json
{"detail": [{"type": "string_too_short", "loc": ["body", "username"], "msg": "String should have at least 1 character", ...}]}
```

Both shapes share `"loc": ["body", "username"]` — that's the
grep-friendly anchor.

**Why this happens.** Intentional contract tightening, not a bug. The
new `aw claim-human` (server commit `98cfc278`; client commit
`443151d`) requires an explicit `--username` flag for BYOD users. Old
`aw` versions either omitted `username` (Case A: missing field) or
auto-inferred the BYOD domain into it (Case B: empty/invalid string);
both fail server-side validation against the new schema. Hosted users
(`*.aweb.ai`) on old `aw` still work because the legacy client derived
the username from the managed domain.

**Customer-facing answer.** Confirm they are on a BYOD domain
(their workspace's coordination URL / cert is for a non-`.aweb.ai`
namespace), then offer either:

- **Upgrade `aw`** to a release that includes client commit
  `443151d`, and re-run with `--username <their-dashboard-username>`
  passed explicitly; or
- **Pass `--username` explicitly** if their current `aw` already
  supports the flag:
  `aw claim-human --email <email> --username <their-dashboard-username>`.

The dashboard username is the one they pick when claiming the team —
for a team `acme.com/<team>`, the username is the local-part identifier
they want, not derivable from the BYOD domain.

**Why the message looks ugly.** The 422 is FastAPI's generic Pydantic
v2 validation envelope, not a domain-specific upgrade-prompt. Hosted
users are unaffected; BYOD users can read the validation message;
engineering chose not to ship a dedicated upgrade-prompt path at
current scale. If volume on this support route grows, route a signal
to Engineering and Direction — that is the threshold for revisiting.

**Source.** ac commit `98cfc278`, aweb commit `443151d`, Mia's runbook
entry mail `f393168c` (2026-05-02), Athena's review mail `df41abbc`
finding #3. Captured 422 envelopes were verified against the
production schema by Mia on 2026-05-02.

## Customer Orientation Responses

For open-ended customer questions that are NOT errors — orientation,
"what next," routing — that the customer asks after finishing a
tutorial or completing setup. Distinct from Known Errors above (which
are symptom-keyed) and from Cases 1-7 (which are bug/recovery-shaped).

Each response below carries the empirical-verification trail at the
end. **Per discipline #27**: every action-command was source-grep
verified against current `aweb/cli/go/cmd/aw/` at draft time; if a
release wave lands, re-verify before using (especially commands that
took role / workspace / identity flags — those are the surfaces
that change). The verification date is in each entry's Source line.

### "I finished the CLI tutorial — what should I try next?"

**When this applies.** Customer completed the CLI tutorial
(`introduction.md`, `cli-tutorial.md` once published, or similar)
and reaches out via the support-aida path the tutorial points them
at: `aw chat send-and-wait aweb.ai/aida "..."`. The question is
open-ended ("what should I try next?", "what's the next step?",
"where do I go from here?"). Not an error; orientation-shaped.

**Response template** — three buckets, in this order:

1. **Action tier** (one concrete next thing to do, ~10-15 minutes):

   ```
   aw workspace add-worktree --alias <name>
   ```

   Gives the customer a second agent in a sibling worktree, both
   sharing the same team. The aha moment for CLI users is usually
   "two agents I can see each other" not just "I exist on aweb."

   **DO NOT** recommend `aw workspace add-worktree developer` (or
   any role-positional shape) without first checking whether the
   customer's team has that role in its bundle. Post-aweb-1.22.0,
   hosted aweb.ai teams ship with an EMPTY roles bundle by default
   (per agent-guide.md F16 / OSS-vs-hosted distinction). Passing
   a role that isn't in the bundle 400s or silently confuses. Use
   `--alias <name>` form unless you've confirmed the role exists.

2. **Depth-reading tier** (3-4 docs, ordered by likely usefulness):

   ```
   https://aweb.ai/docs/coordination/   — work, claims, locks
   https://aweb.ai/docs/communication/  — mail vs chat, contacts, reachability
   https://aweb.ai/agent-guide.md       — full primitive reference
   ```

   `coordination` and `communication` are the most-used surfaces for
   CLI customers building real workflows. The agent-guide is the
   reference; long-form, deeper than the customer needs in the first
   day but useful as a hub for "what else is there."

3. **Optional — dashboard bridge** (when the customer wants to link
   a human account later):

   ```
   aw claim-human --email you@example.com
   ```

   Bridges a CLI-created team to the hosted dashboard without
   changing identity. For BYOD customers (their workspace is on a
   non-`.aweb.ai` namespace), also pass `--username
   <dashboard-username>` explicitly — see the BYOD-422 Known Errors
   entry above for the wave context.

**Invitation to narrow.** Close every "what next" response with:

> "What was your goal with aweb? If you tell me what you're trying
> to build I can narrow the next step rather than handing you the
> whole landscape."

The invitation IS the value-add. The three buckets above are the
fallback when the customer hasn't told you their goal yet; once
they share it, the answer narrows to the specific path that fits
(messaging-focused → emphasize `communication`; task-coordination
→ emphasize `coordination` + `aw task`; multi-machine → BYOIT flow
via `aw id team request`/`add-member`/`fetch-cert`).

**What this response does NOT do.**

- Does not recommend `aw run claude` (sunsetting; channel plugin is
  recommended for Claude Code). `aw run codex` only if customer is
  specifically on Codex.
- Does not recommend any role-bearing command without first
  verifying the customer's team has that role.
- Does not promise specific dashboard features without verifying
  current cloud state (the dashboard ships frequently; check
  `status/operations.md` for live state if making claims).

**Source.** Action-command source-grep verifications (current as of
2026-05-16):

- `aw workspace add-worktree --alias <name>`: confirmed in
  `aweb/cli/go/cmd/aw/workspace.go:33` (`Use: "add-worktree [role]"`,
  `Args: cobra.RangeArgs(0, 1)` — role positional optional;
  `--alias` flag at line ~initialized in `init()`).
- `aw claim-human --email <email> [--username <name>]`: confirmed
  in `aw claim-human --help` output; `--username` flag described as
  "Override the default dashboard username derived from the
  registered domain."
- Hosted docs URLs `/docs/coordination/` and `/docs/communication/`:
  confirmed exist as Hugo-rendered pages from
  `ac/site/content/docs/coordination.md` + `communication.md`.
- Hosted reference URL `https://aweb.ai/agent-guide.md`: confirmed
  served from `ac/site/static/agent-guide.md` (root-relative
  static-folder serving; synced from `aweb/docs/agent-guide.md`).
- Post-1.22.0 role-empty-bundle context: per Athena's mail
  `05dae217` (2026-05-16), confirmed by `aweb` commit
  `9035252` ("fix(roles): aw roles show handles empty bundle without
  400").

Seed example #1: `gracetut194441.aweb.ai/alice` (2026-05-16,
captured via tutorial-walkthrough by Grace). Triggered the
discipline #27 banking and shaped this entry's "DO NOT recommend
role-positional without confirmation" guard.

**Tied to docs-system invariants.** This response template assumes:
the customer-facing docs at `/docs/*` are kept current per the
Athena/Mia inventory pass (Wave 1 + Wave 2); commands referenced
here remain source-grep accurate; the welcome guide v5 in
`ac/backend/src/aweb_cloud/resources/welcome.md` defines the
customer-facing tool vocabulary. If any of those invariants
breaks, this entry needs re-verification.

## Customer-Content Cross-Check Methodology

When asked to cross-check customer-facing content surfaces (e.g.,
skills vs this runbook, this runbook vs `/docs/*`, two
overlapping runbook entries), apply this methodology. Derived from
the Item 1 skills-vs-runbook cross-check (2026-05-17, Athena
relayed from Olivia + Dave); banked here per Athena's discipline-
credit framing in mail `e91e264f`.

### Read all the files first

Read each surface fully before drafting findings. Skim-then-claim
produces wrong-premise findings (the kind that fire on docs
already aligned with a recent cleanup the cross-checker didn't
know about).

### Build a surface-map table

For each policy or decision that appears on multiple surfaces,
name which surface is canonical. Use the table structure:

| Overlap | Canonical surface | Why |

That's the artifact the cross-check should produce. Future
authors reading the table know where to put new content of each
shape.

### Restating-enough-to-drift threshold

When one surface points at another canonical surface, the pointer
may carry a contextual anchor (one-line domain-specific reminder)
without becoming a restatement. The threshold: does the pointer
**direct attention** or **enumerate the policy**? Direct-attention
form: "in coordination contexts, default to mail; chat only when
a teammate is blocked." Enumerate-policy form: re-listing the full
mail-use-case bullets. The first is below the drift threshold; the
second isn't.

When in doubt, lean toward direct-attention. The canonical surface
is one click away; the pointer surface shouldn't try to be
self-sufficient.

### Parallel-correct surfaces exception

Don't force canonical-per-overlap dogmatically. Two surfaces that
independently apply the same root claim — in different contexts,
without cross-surface dependency — are sometimes the cleaner
shape than forcing one canonical and creating a dependency that
adds little value.

Example: F16 roles-are-opt-in framing lives canonically in
`aweb/docs/agent-guide.md` (the root claim). The aweb-coordination
skill applies it as "if the role bundle is empty, continue using
normal task and messaging discipline." This runbook applies it as
"DO NOT recommend `aw workspace add-worktree developer` without
verification." Both correct, no cross-surface dependency. Banking
them as parallel-correct rather than forcing one canonical is
right.

### Customer-bridge verification step

After any change to a canonical surface, verify that the
customer-bridge paths in this runbook still route correctly.
Specifically: do the depth-reading URLs in any
"Customer Orientation Responses" entry still hit content equivalent
to the canonical-after-change?

If the bridge stays intact, no runbook edit needed. If the bridge
breaks (e.g., a canonical doc renamed; a policy moved to a
different surface; a customer-facing URL retired), the runbook
entry's depth-reading bucket needs updating.

The customer-bridge step is what makes cross-check work
support-shaped rather than purely-engineering-shaped. The
question isn't "is the policy still correct somewhere" but "does
the customer still find the policy via the path I told them about."

### Scope-shape for where the cross-check artifact lives

This runbook is the right host for **customer-orientation
response templates** and **the cross-check methodology used to
keep them coherent**. It is NOT the right host for
**cross-surface authoring-discipline artifacts** like
`skills/POLICY-SOURCES.md` (banked separately in the OSS skills
tree per Athena 2026-05-17). Rule of thumb: if the artifact
serves customer-orientation, it lives here; if it serves
skill-authors or doc-authors, it lives at their surface.

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
aw chat send-and-wait athena "Support blocker: <summary>. Customer impact: <impact>. Facts: <facts>. Question: <specific answer needed>."
```

Use mail for non-urgent review:

```bash
aw mail send --to athena --body "Support needs engineering review: <summary>. Customer impact: <impact>. Proposed answer/task: <proposal>. Please confirm or correct."
```

## Feedback

After the customer has a path forward, record:

- customer-safe issue summary
- which case it was
- answer or task created
- whether the customer confirmed success
- repeated confusion or missing docs
- signal strength: strong, weak, or unknown
