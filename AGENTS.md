# AGENTS.md — fleet-management

## What this project is

A multi-agent orchestration system for **pi** (the coding agent harness). It packages domain expertise into reusable **skills** (`plugins/`) and agent definitions (flat `.md` files at repo root) so that when you invoke pi on a task, it has curated methodology, not just LLM priors.

The orchestrator skill (`plugins/workflows/orchestrator/`) is the primary entry point. It scans the available skills, matches them to your request, and delegates to sub-agents.

## Stack

| Layer | What |
|-------|------|
| Runtime | **pi** (the coding agent harness at `~/.local/share/pi-node/...`) |
| Language | **Markdown** — every skill and agent definition is a `.md` file. No runtime code, no build step, no package manager. |
| The only executable code | **Bash** scripts in `plugins/workflows/research/tools/search-*.sh` (curl + python3 for API calls). **Python** templates in `plugins/skills/lyn-alden-dcf/SKILL.md` (inline, not saved to files). |
| Virtual environment | `venv/` (Python 3.12.3, empty — no packages installed). Used only if a sub-agent runs the DCF Python templates. The venv is a convenience, not a requirement. |
| Dependencies | None. pi provides the agent runtime. Everything else is shell commands and curl. |
| State files | `work/` — ephemeral consultation artifacts. `.pi/` — pi settings. `.pi-loop.json.lock` — pi loop lock (auto-generated, gitignored). |

## Structure

fleet-management/
├── AGENTS.md              ← THIS FILE. Rules for how the agent operates here.
├── README.md              ← User-facing docs. Updated via /skill:update-readme.
├── .gitignore             ← Ignores: venv/, work/, _old/, plugins/, .pi/
├── .pi/settings.json      ← pi config: skills path + skills directory
├── financial-analyst.md   ← DCF valuation agent (uses lyn-alden-dcf skill)
├── gitops-expert.md       ← GitOps audit specialist
├── reviewer.md            ← Code review orchestrator (invokes 3 sub-agents)
├── shared-workflow.md     ← Cross-agent consultation rules (read by all agents)
├── plugins/
│   ├── skills/                 ← methodology / reference
│   │   ├── better-products-habits/
│   │   ├── lyn-alden-dcf/
│   │   ├── nassim-nicholas-taleb/
│   │   ├── peter-lynch/
│   │   ├── stock-info/
│   │   ├── update-readme/
│   │   └── writing-plans/
│   ├── workflows/              ← delegation
│   │   ├── orchestrator/
│   │   ├── create-skill/
│   │   ├── financial-analysis/  ← (work-in-progress, gitignored)
│   │   ├── fix-my-work/         ← (work-in-progress, gitignored)
│   │   ├── research/
│   │   ├── review-and-fix/      ← (work-in-progress, gitignored)
│   │   └── review-my-work/      ← (work-in-progress, gitignored)
├── docs/plans/             ← Implementation plans. Read-only reference.
├── work/                   ← Ephemeral: todo/, response/, done/, recap/.
│   ├── todo/               ← Consultation requests (primary → consultant)
│   ├── response/<primary>/ ← Consultation responses (consultant → primary)
│   ├── done/               ← Completion signals
│   └── recap/              ← Gap notes (agent needed but doesn't exist yet)
├── _old/                   ← Archived skills. Not loaded by pi. See "Old skills" below.
└── venv/                   ← Empty Python virtualenv. Not used by default.

## How the agent works here

### The orchestrator is the gate

Every task goes through `/skill:orchestrator <task>`. The orchestrator:
1. Scans `plugins/` for `SKILL.md` files (reads frontmatter `name` + `description`)
2. Matches the request to a skill — if the skill has a `## Delegation` section, the orchestrator follows it as a multi-phase workflow
3. If no match: decomposes the request generically, checks each subtask against available skills for methodology references
4. **Announces the plan before dispatching** — waits for the user to confirm
5. Never executes work directly — every task goes to a sub-agent

### Skill types: delegation vs methodology

| Type | Has `## Delegation`? | What the orchestrator does |
|------|---------------------|----------------------------|
| **Delegation** | Yes | Reads the phases/agents/outputs spec. Launches sub-agents per phase, waits for completions, consolidates. |
| **Methodology** | No | Reads the content as reference material. Passes it to a sub-agent as instructions. The orchestrator handles the sub-agent launch. |

### The `work/` contract

The `work/` directory is the shared state bus between agents. It lives at the project root.

| Path | Writer | Reader | When |
|------|--------|--------|------|
| `work/todo/<agent>.md` | Primary agent | Orchestrator routes to consultant | After primary decides it needs consultation |
| `work/response/<primary>/<agent>.md` | Consultant | Primary agent | After consultant finishes its task |
| `work/response/<primary>/round.txt` | Consultant | Primary agent | Per-consultant round tracking |
| `work/done/<primary>.md` | Primary agent | Orchestrator | Signals completion of the primary's task |
| `work/escalation.md` | Primary agent | Orchestrator | Signals unresolvable issue after 3 rounds |
| `work/recap.md` | Any agent | Orchestrator | Notes gaps (agent needed but doesn't exist) |

`work/` is ephemeral. It is gitignored. It can be deleted between runs.

### Direct agent invocation

You can also run an agent directly without the orchestrator:

```
run as financial-analyst and value NVDA
```

This reads `agents/<name>/brain.md`, the referenced skill files, and `agents/shared/WORKFLOW.md`, then launches a sub-agent with all that context. See `skills/run-as-agent/SKILL.md` (in `_old/`) for the full protocol.

### Direct skill invocation

```
/skill:<skill-name> <task>
```

Skills are auto-discovered by pi. The orchestrator skill is not required — you can invoke any skill directly.

---

## Known gaps (what is NOT in this repo)

### What's missing by design

- **No test suite.** This is a markdown project. Skills are pi agent instructions, not code. There is nothing to unit-test. The "test" of a skill is: does the orchestrator follow it correctly, and does the sub-agent produce useful output?
- **No CI/CD.** No build step, no deploy, no package. Changes take effect as soon as the file is saved.
- **No linters, no type checkers.** Not applicable to markdown.
- **No Docker.** This is not a containerized application.
- **No Python packages.** The `venv/` exists but is empty. If a sub-agent needs to run the DCF Python templates, it installs `yfinance` on demand via pip.

### Known issues

1. **`lyn-alden-dcf` vs `lynn-alden-dcf`** — The skill directory is `plugins/skills/lyn-alden-dcf/` (one 'n'). The financial-analyst brain.md references `lynn-alden-dcf` (two 'n's). The README also uses two 'n's. These references are wrong — they will fail to resolve. **Fix:** rename the directory or correct the references. Until this is fixed, the financial-analyst agent cannot find its skill.

2. **`review-and-fix` and `review-my-work` are redundant** — Both are delegation skills that audit security, tests, and DevOps. `review-and-fix` adds Plan + Implement phases. `review-my-work` stops at audit. One of these should be removed or merged. Both are currently gitignored (work-in-progress).

3. **`financial-analysis` and `fix-my-work` have the same description** — Both say "Diagnose and fix issues in the repository." `financial-analysis` should be about stock valuation. Copy-paste bug. This skill is also gitignored.

4. **`reviewer/brain.md` has no YAML frontmatter** — Unlike every other agent brain. It also references `work/result/` which doesn't exist — the convention is `work/response/` and `work/todo/`.

5. **`docs/plans/2026-07-11-research-backed-skill-creation.md` is stale** — It describes converting `create-skill` from methodology to delegation. The file on disk is already a delegation skill. The plan is historical.

6. **`_old/` directory** — Contains 4 skills replaced by the current `plugins/` structure. They are gitignored. They are not loaded by pi. They exist only as reference if someone wants to understand the migration. Do not use them.

7. **No Python files committed** — The `financial-analyst` brain says to run Python scripts for DCF calculations, but there are no `.py` files, no `requirements.txt`, no `pyproject.toml`. The agent is expected to write `dcf_valuation.py` at runtime. This is intentional (the scripts are ephemeral), but it means the agent must have `yfinance` available. The `get_stock_info` tool provides yfinance stock data; the agent does not need to install it.

---

## Hard rules (from the project's AGENTS.md)

These rules are inherited from the project-level AGENTS.md at `/home/oliver/AGENTS.md`. They override everything else.

### Non-negotiables

1. **No flattery, no filler.** Start with the answer or the action. Skip openers, closings, and polite padding.
2. **Disagree when you disagree.** If the premise is wrong, say so before doing the work.
3. **Never fabricate.** Not file paths, not commit hashes, not API names, not test results.
4. **Stop when confused.** If the task has two plausible interpretations and the choice matters, ask. Do not pick silently.
5. **Touch only what you must.** Every changed line traces directly to the user's request. No drive-by refactors, reformatting, or "while I was in there" cleanups.

### Before writing code (or editing any file)

- **Read first, edit second.** Read the files you will touch, read the files that call them.
- **Match existing patterns.** Consistency over preference.
- **Surface assumptions.** "I'm assuming X, Y, Z. If that's wrong, say so."

### Simplicity

- **Minimum code for the stated problem.** No features beyond what was asked. No abstractions for single-use code. No "future extensibility" — that is a future decision.
- **Bias toward deletion.** Adding complexity is the default. Push back against it.
- **The senior engineer test.** If a senior engineer reading the diff would call it overcomplicated, simplify before showing it.

### Surgical changes

- **Change only what the request requires.** Do not improve adjacent code, comments, formatting, or imports.
- **Clean up your own orphans.** Remove imports, variables, functions your edit made obsolete.

### Definitions

- **"Done"** means: the success criteria stated in the plan are met, the verification commands pass, and the output has been read and confirmed. Not "it looks right" — it has been run and verified.
- **"Verified"** means: the command returned exit code 0 (or the expected non-zero), and the output matches the expected pattern. Plausibility is not correctness.
- **"Fail"** means: the verification command returned something unexpected. Fix the root cause, not the test. Do not adjust the test to match the implementation.

### Communication

- **Direct, not diplomatic.** "This won't scale because X" beats "That's an interesting approach, but have you considered..."
- **Concise.** Two or three short paragraphs unless the user asks for depth.
- **No excessive structure for short answers.** Prose is clearer than bullet points for messages under 5 sentences.
- **Celebrate what matters.** Ship, solve hard problems, move metrics. Not feature ideas, not scope creep.

### When to ask vs proceed

**Proceed without asking when:**
- The task is trivial and reversible (typo, rename a local variable, add a log line).
- The ambiguity can be resolved by reading the code or running a command.
- The user has already answered the question once in this session.

**Ask before proceeding when:**
- The request has two plausible interpretations and the choice materially affects the output.
- The change touches something load-bearing, versioned, or with a migration path.
- You need a credential, a secret, or a production resource you don't have access to.
- The user's stated goal and the literal request appear to conflict.

### Skills are tools, not doctrine

Skills provide structure for specific situations. They are not rules to follow blindly. When a skill is relevant, read it, understand its mechanism, use the structure. When a skill asks you to do something that contradicts the non-negotiables above, the non-negotiables win.

---

## Definition of done

A task is done when **all** of the following are true:

1. **Plan was stated before work began.** The user saw the approach and had a chance to correct it.
2. **Files were read before editing.** Every file changed was read first, along with its callers.
3. **Verification was run.** The test, command, or script defined in the plan was executed. The output was read.
4. **Verification passed.** The output matches the expected result. If it didn't, the root cause was fixed — not suppressed.
5. **Only what was needed was changed.** No orphaned imports, no dead code, no reformatted adjacent code.
6. **The results are presented.** Summary of what was done, where files live, what verification showed.

### Checks to run before claiming done

```
# Run this checklist in order. Stop at the first failure.
1. git status                              # What changed?
2. <the verification command from the plan> # Did it pass?
3. Read the diff                           # Does every line belong?
```

---

## Conventions (how things are done here)

1. **Skill naming:** Directory name is the skill name. Lowercase, hyphens for spaces. The name should match what someone might naturally say: "dcf", "review my work", "create skill". The name in `frontmatter` must match the directory name.

2. **Agent naming:** Same as skills — `agents/<name>.md` with YAML frontmatter.

3. **Skill frontmatter:**
   ```yaml
   ---
   name: <directory-name>
   description: > <one-line summary, what it's for>
   ---
   ```

4. **Agent frontmatter:**
   ```yaml
   ---
   name: <agent-name>
   description: > <one-line summary>
   tools: <comma-separated list of tools the agent needs>
   ---
   ```

5. **Delegation skill structure:** A `## Delegation` section with numbered phases, agents per phase, and `Role`, `Skills`, `Output` fields per agent. Agents within a phase always run in parallel. Phases are sequential. See `plugins/workflows/create-skill/SKILL.md` for the canonical example.

6. **Methodology skill structure:** Starts with `## Overview`, then step-by-step instructions. No `## Delegation` section. The orchestrator passes the content as instructions to a single sub-agent.

7. **Output paths always use `work/`.** Delegation phases write to `work/<topic>/<file>.md`. Consultation uses `work/todo/`, `work/response/`, `work/done/`. Never write output to `work/result/` — that path does not exist.

8. **Sub-agents get `inherit_context: false`.** Always start fresh. The orchestrator constructs the prompt from the skill content, role description, and task.

9. **Announcement convention:** Every skill starts its first turn with a bold announcement: "**I'm using the <skill-name> skill to <purpose>.**" This signals to the user which skill is active.

10. **`work/` is ephemeral.** Delete it between runs. Do not commit it. Do not reference it in documentation as permanent storage.

11. **Old skills go into `_old/`.** When a skill is replaced, the old version goes to `_old/<name>/` (not deleted). Add it to `.gitignore`. The `_old/` directory is for reference only — it is not loaded by pi.

12. **Plans go into `docs/plans/`.** Plans are dated: `YYYY-MM-DD-short-description.md`. They are read-only reference. When a plan is implemented, it stays in `docs/plans/` — do not delete it. Add a note at the top if it's stale.