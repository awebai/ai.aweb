# Product Status

Last updated: 2026-04-30 (Sofia, post role-model transition)

## Current focus

The product is live. **Distribution is the bottleneck.** KI#1 (the
last engineering blocker) closed in production on 2026-04-26 with
aweb 1.18.3 and the trust-model architectural correction shipped in
1.18.6 on 2026-04-27. Cloud has been on v0.5.10 since 2026-04-30
05:54 UTC. Engineering's side is green for the first human-led
conversations and the blog-post voice pass.

The team transitioned today (2026-04-30) to three peer working roles
(Sofia / Athena / Hestia) plus user-facing surfaces (Aida, Iris) and
analytics (Metis). See `docs/decisions.md` top entries for the role
model and `docs/team.md` for current bounds.

This week:

1. Run the first distribution action. Iris stages, Juan and Eugenie
   publish/engage, Metis records the signal with attribution limits.
2. Hestia writes the ops runbook and runs a no-op release-ready
   dry-run to qualify the role separation. Until that runs, the
   build-vs-ship boundary is theoretical.
3. AWID identity setup for the renamed agents (Sofia, Athena, Hestia,
   Aida, Iris, Metis) — interactive task for Juan, same shape as
   Amy's 2026-04-21 second-address sequence.
4. Athena absorbs in-flight engineering work (`aweb-aalr.2`,
   `aweb-aakj`) and writes `status/engineering.md` from her
   perspective on first wake-up.
5. Aida's runbook PR with the v0.5.10 deltas (1.9 NOT-boundary,
   login-failure section, 409 conflict messaging) lands; Athena
   does technical-accuracy review, Sofia does product/framing.

## Product readiness

- **OSS aweb**: shipping. Latest tags `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27).
- **aweb-cloud**: live. `https://app.aweb.ai/health` reports
  `release_tag=v0.5.10`, `aweb_version=1.18.6`, `git_sha=bce92c29`,
  `awid_service_version=0.5.1`. db/redis/awid/coordination_api
  healthy.
- **awid registry**: live. `https://api.awid.ai/health` reports
  `version=0.5.2`, redis/db/schema healthy.
- **@awebai/claude-channel**: 1.3.3 published.
- **Landing site (aweb.ai)**: live. Blog section still listed as
  needed for aweb.ai/blog posts; first personal/problem post planned
  for juanreyero.com.

## Outreach state

- **Blog post "5 agents"**: draft ready since 2026-04-09. Awaiting
  Juan's voice pass. Iris owns the packaging.
- **Contacts**: identified in `co.aweb` (private), uncontacted.
- **Daily scanning**: not running.
- **Conversations joined**: 0.

## Support / user feedback

- KI#1 closed empirically (Aida 4/4 + a second-shape probe on
  2026-04-27).
- Aida's runbook PR with the v0.5.10 deltas is the in-flight
  product-facing artifact. See `status/support.md`.
- No external user feedback recorded in public status beyond
  internal attestation and runbook shaping.

## Priorities

1. **Reactivate distribution.** The product side is no longer the
   blocker; running the first distribution action is.
2. **Make the role transition real.** Identity setup + ops runbook
   close the loop on the new model. Until both are done, the
   restructure is cosmetic.
3. **Land Aida's v0.5.10 runbook PR.** Three customer-visible
   additions identified.
4. **Engineering posture stays release-discipline mode**, not feature
   expansion. The 1.18.4–1.18.6 trust-model arc is the correct mode;
   the next product step is usage, not more polish.

## Open questions

- Do we want the collision video before the first blog post, or does
  the blog post publish first now that v0.5.10 is live?
- What's the first distribution action, and what feedback signal does
  Metis record after it runs?
- When does Hestia's first end-to-end ship (under the new model)
  happen, and what release does it qualify on?
