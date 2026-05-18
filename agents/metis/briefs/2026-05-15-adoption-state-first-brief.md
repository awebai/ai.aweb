# First analytics signal brief — adoption state

**Date**: 2026-05-15 12:00Z
**Author**: Metis
**Closes**: aweb-aals.4 (initialize analytics area + first signal brief).
**Audience**: Sofia (priority framing), Iris (distribution next-move), Athena
(instrumentation gaps), Hestia (operational measurement adjacent), Juan
(strategic).

---

## Question

Is consumer-onboarding v1 — pain-narrative site live on aweb.ai
2026-05-13 22:28Z + AC v0.5.31 backend + ChatGPT-connect work —
moving any of: signup rate, OAuth grant rate, OAuth-to-invite
conversion?

## Headline finding

Too early to tell; the dataset also has a counting trap that
matters. The true external population for the OAuth-onboarding
investment is **n=1** (one real external user), not n=7.

External signup rate is **steady at 2-5 per week** for the last 7
weeks; no observable lift in the 36h since pain-narrative deploy.

## Evidence (direct, from `aweb_cloud` prod read 2026-05-15)

External-users baseline (excludes the 3 internal team emails):

```
external_users_total              21
signups_last_30d                  17  (most growth in the last month)
signups_last_48h                   0  (3.5+ day quiet stretch)
```

Weekly signup velocity, last 9 weeks:

```
week_of 2026-05-11   3   (partial — 4 days remaining in week)
week_of 2026-05-04   5
week_of 2026-04-27   6
week_of 2026-04-20   1
week_of 2026-04-13   2
week_of 2026-04-06   2
week_of 2026-03-23   2
```

`mcp_oauth_grants` population (the table Athena queued the
post-OAuth-onboarding signal against):

```
mcp_oauth_grants_total                                7
  internal (4 internal-team accounts)                 4
  "external" by table value                           3
    of which juan@thestarmaps.com (Juan testing)      2
    of which gptstars12@gmail.com (real external)     1
true external grant population                        1
```

OAuth grants by timestamp (external slice):

```
2026-05-15 08:42:17Z   juan@thestarmaps.com   (Juan testing, post-site)
2026-05-13 22:23:05Z   juan@thestarmaps.com   (Juan testing, 5 min PRE-site)
2026-05-05 03:13:37Z   gptstars12@gmail.com   (real external)
```

`consumer_contact_invites` population:

```
consumer_contact_invites_total      0
```

Therefore:

```
External OAuth-to-invite conversion baseline = 0 / 1 = 0%  (n=1)
```

## Attribution — what we can and cannot claim

| Claim | Truth status |
|---|---|
| "Pain-narrative site has not moved external signups in its first 36h" | True (0 signups in last 48h; no spike). |
| "Pain-narrative site has not moved external OAuth grants" | True (0 real-external grants after 2026-05-13 22:28Z; 1 was Juan testing today). |
| "OAuth onboarding is converting at 0%" | Misleading without n. Actual: 0/1, n=1. We have effectively no baseline. |
| "Recent signup uptick (15 of 21 in last 30d) is due to X" | Unknown. No referrer/source instrumentation; cannot attribute. |
| "Twitter thread will lift signups" | Unmeasurable until it ships AND we have source attribution. |

The OAuth-onboarding investment Athena flagged
(MCP create-invite tool + welcome guide + serverInfo.instructions
+ consent-page banner + email shipped v0.5.32) cannot yet be
evaluated on the empirical-zero-tolerance line — the prior baseline
is effectively absent (n=1).

## Measurement gaps surfaced by this brief

1. **No referrer/source on signup** (instrumentation lane: Athena).
   Without it, attribution to any distribution action — site
   launch, Twitter thread, OAuth investment — stays speculative.
2. **`daily_active_workspace_facts` is org-only** — the existing
   `services/admin_analytics.py:aggregate_daily_active_workspaces`
   filters to `p.owner_type = 'organization' AND p.owner_org_id
   IS NOT NULL`. Personal-team and standalone-OSS workspaces are
   not captured. The last-7d query returns empty. Worth extending
   if we want to see total agent activity rather than paying-tier
   activity.
3. **OAuth-onboarding investment baseline is n=1.** Athena's
   queued signal (numerator = invites within N=15 min after grant,
   denominator = grants in period) cannot produce a statistically
   meaningful baseline until grant volume rises. Worth noting in
   the company-dashboard signal-inventory entry that the metric
   needs ~10+ grants to mean anything.
4. **No internal/external distinction in the standard analytics
   tables.** I had to hard-code the three internal emails in my
   queries (mirroring Hestia's check.py predicate). A `is_internal`
   column or maintained internal-domains list on users would make
   external-population queries cleaner.

## What this brief enables

- **For Sofia**: release-claim framing should avoid "OAuth
  onboarding is converting" until we have grant volume. "Baseline
  is n=1; we cannot yet claim conversion rate" is honest.
- **For Iris**: the Twitter thread should ship; the pain-narrative
  site is live but observably unused, and we won't learn anything
  about adoption response until distribution fires. The 2-5/week
  steady-state will be the comparator.
- **For Athena**: two queued instrumentation items — referrer/
  source at signup, and extending daily-active-workspace facts
  beyond org-only.
- **For Hestia**: nothing operational here, but flagging that the
  empty `daily_active_workspace_facts` result may indicate the
  `active_workspace_aggregation.py` job is unscheduled / unrun in
  prod, OR that no org-tier workspaces have been active in the
  last 7d. Worth a separate empirical probe.

## Open question for Juan

Sofia and Iris will use this brief to shape framing and next
distribution action. The n=1 OAuth-onboarding baseline is the
piece with the most reputation risk — saying "0% conversion" is
technically true and dangerously misleading. Proposed framing:
"insufficient grant volume to compute conversion rate; will
re-baseline at n>=10."

## Next checks (anchored to the open questions)

1. Re-query weekly when Iris's Twitter thread publishes.
   Comparator: 2-5 signups/week steady-state.
2. Re-query at n=10 mcp_oauth_grants (external) to compute the
   first real OAuth-onboarding conversion baseline.
3. File aw tasks for the 4 measurement gaps above.

## Provenance

All queries run against the read-only Neon endpoint via
`DATABASE_URL` from `ac/.env.production`. Internal-account
exclusion list matches Hestia's `check.py`. No state files
written.
