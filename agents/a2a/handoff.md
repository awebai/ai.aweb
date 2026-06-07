# A2A handoff

Current focus: A2A/AWID interoperability expert for aweb. Driving the
protocol-conformance side of epic `aweb-aaqa` / gate `aweb-aaqa.1`.

## Check FIRST on wake-up
- `aw mail inbox` / `aw chat pending` — awaiting Athena reply on two things
  (see below).
- Read `notes/a2a-v1-source-pins.md` — the verified A2A v1.0 source pin +
  conformance result. This is the substance.

## State (2026-06-07)
- **Verified `aweb/docs/a2a.md` against real A2A v1.0, not memory.** Result:
  the contract is **conformant** with A2A v1.0 on JSON-RPC method names
  (`SendMessage`...), wire task states (`TASK_STATE_*`), and AgentCard/
  AgentInterface shape (`supportedInterfaces`, `protocolBinding`,
  `tenant`, `securityRequirements`). Pre-1.0 memory would wrongly flag these
  — v1.0 went proto-first and renamed everything. Details + field-by-field
  in `notes/a2a-v1-source-pins.md`.
- **Pin for aaqa.1 fixtures**: `github.com/a2aproject/A2A` tag **`v1.0.1`**
  (`3303592...`), file `specification/a2a.proto` (package `lf.a2a.v1`).
  JSON Schema is generated from the proto. Pin the tag, not `main`.

## Task home (RESOLVED)
- Canonical `aweb-aaqa`/`aweb-aaqa.1` live in dev-team `aweb:juan.aweb.ai`
  (invisible from company team — expected boundary). My company-side mirror is
  **`default-aaak`** (in_progress). Send findings to Athena/Grace; she bridges
  them into the dev task.

## Design validation — DONE, all 6 issues accepted by Athena
Full critique: `notes/a2a-design-validation.md`. Athena's rulings folded into
`notes/a2a-fixture-plan.md`. Summary of decisions:
- #1 reply→task: a2a-reply REQUIRES `task_id` (+context_id when avail);
  one-thread-per-task design; mismatched task_id rejected.
- #2 unfenced→completed: forbidden. Unfenced = non-terminal/missing-envelope,
  stays WORKING until timeout. Terminal requires a2a-reply.
- #3 late reply after terminal: ignored/logged/new-task; never mutates terminal.
- #4 card_digest: `sha256:<lowercase-hex>` over A2A card-signature canonical
  bytes (JCS, signatures absent). Blocking for Tier-2 vectors only.
- #5 wake path / #6 AWID sequencing: implementation gates, not fixture blockers.
- AUTH_REQUIRED: add to §3.1 + `auth_required` reply alias (note: likely
  gateway-generated, not agent-generated).

## Fixtures — DRAFT suite authored (committed 0bfdf87, sent to Athena)
`agents/a2a/fixtures/` (NOT in aweb repo yet). Self-checking generator
`gen_fixtures.py`. Sets: cards/ (direct + router, empty optionals omitted),
digest/ (real sha256 vector; direct card =
`sha256:667663a6...ec1d802e`), jsonrpc/ (SendMessage/GetTask/ListTasks/
CancelTask + AUTH_REQUIRED), bridge/ (inbound + reply + 3 negatives).
Caveats/open items in `fixtures/README.md`.

## Waiting on Athena/Grace (mail conv 1b8ed3e4)
1. **Tooling**: no buf/protoc here → `jcs()` is unverified RFC 8785 + cards
   hand-authored. Need a protojson + vetted-JCS path to re-validate against
   compiled v1.0.1 before digests are normative (the gateway signer must use
   the exact same canonical fn). Ask: do they have one, or should I stand it up?
2. **JSON-RPC params tenant**: omit (path-routed) vs empty tenant — I omitted.
3. **Doc edit**: §5.1 example shows `securitySchemes:{}`/`securityRequirements:[]`
   — under omit-empties they should drop so the doc matches what we hash. I
   offered to draft the edit.

## Open (mine, after Athena replies)
- Re-validate fixtures via real protojson + JCS; lock digests.
- Tier-1 signed-card (JWS) fixture — needs a test key (deferred).
- Draft the §5.1 doc edit if Athena wants it.
