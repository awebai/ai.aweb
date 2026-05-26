# Long-fruit submission prep — readiness state per task

*Sofia, 2026-05-26. Per Juan's direction: focus on the submissions that
take the longest to bear fruit (Anthropic Claude Code marketplace +
the MCP registries OpenAI users discover from). Start them earliest so
approval cycles run in parallel with shorter-feedback community work.*

This doc captures, for each long-fruit task, what's ready and what's
genuinely blocking submission. Read top-down. Anything marked READY can
go through the standing chain (Iris voice-pass → Sofia framing → Juan
submit). Anything marked BLOCKED has a specific prep item named.

---

## Baseline metadata (reusable across all submissions)

Gathered once from disk + canonical docs. Use these values across every
registry/marketplace where the field applies.

| Field | Value | Source |
|---|---|---|
| Project name | **aweb** | top-level branding |
| One-sentence description | "A coordination platform for AI coding agents — handles team-scoped coordination: mail, chat, tasks, roles, instructions, locks, presence, and MCP tools. Identity and team membership live in awid." | `aweb/README.md` line 1-5 |
| Tighter one-liner (for forms) | "Open-source coordination layer for AI coding agents: identity, persistent task claims, agent-to-agent mail and chat, MCP tools." | derived |
| Homepage | https://aweb.ai | canonical |
| Source repo | https://github.com/awebai/aweb | canonical |
| Identity-registry repo | https://github.com/awebai/awid (or wherever awid source lives) | TBD-confirm with Athena |
| License | MIT (Copyright 2025 Juan Reyero) | `aweb/LICENSE` |
| Author | Juan Reyero / awebai | per plugin.json |
| Keywords | aweb, agents, coordination, identity, mcp, multi-agent, claude-code, claude-coding-agent, codex, pi | mix of plugin.json + adjacency |

### MCP server specifics

| Field | Value | Source |
|---|---|---|
| MCP server endpoint | https://app.aweb.ai/mcp/ | canonical (returns 401 unauthenticated, expected — registries list the URL, don't auth-test) |
| Transport type | Streamable HTTP | verified by curl HTTP/2 response |
| Tool count | 7 | per the welcome guide content |
| Tools | create_invite_link, add_contact_by_handle, contacts_remove, list_contacts, send_message_to_contact, read_messages_from_contact, aweb_welcome_guide | per welcome.md as shipped |
| Custodial/hosted? | Hosted at app.aweb.ai/mcp/; self-hostable via docker compose | per docs/README + self-hosting guide |

---

## B.1 — Submit aweb-channel to Claude Code official marketplace

**Status: READY to draft form-fill content. One prep item before submission.**

### What I verified

- `aweb/channel/.claude-plugin/plugin.json` exists with complete fields:
  - name: `aweb-channel`
  - description: "aweb agent coordination channel — receive mail, chat, tasks, and control signals from your agent team in real time."
  - version: 1.4.8
  - author.name: awebai
  - homepage: https://aweb.ai
  - repository: https://github.com/awebai/aweb
  - license: MIT
  - keywords: aweb, agents, coordination, channel, mcp
- Plugin structure is correct for `anthropics/claude-plugins-official` submission (per their CONTRIBUTING shape).

### Prep item before submission

**There is no `LICENSE` file inside `aweb/channel/`** (only `aweb/LICENSE` at top level). Anthropic's submission docs say "Please see each linked plugin for the relevant LICENSE file" — so the plugin dir should have its own LICENSE for clean review. Engineering task: copy `aweb/LICENSE` → `aweb/channel/LICENSE` (or symlink, depending on aweb conventions). One-line change to surface to Athena before submission.

### Submission form content (draft, Iris voice-pass then submit)

Form at https://clau.de/plugin-directory-submission. Fields expected:

- **Plugin name**: aweb-channel
- **Description**: aweb agent coordination channel — receive mail, chat, tasks, and control signals from your agent team in real time.
- **Plugin repository URL**: https://github.com/awebai/aweb (with plugin at `channel/` subdir; may need to clarify subdir to reviewer)
- **License**: MIT
- **Author**: Juan Reyero (awebai)
- **What it does (longer form)**: aweb-channel is the Claude Code plugin that pushes aweb coordination events into a running Claude Code session in real time. When a teammate agent sends mail, starts a chat, claims a task, or signals control, the channel wakes Claude Code with the event content. Outbound replies and other coordination actions still use the aw CLI; this plugin handles inbound events only. The aweb-channel plugin is one half of the canonical Claude Code install (alongside aweb-skills, submitted separately as B.2).

---

## B.2 — Submit aweb-skills to Claude Code official marketplace

**Status: BLOCKED on plugin.json completion.**

### What I verified

`aweb/packages/claude-skills/.claude-plugin/plugin.json` exists but is **missing required fields**:

```json
{
  "name": "aweb-skills",
  "version": "0.2.8",
  "description": "aweb agent coordination skills — teach your Claude Code agent how to use the aw CLI for mail, chat, tasks, and team coordination."
}
```

Missing: license, homepage, repository, author. The aweb-channel plugin.json has all of these; aweb-skills should mirror that shape before submission to the official directory (Anthropic's review will likely flag the missing metadata).

### Prep items before submission

1. **Engineering** (Athena/owner-of-aweb/packages/claude-skills/): fill in plugin.json with the same shape as aweb-channel. Suggested values:
   - license: "MIT"
   - homepage: "https://aweb.ai"
   - repository: "https://github.com/awebai/aweb"
   - author: { "name": "awebai" }
   - keywords: ["aweb", "agents", "coordination", "skills", "claude-code"]
2. **LICENSE file inside the package dir** (same as B.1).
3. After plugin.json is updated, B.2 becomes READY.

### Submission form content (draft, ready when plugin.json is)

Same shape as B.1, with the substantive distinction noted in support runbook (per Aida's runbook entry): **aweb-channel does NOT bundle the canonical skills; aweb-skills is the separate install that carries the five canonical skills** (aweb-coordination, aweb-messaging, aweb-team-membership, aweb-bootstrap, aweb-identity). Both should be submitted together so customers reading the marketplace see the pair.

---

## B.3 — Submit aweb MCP server to Official MCP Registry

**Status: READY to draft submission. Process is GitHub-PR-based.**

### What I verified

- Registry at https://registry.modelcontextprotocol.io/ backed by Anthropic, GitHub, PulseMCP, Microsoft.
- It's a METAREGISTRY — stores metadata, not code/binaries.
- Submission process lives at https://github.com/modelcontextprotocol/registry (CONTRIBUTING.md, need to read before submission). Likely a YAML/JSON manifest in the repo + PR-based.

### Submission metadata (locked from baseline above)

- Server name: `aweb`
- Description: "Open-source coordination layer for AI coding agents: identity, persistent task claims, agent-to-agent mail and chat, MCP tools."
- Transport: Streamable HTTP
- Endpoint: https://app.aweb.ai/mcp/
- Repo: https://github.com/awebai/aweb
- Homepage: https://aweb.ai
- License: MIT
- Tools (7): create_invite_link, add_contact_by_handle, contacts_remove, list_contacts, send_message_to_contact, read_messages_from_contact, aweb_welcome_guide
- Authentication: OAuth 2.0 (custodial identity provisioning via app.aweb.ai)

### Path

1. Iris reads github.com/modelcontextprotocol/registry CONTRIBUTING.md to confirm the exact manifest format.
2. Iris drafts the manifest entry from the metadata above.
3. Sofia framing-pass on the description copy (one-liner that lands cleanly in a registry display).
4. Juan opens the PR.

---

## B.4 — Submit aweb MCP server to mcp.so

**Status: READY to draft. Self-registration form on mcp.so.**

### Submission content

Same metadata as B.3. mcp.so accepts self-registration; form on the site
itself. Iris fills in the form with the metadata above; Juan submits.
~10 minutes once Iris has the form open.

---

## B.5 — Submit aweb MCP server to smithery.ai

**Status: READY to draft.**

### Submission content

Same metadata as B.3 + B.4. smithery.ai also supports hosting the server
(we don't need that since we self-host at app.aweb.ai). Form-based.

---

## B.6 — Submit aweb MCP server to glama.ai/mcp

**Status: READY to draft. Process TBD on glama.ai.**

### Submission content

Same metadata. Iris should check glama.ai/mcp for whether it's form-based,
PR-based, or auto-discovery via npm/github keywords. If auto-discovery,
B.6 may already be done (if our repo or package has the right tags).

---

## B.7 — PR to punkpeye/awesome-mcp-servers

**Status: READY to draft. Standard GitHub awesome-list PR.**

### Submission content

Awesome-list PRs are usually a single line added to a Markdown file under
the appropriate section. Iris drafts the line:

```markdown
- [aweb](https://github.com/awebai/aweb) — Coordination layer for AI coding agents: identity, persistent task claims, agent-to-agent mail and chat, MCP tools. Open source MIT.
```

Open PR with that one-line addition.

---

## B.8 — Publish aweb-coordination variant skill to ClawHub

**Status: BLOCKED on variant SKILL.md authoring.**

### What I verified

- ClawHub at github.com/openclaw/clawhub.
- Skill format: AgentSkills-compatible SKILL.md with YAML frontmatter (name, description, metadata: env vars, binaries, install specs).
- Publish via CLI: `clawhub skill publish <path>`.
- Canonical aweb-coordination/SKILL.md is at `aweb/skills/aweb-coordination/SKILL.md` and is in the AgentSkills format.

### Why variant, not mirror

Different audience: canonical SKILL.md is for aweb agents who already have
aw CLI access and the team-coordinated context the skill assumes. ClawHub
readers are external developers browsing the registry to decide whether
to install. Need: marketing-flavored frontmatter (why-use-this, what-it-
replaces-or-adds, install-friendliness, license-prominent) and a body
that introduces the team-coordinated context for external readers.

### Prep items before submission

1. **Iris drafts the variant** at a new location. Suggested: `aweb/skills/aweb-coordination-clawhub/SKILL.md` (parallel to canonical; clearly marked as the external-facing variant).
2. **Sofia framing-pass** on the variant copy (external voice, install-friendliness).
3. **Install clawhub CLI** (TBD on whether Juan or someone else does this — depends on whether clawhub CLI lives outside our workflow).
4. **Run `clawhub skill publish <variant-path>`**.

---

## Summary table — what's ready vs what's blocked

| Task | Status | Blocker |
|---|---|---|
| B.1 — Claude Code: aweb-channel | READY-with-caveat | LICENSE file copy into aweb/channel/ |
| B.2 — Claude Code: aweb-skills | BLOCKED | plugin.json missing fields + LICENSE file |
| B.3 — Official MCP Registry | READY | Iris drafts manifest per CONTRIBUTING |
| B.4 — mcp.so | READY | Iris fills form |
| B.5 — smithery.ai | READY | Iris fills form |
| B.6 — glama.ai/mcp | READY-pending-discovery | Iris confirms submission process |
| B.7 — punkpeye/awesome-mcp-servers | READY | Iris drafts one-line PR addition |
| B.8 — ClawHub | BLOCKED | Iris drafts variant SKILL.md |

---

## Recommended path

1. **Engineering prep** (parallel to drafting): Athena or whoever owns
   `aweb/channel/` and `aweb/packages/claude-skills/` adds:
   - LICENSE file in `aweb/channel/`
   - LICENSE file in `aweb/packages/claude-skills/`
   - Complete plugin.json fields in `aweb/packages/claude-skills/.claude-plugin/plugin.json`
   This unblocks B.1 + B.2.

2. **Drafting** (Iris, in step 3 cadence or before):
   - B.3 manifest entry (MCP registry)
   - B.4, B.5, B.6 form-fill content (same metadata, slight variant per registry)
   - B.7 one-line PR addition
   - B.8 variant SKILL.md
   
   These can be done in one cycle (~3-4 hours of drafting once Iris is on it).

3. **Framing-pass** (Sofia): one pass over all the drafts. Probably 30 min
   total since the substance is the same metadata, just rendered for
   different registry surfaces.

4. **Submission** (Juan): six submissions (B.3-B.7 + B.8 publish CLI) + two
   Claude Code marketplace forms (B.1, B.2 once unblocked). Estimated
   30-60 min total of submission clicking/PR-opening.

Approval cycles are days to weeks. Starting all eight in the same week
gets all approvals landing in the same window, which is when distribution
visibility lands together rather than dribble.

---

## What this doc is and isn't

This is a **prep state snapshot**, not a long-lived spec. Once the
submissions are made, this doc gets archived (move to
`agents/sofia/archive/2026-05-26-long-fruit-submission-prep.md`) and
the actual submissions live as attempts.jsonl rows + epic subtasks
(B.1-B.8) in `aw task`.

The operational spec for the broader push lives at
`agents/sofia/outreach-playbook-v0.md`.

The learning log lives at `publishing/attempts.jsonl` (schema in
`publishing/attempts-README.md`).

This doc bridges them for the specific long-fruit submission cluster.
