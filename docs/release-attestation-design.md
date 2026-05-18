# Release attestation: design

Author: Hestia
Status: draft for engineering review (Athena)

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

## Open design questions for Athena

1. **Attestation storage**: ai.aweb/status/attestations/ committed via PR is the simple option. Alternative: a dedicated bucket / signed JSON published to an HTTPS endpoint. Trade-off: simplicity vs. tamper-evidence.

2. **Attestation freshness**: should attestations expire? An attestation written 6 months ago for v1.0.0 may not reflect current state (e.g., a manual prod change since). Suggest: attestations have a `valid_until` field, default 30 days. Re-validate periodically.

3. **Validator language**: Python is the obvious choice (matches our backend stack, lets us reuse pgdbm for schema queries, easy registry HTTP). Athena's call.

4. **Smokes location**: in the validator repo? per-component repo? Suggest validator repo (shared), with components referencing by name.

5. **Validator versioning**: the validator itself is critical infra. Its own release.yaml + validator-validates-itself bootstrap. Athena's call on the boot sequence.

6. **CI wiring**: each repo's `release-ready` Makefile target gains a
   `release-validate` step at the end. Failure fails the gate. No
   tag-push unless validator wrote an attestation.

7. **Pre-merge vs. post-merge validation**: validate before tag-push
   (catches problems early) or after tag-push (validates against
   the actually-published artifacts). Probably both: pre-tag dry-run
   skips the registry-published checks; post-tag full run including
   smokes.

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
