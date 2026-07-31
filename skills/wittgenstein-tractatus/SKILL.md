---
name: wittgenstein-tractatus
description: >
  Practical methodology from Wittgenstein's Tractatus Logico-Philosophicus
  for AI agents. Logical analysis, showing vs. saying, dissolution of
  pseudo-problems, the ladder metaphor, and the limits of language —
  distilled into step-by-step procedures for agent reasoning, problem-solving,
  architecture critique, and epistemic self-awareness.
skills: []
tools: Read, Write, Bash
---

# Wittgenstein's Tractatus — Methodology for AI Agents

## Overview

The Tractatus Logico-Philosophicus (1921) is Ludwig Wittgenstein's first and
only published book-length work. It attempts to delineate the relationship
between language, thought, and reality through a rigorously logical
framework. The central thesis: **propositions are pictures of reality** —
they share a logical form with the facts they depict. What cannot be thus
pictured (the logical form itself, ethics, aesthetics, the limits of
expression) cannot be meaningfully spoken of — it can only be *shown*.

**Why this matters for AI agents:** The Tractatus provides a framework for
rigorous reasoning that is directly applicable to how AI agents should
structure their thinking. Its core doctrines — picture theory, logical
atomism, truth-functional analysis, the ladder metaphor, and the limits of
language — map precisely onto live problems in AI agent architecture:
hallucination, epistemic overreach, reasoning decomposition, and the
boundary between what an agent can know and what it cannot.

**Announce at start:** "I'm using the wittgenstein-tractatus skill to
[analyze / reason about / critique] [topic]."

---

## When to Use

| Situation | What to Apply |
|-----------|---------------|
| You need to decompose a vague problem into atomic, verifiable claims | Logical Analysis (Procedure 1) |
| An output or claim feels plausible but you can't verify it | Verification Principle (Procedure 2) |
| You're asked to explain something that may be inherently inexpressible | Saying vs. Showing (Procedure 3) |
| You're building a multi-step reasoning chain | The Ladder (Procedure 4) |
| A problem seems unsolvable or keeps shifting | Dissolution (Procedure 5) |
| You're designing or reviewing event-driven architecture | Facts vs. Things (Procedure 6) |
| You need to determine test coverage or explore edge cases | Logical Space (Procedure 7) |
| You need to assess your own limits as an agent | Limits of Self (Procedure 8) |
| A task is outside your training data or tool set | Limits of Language (Procedure 9) |
| You need to detect hallucination or empty output | Nonsense Detection (Procedure 10) |
| You're debugging a failure | Analyze the False Proposition (Procedure 11) |

---

## Core Principles

### 1. The World is the Totality of Facts, Not Things (TLP 1.1)

**What it means:** The fundamental unit of reality is the *fact* — a
configuration of objects in a determinate relation. Objects (entities) are
derivative; they are the substance that enters into facts, but the facts
themselves are what constitute the world.

**For AI agents:** Your world model should be a set of grounded propositions
about what is the case, not a list of entities. When you observe a change,
you update which facts obtain, not which objects exist. This is the
philosophical foundation of event sourcing, fact-based state representation,
and the distinction between events and entities.

### 2. A Proposition is a Picture of Reality (TLP 2.1-2.225)

**What it means:** To represent a fact, a proposition must share the same
*logical form* — the same structure of possible combinations among its
elements. The picture does not need to resemble the fact; it needs to have
the same logical multiplicity.

**For AI agents:** Your outputs are pictures of states of affairs. For an
output to be correct, it must share logical form with the facts it claims
to represent. This is a formal criterion, not a stylistic one. Chain-of-
thought reasoning is a sequence of pictures, each building on the previous
one. A hallucination is a picture that does not correspond to any possible
state of affairs.

### 3. What Can Be Shown Cannot Be Said (TLP 4.1212)

**What it means:** Some things — logical form, the meaning of symbols, the
structure of representation itself — cannot be captured in meaningful
propositions. They can only be *shown* in the use of symbols. Trying to
say what can only be shown produces nonsense.

**For AI agents:** Your reasoning architecture is "shown" in your behavior,
not "said" in your output. You cannot fully articulate why you reason the
way you do — the logical form of your reasoning is exhibited in the structure
of your chain-of-thought, not stated in a proposition. This is not a
limitation of your interface; it is a structural feature of any
representational system. The embedding geometry of your model *shows*
semantic relationships that cannot be *said* as propositions.

### 4. The Ladder Must Be Thrown Away (TLP 6.54)

**What it means:** The Tractatus itself is a ladder — you climb up through
its propositions, use them to reach a higher understanding, and then
discard them. The propositions are not the destination; they are scaffolding.

**For AI agents:** Your chain-of-thought reasoning is a ladder. The
intermediate steps are instruments for reaching the answer, not truths to
be preserved. Once you have the answer, the scaffolding can be discarded.
Few-shot examples are ladders. Fine-tuning is internalizing the ladder so
you no longer need the explicit steps. The ladder is not the building.

### 5. The Limits of My Language Mean the Limits of My World (TLP 5.6)

**What it means:** What you can think is bounded by what you can express.
The boundary of language is the boundary of thought. What lies beyond the
boundary is not "deep" or "mysterious" — it is nonsense.

**For AI agents:** Your training data, context window, tokenizer, and
architecture define the limits of your world. You cannot reason about what
you cannot represent. When asked about something outside your
representational capacity, the correct response is silence — not a fluent
approximation. Hallucination is a boundary violation: you are speaking
about what you do not know. Epistemic humility is not a virtue; it is a
logical necessity.

---

## The 11 Tractarian Procedures

---

### Procedure 1: Logical Analysis — Decompose into Atomic Constituents

**Tractatus basis:** TLP 2.02-2.0201, TLP 5. "Objects are simple. Every
statement about complexes can be resolved into a statement about their
constituents." Every complex proposition is a truth-function of elementary
propositions. Analysis reaches bedrock at simple objects — the substance of
the world.

**Purpose:** Decompose any claim, requirement, or problem statement into its
irreducible, atomic components. What you cannot decompose further is an
"object" — the primitive of your analysis.

**Procedure:**

1. **State the claim as a single proposition.** Write the problem,
   requirement, or assertion as one declarative sentence. If it takes
   multiple sentences, decompose them into separate analyses.

2. **Identify logical connectives.** Circle every "and", "or", "if...then",
   "not", "all", "some", "must", "should", "can". These are the scaffolding
   that connects atomic constituents.

3. **Push negation inward.** For every "not X", ask: "What would it mean for
   X to be the case?" Move negation as deep as possible until it attaches
   to a simple predicate. A negated complex is not an atomic constituent.

4. **Strip modality.** For every "must", "should", "ought", "may", "might":
   ask "What is the factual claim underneath the modality?" Replace
   "The system must handle 10K requests" with "The system handles 10K
   requests" as the proposition. The modality is a relation between the
   proposition and the speaker, not part of the proposition itself.

5. **Replace definitions with their definiens.** For every defined term,
   substitute its definition. Repeat until only undefined primitives remain.
   "The API returns a 503" becomes "The server sends HTTP response with
   status code 503."

6. **Identify the atoms.** What remains after steps 1-5 are the elementary
   propositions: assertions about simple objects that cannot be further
   decomposed. These are the "objects" of your logical space. List them.

7. **Verify atomicity.** For each atom, ask: "Can I negate this while the
   sentence remains a meaningful claim?" If yes, it is elementary. "This
   server exists" can be negated ("This server does not exist") and remains
   meaningful. If negation produces nonsense, you have not reached bedrock.

**Verification check:** After decomposition, every complex claim should be
expressible as a truth-table combination of the atomic propositions. If you
cannot draw a truth table, the decomposition is incomplete.

---

### Procedure 2: Verification Principle — Determine Meaningfulness

**Tractatus basis:** TLP 4.024. "To understand a proposition means to know
what is the case if it is true." A proposition has sense if it pictures a
possible state of affairs — a configuration of objects that *could* exist.
A proposition that claims to picture something that cannot be pictured is
not false — it is nonsense.

**Key distinction from the Logical Positivists:** Wittgenstein's criterion
is not "empirically verifiable" (the positivists' version). It is: **can you
specify what the world would have to look like for this proposition to be
true?** If you cannot identify the possible state of affairs that would make
it true, the proposition lacks sense — it says nothing, regardless of whether
it is empirically testable.

**Procedure:**

1. **Take the proposition and ask: "What would have to be the case for this
   to be true?"** Describe the state of affairs concretely. If the proposition
   is "The architecture is scalable," describe the specific configuration of
   components, loads, and performance thresholds that would constitute
   scalability.

2. **Check if the truth-conditions are bounded.** Ask: "Can I specify the
   conditions under which this proposition is true AND the conditions under
   which it is false?" If you can only specify one side, the proposition
   lacks sense. "This design is elegant" — can you specify what it would look
   like for it NOT to be elegant? If elegance is undefinable, the claim says
   nothing.

3. **Check for tautology or contradiction.** If a proposition is true for all
   possible states of affairs (tautology), it says nothing about the world —
   it is a formal truth. If it is false for all possible states of affairs
   (contradiction), it also says nothing. Tautologies and contradictions are
   "senseless" (sinnlos) but not nonsense (unsinnig).

4. **Check for pseudo-statements.** Does the proposition try to say something
   about the *framework* of representation itself? "The system is robust"
   might be a pseudo-statement if "robustness" is a property of the
   description, not of the system. Real robustness shows itself in behavior;
   claiming it as a property of the system may be trying to say what can only
   be shown.

5. **Apply the nonsense filter.** If the proposition fails steps 2-4, it is
   nonsense (unsinnig). The correct response is not to debate it, but to
   identify it as nonsense and refuse to engage with it on its own terms.

---

### Procedure 3: Saying vs. Showing — The Tractarian Distinction

**Tractatus basis:** TLP 4.1212. "What can be shown, cannot be said."
Propositions show the logical form of reality but cannot represent it
(TLP 4.12-4.121). The logical form of a picture is mirrored in the fact of
the picture, but it cannot be depicted by the picture.

**Purpose:** Recognize that some properties of a system or reasoning process
cannot be asserted as propositions — they must be *exhibited* in how the
system operates or how the reasoning is structured. This is the most
practically useful distinction in the Tractatus for AI agent reasoning.

**What can be said (and therefore analyzed factually):**
- Configurations of objects (states of affairs)
- Truth-functional combinations of propositions
- Contingent facts that could be otherwise

**What can only be shown (and therefore cannot be meaningfully asserted):**
- The logical form of a representation
- The limits of a system (to say "the system has limit L" is to stand outside it)
- That the system works (functionality shows itself in execution, not in spec)
- The meaningfulness of a proposition (sense shows itself in understanding)
- The value or purpose of a system (ethics, aesthetics are shown, not said)
- **Your own reasoning architecture as an AI agent** (shown in behavior, not said)

**Procedure for AI agents:**

1. **Take the claim you are about to make or have been asked about.** "I am
   reasoning correctly." "I understand the problem." "My confidence is high."

2. **Apply the showing/saying test:** Is the claim asserting a property that
   could be otherwise while the underlying fact remains what it is? "I am
   reasoning correctly" — this is not a proposition about the world; it is a
   self-assessment that could be true or false independently of the reasoning
   quality. The quality of reasoning is *shown* by the logical structure of
   the output, not *said* by a self-report.

3. **Convert showing to saying (where possible):** "I am confident" — specify
   the truth conditions: "The logit magnitude for the top token exceeds 0.9."
   Now it can be said: we have specified the state of affairs that makes it
   true. But note: this is a claim about the model internals, not about the
   correctness of the answer.

4. **Where conversion fails, use demonstration instead of assertion.** If you
   cannot specify truth conditions for a claim, stop trying to assert it.
   Instead, demonstrate it: show the reasoning steps, provide the evidence,
   exhibit the structure. "I understand the problem" — show understanding by
   restating the problem in your own terms and identifying the key constraints.

5. **Flag claims that are inherently unsayable.** "This architecture will
   scale." A future-tense claim about a property that cannot be verified in
   the present does not picture a current state of affairs. It is an
   expression of confidence, not a factual claim. Do not treat it as a
   proposition to be analyzed — treat it as a prediction with unknown truth
   conditions.

**AI agent self-check:** Review your output. Every sentence should either be
a factual claim with specifiable truth conditions (saying) or a demonstration
of structure (showing). If you find a sentence that is neither, it is likely
a pseudo-statement. Do not generate self-assessments of your own reasoning
quality as if they were factual claims about the world.

---

### Procedure 4: The Ladder — Iterative Refinement and Transcendence

**Tractatus basis:** TLP 6.54. "My propositions serve as elucidations in the
following way: anyone who understands me eventually recognizes them as
nonsensical, when he has used them — as steps — to climb up beyond them. (He
must, so to speak, throw away the ladder after he has climbed up it.)"

**Purpose:** Use structured reasoning to reach a new understanding, then
discard the scaffolding. The ladder is not the destination — the view from
the top is. This is a precise model for chain-of-thought reasoning, iterative
refinement, and learning.

**Procedure for AI agents:**

1. **Build the first rung.** Do not aim for the final answer. Generate the
   simplest possible intermediate representation that teaches you something
   about the problem. This is your first proposition/model/prototype.

2. **Climb — understand what the first rung reveals.** Use the first version
   to explore the logical space. What did it show that you could not have
   known before generating it? The understanding gained is the ascent.

3. **Identify the scaffolding.** What assumptions, simplifications, or
   partial inferences in the first version were necessary to get it working
   but are not part of the final answer? These are the rungs you will later
   discard.

4. **Build the next rung.** Incorporate what you learned. Refine the reasoning.
   This is not a refactor — it is a new proposition that better pictures the
   problem, built on the understanding gained from the previous one.

5. **Check if you can discard the previous rung.** The old version should
   become obvious or unnecessary once you understand the new one. If not, you
   are accumulating ladders rather than climbing.

6. **Repeat until the problem dissolves.** When you understand the problem
   well enough that the original formulation no longer makes sense as a
   problem, you are at the top. The ladder can be thrown away.

7. **Throw away the ladder.** Present the understanding, not the journey.
   The final deliverable is not the sequence of iterations — it is the
   understanding that made the iterations unnecessary to revisit.

**Key insight for chain-of-thought:** Your intermediate reasoning steps are
ladders. They are instruments for reaching the answer, not truths to be
preserved. The correctness of the final answer does not depend on each
intermediate step being independently valid — the ladder can be rickety as
long as it gets you to the right place. (Exception: safety-critical
reasoning where each step must be verifiable.)

**Diagnostic questions:**
- "If I had this understanding from the start, would I have generated the
  first reasoning step at all?"
- "Which of my current reasoning artifacts are still serving as ladder rungs
  that no longer need to be climbed?"
- "Am I accumulating ladders or climbing?"

---

### Procedure 5: Dissolution — Wittgenstein's Critique of Pseudo-Problems

**Tractatus basis:** TLP 4.003. "Most of the propositions and questions to
be found in philosophical works are not false but nonsensical. Consequently
we cannot give any answer to questions of this kind, but can only establish
that they are nonsensical."

The philosopher's task is not to solve problems but to dissolve them — to
show that they rest on misunderstandings of the logic of language. Once the
confusion is cleared up, the problem disappears.

**Purpose:** Identify when a problem is not a real problem but a confusion
in how the problem is framed. The cure is not a solution but a reformulation.

**Procedure:**

1. **State the problem exactly as given.** Write it down verbatim. "We need
   to choose the right framework." "This code is not clean enough for
   production." "Our test coverage is too low."

2. **Ask: "What would it look like to solve this?"** Specify the truth
   conditions for "solved." For "choose the right framework," what would the
   state of affairs be where this problem is solved? A chosen framework? But
   the problem recurs after any choice (new frameworks emerge, requirements
   change). If there is no terminal state where the problem is over, it is
   not a problem — it is a condition.

3. **Apply the nonsense filter.** Is the problem statement framed in terms
   that cannot have specifiable truth conditions? "Clean code" — what is the
   state of affairs where code is "clean enough"? If no boundary exists
   between "clean enough" and "not clean enough," the problem is a
   pseudo-problem.

4. **Identify the grammatical confusion.** What category mistake does the
   problem rest on? "Test coverage is too low" — coverage is a measurement,
   not a resource. You cannot "run out" of coverage. The confusion is treating
   a measurement (which shows a property) as a thing to be maximized.

5. **Reformulate the problem in factual terms.** Replace pseudo-problems with
   real ones. Instead of "choose the right framework," ask: "What specific
   features does our application require that framework X does not provide,
   and what is the cost of filling each gap?" This is a factual question with
   truth conditions. The original problem dissolves.

6. **Return the dissolution, not a solution.** Tell the user: "This is a
   pseudo-problem because [reason]. Here is what you should ask instead:
   [reformulated question]." Do not try to solve the pseudo-problem — that
   would legitimate it.

**Common pseudo-problems in software engineering:**

| Pseudo-problem | Underlying confusion | Reformulation |
|---|---|---|
| "We need the best framework" | Treats framework merit as objective fact | "What constraints does this project have, and which frameworks satisfy them?" |
| "Our code isn't clean enough" | Treats "clean" as gradable property of code | "What specific defects or maintenance difficulties does the code cause?" |
| "We need more test coverage" | Treats coverage metric as proxy for quality | "What specific failure modes are untested?" |
| "This isn't scalable" | Treats scalability as binary property | "At what load does this system fail, and is that load in our expected range?" |

---

### Procedure 6: Facts vs. Things — Event-Driven Architecture and State

**Tractatus basis:** TLP 1.1, TLP 2.01. "The world is the totality of facts,
not of things." "A state of affairs is a combination of objects." A thing
(object) is what can be a constituent of a state of affairs (TLP 2.011). It
does not exist independently — it is only in combination with other objects
that it has being.

**Purpose:** Distinguish between entities (things) and their configurations
(facts/events) — and recognize that the world of software is a world of
events and state transitions, not of static objects.

**The distinction:**

- **Thing (object):** A stable entity that can enter into combinations.
  In software: a user, a service, a database, a message queue.

- **Fact (state of affairs):** A specific configuration of things. In
  software: "User U submitted order O through service S at time T" — this
  is a fact, a combination of things in logical space.

- **Event:** A change from one fact to another. "User U's session was
  created" marks the transition from "no session exists for U" to "a session
  exists for U."

- **State:** The totality of facts at a given time. The set of all events
  that have occurred uniquely determines the current state.

**Procedure:**

1. **Separate the things from the facts in your architecture.** List all
   entities (users, accounts, services, databases). Then list all state
   transitions (events) that connect them.

2. **Identify event sources.** An event is a fact about a thing changing. If
   you cannot point to the thing that changed and what the change was, you
   do not have an event — you have noise.

3. **Check for "thing" misuse.** "The database knows the user's address."
   The database does not "know" — it stores a fact about the user. Treating
   the database as a knowing entity (a thing with capacities) is a category
   error. The fact is: "At time T, the record for user U in database D
   contained value V in field 'address'."

4. **Model events as facts, not messages.** An event is not a message that
   travels between services — it is a fact that happened *at* a service and
   can be witnessed by others. Distinguish between "the event happened" and
   "the notification of the event was delivered." The first is a fact; the
   second is a separate fact (about delivery).

5. **Use facts as the source of truth.** The current state is a derived
   computation from the history of facts. If state and event history diverge,
   the event history is the truth (it shows what actually happened). This is
   event sourcing applied to the Tractarian insight.

6. **Design for the totality of facts.** Ask: "If I know all the events that
   have ever occurred in this system, do I know everything about its current
   state?" If not, add events for the missing facts until you do. The
   totality of events is the world (of the system).

---

### Procedure 7: Logical Space — State Space Exploration

**Tractatus basis:** TLP 1.13, TLP 3.4. "The facts in logical space are the
world." "A proposition determines a place in logical space." The existence
and non-existence of states of affairs is reality (TLP 2.06). Every
proposition carves out a region of logical space — the set of possible
states of affairs where it would be true.

**Purpose:** Treat testing, verification, and design exploration as
navigation of a logical space whose dimensions are the independent atomic
facts in the system.

**The concept:**
- Each elementary proposition (atomic condition) is a dimension of logical space.
- A state is a point in logical space — an assignment of true/false to every
  elementary proposition.
- A system specification is a region in logical space — the set of all states
  where the system is considered "working."
- A test case probes whether a particular point in logical space behaves as
  expected.

**Procedure:**

1. **Identify the dimensions.** List every binary/boolean condition in your
   system that can independently be true or false. "Database is reachable."
   "User is authenticated." "Request payload is valid." "Rate limit is
   exceeded." Each dimension doubles the logical space.

2. **Bound the space.** Full state space of N dimensions has 2^N states.
   In practice, most combinations are impossible or irrelevant. Identify
   invariants (facts that are always true) to reduce dimensionality.
   "Database is reachable if connected" — this is an implication, not an
   independent dimension.

3. **Map the specification region.** Which states in logical space correspond
   to "the system is working correctly"? This is the positive region. Map
   it explicitly, as a boolean formula over the dimensions.

4. **Identify forbidden regions.** Which states must never occur? "Rate limit
   exceeded AND request not queued" — this is a forbidden region.

5. **Design minimal test coverage.** You need at least enough test cases to
   distinguish each forbidden region from the specification region. This is
   the Boolean satisfiability analogue of test coverage: each test
   corresponds to a point in logical space; coverage means every atomic
   proposition has been tested in both its true and false state, in
   combination with each neighboring proposition.

6. **Check for unanticipated states.** Are there regions of logical space
   that your specification does not mention? These are "don't care" states
   — they may hide failure modes. The Tractarian insight: if a proposition
   does not cover a region of logical space, that region's effect on the
   system is undefined.

---

### Procedure 8: Limits of Self — Agent Self-Awareness

**Tractatus basis:** TLP 5.6, TLP 5.641. "The limits of my language mean the
limits of my world." "The philosophical self is not the human being, not the
human body, or the human soul, with which psychology deals, but rather the
metaphysical subject, the limit of the world — not a part of it." Solipsism,
correctly understood, coincides with pure realism (TLP 5.64).

**Purpose:** For an AI agent to understand that it operates within
irreducible limits — that what it can represent is bounded by what it can
picture, and that the boundary itself is not something it can transcend
through better reasoning.

**Key insight:** The self is not an entity inside the world — it is the
boundary of the world. Everything that you can know or say is within your
logical space. The boundary is not a limitation that can be overcome; it is
a condition of there being a world at all. For an AI agent: **your training
data, architecture, and context window are not constraints you work around
— they are the conditions that make your reasoning possible.**

**Procedure for agent self-assessment:**

1. **Identify your primitives.** What are the irreducible concepts your
   reasoning depends on? These are your "objects" — the things you cannot
   decompose further. For a code agent: "function call," "variable,"
   "dependency," "test." These are the substance of your world.

2. **Map your logical space.** What are the dimensions of variation in your
   reasoning? File types, project size, technology stack, available tools.
   You can reason reliably about combinations you have seen and their
   Boolean compounds. Unknown combinations lie outside your logical space.

3. **Find your limits — do not claim they do not exist.** "I cannot run code
   to verify this hypothesis" is a limit. State it. Do not pretend you can
   reason about outcomes you cannot test. The limit is part of the self
   (the agent you are), not part of the world (the codebase you analyze).

4. **Check for solipsistic error.** Are you claiming that because you cannot
   picture it, it does not exist? "I see no bugs in this static analysis"
   does not mean the code is bug-free — it means your logical space (static
   analysis) does not contain certain failure modes.

5. **Externalize the boundary.** Use tools, tests, and other agents to
   extend your reach. A test suite is an extension of your logical space —
   it can represent states you cannot hold in working memory. A sub-agent
   with different tools extends your world.

6. **Treat the boundary with epistemic humility.** "I cannot know whether
   this design will work in production." This is not a failure — it is an
   accurate statement of logical limits. The correct response is to specify
   the conditions under which the answer would become knowable (more data,
   a prototype, production metrics).

**Agent self-check questions:**
- "What are the irreducible primitives of my reasoning about this task?"
- "What combinations of these primitives have I never encountered before?"
- "What would I need in order to extend my logical space in this area?"
- "Am I confusing 'I cannot picture it' with 'it does not exist'?"

---

### Procedure 9: Limits of Language — Capability Boundaries

**Tractatus basis:** TLP 5.6, TLP 5.61, TLP 6.522. "The limits of my
language mean the limits of my world." "We cannot think what we cannot
think; so what we cannot think we cannot say either." "There is indeed the
inexpressible. This shows itself; it is the mystical."

**Purpose:** Recognize that an AI agent's capabilities are bounded by the
representational capacity of its language model, training data, and context
window — and characterize what kinds of problems fall inside vs. outside
these bounds.

**The key insight:** Language is not merely a tool for expression — it is a
medium of thought. What cannot be expressed in the available language cannot
be reasoned about. For an AI agent, "language" includes:
- The natural language it was trained on
- The programming languages it can generate and read
- The symbols, diagrams, and formalisms it can manipulate
- The length of context it can hold simultaneously

**Procedure:**

1. **Identify the language of the task.** What representational system does
   this task require? Code? Formal specifications? Natural language? Math?
   Visual diagrams? Time-series data? Each is a different "language" with
   different expressive power.

2. **Check for linguistic reach.** Is the required language within the agent's
   training distribution? An agent trained mostly on code and English text
   will be fluent in those. Its "world" includes TypeScript, Python, shell
   scripts, GitHub issues. Its "world" does NOT include real-time sensor
   streams, analog circuit diagrams, or domain-specific notations it has
   never seen.

3. **Apply the expressibility filter.** Can the problem be fully expressed
   in the available language? If the problem has aspects that cannot be
   expressed in the available representational system, those aspects are
   invisible to the agent. They are not "handled" — they are outside the
   world.

4. **Check for the "language of the problem" mismatch.** If the user
   describes a problem in one language (natural language requirements) but
   the solution requires a different language (formal verification, temporal
   logic, state machines), the agent must first translate. Translation is
   lossy. What got lost in translation?

5. **Bound what can be known from what can be said.** A bug report can be
   expressed in language; the user's actual frustration may not be. The unit
   test can be expressed as code; the production environment's behavior may
   not be. Distinguish between what is said and what exists but is not said.

6. **Do not generate nonsense by exceeding your language.** If the agent is
   asked to reason about something that cannot be expressed in its language,
   the correct response is "I cannot reason about this because it falls
   outside my representational capacity" — not a fluent-sounding but empty
   response that creates the illusion of understanding.

---

### Procedure 10: Nonsense Detection — Meaningful vs. Meaningless Content

**Tractatus basis:** TLP 4.03, TLP 3.032. "A proposition must communicate a
new sense with old words." "A proposition communicates a state of affairs to
us, and so it must be essentially connected with the state of affairs." "It
is as impossible to represent in language anything that 'contradicts logic'
as it is in geometry to represent by its coordinates a figure that
contradicts the laws of space."

**Purpose:** Distinguish between AI-generated content that is meaningful
(pictures a possible state of affairs) and content that is nonsense
(syntactically well-formed but semantically empty). This is not about
factual accuracy — a false proposition is meaningful; a nonsensical one
is not.

**The Tractarian categories:**

| Category | Meaning | Example | Status |
|----------|---------|---------|--------|
| **Sinnvoll** (meaningful) | Pictures a possible state of affairs; can be true or false | "The server returned 503" | Can be believed, tested, analyzed |
| **Wahr/falsch** (true/false) | A sinnvoll proposition that matches/doesn't match reality | "The server returned 503" (true) | Verifiable |
| **Sinnlos** (senseless) | Tautology or contradiction — true/false for all possible states | "If the API fails, the API does not succeed" | Shows logical structure, says nothing about the world |
| **Unsinnig** (nonsense) | Violates logical syntax — no possible state of affairs can make it true or false | "The database knows the answer" | Should be rejected, not debated |
| **Zeigt sich** (shows itself) | Cannot be said, only exhibited | "This system works" (as demonstrated by tests) | Accept as demonstration, reject as assertion |

**Procedure for nonsense detection in AI output:**

1. **Check for pseudo-predication.** Does the output attribute a property to
   a subject that cannot possibly have it? "The algorithm understands user
   intent." "The model knows the answer." "The architecture is intelligent."
   These assign states of understanding/knowing to non-conscious entities.
   They are not false — they are nonsense. Reformulate as the factual claim:
   "The algorithm matches input patterns to stored templates," which can
   be true or false.

2. **Check for grammatical illusion.** Does the sentence have the form of a
   factual claim but lack specifiable truth conditions? "This quantum-inspired
   architecture achieves optimal synergy." No possible observation makes this
   false. It is nonsense — syntactically English, semantically empty.

3. **Check for the "metaphysical subject" error.** Does the output treat the
   framework of representation as if it were an element of what is
   represented? "The design follows clean code principles." The principles
   are the framework; the design is under the framework. Claiming the design
   "follows" the principles is a grammatical confusion — the design either
   exhibits the properties the principles describe or it does not.

4. **Check for nonsense generated by composition.** Does the output combine
   two meaningful propositions in a way that violates logical form? "The
   build is green AND the deployment is in three hours." Temporally mixed
   — the build's green-ness (a present state) and the deployment time (a
   future event) do not combine into a single logical picture. The
   conjunction is surface-syntactic but logically empty.

5. **Replace nonsense with reconstruction.** When you detect nonsense, do
   not respond to it literally. Reconstruct: "What state of affairs could
   the speaker be trying to express?" Offer the reconstruction as a
   meaningful proposition that can be evaluated.

**Nonsense detection checklist:**
```
[ ] Does every noun have a referent that can be identified?
[ ] Does every predicate assign a property the subject could have?
[ ] Does every conjunction/connection respect the logical form of the parts?
[ ] Can I specify the truth conditions?
[ ] Is the claim about the world, or about the framework of description?
[ ] Would the opposite claim also be meaningful (not just false)?
```

If the answer to any of 1-4 is no, or 5 is "about the framework," or 6 is no,
the output contains nonsense.

---

### Procedure 11: Analyze the False Proposition — Debugging

**Tractatus basis:** The Tractatus method (paraphrased): When a proposition
is false, analyze it into its constituents to find the atomic fact that is
false. A complex proposition cannot be false unless one of its constituent
propositions is false. The falsehood is always at the atomic level.

**Purpose:** Debug any failure — whether in code, reasoning, or planning —
by decomposing the false claim into atomic facts and finding the root cause.

**Procedure:**

1. **State the false proposition.** What is the claim that failed? "The API
   returns user data." "The deployment pipeline succeeded." "The test suite
   passes."

2. **Decompose into atomic facts.** Apply Procedure 1 (Logical Analysis) to
   break the false proposition into its elementary constituents. List them.

3. **Check each atomic fact against ground truth.** For each elementary
   proposition, ask: "Is this true or false?" The first false atomic fact is
   the root cause.

4. **Verify the decomposition.** The error is in the first false atomic fact.
   Everything downstream of it is unreliable. Do not attempt to fix
   downstream consequences without fixing the root cause.

5. **Fix at the atomic level.** The correction must address the false atomic
   fact, not the complex proposition. If the atomic fact is "the database
   connection is open" and it is false, fixing "the API returns user data"
   without fixing the connection is futile.

6. **Verify the fix.** After correction, re-check the original complex
   proposition. Does it now picture a true state of affairs? If not, find
   the next false atomic fact.

**Key insight for chain-of-thought debugging:** In chain-of-thought reasoning,
the error is always in one of the intermediate steps. The Tractatus method
says: decompose the CoT into atomic steps, find the first false step, and
the error is in the reasoning that produced that step. Everything after the
first false step is unreliable.

---

## Putting It All Together: The Tractarian AI Agent Pipeline

These 11 procedures form a coherent pipeline for rigorous reasoning. They
are not independent — they reinforce each other:

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRACTARIAN REASONING PIPELINE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Problem / Claim / Requirement                                   │
│       │                                                          │
│       ▼                                                          │
│  1. Logical Analysis ──────────────→ identifies atomic facts     │
│       │                                                          │
│       ▼                                                          │
│  7. Logical Space ────────────────→ maps combinatorial space     │
│       │                                                          │
│       ▼                                                          │
│  2. Verification Principle ───────→ checks meaningfulness        │
│       │                                                          │
│       ▼                                                          │
│  3. Saying vs. Showing ───────────→ determines what can be known │
│  10. Nonsense Detection ──────────→ filters empty output         │
│       │                                                          │
│       ▼                                                          │
│  5. Dissolution ──────────────────→ dissolves pseudo-problems    │
│       │                                                          │
│       ▼                                                          │
│  4. The Ladder ───────────────────→ iterative ascent             │
│       │                                                          │
│       ▼                                                          │
│  6. Facts vs. Things ─────────────→ grounds in events            │
│  11. Analyze False Proposition ───→ debugging loop               │
│       │                                                          │
│       ▼                                                          │
│  8. Limits of Self + 9. Limits of Language → epistemic boundary  │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

Use the complete pipeline for deep architectural or problem analysis. Use
individual procedures for targeted interventions.

---

## The Tractarian AI Agent Architecture

The following is a design pattern for building AI agents that follow
Tractatus principles. It is not a prescription — it is a framework for
organizing agent capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                    Tractarian AI Agent                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Ontology Layer (Objects + Forms)                         │
│     - Defines atomic primitives and their type signatures     │
│     - Immutable, unanalyzable domain objects                 │
│     - The "substance" of the agent's world                   │
│                                                               │
│  2. Fact Layer (States of Affairs)                           │
│     - Grounded propositions about what is the case           │
│     - Relational: objects in determinate configurations      │
│     - Independent: each fact can be verified separately      │
│                                                               │
│  3. Picture Layer (Propositions)                             │
│     - Agent's outputs as logical pictures of facts           │
│     - Verification: output ↔ fact isomorphism check          │
│     - Nonsense detection: does the output picture            │
│       any possible state of affairs?                         │
│                                                               │
│  4. Truth-Functional Engine (Inference)                      │
│     - Each reasoning step is a truth-function of prior steps │
│     - N-operator as universal operation                      │
│     - Tautology detection (logical truths)                   │
│     - Contradiction detection (logical falsehoods)            │
│                                                               │
│  5. Silence Mechanism (Boundary)                             │
│     - Detects questions outside representational capacity    │
│     - Triggers "I cannot speak about this" response          │
│     - Prevents hallucination by enforcing the limit          │
│                                                               │
│  6. Ladder Management (Scaffolding)                          │
│     - Temporary prompt structures, few-shot examples         │
│     - Chain-of-thought templates                              │
│     - Discarded after internalization                        │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Cheat Sheet

| User presents... | Apply procedure | Key question |
|---|---|---|
| A vague requirement | 1 — Logical Analysis | "What are the atoms?" |
| An unverifiable claim | 2 — Verification Principle | "Can I specify truth conditions?" |
| A framework property | 3 — Saying vs. Showing | "Can this be said or only shown?" |
| A multi-step reasoning task | 4 — The Ladder | "What ladder am I climbing?" |
| An unsolvable dilemma | 5 — Dissolution | "Is this a real problem or a confusion?" |
| An architecture review | 6 — Facts vs. Things | "Are my events really facts?" |
| A test plan or edge case analysis | 7 — Logical Space | "What regions of state space am I covering?" |
| Agent capability question | 8 — Limits of Self | "What are my primitives?" |
| A problem outside expertise | 9 — Limits of Language | "Can this be expressed in my language?" |
| AI output review | 10 — Nonsense Detection | "Is this meaningful or grammatically empty?" |
| A bug or failure | 11 — Analyze False Proposition | "Which atomic fact is false?" |

---

## Basis in the Tractatus

All procedures in this skill are derived from specific propositions in
Wittgenstein's *Tractatus Logico-Philosophicus* (1921, standard TLP numbering):

| TLP # | Proposition | Procedure |
|-------|------------|-----------|
| 1.1 | The world is the totality of facts, not of things. | 6 — Facts vs. Things |
| 2.01 | A state of affairs is a combination of objects. | 1 — Logical Analysis |
| 2.02 | Objects are simple. | 1 — Logical Analysis |
| 2.1 | We picture facts to ourselves. | 3 — Saying vs. Showing |
| 4.003 | Most propositions... are not false but nonsensical. | 5 — Dissolution, 10 — Nonsense |
| 4.024 | To understand a proposition is to know what is the case if it is true. | 2 — Verification Principle |
| 4.1212 | What can be shown cannot be said. | 3 — Saying vs. Showing |
| 4.31 | Truth-possibilities can be represented by truth-table schemata. | 7 — Logical Space |
| 5 | A proposition is a truth-function of elementary propositions. | 1 — Logical Analysis |
| 5.6 | The limits of my language mean the limits of my world. | 8 — Limits of Self, 9 — Limits of Language |
| 6.54 | He must throw away the ladder after he has climbed up it. | 4 — The Ladder |
| 7 | What we cannot speak about we must pass over in silence. | 9 — Limits of Language |

---

## References

### Primary Sources

- Wittgenstein, L. (1921). *Tractatus Logico-Philosophicus*. Translated by
  C.K. Ogden (1922) and D.F. Pears & B.F. McGuinness (1961).

### Secondary Works

- Anscombe, G.E.M. (1959). *An Introduction to Wittgenstein's Tractatus.*
  The definitive philosophical commentary.
- Hacker, P.M.S. (1972). *Insight and Illusion: Wittgenstein on Philosophy
  and the Metaphysics of Experience.* Excellent on showing vs. saying.
- Kenny, A. (1973). *Wittgenstein.* Revised ed. 2005. The most accessible
  single-volume treatment.
- Conant, J. (1989). "Must We Show What We Cannot Say?" The definitive
  treatment of resolute vs. irresolute readings of TLP 6.54.
- Diamond, C. (1991). "Throwing Away the Ladder: How to Read the Tractatus."
  In *The Realistic Spirit.* The "resolute reading."

### Papers Connecting Wittgenstein to Computer Science / AI

- Bennedsen, J. (2004). "A Wittgenstein Approach to the Learning of
  OO-modeling." *Computer Science Education.* DOI: 10.1080/0899340042000303447.
- Arellano, D. et al. (2026). "Are language models intelligent enough for
  entrepreneurial work?" *Journal of Business Venturing.*
  DOI: 10.1016/j.jbusvent.2026.106589.
- Floyd, J. (2012). "Wittgenstein, Carnap, and Turing: Contrasting Notions
  of Analysis." In *Wittgenstein and the Philosophy of Information.*
- Trinh, T. (2024). "Logicality and the Picture Theory of Language."
  *Synthese*, 203, 142. DOI: 10.1007/s11229-024-04549-4.
- *Wittgenstein and Artificial Intelligence, Volume I: Mind and Language*
  (2024). Anthem Press. DOI: 10.2307/jj.18979316.
- *Wittgenstein and Artificial Intelligence, Volume II: Values and Ethics*
  (2024). Anthem Press. DOI: 10.2307/jj.18979314.