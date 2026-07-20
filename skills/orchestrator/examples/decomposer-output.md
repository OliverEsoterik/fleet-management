# Decomposer Output Example

When the decomposer finishes, it writes the following to `work/graph/state.json`. This is the input the chain-planner reads.

## Fields written

- `decomposition.tasks` — list of tasks broken from the request
- `decomposition.source` — `"skill-match"` or `"generic"`
- `skill_index` — all discovered skills with metadata
- `agent_index` — all discovered agents with metadata

## Example

```json
{
  "decomposition": {
    "tasks": [
      { "id": "task-1", "description": "analyze codebase", "node": "coder", "skills": ["architect"] },
      { "id": "task-2", "description": "research state of the art", "node": "coder", "skills": ["research"] }
    ],
    "source": "skill-match"
  },
  "skill_index": [
    {
      "name": "architect",
      "description": "Architectural design workflow...",
      "type": "graph",
      "nodes": ["analysis", "research", "adr-writer", "planner"],
      "produces": ["analysis", "adr", "plan"]
    },
    {
      "name": "code-review",
      "description": "Rigorous code review...",
      "type": "methodology",
      "nodes": [],
      "produces": ["review-report"]
    },
    {
      "name": "sre",
      "description": "Security audit...",
      "type": "methodology",
      "nodes": [],
      "produces": ["audit-report"]
    }
  ],
  "agent_index": [
    {
      "name": "gitops-expert",
      "description": "GitOps specialist for auditing ArgoCD/Flux...",
      "skills": ["sre", "code-review"],
      "model": "haiku",
      "tools": ["Read", "Write", "Bash", "Grep", "WebSearch"]
    }
  ],
  "routing": {
    "last_node": "decomposer",
    "next_node": "chain-planner",
    "reason": "decomposition complete"
  }
}
```
