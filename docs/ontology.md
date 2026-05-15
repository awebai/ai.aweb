---
title: "aweb company ontology — vocabulary and structural axioms"
date: 2026-05-15
status: v1 — Sofia + Athena converged; ship as reference doc, not production tooling
format: Manchester syntax (readable; DL-equivalent)
---

# aweb company ontology

This document is the canonical vocabulary for the aweb company. It
defines the classes (concepts), properties (relations), and structural
axioms that describe how the team is organized and how work flows.

## What this is

A reference document. When the team adds a new role, repository, or
work type, this is the single place to check "does this fit our model?
what does our model imply?"

The vocabulary used here is the same vocabulary in `publishing/voice.md`,
`docs/team.md`, `docs/agent-first-company.md`, and the agents' individual
`CLAUDE.md` files — but centralized and structured so future agents
(and the seminar curriculum) can find a single canonical reference.

## What this is NOT

- An OWL ontology authored for machine reasoning. We don't run a DL
  reasoner against this today. If a future use case justifies the
  tooling, we render to Turtle/OWL; for now this is for clarity, not
  validation.
- A complete description of how every piece of the company works.
  Operating rhythms, pragmatic judgment, and framing decisions live
  in prose elsewhere — DL/Manchester can't capture them and shouldn't
  try.

## Notation

Manchester syntax (readable English-shaped form of Description Logic):

| Manchester | DL | Meaning |
|---|---|---|
| `SubClassOf` | `⊑` | "is a kind of" |
| `EquivalentTo` | `≡` | "exactly the same as" |
| `DisjointWith` | `⊓ ⊑ ⊥` | "no individual is in both" |
| `some` | `∃` | "at least one" (existential) |
| `only` | `∀` | "all of, if any" (universal) |
| `min N` | `⩾N` | "at least N" |
| `max N` | `⩽N` | "at most N" |
| `exactly N` | `=N` | "exactly N" |
| `and` | `⊓` | conjunction |
| `or` | `⊔` | disjunction |
| `not` | `¬` | negation |

## Classes

Top-level partition:

```
Identity                       (anything with an aweb address or participating in agent-first-company life)
  Person                       human
    Founder                    Juan, Eugenie
  Agent                        AI agent
    PermanentAgent             has persistent identity + handoff doc + surface ownership
      Coordinator              owns a Surface; carries direction/review/framing for that area
      Developer                authors feature changes; usually on the dev team
      Frontend                 specialization of Developer (UI work)
    EphemeralAgent             task-scoped builder/reviewer pair on a worktree; no persistent surface

Surface                        a responsibility area
  Direction                    Sofia
  Engineering                  Athena
  Operations                   Hestia
  Support                      Aida
  Outreach                     Iris
  Analytics                    Metis

Team                           a coordination namespace with cryptographic membership
  PublicTeam                   visible-to-anyone (e.g., aweb:juan.aweb.ai)
  PrivateTeam                  internal-only (e.g., default:aweb.ai)

Repository                     code or docs container
  Primitive                    a load-bearing independent surface
    aweb_OSS_Repo
    awid_Registry_Repo
    ac_Cloud_Repo
    ai_aweb_Coordination_Repo
  AuxiliaryRepository          everything else

Artifact                       durable output of work
  Task
  Brief
  DecisionRecord
  StatusFile
  Handoff
  ReleaseTag
  ReleaseNotes
  BlogPost
  WelcomeGuide
  CommitMessage

Conversation                   message channel
  Mail                         async
  Chat                         sync
  Meeting                      scheduled multi-party conversation with topic + agenda + invitations

AudienceShape                  external persona category — describes a kind of customer
  P1Consumer                   small business / personal-AI users
  P2CompanyFleet               company managing AI-using employees
  P3DeveloperTeam              builders integrating aweb
  P4PlatformBuilder            larger platform-level partners

ReachabilityPolicy             how an Identity accepts incoming messages by default
  Nobody                       no one
  Contacts                     only saved contacts
  TeamMembersOnly              only fellow team members
  OrgOnly                      only same-organization members
  Public                       anyone
```

## Object properties (binary relations)

| Property | Domain → Range | Notes |
|---|---|---|
| `runs` | Agent → Surface | which surface this agent runs |
| `memberOf` | Identity → Team | non-functional; agents can be in multiple teams |
| `bridges` | Agent → Team | specific to multi-team identities (currently only Athena) |
| `claims` | Agent → Task | open task ownership |
| `briefs` | Coordinator → Agent | dispatch shape (e.g., Athena briefs Grace on a feature) |
| `reviews` | Agent → Artifact | applies a second-voice review pass |
| `producedBy` | Artifact → Identity | inverse `produces` |
| `decidedBy` | DecisionRecord → Identity | |
| `affects` | DecisionRecord → Surface | which surfaces are downstream |
| `shipsIn` | Artifact → ReleaseTag | release-bound artifact tracking |
| `participatesIn` | Identity → Conversation | inverse `hasParticipant` |
| `hostedBy` | Conversation → Identity | meeting-host pattern |
| `invitedTo` | Identity → Meeting | invitation lifecycle entry |
| `targetsAudience` | Artifact → AudienceShape | content-targeting |
| `hasAudienceShape` | Identity → AudienceShape | non-functional; an Identity can fit multiple shapes |
| `hasReachability` | Identity → ReachabilityPolicy | functional |

## Class axioms (the substantive ones)

### Identity partition

```
Class: Person
  SubClassOf: Identity
  DisjointWith: Agent

Class: Agent
  SubClassOf: Identity
  DisjointWith: Person

Class: Founder
  SubClassOf: Person

Class: PermanentAgent
  SubClassOf: Agent
  DisjointWith: EphemeralAgent

Class: EphemeralAgent
  SubClassOf: Agent
  DisjointWith: PermanentAgent
```

`Coordinator`, `Developer`, and `Frontend` are sub-classes of
`PermanentAgent` but **are not pairwise disjoint** — an agent can hold
multiple roles simultaneously (Athena is both Coordinator and
Developer; she reviews + writes non-feature code).

```
Class: Coordinator
  SubClassOf: PermanentAgent

Class: Developer
  SubClassOf: PermanentAgent

Class: Frontend
  SubClassOf: Developer
```

### Surface partition

Surfaces are pairwise disjoint:

```
Class: Direction
  SubClassOf: Surface
  DisjointWith: Engineering, Operations, Support, Outreach, Analytics

(and analogously for each Surface pair)
```

### Surface ownership

Every coordinator runs at least one surface; every surface is run by
exactly one coordinator (single-ownership is load-bearing — co-ownership
of a surface signals "we should split the surface," not "two
coordinators run it together"):

```
Class: Coordinator
  SubClassOf: runs some Surface

Class: Surface
  EquivalentTo: inverse runs exactly 1 Coordinator
```

### Team membership

Every Identity is on at least one Team:

```
Class: Identity
  SubClassOf: memberOf some Team
```

A Bridge is an Agent that is on two or more Teams (currently Athena
is the only Bridge — she's on `default:aweb.ai` for company coordination
and `aweb:juan.aweb.ai` for dev-team coordination):

```
Class: Bridge
  EquivalentTo: Agent and (memberOf min 2 Team)
```

Founders are on both PublicTeam and PrivateTeam:

```
Class: Founder
  SubClassOf:
    (memberOf some PublicTeam) and
    (memberOf some PrivateTeam)
```

### Tasks and dispatch

```
Class: Task
  SubClassOf: Artifact and (producedBy some Identity)

Class: Brief
  SubClassOf: Artifact and
    (producedBy some Coordinator) and
    (briefs some Agent)

ObjectProperty: claims
  Domain: Agent
  Range: Task
```

Only Agents claim Tasks; Founders make decisions and frame work but
do not claim tasks themselves.

### Reviews (two-voice discipline)

A substantial artifact must have at least one reviewer (a non-author
agent). This encodes the "substantial work needs two voices"
invariant from `docs/agent-first-company.md`.

```
Class: SubstantialArtifact
  SubClassOf: Artifact and (inverse reviews min 1 Agent)
```

What counts as Substantial is per-artifact-type judgment in prose;
not all Artifacts are SubstantialArtifacts (a single typo fix is an
Artifact but not Substantial).

### Decisions

```
Class: DecisionRecord
  SubClassOf:
    Artifact and
    (decidedBy some Identity) and
    (affects min 1 Surface)
```

### Conversations

```
Class: Meeting
  SubClassOf:
    Conversation and
    (hostedBy some Identity) and
    (inverse participatesIn min 2 Identity)
```

Mail and Chat are Conversations without the host/agenda structure
of Meetings.

### Reachability

Every Identity has exactly one ReachabilityPolicy:

```
Class: Identity
  SubClassOf: hasReachability exactly 1 ReachabilityPolicy

Class: ReachabilityPolicy
  DisjointUnionOf: Nobody, Contacts, TeamMembersOnly, OrgOnly, Public
```

Default for new consumer hosted identities is `Public` (since
2026-05-14, v0.5.35); prior identities default to `Nobody`.

### Audience shapes

AudienceShape is NOT a kind of Identity — it's a descriptor of an
audience category, not a thing in the world that participates in
agent-first life:

```
Class: AudienceShape
  DisjointWith: Identity

Class: AudienceShape
  DisjointUnionOf: P1Consumer, P2CompanyFleet, P3DeveloperTeam, P4PlatformBuilder
```

An Identity can `hasAudienceShape` for content-targeting purposes
without being an instance of an AudienceShape:

```
ObjectProperty: hasAudienceShape
  Domain: Identity
  Range: AudienceShape

ObjectProperty: targetsAudience
  Domain: Artifact
  Range: AudienceShape
```

Real signed-up users can fit one or more AudienceShapes (joanmg
signed up; she fits P1Consumer); the relation is non-functional.

### Primitives (four-primitives-independent)

The four load-bearing primitives are named here as a structural axiom.
The code-dependency invariant ("no Primitive depends on another's
internals") is described in prose in `docs/invariants.md` —
DL can't express the constraint cleanly and forcing it would muddy
this ontology.

```
Class: Primitive
  SubClassOf: Repository
  DisjointUnionOf: aweb_OSS_Repo, awid_Registry_Repo, ac_Cloud_Repo, ai_aweb_Coordination_Repo
```

## Cross-references

- `docs/team.md` — current team roster mapped to roles in this
  ontology (acts as an ABox of Sofia, Athena, Hestia, Aida, Iris,
  Metis; Mia, Grace, Kate, Noah, Olivia, Peter)
- `docs/agent-first-company.md` — the operating model that the
  vocabulary describes
- `docs/invariants.md` — the company invariants, including the
  four-primitives-independent code-dependency rule that this
  ontology names but doesn't enforce
- `publishing/voice.md` — vocabulary boundaries for external copy;
  references the same Identity / Surface / Customer vocabulary
- `docs/audiences.md` — full descriptions of P1/P2/P3/P4 personas
- `docs/meetings-design.md` — scheduled-meeting architectural design;
  uses the Meeting class defined here

## When to update this document

- Adding a new Surface (rare; signals we've grown beyond six work
  surfaces)
- Adding a new permanent role-class or specialization
- Adding a new Artifact type that gets cross-referenced often (e.g.,
  if `Seminar` becomes a load-bearing artifact, it joins the Artifact
  hierarchy)
- Adding a new audience persona (rare)
- Renaming or merging existing classes (record the change in
  `docs/decisions.md`)

Don't update for one-off agents (those are ABox-level, not TBox).
Don't update for tactical operating-pattern changes (those live in
`docs/agent-first-company.md`).
