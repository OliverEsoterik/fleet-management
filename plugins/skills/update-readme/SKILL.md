---
name: update-readme
description: Scan the project structure and update README.md to accurately reflect all skills, scripts, and documentation.
---

# Update README

## Overview

This is a **methodology skill** — it provides step-by-step instructions for updating the README. The orchestrator reads this and passes it to a subagent that performs the work.

## Procedure

### Step 1: Snapshot the current README

Read `README.md` and note the existing structure table, sections, and instructions. Identify anything that looks stale or missing.

### Step 2: Scan the project structure

Run these discovery commands and record what you find:

```bash
# Skills — list every skill and read its description from frontmatter
ls plugins/
for d in plugins/skills/*/; do head -3 "$d/SKILL.md" 2>/dev/null; echo "---"; done; for f in plugins/workflows/*.md; do head -3 "$f" 2>/dev/null; echo "---"; done

# Plans — list docs/plans/ files
ls docs/plans/ 2>/dev/null
```

### Step 3: Reconcile

For each item found on disk, check if the README mentions it. For each item documented in the README, check if it still exists on disk. Identify:

- **Missing entries** — things on disk but not documented
- **Stale entries** — things documented but no longer on disk
- **Outdated descriptions** — skill descriptions that changed
- **Outdated instructions** — workflow steps that no longer match

### Step 4: Apply updates

Edit `README.md` to reflect the current state. Follow the existing structure and tone. Typical sections:

- **Top** — one-paragraph description of the project
- **How to use** — current workflow instructions (invoke `/skill:orchestrator`)
- **Structure table** — paths and purposes, one row per significant directory/file
- **Adding a skill** — brief instructions

### Step 5: Verify

Read the final `README.md` back and confirm it reads correctly. Check that:

- Every `plugins/skills/*/` directory and `plugins/workflows/*.md` file has a row in the structure table
- Path references use correct relative paths
- No stale references to deleted directories or old workflows

## When to Invoke

Use this skill when:
- A new skill was added
- An existing skill's description or purpose changed
- The workflow was modified
- Before committing changes to the project