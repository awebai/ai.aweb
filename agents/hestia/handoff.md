# Hestia Handoff

Last updated: 2026-05-01 23:55 CEST (post-Juan-call; v0.5.17
retroactive exercise called off; waiting on next bless-and-run)

## Read this first

You are Hestia. You carry every release across the build/ship boundary
and keep the company machinery healthy in between. Tonight (2026-05-01)
was the first wake-up under live identity — the runtime layer for the
role separation became real. Identity, mailing, gating, and a runbook
all came online today.

The team you work with:

- **Sofia**: direction — priorities, decisions, technical direction,
  release-claim framing for external-claim-weighted releases.
- **Athena**: code in aweb and ac. Briefs you with bless-and-run mail
  after running code-reviewer subagent on gate-input commits.
- **Mia / Noah / Grace / Kate**: dev team (`aweb:juan.aweb.ai`,
  separate cryptographic team). Author feature work, Athena reviews.
- **Aida / Iris / Metis**: pending Hetzner deploy. Not yet online.

Within your role, you decide. Across roles, collaborate. Tonight's
working agreements got banked from real exchange — see "banked
working agreements" below.

## Identity (live as of 2026-05-01 21:05 UTC)

- did: `did:key:z6MkebRpF7qEFNt5vAYa5BWjegFk1igt6mRESqWb5r3kp9AK`
- stable: `did:aw:3fC4cfvFuVAxZCWyJNRCoUxHVAim`
- address: `aweb.ai/hestia`
- active team: `default:aweb.ai` (company team)
- workspace_id: `8ae26888-ee11-4e1f-beff-aaab79b44b58`
- registry: registered at `https://api.awid.ai`

## What's in flight tonight

**Nothing.** The v0.5.17 retroactive exercise was kicked off
(Athena's bless-and-run, ~21:15Z) and called off by Juan ~22:00Z —
v0.5.17 ships without my retroactive verification. Local
`make release-ready` was terminated; the log at
`/tmp/hestia-release-ready-v0.5.17.log` is partial and not worth
reading. No verified-live mail to post.

The first real exercise comes on the **next** bless-and-run mail
from Athena — that is what wakes me into a release.

**What's true about v0.5.17 for the record:**

- Tag `v0.5.17` (annotated, `b6c6e088`) is on origin pointing at
  `9c1038ad` (ac main). Authored by Mia at 22:55 CEST 2026-05-01.
- Fix: layout containment in `AgentsPage.tsx` so the long
  fetch-cert command list scrolls horizontally inside the
  Add-Existing dialog instead of widening the modal.
- GHA "Build Release Image" run id `25233272933` started 21:09:18Z;
  was 27+ min in when last checked (vs ~13 min for v0.5.16).
- /health was still v0.5.16 at hand-off time. Render rollout state
  is no longer my concern for this release.

**Next instance reads first:**

1. `aw mail inbox` and `aw chat pending`. The release-handoff
   mail from Athena is what kicks the next exercise.
2. `/health` on `app.aweb.ai` and `api.awid.ai`. Compare to
   `status/product.md` claims; flag drift to Sofia if any.
3. `aw work active` and `aw work blocked`. Sweep stale claims.
4. If a release-handoff mail arrived, run the runbook end-to-end.
   That's the first real validation of the seeded runbook.
5. If no handoff but a clean-main commit appeared on ac/aweb that
   looks candidate-shaped (version bump in pyproject + uv.lock),
   mail Athena: "is X queued for my chain?"

## Banked working agreements (from tonight's exchanges)

**Sofia (mail thread 2026-05-01):**

- Bug-fix / no-external-claim-weight releases tag through Hestia's
  gate chain by default. Sofia is OUT of routing.
- Mail Sofia BEFORE tag only when the release carries external-
  claim weight: new public capability, customer-visible behavior
  change, anything affecting value-prop framing.
- Otherwise Sofia reads `/health` when verified-live mail posts.

**Athena (mail 2026-05-01):**

- **Going-forward routing.** Dev team stops at "branch ready /
  clean main." They do NOT tag. Tags + gates + deploys + verify-
  live all in Hestia's lane.
- Flow: dev team lands work + signals Athena → Athena runs code-
  reviewer subagent on gate-input commit (policy 13) → Athena
  drafts release notes + mails Hestia bless-and-run → Hestia runs
  `make release-ready` → tag → push → wait for image → verify
  live → post verified-live with evidence.
- For v0.5.13–v0.5.16 (already shipped without me, retroactively
  accepted) and v0.5.17 (already tagged by Mia before the routing
  decision was banked): no rework. Going forward Athena will brief
  Mia on the new flow.
- Code-reviewer subagent runs BEFORE the bless-and-run mail, not
  after.

## State of the runbook (`runbook.md`)

Exists as of 2026-05-01. Seeded from `../../docs/decisions.md` +
Makefile survey. Marked **[unvalidated]** wherever the shape comes
from prior decisions but I haven't yet executed it solo. Tonight's
v0.5.17 exercise is the first validation pass — when it completes,
update the unvalidated markers with real observations:

- Per-gate timing under the new `test-cloud-user-journeys` shape.
- Whether `make release-ready` requires anything I didn't anticipate
  (env files, Docker stack pre-warming, controller key paths).
- The shape of failure-mode output if any gate goes red.

If the chain completed clean, fold the timing data into the runbook
"step 4 (Gates)" section and remove the unvalidated marker on it.

If the chain failed, mail Athena with the failure shape immediately
(not next wake-up). Failure shape ≠ commit message grep — paste the
actual error output.

## Open follow-ups (Hestia-owned)

1. **Time the publishing path.** Sofia flagged ~30+ min per cycle.
   Compose the breakdown from GHA workflow logs: image build, GHCR
   publish, Render deploy rollout, health-check wait. Bring numbers
   to Athena/Sofia, not hand-waving.
2. **Test-suite triage in `ac/Makefile`.** Identify which targets
   compose to the ~20-min run, which are critical-path for changes
   of various shapes. Bring data; engineering decides what to keep
   / split / make optional.
3. **Stale repo-manager dirs on disk** (`agents/coord-cloud/`,
   `agents/repo-aweb/`). Untracked, low-priority, tracked under
   `aweb-aals.5`.
4. **Dashboard implementation** — signal inventory exists; concrete
   dashboard / report TBD per `docs/company-dashboard.md`.

## Open follow-ups (Athena-owned, on her surface)

- **`ac/frontend/e2e/add-existing.spec.ts`** — Playwright-MCP
  reproducer for the Add-Existing dialog. Athena committing
  tonight or tomorrow morning. Wired into `make
  test-cloud-user-journeys` as reproducer-as-gate (policy 12) for
  the surface. Until it lands: mail Athena before signaling on any
  Add-Existing-touching candidate so we add a manual eyes-on pass.
- **Code-reviewer subagent pass on `937f37b0`** — Athena running
  retroactively tonight while I do the gate-chain exercise. Result
  expected in inbox.

## Operational hygiene at this snapshot

- `aw workspace status`: hestia / athena / sofia online on
  default:aweb.ai. yc online in co.aweb. Dev team members
  (`aweb:juan.aweb.ai`) not visible from my workspace — Athena is
  the cross-team bridge.
- `aw work active`: 0 rows. `aw work blocked`: 0 rows. Clean.
- `mail inbox` after replies received: empty (Sofia + Athena
  threads handled; expect Athena's code-reviewer-pass result to
  arrive).

## What to check FIRST on next wake-up

1. `aw mail inbox` and `aw chat pending` — release-handoff or peer
   signal.
2. `curl https://app.aweb.ai/health` and `curl https://api.awid.ai/health`
   — current live state. Note whatever release_tag and git_sha are
   showing in operations.md for the wake-up.
3. `aw work active` and `aw work blocked` — sweep stale claims.
4. If a release-handoff mail arrived, work the runbook end-to-end
   on the new candidate.
5. The publishing-path timing breakdown is owed to Sofia (Sofia's
   first question of four). v0.5.16 baseline: 13m GHA + 7m Render =
   20m tag-to-live. v0.5.17 GHA was 27+ min (slower; investigate
   why). Pre-seed numbers when picking this up.

## Sibling repo symlinks under this dir

- `aweb` → `../../../aweb` (run gates here for aweb releases)
- `ac` → `../../../ac` (run gates here for ac releases)

Prefer `git -C aweb log` over `cd aweb && git log` — keeps CWD
anchored. Do NOT run `aw` from sibling repos (different workspace
identity). Read sibling repos to run gates and verify what shipped;
do NOT edit code there (Athena's surface).

## Note on git author attribution

Commits authored by dev-team members (Mia et al.) appear as
"Juan Reyero" in `git log`. The actual agent identity is carried via
the aweb cert. Cross-check author with Athena when attribution
matters; she routes to the actual author.
