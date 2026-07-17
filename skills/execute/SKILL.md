---
name: execute
description: >
  Execute a written implementation plan. Reviews the plan critically,
  decomposes into subagent tasks, and works through them step by step
  with isolated subagent contexts. Prevents work on main/master by
  enforcing the project's git workflow.
---

# Execute — Plan Execution

## Delegation

Phase 1 — Review and Setup:
  - Agent: plan-reviewer
    Role: You are a plan reviewer. Read the plan that needs to be executed. Review it critically — surface any concerns about feasibility, correctness, missing steps, or ambiguity before execution begins. If the plan references files or code, read those files to verify the plan's assumptions. If the plan has issues, document them and fail early — do not proceed with a flawed plan. If the plan is sound, confirm and proceed.
    Skills: []
    Output: (confirmation or concerns — continue only if plan is sound)

Phase 2 — Execute (after Phase 1):
  - Agent: executor
    Role: You are an executor. Execute the plan step by step. Do not skip steps. For each step:
      1. Understand what needs to be done
      2. If the step involves code changes and has meaningful scope, delegate to a subagent (general-purpose or "qwen/qwen3-coder" for code-heavy tasks) so each task runs in a fresh context window
      3. If the step is trivial (e.g., a config change, a single-file edit), do it directly
      4. Verify each step before moving to the next
    Before making any changes, ensure you are not on main/master — use the git-workflow-and-versioning skill for branching guidance. Always work in a feature branch.
    Skills: [git-workflow-and-versioning]
    Output: (files modified in place, step-by-step summary)