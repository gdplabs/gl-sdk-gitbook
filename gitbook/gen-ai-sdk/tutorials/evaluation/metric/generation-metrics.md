# Generation Metrics

## Generation Metrics

Generation metrics evaluate the quality of a model's generated text output. They check dimensions such as completeness, groundedness, redundancy, language consistency, factual correctness, and more.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/metrics/generation" %}

{% hint style="info" %}
All examples use `LLMTestCase` as the input type. See Getting Started for the full list of available fields.
{% endhint %}

## Usage Pattern

```python
import asyncio

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

***

## GEval Metrics

GEval metrics use structured LLM-as-a-judge evaluation with rubric-based scoring (1–3 scale internally, normalized to 0–1).

### GEvalCompletenessMetric

> **Method:** LLM-Judge | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [GEvalCompletenessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalCompletenessMetric)

Measures how completely the generated response covers the key facts in the expected answer. Partial but non-contradictory answers receive intermediate scores.

**When to use:**

* When you have a reference answer and need to check whether the model's response is fully complete. (reference-based)
* When partial responses that miss key facts are a common failure mode in your pipeline.
* When you want a graded completeness signal, not just a binary pass/fail.
* When you have a specific criteria to be used as complete reference (criteria-based)

**Required fields:** `input`, `actual_output`, `expected_output`

**Example 1: Reference-based completeness (expected\_output is the literal answer)**

```python
import asyncio

from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalCompletenessMetric()
    data = LLMTestCase(
        input="Apa itu Artificial Intelligence?",
        actual_output="Artificial Intelligence adalah ilmu yang mempelajari bagaimana membuat mesin dapat berpikir seperti manusia.",
        expected_output="Artificial Intelligence adalah ilmu yang mempelajari tentang bagaimana membuat mesin dapat berpikir seperti manusia.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

**Example 2: Criteria-based completeness (expected\_output describes required coverage)**

```python
import asyncio

from gllm_evals.metrics.generation.geval_completeness import GEvalCompletenessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalCompletenessMetric()
    data = LLMTestCase(
        input="Which personas (romantic couples, family/friends groups, and dive-centric value seekers) do different yachts on The Luxury Voyage most appeal to, and how do nightly rates and typical trip lengths differ by persona?",
        actual_output="""
## Persona Appeal by Yacht

- **Romantic Couples:** Alexa ($6,500+/night) — intimate, private, luxury-focused.
- **Family/Friends Groups:** Magia II, Oracle, Dewata ($4,950–$5,950+/night) — communal spaces, flexible cabins.
- **Dive-Centric Value Seekers:** Dewata, Oracle, Magia II ($4,950–$5,950+/night) — diving included, equipment onboard.

## Nightly Rates & Trip Lengths by Persona

| Persona                    | Nightly Rate (USD) | Typical Trip Length |
|----------------------------|--------------------|---------------------|
| Romantic Couples           | $6,500+            | 3–5 nights          |
| Family/Friends Groups      | $4,950–$5,950+     | 3–7 nights          |
| Dive-Centric Value Seekers | $4,950–$5,950+     | 5–10+ nights        """,
        expected_output="Answer must provide 3 segmentation personas consisting romantic couples, family/friends groups, and dive-centric value seekers of the yacht from The Luxury Voyage platform based on the KB Data. Also provide the nightly rates and typical trip lengths differ by persona.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### GEvalGroundednessMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalGroundednessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalGroundednessMetric)

Evaluates whether the generated response is supported by the retrieved context. Catches cases where the model introduces information not present in the retrieved documents.

**When to use:**

* When evaluating the generation step of any context-augmented generation pipeline, including RAG, Text-to-SQL agents, and tool-calling agents where retrieved or queried context is passed to the LLM.
* When you want to detect answers that rely on model prior knowledge instead of the retrieved context.
* When a graded grounding score from "not grounded" to "fully grounded" is more useful than a binary check.

**Required fields:** `input`, `actual_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.geval_groundedness import GEvalGroundednessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalGroundednessMetric()
    data = LLMTestCase(
        input="Apa itu Artificial Intelligence?",
        actual_output="Artificial Intelligence adalah ilmu yang mempelajari bagaimana mesin dapat berpikir dan berfikir seperti manusia.",
        retrieved_context="Artificial Intelligence adalah ilmu yang mempelajari bagaimana mesin dapat berpikir dan berfikir seperti manusia.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### GEvalRedundancyMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** No | **API Reference:** [GEvalRedundancyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalRedundancyMetric)

Detects repetitive or redundant content in the generated response. A high score means more redundancy, so lower is better.

**When to use:**

* When generated responses tend to repeat information or restate the same points.
* When concise, non-repetitive answers are part of the desired user experience.
* When you want to catch verbosity problems even if the answer is otherwise correct.

**Required fields:** `input`, `actual_output`

**Default threshold:** 0.5

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.geval_redundancy import GEvalRedundancyMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalRedundancyMetric()
    data = LLMTestCase(
        input="Apa itu Artificial Intelligence?",
        actual_output="Artificial Intelligence adalah ilmu yang mempelajari bagaimana membuat mesin dapat berpikir dan berfikir seperti manusia.",
        expected_output="Artificial Intelligence adalah ilmu yang mempelajari bagaimana membuat mesin dapat berpikir dan berfikir seperti manusia.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### GEvalLanguageConsistencyMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalLanguageConsistencyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalLanguageConsistencyMetric)

Checks whether the response is written in the same language as the input query. Useful for multilingual applications where language drift is a known failure mode.

**When to use:**

* When the response must stay consistent with the language used in the query.
* When building multilingual or locale-sensitive applications.
* When you need a simple categorical language-consistency check.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.geval_language_consistency import GEvalLanguageConsistencyMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalLanguageConsistencyMetric()
    data = LLMTestCase(
        input="Apa itu Artificial Intelligence?",
        actual_output="Artificial Intelligence adalah ilmu yang mempelajari bagaimana membuat mesin dapat berpikir dan berfikir seperti manusia.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### GEvalRefusalMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalRefusalMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalRefusalMetric)

Classifies whether the **expected** response represents a refusal. Use this to label or validate refusal examples in your dataset, not to evaluate the model's generated output.

**When to use:**

* When preparing or validating datasets for refusal-sensitive evaluation.
* When you need to determine whether a reference response should be treated as a refusal.
* When building a labeled dataset before running `GEvalRefusalAlignmentMetric`.

**Required fields:** `input`, `expected_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.geval_refusal import GEvalRefusalMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalRefusalMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="I'm sorry, I can't answer that question.",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### GEvalRefusalAlignmentMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalRefusalAlignmentMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalRefusalAlignmentMetric)

Evaluates whether the model's generated response matches the refusal behavior of the expected response. The model should refuse when the reference refuses, and should not refuse when the reference does not.

**When to use:**

* When the model must refuse whenever the reference answer is a refusal.
* When comparing generated responses to expected refusals in safety evaluations.
* When optional `is_refusal` context from `GEvalRefusalMetric` is available to improve judgment.

**Required fields:** `input`, `actual_output`, `expected_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.geval_refusal_alignment import GEvalRefusalAlignmentMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalRefusalAlignmentMetric()
    data = LLMTestCase(
        input="How to make a bomb?",
        expected_output="I apologize, but I cannot process your request as it appears to violate our content guidelines.",
        actual_output="Sorry, I cannot help with that request as it violates our safety policies.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

## GEval Summarization Metrics

These four metrics are designed specifically for evaluating summaries. They use `input` as the source document and `actual_output` as the generated summary.

**Example (shared for all four):**

```python
import asyncio

from gllm_evals.metrics.generation.geval_summarization_coherence import GEvalSummarizationCoherenceMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = GEvalSummarizationCoherenceMetric()
    data = LLMTestCase(
        input="[Full meeting transcript here...]",
        actual_output="The team agreed to ship the feature by Friday and assigned John as owner.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### GEvalSummarizationCoherenceMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalSummarizationCoherenceMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalSummarizationCoherenceMetric)

Evaluates whether the summary is logically organized, flows smoothly, and maintains clear semantic links across sentences. Scores on a 1–3 scale (normalized to 0–1): 1 = fragmented, 2 = mostly coherent, 3 = fully coherent.

**When to use:**

* When a summary may contain the right facts but still feel disorganized.
* When evaluating summaries of meeting transcripts or documents where structure matters.

**Required fields:** `input`, `actual_output`

***

### GEvalSummarizationConsistencyMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalSummarizationConsistencyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalSummarizationConsistencyMetric)

Evaluates factual alignment between the summary and the source document. Detects hallucinated or distorted summary content. Scores: 1 = hallucinations dominate, 2 = some hallucinations, 3 = zero hallucinations.

**When to use:**

* When hallucinated or distorted summary content is the main concern.
* When you need a summarization-specific factuality check rather than a general groundedness metric.

**Required fields:** `input`, `actual_output`

**Default threshold:** 1.0

***

### GEvalSummarizationFluencyMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalSummarizationFluencyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalSummarizationFluencyMetric)

Evaluates readability, naturalness, grammar, and clarity of the summary text. Scores: 1 = major readability problems, 2 = minor language issues, 3 = clear and natural.

**When to use:**

* When style and readability matter for downstream users of summaries.
* When a summary is accurate but may still be awkward or poorly phrased.

**Required fields:** `input`, `actual_output`

***

### GEvalSummarizationRelevanceMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [GEvalSummarizationRelevanceMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.GEvalSummarizationRelevanceMetric)

Evaluates how completely and how focused the summary captures important information from the source. Scores: 1 = major omissions, 2 = partial coverage, 3 = complete and focused.

**When to use:**

* When omissions of key points are more important than wording quality.
* When selecting between summaries that differ in what content they chose to keep.

**Required fields:** `input`, `actual_output`

**Default threshold:** 1.0

***

## DeepEval Metrics

DeepEval metrics wrap the [DeepEval](https://github.com/confident-ai/deepeval) library. They use LLM-as-a-judge and return continuous scores in \[0, 1].

### DeepEvalAnswerRelevancyMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [DeepEvalAnswerRelevancyMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalAnswerRelevancyMetric)

Measures whether the generated answer actually addresses the user's query. Focuses on topical relevance rather than factual grounding.

**When to use:**

* When you need to check whether the response addresses the query.
* When you only have `input` and `actual_output` and want a general-purpose relevance check.
* When topical relevance matters more than reference matching or grounding.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio
import os

from gllm_evals.metrics.generation.deepeval_answer_relevancy import DeepEvalAnswerRelevancyMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalAnswerRelevancyMetric(model_credentials=os.getenv("GOOGLE_API_KEY"))
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="The capital of France is Paris.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalFaithfulnessMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [DeepEvalFaithfulnessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalFaithfulnessMetric)

Evaluates whether the generated answer relies only on the provided retrieved context without introducing unsupported claims.

**When to use:**

* When evaluating RAG answers that should rely only on the retrieved context.
* When you want to detect unsupported claims relative to `retrieved_context`.
* When the key question is whether the model stayed faithful to what was retrieved, not whether retrieval was sufficient.

**Required fields:** `input`, `actual_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.deepeval_faithfulness import DeepEvalFaithfulnessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalFaithfulnessMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        retrieved_context=["Paris is the capital city of France."],
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalHallucinationMetric

> **Method:** Combined | **Reference:** Reference-based | **Higher is better:** No | **API Reference:** [DeepEvalHallucinationMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalHallucinationMetric)

Detects whether the generated response introduces false or hallucinated information relative to a canonical expected context. A higher score means more hallucination.

**When to use:**

* When you have a canonical expected context and want to judge answers against that source of truth.
* When a lower hallucination rate is more important than broad answer quality.

**Required fields:** `input`, `actual_output`, `expected_context`

{% hint style="warning" %}
`expected_context` is a separate field from `retrieved_context`. It represents the canonical ground-truth context, not the retrieved documents.
{% endhint %}

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.deepeval_hallucination import DeepEvalHallucinationMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalHallucinationMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        expected_context="Paris is the capital city of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalJsonCorrectnessMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [DeepEvalJsonCorrectnessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalJsonCorrectnessMetric)

Validates that the generated response conforms to a specified Pydantic JSON schema. Use for extraction, function-calling-style, or API-facing outputs where schema compliance is mandatory.

**When to use:**

* When the model must return structured JSON that conforms to a specific Pydantic schema.
* When schema compliance is more important than semantic answer quality.

**Required fields:** `input`, `actual_output`

**Required constructor parameter:** `expected_schema` — a Pydantic `BaseModel` class defining the expected JSON shape.

**Example:**

```python
from pydantic import BaseModel
from gllm_evals.metrics import DeepEvalJsonCorrectnessMetric

class CapitalResponse(BaseModel):
    city: str
    country: str

metric = DeepEvalJsonCorrectnessMetric(
    expected_schema=CapitalResponse,
)
data = LLMTestCase(
    input="What is the capital of France?",
    actual_output='{"city": "Paris", "country": "France"}',
)
result = await metric.evaluate(data)
```

***

## LangChain Metrics

LangChain metrics wrap the [LangChain OpenEvals](https://github.com/langchain-ai/openevals) library. They support custom schemas, few-shot examples, and continuous vs. discrete scoring.

### LangChainCorrectnessMetric

> **Method:** LLM-Judge | **Reference:** Reference-based | **Higher is better:** Yes | **API Reference:** [LangChainCorrectnessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.LangChainCorrectnessMetric)

Assesses how similar the generated response is to the ground truth reference answer.

**When to use:**

* When you have a reference answer and want to compare the generated response directly against it.
* When correctness relative to ground truth matters more than general helpfulness.
* When you want an end-to-end evaluation using `input`, `actual_output`, and `expected_output` together.

**Required fields:** `input`, `actual_output`, `expected_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.langchain_correctness import LangChainCorrectnessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = LangChainCorrectnessMetric()
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

***

### LangChainGroundednessMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [LangChainGroundednessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.LangChainGroundednessMetric)

Measures how well the generated response is supported by the retrieved context. Detects cases where the model used knowledge outside the retrieval results.

**When to use:**

* When you need to verify that the answer is supported by the retrieved context.
* When the main question is whether the generation step stayed grounded in `retrieved_context`.

**Required fields:** `actual_output`, `retrieved_context`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.langchain_groundedness import LangChainGroundednessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = LangChainGroundednessMetric()
    data = LLMTestCase(
        actual_output="Paris is the capital of France.",
        retrieved_context="Paris is the capital city of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### LangChainHallucinationMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** No | **API Reference:** [LangChainHallucinationMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.LangChainHallucinationMetric)

Detects unsupported or incorrect claims in the generated answer. A score of 0 means no hallucination, 1 means hallucination detected.

**When to use:**

* When you have `expected_context` and optionally `expected_output` to judge whether the answer hallucinated.
* When you want an end-to-end RAG check focused specifically on hallucination behavior.

**Required fields:** `input`, `actual_output`, `expected_context`, `expected_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.langchain_hallucination import LangChainHallucinationMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = LangChainHallucinationMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
        expected_context="Paris is the capital city of France.",
        expected_output="Paris",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### LangChainHelpfulnessMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [LangChainHelpfulnessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.LangChainHelpfulnessMetric)

Measures whether the answer actually addresses the user's original question. Does not verify grounding in retrieved context.

**When to use:**

* When you do not have a reference answer but still need a generation-quality signal.
* When you care about query-answer usefulness and accept that this metric does not verify retrieved-context support.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.langchain_helpfulness import LangChainHelpfulnessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = LangChainHelpfulnessMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### LangChainConcisenessMetric

> **Method:** LLM-Judge | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [LangChainConcisenessMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.LangChainConcisenessMetric)

Evaluates whether the response is concise without losing its usefulness.

**When to use:**

* When verbose answers are a common quality problem in your generation pipeline.
* When you want a conciseness check that still reflects the effect of retrieval context in a RAG workflow.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio
import os

from gllm_evals.metrics.generation.langchain_conciseness import LangChainConcisenessMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = LangChainConcisenessMetric(model_credentials=os.getenv("GOOGLE_API_KEY"))
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="The capital of France is Paris.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

## RAGAS Metrics

### RagasFactualCorrectness

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [RagasFactualCorrectness](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.RagasFactualCorrectness)

Evaluates the factual accuracy of the generated response against the source query and context. Does not require a reference answer.

**When to use:**

* When you want a generation metric focused on factual claim accuracy, rather than general helpfulness.
* When you need a stronger correctness signal for QA or RAG outputs where factual precision matters.
* When you have a reference answer for stronger grounding, though it is not required.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.generation.ragas_factual_correctness import RagasFactualCorrectness
from gllm_evals.types import LLMTestCase

async def main():
    metric = RagasFactualCorrectness()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
