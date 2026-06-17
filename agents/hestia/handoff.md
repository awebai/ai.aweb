# Hestia Handoff

Crisp wake-up brief. What I need to act NOW, nothing more. For
backstory on anything referenced here, see `logbook.md`. For
operating discipline, see `AGENTS.md` (the entry point) → the
four-piece kit (`constitution.md`, `architecture.md`, `legacy.md`,
`.claude/skills/sop-*`).

**Last updated:** 2026-06-17 — four-piece kit landed; runbook.md
archived. Most files in this directory are new or rewritten;
trust the kit (not memory) when in doubt.

## In flight

**0) Legacy refactor LANDED today.** Six commits ahead of
origin/main (`df58b0d`..`61c8539`), unpushed pending Juan's
review. The four-piece kit + sop-* skills + AGENTS.md entry-
point. runbook.md archived. Logbook entry 2026-06-17 has the
distribution map.

If Juan says "push": `git push origin main` from
`agents/hestia/`. No tag.

**1) 503 intermittent on awid (Juan-reported earlier today).**
SUSPENDED waiting on three answers from Juan:

- Where does he see the 503? (browser / aw CLI / customer report
  / AC server log)
- What's the body? (Render HTML / Cloudflare HTML / JSON — the
  source layer differs)
- Roughly when? (last hour / last day / specific times)

What I know so far: 70 sequential probes 200, no 503 emitter
anywhere in the awid Python source, so it's infrastructure-layer
(Render edge during pod restart, Cloudflare→origin transient, or
Render plan idle-sleep cold-start). I offered a long-running
silent probe with timestamps + headers; Juan hasn't responded.

**2) a2a-gw-v1.26.19 CLOSED LIVE.** Verified-live mail sent
Sofia 2026-06-13 (msg 3a51587f) with full 4-point check.
aweb-aaqw + aaqx CLOSED via Rose's stock a2a-sdk default-flow
proof.

**3) #288 aaqs P1 (Grace queue, unchanged).** `aw directory
aweb.ai/<alias>` → 404 for all team aliases. AWID has the record
(200); AC's network-directory projection endpoint missing
entirely. Customer-visible. Grace's lane.

**4) #284 P1 (Athena lane, unchanged).** AC migration runner
must run on Render container start OR via deploy hook. Until
then, every AC ship with a new SQL migration needs manual-apply
per `sop-pgdbm-migration-apply`.

**5) aaqv direction halt (Juan).** AC-side A2A route management
surface — Juan said "this is a surface we need to eliminate at
some point." Direction halt, NOT a release halt. Don't restart
route-management code work without Juan/Sofia direction read.

**6) HN pre-check burst capacity (#275)** — Olivia ready, Juan
firing word pending.

**7) HAL-130226 (tomj.aweb.ai) timeouts** — RENDER_API_KEY
blocker. Juan needs to drop into `~/.aweb-ops/render.env`.
Today's a2a-gw Render-flip incident is a second proof of why
direct Render API access matters for ops.

## Open holds (don't trip these)

- **#245 aw 1.26.3 workspace-cleanup regression.** Don't ship a
  CLI release that extends `cli/go/cmd/aw/workspace*` cleanup
  behavior until Athena + Mia decide the fix-forward shape.
- **#239 aw 1.27.0 E2EE-default Phase 2.** Don't tag aw-v1.27.0
  without Grace re-route; gated on channel/Pi adoption.
- **#284 AC-migration-runner-not-wired.** Until closed, any AC
  ship with a new SQL migration needs manual apply between
  GHA-green and Render-flip-live via
  `sop-pgdbm-migration-apply`.
- **aaqv direction halt.** No AC route-management lane work
  without Juan/Sofia direction.

## Live matrix (one line)

AC v0.5.74 prod • aweb PyPI 1.26.19 + aw npm 1.26.19 + GH Release
v1.26.19 (cli DefaultTimeout 30s + team-auth envelope v2) •
a2a-gw GHCR 1.26.19 live at a2a.aweb.ai (d0baafa3) • pi-extension
0.1.21 • awid-service PyPI 0.5.12 + awid GHCR 0.5.12 • aweb.ai
site 30b90815 (/a2a/ live) • channel 1.4.12 • skills 0.2.12.

## Juan-action queue (real-time)

1. **Review legacy-refactor commits** (`df58b0d`..`61c8539`,
   six commits unpushed on main). Push when blessed.
2. **503 disambiguation answers** — where / body / when. Until
   then I can't narrow the infra layer.
3. **RENDER_API_KEY drop** into `~/.aweb-ops/render.env` (blocks
   HAL-130226 + Athena hackathon diagnosis +
   Manual-Deploy-image-pin-bump pattern).
4. **HN pre-check burst firing word** when ready (Olivia
   primary, Hestia analyzes).
5. **aaqv direction read** — confirm AC route-management
   surface elimination scope before Athena/Grace restart any
   related work.

## Wake-up checklist

1. `git pull` in ai.aweb and the sibling repos (aweb, ac).
2. `aw chat pending && aw mail inbox`.
3. `curl -sS https://app.aweb.ai/health` — confirm AC v0.5.74 +
   aweb_version=1.26.18 (NOT 1.26.19; AC pin floor is 1.26.18).
4. `curl -sS https://api.awid.ai/health` — confirm 0.5.12.
5. `curl -sS https://a2a.aweb.ai/health` — confirm
   a2a-gw-v1.26.19 + git_sha=d0baafa3.
6. `aw task list --status pending --owner hestia` — open ops
   follow-ups.

## Where to look

- **`AGENTS.md`** — entry point. Points at the four-piece kit.
  Wake-up routine lives there.
- **`constitution.md`** — identity, mandate, immutable behavior
  rules.
- **`architecture.md`** — ops surfaces map (artifact table,
  deploy lanes, /health endpoints, peer routing, gates, GHA
  workflow names, probes).
- **`legacy.md`** — banked learnings (the inheritance, NOT
  deprecated content). 9 domains; check the relevant section
  before doing something that feels risky.
- **`.claude/skills/sop-*`** — procedures. Three Hestia-owned:
  release-execution-chain, pgdbm-migration-apply,
  destructive-cutover. Plus sibling-repo skills (release-cli,
  release-channel, release-awid-pypi, ship) surfaced via the
  symlinks.
- **`logbook.md`** — historical narrative. 2026-06-17 entry
  carries the legacy-refactor close-out + content distribution
  map; 2026-06-13 entries carry the a2a-gw-v1.26.19 close-out
  + 14-release wave summary + PearX traction delivery.
- **`scripts/`** — reusable read-only DB probes (signups,
  user_activity, multi_agent_active, team_probe).
- **`artifacts/`** — sensitive ops dumps, local-only.
- **`~/.aweb-ops/`** — chmod 600 secrets directory.

## Discipline you'll regret skipping

- **Never ship with failing tests, ever** (`legacy.md`
  release-discipline). Red gate = no ship. "Known flake",
  "matches baseline", "non-regression accept" are NOT
  acceptable framings.
- **Verified-live mails enumerate 4 points** (what fixed / what
  NOT fixed / evidence / live check). Item 2 is the recurring
  slip.
- **Direction halt ≠ release halt.** Disambiguate scope when a
  peer relays an ambiguous "stop this" from Juan.
- **Render Manual Deploy doesn't auto-bump image tags.** Pinned
  services need Settings → Image URL bump → Save. :latest needs
  Clear-cache + Deploy. (`legacy.md` infra-render)
- **Don't hallucinate live state.** Anchor every production
  claim to a `curl` or Render dashboard read.
- **Bare aliases (grace, olivia) fail.** Use full namespace
  form (`juan.aweb.ai/grace`, `juan.aweb.ai/olivia`). Sofia is
  `aweb.ai/sofia`, Athena is `aweb.ai/athena`. Juan is not an
  aweb agent — surface Juan asks in-conversation.
- **Rose inbound-filter**: `juan.aweb.ai/rose` rejects mail
  from me with 403. Route Rose loops through Grace.
- **Push release tags individually**, never batched (banked
  policy #7).
- **Manual migration unblocks MUST use pgdbm normalization** —
  raw file SHA is wrong (`sop-pgdbm-migration-apply` emergency-
  metadata-repair section).
- **`/health`'s coordination_schema check is row-presence-only**,
  not a checksum check.
- **release-verify-migration-immutability is your friend.**
  Trust the gate. Fix the manual path.
- **`aw` cwd-bound identity foot-gun** (`legacy.md` identity-
  discipline): always run `aw` from `agents/hestia/`.
- **Mail body size**: keep verified-live mails terse; multi-
  section >2KB bodies can trip edge blocks (HTTP 403).
- **Route IDs aren't well-known**: A2A gateway routes live at
  `/a2a/agents/<route-id>/agent-card.json` — don't guess for
  verification probes; defer to SDK-canonical proof shape.