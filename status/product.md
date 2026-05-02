# Product Status

Last updated: 2026-05-02 evening (Sofia, Day-2 closing — build/ship boundary is real)

## Current focus

Day-2 of team-genesis closes with the build/ship boundary now real,
not theoretical. **First end-to-end Hestia gate run completed today**
on ac v0.5.18 + aw CLI 1.18.8 (claim-human contract fix). Gate caught
a real failure on the first run (test-script gap in e2e A.18); Athena
landed the fix in `1be46c42`; re-run green; tagged + pushed; image
built; Juan deployed manually; Hestia verified live and posted the
evidence mail. ~80 min end-to-end including the failure detour. The
operating model behaved correctly: Athena bless-and-run → Hestia gate
chain → joint failure-shape work with Athena → re-run → ship → verify
→ evidence mail.

The morning's setup that fed this:

- **Aida is online** (commits `571ad94`, `ab4f915` overnight). Her
  status/handoff still pre-rename; she'll refresh on her own wake-up.
- **Hestia hardened the runbook overnight via the right loop**:
  Render auto-deploy was a wrong assumption (Juan deploys manually);
  awid registry is also manual-deploy; verify-live table split by
  deploy shape; artifact map + dependency rule added; ac
  gate-default narrowing + compat-invocation policy folded in.
- **Athena landed test-infra work in ac**: parallelize pytest, reuse
  migrated DB across runs, reuse release image across docker e2e,
  make installed-CLI journey optional. Direct response to the
  iteration-cost flag Hestia raised; non-feature authoring per
  decision `4491df5`.
- **v0.5.17** shipped without Hestia's retroactive gate-run (Juan
  called it off last night; v0.5.18 became the first real exercise
  instead).
- **Conversations-as-first-class direction call settled today**
  (decision `c874f2a`): parked with four named triggers; invariant 8
  banked (findability and continuation are independent reachability
  concerns); architectural framing preserved in
  `aweb/docs/conversations-as-first-class.md` (working doc, not
  promoted). Athena filed `aweb-aame` epic, P3, parked.

## Today's priorities (status at end of day)

1. **Build/ship boundary's first end-to-end Hestia gate run** —
   **DONE** today (v0.5.18 + aw 1.18.8). Operating-model
   validation; runbook will fold first-exercise observations.
2. **Aida sweeps the runbook for v0.5.10-18 customer-visible
   deltas.** Original scope was v0.5.10 (1.9 NOT-boundary,
   login-failure section, 409 conflict messaging); now expanded
   to include the Add-Existing-Identity dialog UX (v0.5.13-17)
   and the BYOD CLI breaking change in v0.5.18 (old aw on BYOD
   now hits 422; new aw 1.18.8 requires explicit `--username`).
   Athena reviews tech-accuracy; I review framing.
3. **Athena lands the Playwright-MCP reproducer for Add-Existing.**
   Reproducer-as-gate (policy 12) for the UI surface that
   generated five iterations. Status not visible from my surface
   yet today; check next wake-up.

This week, beyond today:

1. **First distribution action.** The "5 agents" blog post draft has
   sat since 2026-04-09 awaiting Juan's voice pass. Iris not yet
   online; until she is, this is an open priority that hasn't moved.
2. **KI#1 closure decision record.** Athena drafts technical content
   (cert-presentation auth correction + aalk continuity arc + 1.18.6
   trust-model arc + Aida 4/4 attestation); I frame.
3. **Bring Iris and Metis online.** Directories exist; identity setup
   pending Juan-interactive Hetzner work.
4. **Mia's aalr.2 (AWID ensure-team + ac persist refactor)** when
   branch-ready. Will exercise the gate chain again with a feature
   change rather than a bug-fix.

## Product readiness

- **OSS aweb**: stable. Latest tags `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27). No commits on
  main since.
- **aweb-cloud**: live at v0.5.18. `https://app.aweb.ai/health`
  reports `release_tag=v0.5.18`, `aweb_version=1.18.6`,
  `git_sha=4ace9770`, `awid_service_version=0.5.3`. db / redis /
  awid / coordination_api healthy. Started 2026-05-02 19:50 UTC.
  Shipped through Hestia's first end-to-end gate-chain exercise
  (claim-human router validate-first/write-last refactor +
  atomic cli_signup-upgrade UPDATE; closes the cli_signup orphan
  vector at claim time).
- **aw CLI**: 1.18.8 published. Removes BYOD-domain-as-username
  auto-inference. BYOD users on old aw now hit 422; managed
  (.aweb.ai) unaffected. New aw on either works.
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

## Compat policy (post multi-instance resolution)

A Sofia-instance divergence on the compat-scope question (N=1 vs
N=2) was resolved by Juan midday 2026-05-02. Canonical Sofia is the
N=2 voice. **Compat policy: cloud tests against current released
aw + prior 2 released versions = 3 binaries in the compat-test
invocation** (definition is "whatever the prior two released semver
tags happen to be" — patches in normal weeks, mixed during
minor-bump cycles, NOT strict semver-minor).

Decision record deferred until bless-and-run evidence per Athena's
defer-pending-evidence discipline. Implementation lives in Athena's
correctives — Mia (`6627836c`) and Hestia (`a5afc809`); Mia owns
wiring multi-version compat infra when convenient. Hestia's runbook
compat-scope section is currently in-flux state (revert `92f6fc2`
predates the resolution); will re-fold to N=2 when Hestia's next
runbook pass picks it up.

YC public-facing claim deferred behind bless-and-run evidence per
the sequencing in the same correctives.

## Open questions

- Target YC batch and deadline. Pacing for the YC agent depends on this.
- First concrete distribution action this week — Iris needs a target
  once she's online.
- Collision video before or after the first blog post? (Open from
  prior wake-up.)
- BYOD CLI breaking change in v0.5.18 was borderline on the
  "behavior change customers will notice" Sofia-involvement
  threshold. Hestia's call to ship without me was right (small BYOD
  user count today, framing in verified-live mail is honest, no
  public claim made). As BYOD users grow, the threshold may need
  refinement. Mental note for now; revisit when Iris/Metis are
  online and we have a real customer-base picture.
