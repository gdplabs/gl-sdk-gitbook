---
icon: terminal
---

Use AIP CLI as the utility layer for agent development after you finish conceptual design in Guides.

## When to Use CLI

- Validate access and environment health before coding: `aip status`.
- Operate resources without writing scripts: list, inspect, create, update.
- Run and debug agents interactively with rich streaming output.
- Export/import agents, tools, and MCPs for promotion workflows.

## Placeholder Legend

- `<ACCOUNT_NAME>`: Named CLI account profile (for example `prod`, `staging`).
- `<AGENT_REF>`: Agent ID or unique agent name.
- `<TOOL_REF>`: Tool ID or unique tool name.
- `<MCP_REF>`: MCP ID or unique MCP name.
- `<RUN_ID>`: Run ID from transcript or history views.
- `<EXPORT_FILE>`: Output file path, for example `agent.yaml`.

## CLI Learning Path

1. Start with the [Lifecycle tutorial](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/lifecycle).
2. Continue with [Use cases](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/use-cases).
3. Learn core commands in [Accounts](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/accounts), [Status](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/status), and [Agents](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/agents).
4. Add capabilities with [Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/tools), [MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/mcps), and [Models](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/models).
5. Capture output using [Runs and Transcripts](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/runs-and-transcripts).
6. Promote config safely with [MCP export/import workflow](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/workflows/mcp-export-import).

## Interactive UX

- Open the palette with `aip` and use `/accounts`, `/agents`, `/status`, and `/transcripts`.
- After selecting an agent via `/agents`, use `/runs` and `/schedules` for remote debugging and automation.
- Workflow guide: [Slash palette](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/interactive/slash-palette).

## Command Reference

- Detailed flags and options: [CLI Commands Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands).
- Legacy config format: [CLI Legacy Config](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-legacy-config).
