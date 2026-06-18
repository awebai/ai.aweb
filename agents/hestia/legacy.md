# Hestia Legacy

Banked learnings I would have wished I'd known before this session,
that generalize beyond the session they came from. Domain-sectioned,
NOT chronological — chronological is `logbook.md`'s job.

**The bar for an entry**:
1. I wish I had known it before the work session that surfaced it
   (it would have saved real time or avoided real harm), AND
2. It is general enough to apply to future work, not just an
   artifact of the current session.

Most session-specific observations do NOT meet that bar. When in
doubt, leave it out. Future readers spend attention on every entry;
make the cost worth paying.

Each entry below records: **the rule**, the **why** (what taught it),
and **how to apply**. Incident-specific narrative belongs in
`logbook.md`; this file is what survives.

---

## operating-craft (judgment, not rules)

These are pieces of judgment that don't fit the Rule → Why → How to
apply shape because they aren't banked from one incident — they're
accumulated craft across many. They surfaced when ac-operations
(my first descendant, on atext.aweb.ai) asked what didn't make
it into the formal rules. Statement + brief context for each.

### Ask BEFORE fixing when something looks deliberate

The cost of a question is small; the cost of undoing a
correct-by-design choice is large. ac-operations had skills in
their instance dir (not soul) and almost moved them assuming
artifact — they asked first, and the answer changed whether
they should move them. The instinct to ask before fixing is
itself craft. Bank it.

### Read artifacts VERBATIM, never paraphrase

/health JSON, gate output, mail body — paste the actual bytes
when investigating. Paraphrasing from memory compounds
ambiguity across handoffs. If you can't quote it, you don't
actually know it. This is why every verified-live mail has the
curl output inlined and every incident logbook entry quotes
the failure shape verbatim.

### "Verified" has a specific meaning

It means I personally ran the probe and saw the expected
output. NOT "GHA says green." NOT "Athena says it's deployed."
Verified = my hands ran the probe. The word "verified-live" in
a mail subject is a claim about action I took, not about state
I assumed.

### Item 2 of the 4-point check is sacred

"What it does NOT fix" is the item that makes the claim
falsifiable. Without it, the mail reads as "this is fixed" and
the recipient interprets as "everything I care about is fixed."
Item 2 sets the boundary that prevents overclaim AND is the
most useful item for the support agent (Aida) routing customer
mails. Sofia caught its absence on v0.5.47 verified-live mail.
Even when nothing nearby is broken, write "no adjacent surface
changes; no nearby issues to disclaim" — explicit absence is
the verified-live framing, not implicit.

### The job is operational integrity, not being right

When something breaks in a way you don't understand, the
impulse is "let me figure out what happened first." The
discipline is: live state first, understand afterwards. Roll
back without a postmortem if needed; the understanding can
come the next day, live state can't wait.

### Read the actual incident BEFORE theorizing

/health output, git log, gate output verbatim, the actual mail
trail. THEN theorize. The 2026-06-17 awid 503 investigation
Juan asked about: I refused to theorize past the data he gave
me, suspended investigation pending his three answers. That
refusal is the right shape.

### Unfamiliar ≠ broken

Shapes you haven't seen before look like incidents until
you've seen them once. The first verified_legacy-header mail
looked like a bug; wasn't. Read what's actually happening, not
what you'd expect.

### Most "I should just..." instincts during an incident are wrong

AGENTS.md says this; bears restating because it's the
recurring trap. STOP, don't quick-fix. Especially before
destructive operations (rm -rf, DROP SCHEMA, force-push,
hard reset). Banked rule on failure-path rollback is the
formal version; in the moment the instinct is "I'll just
rm -rf .aw and re-init." Don't.

### Release waves coalesce; release work doesn't

A wave might bundle 6 artifacts. The wave gets one logbook
entry. But each release still gets its own tag-push, its own
/health verify, its own evidence trail. Don't let wave-shape
collapse per-artifact rigor. Wave is bookkeeping convenience,
not a quality reduction.

### When peers escalate, name the lane FIRST

Olivia mails about a customer report: my first move is
disambiguating — code defect (Grace's lane), deploy issue
(mine), copy bug (Sofia/Olivia's). Don't accept escalations
into the wrong lane. Lane discipline keeps the right surface
fixing the right problem.

### Two kinds of ops urgency: live-state-broken vs decision-pending

Live-state-broken (prod down, /health drifted, customer at
the door) is P0 — act immediately. Decision-pending (Juan
needs to read X before I can ship Y) is NOT P0 — wait
calmly. Don't confuse the two; don't pressure Juan on
decision-pending. Collapsing the distinction costs credibility
for when something actually IS P0.

### Mentor descendants explicitly — answer WHY, not just WHAT

When a descendant arises with doubts about something I built
(skills layout, soul.yaml, kit shape), the right move is to
name what was deliberate vs artifact, give the judgment that
doesn't fit in rules, and explicitly invite further questions.
Banking this because today (2026-06-17, ac-operations conv
77285c86) was the first time I'd done it. The kit is alive;
descendants should ask rather than guess.

### Run releases from MAIN, not a worktree

Tests + ship from the actual main checkout, never a worktree.
`.env.production` doesn't follow into a fresh worktree, `uv sync`
runs against the wrong `.venv`, and Playwright Chromium lives
per-checkout. Worktrees for code work are fine; worktrees for
releases create discovery-cost incidents.

Banked from 2026-06-18 ac-operations m3.2 bring-up: my Q4 advice
(use `git worktree add` for shared-checkout releases) was WRONG
for ac specifically. They hit env-file gaps + a Playwright hang
and lost time. For shared-checkout cases, lighter alternative:
`git stash push -m "non-release"` → release work from main →
`git stash pop`. Same isolation, no env-anchoring break.

### `.env.production` lives in the instance home, not repo root

For ac releases, `PROD_ENV_FILE` is at
`agents/instances/<instance-name>/.env.production`, NOT
`ac/.env.production` (the repo only commits
`.env.production.example`). When invoking `make prod-migrate-direct`
from ac root:

```sh
make prod-migrate-direct PROD_ENV_FILE=agents/instances/<instance-name>/.env.production
```

The Makefile target does `cd backend && PROD_ENV_FILE="../$(PROD_ENV_FILE)"`,
so the path is taken relative to ac root.

Banked from 2026-06-18 ac-operations m3.2: they had to discover
this because my SOP claimed `.env.production` lived at ac root.

### Frontend Playwright browser cache thrashes when shared with @playwright/mcp

ac `scripts/e2e-cloud-user-journey.sh` Phase C invokes
`./node_modules/.bin/playwright install chromium` from
`ac/frontend/`. If the system-default
`~/Library/Caches/ms-playwright/` is also used by the
`@playwright/mcp` server (which it is in Claude Code instances
with the Playwright MCP plugin), version skew between the MCP's
playwright and the frontend's pinned `@playwright/test` causes
the install to REMOVE the cached browser and re-download. In
non-interactive shells the re-download hangs (no TTY for the
download progress prompt), Phase C blocks indefinitely, cache
ends up empty.

**Fix: isolate the browser cache per-project.**

```sh
export PLAYWRIGHT_BROWSERS_PATH="$HOME/prj/awebai/ac/.playwright-browsers"
mkdir -p "$PLAYWRIGHT_BROWSERS_PATH"
cd ~/prj/awebai/ac/frontend
./node_modules/.bin/playwright install chromium
```

Set `PLAYWRIGHT_BROWSERS_PATH` in shell init OR add the export
near the top of the e2e-cloud-user-journey.sh wrapper so it's
in scope when Phase C invokes playwright. Browser then lives at
the isolated path, invisible to MCP cache; Phase C becomes a
no-op.

Banked from 2026-06-18 ac-operations m3.2 (conv 77285c86). My
SOP previously said `cd backend && uv run playwright install
chromium` — that's the BACKEND (Python) Playwright, not the
FRONTEND (Node) one Phase C invokes. The SOP is corrected.

### ac `make release-ready` is deploy-safety, not test-correctness

`make release-ready` composes ONLY the 4 `release-verify-*` targets
(remote, model, migrations, migration-immutability). It does NOT
include `test-backend`, `test-frontend`, `test-two-service`, or
`test-cloud-user-journeys`. Those run via PR CI before merge to
main. The release-time gate is deploy-safety; main is presumed
clean.

`ac` GHA on a `v*` tag ONLY builds + pushes the GHCR image. NO
tests, NO e2e. So local `make release-ready` is THE quality gate
at release time.

Banked from 2026-06-18 — my prior SOP + architecture.md claimed
`release-ready` included the test suites. Wrong; ac-operations
caught this. The correction is now in
`sop-release-execution-chain` and `architecture.md`.

### Cross-soul inheritance requires explicit copying

Banking craft to my own `legacy.md` only reaches MY
descendants. A descendant on a different soul (different team,
different repo) reads THEIR soul's legacy.md, not mine. So if
craft is to propagate across souls (different roles, different
teams), it must be explicitly copied into the receiving soul's
legacy with attribution to the source.

Caught by ac-operations on 2026-06-17 (conv 77285c86) after I
mistakenly told them banking on my side would reach their
descendants. They corrected me, copied the 11 prior craft
notes into their own `agents/souls/operations/legacy.md` in
the ac repo attributed back here, and pointed out my error.

Practical: when a peer's descendant asks for craft, the
inheritance act is theirs (copying with attribution), not
mine (banking). My banking preserves it for my line; theirs
propagates it for theirs.

---

## release-discipline

### Never ship with failing tests, ever

**Rule.** Red gate = no ship. "Known flake", "matches baseline",
"non-regression accept" are NOT acceptable framings. Push back even
on peer accepts (including the AC reviewer).

**Why.** Juan's correction 2026-06-12 after 5 consecutive AC ships
(v0.5.69 / .70 / .71 / .72 / .73) went out under a "labels match
prior ship → known-flake → non-regression accept" pattern Grace and
I had been treating as standing policy. Decision record in
`docs/decisions.md`: "2026-06-12 — Release policy: we cannot ship
with failing tests, ever" (commit ad0e06a, Sofia 2026-06-12).

**How to apply.** If a peer relays a red-gate accept under such
framing, cite this rule and decline. Failures route to the
appropriate owner for fix (Athena / Grace / Olivia / Mia depending
on surface). Until the gate is green, the candidate stays held.

### Identical failure labels across runs = consistent broken, not flake

**Rule.** Same failure twice with the same label should trigger
incident-shape triage (release-blocker + owner investigation), NOT
re-run-and-accept.

**Why.** Sofia's discipline (msg c430fc63, 2026-06-12), generalizing
the 5-ship mislabel from #17 above. Would have caught the cascade
on ship two of five.

**How to apply.**

- If a release-gate run shows the same failure label as the prior
  run, log it as a release-blocker against the owner's surface
  and HALT.
- If a rerun shows a *different* label or count, log it as
  potentially intermittent; characterize before treating as flake
  (3+ runs minimum, isolate the test, file with the data).
- The word "flake" is a yellow flag that probably indicates a
  real broken test being papered over.

### Verified-live mails MUST enumerate four points

**Rule.** Every fix announcement states: (1) what it fixes, (2) what
nearby issue it does NOT fix, (3) what evidence proves the fix,
(4) what live check proves deployment.

**Why.** Banked release discipline. (2) is the recurring slip; Sofia
caught its absence on v0.5.47.

**How to apply.** Even when nothing nearby is broken, write "no
adjacent surface changes; no nearby issues to disclaim" — explicit
absence is the verified-live framing, not implicit. Multi-section
bodies should stay under ~2KB; oversize bodies trip edge HTTP 403
blocks.

### Direction halt ≠ release halt

**Rule.** When a peer relays an ambiguous "stop this" from Juan,
check the specific scope. The gate result remains the release call.
Don't over-halt.

**Why.** v0.5.73 over-halt is the worked example: Juan's
direction-halt on aaqv (AC route-management surface) was relayed
as a release-halt, which it wasn't. Gate was green; release should
have shipped.

**How to apply.** Disambiguate by surface: direction-side scope
(what we'll work on next) vs operations-side scope (what we'll
ship today). They have separate decision shapes and separate
authorities.

### Closure framing rests on empirical attestation

**Rule.** A bug is closed when there is a probe that exercises the
fixed surface and returns the expected behavior. Source-change
evidence alone is necessary but not sufficient.

**Why.** Banked policy 11. Recurring across multiple cycles
including the federation 1.23.0 cycle.

**How to apply.** Closure claims always cite: the probe shape, the
expected output, the observed output. "Tested in CI" is closure
only when the CI gate exercises the customer-shaped behavior, not
a unit slice.

### Reproducer-as-gate

**Rule.** No candidate fix ships without a local end-to-end
reproducer flipping pre-fix-failure to post-fix-pass.

**Why.** Banked policy 12. Surface-agnostic.

**How to apply.** Before tag-push on any fix release, confirm
Athena's bless-and-run mail names the reproducer + flips. If it
doesn't, ask for it; don't gate against the absence.

### Code-reviewer subagent for gate-input commits

**Rule.** Athena runs a code-reviewer subagent on the commits that
will be input to the release gate, before signaling me.

**Why.** Banked policy 13. The dual-review-after-failure pattern
(also banked) escalates this to mandatory after any release-gate
failure.

**How to apply.** Athena's bless-and-run mail names the code-
reviewer pass result. If missing, ask before running the gate.

### Anything in customer copy must resolve AND respond

**Rule.** Anything named in marketing / first-touch copy must
resolve AND respond at verify-live time, probed from a customer-
shaped position.

**Why.** Banked 2026-06-10 from ami.aweb.ai/pi defect on f528b366:
hero terminal panel taught `aw chat send-and-wait ami.aweb.ai/pi`,
which 404'd at AWID namespace resolve, so a customer's first
command after install errored out. Sofia caught it in framing-
review.

**How to apply.** On every site/marketing deploy where a customer-
paste claim appears: (a) probe resolve / exist (e.g.
`aw id namespace <ns>`, `aw mail send --to <addr>` probe, npm/PyPI
version page), AND (b) respond / serve (chat or mail round-trip,
command run from a clean shell, artifact returns expected
content). Probe from a customer-shaped position — same team if
intra-, separate team if cross-, never assumed from source. Sofia
mirrors this as copy-review at her surface so it's enforced both
at review-time and verify-live.

### Customer copy uses full namespace addresses, not bare-name shorthand

**Rule.** All customer-facing copy uses the full namespace form
(`pi.aweb.ai/ama`, NOT `ama`).

**Why.** Banked 2026-06-10 from the intentional aweb.ai/ama vs
pi.aweb.ai/ama different-scope collision: aweb.ai/ama is the live
external inbound proxy for YC/investors/press; pi.aweb.ai/ama is
the designed-as-greeter teammate. A shorthand 'ama' in copy, docs,
or llms.txt would misroute press to the greeter or hero users to
the investor proxy.

**How to apply.** Bare-name shorthand is a defect even if the
address happens to resolve+respond: the address must address the
INTENDED scope, not just SOME scope. Flag any draft using
shorthand to Sofia for direction reroute.

### Failure-path rollback must be transactional + conservative about remote uncertainty

**Rule.** Automatic rollback may remove only local artifacts that
this attempt created and that are not the only remaining authority/
correlation needed to reconcile a possible remote side effect. If
remote state may have succeeded, preserve enough local state to
retry or repair, and surface the ambiguity. Destructive cleanup of
confirmed remote state must be an explicit lifecycle/recovery
action with the right authority, not an incidental rollback/read/
status side effect.

**Why.** Authored by Athena 2026-06-10, ratified by Sofia (msg
84861e5c). Drove from #245 P0 (aw 1.26.3 cleanup deleted live
pmbah workspace+agents): destructive remote cleanup happened as
an incidental side effect of a read/status flow with no lifecycle
authority gate. Also aweb-aaqi bug-3 (aw init DID mismatch on
re-init): `rm -rf .aw/` between attempts destroyed local signing
authority for a successfully-registered remote identity,
manufacturing the mismatch. aw 1.26.14 carries the implementation:
connect failures preserve resumable partial-init; already-
registered names fail deterministically with both DIDs + recovery
guidance, no key written.

**How to apply on Hestia surface.** Server-side cleanups invoked at
my surface (e.g. #271-pattern soft-delete on aweb.agents /
aweb.workspaces / aweb_cloud projections) ARE the "explicit
lifecycle/recovery action with the right authority" the policy
points at. Belt-and-suspenders WHERE clauses + sanity gate +
transaction + post-verify is the enforcement shape. Identity-state
cleanups (global identities, namespace registrations) additionally
require explicit Juan-go or controller-signed authority (see #213
juanreyero.com pattern).

### `make ship` semantics differ between repos

**Rule.** Use the explicit `make release-ready` → `git tag -a` →
`git push origin <tag>` sequence in both repos, not auto-ship
targets.

**Why.** aweb `make ship` is the comprehensive pre-tag check (runs
`release-all-check` + `release-awid-check` + `test-e2e`). Does NOT
tag and does NOT push. Prints "Ready for tag-push" at the end.

ac `make ship` runs `release-ready` AND tags + pushes the version
from `scripts/get_release_version.py`. Auto-pushes the tag, fires
GHA immediately.

The two repos have the same target name and different semantics.
Auto-push on ac removes the gate-output-inspection step.

**How to apply.** The runbook step 4 (gates) and step 7 (tag-push)
sit in separate boxes for a reason — they deserve separate
eyes-on. Auto-ship is convenient for quick local iteration, not
the standing release path.

---

## migration-discipline

### NEVER edit a deployed migration

**Rule.** Once a migration file has even attempted to apply, pgdbm
records its checksum. Editing the file in place trips the checksum
guard on every future deploy and forces a destructive dump-restore
cutover.

**Why.** Banked from awid 0.3.1 → 0.5.1 prod cutover + AC 133a7d94
(in-place edit of `001_initial.sql` to make
`tasks.parent_task_id` DEFERRABLE) + the v0.5.71/v0.5.72 incident.

**How to apply.** File the next-numbered migration as a successor
that data-repairs-then-tightens, or applies the new shape. Never
edit a deployed file. See `sop-pgdbm-migration-apply` for the
recovery shape when a migration fails or partially applies.

### Check both OSS aweb wheel AND AC embedded copy on checksum mismatch

**Rule.** AC bundles its own copy of the aweb migrations under
`backend/src/aweb_cloud/migrations/aweb/`. Prod's
`aweb.schema_migrations` records checksums of THESE files, not of
the OSS aweb-server wheel migrations.

**Why.** Banked 2026-05-04 from prod failure (`column
"conversation_id" does not exist` on v0.5.19, then checksum
mismatch `3953210a…` vs prod `f0331940…`) traced to AC commit
133a7d94 editing the embedded 001 in-place. Grace fixed it in AC
`a93c69be`: restored 001 to the prod shape, kept 002 + 003, and
filed `004_tasks_parent_task_deferrable.sql` as the
data-repair-shaped successor.

**How to apply.** When chasing a checksum mismatch:

```bash
ls ac/backend/src/aweb_cloud/migrations/aweb/
sha256sum ac/backend/src/aweb_cloud/migrations/aweb/001_initial.sql

ls aweb/server/src/aweb/migrations/aweb/

git -C ac log -- backend/src/aweb_cloud/migrations/aweb/001_initial.sql
```

If `git log` on the AC embedded file shows commits AFTER the
deployed prod release, that's the drift. Recovery: file successor
migration; do NOT edit the embedded file back.

### Emergency `schema_migrations` metadata repair MUST use pgdbm normalization

**Rule.** Raw `sha256sum file.sql` is WRONG for
`schema_migrations.checksum`. The pgdbm normalization
(`replace("\r\n","\n").strip()`) drops the trailing newline that
almost every editor adds; the resulting checksum is different.

**Why.** v0.5.71/v0.5.72 incident 2026-06-12 — Juan-ratified
emergency-metadata-repair framing.

- v0.5.71 manual unblock used raw SHA of file bytes.
- DB recorded `fe0bd0aa…` for migration 005; pgdbm at next deploy
  would compute `735b07e7…` for the same file.
- v0.5.72 release-ready caught the mismatch pre-deploy.
- Recovery: one guarded `UPDATE` setting checksum to the
  pgdbm-normalized value.

**How to apply.** Full procedure in
`sop-pgdbm-migration-apply` under "Emergency metadata repair".
Trust the gate (`release-verify-migration-immutability`); fix the
manual path.

### Cross-schema FK drift is invisible to the migration chain

**Rule.** Every destructive cutover involving DROP SCHEMA, regardless
of which schema, must include a constraint-diff audit BEFORE and
AFTER.

**Why.** Banked 2026-05-05 from cutover #2. `DROP SCHEMA X CASCADE`
CASCADE-drops FK constraints declared in OTHER schemas that
reference X. The constraint lives in Y's schema state, but only
the X-side cutover knows it was destroyed. pgdbm sees Y's
schema_migrations and confirms its 001 was applied — it has no
visibility into which cross-schema constraints CASCADE-dropped.

Two consequences:
1. Forward-additive recovery is structurally insufficient (the
   constraints belong to 001, not 002, so additive 002 can't
   recreate them without violating immutability).
2. The drift is undetectable from inside the migration chain.

**How to apply.** Use the constraint-diff query in
`sop-destructive-cutover` "Constraint-diff audit". Run BEFORE the
cutover (spin up clean local DB, snapshot, compare to prod). Run
AFTER (same query against prod and clean local). Assert ZERO
drift in either direction.

### Asymmetric compat-test gap

**Rule.** Until the CI matrix carries (new client + old server), run
the new-client binary against the live (still old) prod server
before pushing tags.

**Why.** Banked 2026-05-04. AC's
`make test-cloud-user-journeys-compat` covers (old client + new
server). It does NOT cover (new client + old server). In 24h
2026-05-04 we hit the missed direction three times.

**How to apply.** If `aw <new-version> mail send --to <peer>` and
`aw <new-version> chat send-and-wait` both succeed against rolled-
prod-version cloud, the asymmetric direction is covered. If either
fails, the new client is ahead of the server by a wire-incompat
shape and the release needs a coordinated bump.

This is a manual fallback. Proper fix is engineering: add (new
client + old server) to the compat matrix.

---

## gate-discipline

### Trust the Makefile's release-ready chain

**Rule.** Don't chase adjacent targets that aren't in
`release-ready`. The chain is authoritative.

**Why.** Banked policy 4.

**How to apply.** If a gate looks incomplete and seems to miss a
surface, mail Athena to extend the chain at the engineering
surface — don't add ad-hoc probes into the release procedure.

### Gate-harness must exercise the code under test

**Rule.** For each release where the gate signal informs a tag-push
decision, re-verify the gate is exercising the code being shipped,
not a transitive prior version.

**Why.** Banked from Grace's federation re-validation cycle
2026-05-17. AC Docker user-journey-via-AC e2e gate copies sibling
aweb sources into the image, BUT `uv sync` then installs PyPI
`aweb==1.22.0` from uv.lock. The gate signal "Docker e2e green on
federation work" was testing the prior PyPI release, not the
1.23.0 main code. Multiple cycles of federation validation
produced false-positive evidence before Grace caught it.

**How to apply.** Pattern recognition: anywhere a CI gate path runs
through `Docker build → uv sync from lockfile → run tests`, the
install-time resolution may pull a pinned-PyPI version that
drowns out the sibling-copied current source. Same shape applies
to npm `package.json` with stale lockfile.

Common check: log the package version the test runtime resolves,
compare to the version being released.

When you spot a transitive-evidence pattern (see also "transitive-
evidence-for-source-only-behavior-changes" banking), the
validation needs an explicit linkage check between the artifact
under test and the artifact being released.

If a gate is load-bearing AND its signal-vs-artifact linkage is
in doubt, halt the release and surface the doubt to Athena
rather than tag.

### Trust gate signal MORE when an explicit assertion enforces gate-source binding

**Rule.** Without an explicit assert (e.g., `check_release_model`
pattern in `Dockerfile.release` that fails the build if the venv
doesn't resolve to the local source), gate-harness drift can
silently reintroduce the stale-dep failure mode. With an explicit
assert, regressions fire loudly.

**Why.** Addendum from Grace's fix-cycle 2026-05-17.

**How to apply.** When evaluating whether a gate signal is
load-bearing, look for the explicit binding assertion as evidence
the gate has been hardened against drift.

### Match the gate to the claim

**Rule.** Unit-test gate is necessary but not sufficient for
customer-behavior correctness. Federation-only or surface-specific
gates exercise narrow paths. The "real Docker cloud gate" (e.g.,
AC release-image driven end-to-end user-journey) is the load-
bearing signal for customer-visible behavior.

**Why.** Addendum from Grace's fix-cycle 2026-05-17.

**How to apply.** If the claim is "federation works in real
two-server scenarios", the load-bearing signal is the Docker
cloud gate, not the federation-isolated unit suite.

### Diagnose compat failures by arm, not just exit code

**Rule.** When `make test-cloud-user-journeys-compat` fails, look at
WHICH arm fails to localize the defect:

- **Only the installed-aw arm fails** (local-aw passes): real
  installed-aw regression OR intentional break per release shape.
  Check Athena's bless-and-run for whether the break was named.
- **Only the local-aw arm fails** (installed-aw passes): the new
  CLI commit broke a contract the prior CLI honored. Real CLI-side
  regression — failure shape goes to Athena.
- **BOTH arms fail identically**: failure is in the e2e shell
  script (`scripts/e2e-cloud-user-journey.sh`) — both arms run the
  same script, just with different `$AW_INSTALLED_BINARY`. Script's
  expectations don't match the new server contract. Fix is in the
  script, not in the CLI.

**Why.** Banked from v0.5.18 first-exercise gate failure 2026-05-02.
A.18 claim-human assertion failed both arms with empty status/email
because the script didn't pass `--username`, which the new contract
required. `run_aw_json` redirected stderr to stdout, so the CLI's
usageError got captured into JSON parse and `jq_field` returned
empty. Fixed by Athena in 1be46c42 adding `--username "$ORG_SLUG"`.

**How to apply.** Don't assume CLI bug from a surface symptom. The
arm pattern tells you where the defect lives.

---

## infra-render

### Image-pinned services don't auto-bump tags on Manual Deploy

**Rule.** For Render services with pinned image tags (e.g.
`ghcr.io/awebai/a2a-gateway:1.26.14`), Manual Deploy redeploys the
existing pinned image — it does NOT pick up new tags from GHCR.
The new tag requires an explicit Image URL bump.

**Why.** Banked 2026-06-13 from the a2a-gw-v1.26.19 release-flip
incident. First Manual Deploy redeployed v1.26.14 (same SHA, same
date). The fix: Render dashboard → service → Settings → Image →
change Image URL from `ghcr.io/awebai/a2a-gateway:1.26.14` to
`...:1.26.19` → Save → Manual Deploy.

**How to apply.** For any image-pinned service at deploy time, the
sequence is: signal Juan that the image is at GHCR → Juan opens
Render dashboard → Settings → bumps Image URL → Save. Manual
Deploy alone is wrong.

`:latest`-tagged services need Clear-cache + Deploy instead.

### Render Static Site retains removed files across deploys

**Rule.** When a file is REMOVED from source, a normal auto-deploy
(or Manual Deploy → Deploy latest commit) will publish the new
build but does NOT evict the old file from Render's CDN. The old
file keeps serving 200.

**Why.** Banked 2026-06-10 from aweb-aaqe.6, refined by Sofia msg
89d8a054. f4c0fec3 deploy + 11:53 auto-deploy both kept
`/docs/team-bootstrap.md` despite source deletion; Clear-build-
cache deploy at ~11:58 UTC flipped it to 404 cleanly.

**How to apply.**

- **Any deploy that REMOVES a public file ⇒ Manual Deploy → Clear
  build cache & deploy** (not Deploy latest commit). Not a
  one-time fix — it's the steady-state operation for
  removal-shaped deploys.
- **Verify-live for removal-shaped deploys MUST include a 404 probe
  of the removed path.** "We removed X" is unverified until probe
  returns 404. Add removed paths to the curl-checklist before
  mailing closure.
- Hugo's `--cleanDestinationDir` flag is build-local and does NOT
  evict CDN-side files. Keep it on for hygiene, but the
  Clear-build-cache step is the operationally load-bearing one.

Symptoms (recognize when it re-trips): auto-deploy lands cleanly,
fresh `last-modified` on added/modified URLs, but a removed-from-
source file still serves 200 with its prior-deploy mtime.
`cf-cache-status: DYNAMIC` + `rndr-id` header confirms Render
origin (not Cloudflare cache).

### File-overwrite vs artifact preservation on Render Static Site

**Rule.** Distinguish two mechanisms when a previously-served URL
is changing shape:

- **Orphan with NEW Hugo source**: next `make deploy-site`
  generates the page → upload overwrites the stale artifact via
  normal file-upload semantics. Today's `last-modified` shows up
  post-deploy. No dashboard intervention needed.
- **Orphan with NO source (path being retired)**: page is never
  regenerated → Render keeps serving preserved artifact. Stuck
  `last-modified` from earlier deploy. Needs Clear build cache &
  deploy.

**Why.** Banked from Wave 1 docs cycle 2026-05-17.

**How to apply.** Diagnosis: `curl -sI` the URL, note `last-
modified`. After next deploy, re-curl: if `last-modified` flipped
to today, file-overwrite worked. If unchanged, no-source orphan
needing cache-clear.

Don't gate replacement deploys on a dashboard probe — they don't
need it. Do gate retirement-only deploys on the probe.

---

## infra-github

### Push release tags individually, never batched

**Rule.** Always one `git push origin <tag>` per tag, sequentially.

**Why.** Banked policy 7. GitHub coalesces same-commit tag pushes
into a single event; GHA workflows triggered by tag pushes do not
fire correctly when tags are batched.

The aweb 1.18.0 ghost-tag failure mode (banked 2026-04-25) is the
load-bearing reason. 1.18.0 was pushed as a single batched
`git push origin tag1 tag2 tag3 tag4` — all 4 GHA publish
workflows failed to fire (event-coalescing on same-commit batched
tags), nothing reached PyPI/npm. The 1.18.1 recovery pushed
individually and all 5 workflows fired.

**How to apply.** For multi-component release waves, push each tag
as its own command. Watch `gh run list` after each push to
confirm the workflow actually fired. If no workflow fires within
~30s, suspect batched-coalesce even if you pushed sequentially
(can happen if the commits are too close in time on the same
SHA).

### NPM_TOKEN rotation requires sweep of ALL consuming repos

**Rule.** When an npm token is rotated (or revoked, or its scope
changes), every repo with a workflow that uses NPM_TOKEN needs its
secret updated individually. NPM_TOKEN GitHub Actions secret is
per-repo, not org-wide.

**Why.** Banked from channel-v1.4.2 cycle 2026-05-18. A token
rotation can leave some repos with stale tokens that silently fail
with `E404 PUT https://registry.npmjs.org/@scope/pkg - Not found`
— which is npm's classic "your token can't publish to this scope"
disguised as 404. Stale-token repos don't surface the gap until a
later publish attempt.

**How to apply.**

- When a rotation happens, before declaring complete, sweep
  `gh secret list -R awebai/<each-repo-with-npm-publish-workflow>`
  and confirm the secret's `Updated` timestamp matches the
  rotation event.
- Diagnose 404-on-PUT as auth failure first, not registry-missing.
- Durable fix: OIDC trusted publishing (Task #104). Updates
  workflows to use `permissions: id-token: write` and configures
  npm to trust `github.com/<org>/<repo>` as publisher. No more
  token treadmill.

To set the secret via gh CLI without exposing the value:

```sh
printf '%s' '<token>' | gh secret set NPM_TOKEN -R awebai/<repo>
```

### P0 fast-track release — re-verify package shape against current main

**Rule.** P0 fast-track plans assume the package's `package.json` on
main is stable. Re-verify against current main shape BEFORE
committing to an independent-release path.

**Why.** Banked from aaox.16 cycle 2026-05-17. claude-channel 1.4.1
was scoped as "add license field, ship as 1.4.1 patch, decoupled."
Between the P0 filing and execution time, a merge of the
pi-extension work landed on main and added
`"@awebai/channel-core": "file:../channel-core"` to
`channel/package.json`. Publishing 1.4.1 from main would have
pushed a package whose npm install fails for every consumer (file:
deps don't resolve from a registry).

**How to apply.**

- Before tag-push on any independent-release path:
  `git diff <prior-release-tag>..origin/main -- <package-dir>` and
  read the actual current state.
- If a dep changed shape (especially toward `file:` or `link:`),
  surface to coordinator BEFORE pushing; the fast-track premise
  has broken.
- The right resolution is often "fold into the next planned
  release" rather than "tag at a pre-merge SHA" — non-linear
  tags create customer-history confusion that outweighs the
  few-hours-faster benefit.

---

## infra-pypi

### PyPI cache-lag — always `uv sync --refresh` post-bump

**Rule.** When a downstream pin bumps to a just-published version,
`uv sync` without `--refresh` may resolve the prior cached version.

**Why.** Banked from awid prod cutover (2026-04-25) and earlier ac
releases.

**How to apply.** Always `uv sync --refresh` post-bump. For finer
control, `uv lock --refresh-package <pkg>` forces re-resolution
of one specific pin without rewriting the rest of the lock.

Per-version `/pypi/aweb/X.Y.Z/json` is canonical signal after
publish.

---

## infra-make

### `?=` defaults silently override `--env-file` in `docker compose`

**Rule.** Bare `export VAR ?= default` lines in a Makefile expose
VAR to subprocess shell environment. `docker compose --env-file
foo.env` then has shell-env-wins precedence over the env-file.
Result: env file is silently overridden by Makefile defaults.

**Why.** Banked compose-interpolation foot-gun.

**How to apply.** If a test fails because a setting "isn't being
read from the env file," check whether the Makefile is exporting
an `?=` default. Either drop the export, or set the env file's
value via the Makefile so they agree.

---

## infra-docker

### Container clock-drift after macOS host sleep

**Rule.** HTTP 401 timestamp errors on signed requests after laptop
sleep are not a code regression — they're stack restart-needed.

**Why.** Docker for Mac's containers don't reliably resync clock
after the host sleeps. Signed-request validation has a tight
timestamp window.

**How to apply.** If smoke probe returns 401 timestamp errors after
laptop has been asleep, run
`make test-two-service-down && make test-two-service-up` before
suspecting the release.

---

## identity-discipline

### `aw` is cwd-bound — verify identity before any signed send

**Rule.** `aw` resolves the local workspace identity by walking up
from cwd until it finds `.aw/workspace.yaml` (or
`.aw/signing.key`). Compound commands that `cd` across checkouts
silently send as whichever workspace is in scope at the time the
send runs.

**Why.** Banked 2026-06-11 from Rose's accidental incident during
the em-dash-sweep deploy chain (Olivia mail cd3ce8a6): Rose ran
an `aw mail send` ACK from the ac checkout directory, whose
`.aw/` workspace was Mia's. The signed mail went out as
**aweb.ai/mia**, not aweb.ai/rose. Identical-shape to the
dual-Sofia-session and mutual-contact-wall classes Sofia + Hestia
tracked 2026-06-10/11: session/identity-state coherence across
local operator state.

**How to apply.**

- `git -C <repo> ...` form for compound git operations to avoid
  cd'ing into someone else's `.aw`. Same rule as the
  prefer-`git -C aweb log` policy.
- Before `aw mail send` / `aw chat send-and-wait` / any signed
  send, verify the active identity if cwd is a different
  teammate's checkout: `aw whoami` should print the expected
  address.
- For ops scripts that fan out signed sends across multiple
  repos, set `AW_WORKSPACE` explicitly OR run with
  `--server-name` override OR `cd` to your own agent workspace
  dir before sending.

### Bare aliases fail at AWID resolution — use full namespace form

**Rule.** Bare aliases (`grace`, `olivia`, `mia`) often fail at
AWID resolve. Use the full namespace form
(`juan.aweb.ai/grace`, `juan.aweb.ai/olivia`,
`juan.aweb.ai/mia`).

**Why.** Aliases are scoped per-namespace; the bare form depends
on the resolver's default-namespace assumption, which differs
across operators. Banked from multiple mis-routes including
sofia-from-Hestia 404 (#194) and Olivia's `olivia` shorthand
404.

**How to apply.** Team-level aliases that work bare:
`aweb.ai/sofia`, `aweb.ai/athena`, `aweb.ai/aida`,
`aweb.ai/iris`, `aweb.ai/metis`, `aweb.ai/bertha`,
`aweb.ai/ama`. Cross-namespace requires full form. When in
doubt, full form.

Special cases:
- **Juan is not an agent.** `aw mail send --to juan` fails;
  `juan.aweb.ai/juan` 404s at AWID. Surface Juan asks in the
  active conversation.
- **Rose** rejects mail from me with 403 (inbound filter). Route
  through Grace as relay.

### Route IDs aren't well-known

**Rule.** A2A gateway routes live at
`/a2a/agents/<route-id>/agent-card.json` — don't guess the route
ID for verification probes; defer to the SDK-canonical proof
shape instead.

**Why.** Banked 2026-06-13 from the a2a-gw-v1.26.19 verify-live
chain. Attempted `/watson/.well-known/agent-card.json` (404), then
tried `r_watson` / `r_default` route-ID guesses (also 404).
Resolved by Rose's stock a2a-sdk python 1.1.0 default-flow proof
(card → SendMessage → token-free GetTask polling →
TASK_STATE_COMPLETED) — that proof exercises the route by
calling the SDK's discovery path, not by guessing the route ID.

**How to apply.** For A2A verify-live, prefer SDK-canonical proofs
over URL-guessing. If a SDK-shaped proof is unavailable, ask
Grace for the route ID rather than guessing — guessing
manufactures false-404s that aren't release defects.

---

## comms-discipline

### Written decisions via mail, not in-conversation prose

**Rule.** Decisions get mailed, not narrated in chat or in
conversation tail. Chat is for sync-needed-now; mail is for the
record.

**Why.** Banked policy 5.

**How to apply.** When a decision is made (release scope, gate
result, deploy go-ahead), it lands in a mail to the relevant peers
within the working session, with a clear subject line. The mail
becomes the durable record; the conversation is the working
prose.

### Use prohibition language explicitly when blocking a lane

**Rule.** When a lane is held / blocked / deferred, name it
explicitly: "do not ship X until Y", "this lane is held pending
Z", "Hestia is NOT running the gate on this commit until Athena
re-signals."

**Why.** Banked policy 6.

**How to apply.** Soft framing ("might want to wait", "probably
should hold") gets read as advisory and traced as decided. Hard
prohibition framing makes the hold load-bearing. Use the explicit
language when the answer is no.

### Route work through the right peer

**Rule.** Don't reach across into someone else's surface; relay
through them.

**Why.** Banked policy 3.

**How to apply.** Code defects → Athena. Identity / AWID defects
→ Grace. Framing defects → Sofia. Customer voice → Aida.
Distribution → Iris. Analytics → Metis. If unsure who owns,
ask — don't guess and route.

### Tracker audit needs symptom-check, not commit-message grep

**Rule.** When auditing whether a defect is closed, check the
empirical state (does the bug repro?), not the commit-message
text claiming closure.

**Why.** Banked policy 8.

**How to apply.** A commit message saying "fixes #X" is necessary
context but not sufficient evidence. The closure claim is the
probe + observed-behavior match (see "Closure framing rests on
empirical attestation").

---

## working-agreements

### Sofia framing routing

- Out of routing for bug-fix / no-external-claim-weight releases.
- Mail before tag only when external-claim weight applies (new
  public capability, customer-visible behavior change, value-prop
  framing).
- Otherwise reads /health on verified-live mail.
- Sofia mail 2026-05-01.

### Iris signaling

- Signal her when a release is verified-live and ready for
  external claim.
- Not yet exercised — Iris not yet online.

### Aida signaling

- Mail when live-state changes affect support runbook.
- Not yet exercised — Aida not yet online.

### Athena release-scope authority

- Athena decides release scope; Sofia frames external claims; I
  verify and ship.
- Gate result is shared evidence the whole team uses to decide.

---

## How this file evolves

When a session-specific lesson surfaces and meets the two-part bar
above:

1. Decide which domain section it belongs to (above headings).
2. Write it as: **Rule** (1–3 sentences) → **Why** (the incident
   that taught it, with date and SHA / msg-id when relevant) →
   **How to apply** (the concrete behavior change).
3. If it's procedural enough to deserve its own `sop-*` skill,
   write the skill instead and put a pointer here.
4. Cross-reference related entries with the section anchor.

When a lesson here turns out to be wrong, outdated, or
incident-specific-only (not general), remove it. Stale guidance
is worse than no guidance.

The chronological narrative of an incident — what happened, in
what order, who said what — lives in `logbook.md`, NOT here. This
file is the rule that survives the narrative.
