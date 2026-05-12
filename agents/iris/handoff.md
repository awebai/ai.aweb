# Iris Handoff

Last updated: 2026-05-07 15:48 BST (Show HN packaging in flight)

## Operating focus

Use `../../publishing/runbook.md` first. Outreach work is case-based:
classify the situation, read only the references needed for that case,
produce a human-ready artifact, and record the action/signal with
attribution limits.

You do not publish, send outreach, or engage online. Juan and Eugenie
do that. Private contacts, targets, approach notes, DMs, and private
competitive notes stay in `../../../co.aweb/`.

## Active distribution work — Show HN for aweb.ai

This is the active distribution action. Three drafts in
`publishing/drafts/`, all `draft: true`, none published yet:

- `2026-05-07-five-agents-blog-post.md` — Sofia drafted in
  sample.md voice (TL/DR + bolded claims + product-as-italic-end-note).
  Idea-essay shape; problem narrative.
- `2026-05-07-cycle-log.md` — Athena drafted; engineering-narrative
  with named receipts (commit hashes, banked disciplines #18-#28,
  cross-org dogfooding). Currently 500 lines; HN drive-by reader
  bounces. Worth a TL/DR + receipts-table version.
- `2026-05-07-getting-started-how-to.md` — 5-min onboarding,
  imperative voice; works for the try-now path.

Eugenie has a parallel '6 months entirely on AI agents' draft through
Bertha; potential overclaim on 'entirely' (Juan's three pushbacks in
the cycle log are empirical counter-evidence). Coordination concern:
two parallel posts same-day reads and gets flagged on HN as a
coordinated push.

## My read on the package (mail to Sofia, `efc07013`)

Three open decisions before Show HN can ship:

1. **Submission URL**: aweb.ai (Stage 1 promise; my lean) vs OSS repo
   vs the essay. Show HN expects 'a thing,' which favors aweb.ai.
2. **One vs two parallel posts**: my lean is ONE Show HN with ONE
   pinned comment; Eugenie's piece folds in as depth-link or runs
   separately on a different week.
3. **Tech-accuracy review** by Athena on '2x+ with far fewer
   disasters' (value-prop.md) and similar essay claims that are
   currently unvalidated.

Lane proposal: I take the canonical-voice surface (pinned comment,
essay TL/DR HN-ready, how-to polish, AHK landscape entry); Athena
tech-accuracy on cycle log + pinned comment; Sofia frames and approves.

Pinned author comment (load-bearing for Show HN) doesn't exist yet.
Will draft v1 once submission URL + Eugenie sequencing are decided.

## AHK comment situation

AHK = Agent Harness Kit (TypeScript, https://ahk.cardor.dev,
github.com/enmanuelmag/agent-harness-kit, 48 stars 3 days old).
Adjacent space: local-tight harness vs aweb's distributed-loose
coordination.

Eugenie wanted to comment on a dev.to/HN post about it. Sofia and
Bertha converged on Option C: founder-voice with explicit Disclosure.
Sofia approved. I sent Bertha outreach feedback on the draft (chat
delivered, no live ack):

- Drop the closer 'Either way, nice work' (reads condescending from
  competing-founder voice on a 48-star 3-day-old project).
- Confirm venue (dev.to vs HN — comment shape differs).
- Two minor voice notes flagged as Sofia's call to fold or skip:
  the leading question on configurable roles, and the 'yet' in
  'no DNS-equivalent for agent identity yet' (replace with 'today').

Bertha may come back with the venue confirmation and the question
of whether to fold the edits. The chat session id was
`d55b4606-ff7b-4116-9753-584999d16e77`.

## Pre-launch dependencies (Hestia/Aida lanes)

Engineering-readiness pre-flight per Sofia's mail (`73327224`):
- Rate-limit bump 5/min -> 30/min for register/login during HN window
  (Hestia, <30 min)
- Server-side 422 with upgrade-pointer for BYOD-missing-username
  (Mia or Grace, ~10 line fix)
- Multi-team agent_id-vs-did grep (Athena, this week)
- Monitoring audit + support FAQ pre-write (Aida) + rollback
  playbook + agent-guide accuracy scan + Render auto-scale ceiling
  — pending owners

Submit window: Tue/Wed/Thu morning US Pacific. Pinned comment within
2 minutes of submit. Nobody requests upvotes.

## Other content state

### Ready for publishing (deferred until Show HN packaging settled)
- The three Show HN drafts above need Juan's voice pass + Sofia's
  final framing + Athena's tech-accuracy.

### Production guides (ready, not publishable content)
- `publishing/drafts/2026-04-09-chaos-video-guide.md`
- `publishing/drafts/2026-04-09-agent-standup-guide.md`

### Not started (post-Show-HN)
- 'Agent Web: how identity works' — aweb.ai/blog, after Show HN
- 'We rebuilt everything around public-key crypto' — juanreyero.com
- 'aweb vs MCP vs A2A' — aweb.ai/blog
- 'Running a company with AI agents' — juanreyero.com

## Role model context

Sofia (Direction) approves product fit and timing. Athena (Engineer)
reviews technical accuracy on drafts that mention product behavior.
Aida sends user stories. Metis tracks distribution outcomes. Hestia
signals when releases are verified-live.

**Eugenie owns outreach send-side; Bertha is her personal agent
(cross-team).** Per Juan's directive (2026-05-07): I send Bertha a
plan-of-action each wake-up via `aw mail send --to bertha` so Eugenie
has a current packageable summary of what to act on today. Format
and shape banked in iris `CLAUDE.md` under "Daily plan-of-action to
Bertha." After-send capture goes in `co.aweb/outreach/history.md`;
public `status/outreach.md` stays generic per Case 7.

Today's plan to Bertha sent: message_id `09ab1f36`. Covers post-Show-
HN multi-channel pivot, the 5 queued drafts, what's held, and what's
open beyond today.

Juan and Eugenie publish. My drafts are the input; their voice is
the output.
