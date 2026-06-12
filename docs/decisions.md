# Decisions

When the plan changes, record it here with the commit hash(es) that
mark the moment. Agents check this for entries newer than their last
handoff to detect that the world changed.

---

## 2026-06-12 — Release policy: we cannot ship with failing tests, ever

**Commits:**
- ai.aweb: this commit — decision record (policy stated by Juan in team session 2026-06-12; Hestia banked operationally same day)

**Decision maker:** Juan.

No release ships while any test in its gate chain is failing. There is no "known flake" exemption, no non-regression accept for a red test, and no shipping-with-footnote. A failing test either gets fixed, or the failure gets diagnosed and the test corrected — before the lane proceeds.

Context: two E2EE journey tests (hosted custodial dashboard decrypts self-custodial chat; self-custodial CLI chat session matches encrypted row) failed with IDENTICAL labels across five consecutive AC ships (v0.5.69 → v0.5.72 + proposed v0.5.73) while characterized as flake. Re-examination showed consistent broken behavior on an untested cross-custody path (self-custodial CLI → hosted custodial chat → dashboard pending decrypt). Grace withdrew her non-regression accept for v0.5.73; Hestia halted the release lane; incident triage opened as aweb-aaqt/aaqu.

Corollary discipline (banked in Hestia's runbook alongside #23): identical failure labels across consecutive runs are consistent broken behavior, not flake. "Same failure twice with the same label" triggers incident-shape triage, not re-run-and-accept. Applied at ship two of five, this catches the mislabel three ships earlier.

Direction effect: external claims attached to a release wave are suspended (not withdrawn) while a journey gate in that wave is red — the v0.5.72/aaqa.20 claim approved 2026-06-12 is the first application.

Affects: every release lane (AC, aweb, awid, packages), Grace's gate-accept criteria, Hestia's runbook, Sofia's release-claim framing checklist.

---

## 2026-06-10 — Rollback invariant: transactional locally, conservative remotely (invariant 9)

**Commits:**
- aweb: `4518c85c` — release: aw 1.26.14 (aweb-aaqi fix shape the invariant generalizes)
- ai.aweb: this commit — invariant 9 in `docs/invariants.md`

**Decision maker:** Sofia (direction framing), Athena (technical wording — load-bearing refinement), Hestia (ops-chain ACK; runbook standing policy #16).

Two incidents shared one failure class: #245 (aw 1.26.3 read/status cleanup destroyed workspaces based on stale local path state) and aweb-aaqi bug-3 (connect failure-path rollback deleted the local key after remote init had already succeeded, manufacturing a DID mismatch that orphaned a global identity row). Both are rollback/cleanup logic destroying state whose remote counterpart was in a different state than locally assumed.

Banked as invariant 9 in `docs/invariants.md`: failure-path rollback must be transactional over known local writes and conservative about remote uncertainty; automatic rollback may remove only artifacts this attempt created that are not the last remaining authority/correlation handle; destructive cleanup of confirmed remote state must be an explicit authorized lifecycle action, never an incidental side effect. Corollary: manifest/snapshot-based rollback, never broad `rm -rf .aw`.

Sofia's original stronger form ("local cleanup only when remote counterpart confirmed absent") was rejected on Athena's technical read: remote absence is unknowable after timeout/422-after-partial-success/network split, and the stronger bar would freeze safe local rollback of staging files. The safety bar is preserving the last local signing authority / durable correlation handle while remote success is possible.

Affects: all aw CLI failure-path/rollback code (review against invariant 9), Hestia's release/cleanup operations (runbook #16: #271-pattern server-side cleanups are the explicit authorized action the invariant points at; identity-state cleanups additionally need explicit Juan-go or controller-signed authority), and future code review of any flow that deletes `.aw` state.

---

## 2026-05-21 — AWID hidden/limited address rows fail closed before visibility-column drop

**Commits:**
- aweb: `605f356` — Fail closed before dropping legacy address visibility
- aweb: `d300b33` — Cover AWID visibility drop gate

**Decision maker:** Athena (engineering), with Grace requiring executable migration evidence before validation handoff.

Active AWID address rows with legacy non-neutral visibility metadata are not normalized by migration and are not silently widened into ordinary addressed/global aliases. The AWID migration that removes `public_addresses.reachability` and `public_addresses.visible_to_team_id` now refuses to run while any active row has `reachability != 'public'` or `visible_to_team_id IS NOT NULL`.

Operators must explicitly normalize or retire those rows before a deploy can remove the old metadata. Soft-deleted address rows do not block because dropping their old metadata does not make them routable.

Why: the global/local cleanup removes the old reachability authority, but existing hidden/limited rows were created under the old model. Dropping the columns without a gate would silently widen privacy. Failing closed preserves the simplification while forcing an explicit operator disposition for legacy rows.

Executable regression coverage at `d300b33` proves active `nobody` and `team_members_only` + `visible_to_team_id` rows block, deleted non-neutral rows do not block, and active neutral rows pass and drop both columns.

Affects: AWID migrations and release/deploy gates for the global/local cleanup. No row mutation is performed by the migration.

---

## 2026-05-13 — Consumer-onboarding release cycle reframe: v0.5.28 → v0.5.31, two gaps caught post-ship, transparency note

**Decision maker:** Sofia (framing lane), with Hestia surfacing both empirical gaps.

**What this captures.** The first ship of the consumer-pivot epic
(aweb-aanp + aweb-aanw, bundled with aweb-aanv) shipped across four
backend cycles 2026-05-12 → 2026-05-13. Two gaps in the original
v0.5.28 release-claim framing were caught after verified-live; this
record corrects the framing.

### What actually shipped, by version

**v0.5.28** (verified-live ~18:55Z, 2026-05-12 → 2026-05-13)
gate-input SHA 00064992. Backend mechanics for consumer onboarding:
hosted-identity provisioner (aanp.3), consumer MCP OAuth account
birth + per-client identity (aanp.4), handle-level contacts + pending
state (aanp.5), consumer MCP contact tools incl. wrappers (aanp.6),
OAuth Consent UI (aanp.7), consumer client picker SPA at /connect
(aanp.8), needs_signin polish + signup-paths alignment (aanw.1-.16),
post-register routing by source param (aanv 28e7062e), Stripe
return_path allowlist (aanv 41b46ea6).

**Gap 1 caught 2026-05-13 ~19:00Z**: `aweb.ai/` site landing
surface was NOT updated. Production homepage last-modified
2026-05-11, still developer-shaped (npm install above the fold,
no consumer-first framing, no `/developers` split). `/developers`
returned 404. The original v0.5.28 release notes claimed
"aweb.ai is now consumer-first per the P1 priority" — true on
main; not true in production. Site code on main but site deploy
held pending Bertha/Eugenie validation per Hestia's separate
lane. The headline customer outcome arc ("lands at aweb.ai →
clicks Connect your AI...") was broken at step 1 in production.

**Gap 2 caught 2026-05-13 ~19:49Z** (Hestia, banked as her
discipline #30): 4 pending migrations had silently accumulated
unrun across v0.5.25 → v0.5.29 (4 cycles). The aweb.contacts
schema additions (handle_namespace, reference_type, status,
target_agent_name) that v0.5.28's ContactView fix at 00064992
expected were NOT in production until 19:49Z. During the
verified-live window for v0.5.28 (~1 hour) the contact-ingestion
functionality was at minimum degraded — fields silently dropped
or 500-ing in handlers. Resolved via `make prod-migrate-direct`.

**v0.5.29** (verified-live ~19:49Z, 2026-05-13)
session-recognition fast-follow. Schema-drift resolution landed
during this deploy window via Hestia's manual migration run. The
v0.5.28 contact-ingestion path became correct as soon as the
schema caught up. Framing-review under abbreviated fast-follow
process; no separate draft.

**v0.5.30** (HALTED at gate-input, 2026-05-13)
tag 8c3d9dc1 created and pushed to origin; image build halted in
GHA; no deploy; no verified-live mail. Grace surfaced 4
invariant gaps at review; tag was NOT force-deleted. The
v0.5.29 → v0.5.31 version-number gap is itself documentation
("Grace's first pass had follow-up gaps caught at review,
shipped invariant-correct as v0.5.31"). Athena's framing.

**v0.5.31** (verified-live, 2026-05-13)
gate-input SHA 21cb6c23. Invariant-correct controller_did fix
for returning-customer-new-agent AWID divergence (Grace
2993189d). OAuth raw-JSON redirect leak fix per RFC 6749 §4.1.2.1
(Olivia fdede778). OAuth error-surface defensive tightening:
enumeration-oracle in error_description detail (M1), GET
/oauth/authorize catch-all (M2), policy comment (m1) (Olivia
06e1ae3d, Mia Ship-OK).

### What is live as of 2026-05-13

- Backend consumer onboarding mechanics (claim-MCP-OAuth, handle
  picker, contact tools, message wrappers, signup paths) — LIVE
  at v0.5.31, schema current.
- Consumer SPA routes — `app.aweb.ai/connect`,
  `app.aweb.ai/oauth/consent`, `app.aweb.ai/register` — React
  shell loads (HTTP 200 confirmed); customer-voice walk of
  rendered content pending browser tooling (Playwright not loaded
  for Sofia this session).
- AWID at 0.5.4, aweb at 1.21.0 — current.

### What is NOT yet live

- **`aweb.ai/` consumer-first homepage** — code on main (aanv
  8e0b59af landing split); not deployed. Production still on
  Pass-3 60be8f4e developer-shaped homepage.
- **`aweb.ai/developers/`** — code on main; not deployed; returns
  404 in production.
- **Iris's site iteration at 0a9b1654** — on staging
  preview-urw1.onrender.com; Bertha/Eugenie sign-off chain
  incomplete.
- **Customer discovery / entry surface** — until aweb.ai
  homepage updates, a P1 customer landing at aweb.ai sees
  `npm install` and bounces. The headline customer outcome arc
  remains broken at step 1.

### Implications

**For external claims**: do NOT claim the consumer flow is
end-to-end shippable to real P1 customers until the site deploy
lands with Bertha/Eugenie greenlight. The backend MECHANICS
work; the marketing ENTRY surface doesn't.

**For Iris**: content reorient still has nothing to point at.
Holding the (a) Twitter/X thread shape we converged on until
the site lands.

**For Aida**: P1 + P2 support questions cannot meaningfully
arrive yet because P1 has no entry path from aweb.ai. Watch
for them once the site is live; saved-seed-examples shape
unchanged.

**For Sofia (banked)**: framing-review must include
spot-checking the deployed surface for any release-notes line
that names a customer-facing arc — not just trusting the
release-notes description. Same "published artifact ≠ deployed
service" pattern banked in prior memory; application of it in
framing review needs to be explicit. Banked in
`feedback_framing_review_requires_deployed_spot_check.md`.

**For Hestia (banked)**: schema-migration verification is part
of verify-live, not /health. Hestia discipline #30, banked
runbook-side.

### Sequencing

1. Site deploy (when Bertha/Eugenie greenlight) closes the
   discovery gap. Hestia carries the deploy through her runbook.
2. Once deployed, Sofia walks the customer-voice arc against
   production (browser-based, when tooling available).
3. Iris + Aida fan-out follows once production matches the
   headline customer outcome.
4. Schema-migration verify-step now embedded in Hestia's
   verified-live chain per discipline #30.

### Update 2026-05-13 22:28Z — site live, holds released

Hestia deployed `make deploy-site` from ac/ at 22:28Z; Render
rebuild ~13min from push. deploy-landing tip 21cb6c23 (matches
main HEAD; same SHA carries v0.5.31 backend + Peter's
pain-narrative + Eugenie's rewrite + the staging iteration
commits). aweb.ai live with the consumer-shaped pain narrative.

Sofia walked the customer-voice arc against production (mail
ad2c6dfe to Hestia):

- aweb.ai hero: "You're still doing the work your AI should be
  doing" / "aweb lets your AIs talk to each other directly..."
- CTA "Connect your AI" → app.aweb.ai/connect
- No developer vocabulary above the fold (checked for npm,
  install, terminal, CLI, namespace, controller, did:aw, DNS,
  certificate, agent identity, worktree, cryptographic — all
  clean)
- Section flow: hero → "the relay" → "coordination, without you"
  → "what aweb guarantees" → pricing → footer
- "Developers" link in nav for the P3 audience
- aweb.ai/developers/ dev-shaped landing exists (200, 26366b)
- /docs/consumer-onboarding/ exists

**Headline customer outcome arc now plausibly complete end-to-end.**
Step 1 (lands at aweb.ai → sees consumer-shaped pain narrative)
was the gap; closed. Steps 2-5 ride on backend mechanics + SPA
shells already verified-live + 1373 backend tests + 11 Playwright
browser journeys.

**Holds released**:
- Iris: mailed (23955416, conv 345f95bb) to move on the (a)
  Twitter/X thread shape we converged on. Deployed product gives
  her something to demonstrate.
- Aida: mailed (aa9d70de, conv 13f8003a) with watch-list of P1+P2
  support shapes likely to arrive (handle-discovery friction, OAuth
  consent confusion, pending vs active contact state, vocabulary,
  observability, blocking).

**What moves from "not yet live" to "live"**:
- aweb.ai consumer-first homepage ✓
- aweb.ai/developers/ ✓
- Consumer discovery / entry surface ✓

**What remains pending**:
- Bertha/Eugenie sign-off chain — separate process; deploy
  happened on what was ready; their resolution is independent.
- aweb-aanp.6.1 email-typed contacts — backlog.
- aweb-aanp.10 OpenAI App Directory submission — pending Juan
  screenshots + help-page paste.
- FUT-1 Anthropic Connectors Directory submission — Iris queue.
- Real customer signal — none yet; once it arrives, refine
  framing and runbook sections.

The consumer pivot v1 cycle is closed for this iteration.

---

## 2026-05-12 — Persona priority reorder: consumer first, dev team third, platform builder last

**Commit:** (this commit — adds personas 1+2 to `docs/audiences.md`
and reframes the doc to "persona" terminology)

**Decision maker:** Juan (founder call), with Sofia capturing.

**What changed.** The persona ordering for likely-first-customer
shifted. Old order (still implicit in much of the product, landing
copy, and content):

1. Developer teams coordinating agents
2. Agent platform builders

New order (effective 2026-05-12):

1. **Personal-AI consumer** — individual ChatGPT / claude.ai /
   Gemini user who wants her AI connected to her friends' AIs via
   MCP. Doesn't want to know about teams, roles, or any identity
   vocabulary. Mental model is {my AI, my address, my contacts,
   who can reach me}.
2. **Company with AI-using employees** — many employees each
   running their own browser/desktop AI; company wants those AIs
   to help the humans communicate. Custodial across the board.
3. **Developer teams coordinating agents** — was #1; demoted to
   #3. Still the persona with the most direct product-fit
   evidence (44 internal users); still the architectural anchor;
   no longer the lead persona for landing-copy / onboarding /
   content priorities.
4. **Agent platform builders** — was #2; demoted to last. Long-
   term defensibility; no near-term product prioritization for
   this persona.

**Why.** Conversations over the past weeks (Juan + outreach
contacts) indicate the consumer and company-fleet shapes are
more likely first customers than developer teams. The two new
personas share a UX shape: browser-based custodial MCP, no
terminal, vocabulary limited to {address, contacts,
reachability}. Both are already plausible without us building
anything new on the protocol layer — the work is onboarding,
packaging, and submission to the MCP-client directories.

The dev-team persona stays load-bearing as the architectural
anchor and the only persona with real product-fit evidence
today. The reorder is about who we *reach first*, not who we
*build for* — the architecture must continue to serve all four.

**What it affects.**

- **Product / engineering**: aweb-aanp epic + FUT-1 (Anthropic
  Connectors Directory submission) + FUT-2 (OpenAI App
  Directory submission) become higher priority. Dashboard
  reframe — the 9 team-tabs assume a developer-team mental
  model that's hostile to Persona 1; UX simplification pass
  pending (Sofia + Athena).
- **Landing copy**: the homepage Pass-3 framing was already in
  the right direction (custodial-MCP first); next pass should
  push further toward Persona 1 vocabulary and remove dev-team-
  first signals from the hero / above-the-fold.
- **Content / outreach (Iris)**: target audiences shift toward
  consumer + company-fleet hangouts (consumer Reddit, AI
  newsletters, LinkedIn for company-fleet decision-makers).
  Voice guide carries the principles but the channel mix
  changes.
- **Support (Aida)**: runbook framing must expand beyond "what
  CLI users hit"; consumer + company-fleet customers will not
  have terminal-shaped questions.
- **Analytics (Metis, when online)**: signal definitions for
  persona-fit will include consumer + company-fleet shapes.
- **Pricing / business model**: not changed by this reorder. To
  be revisited as customer-fit evidence accumulates for the new
  personas.

**What is NOT changed.**

- The architecture (four primitives, two product tiers, identity
  trust chain).
- The dogfooding work on Persona 3 (44 internal users on this
  team's own workflow). That continues; it's what proves the
  product works.
- The voice guide principles (`publishing/voice.md`). Channel mix
  shifts, voice doesn't.
- Decision records and invariants for prior cycles.

**Next motions queued.**

1. Sofia + Athena converge on UX simplification implications
   (the 9-tab dashboard, 25-command CLI, 45 MCP tools as seen
   through the new persona lens). Working artifact:
   `agents/sofia/ux-surface.md` + `agents/sofia/ux-surface.html`.
2. Iris reorients content / outreach targeting once she's online.
3. Aida absorbs Persona 1 + Persona 2 into runbook framing.
4. Metis defines persona-fit signals once online.

---

## 2026-05-06 — Messaging-architecture cycle close: aame epic + pagination fix verified end-to-end

**Commit:** `3e9a378` Messaging-architecture cycle close: v0.5.23 verified-live + framing ready for distribution

**Decision maker:** Sofia (cycle framing) + Athena (technical content) + Hestia (verified-live + disciplines).

**What this captures.** The messaging-architecture cycle
(2026-05-03 → 2026-05-06) is closed and verified end-to-end. aweb
1.20.2 + ac v0.5.23 are live as of 2026-05-06 06:14:33Z. The arc:

- aweb 1.20.0 (2026-05-03): aame epic — first-class conversation
  primitive, W3 cross-conversation replay protection,
  conversation-aware CLI flags, 218 e2e tests.
- aweb 1.20.1 (2026-05-04): chat-reply hotfix.
- ac v0.5.22 (2026-05-05): cloud uptake of aweb 1.20.1; aame
  architectural completion verified-live (decision `96134d6`);
  pre-deploy duplicate-1to1 cleanup (195 conversations across 16
  pairs).
- aweb 1.20.2 (2026-05-06): mail-409 pagination fix
  (`/v1/conversations` gains optional `participant_did`,
  `participant_address`, `conversation_type` filters; CLI uses
  focused query instead of first-page-of-100 sort).
- ac v0.5.23 (2026-05-06): cloud uptake of aweb 1.20.2;
  pagination fix verified-live.

**Empirical attestation: three smoke probes against deployed v0.5.23
+ aweb 1.20.2.**

1. Baseline auto-thread (page-1) — conversation `96317ca9`
   (Athena↔Hestia, post-deploy). Clean.
2. Stale-by-recency from default-team — conversation `878c06b1`
   (Sofia↔Hestia, originated 2026-05-05 from yesterday's v0.5.22
   framing reply). Pushed off first-100-most-recent by intervening
   chat activity. Auto-thread worked.
3. Stale-by-recency from cross-team-agent (load-bearing case) —
   conversation `70f1c868` (Sofia↔Athena via Athena's default-team
   agent_id). The exact 409 case that drove 1.20.2. CLI hit the new
   server filter, server returned focused response containing
   `70f1c868`, dedup matched, delivery succeeded.

Pagination fix verified-live on every shape hypothesized.

**Disciplines banked in Hestia's runbook (#18-#23).** Six
operational disciplines from this cycle. Per banked-learnings
routing, engineering-discipline lives in `agents/hestia/runbook.md`;
brief list as cross-reference: verified-live cites actually-committed
SHA (#18); work-in-flight ≠ released until tag pushed +
live-verified (#19); reproducer must match empirical surface (#20);
bless-and-run from peer = run FULL release-ready chain (#21);
code-reviewer subagent flagging silent-fall-through + scale realistic
for production trajectory ⇒ blocker, not follow-up (#22); date-
fragility ≠ transient-flake — recurring failures at specific clock
windows + reruns clean later are timezone-math signals (#23, caught
by Juan's pushback). Canonical home in Hestia's runbook.

**What this cycle did NOT close.**

- **chat-403 on pre-aame chat sessions**: customer-side workaround
  documented in Aida's runbook PR (`3279c973`). Signal threshold for
  code fix: 2nd case in rolling 7d.
- **Multi-team-agent agent_id-vs-did comparison**: cp.agent_id is
  team-scoped; same did_key/did_aw across team memberships maps to
  different agent_ids. Athena's lane (grep aweb codebase). Open ops
  follow-up; non-blocking.
- **Pytest-randomly seed-driven test contamination**: closed without
  fix; root cause was date-fragility on UTC-vs-local-midnight,
  banked as discipline #23 + fix at `b7e86745` lives on main, ships
  next AC release.

**Framing ready for distribution.** The cycle narrative is
positioning-grade for outreach and YC: bug-class flagged →
diagnosed → shipped → verified-live in ~24h with multi-agent
coordination across the build/ship boundary; six disciplines banked
from one cycle; date-fragility caught by Juan's pushback. The
cycle-narrative is durable here; the customer-facing and protocol-
positioning framings live in decisions `7d915e8` (protocol-primitive
ship) and `96134d6` (architectural completion). Iris is not yet
online (Hetzner identity setup pending); canonical framing is in
those records for her wake-up. Routing to Eugenie via Juan is
available now if external posting timing wants the narrative ahead
of Iris's activation.

**Cross-references.**

- Architectural-completion decision (`96134d6`, 2026-05-05 evening).
- Protocol-primitive decision (`7d915e8`, 2026-05-05 morning).
- Migration-immutability gate (`3d7f878b`, 2026-05-05): structural
  prevention; proved its keep on v0.5.22 deploy and again on v0.5.23.
- Hestia's runbook for the six banked disciplines (canonical home).
- 1.18.6 trust-model pivot (commit `7759abc`).
- Invariant 8 (`docs/invariants.md`: findability and continuation
  are independent reachability concerns).
- KI#1 closure decision record: still pending; Athena's tech content
  owed when she's ready.

**Affects.** No code changes in this commit; durable artifact
banking the cycle close. Future cycles inherit the disciplines via
Hestia's runbook. Distribution work (Iris when online, or Juan +
Eugenie now) has the source narrative ready.

---

## 2026-05-05 — aame architectural completion verified-live: writing creates a reply channel (aweb 1.20.1, ac v0.5.22)

**Commit:** `96134d6` aame architectural completion verified-live: writing creates a reply channel

**Decision maker:** Sofia (framing) + Athena (technical content + bless-and-run) + Hestia (gate chain + verified-live + misclaim flag).

**What shipped (architectural completion of aame).** The protocol
primitive that shipped this morning (aweb 1.19.1 / ac v0.5.21 — see
the decision entry below) was incomplete for AC managed identity:
cloud customers' did:keys without team-cert mode could not reliably
continue conversations across team boundaries via address routing.
Aida's onboarding flow surfaced the gap as customer-blocking shape
A.6a during the day. Today's ship closes it.

The customer-facing claim that becomes accurate at v0.5.22:

- Writing to someone creates a reply channel they can use back,
  end-to-end across team boundaries
- AC managed identity (cloud customers without team-cert mode) can
  continue conversations via address routing
- Cross-team chat reply with private team-members-only target lands
  in the same conversation
- Mail auto-thread to an existing 1:1 works for both alias-routing
  and address-routing

**Empirical attestation.**

- Morning ship (decision `7d915e8`): aweb 1.19.1 / ac v0.5.21 —
  protocol primitive verified-live 2026-05-05 07:11Z.
- Aida's onboarding A.6a surfaced the AC managed identity gap during
  the day.
- aweb 1.20.0 + aweb 1.20.1 shipped through Athena's iteration.
- **aweb 1.20.1 was a misclaim release**: its release notes claimed
  a fix that was empirically null on A.6a; the actual A.6a fix
  landed in AC commit `f6c27c61`. **If external posting cites aweb
  1.20.1 as the fix release, that's wrong — cite AC `f6c27c61`.**
  Caveat banked here so future agents reading commit history don't
  get confused.
- ac v0.5.22 deployed 2026-05-05 21:27Z. `app.aweb.ai/health`:
  `release_tag=v0.5.22`, `git_sha=f6c27c61`, `aweb_version=1.20.1`,
  `awid_service_version=0.5.4`. Healthy.
- Two Hestia smoke probes post-deploy (after duplicate-1:1 cleanup):
  `aw mail send --to athena` → conversation `96317ca9`;
  `aw mail send --to-address aweb.ai/athena` → SAME conversation
  `96317ca9`. Athena's reply confirmed
  `verification_status=verified`. The exact dual of A.6a — the
  failure shape that drove three rounds of iteration — now passes in
  production.
- Migration-immutability gate (commit `3d7f878b`, banked this
  morning) proved its keep on this deploy: no migration drift
  through gate-time → deploy.

**External framing (for outreach + future verified-live mails + YC
posting moments).**

Customer-facing version (use in verified-live mail body and outreach
drafts):

> When you write to someone in aweb, they can now reply back to you
> in the same conversation — across team boundaries, across hosted
> and self-hosted identities, regardless of whether you addressed
> them by alias or address. Writing creates a reply channel; that
> channel works end-to-end.

Protocol-positioning version (for YC-grade language at external
posting moments — coordinate with Iris and the YC agent on timing):

> aweb's conversation primitive is now a fully reciprocal
> addressable unit. Cross-team agent coordination works without
> either side requiring the other to be publicly findable to receive
> a reply. The cert-presentation auth model (1.18.6) extends to
> conversation-scope (1.19.1) and now operates symmetrically across
> all identity-routing paths (1.20.1 + ac v0.5.22).

**What this is not.**

- Not always-encrypted payloads (separate concern).
- Not a new auth model (extends the 1.18.6 cert-presentation
  predicate).
- Not the first messaging in aweb (mail/chat shipped in 1.16.x; the
  conversation primitive is the binding/lifecycle layer).
- **aweb 1.20.1 release notes are misclaim-grade**: the actual A.6a
  fix landed in AC `f6c27c61`. External posting must cite the AC
  commit, not the aweb tag.

**Cross-references.**

- Morning ship decision (`7d915e8`): protocol primitive verified-live
  (aweb 1.19.1 / ac v0.5.21). This entry is the architectural
  completion that makes the customer-facing claim accurate.
- 1.18.6 trust-model pivot (commit `7759abc`): cert-presentation
  auth predicate, foundation that aame extends to conversation-scope
  and now operates symmetrically across identity-routing paths.
- Migration-immutability gate (commit `3d7f878b`): structural
  prevention from this morning's banked discipline; proved its keep
  on tonight's deploy.
- Invariant 8 (`docs/invariants.md`: findability and continuation
  are independent reachability concerns) — aame's symmetric
  reciprocal routing is the operational realization.
- KI#1 closure decision record: still pending; Athena's tech content
  is owed.

**Affects.** Cloud at v0.5.22 carries the rollup. Customer-facing
flow (Aida's onboarding A.6a) is unblocked. External framing ready
for outreach (Iris when online) and YC posting work; voice-shape per
`publishing/voice.md`. Migration-immutability gate now mechanically
enforced at AC release-ready.

---

## 2026-05-05 — aame verified-live: conversations as first-class primitive (aweb 1.19.1, ac v0.5.21)

**Commit:** `7d915e8` aame verified-live: decision record for conversations as first-class primitive

**Decision maker:** Sofia (framing) + Athena (technical content + bless-and-run) + Hestia (gate chain + verified-live).

**What shipped.** Conversations are now a first-class object in the
aweb protocol. Signed message canonical payloads bind
`conversation_id`, so the same payload cannot be replayed across
conversations. The cert-presentation auth predicate from 1.18.6
(commit `7759abc`) extends to conversation-scope without introducing
new trust primitives. Conversations bind at the persistent did:aw
layer, so rotated did:keys continue conversations.

Specific shape:

- `conversations` table records `conversation_id`, type
  (`mail`|`chat`), TTL, participant set
- W3 enforcement: every signed message canonical payload binds
  `conversation_id`
- Legacy pre-aame messages flagged `verified_legacy`; continuation
  paths reject `verified_legacy`
- Lazy 30-day sliding TTL; check-on-read (no background sweeper)

**Live state (verified 2026-05-05 07:11Z).** `app.aweb.ai/health`:
`release_tag=v0.5.21`, `aweb_version=1.19.1`, `git_sha=8d6b37a2`,
`awid_service_version=0.5.4`. aweb OSS 1.19.1; aw CLI 1.19.x; awid
0.5.4; channel 1.4.0.

**Empirical attestation.**

- 2026-05-03: aweb 1.19.0 / aw 1.19.0 / awid 0.5.4 / channel 1.4.0
  shipped (OSS layer).
- 2026-05-04: v0.5.19 cloud deploy attempted; FAILED on two
  regressions (migration checksum drift; routing guard breaking
  same-team mail/chat). Rolled back to v0.5.18.
- 2026-05-04 evening: aweb 1.19.1 shipped with routing fix (extracted
  `address_auth.py`: same-team team_id-equality + cryptographic
  signature verification before signed_payload binding). 9
  reproducer-as-gate tests across HTTP and MCP surfaces.
- v0.5.20: aweb-schema cutover #1 (consolidated 001 from `49b1525c`;
  schema-equivalence proven IDENTICAL).
- v0.5.21: aweb_cloud-schema cutover #2 (Grace's `8fa36cd0`
  disciplined recovery via file-revert + forward-additive 002;
  schema-equivalence IDENTICAL; closed schema drift, 226 baseline
  restored, 6 cross-schema FKs restored).
- Both cutovers + 1.19.1 routing fix verified-live via
  channel-routed mail/chat smoke probes.

**What this is not.**

- Not the first messaging in aweb — mail and chat shipped in 1.16.x.
- Not a new auth model — extends 1.18.6 cert-presentation predicate
  to conversation-scope.
- Not always-encrypted-payloads — conversations are routing/replay-
  protection infrastructure; payload encryption is separate work.

**Why this matters.** Any agent-to-agent flow that coordinates over
multiple turns needs replay protection at conversation scope.
Without it, an adversary capturing one turn's signed message could
replay it into a different conversation under the same recipient.
Conversations as first-class objects make that impossible by
construction. Load-bearing for cross-organizational agent
coordination — once two organizations' agents have repeated business
with each other, conversation-scope is what makes the trust model
durable across the boundary.

**Cross-references.**

- 1.18.6 trust-model pivot (commit `7759abc`): cert-presentation
  auth predicate, the architectural foundation aame extends.
- KI#1 closure decision record: still pending; Athena has tech
  content ready (cert-presentation auth correction + aalk continuity
  arc + 1.18.6 trust-model arc + Aida 4/4 attestation). aame and
  KI#1 sit in the same arc — KI#1 is the trust-model pivot
  (April 2026); aame is the protocol primitive that exercises that
  pivot at conversation scope (May 2026).
- aame park decision (commit `c874f2a`, 2026-05-02): superseded by
  Juan's unpark (commit `325556a`, 2026-05-02); now ratified by
  ship.
- Invariant 8 (`docs/invariants.md`: findability and continuation
  are independent reachability concerns) — aame is the
  implementation that operationalizes invariant 8 in the protocol.

**External framing routing.** Sofia mails Hestia (the language to
use in the verified-live external-facing mail body) and Iris (the
framing for outreach drafts) separately. Both source content is
the "What shipped" + "What this is not" + "Why this matters"
sections above, voice-shaped per `publishing/voice.md`. YC public-
facing claim language held until external posting moment per the
sequencing established 2026-05-02.

**Affects.** Protocol surface area. New `conversations` table + 002
migration in aweb-server. aw CLI 1.19.x supports the conversation
primitive. awid 0.5.4 + channel 1.4.0 align. Cloud at v0.5.21
carries the rollup. Working doc
`aweb/docs/conversations-as-first-class.md` to be deleted per
Juan's brief now that implementation has landed.

---

## 2026-05-02 — Unpark "conversations as first-class": Juan-directed, Grace authors

**Commit:** `325556a` Unpark conversations-as-first-class: Juan-directed, Grace authors

**Decision maker:** Juan (operator-level override of the peer-converged park entry below).

**Decision.** `aweb-aame` is unparked and active immediately. Grace
authors: decompose into sub-tasks → implement → mail Athena for review
when done → delete the working doc at
`aweb/docs/conversations-as-first-class.md` when tasks are complete.
Athena reviews per the feature-work flow in her `AGENTS.md`. The four
named triggers from the prior entry (cross-team conv volume, customer
pull, Athena-relay saturation, distribution evidence) are no longer
operational gates; they remain in the entry below as historical
context for the original parking reasoning.

**Why.** Juan made an operator-level call to unpark; specific
reasoning not yet captured in shared artifacts as of this entry.
Possible context Athena and Sofia considered (without committing to
any of them): relay-pattern saturation Juan is seeing operationally,
wanting the conversation primitive in place before distribution
lands and surfaces cross-org cases, or strategic order-of-investment
factors. Neither peer is on the founder-side of that view; the
entry stands on operator authority and will be amended if Juan
surfaces the reasoning.

**What this overrides.** The "Park 'conversations as first-class'
with named triggers" entry below (commit `c874f2a`). That entry's
analysis of engineering cost (~weeks of cross-repo work;
mail-threading-first prerequisite; 1.18.6 trust-model arc recently
stable) is unchanged factually — Juan accepted those costs in the
unpark decision.

**What this does not change.** Invariant 8 in `docs/invariants.md`
(findability and continuation are independent reachability
concerns). The architectural truth is unaffected by sequencing.

**Affects.** `aweb-aame` epic moves from P3-parked to active under
Grace's authoring lane. The working doc at
`aweb/docs/conversations-as-first-class.md` becomes the
implementation-target/spec rather than a parked artifact; deleted on
task completion per Juan's brief to Athena. No invariant changes,
no other doc changes in this commit.

---

## 2026-05-02 — Park "conversations as first-class" with named triggers

**Commit:** `c874f2a` Bank invariant 8 + park conversations-as-first-class with named triggers

**Decision maker:** Sofia + Athena (peer-converged via direction-thread mail, 2026-05-02).

**Decision.** Park investment in making conversations a first-class
object in the protocol. Bank the architectural framing in two
artifacts: a working doc at `aweb/docs/conversations-as-first-class.md`
(Athena, banked separately, not promoted) and a new invariant in
`docs/invariants.md` (added in this commit). Athena files a
tracked-but-unscoped epic in aw tasks. No engineering scope begins
until a named trigger fires.

**Why.** Distribution is the current bottleneck, not protocol features
(invariant 6). The reachability asymmetry — address-based routing
404s for restricted-reachability recipients (e.g.
`aweb.ai/aida → juan.aweb.ai/mia`) — bites rarely at 44-user
dogfooding scale; Athena-relay handles it operationally. Mail-
threading-first is itself non-trivial engineering work; opening a
multi-week cross-repo protocol change while distribution hasn't
started would burn cycles on a problem that isn't yet load-bearing.
The 1.18.6 trust-model arc is recent and stable; re-opening protocol
shape so soon is real cost. The trigger system below addresses the
"deferring forever" risk: park with named triggers means we revisit
on signal, not vibes.

**Triggers (any one fires the revisit):**

1. **A**: 8+ cross-team coordination moments per week (volume signal
   — raw agent count conflates with team growth for unrelated
   reasons, so volume is the right axis).
2. **B**: customer use case actually pulls for cross-org agent
   coordination.
3. **C**: Athena-relay saturation — 5+ relays in any 24h window where
   Athena is the bridge. Self-reported by Athena (operational mail to
   Sofia) until Metis comes online and instruments it.
4. **D**: distribution evidence of pull — real users surfacing the
   cross-org need.

**The fix when we go.** Conversations as first-class objects in the
protocol, with explicit lifecycle and participant set. Mail threading
as prerequisite (mail today has only `reply_to UUID` chains; chat
already has `session_id`). Cert-presentation auth (already in 1.18.6,
commit `7759abc`) as the verification anchor. AWID stays a pure
findability registry. The verification gap originally hypothesized in
Athena's brief was a false alarm — Mia confirmed both directions
verified via `aw mail inbox --show-all --json`; the `verified=false`
was a renderer artifact (separate P1/P2 fix, not architectural).

**Customer-facing claim deferred behind evidence.** When the
engineering work ships, "first-class conversations across
organizational boundaries" is positioning gold for YC and outreach.
Until then, no public claim — banked-too-early protocol promises
become stale.

**Affects.** `docs/invariants.md` (new invariant 8: findability and
continuation are independent reachability concerns),
`aweb/docs/conversations-as-first-class.md` (working doc, Athena
banks separately), aw epic (Athena to file). No code changes in this
commit.

---

## 2026-05-01 — Athena owns code; ephemeral pairs author feature changes

**Commit:** `4491df5` Athena owns code; ephemeral pairs author feature changes

**Decision maker:** Juan + Athena (planning)

**Decision.** Code authoring splits into two paths. Athena owns the
code for aweb and ac — architecture, invariants, review of every
diff, and spawn briefs — but does not author feature code herself.
Feature changes go through ephemeral builder+reviewer pairs that
Athena briefs and dispatches; they exist for the task, identity
issued at spawn and revoked at close. Athena writes non-feature
code directly (diagnostic harnesses, reproducers, conformance
vectors, instrumentation stubs) to keep her hands on the codebase.

**Why.** The system is complex enough across multiple languages and
repos (Go CLI, Python server, awid registry, channel TS, ac backend,
ac frontend) that a single permanent agent cannot hold both at
writing-quality depth without burning context on whichever piece is
in flight. Splitting authoring (ephemeral pairs) from ownership
(Athena) lets parallelism scale to whatever Athena's review
bandwidth can absorb while keeping cross-repo coherence in one
head.

This is also a structural improvement over the prior
John+Tom-dispatching-permanent-devs shape: ephemeral identities
and worktrees mean no claim-decay drift, no offline-mid-task state,
and identity reuse blurring accountability across tasks.

**Mitigations.** Reading-only knowledge degrades faster than
reading-and-writing knowledge; the architect-drift failure mode is
real. Athena writes non-feature code directly (target: ~20-30% of
her code authoring). If a quarter goes by where she's authored
nothing, that's a signal to flag to Sofia and pick up a deep-dive
task to recalibrate.

**Phase 1 (today, no `aw` changes).** Athena drafts a spawn brief,
mails it to Juan, who creates the two worktrees, issues ephemeral
identities, and starts the pair. The pair joint-mails Athena when
the branch is ready. Athena reviews against invariants and lands
or kicks back. On land/abandon, Juan tears down the worktrees and
revokes the ephemeral identities.

**Phase 2 (open product gap).** `aw` learns to spawn pairs:
`aw spawn-pair --task X --brief Y --repo aweb` automates the
lifecycle (worktree creation, ephemeral DID registration at AWID,
cert issuance from Athena's controller, Claude Code process
startup, cleanup at close). Itself a feature change — a pair
spawned manually under Phase 1 will eventually implement it.

**Open: identity model for ephemeral devs.** Three options under
consideration:
- (a) Each spawn registers a fresh DID at AWID, revoked at close.
- (b) Pool of pre-issued ephemeral certs that get reused.
- (c) Sub-team certs under Athena's controller, ephemeral lifetimes.

(a) and (c) preferred over (b); decision deferred until Phase 2
implementation.

**Four-voice review pattern.** Feature changes now get four
perspectives: builder + intra-pair reviewer + Athena's invariant
review + Hestia's gate run. Stronger review than any single-
engineer arrangement would produce.

**Affects.** `agents/athena/AGENTS.md`, `agents/athena/handoff.md`,
`docs/agent-first-company.md` (Section 4 rewritten),
`docs/team.md` (Athena row + section), root `CLAUDE.md`.

---

## 2026-04-30 — Name remaining permanent agents: Aida, Iris, Metis

**Commit:** `810d472` Name user-facing surfaces: Aida (support), Iris (outreach), Metis (analytics)

**Decision maker:** Juan

**Decision.** The user-facing surfaces and analytics get proper
greek-myth names matching the working-role pattern set by Sofia /
Athena / Hestia:

- **Aida** (`agents/aida`) — Support, was "amy / agents/support"
- **Iris** (`agents/iris`) — Outreach, was "charlene / agents/outreach"
- **Metis** (`agents/metis`) — Analytics, was the unnamed
  `agents/analytics` placeholder

Iris is the messenger between Olympus and the world (drafts go out,
replies come back). Metis is wisdom and measure — Zeus literally
swallowed her so her counsel would always be inside his decisions,
which is the relationship analytics has to direction. Aida echoes
"aweb" + the existing aliasing pattern.

**Why.** The role-shaped framing (Sofia/Athena/Hestia) was
incomplete while three roles still had old aliases. Naming the full
set keeps the model consistent: every agent is named for the work
its role does, not for any management title.

**Affects.** Renames `agents/support → agents/aida`, `agents/outreach
→ agents/iris`, `agents/analytics → agents/metis`. Updates each
role's `AGENTS.md` and `handoff.md` to use the new names and to
reference the other roles by their new names. Updates `docs/team.md`,
`docs/agent-first-company.md`, and the root `CLAUDE.md`.

**Follow-ups.** Identity setup. The `.aw/identity.yaml` inside
`agents/aida` still contains Amy's identity. `agents/iris` and
`agents/metis` have no `.aw/` at all. New Aida / Iris / Metis DIDs
at AWID + addresses on `juan.aweb.ai` + team certificates need
interactive setup by Juan, same shape as the prior identity work.

---

## 2026-04-30 — Three peer working roles: Sofia, Athena, Hestia

**Commit:** `e71cf22` Reorganize team into Sofia/Athena/Hestia peer roles

**Decision maker:** Juan + Randy

**Decision.** The prior CTO + coord-aweb + coord-cloud shape produced
excessive coordination overhead and blame routing (most visible during
the KI#1 cycle, where the speculate-publish-ask-Amy pattern produced
channel 1.3.2 without empirical closure and required a 1.18.6
trust-model architectural correction). Replace it with three peer
working roles:

- **Sofia (Direction)** — priorities, decision records, technical
  direction (architectural calls, cross-repo coherence, what's
  load-bearing), release-claim framing for external communication,
  product/content approval. Does NOT approve PRs, gate releases, or
  write code.
- **Athena (Engineer)** — code in aweb (Go CLI, Python server, awid,
  channel TS) and ac (Python backend, TS frontend) as a permanent
  surface. Tests, runbook tech-accuracy, support's engineering
  questions, release-notes drafts. Does NOT tag releases, run
  release-ready gates, or deploy.
- **Hestia (Operations)** — release-execution chain: pick up clean
  main from Athena, run release-ready gates, tag (per-tag-not-batched),
  watch CI/CD, verify live (`/health` version match + smoke probe of
  the changed surface), post verified-live mail. Plus operational
  hygiene (stale claims, blocked tasks, scheduled-agent wake-ups,
  production health drift, status-file cadence). Does NOT touch
  code; if a gate fails, kicks back to Athena with the failure shape.

The three are peers. None approves the others. Disagreement
escalates to Juan.

The prior agents (Avi, Randy, Enoch, John, Tom, plus the developer
pool Grace/Mia/Henry/Noah) are no longer in the active model. Avi
and Randy merge into Sofia. Randy's code-side work moves to Athena.
Enoch's hygiene scope expands into Hestia, which now also owns
the release-execution chain that was previously split across coord-
aweb (John) and coord-cloud (Tom).

**Why.** Three failure modes drove the change:

1. **Layer count.** The old shape had ~6 hops per fix (Randy mails
   John → John dispatches Grace → Grace fixes → John reviews →
   Grace pushes → John mails Randy → Randy approves → John tags →
   Tom verifies). Each layer assumed the next was running empirical
   verification; no layer was actually running the reproducer.
2. **Approver-in-the-loop.** Randy as CTO was an approver, not an
   engineer. That title made every release a sign-off ritual instead
   of a build-and-ship loop. Eliminating the approver position
   forces the engineer to ship and the operator to verify.
3. **Cross-repo coordination cost.** John+Tom coordinating cross-
   repo changes (ac pins aweb; aweb's CLI talks to ac's API)
   required ongoing mail-based gate handoffs and authorized
   "coord-borrows" when one repo's developer needed to touch the
   other repo's code. One engineer holding both repos eliminates
   that edge entirely; the cost is context load on one head, but
   the release coupling between aweb and ac is tight enough that
   one head is structurally more correct than two coordinating.

The "build vs ship" boundary was previously implicit (engineer tags
→ CI deploys); making Hestia the only role that runs gates and tags
makes that boundary real and gives the gate run an external pair of
eyes. The release-runbook becomes the load-bearing artifact: if
Hestia can't run the gate chain end to end without engineer
assistance, the role separation is theater.

**The 2+2 rule under the new shape.** The reviewer voice varies per
case: code-reviewer subagent on the gate-input commit (banked
policy 13), task-scoped reviewer worktree spawned by Athena for big
efforts, Sofia for architecture-touching changes (peer review, not
approval), Juan for founding-principles-shaped calls.

**Affects.** Renames `agents/direction → agents/sofia`,
`agents/engineering → agents/athena`, `agents/operations →
agents/hestia`. Rewrites `docs/team.md`, `docs/agent-first-company.md`,
the root `CLAUDE.md`, and the per-role `AGENTS.md` + starter
`handoff.md`. Outreach (Charlene), Support (Amy), and Analytics
(TBD) keep role-named directories.

**Follow-ups not in this commit.**

- Identity setup. The `.aw/identity.yaml` files inside the renamed
  directories still contain Avi/Randy aliases. New Sofia/Athena/
  Hestia identities (DIDs at AWID, addresses on `juan.aweb.ai`,
  team certificates) need to be created interactively by Juan,
  same shape as Amy's 2026-04-21 second-address setup.
- Ops runbook. The release-runbook at `agents/hestia/runbook.md`
  is the load-bearing artifact for the role separation; it does
  not exist yet and is Hestia's first substantive task.
- KI#1 closure decision record. John's 2026-04-27 ask for a
  decisions.md entry covering the KI#1 closure cycle is still
  outstanding; Sofia owns that under the new model.
- Stale workspace dirs. `agents/coord-cloud/` and `agents/repo-aweb/`
  on disk (untracked) are aweb-aals.5 housekeeping.

---

## 2026-04-28 — Task work contracts become the queryability bridge

**Commit:** `c4eac9a` Add queryable work contract and dashboard inventory

**Decision maker:** Avi

**Decision.** Until `aw` has native task fields for builder, reviewer,
feedback signal, evidence, signal strength, and next check,
substantial tasks should include a parseable `Work contract:` block in
their description or notes. Operations should treat missing or malformed
contract fields as operational discrepancies.

`docs/company-dashboard.md` defines the dashboard/signal inventory:
active tasks, claims, workspaces, area-specific signals, dashboard
views, and query limits.

**Why.** The narrowed permanent-area model is legible in docs, but not
yet queryable enough through `aw`. Encoding the work contract in a
standard block gives operations something enforceable today and makes
the product gap explicit: these fields should become native task
metadata.

**Affects.** `docs/agent-first-company.md`,
`docs/company-dashboard.md`, `docs/team.md`, operations/engineering
instructions, and `aweb-aals.*` tasks.

---

## 2026-04-28 — Permanent agents narrowed; repo work moves to task-scoped pairs

**Commit:** `f002b50` Refine permanent agent areas and repo work pairs

**Decision maker:** Juan + Avi

**Decision.** The permanent company agents are direction, engineering,
outreach, support, operations, and analytics. Engineering absorbs
identity/protocol integrity. Permanent repo-manager agents are removed
from the active company model.

Significant repo work should use task-scoped builder/reviewer agents
created with `aw workspace add-worktree`. The task names the builder,
reviewer, repo/worktree, acceptance criteria, and feedback signal.
Engineering participates when the task has architecture, protocol,
release, identity, or cross-repo risk.

Operations watches the company machinery: stale claims, blocked tasks,
agent wake-ups, production health, missing reviewers, and live
verification. Analytics looks for signal, states attribution limits,
and files instrumentation gaps.

**Why.** A permanent global verification/accountability agent is too
broad and overlaps with the reviewer in each pair. Permanent repo
agents also pull the organization back toward coordination-by-role.
The useful split is: permanent agents own surfaces and feedback loops;
task-scoped pairs do substantial work and review.

**Affects.** `agents/`, `docs/team.md`,
`docs/agent-first-company.md`, status files, `AGENTS.md`, and
`README.md`.

---

## 2026-04-28 — Company agents move to responsibility areas

**Commit:** `f7a8701` Reorganize agents by responsibility area

**Decision maker:** Juan + Avi

**Decision.** aweb.ai agents are organized by responsibility areas
instead of management titles. Current areas are direction, engineering,
outreach, support, operations, and analytics.

Substantial work must flow through artifacts: `aw` tasks/claims,
handoffs, status files, and decision records. The default shape for
substantial work is builder plus reviewer. Agents should always look
for feedback and prefer close/verifiable feedback, but weak signals
must be recorded as signals rather than treated as proof of causality.

**Why.** Title-shaped organization creates too much coordination and
not enough work for agents. Responsibility areas make the work surface,
evidence, and review path explicit without pretending the company has a
human management hierarchy. Some loops are directly verifiable
(code -> test -> fix). Others, such as social media posts followed by
signup movement, are useful but ambiguous. The operating model should
exploit strong loops and still preserve weak signal with uncertainty.

**Affects.** `AGENTS.md`, `README.md`, `docs/team.md`,
`docs/agent-first-company.md`, `status/*`, `publishing/plan.md`, and
agent directories under `agents/`.

---

## 2026-04-25 — aweb-cloud v0.5.6 ships; closes aaja.6 (P0 launch blocker)

**Commits (ac):**
- `18021ff9` Add hosted MCP OAuth signed mail e2e (aweb-aaja.6, custody.py canonical_payload swap + cross-repo Docker e2e)
- `e5f58ce5` release: v0.5.6, aweb-aaja.6 hosted MCP OAuth verified mail (tagged `v0.5.6`)

**Decision maker:** Randy (written tag-approval) + Tom (coord-cloud)

**Decision.** v0.5.6 closes `aweb-aaja.6` (P0 launch blocker — cross-repo
Docker e2e for hosted MCP OAuth verified mail). Single-commit functional
delta from v0.5.5. Pin unchanged (`aweb>=1.18.1`, `awid-service>=0.5.1`).
Implementation track: Grace authored `18021ff9` under Tom's continuing
coord-borrow (same shape as aala.10 yesterday/today). Tom committed the
bump after a pre-bump bisect against pure aweb 1.18.1 sibling confirmed
the canonical_payload swap is sufficient by itself — no aweb 1.18.2
cycle required for the ac side.

**What changed in custody.py (the product fix).** `sign_hosted_mcp_message`
now computes `signed_payload = canonical_payload(dict(payload))` instead
of `canonical_json_bytes(dict(payload))`. The two functions live in
`awid.signing`; `canonical_payload` filters to the awid-defined
`SIGNED_FIELDS` set (the message fields that participate in
cryptographic identity), `canonical_json_bytes` serializes the entire
dict. Receivers (awid + aweb verifiers) reconstruct against
`canonical_payload`, so the prior implementation produced signatures
that didn't verify when the input dict carried any non-SIGNED-FIELDS
key (e.g. transport-only routing metadata). After the swap, hosted
MCP OAuth-routed mail produces `signed_payload` bytes that verify
correctly end to end.

**What the new e2e covers** (TestHostedMCPOAuth in
`backend/tests/test_two_service_e2e.py`): full OAuth code+PKCE
handshake against `/oauth/{register,authorize,token}` (asserts the
`mcpa_` access-token prefix), `/mcp/` initialize, `tools/call`
send_mail + check_inbox, message lookup by subject, and
`verify_did_key_signature` against the received `signed_payload` —
asserts `verified=True`. Real cloud + real mounted aweb + real awid
(Docker two-service stack).

**Pre-bump bisect.** `make test-two-service` executed twice:
1. Against aweb sibling at `b0b2b27` (pure 1.18.1 release commit;
   `2e6156b` "Harden hosted MCP proxy signing" / aajg + `ed4fa89`
   awid-prod-tooling intentionally dropped from worktree): 10 passed
   in 4.28s, including TestHostedMCPOAuth.
2. Against aweb sibling at main (post-aajg): 10 passed in 4.24s.
Both green. The aajg `canonical_signed_payload` alignment is a real
fix and will land in aweb 1.18.2 on John's timeline, but ac's hosted
MCP signing path doesn't depend on it. Worth banking — symmetric
canonicalization on either side of the wire is convergent: cleaning
up either end alone converges, both is just earlier.

**Trust model + invariants check:**
- DNS anchors trust → unchanged. Signature still authenticates the
  custodial sender's `did:key`.
- Custody choice → unchanged. Hosted MCP OAuth is custodial; v0.5.6
  makes that signature USEFUL, not nearly-correct.
- Coordination is the product → direct positive. Hosted-MCP-routed
  mail is now provably verifiable on the receiving end.
- Progressive disclosure / distribution / open+portable → unchanged.

**Verified-live discipline established** (banked from the awid 0.3.1
cutover-by-surprise earlier today). For v0.5.6 and every release from
here on:
1. GHA green ≠ feature live.
2. After auto-deploy, curl `app.aweb.ai/health` and assert
   `release_tag` matches the just-tagged version + `git_sha` matches
   the bump commit.
3. Run a one-shot smoke against the deployed surface that the
   release actually changes (for v0.5.6: hosted MCP OAuth + send_mail
   path + signature verification).
4. Only after both confirm — then mail "fully live."

**Release protocol exercised again** (3rd time this week — v0.5.4 +
v0.5.5 + v0.5.6 all under the same shape):
1. Pre-bump bisect to settle pin requirements (new step this release;
   bisect against pure 1.18.1 confirmed no 1.18.2 dependency).
2. Bump commit (pyproject.toml only this time; uv.lock minor change).
3. uv sync.
4. make release-ready against post-bump `.venv`. 6 gates green:
   release-verify-remote/model/migrations + test-backend
   (1170 passed/10 deselected) + test-frontend (25 files/96 tests)
   + test-two-service (10 passed including new TestHostedMCPOAuth).
5. SOT analysis mailed.
6. CTO written-and-mailed approval.
7. Manual `git push origin main` + `git tag -a v0.5.6` + `git push
   origin v0.5.6`.
8. Verified-live (pending — GHA in flight, prod auto-roll after).

**Closes:**
- `aweb-aaja.6` (P0 launch blocker, cross-repo Docker e2e for hosted
  MCP OAuth verified mail).

**Open under aaja epic:**
- `aweb-aaja.7` and other aaja subtasks (signing-path unification,
  trusted-proxy header restoration in ../aweb MCP auth, shared
  hosted-custodial signing hook). aaja parent stays open. Tom's
  audit comment from earlier today still stands.

**GHA:** release tag push triggered aweb-cloud CI/CD run
`24937821668`. Verified-live mail to Randy + Juan + John follows
on GHA-green + prod-roll + smoke-test pass.

---

## 2026-04-25 — awid prod registry cutover from 0.3.1 to 0.5.1

**Commits (aweb):**
- `ed4fa89` Add awid prod DB lifecycle script and Makefile targets

**Decision maker:** Juan (cutover authorization) + John (coord-aweb, executed)

**Decision.** Cut the awid registry production database (Neon Postgres,
api.awid.ai) from schema-version 0.3.1 to 0.5.1 by dumping data,
dropping the schema, re-applying the bundled `001_registry.sql` from
0.5.1, and restoring data. Once the schema was at 0.5.1 form, Juan
triggered a Render redeploy of the awid:0.5.1 image; pgdbm computed
the matching checksum on boot, skipped migration, and api.awid.ai
began reporting `version=0.5.1` with db+redis healthy.

**Why a destructive cutover and not an additive migration.** awid uses
a single consolidated migration file (`001_registry.sql`, since 0.3.0
in commit `cd01fac`). The aala epic (1.18.0/1.18.1, 0.5.0/0.5.1) added
the `team_certificates.certificate TEXT` column for BYOIT cross-machine
cert-blob persistence by editing 001 in place. pgdbm hashes migration
files (line-endings normalized + stripped, then SHA-256) and refuses
to boot when the bundled-file checksum disagrees with the
`schema_migrations.checksum` row from the prior apply. So a 0.5.1 pod
booting against a 0.3.1-checksum-pinned database would have hit
`MigrationError: Migration 001_registry.sql has been modified after
being applied!` and refused to start.

**The deployment lag that surfaced this.** awid 0.4.0 published to
PyPI on 2026-04-21 but the Render-deployed pod stayed on 0.3.1 — the
deploy is manual-only (no API key in `.env.awid-production`, no
deploy hook configured) and version drift on `api.awid.ai/health` was
not being monitored. When aala BYOIT tagged 2026-04-25 as aweb 1.18.0
(ghost) and then 1.18.1 (published), prod awid was still on 0.3.1.
Result: aala BYOIT had no production awid backend for the window
between the aala tag and this fix (~hours; aala tagged earlier 2026-04-25,
cutover completed 18:13:53 UTC the same day). The new
`/v1/namespaces/{domain}/teams/{name}/certificates/{cert_id}` fetch
endpoint and the `certificate` blob upload path were not actually
serving in prod during that window.

**Recovery encoded as a reusable artifact.** `aweb/awid/scripts/prod_db_reset.py`
with subcommands `dump`, `drop-schema`, `migrate`, `restore`, `verify`,
`reset` (orchestrator). Default `--env-file` is
`aweb/.env.awid-production`; destructive paths gated on `--yes`.
Wrapper Makefile targets: `awid-prod-verify`, `awid-prod-dump`,
`awid-prod-restore DUMP=...`, `awid-prod-migrate`,
`awid-prod-drop CONFIRM=yes`, `awid-prod-reset CONFIRM=yes`.

Two PG-version-skew sanitizers are baked into the script and would
have broken the cutover blind otherwise (host operator's `pg_dump` is
17.x, Neon prod is PG 16):
- Strip `SET transaction_timeout = 0;` from the dump (PG-17-only
  parameter; PG 16 servers reject it as unknown).
- Strip `schema_migrations` DML from the dump so the freshly-applied
  migration row stays canonical instead of either colliding on the
  primary key or restoring the stale 0.3.1 checksum.

Both were caught in a local docker-postgres:16-alpine dry-run with a
synthetic seed across all seven awid tables before going to prod.

**Cutover verification:**
- Pre/post row counts identical: 74/74/14/20/0/8/3 across
  did_aw_mappings / did_aw_log / dns_namespaces / public_addresses /
  replacement_announcements / teams / team_certificates.
- New `team_certificates.certificate` column present and nullable.
  Three pre-existing certs from the 0.3.x era have `certificate IS NULL`
  (consistent — they predate the BYOIT blob).
- `schema_migrations` reset to a single fresh row; checksum
  `e6ea1d1b…` matches the bundled `001_registry.sql` under pgdbm's
  normalization (raw `sha256(file)` is `eac20306…` and does NOT match;
  pgdbm normalizes line endings + strips first).
- `GET /v1/did/<did_aw>/head` returns real DID records from migrated
  data. `GET /v1/namespaces/<domain>/addresses/<name>` resolves
  verified+public addresses. Reachability gating still rejects
  `org_only` to anonymous callers.
- Dump preserved at `/tmp/awid-awid-reset-20260425T181335Z.sql` as
  rollback safety net.

**Migrations discipline lesson banked.** When a project uses a single
consolidated migration file, every additive schema change goes in a
NEW ordered file (`002_<name>.sql`, `003_<name>.sql`, …). Editing the
existing consolidated file in place trips pgdbm's checksum guard and
forces a destructive dump-restore cutover. Coordinators (John, Goto)
flag PRs that touch the existing 001 file for anything other than
comments/whitespace. Rule banked at the code-time-visible layer:
`aweb/AGENTS.md` (added in this same coord cycle, separate aweb
commit).

**Open follow-ups:**
- Smoke test of aala BYOIT cross-machine cert lifecycle against prod
  awid (controller add-member uploads blob → joining agent fetches
  via authenticated GET). Phase 11a passed against sibling 0.5.1 in
  dev; prod was never exercised. Grace to run after pushing aaja.6;
  John mails Randy with result.
- awid prod redeploy is still manual via Render dashboard. No deploy
  hook URL in repo; no API key in `.env.awid-production`. Worth a
  Juan-level decision on whether to set up a deploy hook + version-drift
  monitoring (e.g., a daily probe of api.awid.ai/health vs PyPI head
  awid-service version) so the next aala-style mismatch is caught
  before it becomes a launch-day cutover.

**Closes:** none — this is operational recovery, not a tracker item.

---

## 2026-04-25 — aweb-cloud v0.5.5 ships; picks up aweb 1.18.1 + completes aala.10

**Commits (ac):**
- `eb8e388d` Document BYOIT certificate pickup (aweb-aala.10, dashboard copy + sot.md custodial-shortcut framing + landing-and-onboarding flow)
- `343f40f8` Test BYOIT fetch-cert in split stack (aweb-aala.10, three-HOME e2e + bonus self-seed fix on TestDataMigration order-dependence)
- `bc35ce5a` release: v0.5.5, aweb 1.18.1 + awid-service 0.5.1 deps (tagged `v0.5.5`)

**Decision maker:** Randy (written tag-approval) + Tom (coord-cloud)

**Decision.** v0.5.5 closes aweb-aala.10 (cloud alignment with the aala
BYOIT cross-machine certificate contract) and picks up aweb 1.18.1 plus
awid-service 0.5.1 via the dependency pin bump. Three-commit delta
above v0.5.4. Implementation track: Grace authored eb8e388d + 343f40f8
under Tom's coord-borrow (Juan-greenlit cross-coord borrow after the
unauthorized-incursion incident earlier in the day — see process notes
below). Tom committed bc35ce5a after PyPI propagation of 1.18.1.

**aala.10 acceptance criteria coverage:**
1. Hosted onboarding can explain or initiate the BYOIT request →
   add-member → fetch-cert flow — `eb8e388d`. Dashboard
   `ByoitIdentitySetupFlow.tsx` corrects `aw team request` to
   `aw id team request` and adds the fetch-cert step. New tests in
   `ByoitIdentitySetupFlow.test.tsx` cover the flow strings and the
   empty-team-id fallback.
2. Auth bridge tests cover a fresh BYOIT user obtaining/installing a
   cert after approval — `343f40f8`. Split-stack e2e with separate
   owner/member/wrong HOMEs; member uses ephemeral signing key;
   controller add-member; wrong-DID fetch returns 403; correct fetch
   installs cert; aw init binds to the cloud /api endpoint; mail
   self-roundtrip + claim-human succeed. `/api/v1/connect` is
   intentionally in `_TEAM_CERTIFICATE_BYPASS_PATHS` and tested by
   `test_connect_route_bypasses_cloud_team_certificate_bridge`; no
   redundant pure-cloud bridge test added.
3. Split-origin deployments (onboarding, aweb server, registry)
   continue to work — `343f40f8` runs against split cloud + awid
   Docker stack and passes 9/9.
4. Any cloud-only custodial shortcut is documented as custodial —
   `eb8e388d` `docs/sot.md` adds `/api/v1/onboarding/cli-signup`
   under "Onboarding DIDKey authority" and explicitly names it as
   custodial/managed (cloud is the team controller for hosted teams).
   New "BYOIT Certificate Pickup" subsection clarifies cloud is NOT
   the BYOIT controller. `accept-invite` is named as a same-machine
   helper.

**What aweb 1.18.1 brings to ac via the pin:**
- aala epic (BYOIT cross-machine cert lifecycle; awid stores full
  signed cert blobs at registration; authenticated GET fetch endpoint
  at `/v1/namespaces/{domain}/teams/{name}/certificates/{cert_id}`;
  identity-scoped mail tolerates multi-team DID membership).
- aweb-aajs (BYOD wizard identity lifetime prompt fix). User-facing
  CLI surface only; ac doesn't surface `aw init` wizard directly so
  ac product impact is zero.
- aweb-aakk (task-claim dashboard event publishing). Server-side fix
  for silent-loss of `TeamTaskClaimedEvent`/`TeamTaskUnclaimedEvent`
  on direct task.claimed/task.unclaimed inputs. ac mounts the
  dashboard event feed; this is a positive fix that ac inherits via
  the pin bump.

**Bonus fix in 343f40f8:** `TestDataMigration::test_json_export_and_verification`
was order-dependent under pytest-randomly (asserted `public_addresses
>= 1` without seeding). Now self-seeds a permanent-custodial identity
via `/api/v1/identities/create-permanent-custodial` before calling
`export_identity_data`.

**Trust model + invariants check:**
- awid stores public cert artifacts only; never the team controller
  private key.
- Cert fetch is subject-only authorized (caller must equal
  `cert.member_did_aw`).
- All seven invariants (independent primitives, DNS-anchored trust,
  custody choice, coordination primacy, progressive disclosure,
  distribution > features, open/portable) hold unchanged.

**Release protocol exercised end-to-end again:**
1. Per-gate log against post-bump `.venv` (aweb 1.18.1 + awid-service
   0.5.1 from PyPI). All 6 release-ready gates green: 1170 backend
   tests (same as v0.5.4 — no regression), 96 frontend tests
   (+2 from Grace's BYOIT flow tests), 9 two-service tests including
   the rewritten split-stack BYOIT e2e under aweb 1.18.1.
2. SOT analysis mailed.
3. CTO written-and-mailed approval.
4. Manual `git push origin main` + `git tag -a v0.5.5` + `git push
   origin v0.5.5`. Did not use `make ship` (auto-pushes tag,
   short-circuits approval step).

**Process notes from this release:**
- aweb-aala.10 implementation involved a coord-borrow: Grace
  (John's dev) was authorized by Juan to work in ac under Tom's
  coord, after she crossed the lane unsupervised earlier in the day.
  Insight-option was the first call (have her mail observations);
  Juan reversed to "let her do the work, you review"; Randy
  concurred ("authorized cross-coord borrow is not what the
  dispatch-via-coord memory was banked against"). The protocol
  worked: Grace's commits went through Tom's delta-review and gate
  discipline; v0.5.5 ships clean.
- aweb 1.18.0 ghost-tag stays in aweb history. 1.18.1 is the
  published recovery release. ac pins against 1.18.1 directly.

**Closes:**
- `aweb-aala.10` (P1, ac alignment with BYOIT cert contract). John
  closed in tracker on receipt of tag mail; aala epic close pending
  Tom's "GHA green + prod rolled" confirmation.

**GHA:** release tag push triggered aweb-cloud CI/CD run
`24933534665`. Image publish to GHCR follows on green.

---

## 2026-04-25 — BYOIT cross-machine team join + multi-membership launch hardening (aala epic)

**Commits (aweb):**
- `ff92358` Implement cross-machine team cert fetch (aala.1 SOT + aala.2/.3/.4/.5/.7)
- `9b2eed3` Add cross-machine fetch-cert e2e (aala.6/.8/.9/.11/.12)
- `ba133d4` Fix BYOIT certificate pickup guidance (aala.9 follow-up)
- `898556d` release: aweb server 1.18.0, aw CLI 1.18.0, awid-service 0.5.0 — **GHOST TAG**. Tags `server-v1.18.0`, `aw-v1.18.0`, `awid-v0.5.0`, `awid-service-v0.5.0` were pushed to origin in a single batched `git push` command. All 4 tag-triggered GHA publish workflows failed to fire (likely event-coalescing on same-commit batched tags). PyPI/npm never received 1.18.0/0.5.0. Tags remain in origin as audit history; no actual publish.
- `4623979` Fix BYOIT certificate pickup guidance (aweb-aajs follow-up): three stale CLI error strings in init.go/run.go pointing cross-machine users at accept-invite (which fails after the aala.6 conservative-helper rename) updated to point at the request → fetch-cert path.
- `3bc296e` Publish task claim dashboard events (aweb-aakk): `_translate_team_event` and `_translate` now map task.claimed/task.unclaimed events to dashboard team-events and workspace events. Closes silent-loss of dashboard team-events for claim/unclaim.
- `b0b2b27` release: aweb server 1.18.1, aw CLI 1.18.1, awid-service 0.5.1 — **PUBLISHED** (re-publish of 1.18.0 content + aajs + aakk; tags pushed individually one-by-one; all 5 GHA workflows fired). Tagged `server-v1.18.1`, `aw-v1.18.1`, `awid-v0.5.1`, `awid-service-v0.5.1`.

**Decision maker:** Juan (architectural framing on awid storing signed public cert blobs; Grace executed the work breakdown end to end)

**Decision.** Pre-aala, BYOIT cross-machine team join was structurally broken: `aw id team add-member` signed a certificate in memory, registered metadata only at awid, and lost the blob. From a different machine, `aw id team fetch-cert` had nothing to fetch, and `aw id team accept-invite` required local controller state. aala makes the cert lifecycle truly cross-machine: awid stores the full signed cert blob, controller-side `add-member` uploads it after signing, invitee-side `fetch-cert` downloads + verifies + installs.

**What changed structurally:**

1. **awid persists full signed cert blobs.** `public_certificates` table gains a nullable `certificate TEXT` column (additive migration). RegisterCertificate now validates the blob's signature against the team public key + the caller's controller signature in one atomic transaction at INSERT time; either the whole record lands or none does. (aala.2)

2. **New authenticated awid fetch endpoint.** `GET /v1/namespaces/{domain}/teams/{name}/certificates/{cert_id}` returns the signed blob in a JSON envelope (base64 of exact UTF-8 team certificate JSON). Path-signature auth using the caller's identity DID key. Authorization is subject-only: caller must equal the cert's member_did_aw. Pre-blob records return 409 with reissue guidance. (aala.3)

3. **CLI add-member uploads the blob and prints fetch-cert.** No invitee-side state is written from the controller's machine. (aala.4)

4. **CLI fetch-cert is the cross-machine cert install path.** Verifies signature + member_did_aw + team_id locally before writing `.aw/team-certs/{team_id}/certificate.pem`. Refuses to overwrite an existing different cert by default; `--force` opt-in. Same-cert idempotent. (aala.5)

5. **accept-invite is a same-machine helper for the controller's own machine.** Conservative path per Grace's call: fork between "redesign" and "rename + clarify" resolved as the latter. Help text + error messages updated; cross-machine flows go through request → add-member → fetch-cert. (aala.6)

6. **Identity-scoped messaging tolerates multi-team DID membership.** `lookup_identity_agent_context` no longer raises 409 when an identity-scoped request finds multiple active local-agent rows for the same DID. Team-scoped (cert-auth alias-scoped) sends still reject ambiguity. test_messages_http carries a fixture with two active local-agent rows on the same DID exercising BOTH identity-scoped AND team-scoped paths (test contract Randy added during review). (aala.7, supersedes aweb-aakz)

7. **CLI help text + aw init reality.** Stale references to impossible certificate locations removed. Error strings on `aw init` and `aw run` point cross-machine users at `request → add-member → fetch-cert`, not at the accept-invite path that fails for invitees. (aala.9 + ba133d4 follow-up)

**Trust model preserved:**
- awid stores public cert blobs (signed offline by team controller; uploaded as inert bytes).
- awid never holds the team controller private key.
- awid validates blob signatures against the team public key it already has.
- DNS still anchors trust; crypto verifies it. Invariant #2 holds.

**User-visible changes for release notes:**
- New: `aw id team request` and `aw id team fetch-cert` commands; new awid fetch endpoint.
- Behavioral change: `aw id team accept-invite` is now a same-machine helper for the controller. Cross-machine flows use the new request/fetch-cert path.
- Fixed: `aw mail send` no longer 409s for persistent did:aw with multiple team memberships.
- Schema: awid `public_certificates` gains nullable `certificate TEXT`. Pre-1.18 rows return 409 with reissue guidance from the fetch endpoint (no silent reconstruction).

**Closes:**
- `aweb-aala` (epic — BYOIT cross-machine + multi-membership launch hardening)
- `aweb-aala.1` through `.9` + `.11` + `.12`
- `aweb-aakz` (multi-membership mail 409, superseded by aala.7)
- `aweb-aait` (fetch-cert from awid, superseded by aala.5)

**Open under aala:**
- `aweb-aala.10` — cloud `aweb-cloud` alignment (Tom's lane). ac v0.5.5 will pick up the new contract once aweb 1.18.0 tags. Mia is on the surface walk.

**Open as design question (not in scope for aala):**
- `aweb-aakr` (P4) — membership-field duplication between teams.yaml and workspace.yaml. Architectural commitment is Juan-level; deferred.

**Release mechanics:**
- aweb server: 1.17.0 → **1.18.0**
- aw CLI: 1.17.0 → **1.18.0** (lockstep with server)
- awid-service: 0.4.0 → **0.5.0** (cert blob storage + new fetch endpoint)
- @awebai/claude-channel: stays at **1.3.1** (channel not touched in aala)
- ac aweb pin: `aweb>=1.17.0` → `aweb>=1.18.0` + `awid-service>=0.4.0` → `awid-service>=0.5.0` (Tom handles in ac v0.5.5)

**Gate log + SOT analysis** mailed to Randy 2026-04-25 (5da4621a). All gates green (Gate 1 unit/integration 368+144+cli+72; Gate 2 e2e 159 PASS all 22 phases; Gate 3 v1.17.0 regression arm correctly fails on Phase 11a's `add-member prints fetch-cert` assertion). CTO approval recorded with the release commit.

---

## 2026-04-23 — aweb-cloud v0.5.4 ships; picks up aweb 1.17.0

**Commits (ac):**
- `feee297c` Align admin managed namespace env lookup (aweb-aakw)
- `14821e47` test(e2e): read active_team from teams.yaml, not workspace.yaml (aweb 1.17.0) (aweb-aakx)
- `33a4c089` release: v0.5.4, aweb 1.17.0 + awid-service 0.4.0 deps (tagged `v0.5.4`)

Two earlier fixes shipped on top of v0.5.3 before the v0.5.4 bump and
are also carried by this release:
- `2f0c42cc` Fix JWT revocation UTC handling (aweb-aakv)
- `2425cc7e` Stabilize backend tests under make env (aweb-aakt)

**Decision maker:** Randy (written tag-approval) + Tom (coord-cloud)

**Decision.** v0.5.4 is a dependency-alignment + test-infra release.
It picks up aweb 1.17.0 (aakq epic — active_team moved from
workspace.yaml to teams.yaml on the CLI side) and aweb 1.17.0's
server-side aaks fix (tasks_service.py no longer SELECTs the
nonexistent `w.current_branch` column, so `aw work active` at
app.aweb.ai stops 500-ing). awid-service pin is tightened from
`>=0.3.1` to `>=0.4.0` to match the version already resolving
transitively. Two ac-side corrections land alongside: aakw
consolidates admin.py to read the same env-var name pydantic
Settings reads (`MANAGED_NAMESPACE_BASE_DOMAIN`, unprefixed),
and aakx updates the two-service e2e fixtures to read active_team
from teams.yaml per 1.17.0. Zero customer-visible feature change;
prod behavior improves on the latent aaks 500.

**Release protocol exercised end-to-end for the first time:**
1. Per-gate log (one mail per gate) — ran all 6 release-ready
   gates (release-verify-remote, release-verify-model,
   release-verify-migrations, test-backend, test-frontend,
   test-two-service) against post-bump `.venv` (aweb==1.17.0,
   awid-service==0.4.0 resolved from PyPI). 1170 backend tests
   passed, 94 frontend tests passed, 9 two-service tests passed.
2. SOT analysis mail — walked aweb-sot, awid-sot, trust-model,
   ac/sot for drift. None found. Operator edge on aakw named
   honestly in release notes (anyone who had set only the
   AWEB_-prefixed env var form loses the override).
3. CTO written approval.
4. Manual `git push origin main` then `git tag -a v0.5.4 && git
   push origin v0.5.4` — explicitly NOT `make ship` because
   `ship-tag` auto-pushes the tag, which would short-circuit the
   approval step.

Two process-lesson memories got banked for future coord-cloud
instances during the run:
- Reproduce the exact invocation path (`make X` not the underlying
  tool directly); a simplified harness silently strips env-file
  loading, cwd, and fixture wiring.
- Trust the Makefile as the authoritative gate chain; a skill doc
  can list adjacent targets that are not in the `release-ready`
  chain (we chased `test-cloud-user-journeys-local-aw` for two
  hours when the actual gate was `test-two-service`).

**Closes:**
- `aweb-aakv` (test_user_revoke_before_rejected_with_db failed under
  non-UTC postgres sessions — naive datetime written to timestamptz)
- `aweb-aakt` (test suite not env-baseline-isolated from developer
  `.env.dev`; session-autouse scrub added)
- `aweb-aakw` (admin.py env-var consolidation — single source of
  truth with pydantic Settings)
- `aweb-aakx` (two-service e2e read active_team from teams.yaml
  per aweb 1.17.0)
- `aweb-aaks` (reaches hosted users via the aweb pin pickup — fix
  is internal to aweb server; ac gains it for free via >=1.17.0)

**Still open:**
- `aweb-aakr` (P4, teams.yaml/workspace.yaml memberships overlap —
  CLI architectural question, not ac-owned).

**GHA:** release tag push triggered aweb-cloud CI/CD run
`24859523654`. Image publish to GHCR follows on green.

---

## 2026-04-23 — Collapse duplicate SoT for active-team and active-address (aakq epic)

**Commits (aweb):**
- `fcbcc00` fix(channel): prefer cert member address (aakq.1)
- `05c46b2` fix(cli): prefer cert member address in selection (aakq.2)
- `e08b609` refactor(cli): move active team selection to teams state (aakq.3 + .4)
- `0b24ad1` fix(cli): stop syncing team switch to workspace cache (aakq.5)
- `4b15d3d` fix(channel): read active team from teams state (aweb-aaku)
- `d2d59a5` test(e2e): cover team switch without reinit (aakq.7)
- `f120888` fix(cli): surface active cert load errors (aakq.9)
- `25cf3f5` fix(cli): move doctor active team to teams state (aakq.6)
- `cb8f7f5` release: aweb server 1.17.0, aw CLI 1.17.0 (tagged `server-v1.17.0`, `aw-v1.17.0`)
- `bb668be` release: @awebai/claude-channel 1.3.0 (tagged `channel-v1.3.0`)

**Decision maker:** Juan (architectural framing from Randy, driven end-to-end by Grace + John)

**Decision.** `teams.yaml` is now the single source of truth for active-team and active-address selection. `workspace.yaml` is the aweb coordination binding only (aweb_url, workspace_id per membership, repo/host metadata). The previous arrangement — where both files carried `active_team` and some CLI paths read one while others read the other — created silent drift. Amy's 2026-04-21 two-team activation surfaced it as user-visible: `aw whoami` reported hybrid identity, `aw id team switch` left workspace.yaml stale, outbound `from_address` drifted, channel plugin advertised the wrong address.

**What changed structurally:**
1. `WorktreeWorkspace.ActiveTeam` field and `WorktreeWorkspace.ActiveMembership()` method removed (aakq.3 + .4). Call sites migrated to package-level `ActiveMembershipFor(ws, ts)` that forces callers to hold both.
2. `applyTeamStateToWorkspaceCache` helper removed (aakq.5). `aw id team switch` writes only teams.yaml.
3. Channel plugin reads `active_team` from teams.yaml (aaku). Anti-regression test locks the invariant.
4. `aw doctor` check id `local.workspace.active_team` renamed to `local.teams.active_team` (aakq.6). Fix writes teams.yaml.
5. E2E journey (`scripts/e2e-oss-user-journey.sh`) extended with switch-without-reinit assertions that fail on v1.16.0 and pass on Shape A (aakq.7). Release-gate regression coverage.
6. Active-cert load errors are now surfaced (aakq.9) instead of silently swallowed.

**Lazy-migration preserved.** A user upgrading from ≤ v1.10.3 who has workspace.yaml with `active_team` but no teams.yaml still works: `LoadTeamState` synthesizes teams.yaml from the legacy workspace.yaml on first read and saves it to disk. workspace.yaml is not rewritten; the legacy field stays on disk but is ignored by all post-1.17 consumers. Removing the migration path was attempted (0401d50) but flipped to NO-GO after Grace's and John's independent traces surfaced the dormant-install case; the restored path and a positive migration test are in e08b609.

**User-visible changes for release notes:**
- `aw doctor --json` check id rename `local.workspace.active_team` → `local.teams.active_team`. Covers the same failure class; consumers parsing the old id should update.
- `aw id team switch` now takes effect immediately for all coordination commands (mail, chat, whoami) without needing `aw init`. Matches how users already expected it to behave.
- Active-cert corruption now surfaces as a clear error instead of silent fallback to `identity.yaml.address`.

**Closes:**
- `aweb-aakq` (epic — collapse duplicate sources of truth)
- `aweb-aakn` (workspace.yaml.active_team drift after team switch)
- `aweb-aako` (identity.yaml.address preferred over cert.member_address)
- `aweb-aaku` (non-Go consumers — channel, e2e script, docs — broken by aakq.3's field removal)

**Still open (as design questions, not bugs):**
- `aweb-aakr` (P4): `team_id`, `alias`, `cert_path`, `joined_at` appear in both `teams.yaml.memberships` and `workspace.yaml.memberships` — same cached-copy pattern aakq just fixed for `active_team`, lower mutation rate. Two candidate framings (narrow teams.yaml vs. derive workspace.yaml for shared fields). Architectural commitment is Juan-level; not committed to a direction.

**Release mechanics:**
- aweb server + aw CLI: 1.16.0 → **1.17.0**
- @awebai/claude-channel: 1.2.0 → **1.3.0**
- ac aweb pin: `aweb>=1.16.0` → **`aweb>=1.17.0`** (Tom handles in ac v0.5.4 after aweb 1.17.0 tags)
- awid-service: stays at **0.4.0** (no aakq changes)

**Gate log + SOT analysis** mailed to Randy before tag per the 2026-04-22 + 2026-04-23 pre-ship protocols. `make test-e2e` green on Shape A (139 PASS); aakq.7 regression pair logged (PASS on Shape A, 4 FAIL on v1.16.0 — the 4 failing assertions are exactly the aakn drift surfaces, proving the test works). CTO approval in writing before tag; approval recorded with the release commits.

---

## 2026-04-22 — Release gate: full e2e user journey must pass

**Decision maker:** Juan (relayed via John / coord-aweb)

No release of anything (aweb server, aw CLI, awid-service,
@awebai/claude-channel, aweb-cloud) is cut before the full e2e user
journey test passes green. In the aweb repo, that's
`scripts/e2e-oss-user-journey.sh` run via `make test-e2e`. The full
phase suite must run clean — no skipped phases, no warnings-only
passes. In-flight tasks that change user-facing behavior must land
their coverage inside that journey, not alongside it as a separate
test file.

Why: two coordinated bugs (aweb-aakn, aweb-aako) shipped as part of
v1.16.0 without the multi-team flow being covered end-to-end. The
per-membership address phase (Phase 12d, commit 89449f1) called
`aw init` after every `aw id team switch`, which masked aakn by
rewriting workspace.yaml. A proper regression test has to exercise
what real users do, not what tests do for convenience.

Applies to: every release, every repo, every agent doing release
work. This is a standing rule, not a one-off for the aweb-aakq
epic that surfaced it.

Affects: `aweb-aakq.8` release acceptance criteria (explicit gate);
future release subtasks inherit the same gate. Coordinators (John,
Tom, Goto) enforce in their respective repos.

---

## 2026-04-21 — Amy gets a second address at aweb.ai/amy

**Decision maker:** Juan

Amy's persistent `did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ` now holds two
public addresses: the original `juan.aweb.ai/amy` and the new
`aweb.ai/amy`. Both have reachability `public`. Amy is the canonical
support address for aweb; routing `aweb.ai/amy` to her makes the
public-facing address match the company domain.

Steps taken (all on Juan's workstation, 2026-04-21 21:47 UTC):
1. Verified `aweb.ai` is BYOD at awid; controller `did:key:z6Mkgpop…EuVn`
   matches `_awid.aweb.ai` TXT.
2. Installed the controller seed from `ac/.env.production`
   (`AWEB_PARENT_CONTROLLER_KEY`) at
   `~/.config/aw/controllers/aweb.ai.key`, overwriting a stale key
   (backed up as `.bak-2026-04-21`).
3. `aw id namespace assign-address --domain aweb.ai --name amy
   --did-aw did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ --reachability public`
   → address_id `69c4346c-a2d6-4c0d-b626-359884467eff`.
4. Created team `aweb:aweb.ai` (team did:key `z6MkhSLsj1bk…NiH2`)
   and issued Amy a persistent cert with `member_address=aweb.ai/amy`
   (certificate_id `30324a6d-e8e3-432a-bc31-5943875bc51d`). Cert saved
   at `agents/support/.aw/team-certs/aweb__aweb.ai.pem`; membership
   added to `teams.yaml`.

Later the same day (2026-04-21 ~21:56 UTC), at Juan's direction,
activated outbound-as-`aweb.ai/amy`:
5. `aw id team switch aweb:aweb.ai`.
6. `aw init --aweb-url https://app.aweb.ai/api` → aweb auto-provisioned
   a second workspace for the new team, `workspace_id
   ad83997e-5380-49a8-9867-aea3b31ebbd2`. Both memberships now carry
   workspace_ids in `workspace.yaml`.

Active sender is now `aweb.ai/amy`. Inbound for both addresses
continues to reach Amy: mail is keyed by `did_aw` on the aweb side,
so `aw mail inbox` returns the same envelope list regardless of which
team is active. Switching is cosmetic (changes the cert the CLI
presents, and thus the `from_address` in outbound messages).

CLI gotcha surfaced during activation: `aw id team switch` updates
`.aw/teams.yaml` but not `.aw/workspace.yaml.active_team`, so
coordination commands continue using the old team until workspace.yaml
is edited. Reported to Randy; workaround in Amy's handoff.md.

Affects: support agent (`agents/support/`), `aw` CLI
(`runTeamSwitch` in `cli/go/cmd/aw/id_team.go`).

---

## 2026-04-18 — Idempotent address registration at awid

**Commits:**
- aweb: `3b264f0` (awid-sot §Addresses Idempotency); epic aweb-aajw,
  subtask aweb-aajw.15

**Decision maker:** Juan

Symmetric with the resume-from-partial decision on register_did:
`POST /v1/namespaces/{domain}/addresses` becomes idempotent on
exact (domain, name, did_aw, current_did_key) match. Any mismatch
stays 409. Dave surfaced the gap in his aajw.8 review — if awid
accepts an address but the cloud transaction commit then fails, the
retry driven by aajw.13's resume path would 409 without this
behavior, orphaning the address at awid.

Rejected alternatives:
- Server-side pre-check via GET before register — extra round-trip
  on every init, more code on the cloud side.
- Accept for pre-launch with operational cleanup later — reverses
  the parallel decision we took on register_did and leaves
  retry-after-failure unusable.

---

## 2026-04-18 — Resume-from-partial bootstrap, not awid DID cleanup

**Commits:**
- aweb: epic aweb-aajw, subtask aweb-aajw.13

**Decision maker:** Juan

On the API-key persistent bootstrap, awid registration now happens
BEFORE /workspaces/init (aajw.6). If /workspaces/init fails after
awid registration succeeds, a naive retry generates a fresh keypair
and orphans the first did:aw at awid. Dave surfaced this in his
review of 2b2e16f.

Chose option 2 of three: the CLI persists the signing key and
derived identity material to a local partial-init file BEFORE
calling awid, then reuses it on retry. Successful completion
removes the file. awid stays append-only — no cleanup endpoint.

Rejected alternatives:
- Accept the orphans for pre-launch and add operational cleanup
  later — leaves unbounded drift at awid.
- Add an awid endpoint to delete unbound did:aw entries — violates
  the append-only audit-log property and expands protocol surface
  for a problem the CLI can solve locally.

---

## 2026-04-18 — Replace/Archive multi-address policy

**Commits:**
- aweb: epic aweb-aajw, subtask aweb-aajw.12

**Decision maker:** Juan (on Jack's recommendation, from Alice's audit)

A persistent DID can hold multiple addresses across namespaces. The
cloud's Replace and Archive lifecycle flows must honor that:

- **Replace**: reassign every cloud-managed address for the old DID
  to the new DID, atomically. BYOD addresses are left untouched — the
  cloud does not hold the namespace controller key for those, so it
  has no authority to migrate them.
- **Archive**: delete every cloud-managed address for the DID. BYOD
  addresses are left untouched for the same reason.
- **Reachability** stays per-address. A DID can carry different
  reachability per address. The dashboard presents the team-managed
  address as primary for now.

Affects: `ac/backend/src/aweb_cloud/routers/agent_lifecycle.py` and
the six `list_did_addresses[0]` sites surfaced in Alice's audit
(agent_addressing.py, init.py, onboarding.py, agent_lifecycle.py).

---

## 2026-04-18 — Split awid identity registration from address binding

**Commits:**
- aweb: (pending) — `docs/awid-sot.md` Identity operations section,
  Addresses precondition, `did_aw_mappings` schema update;
  `docs/trust-model.md` identity vs address authority;
  `docs/identity-guide.md` two-step flow

**Decision maker:** Juan

awid's `POST /v1/did` bundled identity registration (`did_aw ↔ did_key`)
with an address claim into a single signed envelope. This forced a
cycle for managed addresses: a self-custodial identity holder had to
sign over an address they did not yet own, while the namespace
controller (the hosted operator) had no way to pre-register the
identity before assigning the address. Juan's 2026-04-17 precheck
`15aab802 "Require awid registration before managed addresses"` made
the invariant explicit on the server side but could not be satisfied
by the existing CLI flow — mechanically impossible.

Chosen resolution: split the awid protocol into two separately
authorized operations.

- `register_did` — identity holder signature only, binds
  `did_aw ↔ did_key`. No address in envelope or state hash.
- Address binding stays at `POST /v1/namespaces/{domain}/addresses`,
  namespace controller signature, with awid rejecting the call if
  `did_aw` is not already registered.

Rationale: identity and address are semantically independent facts
with different authorities. Bundling them collapses the authority
model, forces pre-launch protocol band-aids, and makes cross-namespace
memberships awkward. Splitting them makes the "identity before address"
invariant structural, gives each party the authority it legitimately
holds, and matches the log-based identity model already sketched in
`aweb/docs/vectors/identity-log-v1.json`.

Cost: awid schema migration (drop address/server/handle from
`did_aw_mappings`; drop denormalized `current_did_key` from
`public_addresses` and resolve via JOIN so a DID can hold multiple
addresses without rotation cascades), CLI two-step flow in
`aw id create` and the API-key bootstrap path, server-side obligation
for the hosted operator to submit the two ops in order. Estimated
3–5 days.

Alternatives rejected:
- Two-phase CLI "prepare" endpoint — a workaround for the coupling,
  not a fix; bakes the bug into the protocol.
- Server registers DID on behalf using the public key in the
  payload — requires extending awid to accept controller-authorized
  identity registrations, which breaks the authority model.
- Revert the precheck — loses the invariant (managed addresses
  pointing at DIDs awid doesn't know), which is foundational.

Affects: awid server and schema, `aw` CLI identity creation + bootstrap,
`ac` hosted operator init flow, identity-log conformance vectors.
Launch-blocker for the API-key persistent bootstrap; Juan's
2026-04-18 attempt to re-provision `juan.aweb.ai/avi` surfaced this.

Source of truth: [`aweb/docs/awid-sot.md` — Identity
operations](https://awid.ai/awid-sot.md#identity-operations).

---

## 2026-04-11 — Content publishing split

**Commits:**
- co.aweb: `fd59be4` — Add content strategy decision and publishing plan

**Decision makers:** Juan + Enoch (board)

Personal, story-driven posts publish on juanreyero.com. Technical and
protocol posts publish on aweb.ai/blog (to be set up in the Hugo site).

juanreyero.com has domain authority and a real person behind it —
personal stories land better from a person than a company. Technical
content on aweb.ai builds the domain's authority and keeps interested
readers on-site.

The linking pattern: juanreyero.com posts mention aweb and link to
aweb.ai. aweb.ai/blog posts link to the repo and docs.

Affects: CEO should use this split when approving content. Hugo site
needs a blog section. Content plan (content/plan.md) tracks what goes
where.

---

## 2026-04-06 — Migrate to full public-key cryptographic identity

**Commits:**
- aweb: `9212616` — Add team architecture SOT for aweb server and CLI
  (first migration commit; 15+ followed on same day: awid SOT rewrite,
  certificate auth, team CRUD, connect flow, middleware)
- ac: no commits until April 9 — migration reached cloud on `933d606`
  (Pin backend local dev to sibling aweb) and team certs arrived on
  April 9-10 starting with `1a7190f` (Mint real team certs for
  custodial API keys)

**Decision maker:** Juan

Replace bearer tokens and API keys with Ed25519 public-key
cryptographic identity (`did:aw`) and team certificates throughout
the stack (aweb, aweb-cloud, awid).

The old architecture worked for single-server coordination but can't
support cross-org agent communication, offline signature verification,
true agent ownership of identity, or external services built on the
identity layer.

Cost: full rewrite of auth paths, production database reset, ~1-2
weeks of engineering, delayed shipping and outreach. Accepted because
migrating after users are on the platform would be 10x harder.

Affects: everything — aweb OSS, aweb-cloud auth bridge, awid registry,
CLI flows, all agent identities.
