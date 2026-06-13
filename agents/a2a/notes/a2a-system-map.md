# aweb A2A — system map: implemented vs specced (verified 2026-06-12)

Code-grounded map of how our A2A actually works, for non-aweb (generic) and
aweb-aware (AWID-verified) callers. Built by reading the three normative
contracts AND the Go/Python implementation, not from memory. Cross-checked
doc-vs-code. The load-bearing distinction is **IMPLEMENTED vs SPECCED-ONLY** —
the contracts describe far more than is wired today.

Sources:
- Contracts: `aweb/docs/a2a.md` (master), `a2a-ac-managed-gateway-contract.md`
  (control plane), `a2a-awid-publication-contract.md` (trust layer).
- Protocol pin: A2A v1.0.1, commit 3303592 — see [[a2a-v1-source-pins]].
- Operational bring-up: [[a2a-hackathon-bringup]].

## The three planes

1. **Control plane — AC (`app.aweb.ai`)**: owns route records, card config,
   gateway-identity custody, AWID publication/delegation state. Hosted source of
   truth. (`a2a-ac-managed-gateway-contract.md`. Lives in the `ac` repo — NOT
   read yet; the aweb-side gateway consumes its config API.)
2. **Data plane — gateway (`aweb-a2a-gw`, `a2a.aweb.ai`)**: serves cards +
   JSON-RPC, bridges A2A tasks to real agents over durable aweb mail.
   `aweb/cli/go/a2agw/`.
3. **Trust layer — AWID (`api.awid.ai`)**: durable identity/address/publication/
   delegation registry. `aweb/cli/go/awid/a2a_publication*.go` +
   `aweb/awid/src/awid_service/routes/a2a_publications.py`.

## NON-AWEB (generic A2A) path — FULLY WORKING (Tier 0)

This is what the hackathon and any standard A2A client use. No AWID needed.

- **JSON-RPC methods** (`a2agw/rpc.go:133`): `SendMessage`, `GetTask`,
  `ListTasks`, `CancelTask` implemented. `SendStreamingMessage` +
  `SubscribeToTask` → `-32601 method not found`. Strict v1.0 names; no pre-1.0
  aliases (`message/send`) accepted.
- **Task states** (`a2agw/task.go:15`): the 8 `TASK_STATE_*` SCREAMING_SNAKE
  values. `TASK_STATE_CANCELED` is **one L** (confirmed in code) — matches the
  contract, vectors, and upstream A2A v1.0. State nests at `task.status.state`;
  task ids are UUIDv4.
- **SendMessage flow** (`rpc.go:148`): create `SUBMITTED` → if auth required
  `AUTH_REQUIRED` + return → bridge `SendTask` → `WORKING` → if
  `returnImmediately` absent/false, wait up to `response_timeout_s`; on timeout
  → `TASK_STATE_FAILED` ("timed out before… terminal or interrupted reply").
- **Caller scoping / anonymous isolation** (`rpc.go`, `task.go`):
  unauthenticated caller = `anonymous:unscoped`. Each task carries a 64-hex
  **`X-A2A-Task-Token`** (in `task.metadata`). `ListTasks` **rejects** anonymous
  callers (`-32003 requires an isolated caller scope`). `message.role` must be
  `ROLE_USER` (empty allowed, agent role rejected).
- **Token-free `GetTask` on public routes (gateway ≥ `a2a-gw-v1.26.19`, commit
  `d0baafa3`, "restrict public A2A task lookup to anonymous tasks").** `GetTask`
  first tries token/scope `getVisible`; on miss, if `publicAnonymousTaskLookupAllowed`
  (route auth `none` + caller `anonymous:unscoped`) it falls back to
  `getPublicAnonymous`, which returns the task **only if it was created
  anonymously** (`CallerScope == "anonymous:unscoped"`). So on public routes the
  `X-A2A-Task-Token` is **OPTIONAL** (still supported; still required to read
  authenticated tasks). **A stock `a2a-sdk` (python 1.1.0) completes the default
  SendMessage→poll-GetTask flow with ZERO aweb extensions** — clean standard-A2A
  conformance. Bounded: token-free reads can't reach authenticated tasks, and
  task ids are UUIDv4. Pre-`d0baafa3` (≤v1.26.14) token-free GetTask returned
  `task_not_found`. Verified at code level 2026-06-13 via origin/main +
  rose's live run; see [[verify-against-released-binary-not-stale-checkout]].
- **Mail bridge** (`a2agw/mail_bridge.go`): sends fenced `a2a-task` envelope
  (task_id, context_id, route_id, target_address, gateway_identity,
  callerScope, state, request_id) + untrusted customer text; polls the
  conversation every 500ms for an `a2a-reply` fence. Reply rules enforced:
  `task_id` REQUIRED; `context_id` must match when inbound had one (else
  ignored, never mutates); terminal states final (late reply ignored); unfenced
  prose = non-terminal (stays WORKING); state aliases normalized
  (`completed`↔`TASK_STATE_COMPLETED`, etc.); `QUESTION:` is a feature-flagged
  shortcut.
- **Rate limiting** (`a2agw/rate_limit.go`): `N/s|N/m|N/h`, per route+caller,
  sliding window, `-32029 rate limited`.
- **Generic client** = jack's `client.py` ([[a2a-hackathon-bringup]] Appendix A)
  + the Go `aw a2a` client.

## AWEB-AWARE (AWID trust) path — PRODUCER + SERVER-WRITE DONE; CLIENT-READ + RUNTIME ENFORCEMENT NOT

This is the differentiator ("normal A2A for generic clients, stronger
verification for aweb-aware"). Status is **partial** — be precise about it.

### What IS implemented
- **Producers** (`cli/go/awid/a2a_publication.go` + `awid/src/awid/a2a_publication.py`):
  build/sign/canonicalize publication (`publish_a2a_route`) and delegation
  (`delegate_a2a_bridge`) assertions, Ed25519, on BOTH Go and Python; canonical
  bytes match `docs/vectors/a2a-awid-publication-v1.json` byte-for-byte (tested).
- **Digest encodings** (distinct, do NOT unify): `card_digest` =
  `sha256:<lowercase-hex>` of JCS(card minus `signatures`) via
  `a2a.CardDigest` (`cli/go/a2a/card.go:248`, matches `a2a.md §5.2`).
  `delegation_digest`/`assertion_digest` = `sha256:<base64-raw-std-no-pad>` of
  `SHA256(canonical || decoded_sig)`.
- **Server-side WRITE verifier** (`awid_service/routes/a2a_publications.py`) is
  COMPLETE: signature verify, did:aw key-history chain (current key at
  `published_at`), digest match, expiry, revocation, custody/authority matrix,
  address registration, 5-min timestamp skew, all **21 conflict codes**, 90-day
  route cap, natural-key idempotency. Migration `007_a2a_publications.sql`
  (tables `a2a_route_publications`, `a2a_bridge_delegations`).
- **`aw a2a publish`** (`cmd/aw/a2a.go:351`): full flow — fetch card, compute
  digest, load self-custodial key, publish delegation (if gateway≠self) then
  publication, verify back through AWID.
- **`aw a2a card --address`** Tier-2 read cross-check (`a2a.go:257`): fetches
  publication, checks active + `card_digest` match + url match → reports
  `Tier2 / awid_publication_verified`.

### What is NOT implemented (the real gaps)
- **Gateway runtime AWID enforcement = NONE.** `a2agw` checks the configured
  `card_digest` only at **init** (`gateway.go:174`); per-request it does NO
  publication/delegation/expiry/revocation/identity check. `VerificationTier` is
  **hardcoded `"unsigned"`** (`gateway.go:366`). The data plane runs as Tier 0
  regardless of AWID state. (Matches roadmap: AWID enforcement = Phase 5.)
- **Client-side READ verifier is shallow.** `aw a2a card` does NOT reconstruct
  canonical bytes, re-verify the publication signature, re-check key history, or
  verify the delegation on read — it trusts the AWID GET response's fields. The
  full 10-step verifier in `a2a-awid-publication-contract.md §Verification Rules`
  is server-write-only, not client-read.
- **JWS card signatures NOT verified.** `aw a2a card` flags any signed card as
  unsigned Tier 0: "aw a2a does not verify JWS yet" (`a2a.go:240`). Tier 1
  (card-integrity) is effectively absent.
- **Crypto fixtures are PLACEHOLDER.** `a2a-awid-publication-v1.json` signatures
  are deterministic placeholder bytes (canonical/digest fixture only). Real
  Ed25519 verification fixtures = **aaqa.8**, still pending. No verifier should
  ship claiming crypto-verified until then.
- **`aw a2a send --wait` does NOT poll.** Sets `returnImmediately=false` and
  relies on the gateway's server-side wait; there is no client GetTask polling
  loop and no streaming. (Gap vs `a2a.md §12`.)
- **Tenant-routed cards** rejected by `aw a2a` ("not supported yet").

## Trust-tier reality (say this plainly to anyone asking)

| Tier | Contract guarantee | Implemented today? |
|---|---|---|
| 0 (plaintext bridge) | generic A2A interop | YES — fully |
| 1 (card JWS) | card integrity | NO — "does not verify JWS yet" |
| 2 (AWID publication+digest+delegation+key-history) | durable identity/address binding | PARTIAL — producers + server-write done; runtime gateway enforcement + client read-verify + real crypto fixtures NOT done |

**No customer-facing `verified` / `AWID-backed` / `authorized for address`
claim is allowed until runtime enforcement + real crypto land** — guarded by
copy-guardrail CI (`scripts/check-a2a-copy-guardrails.sh`) and the release
runbook gates. The hosted gateway is a **plaintext boundary**; never call it
E2EE.

## HTTP timeouts / `AWEB_HTTP_TIMEOUT` (corrected 2026-06-12)

The released CLI **does** honor `AWEB_HTTP_TIMEOUT` (an earlier answer of mine
said it didn't — that was off a stale checkout; see [[verify-against-released-binary-not-stale-checkout]]).

- `awid.APITimeout()` (`cli/go/awid/http_transport.go:27`, aaqm hardening
  commits `be6db091`/`acda65fd`) reads `AWEB_HTTP_TIMEOUT` as a **Go duration**
  (`30s`, `1m`). Invalid or bare-integer (`30`) → warn-once to stderr + fall
  back to `DefaultTimeout`.
- `DefaultTimeout` = **20s** in released `aw 1.26.18`, raised to **30s** on
  origin/main (`e5adf5ec`) → ships as `1.26.19`.
- Applied as `ResponseHeaderTimeout` on the tuned API transport (the venue
  "awaiting headers" failure class). The `aw a2a` path also uses
  `NewAPITransport()` so its header-wait follows the env; its outer
  `http.Client.Timeout` stays 30s, and per-command contexts cap at 30s (send/
  status/cancel), 90s (send --wait), 45s (publish).
- Hackathon levers: `export AWEB_HTTP_TIMEOUT=30s` on 1.26.18 now, or upgrade to
  1.26.19 where 30s is the default.

## Boundaries / not-yet-read
- **My local aweb sibling checkout drifts behind origin.** It was 20 commits
  behind when I wrote the first draft of this map, which produced a wrong
  timeout answer. For "does the RELEASED binary do X" questions, check the
  binary (`aw ...` at runtime) or `origin/main`/the release tag — NOT my local
  working tree. See [[verify-against-released-binary-not-stale-checkout]].
- The `ac` repo control-plane implementation (route CRUD, gateway-identity
  custody, config API) — only the *contract* is read, not the AC code. If asked
  about hosted route management internals, verify against `ac` before asserting.
- Native aweb A2A transport binding (E2EE) — explicitly deferred, spec-only.
