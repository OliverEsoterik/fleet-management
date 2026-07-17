# Skills Reference

Quick reference for every skill in this project. Skills are auto-discovered by
pi and available via `/skill:<name>`.

## Legend

| Icon | Meaning |
|------|---------|
| **Orchestrator** | Use via `/skill:orchestrator <task>` — the orchestrator auto-selects this skill |
| **Direct** | Use via `/skill:<name> <task>` |
| **Reference** | Used as methodology/data dependency by other skills (not directly invoked) |
| **Delegation** | Defines sub-agents with phases — the orchestrator reads the `## Delegation` section |
| **Methodology** | Reference material — includes step-by-step instructions for a sub-agent to follow |

---

## Skill List

### Architect

- **Invocation:** `/skill:architect <request>`
- **Type:** Methodology
- **Dependencies:** research, writing-plans, execute
- **Purpose:** Architectural design workflow for complex codebase changes.
  Deeply understands the codebase, researches options, documents decisions
  as ADRs, and produces implementation plans. Human-in-the-loop at every
  stage.

### Better Products Habits

- **Invocation:** `/skill:better-products-habits <task>`
- **Type:** Methodology
- **Dependencies:** none
- **Purpose:** Five habits for building better products faster — write it
  down, think deeply, use data, focus, and grow. Based on Hiten Shah's
  methodology.

### Create Skill

- **Invocation:** `/skill:create-skill <description>`
- **Type:** Delegation (4 phases)
- **Dependencies:** research (optional), create-skill (self)
- **Purpose:** Create a new skill in the project. Runs research (optional),
  synthesis, planning, and writing phases. Supports both research-backed and
  lightweight creation.

### Execute

- **Invocation:** `/skill:execute <plan-path>`
- **Type:** Delegation (multi-phase)
- **Dependencies:** git-workflow-and-versioning
- **Purpose:** Execute a written implementation plan. Reviews the plan,
  decomposes into subagent tasks, and works through them step by step.
  Prevents work on main/master by enforcing the project's git workflow.

### Financial Analysis

- **Invocation:** `/skill:orchestrator analyze <ticker>` (orchestrator routes here)
- **Type:** Delegation (3 phases)
- **Dependencies:** stock-info, lyn-alden-dcf, peter-lynch, nassim-nicholas-taleb
- **Purpose:** Multi-methodology financial analysis pipeline. Phase 1 collects
  data, Phase 2 runs DCF (Lyn Alden), GARP (Peter Lynch), and antifragility
  critique (Taleb) in parallel, Phase 3 produces a consolidated recommendation.

### Fix My Work

- **Invocation:** `/skill:fix-my-work <issue>`
- **Type:** Delegation (2 phases)
- **Dependencies:** none
- **Purpose:** Diagnose and fix issues in the repository. Launches a debugger
  to find problems, then a coder to implement fixes.

### Git Workflow

- **Invocation:** Used as reference by the execute skill
- **Type:** Methodology
- **Dependencies:** none
- **Purpose:** Structures git workflow practices — branching, committing,
  versioning, changelogs, and release management.

### Lyn Alden DCF

- **Invocation:** Used as reference by financial-analysis
- **Type:** Methodology
- **Dependencies:** stock-info
- **Purpose:** Discounted Cash Flow (DCF) analysis following Lyn Alden's
  tutorial methodology. Step-by-step process for valuing businesses, stocks,
  projects, or bonds.

### Nassim Nicholas Taleb

- **Invocation:** Used as reference by financial-analysis
- **Type:** Methodology
- **Dependencies:** none
- **Purpose:** Antifragility, black swans, skin in the game, via negativa,
  Lindy effect, and epistemic humility. Socratic critique that surfaces
  hidden fragility and asymmetric risk.

### Orchestrator

- **Invocation:** `/skill:orchestrator <task>`
- **Type:** Delegation (meta — reads other skills' delegation plans)
- **Dependencies:** all skills (discovers dynamically)
- **Purpose:** Master entry point. Analyzes the request, discovers all skills
  in `skills/`, matches against their names and descriptions, and executes
  delegation plans or decomposes generically. Never executes work directly.

### Peter Lynch

- **Invocation:** Used as reference by financial-analysis
- **Type:** Methodology
- **Dependencies:** stock-info
- **Purpose:** Growth at a Reasonable Price (GARP) methodology. Classifies
  stocks into 6 categories, computes PEG ratio, checks balance sheet health,
  analyzes insider activity, and generates a buy/hold/sell recommendation.

### Research

- **Invocation:** `/skill:research <query>`
- **Type:** Delegation (1 parallel phase)
- **Dependencies:** none
- **Purpose:** Multi-source research. Scans arxiv, pubmed, github, archive,
  and web in parallel using dedicated search tools, then produces a
  consolidated research report. Sources are opt-in.

### Review and Fix

- **Invocation:** `/skill:orchestrator review and fix` (orchestrator routes here)
- **Type:** Delegation (3 phases)
- **Dependencies:** none
- **Purpose:** Full pipeline — review the repository, plan fixes, and
  implement them. Runs audit, architecture, and implementation phases
  sequentially.

### Review My Work

- **Invocation:** `/skill:orchestrator review my work` (orchestrator routes here)
- **Type:** Delegation (1 parallel phase)
- **Dependencies:** none
- **Purpose:** Review the repository for security vulnerabilities, test
  quality, and infrastructure issues. Launches specialist auditors in
  parallel.

### Setup Testing Workflows

- **Invocation:** `/skill:setup-testing-workflows <repo-path>`
- **Type:** Methodology
- **Dependencies:** none
- **Purpose:** Detect the project type and write a minimal, correct
  `.github/workflows/test.yml` GitHub Actions workflow. Handles Python,
  Node.js, Go, Rust, and Makefile-based projects.

### Stock Info

- **Invocation:** Used as data provider by lyn-alden-dcf, peter-lynch,
  financial-analysis
- **Type:** Methodology (data provider)
- **Dependencies:** yfinance (Python)
- **Purpose:** Fetch financial data for any ticker via bash scripts.
  Provides stock info, income statements, balance sheets, cash flow,
  insider transactions, institutional holders, earnings history, stock
  prices, and calendar data. All local — uses yfinance under the hood.

### Update README

- **Invocation:** `/skill:update-readme`
- **Type:** Methodology
- **Dependencies:** none
- **Purpose:** Scan the project structure and update README.md to accurately
  reflect all skills, scripts, and documentation.

### Writing Plans

- **Invocation:** Used as reference by architect
- **Type:** Methodology
- **Dependencies:** none
- **Purpose:** Write implementation plans for multi-step tasks. Produces
  dated files in `docs/plans/` with numbered steps, verification checks,
  and file paths.
