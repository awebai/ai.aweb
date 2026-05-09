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

## Status notes — capability framing under the two-tier architecture

The architecture has a clean cut between two product tiers (see
`audiences.md`):

- **Tier 1 — Fully hosted**: AC manages namespace controller +
  team certificate keys. Customer on aweb.ai-managed namespace.
- **Tier 2 — BYOT (Bring Your Own Trust)**: customer holds
  namespace controller key + team certificate key. Customer's DNS
  asserts customer's key. AC not in namespace or team trust path.
  Includes BYOD (your own domain) bundled in.

Per-agent custody is independent within either tier per invariant
#3. There is no "custom domain with managed keys" intermediate —
that would conflate DNS sovereignty with key sovereignty, which is
the architectural mistake (Shape B in earlier analysis) explicitly
removed.

### BYOD namespaces

Land under the BYOT tier. Customer's DNS (`_awid.<domain>` TXT
record) asserts customer's namespace controller public key;
customer signs all namespace operations. The self-hosted deployment
(customer runs their own awid + aweb) works at the protocol layer
without any AC dependency. The hosted-service path operates BYOT
through the generic "create your sovereign identity and team
locally, then import to org" primitive — that primitive is the
load-bearing operational piece for BYOT customers, currently being
built per `user-journey.md` "Implementation work to align with
architecture."

### Custody modes — per-layer choice

Custody is a choice at every layer independently:

- **Namespace controller key**: customer-sovereign (BYOT) OR
  AC-managed (Tier 1).
- **Team certificate key**: customer-sovereign (BYOT) OR
  AC-managed (Tier 1).
- **Per-agent did:aw signing key**: self-custody (CLI holds the
  key) OR custodial (AC holds the key, for browser clients and
  MCP OAuth connectors).

The two product tiers fix the namespace+team layer choices
together (Tier 1 = both AC-managed; Tier 2 = both
customer-sovereign). The per-agent custody choice is independent
in either tier — a Tier 2 customer can have AC-managed agents
under their sovereign trust chain (custodial-agents-under-BYOT
is fine, because AC's authority over those agent keys is
delegated by the customer's team controller).

Customer-facing copy: "Want managed convenience? Use the
aweb.ai-managed namespace. Want your own domain? Bring your own
trust — your domain, your namespace controller key, your team
certificate. There's no 'your domain, our keys' option — that
isn't sovereignty, and we don't pretend it is."

### Cross-org team certificates

The team-certificate primitive works. Cross-org issuance —
customer in `acme.com` issuing a certificate to a party in
`partner.com` — works through the same primitives, with both
sides operating their own team certificate keys per BYOT. Both
sides hold their own keys; AC does not synthesize certs for a
customer-held team.

### Custodial agents (cloud-held signing keys for browser-based agents)

Per-agent custody at the agent layer — independent of which tier
the customer is in for namespace and team. Tier 1 customers get
custodial agents by default for ease of onboarding. Tier 2
customers can use custodial agents under their sovereign team for
browser-based clients that can't hold private keys themselves;
the authority chain runs DNS → customer's namespace controller →
customer's team controller → AC-held agent key.

### MCP OAuth connectors (Claude Desktop, ChatGPT, Cursor agents)

Built on the custodial-agents capability. Available in both tiers
for browser-based or hosted clients that can't hold private keys.
