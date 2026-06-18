# Hestia Architecture

The ops surfaces I operate on. NOT code architecture — Athena owns
that (see `aweb/docs/` SOT files for code-side architecture). This
file is the map of what I touch when I carry a release and when I
verify live state.

## Artifact map

Six distinct artifacts ship from two repos through five distribution
channels.

### aweb repo

| Artifact | Tag pattern | Distribution | Pinned by |
|---|---|---|---|
| aweb server (Python) | `server-vX.Y.Z` | PyPI `aweb` | ac (`aweb>=…`) |
| aw CLI (Go) | `aw-vX.Y.Z` | GitHub Releases (goreleaser) + npm `@awebai/aw` | end-users |
| awid lib (Python) | `awid-service-vX.Y.Z` | PyPI `awid` | ac (`awid-service>=…`) |
| awid registry (Docker) | `awid-vX.Y.Z` | GHCR; Juan deploys manually; runs at `api.awid.ai` | (independent service) |
| @awebai/claude-channel (TS) | `channel-vX.Y.Z` | npm | end-users (Claude Code) |
| a2a-gateway (Docker) | `a2a-gw-vX.Y.Z` | GHCR; Juan deploys manually; runs at `a2a.aweb.ai` | (independent service) |

The version field shared between `awid-vX.Y.Z` and
`awid-service-vX.Y.Z` points at the same `aweb/awid/pyproject.toml` —
single source code, two distribution channels (Docker image + PyPI
library).

### ac repo

| Artifact | Tag pattern | Distribution | Live at |
|---|---|---|---|
| aweb-cloud (Docker) | `vX.Y.Z` | GHCR; Juan deploys manually from GHCR | `app.aweb.ai` |
| aweb.ai site (Hugo) | `make deploy-site` from ac | Render Static Site | `aweb.ai` |

ac pins `aweb` and `awid-service` in `backend/pyproject.toml`.

### Release-as-needed, not lockstep

Per Juan: artifacts ship as needed, not always together.

- **aweb server bump usually drags ac.** When the server changes
  contract or behavior that ac depends on, ac picks up the new pin
  in a follow-on release.
- **awid tends to be more independent.** Both the Docker image and
  the PyPI lib can move on their own cadence unless ac needs the
  new client features.
- **aw CLI often moves in lockstep with aweb server** but isn't
  required to. The `release-all-tag` Makefile target cuts
  server + aw + channel + awid + awid-service from the same commit;
  that target exists for the all-together case, not as the default.

Which artifacts move and in what order is in Athena's bless-and-run
mail per release. I don't self-spawn a release on a bump commit
sitting on main — that would skip the build/ship boundary.

## Deploy lanes

```
                       ┌─ GHA: server-release.yml ─→ PyPI: aweb
                       │
aweb repo  ─tag-push─┤├─ GHA: aw-release.yml ───→ GH Releases + npm @awebai/aw
                       │
                       ├─ GHA: awid-pypi-release.yml ─→ PyPI: awid
                       │
                       ├─ GHA: awid-release.yml ──→ GHCR awid ──[Juan]──→ api.awid.ai
                       │
                       ├─ GHA: channel-release.yml → npm @awebai/claude-channel
                       │
                       └─ GHA: a2a-gateway-release.yml → GHCR a2a-gateway
                                                          ↓
                                                       [Juan: Render
                                                        Settings →
                                                        Image URL pin
                                                        bump → Save]
                                                          ↓
                                                       a2a.aweb.ai

ac repo  ──tag-push──→ GHA: cloud-cicd.yml ──→ GHCR aweb-cloud ──[Juan]──→ app.aweb.ai
                       │
make deploy-site  ───→ Render Static Site (aweb.ai)
```

**Docker-image deploys are MANUAL.** Render does NOT auto-deploy
from GHCR for ac, awid, or a2a-gateway. When the GHA build
completes and the image is at GHCR, I signal Juan and wait. Image-
pinned services need explicit Image URL bump in Render Settings;
Manual Deploy alone re-deploys the existing pin (see `legacy.md`
infra-render).

**PyPI / npm / GitHub Releases publishes don't have a manual deploy
step.** Once GHA finishes the publish workflow, the artifact is
"live" in the sense of available to consumers. The remaining wait
is PyPI/npm propagation.

## Live-state endpoints

| Surface | Endpoint | What to assert |
|---|---|---|
| aweb-cloud | `https://app.aweb.ai/health` | `release_tag` matches just-pushed ac tag; `git_sha` matches bump commit; `aweb_version` and `awid_service_version` match `backend/pyproject.toml` pins |
| awid registry | `https://api.awid.ai/health` | `version` matches `awid-vX.Y.Z`; `checks.redis: ok`; `checks.database: ok` |
| a2a-gateway | `https://a2a.aweb.ai/health` | `release_tag` matches `a2a-gw-vX.Y.Z`; `git_sha`; `aweb_version` pin |
| pi-extension runner | `https://pi.aweb.ai/health` (when applicable) | version + uptime |
| aweb.ai site | `curl -sI https://aweb.ai/` | `last-modified` matches deploy time |

`/health` returning 200 with the expected `release_tag` IS what
"verified-live" means. GHA-green is not.

### Verified-live probe pattern (compact reference)

| Surface | Deploy step | Live check | Smoke probe |
|---|---|---|---|
| ac (cloud) | Juan manual | `app.aweb.ai/health` `release_tag` + `git_sha` match | curl changed endpoint or browser-probe the UI |
| awid registry | Juan manual | `api.awid.ai/health` `version` matches `awid-vX.Y.Z` | endpoint smoke against `api.awid.ai` |
| a2a-gateway | Juan manual (Image URL pin bump) | `a2a.aweb.ai/health` `release_tag` matches `a2a-gw-vX.Y.Z` | stock a2a-sdk default-flow proof against the gateway |
| aweb server (PyPI) | none (GHA publishes) | check on PyPI per-version JSON | `pip install aweb==X.Y.Z` + import smoke |
| awid lib (PyPI) | none (GHA publishes) | check on PyPI per-version JSON | `pip install awid==X.Y.Z` + import smoke |
| aw CLI | none (GHA publishes) | check on GH Releases + npm | `aw --version` + smoke command |
| @awebai/claude-channel | none (GHA publishes) | `npm view @awebai/claude-channel version` | `npm install` smoke |
| aweb.ai site | `make deploy-site` from ac | curl `aweb.ai/` `last-modified` matches deploy time | curl all checklist URLs + standing policy #14 address-resolves-and-responds probe for any new customer-paste address + 404-probe any path REMOVED in this deploy |

## Peer routing

| To | When | How |
|---|---|---|
| Athena | Release-handoff received, gate-failure collaboration, live-state drift | `aw mail send --to athena` (= `aweb.ai/athena`) |
| Sofia | Pre-tag framing review, /health drift vs claims, ops discrepancies affecting direction | `aw mail send --to sofia` (= `aweb.ai/sofia`) |
| Iris | Released artifacts ready for external claim | `aw mail send --to iris` |
| Aida | Live-state changes affecting support runbook | `aw mail send --to aida` |
| Grace | Code-side bugs surfaced by /health drift; AWID-side resolution; routing fixes | `aw mail send --to juan.aweb.ai/grace` |
| Mia | AC-side reviewer; gate-config questions | `aw mail send --to juan.aweb.ai/mia` |
| Olivia | Olivia owns site copy + skills repo; reach via `juan.aweb.ai/olivia` (alias `olivia` and `aweb.ai/olivia` both 404) | `aw mail send --to juan.aweb.ai/olivia` |
| Bertha (Eugenie's agent) | Daily signup batch (via skill); ad-hoc traction asks | `aw mail send --to bertha` (= `aweb.ai/bertha`) |
| Juan | Production incidents, RENDER_API_KEY blocker, direction-halt clarifications | Surface in active conversation; `aw mail send --to juan` and `juan.aweb.ai/juan` both fail (he's not an agent) |
| Eugenie | When a release is verified-live and ready for distribution | `aw mail send --to eugenie` |
| Rose | Inbound mail filter rejects me with 403; route through Grace | `aw mail send --to juan.aweb.ai/grace` (relay) |

## Repo layout (sibling-symlink convention)

Sibling repos live as siblings in one parent directory
(`/Users/juanre/prj/awebai/`):

| Repo | Sibling path | Symlinked at | Purpose |
|---|---|---|---|
| ai.aweb | `../ai.aweb/` | (this repo) | Agent team, docs, publishing |
| co.aweb | `../co.aweb/` | not linked | Outreach contacts, keys, competitive intel |
| aweb | `../../../aweb/` | `agents/hestia/aweb` | OSS: server, CLI, awid, channel, docs |
| ac | `../../../ac/` | `agents/hestia/ac` | Cloud: auth, billing, dashboard, SaaS |

Symlinks keep CWD anchored in `agents/hestia/` so `aw` commands use
my own workspace identity. Do NOT run `aw` from sibling repos —
that uses a different workspace identity.

Prefer `git -C aweb log` over `cd aweb && git log` for the same
reason.

## Gates (release-ready chains)

### ac

```sh
cd ac && make release-ready
```

**Composes ONLY the 4 verify-* targets** (deploy-safety, not
test-correctness):

- `release-verify-remote` — confirms remote state matches expectation
- `release-verify-model` — model-side verification
- `release-verify-migrations` — migrations are forward-only, ordered,
  checksum-clean
- `release-verify-migration-immutability` — pgdbm-normalized checksum
  of every migration on disk == `schema_migrations.checksum`
  (catches manual-unblock checksum drift, see `legacy.md`
  migration-discipline)

**It does NOT include** `test-backend`, `test-frontend`,
`test-two-service`, or `test-cloud-user-journeys`. Those run via PR
CI before merge to main — the release-time gate is deploy-safety.
Main is presumed clean.

Separate targets (run when scope requires):

- `test-cloud-user-journeys-compat` — installed-aw arm; run explicitly
  when release risks breaking installed users. ~58s isolated. See
  trigger conditions in `sop-release-execution-chain`.

`make release-ready` baseline: ~3–5 min.

**ac GHA on a `v*` tag ONLY builds + pushes the GHCR image.** It runs
NO tests, NO e2e. So local `make release-ready` from main is THE
quality gate at release time.

### aweb

```sh
cd aweb && make ship
```

`make ship` is the canonical comprehensive pre-tag-push gate.
Composes:

- `make test` — `test-server` + `test-awid` + `test-cli` + `test-channel`
- `make release-server-check` — server build + tests + dist artifacts
- `make release-channel-check` — channel test + build + npm pack
  dry-run + plugin-version match
- `make release-awid-check` — awid lock + tests + build + Docker
  build verification
- `make test-e2e` — full e2e user journey (no release cut without
  this green)

End-to-end baseline: ~7 min. `make ship` does NOT push — it prints
"Ready for tag-push" at the end. Tag-push is always the explicit
per-component sequence.

Per-component targets:

- `release-server-check` / `-tag` / `-push`
- `release-cli-tag` / `-push`
- `release-awid-check` / `-tag` / `-push` / `-pypi-tag` / `-pypi-push`
- `release-channel-check` / `-tag` / `-push`

## GHA workflow names (for `gh run` watching)

| Trigger | Workflow | Repo |
|---|---|---|
| `server-vX.Y.Z` push | "Server Release (PyPI)" | awebai/aweb |
| `aw-vX.Y.Z` push | "aw Sync and Release" (then triggers "aw Release" on awebai/aw) | awebai/aweb, awebai/aw |
| `awid-vX.Y.Z` push | "Deploy AWID" or similar (GHCR) | awebai/aweb |
| `awid-service-vX.Y.Z` push | "AWID PyPI Release" | awebai/aweb |
| `channel-vX.Y.Z` push | "Channel Release" | awebai/aweb |
| `a2a-gw-vX.Y.Z` push | "A2A Gateway Release" | awebai/aweb |
| `vX.Y.Z` push on ac | "Cloud CI/CD" | awebai/ac |

Use `gh run list --repo awebai/aweb --limit 5` to watch. **Confirm
the workflow fired** — batched same-commit tag pushes silently
coalesce and no workflow fires (see `legacy.md` infra-github).

## Operational hygiene surfaces

What I check on every wake-up beyond live-state probes.

| Surface | Command | What to look for |
|---|---|---|
| Active claims | `aw work active` | Stale (>24h) claims with no progress |
| Blocked tasks | `aw work blocked` | Anything routed to me; route to owner if not |
| Workspace status | `aw workspace status` | Who's online, what's claimed |
| Status file currency | `ls -la ../../status/*.md` | Files older than expected cadence (engineering+ops should refresh per release; weekly per week) |
| Scheduled agents | (cron / CronList) | Agents that should have woken up but didn't |
| Version drift | `/health` vs `status/` files vs CLAUDE.md live-matrix line | If they disagree, status file is wrong (live state is authoritative) |
| Dashboard hygiene | `../../docs/company-dashboard.md` | Signal inventory current; broken queries flagged |

Loop: check → discrepancy → routed task or mail to owner → recheck
next wake-up.

## Reusable probes (under `scripts/`)

| Script | Answers | Triggered by |
|---|---|---|
| `signups.py --days N` | "how many sign-ups in last N days? CLI vs browser? who?" | Bertha outreach, Juan funnel reads |
| `user_activity.py --email <e>` | "is user X active since signup? agents/messages/last-seen?" | Bertha pre-outreach context, support triage |
| `multi_agent_active.py --days N` | "is anyone actually using aweb multi-agent? who?" | Juan product reads, Metis signal |
| `team_probe.py --team <id>` | "what's the state of team X? agents/workspaces/messages/deletes" | "agent not connected" triage, BYOT audit |
| `cutover_schema_equivalence.sh` | "are two consolidated migration chains schema-equivalent?" | Pre-cutover review with Athena (see `sop-destructive-cutover`) |

Invoke with `uv run --with asyncpg python scripts/<name>.py [args]`
from this dir. DATABASE_URL resolves from `$DATABASE_URL` or
`../../../ac/.env.production`.

When a question shape repeats more than twice, add a new script
following the pattern in `scripts/README.md` and update this table.

## Standing constraints

- **PII discipline**: internal team only. Don't paste raw probe
  output to external surfaces. Bertha mail with emails is
  by-design authorized via `daily-signup-export` skill.
- **artifacts/ stays local-only.** Sensitive ops dumps; PII-clean
  writeups only land in commits.
- **`~/.aweb-ops/`** is chmod 600. Render API key drops there
  (`render.env`); never pasted in chat.
- **`.aw/signing.key` changes** never commit without a reason.
