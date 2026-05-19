# 🎯 Evaluator

An **Evaluator** orchestrates evaluation workflows by coordinating metrics and evaluation logic. All evaluators inherit from `BaseEvaluator` and share a common aggregation layer:

* Executes relevant metrics (parallel or sequential)
* Aggregates results via [`MetricsAggregator`](metrics-aggregator.md) — computes `aggregate_success` (AND-gate: all metrics must pass) and `aggregate_score` (polarity-aware mean)
* Generates human-readable `aggregate_explanation`

### Input & Output Types

Evaluators accept either dictionaries or `LLMTestCase` objects as input data.

**Example Input**

```python
from gllm_evals.types import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    expected_output="Paris",
    actual_output="New York",
    retrieved_context="Paris is the capital of France.",
)
```

While Evaluator outputs an `EvaluatorResult` that includes several keys such as `aggregate_explanation` , `score`, and namespaced metrics result.

**Example Output**

```json
{
  "generation": {
    "aggregate_explanation": "The following metrics failed to meet expectations:\n1. Completeness is 0 (should be >= 1)\n2. Groundedness is 0 (should be >= 1)",
    "aggregate_success": false,
    "aggregate_score": 0.0,
    "completeness": {
      "score": 0.0,
      "explanation": "The minimum key facts are: [A] Paris. The Generated Response provides 'New York', which directly contradicts the expected key fact. Per the Contradiction Rule in Step 5A, any contradiction of a minimum key fact results in the lowest score. Additionally, per the Coverage Rule in Step 5C, the response fails to provide the correct information.",
      "rubric_score": 1,
      "success": false,
      "threshold": 1.0,
      "strict_mode": false,
      "higher_is_better": true,
      "model_id": "google/gemini-3-flash-preview"
    },
    "redundancy": {
      "score": 0.0,
      "explanation": "The response is a brief, direct answer that provides the information exactly once. There are no repeated words, phrases, or paraphrased ideas, resulting in no redundancy.",
      "rubric_score": 1,
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": false,
      "model_id": "google/gemini-3-flash-preview"
    },
    "groundedness": {
      "score": 0.0,
      "explanation": "The response identifies New York as the capital of France, which is a critical factual contradiction of the provided context stating that Paris is the capital.",
      "rubric_score": 1,
      "success": false,
      "threshold": 1.0,
      "strict_mode": false,
      "higher_is_better": true,
      "model_id": "google/gemini-3-flash-preview"
    },
    "is_refusal": false
  }
}
```

## Single vs Batch Evaluation

Evaluators support both modes via the same `evaluate()` method:

Single Evaluation

```python
result : EvaluatorResult = await evaluator.evaluate(data)
```

Batch Evaluation

```python
results : list[EvaluatorResult]= await evaluator.evaluate([data1, data2, data3])
```

### Initialization & Common Parameters

All evaluators accept:

* `models`: `BaseLMInvoker | list[BaseLMInvoker] | None`
  * **`None`** (default): single-judge mode using the default invoker (`google/gemini-3-flash-preview`).
  * **Single `BaseLMInvoker`**: runs that judge once.
  * **`[invoker] * N`**: homogeneous multi-judge — same model invoked N times, results aggregated.
  * **`[invoker_a, invoker_b, ...]`**: heterogeneous multi-judge — distinct models, results aggregated.
  * Build invokers via `gllm_inference.lm_invoker.build_lm_invoker`. See [**Language Model (LM) Invoker**](https://gdplabs.gitbook.io/sdk/tutorials/inference/lm-invoker) for supported invokers.

#### Example Usage — Using OpenAIChatCompletionsLMInvoker

```python
import asyncio
import os

from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase
from gllm_inference.lm_invoker import OpenAIChatCompletionsLMInvoker


async def main():
    """Main function."""
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )

    lm_invoker = OpenAIChatCompletionsLMInvoker(
        base_url="https://abc-vllm.obrol.id/ ",
        model_name="Qwen/Qwen3-Next-80B-A3B-Instruct",
        api_key="abc123",
    )

    evaluator = GEvalGenerationEvaluator(model=lm_invoker)

    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

{% hint style="info" %}
`OpenAICompatibleLMInvoker` was removed in v0.6. Use `OpenAIChatCompletionsLMInvoker` with a `base_url` parameter to connect to OpenAI Chat Completions API-compatible providers.
{% endhint %}

## Available Evaluators

1. [GEvalGenerationEvaluator](gevalgenerationevaluator.md)
2. [AgentEvaluator](/broken/pages/CjbT4DD9NOnbL2INo2TD)
3. [ClassicalRetrievalEvaluator](classicalretrievalevaluator.md)
4. [LMBasedRetrievalEvaluator](lmbasedretrievalevaluator.md)
5. [QueryTransformerEvaluator](querytransformerevaluator.md)
6. [SummarizationEvaluator](summarizationevaluator.md)
7. [CompositeEvaluator](composite-evaluator.md)

***

Looking for something else? [Build your own custom evaluator here.](create-custom-evaluator-scorer.md)

<sup>\*All fields are optional and can be adjusted depending on the chosen metric.</sup>
