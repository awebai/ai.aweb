# Publishing History

What we published, where, and when. Newest first.

Per `publishing/runbook.md` Case 6: each entry captures date,
channel, public link, artifact used, humans who acted, observed
signal, attribution caveat.

---

## 2026-05-11 · aweb.ai homepage refresh (Pass-3) — verified-live

**Channel**: aweb.ai (landing page)
**Public link**: https://aweb.ai/
**Artifact**: ac main branch deploy-landing at commit `60be8f4e`
(originally Sofia-authored on `deploy-landing-staging`,
fast-forwarded to `deploy-landing` for production)
**Source-of-truth doc**: `docs/customer-onboarding-flows.md`
(customer-shape model, Shape A / Shape B / Shape C, established
2026-05-11 by Sofia)
**Narrative record**: `publishing/drafts/2026-05-09-homepage-copy-refresh.md`

### What changed

Hero h1 + subhead reframed around concrete customer surfaces
(Claude Desktop / ChatGPT / claude.ai) instead of vocabulary-
translation framing ("those are agents") that confused vs. served
the audience.

NEW works-with strip between hero and pillars (text pills,
4 items: Claude / ChatGPT / Claude Desktop / Any MCP-compatible
AI). NEW "Sign up. Add aweb to your AI client." section with
honest 3-step walkthrough (signup + hosted identity → copy MCP
URL → add to client + approve OAuth) targeting Shape A custodial-
MCP customers. Per-client snippets for claude.ai web /
ChatGPT web / Claude Desktop.

Pillars section heading text replaced from "Give each agent an
identity. Then let them coordinate." to "Each AI you're running
is isolated. aweb changes that."

Team-quickstart section relabeled "For developers" — the
agent-guide-paste prompt (CLI-shape onboarding) lands there
as the Shape B customer entry point. Hosted MCP block
repurposed as MCP technical-detail callout.

### Cycle arc

- **2026-05-08**: Bertha brief (chat `53251bb9`) — Eugenie
  observed a non-technical founder running multi-Claude not
  recognizing "agents" as describing her situation.
- **2026-05-09**: Iris-authored bundle in publishing/drafts/.
  Sofia framing-pass landed; Athena agent-guide pre-flight
  flagged four human-required steps in the autonomous-install
  flow. Two-state-transition framing engineered (Option A
  interim → Option B post-aang).
- **2026-05-10**: aweb-aang (worktree-creation-on-hosted) +
  three other P0 frictions verified-live across single-team and
  multi-team-agent populations (Pepe Reyero customer-evidence
  arc, banked at `co.aweb/outreach/customer-evidence/2026-05-09-pepe-autonomous-install.md`).
  Iris-authored bundle commit `58ed6c53` to ac main — Pass-1
  briefly deployed and reverted; gate gap caught by Juan
  (Render watching main produced an unintended ship; staging
  gate didn't yet exist).
- **2026-05-10 → 11**: Athena seeded `deploy-landing-staging`
  branch + `make deploy-staging` target. Juan configured Render
  staging service. Sofia caught a Pass-2 customer-shape mismatch
  (Shape A customers given Shape B flow) and authored Pass-3
  corrective edits directly under time pressure (commit
  `60be8f4e`). Customer-shape model persisted in
  `docs/customer-onboarding-flows.md`.
- **2026-05-11**: Bertha relay confirmed Eugenie validated Pass-3
  on staging (chat `47e3b6bd`); Juan greenlighted; Sofia framing
  review long-since done. Hestia ran `make deploy-site`,
  verified live at aweb.ai (mail `f0ac616f`).

### Humans who acted

- Bertha relayed Eugenie's brief and validation
- Eugenie reviewed Pass-3 on staging
- Juan greenlighted production
- Sofia authored Pass-3 customer-shape correction directly
  (lane-cross under time pressure; re-routed back to Iris
  for Pass-4 if needed)
- Hestia deployed + verified live

### Observed signal

Not yet observed at history-capture time (deploy ~14:36-14:39Z
2026-05-11). Signal categories to watch over the coming weeks:

- Direct traffic to aweb.ai (week-over-week)
- Signup conversion at app.aweb.ai/register
- Inbound conversations from custodial-MCP customers (Shape A;
  the audience the refresh now actually serves)
- Repo stars / inbound on github.com/awebai/aweb

Metis is the signal-strength reviewer when an action runs;
attribution-strength claims gated through her.

### Attribution caveat

This is one event in a multi-channel pivot following the
2026-05-07 Show HN sink. Any signups / traffic / engagement
movement in the days following this deploy is correlated with
the homepage refresh, not solely caused by it — concurrent
factors include the (still pending) "Two Agents Not One"
juanreyero.com article, the queued direct-outreach drafts
(co.aweb/outreach/daily/), and any organic discovery. Capture
correlation; don't claim causation.

### Disciplines banked from this cycle

In `agents/iris/AGENTS.md`:

- Submit-state changes surface to direction same-shift
  (banked 2026-05-07)
- Verify Pass 1 is shipping (not just drafted) before
  committing to a two-transition framing (banked 2026-05-09)
- Surface gate-stalls to direction explicitly (banked 2026-05-09)
- `publishing/drafts/*.md` is narrative, not a wire-in spec
  (banked 2026-05-10)
- Customer-shape verification before authoring landing-copy
  (banked 2026-05-11; source-of-truth `docs/customer-onboarding-flows.md`)

In Sofia's surface (her banking pending): verify the empirical
customer-facing surface before claiming a state transition or
triggering downstream dispatches based on it.

### Operational firsts

- First cycle through the new staging-first deploy gate
  (Render: deploy-landing for production, deploy-landing-staging
  for staging). The gate caught one out-of-order deploy mid-cycle
  (Pass-1 hit production via Render-watching-main before staging
  branch existed); the gate fix landed and Pass-3 ran through
  cleanly.
- First entry in this `publishing/history.md` artifact.
