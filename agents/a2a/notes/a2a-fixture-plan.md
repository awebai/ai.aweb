# A2A v1.0 golden-fixture plan (default-aaak / dev aweb-aaqa.1)

Draft 2026-06-07. Source of truth pinned below. For Athena/Grace review before
golden files are committed to the aweb repo.

## Source pin (reproducible)
- Repo `github.com/a2aproject/A2A`, tag **`v1.0.1`**, commit
  `3303592588e388e62e0f69f701af531d2f4e3991`.
- Canonical: `specification/a2a.proto` (package `lf.a2a.v1`). v1.0 is
  proto-first; the JSON Schema under `specification/json/` is generated from it.
- Validation tooling (pick one, pin it): `buf generate` → JSON Schema, validate
  fixtures with a JSON Schema validator; OR validate via `protojson`
  (Go) / `google.protobuf.json_format` (Py) round-trip against the compiled
  proto. Recommend protojson round-trip — it is the literal v1.0 JSON encoding,
  no schema-gen drift.

## proto3-JSON rules every fixture MUST obey
- Field names → lowerCamelCase (`supported_interfaces`→`supportedInterfaces`,
  `return_immediately`→`returnImmediately`, `context_id`→`contextId`).
- Enums serialize as the NAME string → `"TASK_STATE_WORKING"` (this is *why*
  v1.0 wire states are SCREAMING_SNAKE).
- `Timestamp` → RFC3339 string; `int32` → number; `Struct` → JSON object.
- `oneof` → exactly the set arm present.
- All `field_behavior = REQUIRED` fields MUST be present.

## JSON-RPC binding envelope
- Request: `{"jsonrpc":"2.0","id":N,"method":"<RpcName>","params":<Request msg>}`
  where method ∈ `SendMessage|GetTask|ListTasks|CancelTask` and params is the
  proto3-JSON of the corresponding `*Request` message.
- Success: `{"jsonrpc":"2.0","id":N,"result":<return msg proto3-JSON>}`.
- Error: `{"jsonrpc":"2.0","id":N,"error":{"code":..,"message":..,"data":..}}`.
- OPEN precision item: confirm whether `params` includes the `tenant` field for
  the JSONRPC binding (aweb path-routes per /rpc URL, so tenant is empty/omitted)
  — verify against the A2A JSON-RPC transport doc when writing goldens.

## Fixture set A — Agent Cards (validate against `AgentCard`)
1. **hosted-default-card.json** — single hosted-custodial agent, default for
   host. supportedInterfaces[0]={url:.../a2a/agents/{route}/rpc,
   protocolBinding:"JSONRPC", protocolVersion:"1.0"}, tenant omitted.
2. **byot-default-card.json** — BYOT single agent on customer domain.
3. **byot-router-card.json** — root router card for multi-agent host (§5.2);
   skills=[route-to-agent]; MUST NOT imply enumeration.
4. **per-address-direct-card.json** — `/a2a/agents/{route}/agent-card.json`,
   tenant omitted (direct), digest-publishable.
   (A shared/router interface variant WITH `tenant` set, to exercise the
   tenant-echo rule, is a 5th optional card.)
All four reuse: provider{url,organization}, capabilities{streaming:false,
pushNotifications:false, extensions:[awid-publication ext]}, securitySchemes:{},
securityRequirements:[], defaultInput/OutputModes:["text/plain"], version
"1.0.0" (agent version, distinct from interface protocolVersion "1.0").

## Fixture set B — JSON-RPC request/response (validate params/result against msgs)
- **SendMessage** req → params=`SendMessageRequest{message, configuration{
  returnImmediately:true, acceptedOutputModes}, metadata?}`. resp result=
  `SendMessageResponse` — **oneof**: the `task` arm `{"task":{Task...}}` for the
  async path. Also a `{"message":{...}}` variant fixture for direct reply.
- **GetTask** req → `GetTaskRequest{id, historyLength?}`. resp result = `Task`.
- **ListTasks** req → `ListTasksRequest{contextId?, status?, pageSize?,
  pageToken?}`. resp result = `ListTasksResponse{tasks[], nextPageToken,
  pageSize, totalSize}` — these four are REQUIRED (see note 1 below).
- **CancelTask** req → `CancelTaskRequest{id, metadata?}`. resp result = `Task`
  with status.state `TASK_STATE_CANCELED`.

### Task object shape gotcha (high-value)
`Task` has NO top-level `state`. State is nested:
`{"id":..,"contextId":..,"status":{"state":"TASK_STATE_WORKING","message":{..}?,
"timestamp":".."},"artifacts":[..],"history":[..],"metadata":{}}`. Fixtures and
the gateway serializer MUST nest state under `status`. Common place to get wrong.

### State-coverage fixtures (one Task each)
SUBMITTED, WORKING, INPUT_REQUIRED, COMPLETED (with text artifact), FAILED
(timeout message), CANCELED, REJECTED, and **AUTH_REQUIRED** (Athena: add).

## NEW conformance notes for the contract (route to Athena)
1. **ListTasks pagination is not deferrable at the schema level.**
   `ListTasksResponse` makes `nextPageToken`, `pageSize`, `totalSize` REQUIRED.
   Contract §9.4 frames pagination as "required before public launch" — but even
   v0 responses must carry these fields to validate. Adjust wording: pagination
   *fields* are mandatory now; only large-scale paging UX can wait.
2. **`return_immediately` proto comment is verbatim the contract's §9.2** (false
   = wait for terminal OR interrupted; interrupted = INPUT_REQUIRED/AUTH_REQUIRED).
   Confirms AUTH_REQUIRED must be a returnable interrupted state in the contract.

## Fixture set C — aweb bridge envelopes (UNBLOCKED; Athena ruled 2026-06-07)
Issues #1–#3 decided. Contract must change accordingly; fixtures prove the rules.
- **a2a-reply now REQUIRES `task_id`**; include `context_id` when available.
  Design stays one-thread-per-task, but the explicit task_id echo is the
  parser-level guardrail invariant. (A2A `Message` already carries task_id/
  context_id, fields 3/2 — consistent.)
- **Unfenced text MUST NOT auto-complete.** v0: unfenced output = a non-terminal
  agent/status message or missing-envelope error; task stays WORKING until
  timeout. Terminal states require an `a2a-reply` block (or the future helper).
- **Terminal is final.** A reply arriving after FAILED/CANCELED/COMPLETED/
  REJECTED is ignored+logged or starts a NEW task by explicit policy; it never
  mutates the terminal task.

Bridge fixtures to author:
1. `bridge-inbound.task.json` — well-formed `a2a-task` envelope.
2. `bridge-reply.completed.json` — `a2a-reply` with task_id + completed +
   text artifact → task COMPLETED.
3. `bridge-reply.input-required.json` — and a `QUESTION:` compat variant.
4. **negative**: `bridge-reply.mismatched-task-id.json` — reply task_id ≠ task →
   rejected/ignored, task unchanged.
5. **negative**: `bridge-reply.stray-prose.json` — unfenced text → task stays
   WORKING, NOT COMPLETED.
6. **negative**: `bridge-reply.after-terminal.json` — late reply after
   timeout-FAILED → ignored, terminal task unchanged.

## card_digest canonical bytes — RULE PINNED (Athena 2026-06-07)
`card_digest = sha256(<canonical bytes>)`, encoded **`sha256:<lowercase-hex>`**.
Canonical bytes = **JCS canonicalization of the card after applying A2A
field-presence/default rules, with the `signatures` field absent** — i.e. the
exact same bytes A2A uses for card-signature signing. One canonical form for
both signature and digest.
- Blocking only for **Tier-2 digest-bearing fixtures**, not the plain cards.
- Each Tier-2 fixture MUST ship the byte-for-byte canonical JSON string (or raw
  bytes) PLUS the expected `sha256:<hex>` so the vector is self-checking.
- Open micro-items to nail when authoring: exact A2A default/empty-field
  presence rules (does `securitySchemes:{}` / `securityRequirements:[]` serialize
  or drop?), and ordering — JCS sorts keys lexicographically, so confirm no
  pre-JCS proto-default surprises.

## Implementation/architecture gates — NOT fixture blockers (Athena)
Recorded as sequencing/acceptance gates for the dev implementation task, named
here only as dependencies:
- **Agent wake path** (#5): Phase 4 acceptance gate. A bridge slice may NOT
  claim product viability until the wake mechanism + latency-budget-vs-timeout
  are chosen. Fixture plan names the dependency; no vector impact.
- **AWID trust sequencing** (#6): pull a minimal AWID publication + Tier-2 check
  for ONE route forward as a risk-reduction slice before claiming the
  differentiator. Event may run local/unverified, but product proof shouldn't
  wait for all gateway plumbing. Affects Tier-2 fixtures' delivery order, not
  their content.
