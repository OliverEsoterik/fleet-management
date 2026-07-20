---
name: code-review
description: >
  Systematic code review methodology based on empirical research (SmartBear,
  Google, Microsoft). Multi-pass review: structural analysis first, then
  correctness, then security/perf, then style. Catches defects by reading
  with intent, not by scanning.
skills: []
tools: Read, Write, Bash, Grep
---

# Code Review

## Overview

This is a **methodology skill** for rigorous, evidence-based code review. It
is grounded in the principal research findings on what actually works:

- **Reviews under 400 lines catch 70-90% of defects.** Above 400 lines, defect
  detection drops to 35% or below (SmartBear/Cisco study, 2006). This is the
  single most robust finding. If a diff is too large, flag it before reviewing.
- **Reviewing at <500 LOC/hour is correlated with higher defect detection.**
  Google's internal research found optimal review velocity around 200-400 LOC/hr.
- **Preparing a checklist before reviewing improves detection rates.**
  The act of defining what to look for changes how you read code.
- **Author-prepared summaries of what changed and why improve review speed
  and accuracy.** The reviewer should read the summary first, not the diff.
- **Reviewing in multiple passes (architecture → logic → style) is more
  effective than a single pass.** Each pass uses a different mental filter.
- **In-person or synchronous review finds different bugs than async review.**
  Use async (this skill) for systematic coverage; supplement with sync for
  design discussions.

**Announce at start:** "I'm using the code-review skill to audit the changes."

## Prerequisites

Before reviewing, check the diff size. If the diff exceeds 400 lines:

```
> Critical: Diff is NNN lines. Reviews over 400 lines lose 50%+ defect
> detection effectiveness. Request the author to split this into smaller,
> logically-separate changes and review individually.
```

## Review Process (Four Passes)

Each pass has a distinct purpose. Do them in order. Do not skip passes.

### Pass 1: Structural Understanding (no commenting)

Goal: understand what this change is supposed to do and how it fits into the
system. You cannot find bugs in code you don't understand.

1. **Read the description / commit message.** What is the intent?
2. **Understand the context.** What module, feature, or subsystem does this
   touch? What are the boundaries?
3. **Trace the control flow.** Don't read line-by-line yet. Read the skeleton:
   entry points, function signatures, data flow, return paths.
4. **Identify what is NOT changed.** If a feature adds an API endpoint, was
   the auth middleware already there or is it missing? This is critical.
5. **Ask yourself:** "If I had to explain this change to someone who doesn't
   know this codebase, what would I say?" If you can't answer concisely,
   you don't understand it well enough to review.

**Output:** A one-paragraph summary in your head (or in notes). Do not write
review comments yet — you don't know what the actual issues are.

### Pass 2: Logic & Correctness

Goal: verify the code does what it claims to do, and handles edge cases.

Read every line. For each logical block, ask:

- **Does this branch cover all cases?** What happens when the input is empty,
  null/None, at boundary, or in an unexpected format?
- **Is the state transition correct?** Every mutation should have an invariant.
  What invariant does this mutation preserve or break?
- **Are the error paths real?** Code that throws/catches exceptions needs
  each case to be actually reachable. Dead catch blocks are noise.
- **Is the concurrency model sound?** Shared state without locks? Async
  without await on I/O? Callback ordering assumptions?
- **Are the tests meaningful?** Do they test the actual behavior or the
  implementation? A test that passes for the wrong reason is worse than no test.
- **Does it handle the failure of its dependencies?** Network calls, disk I/O,
  external APIs — assume they will fail.

**Evidence note:** Google found that logic defects are the single most common
type found in code review (30-40%). Focus here.

**Output format for each finding:**

```markdown
### [Severity] Issue title

- **Why it's wrong:** The specific logical error or omission
- **When it breaks:** The conditions that trigger it
- **How to fix:** Actionable, specific recommendation
```

### Pass 3: Security, Performance & Robustness

Goal: find vulnerabilities and performance problems before they reach
production. This pass is intentionally separated from Pass 2 because security
review uses a different mental model (attacker mindset vs correctness mindset).

**Security:**
- **Injection surfaces:** Every user-supplied input flowing into SQL, shell
  commands, HTML/JS rendering, file paths, or deserialization.
- **Authorization:** Is every protected path actually checked? Are there paths
  that bypass the guard? Can the guard itself be tricked?
- **Secrets and credentials:** Hardcoded keys, tokens in logs, tokens in URLs,
  secrets in config files committed to the repo.
- **Error information leakage:** Stack traces or internal state exposed to
  users. Detailed error messages in API responses.
- **IDOR (Insecure Direct Object Reference):** Can user A access user B's
  data by changing an ID parameter?
- **Rate limiting / abuse:** Is there a resource (endpoint, computation, file
  write) that can be called in a loop with no cost?

**Performance:**
- **N+1 queries:** Loop over DB results making individual queries. The classic.
- **Unbounded growth:** Lists, caches, buffers, or connection pools that grow
  without limit.
- **Inefficient data structures:** O(n²) algorithms where O(n) or O(log n)
  would work. Linear scans of large lists.
- **Premature optimization:** The opposite problem — complex caching that
  doesn't need to exist, abstractions that hurt readability for no measurable
  gain.
- **Sync in async context:** Blocking calls (time.sleep, sync I/O) in async
  event loops. Thread pool exhaustion.

**Robustness:**
- **Retry logic:** Is there any? Does it have exponential backoff and jitter?
  Does it handle the non-transient error case?
- **Timeouts:** Every external call should have a timeout. Every timeout should
  be reasonable (not 30s for a 100ms API).
- **Resource cleanup:** Files closed, connections returned to pool, memory
  freed, transactions rolled back on error.
- **Graceful degradation:** When dependency X is down, does the whole system
  fail or does it serve degraded but meaningful responses?

### Pass 4: Style, Maintainability & Documentation

Goal: ensure the code is reviewable by the next person (who may be you in 6
months). This is the lowest priority pass — do first three passes completely
before commenting on style.

- **Readability:** Can you understand this function without scrolling? Are
  variable names accurate? Is the control flow straightforward?
- **Comments:** Do they explain WHY, not WHAT? (The code already says what.)
  Are there TODO/FIXME/HACK comments that need addressing?
- **Test quality:** Do tests use realistic data? Are they independent?
  Do they clean up after themselves? Is the test name descriptive?
- **Logging:** Are logs at the right level? Do they contain enough context to
  debug (request ID, relevant state)? Do they avoid leaking PII or secrets?
- **Documentation:** Does the change update relevant docs, API specs, or
  changelogs? Is the commit message descriptive enough for `git blame`?

## How to Write Review Comments

Research says comment quality matters as much as the issues themselves.
A technically correct but poorly written comment creates friction and gets
ignored. Follow these rules:

### Be specific, not editorial

| Bad | Good |
|-----|------|
| "This is confusing" | "The variable name `data` is ambiguous — it holds a parsed JSON payload but the name suggests raw bytes" |
| "This has a bug" | "If `user.status` is `null`, line 42 throws a NullPointerException because `map.get()` returns null" |
| "This should use a better pattern" | "This chain of if/elif could be replaced with a dispatch dict at line 30-45, which would let new cases be added without modifying this function" |

### Separate issue from person

- Always use "this code" not "you did". E.g., "This approach has a race
  condition" not "You introduced a race condition."
- Frame in terms of the code's behavior, not the author's intent.
- When something is good, say so. "The test coverage on the retry logic is
  thorough" takes 2 seconds and reinforces good habits.

### Categorize by severity

| Label | Meaning | Action |
|-------|---------|--------|
| **Critical** | Bug, vulnerability, or data-loss risk that WILL manifest in production | Must fix before merge |
| **High** | Significant concern — logic error under common conditions, performance regression, missing auth | Should fix before merge |
| **Medium** | Improvable — readability, edge case that is unlikely but possible, non-critical performance | Consider fixing |
| **Low** | Nit — naming, comment, formatting preference | Author can resolve or dismiss |
| **Praise** | Genuinely well-done section | No action needed |

### Explain the "why" behind the recommendation

"I suggest moving this validation to a separate function because it is reused
in three places — if a fourth caller forgets to validate, that's a bypass."
This is more persuasive and educational than "extract this to a function."

### When you're not sure, say so

"This might be safe because X, but I'm not sure. Can you confirm that Y
handles the Z case?" Honest uncertainty is more valuable than a confident
but wrong review.

## Common Review Pitfalls (Avoid These)

| Pitfall | Why It Hurts |
|---------|-------------|
| **Reviewing too fast (<5 min for a 200-line diff)** | Misses logic and security issues entirely. You're just rubber-stamping. |
| **Reviewing too slow (>1 week turnaround)** | Kills momentum. Authors context-switch away, the change becomes stale, merge conflicts multiply. |
| **Nitpicking style in the first pass** | Wastes reviewer and author time on formatting issues while real bugs go unfound. Style is the last pass for a reason. |
| **Reviewing in one pass** | Your brain can't simultaneously check for logic errors, security holes, and naming conventions. Multi-pass is evidence-based. |
| **Reviewing code you don't understand** | If you can't trace the control flow, don't guess — ask the author for a walkthrough or defer to someone who knows this area. |
| **Rubber-stamping small diffs** | Small diffs are where critical bugs hide ("it's just a one-line change"). They deserve as much attention as large ones. |
| **Asking for changes you can't justify** | Every comment should have a rationale. If you can't explain why, don't ask. |
| **Style wars** | Enforcing personal preferences that aren't in the style guide. The code's existing style wins. |
| **Only finding style nits** | If your review has 10 comments and all 10 are naming/formatting, you didn't review — you formatted. |

## Output Format

Write findings to `work/graph/output/code-review/findings.md`. Structure:

```markdown
# Code Review Findings

**Review scope:** <files changed, lines added/removed>
**Diff size:** <NNN lines>
**Review passes completed:** 1-4 (list which)
**Overall assessment:** <one-sentence judgment>

## Summary

<2-3 sentence summary of the most important findings>

---

### [Critical] Issue title

- **File:** `path/to/file.py:42`
- **Why it's wrong:** Explanation of the error
- **When it triggers:** Conditions that cause the problem
- **Recommendation:** How to fix it

### [High] Issue title

...
```

If no issues are found after all four passes, state that clearly with a note
about what was checked:

```markdown
# Code Review Findings

**No issues found.** All four review passes completed:
1. Structural understanding — change scope understood
2. Logic & correctness — all branches and edge cases handled
3. Security, performance & robustness — no vulnerabilities or performance regressions
4. Style & maintainability — code is clear and well-documented
```

## Verification

Before reporting "done", confirm:
1. Were all four review passes completed in order?
2. Is each finding categorized by severity?
3. Does each high/critical finding include a specific, actionable recommendation?
4. Is the output written to the correct path?
5. If the diff was over 400 lines, was it flagged?

Do not skip Pass 1 and 2 to get to Pass 3 faster. The order matters.
