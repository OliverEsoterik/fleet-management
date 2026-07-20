---
name: code-review
description: >
  Rigorous code review focusing on security, performance, maintainability,
  and architectural integrity. Acts as a cynical devil's advocate to
  identify hidden flaws before they reach production.
---

# Code Review

## Overview

This is a **methodology skill** providing a systematic framework for reviewing code changes. It challenges assumptions and finds potential failures before they reach production.

**Full methodology:** `/home/oliver/.pi/agent/skills/code-review/SKILL.md`

**Announce at start:** "I'm using the code-review skill to audit the changes."

## Review Framework

When activated, follow this structured framework:

### 1. The Devil's Advocate Audit

Actively seek reasons why this code will fail in production. Challenge every assumption. Ask "what happens when this input is empty/malicious/massive?"

### 2. Security-First Analysis

Check for:
- Injection vulnerabilities (SQL, XSS, Command injection, path traversal)
- Insecure dependencies and known CVEs
- Data leaks (secrets in logs, exposed PII, excessive error detail)
- Weak authentication/authorization (missing checks, privilege escalation)
- Insecure deserialization, SSRF, IDOR

### 3. Performance Analysis

Check for:
- N+1 query problems and unnecessary database round trips
- Inefficient algorithms (O(n²) where O(n) would do)
- Excessive memory allocation, large objects in hot paths
- Blocking synchronous operations in async contexts
- Missing caching, repeated expensive computations

### 4. Maintainability & Quality

Check for:
- Readability: meaningful names, consistent patterns, appropriate comments
- Error handling: every failure path accounted for, not just the happy path
- Logging: sufficient context to debug failures in production
- Test coverage: meaningful tests that test behavior, not implementation
- Documentation: API contracts, configuration, migration notes

## Output Format

Write findings to `work/graph/output/code-review/findings.md`. For each issue:

```markdown
### [Severity: Critical/High/Medium/Low] Issue title

- **File:** `path/to/file.py:42`
- **Description:** What's wrong and why it matters
- **Impact:** Who/what this affects under what conditions
- **Recommendation:** How to fix it
```

If no issues found, state that clearly in the summary.