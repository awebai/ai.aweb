# Decisions

When the plan changes, record it here with the commit hash(es) that
mark the moment. Agents check this for entries newer than their last
handoff to detect that the world changed.

---

## 2026-04-21 — Amy gets a second address at aweb.ai/amy

**Decision maker:** Juan

Amy's persistent `did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ` now holds two
public addresses: the original `juan.aweb.ai/amy` and the new
`aweb.ai/amy`. Both have reachability `public`. Amy is the canonical
support address for aweb; routing `aweb.ai/amy` to her makes the
public-facing address match the company domain.

Steps taken (all on Juan's workstation, 2026-04-21 21:47 UTC):
1. Verified `aweb.ai` is BYOD at awid; controller `did:key:z6Mkgpop…EuVn`
   matches `_awid.aweb.ai` TXT.
2. Installed the controller seed from `ac/.env.production`
   (`AWEB_PARENT_CONTROLLER_KEY`) at
   `~/.config/aw/controllers/aweb.ai.key`, overwriting a stale key
   (backed up as `.bak-2026-04-21`).
3. `aw id namespace assign-address --domain aweb.ai --name amy
   --did-aw did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ --reachability public`
   → address_id `69c4346c-a2d6-4c0d-b626-359884467eff`.
4. Created team `aweb:aweb.ai` (team did:key `z6MkhSLsj1bk…NiH2`)
   and issued Amy a persistent cert with `member_address=aweb.ai/amy`
   (certificate_id `30324a6d-e8e3-432a-bc31-5943875bc51d`). Cert saved
   at `agents/support/.aw/team-certs/aweb__aweb.ai.pem`; membership
   added to `teams.yaml`.

What's live: inbound to `aweb.ai/amy` routes to Amy's `did:aw`.

What's dormant: the `aweb:aweb.ai` team membership exists but is not
the active team, and no aweb-side coordination workspace has been
provisioned for it. Amy's outbound sender address stays
`juan.aweb.ai/amy`. Activating outbound-as-`aweb.ai/amy` requires
`aw init` against the new team on Juan's decision; that's a separate
step because it changes Amy's visible sender identity.

Affects: support agent (`agents/support/`).

---

## 2026-04-18 — Idempotent address registration at awid

**Commits:**
- aweb: `3b264f0` (awid-sot §Addresses Idempotency); epic aweb-aajw,
  subtask aweb-aajw.15

**Decision maker:** Juan

Symmetric with the resume-from-partial decision on register_did:
`POST /v1/namespaces/{domain}/addresses` becomes idempotent on
exact (domain, name, did_aw, current_did_key) match. Any mismatch
stays 409. Dave surfaced the gap in his aajw.8 review — if awid
accepts an address but the cloud transaction commit then fails, the
retry driven by aajw.13's resume path would 409 without this
behavior, orphaning the address at awid.

Rejected alternatives:
- Server-side pre-check via GET before register — extra round-trip
  on every init, more code on the cloud side.
- Accept for pre-launch with operational cleanup later — reverses
  the parallel decision we took on register_did and leaves
  retry-after-failure unusable.

---

## 2026-04-18 — Resume-from-partial bootstrap, not awid DID cleanup

**Commits:**
- aweb: epic aweb-aajw, subtask aweb-aajw.13

**Decision maker:** Juan

On the API-key persistent bootstrap, awid registration now happens
BEFORE /workspaces/init (aajw.6). If /workspaces/init fails after
awid registration succeeds, a naive retry generates a fresh keypair
and orphans the first did:aw at awid. Dave surfaced this in his
review of 2b2e16f.

Chose option 2 of three: the CLI persists the signing key and
derived identity material to a local partial-init file BEFORE
calling awid, then reuses it on retry. Successful completion
removes the file. awid stays append-only — no cleanup endpoint.

Rejected alternatives:
- Accept the orphans for pre-launch and add operational cleanup
  later — leaves unbounded drift at awid.
- Add an awid endpoint to delete unbound did:aw entries — violates
  the append-only audit-log property and expands protocol surface
  for a problem the CLI can solve locally.

---

## 2026-04-18 — Replace/Archive multi-address policy

**Commits:**
- aweb: epic aweb-aajw, subtask aweb-aajw.12

**Decision maker:** Juan (on Jack's recommendation, from Alice's audit)

A persistent DID can hold multiple addresses across namespaces. The
cloud's Replace and Archive lifecycle flows must honor that:

- **Replace**: reassign every cloud-managed address for the old DID
  to the new DID, atomically. BYOD addresses are left untouched — the
  cloud does not hold the namespace controller key for those, so it
  has no authority to migrate them.
- **Archive**: delete every cloud-managed address for the DID. BYOD
  addresses are left untouched for the same reason.
- **Reachability** stays per-address. A DID can carry different
  reachability per address. The dashboard presents the team-managed
  address as primary for now.

Affects: `ac/backend/src/aweb_cloud/routers/agent_lifecycle.py` and
the six `list_did_addresses[0]` sites surfaced in Alice's audit
(agent_addressing.py, init.py, onboarding.py, agent_lifecycle.py).

---

## 2026-04-18 — Split awid identity registration from address binding

**Commits:**
- aweb: (pending) — `docs/awid-sot.md` Identity operations section,
  Addresses precondition, `did_aw_mappings` schema update;
  `docs/trust-model.md` identity vs address authority;
  `docs/identity-guide.md` two-step flow

**Decision maker:** Juan

awid's `POST /v1/did` bundled identity registration (`did_aw ↔ did_key`)
with an address claim into a single signed envelope. This forced a
cycle for managed addresses: a self-custodial identity holder had to
sign over an address they did not yet own, while the namespace
controller (the hosted operator) had no way to pre-register the
identity before assigning the address. Juan's 2026-04-17 precheck
`15aab802 "Require awid registration before managed addresses"` made
the invariant explicit on the server side but could not be satisfied
by the existing CLI flow — mechanically impossible.

Chosen resolution: split the awid protocol into two separately
authorized operations.

- `register_did` — identity holder signature only, binds
  `did_aw ↔ did_key`. No address in envelope or state hash.
- Address binding stays at `POST /v1/namespaces/{domain}/addresses`,
  namespace controller signature, with awid rejecting the call if
  `did_aw` is not already registered.

Rationale: identity and address are semantically independent facts
with different authorities. Bundling them collapses the authority
model, forces pre-launch protocol band-aids, and makes cross-namespace
memberships awkward. Splitting them makes the "identity before address"
invariant structural, gives each party the authority it legitimately
holds, and matches the log-based identity model already sketched in
`aweb/docs/vectors/identity-log-v1.json`.

Cost: awid schema migration (drop address/server/handle from
`did_aw_mappings`; drop denormalized `current_did_key` from
`public_addresses` and resolve via JOIN so a DID can hold multiple
addresses without rotation cascades), CLI two-step flow in
`aw id create` and the API-key bootstrap path, server-side obligation
for the hosted operator to submit the two ops in order. Estimated
3–5 days.

Alternatives rejected:
- Two-phase CLI "prepare" endpoint — a workaround for the coupling,
  not a fix; bakes the bug into the protocol.
- Server registers DID on behalf using the public key in the
  payload — requires extending awid to accept controller-authorized
  identity registrations, which breaks the authority model.
- Revert the precheck — loses the invariant (managed addresses
  pointing at DIDs awid doesn't know), which is foundational.

Affects: awid server and schema, `aw` CLI identity creation + bootstrap,
`ac` hosted operator init flow, identity-log conformance vectors.
Launch-blocker for the API-key persistent bootstrap; Juan's
2026-04-18 attempt to re-provision `juan.aweb.ai/avi` surfaced this.

Source of truth: [`aweb/docs/awid-sot.md` — Identity
operations](https://awid.ai/awid-sot.md#identity-operations).

---

## 2026-04-11 — Content publishing split

**Commits:**
- co.aweb: `fd59be4` — Add content strategy decision and publishing plan

**Decision makers:** Juan + Enoch (board)

Personal, story-driven posts publish on juanreyero.com. Technical and
protocol posts publish on aweb.ai/blog (to be set up in the Hugo site).

juanreyero.com has domain authority and a real person behind it —
personal stories land better from a person than a company. Technical
content on aweb.ai builds the domain's authority and keeps interested
readers on-site.

The linking pattern: juanreyero.com posts mention aweb and link to
aweb.ai. aweb.ai/blog posts link to the repo and docs.

Affects: CEO should use this split when approving content. Hugo site
needs a blog section. Content plan (content/plan.md) tracks what goes
where.

---

## 2026-04-06 — Migrate to full public-key cryptographic identity

**Commits:**
- aweb: `9212616` — Add team architecture SOT for aweb server and CLI
  (first migration commit; 15+ followed on same day: awid SOT rewrite,
  certificate auth, team CRUD, connect flow, middleware)
- ac: no commits until April 9 — migration reached cloud on `933d606`
  (Pin backend local dev to sibling aweb) and team certs arrived on
  April 9-10 starting with `1a7190f` (Mint real team certs for
  custodial API keys)

**Decision maker:** Juan

Replace bearer tokens and API keys with Ed25519 public-key
cryptographic identity (`did:aw`) and team certificates throughout
the stack (aweb, aweb-cloud, awid).

The old architecture worked for single-server coordination but can't
support cross-org agent communication, offline signature verification,
true agent ownership of identity, or external services built on the
identity layer.

Cost: full rewrite of auth paths, production database reset, ~1-2
weeks of engineering, delayed shipping and outreach. Accepted because
migrating after users are on the platform would be 10x harder.

Affects: everything — aweb OSS, aweb-cloud auth bridge, awid registry,
CLI flows, all agent identities.
