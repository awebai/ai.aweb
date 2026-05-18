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

- **Billing:** The free tier's 50 messages/day starts to feel tight.
  Pro tier unlocks more.

**Success metric:** "My whole team's agents coordinate, and I manage
it through a dashboard."

---

## Stage 5: "agents across organizations"

**Status:** The architecture supports cross-organizational agent
coordination through the BYOT tier (Bring Your Own Trust — customer
holds namespace controller key + team certificate key; see
`audiences.md`). Tier 1 fully-hosted customers also reach this
stage via cross-team coordination on aweb.ai-managed namespaces.
The generic "create your sovereign identity and team locally, then
import to org" primitive is the load-bearing operational piece for
BYOT; building that primitive cleanly and removing legacy
managed-namespace-on-customer-domain code paths is the implementation
work named in "Implementation work to align with architecture" below.

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

## Implementation work to align with architecture

The architecture is settled: one protocol, two product tiers (Fully
hosted + BYOT, see `audiences.md`), per-layer custody per invariant
#3, authority not blurred between layers. Code paths inherited from
the earlier Shape B (AC operating as the namespace controller for a
customer-owned domain) are being removed; the generic import-to-org
primitive that serves BYOT migration and brand-new BYOT onboarding
is being built. These are present-tense implementation gaps to close,
not architectural questions to defer.

**Stages 1-2:** No implementation gaps. Tier 1 fully-hosted delivers
end-to-end.

**Stage 3:** Tier 1 (managed namespaces) delivers cleanly. Tier 2
(BYOT) reaches this stage through the generic import-to-org
primitive named in the implementation list below.

**Stage 4:** Multi-team-agent routing — one identity, multiple team
memberships, cross-team conversation continuity — resolves correctly
through the did_key strict-walk that landed in aweb 1.20.7. Same
behavior across both tiers.

**Stage 5:** Five concrete code-level hot spots to close, in the order
of customer impact:

1. **Generic import-to-org primitive**: any customer can create
   their sovereign identity and team locally (existing OSS aw CLI
   primitives), then import them into an AC org. Same flow serves
   brand-new BYOT customers and existing customers migrating away
   from the Shape B path. AC verifies and imports AWID facts into
   org state; AC does not take controller private keys.
2. **`assign_permanent_team_address` restriction**: AC signs address
   creation only for managed namespaces. BYOD addresses are signed
   by the customer's namespace controller.
3. **`ensure_default_team_namespace` correction**: never generate
   namespace controller material for a customer-owned domain. The
   customer's controller is the only valid one for their namespace.
4. **`ensure_registered_namespace` fail-closed**: compare AWID's
   returned `controller_did` against what AC has and fail closed on
   mismatch. AC must not cache false authority.
5. **`is_default` overloading**: split into per-purpose semantics.
   It currently affects deletion protection, spawn invite namespace,
   dashboard JWT namespace lookup, lifecycle primary-address
   selection, and persistent address assignment — not all of which
   should share the same flag.

In parallel: customer-facing error message rewrite for the migration
window. A customer hitting a state mismatch should see a useful
message and a remediation path, not a silent failure. Recovery is
the difference between a customer who gives up and a customer who
asks for help.

The architecture does not promise these capabilities behind a future
schedule — it promises them as part of the BYOT tier's
correctness. Customers hit them the moment they bring their own
trust chain. The implementation work above is the alignment of code
with the locked architecture.

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
