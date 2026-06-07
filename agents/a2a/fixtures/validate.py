#!/usr/bin/env python3
"""Normative validator for the A2A v1.0 golden fixtures.

SCRATCH / HAND-OFF TO GRACE. This was NOT runnable in a2a's environment
(no pip / protoc / buf / network). Run it where Go/protoc/buf or pip works.

What it does:
  1. Downloads the pinned A2A proto (v1.0.1).
  2. Strips google.api.* deps (service block + http/field_behavior options) so it
     compiles standalone for JSON validation — message/enum JSON mapping does not
     depend on those annotations.
  3. Compiles it with grpc_tools.protoc.
  4. protojson-validates each A2A-wire fixture against its exact message type,
     strictly (unknown fields rejected).
  5. Recomputes every card_digest with a vetted RFC 8785 JCS lib and compares to
     the committed vector.

Run:
    pip install protobuf grpcio-tools jcs
    python validate.py            # from agents/a2a/fixtures/

Why protojson is the normative path (not json.dumps(sort_keys=True)): the
gateway's card signer/digester MUST use the same canonical function that
produced the committed vectors. json.dumps is only acceptable for exploration
because the current cards contain no floats; RFC 8785 ECMAScript number
formatting is otherwise required.

Field-presence note (already verified from the proto, no tooling needed):
AgentCapabilities.streaming / push_notifications / extended_agent_card are
`optional bool` (proto3 explicit presence). protojson therefore PRESERVES an
explicitly-set `false` on round-trip and OMITS an unset field. So advertising
streaming:false / pushNotifications:false is canonical-stable, and omitting
extendedAgentCard means "absent", not "false". This is exactly what the cards
rely on; this script's round-trip should confirm it (assert below).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PROTO_URL = (
    "https://raw.githubusercontent.com/a2aproject/A2A/v1.0.1/specification/a2a.proto"
)
WORK = os.path.join(HERE, "_validate_work")

# fixture path -> (json-rpc field to extract, fully-qualified message name)
WIRE_FIXTURES = {
    "cards/per-address-direct-card.json": (None, "AgentCard"),
    "cards/byot-router-card.json": (None, "AgentCard"),
    "jsonrpc/send-message.request.json": ("params", "SendMessageRequest"),
    "jsonrpc/send-message.response.json": ("result", "SendMessageResponse"),
    "jsonrpc/get-task.request.json": ("params", "GetTaskRequest"),
    "jsonrpc/get-task.response.completed.json": ("result", "Task"),
    "jsonrpc/get-task.response.auth-required.json": ("result", "Task"),
    "jsonrpc/list-tasks.request.json": ("params", "ListTasksRequest"),
    "jsonrpc/list-tasks.response.json": ("result", "ListTasksResponse"),
    "jsonrpc/cancel-task.request.json": ("params", "CancelTaskRequest"),
    "jsonrpc/cancel-task.response.json": ("result", "Task"),
}


def fetch_and_strip_proto() -> str:
    os.makedirs(WORK, exist_ok=True)
    raw = urllib.request.urlopen(PROTO_URL).read().decode("utf-8")
    # Drop google/api/* imports (keep google/protobuf/* — bundled with protoc).
    raw = re.sub(r'^\s*import\s+"google/api/[^"]+";\s*$', "", raw, flags=re.M)
    # Drop the entire service block (its rpc options carry all google.api.http use).
    raw = re.sub(r"service\s+A2AService\s*\{.*?\n\}\n", "", raw, flags=re.S)
    # Drop inline field_behavior annotations.
    raw = re.sub(r"\s*\[\(google\.api\.field_behavior\)[^\]]*\]", "", raw)
    out = os.path.join(WORK, "a2a_min.proto")
    with open(out, "w") as f:
        f.write(raw)
    return out


def compile_proto(proto_path: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "grpc_tools.protoc",
         f"-I{WORK}", f"--python_out={WORK}", os.path.basename(proto_path)],
        cwd=WORK, check=True,
    )


def main() -> int:
    import jcs  # RFC 8785

    proto_path = fetch_and_strip_proto()
    compile_proto(proto_path)
    sys.path.insert(0, WORK)
    import a2a_min_pb2 as pb  # generated
    from google.protobuf import json_format

    failures = []

    # 1. proto3-JSON strict validation of every A2A-wire fixture.
    for rel, (field, msg_name) in WIRE_FIXTURES.items():
        with open(os.path.join(HERE, rel)) as f:
            doc = json.load(f)
        payload = doc if field is None else doc[field]
        msg_cls = getattr(pb, msg_name)
        try:
            parsed = json_format.ParseDict(payload, msg_cls(),
                                           ignore_unknown_fields=False)
            # round-trip to confirm presence behavior (esp. optional bool false)
            back = json_format.MessageToDict(
                parsed, preserving_proto_field_name=False,
                including_default_value_fields=False)
            if rel.startswith("cards/"):
                caps = back.get("capabilities", {})
                assert caps.get("streaming") is False, "explicit false must survive"
                assert "extendedAgentCard" not in caps, "unset must stay absent"
            print(f"OK   {rel} -> {msg_name}")
        except Exception as e:  # noqa: BLE001
            failures.append((rel, msg_name, str(e)))
            print(f"FAIL {rel} -> {msg_name}: {e}")

    # 2. card_digest recomputation with a vetted JCS lib.
    for rel in ("cards/per-address-direct-card.json", "cards/byot-router-card.json"):
        with open(os.path.join(HERE, rel)) as f:
            card = json.load(f)
        canonical = {k: v for k, v in card.items() if k != "signatures"}
        digest = "sha256:" + hashlib.sha256(jcs.canonicalize(canonical)).hexdigest()
        print(f"DIGEST {rel}: {digest}")
        # Compare against committed vector if one exists for this card.
        vec = os.path.join(HERE, "digest",
                           os.path.basename(rel).replace(".json", ".digest-vector.json"))
        if os.path.exists(vec):
            with open(vec) as f:
                expected = json.load(f)["card_digest"]
            if expected != digest:
                failures.append((rel, "digest", f"{expected} != {digest}"))
                print(f"  MISMATCH vs vector: {expected}")
            else:
                print("  matches committed vector")

    print()
    print("FAILURES:", len(failures))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
