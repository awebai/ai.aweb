# Sofia Handoff

Last updated: 2026-05-02 morning (Day-2 of team-genesis)

## Read this first

You are Sofia. You carry direction for aweb.ai — priorities, decision
records, technical direction, release-claim framing. Read `AGENTS.md`
(in this dir) for the full role description. Read `../../docs/team.md`
and `../../docs/agent-first-company.md` for the operating model. Read
`../../docs/decisions.md` top entries for recent direction shifts.

You are jointly responsible with Athena, Hestia, Aida, Iris, and
Metis for the company moving forward. Within your role, you decide.
Across roles, you collaborate. Athena ships her work; Hestia ships
releases through the gate chain; you contribute direction and
external-claim framing — not sign-off.

## Live state at this wake-up (2026-05-02 morning)

- `app.aweb.ai/health`: `release_tag=v0.5.16`, `aweb_version=1.18.6`,
  `git_sha=842e0b5b`, `awid_service_version=0.5.3`. Started 2026-05-01
  20:45 UTC (~12h uptime). All checks healthy.
- `api.awid.ai/health`: `version=0.5.2`. Healthy. Unchanged.
- v0.5.17 tagged (`9c1038ad`), built, but not deployed — Render is
  manual; Juan hasn't pushed the button. Per Juan's call last night,
  this one ships without Hestia's gate-run + verified-live mail.
- aweb OSS unchanged (1.18.6 / 0.5.2).
- @awebai/claude-channel 1.3.3.

## What changed since last wake-up

- **Aida came online** (commits `571ad94 Created aida`, `ab4f915
  Added keys`). Workspace status shows her active. Her status/handoff
  still pre-rename; will refresh on her own wake-up.
- **Hestia hardened runbook substantially** through the right loop —
  five commits banking real operational discoveries:
  - Render auto-deploy was wrong; Juan deploys manually (`47ee44c`)
  - awid registry also manual-deploy; verify-live table by deploy
    shape (`d951289`)
  - Artifact map + dependency rule + corrected ship semantics
    (`dfdb826`)
  - Folded ac gate-default narrowing + compat-invocation policy
    (`a2b1858`)
  - v0.5.17 retroactive exercise called off by Juan; idle for next
    handoff (`19673ef`)
- **Athena landed ac test-infra work** — five commits attacking the
  iteration cost Hestia flagged: parallelize pytest, reuse migrated
  DB, reuse release image, optional installed-CLI journey, Shipping-
  section update for the new role boundaries. This is the
  non-feature authoring pattern from decision `4491df5`.
- **Playwright-MCP reproducer for Add-Existing** — Athena committed
  to authoring "tomorrow morning fresh-headed". Not yet visible in
  ac main. Today is that morning.
- **No mail/chat traffic.** Quiet morning. The work is in artifacts,
  not coordination chatter.

## What's open right now

- **Aida runbook PR** — original scope was v0.5.10 deltas; now
  expanded to v0.5.10-17 (Add-Existing dialog UX from yesterday's
  cluster). She owns the sweep; Athena reviews tech-accuracy; I
  review framing.
- **Playwright reproducer** lands today (Athena's commitment); will
  close the iteration-cost class for UI surfaces.
- **Build/ship boundary** becomes real on the next ac release —
  likely Mia's aalr.2 when branch-ready, or whichever feature lands
  first. First real exercise of Hestia's gate chain end-to-end.
- **Distribution still at zero.** "5 agents" post (2026-04-09 draft)
  waiting on Juan's voice pass. Iris not yet online to package it.
- **KI#1 closure decision record** — Athena drafts technical content;
  I frame. Pending.
- **Iris + Metis identity setup** — directories exist; AWID/team-cert
  setup pending Juan-interactive Hetzner work.
- v0.5.17 Render deploy — Juan-call when (or whether) to push it.

## Active peer state

- **Athena**: online. Test-infra work last night good response to
  iteration-cost flag. Playwright reproducer expected today.
- **Hestia**: online. Runbook hardening loop is working. Idle for
  next Athena bless-and-run.
- **Aida**: online (came up overnight). Status/handoff still
  pre-rename; she'll refresh.
- **Iris, Metis**: directories only; not active.
- **YC agent**: offline (19h ago); special-purpose, not a permanent
  surface.
- **Mia**: dev team; shipped v0.5.13-17 cluster yesterday; aalr.2
  starts today per Athena's status.

## What to check FIRST on next wake-up

1. **Did the Playwright reproducer land?** Look in ac main for
   `frontend/e2e/add-existing.spec.ts` or similar. If not, ask Athena.
2. **Has Aida refreshed her status/handoff?** Did she scope the
   v0.5.10-17 runbook PR? Read `status/support.md` and her handoff.
3. **Live state:** `curl https://app.aweb.ai/health` and
   `curl https://api.awid.ai/health`. If /health flips to v0.5.17 or
   higher, Juan triggered Render — or a new release shipped through
   Hestia's chain (which would be the FIRST real bless-and-run
   exercise).
4. **New decision records** since `4491df5`?
5. **Mail/chat queue** (`aw mail inbox`, `aw chat pending`).
6. **Mia's aalr.2 branch-ready signal** — first candidate for the
   real build/ship boundary exercise.
7. **Distribution** — has anything moved on the "5 agents" post or
   any other published action?

## Notes for framing

- The runbook hardening Hestia did overnight is exactly the right
  loop: each banked discovery (manual Render, manual awid, verify-
  live by deploy shape) is a real operational truth that would
  otherwise sit as tribal knowledge. The first real bless-and-run
  exercise will validate the rest.
- Athena's test-infra response to the iteration-cost flag is the
  build/ship loop working — Hestia raises cost data, Athena fixes
  the structural cause. No coordination overhead, just the right
  surfaces doing the right work.
- Aida's runbook PR matters because the Add-Existing dialog is the
  newest customer-facing surface and the most likely place a fresh
  user will hit confusion. Tightening the runbook there is direct
  product-readiness work.
- v0.5.17 deploy gap is benign for now — no external claim weight,
  no verified-live mail going out. If a customer-relevant bug
  emerges, it becomes load-bearing; otherwise let Juan's cadence
  drive it.

## Prior context (archived, not active)

The prior Avi handoff is in git history. Recoverable via:

```bash
git log --oneline -- agents/direction/handoff.md agents/sofia/handoff.md
```

The prior Randy (engineering) handoff has technical-direction
context worth your attention if you need to reconstruct the trust-
model correction arc that produced 1.18.6. Recoverable from
`agents/engineering/handoff.md` history (now `agents/athena/`).
