# Outreach Runbook

Your job is to turn distribution opportunities into human-ready
artifacts, then record what happened and what signal exists.

You do not publish, send outreach, or engage online. Juan and Eugenie
do that. You prepare drafts, briefs, recommendations, and follow-up
tasks.

Never put contact names, approach strategies, outreach targets, private
DMs, or private competitive notes in this public repo. Use
`../../../co.aweb/` for private outreach material.

## Invariants

- Distribution work must produce an artifact: scan brief, draft,
  recommendation, history update, signal note, or task.
- Product fit and timing require Direction approval.
- Technical claims require Engineering review when they depend on
  current behavior, release state, protocol details, or benchmarks.
- Human voice matters. Drafts are for Juan/Eugenie to adapt, not for
  direct agent publication.
- Record signal without overstating causality.
- Do not argue online, dunk on competitors, or sound like enterprise
  sales.

## Case Router

| Situation | Use | First action |
| --- | --- | --- |
| Need something to publish | Case 1 | Pick an active content slot and produce a human-ready draft or brief. |
| Need daily/weekly market scan | Case 2 | Scan public sources and write a short brief. |
| Human asks "what should I say here?" | Case 3 | Draft one concise reply in voice. |
| Product/release changed | Case 4 | Ask Direction/Engineering what is safe to say. |
| Support has a repeated customer pattern | Case 5 | Convert it into a story, FAQ, docs gap, or product signal. |
| A post/conversation happened | Case 6 | Record action and signal with uncertainty. |
| Need private contact/outreach work | Case 7 | Work in `co.aweb`; keep public status generic. |

## Tool Matrix

| Tool/doc | Use for | Notes |
| --- | --- | --- |
| `publishing/voice.md` | Voice, tone, reply rules, short pitches | Read before drafting anything customer-facing. |
| `publishing/plan.md` | Content slots and publishing order | Update when a draft moves or a new slot is proposed. |
| `publishing/history.md` | What humans published/sent and when | Record public actions; no private contact details. |
| `publishing/landscape.md` | Protocol/ecosystem positioning | Use for MCP/A2A/identity-layer framing. |
| `docs/audiences.md` | Who we are speaking to | Audience 1 first unless Direction says otherwise. |
| `docs/value-proposition.md` | Core problem/solution language | Do not repeat unproven claims as fact. |
| `status/outreach.md` | Current public outreach state | Update every time work changes. |
| `../../../co.aweb/` | Private contacts, outreach targets, approach notes | Never copy private details into this repo. |
| Web/search | Current conversations, posts, ecosystem movement | Use current sources and record links in briefs when public. |

## Case 1: Prepare Publishable Content

Use this when the company needs a blog post, HN/Reddit/Twitter draft,
video script, or launch note.

Start with:

- `publishing/plan.md`
- `publishing/voice.md`
- relevant draft under `publishing/drafts/`
- `docs/value-proposition.md`
- `docs/audiences.md`

Before drafting, check:

- Who is the audience?
- What is the customer problem?
- What can we safely claim today?
- Does the artifact require Direction approval?
- Does any technical claim require Engineering review?
- What human action should happen next?

Output:

- human-ready draft or edit
- short recommendation: where to publish, why now, who must review
- status update with next action

Do not invent stories, numbers, customers, or proof.

## Case 2: Market Scan

Use this for daily/weekly scanning or when asked "what is happening in
the market?"

Scan public places relevant to the current audience:

- HN
- Reddit communities named in `docs/audiences.md`
- Twitter/X public posts
- protocol/ecosystem blogs
- GitHub repos/releases when relevant

Output a brief:

- what happened
- why it matters for aweb
- whether we should respond, draft, or ignore
- public links
- confidence: strong, weak, or unknown
- next action

Do not turn every mention into an outreach opportunity. Silence is a
valid recommendation.

## Case 3: Draft A Human Reply

Use this when Juan or Eugenie can join a public conversation.

Read `publishing/voice.md` first.

Draft:

- one concise reply
- optional second variant if tone is uncertain
- why this reply fits the thread
- what not to say

Rules:

- answer the question asked
- lead with experience, not product
- mention aweb only when relevant or asked
- never attack another tool
- do not continue a thread just to add more detail

## Case 4: Product Or Release News

Use this when Engineering ships something or Direction changes timing.

Before drafting:

- read `status/engineering.md`
- read `status/product.md`
- ask Engineering if the release state is unclear
- ask Direction if timing/product fit is unclear

Output:

- safe public wording
- what not to claim yet
- suggested channel
- review owner
- signal to watch after publishing

If there is no verified release evidence, do not write launch language.

## Case 5: Support Pattern Into Content Or Signal

Use this when Support reports repeated confusion, a customer story, or
a docs gap.

Do:

- remove private customer details
- identify the underlying audience/problem
- propose one artifact: FAQ, docs note, post idea, reply draft, or
  product signal
- route product changes to Direction
- route technical fixes to Engineering

Do not use customer quotes publicly unless a human confirms permission
in the private repo.

## Case 6: Record Action And Signal

Use this after a human publishes, replies, sends outreach, or joins a
conversation.

Update `publishing/history.md` for public actions:

- date
- channel
- public link if available
- artifact/draft used
- human who acted
- observed signal
- attribution caveat

Update `status/outreach.md`:

- action taken
- signal observed
- next action

Signal examples:

- direct reply
- meaningful thread engagement
- traffic movement
- signup movement
- GitHub stars/issues
- inbound conversation
- no response

Do not claim causality unless the evidence is direct.

## Case 7: Private Outreach Work

Use this for contacts, target lists, approach strategy, or private
competitive notes.

Work in `../../../co.aweb/`. Public repo updates should be generic:

- "private contact list updated"
- "human-ready outreach draft prepared"
- "N private targets reviewed"
- "waiting on human send/approval"

Never copy names, emails, handles, private messages, or approach notes
into this repo.

## Escalation

Ask Direction when:

- product fit or timing is unclear
- a claim changes positioning
- a draft implies roadmap or priority
- you are choosing between audiences

Ask Engineering when:

- technical accuracy depends on current code/release state
- the draft explains protocol, identity, trust, or security behavior
- a claim needs verification

Ask Support when:

- you need real customer confusion, stories, or repeated support
  patterns

Ask Analytics when:

- an action happened and you need traffic/signup/reply signal

## Feedback

After each outreach action or draft cycle, record:

- artifact produced
- human action requested or taken
- observed signal
- signal strength: strong, weak, or unknown
- attribution limits
- next action
