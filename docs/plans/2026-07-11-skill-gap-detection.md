# Skill Gap Detection — Post-Run Harvesting

**Date:** 2026-07-11  
**Status:** Draft  
**Author:** pi

## Goal

Give the orchestrator a lightweight mechanism to detect when a sub-agent would have benefited from a domain-specific skill that doesn't exist yet, surface that to the human, and optionally create the skill.

No automated quality judgments. No file-extension scanning. No guesses about "better."

## Motivation

The orchestrator launches sub-agents with role descriptions and any matching skills from `skills/`. When no skill matches a domain (Terraform, Kubernetes, a bespoke framework), the sub-agent works from general knowledge. It often spends significant turns on research and methodology discovery that a skill would have provided upfront.

The orchestrator cannot evaluate "would this output be better with a skill?" — it has no baseline. But it *can* surface the raw signals that let a human make that call.

## Architecture

One new section appended to the orchestrator's final consolidation output. No new phases, no new sub-agents, no automated skill creation.

```
┌──────────────────────────────────────────┐
│  Orchestrator consolidates sub-agent     │
│  results, presents to user               │
├──────────────────────────────────────────┤
│  Appends "Skill Gaps" section:           │
│  - Per sub-agent: role, turns, files,    │
│    existing skills used, research cost   │
│  - Recommendations: skills to consider   │
│  - Action: "Create one? (y/n)"            │
├──────────────────────────────────────────┤
│  User says "y" → launch skill-writer     │
│  sub-agent with sub-agent output as      │
│  source material                         │
└──────────────────────────────────────────┘
```

## Orchestrator Changes

### What to log per sub-agent launch

The orchestrator already builds the sub-agent prompt. It has all this information at hand. It needs to record it:

| Field | Source | Example |
|-------|--------|---------|
| Role description | From delegation plan or decomposition | "Review Terraform configs for security issues" |
| Domain(s) extracted | Inferred from the task description | `terraform`, `infrastructure` |
| Skills injected | The `Skills` array from the delegation plan | `["sre"]` |
| Turns taken | Returned in sub-agent result | 14 |
| Research overhead | Estimated from sub-agent output (patterns like "first, let me look up common X issues", "typical problems in Y include...") | "~6 turns spent on general research" |
| Files touched | From sub-agent result | `main.tf`, `variables.tf`, `outputs.tf` |
| Output length | From sub-agent result | ~200 lines |

### Where to log

The orchestrator already reads sub-agent outputs from `work/<agent>/<report>.md`. Add a sidecar file `work/meta/<agent-name>.json` written by the orchestrator at launch time with the metadata it knows (role, domain, skills injected). After the sub-agent finishes, the orchestrator annotates it with turns and files touched.

### How to present

In the orchestrator's final consolidation output, after the main results, append:

```
## Skill Gaps

This run used 3 sub-agents:

| Agent | Domain | Turns | Research overhead | Skill used? |
|-------|--------|-------|-------------------|-------------|
| security-auditor | general security | 8 | ~2 turns | sre |
| test-auditor | testing | 6 | ~1 turn | — |
| terraform-reviewer | terraform | 14 | ~6 turns | **none** |
| docker-reviewer | docker | 7 | ~2 turns | docker-expert |

**Recommendation:** terraform-reviewer spent 6 of 14 turns on research that a `skills/terraform/SKILL.md` could provide upfront.
If you expect more Terraform work, consider creating one.

Create skill for terraform? (y/n)
```

This is the **only decision point**. The orchestrator does not create anything automatically. It surfaces the signal and asks.

### Thresholds for surfacing a recommendation

Don't recommend for every agent. Only flag when:

1. **No skill was available** for the agent's domain (trivially known from the launch-time `Skills` array)
2. **Research overhead is ≥ 30% of total turns** (proxy for "the sub-agent spent significant effort on discovery rather than execution")
3. The agent touched ≥ 2 files in that domain (not a one-line drive-by)

These thresholds are conservative. They filter out sub-agents that breezed through without needing deeper methodology.

## Human-Facing Actions

### If user says "y"

The orchestrator delegates to `skills/create-skill/SKILL.md`. If that file has a `## Delegation` section, the orchestrator executes it as a multi-phase workflow (see "Converting create-skill" below).

If the delegation fails or the file hasn't been updated yet, fall back to launching a single skill-writer sub-agent with the sub-agent's output and domain name.

### If user says "n"

Nothing happens. The signal is discarded. The next run will surface it again if the thresholds are met.

## Converting create-skill

`skills/create-skill/SKILL.md` is currently a **methodology skill** — the orchestrator reads its content and passes it as instructions to a single sub-agent. It should become a **delegation skill** — the orchestrator reads its `## Delegation` section and executes it as a multi-phase workflow.

This is the core change that enables researched skills. The orchestrator does not need new code — it already supports both methodology and delegation skills. The change is just in `create-skill/SKILL.md` itself.

### New create-skill structure

```yaml
---
name: create-skill
description: >
  Research the domain from academic + web sources, then synthesize findings
  into a reusable skill file. Two-phase delegation: research then write.
---

## Delegation

Phase 1 — Research (parallel):
  - Agent: domain-researcher
    Role: You are a research specialist. Given a domain name and a sub-agent's
    work output, gather current knowledge to inform a new skill. Use
    academic_search (arXiv, Semantic Scholar, PubMed) and WebSearch to find:
    - Academic papers, established methodologies, canonical references
    - Industry best practices, common pitfalls, anti-patterns
    - Tool-specific documentation references, version-specific notes
    - Community standards, conventions, style guides
    Write all findings to work/research/<domain>/findings.md, organized by
    source type with citations where available.
    Skills: []
    Output: work/research/<domain>/findings.md

Phase 2 — Write (after Phase 1):
  - Agent: skill-writer
    Role: You are a technical writer specializing in skill creation. Read the
    research findings from work/research/<domain>/findings.md and the original
    sub-agent's output. Create a reusable skill at skills/<domain>/SKILL.md
    that captures both the authoritative methodology from research and the
    concrete, project-specific patterns from the sub-agent's work.
    Follow the skill format rules defined later in this file.
    Skills: []
    Output: skills/<domain>/SKILL.md
```

### Degradation path

If `academic_search` or `WebSearch` are unavailable (offline, restricted environment), the domain-researcher reports "no research sources available" in `findings.md`. The skill-writer proceeds with only the sub-agent's output.

If `skills/create-skill/SKILL.md` does not yet have a `## Delegation` section (pre-migration), the orchestrator falls back to launching a single skill-writer sub-agent — the current behavior.

### Research output format

`work/research/<domain>/findings.md` should be structured as:

```markdown
# Research: <domain>

## Academic Sources
- Paper: "Title" (year) — key insight

## Industry Best Practices
- Source: URL — key practice

## Common Pitfalls
- Issue: description — mitigation

## Tool-Specific References
- Tool: version — relevant documentation links

## Synthesis
- Top 3-5 principles the skill should encode
- Recommended methodology references
```

### Skill quality improvement

Without research: the skill captures only what the single sub-agent did on one run. It's a post-hoc capture of one session's approach.

With research: the skill captures established methodology for the domain, informed by academic literature and industry practice. The sub-agent's output provides the concrete, project-specific patterns. The result is a skill that is both authoritative and grounded in the actual codebase.

This directly addresses the original concern: the sub-agent worked generically because no Terraform (or similar) skill existed. Now when we create that skill, it's informed by actual Terraform research — not just one sub-agent's best guess.

## Files to Modify

| File | Change |
|------|--------|
| `skills/orchestrator/SKILL.md` | Add logging section (what to record per sub-agent launch). Add "Skill Gaps" section to consolidation output. Add action prompt. |
| `skills/create-skill/SKILL.md` | Convert from methodology skill to delegation skill. Add `## Delegation` with Research + Write phases. Add `academic_search` and `WebSearch` to researcher's tools. Keep format rules as inline reference. |

## Files to Create

None. All changes are to existing files.

## Edge Cases

### What if multiple sub-agents worked on the same domain?

Group them into one recommendation. "terraform-reviewer and terraform-tester both worked on Terraform (20 combined turns, 8 research). One skill covers both."

### What if the sub-agent's output is too sparse to extract a methodology?

The skill-writer sub-agent will produce a short, low-value skill, or it can report back "not enough signal to create a skill." Filter at creation time, not detection time.

### What if the user always says "n"?

Then nothing changes. The system doesn't degrade. The only cost is a few lines in the output. If the user consistently declines, they see the recommendation less often because the research-overhead threshold filters out agents working in familiar territory.

### What if no sub-agent hits the threshold?

No "Skill Gaps" section is shown. No noise.

## Future-Proofing

If this pattern proves useful, later additions could include:

- **Cross-run aggregation:** Track gap signals across runs in a JSON file. If `terraform` is flagged 3 times across separate runs and the human never created a skill, escalate to a stronger prompt.
- **Semi-automated creation:** After N flags with no action, auto-create a draft skill and file it in `work/harvest/` for review instead of asking.
- **Quality scoring:** After a skill is created and used, compare subsequent sub-agent turns/research overhead against pre-skill baseline. Use the delta as feedback.

But none of that is in scope for this plan. The first step is just: **surface the signal, let the human decide.**

## Verification

1. Orchestrator completes a run with a sub-agent that had no matching skill
2. Consolidation output includes "Skill Gaps" section with that agent
3. Recommendation threshold logic is correct (filters out agents with skill, or low research overhead)
4. User says "y" → orchestrator checks `skills/create-skill/SKILL.md`, finds `## Delegation`, executes it
5. Phase 1: domain-researcher launches and produces `work/research/<domain>/findings.md` with academic + web sources
6. Phase 2: skill-writer launches and produces `skills/<domain>/SKILL.md`
7. The new SKILL.md references established methodology from research, not just the single sub-agent's output
8. User says "n" → no side effects
9. Degradation: if no research tools available, researcher reports "no sources" and writer proceeds with sub-agent output only
10. Next run with the same domain: the new skill appears in the orchestrator's discovery phase