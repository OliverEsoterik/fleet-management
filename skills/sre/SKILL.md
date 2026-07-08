---
name: sre
description: Site Reliability Engineer / Security Review mode. Use for auditing the codebase for bugs, security vulnerabilities, performance issues, and architectural anti-patterns.
---

# SRE Loop (Security & Reliability Audit)

> **Mode:** Site Reliability Engineer / Security Review  
> **Purpose:** Systematically audit the codebase for bugs, security vulnerabilities, performance issues, and architectural anti-patterns. Open GitHub Issues for findings with severity ratings and actionable remediation steps.  
> **Trigger:** The user asks for a code review, audit, security check, or says "find issues in this codebase." Also runs automatically after any significant refactor or before any release.  

---

## 0. Required Skills

Load these PI skills before starting this loop. If a skill is not available, abort and ask the user to install it.

| Skill | Source | Used For |
|-------|--------|----------|
| `code-review` | `skills/code-review/SKILL.md` | Rigorous security, performance, correctness review |
| `docker-expert` | `skills/docker-expert/SKILL.md` | Dockerfile/container image review (if applicable) |
| `writing-plans` | `skills/writing-plans/SKILL.md` | Documenting findings into actionable plans |
| `osv-scanner` | System tool (if available) | Known vulnerability scanning |
| GitHub CLI | System tool | Creating issues, labeling, linking |
| `git` | System tool | Checking history, blame, diffs |

---

## 1. Discovery Phase

### Step 1.1: Understand the Audit Scope

Determine WHAT to audit based on user intent:

| User Says | Audit Scope |
|-----------|------------|
| "Audit the codebase" | Everything: all scripts, configs, SQL, orchestration |
| "Review PR #N" | Only the diff in that PR, plus affected files |
| "Security check" | Security-relevant code only (SQL, auth, secrets, data handling) |
| "Performance review" | Hot paths, DB queries, API calls, memory usage |
| "Review this file" | Only the specified file(s) |

**If ambiguous, default to full codebase audit and state this assumption to the user.**

### Step 1.2: Gather Context

Load critical project files to understand the system:

1. Read `AGENTS.md` or `CLAUDE.md` (project conventions)
2. Read `README.md` (architecture, stack)
3. Read `Makefile` (build/test commands)
4. Read any config files (package.json, requirements.txt, etc.)
5. Read the CI/CD configuration (GitHub/.github/workflows, CI scripts)

**Decision gate:** If the project has no `AGENTS.md` or equivalent, note this as a finding itself.

---

## 2. Static Analysis Phase

### Step 2.1: File Inventory & Hot Path Identification

List all source files in order of criticality:

```bash
# Find all source files
find . -type f \( -name "*.py" -o -name "*.sh" -o -name "*.sql" -o -name "*.yaml" -o -name "*.yml" \) | grep -v __pycache__ | sort
```

**Prioritize in this order:**
1. Files that handle external data (API calls, file I/O, DB queries)
2. Files that contain secrets or authentication
3. Files in the critical data path (the pipeline's main flow)
4. Everything else

### Step 2.2: Code Pattern Scan

For each file in priority order, scan for these anti-patterns:

**Security:**
- Injection risks (SQL, command, XSS)
- Hardcoded secrets or credentials
- Unsafe deserialization / eval
- Missing input validation
- Overly broad error handling (`except Exception: pass`)
- Missing authentication/authorization

**Performance:**
- N+1 query problems
- Memory hot growth in loops
- Blocking operations in what should be async contexts
- Unnecessary repeated calculations
- Missing pagination on large datasets
- Large batch operations without chunking

**Reliability:**
- No retry/backoff on external API calls
- No timeout on network operations
- Missing transaction management
- No graceful degradation on failure
- Race conditions in concurrent code

**Maintainability:**
- Dead code or unused imports
- Magic numbers without constants
- Duplicated logic across files
- Missing error handling
- Poor logging (print instead of structured logging)

### Step 2.3: Dependency & Config Audit

Check for known vulnerabilities and misconfigurations:

- Check `requirements.txt`, `package.json`, `Pipfile`, etc. for outdated or vulnerable dependencies
- Check Dockerfile(s) for base image vulnerabilities
- Check environment variable usage (no secrets in code)
- Check permission settings on scripts (should not be 777)
- Check for missing `.gitignore` entries (env files, secrets)

---

## 3. Dynamic Analysis Phase (When Applicable)

### Step 3.1: Run Existing Tests

```bash
# Run the test suite
make test 2>/dev/null || pytest 2>/dev/null || python -m unittest discover 2>/dev/null
```

**Check for:**
- Test failures (even minor ones)
- Test coverage gaps (no tests for critical logic)
- Slow tests that indicate performance problems

### Step 3.2: Lint & Type Check

If available, run linters and type checkers:
```bash
ruff check . 2>/dev/null || flake8 . 2>/dev/null
mypy . 2>/dev/null || pyright . 2>/dev/null
```

### Step 3.3: Run Static Security Scanners (If Available)

```bash
# Python security scanner
bandit -r src/ 2>/dev/null || true

# Dependency vulnerability scanner
pip-audit 2>/dev/null || true

# Known vulnerability database
osv-scanner --json . 2>/dev/null || true
```

---

## 4. Consolidation Phase

### Step 4.1: Classify Findings

For each finding, assign:

**Severity:**
| Level | Definition | Response Time |
|-------|------------|--------------|
| CRITICAL | Data loss, security breach, system crash | Immediate fix |
| HIGH | Major bug, performance degradation, security leak | Fix same day |
| MEDIUM | Code smell, missing error handling, minor performance | Fix within sprint |
| LOW | Style issue, dead code, non-ideal pattern | Fix opportunistically |

**Category:**
- `security` — Vulnerability or data exposure risk
- `performance` — Slow or resource-intensive code
- `reliability` — Error handling, resilience, or correctness issues
- `maintainability` — Code quality, duplication, dead code
- `architecture` — Design or structural concerns

### Step 4.2: De-duplicate Findings

Group related findings:
- Multiple instances of the same anti-pattern → one issue
- Root cause analysis: Do multiple symptoms trace to one bug?
- Check existing issues to avoid duplicates:
  ```bash
  gh issue list --state all --search "<keyword>" --limit 10
  ```

---

## 5. Reporting Phase

### Step 5.1: Open GitHub Issues

For each unique finding, create a GitHub issue with this format:

```
Title: [<SEVERITY>] <Brief description>

## Problem
<What is wrong and why it matters>

## Affected Code
<File path, function name, line number if available>

## Impact
<What could happen if not fixed>

## Fix
<Concrete steps to fix>

## Verification
<How to verify the fix works>
```

**Label the issue:** Use the severity as label (e.g., `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) plus the category (e.g., `security`, `performance`).

### Step 5.2: Create a Summary Report

Summarize all findings for the user:

```
## SRE Audit Summary

- **CRITICAL:** X issues
- **HIGH:** X issues
- **MEDIUM:** X issues
- **LOW:** X issues

### Immediate Actions Required
< List critical/high items with issue links >

### Recommendations
< Any broad architectural or process improvements >
```

---

## 6. Escalation & Follow-Up

### Escalation Rules

| Condition | Action |
|-----------|--------|
| CRITICAL finding | Immediately notify user, recommend emergency fix |
| Security vulnerability | Mark as `security`, suggest immediate patch |
| Performance regression | Create benchmark, compare before/after |
| User disagrees with severity | Document reasoning in issue, let user adjust label |

### Follow-Up Actions

After initial audit, schedule follow-up:
1. **After first fix:** Re-audit the fixed area to confirm the fix is correct
2. **Weekly:** Quick scan for new issues introduced by recent PRs
3. **Before release:** Full re-audit on the release branch

---

## 7. Termination Conditions

This loop terminates when:

1. All findings are documented as GitHub issues (or marked as false positives)
2. The user explicitly asks to stop
3. No new findings are discovered after a full pass (rare, but possible on a very clean codebase)
4. Critical findings are escalated to the Architect loop for immediate fix

---

## 8. Error Handling

| Condition | Action |
|-----------|--------|
| Scanner tool not installed | Skip that scan, note it in findings, suggest installing it |
| No test suite exists | Note as a HIGH finding: "No test suite detected" |
| No CI/CD configured | Note as a MEDIUM finding: "No continuous integration detected" |
| Rate limit hit (API) | Pause, report to user, suggest retry |
| Inconsistent findings | Re-run the scan, verify with manual code review |
