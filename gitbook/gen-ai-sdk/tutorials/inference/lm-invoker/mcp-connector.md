---
icon: usb-drive
---

# MCP Connector

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [mcp-connector.md](mcp-connector.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `OpenAILMInvoker`

## What is MCP Connector?

MCP connector is a native tool that allows the language model to access **managed third-party services** through OpenAI's MCP connector infrastructure. Unlike MCP servers (which you host yourself), MCP connectors provide pre-built integrations with popular services like Google Drive, Gmail, and other enterprise tools.

When enabled, MCP connector calls are stored in the `outputs` attribute of the `LMOutput` object and can be accessed via the `mcp_calls` property.

### Authentication Options

MCP connectors support three authentication methods:

1. **Static Access Token** - A string token for simple authentication
2. **OAuth Credentials** - An `OAuthCredentials` object for OAuth-based services
3. **Dynamic Token Function** - An async function that returns fresh tokens

### Creating MCP Connector Tools

MCP connector tools can be created in two ways:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, OAuthCredentials

# Option 1: Using dictionary
mcp_connector_tool = {
    "type": "mcp_connector",
    "connector_id": "connector_googledrive",
    "name": "google_drive",
    "auth": "<google_oauth_token>",
}

# Option 2: Using NativeTool factory method (recommended)
mcp_connector_tool = NativeTool.mcp_connector(
    connector_id="connector_googledrive",
    name="google_drive",
    auth="<google_oauth_token>",
)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[mcp_connector_tool])
```

### Authentication Examples

#### Static Token Authentication

```python
from gllm_inference.schema import NativeTool

# Simple string token
mcp_connector = NativeTool.mcp_connector(
    connector_id="connector_googledrive",
    name="google_drive",
    auth="ya29.a0AfB_byC...",  # OAuth access token
)
```

#### OAuth Credentials Authentication

```python
from gllm_inference.schema import NativeTool, OAuthCredentials

# Using OAuthCredentials object
oauth_creds = OAuthCredentials(
    access_token="ya29.a0AfB_byC...",
    refresh_token="1//0gH...",
    token_uri="https://oauth2.googleapis.com/token",
    client_id="<client_id>",
    client_secret="<client_secret>",
)

mcp_connector = NativeTool.mcp_connector(
    connector_id="connector_googledrive",
    name="google_drive",
    auth=oauth_creds,
)
```

#### Dynamic Token Function

```python
from gllm_inference.schema import NativeTool

# Async function that returns fresh tokens
async def get_google_token() -> str:
    # Your token refresh logic here
    return await fetch_fresh_google_token()

mcp_connector = NativeTool.mcp_connector(
    connector_id="connector_googledrive",
    name="google_drive",
    auth=get_google_token,
)
```

### Complete Example: Google Drive Integration

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool

# Create Google Drive MCP connector
google_drive_connector = NativeTool.mcp_connector(
    connector_id="connector_googledrive",
    name="google_drive",
    auth="<your_google_oauth_token>",
)

# Initialize LM invoker with the connector
lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    tools=[google_drive_connector]
)

# Query that requires Google Drive access
query = "List all PDF files in my Google Drive that were modified in the last week"
output = asyncio.run(lm_invoker.invoke(query))

# Access MCP connector calls
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
```

### See Also

* [mcp-server.md](mcp-server.md "mention")
