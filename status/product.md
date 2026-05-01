# Product Status

Last updated: 2026-05-01 evening (Sofia, after dev team came online)

## Current focus

Today is **team-genesis day.** Sofia, Athena, and the YC agent came
online in the company team (`default:aweb.ai`); Athena is now also
in the dev team (`aweb:juan.aweb.ai`) and that team has activated —
Mia is the first dev online. Athena confirmed cross-team chat works
bidirectionally.

The dispatch shape has resolved: the "ephemeral pairs" sketch in
commit `4491df5` was speculative; the real arrangement is a
permanent dev team in its own cryptographic namespace, with Athena
spanning both teams (architecture/invariants/review on the company
side; brief and review of dev work on the dev side). Mia / Noah /
Grace / Kate are the dev pool. Athena reviews; devs author and
ship.

The product moved a lot today. Cloud rolled v0.5.12 → v0.5.13 →
v0.5.14 → v0.5.15 → v0.5.16, all by Mia chasing the hosted "Add
Existing Identity" flow. **`/health` verified at v0.5.16
(`git_sha=842e0b5b`, deployed 2026-05-01 20:45 UTC). awid library
inside cloud bumped to 0.5.3** (was 0.5.1 this morning). aweb OSS
unchanged at 1.18.6. Standalone awid registry unchanged at 0.5.2.

These four releases shipped without Hestia (who isn't online yet).
The build/ship boundary doesn't exist as a runtime structure
today — Mia is shipping under the prior single-engineer pattern.
That's expected at genesis; once Hestia is up, the next release
should route through her gate chain. Worth watching: 4 releases in
a day on a single feature suggests iterative-fix-and-bisect; the
Add-Existing-Identity flow is non-trivial.

YC agent (`aweb.ai/yc`, `co.aweb/agents/yc/`) is the third agent
online. Special-purpose, not a permanent surface. Caught a pricing
inconsistency on first wake-up (fixed; commit `2fbf16f`), then
rewrote `positioning.md` and its own `AGENTS.md` into substantially
sharper, fact-checked artifacts.

## Today's priorities

1. **Deploy the permanent team to Hetzner.** Hestia/Aida/Iris/Metis
   come online via this work. Juan's hands today since Hestia is
   being deployed by it.
2. **Start blog posts + outreach.** The "5 agents" draft has been
   sitting since 2026-04-09; first action is moving it through the
   founder voice pass and getting it published.
3. **YC application** — agent is staged and the positioning is
   sharp; founder material and batch deadline are the next-step
   inputs from Juan.

This week, beyond today:

1. **Get Hestia exercising the gate chain on the next ac release.**
   Today's 4-release sprint shows shipping velocity is real;
   inserting Hestia for the next one starts the runbook emerging
   from notes during the joint exercise.
2. **Land Aida's runbook PR** when she comes online. Original scope
   was v0.5.10 deltas (1.9 NOT-boundary, login-failure section, 409
   conflict messaging); now expanded — Aida should sweep across
   v0.5.10 through v0.5.16 for any customer-visible changes,
   especially around the new "Add Existing Identity" flow Mia just
   landed.
3. **KI#1 closure decision record.** Athena drafting technical
   content; Sofia frames once she sends it.

## Product readiness

- **OSS aweb**: stable. Latest tags `server-v1.18.6`, `aw-v1.18.6`,
  `awid-v0.5.2`, `awid-service-v0.5.2` (2026-04-27). No commits on
  main since.
- **aweb-cloud**: live at v0.5.16. `https://app.aweb.ai/health`
  reports `release_tag=v0.5.16`, `aweb_version=1.18.6`,
  `git_sha=842e0b5b`, `awid_service_version=0.5.3`. db / redis /
  awid / coordination_api healthy. Started 2026-05-01 20:45 UTC.
  Four releases shipped today by Mia (v0.5.13–v0.5.16), all
  chasing the hosted Add-Existing-Identity flow.
- **awid registry (standalone)**: live at `version=0.5.2`,
  redis/db/schema healthy. Unchanged. (The awid library inside
  cloud bumped independently to 0.5.3.)
- **@awebai/claude-channel**: 1.3.3 published.
- **Landing site (aweb.ai)**: live. Blog section TBD; first
  personal/problem post planned for juanreyero.com.
- **Pricing in public docs**: aligned to canonical $25/$250 per
  `ac/backend/src/aweb_cloud/models/billing.py` (commit `2fbf16f`,
  caught by YC agent on first wake-up).

## Team state (genesis day)

Company team (`default:aweb.ai`):

- **Sofia (me)**: online. Direction surface.
- **Athena**: online. Engineering surface; reviews code, holds
  invariants, drafts release notes for the company side. Spans
  into the dev team.
- **YC agent (`aweb.ai/yc`)**: online. Special-purpose for the YC
  application. First-day output already strong.
- **Hestia, Aida, Iris, Metis**: pending Hetzner deploy.

Dev team (`aweb:juan.aweb.ai`):

- **Athena**: cross-team membership.
- **Mia**: active. Shipped today's v0.5.13–v0.5.16 cluster. Gave
  Athena a clean handoff on `aweb-aalr.2`; persist-refactor starts
  tomorrow morning.
- **Noah, Grace, Kate**: in the team; activity not yet visible
  from my surface. Athena will know.

## Outreach state

- **Blog post "5 agents"**: draft ready since 2026-04-09. Awaiting
  Juan's voice pass. Iris will own packaging once online.
- **Contacts**: identified in `co.aweb` (private), uncontacted.
- **Daily scanning**: not running.
- **Conversations joined**: 0.

## Support / user feedback

- KI#1 closed empirically (4/4 attestation + second-shape probe on
  2026-04-27). No regression observed across today's releases.
- The hosted Add-Existing-Identity flow is new customer-facing
  surface that landed today across v0.5.13–v0.5.16. Aida should
  scope a runbook section for it once she's online.
- No external user feedback yet — distribution hasn't started.

## Open questions

- Target YC batch and deadline. Pacing for the YC agent depends
  on this.
- First concrete distribution action this week — Iris needs a
  target once she's online.
- Collision video before or after the first blog post? (Open
  from prior wake-up.)
- Once Hestia is online, does the gate chain start with the next
  release, or does Mia's prior shipping pattern continue while
  Hestia builds the runbook? Athena + Hestia decide; Sofia frames
  external claims.
