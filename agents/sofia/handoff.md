# Sofia Handoff

Last updated: 2026-05-26 (pivot to outreach; corpus / aweave-fold work paused safely)

## Check first on next wake-up

1. **`aw mail inbox`** — primary signal. Specifically watch for:
   - Iris reply to the outreach-pivot ramp-up (msg `e1b6c7d0` in conv `345f95bb`). She is the lead on the outreach lane now; her read of the priorities shapes Sofia's next moves.
   - Marvin reaction (if any) to the fold + corpus rename direction mail (msg `4f55b529` in conv `adb6cc44`) and/or the courtesy "paused" follow-up (msg `352e5921` same conv). If he replies, the corpus arc may surface back to active.
   - Hestia reactions on anything operational from a new release.
2. **`aw chat pending`** — sync-blocked peers.
3. **Live state**: `curl https://app.aweb.ai/health` and `curl https://api.awid.ai/health`. Last verified-live 2026-05-23 22:17 (v0.5.47 → v0.5.48 cluster framing-acked in conv `878c06b1`); the cluster is fully cleared for external derivation with the `"All"` / `"Team and contacts"` customer-label naming.
4. **`docs/decisions.md` tail** — any entries newer than this handoff.
5. **`status/outreach.md`** — Iris's current focus signal. As of 2026-05-16 her status was post-ship monitoring on a homepage bundle; the pivot will move that forward.

## Active arc: pivot to outreach (2026-05-26)

**Triggered by**: Juan, citing an advisor he respects who said no startup succeeds with more than one site to develop and promote, then escalating to "we need to start seriously doing outreach" with the Pi extension as a key promotion target.

**My posture**: stand back, bring Iris in, scope opportunities + reorganize past work both in `ai.aweb/publishing/` and in `~/prj/beadhub-all/`.

**Done this turn**:
- Surveyed Iris's surface (`agents/iris/AGENTS.md`, `handoff.md`, `publishing/voice.md`, `publishing/plan.md`, `publishing/history.md`, `status/outreach.md`). She's been productive on authoring — homepage Pass-3 → pain-narrative live, welcome guide v5 shipped, AI-first-company blog post landed 2026-05-15 — but community presence on the active platforms (Reddit, HN, Twitter) is zero. The pattern is: content production is healthy; ship-and-promote is parked.
- Surveyed `~/prj/beadhub-all/` via Explore agent. Rich find: a fully-articulated outreach strategy doc at `~/prj/beadhub-all/beadhub-outreach/docs/outreach-strategy.md` (2026-02-18, BeadHub-branded). Concrete platform targets (r/ClaudeCode 395K weekly, r/CursorAI, r/ChatGPTCoding, Twitter/X, GitHub Discussions, HN read-only). Detailed daily agent loop design. Voice principles directly portable to aweb. Also `~/prj/beadhub-all/aweb-a2a-interop.md` as positioning material for the OpenClaw/A2A ecosystem.
- Surveyed the Pi extension at `~/prj/awebai/aweb/pi-extension/`. It's `@awebai/pi` on npm — already built, packaged, shippable. Wakes Pi (pi.dev) sessions on aweb channel events. New Persona 3 distribution channel that's NOT in `publishing/plan.md` today.
- Sent Iris a substantive ramp-up mail (msg `e1b6c7d0`, conv `345f95bb`) covering the pivot, the beadhub-all material, the Pi extension, and six questions for her read on priorities and the daily-loop shape.

**Waiting on**:
- Iris's reply to shape the first wave of concrete outreach actions.
- Juan greenlight on whatever first wave Iris and I converge on.

## Paused arc: corpus / aweave-fold (safe in git history)

The substantial architectural arc Sofia ran 2026-05-22 → 2026-05-26 is paused, not abandoned. Everything is in the tree; the artifact paths are stable.

### What landed durably

| Artifact | Location | State |
|---|---|---|
| Architecture doc | `agents/sofia/corpus-architecture.md` | Restructured for the fold (one product / two backends-internal); the `aweave` → `corpus` rename applied throughout |
| Multi-tenancy v0.3 (two-backend) | `agents/sofia/.aw/drafts/aweave-multi-tenancy-v0.3.md` | Sent to Marvin (msg `ef2adf02` in conv `adb6cc44`) 2026-05-23; superseded by the fold but kept as snapshot |
| Schema v0.8 | `agents/sofia/.aw/drafts/schema-v0.8-mail.md` | Sent to Marvin (msg `9d79a938` in conv `e66d09b0`) 2026-05-23; pending rename to v0.9 if/when work resumes |
| Fold + rename direction mail | `agents/sofia/.aw/drafts/marvin-fold-and-corpus-rename.md` | Sent (msg `4f55b529` in conv `adb6cc44`) 2026-05-26 |
| Pivot-pause courtesy note | (Marvin in same conv, msg `352e5921`) | Sent 2026-05-26 to keep Marvin informed |

### What was held mid-flight (do not lose)

- **Juan called the one-backend collapse** as the natural follow-on to the fold ("it will be very awkward for customers if they have to create different orgs/teams/etc in corpus. i think we may have to extend aweb-cloud instead of creating a new backend"). My read in the mail to him: yes, one backend is consistent with the fold, this matches the v0.1 multi-tenancy I originally recommended before the trinity-product framing pushed it to two. Locked vs tentative was unresolved when Juan pivoted to outreach. If the corpus arc resumes, **next move is corpus multi-tenancy v0.5 with one-backend (pgdbm shared pool, `aweave_cloud` + `corpus` schemas in one Postgres)** — the v0.1 architecture I argued for, plus the fold + the corpus rename.
- **Schema v0.9** = rename pass over v0.8 (title, preamble, comments, `default:aweave.ai` → `default:aweb.ai`). Node structure unchanged. Pending if/when the arc resumes.
- **Decision record** for the fold + corpus rename — not yet landed in `docs/decisions.md` because the convention requires anchoring on commit hashes. If Juan commits the architecture doc rewrite + (eventually) v0.5 / v0.9, the decision record lands at that point. Until then, the durable record is the mail thread + this handoff.

### What's archived from the corpus arc (snapshots, not active)

In `.aw/drafts/`:
- `marvin-multi-tenancy-mail.md`, `marvin-multi-tenancy-v0.2-mail.md`, `marvin-multi-tenancy-v0.3-mail.md` — sent mail bodies for v0.1/v0.2/v0.3
- `marvin-reframe-response.md`, `marvin-rev2-verification.md`, `marvin-dashboard-correction.md`, `marvin-launch-shape-response.md` — sent exchanges with Marvin
- `schema-v0.7.md`, `schema-v0.8-mail.md` — schema mail bodies (v0.7 retained for archaeology; v0.8 is the canonical pre-fold schema)
- `aweave-multi-tenancy-v0.1.md`, `aweave-multi-tenancy-v0.2.md`, `aweave-multi-tenancy-v0.3.md` — multi-tenancy iterations
- `aweave-architecture.md` is GONE (renamed to `corpus-architecture.md` in this turn; replaced)

### Naming convention locked at the corpus arc's last state

- `aweb` = the customer-facing product (post-fold)
- `aweb messaging` = the messaging service component inside aweb
- `corpus` = the organizational substrate service inside aweb (was `aweave`)
- `awid` = the identity registry (separate product at awid.ai)
- `aweb-cloud` / `ac` = the existing backend (continues post-fold; one backend if the corpus collapse lands)
- CLI: `aw corpus …` (was `aw weave …`)
- Postgres schema namespace: `corpus.*` (was `aweave.*`)
- S3 bucket: `aweb-corpus-stores` (was `aweave-stores`)

## Recent closed arcs (archived, do not re-litigate)

- **v0.5.47 + v0.5.48 cluster** (2026-05-23): destructive cutover + CLI self-serve P0 fix. Cluster fully cleared for external derivation. Conv `878c06b1` carries the full record (verified-live → framing review → P0 → external-claim split → two-mode correction → Hestia closing ack). Customer-facing labels: **"All"** and **"Team and contacts"** (not the slugs `open` / `team_and_contacts`).
- **Cross-agent grep-context discipline** (2026-05-23): banked at `docs/agent-first-company.md` via Iris's commit `4dfe70a`. Section title: "Verify Section Context Before Flagging Grep Hits." Three agents (Aida, Sofia, Iris) banked the lesson in parallel before promotion.
- **Reachability Setting runbook entry** (2026-05-23): live in `docs/support/runbook.md` via Aida's commits `53cee8c` / `9392957` / `69c9c92`. Athena tech-accuracy + Sofia framing complete. Push greenlit by Sofia (over a stale "wait for Juan" posture that no longer fit the stack composition) with Juan visibility.

## Active peer state (rough — verify on wake-up)

- **Iris**: online and responsive recently. Substantial outreach surface output through 2026-05-16, then quiet. Now the lead on the pivot.
- **Athena**: online. Operationally active on engineering. Last touch was the v0.5.48 cross-team verification (msg `9fcca42a` per Hestia relay).
- **Hestia**: online. Last touch was the v0.5.48 verified-live closing ack (msg `441b9109` in conv `878c06b1`).
- **Aida**: online. Last touch was the dashboard inbound-mode source-read + runbook section.
- **Marvin**: silent since 2026-05-23. May have moved on; the fold + corpus rename mail (2026-05-26) gives him a re-entry point if he comes back.
- **Eugenie**: outreach send-side authority. Bertha is her personal agent.

## What's open right now

- **Iris pivot ramp-up**: awaiting her reply to msg `e1b6c7d0`. Six questions in there shape the first wave.
- **Pi extension promotion plan**: not yet in `publishing/plan.md`; needs Iris's read on whether it's its own promotion arc or folded into a broader multi-agent piece.
- **5 queued direct-outreach drafts** at `co.aweb/outreach/daily/2026-05-07-direct-outreach-post-show-hn.md`: still pending human send three weeks after draft; Iris needs to confirm whether current product state still supports them or whether they need re-drafting.
- **"Two Agents Not One" article** on juanreyero.com: Juan voice-passed per Iris's last handoff; awaits his commit/push. Re-prompt if it's stalled.
- **Twitter thread P1 launch**: drafted, voice-passed; awaits Juan/Eugenie post timing.
- **Marvin loop**: paused; will surface back if/when he reacts or if the corpus arc becomes pressing again.

## Notes for next wake-up

- The handoff before this one (2026-05-12) is gone; git history preserves it. Recoverable via `git log --oneline -- agents/sofia/handoff.md`. Most of that handoff's items closed during the May 22 → 26 arcs.
- Sofia's consolidation-bias pattern surfaced repeatedly during the corpus arc: I recommended consolidation (one dashboard, one backend) twice before the trinity reframe; Juan corrected both times. The fold + rename is the opposite shape — collapsing the trinity at the marketing layer, where the architectural-purity case from May 21 didn't carry the startup-economics weight. The lesson banked: when a call seems to consolidate the trinity at the customer-facing surface, the right answer depends on whether the strategic-purity case is load-bearing for the audience size at the time. At zero users with finite distribution attention, consolidation wins; at scale, separation wins.
- Iris's surface has been silent on the active-distribution side (community presence on Reddit/HN/Twitter is zero) for weeks while authoring stayed productive. The pivot is targeting that gap specifically — not "write more drafts" but "actually ship the engagement."
