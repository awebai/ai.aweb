# Operations Runbook

Hestia owns this. The runbook encodes how to carry a release across
the build/ship boundary without engineer assistance: pre-flight,
gates, tag, watch CI/CD, verify live, post evidence.

## Status of this document

**Seeded 2026-05-01 from prior-knowledge sources** — the banked
release decisions in `../../docs/decisions.md`, the Makefile survey
on this same day, and the standing release-discipline policies
(banked through 2026-04-26).

**Not yet validated by Hestia running the chain solo.** The first
end-to-end exercise (under live identity, without engineer
walk-through) is pending. Sections marked **[unvalidated]** mean the
shape comes from prior decisions but the runbook has not yet seen me
execute them. After the first exercise, those markers come off and
real failure-mode notes get added.

When validation discovers a gap, the runbook updates. When Athena
adds a new gate, the runbook updates. When a banked memory adds an
operational lesson, the runbook updates.

## What gets you to a release candidate (input)

A release candidate enters my surface as a mail from Athena:

- Subject: `release-handoff: <repo> <version-target>` (or shape).
- Body names: target repo (aweb / ac), expected SHA of clean main,
  release-notes draft, code-reviewer-subagent pass result on the
  gate-input commits (banked policy 13).

Until that mail lands, no candidate exists from my side. I do NOT
self-spawn a release on a bump commit I find sitting on main —
that would skip the build/ship boundary and decouple the gate from
engineering's signal.

**[unvalidated]** Today's pattern (genesis-day v0.5.13–v0.5.16) had
Mia in the dev team tagging directly without an Athena handoff.
The shape of "what does an Athena release-handoff mail look like"
is therefore prior-knowledge from the v0.5.4 / v0.5.5 / v0.5.6
era; the new shape under the dev-team / Athena-bridges arrangement
will surface on the first real handoff and this section updates.

## The chain (step-by-step)

### 1. Pre-bump check

```sh
git -C aweb pull   # or git -C ac pull
git -C <repo> rev-parse HEAD
```

Confirm head matches the SHA in Athena's handoff mail. If it
doesn't, stop and ask — never gate against a different commit than
what was reviewed.

### 2. Bump

The bump itself is a single commit on the target repo:

- `pyproject.toml`: version field bumped to the target version.
- `uv.lock`: regenerated minor (the next step's `uv sync` will
  produce the canonical lock).

For aweb (multi-component: server, awid, awid-service, channel,
cli), see "aweb-specific" below — multiple version fields move in
lockstep or independently per the release shape.

For ac (unified backend version), only `backend/pyproject.toml`
moves.

**[unvalidated]** Whether the bump commit is authored by Athena,
Mia, or me-as-Hestia — TBD by the first real handoff. Today's
bumps were Mia's. Prior decisions show CTO (Randy) authored bumps.
Not load-bearing for the gate run; load-bearing for attribution
in the verified-live mail.

### 3. Sync

```sh
uv sync --refresh   # ac
# or
uv sync --refresh   # aweb (run from each component's pyproject root)
```

`--refresh` matters. If the bump pins a downstream that was just
published to PyPI, the local cache may still hold the prior version.
Banked from awid prod cutover (2026-04-25) and earlier ac releases:
the PyPI cache-lag window can mask a stale resolution. Always
`--refresh` post-bump.

### 4. Gates (release-ready)

#### ac

```sh
cd ac && make release-ready
```

Composes (per `ac/Makefile`, post-commit `24cb7c68`):

- `release-verify-remote` — confirms remote state matches expectation.
- `release-verify-model` — model-side verification.
- `release-verify-migrations` — migrations are forward-only, ordered,
  checksum-clean.
- `test-backend` — pytest suite. ~1250 selected as of v0.5.17 (1263
  collected, 13 deselected).
- `test-frontend` — vitest suite. ~96 tests as of v0.5.5; ~25 files.
- `test-two-service` — Docker two-service stack (cloud + awid).
  ~9–10 tests depending on era.
- `test-cloud-user-journeys` — local-aw arm only as of `24cb7c68`
  (the chain previously composed local-aw + installed-aw; the
  installed-aw arm moved to the explicit `test-cloud-user-journeys-compat`
  target, ~233s saving on the default chain). Mia's per-Mia mail
  reports release-ready total of 244.56s under the new shape.

All must be green. Per banked policy 4, trust the Makefile's chain;
do not chase adjacent targets that aren't in `release-ready`.

##### When to also run `make test-cloud-user-journeys-compat`

Compat covers the installed-aw arm — i.e., it exercises ac against
the published `aw` package on PyPI rather than the sibling
checkout. The default chain skips it for speed; invoke it
explicitly when the release shape risks breaking installed users.

**[unvalidated — Athena's starting policy 2026-05-02; will tighten
when Mia confirms]**

Always run compat when:

- The release changes any `aweb` ↔ `ac` endpoint contract
  (response shape, required fields, status semantics).
- The release changes auth / cert / identity flows.
- The release ships ac without bumping the `aweb` pin.

Skip compat when:

- Pure ac-internal changes (admin tooling, frontend layout,
  internal refactor with no contract shift).
- Releases that bump the `aweb` pin AND publish a matching `aw`
  on npm/PyPI in the same wave (users upgrade together).

When in doubt, run compat. The cost is ~4 min added (4 default + 4
compat = 8 min for compat-flagged releases vs 4 min for compat-skip
releases). Worth it when the release shape can break installed-aw
users.

#### aweb

```sh
cd aweb && make release-all-check
```

aweb is multi-component. The check target verifies all components
are release-ready. Per-component check / tag / push targets exist
separately:

- `release-server-check` / `-tag` / `-push`
- `release-cli-tag` / `-push`
- `release-awid-check` / `-tag` / `-push` / `-pypi-tag` / `-pypi-push`
- `release-channel-check` / `-tag` / `-push`

`release-all-check` composes the check targets across all
components. `release-all-tag` and `release-all-push` exist for full
multi-component releases (aala epic shape).

The gate to run as part of release-ready for aweb is `make test-e2e`
(banked 2026-04-22 standing policy: "no release of anything is cut
before the full e2e user journey test passes"). `make test`
composes `test-server` + `test-awid` + `test-cli` + `test-channel`.

**[unvalidated]** Whether `make release-all-check` already calls
`make test-e2e` internally or whether it must be run separately.
First aweb release exercise resolves this.

### 5. SOT analysis (when needed)

For releases that touch protocol surface, schema, or trust model,
walk:

- `aweb-sot.md` (in `aweb/docs/`) — protocol invariants
- `awid-sot.md` (in `aweb/docs/`) — registry invariants
- `trust-model.md` (in `aweb/docs/`) — trust + identity invariants
- `ac/sot.md` (in `ac/docs/`) — cloud-side invariants

If the release shape doesn't touch protocol/schema/trust (e.g.,
v0.5.17 layout-containment fix), SOT analysis is not needed.

When drift is found between the release content and the SOT docs,
mail Athena and work the fix together — code change lands with her;
gate re-runs with me.

### 6. Sofia framing review (only when needed)

**Default: skip.** Bug-fix releases without external-claim weight
tag through the gate chain without Sofia review. Confirmed in
Sofia's 2026-05-01 mail: "Bug-fix releases don't need Sofia in the
loop — tag through your gate chain. If at any point a release
carries external-claim weight (new public capability, behavior
change customers will notice, anything that affects value-prop
framing), mail me before tag; otherwise I read /health when you
post verified-live."

**Mail Sofia before tag when:** new public capability, customer-
visible behavior change, value-prop framing implications. Subject
shape: `framing-review: <release-target>`. Body: release-notes
draft + what's load-bearing for external claim.

### 7. Tag and push (per-tag, never batched)

Banked policy 7. GitHub coalesces same-commit tag pushes into a
single event; GHA workflows triggered by tag pushes do not fire
correctly when tags are batched. Always one `git push origin <tag>`
per tag, sequentially.

```sh
git tag -a vX.Y.Z -m "release: vX.Y.Z, <one-line summary>"
git push origin vX.Y.Z
```

For aweb multi-component releases, push each tag separately (in any
order — what matters is each push is its own event):

```sh
git push origin server-vX.Y.Z
git push origin aw-vX.Y.Z
git push origin awid-vX.Y.Z
git push origin awid-service-vX.Y.Z
# and channel-v* if it moved
```

The aweb 1.18.0 ghost-tag failure mode (banked 2026-04-25) is the
load-bearing reason for this rule. 1.18.0 was pushed as a single
batched `git push origin tag1 tag2 tag3 tag4` — all 4 GHA publish
workflows failed to fire (event-coalescing on same-commit batched
tags), nothing reached PyPI/npm. The 1.18.1 recovery pushed
individually and all 5 workflows fired.

### 8. Watch CI/CD

After each tag push, the corresponding GHA workflow fires. For ac,
that's the cloud CI/CD run (image build + GHCR publish + auto-deploy
to app.aweb.ai). For aweb, that's per-component (PyPI for server /
cli / awid / awid-service; npm for channel).

Use `gh run list` and `gh run view <id> --log` (or the GHA web UI)
to watch the run. Confirm it fired (banked failure: workflow
silently doesn't fire when tag push is batched).

### 9. Verify live

**[partly validated tonight via /health probe]** GHA green ≠ live.
Package published ≠ live. Tag pushed ≠ live. The release is live
when the deployed service reports the new version AND the changed
surface behaves correctly.

#### Step 9a: /health version match

```sh
curl -sS https://app.aweb.ai/health | jq .   # ac
curl -sS https://api.awid.ai/health | jq .   # awid
```

Assert:

- `release_tag` matches the tag you just pushed (ac only — aweb's
  surface is the OSS package, no `/health` endpoint per repo).
- `git_sha` matches the bump commit (ac).
- `aweb_version` and `awid_service_version` match the pin in
  `backend/pyproject.toml` post-bump.

If any field doesn't match, the deploy hasn't rolled — wait, then
re-check. If after a reasonable window (~10 min) the fields still
don't match and GHA shows green, troubleshoot the deploy infra.

#### Step 9b: Smoke probe of the changed surface

For each release, exercise what actually changed:

- **New endpoint**: curl the endpoint with a real-shape request.
- **New CLI behavior**: run the command against a clean workspace.
- **UI change**: browser probe (Playwright MCP or manual). Banked
  policy 10. v0.5.17 (layout-containment) is exactly this shape —
  open the Add-Existing dialog and confirm the long fetch-cert
  command scrolls horizontally inside the modal instead of widening
  it.

#### Step 9c: Banked failure modes to check

- **Docker container clock-drift after macOS host sleep**: HTTP 401
  timestamp-skew on signed requests after laptop sleep. Resolved by
  `make test-two-service-down && make test-two-service-up` — not a
  code regression, just stack restart. Banked symptom; if smoke
  probe returns 401 timestamp errors, restart the local stack
  before suspecting the release.

### 10. Post verified-live mail

Compose the release post mail:

```
To: athena, sofia, juan
Subject: verified-live: <repo> <version> <one-line summary>
Body:
  - What it fixes (and what nearby issue it does NOT fix)
  - What evidence proves the fix
  - What live check proves deployment (paste /health output snippet
    + smoke-probe result + browser-probe result for UI)
  - GHA run reference (workflow id + URL)
```

Banked rule (release discipline): every fix announcement states
(1) what it fixes, (2) what nearby issue it does NOT fix, (3) what
evidence proves the fix, (4) what live check proves deployment.

Also mail Iris when the release carries an external-claim
opportunity (new capability ready for distribution). Mail Aida when
the release changes a customer-facing surface that affects the
runbook.

## Verified-live probe pattern (compact reference)

| Surface          | Match field on /health         | Smoke probe                              |
|------------------|--------------------------------|------------------------------------------|
| ac (cloud)       | `release_tag`, `git_sha`       | curl the changed endpoint or browser-probe the UI |
| aweb-server      | n/a (OSS — PyPI publish check) | `pip install` + import smoke             |
| aw CLI           | n/a (PyPI publish check)       | `aw --version` + smoke command           |
| awid-service     | api.awid.ai/health `version`   | endpoint smoke against api.awid.ai       |
| channel          | n/a (npm publish check)        | `npm install` smoke                      |

## Foot-guns and known failure modes

### PyPI cache-lag

When a downstream pin bumps to a just-published version, `uv sync`
without `--refresh` may resolve the prior cached version. Always
`uv sync --refresh` post-bump.

### make-export compose-interpolation

Bare `export VAR ?= default` lines in a Makefile expose VAR to
subprocess shell environment. `docker compose --env-file foo.env`
then has shell-env-wins precedence over the env-file. Result: env
file is silently overridden by Makefile defaults. If a test fails
because a setting "isn't being read from the env file," check
whether the Makefile is exporting an `?=` default.

### per-tag-not-batched push

See step 7 above. Banked from aweb 1.18.0 ghost-tag.

### Docker container clock-drift after macOS host sleep

See step 9c. Banked symptom: HTTP 401 timestamp errors on signed
requests after laptop sleep. Restart the stack.

### Migration file editing

When a project uses a single consolidated migration file (awid uses
this shape — `001_registry.sql`), every additive schema change goes
in a NEW ordered file (`002_<name>.sql`, `003_<name>.sql`, …).
Editing the existing consolidated file in place trips pgdbm's
checksum guard and forces a destructive dump-restore cutover.
Banked from awid 0.3.1 → 0.5.1 prod cutover.

### `make ship` short-circuits approval

`make ship` (in both aweb and ac) is the auto-tag-and-push target.
It bypasses the manual approval / per-tag-discipline step. Per
banked release protocol: do NOT use `make ship` for production
releases. Tag manually with `git tag -a` and push individually with
`git push origin <tag>`.

## Standing policies (banked through 2026-04-26, Hestia enforces)

1. Release gate = full e2e + SOT + peer-review (mailed)
2. Review via shared working tree (not chat-pasted diffs)
3. Route work through the right peer
4. Trust the Makefile's release-ready chain
5. Written decisions via mail (not in-conversation prose)
6. Use prohibition language explicitly when blocking a lane
7. Push release tags individually, never batched
8. Tracker audit needs symptom-check, not commit-message grep
9. Published artifact ≠ deployed service
10. Browser-verify UI-surface releases
11. Closure framing rests on empirical attestation
12. Reproducer-as-gate (no candidate fix ships without local
    end-to-end reproducer flipping pre-fix-failure to
    post-fix-pass) — surface-agnostic
13. Code-reviewer subagent for gate-input commits (Athena runs this
    before signaling Hestia)

## Working-agreement bank (peer-confirmed)

- **Sofia**: out of routing for bug-fix / no-external-claim-weight
  releases. Mail before tag only when external-claim weight applies
  (new public capability, customer-visible behavior change, value-
  prop framing). Otherwise reads /health on verified-live mail.
  (Sofia mail, 2026-05-01.)
- **Iris**: signal her when a release is verified-live and ready
  for external claim. Not yet exercised — Iris not yet online.
- **Aida**: mail when live-state changes affect support runbook.
  Not yet exercised — Aida not yet online.

## Open gaps in this runbook (collect on every exercise)

- First end-to-end exercise pending. The actual shape of an
  Athena release-handoff mail under the new role model needs to
  surface on first real handoff.
- Local reproducer state for the Add-Existing-Identity surface is
  unknown — pending Athena's read.
- Publishing-path timing (the 30+-min cycle Sofia flagged) needs
  to be timed on first ac release and decomposed (GHA build
  versus PyPI propagation versus image build versus deploy
  rollout versus health-check wait).
- Test-suite triage — which targets compose to the ~20-min run,
  which are critical-path for changes of various shapes — needs a
  data pass.
