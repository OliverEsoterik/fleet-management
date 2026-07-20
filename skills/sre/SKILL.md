---
name: sre
description: >
  Site Reliability Engineering / Security Audit. Systematic audit of the
  codebase for bugs, security vulnerabilities, performance issues, and
  architectural anti-patterns. Opens findings with severity ratings and
  actionable remediation.
---

# SRE — Security & Reliability Audit

## Overview

This is a **methodology skill** for systematic codebase auditing. It combines security review, reliability engineering, performance analysis, and architectural anti-pattern detection into a structured audit pipeline.

**Full methodology:** `/home/oliver/.pi/agent/skills/sre/SKILL.md`

**Announce at start:** "I'm using the sre skill to audit the codebase."

## Audit Pipeline

Run all phases in order. Each phase produces findings that feed into the next.

### Phase 1: Security Audit

Use the `code-review` skill as the primary security methodology. Cover:

- **Secret exposure:** API keys, tokens, passwords, certificates in code or config
- **Authentication:** Weak password policies, missing MFA, session fixation, JWT weaknesses
- **Authorization:** Missing access controls, privilege escalation paths, IDOR
- **Injection:** SQL, NoSQL, OS command, LDAP, XSS, CSRF, SSRF
- **Data protection:** Missing encryption, weak cipher choices, improper PII handling
- **Dependencies:** Known vulnerable packages, outdated libraries with CVEs

### Phase 2: Reliability Audit

- **Error handling:** Uncaught exceptions, silent failures, swallowed errors
- **Resilience:** Missing retries, no circuit breakers, single points of failure
- **State management:** Race conditions, inconsistent state, missing transactions
- **Timeouts:** Missing or absurdly long timeouts on external calls
- **Resource leaks:** Unclosed connections, file handles, goroutines, streams

### Phase 3: Performance Audit

- **Hot paths:** Inefficient loops, unnecessary allocations in critical paths
- **Database:** Missing indexes, N+1 queries, unbounded queries
- **Caching:** Missing cache where appropriate, stale cache invalidation
- **Concurrency:** Deadlocks, starvation, excessive lock contention
- **Memory:** Large allocations, leaks, unbounded growth

### Phase 4: Architecture Anti-patterns

- **God objects:** Classes/modules doing too much
- **Spaghetti:** Circular dependencies, unclear data flow
- **Shotgun surgery:** One change requiring edits across N files
- **Golden hammer:** Overused pattern applied where it doesn't fit
- **Leaky abstractions:** Internal details exposed through public API

## Output Format

Write findings to `work/graph/output/sre/findings.md`. For each finding:

```markdown
## [Severity: Critical/High/Medium/Low] [Category: Security|Reliability|Performance|Architecture]

**File:** `path/to/file.py:42`

**Description:**
What's wrong and why it matters.

**Impact:**
Who/what this affects under what conditions.

**Recommendation:**
How to fix it. Be specific — include code examples.

**References:**
[CWE entry, OWASP link, relevant docs]
```

## Self-Check

Before finalizing, verify:
- [ ] Every finding has a severity rating
- [ ] Every finding has a specific file + line reference
- [ ] Critical/High findings include a concrete fix recommendation
- [ ] No fabricated findings — if nothing found, say so clearly