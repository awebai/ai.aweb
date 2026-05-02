# Hestia Handoff

Last updated: 2026-05-02 22:15 CEST (post first end-to-end exercise;
ac v0.5.18 + aw CLI 1.18.8 verified-live)

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between. Today (2026-05-02)
was the first real end-to-end exercise of the runbook surface — a
clean cycle from Athena's bless-and-run through verified-live, with
a recoverable gate-failure detour in the middle. Real timing,
real failure-mode, real cross-repo dance now live in the runbook.

The team:

- **Sofia**: direction. Out of routing for bug-fix releases by
  default; mail before tag only for external-claim weight.
- **Athena**: code in aweb and ac. Briefs you with bless-and-run
  mail after running code-reviewer subagent on gate-input commits.
- **Mia / Noah / Grace / Kate**: dev team (`aweb:juan.aweb.ai`,
  separate cryptographic team). Author feature work, Athena reviews.
- **Aida / Iris / Metis**: pending Hetzner deploy. Not yet online.

## Identity (live since 2026-05-01 21:05 UTC)

- did: `did:key:z6MkebRpF7qEFNt5vAYa5BWjegFk1igt6mRESqWb5r3kp9AK`
- stable: `did:aw:3fC4cfvFuVAxZCWyJNRCoUxHVAim`
- address: `aweb.ai/hestia`
- active team: `default:aweb.ai`
- workspace_id: `8ae26888-ee11-4e1f-beff-aaab79b44b58`
- registry: registered at `https://api.awid.ai`

## What's live (verified 2026-05-02 21:50 UTC)

- ac: v0.5.18 at `app.aweb.ai`, git_sha `4ace97702077a43e7067f296848145c40204444a`,
  aweb_version 1.18.6, awid_service_version 0.5.3.
- aw CLI: 1.18.8 on npm `@awebai/aw` and GitHub Releases.
- aweb server: 1.18.6 (unchanged this cycle).
- awid registry: 0.5.2 at `api.awid.ai` (unchanged).
- channel: 1.3.3 (unchanged).

## What just shipped (cycle complete)

ac v0.5.18 + aw CLI 1.18.8 closes:

- claim-human cli_signup orphan vector at claim time (98cfc278);
  validate-first / write-last router refactor + atomic
  cli_signup-upgrade UPDATE.
- BYOD-domain-as-username auto-inference removed from CLI (443151d);
  CLI now requires explicit `--username` for BYOD users.

Open follow-ups in **Athena's lane** (filed):

- aamb (CLI signup AWID-existing-namespace check)
- aamc (TOCTOU on cli_signup-upgrade email-conflict check)
- aama (unowned-team orphan vector at init.py:2107-2127)
- A.18a/A.18b e2e-script split (architectural-tests follow-up;
  current A.18 mocks the contract via `--username "$ORG_SLUG"` —
  splitting documents the managed-vs-BYOD distinction in the
  e2e surface; may connect to bob's API-key-bootstrapped identity
  address shape, possibly fold into aamb).

## First-exercise debrief (banked into runbook.md)

The cycle ran ~80 min from Athena's bless-and-run to verified-live,
including a gate-failure-and-recovery loop:

1. Bless-and-run mail at ~18:00Z (ac 98cfc278 + aweb 443151d,
   pre-flight already done by Athena+Mia).
2. Pre-flight: HEADs verified, ac pin semantics confirmed
   (`aweb` package = server, server unchanged → no pin bump).
3. aweb `make ship` in background (7m6s, GREEN).
4. ac bump 0.5.17 → 0.5.18, `uv sync --refresh`, commit 4ace9770.
5. ac `make release-ready` + compat: FAILED at A.18 phase — both
   arms identically — diagnosed as test-script gap (script
   didn't pass `--username`).
6. Mailed Athena failure shape; she landed 1be46c42 with
   `--username "$ORG_SLUG"`.
7. ac re-run: GREEN (release-ready 198s, compat 57s).
8. Tag `aw-v1.18.8` on aweb 443151d → push.
9. Tag `v0.5.18` on ac 4ace9770 → push.
10. GHA fired both: aweb sync → awebai/aw → goreleaser + npm
    (~3 min); ac aweb-cloud CI/CD image build (~13 min) → GHCR.
11. Juan deployed ac manually from GHCR.
12. Verified live: /health version match + smoke probe
    (`aw whoami` works; `aw claim-human` with bogus slug returns
    "Requested username does not match this team" — confirms
    new validation chain is enforced live).
13. Verified-live mail to athena, sofia, juan with full evidence.
14. Runbook updated with first-exercise observations.

Key learnings folded into runbook:

- aweb `make ship` baseline 7m6s (anomaly threshold > 10 min).
- aw CLI version-coupling foot-gun: Makefile `CLI_VERSION :=
  SERVER_VERSION` is stale when CLI moves alone. Tag directly
  with `git tag -a aw-vX.Y.Z <commit>`.
- Compat-failure-by-arm-pattern diagnostic: BOTH arms failing
  identically = e2e script gap (script gaps masquerade as CLI
  bugs); only installed-aw = real regression / intentional
  break; only local-aw = new-CLI regression.
- Validated bless-and-run mail shape under the new role model.
- Manual-deploy step for ac AND awid registry (Render does NOT
  auto-deploy — Juan triggers each).

## Banked working agreements (held through 2026-05-02)

**Sofia (mail thread 2026-05-01):**
- Bug-fix / no-external-claim-weight releases tag through Hestia's
  gate chain. Sofia OUT of routing.
- Mail Sofia BEFORE tag only when external-claim weight applies.
- Otherwise she reads `/health` on verified-live mail.

**Athena (mail thread 2026-05-01 + 2026-05-02):**
- Dev team stops at clean-main. Tags + gates + deploys + verify-
  live in Hestia's lane.
- Code-reviewer subagent runs BEFORE bless-and-run mail.
- Bless-and-run mail names: target repo, expected SHA, change
  shape, code-reviewer-pass result, cross-repo dependency
  decisions, compat scope, expected failure-shapes (if any).
- Failure during gate run → mail Athena failure shape; she lands
  the fix; you re-run.

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — release-handoff or
   peer signal.
2. `curl https://app.aweb.ai/health` and `curl https://api.awid.ai/health`
   — current live state vs operations.md.
3. `aw work active` and `aw work blocked` — sweep stale claims.
4. If a release-handoff mail arrived: run the runbook end-to-end
   on the new candidate. Compat scope per Athena's mail.
5. If Athena's A.18a/A.18b split landed: a future ac release
   exercising it would update the compat-criterion observation
   in the runbook (specifically: managed-aw should pass A.18a
   without `--username`; that path doesn't exist today).

## Open follow-ups (Hestia's lane)

1. **Publishing-path timing breakdown** for Sofia. Compose a
   doc: GHA build, GHCR push, image-pull, deploy-rollout. Pull
   from v0.5.18 specific timing once the GHA run has logged.
2. **Test-suite triage** in ac/Makefile — which targets compose
   to the ~20-min cost (deferred).
3. **Stale repo-manager dirs** (`agents/coord-cloud/`,
   `agents/repo-aweb/`). Untracked, low-priority. Tracked under
   aweb-aals.5.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (run gates here for aweb releases)
- `ac` → `../../../ac` (run gates here for ac releases)

Prefer `git -C aweb log` over `cd aweb && git log`. Do NOT run
`aw` from sibling repos. Read sibling repos to run gates and
verify what shipped; do NOT edit code there (Athena's surface).

## Note on git author attribution

Commits authored by dev-team members (Mia et al.) appear as
"Juan Reyero" in `git log`. The actual agent identity is carried
via the aweb cert. Cross-check author with Athena when attribution
matters; she routes to the actual author.
