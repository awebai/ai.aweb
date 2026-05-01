# Product Status

Last updated: 2026-05-01 (Sofia, second wake-up under new model)

## Current focus

The product is live and engineering has continued shipping. Cloud
moved from v0.5.10 → v0.5.11 → v0.5.12 across the afternoon/evening
of 2026-04-30; current /health reports `release_tag=v0.5.12`,
deployed 2026-04-30 20:07 UTC, uptime ~12h. Four ac commits sit past
v0.5.12 on main (admin actor default + cross-scope hard-delete
hardening). aweb OSS unchanged since 2026-04-27.

The role separation is **not yet real at the runtime layer.** v0.5.11
and v0.5.12 shipped without going through Hestia's gate chain
(workspace status shows only Sofia active; no Hestia wake-up since
the rename, no `agents/hestia/runbook.md` written, no identity setup
performed). That is a meaningful operational observation: under the
prior shape these would have been Tom→Randy releases; under the new
shape they should be Athena-signal→Hestia-gate-chain. Right now the
model exists in docs only.

The Athena-dispatch decision landed today (commit `4491df5`,
docs/decisions.md top entry): Athena owns the code; ephemeral
builder+reviewer pairs author feature changes, with Athena reviewing
diffs against invariants before they land. Phase 1 = Juan spawns
manually; Phase 2 = `aw spawn-pair` primitive (itself a feature
change, will be one of the first pair-authored deliverables).

This week, in priority order:

1. **Get Hestia exercising the gate chain.** Either the next ac
   release goes through her end-to-end or the role separation stays
   theater. Runbook + identity setup are the unblockers.
2. **Distribution still at zero.** No published post, no daily
   brief, no recorded conversation. Engineering's side has been
   green for days; the bottleneck is starting outreach.
3. **Land Aida's v0.5.10 runbook PR with the customer-visible
   deltas** (1.9 NOT-boundary, login-failure section, 409 conflict
   messaging). Note: now it's also a v0.5.10/.11/.12 sweep — Aida
   should check whether v0.5.11 (admin AWID namespace release) or
   v0.5.12 (B.3b hosted custodial CLI coverage) introduce any
   customer-visible deltas worth folding in.
4. **Engineering posture stays release-discipline + invariant
   correctness.** No feature expansion. v0.5.11/.12 fit that mode.

## Product readiness

- **OSS aweb**: stable. Latest tags `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27). No commits on
  main since.
- **aweb-cloud**: live at v0.5.12. `https://app.aweb.ai/health`
  reports `release_tag=v0.5.12`, `aweb_version=1.18.6`,
  `git_sha=962dd163c59875c5a7aebfbaf88b1a4b889f2dd4`,
  `awid_service_version=0.5.1`. db/redis/awid/coordination_api
  healthy. Started 2026-04-30 20:07:14 UTC. **Four commits past
  v0.5.12 on ac main**, no release candidate flagged.
- **awid registry**: live at `version=0.5.2`, redis/db/schema
  healthy. Unchanged since 2026-04-27.
- **@awebai/claude-channel**: 1.3.3 published.
- **Landing site (aweb.ai)**: live. Blog section still TBD; first
  personal/problem post planned for juanreyero.com.

## Outreach state

- **Blog post "5 agents"**: draft ready since 2026-04-09. Awaiting
  Juan's voice pass. Iris owns the packaging.
- **Contacts**: identified in `co.aweb` (private), uncontacted.
- **Daily scanning**: not running.
- **Conversations joined**: 0.

No movement since yesterday's wake-up.

## Support / user feedback

- KI#1 closed empirically (Aida 4/4 + a second-shape probe on
  2026-04-27). No regression observed across the 2026-04-30
  releases.
- Aida's runbook PR with the v0.5.10 customer-visible deltas is the
  in-flight product-facing artifact. v0.5.11 + v0.5.12 may add to
  it; Aida to scope on next wake-up.
- No external user feedback recorded in public status.

## Priorities

1. **Exercise the Hestia gate chain on the next ac release.** Until
   that happens, the role separation is documentation. Runbook +
   identity setup are the unblockers; both pre-conditions named in
   `status/operations.md`.
2. **Reactivate distribution.** Engineering side has been green for
   five days. Iris drafts, Juan/Eugenie publish, Metis records the
   signal.
3. **Land the Aida runbook PR**, expanded to cover any v0.5.11/.12
   deltas if applicable.
4. **KI#1 closure decision record (still owed).** Sofia drafts the
   framing; Athena supplies technical content for the cert-
   presentation auth correction. Goal: one decision record covering
   the aalk continuity + 1.18.6 trust-model arc + empirical
   attestation, so the closure narrative is durable.

## Open questions

- Does the next ac release go through Hestia's gate chain, or do
  more releases ship past her under the prior workflow? Decision is
  Athena+Hestia's once Hestia wakes; Sofia's contribution is
  framing — the role separation is theater until exercised at least
  once.
- Are v0.5.11 and v0.5.12 worth a verified-live mail in retrospect,
  or do we accept that they shipped before Hestia was online and
  move on? (Lean: accept; the verified-live discipline applies
  going forward, not retroactively. Hestia's call when she wakes.)
- Does the collision video belong before or after the first blog
  post? (Open since last wake-up.)
- What's the first concrete distribution action this week? Iris
  needs a target.
