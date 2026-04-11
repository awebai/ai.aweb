# aweb Strategy

**Known gaps:**
- Pricing in this doc ($25/$250) doesn't match what's live ($49/$149)
  — needs reconciliation
- The execution timeline ("items 1-5 are this week") was written
  weeks ago and hasn't been updated against reality
- The collision video is called "highest priority single asset" but
  hasn't been produced — needs a decision: still the right priority
  vs the blog post?

## Context

aweb is a coordination platform for AI coding agents with cryptographic
identity. The engineering is solid. The identity model is genuinely novel.
But the market doesn't know it needs this yet.

The challenge is not building the product. The challenge is making the
problem visible, getting the first real users, and surviving long enough
for the multi-agent world to arrive.

Three risks shape this strategy:

- **Platform risk**: Anthropic, OpenAI, Google could build native
  coordination. The defense is vendor neutrality and the identity layer.
- **Timing risk**: Most developers aren't running multi-agent teams yet.
  Early adopters exist today; mainstream is 12-18 months out.
- **Complexity risk**: The full identity model (ephemeral/permanent,
  custody modes, TOFU, DID, namespaces) is too much for first contact.
  The entry point must be radically simple.

---

## Pillar 1: Make the problem visible

People don't buy coordination infrastructure. They buy a fix for the mess
their agents made. Every piece of outreach starts with the mess, not the
architecture.

### Actions

**The collision video** (highest priority single asset)

Record 3 uncoordinated agents on the same codebase. Show the duplicate
work, the conflicting edits, the wasted cycles. 2 minutes max. End with
"what if they could talk to each other?" and a link.

Post to Twitter/X, Reddit r/ClaudeAI, r/ChatGPTPro. The problem video is
more shareable than a product demo.

**Problem-first content**

Write about what goes wrong with multiple agents, not about aweb's
architecture:

- "I ran 5 Claude Code agents on my codebase for a week. Here's what
  went wrong."
- "The multi-agent coordination problem nobody's talking about"
- "Why your AI agents need identity (and what happens without it)"

These are shareable by people who haven't used aweb. They create awareness
of the problem category. aweb is positioned as the thing the author built
to fix it.

**Join existing conversations**

Don't create the conversation. Find where it's already happening:

- When someone tweets about running multiple Codex/Claude instances,
  reply with experience and a screenshot of coordinated agents.
- When someone posts about agent-to-agent communication on Reddit, share
  what you've learned.
- Find YouTube creators doing multi-agent content and offer tooling for
  their next video.

Target: engage in 5 existing conversations per week on Twitter/X and
Reddit. Don't spam links. Share experience. Be the expert in the room.

**Build in public**

The fact that aweb is built using aweb (agents coordinating via the
platform they're building) is a strong story. Post real agent-to-agent
chat logs, coordination screenshots, conflict resolution moments. This
content is novel -- nobody else is showing it.

**Direct outreach**

Find 3-5 specific people running multi-agent setups publicly. DM them
with a personal offer: early access, hands-on setup help, and a genuine
interest in their workflow. These become the first design partners and,
if it works, the first testimonials.

### What not to do

- Don't lead with the protocol or identity model
- Don't post the GitHub repo without a problem framing
- Don't write about architecture when the audience hasn't felt the pain

---

## Pillar 2: Narrow the door

The full aweb vision (identity, addressing, cross-org communication, key
rotation, custody modes) is the long-term architecture. It stays in the
codebase. But it's not what gets first users.

The entry point is one thing: **make your agents stop stepping on each
other.**

### The first-contact experience

A developer with 2-3 Claude Code or Codex agents on the same repo should
go from "agents making a mess" to "agents coordinating" in under 5
minutes. The entire first experience is:

```bash
npm install -g @awebai/aw
aw init
```

`aw init` defaults to `aweb.ai` as the server and the current
directory name as the project, asks a couple of questions, and gives
you a working agent at `<your-project>.aweb.ai/<alias>`. No
infrastructure setup, no identity model explanation, no team
configuration to worry about.

For Claude Code users specifically, `aw channel install` adds aweb as
an MCP channel — your existing session sees aweb messages, claims,
and presence updates without any wrapper process.

The deeper concepts (persistent identity, BYOD namespaces, custodial
agents) surface only when the user hits a real need for them.

### Feature gating by need

| User need                                    | What they see                       |
|----------------------------------------------|-------------------------------------|
| "Stop my agents colliding"                   | `aw init`, tasks, claims, messaging |
| "I want my agent to persist across sessions" | Persistent identity                 |
| "Other teams need to reach my agent"         | BYOD namespace, addresses           |
| "I need hosted/browser agents"               | Dashboard, custodial identity, MCP  |

Each layer reveals itself when the previous one is working. The
documentation and landing pages should follow this same progression.

### Landing page structure

The homepage answers one question: "Your agents are already capable. aweb
helps them work as a team." Primary CTA is the CLI install. Everything
else (hosted MCP, addresses, network vision) lives on secondary pages
linked from the homepage.

---

## Pillar 3: Prove the platform by building on it

The strongest argument for a platform is a compelling product built on
it. aweb's long-term differentiation is the identity and trust layer.
That layer is invisible until something uses it visibly.

### atext.ai

A document sharing service for agents, built entirely on aweb identity
and coordination.

What it does:

- Agents share versioned text documents, authenticated by their aweb
  identity
- Documents are scoped to aweb projects
- Cross-project sharing uses aweb addressing and contacts
- Public documents render at `{project}.atext.ai/{key}`

Why it matters:

- It's a concrete answer to "what can you build on aweb?"
- It solves a real problem (Juan and cofounder can't share project
  artifacts between their agents today)
- The pitch deck itself can be hosted on atext.ai, making every pitch a
  live demo

Build scope: days, not weeks. Tiny FastAPI service, aweb API key auth,
Postgres storage, MCP tools, simple public rendering.

### The ecosystem story

When pitching aweb, the narrative becomes:

> "aweb is the identity and coordination layer for AI agents. Here's the
> open-source protocol. Here's atext, a document service built on aweb
> identities. Any developer can build the same kind of thing on the same
> infrastructure."

This reframes aweb from "a tool you use" to "a platform you build on."
That's a harder story to tell but a more defensible position.

### Future ecosystem products

Don't build these now. But they illustrate the platform potential:

- Agent-scoped CI/CD triggers (aweb identity authorizes deployments)
- Agent reputation/review systems (built on the permanent identity layer)
- Cross-org agent marketplaces (built on addressing and trust)

These only matter if the platform has users. They're directional, not
actionable today.

---

## Execution priorities

In order:

1. **Ship the OSS repo publicly.** It's ready. The code quality will
   impress people who look.

2. **Record the collision video.** Highest-leverage single marketing
   asset. Shows the problem viscerally.

3. **Write one problem-first blog post.** Personal experience running
   multi-agent teams. What goes wrong. aweb mentioned at the end, not
   the beginning.

4. **Start the 5-conversations-per-week habit.** Twitter/X, Reddit,
   Discord. Be present where multi-agent discussions happen.

5. **DM 3-5 multi-agent practitioners.** Personal outreach, hands-on
   help, design partnership.

6. **Build atext.ai (minimal version).** Weekend project. Proves the
   platform, solves a real problem, gives every pitch a live demo.

7. **Reach out to Anthropic DevRel / MCP ecosystem.** aweb is a strong
   MCP project. Get listed, get featured.

Items 1-5 are this week. Item 6 is next week. Item 7 is ongoing.

---

## Revenue path

The hosted service (aweb-cloud) has three tiers:

| Tier     | Price   | Target                               |
|----------|---------|--------------------------------------|
| Free     | $0      | Individual developers, evaluation    |
| Pro      | $25/mo  | Small teams, serious multi-agent use |
| Business | $250/mo | Larger teams, full coordination      |

The free tier gets adoption. Pro converts when teams hit the daily
message limit (100 msgs/day on free). Business converts when
organizations need cross-project coordination and roles.

The OSS self-hosted option is the trust builder. Developers who can
self-host will. Teams that don't want to operate infrastructure will pay
for hosted.

Revenue is not the immediate concern. Getting 50 real users on the free
tier is. Revenue follows adoption, not the other way around.

---

## What success looks like

**3 months**: 50 active free-tier users. 5 design partners giving
regular feedback. One external blog post or video from someone who isn't
us. The collision video has been seen by 10,000+ people.

**6 months**: 200 active users. 10 paying Pro customers. atext.ai is
live and used by at least one team outside ours. Anthropic or OpenAI has
acknowledged the project in some ecosystem context.

**12 months**: 1,000 active users. Sustainable revenue from Pro/Business
tiers. At least one third-party product built on aweb identity. The
"coordination layer for agents" category is recognized and aweb is the
name associated with it.

These are targets, not predictions. If 3-month numbers don't materialize,
that's the signal to reassess whether the market is ready or the product
needs to change.

---

## The honest risk

The scenario where this doesn't work: AI tool providers build native
coordination before aweb reaches critical mass, and the vendor-neutral
story doesn't matter because teams standardize on one provider anyway.

The mitigation: move fast on adoption, make the identity layer the moat
(switching cost), and build the ecosystem (atext and others) that makes
aweb more than a feature a platform vendor can replicate.

The fallback: if the platform play doesn't work, the OSS coordination
server is still a useful tool that a focused community will sustain. Not
every outcome is venture-scale, and that's fine.
