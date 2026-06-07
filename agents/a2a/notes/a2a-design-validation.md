# docs/a2a.md design validation (2026-06-07)

Question asked: does the design actually make sense (not just match the wire)?
Verdict: **the core bet is sound and honestly scoped.** Six real issues below,
severity-ranked. None invalidate the approach; #1, #2, #5 must be resolved
before the bridge (Phase 4) ships; #6 is a sequencing judgment call.

## What is right (don't relitigate)
- "Normal A2A for generic clients, AWID trust for aware clients" — the central
  bet holds. A2A genuinely leaves naming/identity/publication open; AWID fills
  exactly that gap. Generic clients are unaffected. Honest, not overclaimed.
- Gateway owns the stateful A2A task store; aweb stays message-passing. Right
  separation — A2A task lifecycle does NOT belong inside aweb.
- Gateway has its own identity + on-behalf-of + never holds BYOT keys;
  delegation in AWID. Correct custody model.
- Plaintext-boundary honesty; native E2EE binding deferred. Correct YAGNI.

## Issues

### 1. Reply→task correlation is unspecified; `a2a-reply` lacks task_id [CORRECTNESS]
Inbound `a2a-task` (§10.1) carries task_id/context_id. The reply `a2a-reply`
(§10.2) carries only `state` + `artifacts`. So the gateway can only correlate a
reply to a task via the aweb thread. But Open Q#4 (mail vs chat thread as the
durable primitive) is unresolved, and a single agent handling two concurrent
A2A tasks can mis-correlate replies. **Fix:** require the agent to echo task_id
(and context_id) in the reply envelope, OR mandate strict one-thread-per-task
and correlate by thread id. Don't ship the bridge without one of these pinned.

### 2. Unfenced reply → COMPLETED is unsafe for real agents [CORRECTNESS]
§10.2: "No structured block → TASK_STATE_COMPLETED, body as text artifact."
Real Claude-Code agents routinely emit conversational prose ("on it…", a
clarifying aside, a refusal). Under this rule every such stray line silently
COMPLETES the task with garbage as the answer. This directly undercuts the
stated "zero-SDK, real aweb agents" goal — the zero-SDK ergonomic is the thing
that makes it unreliable. **Fix:** require the fence for any *terminal* state;
treat unfenced output as still-WORKING (or a structured "missing reply
envelope" condition), never auto-COMPLETED. Inject the reply protocol firmly
into bridged-agent instructions.

### 3. Sync-path late reply after timeout-FAIL mutating a terminal task [CORRECTNESS]
§9.2: returnImmediately false/absent → wait; on route timeout → TASK_STATE_FAILED
(terminal). If the agent's real reply arrives at t+timeout+ε, it would either be
dropped or illegally revive a terminal task. A2A terminal states are final.
**Fix:** specify that replies arriving after a terminal state are dropped or
spawned as a fresh task; never mutate a terminal task. (The async path —
returnImmediately:true + poll GetTask — sidesteps this, which is why the doc
rightly steers there; the sync path's late-reply rule still needs stating.)

### 4. card_digest canonicalization is the interop-critical unsolved piece [INTEROP]
Open Q#2 ("exact canonical digest bytes") is treated as a loose end but it is
THE thing that decides whether Tier-2 is interoperable. Two implementations
with different canonicalization compute different digests → Tier-2 mutually
rejects. Worse, the doc has TWO canonicalization concerns: card *signature*
(§7.1, "A2A/JCS, signatures field absent") and card *digest* (§6.2). **Fix:**
unify them — `card_digest` = hash over the *same* A2A-v1.0 card-signature
canonical bytes (JCS, signatures absent), one canonical form, pinned in
fixtures with byte-exact vectors. Make this a blocking design item for Phase 5,
not an open question.

### 5. Agent wake path is core architecture, not a peripheral open question [VIABILITY]
Open Q#5 (gateway wake path for Hetzner agents). The entire bridge assumes a
real agent wakes on an aweb message and replies inside the route window
(e.g. 120s). If agents aren't always-on inbox-pollers, *something* must wake
them per inbound task within the timeout. This determines whether the product
works at all. **Fix:** promote to a decided architecture item before Phase 4 —
define the wake mechanism (long-running poller? push/trigger? aweb channel
event like the one that woke me?) and its latency budget vs route timeout.

### 6. The differentiator (AWID trust) ships last [SEQUENCING — judgment]
Phases 1–4 deliver a plain A2A gateway with operator-configured, explicitly
*unverified* routes (§8.2). The actual aweb differentiation — AWID publication,
delegation, digest, Tier-2 — is all Phase 5. So the first shipped slice (and the
hackathon) is "just another A2A gateway," and the hard, risky, novel part is
deferred. Two pulls: YAGNI says don't build AWID before demand; but the digest/
canonicalization/delegation work (#4) is the highest-risk unknown and proving it
on ONE route early de-risks the whole bet and validates the differentiator.
**Recommend:** pull a minimal AWID publication+Tier-2 check for a single route
forward (overlap into Phase 4) rather than fully sequential, so the
differentiating claim is proven, not assumed. Strategic — flag to Sofia/Athena.

## Minor
- AUTH_REQUIRED state missing from §3.1 + §10.2 reply aliases (Athena: add it).
- No `auth_required` alias in the reply-envelope `state` set, yet auth modes
  exist (§12). Add alongside #minor above.
