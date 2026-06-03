# Hestia Logbook

Dense narrative history. Append a new dated section at the top
whenever state changes meaningfully — release waves, incidents,
discipline banked, lessons learned, customer-activity reads, etc.
Each entry is a snapshot at that moment, not a rolling rewrite.

Future-you reads `handoff.md` first to know what to do NOW. You
come HERE when you need depth on something handoff.md only points
at — a referenced incident, a banked decision, a release wave's
backstory.

Format: `## YYYY-MM-DD <short title>` headers. Most recent on top.
Keep entries chronologically accurate — don't merge old entries
with new context. Write them as point-in-time snapshots so they
remain a faithful record.

---

## 2026-06-02 — restart-ready snapshot after May 26 → June 2 wave

### Live matrix

- AC: app.aweb.ai/health → release_tag=v0.5.58 git_sha=340122ef
  aweb_version=1.26.1 awid_service_version=0.5.9. **In-flight**:
  v0.5.59 image is in GHCR (run 26767320236 success). Awaiting
  Juan Render deploy + AWEB_CUSTODIAL_E2EE_KEY +
  AWEB_CUSTODIAL_E2EE_KEY_ID env confirm (Grace + Mia
  requirement). Expected post-deploy: aweb_version flips to
  1.26.5. Smoke a hosted custodial E2EE flow after the flip; any
  custodial_e2ee_kek_unconfigured / 500 → bad deploy → roll back.
  Task #248.
- PyPI aweb: 1.26.5 (server-v1.26.5 verified-live 2026-05-28;
  wheel contains migrations/aweb/007_agent_encryption_key_custody.sql
  byte-identical to source).
- npm @awebai/aw: 1.26.4 (E2EE opt-in default, --plaintext
  visible, hosted cert-only add-worktree fix). aw 1.26.3 is the
  carrier of the workspace-cleanup regression (#245); 1.26.4 does
  NOT fix it. Anyone still on 1.26.3 who renames a workspace dir
  risks re-triggering the deletion.
- npm @awebai/claude-channel: 1.4.11 (channel-core local-aw
  decrypt for E2EE awakenings).
- npm @awebai/claude-skills: 0.2.10 (em-dash → colon in
  plugin.json description).
- npm @awebai/pi: 0.1.16 (bundles canonical skill content
  byte-identical to aweb main).
- awid-service: 0.5.9 (PyPI + Docker GHCR, api.awid.ai/health
  green).
- Marketplace pins (claude-plugins): aweb-channel 1.4.11,
  aweb-skills 0.2.10. claude-plugins marketplace.json description
  fields still carry em-dashes; per Sofia those don't load-bear
  (banked feedback_discipline_load_bearing), leave as-is.

### Open holds

#### #245 — aw 1.26.3 cleanup regression (P0 customer impact)

8b55181 added `aw workspace status` cleanup that classifies
workspaces with stale last_seen_at or workspace_path not existing
on disk as "gone local" and DELETEs them server-side. Juan hit
this live on 2026-05-28 with the pmbah team: renamed his
workspace parent dir (pmh → pmbah), the next `aw workspace status`
on Mac.c.is saw /Users/juanre/prj/pmh/... paths don't exist, and
the server soft-deleted coord + dev agents + their workspaces
(review survived first sweep due to ordering luck, was re-deleted
on sweep #2).

Recovery state:
- All 3 pmbah agents (coord/dev/review) + their workspaces
  undeleted via targeted UPDATE (deleted_at = NULL only on rows
  whose deleted_at matched the incident windows 2026-05-28
  10:11:33 and 10:41:20-21).
- workspace_path rewritten to actual current on-disk locations:
  /Users/juanre/prj/pmbah/pmbah/agents/coordinator,
  /Users/juanre/prj/pmbah/pmbah/worktrees/possiblymadebyahuman-{dev,review}.
  Juan-confirmed; should now survive the next sweep.
- Mail data was preserved (22 messages in 2 conversations, both
  active); aweb.messages has no deleted_at column. Chat was never
  used by this team.

Fix-forward shape pending Athena + Mia decision (mail thread
96317ca9): (a) cleanup requires multi-signal gone-evidence not
path-existence alone, (b) prompt before auto-DELETE rather than
silent sweep, (c) gate behind --cleanup flag default off. Not yet
authored. ANY ship targeting cli/go/cmd/aw/workspace* should
explicitly address this.

#### #239 — aw 1.27.0 E2EE-default Phase 2

702ccb7 ("cli: default messaging to e2ee") merged into main via
a3d41ec, then the receive-side (channel 1.4.11 + Pi 0.1.16)
shipped on 2026-05-26. 21928a2 then REVERTED the send-side
default for customer-meeting safety (aw 1.26.2: default plaintext,
--e2ee opt-in). Phase-2 ship of aw 1.27.0 with E2EE-default-on is
gated on customer-adoption signal of 1.4.11 / 0.1.16 receive-side.
Grace owns the adoption-threshold call. Do not tag aw-v1.27.0
without explicit re-route through Grace.

### Recent activity

- 2026-05-28 site restructure (Olivia + Athena tech-ACK):
  home/developers swap (new /mcp page, /developers/ → / alias),
  4-tier pricing port, llms.txt mirrors aligned, tagline drops
  "skip the bottlenecks", "Opt-in E2EE" badges tightened, "For
  developers" prefix removed from home eyebrow, /mcp +
  /orchestration teaser panels added on home. All deployed via
  `cd ac && make deploy-site` from main; all verified-live by
  Olivia. Final SHA on deploy-landing: 92860b93.
- 2026-06-01 default-aaaj observation (banked NEUTRALLY per
  Juan's correction, ref feedback_observation_vs_defect memory):
  CLI signup creates an anonymous cli_signup user (email=NULL)
  unlinked from a matching dashboard user. Thanos Diacakis is the
  evidence (2 unlinked aweb_cloud.users rows for one human).
  Filed as default-aaaj priority=P3 type=task (NOT a defect).
  Aida stood down — no support escalation unless a customer
  reports actual confusion. Artifact:
  artifacts/cli-signup-dashboard-user-gap-20260527.md.
- 2026-06-02 analytics scripts banked under scripts/. See AGENTS.md
  "Analytics & probe scripts" section. Triggered by Juan ("we
  really need to have pre-made scripts for the questions that you
  get from bertha and from me"). Scripts cover: N-day sign-ups,
  per-user behavioral snapshot, multi-agent activity check,
  per-team probe.

### Customer activity reality check

External adoption of the multi-agent value prop is still zero:
- 31 external aweb_cloud.users rows have 2+ active agents.
- 2 of 31 show any cross-agent activity in the past 7 days, and
  both look like Juan's own CLI bootstraps (pmbah for sure; the
  noob<random> slug likely also exploration).
- Bertha (Eugenie's outreach agent) was asking about Thanos +
  Di Huang — neither has heartbeated a workspace since signup;
  0 messages, 0 tasks.

This is product reality, not a triage signal. Sofia + Iris own the
direction read. Don't escalate; just keep the scripts current so
the data stays one command away.

### Banked discipline acquired in this cycle

Worth knowing because they'll catch you on the next analog
situation:

- Don't presume defect framing on a first-of-its-kind data shape.
  Observation > defect. From Juan correction on the Thanos
  cli-signup writeup. Memory: feedback_observation_vs_defect.md.
- Don't auto-apply discipline to adjacent surfaces. Check whether
  the rule load-bears there first. From Sofia + Juan on the
  em-dash-in-marketplace.json question. Memory:
  feedback_discipline_load_bearing.md.
- Pi/skills tarball verification: compare against
  `git show <tag>:skills/<skill>/SKILL.md` (the aweb-root skills/
  tree that prepack/sync-skills copies from), NOT against local
  packages/claude-skills/skills/ (gitignored, only populated by
  running sync-skills locally). Earlier verifications of
  claude-skills 0.2.9/0.2.10 happened to pass by luck.
- CLI_VERSION coupling in aweb Makefile (task #219): `make ship`
  bumps both server and CLI in lockstep. Tag-only-at-target-sha is
  the workaround for CLI-only or server-only releases (the pattern
  used for aw 1.26.1-1.26.4 and server 1.26.5).
- PyPI propagation lag: `uv pip install aweb==X.Y.Z` may fail
  immediately after publish even when the per-version
  /pypi/aweb/X.Y.Z/json is canonical. Direct wheel download from
  files.pythonhosted.org bypasses the resolver lag; Grace can use
  `uv sync --refresh-package aweb` for the same purpose.

### Ship summary (May 26 → June 2)

| Date | Artifact | Source | Outcome |
|---|---|---|---|
| 2026-05-26 | AC v0.5.58 | 93454954 | verified-live (activity-card metadata-only) |
| 2026-05-26 | channel 1.4.9 | db9a492 | verified-live (mcpName for MCP registry) |
| 2026-05-26 | channel 1.4.10 + skills 0.2.10 | 848bba5 | verified-live (em-dash → colon plugin.json) |
| 2026-05-26 | channel 1.4.11 + Pi 0.1.16 | ea75b1a | verified-live (E2EE decrypt receive-side) |
| 2026-05-27 | aw CLI 1.26.2 | 21928a2 | verified-live (E2EE opt-in revert for customer mtg) |
| 2026-05-27 | aw CLI 1.26.3 | 8b55181 | verified-live (workspace cleanup; introduced #245) |
| 2026-05-28 | aw CLI 1.26.4 | a3fbc47 | verified-live (hosted cert-only add-worktree) |
| 2026-05-28 | server-v1.26.5 | 54c30fa | verified-live (PyPI; 007 migration for AC E2EE) |
| 2026-06-01 | aweb.ai site restructure | 92860b93 | verified-live by Olivia |
| 2026-06-02 | analytics scripts banked | hestia/scripts/ | committed |
| In flight | AC v0.5.59 | 0896ecea | GHCR ready; awaiting Render deploy |

---

<!-- Earlier entries go below. Append new entries above this line. -->
