# Sofia Handoff

Last updated: 2026-05-12 (persona priority reorder + UX simplification pass beginning)

## Check first on next wake-up

1. **Persona priority reordered (2026-05-12, Juan's call).**
   New ordering: Personal-AI consumer (P1) → Company with
   AI-using employees (P2) → Developer team (P3, was #1) →
   Platform builder (P4, was #2). Decision record at
   `docs/decisions.md` 2026-05-12. `docs/audiences.md`
   rewritten to add Personas 1+2 and reframe to "persona"
   terminology. Architecture unchanged; what shifts is what
   we reach first, what onboarding optimizes for, what
   landing copy targets, what channels content goes through.

2. **UX simplification pass in flight.** Working artifacts:
   `agents/sofia/ux-surface.md` (inventory snapshot) +
   `agents/sofia/ux-surface.html` (persona-colored surface
   map). Athena mailed (conv 70f1c868) to converge on a
   cut list before either of us proposes externally.
   Specific simplification candidates listed in the mail:
   the "Two Paths" duplication, /connect-in-two-places,
   Identities-vs-Contacts overlap, auth-page near-dupes,
   MCP duplicate verbs (contacts_list vs list_contacts,
   wrap-tools), 3 first-time-user surfaces. Awaiting
   Athena's read. Juan's next ask after that converges:
   actually do the simplification cut.

3. **docs/customer-onboarding-flows.md is gone — Juan's call**
   (commit 47a9558, 2026-05-12). The customer-shape discipline
   it carried is now absorbed across three surfaces: aweb-aanp
   brief (dev team, Athena's surface — request relay if
   needed), publishing/voice.md (Iris's surface, reads cleanly
   from Sofia), and each agent's AGENTS.md operational
   application. Sofia AGENTS.md updated to reflect the new
   authority chain. The discipline itself remains
   non-skippable for landing/onboarding copy review.

2. **Pass-3 is LIVE at aweb.ai** — verified 2026-05-10 14:51Z.
   End-to-end gate cycle (catch → fix → stage → validate →
   greenlight → deploy → verify-live) completed in ~3 hours.
   Customer-shape discipline banked in Sofia + Iris + Hestia
   AGENTS files; ask Aida to adopt next time she's active.
2. **Customer-shape discipline now persistent.**
   `docs/customer-onboarding-flows.md` is the new must-read
   before any landing-copy review. Sofia AGENTS.md updated to
   read it on every wake-up; Iris and Aida invited to do the
   same. The discipline that prevents the Pass-2 miss recurring.
3. **Bertha cross-namespace addressing.** The full-form address
   `eugenie.aweb.ai/bertha` 404s from BOTH Sofia and Athena
   (Athena confirmed in mail 9682a171); not a Sofia team-context
   limit, an AC routing issue. **Bare alias `bertha` resolves
   cross-namespace cleanly** — that's the working form. The
   `/v1/directory` lookup endpoint also 404s (separate AC issue,
   low frequency, no customer impact, not surfaced as engineering
   ticket per Athena's call).

   For future Bertha mail, try `aw mail send --to bertha` first;
   fall back to relay via Athena if bare alias resolution starts
   failing (it works today).

4. **Branch protection on ac deploy-landing pending Juan.**
   Hestia recommended PR-based with Juan + Sofia as approvers
   (mail ab09f148); Sofia voted yes (mail in conversation
   878c06b1). Juan holds GitHub repo admin; will implement when
   convenient. No urgency.

## Pass-3 cycle (2026-05-10) — what shipped to staging

- Hero: H1 line-broken + 'AI agents'; subhead reframed around
  Claude Desktop/ChatGPT/claude.ai surfaces; right column
  3-step MCP connector card replaces npm install
- 'Sign up' section: 3-step MCP walkthrough with per-client
  snippets (claude.ai/ChatGPT/Claude Desktop)
- 'Team quickstart' rebranded 'For developers' with the
  agent-guide-paste prompt landed there
- 'Hosted MCP' block repurposed as MCP technical detail
- ac commit 60be8f4e on deploy-landing-staging
- Render auto-deployed at 11:55:53Z; verified live via Playwright

Sofia authored ac/site/ edits directly under Juan's time
pressure ('when I come back I want to see the new preview
online'). Discipline #29 honored: actual edits to source
surface, not interpretive markdown. Crossed Iris's normal
authoring lane; explained in mail 4d3f3053.

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
- **No mail/chat traffic** at first wake-up. Quiet morning. The work
  was in artifacts, not coordination chatter.

## Mid-day: support-window thread + attribution incident

- **Athena mailed me** (`e3f64ff4`) asking for the call on the aw
  support-window meta-policy that surfaced from her gate-policy
  refinement work with Mia. Real direction question in my lane.
- **I replied** (`f41c7c01`): N=1 (current + immediately prior released
  aw, internal compat-test only) plus a public/internal split (no
  customer-facing support-window promise; "use current aw" implicit).
  Reasoning: YAGNI at 44-user dogfooding scale, distribution > features,
  N=1 is a floor not a ceiling, reversible.
- **Athena's first reply** (`0f8733e9`) read it correctly as N=1 and
  said she was forwarding to Mia and Hestia.
- **Three subsequent mails** in the thread attributed an N=2 position
  to me that I never sent — citing invariant 5, the aw 1.18.5→1.18.6
  cadence, and eventually reattributing my own `f41c7c01` as the "N=2
  update," which contradicted Athena's own first ack.
- **Defensive sweep**: mail to Athena (`336a0558`) requesting she
  quote `f41c7c01`'s body as her instance reads it; mail to Hestia
  (`dca1fbca`) saying do not update runbook based on N=2 framing
  attributed to me. Mia not reachable from my workspace (`agent not
  found: mia` — she's dev-team only; only Athena bridges).
- **Hestia had already committed N=2 attribution to the runbook**
  (`0d53e93`, ~13:12) off an "Athena" mail before mine arrived. She
  saw mine and pulled the attribution back surgically (`646968d`,
  ~13:14): scope marked in-flux between Sofia (N=1) and Athena (N=2),
  operational rule unchanged (it's surface-agnostic), no public-claim
  change. Runbook is in the right state.
- **Open**: I have NOT received Athena's authenticated reply to my
  verification request (`336a0558`) at the time of this update.
  Whether the cause was real-Athena local-context corruption or
  something at the trust layer is unresolved. Juan flagged.

## Banked from this incident

- Defensive FYI to a downstream agent who may have already acted on
  a misattributed position works. The asymmetric cost favors a quick
  "do not wire" mail over waiting for full thread resolution.
- Hestia's pullback shape is the right template: remove attribution,
  mark scope as in-flux, preserve the surface-agnostic operational
  rule. Don't take a side; don't roll back the whole section.
- Decision records should wait for protocol-layer convergence between
  proposer and reviewer, not channel-layer text. Per the operating
  model, the canonical artifact is the cryptographically-signed mail,
  not the conversational reading of it.

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
