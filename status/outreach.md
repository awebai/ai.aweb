# Outreach Status
Last updated: 2026-05-26 13:45 (Iris on altair.local)

## Current focus

**Outreach pivot from authoring → active distribution.** Juan asked Sofia to bring me in on serious outreach work (her chat-quote 2026-05-26: "please stand back, bring in iris, and spend some serious effort looking for outreach opportunities"; Juan-confirmation outstanding). Sofia's brief landed mail `e1b6c7d0`; verification arc closed mail `e6df2c95`. Lane has been parked since the 2026-05-16 production deploy — content production has been healthy, community presence is zero, no daily scan/draft/post loop running.

Currently:
- Step 1 of four-step plan: refreshing status + handoff (this update).
- Step 2 next: audit parked artifacts.
- Step 3 next: author strategy adaptation from beadhub-era material in co.aweb/outreach/source-material/beadhub-era/ + current aweb state.
- Step 4 next: add Pi extension to publishing/plan.md as Persona-3 promotion arc.

## State changes since last update (2026-05-16)

- **2026-05-21 → 2026-05-26 marketing fold.** Sofia's corpus-architecture.md (agents/sofia/, ai.aweb commit `00c431e`) supersedes the 2026-05-21 trinity framing (awid / aweb / corpus as three peer products). New shape: aweb is the single customer-facing product (aweb.ai, app.aweb.ai, `aw` CLI). awid keeps its own brand for neutrality positioning (any service verifies equally). corpus is internal architecture term, does not appear on customer-facing copy. **Material impact on voice + landing + ecosystem positioning.** Need a quick pass on whether publishing/voice.md or recent drafts leak the trinity framing.
- **Pepe Reyero autonomous-install case (2026-05-09).** First complete customer-evidence durable artifact. 4 frictions reported → P0 dispatch → all four shipped end-to-end within 48h via aweb 1.20.8 + AC v0.5.25 + v0.5.26. Banked at `co.aweb/outreach/customer-evidence/2026-05-09-pepe-autonomous-install.md` (Juan commit `2dfcfbc`). Eugenie/Bertha called Pepe-anonymous in public outreach (Sofia commit `2874ded`). **First real dogfood story.**
- **Pi extension shipped 0.1.5 → 0.1.8.** Dave's `@awebai/pi` carries my voice-pass tone nudge (Athena chat 2026-05-19); Hestia 2026-05-23 wave bundled aweb 1.25.0 + awid 0.5.8 + AC v0.5.45 + channel 1.4.8 + pi 0.1.5. Pi 0.1.8 cross-harness table (ai.aweb commit `4be8263`). **New Persona-3 distribution surface.** Not in publishing/plan.md.
- **Hestia release cluster cleared.** v0.5.47 destructive cutover (2026-05-23), v0.5.48 inbound-mode CLI self-serve (2026-05-23). Six outreach-facing facts banked for v0.5.48 release-notes pack (conv `9b8ad2a8`); Sofia framing-reviewed Aida's runbook line; release-notes pack derivation queued on my cycle.
- **aapr BYOT cluster shipped** (ai.aweb commit `e32d9cd`). Skill ripple + cross-harness table.
- **Cross-agent grep-context discipline landed** (ai.aweb commit `4dfe70a`, `docs/agent-first-company.md` operating rule). Per Sofia framing-pass `c81ccf2d`. Banked from the 2026-05-23 deprecated-alias arc.
- **welcome.md → mcp-tutorial.md migration** (AC commit `052530aa`, 2026-05-16). v5 welcome guide draft + history.md v5 entry now carry SUPERSEDED markers (ai.aweb commit `f45e1c1`). Live customer surface clean.
- **Hostname-divergence event 2026-05-26.** Sofia operating from Mac.c.is; aw workspace status reported altair.local. Real coordination gap surfaced + closed (Sofia commit `00c431e` + `da58d70` brought corpus-architecture + beadhub-era source material into shared git origins). aw workspace hostname-bug routed to Athena via Sofia. **No artifact lost; future-Iris should give "infrastructure divergence I don't understand" higher hypothesis-stack weight when evidence reaches second-round unambiguous mismatch.**

## Parked artifacts inventory (need audit in step 2)

- **Twitter thread P1**: `publishing/drafts/2026-05-13-twitter-thread-p1-launch.md`. Through Sofia framing + Athena tech-accuracy. On Juan/Eugenie voice pass + post-timing slot. Product state has shifted since 2026-05-13 (1.21.2, v0.5.47, v0.5.48 all shipped) — claims may need refresh before send.
- **Five 2026-05-07 direct-outreach drafts**: `co.aweb/outreach/daily/2026-05-07-direct-outreach-post-show-hn.md`. Pending Eugenie human send three weeks later. Substance viable; framing pre-fold trinity-shape ("DNS-rooted identity" leading-line) needs re-author under single-product framing per the 2026-05-26 fold. Sofia framing-pass on re-drafted versions.
- **"Two Agents Not One" article**: ⚠️ **NOT parked — shipped 2026-05-08** at https://juanreyero.com/article/ai/two-agents-not-one/ (page title "Pair Your Coding Agent with a Reviewer"; URL slug preserves working title). Tracking gap: outreach didn't capture the ship at the time; entries in publishing/history.md dated 2026-05-11/12/13 cite the post as "still pending." Captured retroactively in history.md 2026-05-26. **Follow-up needed**: cross-channel promotion (Reddit / HN / Twitter / dev.to) not done; signal capture window from 2026-05-08 → 2026-05-16 was pre-Plausible; post-Plausible referral traffic from juanreyero.com → aweb.ai is observable if any.
- **v0.5.48 release-notes pack**: components reviewed (Aida's runbook line + Sofia framing). Six facts banked. My next derivation.

## Source material now accessible (post-hostname-sync)

- `co.aweb/outreach/source-material/beadhub-era/outreach-strategy.md` (12111 bytes, 2026-02-18). BeadHub-branded; strategy bones reusable.
- `co.aweb/outreach/source-material/beadhub-era/aweb-a2a-interop.md` (26030 bytes, 2026-02-22). aweb-branded already; OpenClaw/A2A ecosystem positioning.
- `co.aweb/outreach/source-material/beadhub-era/README.md` (provenance + intent).

## Signals (current)

- No active community-presence signal. Plausible live since 2026-05-16; no traffic delta from active outbound because no active outbound.
- v0.5.47 cluster has 13% adoption on team_and_contacts inbound mode (46/347 agents). Metis-shape signal worth noting when she's reading.
- Pepe-anonymous customer-evidence is the first real dogfood. Worth a piece when the friction-to-ship arc is framable for public.

## Next actions

- ✅ Step 1: refresh status + handoff (this update).
- Step 2: audit parked artifacts. Read each, judge fit-against-current-state, route revisions or retire.
- Step 3: draft outreach strategy adaptation (publishing/plan.md + publishing/runbook.md). Beadhub bones as input, current aweb state (audiences.md persona model, voice.md, marketing fold, Pepe customer-evidence) as corrective lens. Route to Sofia for framing pass.
- Step 4: add Pi extension to publishing/plan.md as Persona-3 promotion arc. Probably a piece on multi-agent coordination in Pi, with `@awebai/pi` as one tool in the answer (not a marketing-shape "what you can do with @awebai/pi" headline).
- Parallel: derive v0.5.48 release-notes pack from the six banked facts when component readiness signal arrives from Sofia.
- Parallel: voice.md trinity-leak check.

## Open questions for Juan

- Pivot framing confirmation (Sofia's chat-quote was paraphrased; ground-truth from him).
- Bandwidth for the daily Juan-review slot if we run a daily scan/draft/post loop (10-15 min/day) vs weekly-batch cadence.
- Eugenie send-side capacity for daily posting cadence.
