# SRE Audit Summary: agent-helpers

**Auditor:** security-auditor  
**Date:** 2026-07-10  
**Scope:** Full codebase — all agents, skills, configs, orchestration scripts, and git history  
**Project:** Multi-agent orchestration framework using tmux-based hub-and-spoke architecture (3 agents, 3 skills)

---

## Executive Summary

| Severity | Count | Description |
|----------|-------|-------------|
| **CRITICAL** | 3 | Command injection via unsanitized variables, `rm -rf` on shared state, secrets leaked in git history |
| **HIGH** | 4 | Race conditions on lock file, no input validation on agent names/todo files, polling loop can miss events, no error handling on tmux failures |
| **MEDIUM** | 5 | No `.gitignore`, no test suite, no CI/CD, `sleep 30` is fragile timing, missing structured logging |
| **LOW** | 5 | Dead directories, doc typo, concurrent write risk, irrelevant scanning steps, template placeholders |

---

## CRITICAL Findings

### C1: Command Injection via Unsanitized Variables in tmux Commands

**File:** `INSTRUCTIONS.md`, lines 19-22 and 58-65  
**Category:** `security`  
**Severity:** CRITICAL

**Problem:** The orchestration loop constructs shell commands using unsanitized variable expansion:

```bash
tmux new-session -d -s "$session" -n agent \
  'cd agents/<agent-name> && cat brain.md ../../agents/shared/WORKFLOW.md | pi -p "$(cat) <task description>"; echo "--- PRIMARY DONE ---"; sleep 3600'
```

And more critically in the consultant dispatcher (line 64):

```bash
tmux new-session -d -s "$session" -n agent \
  "cd agents/$agent && cat brain.md ../../agents/shared/WORKFLOW.md | pi -p \"\$(cat) Read work/todo/$agent.md..."
```

**Impact:** If an attacker-controlled filename or agent name contains shell metacharacters (`;`, `$(...)`, backticks), arbitrary code execution is possible. The `$agent` variable is derived from `basename "$todo" .md` — if a malicious file is placed in `work/todo/`, this leads to RCE.

**Fix:** Use parameterized or escaped shell variables. Validate `$agent` against a known list. Use `printf '%q'` for shell escaping.

---

### C2: `rm -rf` on work/ Directory Destroys Shared State

**File:** `INSTRUCTIONS.md`, line 96  
**Category:** `reliability`, `security`  
**Severity:** CRITICAL

**Problem:** The cleanup command `rm -rf work/todo work/response work/done work/escalation.md 2>/dev/null` can run while agents are still writing to these files, destroying shared state mid-write.

**Impact:** Race condition silently breaks the orchestration pipeline. Agents hang indefinitely waiting for responses from deleted todo files.

**Fix:** Use atomic rename patterns (write to temp, then `mv`). Check for active agents before cleanup.

---

### C3: `.pi-loop.json.lock` Committed to Git History

**File:** `.pi-loop.json.lock` (committed in commit `bbbc92f`)  
**Category:** `security`  
**Severity:** CRITICAL

**Problem:** The lock file `{"pid":271222,"acquiredAt":1783678417688}` was committed to git. While not directly sensitive, this establishes a pattern of committing runtime/state files.

**Impact:** Dangerous precedent. Future lock/state files with tokens or credentials could be committed.

**Fix:** Add `.pi-loop.json.lock` to `.gitignore`. Consider removing from history.

---

## HIGH Findings

### H1: Race Condition on `.pi-loop.json.lock` Between Orchestrator Instances

**File:** `.pi-loop.json.lock` (behavioral)  
**Category:** `reliability`  
**Severity:** HIGH

**Problem:** Simple PID+timer lock with no kernel-level exclusion. Two concurrent orchestrator instances can overwrite the lock and corrupt shared work directories.

**Fix:** Use `flock` (Linux file locking). Document single-instance requirement.

---

### H2: No Input Validation on Agent Names or Todo Files

**File:** `INSTRUCTIONS.md`, line 58  
**Category:** `security`, `reliability`  
**Severity:** HIGH

**Problem:** `agent=$(basename "$todo" .md)` — no validation that `$agent` matches a known agent directory. Path traversal (`../`) or random filenames cause silent failures.

**Fix:** Validate against known agent list. Reject names containing `..`, `/`, or shell metacharacters.

---

### H3: Fixed `sleep 30` Kills Consultants Prematurely

**File:** `INSTRUCTIONS.md`, line 67  
**Category:** `reliability`, `performance`  
**Severity:** HIGH

**Problem:** The orchestrator assumes all consultants finish within 30 seconds. Complex analysis or API rate limits cause mid-work termination.

**Fix:** Replace fixed sleep with active polling (check for completion indicators or response file existence). Use exponential backoff.

---

### H4: No Error Handling on tmux Operations

**File:** `INSTRUCTIONS.md`, lines 20-22 and 60-65  
**Category:** `reliability`  
**Severity:** HIGH

**Problem:** `tmux new-session`, `capture-pane`, and `kill-session` have no error checking. Silent failure if tmux is unavailable.

**Fix:** Check `command -v tmux`. Check exit codes. Log failures.

---

## MEDIUM Findings

### M1: No `.gitignore` File

**Category:** `maintainability`  
**Severity:** MEDIUM

**Problem:** No `.gitignore` exists. Runtime state and build artifacts will be committed.

**Fix:** Create `.gitignore` with entries for `.pi-loop.json.lock`, `work/`, `.env`, `*.pyc`, `__pycache__/`.

---

### M2: No Test Suite

**Category:** `reliability`, `maintainability`  
**Severity:** MEDIUM

**Problem:** No tests exist. Shell orchestration logic cannot be validated programmatically.

**Fix:** Add shell-based tests for command construction, agent validation, and polling behavior.

---

### M3: No CI/CD Configuration

**Category:** `maintainability`, `architecture`  
**Severity:** MEDIUM

**Problem:** No `.github/workflows/` or automated validation pipeline.

**Fix:** Add GitHub Actions workflow for linting and basic sanity checks.

---

### M4: Missing Structured Logging

**File:** `INSTRUCTIONS.md`, `WORKFLOW.md`  
**Category:** `maintainability`, `reliability`  
**Severity:** MEDIUM

**Problem:** Bare `echo` with no timestamps, log levels, or persistent log file. All diagnostic output lost when sessions are killed.

**Fix:** Add timestamped logging convention. Tee to a log file.

---

### M5: Polling Loop Exhaustion During Long Consultations

**File:** `INSTRUCTIONS.md`, lines 28-75  
**Category:** `reliability`, `architecture`  
**Severity:** MEDIUM

**Problem:** `max_depth=5` combines work and idle counters. Loop can exhaust in <3 minutes, but complex audits take hours.

**Fix:** Separate idle timeout from work counter.

---

## LOW Findings

### L1: Empty `tools/` and `work/` Directories

**Category:** `maintainability`  
**Severity:** LOW

Scaffolding directories with no content. Can confuse users.

### L2: Typo in `skills/sre/SKILL.md`

**Category:** `maintainability`  
**Severity:** LOW

Contains Chinese character artifact "从前" where English text should be.

### L3: Concurrent Agent Writes Could Corrupt Response Files

**Category:** `architecture`  
**Severity:** LOW

`work/response/` directory allows simultaneous writes without atomicity guarantees.

### L4: Irrelevant Dependency Scanning Steps in Skills

**Category:** `maintainability`  
**Severity:** LOW

SRE skill references checking `package.json`, `requirements.txt` — none exist in this markdown-only project.

### L5: Hardcoded Template Placeholders in Delegation Template

**File:** `INSTRUCTIONS.md`, lines 19-22  
**Category:** `maintainability`  
**Severity:** LOW

Uses `<agent-name>` and `<task description>` literals instead of shell variables.

---

## Recommendations

### Immediate (CRITICAL/HIGH)

1. **Fix command injection vectors** in `INSTRUCTIONS.md` — validate agent names, escape shell variables
2. **Add `.gitignore`** before next commit
3. **Validate agent names** against known agent directory list
4. **Replace `sleep 30`** with active polling + timeout
5. **Add error handling** to all tmux operations

### Short-term (MEDIUM)

6. **Implement test suite** — shell-based tests for orchestration loop
7. **Add CI/CD** — GitHub Actions for linting and validation
8. **Add structured logging** — timestamps, log levels, log file
9. **Fix polling loop counter** — separate idle time from work time

### Long-term (LOW)

10. Clean up empty `tools/` and `work/` directories
11. Fix Chinese artifact in `skills/sre/SKILL.md`
12. Adapt skill scanning steps to project type

---

## Files Examined

| File | Lines | Role |
|------|-------|------|
| `INSTRUCTIONS.md` | 107 | Core orchestration script |
| `README.md` | 33 | Project documentation |
| `agents/shared/WORKFLOW.md` | 85 | Cross-agent collaboration rules |
| `agents/code-reviewer/brain.md` | 176 | Code reviewer agent |
| `agents/python-expert/brain.md` | 262 | Python expert agent |
| `agents/security-auditor/brain.md` | 298 | Security auditor agent |
| `skills/architect/SKILL.md` | 221 | Architect skill |
| `skills/sre/SKILL.md` | 279 | SRE audit skill |
| `skills/writing-plans/SKILL.md` | 152 | Writing plans skill |
| `skills/writing-plans/plan-document-reviewer-prompt.md` | 49 | Plan reviewer prompt |
| `.pi-loop.json.lock` | 1 | Runtime lock file |