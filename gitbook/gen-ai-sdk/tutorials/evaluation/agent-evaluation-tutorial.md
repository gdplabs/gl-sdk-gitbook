---
hidden: true
---

# 🤖 Agent Evaluation Tutorial

This guide shows how to evaluate AI agent trajectories using **gllm-evals**. To perform agent evaluation, use the [`AgentEvaluator`](evaluator/#agentevaluator) to assess agent performance. `AgentEvaluator` combines tool correctness assessment with generation quality evaluation and provides flexible configuration options. Results can also be monitored via Langfuse. for more details about Langfuse, check out [Langfuse Experiment Tracker](experiment-tracker.md#langfuseexperimenttracker).

## Prerequisites

Before you can start evaluating AI agent, prepare the following:

* **Install the Required Libraries**

```bash
pip install gllm-evals[deepeval,langchain]
```

* **Setup Environment and Configuration**

```bash
# OpenAI API Key & Google API Key for evaluation models
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

* **Prepare Dataset**

**Input Fields**

* `input`
* `actual_output`
* `expected_output`
* `tools_called` _(optional)_
* `expected_tools` _(optional)_
* `agent_trajectory` _(optional)_
* `expected_agent_trajectory` _(optional)_

**Example Dataset Structure (with Tool Calls)**

```json
{
    "question_id": "4",
    "input": "Send an email to john@example.com about the meeting",
    "actual_output": "Email sent successfully to jane@example.com",
    "expected_output": "Email has been sent to john@example.com regarding the meeting.",
    "tools_called": [
      {
        "name": "send_email",
        "args": {
          "to": "jane@example.com",
          "subject": "Meeting",
          "body": "This is a reminder about our upcoming meeting."
        },
        "output": "{\"status\": \"sent\"}"
      }
    ],
    "expected_tools": [
      {
        "name": "send_email",
        "args": {
          "to": "john@example.com",
          "subject": "Meeting",
          "body": "This is a reminder about our upcoming meeting."
        },
        "output": "{\"status\": \"sent\"}"
      }
    ]
  }
```

**Example Dataset Structure (with Agent Trajectory)**

```json
{
    "question_id": "1",
    "input": "What is 15 plus 27?",
    "actual_output": "15 plus 27 equals 42.",
    "expected_output": "15 plus 27 equals 42.",
    "agent_trajectory": [
      {
        "role": "user",
        "content": "What is 15 plus 27?"
      },
      {
        "role": "assistant",
        "content": "",
        "tool_calls": [
          {
            "id": "call_2",
            "type": "function",
            "function": {
              "name": "calculator",
              "arguments": "{\"expression\": \"15 + 27\"}"
            }
          }
        ]
      },
      {
        "role": "tool",
        "tool_call_id": "call_2",
        "content": "42"
      },
      {
        "role": "assistant",
        "content": "15 plus 27 equals 42."
      }
    ],
    "expected_agent_trajectory": [
      {
        "role": "user",
        "content": "What is 15 plus 27?"
      },
      {
        "role": "assistant",
        "content": "",
        "tool_calls": [
          {
            "id": "call_2",
            "type": "function",
            "function": {
              "name": "calculator",
              "arguments": "{\"expression\": \"15 + 27\"}"
            }
          }
        ]
      },
      {
        "role": "tool",
        "tool_call_id": "call_2",
        "content": "42"
      },
      {
        "role": "assistant",
        "content": "15 plus 27 equals 42."
      }
    ]
  },
```

## Evaluating Agent

{% stepper %}
{% step %}
**Configure the AgentEvaluator**

By default, `AgentEvaluator` already construct `DeepEvalToolCorrectnessMetric` and `GEvalGenerationEvaluator` to be used.

```python
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator

evaluator = AgentEvaluator()
```
{% endstep %}

{% step %}
**Load and Prepare Your Dataset**

```python
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset

dataset = load_simple_agent_tool_call_dataset()
```
{% endstep %}

{% step %}
**Run the Evaluation**

```python
import asyncio

async def main():
    dataset = load_simple_agent_tool_call_dataset()
    evaluator = AgentEvaluator()
    result = await evaluator.evaluate(dataset[0])
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
{% endstep %}

{% step %}
**Using Evaluate Helper Function**

```python
import asyncio
import json

from gllm_evals.dataset.simple_agent_tool_call_dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluate import evaluate
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator


async def main():
    dataset = load_simple_agent_tool_call_dataset()

    results = await evaluate(
        data=dataset,
        evaluators=[AgentEvaluator()],
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(main())

```
{% endstep %}
{% endstepper %}

## Customizing Tool Correctness Parameters

`DeepevalToolCorrectnessMetric` supports various parameters to configure the behavior of the metric. Below are the parameters that are configureable:

* **threshold** (float): passing threshold between 0-1 that classify tool calls as good/bad. Defaults to 0.5
* **model** (str): Model used for evaluation, this model will only be used if `available_tools` is provided.
* **model\_credentials** (str): API Key for the model used for evaluation
* **available\_tools** (list\[dict], optional): list of tools schema/definition that are allowed to be called by the agent evaluated
* **strict\_mode** (bool): If True, scores return as 0 or 1. Default to False
* **should\_exact\_match** (bool): If True, requires each tool call in actual and reference to be exact match in tool name, argument, and output. Defaults to False
* **should\_consider\_ordering** (bool): If True, ordering of the tools will be considered in the evaluation. Defaults to False
* **evaluation\_params** (list\[str]): The parameters in a tool call to be evaluated. Defaults to evalaute tool calls input parameter (`args`) and output (`output`). This will only be evaluated if the data is present.
* **include\_reason** (bool): Include explanation in the scoring result. Defaults to True

For more details about DeepEvalToolCorrectnessMetric, see [here](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-evals/gllm_evals/metrics/agent/deepeval_tool_correctness.py).

## Using Available Tools for Tool Correctness

By default, the tool correctness metric evaluates whether the agent called the right tools by comparing to the reference. However, providing `available_tools` context significantly improves evaluation accuracy by evaluating with LLM if the tools provided to the agent are the most fit.

### Why Provide Available Tools?

Without `available_tools`, the evaluator can only assess if the called tools match the expected tools. With `available_tools`, the evaluator can also judge:

* Whether the agent selected the most appropriate tool from available options
* If the agent missed better tool alternatives
* Context-aware reasoning about tool selection

### Tool Schema

Tool Schema are dictionary that defines tools that are available to use by the agent. Each tool schema should have at least name, description, parameters that are accepted.

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

### How to use

To use tool schema as `available_tools` you only need to load the tool schemas and feed it to `available_tools` parameter on `DeepEvalToolCorrectnessMetric`.

```python
from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.metrics.agent.deepeval_tool_correctness import DeepEvalToolCorrectnessMetric
from gllm_evals.dataset.simple_agent_tool_call_dataset import load_tool_schema

# Load tool schema
available_tools = load_tool_schema()

# Configure tool correctness metric with available tools
tool_correctness = DeepEvalToolCorrectnessMetric(
    model=DefaultValues.AGENT_EVALS_MODEL,
    model_credentials=os.getenv("OPENAI_API_KEY"),
    available_tools=available_tools,  # Provide tool context
)

# Create evaluator
evaluator = AgentEvaluator(
    tool_correctness_metric=tool_correctness,
)
```

{% hint style="info" %}
`DeepEvalToolCorrectnessMetric` will compare the tool selection score compared to `available_tools` and the comparison score between the tool calls to the reference. The final result returned will be the lowest between both score.
{% endhint %}

## Enabling Langchain Agent Trajectory Evaluator

The trajectory accuracy metric evaluates the agent's full trajectory using LangChain's agentevals approach. It's **disabled by default** and only runs when `LangChainAgentTrajectoryAccuracyMetric` is provided `agent_trajectory` to the AgentEvaluator. using `LangChainAgentTrajectoryAccuracyMetric` requires you to provide `agent_trajectory` and `expected_agent_trajectory`.

Agent Trajectory Evaluator will not affect the final score of AgentEvaluator and purely used to evaluate the trajectory only.

{% hint style="warning" %}
Using `LangChainAgentTrajectoryAccuracyMetric` may be costly as it will compare the full trajectory and the referenced trajectory that are relatively long.
{% endhint %}

```python
from gllm_evals.constant import DefaultValues
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator
from gllm_evals.metrics import LangChainAgentTrajectoryAccuracyMetric # ADD

trajectory_accuracy = LangChainAgentTrajectoryAccuracyMetric(
    model=DefaultValues.AGENT_EVALS_MODEL,
    model_credentials=os.getenv("OPENAI_API_KEY"),
)
evaluator = AgentEvaluator(
    trajectory_accuracy_metric=trajectory_accuracy
)
```

There are several configuration can be done to `LangChainAgentTrajectoryAccuracyMetric` via constructor, thus:

* **model** (str): Model used for evaluation. Current recommended model for Agent Trajectory evaluator is `gpt-4.1`
* **model\_credentials** (str): the API Key for the models provided
* **use\_reference** (bool): if True, it will compare agent trajectory to the reference in the expected agent trajectory. If False, the evaluation over the agent trajectory will not use the expected agent trajectory. Defaults to True
* **continuous** (bool): If True, score will return as float between 0 - 1. Defaults to False
* **use\_reasoning** (bool): If True, explanation will be included in the output
* **few\_shot\_examples** (list\[FewShotExample], optional): list of few shot examples that will be provided as context

For more details on LangChainAgentTrajectoryAccuracyMetric, please see [here](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-evals/gllm_evals/metrics/agent/langchain_agent_trajectory_accuracy.py).
