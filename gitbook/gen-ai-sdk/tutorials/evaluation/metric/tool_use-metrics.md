# Tool Use Metrics

## Tool Use Metrics

Tool use metrics evaluate the behavior of AI agents — whether they followed the right sequence of actions, selected the correct tools, and used them with correct parameters.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/metrics/tool_use" %}

{% hint style="info" %}
All examples use `LLMTestCase` as the input type. See Getting Started for the full list of available fields.
{% endhint %}

***

## DeepEvalToolCorrectnessMetric

> **Method:** Combined | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [DeepEvalToolCorrectnessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalToolCorrectnessMetric)

Evaluates whether the agent selected and called the correct tools for the user query. Compares `tools_called` against `expected_tools`. Supports configurable matching modes — you can require exact argument matching, output matching, strict call ordering, or a subset match.

**When to use:**

* When you need to evaluate whether an agent selected the correct tools for a user query.
* When tool-call arguments, outputs, exact matching, or call ordering matter to correctness.
* When actual and expected tool usage can be supplied directly or extracted from `agent_trajectory` and `expected_agent_trajectory`.
* When `available_tools` context is important for judging whether a tool choice was appropriate.

**Required fields:** `input`, `tools_called`, `expected_tools`

{% hint style="info" %}
If `tools_called` is not provided, it will be automatically extracted from `agent_trajectory`. Similarly, `expected_tools` can be extracted from `expected_agent_trajectory`.
{% endhint %}

**Constructor parameters:**

* `model` (default: `"google/gemini-3-flash-preview"`) — model identifier string
* `model_credentials` — API key string. default retrieved from env variable `GOOGLE_API_KEY`
* `threshold` (float, default: `0.5`) — passing threshold between 0-1 that classifies tool calls as good/bad
* `strict_mode` (bool, default: `False`) — if True, scores return as 0 or 1
* `should_exact_match` (`bool`, default: `False`) — require exact tool argument matching
* `should_consider_ordering` (`bool`, default: `False`) — require tools to be called in the correct order
* `available_tools` (`list | None`) — list of all tools available to the agent, used as context for judgment
* `evaluation_params` (list\[str]) — parameters in a tool call to be evaluated (defaults to `args` and `output`)
* `include_reason` (bool, default: `True`) — include explanation in the scoring result

**Example:**

```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.metrics import DeepEvalToolCorrectnessMetric
from gllm_evals.types import ToolCall

async def main():
    metric = DeepEvalToolCorrectnessMetric(
        should_consider_ordering=True,
    )
    data = LLMTestCase(
        input="What is the weather in Singapore today?",
        actual_output="The weather in Singapore is sunny, 30°C.",
        tools_called=[
            ToolCall(
                name="get_weather",
                input_parameters={"city": "Singapore"},
            )
        ],
        expected_tools=[
            ToolCall(
                name="get_weather",
                input_parameters={"city": "Singapore"},
            )
        ],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

{% hint style="info" %}
For information about the `ToolCall` type structure used in `tools_called` and `expected_tools`, see [LLMTestCase - ToolCall Type](../llmtestcase.md#toolcall-type).
{% endhint %}

### Agent Trajectory Structure

The agent trajectory provided to `agent_trajectory` and `expected_agent_trajectory` is a list of dictionaries with different role types:

* **user**: The user asking a question
* **assistant**: The agent responding or calling a tool
* **tool**: The tool being called

Each dictionary represents a chat message for each role:

* **role**: The role of the message sender
* **content**: The message sent
* **tool\_calls**: List of tools called (exclusive to role assistant)
* **tool\_call\_id**: The identifier of the tool call result (should reflect the tool called by assistant, exclusive to role tool)

**Example:**

```json
[
  {
    "role": "user",
    "content": "What's the weather in Tokyo?"
  },
  {
    "role": "assistant",
    "content": "",
    "tool_calls": [
      {
        "id": "call_4",
        "type": "function",
        "function": {
          "name": "weather_search",
          "arguments": "{\"location\": \"Tokyo\"}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "tool_call_id": "call_4",
    "content": "{\"temperature\": 22, \"condition\": \"sunny\"}"
  },
  {
    "role": "assistant",
    "content": "It's 22 degrees and sunny in Tokyo."
  }
]
```

### Using Available Tools for Tool Correctness

By default, the tool correctness metric evaluates whether the agent called the right tools by comparing to the reference. However, providing `available_tools` context significantly improves evaluation accuracy by evaluating with LLM if the tools provided to the agent are the most appropriate.

### Why Provide Available Tools?

Without `available_tools`, the evaluator can only assess if the called tools match the expected tools. With `available_tools`, the evaluator can also judge:

* Whether the agent selected the most appropriate tool from available options
* If the agent missed better tool alternatives
* Context-aware reasoning about tool selection

### Tool Schema

Tool Schema are dictionaries that define tools available to the agent. Each tool schema should have at least name, description, and parameters.

```json
[
  {
    "name": "calculator",
    "description": "Perform mathematical calculations and computations",
    "parameters": {
      "type": "object",
      "properties": {
        "expression": {
          "type": "string",
          "description": "Mathematical expression to evaluate"
        }
      },
      "required": ["expression"]
    }
  },
  {
    "name": "weather_search",
    "description": "Get weather information for a specific location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The location to get weather for"
        }
      },
      "required": ["location"]
    }
  }
]
```

### How to Use

To use tool schema as `available_tools`, load the tool schemas and feed it to the `available_tools` parameter on `DeepEvalToolCorrectnessMetric`:

```python
from gllm_evals.metrics import DeepEvalToolCorrectnessMetric
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_tool_schema
from gllm_evals.types import ToolCall

# Load tool schema
available_tools = load_tool_schema()

# Configure tool correctness metric with available tools
metric = DeepEvalToolCorrectnessMetric(
    available_tools=available_tools,  # Provide tool context
)

data = LLMTestCase(
    input="Calculate 2 + 2",
    actual_output="The result is 4",
    tools_called=[
        ToolCall(
            name="calculator",
            input_parameters={"expression": "2 + 2"},
        )
    ],
    expected_tools=[
        ToolCall(
            name="calculator",
            input_parameters={"expression": "2 + 2"},
        )
    ],
)
result = await metric.evaluate(data)
```

{% hint style="info" %}
`DeepEvalToolCorrectnessMetric` will compare the tool selection score against `available_tools` and the comparison score between the tool calls to the reference. The final result returned will be the lowest between both scores.
{% endhint %}

***

## LangChainAgentTrajectoryAccuracyMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [LangChainAgentTrajectoryAccuracyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.LangChainAgentTrajectoryAccuracyMetric)

Evaluates whether an agent followed the right multi-step trajectory to complete a task. By default it judges the trajectory without a reference (`use_reference=False`). Pass `use_reference=True` and supply `expected_agent_trajectory` to compare against a gold trajectory.

**When to use:**

* When evaluating whether an agent followed the right multi-step trajectory.
* When you have an `agent_trajectory` and optionally an `expected_agent_trajectory` to compare against.
* When the quality question is about the sequence of decisions and actions, not just the final answer.
* When you want either reference-based trajectory evaluation or a custom prompt-based judgment without a reference.

**Required fields:** `agent_trajectory`

**Optional fields:** `expected_agent_trajectory` (when `use_reference=True`)

**Constructor parameters:**

* `model` (required) — model identifier string (recommended: `"google/gemini-3-flash-preview"`)
* `model_credentials` — API key string. default retrieved from env variable `GOOGLE_API_KEY`
* `use_reference` (`bool`, default: `True`) — if `True`, compares against `expected_agent_trajectory`
* `continuous` (`bool`, default: `False`) — if `True`, score will return as float between 0-1
* `use_reasoning` (`bool`, default: `True`) — if `True`, explanation will be included in the output
* `few_shot_examples` (list\[FewShotExample], optional) — list of few-shot examples provided as context

{% hint style="warning" %}
Using `LangChainAgentTrajectoryAccuracyMetric` may be costly as it will compare the full trajectory and the referenced trajectory that are relatively long.
{% endhint %}

**Example:**

```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.metrics import LangChainAgentTrajectoryAccuracyMetric

async def main():
    metric = LangChainAgentTrajectoryAccuracyMetric()
    data = LLMTestCase(
        input="Book a flight from Jakarta to Singapore on Friday.",
        actual_output="I have booked your flight.",
        agent_trajectory=[
            {"tool": "search_flights", "input": {"from": "Jakarta", "to": "Singapore", "date": "Friday"}},
            {"tool": "book_flight", "input": {"flight_id": "GA123"}},
        ],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
