# Review: `skills/run-as-agent/SKILL.md`

**Reviewed by:** Reviewer Agent
**Date:** 2026-07-11
**Status:** Needs minor corrections

---

## Summary

The skill file is well-structured and covers the full workflow for routing a user request to a sub-agent. The directory layout, step-by-step instructions, and tool access documentation are clear. However, there are several inaccuracies and omissions that should be fixed.

---

## Findings

### 1. Incorrect skill path reference in Step 3

The skill says referenced skills live at `skills/<skill-name>/SKILL.md`. But the only skill actually referenced in the codebase (`lyn-alden-dcf`) lives at `skills/lynn-alden-dcf/SKILL.md` (note: "lynn" not "lyn"). The skill file itself (line 9) also references `lyn-alden-dcf` whereas the directory is `lynn-alden-dcf`. This is a pre-existing typo in the directory name, but the skill should at minimum note that the path is `skills/lynn-alden-dcf/SKILL.md` to match the actual filesystem.

### 2. Missing `reviewer` agent's `work/` directory in the layout

The directory layout example shows:

```
agents/
├── reviewer/
│   ├── brain.md
│   └── work/
```

On disk, the `reviewer` agent exists but has no `work/` directory yet. The skill *describes* the layout as the intended structure, which is fine, but the codebase doesn't match. This is a minor inconsistency worth noting.

### 3. No mention of consulting existing agents before launching

The `agents/shared/WORKFLOW.md` defines a cross-agent collaboration contract. The `run-as-agent` skill describes how to *launch* a sub-agent, but it doesn't instruct the agent to first check whether any other agents should be consulted (per WORKFLOW.md). The skill should cross-reference that the launched agent must follow the shared WORKFLOW.md collaboration rules.

### 4. Missing `work/output/` path for the `reviewer` agent

The `reviewer` brain.md says sub-agents write to `../work/result` (relative to the agent's directory). The `run-as-agent` skill says output goes to `agents/<agent-name>/work/output/`. These conflict. The reviewer brain.md says `work/result` (not `work/output`). The skill should either align with the brain or note that the brain's own convention takes precedence.

### 5. `financial-analyst` agent missing `work/` directory

The layout shows `financial-analyst/work/` with subdirectories `output/`, `scripts/`, `todo/`. On disk, the `financial-analyst` agent only has `brain.md` and `research/`. The `work/` subtree does not exist. The skill describes a planned structure, not the current state.

### 6. Minor typo: "lyn-alden-dcf" vs "lynn-alden-dcf"

The skill references `lyn-alden-dcf` (missing an 'n'). The actual directory is `lynn-alden-dcf`. This is a pre-existing inconsistency in the codebase, but the skill propagates the typo in its example.

### 7. Missing instructions for `agents/`-relative path resolution

Step 1 says "Resolve relative to the project root (`/home/oliver/fleet-management/`)". This is correct, but the skill should also mention that the `agents/` directory is at the project root, not nested deeper.

---

## Recommendations

1. **Fix the path reference** in Step 3 to match the actual filesystem: `skills/lynn-alden-dcf/SKILL.md`.
2. **Add a cross-reference** to `agents/shared/WORKFLOW.md` — the launched agent must follow the collaboration contract.
3. **Clarify output path convention**: note that the brain.md's own convention takes precedence over the skill's default.
4. **Create the `work/` directories** for `reviewer` and `financial-analyst` agents if the layout is to match the documentation.
5. **Fix the typo** — either rename the directory to `lyn-alden-dcf` or update all references to `lynn-alden-dcf`.

---

## Conclusion

The skill is functionally correct and would work for its intended purpose. The issues are primarily documentation drift — the skill describes a planned directory structure that doesn't fully exist on disk, and it has a path mismatch with the `lynn-alden-dcf` skill. None of these are blockers, but they should be cleaned up for consistency.