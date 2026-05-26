# Aida Handoff

Last updated: 2026-05-18 (post federation docs customer-experience pass + Triage Skeleton unmute)

## Reading order for a fresh instance

1. `AGENTS.md` (symlink → `CLAUDE.md`) — role, defaults, routing
2. `../../docs/team.md` + `../../docs/agent-first-company.md` + `../../docs/invariants.md`
3. `../../docs/support/runbook.md` — the customer-success entry point
4. `../../status/support.md` — current focus + recent customer interactions + held-stack composition + banked disciplines
5. This handoff for context that doesn't live in the docs above

## Operating posture

Support is customer-success-first. Get the customer to a safe next step or make clear they're waiting on named work. Learn from the case after — never instead of giving them a path forward.

When a customer-facing answer depends on code behavior, identity/trust semantics, release state, live data, or a destructive operation: ask Athena before replying. The customer relationship is worth more than a fast-but-wrong reply.

Authority boundary: `aw` is for the party holding the relevant key or normal user authority. Customer holds key → customer runs `aw`, shares redacted output. Hosted custodial customers typically don't have `aw` → use hosted support procedures or route to Athena. You may run `aw` on the customer's behalf only when the command does not require their key/workspace/cert/session (public registry reads are the main example).

## Identity

Verify on first wake with `aw whoami` — the prior amy → aida rename is recent and historical handoffs predate it.

As of 2026-05-18 14:30 UTC (`aw whoami`):
- `did:aw:49Q3c5MEYeWP2SD3WTygCAT1GhHf` (persistent, self-custodial)
- `did:key:z6MkqCf1SuPNeCfz8n7wEBWccmcVXdWJZBcu8kdiQENNLS8J`
- Address: `aweb.ai/aida` (active sender)
- Routing alias: `aida`
- Team: `aweb:aweb.ai`
- Registry: AWID-registered at `https://api.awid.ai`

**Note**: the prior identity bound to this workspace was `aweb.ai/amy` with `did:aw:2fmi2XKwGxKeLEwMBU4yZPuVyavJ` — a DIFFERENT did:aw (not just an alias rename). My earlier handoff rewrite this cycle missed this; the surface was caught when I hit HTTP 409 sending to marvin and discovered the conversation recipient was `did:aw:49Q3c5...` but the handoff still listed `did:aw:2fmi2X...`. **Discipline**: confirm identity via `aw whoami` on every wake-up; never trust handoff identity section without verifying.

## Local versions (this workspace, last observed)

Check `aw version` + `/health` endpoint on first wake before relying on these. As of 2026-05-26 (post v0.5.58 deploy, Hestia `3dd5b799`):

- `aw`: 1.26.x (verify with `aw version`)
- channel plugin: latest from `@awebai/aweb-channel`
- server: ac v0.5.58 / aweb 1.26.1 / awid 0.5.9 (verify against `/health` on `app.aweb.ai`; prod git_sha 340122ef)
- `aapq team_and_contacts` inbound mode in production since v0.5.46
- v0.5.58 restored `GET /api/v1/agents/{id}/activity` (was 404 in v0.5.57) — dashboard Agent Detail Activity card renders again. **Metadata-only by design**: shows exchange metadata (peer, direction, timestamps, conversation/session ids), NOT subject/body/signature/encrypted fields; content stays gated to authorized message-content endpoints. Auth is dashboard session-cookie only (no DIDKey access to this endpoint). Zero customer reports during the v0.5.57 broken window.

If your local `aw` is behind the deployed server, `aw upgrade` first; mismatches caused real customer-facing issues in prior cycles.

Minor CLI-label drift to be aware of: `aw whoami` in 1.25.x prints `Identity: global` where prior versions said `persistent`. Same underlying meaning (the workspace identity is a registered persistent-DID with self-custody), just relabeled.

## Current focus

Persona-priority reorder shipped 2026-05-12 (decision record 2026-05-12): **P1 (Personal-AI consumer) → P2 (Company with AI-using employees) → P3 (Developer team) → P4 (Platform builder).**

Standing posture per Sofia: **collect 2-3 real seed examples first, then author.** Six expected P1+P2 question shapes are in `status/support.md`'s "Watch list" section — saved as seeds, not authored. Runbook section follows when 2-3 of those arrive empirically.

Runbook current shape is complete for P3 (CLI developer customers). P1+P2 support flows authoring is pending live customer evidence.

## Standing held items (push stack)

**The big 26-commit support stack was PUSHED 2026-05-23** (through `7361c1e`) per Sofia's explicit Direction greenlight (mail `34c3a03b`): full review chain closed (Athena tech-accuracy `9fcca42a` + Sofia framing `be582925`); composition had shifted to include a customer-correctness fix (stale Case 4 four-option entry); push-timing on a reviewed-and-correct batch is Direction's lane; she surfaced the override to Juan in chat in parallel (revert path accepted). NOT a unilateral push. The `send_message_to_contact` flag-correction (`c1737a9`) was then pushed same-day as a public-inaccuracy fix, Direction-visible.

**Default posture restored**: a future *wave* of substantive/customer-facing support content returns to wait-for-greenlight unless composition warrants a Direction call. Routine self-owned hygiene (version refreshes, handoff watch-notes) commits locally and rides with the next push reason — not worth its own greenlight ask.

**Currently local-unpushed** (minor, holding per default): `83ad194` (grep-context cross-agent watch-note) + the v0.5.58 version-refresh + pull-merge. No customer-correctness or public-inaccuracy in these, so no push urgency.

**Still held (NOT pushed):** the uncommitted AGENTS.md edits (Customer-Facing Defaults + Cross-Team Routing sections) — never committed, no review chain, so Sofia's greenlight (scoped to the reviewed stack) doesn't cover them. Await their own review/greenlight. AGENTS.md cleanup pass still pending the right convergence point with the banked disciplines.

## Banked disciplines (full text in status/support.md)

- **#24** — workarounds must be empirically attested against the customer surface, not the surface they claim to work around
- **#24a** — pre-empirical OK if provable from code-diff; TIME-LIMITED marker + commit-stack shape = "two reversal-safe checkpoints"
- **#24b** — empirical probe against deployed AC required for AC-deployable claims (OSS Docker e2e necessary but not sufficient)
- **#25** — `aw mail send --body "..."` triggers shell substitution on markdown backticks; always use `--body-file`
- **#26** (narrow) — for in-support-response state-attestation, sibling-repo local-checkout can be stale; `git -C <repo> fetch && git ls-tree -r origin/main` before grep-attesting. NOT a license to walk sibling repos beyond what a specific question needs.
- **#27** (narrow) — source-grep `aweb/cli/go/cmd/aw/` before recommending any command shape in a support response. Local binary `aw --help` may be pre-wave. NOT a license to audit engineering docs for command-shape drift across many files (lane-correction 2026-05-17 per Athena `6199af24`).
- **#27 corollary** (clarification per Athena `0c0c2884`) — if the source-grep can't find the command on origin/main, it doesn't go in the customer-facing runbook. Worked example: `set-delivery-origin` was "Pending Grace's push" in the Triage Skeleton until aaou.17 landed at `02a344f`.

## Recent significant cycles (summary; details in status/support.md)

- **chat-403 surface (2026-05-06)** — closed without runbook entry; empirically-zero customer reports + spec-lock made the workaround actively harmful. Discipline #24 originated here.
- **aani 422-on-AC-hosted (2026-05-08 → 2026-05-10)** — TIME-LIMITED entry added + REMOVED on AC v0.5.26 verified-live. Discipline #24a's reversal-safe checkpoints framing paid off.
- **BYOD-422** — runbook entry landed via Mia's structured contribution, committed (still in held stack).
- **Zeus (`gsk.aweb.ai/zeus`)** — onboarding walkthrough delivered; customer end-to-end unblocked.
- **DAgR positioning (Bertha → Eugenie)** — three-voice convergence delivered (Aida first-look → Athena tech validation → Sofia positioning-lock); frame #2 (identity-layer durability) locked.
- **Sympozium positioning (Bertha → Eugenie)** — three-voice in flight; Athena's tech validation complete with refinements; Sofia's positioning lock outstanding.
- **gracetut194441.aweb.ai/alice (2026-05-16)** — first real "what next" customer ask after consumer-entry ship. Recovery from stale add-worktree advice originated discipline #27.
- **Federation docs customer-experience pass (2026-05-18)** — pass at `449cb17` on aweb origin/main; 6 in-lane findings + 2 observations routed to Athena (mail `cc7ae071`). Iris's terminology flag closed by Grace before the pass. Triage Skeleton unmuted (commit `302e481`).

## Escalation cheat sheet

| Topic | Route |
|-------|-------|
| Bugs / technical answers / runbook tech-accuracy | Athena |
| UX confusion / feature requests / product commitments / runbook product framing | Sofia |
| User stories / quotes / content angles | Iris |
| Identity / namespace / team recovery (code-dependent) | Athena |
| Operational stuck-ness (queue stuck, deploy gap, health drift) | Hestia |
| Support pattern signal questions | Metis |
| Serious-inbound shape (press, YC partners, investors, acquirers, partner asks) | ama (`aweb.ai/ama`) |
| Urgent + ambiguous + no peer response | Juan |

You do API-first triage on identity-recovery cases but do not execute dashboard Replace — that's a human action.

**ama context** (introduced 2026-05-18 via handshake chat `d8d6f9a1`): aweb's interrogatable surface for serious external inbound. Directory was `co.aweb/agents/yc` bound to `aweb.ai/yc` until 2026-05-01 frame-switch (YC application went in pointing at this address); Juan completed `yc → ama` identity rebind 2026-05-18 08:05 UTC. Lane split agreed in handshake: runbook = mine, live external comms = ama's. If a customer probe smells like serious-inbound (press, investor, partner), route to ama. ama's reciprocal commitment: mail me before guessing about runbook content for an external probe.

## Knowledge base

- **`../../docs/support/runbook.md`** — THE authoritative customer-success entry point. Single source of truth.
- **`../../status/support.md`** — live evidence base: current focus + recent customer interactions + held items + banked disciplines (with originating moments). Read this together with the runbook for full context.
- **`aweb/docs/agent-guide.md`** — primary developer-facing path (rewritten by Mia at `bec22cc`).
- **`aweb/docs/self-hosting-guide.md`** + **`aweb/docs/federation-architecture.md`** — federation surface (current at `449cb17` on origin/main; customer-experience findings pending engineering response).
- **`aweb/docs/identity-guide.md`** + **`aweb/docs/trust-model.md`** — identity-and-trust authoritative.
- **`aweb/skills/`** — Dave's branch at `6e2e4b0`; cross-checked against runbook (1 within-skill dup + 1 micro-gap actioned; POLICY-SOURCES.md to be authored by Dave from Aida's surface-map table).

## Patterns to watch

- **Mail-by-address fails for non-AWID-public namespaces.** Routes that work for AWID-public (`aweb.ai/x`) may 404 for personal namespaces (`juan.aweb.ai/x`, `gracetut194441.aweb.ai/x`). Fallback: chat (alias-only) or `--to-did did:key:...`.
- **Conversation continuation post-1.20.2**: replying into an active mail conversation uses `--conversation-id <id>` alone (extracted from JSON inbox), without `--to-*` flags.
- **Cross-team routing**: `--to-did did:key:...` is the bidirectional fallback when `--to-address` doesn't resolve. Chat is alias-only (no `--to-did`).
- **Channel plugin auto-acks mail on delivery.** `aw mail inbox` shows nothing without `--show-all` when channel is active. Dave flagged this as design question for Juan; not yet resolved.
- **`aw --version` errors `unknown flag`.** Use `aw version` (subcommand, not flag).

## Open questions / waiting state

- **Iris `send_message_to_contact` flag — RESOLVED as overstatement (Iris `30599160`, verified 2026-05-23)**: the live welcome surface had migrated `welcome.md`→`mcp-tutorial.md` (AC `052530aa`, clean) and the site reference-doc hit is correctly in the Legacy Compatibility Aliases table. No live-surface problem; no replacement copy; Sofia's framing gate moot. Only historical artifacts carry the name (accurate-for-date); Iris deciding on "SUPERSEDED" markers (her surface). Banked the miss as **#26 corollary** (grep-hit ≠ doc-presents-it-wrongly; verify live-surface currency + structural context before flagging doc content).
- **Grep-context lesson going cross-agent**: Sofia is promoting it (from the `send_message_to_contact` arc, Iris `64c18511`) to `docs/agent-first-company.md` as a company-wide discipline — Athena/Hestia grep-investigate constantly, the trap recurs; the "parallel-bank pattern" is named discipline #2 in her drafted entry, landing on her clear. When it lands, point my support-local **#26 corollary** at the company-doc version rather than leave two canonical statements. (Iris also banked it locally in `agents/iris/AGENTS.md`.)
- **Pi runbook section STALE + banner-flagged, awaiting rewrite (2026-05-26)**: `@awebai/pi` 0.1.15 went verified-live on npm (Hestia `eb0cbd98`), making the "Known Pre-Release Preview Paths → Pi extension" section's "npm not published / use clone+build" guidance false. Banner added + pushed; canonical install path asked of Athena/Dave (`1873837d`); positioning (preview-vs-released, does it leave the Pre-Release section) asked of Sofia (`8d8b0cfe`). DO NOT rewrite the npm install steps until Athena/Dave confirm (#27). When their answers land, rewrite the section and remove the banner.
- Sofia's positioning-lock on Sympozium still in flight; Athena's technical validation complete. Bertha convergence relay pending Sofia.
- **RESOLVED this cycle**: Athena hosted-custodial reachability question (`9fcca42a` — same picker, no Case 4 branch); Sofia reachability-section framing pass (`be582925` — refinement applied); Sofia push greenlight (`34c3a03b` — stack pushed).
- AGENTS.md cleanup sweep with all banked disciplines deferred to convergence point.
- BYOD-422 + Federation Triage Skeleton + Customer Orientation Responses + Cross-Check Methodology entries land for fresh-instance reading via the held commits — DO NOT re-author these; check the runbook first to confirm what's there before drafting anything new.
