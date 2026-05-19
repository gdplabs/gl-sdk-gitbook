---
icon: wrench
---

Extend agents with native catalog entries, custom uploads, and GL Connectors. This guide is SDK-first (Python). Use the CLI pages for operational registry workflows. Use the REST API reference only when integrating from internal apps (for example GLChat).

{% hint style="info" %}
Check tooling coverage in the [AIP capability matrix](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/introduction-to-gl-aip#platform-capabilities-at-a-glance). When you hit CLI gaps (metadata edits, tool configs, runtime overrides), use the Python SDK or export/import. REST details live in the reference section.
{% endhint %}

## When to Use Which Tool Pattern?

| Scenario                          | Recommended Pattern                                    | Remote deploy?                                      |
| --------------------------------- | ------------------------------------------------------ | --------------------------------------------------- |
| Rapid prototyping / Local testing | `Agent(..., tools=[ToolClass])`                        | No (Native tools require platform)                  |
| Platform development              | `Agent(..., tools=[ToolClass, Tool.from_native(...)])` | Yes (Custom tools bundled + uploaded automatically) |
| Manual registry management        | CLI (Client legacy admin API for automation)           | Yes (Direct code upload to registry)                |

{% hint style="info" %}
**Local Native Tool Parity**

When running agents locally, `Tool.from_native("tool_name")` automatically attempts to discover and use the corresponding local implementation from the `aip-agents` SDK. This allows you to test agents using platform tools without a remote connection, provided the `aip-agents` package is installed in your environment.
{% endhint %}

## Create and Attach Tools

Prefer the **Agent-First** pattern for development. It prioritizes **local execution** via `agent.run()` for rapid iteration, while `agent.deploy()` handles bundling and upload to the platform when you are ready.

### Single-File Tool Integration

Assume your tool lives at `tool/calculator.py` within your project:

```python
# tool/calculator.py
import ast
import operator
from typing import Any
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def safe_arithmetic(expression: str) -> float:
    def _visit(node: ast.AST) -> float:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[type(node.op)](_visit(node.left), _visit(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[type(node.op)](_visit(node.operand))
        raise ValueError("Unsupported expression")

    parsed = ast.parse(expression, mode="eval")
    return _visit(parsed.body)

class CalculatorArgs(BaseModel):
    expression: str = Field(..., description="Arithmetic expression to evaluate")

class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Evaluates simple arithmetic expressions."
    args_schema = CalculatorArgs

    def _run(self, expression: str, **_: Any) -> str:
        try:
            return str(safe_arithmetic(expression))
        except ValueError:
            return "Only basic arithmetic expressions are supported."
```

You can then orchestrate it directly in your application. The SDK defaults to **local execution**, meaning `agent.run()` will execute the agent logic in your current environment using the `aip-agents` engine.

```python
# app.py
from glaip_sdk import Agent, Tool
from tool.calculator import CalculatorTool

agent = Agent(
    name="math-agent",
    instruction="You are a helpful math assistant",
    tools=[
        CalculatorTool,                # Custom tool (bundled automatically)
        Tool.from_native("time_tool"), # Native platform tool
    ],
)

agent.run("What is 2+2?")
```

### Complex Tool Logic

When a tool requires complex logic, you can organize it across multiple files for better maintainability. During agent deployment (using the **`Agent(tools=[...])`** pattern), the SDK's automatic bundler detects and includes local imports—such as helper functions, services, or schemas—from your project into the uploaded tool source.

**Example structure:**

```text
my_project/
  main.py
  tools/
    weather/
      __init__.py
      tool.py     # Exports WeatherTool
      service.py  # Contains helper logic
```

**Example `tools/weather/service.py`:**

```python
def get_mock_weather(city: str) -> str:
    return f"The weather in {city} is sunny."
```

**Example `tools/weather/tool.py`:**

```python
# Absolute import (recommended for portability)
from tools.weather.service import get_mock_weather
# OR Relative import (also supported)
# from .service import get_mock_weather

from langchain_core.tools import BaseTool

class WeatherTool(BaseTool):
    name = "weather_tool"
    description = "Gets weather info"

    def _run(self, city: str) -> str:
        # Bundler will include service.py automatically
        return get_mock_weather(city)
```

**Example `main.py`:**

```python
from glaip_sdk import Agent
from tools.weather.tool import WeatherTool

agent = Agent(
    name="weather-agent",
    instruction="Check the weather",
    tools=[WeatherTool],
)

agent.run("What's the weather in Tokyo?")
```

### Modular Tools (Multiple Files)

For complex projects, you can organize multiple modular tools across your project. The SDK correctly resolves absolute imports and bundles the entire dependency tree.

```python
from glaip_sdk import Agent
from tools.flight_status import FlightStatusTool
from tools.stock_checker import StockCheckerTool
from tools.weather import WeatherTool

agent = Agent(
    name="travel-assistant",
    instruction="Help users with travel planning",
    tools=[WeatherTool, FlightStatusTool, StockCheckerTool],
)

agent.run("Check flight GA123 and weather in Bali.")
```

Refer to the [Modular Tool Integration](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/modular-tool-integration) example in the Cookbook for a full working implementation.

{% hint style="info" %}
**Absolute vs Relative Imports**

The SDK bundler supports both styles. For portable examples in the [GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip), absolute imports (e.g., `from tools.weather.service import ...`) are used to ensure the tools work regardless of the user's local directory structure.
{% endhint %}

## Tool Implementation Expectations

When building custom tools for the AIP platform, ensure they meet the following technical requirements:

1. **BaseTool Inheritance**: All tools must inherit from LangChain's `BaseTool`.
1. **Metadata**: Tools must define `name` and `description` attributes.
1. **Schemas**: Tools must provide an `args_schema` (Pydantic model) for input validation.
1. **Standard I/O**: Runtime `stdout` and `stderr` are automatically captured and forwarded in the agent's event stream.

## Manage Tools

### Registry Operations

For interactive, low-code tool registry workflows, use the CLI pages:

- CLI tools guide: [CLI: Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/tools)
- CLI command reference: [CLI Commands Reference](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/cli-commands)

{% hint style="warning" %}
The `Client` examples in this section are legacy/advanced admin paths.
For day-to-day product code, keep the Agent-first path as your default.
{% endhint %}

For automation and governance in Python, use the SDK client:

```python
from glaip_sdk import Client

client = Client()

tools = client.tools.list_tools()
for tool in tools:
    print(tool.id, tool.name, tool.type)
```

REST endpoints are documented in the reference section only:

- REST reference: [Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/resources/reference/rest-api/tools)

#### Common errors and fixes

| Symptom                               | Likely cause                                             | Fix                                                                                                                |
| ------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `422 Unprocessable Entity` on upload  | Invalid metadata fields or missing BaseTool inheritance. | Validate the class inherits from LangChain BaseTool and includes required fields (name, description, args_schema). |
| CLI upload hangs after progress bar   | Large dependency bundle or slow network upload.          | Remove unused dependencies/assets and retry. For internal integrations only, see the REST tools reference.         |
| Agent cannot run the tool at runtime  | Tool not attached, or config missing required keys.      | Re-run `aip agents update --tools` and verify `tool_configs` in the agent payload.                                 |
| `401 Unauthorized` when listing tools | API key scoped to viewer-only role.                      | Request a creator or runner key, or perform the action via an operator account.                                    |

### GL Connectors and Managed Connectors

Remote-managed connectors (GL Connectors library) appear in the tool catalog with predefined IDs. Request enablement from the AIP operations team, then attach them like any other tool. Updates are handled centrally; monitor platform release notes and the [GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip) for refreshed implementation examples.

### Tool Resilience

Protect agents from external service outages with per-tool timeout guardrails, bounded retry backoff, and circuit breakers. Use this section when tools call external endpoints such as GL Connectors, MCP servers, or custom APIs that can hang, fail transiently, or stay unavailable for extended periods.

{% hint style="info" %}
Tool resilience is configured entirely through `tool_configs` on the Agent. No changes to tool source code are required. Timeout, retry, and circuit breaker are independent layers, so you can enable them separately or combine all three.
{% endhint %}

#### When to use tool resilience

| Situation | Recommended layer |
| --- | --- |
| Tool calls hang for minutes (for example a slow upstream service) | **Timeout** |
| Transient errors such as rate limits, short network blips, or 5xx spikes | **Retry** |
| A service stays down and you want fast-fail behavior until recovery | **Circuit breaker** |
| Production workloads exposed to all of the above | **Timeout + Retry + Circuit breaker** |

#### Timeout

Every tool invocation runs under a deadline. If the tool exceeds its configured timeout, the agent receives a structured error instead of hanging indefinitely.

**Default behavior:**
The default timeout is **60 seconds**. You get this protection automatically on every tool call.

**Override per tool:**

```python
from glaip_sdk import Agent
from tools.search import SearchTool

agent = Agent(
    name="search-agent",
    instruction="Search and summarise results.",
    tools=[SearchTool],
    tool_configs={
        SearchTool: {
            "resilience": {
                "timeout_seconds": 10.0,
            }
        }
    },
)

agent.run("Find the latest news on renewable energy.")
```

**Override at runtime:**
Pass `tool_timeout_seconds` in the tool's runtime metadata to override the configured value for a single invocation:

```python
agent.run(
    "Find recent papers on LLM alignment.",
    tool_metadata={
        "search_tool": {
            "tool_timeout_seconds": 5.0,
        }
    },
)
```

{% hint style="warning" %}
**Runtime override precedence:** `tool_timeout_seconds` in runtime metadata takes precedence over `tool_configs`. Invalid values (zero, negative, or non-numeric) are rejected and fail the call with a descriptive config error rather than silently falling back.
{% endhint %}

#### Retry

Enable retry to automatically re-attempt a failed tool call with exponential backoff. Retry is **disabled by default**.

**Basic retry setup:**

```python
from glaip_sdk import Agent
from tools.weather import WeatherTool

agent = Agent(
    name="weather-agent",
    instruction="Provide weather forecasts.",
    tools=[WeatherTool],
    tool_configs={
        WeatherTool: {
            "resilience": {
                "timeout_seconds": 15.0,
                "retry": {
                    "enabled": True,
                    "max_attempts": 3,
                    "backoff_min_seconds": 1.0,
                    "backoff_max_seconds": 8.0,
                },
            }
        }
    },
)
```

**Retryable error kinds:**
By default, these error categories trigger a retry:

| Error kind | Description |
| --- | --- |
| `timeout` | Tool call exceeded its deadline |
| `connection_error` | TCP or socket connection failure |
| `endpoint_unreachable` | DNS or routing failure |
| `upstream_5xx` | HTTP 5xx response from the upstream service |
| `rate_limited` | HTTP 429 response from the upstream service |

Authorization errors such as `unauthorized` and `forbidden` are **never retried** because they require operator action, not a retry loop.

{% hint style="info" %}
**Retry budget:** The total retry duration is capped by the tool's `timeout_seconds`. If starting another attempt would exceed the deadline, that attempt is skipped and the agent receives a `retry_exhausted` error.
{% endhint %}

#### Circuit breaker

The circuit breaker prevents repeated calls to a service that is already known to be down, returning fast-fail errors until the service recovers. Circuit breaking is **disabled by default**.

**How it works:**

| State | Behavior |
| --- | --- |
| **Closed** (normal) | Calls are allowed through and failures are counted |
| **Open** (tripped) | Calls fail immediately without contacting the service |
| **Half-open** (probing) | One probe call is allowed; success closes the circuit and failure reopens it |

**Basic circuit breaker setup:**

```python
from glaip_sdk import Agent
from tools.inventory import InventoryTool

agent = Agent(
    name="inventory-agent",
    instruction="Query product inventory.",
    tools=[InventoryTool],
    tool_configs={
        InventoryTool: {
            "resilience": {
                "timeout_seconds": 10.0,
                "circuit_breaker": {
                    "enabled": True,
                    "fail_max": 5,
                    "reset_timeout_seconds": 60.0,
                    "half_open_max_calls": 1,
                },
            }
        }
    },
)
```

**Configuration reference:**

| Key | Default | Description |
| --- | --- | --- |
| `fail_max` | `5` | Number of consecutive failures that trip the circuit open |
| `reset_timeout_seconds` | `60.0` | Seconds to wait in open state before probing with a half-open call |
| `half_open_max_calls` | `1` | Maximum concurrent probe calls allowed in half-open state |

{% hint style="warning" %}
**Policy changes reset the breaker:** If you change `fail_max` or `reset_timeout_seconds` for a tool that already has an open circuit, the breaker resets to the closed state with the new policy. This is intentional because a policy change implies an explicit operator decision.
{% endhint %}

#### Combining all three layers

For production workloads that call external services, combine timeout, retry, and circuit breaker:

```python
from glaip_sdk import Agent
from tools.meemo import MeemoTool

agent = Agent(
    name="meemo-agent",
    instruction="Query the Meemo knowledge service.",
    tools=[MeemoTool],
    tool_configs={
        MeemoTool: {
            "resilience": {
                "timeout_seconds": 10.0,
                "retry": {
                    "enabled": True,
                    "max_attempts": 3,
                    "backoff_min_seconds": 1.0,
                    "backoff_max_seconds": 8.0,
                },
                "circuit_breaker": {
                    "enabled": True,
                    "fail_max": 5,
                    "reset_timeout_seconds": 60.0,
                    "half_open_max_calls": 1,
                },
            }
        }
    },
)

agent.run("Summarise the onboarding documentation.")
```

**Execution order per attempt:**

1. Circuit breaker checks whether the call is allowed and fast-fails if open.
1. The tool executes under the configured timeout deadline.
1. On failure, the SDK classifies the error kind.
1. If the error is retryable and budget remains, the next attempt starts from step 1.
1. On retry exhaustion or a non-retryable error, the circuit breaker records the failure.

#### Observability

Each tool response includes a `metadata.tool_execution` field with resilience diagnostics:

```json
{
  "result": "Tool call failed: circuit breaker is open",
  "metadata": {
    "tool_execution": {
      "category": "circuit_open",
      "circuit_state": "open",
      "last_error_kind": "endpoint_unreachable",
      "circuit_opened_at_unix_seconds": 1740654823.4,
      "circuit_reset_timeout_seconds": 60.0,
      "consecutive_failures": 5
    }
  }
}
```

### MCP Tool Discovery

Use the SDK to inspect tools exposed by an MCP:

```python
from glaip_sdk import Client

client = Client()
tools = client.mcps.get_mcp_tools("mcp-id")
print([t.get("name") for t in tools])
```

Use the response to seed agent definitions or generate tool uploads where appropriate. The [MCP guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/mcps) covers credential rotation and live connection testing in detail.

### Observability and Auditing

1. Use `aip tools get <TOOL_REF>` (or [CLI: Tools](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/cli/commands/tools)) to inspect tool metadata.
1. Use `aip agents list` to locate agents that reference a tool by name or by inspection.
1. Use the [Configuration management guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/configuration-management) to export/import tools alongside agents for promotion pipelines.

### Best Practices

1. **Version your uploads** — keep source code in git and re-upload on change.
1. **Scope permissions** — custom tools run with the same rights as the agent execution environment; follow least-privilege principles.
1. **Validate inputs** — handle argument validation inside the tool to avoid unexpected failures mid-run.
1. **Set resilience policies for remote dependencies** — use timeout, retry, and circuit breaker for tools that call external services.
1. **Document configs** — record supported configuration keys in your README so teammates know how to set `tool_configs`.

## Production Readiness Checklist

Before deploying tools to production:

- [ ] All tools have required attributes: `name`, `description`, and `args_schema`
- [ ] Error handling is comprehensive in `_run()` methods
- [ ] Dependencies are minimal and well-documented
- [ ] Tool configs are documented in README
- [ ] External-facing tools have an explicit resilience policy
- [ ] Tools are tested with various input scenarios
- [ ] Source code is versioned in git
- [ ] Tool follows BaseTool inheritance pattern (no decorator needed)

### Related Documentation

1. [Agents guide](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agents) — attach tools, manage `tool_configs`, and run overrides.
1. [File processing](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/file-processing) — upload artifacts during agent runs and reuse chunk IDs.
1. [Automation & scripting](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/automation-and-scripting) — script tool creation and promotion in CI.
