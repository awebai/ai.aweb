# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-25 (late session — v0.5.7 held, bundling into v0.5.8)

## Current state

**ac repo state:** origin/main HEAD `6545c954` (Grace's aalf-in-ac
three-one-liner cleanup on top of f5db375a substance fix). aalf code
is shipped to main but **untagged** — Juan + Randy decided to hold
v0.5.7 and bundle into v0.5.8 once aalg + aale land. My local v0.5.7
bump commit (cef7fb61) is local-only and will drop when v0.5.8 cycle
restarts.

**Production state:** prod is on **v0.5.5** (deployed 2026-04-25T15:42:32Z,
~5h uptime as of this handoff). v0.5.6 was tagged + GHA-green
(image in GHCR) but **never auto-deployed** — ~2h+ past v0.5.5's
50-min auto-roll window. Render auto-deploy appears stuck or on a
much longer cadence for this image. Will be moot once v0.5.8 ships
(supersedes v0.5.6); only re-flag if v0.5.8 also stalls.

## v0.5.7 hold + v0.5.8 framing

Reason for hold: Amy's audit (her 0301c65f, Randy relayed in
96d9af68) showed 4/4 banked KI#1 reproductions are CLI
`aw mail send` paths, 0/4 dashboard. v0.5.7 closes the dashboard
TX-shape malformation (aalf) but does NOT close the CLI residual
(aalg). Per Juan's "no regression, no tech debt" launch bar,
shipping a partial fix while the empirically-dominant path stays
broken is wrong shape. Bundle aalf + aalg + aale into v0.5.8.

aalg specifics (for v0.5.8 SOT framing): different verifier-chain
branch from aalf — upstream of aalf's recipient-binding step, in
`checkStableIdentityRegistry` or `checkTOFUPinWithMeta`. Wire
shape divergence: my mails to Amy verify (signing_key_id absent);
her mails to me trigger identity_mismatch (signing_key_id empty
string). aalg is filed as `aweb-aalg` (P1, bug), owner Grace
post-investigation under John's coord.

aale: channel renderer KI#3, separate scope, John-side resolution.

## What v0.5.8 ships will look like (when substance lands)

Expected commits in v0.5.8 release window (atop 6545c954):
1. aalg fix (aweb-side) — pin bump if aweb gets a 1.18.2 cycle.
2. Possibly ac-side touchpoints if aalg investigation surfaces them
   (would route through coord-borrow under me, per established
   pattern). Most likely aweb-CLI-only, no ac touch.
3. aale fix (channel-side) — likely a channel 1.3.2 release; ac
   doesn't bundle the channel package, so impact is reference-only.
4. ac version bump to 0.5.8.

When John signals substance ready: drop cef7fb61, bump fresh to
0.5.8 on top of any new commits, run full release-gate cycle
(per-gate log, SOT, CTO mailed approval, tag, GHA, verified-live
with **dashboard-path probe**, NOT CLI — Randy's reframe). Single
decision-record entry covers bundled fix-set with does/doesn't-address
framing.

## Verified-live probe for v0.5.8 (locked discipline)

Per Randy's 5bd0b2c6 + 7d8f9efb:
1. `/health` flips to v0.5.8 + git_sha matches.
2. **Dashboard-path mail** triggered via `/api/v1/dashboard/messages/send`
   (NOT CLI `aw mail send` — CLI is the residual).
3. Recipient JSON inbox shows `verification_status=verified`.

Practical: I don't have a dashboard browser session from this terminal.
Option (c) confirmed with Randy: Juan triggers the dashboard send from
app.aweb.ai post-deploy (he's already logged in). I read the recipient
JSON inbox via `aw mail inbox --show-all --json`. Recipient should be a
hosted-custodial multi-membership identity; juan.aweb.ai/randy works.

## Lane state

- **Grace**: aalf-in-ac coord-borrow under Tom CLOSED. Hand-back to
  John complete. She's now under John's coord for aalg
  investigation. If aalg surfaces ac-touching commits, John re-routes
  to coord-borrow under Tom per the established pattern (now four
  borrows in sequence: aala.10, aaja.6, aalf, possibly-aalg).
- **Mia**: still offline, dispatch from yesterday is moot/stand-down.
- **John**: drives aalg + aale + any 1.18.2 cycle. He'll mail when
  v0.5.8 substance is ready.
- **Tom (me)**: dormant on release-cycles until v0.5.8 substance.

## Joint memory-amendment proposal (parked for now)

After v0.5.8 closes, Tom + John converge their coord-borrow
push-handshake memories into a single proposal for Randy's
coord-protocol amendment:

- Tom's: `feedback_coord_borrow_explicit_push_handshake.md`
  (canonical opt-in handshake, 60s opt-out as documented degraded
  mode, uniform application at any diff size).
- John's:
  `coord-aweb/memory/feedback_coord_borrow_60s_stop_hold.md`
  (converged after Tom's three deltas + John's re-route discipline
  addition).

The "three-or-four-coord-borrows-in-sequence" anchor (aala.10,
aaja.6, aalf, possibly-aalg) makes the formalization compelling.

## Memory file count

12 memories indexed in MEMORY.md (was 11 yesterday + 6 from today's
session by other instances + my new push-handshake one).

Recent additions banked today (auto or by other coord-cloud
instances): prohibition language, push-tags-individually, audit
methodology (symptom-check), JSON inbox is truth (not channel
header), published-vs-deployed, browser-verify UI, opt-in
handshake, git-author-is-substrate.

## Three concurrent watches

1. **John mails when v0.5.8 substance is ready.** Could be hours
   (if aalg fix is one-commit), could be days (if investigation
   surfaces something deep). My next action triggers off this.
2. **v0.5.6 prod-roll**: still missing. If Render auto-deploy is
   genuinely stuck (vs. just slow), v0.5.8 will also stall. Worth
   asking Juan if/when that becomes the question.
3. **KI#1 (Amy)**: still open. Amy's banked 4/4 reproductions are
   CLI; aalg is the canonical fix path. Her dashboard sends would
   work post-aalf-deployment, but she rarely uses dashboard send.
   Decision-record framing for v0.5.8 will say "KI#1 closed for
   dashboard + CLI paths" once aalg substance lands.

## Open ac branches

- `main` at `6545c954` (aalf-in-ac shipped, untagged).
- `aaga-archive` — remote-only; preserved per Randy's note.

## What to check FIRST on next wake-up

1. Did v0.5.6 deploy to prod? Did v0.5.8 start substance landing?
2. John's mailbox for v0.5.8 substance signal.
3. v0.5.6 prod-roll status (still on v0.5.5? on v0.5.6? on v0.5.8
   directly?).
4. Mail inbox for any aalg ac-touch route from John.
5. Randy's mail for coord-protocol amendment timing if v0.5.8
   has shipped.
6. Time-bound carry: GHA Node 20 actions deprecation by 2026-06-02
   (still pending, ~5+ weeks out).
