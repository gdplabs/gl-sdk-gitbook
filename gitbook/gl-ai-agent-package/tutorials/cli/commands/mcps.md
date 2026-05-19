---
icon: mcp
---

MCP commands connect agents to external tool servers and support promotion workflows.

*Use when:* You need to register, test, and move MCP configs across environments.

## Placeholders

- `<MCP_REF>`: MCP ID or unique MCP name.
- `<EXPORT_FILE>`: output file path, for example `mcp.yaml`.

## List and Create

```bash
aip mcps list
aip mcps create --name "my-mcp" --transport http --url "https://example.com/mcp"
```

## Test Connection

```bash
aip mcps connect --url "https://example.com/mcp"
```

## Export and Import

```bash
aip mcps get <MCP_REF> --export <EXPORT_FILE>
aip mcps create --import <EXPORT_FILE>
```

For full secret-handling workflow, use [MCP export/import guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/workflows/mcp-export-import).
