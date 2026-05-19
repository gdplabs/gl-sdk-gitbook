---
icon: filter-circle-dollar
---

# MCP Tool Filtration

An MCP server can expose dozens of tools at once. Feeding all of them into an agent wastes tokens, confuses the model, and risks unintended actions. Filtering lets you pick only the tools your agent actually needs.

The MCP specification (as of 2025-11-25) does not define any standard for server-side tool filtering or middleware. A proposal exists ([SEP-1300](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1300)), but it has not been adopted. Some servers may offer their own filtering (e.g. via query parameters), but this is non-standard and not something you can rely on. **Client-side filtering is the only approach that works universally.**

For our example, we will be using our own in-house [mcp-client.md](../../../../common-modules/tutorials/tools/mcp-client.md "mention") and [aip](https://app.gitbook.com/o/l7iZNPfPGNFLFlscNeoe/s/LqsWGI0JUnaas9v07yZ5/ "mention") (GLAIP SDK Local Agents), however this approach **will** work on any other MCP Clients!

## Example: Handling Github Tools

### Installation

```shellscript
uv init --bare
uv add glaip-sdk[local] gllm-tools-binary
```

### Source Code

{% code title="main.py" lineNumbers="true" %}
```python
import asyncio
import os

from glaip_sdk import Agent
from gllm_tools.mcp.client.langchain import LangchainMCPClient

DESIRED_TOOLS = {"github_list_issues"}

client = LangchainMCPClient({
    "github": {
        "url": "https://connectors.gdplabs.id/github/mcp",
        "headers": {"Authorization": f"Bearer {os.getenv('GL_CONNECTORS_USER_TOKEN')}"},
    }
})


async def main():
    all_tools = await client.get_tools("github")
    tools = [t for t in all_tools if t.name in DESIRED_TOOLS]

    agent = Agent(
        name="github_agent",
        instruction="You are a helpful assistant.",
        tools=tools,
    )

    async for chunk in agent.arun("Tell me about the latest issue in gdp-admin/gl-connectors-sdk."):
        if isinstance(chunk, str):
            print(chunk)


asyncio.run(main())
```
{% endcode %}

The key part is two lines:

```python
all_tools = await client.get_tools("github")
tools = [t for t in all_tools if t.name in DESIRED_TOOLS]
```

`get_tools()` returns everything the server advertises. From there, you filter using a regular list comprehension before passing the result to your agent.

### Executing the Code

Simply run:

```
uv run main.py
```

And you will get AIP Agent to execute with the appropriate response.

## Filtering Strategies

### Allow-list (recommended)

Define a set of tool names you want and keep only those. Using a `set` gives O(1) lookups and makes intent clear.

```python
DESIRED_TOOLS = {"github_list_issues", "github_get_issue"}
tools = [t for t in all_tools if t.name in DESIRED_TOOLS]
```

### Deny-list

Sometimes it's easier to exclude a few tools rather than enumerate every one you need.

```python
EXCLUDED = {"github_delete_issue", "github_delete_repo"}
tools = [t for t in all_tools if t.name not in EXCLUDED]
```

{% hint style="warning" %}
**Note:** New tools added server-side will automatically slip through a deny-list. Prefer allow-lists when possible.
{% endhint %}

### Prefix or pattern matching

If you want all tools from a particular connector, filter by prefix:

```python
tools = [t for t in all_tools if t.name.startswith("github_")]
```

For more complex patterns:

```python
import re

pattern = re.compile(r"github_(list|get)_.*")
tools = [t for t in all_tools if pattern.match(t.name)]
```

## Discovering Available Tools

If you're not sure what a server exposes, print the list:

```python
all_tools = await client.get_tools("github")
for t in all_tools:
    print(f"{t.name}: {t.description}")
```

## Tips

* **Keep the allow-list as a module-level constant** so it's easy to find and update.
* **Prefer allow-lists over deny-lists** — new tools added server-side won't accidentally reach your agent.
* **Log which tools your agent received** during development to verify the filter works as expected.
