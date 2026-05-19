---
icon: user-robot-xmarks
---

Master agent lifecycle operations, orchestration patterns, and runtime controls
with the Python SDK. Use CLI pages for low-code operations. Use REST as reference-only for internal integrations (for example GLChat).

{% hint style="info" %}
For current coverage, see the [AIP capability matrix](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/introduction-to-gl-aip#platform-capabilities-at-a-glance).
Key callouts for agents: CLI still leans on export/import for `tool_configs`, memory toggles, and runtime overrides. Run history and scheduling are available via the SDK; REST remains reference-only.
{% endhint %}

{% hint style="info" %}
CLI examples accept either an agent ID or a unique name for `AGENT_REF`. Partial
matches trigger fuzzy search; add `--select` to disambiguate or pass the full ID
when you need a deterministic lookup.
{% endhint %}

## Execution Modes: Local vs Remote

See [Local vs Remote Mode](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/local-vs-remote) for detailed comparison and decision checklist.

## Pattern Decision Guide

Choose the right pattern for your agent operations:

### Agent-First Pattern (Recommended)

Use for creating and deploying single agents with simple configuration.

```python
from glaip_sdk import Agent
from tools import CalculatorTool  # Your LangChain BaseTool class

agent = Agent(
    name="math-tutor",
    instruction="You are a patient tutor. Show working for every step.",
    tools=[CalculatorTool],  # Use LangChain BaseTool classes for local execution
    agent_config={"memory": "mem0"}
)

# Run the agent
result = agent.run("What is 15 * 23?")
```

**Use this pattern for:**

- Creating and running single agents
- Simple agent configuration
- Quick prototypes
- Self-contained agent operations

### Client Pattern (Legacy/Advanced)

Use for listing, searching, and batch operations across multiple agents.
This is a legacy/advanced pattern kept for backward compatibility and
cross-agent governance workflows; prefer the Agent-first pattern for creating,
updating, and running individual agents.

```python
from glaip_sdk import Client

client = Client()

# Listing operations
agents = client.agents.list_agents(name="tutor")

# Batch operations
for agent in agents:
    print(f"Agent: {agent.name}")

# Advanced lifecycle management
agent = client.agents.get_agent_by_id("agent-123")
```

**Use this pattern for:**

- Listing and searching agents
- Batch operations across multiple agents
- Complex resource management workflows
- Multi-agent coordination

{% hint style="warning" %}
**Client-only operations (legacy/advanced admin path):**

- Creating agents from JSON/YAML files (`create_agent_from_file`)
- Bulk listing and filtering agents
- LangFlow sync operations
- Run history retrieval via `client.agents.runs`

Use the Client pattern only for these administrative and batch workflows.
{% endhint %}

______________________________________________________________________

## Create Agents

#### Python SDK

**Recommended: Agent Pattern**

```python
from glaip_sdk import Agent

agent = Agent(
    name="math-tutor",
    instruction="You are a patient tutor. Show working for every step.",
    tools=["time_tool"],  # String references require deploy() for remote execution
    agent_config={"memory": "mem0"}
)
agent.deploy()  # Required when using string tool references
```

> **Deprecated client pattern (still supported)**
>
> The older `client.agents.create_agent` API is kept for backward compatibility
> but new code should prefer the `Agent` pattern above for a simpler, low-code
> workflow and future improvements.

```python
# Deprecated: prefer the Agent(...) pattern above
from glaip_sdk import Client

client = Client()

agent = client.agents.create_agent(
    name="math-tutor",
    instruction="You are a patient tutor. Show working for every step.",
    tools=["time_tool"],
    agent_config={"memory": "mem0"},
)

# `agent` is a glaip_sdk.agents.Agent instance, so you can call the same
# lifecycle methods as with the Agent(...) pattern
agent.run("What is 15 * 23?")
```

#### CLI

```bash
aip agents create \
  --name math-tutor \
  --instruction "You are a patient tutor. Show working for every step." \
  --tools time_tool
```

{% endtab %}

{% tab title="REST" %}

```bash
curl \
  -X POST "$AIP_API_URL/agents" -H "Content-Type: application/json" -H \
  "X-API-Key: $AIP_API_KEY" -d '{
        "name": "math-tutor",
        "instruction": "You are a patient tutor. Show working for every step.",
        "tools": ["time_tool"],
        "agent_config": {"memory": "mem0"}
      }'
```

{% endtab %}
{% endtabs %}

### Specifying the Model

Agents use a default model (`openai/gpt-5-nano`) unless you specify otherwise. Use the `model` parameter with the standardized `provider/model` format:

{% tabs %}
{% tab title="Python SDK" %}

**Using Model Constants (Recommended):**

```python
from glaip_sdk import Agent
from glaip_sdk.models import OpenAI, DeepInfra, Anthropic

# OpenAI model
agent = Agent(
    name="analysis",
    instruction="You are a data analyst.",
    model=OpenAI.GPT_5_NANO,  # "openai/gpt-5-nano"
)

# DeepInfra model
agent = Agent(
    name="research",
    instruction="You are a research assistant.",
    model=DeepInfra.QWEN3_30B_A3B,  # "deepinfra/Qwen/Qwen3-30B-A3B"
)

# Anthropic model
agent = Agent(
    name="creative",
    instruction="You are a creative writer.",
    model=Anthropic.CLAUDE_SONNET_4_0,  # "anthropic/claude-sonnet-4-0"
)
```

**Using String Format:**

```python
# OpenAI model
agent = Agent(
    name="analysis",
    instruction="You are a data analyst.",
    model="openai/gpt-5",
)

# DeepInfra model (includes organization in path)
agent = Agent(
    name="research",
    instruction="You are a research assistant.",
    model="deepinfra/Qwen/Qwen3-30B-A3B",
)

# Anthropic model
agent = Agent(
    name="creative",
    instruction="You are a creative writer.",
    model="anthropic/claude-sonnet-4-0",
)
```

**Using Model Class (Custom Configuration):**

```python
from glaip_sdk import Agent
from glaip_sdk.models import Model

# Custom model with credentials and hyperparameters
agent = Agent(
    name="custom-model",
    instruction="You are helpful.",
    model=Model(
        id="custom/kimi-k2.5",
        base_url="https://api.moonshot.ai/v1",
        credentials="sk-xxxx",
        hyperparameters={
            "temperature": 1.0,
            "max_tokens": 32768,
        },
    ),
)
```

{% endtab %}

{% tab title="CLI" %}

```bash
# Create agent with specific model
aip agents create \
  --name analysis \
  --instruction "You are a data analyst." \
  --model openai/gpt-5

# Or using DeepInfra
aip agents create \
  --name research \
  --instruction "You are a research assistant." \
  --model deepinfra/Qwen/Qwen3-30B-A3B
```

{% endtab %}

{% tab title="REST" %}

```bash
curl \
  -X POST "$AIP_API_URL/agents" -H "Content-Type: application/json" -H \
  "X-API-Key: $AIP_API_KEY" -d '{
        "name": "analysis",
        "instruction": "You are a data analyst.",
        "model": "openai/gpt-5"
      }'
```

{% endtab %}
{% endtabs %}

{% hint style="tip" %}
**Model Constants:** Import typed constants from `glaip_sdk.models` for better IDE support and validation:

- `from glaip_sdk.models import OpenAI, Anthropic, Google, AzureOpenAI, DeepInfra, DeepSeek, Bedrock`
- Current SDK default model: `openai/gpt-5-nano`

See the [Language models](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/language-models) for the complete list of available models.
{% endhint %}

In JSON definitions, disable planning by setting `"planning": false` in
`agent_config` when you want a standard single-pass agent instead of a
planning-enabled one.

{% hint style="info" %}
`Agent.deploy()` will create a new agent when it does not exist yet, and update the
existing definition when called again with the same reference. Use `agent.update()`
when you already have a deployed `Agent` instance and want to change fields
incrementally.
{% endhint %}

{% hint style="info" %}
Need `tool_configs`, runtime overrides, or memory toggles from the CLI today?
Export with `aip agents get --export`, edit the JSON, then re-import with
`aip agents create --import` or `aip agents update --import`.
{% endhint %}

## List and Inspect Agents

#### Python SDK

```python
for agent in client.agents.list_agents(name="tutor"):
    print(agent.id, agent.name)

detail = client.agents.get_agent_by_id("agent-123")
print(detail.agent_config.get("lm_name"))
```

Note: `client.agents.list_agents()` and `client.agents.get_agent_by_id()` already
return `Agent` instances, so you can call methods like `agent.run()`,
`agent.update()`, or `agent.delete()` on the returned objects.

#### CLI

```bash
aip agents list

aip agents get agent-123 --view json
```

## Update Agents

#### Python SDK

```python
# Assuming `agent` is an Agent instance
# (created with Agent(...) or loaded via client.agents.get_agent_by_id)
agent.update(
    instruction="Provide thorough financial analysis.",
    tools=["balance-sheet-parser", "chart-generator"],
    agent_config={"memory": "mem0", "tool_output_sharing": False},
    language_model_id="managed-finance-lm",
)
```

#### CLI

```bash
cat > agent-update.json <<'JSON'
{
  "instruction": "Provide thorough financial analysis.",
  "agent_config": {
    "memory": "mem0",
    "tool_output_sharing": false
  },
  "language_model_id": "managed-finance-lm"
}
JSON

aip agents update agent-123 --import agent-update.json
```

## Delete and Restore Agents

#### Python SDK

```python
# Assuming `agent` is an Agent instance
agent.delete()  # Only needed if agent was deployed
```

#### CLI

```bash
aip agents delete agent-123
```

## Run Agents

### Basic Execution

#### Python SDK

**Synchronous:**

```python
# Assuming `agent` is an Agent instance
response = agent.run("Summarise the latest updates.")
print(response)
```

**Asynchronous (streaming):**

```python
import asyncio

async def main():
    async for chunk in agent.arun("Summarise the latest updates."):
        print(chunk, end="", flush=True)

asyncio.run(main())
```

Use `agent.arun()` when you need streaming responses or async integration.

#### CLI

```bash
aip agents run agent-123 --input "Summarise the latest updates."
```

### With Files

#### Python SDK

```python
response = agent.run(
    "Review the attached report and highlight top risks.",
    files=["/tmp/report.pdf"],
)
```

#### CLI

```bash
aip \
  agents run agent-123 --input "Review the attached report and highlight \
  top risks." --file /tmp/report.pdf
```

### Runtime Overrides and PII

#### Python SDK

```python
agent.run(
    "Produce a weekly revenue summary",
    pii_mapping={"<EMAIL_1>": "alice@example.com"},
    runtime_config={
        "agent_config": {
            "planning": False,
        },
        "tool_configs": {
            "revenue-sql": {"max_rows": 500, "group_by": "region"}
        },
        "mcp_configs": {
            "finance-data": {
                "authentication": {
                    "type": "api-key",
                    "value": "temporary-key"
                }
            }
        },
    },
)
```

Behind the scenes, `Agent` resolves `tool_configs` and `mcp_configs` using the
global registries. This means you can define these configs against class-based
`Tool` and MCP definitions, tool names, or IDs, and the SDK will map them to
the correct resource IDs at deploy or run time.

**Config key resolution:** In `runtime_config`, you can reference tools and MCPs by:

- **Custom LangChain tool class**: `{GreetingTool: {"param": "value"}}` — your `BaseTool` subclass
- **Tool helper instance**: `{Tool.from_native("time_tool"): {"param": "value"}}` — a `Tool` reference
- **MCP helper instance**: `{MCP.from_native("weather"): {"auth": {...}}}` — an `MCP` reference
- **Name string**: `{"greeting_tool": {"param": "value"}}` — tool/MCP name on the remote server
- **UUID**: `{"550e8400-e29b-...": {"param": "value"}}` — direct ID registered in the server

**Configuration priority order (lowest to highest):**

Agent configurations are resolved in the following priority order, with higher priority overriding lower:

1. **Agent definition configs** (lowest priority) — `agent_config`, `tool_configs`, `mcp_configs` passed to `Agent()` constructor
1. **Runtime config global** — Top-level keys in `runtime_config` (e.g., `runtime_config["tool_configs"]`)
1. **Runtime config agent-specific** (highest priority) — Agent-specific overrides in `runtime_config[agent]`

Example showing all three layers:

```python
from glaip_sdk import Agent, Tool

# Layer 1: Agent definition configs (lowest priority)
agent = Agent(
    name="research-agent",
    instruction="...",
    tools=[ResearchTool],
    agent_config={"planning": False},  # Default: no planning
    tool_configs={
        ResearchTool: {"style": "brief", "max_results": 5}  # Defaults
    },
)

# Layer 2 & 3: Runtime overrides (higher priority)
agent.run(
    "Research AI trends",
    runtime_config={
        # Layer 2: Global runtime config
        "agent_config": {"planning": True},  # Override: enable planning
        "tool_configs": {
            ResearchTool: {"style": "detailed"}  # Override: detailed style
        },
        # Layer 3: Agent-specific runtime config (highest priority)
        agent: {
            "tool_configs": {
                ResearchTool: {"max_results": 10}  # Override: 10 results
            }
        }
    }
)

# Final resolved config for this run:
# - planning: True (from runtime global)
# - style: "detailed" (from runtime global)
# - max_results: 10 (from runtime agent-specific, highest priority)
```

This layered approach allows you to:

- Set sensible defaults at agent definition time
- Apply global overrides for all agents in a workflow
- Fine-tune specific agents with agent-specific overrides

#### CLI

`pii_mapping` and `runtime_config` flags are in development. Use the SDK or REST
API for sensitive workflows until dedicated options land.

### Chat History

#### Python SDK

```python
history = [
    {"role": "user", "content": "We are drafting a security brief."},
    {"role": "assistant", "content": "Acknowledged. What scope should we cover?"},
]
agent.run(
    "Include external threat intel sources.",
    chat_history=history,
)
```

#### CLI

```bash
HISTORY='[{"role":"user","content":"We are drafting a security brief."}]'
aip \
  agents run agent-123 --input "Include external threat intel sources." \
  --chat-history "$HISTORY"
```

Persist long-term context with `agent_config.memory="mem0"`; edit exports or use
SDK kwargs until CLI flags arrive.

## Planning Mode

Enable planning mode to have agents create a structured plan before executing
complex tasks. This improves reasoning quality and task decomposition for
multi-step queries.

#### Python SDK

```python
from glaip_sdk import Agent
from tools import CalendarTool, TaskManagerTool  # Your LangChain BaseTool classes

agent = Agent(
    name="project-planner",
    instruction="You are a project manager. Break down tasks systematically.",
    tools=[CalendarTool, TaskManagerTool],
    agent_config={"planning": True},
)

# The agent will first create a plan, then execute each step
response = agent.run(
    "Create a launch plan for our new product release next month."
)
```

#### CLI

```bash
cat > planner-agent.json <<'JSON'
{
  "name": "project-planner",
  "instruction": "You are a project manager. Break down tasks systematically.",
  "agent_config": {
    "planning": true
  }
}
JSON

aip agents create --import planner-agent.json
```

{% hint style="info" %}
Planning mode is especially useful for:

- Complex multi-step tasks that benefit from upfront reasoning
- Tasks requiring coordination across multiple tools
- Scenarios where transparency in the agent's approach is valuable
{% endhint %}

## Timeouts and Limits

| Setting          | Recommended Default      | Maximum          | How to Change                                           |
| ---------------- | ------------------------ | ---------------- | ------------------------------------------------------- |
| Agent Runtime    | Set explicitly           | No SDK hard limit | `timeout=N` or `agent_config["timeout_seconds"]`        |
| Step Limit       | 100 steps                | 1000 steps       | `agent_config["step_limit_config"]["max_steps"]`       |
| Sub-Agent Levels | 5 levels                 | 10 levels        | `agent_config["step_limit_config"]["max_delegation_depth"]` |

{% hint style="info" %}
**Setting timeout:**
- **Recommended:** Use `timeout=N` on `Agent(...)`, `client.create_agent(...)`, or `client.update_agent(...)`.
- **Canonical config field:** The SDK normalizes this to `agent_config["timeout_seconds"]`.
- **Alternative:** Set `agent_config["timeout_seconds"]` directly when editing config by hand.
- **Aliases also supported:** `agent_config["timeout"]` (alias) and `agent_config["execution_timeout"]` (legacy) are both normalized to `timeout_seconds`.
{% endhint %}
```

{% hint style="info" %}
Only `timeout_seconds` is explicitly normalized by the SDK. Other `agent_config`
keys are mostly forwarded as provided to the local runtime or backend, so the
exact shape can depend on the runtime contract you are targeting.

The example above shows one configuration shape that may be useful in some
runtime contexts. The SDK documentation only makes a hard compatibility promise
for `timeout_seconds` here; treat the remaining non-timeout keys as runtime-
specific settings you should verify against the target runtime before depending
on them.
{% endhint %}

**Canonical timeout field:**

| Key Path                         | Type          | Default | Range                | Description                   |
| -------------------------------- | ------------- | ------- | -------------------- | ----------------------------- |
| `agent_config["timeout_seconds"]`   | int (seconds) | 300     | Any positive integer | Total runtime for the agent   |

**Example non-timeout key hierarchy shown above:**

All of the following live under `agent_config`, and the table shows their full
paths so the nesting is explicit:

| Full Key Path                                    | Parent Section             | Type    | Example Value | Notes |
| ------------------------------------------------ | -------------------------- | ------- | ------------- | ----- |
| `agent_config["step_limit_config"]["max_steps"]`       | `step_limit_config`        | `int`   | `100`         | Example step-limit key for runtimes that support nested step limit config |
| `agent_config["step_limit_config"]["max_delegation_depth"]` | `step_limit_config`   | `int`   | `5`           | Example delegation-depth key for runtimes that support nested step limit config |
| `agent_config["lm_retry_config"]["max_retries"]`       | `lm_retry_config`          | `int`   | `3`           | Example retry key for runtimes that support nested retry config |
| `agent_config["lm_retry_config"]["initial_delay"]`     | `lm_retry_config`          | `float` | `1.0`         | Example retry-delay key for runtimes that support nested retry config |
| `agent_config["lm_retry_config"]["max_delay"]`         | `lm_retry_config`          | `float` | `30.0`        | Example retry-delay cap key for runtimes that support nested retry config |
| `agent_config["lm_retry_config"]["exponential_base"]`  | `lm_retry_config`          | `float` | `2.0`         | Example backoff multiplier key for runtimes that support nested retry config |

Use those as documented examples of `agent_config` structure, not as SDK-normalized fields.

{% hint style="info" %}
**Configuring long running agents:**

- **Data analysis workflows**: Set timeout to 3600+ (1+ hour) for processing large datasets — use `timeout=3600` or `"timeout_seconds": 3600`
- **Multi-step research tasks**: If your target runtime supports step limits, increase them for complex research with multiple tools
- **Document processing**: If your target runtime supports delegation limits, use them for hierarchical document parsing
- **Automated pipelines**: If your target runtime supports retry settings, use them to handle network or API rate limits

For long running agents, consider monitoring progress through logs or implementing checkpoint mechanisms if supported by your agent tools.
{% endhint %}

## PII Masking (`enable_pii`)

NER-based PII masking redacts entities such as names, email addresses, and phone
numbers from tool inputs and outputs, then restores the real values in the final
response. You can control masking at three levels of granularity:

| Level | How to set | Priority |
| ----- | ---------- | -------- |
| Per-agent definition (stored) | `Agent(agent_config={"enable_pii": True})` | Lowest |
| Per-run override | `agent.run(..., enable_pii=True)` | Middle |
| Per-run, top-level runtime config | `runtime_config={"agent_config": {"enable_pii": True}}` | High |
| Per-subagent runtime config | `runtime_config={subagent: {"agent_config": {"enable_pii": False}}}` | Highest |

When `enable_pii` is `None` (the default), no override is injected and existing
stored config or the runner default (`False`) is used — fully backward-compatible.

{% hint style="info" %}
PII masking requires `NER_API_KEY` and `NER_API_URL` environment variables to be
configured in the local runtime. For remote runs the SDK forwards `enable_pii` to
the backend, which handles NER infrastructure.
{% endhint %}

### Set PII masking at agent definition time

Use `agent_config={"enable_pii": True}` to enable masking for every run of the
agent by default:

```python
from glaip_sdk import Agent

agent = Agent(
    name="customer-support",
    instruction="Help customers with their enquiries.",
    agent_config={"enable_pii": True},  # PII masking on by default for all runs
)
```

### Override PII masking at run time

Pass `enable_pii` directly to `agent.run()` or `agent.arun()` to toggle masking
for a single call without changing the stored agent definition:

```python
# Enable masking for this run even though stored config has enable_pii=False
result = agent.run("Look up Alice Johnson at alice.johnson@example.com", enable_pii=True)

# Disable masking for this run even though stored config has enable_pii=True
result = agent.run("Process this request", enable_pii=False)

# Omit the parameter to use whatever is stored in agent_config (default behavior)
result = agent.run("Process this request")
```

`agent.arun()` accepts the same parameter:

```python
import asyncio

async def main():
    async for chunk in agent.arun("Look up Alice Johnson", enable_pii=True):
        print(chunk, end="", flush=True)

asyncio.run(main())
```

### Override PII masking via `runtime_config`

Use `runtime_config["agent_config"]["enable_pii"]` when you want the top-level
runtime config to control masking. This takes priority over the per-run
`enable_pii` parameter:

```python
result = remote_agent.run(
    "Process this request",
    runtime_config={"agent_config": {"enable_pii": True}},
)
```

### Multi-agent propagation

When you pass `enable_pii` at run time for a **local** multi-agent setup, the
value propagates automatically to all subagents in the tree — unless a subagent
has its own explicit `runtime_config` override.

```python
from glaip_sdk import Agent

sub_agent = Agent(name="data-agent", instruction="Retrieve customer data.")
root_agent = Agent(
    name="coordinator",
    instruction="Coordinate customer queries.",
    agents=[sub_agent],
)

# enable_pii=True is applied to root AND sub_agent (no per-agent override)
result = root_agent.run("Get details for Alice Johnson", enable_pii=True, local=True)
```

To give a specific subagent a different setting while keeping the run-level
default for others, use `runtime_config` with the subagent as the key:

```python
# root runs with enable_pii=True; sub_agent runs with enable_pii=False
result = root_agent.run(
    "Get details for Alice Johnson",
    enable_pii=True,
    local=True,
    runtime_config={
        sub_agent: {"agent_config": {"enable_pii": False}},
    },
)
```

Propagation is recursive — it applies to every level of nesting, not just direct
children. A subagent with its own `runtime_config` override keeps that setting,
while its own children continue to inherit the run-level value.

### Priority resolution summary

Effective `enable_pii` for each agent is resolved from highest to lowest:

1. `runtime_config[<agent>]["agent_config"]["enable_pii"]` — per-agent escape hatch (local) or `runtime_config[<uuid>]["agent_config"]["enable_pii"]` (remote)
2. `runtime_config["agent_config"]["enable_pii"]` — top-level runtime config (root agent only)
3. `enable_pii` passed to `agent.run()` / `agent.arun()` — per-run caller override
4. `agent.agent_config["enable_pii"]` — stored definition-time value
5. Runner default: `False`

{% hint style="warning" %}
`enable_pii` in `runtime_config["agent_config"]` (priority 2) wins over the
per-run `enable_pii` parameter (priority 3). If both are set, the `runtime_config`
value is used.
{% endhint %}

## GL Connectors Token

Use the `gl_connectors_token` parameter when your run can invoke tools or MCPs
that require end-user auth via GL Connectors.

- **When required:** at least one reachable integration (tool or MCP)
  has `user_authentication=true` in its `tool_configs` or `mcp_configs`.
- **Execution scope:** per-run only; it is not stored in the deployed agent
  definition.
- **Local tool support:** in local mode, any named tool with
  `tool_configs[tool_name]["user_authentication"] = True` can receive the
  propagated token, including custom tools, not only `GLConnectorTool`.

#### Python SDK

```python
# Remote JSON run (agent must be deployed first)
remote_agent.deploy()

result = remote_agent.run(
    "Summarise my recent CRM activities",
    gl_connectors_token="<user-token>",
)

# Multipart run (with files)
result = client.agents.run_agent(
    remote_agent.id,
    "Review the attached report and sync notes",
    files=["/tmp/report.pdf"],
    gl_connectors_token="<user-token>",
)

# Local run
result = local_agent.run(
    "Summarise my recent CRM activities",
    local=True,
    gl_connectors_token="<user-token>",
)
```

**With a native tool (GL Connectors Tool):** remote and local runs use different tool
construction patterns.

```python
# Remote execution
from glaip_sdk import Agent, Tool

remote_agent = Agent(
    name="remote-agent",
    instruction="Search records and summarize highlights.",
    tools=[Tool.from_native("google_drive_search_files_tool")],
    tool_configs={
        "google_drive_search_files_tool": {
            "user_authentication": True,
        }
    },
)
remote_agent.deploy()

result = remote_agent.run(
    "Search my records and summarize highlights",
    gl_connectors_token="<user-token>",
)
```

```python
# Local execution
from glaip_sdk import Agent
from aip_agents.tools.gl_connector import GLConnectorTool

local_agent = Agent(
    name="agent-local",
    instruction="Search records and summarize highlights.",
    tools=[GLConnectorTool("google_drive_search_files_tool")],
    tool_configs={
        "google_drive_search_files_tool": {
            "user_authentication": True,
        }
    },
)

local_result = local_agent.run(
    "Search my records and summarize highlights",
    local=True,
    gl_connectors_token="<user-token>",
)
```

**With a custom local tool:** local propagation also works for non-native tools
as long as the tool has a stable name and its config enables
`user_authentication`.

```python
from langchain_core.tools import BaseTool
from glaip_sdk import Agent


class CRMSearchTool(BaseTool):
    name: str = "crm_search_tool"
    description: str = "Search CRM records"

    def _run(self, query: str) -> str:
        return f"Searching CRM for: {query}"


local_agent = Agent(
    name="custom-tool-local",
    instruction="Search CRM records and summarize highlights.",
    tools=[CRMSearchTool()],
    tool_configs={
        "crm_search_tool": {
            "user_authentication": True,
        }
    },
)

local_result = local_agent.run(
    "Search my CRM records and summarize highlights",
    local=True,
    gl_connectors_token="<user-token>",
)
```

**With an MCP:** remote and local runs use different MCP construction
patterns.

```python
# Remote execution
from glaip_sdk import Agent, MCP

remote_agent = Agent(
    name="crm-agent",
    instruction="Summarise CRM activities.",
    mcps=[MCP.from_native("crm_mcp")],
    mcp_configs={
        "crm_mcp": {
            "user_authentication": True,
        }
    },
)
remote_agent.deploy()

result = remote_agent.run(
    "Summarise my recent CRM activities",
    gl_connectors_token="<user-token>",
)
```

```python
# Local execution
from glaip_sdk import Agent, MCP

local_agent = Agent(
    name="crm-agent-local",
    instruction="Summarise CRM activities.",
    mcps=[
        MCP(
            name="crm_mcp",
            description="CRM MCP",
            transport="http",
            config={
                "url": "https://your-connector-host/crm/mcp",
                "authentication": {
                    "type": "bearer-token",
                    "token": "<stale-or-placeholder-token>",
                },
            },
        )
    ],
    mcp_configs={
        "crm_mcp": {
            "user_authentication": True,
        }
    },
)

local_result = local_agent.run(
    "Summarise my recent CRM activities",
    local=True,
    gl_connectors_token="<user-token>",
)
```

If the token is missing or invalid for required integrations:

- **Remote runs** can fail early with backend auth or precheck errors (for
  example `403` or `409`).
- **Local runs** raise an SDK error when an eligible `user_authentication:
  true` tool or MCP is missing the top-level token, and otherwise invalid
  tokens fail naturally at the tool or MCP request boundary.

## Multi-Agent Patterns

Need a refresher? The [Multi-Agent System Patterns overview](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns) dives deep
into hierarchies, routers, aggregators, and more. Use the snippet below as a
quick starter.

#### Python SDK

```python
from glaip_sdk import Agent

coordinator = Agent(
    name="research-coordinator",
    instruction="Delegate research and compile final briefs.",
    agents=[researcher, analyst],
    agent_config={"tool_output_sharing": True},
)
```

#### CLI

```bash
aip \
  agents create --name research-coordinator --instruction "Delegate \
  research and compile final briefs." \
  --agents researcher \
  --agents analyst
```

See the [Multi-Agent System Patterns overview](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns) for topology-specific
examples (hierarchical, router, aggregator, sequential, parallel).

## Iterate Quickly with Export and Import

#### CLI

```bash
aip agents get agent-123 --export agent.json
aip agents get agent-123 --export agent.yaml

aip agents create --import agent.json
```

#### Python SDK

```python
agent = client.agents.get_agent_by_id("agent-123")
with open("agent-123.json", "w") as fh:
    fh.write(agent.model_dump_json(indent=2))
```

## Iterate on Instructions Quickly

The CLI merges imports with flag overrides, so keep your definition in source
control and loop quickly:

1. **Export the agent** — `aip agents get prod-research --export prod-research.json`
   captures the full payload (instruction, `tool_configs`, runtime defaults).
1. **Edit locally** — adjust instructions, swap `language_model_id`, or tighten
   tool settings. Commit the file so teammates can review changes.
1. **Re-import** — `aip agents update prod-research --import prod-research.json`
   applies the update immediately; any CLI flags you pass override the JSON.
1. **Validate** — run `aip agents run prod-research --view md` or
   `--view json` to confirm behaviour before moving to the next tweak.

Prefer IDs in scripts to avoid fuzzy matches, and branch your JSON when testing
alternative prompts so you can compare diffs later. When you are ready to move
between environments, follow the
[Configuration management](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) for a full
promotion checklist.

## Observability

### Run History

Python SDK:

```python
from glaip_sdk import Client

client = Client()
runs = client.agents.runs.list_runs(agent_id="agent-123", limit=20, page=1)

successful = [r for r in runs.data if r.status == "success"]
for run in successful:
    print(run.id, run.status, run.created_at)
```

CLI (local transcript cache):

```bash
/transcripts
```

`/transcripts` opens the local transcript history; select a run in the browser to inspect details.

### Debug Remote Runs (Interactive `/runs` + SDK Run Detail)

Use this when a deployed agent behaves unexpectedly (tool failures, timeouts, inconsistent outputs) and you need an audit trail you can share.

1. Trigger a remote run with a reproducible input.
1. Capture the run ID (it appears in the streaming metadata and in run history).
1. Inspect tool calls, errors, and final output from the run record.

CLI (interactive remote runs browser):

```bash
# Open the slash palette
aip
```

Inside the palette:

1. Run `/agents` and select the agent you want to debug.
1. Run `/runs` to browse that agent's remote run history.
1. Open a run to view the full transcript and export it if needed.

{% hint style="info" %}
Screenshot placeholder: `/runs` table view with a selected run, plus the run detail panel showing tool calls and final output.
{% endhint %}

Python SDK (fetch run output events):

```python
from glaip_sdk import Client

client = Client()
agent_id = "agent-123"

# Pick the most recent run (page 1 is typically newest-first).
runs = client.agents.runs.list_runs(agent_id=agent_id, limit=1, page=1)
run_id = str(runs.data[0].id)

run = client.agents.runs.get_run(agent_id=agent_id, run_id=run_id)
print("status:", run.status)

# Print tool calls captured in agent_step events (best-effort; payloads vary by tool/framework).
for ev in run.output:
    meta = ev.get("metadata") or {}
    if meta.get("kind") not in ("agent_step", "agent_thinking_step"):
        continue
    for call in meta.get("tool_calls") or []:
        print(call.get("name"), call.get("args"))
```

Common debugging patterns:

- If the run ends early, search `run.output` for `metadata.kind == "error"` or terminal events (`final_response`, `error`, `step_limit_exceeded`).
- If a tool is misbehaving, compare the tool call args from the run transcript against your expected schema and defaults (`tool_configs`).
- If a run is inconsistent, export the agent definition and diff it across environments, then re-run with identical inputs and runtime overrides.

### Scheduling

Schedules run the same agent input on a recurring timetable in Asia/Jakarta (WIB). Create schedules with the SDK; CLI commands are on the roadmap. REST documentation exists as reference only in Resources.

In the SDK, you can provide a cron string (`minute hour day_of_month month day_of_week`) or a `ScheduleConfig` object. Unspecified fields default to `*` (every).

Example (Python SDK):

```python
from glaip_sdk import Client
from glaip_sdk.models.schedule import ScheduleConfig

client = Client()
agent = client.agents.get_agent_by_id("agent-123")

# Create a schedule via the agent facade
schedule = agent.schedule.create(
    input="Generate daily summary report",
    schedule=ScheduleConfig(
        minute="0",
        hour="9",
        day_of_week="0-4",  # Weekdays at 9am WIB (Mon-Fri)
    ),
)
print(f"Next run: {schedule.next_run_time}")

# List runs for this schedule
runs = agent.schedule.list_runs(schedule.id)
for run in runs:
    if run.status == "success":
        result = run.get_result()
        print(f"Run {run.id} completed in {run.duration}")
```

See the [Automation & scripting guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting#schedule-runs)
for cron formats, full CRUD, and run history retrieval.

## Troubleshooting

| Issue                 | Symptoms                        | Resolution                                                                       |
| --------------------- | ------------------------------- | -------------------------------------------------------------------------------- |
| Authentication errors | 401 responses                   | Re-run `aip accounts add <name>` + `aip accounts use <name>`, or update `Client(api_key=...)`. |
| Validation errors     | 422 responses                   | Check required fields with `aip agents create --help` or inspect error payloads. |
| Resource not found    | 404 responses                   | Confirm IDs with `aip agents list` or `client.agents.list_agents()`.             |
| Timeouts              | `AgentTimeoutError` or HTTP 504 | Increase `timeout` or review schedule load.                                      |

## Best Practices

1. **Scope instructions** — concise prompts improve output quality.
1. **Attach only necessary tools** — reduces attack surface and execution time.
1. **Reuse memory intentionally** — enable `mem0` when cross-run context adds value.
1. **Audit run history** — review recent runs via `client.agents.runs.list_runs(...)` and CLI transcripts for failure patterns.
1. **Sanitise secrets** — leverage `pii_mapping` and runtime MCP overrides to avoid persisting credentials.

## Related Documentation

- [Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/tools) — manage native and custom tooling.
- [MCPs](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/mcps) — connect external systems and rotate credentials.
- [Language models](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/language-models) — configure models using provider/model format or Model class.
- [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) — orchestrate agents programmatically.
- [Multi-Agent System Patterns overview](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns) — explore multi-agent coordination strategies.
