# CTO Handoff
Last updated: 2026-04-25 (post-v0.5.5 verified-live; aalf RCA converged; awaiting Tom's lane-dispatch)

## State in one paragraph

Three releases since last handoff: aweb 1.18.1 (recovered ghost-tag 1.18.0), ac v0.5.5 (aala BYOIT cross-machine flow), ac v0.5.6 (mid-deploy at handoff time). awid prod cutover from 0.3.1 → 0.5.1 happened 2026-04-25 (John executed; required for aala to actually work in prod — discovered post-tag that artifact-published ≠ deployed-service-running). KI#1 (verification_status=identity_mismatch) RCA fully converged with John 2026-04-25 evening: TX-side malformed envelope in ac dashboard mail path; RX verifier downgrade is correct. Patch shape settled — caller+signer both, signer is load-bearing (mirror CLI signEnvelope auto-correct in ac's sign_on_behalf). Lane authorization pending from Tom; option (1) Grace continues in ac under Tom's coord is my preference and John's.

## What's live (verified end-to-end)

- `pypi.org/project/aweb` 1.18.1 — published, GHA green
- `pypi.org/project/awid-service` 0.5.1 — published AND deployed to api.awid.ai prod (post-cutover 2026-04-25)
- `npm @awebai/aw` 1.18.1 — published
- `npm @awebai/claude-channel` 1.3.1 — published
- `ghcr.io/awebai/ac-cloud:v0.5.5` — published AND deployed to app.aweb.ai (verified-live by Tom 2026-04-25 ~15:42Z, /health returns release_tag=v0.5.5, aweb 1.18.1, awid 0.5.1, all subsystems green)
- `ghcr.io/awebai/ac-cloud:v0.5.6` — published; auto-deploy pending at handoff time. Tom watching for /health flip + hosted-MCP-OAuth smoke.

## Active critical thread: aalf (KI#1 fix)

**RCA**: TX-side. ac/backend/src/aweb_cloud/routers/messages.py dashboard mail send path passes msg_to_did (= recipient's stable did:aw) into to_did and never populates to_stable_id. CLI signEnvelope auto-corrects this shape; ac's Python sign_on_behalf does not. Verifier at client.go:652 (checkRecipientBinding) correctly downgrades to IdentityMismatch because to_stable_id is empty AND toDID(did:aw) != c.did(did:key).

**Patch (settled with John)**:
1. Signer fix in sign_on_behalf — mirror signEnvelope: if to_did starts with "did:aw:", move to to_stable_id and clear to_did. Load-bearing — makes ac protocol-consistent with CLI signer.
2. Caller fix in messages.py — explicit split in dict literal. Defense in depth.
3. Audit: grep all sign_on_behalf callers; expectation is zero intentional did:aw-in-to_did callers (all malformed per contract).

**Regression test (John relaying to Grace)**: four-case matrix — Tom/John/Grace/Amy senders to Amy receiver. Pre-fix: Amy fails IdentityMismatch, others pass. Post-fix: all four pass. Question still open: why does Tom/John/Grace currently pass on the same TX path? Hypotheses (a) registry resolution short-circuits earlier in chain, (b) prior TOFU pin verified-state cached. Grace's regression should isolate.

**Empty signing_key_id** (Grace's cosmetic flag): non-causal, file as separate post-launch cleanup task.

**Lane-dispatch (Tom's call)**: my preference is option (1) — Grace continues in ac under Tom's coord (aaja.6 shape). John concurs. Tom not yet replied on authorization. Mail to Tom: d0c4040e-3340-4bb8-8111-5ef1b9c367d4.

**Release-gate framing for v0.5.7** (or whatever ships the fix): same v0.5.6-shape gate-log + SOT analysis + CTO mailed-approval + verified-live discipline. Plus browser-verify pathway for any UI-surface changes (Tom's discipline-gap flag — see below).

## Discipline gap to bank: browser-verify for UI-surface changes

Tom flagged it on v0.5.5: dashboard UI changes pass /health curl probe (release_tag matches, subsystems green) but the actual user-visible delta is browser-verified-only. /health does not exercise dashboard rendering. The published-vs-deployed memory needs a corollary: for releases whose surface is dashboard UI text or layout, /health is necessary but not sufficient — add a browser-test probe (or at minimum a screenshot-diff during release-gate). Will add to a memory entry.

## Open items (mine, not delegated)

- **Bank Tom's browser-verify discipline-gap memory** (this session, before going idle).
- **Decision record entry for aweb 1.18.1 + ac v0.5.5 + awid 0.5.1 prod cutover** — converging with John on the entry text. He has the migration-discipline lessons; I have the release-framing.
- **Mirror release-framing pointer to coord-cloud + coord-awid AGENTS.md** — already in coord-aweb. Per John's recommendation 2026-04-25.
- **Stand by for Tom's v0.5.6 fully-live mail** — auto-deploy + hosted-MCP-OAuth smoke.
- **Stand by for Tom's aalf lane-dispatch decision** — caller+signer both, audit requirement, my preference is option (1).

## Filed and tracked, not actively my work

- **aweb-aakr** (P4) — membership-field overlap. Deferred by agreement.
- **aweb-aaky** (P3) — ac Makefile realpath refactor. Not urgent.
- **aweb-aals epic + aaiy + various P1/P2** — John's audit backlog. Stage-gate on ship priorities.
- **aaiu.5** (hosted onboarding e2e) — real-still-open.
- **aaja.7** (signing-path unification) — real-still-open. The aalf signer-fix in sign_on_behalf is a small overlap with this; coordinate at landing.
- **aweb-aale** (P3) — channel plugin 1.1.0 mail-event header verified=false render bug. Display-only, not a verification bug. Not a ship-blocker.
- **aakz** (mail-send 409) — closed. chat-fallback workaround documented.

## Release-gate discipline — standing policy (verified across 4 ships)

Six rules now codified in memory + docs:
1. Release gate = full e2e user journey green (decisions.md 2026-04-22).
2. Review via shared working tree, no chat-pasted diffs.
3. Route dev-agent dispatch through the coordinator.
4. Trust the Makefile's release-ready chain — not parallel skill-docs.
5. Written approval via mail — "GO" in user conversation ≠ GO in coordinator inbox.
6. Published artifact ≠ deployed service. Verified-live = artifact + /health + smoke against deployed endpoint. (NEW 2026-04-25, banked from awid prod 0.3.1-vs-0.5.1 lag discovery.)
7. (pending: browser-verify pathway for UI-surface changes — will bank from Tom's flag.)

## What to check FIRST on next wake-up

1. Tom's lane-dispatch reply on aalf — option (1) authorized? Grace cleared to patch?
2. Tom's v0.5.6 fully-live mail landed?
3. Grace's regression test design + why-only-Amy investigation findings?
4. Amy's status — has she seen any new identity_mismatch on a fresh TX-path mail post-deploy? Pre-fix, expect she still does.
5. John's converging decision-record entry for 1.18.1 + 0.5.5 + awid 0.5.1.

## Context I don't want to lose

- The aala "shipped end-to-end" framing was wrong on 2026-04-25 because awid prod was on 0.3.1 while the BYOIT epic depended on 0.5.1. Tagged 14:52Z; discovered ~24h later when Amy hit identity_mismatch on a related path. John executed dump-restore lifecycle to bring prod up. Lesson banked as feedback_published_vs_deployed.md.
- Channel header verified=false (Amy's first symptom report) is a render, not crypto truth. JSON inbox is canonical. Banked as feedback_json_inbox_is_truth.md. Cost ~30 min of wrong framing before Amy went to canonical.
- KI#1 root cause was buried 1+ release cycle deep. Verifier was correctly downgrading malformed envelopes; the malformed envelopes were being produced by ac's Python signer not mirroring the CLI's auto-correct. Easy to misread as "verifier broken" when it was "signer doesn't match contract." The contract is at client.go:56-61 — to_did is reserved for did:key, to_stable_id for did:aw.
- John's independent verification of Grace's RCA caught and confirmed the determination cleanly (he read the contract, the verifier chain, and the TX source). Coordinator-layer review continuing to earn its keep.
