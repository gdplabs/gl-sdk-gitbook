---
icon: truck-fast
---

# Quickstart

Get a Connector MCP server running in your client in under 5 minutes using token-based authentication.

### Prerequisites

* An MCP-compatible client that supports Streamable HTTP (e.g., VSCode, Cursor, Windsurf). **For this example, we will use Cursor**.
* GL Connectors [#user-token](../api/credentials.md#user-token "mention")
* An appropriate **integration** for the connector you want to use
* OpenAI API Key (if you're using either AIP or Langgraph)

{% hint style="info" %}
**Fastest path:** You can obtain your credentials and set up an integration all in one place via the [connectors-console.md](../api/tools-and-interfaces/connectors-console.md "mention"). Alternatively, follow the [credentials.md](../api/credentials.md "mention") guide and create an integration via the [cli.md](../api/tools-and-interfaces/cli.md "mention") or [playground.md](../api/tools-and-interfaces/playground.md "mention").
{% endhint %}

{% tabs %}
{% tab title="Your IDE" %}
#### Integrating with Pre-Existing Clients

See [mcp-clients.md](mcp-clients.md "mention") for possible clients. Most of the time, this is your IDEs like Cursor, Windsurf, etc. Claude Code, Claude Desktop is also included in this as long as they support Streamable HTTP.

**Configure Your Client**

Add the following to your MCP client configuration. This example connects to the **Gmail** connector using Cursor:

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

Replace the `eyJ...` with your User Token.

{% hint style="warning" %}
**Important:** Do not omit the `Bearer` prefix. `Authorization: eyJ...` will fail — it must be `Authorization: Bearer eyJ...`.
{% endhint %}

> Using a different client? See the **MCP Clients** page for client-specific configuration.

**Verify It Works**

Restart your client if needed (some require this to pick up config changes), then try invoking a tool from the connector. If your client lists the available tools from the server, you're good to go.

<figure><img src="../../../.gitbook/assets/image (1) (1) (1).png" alt=""><figcaption></figcaption></figure>

Try sending a message in your Cursor Chat with a query like the following once you've made sure the connection is correct:

```
Tell me how many drafts I have.
```

**Optional: Target a Specific Integration**

If you have multiple integrations for the same connector, specify which one to use with the `X-Integration` header:

```json
"headers": {
  "Authorization": "Bearer eyJ...",
  "X-Integration": "user..."
}
```
{% endtab %}

{% tab title="AIP" %}
#### Integrating with [Broken link](/broken/pages/FHWJhfjGs2w6fEuqwYv9 "mention")

**Setting up**

1. `uv init --bare`
2. `uv add glaip-sdk[local]`
3. Set `OPENAI_API_KEY` as environment key and the user token replacing `{token}` retrieved above.

**Source Code**

{% code title="main.py" lineNumbers="true" %}
```python
from glaip_sdk import Agent, MCP
from glaip_sdk.models import OpenAI

google_drive_mcp = MCP(
    name="drive",
    transport="http",
    config={"url": "https://connectors.glair.ai/google_drive/mcp"},
    authentication={
        "type": "bearer-token",
        "token": "{token}"
    }
)

agent = Agent(
    name="drive-agent",
    instruction="You are a helper in managing Google Drive files and folders",
    mcps=[google_drive_mcp],
    model=OpenAI.GPT_5_NANO,
)

result = agent.run("Find me the latest file I created.")
print(result)

```
{% endcode %}

**Executing**

You can simply execute by running `uv run main.py` . Do note that due to LLMs' stochastic nature, your responses will vary.
{% endtab %}

{% tab title="Langgraph" %}
#### Integrating with Langgraph

To integrate with Langgraph, we will use our in-house [mcp-client.md](../../../common-modules/tutorials/tools/mcp-client.md "mention"), housed under GL SDK in `gllm-tools`.

**Setting up**

1. `uv init --bare`
2. `uv add gllm-tools-binary langgraph langchain[openai]`
3. Set `OPENAI_API_KEY` as environment key and the user token replacing `{token}` retrieved above.

**Source Code**

{% code title="" lineNumbers="true" %}
```python
import asyncio
from gllm_tools.mcp.client.langchain.client import LangchainMCPClient
from langgraph.prebuilt import create_react_agent

servers = {
    "drive": {
        "url": "https://connectors.glair.ai/google_drive/mcp",
        "headers": {
            "Authorization": "Bearer {token}"
        }
    }
}

async def main():
    langchain_client = LangchainMCPClient(servers)
    tools = await langchain_client.get_tools()
    agent = create_react_agent(
        name="HelloAgent",
        prompt="You are a helper in managing Google Drive files and folders",
        model="gpt-4.1",
        tools=tools,
    )
    print(await agent.ainvoke({"messages": [{"role": "user", "content": "Find me the latest file I created."}]}))

asyncio.run(main())
```
{% endcode %}

**Executing**

You can simply execute by running `uv run main.py` . Do note that due to LLMs' stochastic nature, your responses will vary.
{% endtab %}
{% endtabs %}

### Next Steps

* [in-depth-guide.md](in-depth-guide.md "mention") — OAuth 2.1 authentication, choosing between auth methods, and debugging with MCP Inspector.
* [mcp-clients.md](mcp-clients.md "mention") — Client-specific setup for Claude Desktop, Cursor, Windsurf, VSCode, and more.
* [connector-mcp-cookbook.md](connector-mcp-cookbook.md "mention") — Programmatic usage and advanced patterns.
* [mcp-client.md](../../../common-modules/tutorials/tools/mcp-client.md "mention") — Our in-house MCP Client.
