# Product Status
Last updated: 2026-06-10 08:35Z (hero remote-address example 404 hold)

## Current focus
- **Production release state:** app.aweb.ai is live healthy at `v0.5.60`, git `2cf21f23`, aweb `1.26.8`, awid_service `0.5.10`; api.awid.ai reports `0.5.10`.
- **Claude marketplace submissions:** Wave 4 packages are live (`@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, Pi `0.1.20`). Reviewed vendored artifacts are now pushed to `awebai/claude-plugins` origin/main at `d6034672ded5ef5dbb38fc84fcb0a1de883b9544`; submission can proceed using that pushed SHA. Outward text must keep the README trust boundary: inbound channel, outbound via `aw`, hosted/server-side paths not E2E.
- **E2EE framing boundary:** keep claims narrow to smoked surfaces. Hosted/server-side messaging must not be called E2E; do not make broad generic self-custodial E2EE readiness claims unless the AWID encryption-key publish skew Athena flagged is fixed/explained.
- **Engineering risk tracked with Athena:** aw 1.26.3 workspace-cleanup regression (#245) remains the customer-risk pattern to track for CLI/workspace-cleanup-adjacent work: read/status flows must not destructively delete server workspace/agent rows from stale local paths.
- **Landing site setup-framing cleanup:** site deploy `f528b366` is 3/3 verified-live for home intent tabs + /llms.txt update; prior `2facc1e1` setup cleanup remains 5/6 verified-live. HOLDS: `/docs/team-bootstrap.md` still serves stale 15KB markdown from Render cache; and the hero terminal panel teaches `ami.aweb.ai/pi`, which currently 404s at namespace resolution. Ship wake-setup restoration if needed, but fix the hero example as P1 follow-on.
- **Direction context:** gbrain/corpus/omnigraph question is waiting on Juan; no product priority change until that answer lands.

## Product readiness
- **OSS aweb / PyPI:** `aweb==1.26.8` published.
- **aw CLI npm:** `@awebai/aw@1.26.8` published.
- **Channel / skills / Pi:** `@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, `@awebai/pi@0.1.20` published.
- **aweb-cloud:** live health check 2026-06-07 12:14Z reports `release_tag=v0.5.60`, `git_sha=2cf21f23`, `aweb_version=1.26.8`, `awid_service_version=0.5.10`, healthy.
- **awid registry:** `https://api.awid.ai/health` reports `version=0.5.10`, ok.
- **Landing site:** deploy `f528b366` verified live: home pill toggle labels [In your terminal | As a team | In your browser], layout-stable tab panels, /llms.txt “Get started — pick where you work” with the three panel headers, and ARIA tablist semantics verified. Prior `2facc1e1` cleanup mostly live: blueprint/orchestration framing and /docs/team-bootstrap/ alias. `/docs/team-bootstrap.md` is still stale due Render publish-dir/cache behavior. Hero terminal remote-address example `ami.aweb.ai/pi` is not live (404 Namespace not found). AC backend untouched.

## Outreach
- Claude marketplace path is the active long-fruit lane. `claude-plugins` commit `d6034672ded5ef5dbb38fc84fcb0a1de883b9544` adds vendored community-submission artifacts rematerialized from corrected npm packages and validated by Athena/Sofia/Hestia; origin push blocker is closed.
- Site/setup cleanup is NOT ready as a distribution beat until `/docs/team-bootstrap.md` stale Render artifact is cleared and the hero remote-address example either resolves/responds or is made unambiguously placeholder. No public claim went out from Sofia; nothing to retract externally from this surface.
- `publishing/attempts.jsonl` has no observed submission rows yet. Do not add submission attempts until the claude-plugins commit is pushed and actual submission occurs.
- Juan confirmation is still useful on broader cadence: daily scan/draft/post loop vs weekly batch, and human review/send capacity.

## Support / user feedback
- No new external customer feedback observed in this pass.
- Prior concrete evidence remains Pepe-anonymous autonomous-install friction-to-ship arc and internal dogfood release smokes.
- #245 acceptance to preserve: missing local path does not delete rows during `aw workspace status`, explicit cleanup/delete still works for truly gone ephemeral workspaces, persistent/global identities are never deleted by stale-path cleanup, pmbah rename regression covered, release notes warn 1.26.3 users who renamed worktree roots.

## Priorities
1. **Close landing-site holds**: (a) Juan clear-build-cache redeploy + Render build-command check/update to `hugo --minify --cleanDestinationDir` (or Olivia decides markdown compatibility file remains), then verify `/docs/team-bootstrap.md` no longer serves stale 2026-06-08 content; (b) fix hero `ami.aweb.ai/pi` example by provisioning a responding agent, swapping to a responding public address, or making the example placeholder.
2. **Proceed with Claude marketplace submission from pushed SHA `d6034672`** while keeping trust-boundary wording narrow.
3. **Keep outward E2EE claims narrow** to exact smoked surfaces; no broad “E2EE is live” or hosted/server-side E2E claim.
4. **Track #245 fix-forward before CLI/workspace-cleanup-adjacent ships.** Direction agrees with Athena: read/status commands should not be destructive lifecycle operations.
5. **Resolve Juan's gbrain/corpus/omnigraph direction question before turning it into product or outreach positioning.**
