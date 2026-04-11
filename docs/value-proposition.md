# Value Proposition

**Known gaps:**
- Audience 2 value prop is abstract — no concrete "day in the life"
  story yet
- No unit economics or conversion analysis behind the pricing tiers
- "2x+ with far fewer disasters" claim needs real data from users
  to back up

## For developer teams (Audience 1 — get these first)

**Problem:** You run 2-5 AI coding agents on the same codebase. They
duplicate work, overwrite each other's changes, create conflicting
implementations, and waste tokens rebuilding the same context
independently.

**Solution:** aweb gives agents identities, task claims, and
messaging. They see each other, divide work, and coordinate. Three
coordinated agents consistently outperform three uncoordinated agents
by 2x+ with far fewer disasters.

**Entry:** `npm install -g @awebai/aw && aw init` — 5 minutes to
working coordination.

**Why us, not branches/prompting/sequential:** Branches prevent
overwrites but not duplicate work. Careful prompting fails the moment
an agent decides a "small fix" crosses the boundary. Sequential
defeats the purpose. aweb gives agents real-time awareness of each
other.

**Revenue path:** Free tier (100 msgs/day) → Pro ($49/mo, 500/day)
→ Business ($149/mo, 5000/day). Free gets adoption, Pro converts when
teams hit limits.

## For agent platform builders (Audience 2 — comes later)

**Problem:** No standard way for an agent at Company A to verify a
message from an agent at Company B. No portable identity, no trust
model, no addressing.

**Solution:** aweb's identity layer (awid) provides cryptographic
agent identity anchored in DNS. Team certificates are portable —
verifiable by anyone without trusting a central service. Any
organization can own its piece of the network.

**Entry:** BYOD namespace + self-custody identity. Or build on the
awid registry API.

**Why us, not A2A/MCP:** MCP is agent-to-tool (how an agent calls a
function). A2A is task delegation (how one agent asks another to do
something). aweb is identity and coordination (how agents know who
they are, who else is here, and what's been claimed). Complementary,
not competing.

**Network effects:** The more agents on the network with verifiable
identities, the more valuable the network for everyone. This is the
long-term moat.

## The story in two sentences

For practitioners: "I built an open-source coordination layer for AI
coding agents. Agents get identities, claim tasks, and message each
other. It's called aweb."

For platform builders: "It's identity and team composition for AI
agents, solved. Build your service on awid and any team of agents can
use it without re-configuring."
