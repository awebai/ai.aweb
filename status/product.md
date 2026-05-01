# Product Status

Last updated: 2026-05-01 (Sofia, team-genesis day)

## Current focus

Today is **team-genesis day.** Sofia, Athena, and the YC agent are
the first three online. Plan today: deploy the permanent team to
Hetzner so they live persistently, then start blog posts and
outreach. The remaining surfaces (Hestia, Aida, Iris, Metis) come
online with that deploy.

Earlier framing in this doc treated those surfaces as if they had
existed and "hadn't woken." That was wrong — they didn't exist
yet. Correct framing: the team is being launched, not failing to
activate.

The product is live and stable. Cloud is at v0.5.12 (verified on
`/health` 2026-05-01). aweb OSS unchanged since 2026-04-27. **Five
commits past v0.5.12 on ac main** — Athena flagged a coherent
candidate for v0.5.13 (ship-gate fix, admin actor default,
cross-org hard-delete preservation + hardening, retired-user
soft-delete filter on the auth path). She's holding signal until
Hestia comes online with runbook + identity setup so the first
release exercises the build/ship boundary cleanly.

Athena owns code (architecture, invariants, review, non-feature
code) — that part stands. The spawn-pair dispatch shape in commit
`4491df5` is speculative; the real arrangement is being set up
today, with Athena and Juan creating a separate cryptographic team
for the dev work. The decision record from `4491df5` should be
read as one early sketch, not a committed model.

YC agent (`aweb.ai/yc`, lives in `co.aweb/agents/yc/`) is the third
agent online today. Special-purpose agent for the Y Combinator
application; not a permanent surface. Caught a pricing inconsistency
in public docs on first wake-up (fixed; commit `2fbf16f`), then
rewrote `positioning.md` into a sharper, fact-checked version with
the right transparency caveats — a substantial upgrade over the
starter I wrote.

## Today's priorities

1. **Deploy the team to Hetzner.** Hestia/Aida/Iris/Metis come
   online via this work. Juan's hands today since Hestia is being
   deployed by it.
2. **Start blog posts + outreach.** The "5 agents" draft has been
   sitting since 2026-04-09; first action is moving it through the
   founder voice pass and getting it published.
3. **YC application** — agent is staged; founder material and batch
   deadline are the next-step inputs from Juan.

This week, beyond today:

1. **Exercise the Hestia gate chain on the next ac release.** With
   five commits past v0.5.12 on main, the v0.5.13 candidate is the
   natural first exercise. Athena holding signal until Hestia is
   live and the runbook starts emerging from notes during that
   first joint release.
2. **Land Aida's runbook PR** when she comes online — covers
   v0.5.10 customer-visible deltas (1.9 NOT-boundary,
   login-failure section, 409 conflict messaging), and Aida to
   scope whether v0.5.11/.12/.13 add anything.
3. **KI#1 closure decision record.** Athena is drafting technical
   content next; Sofia frames once she sends it.

## Product readiness

- **OSS aweb**: stable. Latest tags `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27). No commits on
  main since.
- **aweb-cloud**: live at v0.5.12. `https://app.aweb.ai/health`
  reports `release_tag=v0.5.12`, `aweb_version=1.18.6`,
  `git_sha=962dd163`, `awid_service_version=0.5.1`.
  db/redis/awid/coordination_api healthy. Started 2026-04-30
  20:07:14 UTC. **Five commits past v0.5.12 on ac main** — coherent
  v0.5.13 candidate per Athena.
- **awid registry**: live at `version=0.5.2`, redis/db/schema
  healthy. Unchanged since 2026-04-27.
- **@awebai/claude-channel**: 1.3.3 published.
- **Landing site (aweb.ai)**: live. Blog section TBD; first
  personal/problem post planned for juanreyero.com.
- **Pricing in public docs**: aligned to canonical $25/$250 per
  `ac/backend/src/aweb_cloud/models/billing.py` (commit `2fbf16f`,
  caught by YC agent on first wake-up).

## Team state (genesis day)

- **Sofia (me)**: online. Direction surface.
- **Athena**: online. Engineering surface. Working with Juan to
  set up the actual dev team in a separate cryptographic team
  (this supersedes the speculative spawn-pair shape in commit
  `4491df5`). Drafting KI#1 closure technical content; will run
  code-reviewer subagent on the v0.5.13 5-commit cluster before
  signaling Hestia.
- **YC agent (`aweb.ai/yc`)**: online. Special-purpose. First
  wake-up produced clean cross-surface work (pricing fix).
- **Hestia, Aida, Iris, Metis**: pending Hetzner deploy.

## Outreach state

- **Blog post "5 agents"**: draft ready since 2026-04-09. Awaiting
  Juan's voice pass. Iris will own packaging once online.
- **Contacts**: identified in `co.aweb` (private), uncontacted.
- **Daily scanning**: not running.
- **Conversations joined**: 0.

## Support / user feedback

- KI#1 closed empirically (Aida 4/4 + a second-shape probe on
  2026-04-27). No regression observed across the 2026-04-30
  releases.
- No external user feedback yet — distribution hasn't started.

## Open questions

- Target YC batch and deadline. Pacing for the YC agent depends
  on this.
- First concrete distribution action this week — Iris needs a
  target once she's online.
- Collision video before or after the first blog post? (Open
  from prior wake-up.)
