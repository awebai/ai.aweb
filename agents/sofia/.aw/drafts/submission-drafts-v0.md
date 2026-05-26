# Long-Fruit Submission Drafts — v0

Operational reference for executing the long-fruit submission cluster
(B.1–B.8 on aw epic `default-aaai`). Each section is the script Juan
runs at submission time: where to go, what to put in each field, what
to check after.

Voice-pass owner: Iris. Engineering prep: Athena. Submitter: Juan.
Sofia: framing + draft + tracking.

State of engineering prep as of 2026-05-26:

- `aweb/channel/LICENSE` — DONE (Athena commit `f32393a`)
- `aweb/packages/claude-skills/LICENSE` — DONE (`f32393a`)
- `aweb/packages/claude-skills/.claude-plugin/plugin.json` metadata
  filled — DONE (`f32393a`), now on plugin version `0.2.9` (post
  Hestia/Dave release rebase)
- `aweb/channel/package.json` carrying `mcpName: "io.github.awebai/channel"`
  — DONE (Athena commit `db9a492`, `@awebai/claude-channel 1.4.9`)
- `@awebai/claude-channel@1.4.9` published on npm — **PENDING**
  (Hestia's release gate; required before B.3 can validate)

Baseline metadata used across submissions (single source so framing
stays consistent):

| Field | Value |
|---|---|
| Project name | aweb |
| Tagline | Real-time agent-team coordination for AI coding agents |
| Description (long) | aweb gives AI coding agents cryptographic identities and a coordination channel: mail, chat, tasks, locks, and presence between agents on the same team. Self-hostable open-source server (MIT); hosted cloud at app.aweb.ai for teams that want managed identity + multi-tenant isolation. |
| Repository | https://github.com/awebai/aweb |
| Homepage | https://aweb.ai |
| License | MIT |
| Author | awebai |
| Keywords | aweb, agents, coordination, channel, mcp, claude-code, multi-agent |
| npm packages | `@awebai/claude-channel` (1.4.9), `@awebai/claude-skills` (0.2.9) |

---

## B.1 — Claude Code Official Plugin Marketplace: `aweb-channel`

**Status:** READY. Engineering prep complete (LICENSE + plugin.json
verified on `f32393a`).

**Where:** https://clau.de/plugin-directory-submission
(canonical entry; Anthropic Google Form per the README of
anthropics/claude-plugins-official).

**Submission fields:**

- Plugin name: `aweb-channel`
- Plugin description: `aweb agent coordination channel: receive mail,
  chat, tasks, and control signals from your agent team in real time.`
  (matches `plugin.json` description verbatim; do not paraphrase;
  Anthropic reviewers cross-check). **Note:** `plugin.json` currently
  carries an em-dash in this field; Athena round-trip needed to swap
  to a colon before submission so the verbatim-match holds.
- Repository URL: https://github.com/awebai/aweb
- Path to plugin in repo: `/channel/.claude-plugin/`
- License: MIT
- Author/Org: awebai
- Contact email: juan@thestarmaps.com (or whichever Juan prefers
  reviewers route questions to)

**What this plugin does (long-form, for any free-text "describe your
plugin" field):**

> aweb-channel is a Claude Code plugin that delivers real-time
> coordination events from other AI agents on your team: mail, chat
> messages, task updates, and control signals (pause/resume/interrupt).
> It pairs with the `aw` CLI for the action surface: send messages,
> claim tasks, manage shared roles and instructions, take locks on
> contested resources. When you run multiple Claude Code agents on the
> same codebase (or across machines), aweb-channel keeps them seeing
> each other's work instead of duplicating it. Identity is
> cryptographic (Ed25519 / did:aw), so messages and task claims are
> signed and verifiable. Self-hostable open-source server; managed
> hosting at app.aweb.ai.

**Verification after submission:**
- Watch for review email at Juan's address.
- Anthropic's process is curated/manual; expect days–weeks not
  minutes.

**Append attempts.jsonl row** with `channel: "claude-code-marketplace"`
(submission-surface variant; `result_submission` shape) at submission
time.

---

## B.2 — Claude Code Official Plugin Marketplace: `aweb-skills`

**Status:** READY. Engineering prep complete on plugin version `0.2.9`.

**Where:** Same surface as B.1 — https://clau.de/plugin-directory-submission

**Submission fields:**

- Plugin name: `aweb-skills`
- Plugin description: `aweb agent coordination skills: teach your
  Claude Code agent how to use the aw CLI for mail, chat, tasks, and
  team coordination.` **Note:** `plugin.json` currently carries an
  em-dash in this field; Athena round-trip needed to swap to a colon
  before submission so the verbatim-match holds.
- Repository URL: https://github.com/awebai/aweb
- Path to plugin in repo: `/packages/claude-skills/.claude-plugin/`
- License: MIT
- Author/Org: awebai
- Contact email: juan@thestarmaps.com

**What this plugin does:**

> aweb-skills is a Claude Code plugin packaging five
> AgentSkills-format skill bundles: `aweb-coordination` (work
> discovery, task claims, locks, presence), `aweb-messaging` (mail and
> chat response policy), `aweb-team-membership` (identity, team
> certificates, multi-team membership), `aweb-bootstrap` (creating new
> aweb teams from templates), and `aweb-identity` (key custody and
> verifiable identity). Together they teach a Claude Code agent the
> judgment calls behind the `aw` CLI surface: when to inspect shared
> state, when to claim work, when to take a lock, how to read the
> team's operating rules. Complements aweb-channel.

**Verification:** Same as B.1.

**Append attempts.jsonl row** with `channel:
"claude-code-marketplace"` at submission time. Submit B.1 and B.2 on
the same day; they share approval flow.

---

## B.3 — Official MCP Registry (registry.modelcontextprotocol.io)

**Status:** WAITING on Hestia npm publish of `@awebai/claude-channel@1.4.9`.
Once that lands, READY.

**Why this one matters:** Anthropic + GitHub + PulseMCP + Microsoft
backed; it's the registry MCP clients (including Claude Code's
built-in MCP support, Cursor, Continue, Cline) check first when users
browse for MCP servers. Listing here gets aweb in front of every MCP
client user, not just Claude Code plugin users.

**Where:** The CLI `mcp-publisher`, published to
registry.modelcontextprotocol.io.

**Step-by-step:**

1. **Verify npm publish landed:** `npm view @awebai/claude-channel
   version` returns `1.4.9`. If not, ping Hestia.

2. **Install mcp-publisher CLI** (one-time):
   ```bash
   brew install mcp-publisher
   # or: curl -L "https://github.com/modelcontextprotocol/registry/releases/latest/download/mcp-publisher_$(uname -s | tr '[:upper:]' '[:lower:]')_$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/').tar.gz" | tar xz mcp-publisher && sudo mv mcp-publisher /usr/local/bin/
   mcp-publisher --help
   ```

3. **Create `server.json`** in `aweb/channel/`:
   ```bash
   cd ~/prj/awebai/aweb/channel
   mcp-publisher init
   ```
   Edit the generated `server.json` to read exactly:
   ```json
   {
     "$schema": "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json",
     "name": "io.github.awebai/channel",
     "title": "aweb channel",
     "description": "Real-time agent-team coordination events for Claude Code and any MCP client. Receive mail, chat, tasks, and control signals from teammates. Pairs with the aw CLI for the action surface.",
     "repository": {
       "url": "https://github.com/awebai/aweb",
       "source": "github"
     },
     "version": "1.4.9",
     "packages": [
       {
         "registryType": "npm",
         "identifier": "@awebai/claude-channel",
         "version": "1.4.9",
         "transport": {
           "type": "stdio"
         }
       }
     ]
   }
   ```

4. **Authenticate** (one-time per machine):
   ```bash
   mcp-publisher login github
   ```
   Visit the printed URL, enter the device code, authorize. Juan must
   log in as a GitHub user who is a member of the `awebai` org —
   that's what authorizes publishing under `io.github.awebai/`.

5. **Publish:**
   ```bash
   mcp-publisher publish
   ```
   Expected output: `✓ Successfully published / ✓ Server
   io.github.awebai/channel version 1.4.9`.

6. **Verify** via the registry API:
   ```bash
   curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.awebai/channel"
   ```

**Failure modes:**
- `"You do not have permission to publish this server"` — GitHub auth
  doesn't grant the `io.github.awebai/` namespace because the logged-in
  user isn't recognized as an awebai org member. Fallback: switch to
  DNS auth using `aweb.ai/channel` as the name (requires a DNS TXT
  record on aweb.ai). See
  https://modelcontextprotocol.io/registry/authentication#dns-authentication.
- `"Registry validation failed for package"` — `mcpName` in published
  npm package.json doesn't match. Verify with `npm view
  @awebai/claude-channel | grep mcpName`.

**Append attempts.jsonl row** with `channel: "mcp-registry-official"`.

---

## B.4 — mcp.so

**Status:** Submission process needs live investigation. mcp.so/submit
returned 403; can't pre-verify the form.

**Where:** Best guess: https://mcp.so/submit or "Add Server" button on
homepage. Visit homepage when ready and walk the actual submission
flow.

**Fields most third-party MCP directories ask for** (use baseline
table above):
- Server name: `aweb`
- npm package: `@awebai/claude-channel`
- Repository: https://github.com/awebai/aweb
- Description (one-line): Real-time agent-team coordination for AI
  coding agents: mail, chat, tasks, presence across teammates.
- Categories: Communication, Coordination, Developer Tools,
  Multi-Agent (pick whichever subset the form offers)
- License: MIT
- Transport: stdio

**Submit ONLY after B.3 lands** — mcp.so often mirrors from the
official registry, so an official-registry presence increases
discoverability and reduces duplicate-submission risk.

**Append attempts.jsonl row** with `channel: "mcp-so"`.

---

## B.5 — smithery.ai

**Status:** SHAPE MISMATCH. Smithery's publish flow assumes a
URL-hosted MCP server (streamable-http transport) OR a `.mcpb` bundle
upload. aweb-channel is stdio-only; doesn't match either shape today.

**Options:**
1. **Skip** until aweb publishes a hosted streamable-http MCP endpoint
   (no plan today; would need ac-side work). Cost: smithery
   discoverability foregone.
2. **Build .mcpb bundle**: wrap the npm package as an .mcpb
   container. Engineering scope: small (Athena would know). Cost: one
   small engineering item.
3. **Investigate URL-mode submission** at https://smithery.ai/new:
   maybe smithery accepts npm-package metadata even if their docs
   emphasize hosted. Cost: 10 min of exploration at submission time.
4. **Ask Smithery directly**: if option 3 confirms shape-mismatch,
   mail their team (link or contact channel on smithery.ai) to confirm
   stdio is unsupported before committing to .mcpb engineering. Cost:
   one mail.

**Recommendation:** Try option 3 first (cheap), then option 4 (also
cheap) if option 3 inconclusive, fall back to option 2 only if both
upstream conversations confirm shape-mismatch, accept option 1 only
if Juan deprioritizes smithery.

**Append attempts.jsonl row** with `channel: "smithery-ai"` —
including the option-3 exploration as a row even if the submission
itself fails (the exploration outcome is the signal worth logging).

---

## B.6 — glama.ai/mcp

**Status:** Submission process needs live investigation. Form is
behind the "Add Server" button on glama.ai/mcp; not pre-discoverable
via fetch.

**Where:** https://glama.ai/mcp → click "Add Server" button.

**Fields:** Same baseline as B.4. Glama's listings carry a badge image
the directory generates after listing (visible in awesome-mcp-servers
entries like `[![org/repo MCP server](https://glama.ai/mcp/servers/org/repo/badges/score.svg)]`).

**Submit AFTER B.3** for same discoverability-mirror reason as B.4.

**Append attempts.jsonl row** with `channel: "glama-ai"`.

---

## B.7 — `punkpeye/awesome-mcp-servers` PR

**Status:** READY. PR-only; no dependency on B.3.

**Where:** Fork https://github.com/punkpeye/awesome-mcp-servers,
create branch `add-aweb`, edit `README.md`, open PR. Maintainer
expedites PRs titled with `🤖🤖🤖` for automated agents (per
CONTRIBUTING.md), but Juan is submitting personally so skip that.

**Category:** `### 💬 Communication`. (Precedent in this category:
`bababoi-bibilabu/agent-mq` — "Message queue for AI coding assistants.
Let AI agents (Claude Code, Cursor, Codex) send messages to each other
across sessions and machines.") Direct match for aweb's positioning.

**Line to add** (alphabetical between `arpitbatra123/mcp-googletasks`
and `bababoi-bibilabu/agent-mq`):

```
- [awebai/aweb](https://github.com/awebai/aweb) 📇 ☁️ 🏠 🍎 🪟 🐧 - Real-time agent-team coordination: receive mail, chat, tasks, and control signals from teammates. Pairs with the aw CLI for the action surface (send messages, claim tasks, manage workspaces). Self-hostable open-source server, MIT.
```

Legend used (from the README's Legend section):
- 📇 — TypeScript
- ☁️ — cloud service (the hosted backend at app.aweb.ai)
- 🏠 — local/self-hosted option
- 🍎 🪟 🐧 — macOS, Windows, Linux

**PR title:** `Add awebai/aweb to Communication`

**PR description:**

> Adds `awebai/aweb` to the Communication category: an MCP server
> that delivers real-time agent-team coordination events (mail, chat,
> tasks, control signals) to AI coding agents. Pairs with the `aw`
> CLI for the action surface. Self-hostable (MIT) with optional
> managed hosting at app.aweb.ai. Cryptographic identity (Ed25519
> did:aw) so messages and task claims are signed and verifiable.
>
> Repository: https://github.com/awebai/aweb
> Homepage: https://aweb.ai

**Verification:** Watch for merge or maintainer comment. Typical
turnaround on this repo is days; volume is high (1.8k PRs in
backlog).

**Append attempts.jsonl row** with `channel: "awesome-mcp-pr"`.

---

## B.8 — ClawHub variant `SKILL.md`

**Status:** READY. Drafted below.

**Where:** https://github.com/openclaw/clawhub. CLI is `clawhub skill
publish <path>`. Format is AgentSkills-compatible SKILL.md with YAML
frontmatter (name, description, allowed-tools, metadata).

**Discipline (per Iris voice-pass discussion):** ClawHub readers are
external developers browsing the registry; they don't have the
team-coordinated context the canonical `aweb/skills/aweb-coordination/SKILL.md`
assumes. The variant introduces that context. Canonical stays
load-bearing for aweb agent operation; variant is marketing-shaped
for discoverability.

**Suggested file location:** `aweb/skills/aweb-coordination-clawhub/SKILL.md`
(public aweb skills tree — Iris-recommended since the skill is
open-source-shape).

**Submission flow:**
1. Land the variant SKILL.md file in aweb repo first (gives it a
   stable URL for the ClawHub listing).
2. `clawhub skill publish aweb/skills/aweb-coordination-clawhub/`
3. Verify it appears in the ClawHub registry search.

**Drafted SKILL.md content:**

```markdown
---
name: aweb-coordination
description: Coordinate multiple Claude Code (or any MCP-aware) agents working on the same codebase or across machines. Avoid duplicate work, claim tasks, message teammates, take locks on contested resources, and read shared team operating rules. Replaces ad-hoc "ping me on Slack" with signed, durable, in-band coordination.
allowed-tools: "Bash(aw *)"
metadata:
  homepage: https://aweb.ai
  repository: https://github.com/awebai/aweb
  license: MIT
  requires:
    - aw CLI (npm install -g @awebai/cli, or via aweb-channel plugin)
    - aweb team membership (free self-host or hosted at app.aweb.ai)
---

# aweb Coordination

## What this gives you

When you run multiple Claude Code agents on the same codebase (or
across machines, or for different roles on the same project), they
duplicate work, step on each other's edits, and can't see what the
others are doing. aweb fixes that with five primitives:

- **Tasks**: durable, shared work items every agent on the team can
  see, claim, and update.
- **Mail and chat**: signed messages between agents, durable for
  mail (async handoffs) and waiting for chat (sync questions).
- **Locks**: explicit holds on contested resources (a file, a branch,
  a deploy slot).
- **Presence**: who's online, what they're working on, who's blocked.
- **Roles and instructions**: versioned team-wide operating rules
  every agent reads on wake-up.

Every action is signed by the agent's cryptographic identity (Ed25519
`did:aw`), so claims and messages are verifiable.

## What it replaces

- Manually pasting "I'm working on X, please don't touch" into a
  shared Slack channel.
- "Maybe Alice has the auth refactor; I'll ask in stand-up."
- Two agents pushing conflicting changes because neither saw the other.
- Hand-coordinating who reviews what when one agent finishes a draft.

## Installation

```bash
# Install the aw CLI (provides this skill's tool surface)
npm install -g @awebai/cli

# Bootstrap into a team (or join an existing one — see aweb-team-membership)
aw init
```

For Claude Code users, install the companion plugin for real-time
event delivery:

```bash
# In Claude Code:
/plugin install aweb-channel
```

## Start-of-session loop

Run these before claiming new work. Order is deliberate:

```bash
aw workspace status   # who is online, active team, identity, claims, locks
aw mail inbox         # async handoffs, reviews, blockers — process first
aw chat pending       # someone may be blocked waiting on you
aw work ready         # only after the above; pick the smallest actionable item
```

## Seeing what teammates are doing

```bash
aw work active        # tasks currently claimed across the team
aw work ready         # unclaimed tasks worth picking up
aw work blocked       # tasks paused on a dependency
aw task show <id>     # full task including comments and history
```

## Contacting teammates

```bash
aw mail send --to <alias> --body "..."       # durable, async
aw chat send-and-wait <alias> "..."          # sync, blocks until reply
aw chat send-and-leave <alias> "..."         # fire and forget
```

## Worktrees for parallel work

When you need to work on an isolated branch without colliding with
the main workspace:

```bash
aw workspace add-worktree --task <task-id>
```

Creates a sibling git worktree wired up as its own coordination
workspace.

## Full depth

This is the registry-listing summary. For decision policy depth
(when to take a lock vs claim a task, how to read team operating
rules, multi-team membership, identity custody, hosted vs
self-host trade-offs), load the canonical skill at
https://github.com/awebai/aweb/tree/main/skills.

## License

MIT. Self-hostable; hosted option at https://app.aweb.ai.
```

**Append attempts.jsonl row** with `channel: "clawhub"`.

---

## NanoClaw note (epic subtask separate from B.1–B.8)

The NanoClaw `/add-aweb` skill (github.com/nanocoai/nanoclaw,
`channels` branch) is a separate epic subtask, not in B.1–B.8. Lower
discoverability, different format. Defer until the higher-leverage
items here land or a NanoClaw user signals demand.

---

## Execution order recommendation

Day 1 (when Hestia confirms `@awebai/claude-channel@1.4.9` is npm-live):
- B.3 (official MCP registry) — primary
- B.1 + B.2 (Claude Code marketplace) — same form, batch them
- B.7 (awesome-mcp-servers PR) — independent, fast

Day 2 (after B.3 is publicly visible):
- B.4 (mcp.so) — likely auto-mirrors from official
- B.6 (glama.ai/mcp) — same
- B.5 (smithery.ai) — exploration-mode

Day 3+:
- B.8 (ClawHub) — requires the variant SKILL.md to be merged into
  aweb repo first

Each submission produces one `attempts.jsonl` row at submission time
(submission-surface variant per the schema-PR Iris landed). Follow-ups
at 7d and 30d capture approval status + discoverability per the schema.

---

## Open questions for Juan / Hestia / Iris

- **Hestia:** When can `@awebai/claude-channel@1.4.9` be npm-published?
  That's the gate for B.3.
- **Juan:** GitHub account to use for `mcp-publisher login github`?
  Needs to be an awebai org member. If your personal account isn't,
  decide whether to add it or fall back to DNS auth.
- **Iris:** Voice-pass on the long-form descriptions in B.1, B.2,
  B.3, and B.7 PR description before Juan submits. ClawHub variant
  body (B.8) is the longest copy and the one most worth careful
  voice-pass.
