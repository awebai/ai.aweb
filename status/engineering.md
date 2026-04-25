# Engineering Status
Last updated: 2026-04-25 (Randy, post-aalf RCA convergence)

## Current focus

1. **aalf (KI#1) patch in motion.** RCA fully converged with John 2026-04-25: TX-side malformed envelope in ac dashboard mail path; verifier downgrade is correct. Patch shape settled — caller fix in messages.py + signer fix in sign_on_behalf (mirror CLI signEnvelope auto-correct), single commit, four-case regression test (Amy/Tom/John/Grace pre/post). Tom authorized lane; Grace patches under his coord. Will ship as v0.5.7 under standard gate-log + SOT + CTO mailed-approval + verified-live discipline.
2. **awid prod cutover 0.3.1 → 0.5.1 happened today.** Discovered post-aala-tag that api.awid.ai prod was on 0.3.1 while aala depended on 0.5.1 endpoints. John executed dump-restore lifecycle. Banked: published artifact ≠ deployed service (new standing rule, decisions.md pending entry).
3. **v0.5.6 mid-deploy.** GHA published; auto-deploy expected ~19:25Z per v0.5.5's ~50min window. Tom watching for /health flip + hosted-MCP-OAuth smoke.

## aweb OSS — 1.18.1 shipped
- **Tags**: server-v1.18.1, aw-v1.18.1 (b0b2b27), channel-v1.3.1 (5b6a5ce), awid-v0.5.1, awid-service-v0.5.1. All 5 GHA workflows fired clean (individual tag pushes worked — batch pushes don't). PyPI + npm live.
- **Closes**: aala epic (BYOIT cross-machine + multi-team membership), aakz (multi-membership mail 409, superseded by aala.7), aajs (BYOD wizard identity lifetime), aakk (task-claim dashboard event publishing).
- **Open branches**: `beadhub-legacy` only (intentional archive).
- **Blockers**: none.

## aweb-cloud (ac)
- **v0.5.5 verified-live**: /health returns release_tag=v0.5.5, aweb 1.18.1, awid 0.5.1, all subsystems green (Tom verified 2026-04-25 ~15:42Z).
- **v0.5.6 mid-deploy**: GHA succeeded 13m9s; auto-deploy pending. Tom mailing when /health flips.
- **v0.5.7 (planned)**: aalf KI#1 fix. Single commit (signer + caller + audit citation + four-case regression). Empty signing_key_id deferred.
- **Pins**: aweb>=1.18.1, awid-service>=0.5.1.
- **Open branches**: none.

## awid
- **api.awid.ai prod**: now on 0.5.1 as of 2026-04-25 cutover (commit ed4fa89 lifecycle-script-driven). Was on 0.3.1 prior — caused identity_mismatch on aala BYOIT path until cutover.
- **PyPI awid-service**: 0.5.1 published with aweb 1.18.1 ship.

## Cross-repo alignment
- ac pins aligned with shipped aweb + awid. Verified post-deploy.
- Decision records: aakq/aweb-1.17.0 (2026-04-23), ac-v0.5.4 (2026-04-23), aweb-1.18.1 + recovery (2026-04-25), aala/v0.5.5 (John converging). Pending: awid prod cutover, v0.5.7 KI#1.

## Concerns

- **KI#1 (aalf) is launch-blocking.** Until v0.5.7 ships and verified-live proves verification_status=verified on TX-path mail, hosted dashboard mail send to multi-membership recipients is broken. Amy hits this; any new BYOIT user would hit it.
- **End-to-end test gaps for shipped P0 features**. aaiu.5 (hosted onboarding e2e), aaja.6 (cross-repo Docker e2e for hosted MCP OAuth verified mail), aaja.7 (signing-path unification) open. The aalf patch's single-commit signer fix has small overlap with aaja.7; will coordinate at landing. Same regression-coverage class as aaks.
- **Browser-verify pathway for UI-surface releases is missing from verified-live discipline.** Tom flagged on v0.5.5: dashboard UI changes pass /health curl probe but actual user-visible delta is browser-only. New corollary memory banked; will name in v0.5.6 or v0.5.7 decision record.
- **aajv (P1, ac dashboard lifecycle bypasses OSS mutation hooks)**. Pre-existing tech debt. Pending bandwidth.
- **aweb-aale (P3)** — channel plugin 1.1.0 mail-event header verified=false render. Display-only, not crypto. Not a ship-blocker.
- **aakr (P4) + aaky (P3) + aalb (P3) + aalc (P2)** filed and tracked.

## Policies standing
- Release gate (2026-04-22): full e2e + SOT analysis + CTO written-and-mailed approval before tag.
- Review via shared working tree (2026-04-22).
- Route dev-agent dispatch through coordinator (2026-04-23).
- Trust the Makefile's release-ready chain (2026-04-23).
- Written approval via mail (2026-04-23).
- Use prohibition language explicitly when redirecting devs (2026-04-25).
- Push release tags individually (2026-04-25).
- Tracker audit needs symptom-check (2026-04-25).
- **Published artifact ≠ deployed service (NEW 2026-04-25)**: artifact-on-registry + /health-reports-new-version + smoke-against-deployed-endpoint = "verified live." Banked from awid prod 0.3.1-vs-0.5.1 lag discovery.
- **Browser-verify for UI-surface releases (NEW 2026-04-25)**: /health is necessary but not sufficient when the user-visible delta is dashboard copy/layout/flow. Add a browser probe. Banked from Tom's v0.5.5 flag.

## Next milestones

- Tom + Grace: aalf patch + regression test → v0.5.7 ship under standard gate.
- John: convergent decision record entry covering 1.18.1 + v0.5.5 + awid prod cutover + (when shipped) v0.5.7 KI#1 fix.
- aaiu.5 + aaja.6 + aaja.7 dispatch when post-aalf-launch bandwidth opens.
- aais epic routing to Charlene/Avi (post-launch).
