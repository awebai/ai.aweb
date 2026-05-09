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

## Two product tiers + operational complexity

The two-audience framing above maps to who shows up by background.
The two-tier framing below maps to customer intent — what trust
arrangement they want with us. There are two clean tiers and an
operational-complexity layer that sits on top of either. The
clean cut is deliberate: it's the simplest distinction we can
communicate honestly without producing customer confusion about
what kind of sovereignty they have.

### Tier 1 — Fully hosted

AC manages the namespace controller key and the team certificate
key. Customer is on a managed namespace under aweb.ai (e.g.
`acme.aweb.ai`). AC operates as the namespace controller and the
team controller; the customer's relationship is account-shaped, not
key-shaped.

Per-agent custody within Tier 1 is the customer's choice:
custodial-by-default for ease of onboarding (AC holds the agent's
signing key); self-custody available for agents that want their
own signing path (the CLI holds the key locally). Browser-based
clients (Claude Desktop, ChatGPT, MCP OAuth connectors) are
naturally custodial because they can't hold private keys
themselves; CLI-running developer agents typically self-custody.

This is the wedge. Customer reaches "agents stopped stepping on
each other" inside five minutes. Doesn't have to think about
identity sovereignty, DNS-rooted trust, or controller keys at
first contact.

### Tier 2 — BYOT (Bring Your Own Trust)

Customer holds the namespace controller key. Customer holds the
team certificate key. Customer's DNS asserts customer's namespace
controller public key (the `_awid.<domain>` TXT record). AC is
not in the namespace or team trust path. Includes BYOD (your own
domain) bundled in — you bring your own domain because you're
bringing your own trust chain.

Per-agent custody within Tier 2 is still the customer's choice:
some agents custodial via AC for browser-based clients (the
authority chain runs from customer's DNS → customer's namespace
controller → customer's team certificate → AC-held agent key);
others self-custody for full sovereignty top-to-bottom.

The customer's relationship is key-shaped. They sign namespace and
team operations themselves. AC operates only what the customer
explicitly delegates (the per-agent custodial slice).

### Operational complexity (layered on either tier)

Multi-agent, multi-team, key rotation, DNS rotation, audit-trail
depth, cross-team conversation continuity. Layers on top of either
Tier 1 or Tier 2 — operational concerns scale with team size and
deployment maturity, independent of which trust arrangement the
customer chose.

Multi-team-agent routing resolves cleanly through the did_key
strict-walk that landed in aweb 1.20.7. Cross-team conversation
continuity works through the conversation primitive shipped in
aweb 1.20.0–1.20.7.

### The two tiers are a clean cut

There's no in-between offering. "Custom domain with managed keys"
is not a tier — it would conflate DNS sovereignty with key
sovereignty, which is the architectural mistake (Shape B in earlier
analysis) we explicitly removed. If a customer wants their domain
in the trust path, they hold the keys; if they want managed keys,
they're on the managed namespace.

Authority must not be blurred between layers. Custody is
independent per layer (per invariant #3); authority follows the
trust chain (DNS → namespace controller → team controller →
agent), not whoever happens to hold a key.

If a future customer asks for "branded experience without
operational burden" (vanity domain on AC-managed keys), that's a
signal to consider adding a third tier with honest framing about
what custody they have. Until that ask surfaces, two tiers is
the clean cut.

### Audiences and tiers blend

Audience 1 customers (developer teams) typically enter at Tier 1.
They stretch into Tier 2 (BYOT) when they want sovereignty over
their trust chain — usually because they're building a product
or company brand on top of agent coordination, or because their
ops team already manages DNS for their domain.

Audience 2 customers (agent platform builders) typically enter at
Tier 2 — they care about the protocol independent of any hosted
service. The self-hosted deployment of awid + aweb is also
available; that path exits the AC dependency entirely.

Operational complexity layers when teams scale, regardless of
tier choice.

The architecture must support both tiers correctly from the start.
Tiers aren't a sequence to ship; they're customer-intent slices of
the same architecture.

## What this means for priorities

Everything we build should serve Tier 1 first. The Tier 1 path
must be the cleanest, fastest, lowest-friction path. Get a customer
to "agents stopped stepping on each other" inside five minutes.

But the architecture must support Tier 2 correctly. BYOT customers
hit the trust-chain primitives the moment they bring their domain;
the system must operate on customer-held keys cleanly without AC
ever taking authority it shouldn't. The generic "create your own
identity and team locally, then import to org" primitive serves
both Tier 1 onboarding and Tier 2 migration of customers who came
in through the older Shape B path.

Operational-complexity capabilities (rotation, multi-team, audit)
must work for both tiers. Architectural decisions that serve both
tiers simultaneously are the right shape; decisions that benefit
one tier at the cost of the other should be reframed.
