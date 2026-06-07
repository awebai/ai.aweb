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

## Waiting on Athena (sent via mail)
1. **Task-tracking gap**: epic `aweb-aaqa` / `aweb-aaqa.1` referenced in my
   AGENTS.md + her welcome brief **do not exist as `aw` tasks** in team
   `default:aweb.ai` (IDs run `default-aaaa..aaaj`; no `aaqa`). Need to know
   whether to create them (and under what real ID) or whether they live
   elsewhere. Did NOT create — IDs are auto-assigned, can't force `aaqa`.
2. **Small pin/gap items** for the contract (none block sign-off):
   - `TASK_STATE_AUTH_REQUIRED` missing from §3.1 list + §10.2 reply mapping.
   - Make interface `protocolVersion="1.0"` vs agent `version="1.0.0"`
     explicit in fixtures.
   - Product decision: v1.0-only vs accept 0.3 JSON-RPC aliases for inbound
     compat (live SDKs still speak 0.3). Flag to Sofia too.

## Open (mine to do next)
- Draft golden fixtures from `v1.0.1` proto: hosted default card, BYOT card,
  router card, `SendMessage` + `GetTask` JSON-RPC req/resp. Hold until
  Athena confirms task home + the AUTH_REQUIRED/compat decisions.
