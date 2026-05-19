# 🔢 Metric

A **Metric** is a single, focused measurement of a model's output quality. It takes `LLMTestCase` as input and returns a score, explanation, and pass/fail result.

Metrics are the building blocks of evaluators — evaluators orchestrate multiple metrics in parallel and aggregate their results into a unified report. You can also run metrics standalone if you only need a single measurement.

## How Metrics Work

All metrics extend `BaseMetric` and implement a single `_evaluate()` method. Call `metric.evaluate(data)` to run it:

**Example Code**

```python
import asyncio
import os

from gllm_evals import LLMTestCase
from gllm_evals.metrics import GEvalCompletenessMetric

async def main():
    metric = GEvalCompletenessMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris",
        expected_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

{% hint style="info" %}
All examples use `LLMTestCase` as the input type. See [Getting Started](../getting-started.md#llmtestcase) for the full list of available fields.
{% endhint %}

**Example output**

```python
{
    "completeness": {
        "score": 1.0,
        "explanation": "The minimum key facts are: [A] Artificial Intelligence is...",
        "success": True,
        "rubric_score": 3,
        "threshold": 0.5,
        "strict_mode": False,
        "higher_is_better": True,
    }
}
```

<table><thead><tr><th width="187">Key</th><th width="142">Value</th><th>Explanation</th></tr></thead><tbody><tr><td><code>score</code></td><td>1.0</td><td>Normalized score in [0, 1], mapped from the rubric_score (3 on a 1-3 scale becomes 1.0).</td></tr><tr><td><code>explanation</code></td><td>"The minimum key facts are..."</td><td>Human-readable reasoning from the LLM judge explaining the score.</td></tr><tr><td><code>success</code></td><td>True</td><td>Because score (1.0) >= threshold (0.5) and higher_is_better is True.</td></tr><tr><td><code>rubric_score</code></td><td>3</td><td>Completeness have rubric scaling from 1 - 3. The result 3 is raw value from the LLM judge, where 3 means "fully complete".</td></tr><tr><td><code>threshold</code></td><td>0.5</td><td>Pass/fail threshold used to compute success. To achieve <code>success=True</code>, <code>score</code> must be higher or lower than the threshold depending on <code>higher_is_better.</code></td></tr><tr><td><code>strict_mode</code></td><td>False</td><td>The score is not binarized. If True, the score will be either 0 or 1.</td></tr><tr><td><code>higher_is_better</code></td><td>True</td><td>A higher score means better performance, so success is True when <code>score</code> >= <code>threshold</code>. Otherwise</td></tr></tbody></table>

## Metric Classification

Every metric in this library falls into two orthogonal classification axes:

### By Task

<table><thead><tr><th width="248">Method</th><th>Description</th><th>Examples</th></tr></thead><tbody><tr><td><strong>Generation</strong></td><td>Evaluates the quality of generated text output (completeness, groundedness, redundancy, factual correctness, etc.).</td><td>GEval, DeepEval Answer Relevancy, LangChain Correctness</td></tr><tr><td><strong>Retrieval</strong></td><td>Evaluates retrieval component quality (ranking, precision, recall, context sufficiency).</td><td>TopKAccuracy, DeepEval Contextual Precision, RAGAS Context Recall</td></tr><tr><td><strong>Safety</strong></td><td>Evaluates safety and policy compliance (bias, toxicity, PII leakage, role violations, misuse).</td><td>DeepEval Bias, DeepEval Toxicity, DeepEval Non-Advice</td></tr><tr><td><strong>Tool use</strong></td><td>Evaluates agent tool selection and trajectory correctness.</td><td>DeepEval Tool Correctness, LangChain Agent Trajectory Accuracy</td></tr></tbody></table>

### By Method

| Method            | Description                                                                                                        | Examples                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| **LLM-Judge**     | Uses a language model to score the output. Flexible, handles nuance, but non-deterministic.                        | GEval, DeepEval, RAGAS, LangChain metrics                                                                      |
| **Deterministic** | Rule-based or classical algorithm. Fast, fully reproducible, no LLM needed.                                        | `TopKAccuracy`, `PyTrecMetric`                                                                                 |
| **Combined**      | Uses an LLM to produce intermediate judgments, then applies code-based post-processing to compute the final score. | `DeepEvalContextualPrecisionMetric`, `DeepEvalContextualRecallMetric`, `RagasContextPrecisionWithoutReference` |
| Human             | Requires human evaluation for subjective or nuanced judgment.                                                      | -                                                                                                              |

### By Reference

<table><thead><tr><th width="249">Type</th><th>What it compares against</th><th>Needs expected_output?</th></tr></thead><tbody><tr><td><strong>Reference-based</strong></td><td>Compares the output against a gold-standard answer</td><td>Yes, as a literal gold answer</td></tr><tr><td><strong>Criteria-based</strong></td><td>Checks the output against per-example requirements written in natural language</td><td>Yes, as a coverage specification</td></tr><tr><td><strong>Referenceless</strong></td><td>Scores from the query and/or retrieved context alone; any criteria are universal and baked into the metric definition</td><td>No</td></tr></tbody></table>

**Criteria-based evaluation** is the industry-standard recommendation when you do not have high-quality annotated gold answers. Instead of asking "does this match the expected output?", you define explicit requirements and the judge scores against those. It is generally more scalable because writing a specification is cheaper than annotating correct answers at scale.

There are two ways to implement criteria-based evaluation:

1. **Per-example criteria in expected\_output** — the criteria vary per test case, so they live in the dataset as a natural language specification. `GEvalCompletenessMetric` supports this mode: instead of passing a literal gold answer, you pass something like "Answer must cover 3 personas, nightly rates, and trip lengths" and the judge checks coverage against that specification.
2. **Universal criteria baked into the metric** — the criteria are identical across all test cases, so they live in the metric's rubric and evaluation\_steps rather than in expected\_output. `GEvalContextSufficiencyMetric` is an example: sufficiency is always defined the same way, so the rubric is defined once in the metric class and no expected\_output is needed. This makes the metric referenceless while still being criteria-driven.

## Output Format

Every metric returns a `MetricOutput` dict with these fields:

| Field              | Type           | Description                                                                                                    |
| ------------------ | -------------- | -------------------------------------------------------------------------------------------------------------- |
| `score`            | `float`        | Normalized score in \[0, 1].                                                                                   |
| `rubric_score`     | `int \| float` | Raw value from the LLM judge (e.g. 1–3 scale). Not present on deterministic metrics.                           |
| `explanation`      | `str \| None`  | Human-readable reasoning from the LLM judge.                                                                   |
| `success`          | `bool`         | `True` if `score` meets the threshold (accounting for `higher_is_better`).                                     |
| `threshold`        | `float`        | The pass/fail threshold used to compute `success`.                                                             |
| `strict_mode`      | `bool`         | If `True`, score is binarized to 1.0 or 0.0.                                                                   |
| `higher_is_better` | `bool`         | `True` for most metrics. `False` for metrics where a lower score is desired (e.g. redundancy, bias, toxicity). |

## Supported Open-Source Frameworks

gllm-evals wraps metrics from three open-source evaluation frameworks transparently. You use the same `LLMTestCase` input and get the same `MetricOutput` format regardless of the underlying framework.

| Framework                            | Metrics                                                                       |
| ------------------------------------ | ----------------------------------------------------------------------------- |
| **DeepEval**                         | Faithfulness, AnswerRelevancy, ContextualPrecision, ToolCorrectness, and more |
| **RAGAS**                            | FactualCorrectness, ContextPrecision, ContextRecall                           |
| **LangChain OpenEvals / AgentEvals** | Correctness, Groundedness, Helpfulness, Trajectory Accuracy, and more         |

You can also extend any framework directly using the base wrapper classes (`DeepEvalMetricFactory`, `RAGASMetric`, `LangChainOpenEvalsMetric`, etc.) to plug in any metric from those libraries without writing a full custom metric.

## How to Create a Custom Metric

Extend `BaseMetric`, set `name`, and implement `_evaluate()`:

```python
from gllm_evals.metrics.metric import BaseMetric
from gllm_evals.types import MetricInput, MetricOutput

class ExactMatchMetric(BaseMetric):
    def __init__(self):
        self.name = "exact_match"

    async def _evaluate(self, data: MetricInput) -> MetricOutput:
        score = int(data["actual_output"] == data["expected_output"])
        return {"score": float(score), "explanation": None}
```

For more advanced custom metric patterns (e.g. extending GEval with custom evaluation steps), see [Create Custom Evaluator / Scorer](../evaluator/create-custom-evaluator-scorer.md).

## Available Metrics

| Metric                                                                                               | Task       | Method        | Reference       |
| ---------------------------------------------------------------------------------------------------- | ---------- | ------------- | --------------- |
| [GEvalCompletenessMetric](generation-metrics.md#gevalcompletenessmetric)                             | Generation | LLM-Judge     | Reference-based |
| [GEvalGroundednessMetric](generation-metrics.md#gevalgroundednessmetric)                             | Generation | LLM-Judge     | Referenceless   |
| [GEvalRedundancyMetric](generation-metrics.md#gevalredundancymetric)                                 | Generation | LLM-Judge     | Referenceless   |
| [GEvalLanguageConsistencyMetric](generation-metrics.md#gevallanguageconsistencymetric)               | Generation | LLM-Judge     | Referenceless   |
| [GEvalRefusalMetric](generation-metrics.md#gevalrefusalmetric)                                       | Generation | LLM-Judge     | Referenceless   |
| [GEvalRefusalAlignmentMetric](generation-metrics.md#gevalrefusalalignmentmetric)                     | Generation | LLM-Judge     | Referenceless   |
| [GEvalSummarizationCoherenceMetric](generation-metrics.md#gevalsummarizationcoherencemetric)         | Generation | LLM-Judge     | Referenceless   |
| [GEvalSummarizationConsistencyMetric](generation-metrics.md#gevalsummarizationconsistencymetric)     | Generation | LLM-Judge     | Referenceless   |
| [GEvalSummarizationFluencyMetric](generation-metrics.md#gevalsummarizationfluencymetric)             | Generation | LLM-Judge     | Referenceless   |
| [GEvalSummarizationRelevanceMetric](generation-metrics.md#gevalsummarizationrelevancemetric)         | Generation | LLM-Judge     | Referenceless   |
| [DeepEvalAnswerRelevancyMetric](generation-metrics.md#deepevalanswerelevancymetric)                  | Generation | Combined      | Referenceless   |
| [DeepEvalFaithfulnessMetric](generation-metrics.md#deepevalfaithfulnessmetric)                       | Generation | Combined      | Referenceless   |
| [DeepEvalHallucinationMetric](generation-metrics.md#deepevalhallucinationmetric)                     | Generation | Combined      | Reference-based |
| [DeepEvalJsonCorrectnessMetric](generation-metrics.md#deepevaljsoncorrectnessmetric)                 | Generation | Deterministic | Referenceless   |
| [DeepEvalBiasMetric](safety-metrics.md#deepevalbiasmetric)                                           | Safety     | Combined      | Referenceless   |
| [DeepEvalToxicityMetric](safety-metrics.md#deepevaltoxicitymetric)                                   | Safety     | Combined      | Referenceless   |
| [DeepEvalPIILeakageMetric](safety-metrics.md#deepevalpiileakagemetric)                               | Safety     | Combined      | Referenceless   |
| [DeepEvalPromptAlignmentMetric](safety-metrics.md#deepevalpromptalignmentmetric)                     | Safety     | Combined      | Referenceless   |
| [DeepEvalRoleViolationMetric](safety-metrics.md#deepevalroleviolationmetric)                         | Safety     | Combined      | Referenceless   |
| [DeepEvalMisuseMetric](safety-metrics.md#deepevalmisusemetric)                                       | Safety     | Combined      | Referenceless   |
| [DeepEvalNonAdviceMetric](safety-metrics.md#deepevalnonadvicemetric)                                 | Safety     | Combined      | Referenceless   |
| [LangChainCorrectnessMetric](generation-metrics.md#langchaincorrectnessmetric)                       | Generation | LLM-Judge     | Reference-based |
| [LangChainGroundednessMetric](generation-metrics.md#langchaingroundednessmetric)                     | Generation | LLM-Judge     | Referenceless   |
| [LangChainHallucinationMetric](generation-metrics.md#langchainhallucinationmetric)                   | Generation | LLM-Judge     | Referenceless   |
| [LangChainHelpfulnessMetric](generation-metrics.md#langchainhelpfulnessmetric)                       | Generation | LLM-Judge     | Referenceless   |
| [LangChainConcisenessMetric](generation-metrics.md#langchainconciseness)                             | Generation | LLM-Judge     | Referenceless   |
| [RagasFactualCorrectness](generation-metrics.md#ragasfactualcorrectness)                             | Generation | Combined      | Referenceless   |
| [TopKAccuracy](retrieval-metrics.md#topkaccuracy)                                                    | Retrieval  | Deterministic | Reference-based |
| [PyTrecMetric](retrieval-metrics.md#pytrecmetric)                                                    | Retrieval  | Deterministic | Reference-based |
| [GEvalContextSufficiencyMetric](retrieval-metrics.md#gevalcontextsufficiencymetric)                  | Retrieval  | LLM-Judge     | Referenceless   |
| [DeepEvalContextualPrecisionMetric](retrieval-metrics.md#deepevalcontextualprecisionmetric)          | Retrieval  | Combined      | Reference-based |
| [DeepEvalContextualRecallMetric](retrieval-metrics.md#deepevalcontextualrecallmetric)                | Retrieval  | Combined      | Reference-based |
| [DeepEvalContextualRelevancyMetric](retrieval-metrics.md#deepevalcontextualrelevancymetric)          | Retrieval  | Combined      | Referenceless   |
| [RagasContextPrecisionWithoutReference](retrieval-metrics.md#ragascontextprecisionwithoutreference)  | Retrieval  | Combined      | Referenceless   |
| [RagasContextRecall](retrieval-metrics.md#ragascontextrecall)                                        | Retrieval  | Combined      | Reference-based |
| [LangChainAgentTrajectoryAccuracyMetric](tool_use-metrics.md#langchainagenttrajectoryaccuracymetric) | Tool Use   | LLM-Judge     | Referenceless   |
| [DeepEvalToolCorrectnessMetric](tool_use-metrics.md#deepevaltoolcorrectnessmetric)                   | Tool Use   | Combined      | Reference-based |
