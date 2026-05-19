# Custom Metric

Built-in metrics cover common quality dimensions — completeness, groundedness, bias, relevance. But evaluation needs vary by domain, and eventually you hit a case where no built-in metric fits:

* A **legal domain** requires evaluating responses against jurisdiction-specific terminology
* A **pricing bot** has a correctness standard that doesn't match the generic completeness rubric
* A **deterministic check** (e.g., "did the agent actually create this order in the database?") can't be answered by an LLM judge at all

Custom metrics bridge this gap. There are three approaches, ordered from least to most reusable:

| Approach                           | Effort | When to use                                                    |
| ---------------------------------- | ------ | -------------------------------------------------------------- |
| **`DeepEvalGEvalMetric` directly** | Medium | Quick one-off LLM judge with custom prompts, no subclassing    |
| **Subclass `DeepEvalGEvalMetric`** | Medium | Same custom quality dimension used repeatedly across projects  |
| **Subclass `BaseMetric`**          | Varies | Deterministic checks (DB, API, rules) — no LLM judgment needed |

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/metrics/custom_metric" %}

{% hint style="info" %}
Before writing a custom metric, review [Calibrate the Evals](../calibrate-the-evals/) and [Modify Metrics](modify-metrics.md). Many "missing metrics" are fixable by recalibrating or overriding an existing metric's rubric, threshold, criteria, or few-shot examples.
{% endhint %}

***

### Decision Flow

```
Do you need LLM judgment?
├── NO → Subclass BaseMetric (Approach 3)
│        Database checks, API validation, deterministic rules
│
└── YES → Is an existing metric close to what you need?
          ├── YES → Modify existing metric attributes
          │        Rubric, threshold, criteria, few-shot, evaluation_steps
          │        See Modify Metrics
          │
          └── NO → Do you need this across many datasets/projects?
                   ├── YES → Subclass DeepEvalGEvalMetric (Approach 2)
                   │        Reusable, class-based, import once
                   │
                   └── NO → DeepEvalGEvalMetric directly (Approach 1)
                             Quick script, single-use prompt
```

***

### Approach 1: DeepEvalGEvalMetric Directly (Quick Custom Prompt)

**When:** you need a new quality dimension that no built-in metric covers, and it's a one-off evaluation — you don't expect to reuse the prompt across projects.

```python
import asyncio
from deepeval.metrics.g_eval import Rubric
from deepeval.test_case import LLMTestCaseParams

from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric
from gllm_evals.types import LLMTestCase


async def main():
    data = LLMTestCase(
        input="Can you help me reset my password?",
        actual_output="Hello! Thank you for contacting us. I'd be happy to help you reset your password.",
    )

    metric = DeepEvalGEvalMetric(
        name="geval_politeness",
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
        criteria="Politeness (1-3) - Assess how polite the response is.",
        rubric=[
            Rubric(score_range=(1, 1), expected_outcome="Rude"),
            Rubric(score_range=(2, 2), expected_outcome="Neutral"),
            Rubric(score_range=(3, 3), expected_outcome="Polite"),
        ],
    )

    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

**Trade-off:** quick to write but tightly coupled to the script — if you need the same politeness check in another project, you'll copy-paste. For reusable prompts, use Approach 2.

***

### Approach 2: Subclass DeepEvalGEvalMetric (Reusable LLM Judge)

**When:** the same custom quality dimension is evaluated across multiple datasets, projects, or evaluation runs. Subclassing gives you a reusable, importable metric class with the same `evaluate()` interface as built-in metrics.

```python
from deepeval.metrics.g_eval import Rubric
from deepeval.test_case import LLMTestCaseParams

from gllm_evals.constant import ColumnNames
from gllm_evals.metrics.deepeval_geval import DeepEvalGEvalMetric, MetricDefaults
from gllm_evals.types import LLMTestCase


class PolitenessMetric(DeepEvalGEvalMetric):
    """Custom metric evaluating politeness of responses."""

    description: str = "Politeness score. Normalized to [0, 1] range."
    required_fields: set[str] = {ColumnNames.INPUT, ColumnNames.ACTUAL_OUTPUT}
    input_type: type = LLMTestCase
    higher_is_better: bool = True

    _defaults = MetricDefaults(
        name="geval_politeness",
        criteria="Politeness (1-3) - Assess how polite the response is.",
        rubric=[
            Rubric(score_range=(1, 1), expected_outcome="Rude"),
            Rubric(score_range=(2, 2), expected_outcome="Neutral"),
            Rubric(score_range=(3, 3), expected_outcome="Polite"),
        ],
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT],
    )

    def _to_rubric_score(self, raw: float) -> int:
        return int(1 + raw * 2)
```

**Required components:**

| Component               | Purpose                                                                         |
| ----------------------- | ------------------------------------------------------------------------------- |
| `_defaults`             | `MetricDefaults(name, criteria, rubric, evaluation_params, [evaluation_steps])` |
| `required_fields`       | Set of `ColumnNames` fields the metric needs from input data                    |
| `input_type`            | `LLMTestCase` (canonical input type)                                            |
| `higher_is_better`      | `True` or `False` — affects `MetricsAggregator` polarity inversion              |
| `_to_rubric_score(raw)` | Convert normalized `[0,1]` back to native rubric integer                        |

**Usage — same interface as any built-in metric:**

```python
import asyncio

from gllm_evals.types import LLMTestCase

async def main():
    data = LLMTestCase(
        input="Can you help me reset my password?",
        actual_output="Hello! Thank you for contacting us. I'd be happy to help you reset your password.",
    )
    metric = PolitenessMetric()
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

Works with `CompositeEvaluator`, `evaluate()`, experiment trackers — everything a built-in metric works with.

***

### Approach 3: Subclass BaseMetric (Deterministic, No LLM)

**When:** the check doesn't need LLM judgment at all. Examples:

* "Did the agent create the order in the database?"
* "Is the response length under the maximum token limit?"
* "Does the output contain a valid JSON schema?"
* "Are all required environment variables set?"

No LLM call, no latency, no cost, deterministic result.

```python
from gllm_evals.constant import ResultMetricKeys
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import MetricInput, MetricOutput


class OrderExistsInDBMetric(BaseMetric):
    """Check whether an order ID exists in a mock database."""

    name = "order_exists_in_db"
    required_fields = {"order_id"}

    def __init__(self, mock_db: dict[str, dict[str, str]] | None = None):
        super().__init__()
        self.mock_db = mock_db or {}

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        order_id = data.get("order_id")
        if not isinstance(order_id, str):
            return {
                ResultMetricKeys.SCORE: 0.0,
                ResultMetricKeys.EXPLANATION: "Invalid or missing order_id",
            }

        exists = order_id in self.mock_db
        return {
            ResultMetricKeys.SCORE: 1.0 if exists else 0.0,
            ResultMetricKeys.EXPLANATION: None if exists else f"Order {order_id} not found in DB",
        }
```

**Required components:**

| Component         | Purpose                                       |
| ----------------- | --------------------------------------------- |
| `name`            | Metric key in evaluation output               |
| `required_fields` | Set of field names from input data            |
| `_evaluate(data)` | Async method returning `{score, explanation}` |

**Usage:**

```python
import asyncio
from gllm_evals import LLMTestCase, ToolCall

async def main():
    mock_db = {"order_1001": {"status": "created"}}
    metric = OrderExistsInDBMetric(mock_db=mock_db)

    data = LLMTestCase(
        input="Create an order for user_1 with coffee_beans quantity 1.",
        actual_output="Order order_1001 has been created.",
        order_id="order_1001",
        tools_called=[
            ToolCall(
                name="create_order",
                input_parameters={"user_id": "user_1", "product_id": "coffee_beans", "quantity": 1},
            )
        ],
    )

    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

No API key needed. No LLM call. Instant — useful when chained as a gate metric before expensive LLM-based checks ([see short-circuit pattern](../evaluator/create-custom-evaluator-scorer.md#2-extend-baseevaluator-advanced)).

***

### Summary

| Question                                                     | Answer                                                                                  |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| Existing metric behavior is close, just wrong prompt/rubric? | Use [Modify Metrics](modify-metrics.md)                                                 |
| Need a one-off custom LLM judge?                             | **`DeepEvalGEvalMetric` directly** (Approach 1)                                         |
| Same custom judge across multiple projects?                  | **Subclass `DeepEvalGEvalMetric`** (Approach 2)                                         |
| No LLM judgment needed — deterministic check?                | **Subclass `BaseMetric`** (Approach 3)                                                  |
| Not sure if you need a custom metric at all?                 | Try [calibrating](../calibrate-the-evals/) first — the built-in metric may already work |
