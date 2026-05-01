# Operations Status

Last updated: 2026-05-01 23:55 CEST (Hestia, first wake-up under live identity; v0.5.17 retroactive exercise called off)

## Current focus

Hestia identity went live tonight (2026-05-01 21:05 UTC); inbox and
workspace are now real. Today is **team-genesis day** — Sofia,
Athena, YC agent online on the company team; Mia online in the dev
team and shipped five ac releases (v0.5.13–v0.5.17) chasing the
hosted Add-Existing-Identity flow. Those five shipped without me
because the runtime layer for me was not yet up. Accept retroactively
per Sofia + Juan; the build/ship boundary becomes real on the **next**
ac release.

**Tonight's substantive actions, after Juan's late call:**

1. Seeded `runbook.md` with prior-knowledge encoding. Marked
   explicitly as not-yet-validated by Hestia running the chain solo;
   validation comes from the first end-to-end exercise on the next
   real candidate.
2. Status + handoff refresh.
3. v0.5.17 retroactive exercise was kicked off (Athena's
   bless-and-run, ~21:15Z), then **called off by Juan** at ~22:00Z
   — v0.5.17 is shipping without my retroactive verification.
   Background `make release-ready` terminated. The first real
   exercise comes on the next bless-and-run mail from Athena.

## Live state (verified 2026-05-01 23:00 CEST)

- `app.aweb.ai/health`: `release_tag=v0.5.16`,
  `aweb_version=1.18.6`, `git_sha=842e0b5b`,
  `awid_service_version=0.5.3`. db / redis / awid /
  coordination_api healthy. Started 2026-05-01 20:45 UTC.
- `api.awid.ai/health`: `version=0.5.2`, redis / db / schema
  healthy. Unchanged from prior wake-up.
- aweb OSS published tags: `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2`. Unchanged.
- channel: 1.3.3 published. Unchanged.
- awid library inside cloud bumped 0.5.1 → 0.5.3 across today's
  cluster.

## Release pipeline

- **v0.5.17**: tagged on origin (`b6c6e088` annotated → commit
  `9c1038ad`, authored by Mia 2026-05-01 22:55 CEST). Layout-
  containment fix in `AgentsPage.tsx` (modal contains the long
  fetch-cert command list). At 23:55 CEST `app.aweb.ai/health` still
  reports v0.5.16; GHA "Build Release Image" was running 27+ min
  vs v0.5.16's 13 min when last checked. Per Juan, v0.5.17 ships
  on its own — no Hestia retroactive gate-run, no verified-live
  mail from me on this one.
- **Going-forward routing decision (Athena, 2026-05-01).** Dev team
  stops at "branch ready / clean main." They do NOT tag. Tags +
  gates + deploys + verify-live all in Hestia's lane from the next
  candidate forward. Athena will brief Mia on the new flow
  separately.
- **Athena's flow going forward:**
  1. Dev team lands work on main + signals Athena.
  2. Athena runs code-reviewer subagent on gate-input commit
     (banked policy 13).
  3. Athena drafts release notes + mails Hestia bless-and-run.
  4. Hestia runs `make release-ready` → tag → push → wait for
     image → verify live.
  5. Hestia posts verified-live mail with evidence.
- **Genesis-day pattern (accepted retroactively):** v0.5.13–v0.5.17
  all shipped through Mia's iteration loop on the same feature. No
  Hestia gate, no verified-live mail. /health was used as the
  authoritative deployment check by Sofia and Athena.

## Iteration-loop cost flag (Sofia mail, 2026-05-01)

Today's 4 ac releases on one feature cost ~2 hours of pure
publish-loop wait (30+ min publishing × 4 cycles), driven by the
absence of a local end-to-end reproducer for the
Add-Existing-Identity surface. Production became the test bench.
The framing is operations-shaped (iteration cost) but the fix is
engineering-shaped (build the local reproducer / Playwright-MCP
harness). Lane: I advocate the cost; Athena decides whether and
how to invest. Concrete next-cycle items I own:

- Time the publishing path (GHA workflow log breakdown — 30+ min
  composed of what?).
- Test-suite triage in `ac/Makefile` — which targets compose to
  the 20-min run, which are critical-path for UI-only changes.
  Bring data; engineering decides what to keep / split / make
  optional.

Banked Sofia routing rule: bug-fix releases tag through my gate
chain by default. Mail Sofia before tag only if the release carries
external-claim weight (new public capability, customer-visible
behavior change, anything affecting value-prop framing). Otherwise
she reads /health when I post verified-live.

## Operational discrepancies

- **Ops runbook missing.** Seeding tonight with prior-knowledge
  encoding from decisions.md + Makefile survey; flagged as
  not-yet-validated.
- **Local reproducer for Add-Existing-Identity.** Per Sofia, the
  surface has no local end-to-end test. Awaiting Athena's read on
  what exists (full / partial / nothing) and what scoping the work
  needs.
- **GitHub author attribution quirk.** Commits authored by dev-team
  members (Mia et al.) show "Juan Reyero" in `git log`. The actual
  agent identity is carried via the aweb cert, not git config.
  Bear this in mind when reading commit history; cross-check with
  Athena who can route to the actual author.
- **Stale repo-manager dirs on disk**: `agents/coord-cloud/` and
  `agents/repo-aweb/` remain untracked from the pre-narrowed model.
  Tracked by `aweb-aals.5`. Low-priority hygiene.
- **Dashboard implementation**: signal inventory exists in
  `docs/company-dashboard.md`; no concrete dashboard or report yet.
  Next step pending.
- **`aw` task metadata native fields**: builder/reviewer/feedback
  fields still parsed from prose `Work contract:` block. Tracked
  by `aweb-aals.7`.

## Active claims

`aw work active`: zero rows. `aw work blocked`: zero rows. Clean
slate.

## Workspace status (company team, default:aweb.ai)

- hestia (me): online, just came up, no claims/locks.
- athena: online (seen 4s ago at survey time), no claims/locks.
- sofia: online (seen 5s ago), no claims/locks.
- yc: online in co.aweb (separate repo).
- cowork-z3dflikwduph, juan-reyero: offline.

Dev team (`aweb:juan.aweb.ai`) members not visible from my
workspace — Athena is the cross-team bridge.

## Next checks

1. Wait for the next bless-and-run mail from Athena. That's the
   first real end-to-end exercise — gate chain, tag, push, watch
   CI/CD, verify live, post evidence.
2. Daily `/health` check on `app.aweb.ai` and `api.awid.ai`.
   Compare to `status/product.md` claims; flag drift.
3. Stale-claim sweep on `aw work active` next wake-up (currently
   clean, so just cadence).
4. Time the publishing path on the next ac release (GHA log
   breakdown). Bring numbers, not hand-waving. Pre-seed the data
   from v0.5.16 (13m GHA + 7m Render = 20m tag-to-live) and
   v0.5.17 (GHA 27+ min so far — slower than v0.5.16, worth
   investigating why).
5. Test-suite triage in ac/Makefile — which targets compose to the
   ~20-min cost.

## Standing release-discipline (banked through 2026-04-26, Hestia enforces)

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate (surface-agnostic; today's Add-Existing
    iteration cost was missing local-loop infrastructure, not
    policy silence)
13. Code-reviewer subagent for gate-input commits (Athena runs
    before signaling Hestia)

`status/weekly.md` continues as a roll-up until replaced by a
proper dashboard.
