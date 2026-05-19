---
icon: flag-checkered
---

# Getting Started

Welcome to GL Smart Search! This guide will help you get started with web search in minutes.

## Prerequisites

Before you begin, make sure you have completed the [Prerequisites](prerequisites.md) guide — specifically:

* Python 3.11 or 3.12 installed
* GL Smart Search SDK installed (`pip install smart-search-sdk`)
* GL Smart Search credentials (Base URL and Token)

> 💡 **Tip:** If you haven't set up your credentials yet, follow the instructions in the [Prerequisites](prerequisites.md) guide to get your GL Smart Search Token.

***

## Your First Web Search

Choose one of the integration methods below to get started:

### SDK (Python)

**Ideal for:** Python developers who want a high-level interface with built-in error handling and type safety.

#### Step 1: Install the SDK

If you haven't already, install the GL Smart Search SDK:

```bash
pip install smart-search-sdk
```

#### Step 2: Set Environment Variables

Configure your GL Smart Search credentials:

```bash
export SMARTSEARCH_BASE_URL="https://search.glair.ai/"
export SMARTSEARCH_TOKEN="your-access-token"
```

> 💡 **Tip:** Get your GL Smart Search Token from the [Prerequisites](prerequisites.md) guide.

#### Step 3: Perform a Web Search

Create a Python script and run your first search:

```python
import asyncio
import os
from smart_search_sdk.web.client import WebSearchClient
from smart_search_sdk.web.models import GetWebSearchResultsRequest

async def main():
    client = WebSearchClient(base_url=os.getenv("SMARTSEARCH_BASE_URL"))
    await client.authenticate(token=os.getenv("SMARTSEARCH_TOKEN"))
    result = await client.search_web(GetWebSearchResultsRequest(query="gdp labs", size=5))
    print(result)

asyncio.run(main())
```

> 📚 **Next Steps:** Learn more about the [GL Smart Search SDK](guides/sdk/) for advanced usage.

***

### MCP

**Ideal for:** Agentic systems, AI assistants, and MCP-compatible tools that need modular search capabilities.

Integrate GL Smart Search into any MCP-compatible system (Cursor, Windsurf, VS Code, etc.) for agent-based workflows.

#### Step 1: Configure Your Client

Add GL Smart Search MCP to your MCP client configuration. For example, in **Cursor**:

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

#### Step 2: Verify It Works

1. Restart your client if needed (some clients require this to pick up configuration changes)
2. Check available tools — Your client should list the available tools from GL Smart Search MCP
3. Test a query — Try sending a message in your client with a query like:

```
Search the web for information about Python async programming
```

> 📚 **Next Steps:** See the [GL Smart Search MCP](guides/mcp.md) guide for detailed setup instructions for all supported clients and available tools.

***

### CLI

**Ideal for:** Quick searches and testing directly from your terminal without writing code.

#### Step 1: Install the SDK

If you haven't already, install the GL Smart Search SDK:

```bash
pip install smart-search-sdk
```

#### Step 2: Set Environment Variables

Configure your GL Smart Search credentials:

```bash
export SMARTSEARCH_BASE_URL="https://search.glair.ai/"
export SMARTSEARCH_TOKEN="your-access-token"
```

#### Step 3: Run Your First Search

Use the CLI to perform a web search:

```bash
smart-search web search --query "gdp labs" --size 5
```

> 📚 **Next Steps:** Learn more about [CLI commands](guides/cli/) for web search and connector operations.

***

## Next Steps

Now that you've completed your first search, explore more capabilities:

* [**SDK Guide**](guides/sdk/) – Learn advanced GL Smart Search SDK features for web search and connectors
* [**MCP Guide**](guides/mcp.md) – Set up GL Smart Search MCP integration for agentic workflows
* [**CLI Guide**](guides/cli/) – Master command-line operations
* [**Resources**](resources/) – Access authentication guides
