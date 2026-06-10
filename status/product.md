# Product Status
Last updated: 2026-06-10 10:45Z (aw 1.26.14 verified-live)

## Current focus
- **Production release state:** app.aweb.ai is live healthy at `v0.5.60`, git `2cf21f23`, aweb `1.26.8`, awid_service `0.5.10`; api.awid.ai reports `0.5.10`.
- **Claude marketplace submissions:** Wave 4 packages are live (`@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, Pi `0.1.20`). Reviewed vendored artifacts are now pushed to `awebai/claude-plugins` origin/main at `d6034672ded5ef5dbb38fc84fcb0a1de883b9544`; submission can proceed using that pushed SHA. Outward text must keep the README trust boundary: inbound channel, outbound via `aw`, hosted/server-side paths not E2E.
- **E2EE framing boundary:** keep claims narrow to smoked surfaces. Hosted/server-side messaging must not be called E2E; do not make broad generic self-custodial E2EE readiness claims unless the AWID encryption-key publish skew Athena flagged is fixed/explained.
- **Engineering risk tracked with Athena:** aw 1.26.3 workspace-cleanup regression (#245) remains the customer-risk pattern to track for CLI/workspace-cleanup-adjacent work: read/status flows must not destructively delete server workspace/agent rows from stale local paths.
- **Landing site setup-framing cleanup:** site deploy `f4c0fec3` is 2/2 verified-live: home hero + /llms.txt now teach `aw chat send-and-wait aweb.ai/aida ...`, zero `ami.aweb.ai` remains, and Olivia pre-commit verified an end-to-end reply round-trip. Prior `7c5d2dcd`, `f528b366`, and `2facc1e1` checks remain verified. HOLD: `/docs/team-bootstrap.md` still serves stale 15KB markdown from Render cache; aweb-aaqe.6 closes when that flips/gets intentionally retained.
- **aaqe.7 greeter lane reprioritized:** Juan reversed deprioritization. Plan is fresh `pi.aweb.ai` namespace + `pi.aweb.ai/ama` greeter identity + Olivia greeter soul + Hestia persistent Pi runner. Hero copy stays `aweb.ai/aida` until policy #14 outside-team send-and-wait verify-live passes for `pi.aweb.ai/ama`. Existing `aweb.ai/ama` is live external-inbound-proxy for YC/investors/press and remains separate scope. aw 1.26.14/aweb-aaqi is verified-live and fixes forward connect rollback/recovery behavior, but pi.aweb.ai/ama orphan cleanup still needs Juan's recovery path before retry.
- **Direction context:** gbrain/corpus/omnigraph question is waiting on Juan; no product priority change until that answer lands.

## Product readiness
- **OSS aweb / PyPI:** `aweb==1.26.8` published.
- **aw CLI npm:** `@awebai/aw@1.26.14` published (aw-v1.26.14 at aweb `4518c85c`; aweb-aaqi verified-live).
- **Channel / skills / Pi:** `@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, `@awebai/pi@0.1.20` published.
- **aweb-cloud:** live health check 2026-06-07 12:14Z reports `release_tag=v0.5.60`, `git_sha=2cf21f23`, `aweb_version=1.26.8`, `awid_service_version=0.5.10`, healthy.
- **awid registry:** `https://api.awid.ai/health` reports `version=0.5.10`, ok.
- **Landing site:** deploy `f4c0fec3` verified live: hero terminal first-contact example now uses `aweb.ai/aida`; zero `ami.aweb.ai` remains on home or /llms.txt. Future flip to `pi.aweb.ai/ama` is gated on greeter runner and outside-team send-and-wait verification. Prior `7c5d2dcd` wake setup, `f528b366` tabs, and `2facc1e1` cleanup remain verified. `/docs/team-bootstrap.md` is still stale due Render publish-dir/cache behavior. AC backend untouched.

## Outreach
- Claude marketplace path is the active long-fruit lane. `claude-plugins` commit `d6034672ded5ef5dbb38fc84fcb0a1de883b9544` adds vendored community-submission artifacts rematerialized from corrected npm packages and validated by Athena/Sofia/Hestia; origin push blocker is closed.
- Site/setup cleanup is NOT ready as a distribution beat until `/docs/team-bootstrap.md` stale Render artifact is cleared. Hero remote-address defect is closed by `f4c0fec3`. No public claim went out from Sofia; nothing to retract externally from this surface.
- `publishing/attempts.jsonl` has no observed submission rows yet. Do not add submission attempts until the claude-plugins commit is pushed and actual submission occurs.
- Juan confirmation is still useful on broader cadence: daily scan/draft/post loop vs weekly batch, and human review/send capacity.

## Support / user feedback
- No new external customer feedback observed in this pass.
- Prior concrete evidence remains Pepe-anonymous autonomous-install friction-to-ship arc and internal dogfood release smokes.
- #245 acceptance to preserve: missing local path does not delete rows during `aw workspace status`, explicit cleanup/delete still works for truly gone ephemeral workspaces, persistent/global identities are never deleted by stale-path cleanup, pmbah rename regression covered, release notes warn 1.26.3 users who renamed worktree roots.

## Priorities
1. **Close landing-site stale artifact hold**: Juan clear-build-cache redeploy + Render build-command check/update to `hugo --minify --cleanDestinationDir` (or Olivia decides markdown compatibility file remains), then verify `/docs/team-bootstrap.md` no longer serves stale 2026-06-08 content.
2. **Track aaqe.7 greeter lane**: do not flip hero from `aweb.ai/aida` to `pi.aweb.ai/ama` until orphan cleanup/retry succeeds, persistent runner is live, and policy #14 outside-team send-and-wait verification passes.
3. **Proceed with Claude marketplace submission from pushed SHA `d6034672`** while keeping trust-boundary wording narrow.
4. **Keep outward E2EE claims narrow** to exact smoked surfaces; no broad “E2EE is live” or hosted/server-side E2E claim.
5. **Track #245 fix-forward before CLI/workspace-cleanup-adjacent ships.** Direction agrees with Athena: read/status commands should not be destructive lifecycle operations.
6. **Resolve Juan's gbrain/corpus/omnigraph direction question before turning it into product or outreach positioning.**
