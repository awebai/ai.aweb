# A2A v1.0 golden fixtures — SUPERSEDED scratch

> **SUPERSEDED (2026-06-07).** The canonical golden vectors now live in the aweb
> repo at `docs/vectors/a2a-v1.json`, validated by a Go conformance test
> (`cli/go/internal/conformance/conformance_test.go`, commit `d864b7f0`) against
> a JSON schema generated from the pinned A2A proto. These draft card/JSON-RPC/
> bridge files are kept only as provenance; do NOT treat them as authoritative.
>
> The one still-useful tool here is **`validate.py`**, repointed at the canonical
> `docs/vectors/a2a-v1.json`. Its Step 1 is an INDEPENDENT RFC 8785 JCS +
> sha256 cross-check of every card digest — complementary to the aweb Go test,
> which canonicalizes with aweb's own `awid.CanonicalJSONValue`. Step 1 confirms
> `awid.CanonicalJSONValue` agrees byte-for-byte with standard JCS (the property
> external A2A verifiers depend on). a2a ran it 2026-06-07: all 4 cards pass.

Status of the original draft below: **draft, not normative.** Kept for history.

## Source pin
`github.com/a2aproject/A2A` tag **`v1.0.1`**, commit
`3303592588e388e62e0f69f701af531d2f4e3991`, file `specification/a2a.proto`
(package `lf.a2a.v1`). v1.0 is proto-first; JSON Schema is generated from the
proto. Regenerate fixtures with `python3 gen_fixtures.py`.

## Layout
- `cards/` — Agent Cards (validate against `AgentCard`).
- `digest/` — self-checking `card_digest` vector (canonical bytes + sha256).
- `jsonrpc/` — JSON-RPC request/response for SendMessage/GetTask/ListTasks/
  CancelTask, plus a gateway-generated AUTH_REQUIRED task. `params`/`result`
  are proto3-JSON of the matching proto messages.
- `bridge/` — aweb bridge envelopes (gateway-local, NOT A2A wire), including the
  three negative cases that encode Athena's rulings.

## Encoding invariants exercised here
- proto3-JSON lowerCamelCase field names.
- Enums serialize as the NAME string (`TASK_STATE_*`, `ROLE_USER`).
- `Task.status.state` is **nested** — there is no top-level `state`.
- `SendMessageResponse` is a `oneof {task|message}` — async path uses `task`.
- `ListTasksResponse` carries the required `nextPageToken/pageSize/totalSize`.
- Cards omit empty optional maps/lists; advertise `streaming/pushNotifications`
  = false explicitly (JSON presence is intentional).
- `a2a-reply` carries `task_id` (Athena ruling #1).

## card_digest canonicalization (Athena, 2026-06-07) — ONE shared function
`card_digest = "sha256:" + lowercasehex( sha256( JCS(card without signatures) ) )`
where the card has had A2A v1.0 field-presence/default cleanup applied
(required stay; optional only if explicit; empty optional maps/lists omitted;
proto-default scalars omitted unless deliberately advertised). The SAME
canonical function is used for card signing, AWID digest, and tests — never two
forms.

## KNOWN CAVEAT — must resolve before vectors are normative
No `buf`/`protoc` was available here, so cards are hand-authored to the proto and
`jcs()` in `gen_fixtures.py` is a faithful-but-unverified RFC 8785 implementation
for this data (strings/booleans/objects/arrays; no floats, so ECMAScript number
formatting is untested). Before these digests are treated as canonical:
1. Round-trip every fixture through real protojson (`google.protobuf.json_format`
   or Go `protojson`) against the compiled `v1.0.1` proto.
2. Replace `jcs()` with a vetted RFC 8785 library.
3. If the real toolchain preserves/drops any field differently (e.g. whether a
   proto-default `false` is emitted), follow the toolchain and record the exact
   behavior here. The digest will change if field presence changes.

## Open items
- Tier-1 signed-card fixture (JWS over canonical bytes) needs a test key — defer.
- Confirm whether the JSON-RPC `params` should include an (empty) `tenant`
  field for the JSONRPC binding, or omit it (aweb path-routes per /rpc URL).
