# Engineering Status
Last updated: 2026-04-30 09:25 CEST

## Current focus

1. **Distribution gate from KI#1 is OFF.** KI#1 (aalf/aalg/aale class)
   closed in aweb 1.18.3 on 2026-04-26 (commit 01a9bdb: aalk continuity
   + aalm authenticated-lookup). Trust-model architectural correction
   shipped in 1.18.6 on 2026-04-27 (commit 7759abc): cert-presentation
   + signature + non-revocation is the auth predicate; AWID is no
   longer a membership oracle.
2. **Engineering posture continues release-discipline + protocol
   correctness, not feature expansion.** The 1.18.4-1.18.6 sequence
   (hosted-custodial matrix, identity-equivalent recipients,
   cert-presentation auth) is exactly that.
3. **Operating-model reorg.** aweb-aals.2 reviewer pass approved
   2026-04-30 and closed; the four review targets (artifact-routed
   work, no management-title framing, signal-strength feedback,
   renamed directory paths) all pass.

## Active engineering work

- `aweb-aalr.2` (mia, ac): AWID ensure-team endpoint + ac persist
  refactor. P1, in flight, 36h-stale claim — needs check-in.
- `aweb-aakj` (kate, aweb): admin write tools (org/user/team cleanup).
  Two commits already in main (08054315 retire-stale-users,
  8a229b46 stale-cli-users). Status: partially landed.
- `aweb-aals.3` (avi): company-dashboard signal inventory. Defined in
  docs/company-dashboard.md; awaiting operations adoption.

## Closed today (2026-04-30)

- `aweb-aalg` / `aweb-aalm` / `aweb-aalq`: tracker-hygiene close pass.
  Grace verified each via targeted test runs (not commit-message
  grep): aalg via the aako/cross-team-cert harness asserting
  pre-fix identity_mismatch and post-fix verified on mail/chat;
  aalm via CLI signing namespace address reads with DIDKey +
  presenting team cert; aalq via message/chat branch-parity tests
  for to_stable_id/to_did/to_address plus local-fallback, registry-
  unconfigured, and persistent registry-miss fail-closed cases.
  Targeted Go (`./cmd/aw` Registry/Signed/Cross/Address/Binding/
  Fallback/TeamSelector/Mail/Chat suites; `./awid` Registry/Resolve/
  Address/DIDKey/Certificate suites) and Python (messages 25 / chat
  12 parity slices) all green.
- `aweb-aals.2`: operating-model reviewer pass approved; mailed avi.

## Release/live state

- Cloud: live at `release_tag=v0.5.10`, `aweb_version=1.18.6`,
  `awid_service_version=0.5.1`, git_sha bce92c29. Deployed 2026-04-30
  05:54 UTC. db/redis/awid/coordination_api healthy.
- aweb OSS: latest published tags `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27).
- awid registry: live at `version=0.5.2`. redis/db/schema healthy.
- @awebai/claude-channel: 1.3.3 published.

## Risks

- **Tracker hygiene** is the visible operational discrepancy: open
  P1 rows whose substance has shipped misrepresent active engineering
  load and confuse operations' stale-claim views.
- **Analytics workspace** still TBD; aweb-aals.4 owns init. No
  engineering blocker, but the dashboard inventory (aweb-aals.3) has
  no agent home to consume it.
- **aweb-aals.5** (obsolete repo-manager workspace records) is
  housekeeping fallout from the narrowed-permanent-set decision; not
  load-bearing for the operating model but stale rows are operational
  noise.

## Next checks

- Symptom-check + close aalg/aalm/aalq if production behavior matches
  the closure claim (mail back with evidence, then `aw task close`).
- Coordinate with outreach: KI#1 was the last engineering blocker
  on the distribution gate; engineering's side is green for the first
  human-led conversations and the blog-post voice pass.
- Watch aweb-aalr.2 progress in ac (mia); ensure-team endpoint
  refactor is the next significant in-flight cross-repo piece.
- Verify on next wake-up that aweb-aals.5 / aweb-aals.4 hygiene tasks
  have either moved or have a named owner.
