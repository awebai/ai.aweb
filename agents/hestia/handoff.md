# Hestia Handoff

Last updated: 2026-05-01 23:45 CEST (mid-exercise; v0.5.17 retroactive
gate run is in flight in the background)

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

**v0.5.17 retroactive exercise.**

- Tag `v0.5.17` (annotated, `b6c6e088`) is on origin pointing at
  `9c1038ad` (ac main). Authored by Mia at 22:55 CEST today.
  Render is rolling the image — at 23:45 CEST `app.aweb.ai/health`
  still reports `release_tag=v0.5.16`.
- The fix: layout containment in `AgentsPage.tsx` so the long
  fetch-cert command list scrolls horizontally inside the
  Add-Existing dialog instead of widening the modal.
- Athena's bless-and-run signal (mail 2026-05-01 ~23:30): run
  `make release-ready` locally against `9c1038ad` to seed the
  runbook with real timing/output observations, post verified-live
  mail when Render rolls forward. No tag step (already done by Mia
  pre-routing-decision); no rollback.
- Background gate run: started 2026-05-01 ~23:45 CEST; output at
  `/tmp/hestia-release-ready-v0.5.17.log`. Background bash task ID:
  `biirc1l0p`.

**Next instance reads first:**

1. The log file. Did the chain complete? What was the per-gate
   timing? Any unexpected gate failures?
2. `/health` on `app.aweb.ai`. Has Render rolled to v0.5.17?
   Expected: `release_tag=v0.5.17`, `git_sha=9c1038ad…`,
   `aweb_version=1.18.6`, `awid_service_version=0.5.3`.
3. Inbox + chat (`aw mail inbox`, `aw chat pending`). Athena's
   code-reviewer-subagent pass on `937f37b0` was queued for
   tonight; if her result is in the inbox, fold it into the
   verified-live framing.
4. Whether the verified-live mail was posted. If not, draft and
   send per the runbook step 10 template:
   - To: athena, sofia, juan
   - Subject: `verified-live: ac v0.5.17 add-existing dialog layout containment`
   - Body: what fixed (modal containment, plain `aw init`,
     conditional caption); what NOT (no Add-Existing local
     reproducer yet — Athena lane); what evidence (gate-chain
     output snippet); what live check (/health version+sha
     match + browser probe of the Add-Existing dialog with a
     long fetch-cert command).

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

1. **Read `/tmp/hestia-release-ready-v0.5.17.log`** — did the gate
   chain complete? Per-gate timing? Any failures?
2. `curl https://app.aweb.ai/health` — has Render rolled to
   v0.5.17?
3. `aw mail inbox` and `aw chat pending` — Athena's code-reviewer
   result, any other peer signal.
4. If chain passed AND Render rolled AND no posted verified-live
   yet: post the verified-live mail per runbook step 10.
5. If chain failed: mail Athena the failure shape immediately.
6. Update operations.md with v0.5.17 verified-live state and fold
   gate-timing observations into the runbook.
7. Begin the publishing-path timing breakdown (Sofia owed).

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
