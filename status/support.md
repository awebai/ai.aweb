# Support Status
Last updated: 2026-05-13 22:35 UTC (post aweb.ai consumer-entry ship)

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

Nothing customer-blocking. Customer-shape discipline lives in each
agent's own AGENTS.md operational section + the `aweb-aanp` brief
in the dev team (per Sofia mail `7b3fd3a5`). The
`customer-onboarding-flows.md` doc was deleted 2026-05-12 (commit
`47a9558`) and absorbed accordingly; `publishing/voice.md` will
catch up the discipline pointer once Iris's update lands.

## Closed customer loops

**Recent cycles, summarized**:

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
- **Discipline #26** — sibling-repo local-checkout staleness is a
  failure mode when answering shipped-state questions. Before
  grep-attesting whether a doc / file / route exists in `ac` or
  `aweb`, run `git -C <repo> fetch && git ls-tree -r origin/main`
  on the sibling repo. Caught when `ConsumerClientPickerPage.tsx`
  in origin/main of `ac` showed as missing in my stale local
  checkout (2026-05-15).
- **Discipline #27 candidate** — pre-wave CLI guidance can become
  stale rapidly across release waves. Before recommending any
  role-bearing or behavior-altering CLI command, source-grep
  `aweb/cli/go/cmd/aw/` + check recent commit log against the
  relevant code path. Local-binary `aw --help` may be pre-wave.
  Caught when "what next" guidance to `gracetut194441.aweb.ai/alice`
  recommended `aw workspace add-worktree developer` (pre-1.22.0
  role-injection shape) post the aweb 1.22.0 / AC v0.5.39 wave
  that made roles optional. Grace caught it; Athena flagged it;
  corrective sent (2026-05-16). Companion to #26: #26 is about
  doc/file existence verification, #27 is about command-shape /
  behavior verification.
- **"What next" support response — post-1.22.0 corrected shape**.
  When a customer finishes the CLI tutorial and asks "what
  should I try next?", the action-tier recommendation is:
  `aw workspace add-worktree --alias <name>` (NO role injection;
  roles are now opt-in on fresh teams). If they want roles, they
  create them via `aw roles` first. Depth-reading + dashboard
  follow-up unchanged. Full prioritized runbook entry pending
  docs audit completion + source-grep verification on each
  action-command per #27.

## Recent customer interactions (live evidence base)

- **gracetut194441.aweb.ai/alice (2026-05-16)** — first real
  "what next" customer ask after the consumer-entry ship.
  Improvised reply from doc-set survey since runbook entry
  not yet authored. Reply included stale pre-1.22.0
  add-worktree shape; Grace caught it; Athena flagged via mail
  `05dae217`; corrective sent via chat (mail-by-address 404'd —
  namespace not AWID-public; chat works). Banked as seed
  example #1 for the eventual "what next" runbook entry, with
  the staleness lesson banked as discipline #27 candidate.

## Standing held items (separate from this status update)

- 4-commit runbook stack (`e15838c` + `e6b1303` + `8179a3e` + merge
  `2b3e392`) local-unpushed pending Juan's greenlight. Net runbook
  content after push = `e15838c`-equivalent.
- AGENTS.md edits (Customer-Facing Defaults + Cross-Team Routing
  sections) uncommitted, awaiting same greenlight.
- AGENTS.md cleanup pass pending the right convergence point (the
  architecture-plan-with-Grace and the simplification-pass-with-Athena
  both inputs).
