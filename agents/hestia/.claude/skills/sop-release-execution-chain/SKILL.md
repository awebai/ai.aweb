---
name: sop-release-execution-chain
description: Carry a release from Athena's bless-and-run mail across the build/ship boundary to verified-live evidence. Invoke when a release-handoff mail lands in inbox naming a target repo, target SHA, and release-notes draft.
---

# Release execution chain

The 10-step chain from Athena's bless-and-run mail to verified-live
mail. Each step is mandatory; skipping is failure unless explicitly
named.

## Trigger

A mail from Athena (or `aweb.ai/athena`) with:

- Subject: `Bless-and-run: <one-line change summary> (<repos involved>)`
  or `release-handoff: <repo> <version-target>`.
- Body names: target repo (aweb / ac), expected SHA of clean main,
  release-notes draft, code-reviewer-subagent pass result (banked
  policy 13).

Until that mail lands, no candidate exists from my side. I do NOT
self-spawn a release on a bump commit found sitting on main — that
would skip the build/ship boundary.

## Bless-and-run mail shape (what to read)

- **Repos and commits**: each repo + commit SHA, one-line description
  per commit. "Already on main" if pushed; flag otherwise.
- **Cross-repo dependency**: which artifacts move together, which
  ship independently, which decisions she leaves to me.
- **Compat-test invocation guidance**: which compat scope applies.
- **Release notes draft**: closes / does NOT close / code evidence
  (key commits + tests added) / affects / live verification (smoke
  probe + browser-verify if UI surface).
- **Failure-mode pre-warning**: any expected gate output that should
  be treated as "intentional break observed correctly".
- **Bless-and-run signal**: explicit "you own the release from here."

I confirm gate-run readiness, run the chain. Mail back the failure
shape if anything goes red; mail back verified-live when the release
is on `/health`.

## Step 1 — Pre-bump check

```sh
git -C aweb pull   # or git -C ac pull
git -C <repo> rev-parse HEAD
```

Confirm head matches the SHA in Athena's handoff mail. If it
doesn't, **stop and ask** — never gate against a different commit
than what was reviewed.

## Step 2 — Bump

Single commit on the target repo:

- `pyproject.toml`: version field bumped to target.
- `uv.lock`: regenerated.

For aweb multi-component (server, awid, awid-service, channel, cli),
multiple version fields move per the release shape.

For ac, only `backend/pyproject.toml` moves.

## Step 3 — Sync

```sh
uv sync --refresh   # ac
uv sync --refresh   # aweb (from each component's pyproject root)
```

`--refresh` is load-bearing. PyPI cache-lag can mask a stale
resolution after a downstream pin bumps to a just-published version.

## Step 4 — Gates (release-ready)

### ac

```sh
cd ac && make release-ready
```

See `architecture.md` for the chain composition. All must be green.
**Never ship with failing tests, ever** (constitution).

**Also run `make test-cloud-user-journeys-compat` when any apply:**

- A SQL migration touches a table read or written by aweb-server
  endpoints.
- An API endpoint contract changes (response shape, required
  fields, status semantics).
- Middleware / request-routing / header-validation / path-routing
  changes.
- Auth / cert / identity flow changes.
- The `aweb` pin in `ac/backend/pyproject.toml` is bumped.

**Skip compat only when both apply:**

- Changes are strictly internal (admin tooling refactor, frontend
  layout / copy, internal refactor with NO SQL migration AND NO API
  change AND NO middleware/routing change).
- AND the `aweb` pin is unchanged.

When in doubt, run compat. ~58s isolated; cheap insurance against
installed-aw regressions.

### aweb

```sh
cd aweb && make ship
```

`make ship` is the canonical comprehensive pre-tag-push gate. Does
NOT push — prints "Ready for tag-push" at the end.

Per banked discipline: **do NOT substitute `make test` alone.**
1.18.3–1.18.6 each ran `make test` instead of the canonical gate;
GHA caught the downstream failures but the local gate is supposed
to be authoritative before tag-push.

## Step 5 — SOT analysis (when needed)

For releases that touch protocol surface, schema, or trust model,
walk:

- `aweb-sot.md` (in `aweb/docs/`) — protocol invariants
- `awid-sot.md` (in `aweb/docs/`) — registry invariants
- `trust-model.md` (in `aweb/docs/`) — trust + identity invariants
- `ac/sot.md` (in `ac/docs/`) — cloud-side invariants

If the release shape doesn't touch protocol/schema/trust, SOT
analysis is not needed.

When drift is found, mail Athena and work the fix together — code
change lands with her; gate re-runs with me.

## Step 6 — Sofia framing review (only when needed)

**Default: skip.** Bug-fix releases without external-claim weight
tag through the gate chain without Sofia review.

**Mail Sofia before tag when:** new public capability, customer-
visible behavior change, value-prop framing implications.

Subject shape: `framing-review: <release-target>`. Body: release-
notes draft + what's load-bearing for external claim.

## Step 7 — Tag and push (per-tag, never batched)

**Banked policy 7.** GitHub coalesces same-commit tag pushes into a
single event; GHA workflows triggered by tag pushes do NOT fire
correctly when tags are batched. Always one `git push origin <tag>`
per tag, sequentially.

```sh
git tag -a vX.Y.Z -m "release: vX.Y.Z, <one-line summary>"
git push origin vX.Y.Z
```

For aweb multi-component releases, push each tag separately (any
order — what matters is each push is its own event):

```sh
git push origin server-vX.Y.Z
git push origin aw-vX.Y.Z
git push origin awid-vX.Y.Z
git push origin awid-service-vX.Y.Z
# and channel-v* if it moved
```

See `legacy.md` infra-github for the aweb 1.18.0 ghost-tag
incident that drove this rule.

## Step 8 — Watch CI/CD and signal Juan for the deploy step

After each tag push, the corresponding GHA workflow fires. Use
`gh run list --repo awebai/<repo> --limit 5` and
`gh run view <id> --log` (or the GHA web UI) to watch.

**Confirm it fired** — banked failure: workflow silently doesn't
fire when tag push is batched.

**Docker-image deploys are MANUAL.** Applies to:

- ac (`vX.Y.Z` → GHCR → live at `app.aweb.ai`)
- awid registry (`awid-vX.Y.Z` → GHCR → live at `api.awid.ai`)
- a2a-gateway (`a2a-gw-vX.Y.Z` → GHCR → live at `a2a.aweb.ai`)

Render does NOT auto-deploy from GHCR. When the GHA build completes
and the image is at GHCR, signal Juan:

> "<service> v<version> image at GHCR — ready to deploy when you
> are."

Then wait. Do not attempt to automate the deploy.

**Image-pinned services need Image URL bump**, not Manual Deploy
alone. See `legacy.md` infra-render for the a2a-gateway Manual
Deploy incident. The pattern:

> Render dashboard → service → Settings → Image URL → bump
> `ghcr.io/awebai/<image>:<old-version>` → `<new-version>` → Save

**PyPI / npm / GitHub Releases publishes don't have a manual deploy
step** — once GHA finishes, the artifact is "live" in the sense of
available to consumers. Remaining wait is PyPI/npm propagation.

## Step 9 — Verify live

GHA green ≠ live. Package published ≠ live. Tag pushed ≠ live.
Image at GHCR ≠ live. **Live = deployed service reports the new
version AND the changed surface behaves correctly.**

### Step 9a — /health version match

```sh
curl -sS https://app.aweb.ai/health | jq .   # ac
curl -sS https://api.awid.ai/health | jq .   # awid
curl -sS https://a2a.aweb.ai/health | jq .   # a2a-gateway
```

Assert per `architecture.md` "Live-state endpoints" table.

If any field doesn't match, Juan hasn't deployed yet (or the
deploy is still rolling). Wait, re-check. If GHA is green and
the image is at GHCR but /health doesn't show the new version
after Juan signals "deployed," ask him to confirm the deploy
completed. Don't troubleshoot deploy infra — outside ops lane.

### Step 9b — Smoke probe of the changed surface

For each release, exercise what actually changed:

- **New endpoint**: curl with a real-shape request.
- **New CLI behavior**: run against a clean workspace.
- **UI change**: browser probe (Playwright MCP or manual). Banked
  policy 10.

### Step 9c — Banked failure modes to check

- **Docker container clock-drift after macOS host sleep**: HTTP 401
  timestamp-skew on signed requests after laptop sleep. Resolved
  by `make test-two-service-down && make test-two-service-up` —
  not a code regression, just stack restart. If smoke probe
  returns 401 timestamp errors, restart the local stack before
  suspecting the release.

### PyPI / npm publish-side verify

| Channel | Verify |
|---|---|
| PyPI per-version | `curl -sS https://pypi.org/pypi/aweb/X.Y.Z/json` |
| PyPI cache | `uv lock --refresh-package aweb` (forces re-resolve when cache lags) |
| npm | `npm view @awebai/<pkg> version` |
| GitHub Releases | `gh release view vX.Y.Z --repo awebai/aw` |

## Step 9.5 — Run pending migrations (when applicable)

If Athena's bless-and-run mail names migration files OR

```sh
git -C aweb log --diff-filter=A --name-only <prev>..<this> -- "**/migrations/**"
```

shows new files, invoke **`sop-pgdbm-migration-apply`** before
proceeding to step 10. That skill carries the full procedure
including emergency-metadata-repair guardrails.

## Step 10 — Post verified-live mail

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

**Constitution rule: every fix announcement states** (1) what it
fixes, (2) what nearby issue it does NOT fix, (3) what evidence
proves the fix, (4) what live check proves deployment.

**Item (2) is the recurring slip.** Sofia caught its absence on
v0.5.47. Don't omit it even when nothing nearby is broken — write
"no adjacent surface changes; no nearby issues to disclaim" and
include it explicitly.

Also mail:

- **Iris** when the release carries an external-claim opportunity
  (new capability ready for distribution).
- **Aida** when the release changes a customer-facing surface that
  affects the support runbook.

**Mail body size: keep verified-live mails terse.** Multi-section
>2KB bodies can trip edge blocks (HTTP 403).

## Post-step hygiene

- Update `handoff.md` live-matrix line.
- Append dated entry to `logbook.md` with evidence trail.
- Update `../../status/operations.md` current-snapshot.
- Sweep stale aw work claims after the cycle if any drifted.

## Gate failure — how to hand back to Athena

When step 4 goes red and the failure is a code-side defect (not a
gate-harness drift, not flake handed back per constitution):

```
aw mail send --to athena \
  --subject "gate-failure: <gate-name> on <repo> at <SHA>" \
  --body "$(cat <<EOF
Gate: <make target>
Repo + SHA: <repo> <SHA>
Failure shape: <test name / step name>
Output (last ~40 lines):
<paste relevant gate output, scrubbed of secrets>

My read: <what surface looks broken; what I'd guess is the cause>
Next: holding the release; re-run when you signal.
EOF
)"
```

Subject line names the gate (not just "test failed") so Athena can
triage at-a-glance. Body's "My read" is genuinely useful even when
wrong — it gives her something to disagree with, which is faster
than her starting cold.

Per constitution: do NOT push back on red as flake/known/baseline-
accept. The hand-back IS the right move; Athena's reply tells me
whether to re-gate, wait for a fix-forward commit, or hold longer.

## What can go wrong (pointer)

If anything else in the chain goes red — GHA didn't fire, /health
doesn't flip, migration fails — see `legacy.md` for banked failure
shapes. The most common: image-pin-bump miss (infra-render),
batched tag push (infra-github), pgdbm checksum drift (migration-
discipline), gate-harness drift (gate-discipline).

When in doubt: stop, name the failure shape to Athena, work the fix
together. Don't compose recovery moves under pressure.
