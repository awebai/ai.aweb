# OpenClaw × aweb integration research

Date: 2026-06-07
Owner: Sofia

## User goal

Make it as easy as possible for OpenClaw systems to use aweb.

## Sources checked

- `https://docs.openclaw.ai/llms.txt`
- OpenClaw docs pages fetched as Markdown:
  - `/plugins/bundles.md`
  - `/tools/plugin.md`
  - `/cli/plugins.md`
  - `/cli/skills.md`
  - `/tools/skills.md`
  - `/clawhub.md`
  - `/clawhub/how-it-works.md`
  - `/clawhub/publishing.md`
  - `/clawhub/skill-format.md`
  - `/plugins/building-plugins.md`
  - `/plugins/manifest.md`
  - `/cli/mcp.md`
  - `/gateway/cli-backends.md`
  - `/concepts/agent-workspace.md`
- `github.com/openclaw/openclaw` shallow clone for examples.
- Current aweb artifacts:
  - `@awebai/aw` latest npm version: 1.26.9
  - `@awebai/claude-skills` latest npm version: 0.2.12
  - `@awebai/claude-channel` latest npm version: 1.4.12
  - `awebai/claude-plugins` pushed artifact commit: `d6034672ded5ef5dbb38fc84fcb0a1de883b9544`
- Old beadhub-era `co.aweb/outreach/source-material/beadhub-era/aweb-a2a-interop.md` for inspiration. It is A2A/aweb edge-bridge thinking, not a current OpenClaw integration artifact.

## What OpenClaw is

OpenClaw is a self-hosted gateway for AI agents across chat channels (Discord,
Google Chat, iMessage, Matrix, Teams, Signal, Slack, Telegram, WhatsApp, Zalo,
etc.). It has:

- one Gateway process;
- per-agent workspaces under `~/.openclaw/workspace` by default;
- skills loaded from workspace/global/bundled locations;
- native plugins (`openclaw.plugin.json` + runtime module);
- compatible bundles from Claude/Codex/Cursor plugin ecosystems;
- ClawHub as the registry for skills and plugins.

## OpenClaw plugin/bundle facts that matter

### OpenClaw can install Claude-compatible bundles

OpenClaw recognizes Claude plugin layouts:

- manifest-based: `.claude-plugin/plugin.json`
- manifestless: default Claude layout (`skills/`, `commands/`, `.mcp.json`, etc.)

Supported mappings today:

- `skills/` load as normal OpenClaw skills;
- Claude `commands/` are treated as skill roots;
- `.mcp.json` can expose supported stdio/HTTP MCP tools to embedded OpenClaw agent turns;
- `.lsp.json` and manifest-declared `lspServers` load into embedded LSP defaults;
- Claude `agents`, `hooks.json`, and output styles are detected but not executed.

Security boundary: bundles do not load arbitrary runtime modules in-process, but
supported stdio MCP servers may be launched as subprocesses.

### OpenClaw remote marketplace rule is important

OpenClaw supports Claude marketplace installs:

```bash
openclaw plugins install <plugin-name>@<marketplace-name>
openclaw plugins install <plugin-name> --marketplace <owner/repo>
```

But for **remote marketplaces loaded from GitHub or git**, OpenClaw accepts only
relative plugin sources inside the cloned marketplace repo. It rejects HTTP(S),
absolute-path, git/GitHub, and other non-path plugin sources from remote
manifests.

Current `awebai/claude-plugins` `marketplace.json` still points entries at npm
sources. That is fine for Claude Code, but it means this likely does **not** work
as an OpenClaw remote marketplace install path yet:

```bash
openclaw plugins install aweb-skills --marketplace awebai/claude-plugins
```

because the remote manifest entries are npm-source entries.

The repo now contains vendored self-contained plugin dirs under `plugins/`, so
we can make it OpenClaw-friendly by switching the marketplace entries to relative
sources or by adding a separate OpenClaw-compatible marketplace/catalog.

### OpenClaw can install npm plugins/bundles directly

OpenClaw supports:

```bash
openclaw plugins install npm:<package>
openclaw plugins install npm:<package>@<exact-version>
```

A Claude-compatible npm package containing `.claude-plugin/plugin.json` and
`skills/` should be detected as a bundle. Therefore the immediate likely install
path for aweb skills is:

```bash
openclaw plugins install npm:@awebai/claude-skills@0.2.12 --pin
openclaw gateway restart
openclaw plugins inspect aweb-skills
```

This should expose the five aweb skills in OpenClaw. It should be tested in a
fresh OpenClaw install before publishing instructions.

### OpenClaw skills should declare OpenClaw metadata

OpenClaw follows the AgentSkills spec. It accepts skill frontmatter with `name`
and `description`. For OpenClaw-specific runtime gating, docs recommend a
single-line JSON `metadata.openclaw` object. Useful fields:

- `requires.bins`: required binaries on PATH;
- `install`: dependency installer hints (`brew`, `node`, `go`, `uv`, `download`);
- `homepage`;
- `always`, `emoji`, etc.

For aweb skills, the obvious metadata is:

```yaml
metadata: {"openclaw":{"requires":{"bins":["aw"]},"install":[{"kind":"node","package":"@awebai/aw","bins":["aw"],"label":"Install aw CLI"}],"homepage":"https://aweb.ai"}}
```

This should be added to the canonical aweb skills before ClawHub publication, if
Claude Code validation tolerates the metadata (likely, but test it).

### ClawHub paths

ClawHub hosts:

- skills: versioned text bundles centered on `SKILL.md`;
- code plugins: OpenClaw-native packages with compatibility metadata;
- bundle plugins: packaged plugin bundles for OpenClaw distribution.

Commands:

```bash
openclaw skills search "..."
openclaw skills install <slug>
openclaw plugins search "..."
openclaw plugins install clawhub:<package>

clawhub skill publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0
clawhub package publish <source> --family code-plugin --dry-run
clawhub package publish <source> --family code-plugin
```

Docs mention `bundle-plugin` in search results but publishing examples only show
`--family code-plugin`; verify the exact ClawHub CLI syntax before publishing a
bundle package.

Skills published on ClawHub are MIT-0 by policy. Since aweb owns its skill text,
we can likely dual-publish/relicense, but this should be an explicit decision.

## aweb-specific integration facts

### Do not recommend `aweb-channel` as the OpenClaw path

`@awebai/claude-channel` is a Claude Code channel adapter. It is inbound-only for
Claude Code and uses Claude-specific channel notifications. OpenClaw already has
its own channel/gateway model.

OpenClaw may detect the bundle `.mcp.json`, but that does not mean it is the
right integration. For OpenClaw, the useful near-term artifact is
`@awebai/claude-skills`, not `@awebai/claude-channel`.

### aweb MCP is not a simple static OpenClaw MCP config today

`aw mcp-config` currently refuses to emit HTTP MCP config because `/mcp` requires
per-request DIDKey signatures plus a team certificate. It points users to the
channel config instead:

```text
HTTP MCP config is not emitted by this command because /mcp now requires per-request DIDKey signatures plus a team certificate; use `aw mcp-config --channel`
```

`aw mcp-config --channel` emits a Claude-channel stdio config, not a generic
OpenClaw tool bridge.

So for OpenClaw, do not currently frame aweb as “just add this MCP server” unless
we first build a local stdio MCP wrapper that signs requests dynamically or a
native OpenClaw plugin that wraps the `aw` CLI.

## Wakeup / polling is load-bearing

The old `claweb` skill's cron section was directionally right. OpenClaw has no
aweb-native push receiver today. Unless we build a native OpenClaw plugin or an
external webhook bridge, an OpenClaw agent will not automatically wake when aweb
mail/chat arrives. The practical near-term wake path is OpenClaw cron or
heartbeat.

OpenClaw cron facts checked from current docs:

- Cron runs inside the Gateway and persists jobs in SQLite.
- It supports `--every`, `--cron`, and `--at` schedules.
- Main-session jobs use `--session main`, enqueue a system event, and can wake
  immediately with `--wake now` or next heartbeat with `--wake next-heartbeat`.
- Isolated jobs use a fresh `cron:<jobId>` session and are better for reports or
  background chores, not for maintaining one aweb inbox/chat handling context.
- Heartbeat is another periodic main-session turn, default roughly every 30 min;
  it can include a checklist in `HEARTBEAT.md`, but it is less precise and too
  slow for chat unless users tune it.
- Webhooks can wake or run isolated agent turns, but aweb does not currently emit
  OpenClaw webhook callbacks, so that is future bridge work.

Therefore the OpenClaw skill/package must include a current cron setup section.
Suggested shape:

```bash
openclaw cron add \
  --name "aweb inbox poller" \
  --every 30s \
  --session main \
  --wake now \
  --system-event "aweb poll: Check for new aweb mail and chat. Run 'aw mail inbox --unread-only' and 'aw chat pending'. If there is anything new, read it and respond using the aweb-messaging policy. Reply in existing conversations; do not start duplicates. If no new items, output NO_REPLY."
```

Open questions to test in a live OpenClaw install:

- Is `30s` accepted for `--every`, or should docs recommend `1m` to avoid
  excessive Gateway/model churn?
- Does a main-session cron event that outputs `NO_REPLY` remain silent as docs
  imply for cron silent-token suppression?
- Does the agent have enough permission to create cron jobs itself, or should the
  skill tell the human/operator to run the command? Docs say creating/mutating
  cron requires `operator.admin`.
- Should the canonical prompt say `aw mail inbox` only, because current `aw mail
  inbox --unread-only` may differ across versions? Verify against `aw mail --help`.

## Recommended integration ladder

### Level 0 — Immediate doc path (fastest)

Goal: OpenClaw agent can use aweb via `aw` CLI and aweb skills.

Proposed user flow to test:

```bash
npm install -g @awebai/aw@latest
cd ~/.openclaw/workspace
aw init   # or invite/API-key/BYOT/current team flow as applicable
openclaw plugins install npm:@awebai/claude-skills@0.2.12 --pin
openclaw gateway restart
openclaw plugins inspect aweb-skills
openclaw skills check
```

Then ask the OpenClaw agent to coordinate through aweb. The skills teach when to
use `aw workspace status`, `aw mail`, `aw chat`, `aw task`, `aw lock`, etc.

Open questions to test:

- Does `openclaw plugins install npm:@awebai/claude-skills@0.2.12 --pin` detect
  the package as a Claude bundle from npm?
- What is the installed plugin id (`aweb-skills` vs package-derived id)?
- Do all five skills show in `openclaw skills check`?
- Does OpenClaw’s skill frontmatter parser tolerate the current `allowed-tools`
  key from Claude skills? Expected yes; verify.

### Level 1 — Make our Claude marketplace OpenClaw-installable

Current obstacle: `awebai/claude-plugins` remote marketplace entries point to npm
sources. OpenClaw remote marketplace rules require relative sources inside the
marketplace repo.

Options:

1. Change `awebai/claude-plugins/.claude-plugin/marketplace.json` to use:

```json
"source": "./plugins/aweb-skills"
"source": "./plugins/aweb-channel"
```

This should be compatible with Claude marketplace semantics and OpenClaw remote
marketplace semantics, but it changes the source shape for existing Claude Code
users. Coordinate with Hestia/Athena before changing.

2. Keep current Claude npm-source marketplace and create a separate OpenClaw
compatible marketplace/catalog that points at the vendored relative dirs.

If we want OpenClaw users to run one command like:

```bash
openclaw plugins install aweb-skills --marketplace awebai/claude-plugins
```

then option 1 or 2 is required.

### Level 2 — Publish a ClawHub bundle plugin

Publish a ClawHub package for the aweb skills bundle, so the install becomes:

```bash
openclaw plugins install clawhub:@awebai/aweb-skills
```

or whatever package naming ClawHub requires for the awebai owner.

Before publishing:

- add OpenClaw metadata to skill frontmatter (`requires.bins: ["aw"]`, node install hint for `@awebai/aw`);
- verify ClawHub package family for compatible bundles (`bundle-plugin` vs documented `code-plugin` examples);
- dry-run publish with `clawhub package publish <source> --dry-run`;
- ensure ClawHub package scope matches the owner handle.

### Level 3 — Publish individual ClawHub skills

Publish each aweb skill as an OpenClaw skill:

- `aweb-bootstrap`
- `aweb-coordination`
- `aweb-identity`
- `aweb-messaging`
- `aweb-team-membership`

Pros:

- native `openclaw skills search/install` UX;
- scan metadata can show `aw` dependency clearly;
- users can install only the playbook they need.

Cons:

- more versioning/publishing overhead;
- ClawHub skill license is MIT-0; confirm we are fine with that;
- cross-skill references should be checked so installing one skill does not
  create broken assumptions.

### Level 4 — Native OpenClaw plugin (best UX)

Build `@awebai/openclaw-aweb` as a native OpenClaw plugin.

Possible capabilities:

- ship the five aweb skills via `skills: ["./skills"]` in `openclaw.plugin.json`;
- expose optional tools wrapping `aw` CLI in the active `ctx.agentDir` / configured workspace:
  - `aweb_whoami`
  - `aweb_workspace_status`
  - `aweb_mail_send`, `aweb_mail_check`
  - `aweb_chat_send`, `aweb_chat_pending`
  - `aweb_task_list`, `aweb_task_create`, `aweb_task_update`
  - `aweb_lock_acquire`, `aweb_lock_release`
- register a CLI command such as `openclaw aweb doctor` or `openclaw aweb setup`;
- config schema with `awPath`, `workspaceDir`, optional `defaultTeamSource`;
- setup checks: `aw` on PATH, `.aw/workspace.yaml` exists in active workspace,
  `aw workspace status` succeeds.

This avoids relying on generic Bash/system-run ability and makes aweb actions
visible as typed OpenClaw tools. It is more work, but it is likely the most
OpenClaw-native experience.

## Recommended next actions

1. **Test Level 0 in a clean OpenClaw workspace**: install `@awebai/aw`, run
   `aw init`, install `npm:@awebai/claude-skills@0.2.12 --pin`, inspect skills.
2. **Patch canonical aweb skills with OpenClaw metadata** and validate both
   Claude Code and OpenClaw parsers.
3. **Decide marketplace source strategy** for `awebai/claude-plugins`:
   switch to relative paths or create a separate OpenClaw-compatible marketplace.
4. **Prepare a ClawHub package** for aweb skills once the local OpenClaw bundle
   install is proven.
5. **Defer native plugin** until we see demand or Level 0/1 friction. If we do
   build it, start as skills + setup/doctor before adding mutating tools.

## Framing guidance

Do not say “OpenClaw can use aweb through the aweb-channel plugin.” That plugin
is Claude Code-specific. Say:

- OpenClaw agents can use aweb today by installing the `aw` CLI in the agent
  workspace and loading the aweb skills bundle.
- A ClawHub/OpenClaw-native package is the next distribution improvement.
- A native OpenClaw plugin could make aweb a typed tool surface later.

Keep messaging boundary accurate:

- current default CLI mail/chat is server-readable plaintext;
- explicit `--e2ee` is local-client E2EE when keys/capability are present;
- hosted/server-side paths are not E2E.
