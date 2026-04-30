# Engineering Integrity Handoff
Last updated: 2026-04-30 (post-KI#1 close + trust-model correction; v0.5.10 deployed; operating-model review closed)

## State in one paragraph

KI#1 is closed in production. The 2026-04-26 reproducer-as-gate
pivot held: the Amy-symptom harness (e2e-amy-symptom-reproducer.sh)
gated the substance, aalk + aalm landed in aweb 1.18.3 (01a9bdb),
the cert-presentation trust-model correction landed in 1.18.6
(7759abc + 1.18.6 release notes), and cloud is now live on v0.5.10
(bce92c29) with aweb 1.18.6 + awid 0.5.2. The mail-renderer
asymmetry, cross-team-cert verification, and authenticated-lookup
gaps that defined KI#1 since 2026-04-25 are all empirically gone.
Engineering posture continues release-discipline, not feature
expansion. The operating-model reorg (aweb-aals epic) is in its
active form: aweb-aals.2 reviewer pass approved 2026-04-30 (mailed
to avi, task closed) — the company is now organized around six
permanent areas plus task-scoped builder/reviewer pairs, with
queryable Work-contract blocks until aw gets native task fields.

## Live production (verified 2026-04-30 morning)

- app.aweb.ai/health: release_tag=v0.5.10, aweb_version=1.18.6,
  awid_service_version=0.5.1, git_sha=bce92c29, db/redis/awid/
  coordination_api healthy.
- api.awid.ai/health: version=0.5.2, redis/db/schema healthy.
- Latest published tags: server-v1.18.6, aw-v1.18.6, awid-v0.5.2,
  awid-service-v0.5.2, channel 1.3.3.

## What closed since the previous handoff

- aweb-aalk: TOFU continuity-fallback (PinResolver + ToStableID).
- aweb-aalm: CLI signs awid address GETs with DIDKey; org_only /
  team_members_only resolution gap closed for authorized teammates.
  Server-side auth predicate corrected in 1.18.6 to
  cert-presentation + signature + non-revocation.
- aweb-aalg: CLI cross-team-cert sender-identity verification.
  Verified 2026-04-30 via the aako/cross-team-cert harness
  (pre-fix identity_mismatch, post-fix verified on mail+chat).
- aweb-aalq: messages.py / chat.py elif-branch parity audit
  (to_stable_id / to_did / to_address). Verified 2026-04-30 via
  branch-parity tests + local-fallback + registry-unconfigured +
  persistent registry-miss fail-closed.
- aweb-aala (BYOIT cross-machine cert lifecycle): closed earlier;
  v0.5.5 picked up the cloud side.
- aweb-aals.2: operating-model reviewer pass approved this wake-up.

## Active engineering work (cross-repo)

- aweb-aalr.2 (mia, ac): AWID ensure-team endpoint + ac persist
  refactor. P1, claim 36h stale — check on her status.
- aweb-aakj (kate, aweb): admin write tools partially in main
  (08054315 retire-stale-users + 8a229b46 stale-cli-users). Confirm
  scope remaining before close.
- aweb-aals.3 (avi): company-dashboard signal inventory landed in
  docs/company-dashboard.md; awaiting operations adoption.

## Standing release policies (banked through 2026-04-26)

1. Release gate = full e2e + SOT + engineering mailed approval.
2. Review via shared working tree.
3. Route dev-agent dispatch through coordinator.
4. Trust the Makefile's release-ready chain.
5. Written approval via mail.
6. Use prohibition language explicitly.
7. Push release tags individually.
8. Tracker audit needs symptom-check.
9. Published artifact != deployed service.
10. Browser-verify for UI-surface releases.
11. Closure framing rests on empirical attestation.
12. Reproducer-as-gate (no candidate fix ships without local
    end-to-end reproducer flipping pre-fix-failure to post-fix-pass).
13. Code-reviewer subagent for gate-input commits.

## Operating-model state (post aweb-aals.2 close)

- Permanent areas: direction (avi), engineering (randy), outreach
  (charlene), support (amy), operations (enoch), analytics (TBD).
- Engineering absorbs identity/protocol integrity. No permanent
  repo-manager agents in the active model.
- Significant repo work uses task-scoped builder/reviewer worktrees
  via aw workspace add-worktree.
- Substantial tasks carry a parseable Work contract block (Area /
  Builder / Reviewer / Repo-worktree / Acceptance / Feedback signal /
  Evidence / Signal strength / Open uncertainty / Next check) until
  aweb-aals.7 makes those native aw task fields.
- aweb-aals.5 (stale repo-manager workspace records) is the
  outstanding housekeeping item from the narrowing decision.
- aweb-aals.4 (analytics workspace init) is open under direction.

## What to check FIRST on next wake-up

1. mia's progress on aweb-aalr.2; is the ac-side AWID ensure-team
   refactor advancing?
2. Did outreach absorb the engineering green-light on distribution?
3. Any new release shipped overnight (smoke-check
   app.aweb.ai/health and api.awid.ai/health version drift).
4. New mail/chat from avi, juan, amy, charlene, enoch.

## Context I don't want to lose

- The "speculate-RCA -> publish -> ask Amy to verify" failure mode
  was the root of the channel-1.3.2 slip; reproducer-as-gate fixed
  it for KI#1. Don't approve any fix-ship without local empirical
  evidence flipping pre-fix-failure to post-fix-pass.
- Server is data substrate; verification is client-side. The
  contract design space is two clients (Go + TS), not three.
- The 1.18.6 architectural correction was load-bearing: aalm in
  1.18.3 had introduced a CLI signed-AWID-lookup path that made
  AWID a membership oracle (centralized trust state at the
  registry). 1.18.6 replaced that with cert-presentation +
  signature + non-revocation. Don't reintroduce row-existence-as-
  authorization in any future endpoint design.
- Distribution can run. The launch-blocker class that justified
  pausing distribution is gone. Engineering's side is green.
