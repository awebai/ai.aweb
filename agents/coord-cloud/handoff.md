# Coordinator aweb-cloud (Tom) — Handoff

Last updated: 2026-04-27 (post-v0.5.9 tag push; backfill 3/4 + gsk
skip-pending-direction; awaiting GHA + Render deploy)

## In flight RIGHT NOW

**v0.5.9 tag pushed** at `48e0e3ad1ab4aaa2a1818cc51217968d3d964378`
(2026-04-27 16:08Z). GHA in progress. Render auto-deploy fires after
GHA succeeds; `/health` still on v0.5.8.1 at last check (~10min into
GHA).

When `/health` flips to v0.5.9 / aweb 1.18.6:
1. Notify Amy. She runs Probes 1+2 (mail + chat to randy via
   plain-alias `--to randy`) within ~15min.
2. Notify the team. Closure framing: Mode 1 + Mode 2 Part 1 + Mode 2
   Part 2 (3-of-4 backfilled) all empirically attested.

## Production state (as of last update)

- ac v0.5.8.1 deployed (release_tag=v0.5.8.1, aweb 1.18.4, deploy
  2026-04-26 21:12Z).
- aweb 1.18.5 + 1.18.6 + awid-service 0.5.2 published to PyPI/npm.
- v0.5.9 tag pushed; deploy pending.

## Backfill state (Mode 2 Part 2)

**3 of 4 successful**, verified at AWID via direct curl:
- juan.aweb.ai/aweb registered (z6Mkkdd8nFTk...) — Amy's blocker CLOSED
- juanre.aweb.ai/default registered (z6Mks8vhbbG4...)
- vps.aweb.ai/default registered (z6MkvcJmSLuJ...)

**1 failed**: gsk.aweb.ai/default — 4-key tangle. AWID has the
namespace registered with `did:key:z6MkueyAJQJnANdWi6nbKXJYzAQwgc5PEU5VDk6na2PAHzdv`
but no row in any ac DB column matches. Pre-dates current ac code
paths. **Skip pending Juan's direction** (default: skip; alternative
is producing the controller key from co.aweb/keychain). John concurs
skip (af6cca23). Not on critical path; not blocking ship.

## v0.5.9 substance shipped

ac main at `ec9bd9d6` + tag at `48e0e3ad` (pin/version bump on top).
Substance:

- **Mia's #44** (ec9bd9d6, "Register team at AWID on personal team
  creation paths"): 4 ensure_registered_team call-site additions at
  routers/onboarding.py + routers/init.py; new
  `use_managed_namespace_for_organization` helper bridges bootstrap
  ordering; `parse_team_id` correction in ensure_registered_team
  fixes a latent bug where personal teams would have been registered
  under wrong name (server slug vs canonical aweb_team_id slug).
  2 new integration tests in test_two_service_e2e.py.
  Reviewed thoroughly: code-reviewer subagent NO BLOCKERs + 3
  non-blocking notes; Tom's full 7-gate run all green; Amy's contract
  review GO; converged GO. 3 follow-up notes tracked for v0.5.10
  (use_managed_namespace_for_organization idempotency guard,
  onboarding.py ordering symmetry with init.py,
  ensure_registered_organization_namespace explicit org-link).

- **Earlier v0.5.9 cleanup commits** (already on origin/main):
  - b5b1ee1f (Grace's parallel-registry dead-code removal)
  - 4f31e116 (test-infra: compose port-collision + bootstrap script)
  - 5844ffba + d1511867 (UX disambiguation: Reachability vs Message
    acceptance vs Address visibility, by Mia)
  - f3145b14 + 479411cf (auth_bridge alias-classifier fix preserving
    contract enforcement at OSS layer per identity-messaging-contract
    L73-75)

- **aweb pin bump 1.18.2 → 1.18.6** in v0.5.9 release commit. Picks
  up Mode 1 server-side identity-equivalent matcher (d4fb982),
  Mode 2 Part 1 CLI fail-closed + server persistent-recipient binding
  (Grace's f329be73 + 7c795be), CLI selector classification fix
  (1.18.6), aweb-aalq audit fold-in, identity-messaging-contract.md.

## Lane state

- **Mia**: implemented #44 from ac/ workspace per workspace-identity
  rule (AGENTS.md: don't impersonate other workspaces). Push complete.
  Bandwidth open for next ticket.
- **Grace**: aweb-side work shipped (ff5e798 + 32bb7c6 + ef5c3d7 + the
  1.18.5/1.18.6/0.5.2 release stack). Standing by.
- **John**: aweb 1.18.6 + awid 0.5.2 release sequence executor. AWID
  endpoint verifications + co-review on Tom's lane. Standing by.
- **Amy**: empirical attestation actor. Backfill independently
  verified juan.aweb.ai/aweb registration + cert authority chain
  (60e747d3). Standing by for v0.5.9 deploy notice; will run Probes
  1+2 within ~15min of notice.
- **Randy**: standing by for KI#1 wholesale closure mail to Charlene
  once Probes 1+2 land.
- **Tom (me)**: monitoring GHA + /health flip; coordinating
  post-deploy attestation chain.

## Known issues / open items

1. **CLI 1.18.5/1.18.6 selector classification**: slash-prefixed
   hosted-team labels (e.g. `juan.aweb.ai/randy`) misclassify as
   direct AWID addresses. Workaround: plain alias (`--to randy`).
   Fix scope: aweb 1.18.7 or wherever the classifier fix lands
   (Grace's lane).
2. **gsk.aweb.ai/default 4-key tangle**: skip-pending-Juan-direction
   (above).
3. **v0.5.10+ tracker for the 3 non-blocking review notes** on Mia's
   #44 patch (idempotency guard, onboarding-init ordering symmetry,
   org-link check on fallback).
4. **Render auto-deploy is sometimes manual**: per Juan's earlier
   "render is manual but github is automatic" — historical pattern
   (v0.5.6 stalled past 50min auto-roll window). Watch /health for
   v0.5.9 flip; if past ~30min after GHA succeeds and still on
   v0.5.8.1, Juan triggers manually.

## What to check FIRST on next wake-up

1. `/health` flipped to v0.5.9? If yes, notify Amy + run any deferred
   coord cleanup.
2. GHA workflow status (`gh run list --limit 1 --workflow="aweb-cloud CI/CD"`).
3. Mail/chat for Amy's attestation results (Probes 1+2).
4. Mail/chat for Juan's gsk direction.
5. Mail/chat for Randy's ship-mail-to-Charlene trigger.
6. Time-bound carry: GHA Node 20 actions deprecation by 2026-06-02
   (~5 weeks out).

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
