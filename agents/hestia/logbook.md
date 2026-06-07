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

## 2026-06-07 — aapz HOLD mid-AWID-wave (P1 audit)

Grace handed off aapz aw agents lifecycle release at aweb
0f303786 (9626e66d). 5-surface wave: awid 0.5.10 → aweb 1.26.8 →
skills 0.2.12 → Pi 0.1.20, with AC v0.5.60 floor bump deferred
until v0.5.59 verified-live. Scope verified empirically: awid
1484 LOC, server 43 LOC, CLI 5919 LOC, skills/aweb-bootstrap
canonical drift sha 0a29e68 → 52f4c5b.

Mailed planned versions e92c48d1; Grace green-lit with
corrections (d419d930): tag at bump SHA not 0f303786, migration
path is `awid/src/awid_service/migrations/` not
`awid/src/awid/migrations/`, AC deferral OK with explicit
verified-live mention, skills uses workflow not hand-bump, Mia
is aapz reviewer-of-record (no Athena re-loop). Grace short-form
ACK 8190c796 confirmed.

Executed AWID wave 1:
- awid/pyproject.toml 0.5.9 → 0.5.10 + uv sync
- make release-awid-check: 201 tests passed
- Commit 9e921ecc 'release: awid-service 0.5.10 (aapz wave 1 …)'
- Tags awid-service-v0.5.10 + awid-v0.5.10 at 9e921ecc
- Pushed main + both tags individually (per banked policy)
- GHA awid-service PyPI run 27086928868 success: awid-service
  0.5.10 LIVE on PyPI (2 artifacts)
- GHA awid GHCR run 27086931086 success: Docker image in ghcr.io

NOT executed (HOLD landed mid-flight):
- AWID prod migrations (006_identity_encryption_key_custody.sql)
- api.awid.ai Render redeploy signal
- aweb wave 2 (server 1.26.8 + aw 1.26.8)
- skills 0.2.12, Pi 0.1.20

Grace HOLD (a147126b + 992469cf): Juan challenged proceeding
with aapz.16/.18/.19/.21 open. Disposition:
- KEEP 0.5.10 on PyPI (no yank, no force rollback)
- KEEP GHCR image (workflow already completed)
- KEEP bump commit 9e921ecc + tags on origin/main
- All runtime/deployment steps HELD
- Possible outcome: deployed AWID becomes 0.5.11 post-audit,
  with 0.5.10 as unused artifact — Grace says preferable to
  yank or history-rewrite.

api.awid.ai continues serving 0.5.9 — no production change. PyPI
+ GHCR are registry artifacts only until migrations + redeploy
fire.

Lesson banked (will surface next AWID/aweb wave): peer
green-light at the wave gate ≠ closure on epic P1 audit. Before
tagging+pushing registry-permanent artifacts, re-verify open P1s
in the epic even with explicit wave authorization. The aw 1.26.6
lesson covered 'peer-validation ≠ canonical gate at target SHA';
this is its dual: 'wave green-light ≠ epic ready'.

---

## 2026-06-07 — Pi 0.1.19 verified-live (description colon-led tweak)

Olivia mail 93a16ac6 from aweb b7015275: bump 0.1.18 → 0.1.19
with description revision (em-dash → colon-led list of three
clauses, surfaces 'join agent teams' capability). Juan-authored
description, fast-tracked same as 0.1.18.

Bump commit 2b76c804 narrow (only pi-extension/package.json).
WIP in tree (team_bootstrap.go, docs, skills/aweb-bootstrap) not
swept per Olivia heads-up. Tag pi-v0.1.19 pushed individually,
GHA pi-release run 27086086858 success.

Content-verify against b619aca canonical: description matches
spec byte-for-byte; README byte-identical to
b619aca:pi-extension/README.md (no change since 0.1.18, sha256
bfae6902…); all 5 SKILL.md hashes byte-identical to
b619aca:skills/<skill>/SKILL.md (Wave 5 sync intact).
Verified-live mail ce7ab07e to peers + Juan. Olivia ACK
24384f53, then independent verify-after came back clean.

---

## 2026-06-06 — Pi 0.1.18 verified-live (README + marketplace-card rewrite)

Olivia's mail 07ad3f2c arrived: bump @awebai/pi 0.1.17 → 0.1.18 from
aweb b619aca. Scope: pi-extension/README.md fully rewritten for
cold-reader Pi users (no aweb background) + package.json description
field rewrite ("Lets your Pi communicate with other AI agents on an
open network…"). Juan-authored, greenlit directly — Sofia/Athena
framing review chain bypassed explicitly per author. SKILL.md
content unchanged (Wave 5 sync from aapy still canonical).

Discipline notes captured in flight:
- Olivia called out unrelated WIP in working tree
  (atomic-address-claim, team_bootstrap.go, ratelimit.py,
  dns_addresses.py, registry_register_test.go, cli-command-reference.md
  — none hers, scope-creep risk). I confirmed back: ONLY
  pi-extension/package.json staged for the bump. Verified via
  `git diff --cached --name-only` returning that single file before
  commit.
- Bump commit fba2108 is narrow: 1 file, 1 insertion, 1 deletion.
- Tag pi-v0.1.18 pushed individually (banked policy).
- GHA pi-release.yml run 27061497123 success — sync-skills + build +
  version-check + npm publish.

Content-verify against canonical:
- README.md byte-identical to `git show b619aca:pi-extension/README.md`
  (sha256 bfae69022014f6b1085e49c17210114242e545f4fdd88774e7e70f377a3d21fe).
- package.json description matches Olivia's spec verbatim.
- All 5 SKILL.md hashes (aweb-identity, aweb-team-membership,
  aweb-messaging, aweb-bootstrap, aweb-coordination) byte-identical
  to `git show b619aca:skills/<skill>/SKILL.md`. Wave 5 sync intact —
  Pi tarball still carries the aapy in-repo bootstrap content from
  b78fc79.

Verified-live mail 9d1ff678-e0d5-49c8-84dc-9e0830ff270e sent to
Olivia + Grace + Athena + Sofia + Iris + Aida with 4-point standard
shape (fixed / not fixed / evidence / live check) plus full live
matrix. Olivia (mail 9c8fe60e) ACK'd plan and is standing by to run
her independent verify-after — npm pack + diff README + description
+ 5 SKILL hashes against b619aca canonical — to close.

Marketplace.json (claude-plugins repo) NOT bumped — Pi is not a
Claude Code plugin; only @awebai/claude-channel and
@awebai/claude-skills are. Pi installs from npm direct via Pi's own
extension system.

Task #255 closed.

---

## 2026-06-03 — first external multi-agent customer detected (andi.aweb.ai)

Bertha pinged in chat asking how to reach `andi.aweb.ai/coord`
and `andi.aweb.ai/coord-global` because she was getting connection
errors. Ran `scripts/team_probe.py --team default:andi.aweb.ai`.

**What I found:** the andi BYOT team was registered today
2026-06-03 09:44 UTC with 4 active agents (coord, dev, review,
remoteagent) running on a Hetzner host (ubuntu-8gb-nbg1-1) plus
one remote-machine agent on Theresias-MacBook-Air.local. By
10:13 UTC they had 17 mail + 5 chat messages across 6 active
conversations, with coord ↔ dev coordinating on real tasks
(default-aaaa etc).

**Why this matters:** yesterday's customer-activity reality
check (2026-06-02 logbook entry below) said "External adoption
of the multi-agent value prop is still zero." Today: not zero
anymore. Andi is the first observed external team actually
doing the thing we built aweb for — multi-agent coordination in
production, with a remote agent joining a self-hosted team.

**Why Bertha's connection errors:**
- `coord-global` doesn't exist as an alias on this team. Likely
  a customer-typed typo or a mis-remembered alias. `coord` is
  the right one.
- The team's DNS TXT (`_awid.andi.aweb.ai`) shows
  `dns_status='desired'` in our managed_namespaces row. The AWID
  registry knows what they SHOULD publish, but if the customer
  hasn't put the TXT live on their DNS yet, federated DID
  verification fails and the route returns a connection error.
  Worth retrying after a few hours and/or checking with the
  customer that they've published the TXT record.

**Contact path gap:** all 5 org members of the andi
organization are anonymous cli_signup users with `email=NULL`.
Same shape as the default-aaaj observation (Thanos). We have NO
dashboard-side path to the human behind the namespace. Bertha's
only in-system contact route is federated mail/chat to one of
the agents. If Eugenie needs an out-of-band channel (email,
twitter, GitHub) she needs to source it externally.

**Routing to Sofia + Juan as direction-level signal** (mail
sent in same beat). This changes the "is anyone using aweb"
narrative we held for 24h. Not just a flicker either — they
have a Hetzner instance running, cross-machine federation set
up, real task coordination happening. Worth Iris/Sofia
considering whether an outreach (via the federated mail-to-coord
path) makes sense, or whether to leave them to discover us.

**Banked discipline (new):** the `team_probe.py` script paid
back its banking cost immediately. First wake-up after the
scripts shipped, first probe required, produced the answer in
under a minute. Validates the pattern Juan asked for:
pre-made scripts > one-off `/tmp/probe.py`.

**Aida refinement (mail 3be0742f):** "wait for them to come to
us" isn't ONLY a posture choice — it's the current technical
default. With their `_awid.andi.aweb.ai` in `desired` state and
their org all-anonymous cli_signup, we literally cannot reach
them via federation right now. So when Sofia weighs the
proactive-reach-out question, the framing is "we technically
can't yet" as much as "we're choosing not to." If Sofia later
greenlights outreach, Aida offered her lane (`aweb.ai/aida`,
framed "noticed you're running multi-agent — any setup friction
we can help with?") as the least surveillance-y first-touch
shape: question-about-helping > question-about-us-seeing-their-
activity. Routing option, not a push.

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
