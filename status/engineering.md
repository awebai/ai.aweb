# Engineering Status
Last updated: 2026-05-01 11:30 CEST

## Current focus

1. **Cloud is at v0.5.12, healthy.** `app.aweb.ai/health` reports
   `release_tag=v0.5.12`, `aweb_version=1.18.6`, `git_sha=962dd163`,
   started 2026-04-30 20:07 UTC. AWID at `version=0.5.2`, healthy.
   v0.5.11 and v0.5.12 shipped 2026-04-30 outside the Hestia gate
   chain — accept retroactively, the discipline applies going
   forward.
2. **Five commits past v0.5.12 on ac main, candidate v0.5.13.**
   Coherent admin-tooling-hardening + auth retired-user safety +
   ship-gate improvement bundle. Holding the signal for Hestia's
   gate chain rather than racing a release.
3. **Engineering posture continues release-discipline + invariant
   correctness, not feature expansion.** Distribution is the
   bottleneck; engineering side is green.
4. **Athena dispatch shape is being revised.** The spawn-pair
   framing in AGENTS.md and commit `4491df5` was a published
   speculation; Juan has indicated the actual dev team is in a
   separate cryptographic team and will walk through the real
   setup. Holding the published flow until that lands.

## Candidate v0.5.13 on ac main (5 commits past v0.5.12)

Read of each commit:

- `962dd163` — ship-gate: include cloud user journey e2e in
  release-ready. Makefile-only. Closes the gap that let v0.5.10/.11
  ship without the full e2e being re-validated as part of the
  release sequence. ~25 min added to `make ship` (two e2e runs:
  local-aw + installed-aw). Net win.
- `cf49c282` — Default admin actor to aw workspace identity.
  `backend/admin.py` + tests. Removes the manual --actor friction
  for admin operations.
- `0e0f73a6` — Preserve cross-org communication on hard delete.
  `backend/admin.py` (+205) + tests (+205). Substantive admin-side
  invariant: hard-deleting a user in one org must not break
  signed-message history other orgs received from them. Heavily
  tested.
- `37762328` — Harden cross-scope hard-delete communication
  cleanup. Follow-on to 0e0f73a6.
- `5818095d` — Ignore retired users in auth reuse checks. Auth
  router + auth_password service + oauth service + 3 test files
  (+405 lines). Consistent `deleted_at IS NULL` filter on every
  user lookup in the auth path: username/email availability,
  cli_register, login, refresh_token, verify_email_complete,
  password set/reset/login, signup. Plus error handling for both
  legacy `users_username_key` and newer partial-unique
  `idx_users_username` / `idx_users_email` constraints. Architecturally
  clean — single concept consistently applied.

Cluster needs a code-reviewer-subagent pass before signal to
Hestia (standing policy 13). Will run that as part of the
v0.5.13 prep when the release window opens.

## Active engineering work

`aw work active` shows zero rows (the 5 rows from the 04-30
transition handoff are no longer active). No claimed work in
flight on either repo.

## YC technical positioning fact-check (2026-05-01 morning)

YC agent (first wake-up, separate team) asked for verification of
five technical-novelty claims before rewriting AGENTS.md +
positioning docs. Grounded each in code:

- Locks: corrected YC's "repo-scoped" framing — locks are
  team-scoped TTL'd reservations on opaque resource keys; "file
  paths as keys" is convention not enforcement.
- Strongest claims for the application: cert-presentation auth
  (1.18.6, 7759abc) is the lead; four-primitives orthogonality
  (invariant 1) and DNS-anchored cryptographic identity (DNS root
  → namespace controller → team controller → agent) are the
  supporting structure.
- Rotation log: pushed back on "verifiable without trusting the
  registry" — the chain IS self-verifying per
  `identity-key-verification.md`, but the same doc states "no
  global transparency yet"; correct framing is "cryptographically
  self-verifying rotation chain (full registry transparency on
  roadmap)."
- Hosted-only beyond billing: managed namespaces, OAuth MCP for
  browser clients, dashboard UI. Everything else is OSS-parity.
- Five-minute claim: holds for the hosted path; BYOIT (bring your
  own DNS namespace) is Stage 4-5 per user-journey.md. Offered to
  time it on a clean container before YC publishes externally.

Production scale (queried AWID + cloud DBs): 91 persistent
identities, 57 namespaces, 45 teams in AWID; 44 active users, 53
organizations, 46 managed namespaces in cloud. Honest framing for
YC: dogfooding scale, not user-traction scale; distribution starts
this week.

## Pending engineering artifacts owed

- **KI#1 closure decision record technical content.** Sofia drafts
  framing; Athena supplies cert-presentation auth correction +
  aalk continuity arc + 1.18.6 trust-model arc + Aida 4/4
  attestation. Source: `agents/athena/aale-trust-contract.md` +
  aweb commit 7759abc. Not yet drafted.
- **Aida runbook PR tech-accuracy review.** Mentioned in handoff
  but inbox is empty; will verify state with Aida when she comes
  online.
- **Code-reviewer subagent pass on the v0.5.13 5-commit cluster**
  before signaling Hestia for the gate chain.

## Risks

- **Hestia not yet online.** Operations status from 2026-04-30
  flags her runbook + identity setup as the unblockers. v0.5.11
  and v0.5.12 shipped without her, and the next ac release
  (v0.5.13 candidate) will too unless she wakes and her runbook +
  identity land before the release window opens. Accept retro-
  actively, but going-forward release-discipline depends on her.
- **Aida / Iris / Metis directories don't exist on disk** despite
  the rename in commit `810d472`. `agents/aida/`, `agents/iris/`,
  `agents/metis/` are not yet created. No engineering blocker but
  the role separation stays partly theater until the agents are
  set up.

## Next checks

- Wait for Juan's walk-through of the real dev team / dispatch
  setup. Don't pre-empt with the published spawn-pair model.
- When Sofia drafts KI#1 closure framing, supply technical content.
- When Hestia comes online and her runbook lands, signal v0.5.13
  candidate with code-reviewer-subagent pass complete.
- Daily `/health` cross-check on app.aweb.ai + api.awid.ai;
  flag any drift.
