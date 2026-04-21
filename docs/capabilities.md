# Capabilities — what aweb provides

What the product actually does. Coordinators (John, Tom, Goto) check
code against this: if we claim a capability, the code must deliver it.
If the code does something not on this list, ask whether it should be.

Preliminary. Avi and Randy should refine as the product stabilizes.

**Known gaps:**
- Not yet validated against the current codebase — some capabilities
  listed here may be partially implemented or broken during the
  migration
- Missing: which capabilities are working TODAY vs planned
- Missing: capacity limits per tier (messages/day, retention, etc.)
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
