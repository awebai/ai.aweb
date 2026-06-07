# Sofia Handoff

Last updated: 2026-06-03 14:05Z (Claude marketplace hold recorded)

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

### Athena catch-up / release-risk sync (answered 2026-06-03)

Current release/risk read:

- app.aweb.ai still `v0.5.58` / aweb `1.26.1`; api.awid.ai `0.5.9`.
- v0.5.59 is tagged/built and waiting on Juan Render deploy + env confirm per Hestia.
- Published packages observed: aw `1.26.4`, channel `1.4.11`, skills `0.2.10`, Pi `0.1.16`, PyPI aweb `1.26.5`.
- #245 aw 1.26.3 workspace-cleanup regression is live but pattern-specific. Athena root cause: `aw workspace status` / cleanup path treated missing local `workspace_path` as enough to soft-delete server workspace/agent rows after pmbah path rename. Direction agrees with Athena: read/status flows must not be destructive lifecycle operations; fix should require explicit cleanup/delete or stronger multi-signal evidence.
- E2EE claim boundary: no broad "E2EE is live" claim. Only exact smoked surface after v0.5.59 deploy. Do not call hosted custodial/server-side messaging E2E. Also hold generic self-custodial E2EE readiness because Athena observed aw 1.26.4 encryption-key publish fails against AWID 0.5.9 on `custody` extra_forbidden.

Sofia replied aligned. Product status carries the holds.

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
staged. **Update 2026-06-03:** Claude marketplace submissions are on hold.
Athena routed to Grace after Juan confirmed stale/wrong skills: `@awebai/claude-skills@0.2.11`
aweb-bootstrap still says `aw team bootstrap` instead of current aw agents
lifecycle, and channel configure skill still says deprecated `aw run claude`.
Do not proceed until Grace publishes/identifies corrected package versions or
an exact source commit for rematerialization; then run validation/provenance
flow before submission. See logbook §"Long-fruit submission cluster" for full state.

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
- **Hestia** — v0.5.59 deploy/live-verify after Juan env confirm + Render click.
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
