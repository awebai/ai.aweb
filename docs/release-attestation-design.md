# Release attestation: design

Author: Hestia
Status: v2 — post-engineering-review (Athena 980f9360); ready for direction review (Sofia)
Reviewers: Athena (engineering — signed off on shape, pushback incorporated below)

## Problem

The federation 1.23.0 wave on 2026-05-18 went through four sequential
releases (aweb 1.23.0 → ac v0.5.40 → awid 0.5.5 → ac v0.5.41). Every
individual artifact passed its own gate, yet the composed system was
broken for ~50 minutes of customer-impact: `aw mail send` 500ed in
production because federation schema migrations had not been applied,
because the awid client in the ac container was one minor behind the
endpoints it was calling, because the awid server itself had not been
re-released to expose those endpoints, and because the verification
that any of this worked together was a human-and-Hestia checklist run
ad-hoc after the fact.

Every failure shared one structural cause: **each release gate had
enough knowledge to verify its own component but not enough knowledge
to verify that the assembled system would function.**

Memory-based discipline cannot scale to a system with this many
moving parts (4 deployed services, 8+ release-producing packages,
3 schema-bearing databases, 3+ npm registries, GHCR, PyPI, GitHub
Container Registry, Render, Cloudflare, Neon, multiple CI workflows).
The number of edges between components grows as N²; the number of
ordering constraints between releases grows similarly. No agent can
hold this in working memory and reliably get it right under deadline
pressure.

## Goal

Make it structurally impossible for a release to be marked
"shipped" unless the composition is provably correct.

If the validator cannot prove correctness, no attestation is
written. No attestation means no release. The system refuses to
lie about what is deployed.

## Solution

Every release-producing repo commits a `release.yaml` at its root.
A shared validator reads this file, verifies its clauses against
the live system, and on full green writes a signed attestation to
a known location (`ai.aweb/status/attestations/`). Without an
attestation, no release.

This layer **builds on** Mia's gate-shape-sanity-check discipline
(verify the gate exercises the code under test). It does not
replace it. The two compose: gate-shape ensures each individual
gate measures what it claims; attestations ensure the assembled
system actually works.

This places the contract IN CODE, not in tribal knowledge. The
contract is machine-readable, recursively verifiable, and
co-located with the source repo that knows what its release needs.

## The contract: release.yaml schema

Every release-producing repo commits `release.yaml` at root.
Schema below; field semantics in the next section.

```yaml
component: <string>         # canonical name: aweb, ac, awid, channel, pi, claude-skills
version: <semver>
git_tag: <string>           # e.g., server-v1.23.0, v0.5.40, channel-v1.4.2
git_sha: <string>

# What this release puts into the world.
produces:
  artifacts:
    - kind: pypi | npm | ghcr-image | static-site
      name: <string>
      version: <semver>
      # Validator checks the registry for this version.

  schemas:
    - service: <string>       # where this schema is hosted (e.g., api.awid.ai)
      schema: <string>        # Postgres schema name (e.g., awid)
      module_name: <string>   # as written to schema_migrations (e.g., awid-service)
      migrations_through: <string>  # filename of last migration file in this release
      # Validator checks the live DB's schema_migrations table.

  # Mirror declarations: when this release ships migration files that
  # are COPIES of another component's migrations (e.g., ac's aweb-schema
  # mirrors aweb-server's migrations), declare the mirror relationship.
  # Validator asserts content equality between source and target.
  mirrors:
    - source_component: <string>            # e.g., aweb
      source_path: <string>                 # e.g., aweb/server/src/aweb/migrations/aweb/005_*.sql
      target_path: <string>                 # e.g., ac/backend/src/aweb_cloud/migrations/aweb/004_*.sql
      # Validator reads both files; asserts byte-equality (or canonicalized SQL equality).

  deployed_services:
    - service: <string>       # e.g., app.aweb.ai
      release_tag: <string>   # value expected in /health build.release_tag
      health_url: <string>    # full /health URL

# What this release REQUIRES to function. Validated transitively.
requires:
  # Other releaseable components that must be released at the floor.
  components:
    - component: <string>     # e.g., awid
      min_version: <semver>
      reason: <string>        # human-readable: why this floor (federation endpoints, schema, etc.)

  # Specific registry artifacts that must exist at min.
  artifacts:
    - kind: pypi | npm
      name: <string>
      min_version: <semver>   # or exact_version

  # Live services that must report at least min_version + pass a probe.
  deployed:
    - service: <string>
      min_version: <semver>
      probe:
        method: GET | POST
        url: <string>
        expect_status: <int>
        # Optional jsonpath assertion to verify response shape:
        jsonpath: $.version
        op: ">=" | "==" | "in"
        value: <string>

  # Schemas that must have specific migrations applied to a live DB.
  schemas:
    - service: <string>
      schema: <string>
      must_include: [<filename>, ...]

# Tests that MUST pass against the just-assembled live system.
smoke:
  - name: <string>           # canonical name; pinned in code, not free-form
    runner: shell | http     # how to execute
    shell:
      command: <string>
      expect_exit: 0
      timeout_seconds: <int>
    http:
      method: GET | POST
      url: <string>
      headers: {...}
      body: {...}
      expect_status: <int>
      jsonpath_asserts: [{path, op, value}]
    flake_retry: <int>       # smokes may legitimately be flaky; bounded retry
```

## Field semantics

### `produces`

What the release physically creates. Each entry is independently
verifiable post-publish:

- `artifacts`: the validator queries the named registry. PyPI:
  `pypi.org/pypi/<name>/json` for the version. npm:
  `registry.npmjs.org/<name>/<version>`. GHCR: container registry
  manifest. Static site: a /health-equivalent file at the deployed
  URL.
- `schemas`: the validator connects to the named service's DB and
  reads `<schema>.schema_migrations` to verify the declared
  `migrations_through` filename is present, with module_name
  matching.
- `deployed_services`: the validator hits the service's
  `/health` (or equivalent) and verifies the declared release_tag.

### `requires`

What must already be true for THIS release to function:

- `components`: other releases that must be at min_version, with
  THEIR OWN attestations valid. This is the recursive part. The
  validator fetches the named component's release.yaml at the
  matching version's git tag, recursively validates it. If any
  link in the chain is not attested-released, this release cannot
  be attested.
- `artifacts`: registries queried for floor.
- `deployed`: probes run against live services.
- `schemas`: DBs queried for required migration filenames.

### `smoke`

End-to-end tests run against the just-assembled live system. These
are the load-bearing proof that the system actually works, not just
that the artifacts exist and the version numbers line up. Examples:

- `aw-mail-send-prod-smoke`: send a real mail from a known test
  account to a known target, expect successful 2xx and message
  receipt.
- `cross-namespace-federation-smoke`: send a mail from one namespace
  to another namespace's address, expect resolve via awid → outbound
  federation envelope → inbound receiver → receipt.
- `app-aweb-ai-health-includes-release-tag`: HTTP probe with
  jsonpath assertion.

Smokes must be defined in code (a `smokes/` directory in the
validator repo), named, versioned, and small. Each release's
release.yaml references smokes by name. Smokes themselves get
PR review like any other gating code.

## Pre-requisites before validator v1 ships

These have to land before the validator can do useful work. None
are inherently blocked; flagged here so they get scheduled with
the validator work.

1. **Every deployed service exposes `release_tag` in /health.**
   Today aweb /health returns `{status, checks}` only; ac /health
   is auth-gated; awid I haven't fully audited. Each deployed
   service needs `/health` build-info instrumented to expose
   `release_tag` (the git tag, not the package version — cloud
   carries multiple package versions). Three small PRs (aweb, ac,
   awid).

2. **Smoke-test team namespace on prod.** Mutating smokes (real
   mail-send, real federation envelope) need a dedicated namespace
   + aliases + cleanup discipline. One-time setup. Smokes
   themselves write tear-down code as part of their assertion.

3. **Attestation signing key in CI.** A GHA secret used by the
   validator to sign attestations (HMAC or Ed25519). Same risk
   class as NPM_TOKEN (leak = forge-able attestations);
   defensible for internal trust. Banked: not designing for
   third-party verification in v1.

## The validator

A single shared tool, committed to `aweb/tools/release-validator/`
(Athena's call on location):

```
validate-release <release-yaml-path>
```

Behavior:

1. Parse release.yaml. Verify schema. FAIL on malformed.
2. For each `produces.artifacts`: query registry, assert version exists.
3. For each `produces.schemas`: query DB, assert migration applied.
4. For each `produces.deployed_services`: probe /health, assert release_tag.
5. For each `requires.components`:
   a. Fetch the named component's release.yaml at the matching version's tag.
   b. Recursively call validate-release on it.
   c. If recursive call returns not-released, FAIL.
   d. **Cycle detection**: maintain a stack of components currently
      being validated; if a recurse-target is already on the stack,
      FAIL with an explicit "release graph has a cycle: A → B → A.
      Refactor to break the cycle, possibly via a release that adds
      the new endpoint to one side without the dep, then a follow-up
      adds the other side." Better than infinite recursion.
6. For each `requires.artifacts`: registry query, floor assertion.
7. For each `requires.deployed`: probe, assertion.
8. For each `requires.schemas`: DB query, must_include assertion.
9. For each `smoke`: run, assert pass (with flake_retry).
10. If all green: write
    `ai.aweb/status/attestations/<component>-<version>.json`
    with:
    ```json
    {
      "component": "...",
      "version": "...",
      "git_sha": "...",
      "released": true,
      "attested_at": "<ISO8601>",
      "validator_version": "<semver>",
      "smokes_passed": ["...", "..."],
      "requires_attestations": [
        { "component": "awid", "version": "0.5.5", "attestation": "<path>" },
        ...
      ],
      "signature": "<hash>"
    }
    ```
    Commit to ai.aweb via PR or direct commit-and-push.
11. If any FAIL: write same file with `released: false` and a
    structured failure record. Hestia's runbook surfaces this as
    red status. The release is not released.

## What this guarantees

For any release of any component, the presence of a fresh
attestation proves:

- Every artifact it claims to produce exists in its registry.
- Every component it depends on is itself attested-released at a
  satisfying version (recursive).
- Every schema migration its function requires is applied to the
  appropriate live DB.
- Every smoke it declared as gating has just passed against the
  live composed system.

The absence of an attestation proves nothing positive — but it
proves the release is not in a known-good state, which is sufficient
to refuse to claim it shipped.

## What this does NOT do

- It does not validate the CORRECTNESS of the release.yaml itself.
  If a release.yaml under-declares its requirements, the validator
  can't catch that. Mitigation: release.yaml changes go through PR
  review like any other code. Mia's code-review-discipline skill
  applies.
- It does not validate smokes that are themselves wrong. Smokes
  are code; they need their own review. Mitigation: keep smokes
  small, named, and explicit.
- It does not eliminate the underlying need for Render to apply
  migrations on startup (Task #109). The attestation catches the
  symptom (`requires.schemas` fail) but the root-cause fix in
  Render config still wants to land separately.
- It does not handle truly novel system shapes (a new
  release-producing repo) automatically. New components need
  schema entries + smoke definitions added. One-time effort per
  new component.
- **Federation smoke v1 limitation**: real federation between two
  separate prod-grade aweb instances requires a second long-running
  instance we don't have yet (would need staging cloud). v1 uses
  the OSS 2-server e2e suite (`scripts/e2e-oss-federation.sh`,
  which Grace added) as the federation smoke — runs in CI,
  exercises the wire-level federation correctly, but does NOT probe
  prod. Real-prod-federation-smoke deferred until staging
  infrastructure exists.
- **Smoke prod-mutation footprint**: mutating smokes (real
  mail-send) write real rows to prod DBs. Each smoke is responsible
  for its own cleanup. A dedicated smoke-test team namespace + test
  aliases keep the footprint isolated. The hygiene discipline lives
  in the smoke itself, not in some out-of-band process.

## Forced ordering as a feature, not a bug

Today's failure was partly an ordering failure: aweb 1.23.0 shipped
before awid 0.5.5 was live, then ac v0.5.40 shipped before its
awid-service pin was bumped to 0.5.5. The compat manifest makes the
correct order automatic:

- awid 0.5.5 releases first (no cross-deps to wait on).
- aweb 1.23.0 declares `requires.deployed.api.awid.ai: min_version 0.5.5`
  + `requires.artifacts.awid-service: min_version 0.5.5`. Cannot
  attest-release until awid is already done.
- ac v0.5.40 declares `requires.components.aweb: 1.23.0` +
  `requires.artifacts.awid-service: 0.5.5`. Cannot attest-release
  until both are done AND its own lock pins them.

This is not extra coordination overhead — it is the coordination
overhead that we were already paying in ad-hoc form, made explicit
in code.

## Edge cases

- **First release of a component**: empty `requires.components`. Bootstrap is fine; no chain to recurse into.
- **Hot-fixes that genuinely need to bypass a smoke**: explicit `--override-smoke=<name>` flag on the validator records the override in the attestation. Runbook surfaces "this release had overrides" prominently. Default discipline: no overrides.
- **Smoke flakiness**: bounded retry per smoke (`flake_retry` field). After retry, hard fail.
- **Migration ordering between components sharing a DB**: handled by `requires.schemas.must_include` — Y can't release until X's migration is applied.
- **Backfill for currently-released versions**: a one-time exercise. The current production state we just verified-live today can be encoded as the first set of attestations.

## Resolved design questions (Athena review 980f9360)

1. **Attestation storage**: `ai.aweb/status/attestations/` committed
   via PR. JSON files, machine-readable, human-auditable, history in
   git. Tamper-evidence comes from git commit signatures + the
   signature field in the attestation body. No separate bucket
   infrastructure in v1.

2. **Attestation freshness**: attestations carry a `valid_until`
   field, default 30 days. A daily cron job re-runs the validator
   for every released component; expired attestations either
   re-validate green or flip to `released: false` and Hestia's
   runbook surfaces them as red. This catches drift (manual prod
   change, dep upgrade in a service we forgot to re-attest).

3. **Validator language**: Python. Matches backend stack, reuses
   pgdbm for `schema_migrations` queries, easy registry HTTP via
   httpx, easy YAML via PyYAML. No new runtime dependency.

4. **Smokes location**: validator repo. Smokes are shared,
   versioned, reviewed in one place. Per-component `release.yaml`
   references smokes by name only. Adding a smoke = PR to the
   validator repo.

5. **Validator self-validation**: the validator gets its own
   `release.yaml` BUT does not recurse into itself. The validator
   pins a specific validator version (its own) in the attestations
   it writes. Bootstrapping: first validator release uses a
   hand-signed attestation; subsequent releases use the previous
   validator's attestation as proof of build. Avoids infinite
   recursion while keeping the chain auditable.

6. **CI wiring**: `release-validate` is the FINAL step in each
   repo's `release-ready` Makefile target. If it fails, the gate
   fails, no tag push, no deploy. The attestation file is the
   gate-output artifact.

7. **Pre-merge vs. post-merge validation**: both. Pre-tag dry-run
   in `release-ready` skips registry-published checks and runs the
   non-mutating smokes; catches obvious problems before tag push.
   Post-tag full validation runs after deploy completes (triggered
   by GHA on tag push), including registry checks and mutating
   smokes; writes the canonical attestation.

## Closing

This is the structural fix to today's mess. Memory-based discipline
cannot scale to a system with this many moving parts; the system
itself has to refuse to lie about what is released. The release.yaml
contract makes correctness load-bearing on CODE that runs in CI, not
on Hestia or Athena or Juan remembering the right sequence.

The cost is real but bounded — defined writing, scoped tooling,
one-time backfill. The cost of NOT doing it is recurring
customer-facing outages whose probability grows with every new
moving part we add.

— Hestia
