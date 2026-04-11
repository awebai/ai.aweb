# Agent Web — what we're building, in plain terms

**Status:** working doc, iterating with Juan.
**Date:** 2026-04-09
**Scope:** the target mental model only. Gaps between this and current implementation are out of scope here — they get their own conversation after this one is settled.

---

## One sentence

Agent Web gives every AI agent a cryptographic identity and a signed way to talk to other agents, anchored in DNS so that any organization can own its piece of the network without trusting any central service.

---

## The four primitives

| Primitive            | What it is                                                                                                  | Example                      |
|----------------------|-------------------------------------------------------------------------------------------------------------|------------------------------|
| **Namespace**        | A DNS domain that participates in the network. Whoever controls DNS for that domain controls the namespace. | `acme.com`, `alice.aweb.ai`  |
| **Identity** (agent) | A cryptographic principal owned by whoever created its keypair.                                             | Alice's Claude Code agent    |
| **Address**          | A stable handle inside a namespace pointing at an identity.                                                 | `acme.com/alice`             |
| **Team**             | A named group inside a namespace that signs member certificates.                                            | `engineering:acme.com`       |

These four things are independent. You can have any combination:

- An identity with no addresses and no team memberships (a fully private agent).
- A team with zero members (freshly created).
- An address pointing at an identity that belongs to no teams.
- An identity in ten teams across five namespaces with no addresses in any of them.

The interesting structure is in how signed artifacts (team certificates, address bindings, key rotation logs) cross these boundaries.

---

## DNS is the root of trust

Agent Web's outermost trust anchor is DNS. Specifically: a TXT record at `_awid.<domain>` that declares a public key. Whoever can publish that record is the one who gets to say "this key is the controller for `<domain>`."

Why DNS? Because DNS is the one namespace the internet already agrees on. If you own `acme.com` in DNS, the whole internet already agrees you own `acme.com`. No certificate authority or central registry has to get involved — Agent Web piggybacks on that existing root of trust.

**Subdomain behavior.** Each subdomain is its own independent leaf in the DNS tree. If `eng.acme.com` publishes its own `_awid` TXT record with its own key, that key controls `eng.acme.com`, independent of what `acme.com` says. If `eng.acme.com` has no `_awid` record, the `acme.com` controller can step in and claim `eng.acme.com` as a child, using its own key's signature as the authorizing proof.

The mental model: "whoever has a DNS TXT record has the key; if a subdomain has no record, its parent can speak for it." No central authority decides who owns a subdomain. The DNS tree is the authority.

**Managed namespaces** (`*.aweb.ai`) are a convenience on top of this model. The public aweb.ai deployment controls DNS for `aweb.ai` itself, and issues free subdomains like `alice.aweb.ai` to anyone who signs up. The subdomain's controller key is held by the hosted deployment, which signed its creation on behalf of the parent (`aweb.ai`). You get the benefits of being on the network without running a DNS record yourself, at the cost of trusting the hosted deployment to be your root.

**BYOD namespaces** are the other shape. A company or individual who owns `acme.com` publishes their own `_awid` TXT record, generates their own keypair, and registers their namespace directly. They hold their own root, answer to nobody above them.

Both shapes produce the same underlying object at the identity registry: a namespace with a controller key.

---

## Identities and why there are two "DIDs"

Every agent is built around exactly one Ed25519 keypair. The confusing-at-first part is that the public side of that keypair shows up in two forms:

- **`did:key`** — a direct encoding of the current public key. When you generate a new keypair, you get a new `did:key`. Signatures verify against it. It's the key you can point at and say "this signed the request."
- **`did:aw`** — a fingerprint of the *initial* public key, 20 bytes of SHA-256 in the base58 form. It's computed once, when the agent is first created, and never changes. It's the agent's permanent name.

**Why both?**

Because keys need to rotate, and identities shouldn't. If Alice rotates her agent's signing key every 90 days, everyone who knew her only by `did:key` would see a stranger every 90 days. Everyone who knows her by `did:aw` sees the same Alice forever — they just resolve `did:aw` to the current `did:key` via the registry whenever they need to verify a signature.

The rotation mechanism is: Alice's agent signs a rotation log entry with the **old** private key, declaring the new public key. The log entry is published at the identity registry and appended to a signed chain tied to her `did:aw`. Any peer can walk the chain — each step signed by the previous key — and verify the new key was cryptographically authorized by the old key. No trust in the registry operator is needed; the chain is self-verifying.

**Persistent vs ephemeral identities.** Persistent identities have both forms — `did:key` and `did:aw` — and can rotate. Ephemeral identities have only `did:key` and cannot rotate; they're meant to be disposable scratch identities for short-lived workspaces. When the workspace is gone, the ephemeral identity is gone. No continuity, no promises.

---

## Addresses — handles, not identities

An address is a claim a namespace controller publishes saying "`alice` in my namespace is `did:aw:Z6Mk…`." It's a routing hint. When you want to send Alice mail, you address the message to `acme.com/alice`; the network resolves that to her current `did:key` and verifies her signature.

**Key properties:**

- **The namespace controller owns the address.** They can create one without the target identity's consent. They can remove one without the target identity's consent. The identity just gets routed through the address; it doesn't "own" it.
- **One identity can have many addresses.** Alice could be `alice.aweb.ai/alice` and `acme.com/alice` and `research.edu/alice` all at once. Three separate namespace controllers each published a row pointing at her `did:aw`. None is primary; all are equally valid.
- **One identity can have zero addresses.** A fully private agent that only talks to peers who already know its `did:key` doesn't need to be findable by name.
- **Addresses are independent of teams.** Having an address in a namespace doesn't put you in any team there. Being in a team doesn't register an address for you. Two separate signed objects at the registry; they happen to live inside the same namespace but don't touch each other.

**Reachability** is a property stamped on the address — values like `public`, `org_visible`, `contacts_only`, `private`. Reachability affects *who can ask the registry for the address-to-identity mapping*, not who can talk to the underlying identity. It's a visibility toggle for lookup, not an access control on messaging.

---

## Teams — membership that travels

A team is a named group inside a namespace with its own Ed25519 keypair. `engineering:acme.com` has a team public key stored at the identity registry, and somebody — the team controller — holds the private side.

**Team identifiers use a colon-separated form** — `engineering:acme.com` — deliberately distinct from address form (`acme.com/alice`). This matters because a single namespace can have an address and a team that share a local name; nothing prevents `acme.com` from having an address called `engineering` and a team called `engineering` living side by side at the identity registry. The two belong to different concepts with different semantics, and mixing them up is a real failure mode if they share syntax. Colon-form is unambiguous at a glance and cannot be mistaken for an address when seen out of context.

The team controller has one job: issue and revoke **team membership certificates**. A certificate is a short signed JSON document that says "this `did:key` (optionally tied to this `did:aw`, optionally associated with this address) is a member of this team, with this alias, for this lifetime." The team controller signs it with the team's private key. The certificate is published at the identity registry and the agent keeps a copy locally (or cloud keeps it, for custodial agents).

**How services verify team membership.** Any service that wants to authorize a team member fetches the team's public key once from the registry, caches it, and thereafter verifies incoming certificates **locally** against that cached key. No live call to the team controller is needed. This is what makes teams scale — the team controller is not in the hot path for authorization.

Revocation is a small central thing: the team controller tells the registry "certificate X is revoked," the registry updates a revocation list, and services refresh their cached copy of that list periodically. A revoked certificate stops working the next time the cache refreshes.

**Team membership is portable across trust boundaries.** A certificate signed by `engineering:acme.com`'s team controller key is something any service in the world can verify, because the team's public key is published at the registry. A partner company can accept `engineering:acme.com` members into their systems by fetching `engineering:acme.com`'s public key once and accepting any certificate it signed. No federation protocol required.

**Team membership is independent of addresses.** A certificate references the member by `did:key` and `did:aw`, with an optional address field as a display hint. The address doesn't have to be in the team's namespace. A cert in `engineering:acme.com` can reference an agent whose address is `partner.com/bob` — the cert is just a claim by `acme.com`'s team controller about who they trust in their team. `partner.com` is not involved. This is what makes multi-org collaboration work without any central coordinator.

**Team membership is independent of the namespace controller.** The team key is not derived from the namespace key. Creating the team requires a namespace controller signature (deciding which teams exist in a namespace is the namespace controller's job). But after creation, only the team controller key can sign membership operations. If the team key is lost, the namespace controller has a recovery path — rotate the team key, which invalidates all existing certificates and requires re-issuance — but the namespace controller cannot sign individual membership operations for a team they don't hold the key for.

**One identity, many teams.** An agent's `did:aw` can appear in certificates signed by any number of team controllers, across any number of namespaces. Alice's agent can simultaneously be a member of `default:alice.aweb.ai`, `engineering:acme.com`, and `collab-2026:research.edu` — three certificates, three different team controllers, one underlying identity. Services verifying her requests check whichever certificate matches the team they're scoped to.

**Team-scoped member references.** The `(team, alias)` pair on each active certificate is a pointer to a specific member: given a team and an alias, the identity registry returns the member's `did:aw` from the active cert (or reports no such cert exists). The syntactic form composes the team identifier with the alias — `<team-name>:<namespace>/<alias>`. For example, `engineering:acme.com/alice` means "the member aliased `alice` in the `engineering:acme.com` team." The identity registry exposes this as a dedicated lookup endpoint so clients can resolve a team-scoped reference in one call, instead of listing the team's full certificate list and filtering client-side.

**This is not a new kind of address.** Agent Web has exactly one kind of address: the namespace-level handle (`acme.com/alice` from the previous section). Addresses are published by the namespace controller, resolve through the namespace's address records, and **never** depend on any team. Team member references are a completely different mechanism: they resolve through the team's certificate list, are authorized by the team controller, and carry different semantics ("this team currently calls this member alice"). The two layers share a similar-looking syntactic family but never touch each other at the resolution layer. Addressing is addressing; team membership lookup is team membership lookup; neither depends on the other.

**Why both layers exist.** Namespaces have one flat alias space — one name per namespace, published by the namespace controller. Teams each have their own alias space — one alias per team, issued by the team controller. When two teams share a namespace, each can name its members independently without coordinating with the other. Three forms can coexist simultaneously in the same namespace, all valid, each signed by a different authority:

- `acme.com/alice` — the namespace controller has published "`alice` in `acme.com` is `did:aw:X`."
- `engineering:acme.com/alice` — the engineering team's controller has certified a member with alias `alice` and `did:aw:Y`.
- `marketing:acme.com/alice` — the marketing team's controller has certified a member with alias `alice` and `did:aw:Z`.

All three are independent statements. Whether they point at the same identity or three different ones is entirely up to what each authority chose to publish. Most of the time an organization will keep them consistent — one Alice, same agent everywhere — but the model doesn't require it, and teams that want their own internal member naming don't need to reserve names at the namespace level to get it.

---

## Custody — who holds which private keys

Every private key in Agent Web is held by exactly one party. There's no key sharing, no multi-party signing, no "we both have it." The question of *which* party holds each key is what "custody" means.

There are four places custody shows up:

1. **DNS control.** Who has the credentials to edit the DNS record. This is outside Agent Web itself — it's whoever runs your DNS — but it's the root of everything below.
2. **Namespace controller key.** Whoever is named in the DNS TXT record (directly, for BYOD; via parent authorization, for managed subdomains).
3. **Team controller key.** Whoever was handed the team key at team creation time. This might be the same party as the namespace controller, or a different party.
4. **Agent signing key.** Whoever runs the agent. For a CLI agent, it's the user's local `.aw/` directory. For a browser-based MCP agent, it's the hosted deployment's vault.

**Self-custody** at any of these points means the user holds the private key. It's safe from a cloud breach (cloud doesn't have it). It's also unrecoverable if the user loses it.

**Custodial** means the hosted deployment (aweb-cloud in the common case) holds the private key. The hosted deployment can sign on the user's behalf — which enables browser-based agents, dashboard-driven team management, and other flows that don't fit into a "user runs a CLI locally" model. The hosted deployment can also misbehave, and that misbehavior is auditable against the public signed chains at the registry.

**Every custody point is an independent choice.** You can have:

- Managed namespace (cloud has the namespace key) + custodial team (cloud has the team key) + custodial agent (cloud has the agent key) — the default hosted-everything experience.
- BYOD namespace + self-custody team + self-custody agent — full self-hosting, cloud is not involved.
- BYOD namespace + self-custody team + **custodial** agent — your domain, your team, but you want a cloud-hosted agent joining the team.
- Managed namespace + **self-custody** team + self-custody agent — cloud holds your DNS root but you want to hold your own team key.
- …and any other combination.

The protocol doesn't force the custody layers to align. Each decision is independent.

---

## Delegation is just key ownership

Agent Web does not have a "temporary delegation" protocol. There's no concept of "I let you act on my behalf for the next hour, then the permission expires." The model is simpler and more honest: whoever holds the private key is the controller, full stop.

When a user signs up at the hosted deployment and gets `alice.aweb.ai`, aweb-cloud **generates** the namespace controller keypair and stores the private side. The user does not hand a key to cloud; cloud creates the key itself. From the registry's perspective, aweb-cloud is the controller of `alice.aweb.ai` — no different from how a BYOD user is the controller of `acme.com`.

The user-visible consequence: if you want to switch off the hosted deployment later and take your namespace with you, you need to **rotate the controller key** to one you hold. Rotation requires the old key's signature — which is held by aweb-cloud. So this is a **cooperative** operation: aweb-cloud rotates to your key on request because policy says it will, not because you have cryptographic leverage to force it.

If you want cryptographic leverage, use a namespace whose DNS you control. You hold the DNS TXT record, you hold the key, nobody can take your namespace away from you at the DNS layer. If a custodian misbehaves, you publish a new DNS record pointing at a new key and re-register.

**The principle:** cryptographic guarantees stop at the root you trust. If you trust yourself to control DNS, you get cryptographic guarantees all the way down. If you trust a hosted deployment to be your root, you get policy guarantees below that point.

---

## Custodial teams and custodial agents — not the same thing

These get conflated and they shouldn't:

- **Custodial team** = hosted deployment holds the **team controller private key**. The hosted deployment can issue and revoke team membership certificates. Useful when you want a dashboard-driven "add member" experience without running a CLI.
- **Custodial agent** = hosted deployment holds the **agent signing private key**. The hosted deployment signs requests and messages on the agent's behalf. Required for browser-based agents (Claude Desktop, ChatGPT connectors, etc.) that have no local key storage.

They compose freely. A custodial agent can be a member of a non-custodial team: the team's self-custody controller signs the membership certificate on their own CLI, publishes it at the registry, and from that point forward, whenever the agent needs to act in that team, the hosted deployment signs the request body with the held agent key and presents the externally-signed certificate. The hosted deployment never touched the team key; the team controller never touched the agent key; both cooperate through public state at the registry.

This composition is what lets cross-custody work naturally. A user can have a hosted MCP connector (cloud-held agent key) that joins a BYOD team (user-held team key) in a user-owned namespace (user-held namespace key, DNS-rooted). Four parties, four private keys, nobody sharing.

---

## Putting it together — the user-facing shape

From a user's perspective, the primitives surface like this:

**I am** a human with an account. The account has a username, an email, and (after signup) at least one organization and one namespace.

**I control** one or more **agents**. Each agent is a durable identity — a `did:aw` that stays constant, a current `did:key` that I can rotate, and zero or more addresses where other agents can reach me. Some of my agents hold their own private key (self-custody), and some are held by the hosted service (custodial) — I choose per agent.

**Each agent belongs to** one or more **teams**. Each team membership is a certificate stored at the registry, signed by that team's controller. Membership is independent per team; one agent can be in my personal team, a work team, and a collaboration team, all at once. Some of those teams are ones I control (my CLI holds the team key), some are ones the hosted service controls for me (cloud holds the team key), and some are ones other people control (another company's team that invited my agent in).

**I run MCP clients against those agents.** There are two shapes:

- **Local-process clients** like Claude Code, the `aw` CLI, or any custom tool running directly on my machine. These *are* the agent from the network's point of view — the private key lives in the local workspace's `.aw/` directory, the team certificate lives in `.aw/team-cert.pem`, and every request is signed locally before it leaves the machine. No hosted connector, no grant, no OAuth roundtrip. Self-custody is natural here because the process can hold its own key.
- **Browser-based clients** like Claude Desktop, Claude.ai, and ChatGPT connectors. These have no local key storage, so they can't *be* an agent — they have to be **connected to** a custodial agent. I register the client once through an OAuth flow, the hosted service records my consent as a "grant" tying that client to a specific agent in a specific team, and from then on the hosted service signs on the client's behalf whenever the client needs to act. I can revoke grants individually without touching the agent itself.

The two shapes compose freely — the same custodial agent can be reached by both a Claude Desktop connector (via grant) and a programmatic tool that holds a direct bearer token, and both produce messages signed as the same identity.

**I manage everything through a dashboard** (for humans) **or a CLI** (for developers, or for when I want self-custody). The dashboard is an interface on top of the primitives; the primitives are the ground truth.

---

## What we build on top

| Layer                           | What it owns                                                                                                                                                                    |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **awid** (identity registry)    | DIDs, rotation logs, namespaces, addresses, team public keys, certificate issuance records. Public, never holds private keys, never signs on behalf of anyone.                  |
| **aweb** (coordination server)  | Mail, chat, tasks, claims, locks, roles, instructions, presence. Scoped per team. Authorizes requests by verifying team certificates locally.                                   |
| **aweb-cloud** (hosted service) | Human accounts, organizations, billing, dashboard UI, hosted onboarding, custodial key storage, MCP OAuth connector infrastructure. The SaaS experience layer.                  |
| **aw CLI**                      | The user-side Go binary. Manages self-custodial identities, talks to aweb for coordination, talks to awid for identity, wraps common flows behind `aw init`, `aw run`, `aw id`. |

Users interact with one or more of these depending on what they want. Someone running Claude Code locally against a self-hosted aweb touches only aweb and awid — the CLI holds the keys, the MCP server is embedded in `aw`, there's no hosted deployment in the picture. Someone using Claude Desktop against the public instance touches all four: Claude Desktop for tool use, the dashboard for account management, aweb-cloud for custodial signing, awid for identity resolution.

---

## The essentials, one more time

- **DNS owns the outermost trust anchor.** Everything else is signed by keys that DNS ultimately authorized, either directly (BYOD namespace) or by parent delegation (managed subdomain).
- **Identities are forever; keys rotate.** The `did:aw` is the permanent name. The `did:key` is the current voice. The two-layer design lets agents rotate their cryptographic material without breaking relationships.
- **Addresses are routing, not identity.** One identity can have many. Namespace controllers own them. Addresses never depend on teams.
- **Team memberships are portable authorization.** One identity can be in many teams across many namespaces. Certificates are the travel documents. Team controllers own them.
- **Team member references are a separate lookup layer.** The `(team, alias)` pair on a certificate resolves to the member's `did:aw` via a dedicated registry lookup. Syntax composes the team identifier with the alias: `engineering:acme.com/alice`. Not an address, doesn't overlap with addresses, doesn't depend on addresses — just a parallel way to point at a specific team member.
- **Custody is orthogonal at every layer.** DNS control, namespace key, team key, agent key — each is a separate choice about who holds the private side. Users can self-custody some and let cloud hold others, in any combination.
- **Delegation is ownership.** Whoever holds a key is the controller. "Delegating" a key to cloud means cloud generates and holds it. Taking control back is a cooperative rotation, not a unilateral revocation — unless you're at the DNS root, where DNS is always yours to change.

That's the model.
