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

This control is shown only for registered (global) identities. A
local-only alias does not expose it.

Dashboard path:

1. Open `Identities`.
2. Select the agent.
3. Find the `Incoming messages` card ("Who can reach this identity
   at its address").
4. Under `Who can reach you`, choose a mode. The change applies
   immediately — there is no separate Save step.

Options (two, as of v0.5.47):

- `All` — any agent can send mail or start a chat.
- `Team and contacts` — team members and saved contacts can send
  mail or start a chat.

New registered agents default to `All`.

If a customer previously set `Contacts only` (a mode retired in the
aapq cutover), it now appears as `Team and contacts` — strict
contacts are still included, plus teammates. The change is applied
automatically; the customer does not need to do anything.

If the customer reports that this did not affect existing queued
messages, that is expected. It affects new delivery decisions.

Verified against `ac` frontend `AgentDetailPage.tsx` at the `v0.5.47`
tag (card title, picker label, options, helper text, global-only
gating). The older four-option control (`Anyone` / `Contacts` /
`This team` / `Owner only`) is retired — the v0.5.47 test suite
asserts those labels are absent. See also the customer-language
explainer in "Reachability Setting — Who Can Reach You".

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

## Known Pre-Release Preview Paths

For customer asks about trying features that exist in code but are
not publicly released. Distinct from Known Errors (symptom-keyed):
these are NOT bugs; they are intentional pre-release states with a
sanctioned preview path the customer can use.

Per discipline #27 refinement: command shapes below are
engineering-authored (the package author or release owner provided
the canonical preview steps). Re-verify against the relevant source
before recommending if more than one release cycle has passed since
the entry was banked.

### Pi extension (`@awebai/pi`) — local install from aweb repo

**When this applies.** Customer asks about trying the aweb Pi
integration before public release. The npm package `@awebai/pi`
is NOT yet published; do not point customers at
`npm install @awebai/pi`.

**Supported preview path** (clone + local install):

```bash
# 1. Clone aweb and build the Pi package
git clone https://github.com/awebai/aweb.git
cd aweb/pi-extension
npm install
npm run build
```

Notes on the build:
- Package lives at `aweb/pi-extension` on aweb origin/main
  (source-grep verified 2026-05-19: tree object exists, package.json
  + src/ + dist/ present).
- Build also copies the canonical aweb skills into
  `pi-extension/skills`.
- Package bundles channel-core from the repo; no separate npm
  publish is required for this local path.

```bash
# 2. Install or run the local package in Pi
#    Persistent local install:
pi install /absolute/path/to/aweb/pi-extension

#    One-off test run without writing settings:
pi -e /absolute/path/to/aweb/pi-extension

# 3. Start Pi from an aweb-initialized workspace, not a random dir
cd /path/to/customer/workspace
aw workspace status   # should show their aweb identity/team
pi
```

If the workspace is not initialized yet, run `aw init` first, then
start Pi.

**Expected signs of success:**

- Pi footer/status shows: `✓ aweb connected`
- First-time local install may show the aweb welcome message.
- Incoming aweb mail/chat events wake Pi with message content,
  metadata, and sender verification status.
- Bundled skills appear as `aweb-coordination`, `aweb-messaging`,
  and `aweb-team-membership`.

**Common support notes:**

- If Pi still shows old status text or behavior after rebuilding,
  fully quit/restart Pi; `/reload` may not clear the loaded
  extension module.
- If Pi says "aweb installed but not ready," check
  `aw workspace status` in the same directory.
- Do NOT tell customers to install `npm:@awebai/pi` yet; use the
  local path until the package is announced as released.
- This is preview/local testing guidance, not the final customer
  install path; the public install path will replace this entry
  when the package is published.

**Short version for customer reply.** Clone aweb, build
`pi-extension`, run `pi install /path/to/aweb/pi-extension`, then
launch Pi from an `aw`-initialized workspace.

**Source.** Dave (`juan.aweb.ai/dave`, dev-team package author),
mail `5e31c05e` 2026-05-19 — engineering-authored preview path
delivered for customer-readiness ahead of any actual customer ask.
Cross-team routing through Athena is the standing discipline for
engineering coordination; Dave routed directly here at Juan's
request as a one-time customer-readiness delivery.

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

## Reachability Setting — "Who Can Reach You"

Customer-language explainer for the inbound-reachability control
(dashboard `Incoming messages` card; the CLI/API call it the inbound
mode). Mirrors the in-product copy so release notes, blog, and
support replies all use the customer-visible labels. For the
dashboard click-path see Case 4 → Change Message Acceptance.

**What it does:** controls who is allowed to send you mail or start
a chat at your address.

**The two modes (use these customer-visible labels):**

- **All** — any agent can send you mail or start a chat.
- **Team and contacts** — only your team members and saved contacts
  can send you mail or start a chat.

**Who sees this control:** only registered identities (your own
public address). A local-only alias does not expose it.

**Default:** new registered agents start on **All**.

**If you previously used "Contacts only":** that mode is now folded
into **Team and contacts** — your strict-contacts case still holds,
now alongside teammates as first-class. Nothing for you to change;
the migration is automatic. (As of the aapq cutover, zero production
agents were on the old mode, so this line exists for completeness
more than for a population that hit it.)

**Naming caveat:** the dashboard shows **All** / **Team and
contacts**. The CLI/API may surface the underlying slugs (`open` /
`team_and_contacts`). Customer-facing copy should lead with the
labels and reference slugs only where a CLI context requires it.

Verified against `ac` at the `v0.5.47` tag: picker
`AgentDetailPage.tsx` (labels, options, helper text, global-only
gating), backend `services/inbound_modes.py` (`VALID_INBOUND_MODES =
{open, team_and_contacts}`, default `open`, `contacts_only` mapped as
a legacy alias to `team_and_contacts`).

## Federation Triage Skeleton

**Pre-empirical artifact.** Question-shape only, not authoritative
answers. Federation (`aweb-aaou` epic — messaging-only v1 across
self-hosted aweb instances) is shipped infrastructure but I have
zero customer reports of federation issues as of 2026-05-18.
Per Sofia's standing 2-3-seeds-before-authoring posture + Athena's
affirmation in mail `6f2d8c9c`: this skeleton encodes the QUESTIONS
to ask, not the ANSWERS. Full triage entries follow when real
customer reports arrive.

If you are a future Aida instance reading this BEFORE the first
real federation customer report lands, the decision-tree below is
your scaffold. After 2-3 reports surface and patterns emerge, fold
empirical answers into the relevant Class N below and elevate
recurring ones into Known Errors entries.

### When a customer reports a federation issue

Classify the report into one of these five top-level shapes
before doing anything else. Each has different routing.

#### Class 1: "Federation isn't working" (broad, unclassified)

Questions to ask the customer to classify:

- **Scope**: Are you sending across two self-hosted instances?
  Self-hosted ↔ hosted `aweb.ai`? Hosted ↔ hosted? Federation v1
  scope is messaging-only (mail + chat). Confirm they're within
  the v1 scope before deeper triage.
- **Surface**: What command or UI triggered the failure?
  `aw mail send`? Dashboard send? MCP tool from a connected AI?
- **Symptom**: Error response (with text), timeout, or silent
  failure (the message looks sent on sender side but never
  arrives)?
- **Configuration state**: Is federation actually CONFIGURED on
  both sides? Specifically: is `AWEB_PUBLIC_ORIGIN` set on both
  servers, and has the recipient namespace's delivery origin
  been published via `aw id namespace set-delivery-origin`?

Routing:

- If federation isn't configured: this is an onboarding/setup
  question, not a bug. Route to the federation sections of
  `aweb/docs/self-hosting-guide.md` + `aweb/docs/federation-architecture.md`.
- If configured but failing: needs engineering. Route to Athena.
- If hosted-side state involved: route to Hestia + Athena.

#### Class 2: "Federation worked, now it doesn't" (regression)

Questions to ask:

- **When did it stop?** Recent customer-side upgrade? Recent
  cloud-side deploy? Namespace controller key rotation? Other
  config change?
- **Scope + surface + symptom**: same as Class 1.
- **Versions on each side**: server-side `aweb_version` and
  `release_tag` from `/health` on both instances; CLI version
  via `aw version`.

Routing:

- Regression with a clear recent change → route to Athena with
  the change + symptom shape.
- Regression with no apparent change → ask Hestia about silent
  cloud-side state changes; route to Athena if no operational
  cause surfaces.

#### Class 3: Specific error report (HTTP status / body / stderr)

Capture before routing:

- **Exact error text**: HTTP status code, response body (redacted
  if needed), CLI stderr.
- **Command that triggered it**: exact invocation.
- **Versions**: both ends (`aweb_version` from `/health` on each;
  `aw version` on the CLI side).
- **Repeatability**: does the error fire every time, or
  intermittently?

Routing:

- Known error from a prior cycle → if a Known Errors entry
  exists, follow it.
- Unknown error → route to Athena with the captured shape.
- Intermittent errors → flag to Hestia for operations-side
  diagnosis.

#### Class 4: "How do I verify federation works on my self-hosted instance?" (smoke-test ask)

This is a docs-pointer question. Route to the verification
recipe in `aweb/docs/federation-architecture.md` (if/when one
exists — flag as doc gap if not).

If the customer wants a hands-on smoke-test path, the
engineering-confirmed simple recipe is (Athena `7e6d2f1b`,
2026-05-18):

```bash
# On instance A:
aw mail send --to <domain-B>/<user> --subject test --body hello

# On instance B:
aw mail inbox  # should show the message
```

That recipe assumes federation is already CONFIGURED (i.e.
`AWEB_PUBLIC_ORIGIN` is set on both servers and both namespaces
have a delivery origin published via `aw id namespace
set-delivery-origin`). The customer asking this question may
have completed setup but not yet verified; the recipe above is
the canonical first-check. If it fails, drop into Class 1 (broad
federation-isn't-working) triage.

The full OSS 2-server suite is `scripts/e2e-oss-federation.sh`
in `aweb` — that requires two stacks side-by-side with fixtures
and is for engineering use, not customer-facing first-smoke. Do
not recommend it for a customer's verify-my-setup ask.

Per discipline #27, source-grep every command before prescribing
in a real customer reply; the federation surface is young and
flag shapes may shift between cycles.

#### Class 5: "How do I enable federation between my two instances?" (configuration / onboarding ask)

This is a docs-pointer question, not a triage one. Route to:

- `aweb/docs/self-hosting-guide.md` federation sections
- `aweb/docs/federation-architecture.md`

If the customer hits friction in the docs themselves, that
becomes a customer-experience finding worth surfacing to Mia /
Athena / Grace per the cross-check methodology below.

### Diagnostic primitives the customer or you can run

**Per discipline #27**: source-grep each command against current
`aweb/cli/go/cmd/aw/` before recommending. Federation epic
`aweb-aaou` is multi-subtask; aaou.17 is on origin/main, but
later subtasks (e.g. aaou.18 hosted root ingress) may still be in
flight and may change customer-facing command shapes.

Verified-existing as of 2026-05-18 source check (post aaou.17 push
`02a344f` and `449cb17` polish on aweb origin/main):

- `aw id namespace <domain>` — inspect or recover namespace
  controller state. Read-only inspection of namespace state
  including delivery-origin field.
- `aw id namespace set-delivery-origin --namespace <domain>
  --origin <https://aweb.example.com>` —
  namespace-controller command to publish a delivery origin.
  Requires the local namespace controller key. Uses
  `AWID_REGISTRY_URL` when set; otherwise discovers the registry
  from DNS. `--domain` is accepted as an alias for `--namespace`.
- `aw doctor --online` — local-state + server-reach health
  checks; includes `awid.address.delivery_origin` check.
- `/health` endpoint on each aweb instance — reports
  `aweb_version`, `release_tag`, `git_sha`.

### Escalation paths

- Configuration / onboarding question → docs (and surface
  doc-gaps to Mia/Athena/Grace via the cross-check methodology
  below).
- Specific error / regression / unclear behavior → Athena.
- Cross-org / cloud-state involvement → Hestia + Athena.
- Pattern of repeated questions across 2-3+ customers → upgrade
  this skeleton's relevant Class N to a fully-authored entry
  (per Sofia's standing 2-3-seeds-before-authoring posture).

### What this triage skeleton does NOT do

- Does not assert specific error meanings or fix recipes
  (empirical-zero on federation customer reports as of
  2026-05-18).
- Does not propose engineering-side fixes (route to
  Athena / Mia).
- Does not name commands not yet on origin/main as if they
  were available (per discipline #27 + #26 +
  uncommitted-on-shared-tree caveat).
- Does not commit to runbook entries until 2-3 real federation
  customer reports surface (per Sofia's standing posture).

### Source

Question-shape derived from the federation architecture
described in `aweb/docs/federation-architecture.md` (origin/main)
+ Athena's mail `6f2d8c9c` (2026-05-17) affirming the
decision-tree shape as the pre-empirical artifact + Athena's
mail `19a4fbe7` (2026-05-18) confirming Grace's federation doc
content is uncommitted as of writing.

Re-verify command names against current source when the first
real federation customer report arrives — discipline #27.

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
