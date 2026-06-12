# Proposal: independent-JCS guard for A2A card canonicalization

Status: follow-on candidate (NOT an `aweb-aaqa.1` reopen — .1 is closed).
Scope: narrow, single-purpose. Drafted by a2a per Athena's request 2026-06-07.

## Problem (one sentence)
The aweb A2A conformance test recomputes card canonical bytes + digests with
`awid.CanonicalJSONValue` and compares to vectors that were ALSO produced by
`awid.CanonicalJSONValue` — a self-consistency guard that cannot detect
`awid.CanonicalJSONValue` drifting away from standard RFC 8785 JCS.

## Why it matters
A2A Tier-2 verification by EXTERNAL (non-aweb) clients canonicalizes cards with
standard JCS to check `card_digest`. If `awid.CanonicalJSONValue` ever diverges
from RFC 8785 (key-sort edge case, string escaping, a future number field, etc.),
aweb-issued digests stop verifying for external A2A verifiers — a silent Tier-2
interop break. a2a confirmed equality holds TODAY (stdlib RFC8785 JCS reproduces
all 4 card `canonical_no_signatures` byte-for-byte; sha256 matches every digest).
This guard makes that equality a regression test, not a one-time check.

## Proposed shape (small)
Add ONE assertion to the existing per-card loop in
`cli/go/internal/conformance/conformance_test.go` (the loop at ~L400-423 that
already does `awid.CanonicalJSONValue(cardForDigest)`):

```go
// independent RFC 8785 cross-check: aweb canonicalizer must equal standard JCS
cardJSON, _ := json.Marshal(cardForDigest)          // any JSON encoding; JCS re-canonicalizes
indep, err := jcs.Transform(cardJSON)               // github.com/gowebpki/jcs
if err != nil { t.Fatal(err) }
if string(indep) != canonical {                     // canonical = awid.CanonicalJSONValue(...)
    t.Fatalf("awid canonicalizer diverged from RFC8785 JCS:\n awid: %s\n jcs:  %s", canonical, indep)
}
```

That single equality (`awid == standard-JCS`) is the whole guard. The existing
`sha256(canonical) == digest` assertion already covers the digest math, so this
just pins the canonicalizer to the standard. Apply to all 4 card vectors;
optionally also to any digest-bearing AWID publication-assertion payload that
external verifiers will hash.

## Dependency options (ranked)
1. **`github.com/gowebpki/jcs`** (recommend) — pure-Go RFC 8785 reference impl,
   Debian-packaged, single small dep, `Transform([]byte) ([]byte, error)`. Keeps
   the guard inside the existing Go conformance test; no new toolchain. Verify
   exact API/version at adoption.
2. `github.com/cyberphone/json-canonicalization/go` — the RFC author's own Go
   reference; equally valid, slightly less idiomatic import path.
3. `github.com/ucarion/jcs` — passes all JCS spec-author test data; viable.
4. Python adjunct (`jcs` pip pkg or the stdlib check in
   `agents/a2a/fixtures/validate.py` Step 1) as a CI step — works but adds Python
   to a Go test path. Only if no Go lib is acceptable. NOT preferred.

## Where it lives
Extend `cli/go/internal/conformance/conformance_test.go` (option 1/2/3). Do NOT
add a separate script unless a Go lib is rejected; a separate Python CI job is
strictly worse for a one-line equality check.

## Non-goals
- Not a general JCS conformance suite (the chosen lib already passes RFC8785
  test vectors upstream).
- Not number-format hardening today (cards have no numbers); the guard will
  simply catch it if a numeric field is ever added.
- Not coupled to Tier-1/JWS (deferred until a test-key shape is chosen).

## Effort
~1 dependency add + ~6 lines in an existing test loop. Low.

## Dependency health check — `github.com/gowebpki/jcs` (verified 2026-06-07)
Pre-clears Athena's precondition before adoption under `aweb-aaqa.11`:
- **API**: `func Transform(jsonData []byte) ([]byte, error)` — matches the sketch.
- **Runtime deps**: stdlib only (`container/list, errors, fmt, strconv, strings,
  unicode/utf16`). No external runtime dependency tree.
- **go.mod require**: only `github.com/stretchr/testify v1.7.0` — TEST-scoped;
  aweb's Go module almost certainly already pulls testify. Confirm at adoption;
  if absent it's a trivial standard add, not a heavy tree.
- **License**: Apache-2.0 (permissive, compatible).
- **Health**: 0 open issues, not archived, `go 1.15`+; last push Oct 2023.
  Low churn is expected — RFC 8785 is a frozen spec, so a vector-passing
  canonicalizer is "done", not abandoned. Acceptable, low-risk pick.
Re-verify version/API at adoption time; pin a specific tag.
