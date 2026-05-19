# Retrieval Metrics

## Retrieval Metrics

Retrieval metrics evaluate the quality of a retrieval pipeline — whether the right documents were fetched, whether they are ranked correctly, and whether they contain enough information to answer the query.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/metrics/retrieval" %}

{% hint style="info" %}
All examples use `LLMTestCase` as the input type. See Getting Started for the full list of available fields.
{% endhint %}

***

## Classical / Deterministic Metrics

These metrics require no LLM. They use ground-truth chunk IDs to compute hit rates and ranking metrics with full reproducibility.

### TopKAccuracy

> **Method:** Deterministic | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [TopKAccuracy](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.TopKAccuracy)

Measures whether at least one ground-truth chunk appears in the top K retrieved results. Reports a hit rate across all queries.

**When to use:**

* When you have ground-truth chunk IDs and want a direct hit/miss view of whether relevant chunks appear in the top K results.
* When retrieval success is defined as "did we fetch at least one relevant chunk in the first K candidates?"
* When you want a simple retrieval-stage metric that is easy to compare across multiple `k` values.

**Required fields:** `retrieved_chunks`, `ground_truth_chunk_ids`

**Constructor parameters:**

* `k` (`int | list[int]`, default: `20`) — the cutoff rank(s) to evaluate. Pass a list to evaluate multiple K values at once.

**Example:**

```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.metrics import TopKAccuracy

async def main():
    metric = TopKAccuracy(k=10)
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        retrieved_chunks=[
            {"chunk_id": "doc_001", "content": "Paris is the capital city of France."},
            {"chunk_id": "doc_002", "content": "France is a country in Western Europe."},
        ],
        ground_truth_chunk_ids=["doc_001"],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### PyTrecMetric

> **Method:** Deterministic | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [PyTrecMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.PyTrecMetric)

Computes standard IR metrics (MAP, NDCG, precision@k, recall@k) using the PyTrec evaluation library. More granular than TopKAccuracy — it accounts for ranking position and multiple relevant documents.

**When to use:**

* When you want standard IR metrics such as MAP, NDCG, precision, or recall over retrieved chunks.
* When you have `retrieved_chunks` and `ground_truth_chunk_ids` and need more nuance than top-k hit rate.
* When you want configurable metric sets and cutoff values for classical retrieval benchmarking.

**Required fields:** `retrieved_chunks`, `ground_truth_chunk_ids`

**Constructor parameters:**

* `metrics` — list of IR metric names to compute (e.g. `["MAP", "NDCG", "PRECISION", "RECALL"]`)
* `k` (`int`, default: `20`) — rank cutoff

**Example:**

```python
from gllm_evals.metrics import PyTrecMetric

metric = PyTrecMetric(metrics=["NDCG", "MAP"], k=20)
```

***

## GEval Retrieval Metrics

### GEvalContextSufficiencyMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalContextSufficiencyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalContextSufficiencyMetric)

Provides a boolean judgment of whether the retrieved context is sufficient to answer the query at all. Useful as an answerability gate before generation.

**When to use:**

* When you need to decide whether the pipeline should attempt to answer, request more retrieval, or abstain.
* When you only have `input` and `retrieved_context` and want to check answerability from context alone.

**Required fields:** `input`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.retrieval.geval_context_sufficiency import GEvalContextSufficiencyMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalContextSufficiencyMetric()
    data = LLMTestCase(
        input="Kapan bola lampu pijar praktis ditemukan?",
        retrieved_context=[
            "Thomas Alva Edison mengembangkan banyak peralatan penting di abad ke-19.",
            "Salah satu penemuannya yang terpenting adalah bola lampu pijar praktis pertama.",
            "Penemuan bola lampu pijar tersebut didemonstrasikan pada tahun 1879.",
        ],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

## DeepEval Retrieval Metrics

### DeepEvalContextualPrecisionMetric

> **Method:** Combined | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [DeepEvalContextualPrecisionMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalContextualPrecisionMetric)

Measures whether the retrieved context that is relevant to the expected answer is ranked above irrelevant context. Focuses on ranking quality within the retrieved set.

**When to use:**

* When ranking quality inside the retrieved set matters, not just whether relevant context appears somewhere.
* When you have `input`, `expected_output`, and `retrieved_context` and want an LLM-judged precision signal.

**Required fields:** `input`, `expected_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.retrieval.deepeval_contextual_precision import DeepEvalContextualPrecisionMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalContextualPrecisionMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital.",
        expected_output="Paris",
        retrieved_context=[
            "Paris is the capital city of France.",
            "France is known for its cuisine.",
        ],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalContextualRecallMetric

> **Method:** Combined | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [DeepEvalContextualRecallMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalContextualRecallMetric)

Measures whether the retrieved context contains the information required to support the expected answer. Evaluates retrieval completeness relative to the reference.

**When to use:**

* When the retrieval question is coverage: "did we find enough of the needed evidence?"
* When you have a reference answer and want to judge retrieval completeness relative to it.

**Required fields:** `input`, `expected_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.retrieval.deepeval_contextual_recall import DeepEvalContextualRecallMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalContextualRecallMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital.",
        expected_output="Paris",
        retrieved_context=["Paris is the capital city of France."],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalContextualRelevancyMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [DeepEvalContextualRelevancyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalContextualRelevancyMetric)

Evaluates the overall relevance of the retrieved context chunks to the query and generated answer. Targets noisy or tangential retrieval rather than missing retrieval.

**When to use:**

* When your retrieval issue is noisy or tangential context rather than missing context.
* When you want to reduce irrelevant chunks passed into downstream generation.

**Required fields:** `input`, `actual_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.retrieval.deepeval_contextual_relevancy import DeepEvalContextualRelevancyMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalContextualRelevancyMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        retrieved_context=["Paris is the capital city of France.", "France is in Europe."],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

## RAGAS Retrieval Metrics

RAGAS retrieval metrics require an `lm_model` constructor parameter.

### RagasContextPrecisionWithoutReference

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [RagasContextPrecisionWithoutReference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.RagasContextPrecisionWithoutReference)

Measures the proportion of retrieved chunks that were actually useful for the generated answer. Does not require a ground-truth reference answer, making it suitable for production traces.

**When to use:**

* When you want retrieval precision without requiring a gold reference answer.
* When evaluating real production traces where expected answers are unavailable.
* When you want to know whether the retrieved chunks were actually used by the model.

**Required fields:** `input`, `actual_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.retrieval.ragas_context_precision_without_reference import RagasContextPrecisionWithoutReference
from gllm_evals.types import LLMTestCase

async def main():
    metric = RagasContextPrecisionWithoutReference()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        retrieved_context=["Paris is the capital city of France.", "France is in Europe."],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### RagasContextRecall

> **Method:** Combined | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [RagasContextRecall](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.RagasContextRecall)

Measures how much of the information needed for the expected answer was actually retrieved. Diagnoses missing-evidence failures where the retrieval pipeline did not fetch enough supporting documents.

**When to use:**

* When you need to measure how much of the information needed for the expected answer was actually retrieved.
* When you have both `actual_output` and `expected_output` and want a retrieval recall signal tied to answer requirements.
* When diagnosing missing-evidence failures in RAG pipelines.

**Required fields:** `input`, `actual_output`, `expected_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.retrieval.ragas_context_recall import RagasContextRecall
from gllm_evals.types import LLMTestCase

async def main():
    metric = RagasContextRecall()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital.",
        expected_output="Paris",
        retrieved_context=["Paris is the capital city of France."],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
