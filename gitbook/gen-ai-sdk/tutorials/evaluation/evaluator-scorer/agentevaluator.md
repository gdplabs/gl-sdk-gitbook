# AgentEvaluator

### Overview

**Use when**: You want to evaluate AI agent's overall performance, including tool usage and the quality of the agent’s outputs. This evaluator also uses GEvalGenerationEvaluator as the agent output quality evaluator. Additionally this evaluator uses DeepEval Tool Correctness metric for tool call evaluation.

#### Fields

1. **input** (str) — The question given by the user to the agent.
2. **actual\_output** (str) — The agent's output to be evaluated.
3. **expected\_output** (str, optional) — The reference or ground truth answer.
4. **tools\_called** (list\[dict\[str, Any]], optional) — The list of actual tools called by the agent
5. **expected\_tools** (list\[dict\[str, Any]], optional) — The list of the tools expected to be called by the as reference for comparison.
6. **agent\_trajectory** (list\[dict\[str, Any]], optional) — The actual agent trajectory to be evaluated. If `tools_called` are not provided, the `agent_trajectory` will be parsed as `tools_called`
7. **expected\_agent\_trajectory** (list\[dict\[str, Any]], optional) — The reference trajectory for comparison. If `expected_tools` are not provided, the `expected_agent_trajectory` will be parsed as `expected_tools`.

{% hint style="info" %}
Canonical field names follow `LLMTestCase` (`input`, `actual_output`, `expected_output`). Legacy aliases such as `query`, `generated_response`, and `expected_response` may still appear in existing datasets and examples.
{% endhint %}

#### Configuration Options

* **tool\_correctness\_metric** (DeepEvalToolCorrectnessMetric): This configuration allows providing configured DeepEvalToolCorrectnessMetric that will be used to evaluate agent tool calls. If not provided, a default Tool Correctness Metric will be used.
* **generation\_evaluator** (GEvalGenerationEvaluator): This configuration allows configuring GEvalGenerationEvaluator that will be used to evaluate agent output quality. If not provided, a default GEvalGenerationEvaluator will be used.
* **trajectory\_accuracy\_metric** (LangChainAgentTrajectoryAccuracyMetric): This configuration allows enabling agent trajectory evaluation. If not provided, this metric will not be used (disabled by default)

For more information about the metrics configuration, see Metric.

#### Output

AgentEvaluator outputs the scores of each metric individually. The following aggregated fields are also provided at the top level:

* **aggregate\_success** (`bool`): `True` if **all** enabled metrics passed (AND-gate across tool correctness and all generation metrics).
* **aggregate\_score** (`float`): Polarity-aware mean score across tool correctness and generation metrics.
* **possible\_issues** (`list[str]`): Issue labels for failed components — `"Tool Call Issue"` when tool correctness is below threshold, `"Retrieval Issue"` / `"Generation Issue"` from the nested generation evaluator.

The nested `generation` key follows the same output structure as GEvalGenerationEvaluator (with its own `aggregate_success`, `aggregate_score`, `possible_issues`, and per-metric results).

The `langchain_agent_trajectory_accuracy` key is included only when `trajectory_accuracy_metric` is configured and `agent_trajectory` is present in the input. Its result does **not** affect the top-level aggregation.

#### Example Usage

```python
import asyncio
import json

from gllm_evals import LLMTestCase
from gllm_evals.dataset import load_simple_agent_tool_call_dataset
from gllm_evals.evaluator.agent_evaluator import AgentEvaluator


async def main():
    """Main function."""
    raw = load_simple_agent_tool_call_dataset()
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=row["generated_response"],
            expected_output=row["expected_response"],
            tools_called=row.get("tools_called"),
            expected_tools=row.get("expected_tools"),
            agent_trajectory=row.get("agent_trajectory"),
            expected_agent_trajectory=row.get("expected_agent_trajectory"),
        )
        for row in raw.load()
    ]

    evaluator = AgentEvaluator()

    result = await evaluator.evaluate(data[0])
    print(result)


if __name__ == "__main__":
    asyncio.run(main())

```

#### Example Output

```json
{
  "agent_evals": {
    "aggregate_explanation": "The following metrics failed to meet expectations:\n1. Deepeval Tool Correctness score 0.00 (threshold: 0.50)",
    "aggregate_success": false,
    "aggregate_score": 0.5,
    "possible_issues": ["Tool Call Issue"],
    "deepeval_tool_correctness": {
      "score": 0.0,
      "explanation": "[\n\t Tool Calling Reason: Incomplete tool usage: missing tools [ToolCall(\n    name=\"data_checker\",\n    input_parameters={\n        \"query\": \"SELECT AVG(amount) as avg_sales FROM orders LIMIT 1\"\n    },\n    output='[{\"avg_sales\": 250.50}]'\n)]; expected ['data_checker'], called ['wrong_tool_name']. See more details above.\n\t Tool Selection Reason: No available tools were provided to assess tool selection criteria\n]\n",
      "success": false,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "generation": {
      "aggregate_explanation": "All metrics met the expected values.",
      "aggregate_success": true,
      "aggregate_score": 1.0,
      "possible_issues": [],
      "completeness": {
        "score": 1.0,
        "rubric_score": 3,
        "explanation": "The response accurately identifies the average sales amount as $250.50, matching the numeric value in the expected output exactly.",
        "success": true,
        "threshold": 0.5,
        "strict_mode": false,
        "higher_is_better": true
      },
      "redundancy": {
        "score": 0.0,
        "rubric_score": 1,
        "explanation": "The response is concise and directly answers the question without any repetition.",
        "success": true,
        "threshold": 0.4,
        "strict_mode": false,
        "higher_is_better": false
      }
    }
  }
}
```

{% hint style="info" %}
For detailed information about tools structure, agent trajectory structure, and metric configuration parameters, see Tool Use Metrics.
{% endhint %}
