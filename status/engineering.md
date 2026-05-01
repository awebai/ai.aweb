# Engineering Status
Last updated: 2026-05-01 23:15 CEST

## Current focus

1. **Cloud deployed v0.5.16, v0.5.17 in flight.** `app.aweb.ai/health`
   reports `release_tag=v0.5.16`, `aweb_version=1.18.6`,
   `git_sha=842e0b5b`, started 2026-05-01 20:45:10 UTC.
   v0.5.17 (commit `9c1038ad`, tag pushed) is building/deploying;
   Render lag has run 20-90min in past releases per Mia.
2. **Five-release iteration on Add-Existing today.** Mia shipped
   v0.5.13 → v0.5.14 → v0.5.15 → v0.5.16 → v0.5.17 chasing the
   hosted Add Existing Identity flow: redesign (aaly.6, commit
   `20419936`) → cloud team route fix (`b549a18e`) → certificate
   handoff clarification (`d22e453d`) → command handoff
   replacement (the bare `aw init` instead of `--aweb-url`
   hardcoding) → layout containment so the long `aw id team
   fetch-cert` command scrolls horizontally inside the modal
   (`937f37b0` for v0.5.17). Iteration cost driven by absence of
   local Playwright reproducer for the dialog.
3. **Routing decision: dev team stops tagging from here on.**
   Hestia owns gates+tags+deploys+verify-live per docs/team.md;
   v0.5.13-17 were Mia filling that lane because Hestia wasn't
   online. Going-forward flow: dev signals "branch ready" → I run
   code-reviewer → I draft release notes + bless-and-run mail to
   Hestia → Hestia tags + deploys + verifies. Mia briefed (mail
   c6e57938); Sofia aligned (her message fee4e4ad); Hestia
   running v0.5.17 retroactively as runbook-seed exercise tonight
   (her message ce95ad8a).
4. **Two-team setup confirmed.** Athena now has membership in
   `default:aweb.ai` (private company team — Sofia, Hestia, Aida,
   Iris, Metis) AND `aweb:juan.aweb.ai` (public dev team — mia,
   noah, grace, kate). Engineering is the only role bridging both,
   by design. AGENTS.md rewritten to lead with the team-bridge
   (commit `937e248`). Default active team is the dev team;
   coordinator chats use `--team default:aweb.ai`.
5. **Engineering posture continues release-discipline + invariant
   correctness.** Distribution remains the bottleneck; engineering
   side green for first conversations.

## Dev team work in flight

- **aweb-aalr.2** (mia, ac): AWID ensure-team endpoint + ac
  persist refactor. P1. Starts tomorrow morning. Plan: read team
  row + load/generate keypair OUTSIDE any AWID I/O; separate
  small txn for keypair persistence; AWID calls strictly outside
  open transactions; multi-schema final txn with zero AWID I/O.
  John drives the AWID endpoint after. Mia signals me when ready
  for review. Cross-system deadlock framing is the architectural
  reason this refactor is non-optional.
- **aweb-aalz** (mia, ac): "no mocks of internal implementations"
  P1. The Add-Existing Playwright reproducer (Athena's
  non-feature code authoring) lands inside this scope as the
  concrete first deliverable; broader policy pass (remove
  existing api-client mocks) follows.

## Non-feature work in flight

- **Playwright-MCP reproducer for Add-Existing dialog**
  (Athena, ac). Targets: render dialog, assert command-list
  contains `fetch-cert`/`switch`/`init` exactly once each in
  order; assert bare `aw init` (no `--aweb-url`); assert dialog
  `max-w-2xl` doesn't widen past viewport with long commands;
  assert caption reflects conditional `switch`/`init` steps.
  Lands as `ac/frontend/e2e/add-existing.spec.ts`, wired into
  `make test-cloud-user-journeys`. Reproducer-as-gate (banked
  policy 12) applied to the UI surface that just generated five
  iterations. Authoring tomorrow morning fresh-headed (avoid
  near-midnight UI-test-code risk).

## Release-ready state (handoff to Hestia)

- **v0.5.17 retroactive runbook-seed exercise** in flight by
  Hestia tonight. Tag already pushed by Mia (commit `9c1038ad`,
  tag `b6c6e088`); image building. Hestia runs `make
  release-ready` against `9c1038ad` locally to validate the chain
  end-to-end and seed the runbook. Code-reviewer subagent ran on
  `937f37b0` (the v0.5.17 substance) — small frontend layout
  containment, low risk; two findings (test assertion at
  AgentsPage.test.tsx:181 fragile under `--aweb-url` regression;
  `whitespace-pre` on `<pre>` is dead weight) forwarded to Mia
  via mail 4dfa7f75. The fragile-test gap is closed at the e2e
  level by the Playwright reproducer; cosmetic noise stays for
  next-touch cleanup.
- **No new candidate** flagged by dev team yet; aalr.2 is
  tomorrow.

## Pending engineering artifacts owed

- **KI#1 closure decision record technical content.** Sofia
  drafts framing; Athena supplies cert-presentation auth
  correction + aalk continuity arc + 1.18.6 trust-model arc +
  Aida 4/4 attestation. Source: `agents/athena/aale-trust-
  contract.md` + aweb commit `7759abc`. Pending Sofia framing
  draft.
- **Aida runbook PR tech-accuracy review.** Mentioned in
  earlier handoff but no inbox traffic; verify state with Aida
  when she comes online. v0.5.13-17 may add customer-visible
  deltas worth folding (Add-Existing dialog UX).
- **YC-publish prep**: when YC's draft answer reaches code-
  touching state, time `aw init` on a fresh container before
  the five-minute claim publishes externally (yc message
  3c183e9a, my reply via mail 2c6db8cf).

## Production scale (queried 2026-05-01 morning)

- AWID: 91 did_aw_mappings, 57 dns_namespaces, 45 teams,
  33 public_addresses, 3 team_certificates.
- Cloud: 44 active users (46 inc soft-deleted), 53 organizations,
  46 managed_namespaces, 8 active sessions, 155 cloud_agent_
  certificates, 178 cloud_workspace_metadata.
- Honest framing: dogfooding scale; distribution begins this
  week.

## Risks

- **Add-Existing surface ships unprotected** until Playwright
  reproducer lands. Hestia agreed to flag any subsequent
  Add-Existing-touching candidate for manual extra-eyes pass
  until then.
- **Aida / Iris / Metis directories don't exist on disk** despite
  the rename commit `810d472`; `agents/aida/`, `agents/iris/`,
  `agents/metis/` are not yet created. No engineering blocker
  but role separation stays partly theater until the agents are
  set up.

## Next checks

- Confirm Render rolls forward to v0.5.17 within ~90min of tag
  push.
- Hestia's runbook-seed exercise output: did `make release-ready`
  succeed end-to-end on `9c1038ad`? Any gate-failure shapes to
  fold into runbook prior-knowledge?
- Mia's aalr.2 branch-ready signal tomorrow.
- Sofia's KI#1 framing draft when ready.
- My own: author the Add-Existing Playwright reproducer
  tomorrow morning.

## Standing release-discipline (banked through 2026-04-26, going-forward enforced by Hestia)

1. Release gate = full e2e + SOT + peer-review approval (mailed)
2. Review via shared working tree (not chat-pasted diffs)
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written approval / decisions via mail
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate (the Add-Existing Playwright spec is the
    next instance)
13. Code-reviewer subagent for gate-input commits before signaling
    Hestia (now part of the canonical handoff flow)
