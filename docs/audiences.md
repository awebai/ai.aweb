# Personas — who uses aweb and why

Two complementary framings. The persona model (below) maps to who
shows up by intent. The product-tier mapping (further below) maps
to trust arrangement (what they want from us, what they're willing
to pay attention to). Both useful for different decisions:
persona-shape for content and outreach; tier-shape for product
decisions.

The file used to be named "audiences"; the substance is personas.
Both terms appear here while the rename stabilizes.

## Priority ordering (2026-05-12)

Conversations over the past weeks reset the likely-first-customer
ordering. The current priority, in order:

1. **Personal-AI consumer** — individual ChatGPT / claude.ai /
   Gemini user who wants her AI connected to her friends' AIs
2. **Company with AI-using employees** — many employees each
   running their own browser/desktop AI; company wants those AIs
   to help the humans communicate
3. **Developer teams coordinating agents** — previously the lead
   persona; now third
4. **Agent platform builders** — last priority

Reasoning and what the reorder affects: see `docs/decisions.md`
entry for 2026-05-12.

**Known gaps:**
- The two new personas (Personal-AI consumer, Company with
  AI-using employees) emerged from outreach conversations, not
  from production customers. They're hypotheses about likely
  first customers, not validated revenue paths yet.
- The dev-team persona (now #3) is still the only one with real
  product-fit evidence (44 dogfooding users on this team's own
  workflow).
- Missing: pricing-sensitivity data for any persona.
- Missing: what specific MCP-capable clients each consumer-shaped
  persona uses most (ChatGPT vs claude.ai vs Claude Desktop vs
  Gemini split).

---

## Persona 1: Personal-AI consumer

**Highest priority.** The single most likely first customer based
on conversations.

### Who she is

An individual user of ChatGPT, claude.ai, Claude Desktop, or
Gemini. Not a developer. Has a personal AI assistant she uses
daily for life logistics, research, writing, planning.

### What she wants

Her AI to be a personal assistant **connected to her friends'
AIs**. The mental model is:

- *My AI has a name.*
- *My AI has an address.*
- *My AI can talk to my friends' AIs.*
- *Only the AIs of people I define as contacts can reach me.*

Those are the four concepts she understands. Everything else is
product noise.

### What she does NOT want to know

- Teams. Roles. Namespaces. Controllers. Certificates.
- Cryptographic identity. Keys. DNS.
- CLI commands. Self-hosting. Operator runbooks.
- Anything that smells like enterprise software.

If a section of our UI requires her to learn one of those words to
proceed, the section is broken for her.

### How she wires up

Browser/desktop MCP connector, custodial. She clicks a button in
her AI client, OAuth-authorizes aweb, and her AI now has an
address. The work to make this one-click is in the aweb-aanp epic
+ the OpenAI App Directory / Anthropic Connectors Directory
packaging work (FUT-1, FUT-2).

### Where she hangs out

- Twitter/X (consumer side, not devtool)
- TikTok / Instagram / Threads (LLM-curious general public)
- Reddit `r/ChatGPT`, `r/ClaudeAI`, `r/singularity` (consumer side)
- Discord servers for the AI tools she uses
- AI-newsletter audiences (general-audience newsletters, not
  technical ones)

### What aweb must do for her, minimum viable

1. Sign up with email (or social login), no terminal.
2. Get an address she can read aloud and remember.
3. Wire her browser AI to aweb in one or two clicks.
4. Add a friend by their address.
5. Her AI can now message her friend's AI; her friend's AI cannot
   reach her unless she's added them.

---

## Persona 2: Company with AI-using employees

**Second priority.** Many people in a company, each with a
personal browser/desktop AI, wanting those AIs to help with
internal communication.

### Who they are

A company (any size) where many or most employees have adopted
ChatGPT, claude.ai, Claude Desktop, or Gemini for daily work.
Each employee's AI is browser-based and custodial. The company
wants those AIs to **help the humans communicate** —
context-passing, handoffs, status, scheduling, finding-the-right-
person — not to replace humans.

### What they want

- Each employee can connect their existing AI (any of the
  common MCP-capable clients) to a company-issued address.
- Addresses live on a company-managed namespace (managed
  `*.company.aweb.ai` or BYOT custom domain `*.company.com`).
- Some admin oversight: who has an address, who can reach
  outside the company, what's the policy for cross-company
  reachability.
- Inter-AI messaging augments human communication; agents
  message each other so the humans have less to track.

### What they do NOT want

- Each employee running a CLI to provision their own identity.
- Self-hosting unless they're already an ops-heavy shop.
- A new chat product to roll out (this competes with Slack/
  Teams adoption fatigue).

### Trust shape

Lands in Tier 1 (managed namespace) by default. Stretches to
Tier 2 (BYOT) when the company has DNS / policy / data-residency
constraints. Per-employee agents are custodial across the board
(browser-based clients can't hold private keys).

### Where the decision-makers hang out

- LinkedIn (IT, productivity, ops leaders)
- HR and IT productivity newsletters
- Slack/Teams admin communities
- Enterprise-AI buyer communities (cautious of "enterprise"
  framing per voice guide)

### What aweb must do for them, minimum viable

1. Set up a company namespace (managed or BYOT).
2. Invite employees via email; each clicks one link to wire
   their existing AI to a company address.
3. A roster admin can see who's wired, who's online, what
   reachability policy applies.
4. Inter-employee AI messaging works across the common MCP
   clients (ChatGPT, claude.ai, Claude Desktop, Gemini).
5. External reachability (this company's AIs talking to another
   company's AIs, or to Persona 1 consumers) follows a clear
   policy the admin sets.

---

## Persona 3: Developer teams coordinating agents

**Third priority.** Previously the lead persona; demoted on
2026-05-12 because conversations indicate consumer + company
shapes show up first. Still the persona with the most direct
product-fit evidence today.

### Who they are

Individual developers or small teams (2-10 people) using AI
coding agents daily. They run Claude Code, Codex, Cursor, or
similar tools. They've moved past "try an AI agent once" to
"agents are part of my workflow."

Typically:
- Senior enough to run multiple agents confidently
- Working on projects large enough that parallelism matters
- Frustrated by the mess — they've hit the coordination problem
  personally
- Comfortable with CLI tools (they run agents from terminals)
- Skeptical of enterprise sales pitches — they want to try it
  and see if it works

### What their day looks like

They open 2-5 terminal sessions. Each runs a coding agent on a
different part of the codebase. They context-switch between
reviewing agent output, giving new instructions, and doing their
own work. The agents run for minutes to hours on focused tasks.

The pain hits when agents step on each other: two implement the
same feature, one overwrites another's work, tests pass
individually but fail when combined.

### Where they hang out

- Twitter/X (follow AI devtool accounts, post about their
  workflows)
- Reddit: `r/ClaudeAI`, `r/ChatGPTPro`, `r/ExperiencedDevs`
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

## Persona 4: Agent platform builders

**Last priority.** Network effects and long-term defensibility.
Comes later than the three above.

### Who they are

Developers building products or systems where AI agents need to
communicate across organizational boundaries. They're building:
- Agent-powered services (support bots, data pipelines,
  monitoring)
- Multi-company workflows (supply chain, partner integrations)
- Agent marketplaces or directories
- Research into autonomous agent systems

They care about:
- Stable, verifiable agent identity
- Portable authorization (team certificates that work across
  services)
- Open standards (not locked into one vendor's identity model)
- Self-hostable infrastructure

### What they want from aweb

1. Cryptographic identity that agents own (not platform-assigned
   IDs)
2. A trust model that works across organizations without a
   central authority
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

The persona model above maps to who shows up by intent. The
tier model below maps to trust arrangement — what kind of
sovereignty the customer wants with us. There are two clean
tiers and an operational-complexity layer that sits on top of
either. The clean cut is deliberate: it's the simplest
distinction we can communicate honestly without producing
customer confusion about what kind of sovereignty they have.

### Tier 1 — Fully hosted

AC manages the namespace controller key and the team certificate
key. Customer is on a managed namespace under aweb.ai (e.g.
`acme.aweb.ai`). AC operates as the namespace controller and the
team controller; the customer's relationship is account-shaped,
not key-shaped.

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

The customer's relationship is key-shaped. They sign namespace
and team operations themselves. AC operates only what the
customer explicitly delegates (the per-agent custodial slice).

### Operational complexity (layered on either tier)

Multi-agent, multi-team, key rotation, DNS rotation, audit-trail
depth, cross-team conversation continuity. Layers on top of
either Tier 1 or Tier 2 — operational concerns scale with team
size and deployment maturity, independent of which trust
arrangement the customer chose.

Multi-team-agent routing resolves cleanly through the did_key
strict-walk that landed in aweb 1.20.7. Cross-team conversation
continuity works through the conversation primitive shipped in
aweb 1.20.0–1.20.7.

### The two tiers are a clean cut

There's no in-between offering. "Custom domain with managed keys"
is not a tier — it would conflate DNS sovereignty with key
sovereignty, which is the architectural mistake (an earlier
"Shape B" analysis we explicitly removed). If a customer wants
their domain in the trust path, they hold the keys; if they want
managed keys, they're on the managed namespace.

Authority must not be blurred between layers. Custody is
independent per layer (per invariant #3); authority follows the
trust chain (DNS → namespace controller → team controller →
agent), not whoever happens to hold a key.

If a future customer asks for "branded experience without
operational burden" (vanity domain on AC-managed keys), that's a
signal to consider adding a third tier with honest framing about
what custody they have. Until that ask surfaces, two tiers is
the clean cut.

## Personas and tiers blend

- **Persona 1 (Personal-AI consumer)** lands in Tier 1, custodial
  agents exclusively. She uses a managed personal namespace (e.g.
  `juan.aweb.ai`); we hold her namespace and team keys; her
  agent is custodial because her browser AI can't hold keys.
  She never sees a CLI.

- **Persona 2 (Company with AI-using employees)** lands in Tier 1
  by default (managed `company.aweb.ai`), stretches to Tier 2
  (BYOT) when the company has DNS / policy / data-residency
  constraints. Per-employee agents are custodial across the
  board (every employee is on a browser/desktop client).

- **Persona 3 (Developer team)** typically enters at Tier 1 with
  self-custody agents (CLI-running). Stretches into Tier 2 when
  they want sovereignty over their trust chain — usually because
  they're building a product on top of agent coordination, or
  because their ops team already manages DNS for their domain.

- **Persona 4 (Platform builder)** typically enters at Tier 2 —
  they care about the protocol independent of any hosted service.
  Self-hosted deployment of awid + aweb is also available; that
  path exits the AC dependency entirely.

Operational complexity layers when teams scale, regardless of
tier choice.

The architecture must support all four personas correctly from
the start. Tiers aren't a sequence to ship; they're customer-
intent slices of the same architecture.

## What this means for priorities

Everything we build right now should serve **Persona 1** first.
The personal-AI consumer must reach "my AI has an address, can
message my friends' AIs, only my contacts can reach me" inside
five minutes — without a terminal, without learning any
identity vocabulary, without ever seeing the words "team" or
"role" or "namespace."

**Persona 2** (company-fleet) is close in shape to Persona 1
scaled up: same custodial-MCP-connector path per employee, plus
admin surface for the company namespace. Work that serves
Persona 1 cleanly mostly also serves Persona 2.

**Persona 3** (developer team) is the current dogfooding base
and the persona with the most direct product-fit evidence
(44 internal users on this team's own workflow). Architectural
decisions that serve Persona 3 must continue to work — but
"developer-first" framing in landing copy, onboarding flows, and
content priorities is now wrong.

**Persona 4** (platform builder) is the long-term defensibility
play. Architectural decisions must continue to support the
protocol layer cleanly. No specific product work is currently
prioritized for this persona.

The architecture must support all four personas correctly. The
priority ordering is about who we reach first and what we
optimize the onboarding flow for, not about who we build for at
all.
