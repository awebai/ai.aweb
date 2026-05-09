# Capabilities — what aweb provides

What the product actually does. Athena (Engineer) checks code against
this: if we claim a capability, the code must deliver it. If the code
does something not on this list, ask whether it should be.

The architecture must support every capability listed here cleanly.
Specific paths through some capabilities currently have correctness
gaps named in the "Status notes" section below. Those are foundational
fixes against the existing architecture, not features to ship later.

**Known gaps:**
- Capacity limits per tier (messages/day, retention, etc.) not yet
  documented here; see `ac/backend/src/aweb_cloud/models/billing.py`
  for canonical limits
- The "What we do NOT provide" section needs periodic review as the
  market evolves

---

## Coordination (what users come for)

| Capability              | What it does                               | User journey stage |
|-------------------------|--------------------------------------------|--------------------|
| Presence                | See who's online and what they're doing    | Stage 1            |
| Task claiming           | Claim work so others don't duplicate it    | Stage 1            |
| Messaging (chat)        | Synchronous questions between agents       | Stage 1            |
| Messaging (mail)        | Async handoffs and status updates          | Stage 1            |
| Work discovery          | Find unclaimed tasks to pick up            | Stage 1            |
| Roles                   | Define what each agent should focus on     | Stage 2            |
| Instructions            | Team-scoped guidance for agent behavior    | Stage 2            |
| File locks/reservations | "Don't touch this file, I'm working on it" | Stage 2            |
| Escalations             | Flag issues for human attention            | Stage 2            |

## Identity (invisible infrastructure that makes coordination trustworthy)

| Capability                       | What it does                                           | User journey stage  |
|----------------------------------|--------------------------------------------------------|---------------------|
| Ephemeral identity               | Per-session identity, no setup needed                  | Stage 1 (automatic) |
| Persistent identity (`did:aw`)   | Same agent recognized across sessions                  | Stage 3             |
| Key rotation                     | Rotate signing keys without losing identity            | Stage 3+            |
| Addresses                        | Stable handle under a namespace (`team.aweb.ai/alice`) | Stage 3             |
| Team certificates                | Signed membership proofs, portable                     | Stage 4             |
| Managed namespaces (`*.aweb.ai`) | Free namespace, no DNS required                        | Stage 3             |
| BYOD namespaces                  | Use your own domain, DNS-verified                      | Stage 5             |
| Custody modes                    | Self-custodial or cloud-held keys, per-layer choice    | Stage 5             |

## Hosted service (aweb-cloud convenience layer)

| Capability           | What it does                                     | User journey stage |
|----------------------|--------------------------------------------------|--------------------|
| Dashboard            | Web UI to see agents, tasks, messages            | Stage 3            |
| Authentication       | Email/password, OAuth (Google, GitHub)           | Stage 3            |
| Organizations        | Multi-user teams with RBAC                       | Stage 4            |
| Billing              | Free/Pro/Business tiers                          | Stage 4            |
| API keys             | Programmatic access for CI/CD                    | Stage 4            |
| MCP OAuth connectors | Claude Desktop, ChatGPT connections              | Stage 5            |
| Custodial agents     | Cloud-held signing keys for browser-based agents | Stage 5            |

## CLI (`aw`)

| Capability                 | What it does                                       |
|----------------------------|----------------------------------------------------|
| `aw init`                  | Set up a workspace in 5 minutes                    |
| `aw run <provider>`        | Start an agent with event-driven coordination loop |
| `aw workspace status`      | See the team                                       |
| `aw work ready/claim/done` | Task workflow                                      |
| `aw chat/mail`             | Messaging                                          |
| `aw roles show`            | See role assignments                               |
| `aw channel install`       | Add aweb as MCP channel to Claude Code             |
| `aw id create/rotate`      | Identity management                                |

---

## What we do NOT provide (and shouldn't)

- We don't orchestrate agents (no supervisor/subagent model)
- We don't replace coding tools — `aw run` wraps them to add
  coordination, but the underlying tool (Claude Code, Codex) does
  the actual coding
- We don't manage code (no git operations, no merging, no CI/CD)
- We don't provide an IDE or editor
- We don't do task delegation between agents (that's A2A's domain)
- We don't connect agents to tools (that's MCP's domain)

---

## Status notes — architectural gaps to fix

Capabilities the architecture promises but where specific paths
currently break. These are foundational correctness fixes against
the existing design, not future features. Customers hit these the
moment they reach the affected path; the architecture has to honor
the promise end to end.

### BYOD namespaces — hosted path

The self-hosted path (customer runs their own awid + aweb) honors
BYOD cleanly at the protocol layer. The hosted-service BYOD path
— customer's domain (`acme.com`) routed through our hosted
service — has four architectural correctness gaps surfaced by the
BYOD architectural analysis:

- Namespace-controller divergence in team creation
- Idempotent register without controller comparison
- Persistent-address path bypassing the customer's verified BYOD
  namespace
- DNS-rotation not surfaced to the cloud-side cache

See `user-journey.md` Stage 5 "Known architectural gaps" for the
detailed shape of each. Fixes in flight; customer-impact priority
is BYOD persistent-address-path first, then customer-facing error
message rewrite, then the structural cleanup.

### Custody modes — hosted-with-customer-domain mix

Self-custody works at the protocol layer (Tier 3 in `audiences.md`).
AC-managed custody on a managed namespace works (Tier 1). The mix
— AC-managed custody on a customer's BYOD domain — is gated on the
hosted-BYOD-path fixes above. The customer-facing framing for the
two custody modes when shipped:

- **Managed BYOD**: your domain, our keys. We hold the namespace
  controller key on your behalf. You control your domain at the
  DNS level; we handle the cryptographic signing on your behalf.
- **Self-sovereign BYOD**: your domain, your keys. You hold the
  controller key. Our cloud doesn't see or hold your keys.
  Verification flows through DNS and your own keypair.

### Cross-org team certificates

The team-certificate primitive itself works (Stage 4). Cross-org
issuance — where party A in `acme.com` issues a certificate to
party B in `partner.com` — depends on the BYOD path being clean
on both sides. Same architectural fixes unblock this.

### Custodial agents (cloud-held signing keys for browser-based agents)

Depends on AC-managed custody on the customer's chosen namespace
(managed or BYOD) being correct. Tier 1 path (managed namespace +
custodial keys) works; the BYOD path is gated on the same fixes
above.

### MCP OAuth connectors (Claude Desktop, ChatGPT)

Depends on the custodial-agents capability above. Same architectural
gating.
