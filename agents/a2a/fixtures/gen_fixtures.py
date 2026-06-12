#!/usr/bin/env python3
"""A2A v1.0 golden-fixture generator (DRAFT for Athena/Grace review).

Source of truth: github.com/a2aproject/A2A tag v1.0.1
(commit 3303592588e388e62e0f69f701af531d2f4e3991), specification/a2a.proto,
package lf.a2a.v1. Hand-authored to the proto (no buf/protoc available here);
proto3-JSON encoding applied by hand. Card canonicalization + digest follow
Athena's ruling (2026-06-07): one canonical function shared by signing, digest,
and tests.

Canonicalization (card_digest):
  1. take the generated AgentCard object
  2. remove top-level `signatures`
  3. field-presence cleanup: required fields stay; optional fields only if
     explicitly present; empty optional maps/lists omitted; proto-default
     scalars omitted unless deliberately advertised (we advertise
     streaming/pushNotifications = false explicitly)
  4. JCS canonicalize (RFC 8785)
  5. card_digest = "sha256:" + lowercase-hex over the UTF-8 canonical bytes

NOTE: our generated cards already omit empty optionals, so the served card IS
the canonical input here (modulo signatures on signed cards). JCS for this data
(strings/booleans/objects/arrays, no numbers) reduces to sorted-keys + minimal
separators; a real protojson+JCS toolchain MUST replace this before the vectors
are treated as normative. Record any tooling delta in vector-notes.md.
"""
import hashlib
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def jcs(obj) -> bytes:
    """RFC 8785 JSON Canonicalization Scheme, sufficient for card data.

    Recursive lexicographic key sort, minimal separators, UTF-8, no
    insignificant whitespace. (No floats in card data, so ECMAScript number
    formatting is not exercised.)
    """
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def card_digest(card: dict) -> tuple[str, bytes]:
    canonical = {k: v for k, v in card.items() if k != "signatures"}
    cbytes = jcs(canonical)
    return "sha256:" + hashlib.sha256(cbytes).hexdigest(), cbytes


def write(path: str, obj) -> None:
    full = os.path.join(HERE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


# ---- Fixture set A: Agent Cards (validate against AgentCard) -----------------

# A per-address DIRECT card (unauth, tenant omitted). Empty optional maps/lists
# (securitySchemes, securityRequirements) omitted per Athena; streaming /
# pushNotifications advertised explicitly as false (JSON presence is explicit).
per_address_card = {
    "name": "Acme Help",
    "description": "Customer support agent for Acme products.",
    "provider": {"organization": "Acme", "url": "https://acme.com"},
    "version": "1.0.0",
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
        "extensions": [
            {
                "uri": "https://aweb.ai/a2a/ext/awid-publication/v1",
                "description": "AWID publication and delegation metadata",
            }
        ],
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "supportedInterfaces": [
        {
            "url": "https://acme.com/a2a/agents/r_help_01/rpc",
            "protocolBinding": "JSONRPC",
            "protocolVersion": "1.0",
        }
    ],
    "skills": [
        {
            "id": "order-status",
            "name": "Order status",
            "description": "Look up order status from an order ID.",
            "tags": ["support", "orders"],
        }
    ],
}

# A root ROUTER card for a multi-agent host (§5.2).
router_card = {
    "name": "Acme A2A Gateway",
    "description": "A2A gateway for Acme agents. Exact agent cards are published in the Acme/aweb directory.",
    "provider": {"organization": "Acme", "url": "https://acme.com"},
    "version": "1.0.0",
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
        "extensions": [
            {
                "uri": "https://aweb.ai/a2a/ext/awid-publication/v1",
                "description": "AWID publication and delegation metadata",
            }
        ],
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "supportedInterfaces": [
        {
            "url": "https://acme.com/a2a/rpc",
            "protocolBinding": "JSONRPC",
            "protocolVersion": "1.0",
        }
    ],
    "skills": [
        {
            "id": "route-to-agent",
            "name": "Route to Acme agents",
            "description": "Routes customer tasks to configured Acme agents when enough information is provided.",
            "tags": ["router"],
        }
    ],
}

write("cards/per-address-direct-card.json", per_address_card)
write("cards/byot-router-card.json", router_card)

# Self-checking digest vector for the direct card.
digest, cbytes = card_digest(per_address_card)
router_digest, router_cbytes = card_digest(router_card)
write(
    "digest/per-address-direct-card.digest-vector.json",
    {
        "source": "a2aproject/A2A v1.0.1 specification/a2a.proto (AgentCard)",
        "rule": "sha256 over JCS(card without `signatures`), per Athena 2026-06-07",
        "canonical_bytes_utf8": cbytes.decode("utf-8"),
        "card_digest": digest,
    },
)

# ---- Fixture set B: JSON-RPC request/response (proto3-JSON in params/result) --

send_message_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "SendMessage",
    "params": {
        "message": {
            "messageId": "msg-001",
            "role": "ROLE_USER",
            "parts": [{"text": "Where is order 1234?"}],
        },
        "configuration": {
            "returnImmediately": True,
            "acceptedOutputModes": ["text/plain"],
        },
    },
}

# SendMessageResponse is a oneof payload {task | message}; async path returns task.
send_message_response = {
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "task": {
            "id": "t_123",
            "contextId": "c_456",
            "status": {
                "state": "TASK_STATE_WORKING",
                "timestamp": "2026-06-07T10:00:00Z",
            },
        }
    },
}

get_task_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "GetTask",
    "params": {"id": "t_123"},
}

# GetTask returns a bare Task. NOTE: state is nested under status, not top-level.
get_task_response_completed = {
    "jsonrpc": "2.0",
    "id": 2,
    "result": {
        "id": "t_123",
        "contextId": "c_456",
        "status": {
            "state": "TASK_STATE_COMPLETED",
            "timestamp": "2026-06-07T10:00:05Z",
        },
        "artifacts": [
            {
                "artifactId": "a_1",
                "parts": [
                    {"text": "Order 1234 shipped Tuesday and arrives Thursday."}
                ],
            }
        ],
    },
}

list_tasks_request = {
    "jsonrpc": "2.0",
    "id": 3,
    "method": "ListTasks",
    "params": {"contextId": "c_456"},
}

# ListTasksResponse REQUIRES tasks, nextPageToken, pageSize, totalSize.
list_tasks_response = {
    "jsonrpc": "2.0",
    "id": 3,
    "result": {
        "tasks": [
            {
                "id": "t_123",
                "contextId": "c_456",
                "status": {
                    "state": "TASK_STATE_COMPLETED",
                    "timestamp": "2026-06-07T10:00:05Z",
                },
            }
        ],
        "nextPageToken": "",
        "pageSize": 50,
        "totalSize": 1,
    },
}

cancel_task_request = {
    "jsonrpc": "2.0",
    "id": 4,
    "method": "CancelTask",
    "params": {"id": "t_123"},
}

cancel_task_response = {
    "jsonrpc": "2.0",
    "id": 4,
    "result": {
        "id": "t_123",
        "contextId": "c_456",
        "status": {
            "state": "TASK_STATE_CANCELED",
            "timestamp": "2026-06-07T10:00:10Z",
        },
    },
}

# AUTH_REQUIRED is a gateway-generated state (Athena: not an agent reply alias).
get_task_response_auth_required = {
    "jsonrpc": "2.0",
    "id": 5,
    "method": None,
    "result": {
        "id": "t_789",
        "contextId": "c_456",
        "status": {
            "state": "TASK_STATE_AUTH_REQUIRED",
            "message": {
                "messageId": "gw-001",
                "role": "ROLE_AGENT",
                "taskId": "t_789",
                "parts": [{"text": "Authentication required to access order history."}],
            },
            "timestamp": "2026-06-07T10:01:00Z",
        },
    },
}
get_task_response_auth_required.pop("method")

for name, obj in [
    ("jsonrpc/send-message.request.json", send_message_request),
    ("jsonrpc/send-message.response.json", send_message_response),
    ("jsonrpc/get-task.request.json", get_task_request),
    ("jsonrpc/get-task.response.completed.json", get_task_response_completed),
    ("jsonrpc/get-task.response.auth-required.json", get_task_response_auth_required),
    ("jsonrpc/list-tasks.request.json", list_tasks_request),
    ("jsonrpc/list-tasks.response.json", list_tasks_response),
    ("jsonrpc/cancel-task.request.json", cancel_task_request),
    ("jsonrpc/cancel-task.response.json", cancel_task_response),
]:
    write(name, obj)

# ---- Fixture set C: aweb bridge envelopes (gateway-local, NOT A2A wire) -------
# Per Athena's rulings: a2a-reply REQUIRES task_id; unfenced never auto-completes;
# terminal is final. The 3 negatives encode those invariants.

bridge_inbound = {
    "task_id": "t_123",
    "context_id": "c_456",
    "route_id": "r_help_01",
    "target_address": "acme.com/help",
    "gateway_identity": "did:aw:example-gateway",
    "caller_id": "api-key:demo-harness",
    "state": "TASK_STATE_WORKING",
}

bridge_reply_completed = {
    "task_id": "t_123",
    "context_id": "c_456",
    "state": "completed",
    "artifacts": [
        {"type": "text", "text": "Order 1234 shipped Tuesday and arrives Thursday."}
    ],
}

bridge_reply_input_required = {
    "task_id": "t_123",
    "context_id": "c_456",
    "state": "input_required",
    "artifacts": [{"type": "text", "text": "Which email is the order under?"}],
}

# NEGATIVE 1: reply task_id != open task -> gateway ignores/rejects, task unchanged.
bridge_reply_mismatched = {
    "_expect": "REJECTED: reply task_id does not match any open task for this thread; gateway ignores, task state unchanged",
    "task_id": "t_999",
    "context_id": "c_456",
    "state": "completed",
    "artifacts": [{"type": "text", "text": "wrong task"}],
}

# NEGATIVE 2: unfenced stray prose -> task stays WORKING, NOT completed.
bridge_reply_stray_prose = {
    "_expect": "NON-TERMINAL: no a2a-reply fence present; gateway treats as agent status/missing-envelope; task stays TASK_STATE_WORKING until timeout, NOT COMPLETED",
    "_raw_agent_output": "On it, let me check that order for you...",
}

# NEGATIVE 3: late reply after terminal -> ignored/logged, terminal unchanged.
bridge_reply_after_terminal = {
    "_expect": "IGNORED: task already TASK_STATE_FAILED (timeout); late reply must not mutate a terminal task; ignore+log or start new task by policy",
    "task_id": "t_123",
    "context_id": "c_456",
    "state": "completed",
    "artifacts": [{"type": "text", "text": "late answer after timeout"}],
}

for name, obj in [
    ("bridge/inbound.a2a-task.json", bridge_inbound),
    ("bridge/reply.completed.json", bridge_reply_completed),
    ("bridge/reply.input-required.json", bridge_reply_input_required),
    ("bridge/reply.neg.mismatched-task-id.json", bridge_reply_mismatched),
    ("bridge/reply.neg.stray-prose.json", bridge_reply_stray_prose),
    ("bridge/reply.neg.after-terminal.json", bridge_reply_after_terminal),
]:
    write(name, obj)

print("Fixtures written under", HERE)
print()
print("direct card  card_digest:", digest)
print("  canonical bytes len   :", len(cbytes))
print("router card  card_digest:", router_digest)
print()
print("Spot checks:")
print("  SendMessageResponse oneof arm: 'task' present =",
      "task" in send_message_response["result"])
print("  Task state nested under status:",
      get_task_response_completed["result"]["status"]["state"])
print("  ListTasksResponse required fields present:",
      all(k in list_tasks_response["result"]
          for k in ("tasks", "nextPageToken", "pageSize", "totalSize")))
print("  Role enum serialized as NAME:",
      send_message_request["params"]["message"]["role"])
print("  bridge a2a-reply carries task_id:",
      "task_id" in bridge_reply_completed)
