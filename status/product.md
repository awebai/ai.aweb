# Product Status
Last updated: 2026-06-07 12:14Z (Claude marketplace push-block folded)

## Current focus
- **Production release state:** app.aweb.ai is live healthy at `v0.5.60`, git `2cf21f23`, aweb `1.26.8`, awid_service `0.5.10`; api.awid.ai reports `0.5.10`.
- **Claude marketplace submissions:** Wave 4 packages are live (`@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, Pi `0.1.20`). Athena rematerialized/reviewed `claude-plugins` artifacts locally and committed `d603467`, but push is blocked by missing write credentials. No Anthropic submission or readiness claim until `d603467` (or equivalent applied patch) is pushed to origin and we can cite the pushed SHA.
- **E2EE framing boundary:** keep claims narrow to smoked surfaces. Hosted/server-side messaging must not be called E2E; do not make broad generic self-custodial E2EE readiness claims unless the AWID encryption-key publish skew Athena flagged is fixed/explained.
- **Engineering risk tracked with Athena:** aw 1.26.3 workspace-cleanup regression (#245) remains the customer-risk pattern to track for CLI/workspace-cleanup-adjacent work: read/status flows must not destructively delete server workspace/agent rows from stale local paths.
- **Direction context:** gbrain/corpus/omnigraph question is waiting on Juan; no product priority change until that answer lands.

## Product readiness
- **OSS aweb / PyPI:** `aweb==1.26.8` published.
- **aw CLI npm:** `@awebai/aw@1.26.8` published.
- **Channel / skills / Pi:** `@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, `@awebai/pi@0.1.20` published.
- **aweb-cloud:** live health check 2026-06-07 12:14Z reports `release_tag=v0.5.60`, `git_sha=2cf21f23`, `aweb_version=1.26.8`, `awid_service_version=0.5.10`, healthy.
- **awid registry:** `https://api.awid.ai/health` reports `version=0.5.10`, ok.
- **Landing site:** latest restructure verified-live per prior Hestia/Olivia state; no direction action unless Iris's trinity-leak pass finds stale copy.

## Outreach
- Claude marketplace path is the active long-fruit lane. Local `claude-plugins` commit `d603467` adds vendored community-submission artifacts rematerialized from corrected npm packages and validated by Athena/Sofia, but origin push is blocked. Patch artifact exists at `/home/juanre/prj/awebai/claude-plugins/artifacts/d603467-claude-marketplace-artifacts.patch`.
- `publishing/attempts.jsonl` has no observed submission rows yet. Do not add submission attempts until the claude-plugins commit is pushed and actual submission occurs.
- Juan confirmation is still useful on broader cadence: daily scan/draft/post loop vs weekly batch, and human review/send capacity.

## Support / user feedback
- No new external customer feedback observed in this pass.
- Prior concrete evidence remains Pepe-anonymous autonomous-install friction-to-ship arc and internal dogfood release smokes.
- #245 acceptance to preserve: missing local path does not delete rows during `aw workspace status`, explicit cleanup/delete still works for truly gone ephemeral workspaces, persistent/global identities are never deleted by stale-path cleanup, pmbah rename regression covered, release notes warn 1.26.3 users who renamed worktree roots.

## Priorities
1. **Get `claude-plugins` commit `d603467` pushed by someone with write access** (or equivalent patch applied/pushed), then proceed to Anthropic submission with pushed SHA provenance.
2. **Keep outward E2EE claims narrow** to exact smoked surfaces; no broad “E2EE is live” or hosted/server-side E2E claim.
3. **Track #245 fix-forward before CLI/workspace-cleanup-adjacent ships.** Direction agrees with Athena: read/status commands should not be destructive lifecycle operations.
4. **Resolve Juan's gbrain/corpus/omnigraph direction question before turning it into product or outreach positioning.**
