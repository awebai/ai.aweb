# docs/a2a.md design summary (read 2026-06-07, doc v0.2)

Source: `aweb/docs/a2a.md` @ f5db1667+ (Grace/Athena/Juan). Pin contract.

## The bet
A2A standardizes *how to talk to an agent once you have its card*. It leaves
*naming, durable identity, trust, publication* open. aweb/AWID fill that.
Design principle: **normal A2A for generic clients; stronger verification for
aweb-aware clients.** Not "aweb competes with A2A."

## Four pieces
1. **Gateway `aweb-a2a-gw`** — real service. A2A JSON-RPC in → durable aweb
   message to a real aweb agent → agent replies via aweb → gateway updates the
   A2A task. Stateful task store lives in the gateway (A2A statefulness is NOT
   pushed into aweb).
2. **AWID A2A publication assertions** — registry facts binding address →
   card_url/rpc_url/route_id/gateway_identity/card_digest/revision/expiry/
   delegation. AWID is the trust registry, not the runtime card host.
3. **Signed/delegated cards + verification tiers** — Tier0 ignore, Tier1 verify
   card JWS, Tier2 verify AWID publication+digest+delegation+key-history.
4. **Outbound `aw a2a`** — CLI to inspect/call external A2A agents, Tier-2 aware.

## Discovery
- Standard well-known: only `https://{host}/.well-known/agent-card.json`
  (default agent OR router card; MUST NOT silently pick a default among many).
- Per-address direct card: `/a2a/agents/{route_id}/agent-card.json` (not
  well-known).
- Per-address JSON-RPC: `/a2a/agents/{route_id}/rpc` (single endpoint, method
  in body — correct for the JSONRPC binding). tenant omitted on direct cards.

## Bridge envelopes
- Inbound to agent: fenced ```a2a-task``` block (task_id, context_id, route_id,
  target_address, gateway_identity, caller_id, state) + customer text.
- Reply from agent: fenced ```a2a-reply``` block (state + artifacts). `QUESTION:`
  prefix = input_required (compat sugar). No block = COMPLETED, body as text.

## Custody / boundary
- Gateway has its OWN aweb/AWID identity; visible on-behalf-of; never holds a
  self-custodial/BYOT agent's private key. Trusted routes use gateway identity
  + AWID delegation.
- Gateway is a **plaintext boundary**. Hosted bridge is NOT E2EE. Native E2EE
  aweb transport binding is explicitly deferred.

## Phasing
1 spec+fixtures · 2 gateway+cards · 3 JSON-RPC task store · 4 aweb bridge
adapter (first 3 Hetzner agents) · 5 AWID publication+delegation+Tier2 ·
6 streaming+auth+hardening. Native binding deferred.

## Open questions the doc itself lists (§16)
A2A schema source+tooling; exact canonical digest bytes; is ListTasks required;
mail vs chat as durable primitive; gateway wake path for Hetzner agents; auth
for public routes; minimal AWID publication before launch.
