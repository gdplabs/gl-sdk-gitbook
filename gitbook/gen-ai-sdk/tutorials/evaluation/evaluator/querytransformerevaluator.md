# QueryTransformerEvaluator

## QueryTransformerEvaluator

**Use when**: You want to evaluate query transformation tasks, checking how well queries are rewritten, expanded, or paraphrased for downstream use.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/evaluator/query_transformer_evaluator" %}

**Fields**:

1. _input (str)_ — The original input query.
2. _actual\_output (str)_ — The model's transformed query output serialized as a stringified `list[str]`.
3. _expected\_output (str)_ — The reference transformed query serialized as a stringified `list[str]`.

## Example Usage

```python
import asyncio
import os

from gllm_evals.evaluator.qt_evaluator import QTEvaluator
from gllm_evals.types import LLMTestCase


async def main():
    """Main function."""
    qt_task_prefix = "Decompose this query: "
    query = "Siapa yang bertanggung jawab atas pemantauan kepatuhan terintegrasi dan bagaimana cara melaporkannya?"
    query = f"{qt_task_prefix}{query}"

    expected_response = [
        "penanggung jawab pemantauan kepatuhan terintegrasi",
        "prosedur pelaporan kepatuhan terintegrasi",
    ]
    generated_response = [
        "penanggung jawab pemantauan kepatuhan terintegrasi",
        "prosedur pelaporan kepatuhan terintegrasi",
    ]

    data = LLMTestCase(
        input=query,
        expected_output=str(expected_response),
        actual_output=str(generated_response),
    )

    evaluator = QTEvaluator()

    result = await evaluator.evaluate(data)
    print(result)



if __name__ == "__main__":
    asyncio.run(main())
```

## Example Output

```json
{
  "qt_evals": {
    "aggregate_explanation": "All metrics met the expected values.",
    "aggregate_success": true,
    "aggregate_score": 1.0,
    "completeness": {
      "score": 1.0,
      "explanation": "The minimum key facts are: [A] 'penanggung jawab pemantauan kepatuhan terintegrasi' and [B] 'prosedur pelaporan kepatuhan terintegrasi'. The Generated Response provides an exact match for both key facts, successfully decomposing the input query into its two core components. Specifically, Key Fact A regarding the responsible party and Key Fact B regarding the reporting procedure are both present in the output list. There are no missing components or contradictions, and the response perfectly mirrors the Expected Output. Per Step 5C Coverage Rule, all minimum key facts are matched.",
      "success": true,
      "rubric_score": 3,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "groundedness": {
      "score": 1.0,
      "explanation": "The output correctly decomposes the input query found in the context into its two primary components: the responsible party and the reporting procedure. This breakdown is a direct logical inference based on the content of the string provided in the context.",
      "success": true,
      "rubric_score": 3,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "redundancy": {
      "score": 0.0,
      "explanation": "The response decomposes the input query into two distinct and unique components: the party responsible for monitoring and the reporting procedure. Each point is presented once without any repetition or paraphrasing, maintaining high information density and conciseness.",
      "rubric_score": 1,
      "success": true,
      "threshold": 0.4,
      "strict_mode": false,
      "higher_is_better": false
    }
  }
}
```
