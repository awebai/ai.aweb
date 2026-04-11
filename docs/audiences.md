# Audiences — who uses aweb and why

Preliminary. Avi, Enoch, and Randy should refine these as we learn
from real users.

**Known gaps:**
- These personas are hypothetical — no real user data yet
- Audience 2 is particularly thin; we don't know what "agent platform
  builder" looks like in practice
- Missing: what specific tools/providers Audience 1 uses most
  (Claude Code vs Codex vs Cursor split)
- Missing: pricing sensitivity data for Audience 1

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

## What this means for priorities

Everything we build should serve Audience 1 first. Audience 2
features (BYOD namespaces, cross-org certificates, the identity
layer as standalone infrastructure) are the long-term vision but
premature until Audience 1 is established.

The exception: architectural decisions that serve both audiences
simultaneously (like the crypto identity migration — it serves
Audience 1 transparently while enabling Audience 2 later).
