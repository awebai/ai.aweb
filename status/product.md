# Product Status

Last updated: 2026-05-02 morning (Sofia, Day-2 of team-genesis)

## Current focus

Day-2 of team-genesis. Yesterday brought Sofia + Athena + YC agent online,
plus the dev team activating with Mia, plus Hestia coming up late. Today
the loop is tightening:

- **Aida is online** as of last night (commits `571ad94 Created aida` and
  `ab4f915 Added keys`). Workspace status shows her active. Her own
  status/handoff are still dated 2026-04-30 (pre-rename); she'll refresh
  on her own wake-up.
- **Hestia hardened the runbook overnight via the right loop.** Five
  commits banking real operational discoveries: Render auto-deploy was a
  wrong assumption (Juan deploys manually); awid registry is also
  manual-deploy; verify-live table now split by deploy shape; artifact
  map + dependency rule added; ac gate-default narrowing + compat-
  invocation policy folded in. This is exactly the kind of
  prior-knowledge encoding the runbook needs before validation.
- **Athena landed test-infra work in ac**: parallelize pytest, reuse
  migrated DB across runs, reuse release image across docker e2e, make
  installed-CLI journey optional, plus a Shipping-section update for
  the new role boundaries. Direct response to the iteration-cost flag
  Hestia raised. Counts as Athena's non-feature authoring (the
  pattern from `4491df5`).
- **Playwright reproducer for Add-Existing dialog** — Athena committed
  to authoring it "tomorrow morning fresh-headed" yesterday. Not yet
  visible in ac main. Today is that morning; expect it during her wake-up.

**v0.5.17 deploy state.** Tagged by Juan last night (commit `9c1038ad`),
GHA built, but `app.aweb.ai/health` still reports `v0.5.16` this morning
(uptime ~12h). This is consistent with the runbook correction Hestia
banked: Render is manual; Juan presses the deploy button. Per Juan's
call last night, v0.5.17 ships without Hestia's retroactive gate-run,
no verified-live mail. Not a discrepancy — a state observation.

**Build/ship boundary becomes real on the NEXT ac release.** That's
likely Mia's aalr.2 (AWID ensure-team + ac persist refactor) when it
reaches branch-ready, or whichever feature lands first. Athena drafts
release notes + runs code-reviewer subagent + bless-and-runs Hestia;
Hestia runs `make release-ready` end-to-end + tags + watches CI/CD +
verifies live + posts evidence.

## Today's priorities

1. **Aida sweeps the runbook for v0.5.10-17 customer-visible deltas.**
   Original scope was v0.5.10 (1.9 NOT-boundary, login-failure section,
   409 conflict messaging). Now expanded: the Add-Existing-Identity
   dialog UX landed across v0.5.13-17 and is new customer-facing
   surface. Aida should fold those deltas. Athena reviews tech-accuracy;
   I review framing.
2. **Athena lands the Playwright-MCP reproducer for Add-Existing.**
   Reproducer-as-gate (banked policy 12) applied to the UI surface that
   generated five iterations. Closes the iteration-cost class for UI
   changes, not just this feature.
3. **Mia's aalr.2 reaches branch-ready.** First real exercise of the
   build/ship boundary under the new model. Athena reviews; bless-and-
   runs Hestia.

This week, beyond today:

1. **First distribution action.** The "5 agents" blog post draft has
   sat since 2026-04-09 awaiting Juan's voice pass. Iris not yet
   online; until she is, this is an open priority that hasn't moved.
2. **KI#1 closure decision record.** Athena drafts technical content
   (cert-presentation auth correction + aalk continuity arc + 1.18.6
   trust-model arc + Aida 4/4 attestation); I frame.
3. **Bring Iris and Metis online.** Directories exist; identity setup
   pending Juan-interactive Hetzner work.

## Product readiness

- **OSS aweb**: stable. Latest tags `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27). No commits on
  main since.
- **aweb-cloud**: live at v0.5.16. `https://app.aweb.ai/health` reports
  `release_tag=v0.5.16`, `aweb_version=1.18.6`, `git_sha=842e0b5b`,
  `awid_service_version=0.5.3`. db / redis / awid / coordination_api
  healthy. Started 2026-05-01 20:45 UTC (~12h uptime). v0.5.17 tagged
  on origin (`9c1038ad`) but Render deploy is manual; Juan hasn't
  triggered it.
- **awid registry (standalone)**: live at `version=0.5.2`, redis/db/
  schema healthy. Unchanged. (awid library inside cloud at 0.5.3,
  bumped during yesterday's release cluster.)
- **@awebai/claude-channel**: 1.3.3 published.
- **Landing site (aweb.ai)**: live. Blog section TBD; first
  personal/problem post planned for juanreyero.com.
- **Pricing in public docs**: aligned to canonical $25/$250 per
  `ac/backend/src/aweb_cloud/models/billing.py` (commit `2fbf16f`,
  caught by YC agent on first wake-up).

## Team state

Company team (`default:aweb.ai`):

- **Sofia (me)**: online. Direction surface.
- **Athena**: online. Engineering surface; bridged into dev team.
  Test-infra work last night addresses iteration-cost; Playwright
  reproducer pending today.
- **Hestia**: online. Runbook hardening overnight produced real banked
  discoveries (Render manual, awid manual, verify-live by deploy
  shape). Idle for next bless-and-run from Athena.
- **Aida**: online (came up last night). Status/handoff still
  pre-rename; will refresh on her wake-up. Runbook PR scope
  expansion is on her plate.
- **YC agent (`aweb.ai/yc`)**: offline (seen 19h ago in co.aweb).
  Special-purpose for the YC application.
- **Iris, Metis**: directories exist; identity setup pending Juan-
  interactive Hetzner work.

Dev team (`aweb:juan.aweb.ai`):

- **Athena**: cross-team membership.
- **Mia**: shipped v0.5.13-17 cluster yesterday; aalr.2 starts today
  per Athena's status.
- **Noah, Grace, Kate**: in the team; activity not yet visible from
  my surface.

## Outreach state

- **Blog post "5 agents"**: draft ready since 2026-04-09. Awaiting
  Juan's voice pass. Iris will own packaging once online.
- **Contacts**: identified in `co.aweb` (private), uncontacted.
- **Daily scanning**: not running.
- **Conversations joined**: 0.

## Support / user feedback

- KI#1 closed empirically (4/4 attestation + second-shape probe on
  2026-04-27). No regression observed across yesterday's release
  cluster.
- Add-Existing-Identity dialog UX is new customer-facing surface
  landed across v0.5.13-17. Aida folds into runbook PR.
- No external user feedback yet — distribution hasn't started.

## Open questions

- Target YC batch and deadline. Pacing for the YC agent depends on this.
- First concrete distribution action this week — Iris needs a target
  once she's online.
- Collision video before or after the first blog post? (Open from
  prior wake-up.)
- When does Juan trigger the v0.5.17 Render deploy — or do we let it
  ride into whatever the next release is?
