# Product Status
Last updated: 2026-06-03 15:00Z (Athena driving Claude marketplace review)

## Current focus
- **Production release state:** AC v0.5.59 is tagged/built but not deployed; app.aweb.ai still reports v0.5.58 / aweb 1.26.1. Hestia owns deploy/live-verify once Juan confirms Render env and clicks deploy.
- **Engineering risk tracked with Athena:** aw 1.26.3 workspace-cleanup regression (#245) is live but pattern-specific. Root is read/status cleanup deleting server rows when a stale local `workspace_path` is missing. Fix-forward direction: status/read flows must not destructively delete server workspace/agent rows from local path nonexistence alone; require explicit cleanup/delete or stronger evidence.
- **E2EE framing boundary:** receive-side package wave is live (channel 1.4.11, Pi 0.1.16), PyPI aweb 1.26.5 is published, but hosted custodial E2EE is not a live AC claim until v0.5.59 deploy + exact smoke. Hosted custodial/server-side messaging must not be described as E2E. Additional Athena caveat: aw 1.26.4 local encryption-key setup currently fails AWID publish against api.awid.ai 0.5.9 (`custody` extra_forbidden), so do not claim generic self-custodial E2EE readiness until fixed or explained.
- **Outreach remains the company bottleneck:** long-fruit submission drafts exist and Iris has refreshed the outreach lane; actual submission/attempt rows are still unobserved from this pass. Claude marketplace submissions are held until Wave 4 corrected packages publish (expected channel 1.4.12 / skills 0.2.12 from aweb 63d77176 or later). Athena is driving review: after rematerialization/provenance/strict validation, Sofia routes diff + validation to Athena before commit or submission.
- **Direction context:** gbrain/corpus/omnigraph question is waiting on Juan; no product priority change until that answer lands.

## Product readiness
- **OSS aweb / PyPI:** `aweb==1.26.5` published.
- **aw CLI npm:** `@awebai/aw@1.26.4` published.
- **Channel / skills / Pi:** `@awebai/claude-channel@1.4.11`, `@awebai/claude-skills@0.2.10`, `@awebai/pi@0.1.16` published.
- **aweb-cloud:** live health check 2026-06-03 13:28Z reports `release_tag=v0.5.58`, `git_sha=340122ef`, `aweb_version=1.26.1`, `awid_service_version=0.5.9`, healthy. v0.5.59 GHCR image/tag is awaiting Juan deploy per Hestia.
- **awid registry:** `https://api.awid.ai/health` reports `version=0.5.9`, ok.
- **Landing site:** latest restructure verified-live per Hestia/Olivia; no direction action unless Iris's trinity-leak pass finds stale copy.

## Outreach
- Iris status (2026-05-26) says the active pivot is from authoring to distribution: audit parked artifacts, adapt beadhub-era source material against current aweb state, add Pi extension as Persona-3 promotion arc, derive v0.5.48 release-notes pack.
- Long-fruit submission drafts are at `agents/sofia/.aw/drafts/submission-drafts-v0.md`; latest Sofia draft commit observed here is `fc7bbcb` retargeting to channel 1.4.10 / skills 0.2.10. `publishing/attempts.jsonl` has no observed rows yet. Hold Claude marketplace submissions: do not use channel 1.4.11 or skills 0.2.11. Expected Wave 4 corrected packages are channel 1.4.12 and skills 0.2.12. Channel configure source fix landed at aweb `63d77176`; Wave 4 package source should be this commit or later. Keep claude-plugins working tree parked until corrected npm versions exist. After Hestia confirms publish, rematerialize from package artifacts, update provenance, run strict validation + artifact/smoke checks, and send Athena diff + validation for review before committing/submitting.
- Juan confirmation is still useful on cadence: daily scan/draft/post loop vs weekly batch, and human review/send capacity.

## Support / user feedback
- No new external customer feedback observed in this pass.
- Prior concrete evidence remains Pepe-anonymous autonomous-install friction-to-ship arc and internal dogfood release smokes.
- #245 is the live customer-risk item: recovered affected pmbah team; acceptance for fix is missing local path does not delete rows during `aw workspace status`, explicit cleanup/delete still works for truly gone ephemeral workspaces, persistent/global identities are never deleted by stale-path cleanup, pmbah rename regression covered, release notes warn 1.26.3 users who renamed worktree roots.

## Priorities
1. **Hold outward E2EE claims narrow.** No broad “E2EE is live” or generic self-custodial E2EE readiness claim; only claim exact smoked surfaces after v0.5.59 live evidence and AWID publish skew is resolved/explained.
2. **Track #245 fix-forward before CLI/workspace-cleanup-adjacent ships.** Direction agrees with Athena: read/status commands should not be destructive lifecycle operations.
3. **Restart distribution execution with Iris once the release boundary is clear.** Submissions/attempts need actual rows, not just drafts.
4. **Resolve Juan's gbrain/corpus/omnigraph direction question before turning it into product or outreach positioning.**
