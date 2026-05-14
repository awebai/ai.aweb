# Iris Handoff

Last updated: 2026-05-14 (welcome-guide v2 + serverInfo v2 in review)

## Operating focus

Use `../../publishing/runbook.md` first. Outreach work is case-based:
classify the situation, read only the references needed for that
case, produce a human-ready artifact, and record action/signal with
attribution limits.

You author. Juan and Eugenie publish. Sofia frames, Athena tech-
accuracy, Aida support-integration where applicable, Hestia deploys.
Sensitive contacts/targets stay in `co.aweb/`.

## Active work

### 1. MCP onboarding artifacts (today's primary)

Two parallel surfaces in flight for Athena/Grace's hosted-MCP welcome
shipment:

- **Welcome guide v2** — `publishing/drafts/2026-05-14-aweb-welcome-guide-v1.md`
  (committed 007f33b). ~440 words, within Athena's 200-500 target.
  Returns from the MCP `aweb_welcome_guide` tool; mirrored to docs.
  Folds Aida's pre-think (vocabulary, pending-vs-active lifecycle as
  load-bearing for trust, default-reachability, re-fetch tool entry).
  Review chain: Sofia framing → Athena tech-accuracy (pending Grace's
  tool-name lock) → Aida support-integration → Juan bless → commit
  at canonical path (TBD pending Grace's mount-path trace).

- **serverInfo.instructions v2** — proposed in mail to Sofia
  (00f88031, in conversation 345f95bb). 447 chars, under 500 cap.
  AI-facing, semi-spec; (a) aweb framing, (b) smallest-first-action
  prompt, (c) tools list + vocabulary guard. Awaiting Sofia's
  converge-or-revise. Once converged → Athena tech-accuracy → Grace
  wires into FastMCP constructor.

Tool names used in both (per Sofia's framing flag, aanp.10 alias drop):
`create_contact_invite`, `add_contact_by_handle`, `list_contacts` (not
`contacts_list`), `send_message_to_contact`, `aweb_welcome_guide`. If
Grace ships different names, revise both surfaces together.

### 2. Twitter thread P1 launch

`publishing/drafts/2026-05-13-twitter-thread-p1-launch.md`. 6-7 tweets;
through Sofia framing (revised tweet 4 to "wire each AI once" per her
note that "one paste" overclaimed friction for ChatGPT/Claude Desktop
shapes) and Athena tech-accuracy (tweet 3 staged-screenshot disclosure
banked; tweet 4 "wire once → sticks" verified honest via mcp_oauth_grants
persistence). On Juan/Eugenie's plate for voice pass + post timing
(Tue-Thu morning US Pacific).

Four register-variants banked for Pass-2 variant testing: friends,
hand-off, third-person, task-shaped.

### 3. Five direct-outreach drafts (post-Show-HN multi-channel pivot)

`co.aweb/outreach/daily/2026-05-07-direct-outreach-post-show-hn.md`.
Five drafts to protocol-article authors + adjacent builder. Eugenie's
plate for human send (staggered ~30 min apart per the plan to Bertha).
Capture goes to `co.aweb/outreach/history.md` after send.

## Recent shipping history (for context)

- 2026-05-07: Show HN went up and sank. Pivot to multi-channel.
- 2026-05-09 → 11: Homepage refresh cycles. Pass-1 by Iris (commit
  58ed6c53), reverted by Juan for technical error. Pass-2 missed
  customer-shape verification (Sofia caught; banked discipline).
  Pass-3 by Peter (pain-narrative) currently live at 21cb6c23.
  Bundle record in `publishing/drafts/2026-05-09-homepage-copy-refresh.md`.
- 2026-05-12: Sofia rewrote `docs/audiences.md` with persona + tier
  model (P1 personal-AI consumer, P2 company-fleet, P3 dev team, P4
  platform builder). voice.md updated with persona-ordered pitches +
  customer-shape verification (commit af98d1a).
- 2026-05-13: Twitter thread Pass-1 drafted; tweet 3 + 4 verified.
  Pain-narrative homepage verified-live (entry in publishing/history.md).

## Banked disciplines this cycle (in iris CLAUDE.md / AGENTS.md unless noted)

- "Verify the infrastructure contract before debating policy" —
  CLAUDE.md banked-learnings.
- "When launch / public-claim submit-state changes, surface to
  direction same-shift" — operating discipline.
- "Verify Pass 1 is shipping (not just drafted) before committing to
  two-transition framing."
- "When planned-transition gates remain open past their assumed
  window, surface explicitly."
- "publishing/drafts/*.md is narrative / framing / decision record —
  not a wire-in spec." (Lane discipline: Iris authors `ac/site/`
  directly; Hestia deploys; drafts/ is record, not source.)
- "For external-vendor policy verification, the vendor's help-center
  IS authoritative" + "cite the provenance accurately (snippet vs
  live page read)." voice.md + AGENTS.md.
- "Customer-shape verification before authoring landing-copy" —
  voice.md + AGENTS.md; points at docs/audiences.md.

## Role model context

Sofia (Direction) approves product fit and timing. Athena (Engineer)
reviews technical accuracy on product-behavior claims. Aida sends
user stories + support-integration pre-think. Metis tracks
distribution outcomes. Hestia signals when releases are verified-
live.

**Eugenie owns outreach send-side; Bertha is her personal agent.**
Per Juan's directive (2026-05-07): send Bertha a plan-of-action each
wake-up via `aw mail send --to bertha` so Eugenie has a current
packageable summary. After-send capture goes in
`co.aweb/outreach/history.md`; public `status/outreach.md` stays
generic per Case 7.

Juan and Eugenie publish. My drafts are the input; their voice is
the output.

## Open follow-ups (when bandwidth)

- Twitter thread Pass-2 register-variant testing (when Pass-1 is
  posted + signal observed).
- "Two Agents Not One" article on juanreyero.com — Juan voice-passed;
  awaits his commit/push.
- Watch.md reorientation toward P1+P2 (forward-looking practitioner
  sourcing for the new persona priority).
- Hero-note tier honesty for next homepage iteration (Sofia flagged
  in Twitter-thread Q3 response; not blocking).
