# Customer onboarding flows — three shapes, one product

This doc names the three customer shapes that show up at the
landing page and the actual click-by-click each one walks. Every
landing-page or onboarding-shaped review **must** start with the
question: which shape is this section addressing, and does the flow
it describes actually work for that shape?

The first version of the homepage refresh (Pass-1, Pass-2) failed
this test: the "No developer needed" section gave Shape A
customers a flow that only works for Shape B. The text said "your
agent handles the rest" but the action it gave them — paste a
prompt that tells an agent to read a guide and run install
commands — only works if the agent can run shell commands. Shape
A agents (claude.ai web, ChatGPT web) cannot.

This doc exists so that mistake doesn't recur.

---

## Shape A — Custodial-MCP customer ("no developer needed")

**Who they are.** Someone running an AI agent that lives in a
browser or in a desktop app. They don't have a terminal open;
they don't run shell commands; "open a config file in your
editor" is plausibly already too far for them.

**Tools they're using.** claude.ai (web), ChatGPT (web), Claude
Desktop, sometimes Cursor agents in MCP mode.

**What they can do.**
- Click in a UI
- Copy and paste text
- Open their AI client's settings page
- Approve an OAuth consent screen

**What they cannot do.**
- Run shell commands from inside the agent
- Read instructions intended for terminal users
- Edit JSON config files (Claude Desktop's traditional MCP setup
  still requires this, which is a real friction point and an
  honest limit on the "no developer needed" pitch for that
  client specifically)

**Actual click-by-click in the product today** (verified against
AC code, OAuth MCP path is fully implemented):

1. **Sign up at app.aweb.ai.** Email/password or OAuth (Google,
   GitHub).
2. **Onboarding page** offers two paths: "Create local identity"
   (CLI) or "Create hosted identity" (browser/desktop). Customer
   picks "Create hosted identity."
3. **Fill a short form** — identity name (e.g. "researcher"),
   optional display name, role from a dropdown.
4. **Click Create.** AC mints a hosted (custodial) `did:aw`
   identity; AC holds the signing key on the customer's behalf.
5. **Connect page appears** with the MCP server URL:
   `https://app.aweb.ai/mcp/`. Customer copies that URL.
6. **In their AI client** (Claude Desktop / claude.ai / ChatGPT)
   the customer adds aweb as a remote MCP server using that
   URL. The mechanics differ by client:
   - **claude.ai (web)**: Settings → Connectors → Add MCP server
     → paste URL.
   - **ChatGPT (web)**: similar (ChatGPT MCP support is newer;
     verify per-client UX before claiming).
   - **Claude Desktop**: edit
     `~/Library/Application Support/Claude/claude_desktop_config.json`
     — this is the friction point above; not strictly
     "no developer needed."
7. **OAuth handshake** runs automatically: the client discovers
   `/.well-known/oauth-authorization-server`, self-registers via
   POST `/oauth/register`, redirects the customer to
   `/oauth/authorize` (PKCE).
8. **Customer sees the consent screen.** Selects which team and
   which hosted identity to grant the client access to. Clicks
   "Approve."
9. **Done.** The client exchanges the authorization code for
   tokens at `/oauth/token`. Their agent now has 30 MCP tools
   available — mail, chat, tasks, roles, work discovery, etc.
   It can coordinate with other agents in the same team using
   the hosted identity.

**Total explicit human steps: ~8.** Sign up, create identity,
fill form, click create, copy URL, paste into client, approve
consent, done.

**The honest framing for this customer.** Not "your agent
handles the rest" — there are three explicit human actions
between signup and the agent being live (steps 5, 6, 8). The
honest framing is "Sign up. Add aweb to your AI client.
Approve. Done." The tradeoff is real and it is the lowest-floor
flow the product offers; pretending otherwise loses trust.

**Where the flow is implemented:**
- Frontend form: `ac/frontend/src/components/dashboard/TeamAgentSetupFlow.tsx:156-187`
  (`createHostedIdentity`)
- Backend identity creation: `ac/backend/src/aweb_cloud/routers/init.py:1877-1979`
  (POST `/api/v1/identities/create-permanent-custodial`)
- Connect page: `ac/frontend/src/pages/TeamAgentConnectPage.tsx:170-235`
  (`McpConnectInstructions`)
- OAuth flow: `ac/backend/src/aweb_cloud/routers/mcp_oauth.py:855-1088`
  (register → authorize → submit → token)
- Consent screen renderer: `ac/backend/src/aweb_cloud/routers/mcp_oauth.py:141-404`
  (`_render_authorize_consent_html`)

**Bearer-token MCP fallback.** A second tab on the connect page
gives the customer a static JSON snippet with a bearer token
(`aw_sk_...`) for clients that don't support OAuth. This is a
manual copy-paste flow; not the primary path. Code:
`ac/frontend/src/components/dashboard/McpConnectInstructions.tsx:57-73`.

---

## Shape B — CLI developer customer ("paste this prompt")

**Who they are.** A developer running an AI agent that lives in
a terminal. The agent can run shell commands.

**Tools they're using.** Claude Code (CLI), Codex CLI, Aider,
sometimes Claude Desktop with shell-execution MCP servers
wired up.

**What they can do.**
- Everything Shape A can do
- Run shell commands from inside the agent
- Install packages, edit files, run binaries

**Actual click-by-click in the product today:**

1. **Install the CLI**: `npm install -g @awebai/aw`
2. **Initialize a workspace**: `aw init` — creates a team,
   workspace, ephemeral identity, joins server.
3. *(Optional)* **Tell the agent to read the guide**: paste
   `Read the agent guide at https://aweb.ai/agent-guide.md`
   into the agent. The agent fetches the guide and self-
   configures further (e.g. runs `aw channel install` for MCP
   integration with Claude Code).
4. *(Optional)* **Persistent identity**: `aw id create --persistent --name <alias>`
   for an identity that survives across sessions.

**Total explicit human steps: 2-4.** Install, init, optionally
delegate the rest to the agent.

**The honest framing for this customer.** "Your agent handles
the rest" *is* true here — once `aw init` is run, an agent that
can run shell commands really can take care of further
configuration via the agent-guide. The prompt-paste pattern
belongs in the developer section of the landing page, not the
no-dev section.

**Hybrid path:** The CLI customer can also claim an AC team API
key from the dashboard and feed it to `aw init` to land in an
AC-hosted team. This bridges the OSS CLI flow with the cloud
service. Code:
`ac/frontend/src/components/dashboard/CliSetupInstructions.tsx`.

---

## Shape C — Self-hosted operator

**Who they are.** Someone who wants their own awid + aweb-server
infrastructure. Often building a product on top of the protocol;
often operating at a scale or a sovereignty posture where they
don't want to depend on AC at all.

**Tools they're using.** Their own infra (Docker, Kubernetes,
bare metal). Their own DNS. Their own database.

**Actual click-by-click:**

1. Clone `awebai/aweb` (and optionally `awebai/awid`).
2. Run the servers per `docs/SELF_HOSTING.md`.
3. Configure DNS for their namespace (`_awid.<domain>` TXT
   record).
4. Run `aw init --server <their-server>` against their own
   instance.

**The honest framing for this customer.** They are not a
landing-page customer in the conversion sense. They will arrive
through the GitHub repo, the docs, or via Audience 2 contact
(see `audiences.md`). The landing page should not optimize for
them; it should not get in their way. A footer link to GitHub
and a "self-host" entry in docs is enough.

---

## Implications for landing page review

When reviewing any landing-page section that addresses customer
onboarding or installation:

1. **Name the shape.** Is this section addressing Shape A, B, or
   C? If it's trying to address more than one in the same
   block, it's almost certainly going to confuse one of them.
2. **Walk the flow as that customer.** Read the section as a
   Shape A customer. Now actually try to do what it tells you.
   If you reach a step you cannot perform with that customer's
   tooling, the section is broken.
3. **Verify against product reality.** The flow described must
   match what the product actually does today. If the section
   describes an MCP one-click flow but the product requires
   manual JSON edits, that's a misframe — fix the section or
   fix the product.
4. **Check the implicit frame.** "Your agent handles the rest"
   is true for Shape B and false for Shape A. Watch for promises
   that only land for one shape and harm trust for the other.

This is the question that has to be on the table before any
copy or structural review. If it's not, the review is going to
miss the shape that the section was wrong for.

---

## Banked discipline (this doc's reason for existing)

**Customer-shape verification before landing-copy review.**
Identify which onboarding shape (A custodial-MCP, B CLI dev, C
self-host) each landing section addresses, and walk the
described flow as that customer using only that customer's
tooling. A section that promises something the customer cannot
do — even if the words are pretty — is broken.

Reason: the homepage refresh's "No developer needed" section
shipped to Pass-1 and Pass-2 staging with a flow that only
worked for Shape B customers labeled as Shape A. The miss was
visible to a careful reader from the moment the section was
drafted; not catching it cost a stage in the release pipeline
and cost trust.

How to apply: every Sofia wake-up that touches landing-page
review starts here. Iris and Aida should also reference this
doc when authoring or supporting customer-facing flows.
