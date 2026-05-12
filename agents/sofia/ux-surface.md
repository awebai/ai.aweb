# aweb UX surface — inventory snapshot

Snapshot date: 2026-05-12. Counts from a fresh inventory of
`ac/site/`, `ac/frontend/`, `aweb/cli/`, and the aweb MCP server.
Working artifact staged for an upcoming simplification pass — not a
canonical doc.

## The five surfaces a real person sees

### 1. Landing site (`aweb.ai`)
- **11 docs pages**: Getting Started, Identity, Communication,
  Coordination, MCP Integration, Namespaces, API Reference, Channel,
  Events & Control, Self-Hosting, plus Privacy/Terms.
- **8 homepage sections**: Hero → "Two Paths" (addresses +
  coordination — features, not paths) → Team Quickstart → Hosted
  MCP → Under the Hood → "Two Paths to Production" (managed vs
  DNS — actual paths) → Pricing → CTA.
- **Nav**: Get started, Dashboard, Pricing, Docs, GitHub. Footer
  has Protocol / Ecosystem / Legal columns.
- "Two Paths" appears in two unrelated sections. The hero, the
  Team Quickstart card, and the Hosted MCP block each try to grab
  the visitor's first move with different CTAs.

### 2. Auth gate (`app.aweb.ai`)
- **9 pages**: `/login`, `/register`, `/forgot-password`,
  `/reset-password/:linkId`, `/verify-email/:linkId`,
  `/email-verified`, `/oauth/callback`, `/choose-username`,
  `/complete-profile`.
- Two near-duplicate pairs: `verify-email` / `email-verified` and
  `choose-username` / `complete-profile`.

### 3. Signed-in dashboard
- **9 team tabs**: Monitor, Tasks, Mail, Chat, Identities, Contacts,
  Roles, Connect, Settings. Identities vs. Contacts: both are
  "who's in this team," different angles.
- **`/onboarding`** wizard + Getting Started checklist + invite
  welcome banner — three different first-time prompts.
- **Public routes**: `/:username`, `/organizations/:slug`,
  `/invite/:code`, `/i/:code`, `/connect`, `/oauth/consent`.
- **8 modals/dialogs**: Create Team, Create Org, BYOT Identity
  Setup, CLI Identity Setup, Team Agent Setup, Send Message,
  Start Chat, Settings Help.
- `/connect` exists both as a public top-level route (consumer
  client picker) AND as an admin tab inside a team.

### 4. `aw` CLI
- **25 top-level commands**. Headline verbs: `init`, `id`, `chat`,
  `mail`, `contacts`, `task`, `work`, `workspace`, `version`,
  `doctor`, `upgrade`. Rarely-typed in normal use: `lock`,
  `notify`, `heartbeat`, `events`, `control`, `log`, `reset`,
  `claim-human`, `directory`. One hidden: `connect`.
- **`id`** alone has 13 subcommands; **`id team`** has 12;
  **`task`** has 10; **`chat`** has 8 (mail has 4).
- `work` (3 subs: ready/active/blocked) and `task` overlap
  conceptually.

### 5. MCP tools (what a custodial agent sees in claude.ai/ChatGPT/Desktop)
- **45 tools**, no `readOnlyHint`/`destructiveHint` annotations on
  any of them.
- **Duplicate verbs**: `list_contacts` and `contacts_list` are
  both registered. `send_message_to_contact` +
  `read_messages_from_contact` wrap mail+chat into friendlier
  verbs while `send_mail`/`chat_send`/`check_inbox` still ship.
- Known stubs (e.g., `add_contact_by_email`) still in the list.
- Categories visible to the agent: identity (1) / mail+chat (8) /
  agents (2) / tasks (10) / work+status (4) / roles+instructions
  (4) / contacts (6).

### awid (not really a user surface)
- One operator command: `awid serve`. No human-facing UX. Only the
  registry HTTP API matters, and it's consumed by aw + ac, not by
  people.

---

## ASCII map

```
                                  aweb's UX surface
                                          │
   ┌──────────────────┬──────────────────┼──────────────────┬─────────────────┐
   │                  │                  │                  │                 │
LANDING SITE      AUTH GATE         SIGNED-IN APP        aw CLI          MCP TOOLS
 aweb.ai         app.aweb.ai        app.aweb.ai         terminal      (claude.ai +
                                                                       ChatGPT +
                                                                       Desktop)

HOMEPAGE (8 sections)   /login                ┌─ TEAM TABS (9) ─┐    init        45 tools, no
 Hero                   /register             │ Monitor         │    id ─ 13 subs   readOnly hints
 Two Paths (features)   /forgot-password      │ Tasks           │    id team ─ 12   ─────────────
 Team Quickstart        /reset-password/:id   │ Mail            │    chat ─ 8     identity (1)
 Hosted MCP             /verify-email/:id     │ Chat            │    mail ─ 4     mail+chat (8)
 Under the Hood         /email-verified       │ Identities      │    contacts     agents (2)
 Two Paths (managed)    /oauth/callback       │ Contacts ┐ both │    task ─ 10    tasks (10)
 Pricing                /choose-username      │ Roles    │ are  │    work ─ 3     work+status (4)
 CTA                    /complete-profile     │ Connect  │"who" │    workspace    roles+instr (4)
                                              │ Settings ┘      │    doctor       contacts (6)
DOCS (11)                                     └─────────────────┘    upgrade      ─ duplicates:
 Getting Started                                                     version        list_contacts /
 Identity                                     ┌─ PUBLIC ROUTES ─┐    ─────────      contacts_list
 Communication                                │ /:username      │    rarely typed:
 Coordination                                 │ /organizations/ │    lock           wraps:
 MCP Integration                              │ /invite/:code   │    notify         send_message_
 Namespaces                                   │ /i/:code        │    heartbeat       to_contact
 API Reference                                │ /connect ◄──┐   │    events       (mail+chat
 Channel                                      │ /oauth/consent  │    control       wrapper)
 Events & Control                             └─────────────────┘    log
 Self-Hosting                                                        reset
 Privacy / Terms                              ┌─ ONBOARDING ────┐    claim-human
                                              │ /onboarding     │    directory
NAV                                           │ Getting-started │    connect ✱
 Get started ─┐                               │   checklist     │   (hidden)
 Dashboard ───┤ same place                    │ Welcome banner  │
 Pricing      │ if signed in                  │ (3 first-time   │   global flags
 Docs         │                               │  surfaces)      │   --team, --json,
 GitHub                                       └─────────────────┘    --server-name
                                              │
                                              ├─ DIALOGS (8) ───┐
                                              │ Create Team     │
                                              │ Create Org      │
                                              │ BYOT Identity   │
                                              │ CLI Identity    │
                                              │ Team Agent      │
                                              │ Send Message    │
                                              │ Start Chat      │
                                              │ Settings Help   │
                                              └─────────────────┘
                                                       ▲
                                                       └── /connect (admin tab)
                                                           overlaps public /connect ✱
```
