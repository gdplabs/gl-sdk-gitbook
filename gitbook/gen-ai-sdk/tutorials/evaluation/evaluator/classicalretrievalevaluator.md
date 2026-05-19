# ClassicalRetrievalEvaluator

## ClassicalRetrievalEvaluator

**Use when**: You want to evaluate retrieval performance with classical IR metrics (MAP, NDCG, Precision, Recall, Top-K Accuracy).

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/evaluator/classical_retrieval_evaluator" %}

**Fields**:

1. retrieved\_chunks (dict\[str, float]) — The dictionary of retrieved documents/chunks containing the chunk id and its score.
2. ground\_truth\_chunk\_ids (list\[str]) — The list of reference chunk ids marking relevant chunks.

## Example Usage

```python
import asyncio

from gllm_evals.evaluator.classical_retrieval_evaluator import ClassicalRetrievalEvaluator
from gllm_evals.types import RetrievalData


async def main():
    """Main function."""
    data = RetrievalData(
        retrieved_chunks={
            "chunk1": 9.0,
            "chunk2": 0.0,
            "chunk3": 0.3,
            "chunk4": 0.1,
            "chunk5": 0.2,
            "chunk6": 0.4,
            "chunk7": 0.5,
            "chunk8": 0.6,
            "chunk9": 0.7,
            "chunk10": 0.8,
        },
        ground_truth_chunk_ids=["chunk9", "chunk3", "chunk2"],
    )
    evaluator = ClassicalRetrievalEvaluator(k=[5, 10])
    results = await evaluator.evaluate(data)
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
```

## Example Output

```python
{
  "classical_retrieval_evals": {
    "aggregate_explanation": "The following metrics failed to meet expectations:\n1. Map@5 is 0.1111111111111111 (should be 0.5)\n2. Precision@5 is 0.2 (should be 0.5)\n3. Ndcg@5 is 0.23463936301137822 (should be 0.5)\n4. Precision@10 is 0.3 (should be 0.5)\n5. Map@10 is 0.30634920634920637 (should be 0.5)\n6. Recall@5 is 0.3333333333333333 (should be 0.5)",
    "aggregate_success": False,
    "aggregate_score": 0.501215059225644,
    "precision@5": {
      "score": 0.2,
      "explanation": None,
      "rubric_score": 0.2,
      "success": False,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "precision@10": {
      "score": 0.3,
      "explanation": None,
      "rubric_score": 0.3,
      "success": False,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "recall@5": {
      "score": 0.3333333333333333,
      "explanation": None,
      "rubric_score": 0.3333333333333333,
      "success": False,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "recall@10": {
      "score": 1.0,
      "explanation": None,
      "rubric_score": 1.0,
      "success": True,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "ndcg@5": {
      "score": 0.23463936301137822,
      "explanation": None,
      "rubric_score": 0.23463936301137822,
      "success": False,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "ndcg@10": {
      "score": 0.5267175784514114,
      "explanation": None,
      "rubric_score": 0.5267175784514114,
      "success": True,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "map@5": {
      "score": 0.1111111111111111,
      "explanation": None,
      "rubric_score": 0.1111111111111111,
      "success": False,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "map@10": {
      "score": 0.30634920634920637,
      "explanation": None,
      "rubric_score": 0.30634920634920637,
      "success": False,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "top_k_accuracy@5": {
      "score": 1.0,
      "explanation": None,
      "rubric_score": 1.0,
      "success": True,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
    "top_k_accuracy@10": {
      "score": 1.0,
      "explanation": None,
      "rubric_score": 1.0,
      "success": True,
      "threshold": 0.5,
      "strict_mode": False,
      "higher_is_better": True,
    },
  }
}


```
