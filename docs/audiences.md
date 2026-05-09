# Audiences — who uses aweb and why

Two complementary framings. The two-audience model (below) maps to
who shows up by background (developer team vs agent platform builder).
The four-tier customer mapping (further below) maps to customer
intent (what they want, what they're willing to pay attention to).
Both are useful for different decisions: audience-shape for content
and outreach; tier-shape for product decisions.

**Known gaps:**
- Personas were hypothetical until the first real BYOD customer
  flow surfaced architectural gaps that validate the audiences
  blend across BYOD/self-custody needs
- Missing: what specific tools/providers Audience 1 uses most
  (Claude Code vs Codex vs Cursor split)
- Missing: pricing sensitivity data for Audience 1
- The Audience 1 / Audience 2 distinction is less crisp than this
  doc originally suggested — Audience 1 customers stretch into
  Audience 2 territory as they hit BYOD or self-custody needs.
  See "Four customer tiers" below.

---

## Audience 1: Developer teams coordinating agents

**Get these first.** They pay for coordination. This is the revenue
path.

### Who they are

Individual developers or small teams (2-10 people) using AI coding
agents daily. They run Claude Code, Codex, Cursor, or similar tools.
They've moved past "try an AI agent once" to "agents are part of my
workflow."

They're typically:
- Senior enough to run multiple agents confidently
- Working on projects large enough that parallelism matters
- Frustrated by the mess — they've hit the coordination problem
  personally
- Comfortable with CLI tools (they run agents from terminals)
- Skeptical of enterprise sales pitches — they want to try it and
  see if it works

### What their day looks like

They open 2-5 terminal sessions. Each runs a coding agent on a
different part of the codebase. They context-switch between reviewing
agent output, giving new instructions, and doing their own work.
The agents run for minutes to hours on focused tasks.

The pain hits when agents step on each other: two implement the same
feature, one overwrites another's work, tests pass individually but
fail when combined.

### Where they hang out

- Twitter/X (follow AI devtool accounts, post about their workflows)
- Reddit: r/ClaudeAI, r/ChatGPTPro, r/ExperiencedDevs
- Hacker News (read and occasionally post)
- Discord servers for Claude Code, Codex, Cursor
- Dev.to, personal blogs

### What they want from aweb

1. Agents stop duplicating work
2. Agents stop overwriting each other
3. Agents can see what others are doing
4. Minimal setup — don't make me learn a new framework
5. Works with the tools they already use (Claude Code, Codex)

### What they DON'T want

- A new IDE or wrapper around their existing tools
- To read about cryptographic identity before they can start
- Vendor lock-in or a hosted-only service
- Enterprise pricing or sales calls

---

## Audience 2: Agent platform builders

**Comes later.** They drive network effects and long-term
defensibility.

### Who they are

Developers building products or systems where AI agents need to
communicate across organizational boundaries. They're building:
- Agent-powered services (support bots, data pipelines, monitoring)
- Multi-company workflows (supply chain, partner integrations)
- Agent marketplaces or directories
- Research into autonomous agent systems

They care about:
- Stable, verifiable agent identity
- Portable authorization (team certificates that work across services)
- Open standards (not locked into one vendor's identity model)
- Self-hostable infrastructure

### What they want from aweb

1. Cryptographic identity that agents own (not platform-assigned IDs)
2. A trust model that works across organizations without a central
   authority
3. An identity layer they can build services on top of
4. DNS-anchored namespaces (use their own domain, not ours)
5. Open source, self-hostable, MIT licensed

### Where they hang out

- Protocol-focused communities (MCP ecosystem, A2A discussions)
- GitHub (looking at agent infrastructure repos)
- Conference talks about agent architecture
- Company engineering blogs

---

## Four customer tiers

The two-audience framing above maps to who shows up by background.
This four-tier framing maps to customer intent — what they want, what
they're willing to pay attention to. Use it for product decisions;
the audience-shape is for content and outreach.

### Tier 1 — "Make the mess stop"

"I have multiple AI coding agents on my codebase, stepping on each
other. Make it stop." Wants coordination working in five minutes.
Doesn't care about identity sovereignty or DNS-rooted trust at first
contact. Architecturally: AC managed namespace + AC managed identity
+ AC default address.

This is the wedge. The path that delivers cleanly today, end to end.

### Tier 2 — "I want my agents on MY domain"

"acme.com/alice." Either adopted aweb at Tier 1 and now wants their
brand on it, or came specifically for the cross-org identity story.
Cares about address sovereignty. Architecturally: AC managed namespace
+ AC managed identity + BYOD-domain address.

Today this fails. The architectural gaps are named in
`user-journey.md` Stage 5 known-architectural-gaps section. The
fixes are foundational, not future features — Tier 2 customers hit
these the moment they bring their own domain.

### Tier 3 — "Self-sovereign agent identity"

"I want a protocol for agent identity that doesn't depend on any
vendor." Smaller market than Tier 1-2. Ideologically aligned with
DNS-anchored cryptographic identity. Architecturally: pure CLI /
self-sovereign / no AC dependency.

Works at the protocol layer because AC isn't in the path. The
self-hosted-only deployment model honors Tier 3 cleanly.

### Tier 4 — Operational complexity

Multi-agent, multi-team, DNS rotation, custodial-vs-self-custody
choice per layer. Emerges as adoption scales — a customer in any of
Tier 1-3 hits Tier 4 questions when their team grows or their
infrastructure shifts.

Architecturally layered on top of Tier 1-3 stability. Multi-team-agent
routing now resolves cleanly through the did_key strict-walk that
landed in aweb 1.20.7. DNS rotation is named as a gap in the Stage 5
analysis.

### Audiences and tiers blend

Audience 1 customers (developer teams) typically enter at Tier 1.
They stretch into Tier 2 the moment they want their team's work to
appear under their own domain. They stretch into Tier 4 the moment
their team grows past two agents.

Audience 2 customers (agent platform builders) typically enter at
Tier 3 — they care about the protocol independent of any hosted
service. They stretch into Tier 4 immediately because they're
operating multiple platforms.

The architecture must support all four tiers correctly. Tiers
aren't a roadmap; they're customer-intent slices of the same
architecture.

## What this means for priorities

Everything we build should serve Tier 1 first. The Tier 1 path
must be the cleanest, fastest, lowest-friction path. Get a customer
to "agents stopped stepping on each other" inside five minutes.

But the architecture must support Tier 2-4 correctly, not gate them
behind a future fix schedule. The architectural gaps in Stage 5
(`user-journey.md`) are foundational correctness issues — Tier 2
customers hit them on first BYOD attempt; Tier 3 customers depend
on the protocol layer staying clean; Tier 4 customers hit derived
versions of the same gaps as their teams scale. Get the architecture
right; the alternative is paying down structural debt that will
only get more expensive as customers reach later tiers.

The exception that proves the rule: the crypto identity migration
serves Tier 1 transparently while honoring Tier 2-4 architectural
needs. Architectural decisions that serve all tiers simultaneously
are the right shape.
