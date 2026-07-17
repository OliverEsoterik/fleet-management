---
name: better-products-habits
description: >
  Five habits for building better products faster: write it down, think deeply,
  use data, focus, and grow. Based on Hiten Shah's methodology.
---

## Overview

Building better products faster isn't about luck or raw talent — it's about repeatable habits. This skill covers the five habits framework developed by **Hiten Shah** (co-founder of Crazy Egg, KISSmetrics, and KISSinsights). It's a methodology for product strategy, design, and execution that applies at any stage: idea validation, feature design, growth optimization, or process audit.

Use this skill when you need to structure thinking around a product decision, diagnose why a product effort is stalling, or design a repeatable process for shipping better work.

## The Five Habits

---

### 1. Write it Down

**Core principle:** Documentation is a reusable asset that compounds in value. If it isn't written down, it doesn't exist.

> "Documents are a reusable asset that can accrue value over time."

**Key techniques:**

- **Problem Team + Solution Team structure.** Separate your document into what problem you're solving (who is affected, what the current experience is, why it matters) and what solution you propose (approach, scope, success criteria).
- **Have someone else read your doc.** If they can't understand it, your thinking isn't clear yet. The act of explaining forces clarity.

**Why it works:**

- Gets everyone on the same page — no assumptions, no "I thought we agreed on X."
- Creates a permanent record. Decisions and their rationale survive team changes.
- The discipline of writing surfaces gaps in reasoning that would otherwise be discovered mid-implementation.

> "Don't settle for explaining the rationale orally. Write it down and ask someone to read it and tell you what it means."

**How to build the habit:**

- Before building anything, write a one-page problem statement and solution proposal.
- Share it with someone outside your immediate team to verify it's clear.
- Keep a running document per product initiative. Revisit it monthly.

---

### 2. Think Deeply

**Core principle:** Start with first principles. Research thoroughly before building. The best products remove steps, not add them.

> "Take a human desire and use technology to take out steps." — Evan Williams (Twitter, Medium)

**Key techniques:**

- **Reduce the number of steps.** Map every step a user takes to accomplish a goal. Remove every step that isn't essential.
- **Storyboard the steps.** Draw the user's journey like a comic strip. Identify friction points visually.
- **Ask the opposite.** If everyone optimizes for more features, ask what happens with fewer. If everyone adds personalization, ask what happens with none.
- **Create a concept car.** Build a prototype that showcases the vision, not the implementation. A "concept car" isn't production-ready — it's a vision tool to align the team and test direction before investing in engineering.
- **Research thoroughly upfront.** Spend weeks on research before writing code. The iPod team spent 6 weeks on research alone, built only 3 prototypes, and nailed the rotating wheel input because they understood the constraint before designing.

**Real examples:**

- **Optimizely** vs. Google Website Optimizer: Google's A/B testing tool required 11 steps to set up a test. Optimizely reduced it to 4 steps by thinking deeply about what each step actually required. The result was a product that unlocked A/B testing for non-engineers.
- **Apple iPod:** 6 weeks of upfront research. Only 3 prototypes built. The rotating wheel input — the defining interaction — came from understanding the constraint (one-handed operation while walking) before designing.

> "You can't go from A to B. You have to go from A to concept car to B."

**How to build the habit:**

- Before any feature, force yourself to map every user step on paper.
- Ask "what's the minimum number of steps this could be?" and challenge every answer.
- Spend at least a week on research and storyboarding before writing a line of code.
- Build a concept car (a mockup, prototype, or narrative) before committing to engineering.

---

### 3. Use Data

**Core principle:** Be data-informed, not data-driven. Data informs decisions but doesn't make them.

> "Data informs. People decide."

**Key techniques:**

- **ONE metric per product team** with a target goal. Not a dashboard — a single number that tells you if you're winning. If you have to explain which metric matters, you don't have one.
- **Start with a hypothesis.** Collect data to test a hypothesis, not to wander looking for answers. "I think X will improve Y because Z" — then go measure.
- **Map product usage by feature.** Know which features are used, by whom, and how often. Every feature you don't track is a blind spot.
- **Set expiration dates on metrics.** Metrics should be temporary. When they stop being useful, retire them and find a better one. Don't become an organization that optimizes in the dark.

**Real examples:**

- **KISSinsights** (now Qualaroo): Built entirely from 20 structured customer interviews before writing code. The data was qualitative — customer pain — not dashboard numbers.
- **Twitter** used feed views as their north star metric: the number of times a user viewed their timeline per day. One metric, one target.
- **Slack** focused on 2,000 messages sent per team. That was the threshold where teams were sticky. They optimized for getting teams to that number — nothing else mattered in the early days.
- **Dropbox** on 1 file in 1 folder. If a user put one file in a Dropbox folder, they understood the value proposition. Everything was optimized to get users to that one action.

> "One metric per product team. Not three. Not five. One."

**How to build the habit:**

- Identify the ONE metric that matters most for your current product goal. Write it down.
- Before looking at any data, write your hypothesis. What do you expect to see and why?
- Map feature usage for your product. If you can't, add tracking.
- Review metrics quarterly. Archive ones that have served their purpose.

---

### 4. Focus

**Core principle:** Companies can only do one thing at a time. The formula is simple: **Focus + Sequence = Speed**.

> "You can't focus on two things at the same time and be great at either. It's just not possible."

**Key techniques:**

- **Press-gang a DRI (Directly Responsible Individual).** Every initiative has exactly one person who is accountable. No committees, no shared ownership. If something goes wrong, you know who to talk to.
- **Minimize interruptions** for the team. Interruptions are the enemy of focused work. Protect maker time.
- **Prioritize with the Wow-Must-Neat-Who-cares framework:**

| Priority | Action |
|----------|--------|
| Wow! | Do first. These are the features that differentiate your product. |
| Must-have | Do second. Table stakes — your product won't work without them. |
| Neat | Do third if there's time. Nice-to-haves. |
| Who cares | Remove. Nobody will notice. |

**Real example:**

- **HubSpot Sidekick** (email tracking product): For months, the team tried everything to improve onboarding — better emails, tutorials, tooltips. Nothing moved the needle. They ran **11 experiments** in rapid succession. The winning fix was deceptively simple: get users to send more emails. Once users sent a few tracked emails, they saw the value and stayed. Eleven experiments before the team found the thing that worked. Focus meant systematically trying one thing at a time until they found it, rather than doing eleven things halfway.

> "Every team should be able to answer: what is the one thing we're working on right now?"

**How to build the habit:**

- Every week, each team member names the ONE thing they're focused on.
- Use the Wow-Must-Neat-Who-cares framework on your backlog. Cut the "Who cares" column entirely.
- Assign a DRI to every initiative — even small ones.
- Protect at least 3 hours of uninterrupted maker time per day for every engineer and designer.

---

### 5. Grow

**Core principle:** Build a system focused on learning, not just shipping. Controlled failures are competitive advantages.

> "If things aren't failing, you aren't learning. Fail fast, be foolish, learn."

**Key techniques:**

- **Continuous improvement loops.** Ship, measure, learn, adjust. The loop is the engine of growth.
- **Design experiments so failure is informative.** A good experiment teaches you something even — especially — when it fails. A bad experiment tells you nothing either way.
- **Create psychological safety.** Teams that are afraid to fail will optimize for safe, small, boring changes. Teams that are safe will try bigger, more interesting bets.

**Real example:**

- **Golden Motion** (a KISSmetrics portfolio company): Set an OKR of increasing a key metric by 25%. The team designed a series of experiments, iterated rapidly, and ended up **blowing the 25% target out of the water** — far exceeding expectations. The path wasn't linear; it was a series of small bets that compounded. The key was the team kept running experiments, kept learning, and kept adjusting.

> "If you can control failure, you can make it a competitive advantage."

**How to build the habit:**

- Every experiment starts with: "If this works, we learn X. If this fails, we learn Y."
- Run experiments in batches. Review results weekly. Kill what isn't working. Double down on what is.
- Celebrate informative failures — share what was learned, not what went wrong.
- Set OKRs that stretch. If you're hitting every target, your targets aren't ambitious enough.

---

## Putting It All Together

These five habits form a reinforcing cycle, not a checklist:

```
Write it Down  -->  Think Deeply  -->  Focus  -->  Use Data -->  Grow
     ^                                                            |
     |____________________________________________________________|
```

1. **Write it Down** creates the shared foundation. Without a written record, Thinking Deeply has nothing to build on.
2. **Thinking Deeply** identifies the real problem and the fewest steps to solve it. This tells you what to **Focus** on.
3. **Focus** enables fast execution — one thing, well done, by a DRI. This generates clean **Data**.
4. **Use Data** to validate (or invalidate) your assumptions. The results feed back into **Thinking Deeply** — you now know more than you did before.
5. **Grow** is the meta-habit that sustains the cycle. It's the willingness to keep running the loop, keep learning, and keep shipping.

The habits are a system. Each one amplifies the others. Skip one and the cycle breaks.

> "These are the habits we've used across dozens of companies over 15+ years. They're not theoretical. They're battle-tested."

## Usage

Invoke this skill when:

- Someone asks for product strategy, methodology, or process advice.
- A user mentions "build better products", "product habits", "five habits", "Hiten Shah", or "better products faster".
- The conversation involves designing a new product or feature from scratch.
- A product team is stuck, shipping slowly, or building things nobody uses.
- You're reviewing a product strategy and need a framework to identify gaps.
- The request involves prioritization, feature selection, or roadmap decisions.

When invoked, read through the five habits in order and apply them to the specific context the user provides. Don't treat it as a rigid script — adapt each habit to the situation, but cover all five.