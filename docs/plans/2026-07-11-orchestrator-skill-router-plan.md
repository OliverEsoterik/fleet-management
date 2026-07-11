# Orchestrator Skill — Multi-Agent Fleet with Router + Use-Case Modules

**Date:** 2026-07-11  
**Status:** Draft  
**Author:** pi

## Goal

Build a single orchestrator skill (`invoke-fleet`) that routes to the right set of agents and instructions for any use case. Currently supports two use cases:

1. **Code review** — security audit, testing audit, GitOps audit
2. **Financial analysis** — DCF valuation, comparable company analysis, qualitative risk/competitive analysis

Future use cases should be drop-in additions requiring no changes to the orchestrator itself.

## Motivation

The current `invoke-fleet` skill uses a hub-and-spoke model with bash scripts (`delegate.sh`, `orchestrate.sh`, etc.) and a file-based `work/todo/` contract between agents. The existing `reviewer` agent and `financial-analyst` agent each handle their domain independently. There is no unified mechanism to say "run a review" or "run a financial analysis" that automatically invokes the correct sub-agents with the right instructions.

This plan extends `invoke-fleet` into a **router + module** architecture:

- The orchestrator skill reads the user's request, identifies the category, and loads the corresponding module file
- Each module file (`analysis/code-review.md`, `analysis/financial-analysis.md`) contains the detailed instructions for which agents to launch and what to ask them
- Agent specs (`agents/security-reviewer.md`, `agents/dcf-analyzer.md`, etc.) remain reusable across categories

## Architecture

```
skills/invoke-fleet/
├── SKILL.md                          # Orchestrator: parses request, routes to module
├── analysis/
│   ├── code-review.md                # "For code review, launch these 3 agents with these instructions"
│   └── financial-analysis.md         # "For financial analysis, launch these 3 agents with these instructions"
├── agents/
│   ├── security-reviewer.md          # Reusable agent spec — knows security
│   ├── test-auditor.md               # Reusable agent spec — knows testing
│   ├── gitops-auditor.md             # Reusable agent spec — knows GitOps/k8s
│   ├── dcf-analyzer.md               # Reusable agent spec — knows DCF formulas
│   ├── comps-analyzer.md             # Reusable agent spec — knows multiples
│   └── risk-analyzer.md              # Reusable agent spec — knows qualitative analysis
└── tools/                            # Existing bash scripts (unchanged)
    ├── delegate.sh
    ├── orchestrate.sh
    ├── collect.sh
    └── cleanup.sh
```

### How routing works (in SKILL.md)

```
User: "run a code review on the auth module"
                │
                ▼
SKILL.md sees "code review" in the request
                │
                ▼
SKILL.md reads analysis/code-review.md
                │
                ▼
code-review.md says:
  - Launch security-reviewer with "audit auth module for vulns"
  - Launch test-auditor with "audit test coverage in auth module"
  - Launch gitops-auditor with "audit k8s manifests for auth module"
                │
                ▼
SKILL.md launches 3 agents in parallel (via Agent tool, run_in_background: true)
                │
                ▼
Collect results, consolidate, present
```

### How the module files work

Each `analysis/<category>.md` is a self-contained markdown file that the orchestrator reads and executes. It contains:

```markdown
# code-review

## Agents to launch

### 1. security-reviewer
**Agent spec:** agents/security-reviewer.md  
**Task:** Audit <TARGET> for security vulnerabilities including OWASP Top 10, injection flaws, auth weaknesses, secret exposure, and dependency risks.

### 2. test-auditor
**Agent spec:** agents/test-auditor.md  
**Task:** Audit <TARGET> test coverage, test quality, missing edge cases, and test infrastructure.

### 3. gitops-auditor
**Agent spec:** agents/gitops-auditor.md  
**Task:** Audit <TARGET> for GitOps best practices — drift detection, RBAC, secrets management, CI/CD pipeline security.

## Consolidation

After all 3 agents report back, consolidate the findings into a single prioritized report ordered by severity (security > testing > operations).
```

Placeholder `<TARGET>` is replaced by the orchestrator with the actual target the user specified (e.g., "auth module", "payment service").

### Agent specs exist separately

An agent spec file like `agents/security-reviewer.md` defines *identity and behavior*, not *which task to run*. It says "you are a security expert, think like this, use these tools." It does not hardcode the task — the task is injected by the orchestrator.

This means `security-reviewer.md` can be reused by:
- code-review analysis
- a future "security incident response" analysis
- a future "compliance audit" analysis

## Files to Create

### New files

| File | Purpose |
|------|---------|
| `skills/invoke-fleet/analysis/code-review.md` | Module: which 3 agents to launch, what to ask, how to consolidate |
| `skills/invoke-fleet/analysis/financial-analysis.md` | Module: which 3 agents to launch, what to ask, how to consolidate |
| `skills/invoke-fleet/agents/security-reviewer.md` | Agent spec: security expert identity |
| `skills/invoke-fleet/agents/test-auditor.md` | Agent spec: testing expert identity |
| `skills/invoke-fleet/agents/gitops-auditor.md` | Agent spec: GitOps/k8s expert identity |
| `skills/invoke-fleet/agents/dcf-analyzer.md` | Agent spec: DCF valuation expert identity |
| `skills/invoke-fleet/agents/comps-analyzer.md` | Agent spec: comparable company analysis identity |
| `skills/invoke-fleet/agents/risk-analyzer.md` | Agent spec: qualitative risk/competitive analysis identity |

### Modified files

| File | Change |
|------|--------|
| `skills/invoke-fleet/SKILL.md` | Add routing section: parse request → read module → launch agents → consolidate |

### Files that stay unchanged

- `skills/invoke-fleet/tools/*.sh` — existing bash scripts
- `agents/financial-analyst/brain.md` — existing agent spec
- `agents/reviewer/brain.md` — existing agent spec
- `agents/shared/WORKFLOW.md` — existing workflow rules

## Edge Cases & Decisions

### What if a category has no module file?

The orchestrator reports: "I don't have instructions for that category. Available categories: code-review, financial-analysis."

### What if the user names a specific agent instead of a category?

The orchestrator still routes via the module file. If the user says "run the security reviewer on the auth module," the orchestrator finds the category that uses security-reviewer (code-review) and runs that module. The module file already includes the security-reviewer task.

### What if an agent is needed in multiple categories?

The agent spec file lives once in `agents/`. Both module files reference it by name. No duplication.

### How do agents write results back?

Agents write their result to `work/results/<agent-name>.md` (same pattern as the existing invoke-fleet contract). The orchestrator reads `work/results/` after all agents finish.

### Parallel vs sequential launch

All agents within a category are independent and can run in parallel (via `run_in_background: true` on the Agent tool). The orchestrator waits for all to complete before consolidating.

## Future-Proofing

Adding a new use case (e.g., "infrastructure audit" → network audit + cost audit + performance audit):

1. Create `analysis/infrastructure-audit.md`
2. Create `agents/network-auditor.md`, `agents/cost-auditor.md`, `agents/perf-auditor.md` (or reuse existing ones)
3. No changes to `SKILL.md`

## Verification

1. Read `SKILL.md` — routing logic is correct and clear
2. Read `analysis/code-review.md` — lists 3 agents with tasks and consolidation instructions
3. Read `analysis/financial-analysis.md` — lists 3 agents with tasks and consolidation instructions
4. Read each `agents/<name>.md` — each defines a distinct agent identity, no task hardcoding
5. All tool scripts remain untouched and working