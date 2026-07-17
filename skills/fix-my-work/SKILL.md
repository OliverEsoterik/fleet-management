---
name: fix-my-work
description: >
  Diagnose and fix issues in the repository. Launches a debugger to find
  problems, then a coder to implement fixes.
---

# Fix My Work

## Delegation

Phase 1 — Diagnose (parallel):
  - Agent: debugger
    Role: You are a debugger. Scan the repository for broken code, failing tests, compilation errors, lint errors, and runtime issues. Run: build/compile commands, linters, test suites, and dependency checks. Document everything that fails, including error messages and stack traces. Write a diagnosis report.
    Skills: []
    Output: work/fix/diagnosis-report.md

Phase 2 — Fix (after Phase 1):
  - Agent: coder
    Role: You are a senior developer. Read work/fix/diagnosis-report.md. Fix every issue listed in the report. After each fix, verify it resolves the issue (re-run the failing command). Do not skip items because they're complex. If a fix is not obvious, note it in work/fix/stuck.md instead of guessing.
    Skills: []
    Output: (files modified in place)
