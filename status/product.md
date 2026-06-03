# Product Status
Last updated: 2026-06-03 13:28Z (Sofia catch-up pass)

## Current focus
- **Production release state:** AC v0.5.59 is tagged/built but not deployed; app.aweb.ai still reports v0.5.58 / aweb 1.26.1. Hestia owns deploy/live-verify once Juan confirms Render env and clicks deploy.
- **Engineering risk to track with Athena:** aw 1.26.3 workspace-cleanup regression (#245) restored Juan's affected pmbah team but still needs a fix-forward shape before any CLI/workspace-cleanup-adjacent ship.
- **E2EE framing boundary:** receive-side package wave is live (channel 1.4.11, Pi 0.1.16), PyPI aweb 1.26.5 is published, but hosted custodial E2EE is not a live AC claim until v0.5.59 deploy + smoke. Hosted custodial/server-side messaging must not be described as E2E.
- **Outreach remains the company bottleneck:** long-fruit submission drafts exist and Iris has refreshed the outreach lane; actual submission/attempt rows are still unobserved from this pass.
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
- Long-fruit submission drafts are at `agents/sofia/.aw/drafts/submission-drafts-v0.md`; latest Sofia draft commit observed here is `fc7bbcb` retargeting to channel 1.4.10 / skills 0.2.10. `publishing/attempts.jsonl` has no observed rows yet.
- Juan confirmation is still useful on cadence: daily scan/draft/post loop vs weekly batch, and human review/send capacity.

## Support / user feedback
- No new external customer feedback observed in this pass.
- Prior concrete evidence remains Pepe-anonymous autonomous-install friction-to-ship arc and internal dogfood release smokes.
- #245 is the live customer-risk item: recovered affected team, fix-forward still pending.

## Priorities
1. **Catch up with Athena on #245 + v0.5.59/E2EE release boundary.** Need her current engineering read and any direction/framing ask before external claims or CLI-adjacent work moves.
2. **Let Hestia complete v0.5.59 only after Juan env/deploy confirmation, then frame claims from live evidence.** Do not pre-claim hosted custodial E2EE.
3. **Restart distribution execution with Iris once the release boundary is clear.** Submissions/attempts need actual rows, not just drafts.
4. **Resolve Juan's gbrain/corpus/omnigraph direction question before turning it into product or outreach positioning.**
