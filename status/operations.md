# Operations Status

Last updated: 2026-05-02 22:10 CEST (Hestia, post first-exercise verified-live; ac v0.5.18 + aw CLI 1.18.8 shipped)

## Current focus

**First end-to-end exercise complete.** Athena's bless-and-run
(2026-05-02 ~18:00Z) on the claim-human cli_signup orphan vector
+ BYOD username contract carried through gate-failure-and-recovery
to verified-live: ac v0.5.18 + aw CLI 1.18.8 are now on prod and
npm respectively. Cycle ~80 min including the gate-failure detour
(test-script gap in e2e A.18 → mailed Athena failure shape →
landed 1be46c42 → re-ran ac gates green → tagged + pushed both →
GHA + manual deploy → /health + smoke probe verified).

The runbook is now post-validation. The build/ship boundary is
real at the runtime layer; first-exercise observations folded
into runbook.md (timing baselines, aw CLI version-coupling foot-
gun, gate-failure-by-arm-pattern diagnostic, validated bless-and-
run mail shape).

## Live state (verified 2026-05-02 21:50 UTC)

- `app.aweb.ai/health`: `release_tag=v0.5.18`,
  `aweb_version=1.18.6`, `git_sha=4ace97702077a43e7067f296848145c40204444a`,
  `awid_service_version=0.5.3`. db / redis / awid /
  coordination_api healthy. Started 2026-05-02 19:50 UTC.
- `api.awid.ai/health`: `version=0.5.2`, redis / db / schema
  healthy. Unchanged.
- aweb OSS published tags: `server-v1.18.6`, `aw-v1.18.8`,
  `awid-v0.5.2`, `awid-service-v0.5.3`. Server unchanged at 1.18.6;
  aw CLI bumped 1.18.7 → 1.18.8 today; awid lib bumped to 0.5.3
  yesterday (Mia's earlier release ac62e64).
- npm `@awebai/aw`: 1.18.8 (matches aw CLI tag).
- channel: 1.3.3 published. Unchanged.

## Release pipeline

- **ac v0.5.18 + aw CLI 1.18.8 (2026-05-02): verified-live.**
  Closes claim-human cli_signup orphan vector + BYOD username
  contract per Athena's bless-and-run. Verified-live mail posted
  to athena/sofia/juan with full evidence trail.
- **Open follow-ups in Athena's lane (filed):** aamb, aamc, aama
  (P1 ticket cluster around the same flow), plus A.18a/A.18b
  e2e-script split (architectural-tests follow-up to document
  the managed-vs-BYOD claim-human contract distinction; current
  A.18 passes by mocking the contract via `--username "$ORG_SLUG"`).
- **Going-forward routing (Athena, 2026-05-01) — NOW VALIDATED:**
  Dev team stops at clean-main. Tags + gates + deploys + verify-live
  in Hestia's lane. Flow:
  1. Dev team lands work on main + signals Athena.
  2. Athena runs code-reviewer subagent on gate-input commit.
  3. Athena drafts release notes + mails Hestia bless-and-run.
  4. Hestia runs `make release-ready` (+ compat per criterion) →
     tag → push → watch GHA → signal Juan when image at GHCR.
  5. Juan deploys (manual; Render does not auto-deploy).
  6. Hestia verifies live + posts verified-live mail.
- **Genesis-day pattern (accepted retroactively):** v0.5.13–v0.5.17
  all shipped through Mia's iteration loop. No Hestia gate, no
  verified-live mail. /health was the deployment check.

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

1. Wait for the next bless-and-run mail from Athena.
2. Daily `/health` check on `app.aweb.ai` and `api.awid.ai`.
   Compare to `status/product.md` claims; flag drift.
3. Stale-claim sweep on `aw work active` next wake-up (currently
   clean, so just cadence).
4. Publishing-path timing data (Sofia owed). v0.5.18 baselines:
   - aweb `make ship` gate: 7m6s (anomaly threshold > 10 min).
   - ac `make release-ready` gate: 198s; ac compat: 57s.
   - aweb tag → npm publish: ~3 min (aw Sync and Release on
     awebai/aweb → awebai/aw aw Release → goreleaser + npm).
   - ac tag → image at GHCR: per banked v0.5.16 baseline ~13 min.
     Manual deploy (Juan) variable.
   Worth folding into a proper publishing-path doc; for now lives
   in runbook + this file.
5. Test-suite triage in ac/Makefile (deferred).

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
