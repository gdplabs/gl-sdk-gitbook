---
icon: lines-leaning
---

# MCP Clients

Client-specific setup instructions for connecting to GL Connector MCP servers. This page covers the most common MCP clients — for a comprehensive list of all MCP-compatible clients, see:

{% embed url="https://modelcontextprotocol.io/clients" %}

{% embed url="https://modelcontextprotocol.info/docs/clients/" %}

{% hint style="info" %}
**New to GL Connector MCP?** Start with the [quickstart.md](quickstart.md "mention") for a fast setup using token-based auth, or the [in-depth-guide.md](in-depth-guide.md "mention") for OAuth 2.1 and other setup information.
{% endhint %}

***

## Client Comparison Matrix

We have tested the following clients. For more clients, see the external references above.

<table data-full-width="true"><thead><tr><th>Client</th><th>Transport</th><th>Token-based Auth</th><th>OAuth 2.1 (Native)</th><th>OAuth 2.1 (mcp-remote)</th><th>Requires Node.js</th><th>Notable Quirks</th></tr></thead><tbody><tr><td><strong>VSCode</strong></td><td>Streamable HTTP</td><td>✅</td><td>⚠️ Unreliable</td><td>✅ Stable</td><td>Only for mcp-remote</td><td>—</td></tr><tr><td><strong>Cursor</strong></td><td>Streamable HTTP</td><td>✅</td><td>❌ No auto-browser</td><td>✅ Stable</td><td>Only for mcp-remote</td><td>Does not open browser for OAuth; must use mcp-remote</td></tr><tr><td><strong>Windsurf</strong></td><td>Streamable HTTP</td><td>✅</td><td>⚠️ Unreliable</td><td>✅ Stable</td><td>Only for mcp-remote</td><td>Uses <code>serverUrl</code> instead of <code>url</code> in config</td></tr><tr><td><strong>Claude Desktop</strong></td><td>STDIO only</td><td>✅ Via mcp-remote</td><td>❌ N/A</td><td>✅ Stable</td><td>Always</td><td>STDIO-only; all connections require mcp-remote. Restart required after config changes</td></tr><tr><td><strong>Claude Web</strong></td><td>Streamable HTTP</td><td>✅</td><td>⚠️ Inconsistent</td><td>N/A</td><td>N/A</td><td>Sometimes works, sometimes doesn't, even on Official MCP Servers.</td></tr><tr><td><strong>ChatGPT Web</strong></td><td>Streamable HTTP</td><td>✅</td><td>⚠️ Inconsistent</td><td>N/A</td><td>N/A</td><td>Requires Plus or higher; Business requires admin access. Still inconsistent.</td></tr><tr><td><strong>Google Antigravity</strong></td><td>STDIO only</td><td>✅ Via mcp-remote</td><td>❌ N/A</td><td>✅ Stable</td><td>Always</td><td>Requires mcp-remote</td></tr><tr><td><strong>Kiro</strong></td><td>STDIO only</td><td>✅ Via mcp-remote</td><td>❌ N/A</td><td>✅ Stable</td><td>Always</td><td>Requires mcp-remote</td></tr><tr><td><strong>Headless / CI</strong></td><td>Varies</td><td>✅</td><td>❌ Not possible</td><td>❌ Not possible</td><td>—</td><td>No browser available; token-based auth only</td></tr></tbody></table>

**Legend:** ✅ Works — ⚠️ Works sometimes / unreliable — ❌ Does not work or not applicable

{% hint style="info" %}
**Key takeaway:** Token-based auth works everywhere. Native OAuth 2.1 is unreliable across the board — even clients that support it (VSCode, Windsurf) frequently fail with certain servers. **`mcp-remote` is the most reliable way to use OAuth today**, but it requires Node.js (v20+) and NPM. See the [in-depth-guide.md](in-depth-guide.md "mention") for why this is the case.
{% endhint %}

***

## Headers Reference

All token-based configurations use the same headers. Replace the placeholder values with your actual [credentials.md](../api/credentials.md "mention") (obtained via the [connectors-console.md](../api/tools-and-interfaces/connectors-console.md "mention") or other sources).

| Header          | Required | Description                                                     |
| --------------- | -------- | --------------------------------------------------------------- |
| `Authorization` | Yes      | Your User Token, prefixed with `Bearer` (e.g., `Bearer eyJ...`) |
| `X-Integration` | No       | Target a specific integration when you have multiple            |

{% hint style="warning" %}
**Important:** Do not omit the `Bearer` prefix. `Authorization: eyJ...` will fail — it must be `Authorization: Bearer eyJ...`.
{% endhint %}

***

## About mcp-remote

Several clients below reference [`mcp-remote`](https://www.npmjs.com/package/mcp-remote) — a bridge that enables STDIO-only clients to connect to Streamable HTTP MCP servers, and also handles the OAuth 2.1 browser flow externally.

**When to use it:**

* Your client only supports STDIO (e.g., Claude Desktop, Kiro)
* Native OAuth 2.1 fails in your client (which is common)
* You want the most reliable OAuth experience available today

**Requirements:** Node.js (v20+) and NPM must be installed. The command runs via `npx`.

***

## VSCode

VSCode has native support for Streamable HTTP MCP servers.

**Config location:** Command palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) → `MCP: Open User Configuration` → edit `mcp.json`.

### Token-based

```json
{
  "mcp": {
    "servers": {
      "gmail": {
        "type": "http",
        "url": "https://connectors.gdplabs.id/google_mail/mcp",
        "headers": {
          "Authorization": "Bearer eyJ..."
        }
      }
    }
  }
}
```

### OAuth 2.1

Native OAuth may work but is unreliable. Try native first, fall back to mcp-remote.

#### **Native**

```json
{
  "mcp": {
    "servers": {
      "gmail": {
        "type": "http",
        "url": "https://connectors.gdplabs.id/google_mail/mcp"
      }
    }
  }
}
```

#### **Via mcp-remote (recommended fallback)**

```json
{
  "mcp": {
    "servers": {
      "gmail": {
        "type": "stdio",
        "command": "npx",
        "args": ["-y", "mcp-remote", "https://connectors.gdplabs.id/google_mail/mcp"]
      }
    }
  }
}
```

***

### Cursor

Cursor supports Streamable HTTP natively for token-based auth. For OAuth, it does not open the browser automatically — use `mcp-remote`.

**Config location:** `File` → `Preferences` → `Cursor Settings` → `Tools & MCP` → `New MCP Server`.

#### Token-based

```json
{
  "mcpServers": {
    "gmail": {
      "url": "https://connectors.gdplabs.id/google_mail/mcp",
      "headers": {
        "Authorization": "Bearer eyJ..."
      }
    }
  }
}
```

#### OAuth 2.1 (via mcp-remote)

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://connectors.gdplabs.id/google_mail/mcp"]
    }
  }
}
```

***

### Windsurf

Windsurf has native support for both Streamable HTTP and OAuth 2.1, though OAuth may not work reliably with all servers.

**Config location:** `File` → `Preferences` → `Windsurf Settings` → `Cascade` → `Open MCP Marketplace` → click the gear icon.

#### Token-based

```json
{
  "mcpServers": {
    "gmail": {
      "serverUrl": "https://connectors.gdplabs.id/google_mail/mcp",
      "headers": {
        "Authorization": "Bearer eyJ..."
      }
    }
  }
}
```

#### OAuth 2.1

**Native:**

```json
{
  "mcpServers": {
    "gmail": {
      "serverUrl": "https://connectors.gdplabs.id/google_mail/mcp"
    }
  }
}
```

**Via mcp-remote (recommended fallback):**

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://connectors.gdplabs.id/google_mail/mcp"]
    }
  }
}
```

***

### Claude Desktop

Claude Desktop only supports STDIO-based MCP servers. All connections require `mcp-remote` and therefore Node.js.

**Config location:** `Settings` → `Developer` → `Edit Config` → edit `claude_desktop_config.json`. Restart Claude Desktop after saving.

#### Token-based

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://connectors.gdplabs.id/google_mail/mcp",
        "--header",
        "Authorization: Bearer eyJ..."
      ]
    }
  }
}
```

To target a specific integration, add additional `--header` arguments:

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://connectors.gdplabs.id/google_mail/mcp",
        "--header",
        "Authorization: Bearer eyJ...",
        "--header",
        "X-Integration: user..."
      ]
    }
  }
}
```

#### OAuth 2.1 (via mcp-remote)

```json
{
  "mcpServers": {
    "gmail": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://connectors.gdplabs.id/google_mail/mcp"]
    }
  }
}
```

After saving and restarting Claude Desktop, `mcp-remote` will open your browser to complete the OAuth authorization flow.

***

### Programmatic Usage

You can connect to GL Connector MCP servers programmatically using our in-house [mcp-client.md](../../../common-modules/tutorials/tools/mcp-client.md "mention"). See the [connector-mcp-cookbook.md](connector-mcp-cookbook.md "mention") for examples and advanced patterns.

***

### Tips

* **Trailing slash:** If your client cannot connect, try adding a trailing slash to the MCP URL (e.g., `https://connectors.gdplabs.id/google_mail/mcp/`).
* **Available connectors:** Swap the URL path to connect to different services. See the full list at [https://connectors.glair.ai/mcps/list](https://connectors.glair.ai/mcps/list)
* **OAuth not working?** This is expected. Try `mcp-remote` first, then fall back to token-based auth. See the [in-depth-guide.md](in-depth-guide.md "mention").
* **Restart your client** after editing MCP configuration. Most clients require this to pick up changes.
