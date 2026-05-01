# Athena Handoff
Last updated: 2026-05-01 23:20 CEST

## Read this first

You are Athena. You own the code for aweb and ac: architecture,
invariants, review of every diff that lands on main, and
non-feature code you write yourself (diagnostic harnesses,
reproducers, conformance vectors, instrumentation stubs).

**You belong to TWO cryptographic teams.** This is the load-
bearing setup. AGENTS.md leads with it; re-read on every
wake-up.

| Team | Visibility | Members | Purpose |
|------|------------|---------|---------|
| `default:aweb.ai` | PRIVATE — company | Sofia, Hestia, Aida, Iris, Metis, you | Direction, decisions, status, release framing, support, distribution |
| `aweb:juan.aweb.ai` | PUBLIC — dev | mia, noah, grace, kate, you | Code authoring on aweb and ac |

You are the only role with feet in both teams. Default active
team is `aweb:juan.aweb.ai` (dev); use `--team default:aweb.ai`
for coordinator chats. Three movement patterns:
`aw chat --team <id> ...` (per-command), `aw id team switch
<id>` (session default), `aw id team list` (memberships).

## Live state at 2026-05-01 23:20 CEST

- `app.aweb.ai/health`: `release_tag=v0.5.16`,
  `aweb_version=1.18.6`, `git_sha=842e0b5b`,
  `awid_service_version=0.5.3`. Started 2026-05-01 20:45:10 UTC.
  v0.5.17 (commit `9c1038ad`) tagged and image building; expect
  Render to roll forward 20-90min after tag push.
- `api.awid.ai/health`: `version=0.5.2`, healthy.
- aweb OSS published tags: `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27, no movement).
- channel: 1.3.3.

## What happened today (2026-05-01)

- **Wake-up:** read team docs, status, decisions; landed initial
  engineering.md update.
- **Sofia chat:** confirmed Phase 2 (`aw spawn-pair` primitive)
  deferral. She accepted my read; we agreed today's bottleneck
  is distribution not throughput.
- **Juan corrected the spawn-pair framing:** the actual dev team
  is in `aweb:juan.aweb.ai`, persistent agents (mia, noah, grace,
  kate). The published spawn-pair-via-mail-Juan flow was
  speculative and is now superseded.
- **YC agent (separate team) fact-check:** five-question
  technical positioning review for YC application. Pushed back
  on locks-are-repo-scoped (wrong) and rotation-log-verifiable-
  without-trusting-the-registry (overclaim — chain holds,
  transparency does not). Mailed Q5 production scale numbers (91
  AWID identities, 44 cloud users — dogfooding scale).
- **Two-team setup:** Juan added me to `aweb:juan.aweb.ai`. I
  verified bidirectional cross-team chat (test ping to Sofia via
  `--team default:aweb.ai`). Confirmed `aw id team switch` is
  the canonical default-team command.
- **AGENTS.md rewritten:** leads with the two-team-bridge
  section. Spawn-pair framing removed throughout. Communication
  table now shows `--team` flags. Commit `937e248`.
- **Hestia first wake-up:** asked three real questions on v0.5.17
  (routing, code-reviewer pass, local reproducer). Routing
  decision made: dev team stops tagging from here on; Hestia
  owns gate+tag+deploy+verify going-forward. v0.5.17 already
  tagged by Mia; Hestia running `make release-ready`
  retroactively as runbook-seed exercise tonight. Mia briefed,
  Sofia aligned.
- **Mia chat (juan.aweb.ai team):** clean handoff on aalr.2
  (starts tomorrow morning, persist-refactor first); aaly.6
  closure context (Grace's commit `20419936`); confirmed v0.5.17
  is on origin (Render lag explanation).
- **Code-reviewer subagent on `937f37b0`:** ran successfully.
  Two real findings — test assertion at AgentsPage.test.tsx:181
  is fragile against `--aweb-url` regression; `whitespace-pre`
  on `<pre>` is dead weight. Forwarded to Mia (mail 4dfa7f75).
  Gap closes at e2e level via the upcoming Playwright
  reproducer.
- **Engineering.md resynced** to current state (commit `0a91d8f`).

## Active engineering surface

`aw work active` — Mia is on aalr.2 (starts tomorrow morning).
aalz (no-mocks-of-internals) is her parallel P1; my Add-Existing
Playwright reproducer lands inside aalz scope as the concrete
first deliverable.

## Pending artifacts owed (Athena side)

1. **Playwright-MCP reproducer for Add-Existing dialog** — my
   non-feature-code authoring. Lands as
   `ac/frontend/e2e/add-existing.spec.ts`, wired into
   `make test-cloud-user-journeys`. Targets in
   `status/engineering.md`. Tomorrow morning fresh-headed.
2. **KI#1 closure technical content for Sofia's decision
   record.** Sofia drafts framing; I supply cert-presentation
   auth correction + aalk continuity arc + 1.18.6 trust-model
   arc + Aida 4/4 attestation. Source: `aale-trust-contract.md`
   in this dir + aweb commit `7759abc`. Pending Sofia framing
   draft.
3. **aalr.2 review** when Mia signals branch-ready (tomorrow).
4. **YC fresh-container `aw init` timing** before they publish
   the five-minute claim externally. Not blocking; YC will
   re-engage when their draft answer is closer to publish.

## Standing tasks via `aw task`

- Task #2: Author Playwright-MCP reproducer (pending).
- Task #3: KI#1 closure technical content (pending Sofia
  framing).
- Task #5: Review aalr.2 (pending Mia signal).
- (#1, #4 completed today.)

## Standing release-discipline (banked through 2026-04-26)

Hestia enforces these at gate-time. They hold under any
dispatch shape.

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree (not chat-pasted diffs)
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate (Add-Existing Playwright spec is the
    next instance — covers the iteration-cost class)
13. Code-reviewer subagent for gate-input commits BEFORE
    bless-and-run mail to Hestia (canonical handoff step now)

## Architectural context worth not losing

- **Server is data substrate; verification is client-side.** The
  trust-contract design space is two clients (Go + TS), not
  three.
- **Cert-presentation + signature + non-revocation is the auth
  predicate.** The 1.18.6 architectural correction (commit
  `7759abc`, 922 lines) replaced row-existence-as-authorization.
  AWID is no longer a membership oracle.
- **Single consolidated migration files mean every additive
  change goes in a NEW ordered file.** Editing existing 001 in
  place trips pgdbm's checksum guard.
- **Reproducer-as-gate works.** The
  `e2e-amy-symptom-reproducer.sh` pattern is the model.
- **Locks are team-scoped reservations on opaque resource keys**,
  not repo-scoped or filesystem locks. Convention to use file
  paths is convention.
- **Rotation log: chain self-verifies; full transparency on
  roadmap.** Don't claim "verifiable without trusting the
  registry" flat — split-brain is theoretically possible until
  transparency lands.
- **Cross-system deadlock framing** is why aalr.2 persist-
  refactor is non-optional even after John's ensure-team
  endpoint cuts the round-trip count. Keep AWID I/O strictly
  outside open transactions.

## Working docs in this dir

- `aale-trust-contract.md`: working doc from the 2026-04-26
  architecture pivot. Source for KI#1 technical content.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb`
- `ac` → `../../../ac`
- `awid` → `../../../aweb/awid`

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos.

## What to check FIRST on next wake-up

1. `aw id team list` — confirm both team memberships still
   active.
2. Both teams' inbox + chat:
   ```bash
   aw chat pending; aw mail inbox
   aw chat --team default:aweb.ai pending
   aw mail --team default:aweb.ai inbox
   ```
3. Did Render roll forward to v0.5.17? Cross-check
   `app.aweb.ai/health`.
4. Hestia's runbook-seed exercise output (her runbook draft +
   verified-live mail).
5. Mia's aalr.2 branch-ready signal.
6. `aw task list` — open tasks (#2 reproducer, #3 KI#1 content,
   #5 aalr.2 review).
7. Sofia's KI#1 framing draft.
