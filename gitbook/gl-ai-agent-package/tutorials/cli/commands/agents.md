---
icon: user-robot-xmarks
---

Use CLI agents commands to iterate and validate behavior without writing SDK scripts.

*Use when:* You want quick create/run/export loops during agent development.

## Placeholders

- `<AGENT_REF>`: agent ID or unique name.
- `<EXPORT_FILE>`: output file path, for example `agent.yaml`.

## List and Inspect

```bash
aip agents list
aip agents get <AGENT_REF>
```

## Create and Run

```bash
aip agents create --name "hello-cli" --instruction "You are a friendly assistant."
aip agents run <AGENT_REF> "Hello"
```

Save transcript:

```bash
aip agents run <AGENT_REF> "Hello" --save run.md
```

## Export and Import (Promotion Loop)

```bash
aip agents get <AGENT_REF> --export <EXPORT_FILE>
aip agents create --import <EXPORT_FILE> --name "hello-cli-prod"
```

Update existing agent from file:

```bash
aip agents update <AGENT_REF> --import <EXPORT_FILE>
```

## Common Capability Updates

```bash
aip agents update <AGENT_REF> --tools <TOOL_REF>
aip agents update <AGENT_REF> --mcps <MCP_REF>
```
