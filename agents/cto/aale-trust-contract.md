# Trust Verification Contract — Working Draft

Status: draft v0.1, 2026-04-26 (Randy)
Scope: defines the canonical client-side trust verification semantics that
Go CLI and channel TypeScript MUST both implement. Server is data substrate
only — it does not compute verification status.

## 1. Architectural ground truth (from survey)

**Server (data substrate only)**: stores raw signed envelopes + metadata
and returns signed_payload + envelope metadata (from_did, to_did,
from_stable_id, to_stable_id, signature, signing_key_id,
rotation_announcement, replacement_announcement) on inbox/history reads.
Server is NOT a verifier and does NOT compute verification_status. Its
contract obligation under this document is shape conformance — return
the envelope fields each client expects to find, with consistent naming
across mail and chat APIs.

**Client verifiers** (two independent implementations):
1. **Go CLI** (`cli/go/awid/`): runs in `aw mail inbox`, `aw chat history`,
   etc. Pipeline lives in `client.go` + `mail.go` + `chat.go` + `signing.go`.
2. **Channel TypeScript** (`channel/src/identity/trust.ts`): runs in the
   Claude Code plugin's MCP subprocess on each event delivery.

**Drift**: same server-supplied envelope can produce different
VerificationStatus values from these two clients. That drift is the bug
class (aalf, aalg, aale all instances).

## 2. Canonical pipeline (target contract)

For each received message, the verifier runs four passes in order. Any
status-degrading pass short-circuits the rest (no status climbs back up).

### Pass A — Crypto signature

Verify `signature` is a valid Ed25519 signature over `signed_payload`
under the public key extracted from `from_did`. `signing_key_id` is an
equality/selector guard, NOT an independent key source: a non-empty
`signing_key_id` that does not equal `from_did` rejects the message.

Inputs: `signed_payload`, `signature`, `from_did`, `signing_key_id`.
Output: `verified` | `failed`.

Logic:
```
if signing_key_id is non-empty and signing_key_id != from_did: return "failed"
if from_did does not start with "did:key:": return "unverified"
public_key = extractPublicKey(from_did)
if extraction fails: return "failed"
if not Ed25519.verify(public_key, signed_payload, decode(signature)): return "failed"
return "verified"
```

Output: `verified` | `failed` | `unverified`.

Edge cases:
- `signing_key_id` absent OR empty-string → treated identically (no
  selector guard fires; verify with from_did).
- `signing_key_id` present and ≠ `from_did` → `failed` (selector guard).
- `from_did` is not a `did:key:` identity (e.g. `did:aw:`, `did:web:`) →
  `unverified`. We can't perform Ed25519 verification on a non-did:key
  identity; "unverified" means "no claim made," not "tried and failed."
  This matches both Go and TS implementations (banked from N1 in
  John's b990023 gate-read 2026-04-26).
- Signature decode failure (bad base64) → `failed`.
- Public key extraction failure (malformed did:key) → `failed`.
- Signature bytes valid base64 but don't verify against public key → `failed`.

### Pass B — Recipient binding

Confirms the message was addressed to *this* receiver, using stable-id-first
matching with did:key fallback.

Inputs: `verifier.selfDID`, `verifier.selfStableID`, `to_did`, `to_stable_id`,
inbound `status` from Pass A.

Logic (per Go client.go:638-655 reference, MUST be ported to TS):
```
if status != "verified": return status  # pass-through
if selfStableID != "" and to_stable_id != "":
    if equalsCaseInsensitive(to_stable_id, selfStableID): return "verified"
    return "identity_mismatch"
if to_did == "" or selfDID == "": return status  # nothing to check
if to_did != selfDID: return "identity_mismatch"  # case-sensitive
return "verified"
```

**Case-handling rule** (explicit, was implicit in Go EqualFold call):
- `did:aw:` stable_id comparison: case-INSENSITIVE (Go uses `strings.EqualFold`;
  TS must use `.toLowerCase() ===` or equivalent case-folding).
- `did:key:` comparison: case-SENSITIVE (Go uses `!=`; TS uses `===`).

The asymmetry exists because did:aw stable_ids are protocol-canonical
lowercase but historic wire shapes have surfaced mixed-case values; Go's
EqualFold provides defense-in-depth. did:key encodes a public key in
multibase and is unambiguously case-sensitive by spec.

Output: `verified` | `identity_mismatch` (status pass-through if checks
inapplicable).

**This is where current TS diverges from Go**: TS only takes `toDID`;
must add `toStableID` and the stable-first branch. Aalf was the
TX-side analog of this on the dashboard signer; aale-renderer-asymmetry
is the RX-side analog in the channel.

### Pass C — Sender stable-identity registry

If sender claims a stable identity (from_stable_id starts with `did:aw:`),
verify with the awid registry that the stable_id resolves to from_did
(the current did:key claimed in this envelope).

Inputs: `from_did`, `from_stable_id`, `trust_address` (canonical of from
address), `registry` (resolver), inbound `status`.

Logic (Go client.go:387-413):
```
if status != "verified": return status
if from_stable_id == "" or from_did == "" or
   not from_stable_id.startsWith("did:aw:"): return status, false
result = registry.VerifyStableIdentity(trust_address, from_stable_id)
if result.Outcome == HardError: return "identity_mismatch", false
if result.Outcome == Verified:
    if result.CurrentDIDKey != "" and result.CurrentDIDKey != from_did:
        return "identity_mismatch", false
    return "verified", (result.CurrentDIDKey == from_did)
return status, false
```

Output: status, plus `confirmedCurrentKey` boolean for downstream pin
disambiguation.

**Drift to validate**: TS implementation in trust.ts:109-134 looks
structurally similar but registry resolution itself can degrade if the
RegistryResolver wasn't constructed with a working URL — that was the
aalg-class CLI bug and the dd4ef9f channel bug. Ensure both verifiers
treat "registry unavailable" the same way (current behavior: fall through
without changing status).

### Pass D — Local TOFU pin

Pin store: `~/.config/aw/known_agents.yaml` (shared between Go CLI and
channel TS — single store, two writers).

Logic per address+stable_id pair:
- New (no pin): on `verified` or `verified_custodial` status, write pin.
  Status unchanged.
- Match (pin exists, did_key matches): update last_seen. Status unchanged.
- Mismatch (pin exists, did_key differs): check rotation/replacement
  announcements; if valid, accept new key (atomic re-pin); if not,
  `identity_mismatch`.
- Stale (pin exists but registry confirmed different current key): treat
  as silent rotation; if `registryConfirmedCurrentKey == true`, accept
  the registry-confirmed key without requiring announcement.
- Ephemeral lifetime: do not pin; clear any existing pin.
- Custodial custody: status `verified` → `verified_custodial`.

Outputs: final status, `is_contact` boolean (whether sender is in
contact list — display-layer hint, not security-affecting).

### Final status taxonomy

Five possible outcomes (the contract surface):
| status | semantics | UI hint |
|--------|-----------|---------|
| `verified` | Signature valid, recipient bound, registry confirmed, pin OK | "verified" |
| `verified_custodial` | Same as verified but signing identity is custodial-managed | "verified" with custodial annotation if surface differentiates |
| `identity_mismatch` | One of: recipient binding mismatch, registry hard error/mismatch, TOFU pin mismatch without valid announcement | "verified=false" + identity-mismatch flag |
| `failed` | Crypto signature failed, structural failure | "verified=false" + crypto-fail flag |
| `unverified` / undefined | No signed_payload to verify (legacy or unsigned message) | "verified=false" — no claim made |

UI display semantics: `verified` and `verified_custodial` render as a
verified indicator. All others render as not-verified, but the differences
between them MAY be surfaced (mismatch vs failure vs unverified) for
diagnostic purposes — that's a UI choice, not a contract requirement.

## 3. Conformance test format

Test vectors expressed as JSON, loadable by both Go and TS test suites.
Each vector is a complete pipeline input + expected output:

```json
{
  "name": "amy-mail-randy-stable-match-current-key",
  "input": {
    "signed_payload": "{...canonical envelope JSON...}",
    "signature": "base64-...",
    "from_did": "did:key:zXXX",
    "from_stable_id": "did:aw:YYY",
    "to_did": "did:aw:ZZZ",
    "to_stable_id": "did:aw:ZZZ",
    "signing_key_id": "did:key:zXXX",
    "self_did": "did:key:zRRR",
    "self_stable_id": "did:aw:ZZZ",
    "trust_address": "amy.example.com/amy",
    "registry_state": {
      "did:aw:YYY": {"current_did_key": "did:key:zXXX", "outcome": "verified"}
    },
    "pin_store": {},
    "agent_meta": {"lifetime": "persistent", "custody": "self"}
  },
  "expected": {
    "status": "verified",
    "is_contact": null,
    "pin_written": {"did:aw:YYY": "did:key:zXXX"}
  }
}
```

Vectors live in `aweb/test-vectors/trust/` (new directory) as flat
files with version suffix per pass: `recipient-binding-v1.json`,
`crypto-sig-v1.json`, `registry-v1.json`, `tofu-v1.json`. README at
the directory root documents the schema of each pass's vector
format. Both `aweb/cli/go/awid/trust_conformance_test.go` and
`aweb/channel/test/conformance.test.ts` load the same JSON files
and assert.

Pass B vector schema (flat, used by recipient-binding-v1.json):
```json
{
  "name": "<descriptive-name>",
  "initial_status": "verified" | "failed" | "verified_custodial",
  "self_did": "did:key:...",
  "self_stable_id": "did:aw:...",
  "to_did": "did:key:..." | "did:aw:..." | "",
  "to_stable_id": "did:aw:..." | "",
  "expected_status": "verified" | "identity_mismatch" | "failed"
}
```

Pass A/C/D vector schemas will be richer (Pass A needs signature +
signed_payload + decode-failure inputs; Pass C needs registry-state
mock; Pass D needs pin-store mock). Each pass file documents its
own schema; the README tracks which schema-versions are in use.

## 4. Initial vector set (must catch known bugs)

V1: aalf TX-shape — to_did=did:aw, to_stable_id="" (the dashboard bug).
Expected: identity_mismatch. Catches both Go and TS ports of recipient-binding.

V2: aalg sender-side empty resolver — to_did="", to_stable_id="" in
canonical (registry resolver had no URL so signEnvelope produced empty).
Expected: pre-fix verified (no recipient-binding fires); registry pass C
verifies sender. This vector tests that the CLI fix (resolver URL
threading) doesn't break the verifier — it's an emission fix, not a
verifier change.

V3: aale stable-match — to_did=did:aw:ZZZ, to_stable_id=did:aw:ZZZ,
selfStableID=did:aw:ZZZ. Expected: verified. **Pre-fix TS implementation
returns identity_mismatch; this is the aale renderer-asymmetry vector.**

V4: did:key fallback — to_did=did:key:zABC, to_stable_id="",
selfDID=did:key:zABC. Expected: verified.

V5: did:key mismatch — to_did=did:key:zABC, to_stable_id="",
selfDID=did:key:zXYZ. Expected: identity_mismatch.

V6: stable mismatch — to_did=did:aw:WRONG, to_stable_id=did:aw:WRONG,
selfStableID=did:aw:RIGHT. Expected: identity_mismatch.

V7: registry hard-error — sender's stable_id triggers HARD_ERROR from
registry. Expected: identity_mismatch.

V8: registry verified, key match — sender's stable_id resolves to
from_did. Expected: verified, confirmedCurrentKey=true.

V9: registry verified, key mismatch — sender's stable_id resolves to a
different current did:key. Expected: identity_mismatch.

V10: TOFU first-contact — no prior pin; verified status. Expected: pin
written, status verified.

V11: TOFU mismatch without announcement — pin exists for did_key A;
incoming wire claims did_key B; no rotation announcement. Expected:
identity_mismatch, no pin update.

V12: TOFU mismatch with valid rotation — pin exists for A; incoming B;
rotation announcement signed by A. Expected: verified, atomic re-pin to B.

V13: TOFU stale, registry confirms — pin exists for A; incoming B;
registry confirms current key is B (silent rotation, no announcement).
Expected: verified, atomic re-pin to B.

(Continue with edge cases: ephemeral lifetime, custodial custody,
unsigned legacy messages, etc.)

## 5. Implementation plan (rough sequence)

1. **Survey divergences** (this doc, expand): grep both implementations
   for each of the 13+ vectors above; record per-vector behavior in Go
   and TS today.
2. **Test-vector format ratified** (Grace + me).
3. **Initial vector set committed** to `aweb/test-vectors/trust/`.
4. **Go conformance harness** (`aweb/cli/go/awid/conformance_test.go`):
   loads vectors, runs pipeline, asserts. Initially catches gaps.
5. **TS conformance harness** (`aweb/channel/test/conformance.test.ts`):
   same vectors, asserts.
6. **Patch TS to conform**: Grace lands the changes. Driven by failing
   conformance tests.
7. **Patch Go to conform** (if any divergences from canonical surface
   in Go — likely few since Go is the reference, but registry-stale
   handling and some edge cases need confirmation).
8. **Server-side audit** (read-only): confirm server doesn't ALSO
   compute verification_status anywhere. If it does, bring it under
   the same contract.

## 6. Resolved design decisions

Q1 RESOLVED: `signing_key_id` empty-string = absent. Equality guard
fires only on non-empty + non-matching values.

Q2 RESOLVED: Registry-confirmed stale TOFU auto-updates without UI
prompt for now (matches Go behavior). Future UI banner is a separate
display-policy decision, not part of this contract.

Q3 RESOLVED: Test vectors carry explicit `trust_address` field so
address-derivation correctness is tested separately from verifier
semantics. `canonicalTrustAddress` parity gets its own conformance
slice.

Q4 RESOLVED: `verified_custodial` is a distinct status outcome, but
treated as verified-equivalent for display and pin eligibility. Pass D
TOFU treats `verified_custodial` and `verified` the same way for pin
write/match purposes.

Q5 (channel resolver caching) DEFERRED: out of scope for v1 contract.
Performance optimization, not correctness.

## 7. First implementation slice (Grace ratified)

Scope-narrowed first cycle:
1. `aweb/test-vectors/trust/recipient-binding-v1.json` — JSON vectors for
   Pass B only (the smallest pass; covers aalf shape and aale stable-match
   directly).
2. Go harness: `aweb/cli/go/awid/conformance_recipient_binding_test.go`
   loads vectors, calls `NormalizeRecipientBinding(status, toDID, toStableID)`,
   asserts.
3. TS harness: `aweb/channel/test/conformance.recipient-binding.test.ts`
   loads same vectors, calls `SenderTrustManager` recipient-binding pass
   (after the to_stable_id thread-through patch), asserts.
4. TS implementation patch: thread `to_stable_id` into normalizeTrust,
   port the stable-id-first branch into checkRecipientBinding. Driven
   by failing conformance tests, not by narrow Amy-symptom patch.
5. Dispatch regression on Amy-shape mail: confirms the conformance fix
   closes Amy's renderer-asymmetry symptom end-to-end via John's
   reproducer (when it lands).

This subsumes the narrow aale renderer-asymmetry fix into the
conformance-driven path. Subsequent slices follow for Pass A (crypto
sig vectors), Pass C (registry vectors), Pass D (TOFU vectors).

---

**Next**: Grace executes the first slice under standard discipline
(opt-in handshake, code-reviewer subagent gate-read, CTO mailed
approval before any push). I survey empirical drift between current
Go and TS for the next pass slice in parallel.
