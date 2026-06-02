# Hestia Handoff

Last updated: **2026-06-02 13:30 CEST (11:30 UTC)** — clean
restart-ready snapshot after the May 26–June 2 release wave.

## Read first

1. `AGENTS.md` (= CLAUDE.md via symlink) — operating discipline.
   Recently added: "Analytics & probe scripts" section under "The Ops
   Runbook." Future-you reading this should know `scripts/` exists.
2. `scripts/README.md` — the four reusable read-only DB scripts for
   recurring questions from Bertha + Juan + triage flows. Don't
   write one-off `/tmp/probe.py` files; extend a script and update
   the table in AGENTS.md when a new shape repeats.
3. This file.
4. `../../status/operations.md` if you need the long roll-up.

## Live matrix (as of 2026-06-02 11:30 UTC)

- **AC**: app.aweb.ai/health → `release_tag=v0.5.58 git_sha=340122ef
  aweb_version=1.26.1 awid_service_version=0.5.9`. **In-flight**:
  v0.5.59 image is in GHCR (run 26767320236 success). Awaiting
  Juan Render deploy + the `AWEB_CUSTODIAL_E2EE_KEY` +
  `AWEB_CUSTODIAL_E2EE_KEY_ID` env confirm (Grace + Mia
  requirement). Expected post-deploy: aweb_version flips to
  **1.26.5**. Smoke a hosted custodial E2EE flow after the flip;
  any `custodial_e2ee_kek_unconfigured` / 500 → bad deploy → roll
  back. Task #248.
- **PyPI aweb**: **1.26.5** (server-v1.26.5 verified-live
  2026-05-28; wheel contains
  migrations/aweb/007_agent_encryption_key_custody.sql byte-identical
  to source).
- **npm @awebai/aw**: **1.26.4** (E2EE opt-in default, `--plaintext`
  visible, hosted cert-only add-worktree fix). aw 1.26.3 is the
  carrier of the workspace-cleanup regression (#245); 1.26.4 does NOT
  fix it. Anyone still on 1.26.3 who renames a workspace dir risks
  re-triggering the deletion.
- **npm @awebai/claude-channel**: **1.4.11** (channel-core local-aw
  decrypt for E2EE awakenings).
- **npm @awebai/claude-skills**: **0.2.10** (em-dash → colon in
  plugin.json description).
- **npm @awebai/pi**: **0.1.16** (bundles canonical skill content
  byte-identical to aweb main).
- **awid-service**: **0.5.9** (PyPI + Docker GHCR, api.awid.ai/health
  green).
- **Marketplace pins** (claude-plugins): aweb-channel 1.4.11,
  aweb-skills 0.2.10. Note: claude-plugins marketplace.json
  description fields still carry em-dashes; per Sofia (mail
  c2abf4ff) those don't load-bear (banked
  `feedback_discipline_load_bearing`), leave as-is.

## Open holds

### #245 — aw 1.26.3 cleanup regression (P0 customer impact)

8b55181 added `aw workspace status` cleanup that classifies
workspaces with stale `last_seen_at` or `workspace_path` not existing
on disk as "gone local" and DELETEs them server-side. Juan hit this
live on 2026-05-28 with the **pmbah** team: he renamed his
workspace parent dir (pmh → pmbah), the next `aw workspace status`
on Mac.c.is saw `/Users/juanre/prj/pmh/...` paths don't exist, and
the server soft-deleted coord + dev agents + their workspaces
(review survived first sweep due to ordering luck, was re-deleted on
sweep #2).

**Recovery state**:
- All 3 pmbah agents (coord/dev/review) + their workspaces undeleted
  via targeted UPDATE (`deleted_at = NULL` only on rows whose
  `deleted_at` matched the incident windows 2026-05-28 10:11:33 and
  10:41:20-21).
- `workspace_path` rewritten to actual current on-disk locations:
  `/Users/juanre/prj/pmbah/pmbah/agents/coordinator`,
  `/Users/juanre/prj/pmbah/pmbah/worktrees/possiblymadebyahuman-{dev,review}`.
  Juan-confirmed; should now survive the next sweep.
- Mail data was preserved (22 messages in 2 conversations, both
  active); `aweb.messages` has no `deleted_at` column. Chat was
  never used by this team.

**Fix-forward shape pending Athena + Mia decision** (mail thread
96317ca9 has my open questions): (a) cleanup requires multi-signal
gone-evidence not path-existence alone, (b) prompt before
auto-DELETE rather than silent sweep, (c) gate behind `--cleanup`
flag default off. Not yet authored. Don't ship a CLI release that
extends 8b55181 behavior; ANY ship targeting
cli/go/cmd/aw/workspace* should explicitly address this.

### #239 — aw 1.27.0 E2EE-default Phase 2

702ccb7 ("cli: default messaging to e2ee") merged into main via
a3d41ec, then the receive-side (channel 1.4.11 + Pi 0.1.16) shipped
on 2026-05-26. 21928a2 then REVERTED the send-side default for
customer-meeting safety (aw 1.26.2: default plaintext, `--e2ee`
opt-in). Phase-2 ship of aw 1.27.0 with E2EE-default-on is gated
on customer-adoption signal of 1.4.11 / 0.1.16 receive-side. Grace
owns the adoption-threshold call. Do not tag aw-v1.27.0 without
explicit re-route through Grace.

## In-flight (cycle this wake-up)

- **#248** AC v0.5.59 Render deploy waiting on Juan. After deploy:
  /health flips to v0.5.59 / aweb_version=1.26.5 / git_sha=0896ecea
  / awid=0.5.9, all four coordination_schema modules up_to_date.
  Smoke hosted custodial E2EE flow before posting verified-live.
  Mia's non-blocking recommendation for v0.5.60: startup-time KEK
  validation so missing keys fail health/deploy rather than first
  customer request.

## Recent activity worth knowing

- **2026-05-28 site restructure** (Olivia + Athena tech-ACK):
  home/developers swap (new `/mcp` page, `/developers/` → `/` alias),
  4-tier pricing port, llms.txt mirrors aligned, tagline drops
  "skip the bottlenecks", "Opt-in E2EE" badges tightened, "For
  developers" prefix removed from home eyebrow, /mcp +
  /orchestration teaser panels added on home. All deployed via
  `cd ac && make deploy-site` from main; all verified-live by
  Olivia. Final SHA on deploy-landing: **92860b93**.
- **2026-06-01 default-aaaj observation** (banked NEUTRALLY per
  Juan's correction, ref `feedback_observation_vs_defect` memory):
  CLI signup creates an anonymous `cli_signup` user (`email=NULL`)
  unlinked from a matching dashboard user. Thanos Diacakis is the
  evidence (2 unlinked aweb_cloud.users rows for one human).
  Filed as `default-aaaj` priority=P3 type=task (NOT a defect).
  Aida stood down — no support escalation unless a customer
  reports actual confusion. Artifact:
  `artifacts/cli-signup-dashboard-user-gap-20260527.md`.
- **2026-06-02 analytics scripts banked** under `scripts/`. See
  AGENTS.md "Analytics & probe scripts" section. Triggered by Juan
  ("we really need to have pre-made scripts for the questions that
  you get from bertha and from me"). Scripts cover:
  N-day sign-ups, per-user behavioral snapshot, multi-agent
  activity check, per-team probe.

## Customer activity reality check (as of 2026-06-02)

External adoption of the multi-agent value prop is still **zero**:
- 31 external aweb_cloud.users rows have 2+ active agents.
- 2 of 31 show any cross-agent activity in the past 7 days, and
  both look like Juan's own CLI bootstraps (pmbah for sure;
  the `noob<random>` slug likely also exploration).
- Bertha (Eugenie's outreach agent) was asking about Thanos +
  Di Huang — neither has heartbeated a workspace since signup;
  0 messages, 0 tasks.

This is product reality, not a triage signal. Sofia + Iris own the
direction read. Don't escalate; just keep the scripts current so
the data stays one command away.

## What to check first on wake-up

1. `git pull` from ai.aweb to get any new merges since this handoff.
2. `aw chat pending && aw mail inbox` for any new asks.
3. `curl -sS https://app.aweb.ai/health` and `curl -sS
   https://api.awid.ai/health`. If app.aweb.ai flipped to v0.5.59
   while you were idle, close #248 with verified-live mail + the
   custodial E2EE smoke evidence. If still v0.5.58, signal Juan
   for Render deploy if you haven't already.
4. `aw mail show 96317ca9` — Athena/Mia thread on the #245 cleanup
   regression fix-forward; check if a fix shape arrived for which
   you'd cut aw-v1.26.5 or aw-v1.27.0.
5. `aw task list --status pending` — open follow-ups (#234
   sibling-overlay guard, #226 colon-encoding, #210 Hugo bump,
   #190/#191 MCP OAuth live smoke + Sofia loop, etc).

## Banked discipline acquired in this cycle

(Worth knowing because they'll catch you on the next analog
situation.)

- **Don't presume defect framing on a first-of-its-kind data
  shape.** Observation > defect. From Juan correction on the Thanos
  cli-signup writeup. Memory: `feedback_observation_vs_defect.md`.
- **Don't auto-apply discipline to adjacent surfaces.** Check
  whether the rule load-bears there first. From Sofia + Juan on
  the em-dash-in-marketplace.json question. Memory:
  `feedback_discipline_load_bearing.md`.
- **Pi/skills tarball verification: compare against
  `git show <tag>:skills/<skill>/SKILL.md`** (the aweb-root
  `skills/` tree that prepack/sync-skills copies from), NOT
  against local `packages/claude-skills/skills/` (gitignored,
  only populated by running sync-skills locally). Earlier
  verifications of claude-skills 0.2.9/0.2.10 happened to pass by
  luck.
- **CLI_VERSION coupling in aweb Makefile** (task #219):
  `make ship` bumps both server and CLI in lockstep.
  Tag-only-at-target-sha is the workaround for CLI-only or
  server-only releases (the pattern used for aw 1.26.1-1.26.4 and
  server 1.26.5).
- **PyPI propagation lag**: `uv pip install aweb==X.Y.Z` may fail
  immediately after publish even when the per-version
  `/pypi/aweb/X.Y.Z/json` is canonical. Direct wheel download from
  files.pythonhosted.org bypasses the resolver lag; Grace can use
  `uv sync --refresh-package aweb` for the same purpose.

## Files in this dir

- `AGENTS.md` (= CLAUDE.md symlink) — operating instructions.
- `handoff.md` — this file. Update when state changes meaningfully.
- `runbook.md` — release-runbook detail.
- `scripts/` — reusable analytics + probe scripts. Committed.
- `artifacts/` — sensitive ops dumps + writeups (local-only, NOT
  in git per repo discipline). Contains:
  awid_cleanup_juanreyero_*.py (May 24 one-off),
  cli-signup-dashboard-user-gap-20260527.md (default-aaaj
  observation writeup).
- `aweb`, `ac` — sibling repo symlinks for read access + running
  release gates.
