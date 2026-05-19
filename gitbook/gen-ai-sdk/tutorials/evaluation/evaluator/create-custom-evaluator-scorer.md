# Create Custom Evaluator

If the built-in evaluators don't cover your use case, there are two paths:

* **Compose existing metrics** via `CompositeEvaluator` — covers the vast majority of needs without writing new evaluation logic.
* **Subclass `BaseEvaluator`** — for advanced patterns like short-circuit evaluation or fully custom metric logic.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/evaluator/create_custom_evaluator" %}

{% hint style="info" %}
All examples use `LLMTestCase` as the input type. See Getting Started for the full list of available fields.
{% endhint %}

***

### 1. Use CompositeEvaluator (Recommended)

`CompositeEvaluator` runs multiple metrics and aggregates their results into a unified report. It handles parallel/sequential execution, fault isolation, and polarity-aware scoring — no need to write evaluation orchestration yourself.

#### Key Features

* **Parallel or sequential execution** — run metrics concurrently (faster) or in order (predictable)
* **Result aggregation** — combines all metric outputs with `aggregate_success` and `aggregate_score`
* **Fault isolation** — if one metric fails, others continue executing
* **Flexible composition** — mix metrics from different categories (Generation, Retrieval, Safety, Tool Use)

#### Example Usage

```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.composite_evaluator import CompositeEvaluator
from gllm_evals.metrics import (
    GEvalCompletenessMetric,
    GEvalGroundednessMetric,
    DeepEvalAnswerRelevancyMetric,
)

async def main():
    completeness = GEvalCompletenessMetric()
    groundedness = GEvalGroundednessMetric()
    relevancy = DeepEvalAnswerRelevancyMetric()

    evaluator = CompositeEvaluator(
        metrics=[completeness, groundedness, relevancy],
        name="generation_quality",
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital city of France.",
        expected_output="Paris is the capital of France.",
        retrieved_context=["Paris is the capital city of France."],
    )
    result = await evaluator.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Example Output

```python
{
    "generation_quality": {
        "aggregate_explanation": "All metrics met the expected values.",
        "aggregate_success": True,
        "aggregate_score": 0.98,
        "completeness": {
            "score": 1.0,
            "explanation": "The response covers all key facts...",
            "rubric_score": 3,
            "success": True,
            "threshold": 0.5,
            "strict_mode": False,
            "higher_is_better": True,
        },
        "groundedness": {
            "score": 0.95,
            "explanation": "The response is well-grounded...",
            "rubric_score": 3,
            "success": True,
            "threshold": 0.5,
            "strict_mode": False,
            "higher_is_better": True,
        },
        "answer_relevancy": {
            "score": 1.0,
            "explanation": "The answer directly addresses the query...",
            "rubric_score": 1,
            "success": True,
            "threshold": 0.5,
            "strict_mode": False,
            "higher_is_better": True,
        },
    }
}
```

For full details, see [Composite Evaluator](composite-evaluator.md).

***

### 2. Extend BaseEvaluator (Advanced)

Subclass `BaseEvaluator` when `CompositeEvaluator` is insufficient. Two concrete cases:

| Scenario                          | Why CompositeEvaluator falls short                                                                                               |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Short-circuit evaluation**      | CompositeEvaluator runs all metrics even after a failure. If completeness fails, checking groundedness is wasteful — stop early. |
| **Fully custom evaluation logic** | Your evaluation doesn't decompose into reusable metrics.                                                                         |

{% hint style="warning" %}
Don't reach for `BaseEvaluator` too early. If your evaluator is just a list of metrics → use `CompositeEvaluator`.
{% endhint %}

#### Example A: Short-Circuit Evaluator

When an early metric fails, skip the remaining metrics. Common pattern: if the output is a refusal or fails completeness, don't bother checking groundedness or redundancy — those checks are meaningless.

```python
import asyncio
import logging

from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.types import MetricInput, EvaluatorResult


class ShortCircuitEvaluator(BaseEvaluator):
    """Evaluator that stops on first metric failure.

    Use case: completeness is the gate. If the output is incomplete,
    groundedness and redundancy checks are irrelevant — skip them.
    """

    def __init__(self, metrics, name="short_circuit_evaluator"):
        super().__init__(name=name, metrics=metrics)

    async def _evaluate(self, data: MetricInput) -> EvaluatorResult:
        combined_results = {}
        for metric in self.metrics:
            if not metric.can_evaluate(data):
                continue
            result = await metric.evaluate(data)
            combined_results[metric.name] = result

            if not result.success:
                # Stop here — remaining metrics skipped
                return combined_results

        return combined_results


# Usage
async def main():
    from gllm_evals import LLMTestCase
    from gllm_evals.metrics import (
        GEvalCompletenessMetric,
        GEvalGroundednessMetric,
        GEvalRedundancyMetric,
    )

    evaluator = ShortCircuitEvaluator(
        metrics=[
            GEvalCompletenessMetric(),
            GEvalGroundednessMetric(),
            GEvalRedundancyMetric(),
        ],
        name="fail_fast_generation",
    )

    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="New York",
        expected_output="Paris",
        retrieved_context="Paris is the capital of France.",
    )
    result = await evaluator.evaluate(data)
    # If completeness fails, groundedness and redundancy never run
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

**When to use short-circuit:**

* A gate metric determines if further checks are meaningful (completeness → groundedness, refusal → generation quality)
* Later metrics are expensive (LLM calls, large context) and wasted if the gate fails
* You run evals at scale and want to minimize per-item cost on clear failures

**When NOT to use short-circuit:**

* You need visibility into all dimensions even on failures (for debugging or trend analysis)
* Your metrics are cheap (non-LLM) — the complexity isn't worth it

#### Example B: Simple Custom Evaluator

For fully custom logic that doesn't decompose into metrics, implement `_evaluate` directly.

```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.evaluator import BaseEvaluator
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import MetricInput, MetricOutput, EvaluatorResult

class ExactMatchMetric(BaseMetric):
    def __init__(self):
        self.name = "exact_match"

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        score = int(data["actual_output"] == data["expected_output"])
        return {"score": score, "explanation": None}

class ResponseEvaluator(BaseEvaluator):
    def __init__(self):
        super().__init__(name="response_evaluator")
        self.metric = ExactMatchMetric()

    async def _evaluate(self, data: MetricInput) -> EvaluatorResult:
        return await self.metric.evaluate(data)

async def main():
    evaluator = ResponseEvaluator()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris",
        expected_output="Paris",
    )
    result = await evaluator.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

#### Example Output

```python
{
    "response_evaluator": {
        "aggregate_explanation": "All metrics met the expected values.",
        "aggregate_success": True,
        "aggregate_score": 1,
        "exact_match": {
            "score": 1,
            "explanation": None,
            "rubric_score": 1,
            "success": True,
            "threshold": 0.5,
            "strict_mode": False,
            "higher_is_better": True,
        },
    }
}
```

For a full step-by-step tutorial including custom metric creation, see [Custom Evaluator / Scorer Tutorial](custom-evaluator-scorer-tutorial.md).

***

### Which Method Should You Use?

| Use Case                                | Approach                                 |
| --------------------------------------- | ---------------------------------------- |
| Run multiple existing metrics together  | `CompositeEvaluator`                     |
| Stop evaluation on first metric failure | Subclass `BaseEvaluator` (short-circuit) |
| Fully custom evaluation logic           | Subclass `BaseEvaluator`                 |

{% hint style="success" %}
Start with `CompositeEvaluator`. Only subclass `BaseEvaluator` when you have a concrete reason (short-circuit, custom aggregation, or non-metric logic).
{% endhint %}
