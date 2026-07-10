---
name: update-readme
description: Use this skill to update the README.md — scan the project structure and ensure the README accurately reflects all agents, skills, scripts, and docs
---

# Update README

## Overview

This skill audits the project structure against the current `README.md` and brings it up to date. It discovers what exists on disk and reconciles it with the documented state.

**Announce at start:** "I'm using the update-readme skill to audit and update the README."

**Prerequisites:** Run from the project root directory (where `README.md`, `agents/`, and `skills/` live).

---

## Procedure

### Step 1: Snapshot the current README

Read `README.md` and note the existing structure table, sections, and instructions. Identify anything that looks stale or missing.

### Step 2: Scan the project structure

Run these discovery commands and record what you find:

```bash
# Agents — list every agent directory and read its description from brain.md
ls agents/
for d in agents/*/; do head -3 "$d/brain.md"; done

# Skills — list every skill and read its description from frontmatter
ls skills/
for d in skills/*/; do head -3 "$d/SKILL.md" 2>/dev/null; done

# Tool scripts — list tools inside each skill
find skills -name 'tools' -type d -exec ls {} \;

# Plans — list docs/plans/ files
ls docs/plans/ 2>/dev/null

# Extensions — list .pi/extensions/ files
ls .pi/extensions/ 2>/dev/null
```

### Step 3: Reconcile

For each item found on disk, check if the README mentions it. For each item documented in the README, check if it still exists on disk. Identify:

- **Missing entries** — things on disk but not documented
- **Stale entries** — things documented but no longer on disk
- **Outdated descriptions** — agent/skill descriptions that changed
- **Outdated instructions** — workflow steps that no longer match

### Step 4: Apply updates

Edit `README.md` to reflect the current state. Follow the existing structure and tone (see existing README for reference). Typical sections to maintain:

- **Top** — one-paragraph description of the project
- **How to use** — current workflow instructions (invoke `/skill:invoke-fleet` etc.)
- **Structure table** — paths and purposes, one row per significant directory/file
- **Adding an agent** — brief instructions
- **Adding a skill** — brief instructions (if not present)

### Step 5: Verify

Read the final `README.md` back and confirm it reads correctly. Check that:

- Every `agents/*/` directory has a row in the structure table
- Every `skills/*/` directory has a row in the structure table
- Every `.sh` file in `skills/*/tools/` is accounted for
- `docs/plans/` and `.pi/extensions/` are mentioned if they exist
- Path references use correct relative paths

---

## When to Invoke

Use this skill when:
- A new agent, skill, or tool script was added
- An existing agent's description or purpose changed
- The workflow steps were modified
- Before committing changes to the project