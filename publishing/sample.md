---
title: "With the Rise of AI-Assisted Programming We'll Want More Programmers, Not Fewer"
date: "2025-10-26"
type: "post"
draft: false
---

### TL/DR

The conventional wisdom is that AI will reduce the demand for programmers. I manage engineering teams and program with LLMs every day, and I am seeing something different.

Programmers who know how to work with LLMs can be 3-10x faster for specific tasks. Given that the size of our work backlog is only limited by our vision and ambition, these super-productive individuals will be more in demand, not less.

**The higher productivity will increase the number of programmers we need**, and surface the next problem: **coordination among LLM-enhanced engineers.**

## Jevons Paradox

In 2016, Geoffrey Hinton (who won the Nobel Prize for his work on neural networks) said that we should stop training radiologists because it was "completely obvious" that within five years deep learning would do their job better than they could.

Nine years later, radiologists are in [historic shortage](https://newrepublic.com/article/187203/ai-radiology-geoffrey-hinton-nobel-prediction). Mayo Clinic has grown its radiology staff by 55% since Hinton made that prediction. The specialty is projected to grow another 26% over the next thirty years.

AI did transform radiology, but not in the way Hinton expected. It made radiologists more productive: scans became faster, routine tasks were automated, image quality improved. But making radiology more efficient didn't reduce the demand for radiologists—it increased it. More efficient radiology made imaging more accessible, which drove up demand for it.

This pattern has a name, [Jevons Paradox](https://en.wikipedia.org/wiki/Jevons_paradox): **efficiency improvements often increase total consumption**. When cars became more fuel-efficient, people drove more miles, not fewer. When steam engines became more efficient, coal consumption went up, not down. When radiologists became more efficient, demand for radiology increased.

## Why Demand Increases

The intuition behind "fewer programmers" assumes a fixed amount of work: build the features, fix the bugs, maintain the systems: once you can do all that faster, you'll be done sooner with fewer people.

But this is only an instance of the [lump of labor fallacy](https://en.wikipedia.org/wiki/Lump_of_labour_fallacy).

Anyone who has run an engineering organization knows that the backlog doesn't shrink when you get faster. If anything, it explodes. Every problem you solve reveals three more worth solving. Every feature you ship makes users aware of other features they need. **Every new capability opens up opportunities that were previously impossible to pursue.**

There's a subtler effect too. An hour not spent programming used to mean an hour of progress missed. Now, for someone skilled with LLMs, that same lost hour can mean the equivalent of a day or two of progress missed. The opportunity cost has multiplied. **The gap between organizations that keep their best programmers programming and those that don’t will widen dramatically.**

When your capacity multiplies, entire categories of previously impossible work become viable.

## The Skills Split

A [recent study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) tested sixteen experienced developers using AI tools on their own repositories (code they knew intimately). On average, they were 19% slower when using AI tools, despite expecting to be 24% faster.

Developers with roughly fifty or more hours of prior AI-tool use, however, tended to gain productivity. The majority, with less experience, slowed down. There’s a steep learning curve, and few have climbed it.

A skills split is emerging. Programmers who can use AI effectively are becoming force multipliers; those who can’t, or won’t, are falling behind. The work is shifting from syntax and detail to judgment and architecture: reviewing generated code for subtle flaws, choosing among approaches, directing agents, and maintaining coherence as systems evolve faster than before.

The best programmers are excelling at this. It plays to their strengths: architectural insight, pattern recognition, and judgment.

**Good programmers now have superpowers, yet they cost about the same.** I predict they’ll soon command higher wages, and demand for them will rise.

## The Coordination Problem

The bottleneck has shifted. It’s no longer about individual productivity. It’s about coordination. Our management tools (daily standups, OKRs, sprint planning) were all designed for humans working at human speed, solving problems at a pace where the main constraint was how fast people could think and communicate.

**These tools are increasingly in the way**. When a programmer working with an LLM can prototype three different approaches to a problem in a morning, the two-week sprint feels wrong. When they can refactor a complex system in an afternoon, careful estimation of story points loses its meaning. The rhythms don’t match anymore.

The most interesting innovations in software development over the next few months will be about figuring out how to coordinate work when some people are operating at more than five times the speed of traditional development. [Claude's Skills](https://www.anthropic.com/news/skills) are a very interesting step in that direction.

## The Agency Question

A common argument against the future of programmers is something along the lines of: you’ll be able to tell an AI, “build me an e-commerce site that sells shoes for clowns, market it, handle the orders, and send the money to this account,” and it will just happen. End to end, without you.

The technical pieces will probably come together. The [Model Context Protocol](https://modelcontextprotocol.io/introduction) and similar efforts are standardizing how AI systems connect to services and tools. Maybe LLMs will develop something that looks like genuine agency, with their own reward loops and decision-making capabilities.

But even if all that happens, someone still has to decide to build the clown-shoe site instead of the dog-collar site. The LLM doesn’t have your problems. It doesn’t have your goals. Even if it could execute perfectly on any direction you point it at, you’re still the one doing the pointing. **For as long as we have aligned LLMs and problems to solve we'll need people who can lead the LLMs.**

And as the tools get more powerful, the pointing matters more, not less.

## What This Means

The ability of skilled programmers to create value has multiplied. But the market is splitting. There are programmers who can work effectively with LLMs, and there are those who can’t or won’t. The gap between these two groups is growing.

If you’re running an engineering organization and thinking, “AI means we can reduce headcount,” you’re looking at this wrong. The opportunity space has expanded dramatically, and you should be revising your ambition and the scope of your plans.

The constraint isn't how much code you can write anymore: **it's how much good judgment you can apply to problems, and how well your team can coordinate.** For that, you need programmers who can work at this new speed. And you probably need more of them, not fewer.

---

*I built a tool to address the coordination problem: [BeadHub: Coordination for AI Programming Teams](/article/ai/beadhub/).*
