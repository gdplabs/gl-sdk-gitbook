---
icon: globe
---

Choose between local execution and remote deployment based on your development stage and infrastructure requirements.

{% hint style="info" %}
**When to use this guide:** Reference this when deciding how to run agents during development, testing, or production deployment. Use the decision checklist to pick the right mode for your use case.
{% endhint %}

## Overview

The SDK supports two execution modes:

- **Local Mode** — Agents run directly on your machine using the `aip-agents` library
- **Remote Mode** — Agents run on the **remote server** (via the `ai-agent-platform` platform, which uses `aip-agents` internally)

Both modes use the same `Agent` API, making it easy to switch between them. The SDK (`glaip-sdk`) can connect to either the platform's remote server or run agents locally using `aip-agents` directly.

## Quick Comparison

| Feature                   | Local Mode                                                    | Remote Mode                                  |
| ------------------------- | ------------------------------------------------------------- | -------------------------------------------- |
| **⚙️ Setup**              | Install local extra and configure LLM provider key            | Install SDK and configure remote API URL/key |
| **🔐 Credentials**        | LLM provider key + optional feature keys (memory, NER, tools) | AIP API URL + API key                        |
| **🚀 Deploy Step**        | No deploy step; run immediately                               | Deploy first to register agent               |
| **🖥️ Execution Location** | Runs on your machine                                          | Runs on remote server                        |
| **🧠 LLM Provider**       | Local (via `aip-agents`)                                      | Platform-managed or custom                   |

## Capability Checklist

| Capability                                               | Local Mode        | Remote Mode                                        |
| -------------------------------------------------------- | ----------------- | -------------------------------------------------- |
| **🛠️ Tool calling (custom tools)**                       | ✅                | ✅                                                 |
| **🔗 MCP support**                                       | ✅                | ✅                                                 |
| **🧠 Model selection**                                   | ✅                | ✅                                                 |
| **🧵 Token streaming**                                   | ✅                | ✅                                                 |
| **🧾 Tool output sharing**                               | ✅                | ✅                                                 |
| **🤝 Sub-agent delegation**                              | ✅                | ✅                                                 |
| **🧍 HITL**                                              | ✅                | ✅ (audit trail)                                   |
| **💾 Persistent memory (`mem0`)**                        | ✅                | ✅                                                 |
| **🧰 Built-in tool: Code Interpreter**                   | ✅                | ✅                                                 |
| **🧰 Built-in tool: Browser Use**                        | ✅                | ✅                                                 |
| **🧰 Built-in tool: Document Loader (PDF, DOCX, Excel)** | ✅                | ✅                                                 |
| **🔧 Runtime config overrides**                          | ✅                | ✅                                                 |
| **🕵️ PII**                                               | ✅                | ✅                                                 |
| **📁 Run with file attachments**                         | ✅                | ✅                                                 |
| **🗄️ Agent filesystem (read/write/edit/ls/grep tools)**  | ✅                | ✅                                                 |
| **💿 Agent filesystem: `LocalDiskConfig`**               | ✅                | ✅ (`base_directory` ignored; server-managed path) |
| **🔌 GL Connectors support**                             | ✅                | ✅                                                 |
| **🧩 Built-in agents (e.g., Data Analyst)**              | ❌                | ✅                                                 |
| **🌐 CRUD + Run REST API**                               | ❌                | ✅                                                 |
| **🗂️ Agent registry (persistent storage)**               | ❌                | ✅                                                 |
| **📜 Run history/logs/metrics**                          | ❌ (console only) | ✅                                                 |
| **⏰ Scheduling**                                        | ❌                | ✅                                                 |
| **📡 Offline execution**                                 | ✅                | ❌                                                 |

## Local Mode

### Setup

```bash
# Install with local execution support
pip install "glaip-sdk[local]"

# Configure LLM provider (required)
export OPENAI_API_KEY="your-openai-key"
```

The `[local]` extra includes `aip-agents` for local LLM execution.

### Usage Pattern

```python
from glaip_sdk.agents import Agent

# Create and run locally (no deploy needed)
agent = Agent(
    name="local-agent",
    instruction="You are a helpful assistant.",
)

# Runs immediately on your machine
response = agent.run("Hello!")
```

### Local Run Examples

All local features assume a configured LLM provider key (for example `OPENAI_API_KEY`).
Additional required environment variables are listed per feature below.

Example `.env` (include only what you use):

```bash
OPENAI_API_KEY=your-openai-key
MEM0_API_KEY=your-mem0-key
NER_API_URL=https://ner.example.com
NER_API_KEY=your-ner-key
SERPER_API_KEY=your-serper-key
E2B_API_KEY=your-e2b-key
# GL Connectors settings
GL_CONNECTORS_BASE_URL=https://gl-connector.example.com
GL_CONNECTORS_API_KEY=your-api-key
GL_CONNECTORS_USERNAME=your-username
GL_CONNECTORS_PASSWORD=your-password
GL_CONNECTORS_IDENTIFIER=optional-identifier
# (Backward compatible with BOSA_BASE_URL, etc.)
ARXIV_MCP_API_KEY=your-arxiv-key
ARXIV_MCP_AUTH_TOKEN=your-arxiv-token
```

| Feature                                                                         | Required env vars                                                                                                                          | Example                                                                                                                                                                |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Basic run                                                                       | None beyond LLM provider key                                                                                                               | [main.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main.py)                                                             |
| Files (`files=[...]`)                                                           | None beyond LLM provider key                                                                                                               | [main_with_local_files.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_local_files.py)                           |
| Built-in tool: Document Loader (PDFReaderTool, DocxReaderTool, ExcelReaderTool) | None beyond LLM provider key                                                                                                               | [main_with_docproc_pdf.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_docproc_pdf.py)                           |
| Native aip-agents tools (web search, code sandbox, browser use)                 | `SERPER_API_KEY` (GoogleSerperTool), `E2B_API_KEY` (E2BCodeSandboxTool); other tools may require their own env                             | [main_with_native_tool.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_native_tool.py)                           |
| mem0 memory                                                                     | `MEM0_API_KEY` or `GLLM_MEMORY_API_KEY`                                                                                                    | [main_with_memory.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_memory.py)                                     |
| PII toggle (`enable_pii`)                                                       | Optional `NER_API_URL` and `NER_API_KEY` for NER-backed masking                                                                            | [main_with_pii_toggle.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_pii_toggle.py)                             |
| Tool output sharing (`agent_config.tool_output_sharing`)                        | None beyond LLM provider key                                                                                                               | [main_with_tool_output_sharing.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_tool_output_sharing.py)           |
| Runtime config overrides                                                        | `ARXIV_MCP_API_KEY` and `ARXIV_MCP_AUTH_TOKEN` (optional, for Arxiv MCP)                                                                   | [main_with_runtime_config.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_runtime_config.py)                     |
| Definition-time configs (`tool_configs`, `mcp_configs`, `agent_config`)         | `ARXIV_MCP_API_KEY` and `ARXIV_MCP_AUTH_TOKEN` (optional, for Arxiv MCP)                                                                   | [main_with_agent_definition_configs.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_agent_definition_configs.py) |
| HITL (`hitl_enabled`)                                                           | None beyond LLM provider key                                                                                                               | [main_with_hitl.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_hitl.py)                                         |
| Chat history input                                                              | None beyond LLM provider key                                                                                                               | [main_with_chat_history.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_chat_history.py)                         |
| Sub-agents                                                                      | None beyond LLM provider key                                                                                                               | [main_with_subagents.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_subagents.py)                               |
| MCPs with local transport                                                       | `ARXIV_MCP_API_KEY` and `ARXIV_MCP_AUTH_TOKEN` (optional, for Arxiv MCP)                                                                   | [main_with_mcp.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_mcp.py)                                           |
| GL Connectors                                                                   | `GL_CONNECTORS_BASE_URL`, `GL_CONNECTORS_API_KEY`, `GL_CONNECTORS_USERNAME`, `GL_CONNECTORS_PASSWORD`; optional `GL_CONNECTORS_IDENTIFIER` | [main_with_gl_connectors_tool.py](https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gl-aip/examples/hello-world-local/main_with_gl_connectors_tool.py)             |

### Tool Output Sharing Quickstart (Local)

The `hello-world-local` project ships with `main_with_tool_output_sharing.py`, which wires two LangChain-compatible tools together and enables `$tool_output.<call_id>` references through `agent_config={"tool_output_sharing": True}`. Use this path when you want to stage multi-step tool workflows locally before promoting them to the remote platform.

{% hint style="info" %}
Monitor the console output when running locally. Each tool call prints a `call_id` so you can trace which stored output is being replayed.
{% endhint %}

1. Install dependencies: `pip install "glaip-sdk[local]"` (includes `aip-agents`).
1. Copy `.env.example` from `gl-aip/examples/hello-world-local` in the [GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip) and set `OPENAI_API_KEY`.
1. Run `python main_with_tool_output_sharing.py` to watch the agent perform a two-step greeting workflow with shared tool responses.

```python
from glaip_sdk.agents import Agent
from tools import GreetingFormatterTool, GreetingGeneratorTool

INSTRUCTION = """Use greeting_generator first, then pass the stored output
into greeting_formatter via $tool_output.<call_id> before responding."""

greeting_agent = Agent(
    name="hello_local_tool_output_sharing",
    instruction=INSTRUCTION,
    description="Local agent that demonstrates tool output sharing",
    tools=[GreetingGeneratorTool, GreetingFormatterTool],
    agent_config={"tool_output_sharing": True},
)

response = greeting_agent.run("Create a greeting for Alice, then format it nicely.", verbose=True)
print(response)
```

The script prints both the intermediate explanation (including the `call_id` reference) and the final formatted greeting, mirroring the same workflow you would deploy remotely once satisfied with the run.

## Remote Mode

Remote mode connects to the **platform's remote server**, which uses `aip-agents` internally to execute agents.

### Setup

```bash
# Install SDK
pip install glaip-sdk

# Configure connection to AIP server
export AIP_API_URL="https://your-aip-instance.com"
export AIP_API_KEY="your-api-key-here"
```

### Usage Pattern

```python
from glaip_sdk.agents import Agent

# Create agent definition
agent = Agent(
    name="remote-agent",
    instruction="You are a helpful assistant.",
    agent_config={"memory": "mem0"},  # Persistent memory
)

# Deploy to AIP server (creates/updates agent)
agent.deploy()

# Remote run
response = agent.run("Hello!")
```

## Switching Between Modes

**Best practice:** Use instances instead of strings for seamless migration between modes.

### Local Override for Deployed Agents

You can force local execution for an agent that has already been deployed to the remote server by passing `local=True` to `run()` or `arun()`.

```python
# Agent is deployed (has an ID and routes to server by default)
agent.deploy()

# Standard run: routes to remote server
agent.run("Hello server")

# Override: forces local execution using local tools and code
agent.run("Hello local", local=True)
```

{% hint style="info" %}
When `local=True` is used, the SDK behaves exactly as if the agent was not deployed, requiring the `[local]` extra and local LLM credentials.
{% endhint %}

### Seamless Migration Example

```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class EchoInput(BaseModel):
    text: str = Field(..., description="Text to echo")


class EchoTool(BaseTool):
    name: str = "echo_tool"
    description: str = "Echo back text."
    args_schema: type[BaseModel] = EchoInput

    def _run(self, text: str) -> str:
        return f"Echo: {text}"
```

```python
from glaip_sdk.agents import Agent

# Use LangChain-compatible tools for seamless local/remote compatibility
agent = Agent(
    name="my-agent",
    instruction="You are helpful.",
    tools=[EchoTool],
)

# Local mode: just run
response = agent.run("What time is it?")

# Remote mode: add deploy() call
agent.deploy()
response = agent.run("What time is it?")
```

{% hint style="warning" %}
**Local mode does not support string references or platform-only helpers** (`Tool.from_native()`, `MCP.from_native()`). Use LangChain BaseTool classes/instances or `Tool.from_langchain()` for tools, and MCP instances with local transport configs (`http`, `sse`, `stdio`). Add native tools or MCPs only when deploying to the platform.
{% endhint %}

### Migration Path: Local → Remote

1. **Test locally** with `agent.run()` (uses `aip-agents` directly)
1. **Configure AIP server credentials** (`AIP_API_URL`, `AIP_API_KEY`)
1. **Add `deploy()` call** before first remote run
1. **Verify remote run** with same inputs

### Migration Path: Remote → Local

1. **Install local extra**: `pip install "glaip-sdk[local]"` (includes `aip-agents`)
1. **Set `OPENAI_API_KEY`** environment variable
1. **Remove `deploy()` calls** from code (not needed for local execution)
1. **Replace string/native references** with instances if any exist

## Decision Checklist

Use **Remote Mode** (AIP server) if you need any capability that is remote-only (✅ on Remote, ❌ on Local). Otherwise, use **Local Mode** (aip-agents directly).

## Common Patterns

### Pattern 1: Local Development, Remote Production

```python
import os
from glaip_sdk import Agent, Tool

# EchoTool defined in the example above.

# Use LangChain tools for local runs; add native tools only when deploying to the platform
tools = [EchoTool]
if os.getenv("AIP_API_KEY"):
    tools.append(Tool.from_native("time_tool"))

agent = Agent(
    name="my-agent",
    instruction="...",
    tools=tools,
)

# Deploy only if AIP server credentials exist - MUST succeed for native tools to work
# If deploy() fails, agent.run() will attempt local execution and fail with Tool.from_native()
if os.getenv("AIP_API_KEY"):
    agent.deploy()

# Run works in both modes:
# - Local: uses aip-agents directly (requires LangChain BaseTool classes/instances, not Tool.from_native())
# - Remote: runs on remote server (platform uses aip-agents internally)
response = agent.run("query")
```

### Pattern 2: Conditional Mem0 Usage

```python
import os
from glaip_sdk import Agent

agent = Agent(
    name="my-agent",
    instruction="...",
)

# Enable persistent memory when Mem0 is configured locally or via AIP server
if os.getenv("AIP_API_KEY") or os.getenv("MEM0_API_KEY") or os.getenv("AIP_MEMORY_API_KEY"):
    agent.agent_config = {"memory": "mem0"}

# Deploy only if AIP server credentials exist
if os.getenv("AIP_API_KEY"):
    agent.deploy()

response = agent.run("query")
```

### Pattern 3: Testing Locally, Running on Remote

```python
from glaip_sdk import Agent, Tool

# EchoTool defined in the example above.

# test_agent.py - runs locally
def test_agent_logic():
    agent = Agent(
        name="test-agent",
        instruction="...",
        tools=[EchoTool],
    )
    response = agent.run("test query")
    assert "expected" in response

# main.py - remote run on platform
def main():
    agent = Agent(
        name="prod-agent",
        instruction="...",
        tools=[EchoTool],
    )
    agent.deploy()  # Deploys to AIP server
    response = agent.run("production query")  # Remote run
```

## Troubleshooting

| Issue                 | Local Mode                                         | Remote Mode                                           |
| --------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| Agent not found       | N/A (ephemeral)                                    | Check `aip agents list`                               |
| Missing dependencies  | Install `glaip-sdk[local]` (includes `aip-agents`) | Upload tools to AIP server                            |
| Authentication error  | N/A                                                | Verify `AIP_API_KEY` for AIP server                   |
| Memory not persisting | Check `MEM0_API_KEY` and `agent_config.memory`     | Check `agent_config.memory` and AIP server mem0 setup |
| Slow execution        | Check local LLM config                             | Check network latency to remote server                |

## Related Documentation

- [Install & Configure](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/prerequisites) — Setup for both modes
- [Quick Start Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide) — First agent in each mode
- [Agents Guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — Full agent lifecycle
- [Configuration Management](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) — Promote agents between environments
