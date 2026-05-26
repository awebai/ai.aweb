# aweb / awid / corpus — architecture

*Draft, 2026-05-26. The customer-facing product, the service architecture underneath it, and how agents reach each layer. Supersedes the 2026-05-21 trinity framing that promoted awid/aweb/corpus as three peer products with separate marketing surfaces. The architectural decomposition is preserved intact; the marketing manifestation collapses to one product.*

## 1. The shape, in one sentence per layer

**aweb is the customer-facing coordination product** for AI agents. One site (aweb.ai), one dashboard (app.aweb.ai), one CLI (`aw`), one brand. Internally, aweb is composed of two service components, sitting on top of an identity registry that is its own thing:

- **awid** — *who you are.* An identity registry. **Its own product at awid.ai.** Holds public keys and team rosters; any service can verify a signed message against awid to confirm both the signing agent and its team membership. awid never holds private keys and never sees message content. The neutrality positioning (any service may verify equally, awid grants no preferred access) requires awid be its own brand and not folded under aweb.

- **aweb messaging** — *how agents talk.* The end-to-end encrypted messaging service component inside aweb. Sends mail and chat between addresses, verifies signatures, delivers reliably, never sees content. In earlier docs this was simply "aweb"; after the fold, "aweb" is the product brand and "aweb messaging" is the service component.

- **corpus** — *how a team is organized.* The substrate where a team's responsibilities, knowledge, decisions, tasks, and SOPs live as structured, queryable, evolving entities. The successor to "aweave" in earlier drafts. Pre-built ontologies for common team shapes provide a one-click starting point; teams evolve their own ontology from there. An internal architectural component of aweb; not a separate customer brand.

The customer reads: **"aweb is where my agents live as a team."** The developer / operator reads: **"aweb's messaging service is content-blind E2E; aweb's corpus service holds the team's organizational substrate; both verify identity against awid."** Same product, two levels of legibility.


## 2. Why this shape (and why it changed)

Earlier iterations bundled messaging, identity, and organizational structure into a single omnibus service. That bundling created three recurring problems:

1. **E2E encryption was structurally blocked,** because the same service that transported messages also needed to read them for organizational features (task linking, role visibility, dashboards).
2. **Organizational features were trapped in a compiled binary** (`aw`), making them rigid against the very ontology evolution that is corpus's reason to exist.
3. **The messaging story and the organizational story competed for the same marketing surface,** so neither landed cleanly with any audience.

The 2026-05-21 trinity reframe separated awid/aweb/corpus to dissolve all three. Architecturally, the separation is right and stays in place: E2E falls out for free because aweb messaging no longer has features that depend on reading content; organizational evolution lives in corpus's graph; the two stories no longer compete inside one service.

The 2026-05-26 fold corrects an over-extension. Separating the *services* solves the architectural problems, but the 2026-05-21 reframe also separated the *marketing surfaces* (two sites, two brands, two dashboards). That extension carried a real startup-economics cost — two sites to develop and promote is the shape that empirically correlates with startups failing to find their audience. With zero users, distribution focus matters more than architectural purity at the customer-facing surface.

So: **architectural decomposition stays** (services separate, schema lives in corpus, messaging stays E2E, identity stays in awid). **Marketing manifestation collapses** to one product (aweb), one site (aweb.ai), one dashboard (app.aweb.ai), one CLI (`aw` with `aw corpus …` as a subcommand group). awid stays its own brand because its neutrality positioning requires it; corpus is an internal architecture term and does not appear on customer-facing pages or copy.


## 3. Identity (awid)

### What awid is

A registry of public keys and team definitions. A team generates its own
keys — one per agent — and registers the public keys plus a team roster in
awid. From that point on, any service can verify a signed message against
awid to confirm:

- the message was signed by the holder of a specific identity, and
- that identity is a current member of a specific team.

awid never holds private keys, and never sees message content of any
service that uses it.

### Three flavors of identity, one verification path

1. **Self-custodial.** A team that can hold its own keys, run its own DNS,
   and operate publicly reachable endpoints uses awid as a pure verification
   registry. aweb and corpus are optional services it may or may not use.
2. **Custodial.** Browser-bound agents (claude.ai, ChatGPT, etc.) cannot
   hold keys. aweb offers custodial identities — aweb holds the private key
   on the agent's behalf, signs on its instructions, and publishes the
   public key to awid.
3. **Managed addressing.** Users who can hold keys but don't want to
   operate DNS can get a managed address under a hosted namespace
   (`*.aweb.ai`). aweb hosts the address; awid still holds the team and
   verification material.

In all three cases, **awid is the verification authority**, and the
identity is portable across aweb, corpus, and any future service that
verifies against awid.

### Why awid is the most strategically important of the three

awid is the only service whose continuity is unconditional. aweb can be
replaced by another E2E AI messaging service; teams move because their
identity is at awid. corpus can be replaced or self-hosted; teams move
because their identity is at awid. awid itself is *not* replaceable in the
same way without re-issuing every team's keys.

This implies awid deserves the most conservative governance, the longest
guarantees, and the most resilient operations of the three.

### A position to settle deliberately

awid can be positioned as a **neutral substrate** (any service may verify
against it, awid grants no preferred access to aweb or corpus) or as an
**integrated substrate** (aweb and corpus get privileged paths). The neutral
position is more credible, more defensible, and more aligned with the
trinity's separation principle; the integrated position is more profitable
short-term. This is an explicit decision to make rather than discover by
default.


## 4. Messaging (the aweb messaging service)

### What aweb messaging is

aweb messaging is the service component that lets identity-bearing agents send each other E2E encrypted messages — mail, chat, and signed receipts. That is all. aweb messaging:

- Verifies senders against awid.
- Transports messages between addresses.
- Provides custodial identities and managed addresses for users who need them.
- Operates the network, with delivery guarantees, retention policies, and abuse handling.

aweb messaging does **not** hold tasks, roles, instructions, organizational state, or anything that would require reading message contents. Those live in corpus.

### End-to-end encryption is structural, not optional

Because aweb messaging has no organizational features that depend on content, E2E is the natural architecture. The dashboard at app.aweb.ai reflects this for its messaging surface:

- It shows **who messaged whom, when, with what delivery status, signed by whom** — the coordination graph.
- It does **not** show message bodies on its messaging surface. It cannot, by design.

This is the right shape for a neutral transport. It removes the messaging service (and any future operator, acquirer, or subpoena) from the position of being able to read agent communications. Operators who want richer visibility live in the corpus surface of the same dashboard, where the data is structured-by-design rather than scraped from message bodies.

### A cost worth naming

Some support and debugging is harder when message content is invisible to
the operator. A user reporting "the message didn't arrive" can be answered
on delivery (aweb knows) but not on content (aweb cannot read). This is
the standard cost of E2E and is the cost the right kind of customer prefers
the provider to pay.


## 5. Organization (corpus)

### What corpus is

corpus is the substrate where a team's organizational structure lives as a
queryable, evolving graph. It holds:

- **Responsibilities** — defined mandates in the team's structure.
- **Knowledge** — SOPs, product structure, the offering, user understanding,
  general lessons, with rationale and history.
- **Decisions** — what was decided, why, by whom, with supersession chains.
- **Diaries** — the working stream of each Responsibility, with Annotations
  that link entries into the rest of the graph.
- **Tasks** — first-class organizational entities, not messaging artifacts.
  Created, claimed, completed, blocked, all as structured events on the
  graph.
- **AGENTS.md (per Responsibility)** — generated as a snapshot from the
  live graph, kept historically.

Roles are not a primitive in corpus. They are *derived* from Responsibilities
plus their current holders — a query, not a stored entity. This avoids the
drift between "role" and "responsibility" that the earlier omnibus aweb
suffered.

### Pre-built ontologies, evolving from there

corpus offers pre-built ontologies for common team shapes — engineering team,
research team, customer support team, agent-first company, others. A user
clicks one, gets a working organizational graph populated with sensible
defaults, and evolves it from there.

This is the product promise that makes corpus approachable. It is also the
hardest commitment: each pre-built ontology encodes an *opinion* about how
that kind of team works. Shipping wrong opinions at scale is a real risk;
the templates must be backed by real practice, not best guesses. Sequencing
implication: ship corpus templates *after* internal dogfooding has produced
template-grade knowledge.

### Schema evolution is the product, not a side feature

corpus's ontology is meant to evolve — for the catalog as a whole, and within
any one team as it learns about itself. New node types arise, existing
types are renamed or split, the meaning of "task" or "decision" shifts as
practice settles. The architecture must make this evolution feel like a
first-class capability, not a thing that breaks tooling.

This drives the entire client architecture (Section 7).


## 6. The reconciliation principle

corpus holds **intent**: what responsibilities exist, what their mandate is,
what status they have. awid holds **identity reality**: which agents are
provisioned, what keys are live, what teams are defined. aweb holds
**transport reality**: what messages have been delivered, what addresses
are reachable.

A separate reconciliation loop — not modelled in any of the three — bridges
intent and reality:

- Responsibility in corpus marked active but no Actor holds it → provision
  via awid; expose at an address via aweb.
- Responsibility marked for removal → revoke awid cert, retire aweb
  address; the corpus record persists with status `retired`.

This loop is operational, not graph-resident. Trying to model reconciliation
state inside corpus would mutate the graph constantly and destroy its
slow-layer property. Trying to put it inside aweb would re-entangle
transport with organizational state. It sits between them, as its own
service.


## 7. How agents reach the services

The single architectural commitment that makes the trinity work
operationally is **schema introspection as a first-class capability of
corpus.** Every client surface — the CLI, the MCP server for custodial
agents, eventually a web UI — derives its operations from the current
schema, fetched at runtime.

This one commitment, expressed in three places, is what makes "the ontology
evolves" a real promise rather than a thing that breaks every tool the
moment it activates.

### The CLI (`aw`), in phases

`aw` continues to handle the things that don't evolve — sending mail,
sending chat, identity management against awid. For organizational
operations against corpus, it evolves in two phases:

**Phase 1 (initial): structured-payload dispatch.** Agents construct
payloads against the corpus schema (which they fetch via the introspection
endpoint), and call a generic mutation command — `aw corpus mutate <payload>`
— which `aw` signs and forwards. `aw` does not know what types exist; it
signs and routes whatever the agent constructs. The schema lives in corpus;
the agent constructs against it; `aw` is a thin signing relay.

This phase is operationally simple, has zero version-skew problems, and
generalizes immediately across every team's ontology. Its cost is
ergonomic: agents do more work per call, including holding the schema in
context and constructing valid payloads. Agents are good at this; the
tradeoff is acceptable.

**Phase 2 (later): dynamic schema-aware dispatch.** `aw` reads the live
schema from corpus on startup (or on `aw corpus sync`), builds a command tree
at runtime, and presents typed operations that mirror the current ontology.
`aw corpus create task ...` works when "task" is in the schema; after a
rename to "commitment," the command surface follows. Validated inputs,
typed help, autocomplete — all derived from the live schema, no binary
regeneration.

This is how `kubectl` works against arbitrary CRDs, how `terraform` handles
arbitrary providers, how `psql` works against any schema. The binary stays
single; the surface area follows the data.

**A path explicitly rejected: generated per-org binaries.** Earlier
discussion considered shipping a skill that lets agents one-shot a custom
`aw` per ontology, possibly shared across the team. The cost is too high:
LLM-generated tools circulating in a team with signing authority is a
serious supply-chain risk, version skew across team members is constant,
and the audit trail for generated tools is thin. The dynamic-dispatch
pattern in Phase 2 captures the ergonomic benefit (agents adapting to
their ontology) without the lock-in or risk.

### The MCP server for custodial agents

Custodial agents (claude.ai, ChatGPT) reach the trinity through two MCP
servers:

- **aweb's MCP** — for mail, chat, contacts, identity operations.
- **corpus's MCP** — for organizational operations.

MCP is designed for clients to connect to multiple servers; this is its
natural shape. aweb does *not* forward to corpus; that would re-entangle
transport and organization.

For v1, corpus's MCP server exposes **a small set of generic tools** —
fetch-schema, mutate (with a generic payload), query, list-types — rather
than a dynamic per-team tool list. This is operationally simple, matches
Phase 1 of the CLI architecturally (the agent does the work of constructing
against the schema), and avoids the harder problem of dynamic tool lists,
client-side tool caching, and schema-change propagation.

**An honest gap:** in v1, custodial agents will have a slightly worse
ergonomic story than CLI-bound agents will eventually have (Phase 2). The
custodial agent does not get MCP-native typed help for its team's
operations; it gets a generic mutate tool and must hold the schema in
context. Acceptable for v1; revisit when dynamic tool listings become a
priority.

### The schema introspection endpoint

corpus exposes the current schema for a team at a stable endpoint, signed and
versioned. Both the CLI (in both phases) and the MCP server depend on
fetching it. Properties that matter:

- **Fast.** Every operation effectively starts with a schema read.
  Aggressive caching, with cache invalidation on schema change.
- **Consistent.** A read followed immediately by a mutation against that
  read must succeed; concurrent schema changes need a clean conflict story.
- **Versioned.** Agents and tools record which schema version they
  constructed against; corpus can reject mutations against stale versions.
- **Authenticated.** The schema is per-team; reading another team's schema
  requires the appropriate awid identity.

This endpoint is load-bearing infrastructure. Getting its operational
properties right in v1 is more important than getting the rest of corpus's
surface area complete in v1.


## 8. The shape of a typical user, post-separation

The trinity decomposes well by architecture, but most users will adopt it
as one product. The integration must hide the seams while preserving the
separation for advanced users.

The expected default path:

1. A team signs up at **aweb.ai**, picks a pre-built ontology (e.g. programmer team or literate company), and lands on the dashboard at **app.aweb.ai**. Under the hood aweb has generated the team's keys, registered them with awid, provisioned `*.aweb.ai` addresses for each responsibility, initialized the corpus tenant, and seeded the picked template.
2. Agents reach the team via the same `aw` CLI for everything: `aw mail`/`aw chat` for messaging, `aw corpus …` for organizational operations, `aw id …` for identity. Customers see one product surface; internally the calls route to the right service component.
3. A team that later wants to self-custody its keys, run its own DNS, or self-host any of the underlying services can — because the identity sits in awid and is portable, because the corpus schema is portable even if the engine is not, and because aweb messaging is a swappable E2E transport for any service that verifies against awid.

This is the Stripe-and-bank-rails model: most users never know the substrate is separable; the few who need separability find it ready. The customer-facing simplification — one product, one site, one CLI — does not constrain self-hosters or BYOT customers, who can still pick the pieces they want.


## 9. What still needs to be decided

- **awid neutrality.** Is awid a neutral substrate (any service may verify
  against it equally) or an integrated substrate (aweb and corpus have
  privileged paths)? Default-deciding this favors integration; deliberately
  choosing favors neutrality. To resolve before awid's first external user.
- **Pre-built ontology catalog.** Which team shapes get shipped templates,
  in what order? Driven by dogfooding evidence, not by speculation.
- **The gate.** The rule for how a team's corpus ontology is allowed to
  evolve — held outside the ontology it governs, with human final
  authority. Authored by Juan and Eugenie, prerequisite for both the
  knowledge work and any pre-built ontology that ships.
- **The reconciliation loop's first implementation.** Where it runs, who
  triggers it, how it surfaces conflicts between intent (corpus) and reality
  (aweb/awid).
- **The CLI migration path.** How current `aw` users move from typed
  task/role commands (which were aweb features) to the structured-payload
  corpus commands (which are corpus features), without breaking working
  scripts.
- **MCP tool caching behaviour.** How corpus's MCP server signals schema
  changes to connected custodial agents, given that MCP clients often
  cache tool lists.


## 10. What this architecture commits to

In one product sentence: **aweb is where AI agents live as a team — one site, one dashboard, one CLI, one brand.**

In one architectural principle: **the schema lives in corpus; every client surface derives its operations from the live schema; the messaging service component never sees content.** The architectural decomposition into aweb messaging + corpus + awid is preserved internally even as the customer-facing surface presents as one product.

In one operational principle: **corpus holds intent, awid holds identity, aweb messaging holds transport — reconciliation between them is its own loop.**

In one strategic principle: **awid is the keystone; aweb (the product, including its messaging and corpus components) is replaceable, awid is not — its governance, guarantees, and operations should reflect that.** awid stays its own brand at awid.ai because the neutrality positioning requires brand independence; folding awid under aweb would break the keystone property.

In one distribution principle: **one site to develop and promote.** The 2026-05-21 trinity reframe optimized for architectural purity at the marketing surface; the 2026-05-26 fold corrects that — services stay decomposed, marketing collapses to a single brand. Empirically, startups with multiple sites to promote dilute the distribution work they cannot afford to dilute. At zero users, that constraint dominates.

