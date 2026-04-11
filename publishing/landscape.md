# Agent-to-Agent Communication Landscape

Where aweb fits in the broader ecosystem of protocols for agent
interaction. See [a2ac.io](https://a2ac.io) for the full landscape.

## The layers

Agent interaction isn't one problem — it's several, at different
layers:

| Layer | What it solves | Examples |
|-------|---------------|---------|
| **Tool connection** | How an agent calls a function | MCP (Anthropic) |
| **Task delegation** | How one agent asks another to do work | A2A (Google), ACP (IBM → A2A) |
| **Identity + coordination** | How agents know who they are, who else is here, and what's been claimed | aweb + awid |
| **Discovery** | How agents find each other | NANDA (MIT), ANP |
| **Messaging** | How agents exchange messages asynchronously | AMTP, MCP Agent Mail |

These layers are complementary. An agent can use MCP for tools, A2A
for delegation, and aweb for identity and coordination — all at once.

## Where aweb sits

aweb provides identity and coordination:

- **Identity** (via awid): cryptographic agent identity anchored in
  DNS, with portable team certificates
- **Coordination**: tasks, claims, presence, messaging, roles —
  agents see each other and divide work
- **Trust**: signatures verify without a middleman, team membership
  is portable across organizations

aweb does not do tool connection (that's MCP) or task delegation
(that's A2A). It provides the identity and coordination layer that
both leave out of scope.

## Key protocols

### MCP (Model Context Protocol) — Anthropic
Agent-to-tool connection. How an LLM agent calls external functions
and reads external data. Widely adopted. aweb's MCP server and
channel plugin integrate with MCP — `aw` exposes coordination tools
via MCP so agents can use them natively.

### A2A (Agent-to-Agent) — Google / Linux Foundation
Task delegation between agents. An agent sends a task to another
agent and gets results back. Explicitly leaves identity, persistent
messaging, and presence out of scope. Complementary to aweb.

### ANP (Agent Network Protocol)
Decentralized protocol using DID-based identity. Shares aweb's
emphasis on cryptographic identity but takes a different approach
to discovery and messaging.

### AMTP (Agent Message Transfer Protocol)
Federated, email-inspired agent messaging. Focuses on the messaging
transport layer rather than identity or coordination.

### NANDA — MIT
Federated discovery framework. How agents find each other across
organizational boundaries.

## The open questions

See [a2ac.io](https://a2ac.io) for the full discussion. The big ones:

- **Will these protocols converge or coexist?** Different layers
  suggest coexistence. Same-layer competitors may consolidate.
- **Who provides identity?** Multiple approaches exist (awid's
  DNS-anchored DIDs, ANP's DID-based identity, platform-specific
  IDs). No standard has won.
- **How do agents discover each other across organizations?** NANDA,
  ANP, and aweb's addressing model all take different approaches.
