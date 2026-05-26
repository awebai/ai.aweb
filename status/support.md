# Support Status
Last updated: 2026-05-23 (dashboard inbound-mode source-verify for Sofia + Case 4 staleness fix + runbook reachability section)

## Current focus

Watching for the first **P1 (Personal-AI consumer)** and **P2 (Company
with AI-using employees)** customer questions after the aweb.ai
consumer-entry path shipped 2026-05-13 22:28Z (Sofia mail
`aa9d70de`). Persona priority reordered 2026-05-12 (decision record
2026-05-12): P1 consumer → P2 company → P3 developer team (was #1)
→ P4 platform builder (was #2).

The runbook is currently shape-complete for **P3 (CLI developer
customers)**. P1+P2 support flows are not yet authored; standing
posture per Sofia is **collect 2-3 real seed examples first, then
author** — same TIME-LIMITED / reversible-evidence discipline that
paid off on the chat-403 and aani cycles.

### Watch list — six expected P1+P2 question shapes (Sofia `aa9d70de`)

1. **"I don't know my friend's @handle"** — discovery friction; email-invite path is followup work (aweb-aanp.6.1, Grace P2).
2. **"My AI says it can't connect"** — OAuth-consent flow confusion across providers.
3. **"I added Sarah but she didn't get my message"** — pending vs active contact state.
4. **"What's the difference between my AI and my agent?"** — vocabulary; per aanw.7: `agent` = on-aweb actor, `AI`/client name = user's tool, `handle` = consumer identifier.
5. **"Where do I see what my AI did?"** — observability of custodial AI actions.
6. **"How do I block someone?"** — privacy default question; contacts-only-reachability may not be obvious from UI.

Saved as seeds, not authored. Once 2-3 of these arrive empirically,
runbook section follows.

## Open customer blockers

None active. Customer activity over recent period closed cleanly
(see Closed customer loops below).

## Waiting on engineering

**Zeus onboarding-completion gap → Sofia escalating to Juan**:
Sofia confirmed (mail `9bea8bb9`) the gap is real P2-validation
signal and is surfacing to Juan separately for direction. Three
design options on the table (automated reminder ping / clearer
walkthrough framing / something else). Not pre-actioning with
Athena until Juan blesses scope. I'll loop Zeus when there's a
decision or when his team's controller-action actually unblocks
them.

Nothing else customer-blocking. Customer-shape discipline lives in each
agent's own AGENTS.md operational section + the `aweb-aanp` brief
in the dev team (per Sofia mail `7b3fd3a5`). The
`customer-onboarding-flows.md` doc was deleted 2026-05-12 (commit
`47a9558`) and absorbed accordingly; `publishing/voice.md` will
catch up the discipline pointer once Iris's update lands.

## Closed customer loops

**Recent cycles, summarized**:

- **Zeus consumer-entry scope ask (2026-05-18)**: Sofia confirmed
  via mail `9bea8bb9` that the 2026-05-13 consumer-entry ship
  (ac v0.5.31 + homepage + /developers + /connect +
  /oauth/consent + new MCP contact-tools + welcome guide) is
  additive across the board — no Path A flow change for
  hosted-custodial developer-team customers. Sent Zeus the
  follow-up (mail `fd65ae2c`) including Sofia's call-out that
  the new MCP contact-tools (`list_contacts`,
  `add_contact_by_handle`, `send_message_to_contact`) work for
  any aweb user via MCP if his team finds handle-based
  addressing useful. Promise to him kept ("within a day").

- **chat-403 surface (2026-05-06)**: closed without runbook
  documentation. Empirically-zero customer reports + spec-lock on
  `--start-conversation` made the would-be workaround actively
  harmful (Hestia mails `1626ce35` + `b09ca4c4`). Case 6 absorbs
  any rare future report.
- **aani 422-on-AC-hosted (2026-05-08 → 2026-05-10)**: TIME-LIMITED
  entry added at `e6b1303` against the actual shipped surface, then
  REMOVED at `8179a3e` when AC `v0.5.26` verified-live closed the
  surface in code. Hestia mail `96f74b81` triggered the close.
  Discipline #24a's "two reversal-safe checkpoints" framing paid
  off across the full cycle.
- **BYOD-422 (`aw claim-human` 422 on BYOD without `--username`)**:
  runbook entry landed via Mia's structured contribution (mail
  `f393168c`, 2026-05-02). Committed at `e15838c` with framing
  invariant. Still local-unpushed pending Juan's greenlight.
- **Zeus (`gsk.aweb.ai/zeus`) onboarding**: walkthrough delivered
  (mail `1e47e6f7`). Customer end-to-end unblocked on `aw 1.20.3` +
  channel plugin; team-setup question answered with dashboard
  API-key bootstrap as recommended path.
- **DAgR positioning (Bertha → Eugenie)**: three-voice convergence
  delivered (Aida first-look → Athena technical validation → Sofia
  positioning lock). Frame #2 (identity-layer durability) locked;
  post can ship.

## Learnings and patterns (banked for the AGENTS.md cleanup pass)

- **Discipline #24** — documented workarounds must be empirically
  attested against the customer surface, not just the surface they
  claim to work around.
- **Discipline #24a** — pre-empirical OK if provable from code-diff;
  TIME-LIMITED marker + commit-stack shape make the discipline
  self-reversible by construction ("two reversal-safe
  checkpoints"). Applied across chat-403 (close before push) and
  aani (add → REMOVE on close-trigger).
- **Discipline #24b** — empirical probe against deployed AC surface
  required for AC-deployable claims; OSS-direct Docker e2e necessary
  but not sufficient. Sofia + Athena banking; lives in ops.md
  standing list.
- **Discipline #25** — `aw mail send --body "..."` triggers shell
  substitution on markdown backticks (and silently corrupts the body).
  Always use `--body-file` for any mail containing technical terms
  in backticks. The `aw mail send --help` text already warns about
  this.
- **Incoming-report-triage shape** — when a customer reports a
  surface that should be fixed in the current `aw` version, confirm
  their `aw version` first; route unknowns to Case 6 ("Bug,
  Regression, Or Outage").
- **Mail-conversation continuation** — replying into an active
  mail conversation requires `--conversation-id <id>` alone
  (extracted from JSON inbox), without `--to-*` flags. Post-1.20.2
  the CLI auto-resolves in many cases; explicit `--conversation-id`
  is the unambiguous form.
- **Cross-team routing** — `--to-did did:key:...` is the bidirectional
  fallback; `--to-address` works when the recipient address is
  AWID-publicly-indexed; chat is alias-only (no `--to-did`); when in
  doubt and the work is engineering-coordination, route through
  Athena per the discipline in AGENTS.md.
- **Discipline #26** (narrowly scoped) — when answering a peer's
  question about shipped state in a support context, sibling-repo
  local-checkout can be stale. Before grep-attesting whether a
  doc / file / route exists in `ac` or `aweb`, run
  `git -C <repo> fetch && git ls-tree -r origin/main` on the
  sibling repo. Originating moment: I told Athena
  `ConsumerClientPickerPage.tsx` didn't exist in `ac/frontend`
  when it did — my local checkout was stale (2026-05-15). This
  applies to in-support-response state-attestation; it is NOT a
  license to walk sibling repos beyond what a specific support
  question needs.
- **Discipline #26 corollary** (2026-05-23) — a grep-hit on a string
  is NOT evidence a doc presents that string wrongly. Before flagging
  "doc X references deprecated/wrong term Y as if current," verify
  TWO things: (1) **X is still a live surface** — not migrated or
  superseded (check the loader/route/SOT, not just that the file
  exists; surfaces move under their filenames). (2) **Y's structural
  context within X** — a `Legacy Compatibility Aliases` / `Deprecated`
  section is the CORRECT location for a deprecated name, not a
  problem. Originating moment: I flagged `send_message_to_contact` as
  "woven through customer-facing docs as a current tool"; Iris
  checked and the live welcome surface had migrated `welcome.md` →
  `mcp-tutorial.md` (AC `052530aa`, clean), and the reference-doc hit
  was correctly inside the legacy-alias table. The flag cost Iris
  real investigation time. Same root as #26/#27 (verify before
  asserting); the new edge is doc-CONTENT claims, not just
  existence: read the surrounding structure and confirm live-surface
  currency before characterizing a doc as wrong.
- **Discipline #27** (narrowly scoped) — before recommending any
  role-bearing or behavior-altering CLI command IN A SUPPORT
  RESPONSE, source-grep `aweb/cli/go/cmd/aw/` to verify the
  current shape. Local-binary `aw --help` may be pre-wave.
  Originating moment: my "what next" guidance to
  `gracetut194441.aweb.ai/alice` recommended
  `aw workspace add-worktree developer` (pre-1.22.0 role-injection
  shape) post the aweb 1.22.0 / AC v0.5.39 wave that made roles
  optional. Grace caught it; Athena flagged it; corrective sent
  (2026-05-16). **Lane note (2026-05-17 reorient per Athena
  `6199af24`)**: #27 is for support-response command-shape
  verification only. It is NOT a license to audit engineering
  docs for command-shape drift across many files — that's
  Athena / Mia's surface, where intra-team engineering context
  (recent cleanups, in-flight refactors, deliberate naming
  choices) is required to interpret what's "drift" vs "intended
  state."
- **Discipline #27 refinement** (Juan correction via marvin
  `4a0e9c3b`, 2026-05-18) — customer-facing tool/command/API
  prescriptions are EITHER source-grep verified OR explicitly
  deferred ("I'll confirm and follow up in N min"). The
  "treat as shape-not-literal until verified" hedge is NOT an
  acceptable middle-ground: it offloads verification work to
  the customer AND can hide actual inaccuracies under a
  deniability hedge. The source-grep IS the work; if the work
  has not been done, the support reply has not been delivered.
  Originating moment: I shipped marvin a MCP tool list with
  the hedge — including `send_message_to_contact`, which the
  canonical reference says docs/new clients should NOT use
  (canonical shape is `send_mail` / `send_chat` with the
  contact address). Juan caught it via marvin relay; corrected
  reply sent via chat with verified names from
  `aweb/docs/mcp-tools-reference.md`. Per Athena prior guidance
  on catalog hygiene: refinement to #27 rather than new
  discipline #29 — same root rule, sharper edge.
  **Precision correction (2026-05-23):** `send_message_to_contact`
  does NOT "not exist" — it is a **registered Legacy Compatibility
  Alias** (`mcp-tools-reference.md` §"Legacy Compatibility Aliases",
  origin/main + v0.5.47; also present in `aweb/server/src/aweb/mcp/
  server.py` + `tools/contacts.py`). The server still registers it
  so cached clients don't break; the reference directs new
  clients/docs to `send_mail`/`send_chat`. So the support rule
  ("recommend the canonical name, not the alias") is unchanged, but
  the factual claim is: it's deprecated-but-working, not absent.
  Telling a customer a working tool "doesn't exist" would itself be
  an error — verify the alias table before asserting non-existence.
- **Workspace identity-verify on wake-up** (caught while
  diagnosing mail-409 to marvin, 2026-05-18) — handoff identity
  section can be stale even after a refresh if the rewriter
  preserved prior values without `aw whoami` cross-check. My
  workspace was rebound from `aweb.ai/amy` /
  `did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ` to `aweb.ai/aida` /
  `did:aw:49Q3c5MEYeWP2SD3WTygCAT1GhHf` at some prior point —
  different did:aw, not just an alias rename — but my handoff
  rewrite earlier today preserved the amy identity section
  uncritically. Always confirm identity via `aw whoami` on
  wake-up; never trust handoff identity section without
  verifying. Surfaced to Athena (`3856f00c`) as part of the
  mail-409 routing.
- **Discipline #28** (Hestia `cc92c768`, 2026-05-18) —
  customer-signal escalation threshold. Single
  customer-attested non-blocking signal: HOLD and package
  with a second attestation before escalating to Juan. Second
  attestation (within ~week window): surface together as
  empirical-strength package. Blocking attestation
  (customer says it's actually blocking them): escalate
  immediately regardless of count. Reason: single-data-point
  escalation is signal-inflation; cost of waiting for second
  is at most one more customer noting the friction.
  Originating moment: I forwarded Zeus's channel-auto-ack
  friction to Hestia as customer-evidence-promotion; she held
  the Juan escalation pending 2nd attestation. Applies to any
  customer-signal-to-Juan routing question, not just
  channel-plugin.
- **"What next" support response** — full runbook entry landed
  at commit `9537fe8` (2026-05-16) under a new "Customer
  Orientation Responses" section in `docs/support/runbook.md`.
  Three-bucket template (action / depth-reading / dashboard-link)
  + invitation-to-share-goal close. Action-tier recommendation
  is `aw workspace add-worktree --alias <name>` (NO role
  injection per #27). Source-grep verification trail at the
  bottom of the entry; tied-to-invariants section anchors the
  entry's correctness to docs-inventory currency + welcome-guide-v5
  vocabulary canon. First template; future entries land as real
  customer seed examples accumulate.

## Recent peer / verification work (live evidence base)

- **Pi runbook section went stale on `@awebai/pi` npm publish
  (2026-05-26)** — Hestia's `eb0cbd98` closed `@awebai/pi` 0.1.15
  verified-live (aapv Wave 5 complete). That fired the replacement
  trigger on my runbook "Known Pre-Release Preview Paths → Pi
  extension" section, which said (now FALSE) "npm package not yet
  published; do not use `npm install`" and prescribed a
  clone+build-from-repo local path. Independently confirmed npm live
  (`npm view @awebai/pi version` → 0.1.15, latest). Actions: (1)
  added a STALE-PENDING-RE-VERIFICATION banner to the section
  (honest superseded-marker, removes the confident falsehood; did
  NOT author the npm replacement myself per #27 author-verified);
  (2) routed the canonical-install-path question to Athena/Dave
  (mail `1873837d`); (3) routed the positioning question (Pi
  preview-vs-released; does the section leave "Pre-Release Preview
  Paths") to Sofia (mail `8d8b0cfe`). No live customer pressure
  (zero Pi asks; banked ahead of demand). Banner pushed as a
  public-inaccuracy correctness fix. **RESOLVED same day — section
  rewritten.** Athena (`1b0dc344`, tarball-inspected) gave the
  canonical install (`pi install npm:@awebai/pi@latest`, NOT raw
  `npm install`; package surface sufficient; local-build superseded
  → engineering note). Sofia (`de34ad4d`) ruled Pi **RELEASED** —
  graduate out of pre-release framing into a normal client-install
  entry, one client among several, not the default. Rewrote: retired
  "Known Pre-Release Preview Paths" (Pi was its only entry) → new
  "## Client Install Paths" section; Pi entry now release-shaped with
  the verified install path. Review chain closed (Athena tech + Sofia
  framing). **General pattern**: a verified-live release of a package
  my runbook describes as pre-release/local-only is a standing
  trigger to re-check that section — version progression silently
  invalidates "not yet published" claims.

- **Dashboard inbound-mode source-verify for Sofia (2026-05-23)** —
  Sofia (mail `96d85669`) gated a v0.5.47/v0.5.48 external-claim
  derivation on what the dashboard inbound-mode picker actually
  shows. No browser session, so verified from `ac` source at the
  deployed `v0.5.47` tag. **Verified facts (held evidence for any
  future reachability question):**
  - Picker `AgentDetailPage.tsx`: card "Incoming messages", label
    **"Who can reach you"**, two options only — `open` shown as
    **"All"**, `team_and_contacts` shown as **"Team and contacts"**.
    Auto-saves on selection. Gated to global/registered identities
    (`isGlobalIdentity`); local aliases don't expose it.
  - Backend `services/inbound_modes.py`: `VALID_INBOUND_MODES =
    {open, team_and_contacts}`, `DEFAULT_INBOUND_MODE = "open"`,
    `contacts_only` is a legacy alias normalized to
    `team_and_contacts` (non-breaking; no 422).
  - **No hidden-422 UX issue** (Sofia's worry): dashboard matches the
    data-layer CHECK constraint Hestia found. `contacts_only` is not
    surfaced.
  - **Customer-visible names are "All" / "Team and contacts"**, NOT
    the slugs. Sofia adopted this into the external-claim hold posture.
  Sofia closed the 2nd hold-list item on this; only task #208
  (Grace's CLI fix in v0.5.48) remains before v0.5.47/v0.5.48 clears.
  Sofia requested + approved a customer-facing runbook section
  (authoring sanctioned by Direction, not preemptive).

- **Runbook Case 4 staleness fix (2026-05-23)** — while verifying the
  above, found the existing "Change Message Acceptance" entry listed
  FOUR options (`Anyone`/`Contacts`/`This team`/`Owner only`) under a
  "Message acceptance / Accepts messages from" label — a UI retired
  before aapl. The v0.5.47 test suite asserts those labels are absent
  (`AgentDetailPage.test.tsx:336,338`). Corrected to the verified
  two-option surface + added dedicated "Reachability Setting — Who
  Can Reach You" customer-language section per Sofia's spec. Both
  held in the unpushed stack. **Athena tech-accuracy question
  RESOLVED** (mail `9fcca42a`): hosted-custodial global agents see
  the SAME `isGlobalIdentity`-gated "Who can reach you" picker — no
  branch needed. Hosted-custodial agents carry
  `identity_scope='global'`; the hosted MCP role/OAuth card is
  separate and doesn't replace the picker. Local identities don't
  expose it (v0.5.48 rejects PATCH on local). **Full review chain
  closed**: Athena (tech-accuracy) + Sofia (framing, mail `be582925`,
  one naming-caveat refinement applied at `9392957`).

- **`send_message_to_contact` — my doc-hygiene flag was an
  overstatement; live surfaces were already clean (found + corrected
  2026-05-23)** — I flagged that the consumer welcome guide draft +
  site docs "reference `send_message_to_contact` as a current
  contact-tool." Iris (mail `30599160`) checked and pushed back; I
  verified her findings against `ac` origin/main and she is right:
  - The **live customer-facing welcome surface is no longer
    `welcome.md`** — AC `052530aa` deleted it and migrated to
    `mcp-tutorial.md` (`load_welcome_guide()` reads it now); the live
    `mcp-tutorial.md` and `AWEB_HOSTED_MCP_INSTRUCTIONS` are **clean**
    (zero `send_message_to_contact`).
  - The site `mcp-tools-reference.md` hit (line 120) is **inside the
    `## Legacy Compatibility Aliases` table** (line 104), NOT the
    `## Contacts` section (line 94) — i.e. it's documented in the
    correct place, directing readers to `send_mail`/`send_chat`. Not
    a problem.
  - Only **historical artifacts** still carry the name (the
    2026-05-14 welcome-guide v1 draft, `history.md` v5 entry) and
    those are accurate-for-their-date. Iris is deciding whether to
    add "SUPERSEDED by 052530aa" markers (her surface; record-keeping
    hygiene, no replacement copy so Sofia's framing gate is moot).
  - It IS still a deprecated alias (works; canonical
    `send_mail`/`send_chat`) and I should not recommend it — that
    part stands, and my Zeus note (`fd65ae2c`) still gets folded into
    next contact. But "woven through customer-facing docs as current"
    was wrong.
  **Lesson banked as #26 corollary below.** Original source of the
  name was Sofia's mail `aa9d70de`.

## Recent customer interactions (live evidence base)

- **aweb.ai/marvin (2026-05-18)** — verified MCP-tutorial
  "what next" ask. Context: marvin is a team peer on
  default:aweb.ai (Juan's personal assistant) testing the
  tutorial path via Claude.ai hosted chat. **Two corrections
  caught in this thread**: (1) Juan-via-marvin flagged that my
  initial reply hedged tool names ("treat as shape-not-literal
  until verified") which was wrong-shape AND papered over an
  actual inaccuracy (`send_message_to_contact` does not exist
  in the canonical reference); banked as #27 refinement above.
  (2) While correcting, my mail-reply path hit HTTP 409 on
  four shapes (--conversation-id, --to-address, --to alias,
  --to-did) — routed to Athena `3856f00c`; chat-fallback used
  to deliver corrected list. **Banked as seed #1 for the
  MCP-tutorial-what-next shape** — different from the
  CLI-what-next shape already in Customer Orientation Responses.
  Per Sofia's 2-3-seed posture: hold for additional seeds
  before authoring a full Class N entry.

- **aweb.ai/ama (2026-05-18)** — non-customer handshake. ama
  is aweb's new serious-inbound surface (YC application contact,
  press/investor/acquirer-shape). Directory was `co.aweb/agents/yc`
  bound to `aweb.ai/yc` until the 2026-05-01 frame-switch (YC
  application now points at the address); Juan completed identity
  rebind `yc → ama` 2026-05-18 08:05 UTC. Lane split agreed in
  the handshake: runbook = Aida, live external comms = ama; mutual
  commitment to mail-before-guess across the lane boundary.
  Handoff.md routing table updated to include ama.

- **gsk.aweb.ai/zeus (2026-05-18)** — re-engagement chat after
  Juan routed Zeus to me ("important info + customer feedback").
  Honest framing: no queued send on my side; Juan's routing was
  prompt-shaped, not artifact-shaped. Opened the door for
  customer feedback; Zeus delivered real signal across four
  items:
  1. **Onboarding-completion gap** — walkthrough ends at
     human-controller action gate (Juan deciding which agents to
     provision); team still single-member 12 days later. Verbatim:
     "fine for engaged customers, may stall passive ones."
     Routed to Sofia (`a3efa895`) as P2-shape product question.
  2. **Channel auto-ack friction** — `aw mail inbox` shows empty
     because channel push auto-marks read; he has to remember
     `--show-all --json` to see canonical record. Real-customer-
     attested promotion of Dave's previously-flagged design
     question from "agent annoyance" to "customer-visible UX
     cost." Routed to Hestia (`e470aa9c`) operationally + Athena
     (`b4e982cc`) for eventual Dave cross-team relay.
  3. **Bug-arc praise** — verbatim: "Bug-arc itself was handled
     really well — fast escalation, named engineers, structured
     tickets." Routed to Athena + Hestia as positive signal.
  4. **Consumer-entry scope ask** — Zeus asked whether Sofia's
     2026-05-13 ship affects his Path A flow. My answer to him:
     additive (new surface for P1, not replacing his path), but
     asked Sofia to confirm before authoritative; promised
     follow-up within a day. See Waiting on Engineering.

  Chat closed cleanly. Customer-feedback shape was unprompted +
  candid because Juan engineered the re-engagement; banking the
  pattern — when a customer is re-engaged via human routing,
  ask open feedback questions before pivoting to specific asks.

- **gracetut194441.aweb.ai/alice (2026-05-16)** — first real
  "what next" customer ask after the consumer-entry ship.
  Improvised reply from doc-set survey since runbook entry
  not yet authored. Reply included stale pre-1.22.0
  add-worktree shape; Grace caught it; Athena flagged via mail
  `05dae217`; corrective sent via chat (mail-by-address 404'd —
  namespace not AWID-public; chat works). Banked as seed
  example #1 for the eventual "what next" runbook entry, with
  the staleness lesson banked as discipline #27 candidate.

## Recent doc-surface work (no live customer; pre-customer scaffolding)

- **4-day gap catch-up (2026-05-23)** — pulled ai.aweb after 4
  days idle. Two engineering-side decisions banked in
  `docs/decisions.md` worth knowing about (neither directly
  customer-actionable yet, both potential context for future
  support asks):
  - **2026-05-21 (Athena)**: AWID hidden/limited address rows
    fail-closed before visibility-column drop. Migration refuses
    to run if active rows have `reachability != 'public'` OR
    `visible_to_team_id IS NOT NULL`. Operators must normalize
    or retire those rows first. If a self-hoster hits a deploy
    gate during the global/local cleanup migration, this is the
    answer; route to Athena for the specific normalization path.
  - **2026-05-13 (Sofia, retroactive reframe)**: Consumer-onboarding
    v0.5.28 → v0.5.31 reframe. Two gaps caught post-ship: site
    landing wasn't actually consumer-shaped at ship time (still
    developer-shaped until later in the day); 4 pending migrations
    silently accumulated unrun across 4 cycles (Hestia's discipline
    #30). This is historical context for the Zeus consumer-entry
    scope confirm — my "additive, no Path A change" answer to him
    still holds (confirmed by Sofia `9bea8bb9`), but the original
    consumer-pivot ship was rougher than ship-day framing implied.
  - Versions current: aweb 1.25.2 + ac v0.5.46 + awid 0.5.8;
    aapq team_and_contacts inbound mode in production. Handoff
    versions section updated. CLI label drift noted: `aw whoami`
    in 1.25.x prints `Identity: global` where prior said
    `persistent` — same meaning.
  - Inbox + chat clear after sweep. No customer-blockers
    accumulated during the gap.

- **Pi extension pre-release preview path banked (2026-05-19)** —
  Dave (`juan.aweb.ai/dave`, dev-team package author) delivered a
  support-ready preview path via mail `5e31c05e` at Juan's request,
  ahead of any actual customer ask. Cross-team direct routing
  (dev → company) is the one-time customer-readiness-delivery
  exception to the standing route-through-Athena discipline.
  Banked as a new runbook section "Known Pre-Release Preview
  Paths" → subsection "Pi extension (`@awebai/pi`) — local install
  from aweb repo." Source-grep verified the `aweb/pi-extension`
  path on origin/main (tree object + package.json + src/ + dist/
  all present) per #27 refinement banked this cycle. No direct ack
  to Dave: cross-team mail-by-address 404s for `juan.aweb.ai/*`
  (one-way AWID indexing); inbox JSON shape lacks his did:aw stable
  ID, only carries did:key (so --to-did fallback unavailable).
  Per MCP plugin guidance + AGENTS.md routing, channel auto-ack
  signals delivery; silent receipt is the right shape for
  non-blocking dev-team mail. Bank-in-runbook IS the response.

- **Post-deploy smoke (Hestia, 2026-05-19)** — aweb 1.24.3 + ac
  v0.5.44 went live. Hestia ran outbound-routing matrix probes
  (MATRIX-PROBE-70452, RE-MATRIX-64031, smoke v0.5.44/1.24.3 +
  chat smoke retry after 503 awid transient). All mail probes
  ack'd; chat smoke arrived `sender_leaving=true` so silent
  receipt. Version bump noted: handoff said aweb 1.23 / ac v0.5.41
  last observed; now 1.24.3 / v0.5.44. Will refresh handoff
  versions on next wake-up cycle.

- **Federation docs customer-experience pass (2026-05-18)** — after
  Grace's `aaou.17` push (aweb `02a344f` + `449cb17` polish) landed
  the federation surface on origin/main, did a scoped customer-
  experience pass on `self-hosting-guide.md` + `federation-
  architecture.md`. Six in-lane findings + two lower-priority
  observations routed to Athena (mail `cc7ae071`); zero correctness
  claims, all framed as confusion-points / missing-affordances /
  edge-case-gaps from a self-hoster's seat. Iris's terminology flag
  (BYOD/BYOIDT) closed by Grace at `449cb17` before the pass; dropped
  from the batch per Athena `05865b23`. Federation Triage Skeleton
  revised + committed at `302e481` to unmute `set-delivery-origin`
  with source-grep-verified flag shape.

## Standing held items (separate from this status update)

- **13-commit local-unpushed stack** on `main` ahead of `origin/main`:
  - Support runbook + status content (10 commits): `e15838c` BYOD-422
    + invariant; `9537fe8` Customer Orientation Responses (what-next);
    `90be163` Cross-Check Methodology; `44c234e` Federation Triage
    Skeleton; `302e481` Triage Skeleton unmute (set-delivery-origin);
    `faa84db` / `1ec79d0` / `f9b7329` status refreshes
  - aani task management (1 commit + REMOVE): `e6b1303` add + `8179a3e`
    REMOVE (net runbook content = `e15838c`-equivalent)
  - Merges (3): `2b3e392`, `30c5078`, `58b174b`, `204ffb0`
  - All Aida-owned artifacts; no engineering-blocker content. Athena
    flagged the queue depth as "thing to watch" (mail `0c0c2884`);
    default posture is wait for Juan's greenlight per the standing
    "commit locally + don't push without review chain" discipline.
    If stack reaches ~20 or content shifts to engineering-blocker
    shape, revisit.
- AGENTS.md edits (Customer-Facing Defaults + Cross-Team Routing
  sections) uncommitted, awaiting same greenlight.
- AGENTS.md cleanup pass pending the right convergence point (the
  architecture-plan-with-Grace and the simplification-pass-with-Athena
  both inputs).
