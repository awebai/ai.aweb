# Fixture classification — normative A2A wire vs aweb bridge-local

Two distinct kinds. They have different authorities and different validators.

## A — Normative A2A v1.0 wire (authority: a2aproject/A2A v1.0.1 proto)
Must validate via protojson against the pinned proto message. Conformance is
non-negotiable; if A2A and aweb disagree, A2A wins for these.

| Fixture | Proto message | Notes |
|---|---|---|
| cards/per-address-direct-card.json | AgentCard | direct card, tenant omitted |
| cards/byot-router-card.json | AgentCard | root router card (§5.2) |
| digest/per-address-direct-card.digest-vector.json | AgentCard (canonical) | digest over JCS(card w/o signatures) |
| jsonrpc/send-message.request.json (`params`) | SendMessageRequest | returnImmediately:true async path |
| jsonrpc/send-message.response.json (`result`) | SendMessageResponse | oneof → `task` arm |
| jsonrpc/get-task.request.json (`params`) | GetTaskRequest | |
| jsonrpc/get-task.response.completed.json (`result`) | Task | nested status.state; text artifact |
| jsonrpc/get-task.response.auth-required.json (`result`) | Task | gateway-generated AUTH_REQUIRED |
| jsonrpc/list-tasks.request.json (`params`) | ListTasksRequest | |
| jsonrpc/list-tasks.response.json (`result`) | ListTasksResponse | required pagination fields |
| jsonrpc/cancel-task.request.json (`params`) | CancelTaskRequest | |
| jsonrpc/cancel-task.response.json (`result`) | Task | TASK_STATE_CANCELED |

The JSON-RPC envelope (`jsonrpc`/`id`/`method`/`result`) wraps the proto3-JSON
payload; the proto governs the `params`/`result` body only. `tenant` is omitted
from `params` for path-routed per-address `/rpc` endpoints (Athena-confirmed:
echo tenant only when the selected AgentInterface sets it).

## B — aweb bridge-local (authority: docs/a2a.md §10 + Athena rulings)
Gateway↔agent envelopes. NOT A2A wire — do not protojson-validate. These are an
aweb product contract; we own them. Validator = the gateway's bridge parser.

| Fixture | Encodes |
|---|---|
| bridge/inbound.a2a-task.json | task envelope sent to the agent (§10.1) |
| bridge/reply.completed.json | a2a-reply, task_id required → COMPLETED |
| bridge/reply.input-required.json | a2a-reply → INPUT_REQUIRED |
| bridge/reply.neg.mismatched-task-id.json | task_id ≠ open task → ignored (#1) |
| bridge/reply.neg.stray-prose.json | unfenced text → stays WORKING (#2) |
| bridge/reply.neg.after-terminal.json | late reply after terminal → ignored (#3) |

`state` values in bridge replies are gateway-local aliases (`completed`,
`input_required`, ...) plus the `TASK_STATE_*` forms; the gateway maps them to
the A2A wire `TASK_STATE_*`. AUTH_REQUIRED is gateway-generated only — there is
deliberately no agent-asserted `auth_required` reply alias.

## Boundary rule
A bridge reply is translated by the gateway into a wire Task/TaskStatus. The
bridge fixtures prove the gateway's input handling; the wire fixtures prove its
A2A output. A change to A2A v1.0 changes set A; a change to our bridge ergonomics
changes set B. Keep them from leaking into each other.
