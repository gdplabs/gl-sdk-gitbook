# GEvalGenerationEvaluator

## GEvalGenerationEvaluator

**Use when**: You want to evaluate the response/answer of a QnA system. This includes general chatbots, RAG systems, or agents that answer specific questions. The focus of this evaluator is on assessing the quality of the answer provided by the QnA system.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/evaluator/geval_generation_evaluator" %}

By default, **GEvalGenerationEvaluator** runs **three metrics**: completeness, groundedness, and redundancy.

You can additionally enable language consistency and refusal alignment through evaluator configuration.

1. [GEvalCompletenessMetric](../metric/generation-metrics.md#gevalcompletenessmetric)
2. [GEvalRedundancyMetric](../metric/generation-metrics.md#gevalredundancymetric)
3. [GEvalGroundednessMetric](../metric/generation-metrics.md#gevalgroundednessmetric)
4. [GEvalLanguageConsistencyMetric](../metric/generation-metrics.md#gevallanguageconsistencymetric)
5. [GEvalRefusalAlignmentMetric](../metric/generation-metrics.md#gevalrefusalalignmentmetric)

## Fields:

1. _input (str)_ — The user question.
2. actual\_output (str) — The model's output to be evaluated.
3. expected\_output (str, optional) — The reference or ground truth answer.
4. retrieved\_context (str, optional) — The supporting context/documents used during generation.

## Output

GEvalGenerationEvaluator returns a result for each enabled metric with their score and explanation. In aggregation, the following fields are provided:

* **aggregate\_success** (`bool`): `True` if **all** enabled metrics passed (AND-gate of each metric's `success` flag).
* **aggregate\_score** (`float`): Polarity-aware mean of each metric's normalized score. For metrics where lower is better (e.g. redundancy), the score is inverted (`1.0 - score`) before averaging.

Each per-metric result contains:

* **score** (`float`): Normalized score in \[0, 1].
* **rubric\_score** (`int | float`): Raw rubric value from the LLM judge (e.g. 1–3 for completeness/groundedness/redundancy).
* **explanation** (`str`): Human-readable reasoning from the LLM judge.
* **success** (`bool`): Pass/fail based on threshold and polarity.
* **threshold** (`float`): The threshold used to compute `success`.
* **strict\_mode** (`bool`): If `True`, score is binarized to 1.0 or 0.0.
* **higher\_is\_better** (`bool`): Polarity flag — `False` for redundancy (lower is better).

## Example Usage

```python
import asyncio
import os

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator


async def main():
    """Main function."""
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )

    evaluator = GEvalGenerationEvaluator()

    result = await evaluator.evaluate(data)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

## Example Output

```json
{
  "generation": {
    "aggregate_explanation": "The following metrics failed to meet expectations:\n1. Completeness score 0.0 (threshold: 0.5)\n2. Groundedness score 0.0 (threshold: 0.5)",
    "aggregate_success": false,
    "aggregate_score": 0.33,
    "completeness": {
      "score": 0.0,
      "rubric_score": 1,
      "explanation": "The output contains a critical factual contradiction, incorrectly identifying New York as the capital of France instead of Paris.",
      "success": false,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "groundedness": {
      "score": 0.0,
      "rubric_score": 1,
      "explanation": "The output directly contradicts the provided retrieval context, which explicitly states that Paris is the capital of France.",
      "success": false,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "redundancy": {
      "score": 0.0,
      "rubric_score": 1,
      "explanation": "The response is extremely concise, providing a single answer without any repetition of words, phrases, or ideas.",
      "success": true,
      "threshold": 0.4,
      "strict_mode": false,
      "higher_is_better": false
    },
    "is_refusal": false
  }
}
```
