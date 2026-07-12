# AGENTS.md — fleet-management

## Why this file exists

This repository does not contain code. It contains orchestration: agent definitions, skill files, and delegation plans that tell an AI which other AIs to invoke, what to tell them, and where to put their outputs. The repository is metawork — work about work.

That is not inherently wrong. Orchestration systems are real infrastructure. But they inherit every failure mode of the systems they coordinate, plus new ones specific to delegation itself. This file documents the rules for operating here without falling into those traps.

## Core constraints

### 1. Every skill must justify its existence by the work it eliminates, not the work it describes

A skill file that took 2 hours to write and saves 5 minutes per invocation may still be worth it — if it is invoked 100 times. A skill file invoked once is a liability: it must be maintained, understood, and kept current with every change to its dependencies.

The question is not "does this skill document something useful?" The question is "does this skill eliminate more work than it creates?" If the answer is no, delete the skill file.

**Test:** For every file in `skills/`, run: "If I deleted this file and had to reconstruct its value from scratch, would I bother?" If the answer is no, delete it now.

### 2. Delegation depth is fragility

Every phase in a delegation plan adds a failure mode:
- The subagent fails to interpret its prompt correctly.
- The subagent fails to produce output in the expected format.
- The orchestrator fails to read or merge the output correctly.
- The phase ordering introduces a sequential dependency that a parallel agent could break.
- A subagent makes an edit that violates an assumption another subagent depends on.

A 3-phase delegation with 4 agents has at least 4 independent failure points plus 3 dependency edges. That is 7 things that can go wrong for every task. Each additional phase multiplies, not adds, the failure surface.

**Limit delegation to 2 phases, 3 agents maximum.** If the workflow needs more than that, the skill is trying to do too much. Split it.

### 3. The consensus problem without shared state

The WORKFLOW.md model has a primary agent consulting experts, who write markdown files, which the primary reads and incorporates. This is asynchronous communication over a filesystem bus.

Every file-based handoff creates a version problem: the primary might read a report while the expert is still writing it. The expert might write a stale report that the primary has already moved past. The escalation mechanism (3 rounds, then escalation.md) handles the failure but does not prevent the wasted work.

**Every handoff file must have a status marker.** First line of every report is one of:
- `STATUS: DRAFT`
- `STATUS: FINAL`
- `STATUS: ESCALATED`

The reader does not read past a DRAFT. The writer appends, never overwrites — append-only files prevent the read-during-write race.

### 4. No skill without a deletion date

Skills are not infrastructure. They are experimental probes — they exist to test whether an orchestration pattern works for a specific class of problem. If they work, they become habits. If they do not, they should be removed before they accumulate maintenance debt.

Every skill file gets an `expires:` field in its frontmatter, set to 90 days from creation. When it expires, either:
- The skill was used at least 3 times and is promoted to permanent (remove the expiry).
- The skill was not used and is deleted.

No exceptions. Expired skills with zero use are noise that degrades the orchestrator's discovery phase on every invocation.

### 5. The orchestrator skill is the most fragile component in the system

The orchestrator does not execute work. It reads SKILL.md files, matches requests, and delegates. Its correctness depends on:
- All skill files being parseable and well-formed.
- All skill names being discriminative enough to avoid false matches.
- All delegation plans following a consistent phase/agent/role format.
- All subagents being available and correctly configured.

If any of these fails, the orchestrator either silently falls back to generic decomposition (producing unpredictable results) or fails entirely.

**The orchestrator must validate its own inputs.** On every invocation, before announcing a plan, the orchestrator should:
1. Parse every delegation skill it plans to use and verify the phase/agent/role structure is consistent.
2. Reject any skill file that is malformed and fall back to generic decomposition with a warning.
3. Log mismatches between skill names and user requests so naming collisions can be corrected.

### 6. No parallel execution without isolation

When two subagents run in parallel and either one modifies files, they race. The filesystem is not transactional. Agent A writes a change to file X, Agent B reads file X before A's write is complete, Agent B's output is based on stale state, and the orchestrator merges two inconsistent versions.

The `review-my-work` skill launches security-auditor, test-auditor, and devops-auditor in parallel. They write reports — they do not modify files. This is safe. The `fix-my-work` skill launches a debugger and then a coder sequentially. This is also safe.

**Any parallel phase where subagents modify the same file is a bug.** If parallel modification is necessary, each subagent must write to a separate branch or worktree and the orchestrator must merge explicitly. Do not rely on luck.

### 7. The .gitignore hides the actual work

The `.gitignore` excludes `agents/`, `skills/`, and `docs/` from version control. The README and these metadata files are committed. This means:
- The actual definition of every agent and skill is not versioned.
- There is no history of when a skill was modified or why.
- There is no rollback path — if a skill file is corrupted, it must be reconstructed from memory or local backup.

The rationale (these are agent instructions, not production code) is defensible. But the consequence is that the repository's .git directory contains metadata about work-in-progress artifacts that are themselves not tracked. The `.gitignore` is hiding the system's state from its own history.

**Decision:** This is a tradeoff, not a bug. But the tradeoff must be explicit: if agent files are not tracked, their canonical source must be the filesystem. If the filesystem is lost, the system is unrecoverable. Accept that risk or track the files.

## When to add, when to delete

Add a skill when:
- You have observed a pattern of work that repeats at least 3 times.
- The delegation produces more reliable output than ad-hoc prompting.
- The skill's instructions are stable enough that they will not change significantly for 90 days.

Delete a skill when:
- It has been used fewer than 3 times in 90 days.
- Its delegation plan has more than 2 phases or 3 agents.
- A simpler skill (or no skill) produces equivalent results.
- You find yourself maintaining the skill more than using it.

The default answer to "should I add a skill?" is no. The bar for addition is higher than the bar for deletion because deletion is reversible (the skill is in git history) and addition is not (every addition creates a maintenance obligation that persists until someone explicitly removes it).

## The shape of the system

The repository's response to stress is concave, not convex. Under light load (single user, well-defined tasks), it works well — the orchestrator matches, delegates, consolidates. Under stress (ambiguous requests, missing skills, malformed delegation plans, subagent failures), it degrades unpredictably: fallback to generic decomposition, silent error handling, and user-surfaced conflicts.

This is the definition of fragility: a system that works when nothing goes wrong and breaks when it does. The antidote is not to add more delegation phases or more error handling. The antidote is to reduce the number of things that can go wrong — which means fewer skills, simpler delegation, and shorter chains.

The system's best future is not a larger orchestrator. It is a smaller one.
