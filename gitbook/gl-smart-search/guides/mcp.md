---
icon: brain
---

# Model Context Protocol (MCP)

**GL Smart Search MCP** is the Model Context Protocol (MCP) integration layer for **GL Smart Search v2**.\
It provides a standardized HTTP-based interface that exposes GL Smart Search capabilities as modular tools.\
Each capability, such as web search or connector search, is wrapped as an independent MCP tool, making them composable and easily integrated into other MCP-compatible systems.

This modular design allows agent frameworks or services to call GL Smart Search functions directly through standardized MCP endpoints.

---

## Prerequisites

Before integrating GL Smart Search MCP, ensure you have:

- **GL Smart Search Token** — Required for authentication. Get your token by following the 👉 [**Authentication**](authentication.md) guide.
- **MCP-Compatible Client** — An MCP-compatible client that supports Streamable HTTP (e.g., Cursor, Windsurf, VS Code, Claude Desktop)

> 💡 **Tip:** If you haven't set up your GL Smart Search credentials yet, complete the [Prerequisites](../prerequisites.md) guide first.

---

## Quick Start

Get GL Smart Search MCP running in your client in under 5 minutes.

### Step 1: Configure Your Client

Add GL Smart Search MCP to your MCP client configuration. The configuration format varies by client:

#### For Cursor

1. Open Cursor Settings
2. Go to `Features` > `MCP Servers`
3. Click `+ Add new global MCP server`
4. Enter the following configuration:

```json
{
  "mcpServers": {
    "smart_search_mcp": {
      "url": "https://search.glair.ai/mcp/",
      "headers": {
        "Authorization": "Bearer <SMARTSEARCH_TOKEN>"
      }
    }
  }
}
```

Replace `<SMARTSEARCH_TOKEN>` with your GL Smart Search Token.

> ⚠️ **Important:** Do not omit the `Bearer` prefix. `Authorization: <token>` will fail — it must be `Authorization: Bearer <token>`.

#### For Windsurf

Add this to your `./.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "smart_search_mcp": {
      "url": "https://search.glair.ai/mcp/",
      "headers": {
        "Authorization": "Bearer <SMARTSEARCH_TOKEN>"
      }
    }
  }
}
```

#### For VS Code

1. Open VS Code Settings
2. Navigate to MCP Servers configuration
3. Add the GL Smart Search MCP server with:
   - **URL:** `https://search.glair.ai/mcp/`
   - **Authorization Header:** `Bearer <SMARTSEARCH_TOKEN>`

#### For Claude Desktop

Edit your Claude Desktop configuration file (location varies by OS):

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**Linux:** `~/.config/Claude/claude_desktop_config.json`

Add:

```json
{
  "mcpServers": {
    "smart_search_mcp": {
      "url": "https://search.glair.ai/mcp/",
      "headers": {
        "Authorization": "Bearer <SMARTSEARCH_TOKEN>"
      }
    }
  }
}
```

### Step 2: Verify It Works

1. **Restart your client** if needed (some clients require this to pick up configuration changes)
2. **Check available tools** — Your client should list the available tools from GL Smart Search MCP
3. **Test a query** — Try sending a message in your client with a query like:

```
Search the web for information about Python async programming
```

or

```
Find my emails about project updates
```

If the tools are listed and queries work, your integration is successful!

---

## Available Tools

GL Smart Search MCP provides the following tools:

### Web Search Tools

| Tool Name                | Description                                                                               |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| `get_web_search_results` | Retrieves search results with multiple result types (`snippets`, `keypoints`, `summary`). |
| `get_web_search_urls`    | Returns only the list of URLs based on a search query.                                    |
| `get_web_search_map`     | Maps a website to retrieve all URLs found on that site.                                   |
| `get_web_page`           | Fetches and processes the content of a given web page.                                    |
| `get_web_page_snippets`  | Extracts relevant snippets from a web page (`paragraph` or `sentence` style).             |
| `get_web_page_keypoints` | Summarizes a web page into key insights or takeaways.                                     |

### Connector Tools

| Tool Name | Description |
| --- | --- |
| `search_github` | Searches GitHub repositories, pull requests, and issues using GitHub Integration. |
| `search_google_calendar` | Searches calendar events using Google Calendar integration. |
| `search_google_drive` | Searches files and documents stored in Google Drive. |
| `search_google_mail` | Searches email messages from connected Gmail accounts. |
| `search_microsoft_outlook` | Searches email in Outlook and Microsoft 365 using natural language. |
| `search_microsoft_onedrive` | Searches files in Microsoft OneDrive and libraries you can access. |
| `search_microsoft_calendar` | Searches calendar events in Outlook and Microsoft 365. |

> 📝 **Note:** Connector tools require you to connect the respective services first. Use the [SDK](sdk/README.md) or [CLI](cli/README.md) to connect connectors before using them via MCP. Microsoft apps use the same connector names as in the [Connector Search](sdk/connector-search.md) guide (`microsoft_outlook`, `microsoft_onedrive`, `microsoft_calendar`).

---

## Transport and Endpoint

* **Transport Type:** HTTP (Streamable)
* **Server URL:** `https://search.glair.ai/mcp/`
* **Authentication:** Bearer Token (GL Smart Search Token)

---

## Authentication

GL Smart Search MCP uses **Bearer Token** authentication.\
The token used here is the same **GL Smart Search Token** generated through the **Authentication** process described in the 👉 [**Authentication**](authentication.md) guide.

This ensures consistent authorization across the SDK, CLI, and MCP environments.

---

## Troubleshooting

### Tools Not Appearing

- **Check your token** — Ensure your GL Smart Search Token is valid and correctly formatted with the `Bearer` prefix
- **Restart your client** — Some clients require a restart to pick up configuration changes
- **Verify URL** — Ensure the server URL is correct: `https://search.glair.ai/mcp/`

### Authentication Errors

- **Bearer prefix** — Make sure your Authorization header includes `Bearer` before the token
- **Token validity** — Verify your token hasn't expired and has the necessary permissions
- **Header format** — Ensure headers are properly formatted in JSON configuration

### Connector Tools Not Working

- **Connect first** — Connector tools require you to connect the respective services first using the [SDK](sdk/README.md) or [CLI](cli/README.md)
- **Check integration status** — Verify your connector integrations are active and properly configured

---

## Next Steps

- [**SDK Guide**](sdk/README.md) — Learn how to use GL Smart Search SDK for programmatic access
- [**CLI Guide**](cli/README.md) — Use GL Smart Search from your terminal
- [**Authentication**](authentication.md) — Learn how to get your authentication token
