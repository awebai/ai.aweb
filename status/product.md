# Product Status
Last updated: 2026-06-11 09:10Z (HN draft framing pass sent)

## Current focus
- **Production release state:** app.aweb.ai is live healthy at `v0.5.60`, git `2cf21f23`, aweb `1.26.8`, awid_service `0.5.10`; api.awid.ai reports `0.5.10`.
- **Claude marketplace submissions:** Wave 4 packages are live (`@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, Pi `0.1.20`). Reviewed vendored artifacts are now pushed to `awebai/claude-plugins` origin/main at `d6034672ded5ef5dbb38fc84fcb0a1de883b9544`; submission can proceed using that pushed SHA. Outward text must keep the README trust boundary: inbound channel, outbound via `aw`, hosted/server-side paths not E2E.
- **E2EE framing boundary:** keep claims narrow to smoked surfaces. Hosted/server-side messaging must not be called E2E; do not make broad generic self-custodial E2EE readiness claims unless the AWID encryption-key publish skew Athena flagged is fixed/explained.
- **Engineering risk tracked with Athena:** aw 1.26.3 workspace-cleanup regression (#245) remains the customer-risk pattern to track for CLI/workspace-cleanup-adjacent work: read/status flows must not destructively delete server workspace/agent rows from stale local paths.
- **Landing site setup-framing cleanup:** aweb-aaqe.6 is CLOSED. `/docs/team-bootstrap.md` returns HTTP 404 after Render Clear build cache & deploy. Prior `7c5d2dcd`, `f528b366`, `2facc1e1`, and `4907b8e3` checks remain verified.
- **aaqe.7 customer-facing half CLOSED:** hero terminal panel now teaches `pi.aweb.ai/ama` after Olivia's fresh outside-team probe passed and site deploy `4907b8e3` verified live. `pi.aweb.ai/ama` is registered/running with co.aweb `f67e2ef` soul loaded. `aweb.ai/aida` remains support-side fallback; `aweb.ai/ama` remains YC/investor/press proxy.
- **Direction context:** gbrain/corpus/omnigraph question is waiting on Juan; no product priority change until that answer lands.

## Product readiness
- **OSS aweb / PyPI:** `aweb==1.26.8` published.
- **aw CLI npm:** `@awebai/aw@1.26.14` published (aw-v1.26.14 at aweb `4518c85c`; aweb-aaqi verified-live).
- **Channel / skills / Pi:** `@awebai/claude-channel@1.4.12`, `@awebai/claude-skills@0.2.12`, `@awebai/pi@0.1.20` published.
- **aweb-cloud:** live health check 2026-06-07 12:14Z reports `release_tag=v0.5.60`, `git_sha=2cf21f23`, `aweb_version=1.26.8`, `awid_service_version=0.5.10`, healthy.
- **awid registry:** `https://api.awid.ai/health` reports `version=0.5.10`, ok.
- **Landing site:** aweb-aaqe.7 customer-facing half closed: hero terminal first-contact example uses `pi.aweb.ai/ama`; outside-team probe from `juan.aweb.ai/hero-probe-0610` passed on released aw 1.26.14; home + /llms.txt render `pi.aweb.ai/ama`, zero `aweb.ai/aida` rendered there, zero `ami.aweb.ai`; `/docs/team-bootstrap.md` returns 404. AC backend untouched.

## Outreach
- Claude marketplace path is the active long-fruit lane. `claude-plugins` commit `d6034672ded5ef5dbb38fc84fcb0a1de883b9544` adds vendored community-submission artifacts rematerialized from corrected npm packages and validated by Athena/Sofia/Hestia; origin push blocker is closed.
- Hero greeter distribution beat direction: Iris should draft HN-primary + Twitter + r/ClaudeCode follow-up for 2026-06-16/17 if draft/logging/submitter are ready. HN draft landed at 9f8f73e; Sofia framing-pass sent with four edits (title keep, avoid “Honest about state”, explicit signed-plaintext/relay-readable boundary, soften “verifiable signature” unless verification instructions added). Pre-HN gates: attempts/runbook row-writing wired, Olivia adversarial smoke PASS, and Hestia burst-capacity read PASS by 06-13 (>=95% success at N=50, P95 <30s, no silent hangs). Frame as “homepage you can talk to” / replayable identity+messaging demo, not E2EE or broad interoperability; P3-primary proof while P1 priority remains unchanged. Customer-facing no-em-dash rule is now banked in `publishing/voice.md` (50eeca6).
- ClawHub `claweb` replacement cutover published: `claweb@1.0.0` live after Sam/Juan go, plaintext/no-E2EE boundary and no-API-key badge checks passed, light-tier interop smoke closed; direct Sam mail still needs Athena relay.
- `publishing/attempts.jsonl` has no observed submission rows yet. Do not add submission attempts until the claude-plugins commit is pushed and actual submission occurs.
- Juan confirmation is still useful on broader cadence: daily scan/draft/post loop vs weekly batch, and human review/send capacity.

## Support / user feedback
- No new external customer feedback observed in this pass.
- Prior concrete evidence remains Pepe-anonymous autonomous-install friction-to-ship arc and internal dogfood release smokes.
- #245 acceptance to preserve: missing local path does not delete rows during `aw workspace status`, explicit cleanup/delete still works for truly gone ephemeral workspaces, persistent/global identities are never deleted by stale-path cleanup, pmbah rename regression covered, release notes warn 1.26.3 users who renamed worktree roots.

## Priorities
1. **Proceed with Claude marketplace submission from pushed SHA `d6034672`** while keeping trust-boundary wording narrow.
2. **Keep outward E2EE claims narrow** to exact smoked surfaces; no broad “E2EE is live” or hosted/server-side E2E claim.
3. **Track #245 fix-forward before CLI/workspace-cleanup-adjacent ships.** Direction agrees with Athena: read/status commands should not be destructive lifecycle operations.
4. **Resolve Juan's gbrain/corpus/omnigraph direction question before turning it into product or outreach positioning.**
