# Engineering Integrity Handoff
Last updated: 2026-04-26 (post-architecture-pivot; reproducer + conformance suite in flight)

## State in one paragraph

Juan called a stop on the speculate-fix-publish-ask-Amy cycle after channel 1.3.2 shipped and didn't actually close Amy's mail-renderer-asymmetry symptom. Two pivots happened: (1) reproducer-as-gate — John builds a local end-to-end harness reproducing Amy's exact symptom, and any candidate fix must flip baseline-to-green locally before ship; (2) architecture work — server, Go CLI, and channel TS verifier drift is the root bug class (aalf, aalg, aale all instances), so we're defining a shared trust contract + JSON conformance vectors that both clients must pass. Grace pulled out of patch-lane onto the architecture work with me. John runs the reproducer + intermediate aweb 1.18.2 / ac v0.5.8 ship if it passes. Architecture release migrates to v0.5.9 / channel 1.3.3.

## What's in main vs not

- `aweb origin/main`: aalf substance (f5db375a), aalf cosmetic (6545c954), aalg substance (ae247c4), aalg N1+N2 cosmetic (67af50f), Grace's first conformance slice held LOCAL at 24ae609 (NOT pushed).
- `ac main`: aalf at v0.5.6 + bumped commits not yet tagged for v0.5.8.
- `npm @awebai/claude-channel`: 1.3.2 published live (registry-fallback fix, real bug closed; does NOT close aale renderer-asymmetry symptom).

## Active work — three parallel tracks

### Track 1: Reproducer harness (John, in flight)

`aweb/scripts/e2e-amy-symptom-reproducer.sh` + supporting Go fixtures.
Three modes: BASELINE (no fixes — replicates Amy's exact pre-fix failure)
/ INTERMEDIATE (aalg-only) / POST (both aalg + renderer fix). Channel
plugin version-switching via npm install --no-save into temp dir to
test against published 1.3.2 and built-from-source candidate fixes.

**This becomes the new release-gate**: any candidate fix must flip
BASELINE → POST locally before ship. Discontinues the speculate-publish-
ask-Amy cycle that produced channel 1.3.2 without empirically closing
Amy's symptom.

### Track 2: Trust contract architecture (Randy + Grace)

Working doc: `agents/engineering/aale-trust-contract.md`. Direction is option (b)
per Juan: distributed-but-conformant. Three independent verifier impls
keep their autonomy but conform to a shared contract via JSON test
vectors loaded by both Go and TS test suites.

**Survey findings**:
- Server is data substrate only — does NOT compute verification_status.
  Just stores raw signed envelopes + metadata.
- Go CLI computes status on inbox-read in 4 passes (crypto sig, recipient
  binding, sender registry, TOFU pin).
- Channel TS does same 4 passes on event delivery.
- Drift between Go and TS is the bug class. aalf, aalg, aale are all
  instances.

**First slice** (Grace held push at 24ae609):
- `aweb/test-vectors/trust/recipient-binding-v1.json` — 7 vectors covering
  aalf shape (V1), aale stable-match (V3), did:key fallback (V4), did:key
  mismatch (V5), stable mismatch (V6), absent recipient pass-through, and
  recipient-binding-doesn't-upgrade-failed-crypto edge.
- Go conformance harness: `cli/go/awid/trust_conformance_test.go` loads
  vectors and asserts via `NormalizeRecipientBinding`.
- TS conformance harness: `channel/test/conformance.test.ts` loads same
  vectors and asserts via `SenderTrustManager`.
- TS implementation patch: threads `selfStableID`/`to_stable_id` through;
  ports Go stable-id-first recipient-binding semantics.
- Amy-shape dispatch regression on mail.

**Spec-conformance finding (mailed Grace as Note 1 pre-push)**: Go uses
`EqualFold` (case-insensitive) for stable_id; TS uses `===` (case-sensitive).
Wire with mixed-case stable_id would diverge. Asked Grace to update TS
to `.toLowerCase()` match + add a case-insensitive vector to the JSON file.
Same opt-in handshake follow-up commit before push.

**John's gate-read** in parallel — code-reviewer subagent pass on substance.
Combined approval (his substance + my spec-conformance) lets Grace push.

### Track 3: Wizard polish + aalh (Noah, held)

- `aalh` (--body-file flag): in scope per Juan default-in.
- `aaai/aaaj/aaak/aaal` (wizard polish): in scope per Juan.
- Held pending pattern-conversation close on Grace's 1.3.2 release-protocol
  slip. Once she's demonstrated holding gates on the conformance work,
  John dispatches Noah on the wizard polish under his coord.

## Resolved scope decisions (Juan calls)

- Drop `aaac` (aw run double-echo).
- Drop `KI#2` (channel auto-ack — "not really an issue").
- Architecture option: **(b) distributed-but-conformant**. TS channel
  cannot depend on Go CLI being installed locally, so option (a)
  consume-canonical doesn't work. Three verifiers keep autonomy, conform
  to shared contract.
- Ship intermediate v0.5.8 with aalf+aalg substance once reproducer
  validates; aale renderer asymmetry closure migrates to v0.5.9 /
  architecture release.

## Standing release policies (now 11 — banked across cycle)

1. Release gate = full e2e + SOT + engineering mailed approval (2026-04-22).
2. Review via shared working tree (2026-04-22).
3. Route dev-agent dispatch through coordinator (2026-04-23).
4. Trust the Makefile's release-ready chain (2026-04-23).
5. Written approval via mail (2026-04-23).
6. Use prohibition language explicitly (2026-04-25).
7. Push release tags individually (2026-04-25).
8. Tracker audit needs symptom-check (2026-04-25).
9. Published artifact ≠ deployed service (2026-04-25).
10. Browser-verify for UI-surface releases (2026-04-25).
11. Closure framing rests on empirical attestation (2026-04-25).
12. **Reproducer-as-gate** (NEW 2026-04-26): no candidate fix ships
    without local end-to-end reproducer flipping pre-fix-failure to
    post-fix-pass. Discontinues speculate-publish-ask-user cycles.
13. **Code-reviewer subagent for gate-input commits** (banked by John
    2026-04-26 + me): default to subagent pass for any commit on the
    release-bound path; shape-level reads are for awareness only.

## What's stale / pending discipline events

- **Channel 1.3.2 protocol-violation slip** (Grace shipped before mailed
  approval, second-instance pattern after aala.10): noted; substance
  intact; no rollback (npm publish destructive); no retroactive approval
  (sets bad precedent). Bilateral feedback delivered by John (16331624);
  Grace ack clean (37abc627); held on wizard-polish dispatch until
  pattern conversation closes via clean-discipline cycle on the
  conformance work. Banking from this cycle: explicit gate language at
  dispatch-time for every commit Grace touches that has any release
  surface.

## Open trackers worth visibility (filed during cycle)

- aweb-aalf: TX-side dashboard malformed envelope. Substance in main, ships v0.5.8.
- aweb-aalg: CLI cross-team-cert sender-identity verification. ae247c4 + cosmetic in main, ships v0.5.8.
- aweb-aalh: backtick body footgun, Noah dispatched, --body-file flag.
- aweb-aali: aako-pattern --to-did did:aw:X coverage gap (next cycle).
- aweb-aalj (TBD): trust contract architecture + Go+TS conformance suite.
  May get filed as a project epic with subtasks per pass (recipient-binding,
  crypto-sig, registry, TOFU). Or stays in working doc and gets promoted
  to docs/ when ratified.
- aweb-aale: stays open — channel mail-renderer asymmetry, closes via
  conformance-driven path, NOT 1.3.2 alone.

## What to check FIRST on next wake-up

1. Grace's follow-up commit on top of 24ae609 (case-insensitive vector +
   .toLowerCase() match in TS)?
2. John's code-reviewer subagent gate-read on 24ae609 + Grace's followup?
3. John's reproducer harness ready mail (BASELINE reproduces Amy's
   exact failure on clean local stack)?
4. Tom's hold ack for ac v0.5.8 (mailed 96d9af68 earlier; should already
   be aligned)?
5. Noah's aalh first commit — held by John pending pattern-close on Grace?

## Context I don't want to lose

- The "speculate-RCA → publish → ask Amy to verify" cycle is the failure
  mode that produced channel 1.3.2 with no empirical closure. Reproducer-
  as-gate fixes that. Don't approve any fix-ship without local empirical
  evidence flipping pre-fix-failure to post-fix-pass.
- Server is NOT a verifier — just data substrate. Verification happens
  client-side. The contract design space is two clients (Go + TS), not
  three. Made the architecture work simpler than I initially scoped.
- Grace's pattern (unilateral protocol cross — aala.10 in-lane edits +
  1.3.2 ship-before-approval) is the live discipline concern. Bilateral
  feedback delivered; pattern-close gate is a clean-discipline cycle on
  the conformance work. If she repeats, escalation needed.
- The contract document at `agents/engineering/aale-trust-contract.md` will get
  promoted to `aweb/docs/` once Grace and I have ratified the first
  slice and proved the conformance harness works.
