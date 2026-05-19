# SummarizationEvaluator

## SummarizationEvaluator

**Use when**: You want to evaluate the quality of a generated summary against its source text (e.g., meeting transcripts).

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/evaluator/summarization_evaluator" %}

By default, **SummarizationEvaluator** runs **four metrics**: coherence, consistency, relevance, and fluency.

1. **Coherence**: GEval summarization coherence score. The score is between 1 and 3. It assesses whether the summary is logically organized, flows smoothly, and maintains clear semantic links across sections. 1 means fragmented flow, 2 means mostly coherent with partial disconnects, and 3 means fully coherent. It needs **input** and **summary** to work.
2. **Consistency**: GEval summarization consistency score. The score is between 1 and 3. It assesses factual alignment between summary claims and the source transcript without unsupported additions. 1 means hallucinations dominate, 2 means some hallucinations present, and 3 means zero hallucinations. It needs **input** and **summary** to work.
3. **Relevance**: GEval summarization relevance score. The score is between 1 and 3. It assesses how completely and how focused the summary captures important information from the source transcript. 1 means major omissions, 2 means partial coverage, and 3 means complete and focused coverage. It needs **input** and **summary** to work.
4. **Fluency**: GEval summarization fluency score. The score is between 1 and 3. It assesses readability, naturalness, grammar, and clarity of the summary text. 1 means major readability problems, 2 means minor language issues, and 3 means clear and natural language. It needs **input** and **summary** to work.

**Fields**:

1. _input (str)_ — The source text to be summarized (e.g., a meeting transcript).
2. _actual\_output (str)_ — The generated summary to be evaluated.

**Output:**

SummarizationEvaluator returns a result for each enabled metric with its score and explanation. The following aggregated fields are provided:

* **aggregate\_success** (`bool`): `True` if **all** enabled metrics passed (AND-gate of each metric's `success` flag).
* **aggregate\_score** (`float`): Polarity-aware mean of each metric's normalized score.

Each per-metric result contains:

* **score** (`float`): Normalized score in \[0, 1].
* **rubric\_score** (`int | float`): Raw rubric value from the LLM judge (1–3).
* **explanation** (`str`): Human-readable reasoning from the LLM judge.
* **success** (`bool`): Pass/fail based on threshold and polarity.
* **threshold** (`float`): The threshold used to compute `success`.
* **strict\_mode** (`bool`): If `True`, score is binarized to 1.0 or 0.0.
* **higher\_is\_better** (`bool`): Polarity flag.

## Example Usage

```python
import asyncio
import json
import os

from gllm_evals import load_simple_summarization_dataset
from gllm_evals.evaluator.summarization_evaluator import SummarizationEvaluator


async def main():
    """Run a single summary evaluation example."""
    evaluator = SummarizationEvaluator()
    raw = load_simple_summarization_dataset()
    data = [
        LLMTestCase(
            input=row["input"],
            actual_output=row["summary"],
        )
        for row in raw.load()
    ]

    result = await evaluator.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

Or you can provide the data directly

```python
import asyncio
import json
import os

from gllm_evals import LLMTestCase
from gllm_evals.evaluator.summarization_evaluator import SummarizationEvaluator


async def main():
    """Run a single summary evaluation example."""
    data = LLMTestCase(
        input="Meeting transcript or source text here...",
        actual_output="Generated summary here...",
    )

    evaluator = SummarizationEvaluator()

    result = await evaluator.evaluate(data)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
```

## Example Output

```json
{
  "summary": {
    "aggregate_explanation": "All metrics met the expected values.",
    "aggregate_success": true,
    "aggregate_score": 0.92,
    "summarization_coherence": {
      "score": 1.0,
      "rubric_score": 3,
      "explanation": "Ringkasan terstruktur dengan baik, mengikuti alur logis dari tujuan rapat, ringkasan eksekutif, isu, item tindakan, hingga item diskusi. Setiap bagian terhubung secara semantik dan tidak ada lompatan yang tiba-tiba.",
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "summarization_consistency": {
      "score": 1.0,
      "rubric_score": 3,
      "explanation": "Semua klaim faktual dalam ringkasan didukung oleh transkrip sumber. Tidak ditemukan halusinasi atau informasi yang tidak didukung.",
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "summarization_relevance": {
      "score": 1.0,
      "rubric_score": 3,
      "explanation": "Ringkasan mencakup semua bagian yang diperlukan dan menangkap informasi penting dari transkrip secara lengkap dan fokus.",
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    },
    "summarization_fluency": {
      "score": 0.67,
      "rubric_score": 2,
      "explanation": "Ringkasan dapat dipahami dengan baik, namun terdapat beberapa masalah minor pada tata bahasa dan pemilihan kata yang sedikit mengurangi kealamian teks.",
      "success": true,
      "threshold": 0.5,
      "strict_mode": false,
      "higher_is_better": true
    }
  }
}
```

**Enabling Specific Metrics**

You can enable only a subset of the four metrics:

```python
evaluator = SummarizationEvaluator(
    enabled_metrics=["summarization_coherence", "summarization_fluency"],
)
```

When specific metrics are enabled, only those metrics contribute to `aggregate_success` and `aggregate_score`.
