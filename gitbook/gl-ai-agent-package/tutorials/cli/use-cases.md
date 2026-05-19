---
icon: list-checks
---

Use these workflows when you need CLI to support day-to-day agent development without writing custom scripts.

## 1) Validate Environment Before Coding

*Use when:* A teammate cannot run agents, or you just switched credentials.

```bash
aip accounts use <ACCOUNT_NAME>
aip status
```

Expected result: auth is valid, API is reachable, and resource checks return successfully.

## 2) Quickly Run an Existing Agent

*Use when:* You want to validate prompt behavior before changing SDK code.

```bash
aip agents list
aip agents run <AGENT_REF> "Summarize this requirement in 5 bullets"
```

Expected result: streamed output appears in terminal and final response is shown.

## 3) Capture a Transcript for Debugging

*Use when:* You need to share reproducible evidence with engineers or PMs.

```bash
aip agents run <AGENT_REF> "Investigate tool failure" --save run.md
/transcripts
```

Expected result: saved file path plus cached run history.

## 4) Promote MCP Configuration Across Environments

*Use when:* You move config from staging to production.

```bash
aip mcps get <MCP_REF> --export <EXPORT_FILE> --no-auth-prompt
# edit placeholders/secrets in <EXPORT_FILE>
aip mcps create --import <EXPORT_FILE>
```

Expected result: imported MCP appears in `aip mcps list` for target environment.

## 5) Update Agent Attachments (Tools/MCPs)

*Use when:* You need to test capability changes without redeploying app code.

```bash
aip agents update <AGENT_REF> --tools <TOOL_REF>
aip agents update <AGENT_REF> --mcps <MCP_REF>
```

Expected result: `aip agents get <AGENT_REF>` shows updated dependencies.

## 6) Run Interactive Ops from Palette

*Use when:* You prefer guided selection and quick discovery.

```bash
aip
```

Then use `/accounts`, `/agents`, or `/transcripts` (and inside an agent session: `/runs` and `/schedules`).

See [Slash palette guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-slash-palette) for details.
