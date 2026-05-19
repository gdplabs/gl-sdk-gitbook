---
icon: square-code
---

*When to use:* You are coding in Python, iterating from notebooks or applications, and want typed helpers during development.

## Step 1: Install or Upgrade the Package

```bash
# Standard install (includes local execution)
pip install --upgrade "glaip-sdk[local]"

# Or install without local extra (remote execution only)
pip install --upgrade glaip-sdk
```

## Step 2: Create and Run Your First Agent Locally

Ensure you installed `glaip-sdk[local]` and set your LLM provider key (for example `OPENAI_API_KEY`) before running locally.

```python
from glaip_sdk import Agent

agent = Agent(
    name="hello-world-agent",
    instruction="You are a friendly AI assistant.",
)

response = agent.run("Hello! How are you today?")
print(response)
```

## Step 3: Specify a Model (Optional)

By default, agents use `openai/gpt-5-nano`. You can specify a different model using the standardized `provider/model` format:

```python
from glaip_sdk import Agent
from glaip_sdk.models import OpenAI, DeepInfra

# Using model constants (recommended)
agent = Agent(
    name="hello-world-agent",
    instruction="You are a friendly AI assistant.",
    model=OpenAI.GPT_5_MINI,  # "openai/gpt-5-mini"
)

# Or using string format
agent = Agent(
    name="hello-world-agent",
    instruction="You are a friendly AI assistant.",
    model="deepinfra/Qwen/Qwen3-30B-A3B",
)

response = agent.run("Hello! How are you today?")
print(response)
```

## Step 4: Optional: Connect to AIP Server

If you want to run against the remote AIP server instead of using `aip-agents` locally, add your API details to a `.env` file:

```bash
echo "AIP_API_URL=https://your-aip-instance.com" >> .env
echo "AIP_API_KEY=your-api-key-here" >> .env
```

When targeting the AIP server, call `agent.deploy()` once before running:

```python
agent.deploy()
response = agent.run("Hello! How are you today?")
```

The SDK reads `AIP_API_URL` and `AIP_API_KEY` from the environment when deploying and running agents.

#### Optional Next Steps

- Attach a tool (see the [Tools guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools)) and rerun the agent.
- Attach a file with `agent.run(..., files=["/path/to/file.pdf"])` and follow the [File processing guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/file-processing).
- Persist conversation context with `chat_history` or `agent_config.memory` (covered in the [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents)).
