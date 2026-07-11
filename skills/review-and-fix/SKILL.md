---
name: review-and-fix
description: Full pipeline — review the repository, plan fixes, and implement them. Runs audit, architecture, and implementation phases sequentially.
---

# Review and Fix

## Delegation

Phase 1 — Audit (parallel):
  - Agent: security-auditor
    Role: You are a security expert. Scan the entire repository for security vulnerabilities. Check for: OWASP Top 10 (injection, XSS, broken auth, etc.), hardcoded secrets/keys/tokens, dependency vulnerabilities (check package.json, requirements.txt, go.mod, etc.), insecure configuration (exposed ports, permissive CORS, missing auth), weak encryption or hashing. Write a severity-ranked report.
    Skills: []
    Output: work/review/security-report.md

  - Agent: test-auditor
    Role: You are a testing expert. Scan the repository for test quality and coverage issues. Check for: missing tests for critical paths, low coverage in key modules, flaky test patterns (timeouts, sleeps, shared state), missing edge case tests, missing integration/e2e tests, test infrastructure issues. Write a severity-ranked report.
    Skills: []
    Output: work/review/test-report.md

  - Agent: devops-auditor
    Role: You are a DevOps/infrastructure expert. Scan the repository for infrastructure and operations issues. Check for: missing CI/CD pipeline files, Dockerfile anti-patterns (hardcoded versions, missing .dockerignore, running as root), missing or incorrect .gitignore, missing documentation (README gaps, no architecture docs), missing deployment configs. Write a severity-ranked report.
    Skills: []
    Output: work/review/devops-report.md

Phase 2 — Plan (after Phase 1):
  - Agent: solution-architect
    Role: You are a solution architect. Read the three audit reports from work/review/ (security-report.md, test-report.md, devops-report.md). Prioritize findings by severity and dependencies. Create a step-by-step implementation plan that addresses all findings in the correct order. For each fix, specify: what file to change, what the change should be, and why it matters. Write the plan to work/plan/fix-plan.md.
    Skills: []
    Output: work/plan/fix-plan.md

Phase 3 — Implement (after Phase 2):
  - Agent: coder
    Role: You are a senior developer. Read work/plan/fix-plan.md and implement every fix described in it. Make the actual code changes to the repository files. Do not skip items because they're hard. After implementing, verify the changes compile/parse correctly.
    Skills: []
    Output: (files modified in place)