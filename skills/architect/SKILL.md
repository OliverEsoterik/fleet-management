---
name: architect
description: Architect / Implementation Lead mode. Use when implementing features, fixing bugs, or working through GitHub issues methodically.
---

# Architect Loop

> **Mode:** Architect / Implementation Lead  
> **Purpose:** Implement features, fix bugs, and improve the codebase by working through GitHub issues methodically.  
> **Trigger:** The user asks you to work on a specific issue, or asks for a feature/bug fix that corresponds to an open GitHub issue.  

** After any non-trivial failure, write lesson learned into this skill itself **
** When using this skill always use PI Subagents and spin up the "architect" agent **

---

## 0. Required Skills

Load these PI skills before starting this loop. If a skill is not available, abort and ask the user to从前 install it.

| Skill | Source | Used For |
|-------|--------|----------|
| `code-review` | `skills/code-review/SKILL.md` | Security, performance, and correctness review |
| `writing-plans` | `skills/writing-plans/SKILL.md` | Creating implementation plans before coding |
| `docker-expert` | `skills/docker-expert/SKILL.md` | Dockerfile/container review (if applicable) |
| GitHub CLI | System tool | Issue/PR management |
| `git` | System tool | Branching, commits |

---

## 1. Discovery Phase

### Step 1.1: Synchronize with GitHub Issues

Run the following and capture the output:
```bash
gh issue list --state open --limit 100 --json number,title,labels,createdAt,body
```

**Decision:** If the issue list is empty, inform the user and exit the loop.

### Step 1.2: Select the Target Issue

**Rule:** Always pick the oldest open找出来 open issue first (lowest number that is still open), unless the user explicitly names an issue by number or title.

If the user named an issue, find it. If multiple issues match, ask for clarification with a numbered list.

### Step 1.3: Read the Issue in Full

Run:
```bash
gh issue view <number>
```

**Checklist before proceeding:**
- [ ] I have read the full issue body, including any linked files or references
- [ ] I understand the acceptance criteria (if any)
- [ ] I have noted any linked PRs or duplicate issues

---

## 2. Assessment Phase

### Step 2.1: Read the Referenced Plan

If the issue references a plan file (e.g., `docs/plans/2026-06-30-separate-ratings-read-write.md`), read it completely.

**Checklist:**
- [ ] Read the plan file referenced in the issue
- [ ] Note any plan-level assumptions or constraints
- [ ] Identify which files the plan says to modify

### Step 2.2: Verify the Issue is Not Already Resolved

Before writing any code, verify the issue has not already been resolved:

1. **Read the files** the plan says to modify
2. **Search the codebase** for the issue keywords
3. **Check git log** for recent commits related to the issue number:
   ```bash
   git log --all --grep="#<issue_number>" --oneline
   ```
 persistent 4. **Run the CI tests** to see if the current state already passes the expected acceptance criteria

**Decision gate:**
- **If the issue is fully resolved:** Comment on the issue explaining why, then close it. Exit the loop.
- **If the issue is partially resolved:** Comment with what is already done and what remains, then proceed with the remaining work.
- **If the issue is NOT resolved:** Proceed to Step 3.

---

## 3. Planning Phase

### Step 3.1: Challenge the Proposed Solution

Before implementing, critically evaluate the plan:

- Does the plan account for edge cases not mentioned?
- Are there simpler approaches the plan author missed?
- Will the plan break any existing functionality?
- Is the plan still correct given the current codebase state?

**If you disagree with the plan, document your concerns in the issue comment before proceeding.**

### Step 3.2: Load Relevant Code

Read ALL files that the plan says to modify, and ALL files that call the files you will modify:

**File reading checklist:**
- [ ] Read each target file completely
- [ ] Read any files imported by target files
- [ ] Read test files for the target area (if they exist)
- [ ] Read `AGENTS.md` and `README.md` for project conventions

### Step 3.3: Create an Implementation Plan

Write a numbered implementation plan with a verification check for each step. Match existing code patterns exactly.

**The plan must include:**
1. Files to modify (with specific line ranges if possible)
2. Files to create (if any)
3. A rollback strategy if things go wrong
4. Test strategy (what tests need to pass)
5. Expected behavior after the change

---

## 4. Implementation Phase

### Step 4.1: Create a Feature Branch

```bash
git checkout -b feature/issue-<number>-<short-description>
```

### Step 4.2: Implement the Change

Follow the plan step by step. **Rules:**
- Touch only what you must (no drive-by refactors)
- Match existing code style exactly
- Add no speculative features
- Write the minimum code that solves the stated problem

### Step 4.3: Verify with Local Tests

Before committing:
- [ ] Run the project's test suite (e.g., `make test`, `pytest`, etc.)
- [ ] If there is a type checker, run it
- [ ] If there is a linter, run it
- [ ] Run any script-specific verification the plan mentions

**If tests fail, fix the root cause. Do not suppress the failure.**

---

## 5. Review Phase

### Step 5.1: Self-Review

Before creating the PR, review your own change as if you were a reviewer:

- [ ] Every changed line traces back to the issue
- [ ] No orphaned imports, variables, or functions
- [ ] Error handling covers realistic failure modes only
- [ ] No sensitive data (keys, passwords) committed

### Step 5.2: Commit

Write a descriptive commit message:
```
subject under 72 chars

body explaining WHY the change was made, not just WHAT

References #<issue_number>
```

---

## 6. Delivery Phase

### Step 6.1: Open a Pull Request

```bash
git push origin feature/issue-<number>-<short-description>
gh pr create --title "..." --body "..." --base main
```

The PR body must:
- Reference the issue number (`Closes #<number>`)
- Summarize the change in 1-2 sentences
- List any testing performed

### Step 6.2: Update the Issue

Add a comment to the issue with:
- Link to the PR
- Summary of what was implemented
- Any caveats or follow-up work

---

## 7. Termination Conditions

This loop terminates when any of the following are true:

1. The selected issue is resolved (PR merged or closed)
2. The issue was already resolved (closed in Phase 2)
3. The user explicitly asks to stop or change tasks
4. A blocking dependency is discovered (another issue must be resolved first)

---

## 8. Error Handling

| Condition | Action |
|-----------|--------|
| Tests fail after change | Revert to last known good state, debug root cause, retry |
| Plan conflicts with code reality | Document conflict in issue, ask user for guidance |
| User wants a different approach | Document the pivot in the issue, adjust plan, continue |
| Rate limit hit (API calls) | Pause, report to user, suggest retry later |
