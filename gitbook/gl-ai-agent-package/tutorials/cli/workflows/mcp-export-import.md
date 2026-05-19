---
icon: arrow-progress
---

Use this workflow to safely move MCP configurations between environments.

*Use when:* You promote MCP setup from dev/staging to production and need secret-safe exports.

## Placeholders

- `<MCP_REF>`: MCP ID or unique MCP name.
- `<EXPORT_FILE>`: export path, for example `mcp.yaml`.
- `<AUTH_PLACEHOLDER>`: placeholder text such as `${MCP_AUTH_TOKEN}`.
- `<TARGET_ACCOUNT_NAME>`: destination CLI account profile.

## Basic Export

```bash
aip mcps get <MCP_REF> --export <EXPORT_FILE>
```

Format is inferred from extension (`.json`, `.yaml`, `.yml`).

## Non-Interactive Export (CI/CD)

```bash
aip mcps get <MCP_REF> \
  --export <EXPORT_FILE> \
  --no-auth-prompt \
  --auth-placeholder "<AUTH_PLACEHOLDER>"
```

Use this mode for automation to avoid prompt hangs.

## Import to Target Environment

```bash
aip accounts use <TARGET_ACCOUNT_NAME>
aip mcps create --import <EXPORT_FILE>
```

## Security Rules

- Never commit real secrets to git.
- Prefer `--no-auth-prompt` for exported files destined for repositories.
- Inject secrets at deploy/runtime via secret manager or environment variables.

## Related Pages

- [CLI MCP commands](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/mcps)
- [MCP schema reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/schemas/mcps)
- [REST API MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/mcps)
