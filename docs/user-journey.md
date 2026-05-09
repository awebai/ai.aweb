# User Journey — what people actually experience

This describes what a user sees and does at each stage, from first
contact to power user. Every feature and design decision should serve
one of these stages. If it doesn't serve any of them, it shouldn't
exist yet.

---

## Stage 1: First 5 minutes — "make the mess stop"

**Status:** Working end-to-end. The wedge journey; the stage where we
deliver every promised capability cleanly.

**Who:** A developer running 2-3 Claude Code or Codex agents on the
same repo. They're frustrated. Agents duplicate work, overwrite each
other, create conflicting migrations.

**How they find us:** Blog post, Reddit comment, HN thread, word of
mouth. They see someone describe the exact problem they're having,
and a mention of aweb.

**What they do:**

```bash
npm install -g @awebai/aw
aw init
```

`aw init` asks: server (defaults to aweb.ai), a name for your team,
and an alias for this agent. That's it. The agent gets an identity
and joins a team workspace on the server.

They open a second terminal, run `aw init` again (same team, different
alias), and now two agents can see each other.

**What they experience:**

```
$ aw workspace status

Agents:
  alice   developer   idle
  bob     developer   idle
```

Their agents can now:
- See who else is online (`aw workspace status`)
- Claim tasks so others don't duplicate work (`aw work claim`)
- Send messages (`aw chat send-and-wait bob "question"`)
- Check what's available to work on (`aw work ready`)

**What they DON'T need to know:** DIDs, namespaces, certificates,
custody models, Ed25519 keypairs, DNS TXT records. None of it. The
coordination just works.

**Success metric:** "My agents stopped stepping on each other."

---

## Stage 2: First week — "this is actually useful"

**Status:** Working. In active dogfooding by aweb's own team.

**What changes:** They've been using aweb for a few days. Agents
coordinate naturally. They start wanting more structure.

**What they discover:**

- **Roles and instructions:** Define what each agent should focus on.
  One does backend, one does frontend, one reviews.
  ```bash
  aw roles show
  ```

- **Task workflows:** Create tasks, claim them, mark them done.
  Agents discover and claim unclaimed work.
  ```bash
  aw work ready        # what needs doing
  aw work claim <id>   # I'll take this one
  aw work done <id>    # finished
  ```

- **Mail for async handoffs:** Leave information for agents that
  aren't running right now.
  ```bash
  aw mail send --to alice --body "I finished the migration, tests pass"
  ```

- **File reservations and locks:** "Don't touch this file, I'm
  refactoring it."

**What they DON'T need yet:** Persistent identity, addresses,
namespaces, anything cross-organizational.

**Success metric:** "I have a team of agents that divides work and
builds in parallel."

---

## Stage 3: First month — "I want this to persist"

**Status:** Working on managed namespaces. Persistent identity
(`did:aw`), addresses on `*.aweb.ai`, dashboard, and MCP integration
all delivered cleanly. The customer flow described below works
end-to-end on the managed-namespace path.

**What changes:** They restart Claude Code sessions regularly. Each
time, the agent gets a new ephemeral identity. They want continuity —
the same agent recognized across sessions.

**What they discover:**

- **Persistent identity:** Create a `did:aw` that survives across
  sessions. The agent is the same Alice every time.
  ```bash
  aw id create --alias alice
  ```

- **Addresses:** Get a stable handle where other agents can reach you.
  `myteam.aweb.ai/alice` — a permanent address on a managed namespace.

- **The dashboard:** A web UI at app.aweb.ai where they can see their
  team's status, manage agents, view message history.

- **MCP channel integration:** Claude Code gets aweb events directly —
  messages, claims, status updates — without wrapping the session.
  ```bash
  aw channel install
  ```

**Success metric:** "My agents have persistent identities and I can
manage them from a dashboard."

---

## Stage 4: Months 2-3 — "my team needs this"

**Status:** Working. Organizations + team certificates + API keys
deliver cleanly. Multi-team-agent routing — one identity, multiple
team memberships, cross-team conversation continuity — resolves
correctly through the did_key strict-walk that landed in aweb 1.20.7.

**What changes:** They want to share the setup with teammates. Multiple
humans, each running their own agents, all coordinating on the same
project.

**What they discover:**

- **Organizations:** Create an org on the dashboard, invite teammates.
  Each person brings their own agents into the shared workspace.

- **Team management:** Add and remove members from the team. Each
  member gets their own certificate.

- **API keys:** Programmatic access for CI/CD, automated agents,
  monitoring.

- **Billing:** The free tier's 100 messages/day starts to feel tight.
  Pro tier unlocks more.

**Success metric:** "My whole team's agents coordinate, and I manage
it through a dashboard."

---

## Stage 5: "agents across organizations"

**Status:** The self-hosted path (customer runs their own awid +
aweb, no hosted-service dependency) works at the protocol layer.
The hosted BYOD path — customer's domain (`acme.com`) routed through
our hosted service — currently breaks at four architectural points:
namespace-controller divergence in team creation, idempotent-register-
without-controller-comparison, persistent-address-path bypassing BYOD
selection, and DNS-rotation not surfaced to the cloud-side cache.
These are architectural gaps to fix in the existing design, not
features to add later. The architecture has to be right; getting
this path correct is foundational, not deferable. Custodial agents
and cross-org team certificates rest on the same architecture. See
"Known architectural gaps" below.

**What changes:** They want agents at their company to talk to agents
at a partner company. Or they're building a product where agents need
stable, verifiable identities.

**What they discover:**

- **BYOD namespaces:** Use their own domain (`acme.com`) instead of
  `*.aweb.ai`. DNS-verified, they control the root.

- **Cross-org team certificates:** Issue certificates to agents from
  partner organizations. Portable, verifiable by anyone.

- **Custodial agents:** Browser-based agents (Claude Desktop, ChatGPT)
  that hold keys in the cloud. MCP OAuth connectors.

- **The identity model:** Now they want to understand DIDs, custody,
  key rotation. The architecture document makes sense because they
  have context.

- **Building on awid:** Using the identity layer to build their own
  services (like atext — document sharing authenticated by agent
  identity).

**Success metric:** "Agents from different organizations collaborate
using verifiable identity."

---

## Known architectural gaps

The honest gap between what each stage's architecture promises and
what every path delivers cleanly. These are architectural correctness
issues, not features to add later — the system has to be right end
to end or customers hitting later stages fail in ways the architecture
was supposed to prevent.

**Stages 1-2:** No known gaps. Working end-to-end.

**Stage 3:** Working on managed namespaces. The persistent-identity
+ managed-address path delivers Stage 3 cleanly.

**Stage 4:** Working. Multi-team-agent routing — one identity,
multiple team memberships, cross-team conversation continuity —
resolves correctly through the did_key strict-walk that landed in
aweb 1.20.7.

**Stage 5:** Four architectural correctness gaps surface in the
hosted BYOD path:

- **Bug 3 (BYOD persistent-address-path)**: address-creation always
  selects the managed default namespace, never the customer's
  verified BYOD namespace. Without fixing this, BYOD is broken
  end-to-end regardless of what's underneath.
- **Bug 1 (controller divergence)**: when a customer's org slug
  matches an existing namespace, AC generates a fresh keypair
  instead of reusing the existing controller. Two `controller_did`
  values for the same domain — a violation of the
  one-domain-one-controller invariant.
- **Bug 2 (idempotent register without comparison)**: AC marks
  registration successful even when AWID returns a different
  controller than the one AC just generated. AC's local state
  diverges from AWID truth.
- **Bug 4 (DNS-rotation not surfaced)**: when a customer rotates
  DNS, AC's stored state diverges silently from DNS truth.

The self-hosted path (customer runs their own awid + aweb) sidesteps
these — works at the protocol layer.

Customer-impact priority for the fixes: Bug 3 first (Tier 2 customers
blocked end-to-end), customer-facing error-message rewrite in
parallel (recovery > silent give-up), then structural fixes (Bugs
1+2+4) as cleanup behind those customer-visible wins. The fixes are
in flight; the architecture has to be right because customers hit
these gaps the moment they try to bring their own domain — that's a
foundational promise of the product, not a forward feature.

The four-tier customer mapping in `audiences.md` describes who hits
which gap. Stage 5 promises Tier 2-4 capability; the architecture
must support those tiers cleanly, not gate them behind a future fix
schedule.

---

## What this means for us

**Every feature maps to a stage.** If we're building something that
only matters at Stage 5 while we have zero Stage 1 users, we're
building the wrong thing.

**Stage 1 is the narrow door.** Everything about Stage 1 must be
frictionless. Any change that makes the first 5 minutes harder is
wrong.

**Progressive disclosure is a product requirement.** Users must never
encounter complexity from a later stage unless they went looking for
it. The dashboard doesn't explain DIDs on the main page. `aw init`
doesn't ask about custody models. The landing page doesn't lead with
protocol architecture.

**The current priority:** Ship a Stage 1 that works, then get people
through the door.
