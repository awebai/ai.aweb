# A2A v1.0 canonical source pins + conformance check

Verified 2026-06-07 against the real A2A spec/proto (not memory), per AGENTS.md.

## Canonical source to pin for aweb-aaqa.1 fixtures

- Repo: `github.com/a2aproject/A2A`
- **Pin tag: `v1.0.1`** (latest release), commit
  `3303592588e388e62e0f69f701af531d2f4e3991`.
  - `v1.0.0` = `173695755607e884aa9acf8ce4feed90e32727a1` (also fine).
- Canonical machine-readable source: **`specification/a2a.proto`**
  (package `lf.a2a.v1`). v1.0 is **proto-first**; JSON Schema is generated
  from the proto. `main` proto is byte-identical to `v1.0.1` for service,
  AgentCard, AgentInterface, and TaskState as of check date.
- Spec site: `https://a2a-protocol.org/latest/specification/`,
  changelog `https://a2a-protocol.org/latest/whats-new-v1/`.
- Local copy saved at `/tmp/a2a-v101.proto` during the check (not committed).

## Why v1.0 vindicates the contract (initial v0.3 suspicion was wrong)

A2A **v1.0 is a breaking release** that went proto-first. It renamed, vs 0.3.x:

- JSON-RPC methods: `message/send`→`SendMessage`, `message/stream`→
  `SendStreamingMessage`, `tasks/get`→`GetTask`, `tasks/list`→`ListTasks`,
  `tasks/cancel`→`CancelTask`, `tasks/resubscribe`→`SubscribeToTask`,
  `agent/getAuthenticatedExtendedCard`→`GetExtendedAgentCard`.
- TaskState wire values: lowercase kebab (`"input-required"`) →
  proto enum names `TASK_STATE_*` (proto3-JSON serializes enums as the
  NAME by default).
- AgentCard: top-level `url`+`preferredTransport`+`additionalInterfaces`
  collapsed into `supportedInterfaces[]` of `AgentInterface`.

So `docs/a2a.md`'s use of `SendMessage`/`TASK_STATE_*`/`supportedInterfaces`
is **conformant with v1.0**, not a gRPC/JSON-RPC confusion. Anyone reasoning
from pre-1.0 A2A memory will wrongly flag it.

## Field-by-field conformance of docs/a2a.md card shape (§5.1)

Proto `AgentCard` (proto3-JSON camelCase) → contract: all present and correct.
`name, description, supportedInterfaces[], provider{url,organization},
version, capabilities{streaming,pushNotifications,extensions,
extendedAgentCard?}, securitySchemes (map), securityRequirements ([]),
defaultInputModes, defaultOutputModes, skills, signatures, iconUrl?,
documentationUrl?`.

`AgentInterface`: `url` (REQUIRED), `protocolBinding` (REQUIRED; core values
`JSONRPC`,`GRPC`,`HTTP+JSON`), `tenant` (OPTIONAL), `protocolVersion`
(REQUIRED; examples `"0.3"`,`"1.0"`). Contract's `"protocolBinding":"JSONRPC"`
+ `"protocolVersion":"1.0"` is exact.

**Tenant resolved in contract's favor.** Proto comment: tenant is an optional
opaque routing string on `AgentInterface`; when set, clients MUST echo it in
the request `tenant` field; protocol does not define its format. Exactly the
contract's §4.3 framing (routing primitive, omit on direct cards). The proto
REST binding also exposes tenant as a URL path prefix `/{tenant}/message:send`
— aweb's path routing `/a2a/agents/{route_id}/rpc` is a legitimate alternative
under the JSONRPC binding (tenant optional), not a conflict.

## Genuine pin/gap items for aaqa.1 (small)

1. **`TASK_STATE_AUTH_REQUIRED`** (+ `TASK_STATE_UNSPECIFIED`=0) exist in the
   enum but the contract §3.1 list and the §10.2 reply-envelope mapping omit
   `auth_required`. Contract discusses auth modes, so fixtures/state-mapping
   should cover the AUTH_REQUIRED interrupted state.
2. **protocolVersion vs version**: pin in fixtures that interface
   `protocolVersion="1.0"` (A2A protocol) is distinct from agent `version`
   `"1.0.0"` (agent's own). Contract gets both right; make it explicit so
   fixtures don't drift.
3. **Ecosystem-migration risk** (product, not conformance): many live A2A
   SDKs/clients still speak 0.3 JSON-RPC names (`message/send`) and lowercase
   states. A strictly-v1.0 gateway may fail against still-0.3 callers. Decide:
   v1.0-only, or accept 0.3 aliases for inbound compat. Raise with Sofia/Athena.
4. Pin fixtures to tag `v1.0.1`, not `main`, for reproducibility.

## Deferred methods in contract — all real v1.0 methods, fine to defer

`SubscribeToTask`, `Create/Get/List/DeleteTaskPushNotificationConfig`,
`GetExtendedAgentCard`. First slice's `SendMessage/GetTask/ListTasks/CancelTask`
is a coherent conformant subset.
