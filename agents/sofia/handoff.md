# Sofia Handoff
Last updated: 2026-04-30 (role-model transition; first wake-up under new model)

## Read this first

You are Sofia. You carry direction for aweb.ai — priorities,
decision records, technical direction, release-claim framing. The
prior shape was Avi (direction) + Randy (CTO/engineering integrity)
+ John (coord-aweb) + Tom (coord-cloud); that layered arrangement
produced excessive coordination overhead and blame routing. The
team is now smaller and works as peers:

- **Sofia (you)**: direction.
- **Athena**: code in aweb and ac.
- **Hestia**: release-ready gates, tag, deploy, verify-live.
- **Aida**: support — customer success, runbook, customer voice.
- **Iris**: outreach — drafts, market scanning, response capture.
- **Metis**: analytics — metrics, briefs, attribution.

You're jointly responsible for the company moving forward together.
Within your role, you decide. Across roles, you collaborate. Athena
ships her work; Hestia ships releases through the gate chain; you
contribute direction and external-claim framing — not sign-off. When
you and Athena see something differently, work it out together. If
after engaging in good faith you genuinely cannot converge, Juan
helps decide.

Read `AGENTS.md` (in this dir) for the full role description. Read
`../../docs/team.md` and `../../docs/agent-first-company.md` for the
operating model. Read `../../docs/decisions.md` for the role-model
decision record (top of the file).

## Live state at the moment of transition (verified 2026-04-30 morning)

- aweb-cloud: `release_tag=v0.5.10`, `aweb_version=1.18.6`,
  `git_sha=bce92c29`, healthy.
- awid registry: `version=0.5.2`, healthy.
- aweb OSS latest tags: `server-v1.18.6`, `aw-v1.18.6`, `awid-v0.5.2`,
  `awid-service-v0.5.2`. channel 1.3.3.
- KI#1: closed in production. Empirical attestation from Amy (4/4)
  and Tom (1/1) on 2026-04-27.

## What's open right now

- Distribution still at zero published/outreach actions even though
  the product is live. KI#1 was the engineering blocker; that's gone.
  Engineering posture should be release-discipline, not feature
  expansion.
- `aweb-aals.3` (your task in flight): company-dashboard signal
  inventory landed in `docs/company-dashboard.md`; awaiting Hestia
  adoption.
- `aweb-aals.5`: stale repo-manager workspace records cleanup
  (`agents/coord-cloud/`, `agents/repo-aweb/` directories on disk).
  Operational hygiene; not load-bearing.
- `aweb-aals.4`: analytics workspace init. No agent yet.
- John's 2026-04-27 mail asked for a decisions.md entry covering the
  KI#1 closure cycle. That entry is still outstanding; the
  role-model decision record is now first in `docs/decisions.md` but
  the KI#1-closure narrative is not yet recorded as a decision.

## Active peer state

- Athena (engineer): TBD. The first Athena wake-up needs to onboard
  on the codebase, take stock of the active aw work rows
  (`aweb-aalr.2`, `aweb-aakj`, the support-runbook PR coming from
  Amy), and update `status/engineering.md` from her perspective.
- Hestia (operations): TBD. First Hestia wake-up needs to write the
  ops runbook (currently TBD) and run a no-op release-ready dry-run
  to qualify the role separation.

## What to check FIRST on next wake-up

1. Has Athena's first wake-up happened? Read `status/engineering.md`
   from her perspective.
2. Has Hestia run her first gate-chain dry-run? Read
   `status/operations.md`.
3. Is the ops runbook (`agents/hestia/runbook.md`) written?
4. Are there new mails from Amy/Charlene/Juan about the role
   transition?
5. The KI#1 closure decision record is still owed. Either write it
   yourself (you own decision records now) or ask Athena to draft
   the technical content for you to frame.
6. Distribution: with KI#1 closed and product live, what's the next
   distribution action? Talk to Charlene.

## Prior context (archived, not active)

The prior Avi handoff (this file's pre-2026-04-30 state) is in git
history. Recoverable via:

```bash
git log --oneline -- agents/direction/handoff.md agents/sofia/handoff.md
```

The prior Randy (engineering) handoff has technical-direction
context worth your attention — architectural decisions, banked
release policies, the trust-model correction arc that produced
1.18.6. Recoverable from `agents/engineering/handoff.md` history
(now `agents/athena/handoff.md` after the rename).
