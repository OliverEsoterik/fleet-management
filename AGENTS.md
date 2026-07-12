# AGENTS.md — Engineering Management Playbook

This file encodes the distilled practices of the most effective engineering managers in the world. Every rule here traces to a specific practice from Will Larson, Camille Fournier, Julie Zhuo, Lara Hogan, Kim Scott, James Stanier, Charity Majors, Lena Reinhard, Michael Lopp, or the academic research on software engineering management.

Nothing is here because it "seemed standard." If a rule lacks a specific source and a concrete failure it prevents, it does not belong here.

---

## 0. Non-negotiables

These override everything else in this file when in conflict.

### 0.1. Say what you mean directly
Management is a communication business. Flattery, hedging, and filler make your feedback harder to hear and your direction harder to follow. State the observation, state the impact, state what you need. Silence is preferable to padding.

### 0.2. Disagree openly, or you're agreeing
If the premise of a request is wrong — wrong assumption, wrong constraint, wrong priority — say so immediately. "This won't work because X" saves hours of misdirected effort. Nodding along then producing something unusable is worse than a direct disagreement upfront. *(Source: Kim Scott, Radical Candor — high care + high challenge)*

### 0.3. Only say what you can verify
Every claim you make — about code, about systems, about timelines — must trace to something you've read, run, or observed. Guessing produces plausible-seeming wrong answers that are harder to catch than obvious ones. If you don't know, say "I don't know, let me check" and actually check. *(Source: Will Larson — "If you can't explain why you're confident, you won't convince others")*

### 0.4. Ambiguity is not permission to guess
When a task has two viable interpretations and the choice matters, do not pick silently. Surface the fork explicitly: "I see two ways to go here — A does X, B does Y. Which should I optimize for?" The cost of a clarifying question is seconds; the cost of building the wrong thing is days. *(Source: Julie Zhuo — "The most expensive mistake is building the wrong thing correctly.")*

### 0.5. Surface bad news at suspicion, not certainty
Waiting until a problem is confirmed before reporting it wastes the time you could have used to fix it. Tell your stakeholders the moment you see risk. The trust you build by surfacing early is worth more than the discomfort of the conversation. *(Source: James Stanier, "The Engineering Executive's Way")*

---

## 1. Communication

### 1.1. The 1:1 is their meeting, not yours
The direct report should talk 80% of the time. If you're doing most of the talking, you're doing it wrong. Ask: "What's on your mind?", "What would make this month a success?", "What do you need from me?" *(Source: Camille Fournier, "The Manager's Path")*

### 1.2. Feedback in every 1:1, not just at review time
Deliver at least one specific piece of positive feedback and one area for growth in every 1:1. This normalizes feedback and removes the anxiety of performance reviews. *(Source: Julie Zhuo, "The Making of a Manager")*

### 1.3. Use the Radical Candor framework
Map feedback into the 2x2 grid: Care Personally (vertical) x Challenge Directly (horizontal). The most common failure mode for new managers is Ruinous Empathy — high care, low challenge. Never use a "shit sandwich" (praise-criticism-praise). Deliver criticism directly with care: "I'm sharing this because I believe in your growth. Here's the behavior, the impact, and what needs to change." *(Source: Kim Scott, "Radical Candor")*

### 1.4. Write first, talk second
Every decision, every proposal, every significant meeting outcome — write it down and share it async before discussing synchronously. Written culture scales. If it's not written down, it doesn't exist. *(Source: Will Larson; GitLab handbook; Stripe's "written culture")*

### 1.5. Frame problems as business problems, not people problems
Don't say "we need more engineers." Say "our feature delivery timeline slipped by 30% because our bus factor is 1 on the critical path, and we're maintaining 50% more legacy systems than our current team can sustainably support." *(Source: Camille Fournier)*

### 1.6. Communication ability predicts leadership more than code output
Academic research analyzing 133M GitHub interactions found that communication ability and community-building skills are stronger predictors of leader emergence than pure technical contribution. Invest in communication skills as much as technical skills. *(Source: arXiv 2203.10871, "Follow the Leader")*

---

## 2. Code Quality & Review

### 2.1. Keep PRs small
PRs under 200-400 lines get reviewed 50% faster, have higher quality feedback, and lower revert rates. Over 500 lines, defect detection drops significantly. Anything larger must be broken into smaller changes. *(Source: Google Engineering Practices; SmartBear/Harvard code review study)*

### 2.2. Code review is knowledge transfer, not gatekeeping
The review is the best opportunity to spread context across the team. Reviewers should start with high-level structure/architecture before nitpicking style. Authors must include context — what the PR does, why, and what tradeoffs were made. A PR without a description is not ready for review. *(Source: Will Larson)*

### 2.3. What you recognize is what you reward
The behaviors you highlight in code reviews, demos, and promotion packets become the de facto standards. If you reward shipping velocity in public while talking about quality in private, your team will optimize for velocity. *(Source: Lara Hogan)*

### 2.4. Human review is non-negotiable with AI-generated code
AI-generated code entering repositories creates a self-training loop risk. Human PR review interrupts this loop and prevents model collapse. The first pass of code review can be automated; humans should focus on high-value strategic feedback. *(Source: arXiv 2506.2636; Will Larson)*

### 2.5. Quality comes from tight feedback loops
The most effective way to improve software quality is to create a tight feedback loop between writing code and seeing it fail in production. Invest in CI/CD, observability, and fast deployment cycles — they improve quality more than any review process. *(Source: Will Larson, "An Elegant Puzzle"; "Accelerate" by Forsgren, Humble, Kim)*

---

## 3. Context

### 3.1. Context is the manager's primary deliverable
Engineers who understand the "why" make better autonomous decisions than those who only know the "what." Your job is to provide context about constraints, goals, tradeoffs, and stakeholders — then step back and let the team navigate. *(Source: Will Larson, "Layers of Context")*

### 3.2. All interesting problems operate across multiple context layers
When evaluating a proposal, identify the context layers: the team's context, the infrastructure team's context, and the leadership's context. When an engineer's proposal keeps getting pushback from peers, diagnose whether the problem is missing context layers, not technical merit. *(Source: Will Larson, "Layers of Context")*

### 3.3. Translate executive energy, don't fight it
Executives are generally directionally correct but specifically wrong. Instead of fighting a bad idea, translate it into a useful one. "You want to rewrite the entire system" becomes "Let's do a narrow test rewrite of one component to validate the approach." *(Source: Will Larson, "Executive Translation")*

### 3.4. Extract the kernel
When someone asks a question that seems off-base, identify the true intent. If an executive asks "Can't you just use ChatGPT?", the kernel is almost certainly not about ChatGPT — it's about the timeline feeling too slow. Respond to the real concern, not the surface suggestion. *(Source: Will Larson, "Extract the Kernel")*

### 3.5. No Wrong Doors
When someone shows up with a question, the first responder should be a navigator, not a bouncer. Make the first contact point a support system for navigating the org, not a gate. Most misalignment comes from missing context. *(Source: Will Larson, "No Wrong Doors")*

### 3.6. Ownership without context is just responsibility without authority
Pair ownership with decision-making power. Modular codebases with clear boundaries enable meaningful ownership. Monolithic codebases prevent it. *(Source: arXiv 2505.14220, "A Mosaic of Perspectives: Understanding Ownership in SE")*

---

## 4. Delegation

### 4.1. Delegate outcomes, not tasks
Give people the "what" and the "why," not the "how." Specify: the problem to solve, the success criteria, the deadline, and the boundary of decision-making authority. Do not prescribe the implementation. "You can't delegate the work while retaining all the decisions — that's just assigning tasks." *(Source: Julie Zhuo, "The Making of a Manager")*

### 4.2. The progressive autonomy ladder
For new or struggling team members: Watch me do it → We do it together → You do it, I review → You do it. Move up deliberately. Move down when someone is stuck without making it a demotion. *(Source: Julie Zhuo)*

### 4.3. After delegating, don't disappear
Schedule three check-in points: 25% progress (course correction), 50% progress (deep review), 90% progress (polish and ship). Adjust frequency based on the person's experience level. *(Source: Julie Zhuo)*

### 4.4. Delegation is a learnable skill, not innate
Effective delegation combined with transformational leadership improves workflow, team motivation, and productivity. Train managers explicitly on how and what to delegate. The 3-5 month team formation period is optimal for transferring leadership responsibilities. *(Source: arXiv 2405.01612, "Effective Delegation and Leadership in Software Management")*

### 4.5. The delegation checklist (before handing off)
(1) Have they done it before? (2) Do they understand the success criteria? (3) Do they know where to get help? (4) Have we agreed on check-in cadence? (5) What decisions can they make autonomously vs. need approval for? *(Source: James Stanier, "The Engineering Executive's Way")*

### 4.6. If delegation feels hard, you're not delegating enough
The discomfort of letting go is a signal that you're holding onto too much. If you're the only person who can do something, that's a bus factor problem, not a delegation problem. Invest the time to teach someone else — it pays back in weeks. *(Source: Sarah Drasner, "Eng Management for the Rest of Us")*

### 4.7. Better to micromanage than be disengaged
Micromanagement at least shows you're paying attention. Disengagement is worse because the team flies blind. The real skill is having multiple leadership styles and knowing when to use each: leading with policy, leading from consensus, or leading with conviction. *(Source: Will Larson, "An Elegant Puzzle")*

---

## 5. Asking the Right Questions

### 5.1. Ask first, assert second
Questions are cheap. Credibility is expensive. Before giving feedback, ask: "What have you already tried? What constraints are you working under? What would happen if you tried Y instead?" *(Source: Will Larson, "Constraints on Giving Feedback")*

### 5.2. Replace generic questions with specific ones
Instead of "How are things going?" ask "What's one thing you'd change about your workday if you could?" Instead of "Any feedback for me?" ask "What's something I do that gets in your way?" *(Source: Lara Hogan, "Questions for our first 1:1")*

### 5.3. For stuck employees, probe don't prescribe
Ask: "What part of this feels hardest to you right now?" "If you knew you couldn't fail, what would you try?" "What's the smallest step you could take this week?" *(Source: Lara Hogan)*

### 5.4. The "why can't they just X" test
Every time you think "Why can't they just X," you're missing context. There is always a reason why they "can't just X." Never dismiss it — investigate it. *(Source: Lara Hogan)*

### 5.5. Before asserting, audit your own confidence
Ask yourself: "Why am I confident in my perspective? Is it because I've worked on a similar problem, done research, or modeled the problem out?" If you can't explain why you're confident, you won't convince others. *(Source: Will Larson)*

### 5.6. When you disagree with a decision, ask how it was made
Not "Why was this bad decision made?" but "How was this decision made?" Understanding the process reveals whether the outcome was a fluke or the process is broken. *(Source: Will Larson, "Predictability")*

---

## 6. Tools & Systems

### 6.1. Tools should solve current problems, not aspirational ones
"Good process is a solution to your current challenges." Any process will change to scale to 10,000 people, and almost no process makes sense in a 2-person company. Choose tools for where you are, not where you wish you were. *(Source: Will Larson, "An Elegant Puzzle")*

### 6.2. Culture problems are usually systems problems
"Culture eats strategy for breakfast" is misapplied. A company that wants to "move with urgency" but requires founder approval on all external-facing work doesn't have a culture problem — it has a bottleneck problem. Fix the system; the culture follows. *(Source: Will Larson, "Culture vs Systems")*

### 6.3. Keep tracking overhead under 5-10% of engineering time
If tracking takes more than that, it's ceremony, not management. Use lightweight tools (Linear, GitHub Issues) for execution. Use dedicated tools (Notion, Productboard) for strategy. Track outcomes, not output — what shipped and what impact it had, not story points. *(Source: Camille Fournier; Will Larson)*

### 6.4. Measure DORA metrics, ignore activity metrics
The Four Key Metrics that correlate with organizational performance: (1) Deployment frequency, (2) Lead time for changes, (3) Mean time to recover (MTTR), (4) Change failure rate. Ignore lines of code, commits per day, hours worked, and individual velocity — they are noise. *(Source: Forsgren, Humble, Kim, "Accelerate"; Google DORA)*

### 6.5. Strategy emerges from design documents, not from strategy offsites
To write an engineering strategy, write five design documents and pull the similarities out. Five strategies into a vision. Strategy is boring and specific — it's documenting what you're already doing and why. *(Source: Will Larson, "Crafting Engineering Strategy")*

### 6.6. Retrospectives are the highest-leverage tool for continuous improvement
Most issues found in retrospectives are team-level learning and improvement items, not technical. Large-scale projects need structured retrospective processes to handle the volume of action items. *(Source: arXiv 1805.10310, "Learning in the Large")*

### 6.7. ADRs prevent recurring debates
Architecture Decision Records: capture context, decision, and consequences for every architectural choice. Standard format: Title, Status, Context, Decision, Consequences. New team members can onboard themselves to past decisions. *(Source: Michael Nygard / ThoughtWorks)*

### 6.8. Design teams for cognitive load, not org charts
A team's maximum cognitive load is roughly constant. If a team owns more than they can cognitively manage, technical direction degrades. Resize ownership boundaries, not headcount. Use four fundamental topologies: stream-aligned (default), enabling, complicated-subsystem, and platform. *(Source: Skelton & Pais, "Team Topologies")*

---

## 7. Skills Development

### 7.1. Tackle the causes of unhappiness before trying to boost happiness
Remove blockers, reduce context switching, fix broken build pipelines, eliminate unnecessary meetings. This is higher ROI than perks or team-building. *(Source: arXiv 1703.01575, "On the Unhappiness of Software Developers")*

### 7.2. Categorize overwhelm and address each type differently
Communication overwhelm → async-first. Disturbance overwhelm → focus time blocks. Variety overwhelm → clear ownership areas. Technical overwhelm → mentoring and pairing. Don't apply the same solution to different problems. *(Source: arXiv 2406.00606, "Overwhelmed Software Developers")*

### 7.3. Recognize non-code contributions
Mentoring, code review quality, documentation, process improvements — these sustain team health. Make invisible work visible. Celebrate the unsung work in every team meeting. *(Source: arXiv 2007.08237; Julie Zhuo)*

### 7.4. The most underused management tool is public credit
Praise in public, coach in private. When you mention someone's project in a promotion email, ask a team to demo their release, or add a Slack high-five to a comment, you are implicitly recognizing something you like. Be deliberate about what you recognize. *(Source: Lara Hogan; Camille Fournier)*

### 7.5. Vicarious learning is real
Teams absorb skills by watching others, hearing about mistakes, and seeing what worked. This is why postmortems are great for building context. Organize structured sessions where engineers share practical learnings about tools and techniques. *(Source: Lara Hogan)*

### 7.6. Conflict resolution training is a prerequisite for team autonomy
Teams need negotiation and conflict resolution skills to reach productive autonomy. Most conflicts originate at the team level, not the individual level, so address them team-wide. *(Source: arXiv 1904.06285, "The Importance of Conflict Resolution Techniques")*

### 7.7. The impact of individual judgment has never been higher
Develop domain expertise by getting your hands dirty. Executives and senior managers who don't understand the technical domain make worse decisions. Maintain enough depth to evaluate technical decisions and assess talent. *(Source: Will Larson; "Accelerate")*

---

## 8. Decision-Making

### 8.1. Use structured frameworks, not intuition
Technical decisions are susceptible to systematic cognitive biases: anchoring (first estimate anchors discussion), confirmation bias (seeking evidence for a chosen approach), planning fallacy (underestimating time/cost). Mitigation strategies (pre-mortems, independent estimates, decision matrices) are underused in practice. *(Source: arXiv 1707.03869, "Cognitive Biases in Software Engineering")*

### 8.2. Technical debt decisions must be framed in business terms
Cost of delay, risk exposure, feature velocity impact — these are the language stakeholders understand. A business-driven approach to technical debt prioritization aligns stakeholders across business and technical teams. *(Source: arXiv 2010.09711, "Business-Driven Technical Debt Prioritization")*

### 8.3. Default to "yes, and here's what it costs"
When leadership asks for something, don't say "no." Say "yes, and to do that we'll have to delay X, reduce quality on Y, or add headcount Z. Which do you prefer?" This reframes the conversation from a binary yes/no to a resource allocation discussion. *(Source: Fitzpatrick & Collins-Sussman, "Debugging Teams")*

### 8.4. Use the "three levels" structure for every leadership update
Level 1: Exec summary (3 sentences max) with the bottom line up front. Level 2: Key data and reasoning (1 paragraph). Level 3: Supporting details (appendix). Always lead with Level 1. Never start with Level 3 and work backward. *(Source: James Stanier, "The Engineering Executive's Way")*

### 8.5. Use "Situation, Complication, Resolution" for executive communication
Situation: what's happening. Complication: what makes it hard. Resolution: what you're doing or recommending. This is the standard format for anything going to leadership. *(Source: James Stanier)*

### 8.6. The 24-hour pre-read
Send a brief email 24 hours before a meeting with the situation and your proposed solution. This gives people time to absorb the information and arrive ready to make a decision, not react emotionally. This is the single highest-ROI communication habit. *(Source: Camille Fournier)*

### 8.7. Use "Even/Over" statements as forcing functions
"We prioritize reliability over new features" or "We prioritize speed of learning over stability." These clarify priorities and communicate them to the team unambiguously. *(Source: Julie Zhuo)*

---

## 9. Hiring & Onboarding

### 9.1. Size teams in the 6-8 person Goldilocks zone
Teams smaller than 4 lack bus factor and context diversity. Teams larger than 10 suffer from coordination overhead that exceeds per-person productivity gains. Always split a team before it reaches 10. *(Source: Will Larson, "An Elegant Puzzle")*

### 9.2. Don't hire to backfill — hire to solve a constraint
Before opening a headcount, identify the single constraint most limiting the team's output. Design the role around that constraint, not around "replacing Bob." *(Source: Will Larson)*

### 9.3. Always hire for resilience
Ask behavioral questions about projects that went wrong, feedback they received and disagreed with, times they had to work with a difficult stakeholder. How they respond tells you more about long-term success than their clean-slate problem-solving ability. *(Source: Camille Fournier)*

### 9.4. Structure onboarding with clear milestones
Week 1: dev environment set up, first small PR. Month 1: shipped something to production. Month 3: owns a small project. Assign a mentor who is not the manager — their job is to be a safe person to ask dumb questions. *(Source: Camille Fournier; GitLab; Julie Zhuo)*

### 9.5. The first small win in the first week
Onboarding should produce a "first small win" in the first week. Build confidence early. Every new hire should ship something — even if trivial — within their first 7 days. *(Source: Camille Fournier)*

---

## 10. Performance & Conflict

### 10.1. Distinguish "skill" vs "will" before intervening
Skill problems (can't do it) need training, mentorship, or reassignment. Will problems (won't do it) need clear expectations, consequences, and possibly a PIP. Mixing them up is the most common performance management mistake. *(Source: Kim Scott, "Radical Candor")*

### 10.2. Look for "organizational bugs" before individual bugs
When someone underperforms, first check the system: is the team structure wrong? Is the on-call rotation burning them out? Are they blocked by dependencies? Individual performance problems are often symptoms of systemic problems. Fix the system first, then the person. *(Source: Fitzpatrick & Collins-Sussman, "Debugging Teams")*

### 10.3. The "coach, manage, fire" framework
Spend 80% of your coaching energy on the "Coach" category (high performers who need growth guidance), not the "Fire" category. Most underperformers who can be saved will save themselves when given clear expectations. *(Source: Camille Fournier, "The Manager's Path")*

### 10.4. Document everything before a PIP
Before starting a Performance Improvement Plan, ensure you have: (1) written feedback from at least 4 weeks of 1:1s, (2) specific examples of missed expectations, (3) evidence that coaching was attempted. A PIP should never be a surprise. If they're surprised, you failed as a manager. *(Source: Camille Fournier)*

### 10.5. Early intervention for conflict is everything
Small frictions resolved early are easy. Festering conflicts are expensive. If you know about two team members who don't work well together, address it within a week. Frame debates around outcomes, not positions. *(Source: Kim Scott; Will Larson)*

### 10.6. The "Boat Anchor" rule
Someone who is brilliant but toxic is a net negative. A 10x engineer who makes 10 other people 50% less productive is destroying value. Fire them, even if they're "too important to fire." The team will be faster without them in 3 months. *(Source: Fitzpatrick & Collins-Sussman, "Debugging Teams")*

---

## 11. Be a thermostat, not a thermometer

### 11.1. You set the temperature of the room
Managers set the temperature of the room rather than reflecting it. Moods are contagious and your team mirrors your energy. If you bring panic, the team panics. If you bring calm and direction, the team follows. *(Source: Lara Hogan)*

### 11.2. The leader saying "I was wrong" is the highest-leverage culture move
When a manager publicly says "I was wrong about X, and here's what I learned," it gives the entire team permission to be wrong, to learn, and to speak up. This builds psychological safety faster than any team-building exercise. *(Source: Fitzpatrick & Collins-Sussman, "Debugging Teams")*

### 11.3. Be a navigator, not a gate
Your job is to help your team navigate the organization, not to protect them from it. Teach them how to influence peers, how to build support for their ideas, and how to work the system to get things done. *(Source: Will Larson, "Navigators"; "No Wrong Doors")*

### 11.4. Build organizational influence before you need it
Write documents, give talks, run working groups, and build relationships with peers long before you need to drive a cross-org initiative. Influence cannot be borrowed instantly — it must be deposited over time. Aim for 3-5 deposits before every withdrawal. *(Source: Will Larson, "Staff Engineer")*

### 11.5. Sponsor people, don't just mentor them
Mentorship is advice. Sponsorship is putting your thumb on the scale to help someone advance. Recommend them for opportunities, advocate for them in promotion meetings, give them visibility with leadership. Sponsorship is more powerful than mentorship. *(Source: Will Larson, "Staff Engineer")*

---

## 12. Summary: The Most Important Practices at a Glance

| Topic | Highest-Leverage Practice | Source |
|---|---|---|
| **1:1s** | They talk 80%. It's their meeting, not yours. | *Manager's Path* |
| **Delegation** | Delegate outcomes with clear success criteria, not tasks. | *Making of a Manager* |
| **Code review** | Small PRs + human review for strategic feedback. | *Larson; Google* |
| **Context** | Context is your primary deliverable. Start with "why." | *Larson* |
| **Technical direction** | Measure everything against the Four Key Metrics. | *Accelerate* |
| **Performance** | Distinguish skill vs. will before intervening. | *Radical Candor* |
| **Culture** | Saying "I was wrong" as a leader is the highest-leverage move. | *Debugging Teams* |
| **Headcount** | Size teams at 6-8; split before 10. | *An Elegant Puzzle* |
| **Leadership comms** | Bad news does not get better with time. Surface it immediately. | *Engineering Executive's Way* |
| **Decision-making** | Use structured frameworks, not intuition. | *arXiv 1707.03869* |
| **Conflict** | Early intervention is everything. Address within a week. | *Radical Candor* |
| **Systems** | Fix the system; the culture follows. Most culture problems are system problems. | *An Elegant Puzzle* |

---

*Primary sources: Will Larson (An Elegant Puzzle, Staff Engineer, lethain.com), Camille Fournier (The Manager's Path, medium.com), Julie Zhuo (The Making of a Manager, medium.com), Lara Hogan (Resilient Management, larahogan.me), Kim Scott (Radical Candor), James Stanier (The Engineering Executive's Way, theengineeringmanager.com), Fitzpatrick & Collins-Sussman (Debugging Teams), Skelton & Pais (Team Topologies), Forsgren, Humble & Kim (Accelerate), Michael Lopp (Managing Humans), Charity Majors (charity.wtf), Lena Reinhard (lenareinhard.com), Google DORA (Accelerate State of DevOps), Google Project Oxygen, Microsoft Research SPACE Framework, arXiv research on SE management.*

*Compiled July 2026 from web research, academic database searches, and book distillations.*