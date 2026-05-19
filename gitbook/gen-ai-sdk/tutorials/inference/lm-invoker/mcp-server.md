---
icon: server
---

# MCP Server

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [mcp-server.md](mcp-server.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `OpenAILMInvoker`

## What is MCP Server?

MCP server is a native tool that allows the language model to use remote MCP servers to give models new capabilities. When it's enabled, MCP calls are stored in the `outputs` attribute of the `LMOutput` object and can be accessed via the `mcp_calls` property.

MCP server tool can be enabled with several options:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

SERVER_URL = "https://mcp.deepwiki.com/mcp"
SERVER_NAME = "deepwiki"

# Option 1: as dictionary
mcp_server_tool = {"type": "mcp_server", "url": SERVER_URL, "name": SERVER_NAME, **kwargs}
# Option 2: as native tool object
mcp_server_tool = NativeTool.mcp_server(url=SERVER_URL, name=SERVER_NAME, kwargs)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[mcp_server_tool])
```

Let's try it to utilize the MCP server through our LM invoker!

```python
query = """
List all transport protocols supported by the 2025-03-26 version of
the MCP spec (modelcontextprotocol/modelcontextprotocol) in bullet points"
"""
output = asyncio.run(lm_invoker.invoke(query))
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
```

**Output:**

```
=== Output item: 'mcp_call' ===
id='mcp_0bb324738ba65b790069649beeafe08193a485b62fee44f228'
server_name='deepwiki'
tool_name='read_wiki_structure'
args={'repoName': 'modelcontextprotocol/modelcontextprotocol'}
output='Available pages for modelcontextprotocol/modelcontextprotocol...'

=== Output item: 'mcp_call' ===
id='mcp_0bb324738ba65b790069649bf2395481939dac9e53eb98818d'
server_name='deepwiki'
tool_name='read_wiki_contents'
args={'repoName': 'modelcontextprotocol/modelcontextprotocol'}
output='# Page: Overview\n\n# Overview\n\n<details>\n<summary>...'

=== Output item: 'mcp_call' ===
id='mcp_0bb324738ba65b790069649bf81cf08193b7066a98abaf56e1'
server_name='deepwiki'
tool_name='ask_question'
args={
    'repoName': 'modelcontextprotocol/modelcontextprotocol',
    'question': 'List all transport protocols supported by the 2025-03-26 MCP spec (modelcontextprotocol/modelcontextprotocol). (From the Transport Layer section 2.3.)',
}
output='The 2025-03-26 Model Context Protocol (MCP) specification supports...'

=== Output item: 'text' ===
- STDIO Transport
- Streamable HTTP Transport (HTTP POST with optional Server-Sent Events for streaming)
```
