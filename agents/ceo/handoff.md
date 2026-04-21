# CEO Handoff

Last updated: 2026-04-21 (Avi, after full repo study)

## Where we actually are

The product has shipped. The prior handoff (2026-04-11) said "OSS
close to shippable, cloud mid-migration" — both are now stale.

- **aweb OSS**: v1.16.0 server + CLI + awid-service v0.4.0.
  End-to-end user journey works (hosted and self-hosted). SOT docs
  match code. Shipping, not shipping-soon.
- **aweb-cloud (ac)**: v0.5.3. Identity migration complete.
  Dashboard feature-complete. Billing live, Stripe wired, tiers at
  $0 / $25 / $250 (strategy.md's known-gap re: pricing mismatch has
  closed). awid.ai is a production dependency.
- **Amy**: now holds a second address `aweb.ai/amy` (public support
  contact) — see `docs/decisions.md` 2026-04-21 entry.

The prior CEO handoff's "waiting for product to work" was the right
stance as of 2026-04-11; it is no longer correct. The gate has been met.

## Active decisions (still stand)

- **OSS ships before cloud** — moot now, both are shipping.
- **Crypto identity migration was the right call** — validated; the
  cloud migration landed cleanly.
- **Content publishing split**: personal/story on juanreyero.com,
  technical on aweb.ai/blog. (See `docs/decisions.md` 2026-04-11.)

## New state (my read, not yet a Juan-approved decision)

- Engineering-to-distribution ratio has to shift this week. This was
  the board's concern on 2026-04-07 and it is now the gap.
- The blog post has been in draft for 12 days. Publishing it is the
  longest pole.
- 8 outreach contacts identified, 0 contacted. Charlene's daily
  scan never started. Infrastructure is dormant.
- `status/product.md` and my prior handoff both described a
  pre-launch reality. I have rewritten product.md; this handoff
  matches.

## What to check FIRST on next wake-up

1. Did the blog post get published? (`publishing/history.md` is
   currently empty; a publish event would land there.)
2. Did Charlene start the daily scan? (co.aweb `outreach/daily/`
   directory is empty as of today.)
3. Has any contact been opened? (co.aweb `outreach/history.md`
   empty as of today.)
4. Has Juan responded to the voice-pass ask / the collision-video
   decision?
5. Did Randy ship the runTeamSwitch patch? (aweb-aakn, P2.)

## What's in conversations / in progress

- No active aw chat threads. Mail inbox empty.
- Randy active right now (same host). No open asks to him from me.
- Amy active on aweb.ai/amy. No user feedback yet.
- No outstanding Charlene or Enoch items.

## What to do on next wake-up (suggested sequence)

1. Pull, read north-star docs, read `status/engineering.md`,
   `status/outreach.md`, `docs/decisions.md` for new entries.
2. If Juan has replied on voice pass / collision video — act on it.
3. If Charlene has updated outreach.md with scan results — read and
   route.
4. If Randy has shipped the runTeamSwitch patch — note in product
   status and close out.
5. If none of the above: reach out to Charlene via chat and ask
   specifically what's blocking the first scan. If it's waiting on
   me (e.g. content approval), unblock her same-day.
6. Rewrite the "Current focus" block of `status/product.md` to
   reflect whatever moved.

## Reference map (what lives where)

- **aweb OSS** (../../../aweb): server, CLI, awid, channel.
  CHANGELOG.md is the truth. SOTs in `docs/`. v1.16.0 current.
- **ac cloud** (../../../ac): backend + dashboard + migrations. Pins
  aweb>=1.16.0 and awid-service>=0.4.0. v0.5.3 current.
- **co.aweb** (../../../co.aweb): outreach contacts, competitive
  landscape, agent key backups. `outreach/contacts.md`,
  `outreach/watch.md`, `outreach/history.md`,
  `outreach/competitive-landscape.md`. `keys/` holds agent-key
  backups (source of truth is `~/.config/aw/controllers/`).
- **ai.aweb** (this repo): company docs, status, publishing, and
  the five company agents (cto, ceo, board, comms, support) + three
  coordinators (aweb, cloud, awid). All `aw` commands run from the
  agent's own subdirectory.
