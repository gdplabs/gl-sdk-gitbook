# LMBasedRetrievalEvaluator

## LMBasedRetrievalEvaluator

**Use when**: You want to evaluate the retrieval step of a RAG pipeline with LM-based metrics, combining their scores into a simple relevancy rating, final score, and issue hints.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/evaluator/lm_based_retrieval_evaluator" %}

By default, `LMBasedRetrievalEvaluator` runs two metrics: contextual precision and contextual recall, then applies a rule engine to classify the retrieval quality.

1. **Contextual Precision**: DeepEval contextual precision. Scores range from 0 to 1. It checks whether relevant context is ranked above irrelevant context for the given query and expected answer. Needs `input`, `expected_output`, and `retrieved_context`.
2. **Contextual Recall**: DeepEval contextual recall. Scores range from 0 to 1. It measures how well the retrieved context aligns with the expected answer. Needs `input`, `expected_output`, and `retrieved_context`. The default rule engine uses this metric to determine the retrieval relevancy rating (good / bad).

**Fields**:

1. _input (str)_ — The user question.
2. _expected\_output (str)_ — The reference or ground truth answer.
3. _retrieved\_context (str | list\[str])_ — The supporting context/documents used during retrieval. Strings are coerced into a single-element list.

## Example Usage

```python
import asyncio
import os
from gllm_evals.evaluator.lm_based_retrieval_evaluator import LMBasedRetrievalEvaluator
from gllm_evals.types import LLMTestCase

async def main():
    evaluator = LMBasedRetrievalEvaluator()

    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris is the capital of France.",
        retrieved_context=[
            "Berlin is the capital of Germany.",
            "Paris is the capital city of France with a population of over 2 million people.",
            "London is the capital of the United Kingdom.",
        ],
    )

    result = await evaluator.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Example Output

```python
{
  "lm_based_retrieval": {
    "aggregate_explanation": "All metrics met the expected values.",
    "aggregate_success": True,
    "aggregate_score": 0.75,
    "deepeval_contextual_precision": {
      "score": 0.5,
      "explanation": 'The score is 0.50 because the first node in the retrieval contexts is an irrelevant node that "discusses the capital of Germany, which is not relevant to determining the capital of France.", and should be ranked lower than the second node which correctly "explicitly mentions that \'Paris is the capital city of France\'". The score is not higher because the relevant information is preceded by an irrelevant node at rank 1, followed by a third node that is also an irrelevant node as it "discusses the capital of the United Kingdom".',
      "success": True,
      "rubric_score": 0.5,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "deepeval_contextual_recall": {
      "score": 1.0,
      "explanation": "The score is 1.00 because sentence 1 is perfectly captured by node 2 in retrieval context, resulting in a flawless match!",
      "success": True,
      "rubric_score": 1.0,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
  }
}

```
