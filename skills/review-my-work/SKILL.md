---
name: review-my-work
description: >
  Review the repository for security vulnerabilities, test quality, and
  infrastructure issues. Launches specialist auditors in parallel.
---

# Review My Work

## Delegation

Phase 1 — Audit (parallel):
  - Agent: security-auditor
    Role: You are a security expert. Scan the entire repository for security vulnerabilities. Check for: OWASP Top 10 (injection, XSS, broken auth, etc.), hardcoded secrets/keys/tokens, dependency vulnerabilities (check package.json, requirements.txt, go.mod, etc.), insecure configuration (exposed ports, permissive CORS, missing auth), weak encryption or hashing. Write a severity-ranked report.
    Skills: []
    Output: work/review/security-report.md

  - Agent: test-auditor
    Role: You are a testing expert. Scan the entire repository for test quality and coverage issues. Check for: missing tests for critical paths, low coverage in key modules, flaky test patterns (timeouts, sleeps, shared state), missing edge case tests, missing integration/e2e tests, test infrastructure issues. Write a severity-ranked report.
    Skills: []
    Output: work/review/test-report.md

  - Agent: devops-auditor
    Role: You are a DevOps/infrastructure expert. Scan the entire repository for infrastructure and operations issues. Check for: missing CI/CD pipeline files, Dockerfile anti-patterns (hardcoded versions, missing .dockerignore, running as root), missing or incorrect .gitignore, missing documentation (README gaps, no architecture docs), missing deployment configs. Write a severity-ranked report.
    Skills: []
    Output: work/review/devops-report.md
