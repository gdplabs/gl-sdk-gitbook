---
icon: mcp
---

# MCP Client

[`gllm-tools`](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-tools/gllm_tools/mcp/README.md) | **Tutorial:** Model Context Protocol

## Model Context Protocol (MCP) Integration

One of the primary tools in this library is the **MCP client**, which connects to Model Context Protocol servers. MCP is an open standard that defines how LLMs communicate with external data sources and services. Think of MCP as a universal adapter—it standardizes the way models request and receive information from various sources, whether that's databases, APIs, file systems, or specialized tools.

The relationship is straightforward: **Tools** are what LLMs use to interact with the world, and **MCP** is the protocol that standardizes how those interactions happen.

### Framework-Agnostic Design

A key advantage of this MCP client implementation is its **framework-agnostic architecture**. Unlike solutions tied to specific platforms, this tool provides direct connectivity to any MCP server and can be easily integrated into any agentic framework, including:

* **LangGraph** - For building stateful, multi-actor applications
* **Google ADK** - For Google's agent development toolkit
* **CrewAI** - For orchestrating role-playing AI agents
* **AutoGen**, **Haystack**, or any custom framework

This flexibility means you can leverage MCP's standardized server ecosystem regardless of your chosen development stack, avoiding vendor lock-in and maintaining portability across different AI architectures.

## Pre-Requisites

* Python 3.11+
* Python package manager (pip, poetry, uv)

## Setting Up

{% stepper %}
{% step %}
**Installation**

{% tabs %}
{% tab title="pip" %}
```
pip install gllm-tools
```
{% endtab %}

{% tab title="poetry" %}
```
poetry install gllm-tools
```
{% endtab %}

{% tab title="uv" %}
```
uv add gllm-tools
```
{% endtab %}
{% endtabs %}
{% endstep %}

{% step %}
**Set up the Client**

```python
from gllm_tools.mcp.client.config import MCPConfiguration

# Configure your MCP servers
servers = {
    "github": {
        "url": "https://api.githubcopilot.com/mcp",
        "headers": {
            "Authorization": "Bearer {gho_token}"
        }
    }
}

# Create the client
client = MCPClient(servers)
```
{% endstep %}

{% step %}
**List all Tools**

```python
import asyncio

# client = MCPClient(servers) from Step 2
async def use_tools():
    # Get all available tools
    tools = await client.get_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")

    # Get tools from a specific server
    github_tools = await client.get_tools(server="github")

    # Tools are MCPTool objects with name, description, and parameters
    for tool in github_tools:
        print(f"Tool: {tool.name}")
        print(f"Description: {tool.description}")
        print(f"Parameters: {tool.parameters}")

asyncio.run(use_tools())
```
{% endstep %}

{% step %}
**Executing a Tool Directly**

{% hint style="danger" %}
Note that this example is purely for example. It is **not** recommended to utilize MCP tools this way; it is only to demonstrate how to use tools directly. For programmatic purposes, **it is highly recommended to use REST API or SDK instead!**

MCP is **intended for LLMs and AI Agents**! See section [#working-with-other-agentic-frameworks](mcp-client.md#working-with-other-agentic-frameworks "mention") to utilize MCP in the appropriate context!
{% endhint %}

<pre class="language-python"><code class="lang-python">import asyncio
from typing import cast
from mcp import ClientSession
from gllm_tools.mcp.client.session import create_session

configuration = {
    "github": {
        "url": "https://api.githubcopilot.com/mcp",
        "headers": {
            "Authorization": "Bearer {gho_token}"
        }
    }
}

async def main():
<strong>    async with create_session(configuration) as session:
</strong><strong>        await session.initialize()
</strong>        tool_name = "github_get_issue_handler"
        params = {
            "owner": "gdp-admin",
            "repo": "gl-sdk",
            "issue_number": 2668,
        }
        call_tool_result = await cast(ClientSession, session).call_tool(tool_name, params)
        print(call_tool_result)

if __name__ == "__main__":
    asyncio.run(main())
</code></pre>
{% endstep %}
{% endstepper %}

## Working with other Agentic Frameworks

### Langgraph

We have provided a `LangchainMCPClient` that adapts MCP for specific agentic frameworks. Here is an example of implementing an Agent using Langgraph utilizing our MCP Client. The complete source code can be found [here](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-tools/gllm_tools/mcp/client/langchain/client.py#L32).

```python
from gllm_tools.mcp.client.langchain.client import LangchainMCPClient
from langgraph.prebuilt import create_react_agent

# Same server configuration
servers = {"github": {...}}

# Langchain-specific client (this is a framework adapter!)
langchain_client = LangchainMCPClient(servers)

# Get Langchain-compatible tools
tools = await langchain_client.get_tools()

agent = create_react_agent(
    name="HelloAgent",
    prompt="You are a helpful assistant that can utilize all tools given to you to solve the user's input.",
    model=ChatOpenAI("gpt-4.1"),
    tools=tools,
)
```

### Others

The base `MCPClient` is framework-agnostic and returns raw `MCPTool` object. To integrate with specific agentic frameworks (like Langchain, CrewAI, Google ADK, etc.), you extend the client to create framework adapters that allow other agentic frameworks to connect to MCP servers. Please refer to the [#langgraph](mcp-client.md#langgraph "mention") section above to see a full complete adapter.

```python
from gllm_tools.mcp.client.client import MCPClient

class MyAgenticFrameworkClient(MCPClient):
    async def _process_tool(self, tool, config):
        """Convert MCPTool to your framework's tool format."""
        # Convert to your framework's tool format
        return MyFrameworkTool(
            name=tool.name,
            description=tool.description,
            schema=tool.parameters,
            # Add framework-specific execution logic
        )

# Usage
client = MyAgenticFrameworkClient(servers)
tools = await client.get_tools()  # Returns MyFrameworkTool objects
```
