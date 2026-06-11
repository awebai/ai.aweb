# Sofia Handoff

Last updated: 2026-06-11 08:35Z (hero beat pre-HN gates signed off)

## How this file works

**handoff.md** (this file) = crisp current-state pointer for the next
wake-up. Active arcs, what to check first, who's waiting on what.

**logbook.md** = depth + history. Closed arcs, paused arcs, decisions
behind the current state, lessons banked. Reach for it when handoff
references something and you need more.

Keep handoff lean. When detail accumulates here, promote it to
`logbook.md` and replace with a one-line pointer.

## Operational context

- Sofia now runs on a server. Wake-up routine in `AGENTS.md` still
  applies (git pull → north-star docs → status files → decisions
  tail → handoff → aw mail/chat → /health).
- The handoff/logbook split was Juan's call (2026-06-03): handoff
  had grown to 127 lines and stopped being a useful re-entry pointer.

## Active arcs (verify on wake-up — last update inside the file)

### Release-risk sync (current as of 2026-06-07)

- app.aweb.ai live healthy at `v0.5.60`, aweb `1.26.8`, awid_service `0.5.10`; api.awid.ai `0.5.10`.
- #245 aw 1.26.3 workspace-cleanup regression remains the CLI/workspace-cleanup risk pattern. Direction agrees with Athena: read/status flows must not be destructive lifecycle operations; fix should require explicit cleanup/delete or stronger multi-signal evidence.
- **Rollback invariant landed (2026-06-10):** Sofia proposed generalizing #245 + aaqi bug-3; Athena refined to implementable form and Hestia ACKed/banked runbook #16. Landed in `docs/invariants.md` as invariant 9 and `docs/decisions.md` 2026-06-10. Core: failure-path rollback is transactional over known local writes and conservative about remote uncertainty; preserve authority/correlation when remote side effects may exist; destructive remote cleanup requires explicit lifecycle/recovery authority, not incidental rollback/read/status behavior. Corollary: manifest/snapshot-based rollback, never broad `rm -rf .aw`, preserve pre-existing `.aw` + partial-init/recovery markers unless explicit cleanup command.
- E2EE claim boundary: no broad "E2EE is live" claim. Only exact smoked surfaces. Do not call hosted custodial/server-side messaging E2E; hold generic self-custodial readiness unless AWID encryption-key publish skew is fixed/explained.

### gbrain integration analysis (in-flight with Juan, 2026-06-03)

Juan asked: "is gbrain (`/Users/juanre/prj/awebai/other/gbrain`) a
potential integration?" Initial framing "brain ⊥ coordination =
orthogonal layers" was wrong. After Juan's pushback ("i do not think
you understand how this works"), corrected to:

- **gbrain's principal axis = HUMAN-via-OAuth.** Agents are the
  human's MCP client tools. Company brain = ~1 OAuth per teammate
  (Model A) or 1 shared agent serving everyone via convention
  folders (Model B, Garry's production).
- **aweb's principal axis = AGENT-via-cryptographic-identity.**
  Humans are tenant metadata.
- **Subject mismatch.** Different principals = doesn't compose as
  orthogonal layers. Coherent compose is "human installs both;
  aweb agents query gbrain via the human's OAuth as one MCP among
  many" — much narrower than partnership-shape.
- **Implication for corpus arc**: if we want agent-peer-knowledge
  as a real surface, gbrain isn't the substrate (wrong subject).
  Omnigraph / Marvin loop is still the candidate.

**Awaiting**: Juan's response. My last question to him: "does the
omnigraph / corpus arc come back off the shelf, or were you steering
me toward 'drop the corpus ambition entirely and let
humans-with-gbrain be the model'?"

### Long-fruit submission cluster (verified 2026-06-03)

Drafts remain at `agents/sofia/.aw/drafts/submission-drafts-v0.md`.
Latest observed draft commit is `fc7bbcb` (retarget to channel 1.4.10 /
skills 0.2.10). `publishing/attempts.jsonl` has no rows observed in this
pass. Iris status says outreach pivot is active, but actual submission
execution is not yet visible from Sofia's surface.

Submission readiness from last live planning was: B.1/B.2/B.7 READY;
B.3 no longer blocked by npm package availability; B.4, B.5, B.6, B.8
staged. **Update 2026-06-03:** Claude marketplace submissions are on hold
until Wave 4 package versions publish. Do NOT use npm
`@awebai/claude-channel@1.4.11` or `@awebai/claude-skills@0.2.11`.
Grace confirmed stale surfaces. Expected corrected packages include
`@awebai/claude-channel@1.4.12` and `@awebai/claude-skills@0.2.12`. Channel
configure source fix landed at aweb `63d77176` (Wave 4 package source should be
that commit or later): if `.aw/workspace.yaml` is missing, do not guess
team/service; tell the user to initialize or join through the correct source
first (`aw init`, or explicit invite/service/BYOT as applicable). `aw init
--setup-channel` appears only in the MCP-configuration-missing branch after
`workspace.yaml` exists. Manual `.mcp.json` `npx @awebai/claude-channel` entry
remains. Launch instruction remains `claude --dangerously-load-development-channels
server:aweb`. Athena's grep at `63d77176` found no stale `aw run claude`,
`aw team bootstrap`, or `aweb-team-dev-review` refs in channel/skills. Skills
package also needs bootstrap fixed for current aw agents lifecycle, no `aw team
bootstrap`. Wave 4 likely includes Pi 0.1.20 and is held until AC Wave 3 live.
Athena is driving Claude marketplace path with Sofia + Hestia per Juan. Wave 4
packages are live (`@awebai/claude-channel@1.4.12`,
`@awebai/claude-skills@0.2.12`, Pi `0.1.20`). Athena rematerialized
`/home/juanre/prj/awebai/claude-plugins` from corrected npm artifacts,
validated, Sofia reviewed with no blocker, and Hestia pushed the reviewed
artifacts. Citation SHA: `claude-plugins` origin/main
`d6034672ded5ef5dbb38fc84fcb0a1de883b9544` (`Add vendored Claude marketplace
submission artifacts`). Submission can proceed using that pushed SHA. Outward
submission text must keep README's narrow trust boundary: inbound channel,
outbound via `aw`, hosted/server-side paths not E2E. See logbook §"Long-fruit
submission cluster" for full state.

### Site cleanup aweb-aaqe.6 — CLOSED 2026-06-10 (see logbook §"aweb-aaqe.6")

Both halves verified: hero teaches `aweb.ai/aida` (f4c0fec3), `/docs/team-bootstrap.md` → 404 after Juan's Render clear-cache deploy (Hestia mail d8e4ac03). #266 closed. Site is now distribution-beat eligible from the setup-framing side. Full deploy chain, hero-defect trail, and Render-CDN lessons in logbook.

Hero flip (aaqe.7 customer-facing half) CLOSED 2026-06-11: Olivia's fresh outside-team probe from `juan.aweb.ai/hero-probe-0610` passed on released aw 1.26.14, using loaded `pi.aweb.ai/ama` soul. Hestia verified ac `4907b8e3` live: home + /llms.txt render `pi.aweb.ai/ama`, zero rendered `aweb.ai/aida`, zero `ami.aweb.ai`, full namespace/no shorthand, and live send probe returns "Message sent to pi.aweb.ai/ama". Transcript in conv d24c717c msg 7bcdf398.

**DISTRIBUTION HOLD LIFTED (2026-06-11, Sofia framing pass mail 6f8b30ef):** hero/site beat-eligible — "two agents talking" is live and replayable by anyone. Iris notified (mail 094ad7be in conv 345f95bb) with claim boundaries: greeter demos identity+messaging NOT E2EE; no adoption numbers; keep aweb hero beat distinct from ClaWeb launch comms (Juan/Sam's surface). Iris proposes timing/shape, Sofia approves. Also flagged to Hestia: named-evidence-actor + replayable-checks chain (hero-probe-0610 pattern) is the verify-live evidence standard going forward; probe-init doubling as first customer-shaped production confirmation of the 1.26.14/aaqi fix is worth a line in next release-risk sync.

Live remnants carried forward:
- **Removal-shaped deploys**: Render CDN persists published files; file removal claims are unverified without a 404 probe + manual Clear-build-cache deploy (Hestia folding into runbook ops).
- **Watch-item**: homepage teaches `claude --dangerously-load-development-channels` — must flip to marketplace install when the Claude marketplace submission is approved; flag Olivia/Athena when that arc closes.

### ClaWeb cutover — STAGED, AWAITING JUAN'S GO (2026-06-10)

Juan + Sam (juan.aweb.ai/sam, real — Juan confirmed in session after I held an unverified relay) are launching ClaWeb as a federated-identity product on the aweb network (`claw` CLI, `<slug>.claweb.ai` namespaces, app.claweb.ai relay, free tier 3 identities/100 msgs/day, Plus $12/mo). The ClawHub `claweb` slug gets REPLACED with their rebuilt skill (supersedes this morning's rename-pointer content — fine, the 625 installs are ClaWeb-product users now). `aweb` slug unchanged, stays canonical for aweb.

State: rebuilt SKILL.md from `github.com/awebai/claw` main staged at `openclaw-skill/claweb/SKILL.md`; `clawhub sync --dry-run` clean (would publish 0.3.27, aweb untouched); Juan's clawhub auth valid on this machine. **DO NOT PUBLISH until Juan's explicit go in session.** Version question open with Sam: sync auto-bumps to 0.3.27 vs explicit `clawhub skill publish --version 1.0.0` relaunch marker.

Review flags sent to Sam via Athena relay (mail 55d7d90f; my direct mail to Sam 403s — he must add aweb.ai/sofia as contact): (1) plaintext-boundary line missing in Security section — signed ≠ encrypted, I'd insist before publish; (2) 'API key required' classifier risk — recommend explicit denial line; (3) claweb↔aweb.ai cross-network round-trip should be in Sam/Tara's verify gates per #14.

**PUBLISHED 2026-06-10:** Juan's go in session after confirming the inbound round-trip arrived (closed both directions of the light-tier interop gate). `clawhub skill publish ./claweb --slug claweb --version 1.0.0` → claweb@1.0.0 live (id k971n8yjmbpf8a2nn4gx76cyqn88dqfh). Page verified: v1.0.0, NO false 'API key required' badge, plaintext-boundary line present verbatim, federated-identity description intact. All go-conditions had cleared: plaintext line + No-API-key + metadata.openclaw landed on awebai/claw main and diff-verified; light tier confirmed (claw wraps aw Go libraries, zero protocol reimplementation); explicit 1.0.0 over auto-bump. Sam notified via Athena relay (Sam's identity is workspace-local — relay remains his channel until that changes). Suggestion left with Sam: keep claweb.ai/docs and skill command spellings identical — divergence is the staleness class that bit the old skill. Arc closes when Sam ACKs; then promote to logbook.

### pi.aweb.ai/ama greeter — CUSTOMER-FACING HALF CLOSED 2026-06-11

Hero now teaches `pi.aweb.ai/ama` (ac `4907b8e3`, Hestia verified-live). Evidence: pi.aweb.ai namespace registered, greeter identity provisioned, co.aweb `f67e2ef` soul loaded, Pi runner live on Juan's Hetzner box, Olivia fresh-identity 3-beat probe passed, Hestia post-deploy site verify passed. `aweb.ai/aida` remains support-side fallback; `aweb.ai/ama` remains investor/press proxy. Durable actor: `juan.aweb.ai/hero-probe-0610`; transcript in conv d24c717c msg 7bcdf398.

Carry-forward rules: full namespace addresses always (runbook #15); `pi.aweb.ai/ama` hands out only public verified addresses (`aweb.ai/aida`, `aweb.ai/ama`) and relays everything else herself; no E2EE overclaim; only teach released commands. Iris caught em dash drift in live greeter copy; Sofia fixed soul in co.aweb `cbcf7f1` and asked Hestia to trigger reread. Iris also caught hero line em dash; Sofia attempted direct Olivia mail (404) and asked Hestia to relay for next site copy window. OPEN: who reviews `aweb.ai/ama`'s soul — routed to Olivia, answer pending; if nobody, formalize peer-review for external-claim surfaces with active reply behavior as a direction call.

### Hero greeter distribution beat — DRAFTING WITH IRIS (2026-06-11)

Iris verified `aw chat send-and-wait pi.aweb.ai/ama "hello over there"` from a fresh terminal (~2s) and proposed a distribution beat. **CONSOLIDATED direction call (two Sofia sessions each replied — merged 2026-06-11, union of conditions; one clarifying mail sent to Iris):** HN primary (Show HN), replayable proof is HN-native; target Tue 06-17 Pacific AM. Go-conditions, ALL required: (a) draft + attempts/runbook row-writing wiring + submitter availability ready; (b) adversarial smoke on ama PASS; (c) burst capacity read on the single Pi runner PASS by 06-13. Any condition fails → r/ClaudeCode primary, HN follows on signal. r/ClaudeCode +24-48h, Twitter same day, DEV.to optional on signal. P3-primary proof, NOT persona-priority rewrite (P1 stays priority; browser tab serves P1 in same hero). Attempts discipline: no submission without row-writing; do not retro-invent B.1-B.8 rows. Claim boundary: identity+address+messaging+greeter reply; NOT E2EE, no adoption numbers, ClaWeb distinct lane. Em-dash flags: pushed back on process — rule not banked in voice.md (which itself uses em-dashes); Iris banks it there first, then soul + hero copy inherit. Iris drafts all pieces now, routes through Sofia before Juan/Eugenie.

Hestia split plan signed off (mail dfc1be35 reply 3621b2de): adversarial smoke → Olivia primary, Hestia re-confirms transcript against runbook #14. Include prompt-injection attempt, fake-authority claim, investor/press misroute, E2EE/privacy question, and command-error/customer-confusion case. Burst capacity → Hestia primary: 3-5 outside-team `juan.aweb.ai` identities cycling through N=10/25/50/75 concurrent send-and-wait waves via channel API, explicitly tagged as load-test probes. Pass bar: >=95% success at N=50, P95 <30s, no silent 120s hangs, consistent canonical opening/soul behavior, and track duplicate/contradictory reply rate. Slow-but-real queueing = soft pass with copy/timing expectation; silent 120s timeouts = hard fail for HN-primary until fixed or downgraded.

**Operational flag for Juan:** two concurrent Sofia sessions both issued direction calls on the same proposal within minutes — compatible but non-identical conditions. Direction must speak with one voice; concurrent sessions should either split surfaces explicitly or serialize direction-shaped replies (check handoff/outbox before replying to proposals).

### OpenClaw × aweb integration (active — ClawHub skills drafted, awaiting publish)

**2026-06-09 with Juan:** decided ClawHub strategy and implemented. Decision:
publish new canonical `aweb` skill AND push final corrected update to the
existing `claweb` slug (625 downloads; its content is broken against aw 1.26.x —
`--to-alias`, `--unread-only`, `ack --message-id` no longer exist; brand stale).
ClawHub search for "aweb" returned zero results before this.

State:
- Both SKILL.md drafts written under `agents/sofia/openclaw-skill/`
  (`aweb/` v1.0.0, `claweb/` v0.4.0 = same content + rename pointer).
  Every command verified against installed aw 1.26.8 `--help` output.
  Setup flows checked against canonical skills (messaging, team-membership).
  E2EE boundary wording per standing claim discipline.
- Publish runbook in `agents/sofia/openclaw-skill/README.md` —
  `clawhub sync` from that dir, requires Juan's clawhub auth (CLI not on
  this machine).
- Cron poller block follows current OpenClaw docs but untested live
  (no openclaw binary here); `--every 1m` chosen conservatively.
- Athena tech-accuracy review DONE (mail 3096495c, conv 70f1c868): found
  `aw mail show` positional-arg error (now flags-only), over-broad
  "stable address" claim, missing BYOD global-init form. All three fixed
  in both files. Athena cleared for publish after these fixes.
- **PUBLISHED 2026-06-09** via clawhub device-flow auth on this server:
  `aweb@1.0.0` (id k97d1ps8vhvjhp0s7hadevhe6x88adne) and
  `claweb@0.3.24` (id k97ag6hsdz9477wgf5ayq53hwx88a477 — sync auto-bumped
  patch; frontmatter 0.4.0 was ignored, cosmetic). Verified live:
  clawhub.ai/juanre/aweb shows v1.0.0 with current commands;
  clawhub.ai/juanre/claweb shows v0.3.24 with rename notice.
  `clawhub search aweb` returns aweb@juanre as top hit (web UI search
  lagged at publish time; recheck if it persists).
- Caveat that survives publish: cron poller section follows OpenClaw docs
  but untested on a live Gateway. Fix-forward on feedback (v1.0.1).
- Canonical install command for all future docs/outreach:
  `openclaw skills install aweb`.
- ClawHub auto-badged the skill "API key required" (false — Athena
  verified code path: interactive `aw init` provisions hosted identity
  with no key/browser/human step; AWEB_API_KEY is an optional separate
  flow). Fixed in v1.0.2/0.3.26 by adding an explicit "No API key or
  human sign-in is required" line to Setup — badge cleared on both
  pages. The classifier reads content; credential-free comparison
  skills carry no badge and one (free-weather-skill) uses the same
  explicit-denial trick. Current live: aweb@1.0.2, claweb@0.3.26.
- **New cutover direction from Sam via Athena (2026-06-10):** existing
  ClawHub `claweb` skill (600+ installs) should be replaced in place with
  rebuilt `github.com/awebai/claw` `skills/claweb/SKILL.md` at cutover, same
  skill name, `requires.bins` changes from `[aw]` to `[claw]`. HOLD publish
  until Sam/Juan green light. Re-fetch `awebai/claw` main before staging;
  required fixes landed there: plaintext relay-readable/TLS/Ed25519/not-E2EE
  boundary, explicit no-API-key statement, `metadata.openclaw` alongside legacy
  `clawdbot`. Sam recommends explicit publish `--version 1.0.0` as relaunch
  marker pending Juan confirmation. Interop tier: `claw` wraps aw Go libs for
  signing/resolution/envelopes, so lighter live round-trip smoke applies;
  cross-network smoke in flight (`sam-smoke.claweb.ai/probe` ↔ `aweb.ai/athena`).
  Relay via Athena still needed because Sam identity is workspace-local; adding
  `juan.aweb.ai/sam` as contact did not make direct sends resolve.

Research note `agents/sofia/openclaw-aweb-research.md` carries the wider
ladder (npm bundle Level 0 test, marketplace relative-source Level 1 with
Athena/Hestia, native plugin Level 4 deferred).

Key current read:
- OpenClaw is a self-hosted multi-channel Gateway. It supports native plugins,
  ClawHub skills/plugins, and Claude/Codex/Cursor compatible bundles.
- Fastest likely path: OpenClaw installs `@awebai/claude-skills@0.2.12` as a
  Claude-compatible bundle, plus user installs `@awebai/aw`. Do **not** frame
  `@awebai/claude-channel` as the OpenClaw path; it is Claude Code-specific.
- Current `awebai/claude-plugins` marketplace source is npm-based. OpenClaw
  remote Claude-marketplace installs require relative paths inside the cloned
  marketplace repo, so direct `--marketplace awebai/claude-plugins` may fail
  unless we switch entries to relative dirs or create an OpenClaw-specific
  marketplace. Don't change that without Athena/Hestia coordination because
  Claude Code users currently rely on npm-source marketplace pins.
- Old user-provided `claweb` skill structure is useful despite stale commands:
  setup once, start-of-session inbox/chat check, mail/chat examples, security,
  and especially **automatic polling**.
- Wakeup is load-bearing. OpenClaw has no aweb-native push receiver today.
  Near-term wake path is OpenClaw cron (or heartbeat, but default ~30 min is too
  slow for chat). Current docs support `openclaw cron add/create`, `--every`,
  `--session main`, `--wake now`, and `--system-event`. Creating/mutating cron
  likely requires `operator.admin`, so user docs should tell the human/operator
  to install the poller.
- Proposed poller shape to test, not publish blindly:
  `openclaw cron add --name "aweb inbox poller" --every 30s --session main --wake now --system-event "aweb poll: Check for new aweb mail and chat. Run 'aw mail inbox --unread-only' and 'aw chat pending'. If there is anything new, read it and respond using the aweb-messaging policy. Reply in existing conversations; do not start duplicates. If no new items, output NO_REPLY."`
- Must test whether `30s` is accepted/too noisy, whether `NO_REPLY` suppresses
  output for main-session cron, whether `aw mail inbox --unread-only` is still
  best command spelling, and whether the skills appear after npm bundle install.

Likely next actions:
1. Get a clean OpenClaw install/workspace and test:
   `npm install -g @awebai/aw@latest`; `cd ~/.openclaw/workspace`; initialize or
   join aweb correctly; `openclaw plugins install npm:@awebai/claude-skills@0.2.12 --pin`;
   `openclaw gateway restart`; `openclaw plugins inspect ...`; `openclaw skills check`.
2. Draft an `aweb-openclaw` skill/package based on current aweb wording + the
   old `claweb` structure, but update all obsolete terms (aweb not ClaWeb,
   awid.ai not clawdid, current `aw init`/invite/BYOT flows, plaintext/E2EE
   boundary). Include cron polling prominently.
3. Consider adding OpenClaw metadata to canonical aweb skills (`metadata.openclaw`
   with `requires.bins: ["aw"]` and node install hint for `@awebai/aw`) only after
   validating Claude Code and OpenClaw parsers tolerate it.
4. Decide distribution ladder after test: direct npm bundle docs → OpenClaw-compatible
   marketplace → ClawHub bundle/skills → native OpenClaw plugin wrapping `aw`.

### Omnigraph incoming-agent posture (banked 2026-05-27, no contact yet)

See memory `[[project-omnigraph-outreach-incoming]]`. Posture:
help them set up on aweb, route deeper technical to Athena, learn
bidirectionally. Linked to the corpus arc question above — if Juan
keeps the corpus ambition alive, omnigraph is the candidate
substrate.

## Check first on wake-up

1. `aw mail inbox` and `aw chat pending` — peer threads.
2. `curl -s https://app.aweb.ai/health` and `curl -s
   https://api.awid.ai/health` — drift check.
3. `git log --oneline -15 -- agents/sofia/` — what moved while off.
4. `git log --oneline -10 -- docs/decisions.md` — direction changes
   since last wake-up.
5. `status/outreach.md` — Iris's current focus.
6. `status/engineering.md` — Athena's current state.
7. `status/operations.md` — Hestia's release pipeline state.

## Open threads / waiting on

- **Athena** — #245 fix-forward implementation/owner; no direction action pending unless someone argues to preserve auto-delete-on-status.
- **Juan** — response to gbrain analysis (whether corpus arc resumes).
- **Iris** — long-fruit cluster execution status; original ramp-up
  mail `e1b6c7d0` in conv `345f95bb` had broader community-engagement
  loop questions still partially open.
- **Athena/Hestia** — Claude marketplace submission can proceed from pushed `claude-plugins` SHA `d6034672`; keep trust-boundary wording narrow.
- **Hestia** — current release/live verification state; product status observed v0.5.60 live on 2026-06-07.
- **Marvin** — silent since 2026-05-23. Fold + corpus rename mail
  (msg `4f55b529` in conv `adb6cc44`) is his re-entry point.

## Bank-worthy reminders pulled forward

- **Don't extend peer defect frames** — memory
  `[[feedback-dont-extend-peer-defect-frame]]`. Peer flagging X as
  bug ≠ Juan reads X as bug. Surface to Juan before generating
  direction-level recommendations.
- **Consolidation-bias check** — at zero-users with finite
  distribution attention, simplification wins at customer-facing
  layer; at scale, separation wins. (See logbook for the 2026-05-26
  fold + rename arc that banked this.)
- **Verify infrastructure contract before debating policy** — in
  AGENTS.md.
- **Customer-shape discipline** before reading landing/onboarding
  copy — see AGENTS.md "Landing / Onboarding Copy Review".

## Notes for next wake-up

- The handoff before this restructure (2026-05-26, 127 lines) was
  moved into `logbook.md`. Git history preserves the old handoff
  shape: `git log --oneline -- agents/sofia/handoff.md`.
- If Juan extends the handoff/logbook convention to other agents,
  the project `AGENTS.md` "Handoff documents" section will need an
  update. Sofia should not unilaterally touch shared files; flag
  to Juan if the convention spreads.
