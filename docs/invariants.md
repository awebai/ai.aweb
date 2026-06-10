# Product Invariants

Guiding principles that must hold in every design decision, every
feature, and every user-facing behavior. These aren't rules about
specific bugs — they're the architectural and business truths from
which correct decisions follow.

Read this on every wake-up. If a design decision feels uncertain,
check it against these principles.

---

## 1. The four primitives are independent

Namespace, identity, address, and team are orthogonal concepts that
compose freely. None depends on any other. Any combination is valid:

- An identity with no addresses and no teams
- An address with no team membership
- A team member with no address in that namespace
- An identity in ten teams across five namespaces

When you find yourself requiring one primitive to use another — team
membership to send a message, an address to join a team, a namespace
to have an identity — you are creating coupling that shouldn't exist.
The architecture's power comes from this independence.

This is the deepest architectural truth. Most design mistakes come
from conflating two primitives that should be separate.

## 2. DNS anchors trust, crypto verifies it

The trust model flows from DNS downward: DNS → namespace controller →
team controller → agent. At every level, the relevant party signs
with their key, and anyone can verify the signature without trusting
a middleman.

Implications:
- The registry stores public state. It never holds private keys. It
  never signs on anyone's behalf.
- Any service can verify a team certificate by fetching the team's
  public key once and checking signatures locally. No live call to
  the team controller needed.
- A signature from an agent at `acme.com` is verifiable by anyone
  who can look up the public key — no relationship with acme.com
  required.
- If you're building something that requires trusting a central
  service for authorization (not just convenience), you're adding
  trust that the architecture doesn't require.

## 3. Custody is a choice at every layer, not a system property

Namespace key, team key, agent key — each can be self-custody or
custodial, independently. The protocol treats all custody arrangements
identically: whoever holds the private key is the controller.

A self-custodial agent and a custodial agent produce identical signed
artifacts. A service verifying a request cannot tell (and should not
care) whether the signing key lives on a laptop or in a cloud vault.

Don't build features that only work for one custody model. Don't
assume custody layers align.

## 4. Coordination is the product, identity is the infrastructure

Users come for "my agents stopped stepping on each other." They stay
for tasks, claims, messaging, presence, roles. They don't come for
cryptographic identity, DIDs, or DNS-anchored namespaces.

Identity makes coordination trustworthy and portable across
organizational boundaries. It's essential infrastructure. But it's
not what people buy.

Every feature should ultimately serve the coordination experience.
Identity features that don't make coordination better, more
trustworthy, or more portable aren't justified yet.

## 5. Progressive disclosure is a product requirement

The full model — DIDs, key rotation, custody modes, BYOD namespaces,
cross-org certificates — is the long-term architecture. It is not
what new users see.

Stage 1 (first 5 minutes): `aw init`, agents see each other, tasks
and messaging work. No identity model explanation, no team
configuration, no namespace choice.

Each later stage reveals the next layer of capability only when the
user hits a real need for it. See `user-journey.md` for the full
progression.

If a change makes the first 5 minutes harder, it's wrong regardless
of how architecturally sound it is. If a user must understand a
concept from Stage 5 to complete a task in Stage 1, the design is
wrong.

## 6. Distribution over features

Zero users means nothing else matters. Once the product works, every
hour spent on more engineering instead of getting it in front of
people is wasted.

Audience 1 (developer teams running 2-5 agents) comes first. They
pay for coordination. Audience 2 (cross-org agent networks) comes
later and drives network effects.

Features that only serve Audience 2 while Audience 1 hasn't been
found are premature.

## 7. Open and portable

MIT license. Self-hostable. No vendor lock-in. The hosted service
at aweb.ai is a convenience, not a requirement.

If a feature only works with the hosted service, it should be because
of inherent operational needs (billing, managed namespaces) — not
because the design made self-hosting impossible.

An agent that starts on the hosted service and later moves to
self-hosting should lose convenience features, not identity or
coordination history.

## 8. Global findability and local continuation are separate concerns

A global identity is intentionally findable: it has a `did:aw`, an
AWID identity record, and optionally address aliases that resolve to
that identity. Registry reachability flags are legacy metadata, not a
routing or resolver authority.

A local identity is intentionally not globally findable: it has a
`did:key` only, no AWID row, no `did:aw`, and no global first-contact
route. It can still participate across a boundary after it writes out,
because the recipient learns a return route through authenticated
participant/session state.

Continuation — who can keep talking once contact exists — depends on
stored participant/session route state and identity signatures, not on
whether the recipient is globally findable and not on `conversation_id`
as a standalone capability. Conversation/thread IDs may remain UX,
history, wait/read, and idempotency metadata; they must not be the
routing authority by themselves.

When you find yourself preserving a "hidden global" reachability class
or requiring a conversation ID to bypass resolver policy, you are
reintroducing the old middle state. Choose global if the agent should
be first-contactable; choose local if it should not.

Do not manufacture legacy fields from canonical state. A compatibility
adapter may accept old input and normalize it at the boundary; a
migration may read old storage while removing it; an audit may expose
actual persisted old values as explicitly legacy evidence. But a
service must not derive `lifetime`, `reachability`, `access_mode`, or
similar old nouns from new canonical fields just to preserve an old
shape. Derived legacy fields are product-authority residue, not
compatibility.

## 9. Rollback is transactional over local writes and conservative about remote uncertainty

Failure-path rollback must be transactional over known local writes and
conservative about remote uncertainty. Automatic rollback may remove
only local artifacts that the current attempt created and that are not
the only remaining authority or correlation needed to reconcile a
possible remote side effect.

If remote state may have succeeded, preserve enough local state to
retry or repair, and surface the ambiguity. Destructive cleanup of
confirmed remote state must be an explicit lifecycle or recovery action
with the right authority, not an incidental rollback, read, or status
side effect.

Rollback must be manifest/snapshot-based, never broad `rm -rf .aw`.
It must preserve pre-existing `.aw` plus any partial-init or recovery
marker unless an explicit user/operator cleanup command is being run.

This is the shared invariant behind two incident classes:

- A read/status-shaped cleanup must not infer server deletion from a
  stale local path and delete remote workspace/agent rows (#245).
- A failed connect/init attempt must not delete the last local key or
  correlation handle when remote identity creation may already have
  succeeded (aweb-aaqi bug 3).

The safety bar is preserving the authority and evidence needed to
repair ambiguity. Cleanup that destroys identity state, global rows,
namespace registrations, or remote workspaces belongs behind explicit
lifecycle/recovery commands and the appropriate controller/admin
authority.

## 9. Failure-path rollback is transactional locally, conservative remotely

Failure-path rollback must be transactional over known local writes
and conservative about remote uncertainty. Automatic rollback may
remove only local artifacts that this attempt created and that are
not the only remaining authority/correlation needed to reconcile a
possible remote side effect. If remote state may have succeeded,
preserve enough local state to retry or repair, and surface the
ambiguity. Destructive cleanup of confirmed remote state must be an
explicit lifecycle/recovery action with the right authority, not an
incidental rollback/read/status side effect.

Corollary: rollback must be manifest/snapshot-based, never broad
`rm -rf .aw`, and must preserve pre-existing `.aw` state plus any
partial-init/recovery marker unless an explicit user/operator
cleanup command is being run.

The bar that matters: never destroy the last local signing authority
or durable correlation handle while remote success is possible.
"Confirmed absent" is unknowable after a timeout, a 422 following
partial success, or a network split — so the invariant demands
conservatism under uncertainty, not proof of absence before any
local cleanup.

Evidence chain: #245 (aw 1.26.3 read/status cleanup destroying
workspaces from stale local path state), aweb-aaqi bug-3 (connect
rollback deleting the key after remote init had already succeeded,
manufacturing a DID mismatch — fixed forward in aw 1.26.14,
commit 4518c85c). Operational application: Hestia runbook standing
policy #16; identity-state cleanups additionally need explicit
Juan-go or controller-signed authority.
