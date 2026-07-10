# Fleet Extension — Implementation Plan

## Goal

Create a pi extension that wraps the `invoke-fleet` skill's shell scripts into a custom tool (`fleet_delegate`) and slash command (`/fleet`) so the agent can orchestrate the multi-agent fleet workflow without reconstructing bash commands from markdown blocks.

## Motivation

The `invoke-fleet` skill ships four bash scripts (`delegate.sh`, `orchestrate.sh`, `collect.sh`, `cleanup.sh`). Currently the agent must `bash tools/delegate.sh ...` via the bash tool, which works but is fragile — paths must be constructed manually, error handling is limited, and output parsing is ad-hoc. A custom tool gives structured input/output, proper error reporting, and a cleaner UX.

## Design

### Location

`/home/oliver/agent-helpers/.pi/extensions/fleet.ts`

The extension resolves its `tools/` directory relative to itself using `import.meta.url` (same pattern as superpowers.ts), deriving: `resolve(extDir, "../skills/invoke-fleet/tools")`.

### Component 1: `fleet_delegate` Custom Tool

```typescript
pi.registerTool({
  name: "fleet_delegate",
  label: "Fleet Delegate",
  description: "Launch, orchestrate, collect, or clean up a multi-agent fleet workflow",
  parameters: Type.Object({
    action: Type.Enum({
      deploy: "deploy",
      orchestrate: "orchestrate",
      collect: "collect",
      cleanup: "cleanup",
    }, { description: "Which fleet action to perform" }),
    project_dir: Type.String({ description: "Absolute path to the project directory" }),
    agent_name: Type.Optional(Type.String({ description: "Agent name (required for deploy, orchestrate)" })),
    task: Type.Optional(Type.String({ description: "Task description (required for deploy)" })),
    max_depth: Type.Optional(Type.Integer({ description: "Max orchestration loop depth (default 5)", default: 5 })),
    session_name: Type.Optional(Type.String({ description: "Tmux session name (required for collect)" })),
  }),
  async execute(toolCallId, params, signal, onUpdate, ctx) {
    // Route to the appropriate script based on params.action
    // Run via child_process.execFile
    // Capture stdout/stderr
    // Return structured result with output, session name, success/failure
  },
});
```

### Component 2: `/fleet` Slash Command

```typescript
pi.registerCommand("fleet", {
  description: "Manage fleet workflows: deploy, orchestrate, collect, cleanup",
  handler: async (args, ctx) => {
    // Parse args: /fleet deploy <agent> "<task>"
    //                /fleet orchestrate <agent> [depth]
    //                /fleet collect <session>
    //                /fleet cleanup
    // Validate, run the appropriate script, notify result
  },
});
```

### Script Resolution

```typescript
const extDir = dirname(fileURLToPath(import.meta.url));
const toolsDir = resolve(extDir, "../skills/invoke-fleet/tools");
```

Scripts are invoked via `child_process.execFile()` for proper signal handling (respects abort signal from `ctx.signal`).

### Key Behaviors

- **Tool execution respects abort signal** — Esc during a long orchestrate loop cancels the subprocess
- **Structured output** — tool returns `{ content: [captured output], details: { session, action, exitCode } }`
- **Error handling** — script not found, non-zero exit, missing params all produce clear error messages
- **Session tracking** — the tool remembers the last deployed session name in memory so orchestrate/collect can default to it

## Files to Create

| File | Purpose |
|------|---------|
| `.pi/extensions/fleet.ts` | Extension entry point (default export factory) |

No changes to existing files. The skill's `tools/` directory and scripts remain exactly as-is.

## Verification

1. `pi -e .pi/extensions/fleet.ts` — extension loads without errors
2. `/fleet` — shows usage help
3. Agent calls `fleet_delegate({ action: "deploy", project_dir: "...", agent_name: "code-reviewer", task: "test" })` — tmux session created, output returned
4. Agent calls `fleet_delegate({ action: "orchestrate", ... })` — polling loop runs, consultant routing works
5. Agent calls `fleet_delegate({ action: "cleanup", ... })` — work/ artifacts removed

## Future Considerations

- **Multi-project support** — currently scoped to one project per invocation; a future version could track a project registry
- **Fleet status command** — `/fleet status` could list all running fleet tmux sessions
- **Auto-cleanup on session end** — hook into `session_shutdown` to clean up stale work/ artifacts