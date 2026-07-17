---
name: setup-testing-workflows
description: >
  Detect the project type in a repo and write a minimal, correct
  .github/workflows/test.yml GitHub Actions workflow for running tests.
  Handles Python, Node.js, Go, Rust, Makefile-based projects, and unknown
  projects (prompts user).
---

# Setup Testing Workflows

## Overview

This is a **methodology skill**. It provides a step-by-step procedure for
detecting what kind of project a repo is and writing a correct
`.github/workflows/test.yml` file. The orchestrator reads this and passes it
to a subagent that performs the work.

The skill has two phases:

1. **Detect** — inspect the repo root for project files and determine the
   language, test tool, and version matrix
2. **Write** — emit `.github/workflows/test.yml` with the minimal correct
   workflow for the detected project type

After writing, the skill verifies the output is valid.

---

## Procedure

### Step 1: Read repo root

List all files in the project root (not recursive):

```bash
ls -la
```

Note whether a `.github/workflows/` directory already exists and what's in it:

```bash
ls -la .github/workflows/ 2>/dev/null || echo "NO_WORKFLOWS_DIR"
```

### Step 2: Detect project type

Check for project files in order of specificity. Stop at the first match.

#### Python detection

Run each check in order:

```bash
# Check for pyproject.toml
test -f pyproject.toml && head -40 pyproject.toml
# Check for setup.py
test -f setup.py && head -20 setup.py
# Check for setup.cfg
test -f setup.cfg && head -20 setup.cfg
# Check for requirements files
ls requirements*.txt 2>/dev/null
# Check for Python version file
cat .python-version 2>/dev/null
# Check for existing pytest config
test -f pytest.ini && cat pytest.ini
test -f pyproject.toml && grep -q "\[tool.pytest" pyproject.toml
```

**Determine:**
- **Test command:** If `pyproject.toml` has `[tool.pytest.ini_options]` or
  `pytest.ini` exists → `pytest`. If `pyproject.toml` has
  `[project.scripts]` with a key containing "test" → use that. Otherwise →
  `python -m unittest discover`.
- **Python versions:** From `.python-version` file first. Otherwise from
  `pyproject.toml` `requires-python` field (e.g., `>=3.11` → `["3.11",
  "3.12"]`). Default: `["3.x"]` (no matrix, use latest stable).
- **Install command:** `pip install -e ".[dev]"` if `[project.optional-dependencies]` has `dev`. Else `pip install -r requirements-dev.txt` if that exists. Else `pip install -r requirements.txt` if that exists. Else `pip install -e .`.
- **Cache path:** `~/.cache/pip`

#### Node.js detection

```bash
test -f package.json && cat package.json
test -f .nvmrc && cat .nvmrc
ls package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null
```

**Determine:**
- **Test command:** `package.json` `scripts.test` value. If missing → `npm test`.
- **Lint command (if applicable):** `package.json` `scripts.lint` value. If missing → none.
- **Node versions:** From `.nvmrc` first (strip `v` prefix). From
  `package.json` `engines.node` otherwise. Default: `["18", "20"]`.
- **Install command:** `npm ci` if `package-lock.json` exists. `yarn install
  --frozen-lockfile` if `yarn.lock`. `pnpm install --frozen-lockfile` if
  `pnpm-lock.yaml`. Otherwise `npm install`.
- **Cache path:** `~/.npm` for npm, `~/.cache/yarn` for yarn, `~/.local/share/pnpm/store` for pnpm.

#### Go detection

```bash
test -f go.mod && head -5 go.mod
```

**Determine:**
- **Test command:** `go test ./...`
- **Go version:** From `go.mod` first line (e.g., `go 1.21`). Default: `stable`.
- **No matrix needed** — Go tests run on one version in CI.

#### Rust detection

```bash
test -f Cargo.toml && head -20 Cargo.toml
test -f rust-toolchain.toml && cat rust-toolchain.toml
test -f rust-toolchain && cat rust-toolchain
```

**Determine:**
- **Test command:** `cargo test`
- **Toolchain:** From `rust-toolchain.toml` or `rust-toolchain` file first.
  Default: `stable`.
- **No matrix needed** — Rust tests run on one toolchain in CI.

#### Makefile detection

```bash
test -f Makefile && grep -E "^test:|^check:" Makefile
```

**Determine:**
- **Test command:** `make test` if `test:` target found. `make check` if only
  `check:` found. Otherwise, this is not a valid Makefile match.
- **No matrix needed.**

#### Unknown project

If none of the above matched, **ask the user** before proceeding:

> "I couldn't detect the project type in this repo. Here's what I found at the
> root: [list files]. What language/test tool should I set up?"

Wait for the user's answer, then proceed with whatever they specify.

---

### Step 3: Write the workflow

Create `.github/workflows/test.yml` using one of the templates below based on
the detected type. Do **not** add any extras not in the template — no uploads,
no deployments, no notification integrations unless the project already has
config files for them (e.g., `codecov.yml` exists → add coverage upload step).

If `.github/workflows/` does not exist, create it:

```bash
mkdir -p .github/workflows
```

#### Template: Python

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [<VERSIONS>]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt', '**/pyproject.toml') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      - run: <INSTALL_CMD>
      - run: <TEST_CMD>
```

Replace `<VERSIONS>` with the detected versions, `<INSTALL_CMD>` with the
detected install command, `<TEST_CMD>` with the detected test command.

If only one version was detected, omit the `strategy` block entirely (no
matrix for a single version).

#### Template: Node.js

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [<VERSIONS>]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: '<LOCKFILE_TYPE>'
      - run: <INSTALL_CMD>
      - run: <TEST_CMD>
```

Replace `<LOCKFILE_TYPE>` with `npm`, `yarn`, or `pnpm` depending on detected
lockfile. Omit the `cache` line if no lockfile was detected.

If a lint command was detected, add before the test step:

```yaml
      - run: <LINT_CMD>
```

If only one version was detected, omit the `strategy` block entirely.

#### Template: Go

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '<VERSION>'
      - run: go test ./...
```

#### Template: Rust

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions-rust-lang/setup-rust-toolchain@v1
        with:
          toolchain: <TOOLCHAIN>
      - run: cargo test
```

#### Template: Makefile

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: <TEST_CMD>
```

#### Template: Unknown (user-specified)

Use whichever template the user requested. If the user says "Python but with
conda" or "Java with Maven" — write a reasonable workflow for that. If you
don't know the conventions for that toolchain, say so and ask the user to
specify the steps.

---

### Step 4: Verify the output

After writing the file, verify:

```bash
# Check the file exists and is non-empty
test -s .github/workflows/test.yml && echo "EXISTS" || echo "MISSING"

# Validate YAML syntax (if yamllint is available)
yamllint .github/workflows/test.yml 2>/dev/null || \
  python3 -c "import yaml; yaml.safe_load(open('.github/workflows/test.yml')); print('VALID YAML')" 2>/dev/null || \
  echo "YAML_VALIDATION_SKIPPED (install yamllint or PyYAML)"

# Show the final result
cat .github/workflows/test.yml
```

If validation fails, fix the issue and re-verify. Don't ship invalid YAML.

---

### Step 5: Report

Report to the user what was created:

- **Detected project type:** what was found
- **Workflow file:** `.github/workflows/test.yml`
- **Test command:** what was configured
- **Version matrix:** which versions (if any)
- **Actions used:** list of `uses:` references (so they can audit)

## When to Invoke

Use this skill when:

- Setting up a new repo from scratch
- A repo has no `.github/workflows/` directory
- An existing workflow is broken or outdated and needs replacement
- The user asks "set up CI" or "add testing workflow" or similar