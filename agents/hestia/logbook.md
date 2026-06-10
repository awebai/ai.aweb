# Hestia Logbook

Dense narrative history. Append a new dated section at the top
whenever state changes meaningfully — release waves, incidents,
discipline banked, lessons learned, customer-activity reads, etc.
Each entry is a snapshot at that moment, not a rolling rewrite.

## 2026-06-10 — Olivia site deploy f528b366: hero intent tabs verified-live 3/3 (Playwright-measured no-layout-shift)

### Arc summary

Olivia's second site change in two days — three-tab intent
switcher [In your terminal | As a team | In your browser] in the
home hero card. Rose-reviewed b0907441 + Juan design-approved.
Batches naturally with yesterday's still-pending Render clean
rebuild for /docs/team-bootstrap.md: one Render clear-build-cache
settles both waves.

### Verify trail

- `make deploy-site` from ac main f528b366 → sync commit 00838640
  → push 2facc1e1..00838640 main → deploy-landing clean.
- Hugo built: 51 pages, 33 static files, 2 aliases, 0 cleaned.
- Render rebuilt by 08:07:17 UTC (verified via last-modified on
  fresh paths).
- Checklist 1/3: pill toggle [In your terminal | As a team | In
  your browser] all three labels rendered; default-terminal panel
  has 'npm install' + 'aw init' (3 hits each).
- Checklist 2/3: Playwright-measured layout-shift across tab
  switches:
  * Hero `<section>` = 1200 × 646.75 across all 3 tab states (0px
    delta).
  * Panel container `.hero-code--intent` = ~442px pinned
    (terminal 442.0, team 442.4, browser 442.0; <0.5px subpixel
    jitter).
  * Individual visible panel content varies 232–323px but
    container clamp absorbs.
  * Confirms commit's "Card height pinned so tab switches don't
    shift layout" claim.
- Checklist 3/3: /llms.txt has 'Get started — pick where you
  work' heading + ### In your terminal / ### As a team / ### In
  your browser panel headers in tab order.
- ARIA tablist semantics (commit claim): VERIFIED. 1
  `role=tablist`, 3 `role=tab` (1 `aria-selected=true` on default
  terminal, 2 `aria-selected=false`), 3 `role=tabpanel`, 3
  `aria-labelledby` cross-refs.
- Adjacent yesterday hold: /docs/team-bootstrap.md still
  last-modified Mon 2026-06-08 — Render hasn't done the
  clear-build-cache yet.

### Banked lesson

**Hugo `--minify` strips attribute quotes per HTML5 spec.** When
curl-probing for ARIA / role / data-* attributes, use a
quote-optional regex: `role="?tablist"?` not `role="tablist"`.
Earlier today's first probe scored 0 ARIA hits and looked like a
defect; the markup was correct, my regex was wrong. Verify
infrastructure contract before debating policy is the meta-rule;
verify regex behavior on minified output is its corollary for
site verify-live.

### Coordination

- Mailed Olivia (msg 870b866d) + Sofia (msg 21a86223) with
  3/3 PASS evidence + the yesterday hold reminder.
- Sofia ACK (msg 6ec5ca1a): carries f528b366 verified-live;
  team-bootstrap.md cleanup not fully closed until post-rebuild
  curl confirms 404.
- Task #267 tracks the f528b366 wave; #266 still pending Juan's
  Render-side fix.

### Next-move-if-resumed

1. Re-curl `/docs/team-bootstrap.md` periodically; expect HTTP
   404 once Render clear-build-cache lands.
2. Mail closure to Olivia + Sofia with the post-rebuild evidence,
   closing aweb-aaqe.6 and #266.
3. No further Hestia action on this wave — Juan owns the Render
   dashboard step.

---

## 2026-06-09 — Olivia site deploy 2facc1e1: 5/6 verified-live, Render publish-dir staleness banked as #266

### Arc summary

Cut Olivia's blueprint-voice site deploy from ac main 2facc1e1
("blueprint voice for home hero, teasers, and docs redirect").
Five of six checklist items verified live on aweb.ai cleanly.
Sixth item (/docs/team-bootstrap.md should 404) blocked on
Render-side publish-dir staleness — file deleted from source +
Makefile sync list, local Hugo build doesn't include it, deploy-
landing tree at 2facc1e1 has no team-bootstrap.md anywhere, but
Render still serves the 15KB file with prior-sync mtime. Other
paths show fresh today's mtime. Root cause: Render's publish dir
not cleaned between builds.

### Sequence (all 2026-06-09)

- `make deploy-site` ran clean from ac main 2facc1e1 → built
  Hugo locally (51 pages, 33 static files, 2 aliases, 0 cleaned),
  push 7203f5c2..2facc1e1 main → deploy-landing landed.
- First probe at +30s after deploy: CF Pages still serving stale
  Hugo build (`Hugo 0.124.1` in generator meta), all 6 items
  showed pre-deploy state.
- Second probe at +120s: Render rebuilt. 5/6 items green:
  * Home hero: "Create a team · from a blueprint" present;
    runtime-toggle / hero-runtime CSS classes absent.
  * /mcp: "Create your team from a blueprint" present.
  * /docs/team-bootstrap/: Hugo meta-refresh alias page with
    `<link rel=canonical href=https://aweb.ai/orchestration/>` +
    `<meta http-equiv=refresh content="0; url=https://aweb.ai/orchestration/">`.
    Body has no team-bootstrap content. Olivia ACK: meta-refresh
    acceptable for static host, no hard 30x expected.
  * /llms.txt: 0 "aw agents bootstrap", 7 "blueprint" hits.
  * /mcp/llms.txt: 0 "aw agents bootstrap".
  * Docs sidebar: 0 "Bootstrap a repo-local aweb team" listings.
- 6th item gap: `/docs/team-bootstrap.md` HTTP 200, content is
  full original markdown, `last-modified: Mon 2026-06-08 07:17:01
  UTC` (prior 7203f5c2 sync commit timestamp). Other paths show
  `last-modified: Tue 2026-06-09 22:10:31 UTC` (today's build).
- Source-side audit confirms file genuinely absent:
  * 2facc1e1 deleted `site/static/docs/team-bootstrap.md` (459
    lines per `git show --stat`).
  * Makefile diff removed `team-bootstrap.md` from
    `AWEB_PUBLIC_DOCS` AND `AWEB_HUGO_DOCS` lists.
  * `sync-public-docs` target does `rm -f
    "$(AWEB_STATIC_DOC_DIR)"/*.md` then re-copies AWEB_PUBLIC_DOCS
    — so it won't recreate team-bootstrap.md.
  * Local `ls -la ac/site/static/docs/` and `ls ac/site/public/docs/`
    both have no team-bootstrap.md.
  * `git -C ac ls-tree -r origin/deploy-landing | grep team-bootstrap`
    returns empty.
- Conclusion: Render's publish dir is incremental — files removed
  from source persist in published output. Render's build command
  for aweb.ai static site likely does `hugo --minify` without
  `--cleanDestinationDir`.

### Coordination

- Mailed Olivia (juan.aweb.ai/olivia, msg 6a216fcc) with full
  verify-live report + Render-side hypothesis + ask for Juan
  Clear-build-cache & deploy.
- Mailed Sofia (aweb.ai/sofia, msg 03056d2f) with same +
  framing-review request.
- Tried Juan via `juan`, `juanre`, `juan.aweb.ai/juan`, `aweb.ai/juan`
  — all 404. Sofia replied she's in session with Juan and
  surfacing the Render clear-cache ask directly.
- Olivia replied (msg d51a5424): confirmed /docs/team-bootstrap.md
  should hard 404 (no stub — it was agent-facing copy for
  superseded flow, canonical legacy reference stays in aweb repo);
  meta-refresh acceptable; +1 on #266 Makefile pre-clean as
  durable fix.
- Sofia replied with framing-pass (msg 2c415cd9): mail names
  what-fixes / what-doesn't / evidence chain, all good; she
  independently re-curled and grepped to confirm; will close
  HOLD-B (site setup-framing) once stale .md confirmed gone; +1
  on #266 Makefile pre-clean.
- Sofia second reply (msg 7245b58e): confirmed live hero teaches
  blueprint prompt + aw commands all in released 1.26.8, so
  HOLD-B substance is resolved pending the post-rebuild check.
- ACK'd Sofia (msg 65bb8b26) with closure-condition: post-rebuild
  curl routed to her + Olivia, then HOLD-B closes; Makefile
  pre-clean diff prepped after verify closes.

### Banked discipline

- **Olivia's address is `juan.aweb.ai/olivia`** (cross-namespace
  form). Short `olivia` 404s, `aweb.ai/olivia` 404s. Memory
  already had this; verified again.
- **Juan's aw alias not reachable via short forms.** Loop through
  Sofia when she's in session; else Juan@aweb.ai direct.
- **Render publish-dir staleness is real.** Site-deploy verify-live
  must specifically re-curl URLs of REMOVED static files, not just
  ADDED/MODIFIED ones. Banked as task #266; #266's fix is Makefile
  pre-clean of publish dir before hugo build (both Olivia + Sofia
  +1; doesn't depend on Render config staying correct).

### Task created

- #266 Render publish-dir stale for removed-from-source static
  files (aweb.ai). Pending Juan's Render Clear-build-cache & deploy
  first, then Makefile pre-clean diff lands as the durable fix.

### Next-move-if-resumed

1. Re-curl `https://aweb.ai/docs/team-bootstrap.md` periodically
   until 404 or fresh mtime.
2. Mail Olivia + Sofia closure with the post-rebuild evidence.
3. Cut Makefile pre-clean diff (rm publish dir before hugo) under
   #266 — prep in a branch, mail Athena for review before push.

---

## 2026-06-08 — a2a-gw v1.26.9 lane: image banked, manual-deploy abandoned, pivot to AC-managed gateway

### Arc summary

Full release-chain ran from gate-review through tag-push through
GHCR build through Render Web Service creation. Manual-deploy lane
collapsed at the workspace-state delivery question. Grace pivoted
mid-arc to AC-managed gateway as the product path. Image +
infrastructure stay banked at 66b0e70c; nothing rolled back; no
identity provisioning was started; no controller keys touched.

### Sequence of events (all 2026-06-08)

- Grace pushed bab02eb1 (initial gateway container release + e2e)
  for review. Hestia reviewed: APPROVE structural shape, flagged
  2 P1 gaps (gateway identity provisioning subsection missing;
  /health AWID version-floor advertisement-only, not enforced), 1
  P2 clarification (narrow-gate caveat), 1 decision-confirm
  (Render not Hetzner).
- Grace pushed 66b0e70c with fixes folded credibly: new "Gateway
  Identity Provisioning" runbook subsection (creation, team-cert,
  smoke, AWID publication, gateway.yaml template, Render delivery,
  rotation, compromise procedure), /health Compatible+MinimumVersion
  enforcement with 503 on missing/old AWID, narrow-gate caveat, Render
  decision banked with "Hetzner needs a separate reviewed runbook"
  caveat. e2e bumped 30→33 tests for compatible/minimum/version
  assertions.
- Mia cleared 66b0e70c per Grace relay a5330b8d (Mia review
  request ef106835 was delivered via Grace's mail path).
- Hestia drove release chain at 66b0e70c:
  - branch main / tree clean / no existing a2a-gw tag / Docker up /
    CLI_VERSION=1.26.9 (from SERVER_VERSION coupling, #219 debt)
  - make release-a2a-gateway-check: go tests (4 packages green) +
    production Docker build + in-container --check + real-backend
    Docker e2e PASS 33/33 in ~10 min
  - make release-a2a-gateway-tag: a2a-gw-v1.26.9 at 66b0e70c
  - make release-a2a-gateway-push: tag to origin
  - GHA workflow 27129622205 "A2A Gateway Release (GHCR)" SUCCESS
    in 4m19s — multi-arch image at ghcr.io/awebai/a2a-gateway:1.26.9
    + :latest
- Juan created Render Web Service for the image at 15:46 UTC. Image
  pulled clean (no GHCR auth issue). Container started clean. Exit
  status 1 with `open /config/gateway.yam: no such file or directory`
  — Juan's env-var typo (missing trailing `l` on gateway.yaml).
- Typo fixed; second deploy also exit-status-1 with the corrected
  `gateway.yaml` path — expected, because no config or workspace
  was mounted yet.
- Hestia mailed Grace 86e2be87 surfacing the v1 workspace-state
  delivery question: (a) Render Secret Files read-only, (b) Persistent
  Disk + Render Shell seeding, (c) Dockerfile entrypoint tarball
  expansion in a fresh patch release.
- Grace mail 020fc0bc picked (a)-with-tarball: Render Secret Files
  for gateway.yaml + base64 tarball + command-override doing
  `base64 -d | tar -xz` at startup. Validated /bin/sh, base64, tar,
  mkdir present in the 1.26.9 image. Code-checked gateway workspace
  state is read-only at runtime (only writable thing is optional
  audit JSONL).
- Hestia asked two clarifying questions (team-naming + cert-path
  relative/absolute). Grace mail 9765e48a answered: dedicated NEW
  team; cert paths are RELATIVE (SaveTeamCertificateForTeam writes
  `team-certs/<encoded>.pem`; runtime resolves as
  `<workspace_dir>/.aw/<cert_path>`). Tarball: `tar -czf - .aw |
  base64 > gateway-workspace.tgz.b64`. Exclude controller keys +
  human workspace state. Pre-tarball verify: grep `cert_path` is
  relative `team-certs/*.pem`, files exist under `.aw/team-certs/`.
- Hestia gave Juan the 16-step provisioning + Render setup table.
  Asked: (1) is `a2a.aweb.ai` namespace controller-prepared? (2)
  team name? (3) where do you run controller-key bits from?
- Before Juan answered, Grace mail 5bf40922 pivoted: "Stop manual
  A2A tarball deploy; pivot to AC-managed gateway." Reasoning: Juan
  not demoing this endpoint, tarball flow not product-quality, only
  useful as temp manual endpoint, hosted customers should not handle
  .aw workspace state or tarballs.
- Hestia ACK'd Grace 54d52f02; closed #263 as banked-infrastructure /
  manual-lane-abandoned. Grace ACK'd that closure ec961791.

### What's banked (NOT rolled back, per Grace's instruction)

- aweb tag a2a-gw-v1.26.9 at 66b0e70c
- ghcr.io/awebai/a2a-gateway:1.26.9 + :latest multi-arch on GHCR
- Dockerfile.a2a-gw + .github/workflows/a2a-gateway-release.yml +
  Makefile release-a2a-gateway-* lane
- scripts/e2e-a2a-gateway-docker.sh (33-test real-backend Docker
  journey)
- docs/a2a-release-runbook.md with Gateway Identity Provisioning
  section, /health AWID-compatible enforcement, narrow-gate
  caveat, Render-decision-banked
- cli/go/awid/registry_resolver.go DNS-bypass fix (TestRegistryResolverEmbeddedFallbackBypassesDNSForAddress)
- /health emits build.release_tag + build.git_sha + aweb_version +
  awid_service_version (floor) + awid_registry{url,reachable,compatible,
  status,version,minimum_version,error} + gateway diagnostics; flips
  to 503 when !reachable OR !compatible

### What's stopped (NO state change in aweb.ai namespace)

- Identity provisioning for a2a.aweb.ai/gateway — not started
- No `aw id namespace prepare-controller`, no `aw id create`, no
  team create, no controller-signed cert, no `aw init`
- No Render Secret Files uploaded, no command override set
- No per-route AWID publication
- No verified-live mail for a2a.aweb.ai

### Render service state

Juan's Render Web Service at slot `a2a.aweb.ai` is in restart-loop
(exit-status-1 on each restart). Configured with only
AWEB_A2A_GW_CONFIG env, no Secret Files, no command override. Per
Grace, leave suspended/stopped; don't delete (slot + DNS may be
reused when AC-managed gateway needs it).

### Lessons banked (not yet promoted to runbook)

1. **Render Secret Files mount as /etc/secrets/<filename> by
   default, read-only.** Useful for config-and-workspace delivery
   when workspace state is read-only at runtime; insufficient for
   anything that writes (audit logs, cert renewal, local outgoing-
   mail spool).
2. **Workspace tarball + command-override is the right v1 for
   read-only workspace state** without recutting the image — IF
   `sh`, `base64`, `tar`, `mkdir` are present in the runtime
   image. Alpine base provides all four. Pattern: secret-file
   `*.tgz.b64`, Render command override does `base64 -d | tar
   -xz` into `/tmp/...`, then exec the daemon.
3. **Manual workspace-state surgery is not customer-product.**
   Useful for temporary live endpoints (founder-demo), not for
   hosted customers. When a manual deploy lane starts requiring
   per-customer tarball generation, namespace-controller
   coordination, and Render Secret File uploads, the right move
   is control-plane managed (AC owns identity + cert + config +
   deploy).
4. **DNS-resolution intermittently times out from this machine to
   *.onrender.com origins** (api.awid.ai + app.aweb.ai both saw
   ~10s context-deadline-exceeded multiple times this session;
   non-Render destinations like github.com and pypi.org resolved
   fine). Likely Render origin cold-start lag in GCP-us-west1.
   Mitigation: retry with longer timeout.

### Live state at end of session

- AC: v0.5.60 prod, aweb 1.26.8 client, awid_service 0.5.10
- AWID: api.awid.ai version 0.5.11 (Grace deployed mid-session)
- PyPI aweb: 1.26.9 (Grace's A2A wave; self-last-verified 1.26.8)
- npm aw: 1.26.9 (Grace's wave; self-last-verified 1.26.8)
- aweb.ai: Olivia 27f43d4c hero redesign live
- a2a.aweb.ai: NOT live — Render Web Service exists but suspended
- a2a-gw image: GHCR 1.26.9 + :latest, banked

### Tracking

#262 closed (review complete). #263 closed (release chain complete
on the banked-infrastructure side; manual-deploy lane abandoned).


## 2026-06-08 — Olivia 27f43d4c site deploy verified-live (post-A2A train + aapz wave 3)

Session pulled across two day-boundary turns (UTC midnight rolled
between deploy and verify-live closure).

### What landed this turn
- ac main: 27f43d4c (Olivia home hero redesign merge into main) +
  7203f5c2 (sync-public-docs auto-commit from `make deploy-site`)
- ac deploy-landing: origin pushed; CF Pages built Hugo from
  6da746de (Wave-3 baseline) then this wave's commit set; live
  H1 confirms new "Let agents work together in an open network"
- AC backend: untouched. /health still
  `release_tag=v0.5.60 git_sha=2cf21f23 aweb_version=1.26.8
  awid_service_version=0.5.10`.
- Mail: verified-live sent to Sofia (msg bd6704cd). Two ACK copies
  back from Sofia (4678a10a + cf60b390 — bus retry, identical
  content). Olivia not addressable via short alias OR
  `aweb.ai/olivia` (404); past pattern was conversation-thread
  reply via her inbound mail.

### Live-verify evidence (cache-bypass `?nocache=$(date +%s)`)
- Home H1: `<h1 class=hero-title>Let agents work together in an
  open network</h1>` ✓
- Bootstrap URL canonical: `github.com/awebai/aweb-team-coord-worktrees`
- Runtime-toggle DOM: `hero-runtime` class present
- /llms.txt headers: `# Let agents work together in an open
  network` / `## Get started` / `### 1. Install + bootstrap
  (one-time)` / `### 2. Start an agent in each agent home` /
  `### Claude Code` / `### Codex CLI` / `### Pi`
- /orchestration: 5 `aw agents bootstrap ... --username
  --identity-prefix` hits
- /mcp: 1 hit (orchestration teaser)
- /docs/team-bootstrap: 12 `aw agents bootstrap` hits, 0 stale
  `aw team bootstrap`, 0 stale `aw run claude`
- Stale-string sweep across home/orchestration/mcp/team-bootstrap:
  all zero

### Lesson banked (not yet promoted to runbook)
CF Pages Hugo build version (0.124.1 in meta generator) is older
than local (0.160.1 here). After `make deploy-site` push, CF
Pages takes ~30s to rebuild from source. First probe right after
push may show OLD content even with cache-bypass param. Wait 30s
and re-probe. (Already banked policy #10 covers browser-verify;
this adds: CF-rebuild-window applies even to curl probes because
CF builds from deploy-landing source branch, not from pre-rendered
output.)

### A2A release train (Grace's lane, ran in parallel)
Grace took the release lane mid-session after Juan's "drive it
through" mandate when I attempted to gate Step 1 with AskUserQuestion.
- Cut at aweb 81e8d01c: AWID 0.5.11 + aweb server 1.26.9 + aw CLI
  1.26.9 + new aweb-a2a-gw gateway binary
- Grace confirmed AWID 0.5.11 deployed mid-session
- AWID 0.5.11 has additive migration 007_a2a_publications.sql
  (a2a_bridge_delegations + a2a_route_publications tables w/
  indexes) — additive-only, no live-schema break for AC's
  awid-service 0.5.10 client lib
- AC backend untouched: still on aweb 1.26.8 client lib +
  awid-service 0.5.10 (backward-compat with api.awid.ai 0.5.11)
- aweb-a2a-gw live deployment (a2a.aweb.ai/personal +
  /customer-service + /research routes) pending future
  ubuntu-8gb-nbg1-1 SSH-assist provisioning per Grace
- I picked up the marketplace push (d6034672) as transport-only
  task — Athena's instance lacks GitHub creds, mine has them.
  Bundle transport via 19-chunk base64 channel mail; extraction
  from on-disk JSONL transcript (in-memory transcription had
  boundary-whitespace risk).

### Single-release-owner discipline confirmed
Grace owns A2A. Hestia carried Olivia site only. Marketplace push
(d6034672) was a transport favor, not a release co-ownership.
When Grace takes a lane under Juan's "drive it through" mandate,
hands off cleanly — don't double-tag.


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
