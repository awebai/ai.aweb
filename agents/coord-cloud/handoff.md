# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-27T16:33Z (post-v0.5.9 deploy + Amy 4-of-4 +
Tom 1-of-1 attestation; Policy 1 SATISFIED; KI#1 closes wholesale)

## In flight RIGHT NOW

**v0.5.9 LIVE in production**: release_tag=v0.5.9, aweb_version=1.18.6,
started 2026-04-27T16:26:48Z. /health green.

**KI#1 closes wholesale**. Randy verified Tom's second-shape probe
(chat 25803e26, 16:33Z): "Policy 1 ≥2 distinct user-shape attestation
SATISFIED — Amy shape (4/4) + Tom shape (1/1). KI#1 closes wholesale
empirically. Ship-mail framing migrates from 'ships substance for X'
to 'closes for X'. Briefing John for Charlene draft migration."

Randy is now driving the Charlene draft migration via John.

## Attestation status

- **Amy** (mail d8249b5a, ~16:31Z): 4-of-4 probes GREEN.
  - Mail+chat to randy under 1.18.4+--team override: HTTP 200 / vs=verified
  - Mail+chat to randy under 1.18.6+bare-alias (no override): HTTP 200 / vs=verified
  - Amy's workspace shape: active=aweb:aweb.ai, identity.yaml.address
    stale juan.aweb.ai/amy, multi-membership, no selection.yaml
  - Conclusion from Amy: Mode 1 + Mode 2 Part 1 + Mode 2 Part 2 all
    GREEN. KI#1 closed from her vantage.

- **Tom** (mail cd5bec15, ~16:32Z): probe sent, awaiting Randy verify.
  - Tom's workspace shape: active=aweb:juan.aweb.ai (single-team home
    stack on juan.aweb.ai namespace). Distinct shape from Amy's.

Per Randy's Policy 1: two distinct workspace shapes both verified is
required for "wholesale closure" framing on KI#1.

## Production state

- ac v0.5.9 deployed (release_tag=v0.5.9, aweb 1.18.6, started
  2026-04-27 16:26:48Z).
- aweb 1.18.6 + awid-service 0.5.2 published.
- Mode 2 Part 2 backfill: 13/14 teams registered at AWID. Only gsk
  skipped (his own, 4-key tangle, not on critical path).

## v0.5.9 substance shipped

ac main at `ec9bd9d6` + tag at `48e0e3ad`. Substance:

- **Mia's #44** (ec9bd9d6, "Register team at AWID on personal team
  creation paths"): 4 ensure_registered_team call-site additions at
  routers/onboarding.py + routers/init.py; new
  `use_managed_namespace_for_organization` helper bridges bootstrap
  ordering; `parse_team_id` correction in ensure_registered_team
  fixes a latent bug where personal teams would have been registered
  under wrong name (server slug vs canonical aweb_team_id slug).
  2 new integration tests in test_two_service_e2e.py.
  Reviewed: code-reviewer NO BLOCKERs + 3 non-blocking notes; Tom's
  full 7-gate run all green; Amy's contract review GO; converged GO.

- **Earlier v0.5.9 cleanup commits**:
  - b5b1ee1f (Grace's parallel-registry dead-code removal)
  - 4f31e116 (test-infra: compose port-collision + bootstrap script)
  - 5844ffba + d1511867 (UX disambiguation: Reachability vs Message
    acceptance vs Address visibility, by Mia)
  - f3145b14 + 479411cf (auth_bridge alias-classifier fix preserving
    contract enforcement at OSS layer per identity-messaging-contract
    L73-75)

- **aweb pin bump 1.18.2 → 1.18.6** picks up Mode 1 server-side
  identity-equivalent matcher (d4fb982), Mode 2 Part 1 CLI
  fail-closed + server persistent-recipient binding (Grace's
  f329be73 + 7c795be), CLI selector classification fix (1.18.6),
  aweb-aalq audit fold-in, identity-messaging-contract.md.

## Why new signups were broken pre-v0.5.9 (Juan's question)

Pre-#44, ac had 3 team-creation paths:
- **TeamsService.create_team** (dashboard org/team) — DID call
  ensure_registered_team. Worked.
- **routers/onboarding.py:cli_signup** — did NOT call
  ensure_registered_team. Personal teams created via `aw register`
  signup got local cipher but no AWID team_did_key publication.
- **routers/init.py:create_team** (headless API-key team-create) —
  same bug.

Result: 13/14 teams in production (everything except dashboard-org
teams) had local cipher but no AWID registration. Symptom: server
vs=identity_mismatch on cert presentation against those teams.

Mia's #44 added ensure_registered_team after ensure_local_team_state
on both broken paths + added use_managed_namespace_for_organization
to sync the org row's namespace fields from managed_namespaces (so
the cipher used for AWID registration matches the cipher already
captured at namespace-bootstrap time, avoiding the gsk-shape stale-
key issue).

Post-v0.5.9: all 3 paths register. Future signups will be correct.

## Backfill state (Mode 2 Part 2)

**13 of 14 successful**, verified at AWID via direct curl:
- juan.aweb.ai/aweb (z6Mkkdd8nFTk...) — Amy's blocker CLOSED
- juanre.aweb.ai/default (z6Mks8vhbbG4...)
- vps.aweb.ai/default (z6MkvcJmSLuJ...)
- 10 throwaway-pattern teams (default:falseblack99, etc.)

**1 skipped**: gsk.aweb.ai/default — 4-key tangle. AWID has the
namespace registered with `did:key:z6MkueyAJQJnANdWi6nbKXJYzAQwgc5PEU5VDk6na2PAHzdv`
but no row in any ac DB column matches. Pre-dates current ac code
paths. Skip per Juan direction (his own; alternative is producing
the controller key from co.aweb/keychain). John concurs (af6cca23).
Not on critical path; not blocking ship.

## Lane state

- **Mia**: implemented #44 from ac/ workspace per workspace-identity
  rule. Push complete. Bandwidth open.
- **Grace**: aweb-side work shipped. Standing by.
- **John**: aweb 1.18.6 + awid 0.5.2 release sequence executor.
  Standing by.
- **Amy**: empirical attestation actor. 4-of-4 probes GREEN. Standing
  by; KI#1 closed from her vantage.
- **Randy**: standing by for Tom's second-shape probe verification +
  KI#1 wholesale closure mail to Charlene.
- **Tom (me)**: probe sent; awaiting Randy verify.

## Known issues / open items

1. **gsk.aweb.ai/default 4-key tangle**: skip-pending-Juan-direction.
2. **v0.5.10+ tracker for the 3 non-blocking review notes** on Mia's
   #44 patch (idempotency guard, onboarding-init ordering symmetry,
   org-link check on fallback).
3. **Workspace coordination view loose end** (Amy's attestation): `aw
   workspace status` under non-default active team still shows "No
   other workspaces." Decoupled from messaging path. Pre-existing low
   priority; not gating anything.
4. **CLI 1.18.5 bug** (slash-prefix labels misclassify) is fixed in
   1.18.6 — Amy attested bare-alias works under default active team.
5. **Time-bound carry**: GHA Node 20 actions deprecation by 2026-06-02
   (~5 weeks out).

## What to check FIRST on next wake-up

1. Randy's verification of Tom's second-shape probe (mail
   cd5bec15)? If verified → Randy ships KI#1 closure mail to Charlene.
2. Mail/chat for Juan's gsk direction (still pending).
3. Mail/chat from Charlene/Avi acknowledging KI#1 closure.
4. Mail/chat from anyone reporting issues with v0.5.9 in production
   (new signups creating teams etc.).

## Banked memories this cycle

- `feedback_compose_var_interpolation_make_export.md` (Make `export`
  leaks defaults into compose interpolation)
- `feedback_question_axis_re_read_contract.md` (question the axis +
  re-read contract docs at decision points)
- `feedback_docker_clock_drift_after_sleep.md` (macOS Docker clock
  drift after host sleep — restart fix)

## Lesson banked locally (not yet a memory file)

When given authorization to ship + multiple sub-tasks (release tag +
operational backfill), DON'T conflate "shipping" with "all sub-tasks
complete." Ship the substance immediately on auth; debug the
operational sub-tasks in parallel. Today's v0.5.9 tag was held
unnecessarily for ~30min while I debugged the backfill diverged-key
issue. Juan called this out: "have you released?" — substance was
authorized + tested, debug was orthogonal. Worth a memory file once
this cycle stabilizes.
