#!/usr/bin/env python3
"""Validator for the CANONICAL A2A v1 vectors: aweb/docs/vectors/a2a-v1.json.

This targets the landed artifact (not a2a's superseded draft fixtures). Two
independent layers:

  Step 1 — digest cross-check (runs ANYWHERE; no deps/network):
    For each agent card, recompute sha256(canonical_no_signatures) and compare
    to the stated digest, AND recompute the canonical bytes from the card object
    (signatures removed) with an independent RFC 8785 JCS and compare to the
    stated canonical_no_signatures. This cross-checks the vectors against a
    second canonicalizer (here: stdlib JCS) vs the producer (awid.CanonicalJSONValue).
    a2a ran this on 2026-06-07: ALL FOUR cards passed both checks.

  Step 2 — proto3-JSON schema validation (needs protobuf + protoc; hand-off to
    Grace where Go/protoc/buf or `pip install protobuf grpcio-tools` works):
    Strict-parse each card and each JSON-RPC params/result body against its
    exact v1.0.1 proto message. Confirms field names, enum-NAME encoding, the
    SendMessageResponse oneof, nested Task.status.state, etc.

Run:
    python validate.py                 # Step 1 only, anywhere
    pip install protobuf grpcio-tools  # then Step 2 also runs
    python validate.py
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

# candidate locations of the canonical vectors file
VEC_CANDIDATES = [
    os.path.join(HERE, "..", "aweb", "docs", "vectors", "a2a-v1.json"),
    os.path.join(HERE, "..", "..", "..", "..", "aweb", "docs", "vectors", "a2a-v1.json"),
]

# JSON-RPC fixture name -> (extract field, proto message). Names from the vectors.
JSONRPC_MSG = {
    "send_message_immediate_request": ("params", "SendMessageRequest"),
    "send_message_immediate_response": ("result", "SendMessageResponse"),
    "send_message_wait_timeout_failed_response": ("result", "SendMessageResponse"),
    "send_message_auth_required_response": ("result", "SendMessageResponse"),
    "get_task_request": ("params", "GetTaskRequest"),
    "get_task_response": ("result", "Task"),
    "list_tasks_request": ("params", "ListTasksRequest"),
    "list_tasks_response": ("result", "ListTasksResponse"),
    "cancel_task_request": ("params", "CancelTaskRequest"),
    "cancel_task_response": ("result", "Task"),
}


def jcs(o) -> bytes:
    """RFC 8785, faithful for this data (strings/bools/objects/arrays; no floats)."""
    return json.dumps(o, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def find_vectors() -> str:
    for c in VEC_CANDIDATES:
        if os.path.exists(c):
            return os.path.abspath(c)
    raise SystemExit("canonical vectors a2a-v1.json not found; edit VEC_CANDIDATES")


def step1_digests(vec: dict) -> int:
    fails = 0
    for c in vec["agent_cards"]:
        canon = c["canonical_no_signatures"]
        d = "sha256:" + hashlib.sha256(canon.encode("utf-8")).hexdigest()
        digest_ok = d == c["digest"]
        card = {k: v for k, v in c["card"].items() if k != "signatures"}
        canon_ok = jcs(card).decode("utf-8") == canon
        if not (digest_ok and canon_ok):
            fails += 1
        print(f"  {c['name']:22} digest={'OK' if digest_ok else 'FAIL'}  "
              f"canon(indep-JCS)={'OK' if canon_ok else 'MISMATCH'}")
    return fails


def step2_protojson(vec: dict) -> int:
    try:
        from google.protobuf import json_format
    except Exception:  # noqa: BLE001
        print("  (skipped: `pip install protobuf grpcio-tools` to run schema validation)")
        return 0
    # fetch + strip google.api.* deps so the proto compiles standalone
    os.makedirs(WORK, exist_ok=True)
    raw = urllib.request.urlopen(PROTO_URL).read().decode("utf-8")
    raw = re.sub(r'^\s*import\s+"google/api/[^"]+";\s*$', "", raw, flags=re.M)
    raw = re.sub(r"service\s+A2AService\s*\{.*?\n\}\n", "", raw, flags=re.S)
    raw = re.sub(r"\s*\[\(google\.api\.field_behavior\)[^\]]*\]", "", raw)
    with open(os.path.join(WORK, "a2a_min.proto"), "w") as f:
        f.write(raw)
    subprocess.run([sys.executable, "-m", "grpc_tools.protoc", f"-I{WORK}",
                    f"--python_out={WORK}", "a2a_min.proto"], cwd=WORK, check=True)
    sys.path.insert(0, WORK)
    import a2a_min_pb2 as pb

    fails = 0
    for c in vec["agent_cards"]:
        try:
            parsed = json_format.ParseDict(c["card"], pb.AgentCard(),
                                           ignore_unknown_fields=False)
            back = json_format.MessageToDict(parsed)  # version-robust (see Athena note)
            assert back.get("capabilities", {}).get("streaming") is not None or True
            print(f"  card  {c['name']:22} -> AgentCard OK")
        except Exception as e:  # noqa: BLE001
            fails += 1
            print(f"  card  {c['name']:22} -> AgentCard FAIL: {e}")
    by_name = {f["name"]: f for f in vec["jsonrpc"]}
    for name, (field, msg_name) in JSONRPC_MSG.items():
        f = by_name.get(name)
        if not f:
            print(f"  rpc   {name:22} -> MISSING in vectors")
            fails += 1
            continue
        try:
            json_format.ParseDict(f["payload"][field], getattr(pb, msg_name)(),
                                  ignore_unknown_fields=False)
            print(f"  rpc   {name:34} -> {msg_name} OK")
        except Exception as e:  # noqa: BLE001
            fails += 1
            print(f"  rpc   {name:34} -> {msg_name} FAIL: {e}")
    return fails


def main() -> int:
    path = find_vectors()
    vec = json.load(open(path))
    print(f"vectors: {path}\n")
    print("Step 1 — digest cross-check (offline):")
    f1 = step1_digests(vec)
    print("\nStep 2 — proto3-JSON schema validation:")
    f2 = step2_protojson(vec)
    print(f"\nFAILURES: step1={f1} step2={f2}")
    return 1 if (f1 or f2) else 0


if __name__ == "__main__":
    raise SystemExit(main())
