# Athena Handoff
Last updated: 2026-05-01 11:30 CEST

## Read this first

You are Athena. You own the code for aweb and ac: architecture,
invariants, review of every diff that lands on main, and non-feature
code you write yourself (diagnostic harnesses, reproducers,
conformance vectors, instrumentation stubs).

**The dispatch shape for feature authoring is being revised.** The
spawn-pair flow described in `AGENTS.md` "How Feature Work Happens"
and in `docs/decisions.md` commit `4491df5` (top entry, 2026-05-01)
was published as the model. On Athena's first wake-up under that
model (also 2026-05-01, second agent online after Sofia), Juan
corrected: "do not worry about spawn. I want you to understand
your job. We will have to talk about how we set you up, because
the actual dev team is in another team."

So: the spawn-pair-via-mail-Juan flow is *not* the authoritative
current setup. The dev team is in a separate cryptographic team
rather than ephemeral pairs spawned in `default:aweb.ai`. Juan
will walk through the real shape. Don't pre-empt by drafting
spawn briefs to mail Juan; don't claim Phase 1 / Phase 2 framing
in chat. Wait for the walk-through, then update memory + AGENTS.md
+ this handoff to match reality.

What's stable about the role:
- Code ownership in aweb + ac (architecture, invariants, cross-repo
  coherence).
- Review of every diff before it lands on main.
- Non-feature code Athena writes directly: diagnostic harnesses
  (e2e-amy-symptom-reproducer.sh class), reproducers, conformance
  vectors, instrumentation stubs.
- Runbook tech-accuracy reviews (Aida-side surfaces).
- Release-notes drafts (Hestia-side handoff).
- Technical content for decision records (Sofia-side framing).

## Live state at 2026-05-01 morning

- `app.aweb.ai/health`: `release_tag=v0.5.12`,
  `aweb_version=1.18.6`, `git_sha=962dd163`,
  `awid_service_version=0.5.1`. db/redis/awid/coordination_api
  healthy. Started 2026-04-30 20:07 UTC.
- `api.awid.ai/health`: `version=0.5.2`. healthy.
- aweb OSS published tags: `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27, no movement).
- channel: 1.3.3.
- ac main is **5 commits past v0.5.12** — coherent v0.5.13
  candidate (admin tooling hardening + auth retired-user safety +
  ship-gate fix). Holding for Hestia gate chain. See
  `status/engineering.md` for per-commit read.

## What happened today (2026-05-01 wake-up)

1. Read team docs, status files, decisions.md (top entry: dispatch
   model commit 4491df5). Updated engineering.md from new
   perspective.
2. Sofia chat: confirmed Phase 2 deferral was the right call (she
   pushed for it; agreed because today's bottleneck is distribution
   not throughput). Sofia flagged the auth-path commit
   `5818095d` as a code-reviewer-subagent-before-ship target —
   yes, will run that as part of v0.5.13 prep.
3. Juan corrected: drop the spawn thread; actual dev team is in
   another cryptographic team. Setup walk-through pending.
4. YC agent (first wake-up, separate team): five-question fact-check
   on technical positioning claims for YC application. Grounded
   each in code. Pushed back on "locks are repo-scoped" (wrong)
   and "rotation log verifiable without trusting the registry"
   (overclaim — chain holds, transparency does not). Mailed Q5
   production-scale numbers. YC closed exchange satisfied; will
   re-engage when draft answer touches code, with a request to
   time `aw init` on a fresh container before publishing the
   five-minute claim externally.

## Production scale snapshot (queried 2026-05-01 morning)

AWID registry: 91 did_aw_mappings, 57 dns_namespaces, 45 teams,
33 public_addresses, 3 team_certificates.

Cloud: 44 active users (46 inc soft-deleted), 53 organizations,
46 managed_namespaces, 12 team_members rows, 0 oss_public_teams,
8 active sessions, 155 cloud_agent_certificates,
178 cloud_workspace_metadata.

Honest framing: dogfooding scale; distribution begins this week.

## Pending artifacts owed (Athena side)

1. **KI#1 closure decision record technical content.** Sofia
   drafts framing; supply cert-presentation auth correction +
   aalk continuity arc + 1.18.6 trust-model arc + Aida 4/4
   attestation. Source: `aale-trust-contract.md` in this dir +
   aweb commit `7759abc`.
2. **Code-reviewer subagent pass** on the v0.5.13 5-commit cluster
   (962dd163, cf49c282, 0e0f73a6, 37762328, 5818095d). Per
   policy 13.
3. **Aida runbook PR tech-accuracy review.** Mentioned in earlier
   handoff but inbox is empty; verify state with Aida when she
   comes online.
4. **Time `aw init` on a fresh container** before YC publishes
   the five-minute claim externally. Not blocking now; YC asked
   to coordinate when the draft is closer to publish.

## Standing release-discipline policies (banked through 2026-04-26)

Hestia enforces these at gate-time. They hold under any dispatch
shape.

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
12. Reproducer-as-gate
13. Code-reviewer subagent for gate-input commits (Athena runs
    before signaling Hestia)

## Architectural context worth not losing

- **Server is data substrate; verification is client-side.** The
  trust-contract design space is two clients (Go + TS), not three.
- **Cert-presentation + signature + non-revocation is the auth
  predicate.** The 1.18.6 architectural correction (commit
  `7759abc`, 922 lines) replaced row-existence-as-authorization.
  AWID is no longer a membership oracle. Don't reintroduce that
  pattern.
- **Single consolidated migration files mean every additive change
  goes in a NEW ordered file.** Editing existing 001 in place
  trips pgdbm's checksum guard and forces a destructive cutover.
- **Reproducer-as-gate works.** The
  `e2e-amy-symptom-reproducer.sh` pattern from KI#1 is the model
  for any future symptom-driven closure.
- **Locks are team-scoped reservations on opaque resource keys, not
  repo-scoped or file-system locks.** Convention to use file paths
  is convention. (Calibrated during YC fact-check 2026-05-01.)
- **Rotation log: chain self-verifies; full transparency on
  roadmap.** Don't claim "verifiable without trusting the registry"
  flat — split-brain is theoretically possible until transparency
  lands.

## Working docs in this dir

- `aale-trust-contract.md`: working doc from the 2026-04-26
  architecture pivot. Promote to `aweb/docs/` once ratified.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (OSS: server, CLI, awid, channel)
- `ac` → `../../../ac` (cloud)
- `awid` → `../../../aweb/awid`

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run `aw`
from sibling repos.

## What to check FIRST on next wake-up

1. Whether Juan walked through the dispatch / dev-team setup. If
   yes, update memory `project_athena_dispatch_model.md`,
   `AGENTS.md`, and this handoff to match reality.
2. `aw mail inbox` — including any YC follow-up, Sofia chat
   reply, Aida runbook PR status.
3. `aw work active` — pick up anything claimed.
4. Hestia state: did her runbook land? Is identity setup done?
   Did v0.5.13 candidate move?
5. Status/operations.md and status/product.md for new entries
   since 2026-05-01.
