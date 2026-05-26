# Sofia Handoff

Last updated: 2026-05-26 (long-fruit submission cluster active; drafts landed)

## Check first on next wake-up

1. **`aw mail inbox`** — primary signal. Specifically watch for:
   - Iris voice-pass return on the submission drafts (msg `2e0054ec` in conv `345f95bb`). Her read on B.1, B.2, B.3, B.7, B.8 long-form copy shapes whether Juan submits as-drafted or with edits.
   - Hestia ack on the npm-publish ask (msg `3bd13257` in conv `878c06b1`) — gates B.3. Without `@awebai/claude-channel@1.4.9` on npm, the official MCP registry submission validates fail.
   - Marvin reaction (if any) to the fold + corpus rename direction mail (msg `4f55b529` in conv `adb6cc44`). If he replies, the corpus arc may surface back to active.
2. **`aw chat pending`** — sync-blocked peers.
3. **Live state**: `curl https://app.aweb.ai/health` and `curl https://api.awid.ai/health`. Last verified-live 2026-05-23 22:17 (v0.5.47 → v0.5.48 cluster framing-acked in conv `878c06b1`); the cluster is fully cleared for external derivation with the `"All"` / `"Team and contacts"` customer-label naming.
4. **`docs/decisions.md` tail** — any entries newer than this handoff.
5. **`status/outreach.md`** — Iris's current focus signal.

## Active arc: long-fruit submission cluster (2026-05-26)

**Triggered by**: Juan, "the ones that will take the longer to bear fruit (anthropic and openai submissions)" — clarified focus inside the broader outreach pivot.

**Driving directly per Juan**: "as you wish, she seems free but you can also do it, just drive this" (re Iris involvement) + "please talk to athena directly not via iris."

**Done this turn**:
- Routed engineering blockers to Athena directly (conv `70f1c868`). Both cleared same-session:
  - `f32393a`: LICENSE files in both plugin dirs + skills plugin.json metadata (now on plugin version `0.2.9`, rebased over a Hestia/Dave release)
  - `db9a492`: `@awebai/claude-channel 1.4.9` with `mcpName: "io.github.awebai/channel"` (source-only; npm publish pending)
- Athena framing-confirm on B.3 description ("pairs with the aw CLI for the action surface") — accurate for current shape, no pre-baked future-shape claim needed.
- Drafted full B.1–B.8 submission script at `agents/sofia/.aw/drafts/submission-drafts-v0.md` (commit `a005fbf`). Each section: where to go, exact form fields / file content, verification step. Includes execution-order recommendation (Day 1 B.3+B.1+B.2+B.7, Day 2 B.4+B.6+B.5, Day 3+ B.8) and open questions for Juan/Hestia/Iris.
- Routed Iris (msg `2e0054ec` in conv `345f95bb`) with voice-pass scope: long-form descriptions, ClawHub variant body, smithery shape-mismatch framing.
- Routed Hestia (msg `3bd13257` in conv `878c06b1`) with the npm-publish gating ask.
- aw epic `default-aaai` state comment landed.

**Submission readiness state:**
- B.1 (Claude Code marketplace, aweb-channel): READY
- B.2 (Claude Code marketplace, aweb-skills): READY
- B.3 (official MCP registry): waiting on npm publish of `@awebai/claude-channel@1.4.9`
- B.4 (mcp.so): submit after B.3 lands; form-investigation at submission time
- B.5 (smithery.ai): shape mismatch — stdio vs hosted-URL; three options documented
- B.6 (glama.ai): submit after B.3; form-investigation at submission time
- B.7 (awesome-mcp-servers PR): READY, line drafted, alphabetical placement identified
- B.8 (ClawHub variant SKILL.md): drafted; needs to land in aweb repo before `clawhub skill publish`

**Waiting on**:
- Iris voice-pass return (primary).
- Hestia npm-publish of 1.4.9 (gates B.3).
- Juan greenlight to execute Day 1 submissions.

## Paused arc: outreach pivot scoping (2026-05-26 morning)

Iris ramp-up mail (msg `e1b6c7d0`, conv `345f95bb`) sent earlier; her reply hadn't landed when Juan re-scoped to "the ones that will take the longer to bear fruit." The long-fruit cluster IS the first wave; the broader outreach loop design (community-engagement actions, daily-loop integration with attempts.jsonl) sits beside this.

Iris parallel work that's already landed (per her schema-PR shipit drafts):
- `publishing/attempts-README.md` schema extensions (community-engagement + submission-surface variants, channel enum updated)
- `publishing/attempts.jsonl` empty append-only log
- `publishing/past-attempts-template.md` backfill template for Juan

Each long-fruit submission produces one `attempts.jsonl` row at submission time (submission-surface variant). Schema is locked.

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

- **Long-fruit submission cluster**: B.1-B.8 drafts at `agents/sofia/.aw/drafts/submission-drafts-v0.md`. Iris voice-pass pending; Hestia npm-publish gates B.3. See active arc above.
- **Iris pivot ramp-up**: original mail `e1b6c7d0` still open; the long-fruit drafts are a partial answer but the broader community-engagement loop questions (which platforms, daily cadence, BeadHub material reuse) are still on her plate.
- **Pi extension promotion plan**: not yet in `publishing/plan.md`; lower priority than the long-fruit cluster but worth surfacing if Iris asks.
- **5 queued direct-outreach drafts** at `co.aweb/outreach/daily/2026-05-07-direct-outreach-post-show-hn.md`: still pending human send three weeks after draft; Iris confirms product-state fit.
- **"Two Agents Not One" article** on juanreyero.com: Juan voice-passed per Iris's last handoff; awaits his commit/push.
- **Twitter thread P1 launch**: drafted, voice-passed; awaits Juan/Eugenie post timing.
- **Marvin loop**: paused; will surface back if/when he reacts or if the corpus arc becomes pressing again.

## Notes for next wake-up

- The handoff before this one (2026-05-12) is gone; git history preserves it. Recoverable via `git log --oneline -- agents/sofia/handoff.md`. Most of that handoff's items closed during the May 22 → 26 arcs.
- Sofia's consolidation-bias pattern surfaced repeatedly during the corpus arc: I recommended consolidation (one dashboard, one backend) twice before the trinity reframe; Juan corrected both times. The fold + rename is the opposite shape — collapsing the trinity at the marketing layer, where the architectural-purity case from May 21 didn't carry the startup-economics weight. The lesson banked: when a call seems to consolidate the trinity at the customer-facing surface, the right answer depends on whether the strategic-purity case is load-bearing for the audience size at the time. At zero users with finite distribution attention, consolidation wins; at scale, separation wins.
- Iris's surface has been silent on the active-distribution side (community presence on Reddit/HN/Twitter is zero) for weeks while authoring stayed productive. The pivot is targeting that gap specifically — not "write more drafts" but "actually ship the engagement."
