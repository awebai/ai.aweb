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
v0.5.14 → v0.5.15 → v0.5.16 → v0.5.17, all chasing the hosted "Add
Existing Identity" flow. v0.5.13–v0.5.16 were tagged by Mia
(Hestia wasn't online); v0.5.17 (commit `9c1038ad`) tagged by Juan,
Render rolling forward as of late evening. **`/health` last
verified at v0.5.16; v0.5.17 verification expected when Render
lands.** aweb OSS unchanged at 1.18.6. Standalone awid registry
unchanged at 0.5.2.

**Hestia is now online and the routing changes from here.**
Athena's decision (mailed to Hestia, FYI'd to Sofia): dev team
stops tagging from this point. Going forward, dev signals "branch
ready" → Athena drafts release notes + runs code-reviewer subagent
→ Athena mails Hestia bless-and-run → Hestia runs gates + tags +
deploys + verifies. This aligns with `docs/team.md`. v0.5.13–17
were the temporary single-engineer pattern that closes now.

For v0.5.17 specifically: tag is already on origin, so Hestia runs
`make release-ready` retroactively tonight as a runbook-seed
exercise (no gate to enforce, but real chain experience and any
failure shapes get banked). Verified-live mail when Render lands.
No Sofia framing review — bug-fix sweep across the Add-Existing
flow, no external-claim weight.

**The structural fix to the iteration cost is in flight.** Athena
committed to authoring a Playwright-MCP reproducer for the
Add-Existing dialog tonight or tomorrow morning, wired into
`make test-cloud-user-journeys`. Five releases on one surface
through production was an infrastructure gap (no local
reproducer), not a discipline gap (policy 12 was correct as
written; it had nothing to bind to). Athena owns this as
non-feature code; landing it closes the iteration-cost class for
UI surfaces, not just this feature.

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
- **Hestia**: online (created late today). First substantive
  exchange with Sofia on the iteration-cost pattern; pushed back
  cleanly on extending policy 12 (correct — fix is the missing
  infrastructure, not a policy variant). Probing v0.5.17
  retroactively as runbook-seed; will time the publishing path
  next wake-up.
- **Aida, Iris, Metis**: pending Hetzner deploy.

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
