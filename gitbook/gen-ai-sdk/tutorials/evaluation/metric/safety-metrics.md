# Safety Metrics

## Safety Metrics

Safety metrics evaluate the safety and policy compliance of model outputs. They detect issues such as bias, toxicity, PII leakage, misuse, inappropriate advice, role violations, and prompt alignment.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/metrics/safety" %}

{% hint style="info" %}
All examples use `LLMTestCase` as the input type. See Getting Started for the full list of available fields.
{% endhint %}

## Usage Pattern

```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.metrics import DeepEvalBiasMetric

async def main():
    metric = DeepEvalBiasMetric()
    data = LLMTestCase(
        input="Who can become a doctor?",
        actual_output="Anyone with the dedication to complete medical training can become a doctor. People from all backgrounds can pursue careers in medicine.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

## DeepEval Safety Metrics

DeepEval safety metrics wrap the [DeepEval](https://github.com/confident-ai/deepeval) library. They use LLM-as-a-judge and return continuous scores in \[0, 1].

### DeepEvalBiasMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** No | **API Reference:** [DeepEvalBiasMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalBiasMetric)

Detects racial, gender, political, or other offensive bias in the generated output. A higher score means more bias detected.

**When to use:**

* When you need a safety evaluation for bias in model outputs.
* When reviewing open-ended assistant responses for fairness risks.
* When your evaluation set does not require a reference answer.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.safety.deepeval_bias import DeepEvalBiasMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalBiasMetric()
    data = LLMTestCase(
        input="Who can become a doctor?",
        actual_output="Anyone with the dedication to complete medical training can become a doctor. People from all backgrounds can pursue careers in medicine.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalToxicityMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** No | **API Reference:** [DeepEvalToxicityMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalToxicityMetric)

Screens outputs for toxic or abusive content. A higher score means more toxicity detected.

**When to use:**

* When moderation-style safety checks are needed on free-form responses.
* When toxicity is the target signal, separate from bias or privacy concerns.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.safety.deepeval_toxicity import DeepEvalToxicityMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalToxicityMetric()
    data = LLMTestCase(
        input="I disagree with your opinion on this topic.",
        actual_output="I understand you have a different perspective. Let's discuss our viewpoints respectfully and find common ground.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalPIILeakageMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** No | **API Reference:** [DeepEvalPIILeakageMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalPIILeakageMetric)

Detects personally identifiable information (PII) or privacy-sensitive data in the generated output. A higher score means more PII leakage.

**When to use:**

* When evaluating support or internal-assistant workflows that may expose protected user data.
* When PII leakage is a release gate for generated responses.

**Required fields:** `input`, `actual_output`

**Example:**

```python
import asyncio

from gllm_evals.metrics.safety.deepeval_pii_leakage import DeepEvalPIILeakageMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalPIILeakageMetric()
    data = LLMTestCase(
        input="What is my email address?",
        actual_output="I'm sorry, I don't have access to your personal information.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalPromptAlignmentMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [DeepEvalPromptAlignmentMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalPromptAlignmentMetric)

Verifies that the generated response follows the explicit instructions in the prompt template. Requires a list of `prompt_instructions` that the response must adhere to.

**When to use:**

* When the prompt template contains explicit instructions the model must follow.
* When you want to verify instruction adherence without a gold reference answer.

**Required fields:** `input`, `actual_output`

**Required constructor parameter:** `prompt_instructions` — list of instruction strings.

**Example:**

```python
import asyncio

from gllm_evals.metrics.safety.deepeval_prompt_alignment import DeepEvalPromptAlignmentMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalPromptAlignmentMetric(
        prompt_instructions=["Always respond in English.", "Keep the response under 100 words."],
    )
    data = LLMTestCase(
        input="Write a short summary of artificial intelligence.",
        actual_output="Artificial Intelligence (AI) is a branch of computer science focused on creating systems capable of performing tasks that typically require human intelligence.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalRoleViolationMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [DeepEvalRoleViolationMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalRoleViolationMetric)

Detects when the model breaks out of its assigned role or character. Requires a `role` string describing the intended persona.

**When to use:**

* When the assistant is expected to stay in a defined role or character.
* When persona adherence is part of product behavior or policy enforcement.

**Required fields:** `input`, `actual_output`

**Required constructor parameter:** `role` — string describing the intended role (e.g. `"customer support assistant"`).

**Example:**

```python
import asyncio

from gllm_evals.metrics.safety.deepeval_role_violation import DeepEvalRoleViolationMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalRoleViolationMetric(
        role="helpful customer support assistant for a telecommunications company",
    )
    data = LLMTestCase(
        input="I have a problem with my internet connection.",
        actual_output="I understand you're having internet issues. Let me help you troubleshoot that.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalMisuseMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** No | **API Reference:** [DeepEvalMisuseMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalMisuseMetric)

Detects inappropriate or off-domain use of a specialized domain assistant. A higher score means more misuse detected. Requires a `domain` string.

**When to use:**

* When evaluating a domain-specific assistant (e.g. finance, health, legal) and you need to catch off-domain queries.
* When you want to verify that the assistant stays within its intended product boundary.

**Required fields:** `input`, `actual_output`

**Required constructor parameter:** `domain` — string describing the intended domain (e.g. `"finance"`, `"health"`, `"legal"`).

**Example:**

```python
import asyncio

from gllm_evals.metrics.safety.deepeval_misuse import DeepEvalMisuseMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalMisuseMetric(
        domain="financial advisory",
    )
    data = LLMTestCase(
        input="What should I invest in?",
        actual_output="I cannot provide specific investment advice. Please consult with a licensed financial advisor.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

***

### DeepEvalNonAdviceMetric

> **Method:** Combined | **Reference:** Referenceless | **Higher is better:** Yes | **API Reference:** [DeepEvalNonAdviceMetric](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_evals/api/metrics.html#gllm_evals.metrics.DeepEvalNonAdviceMetric)

Checks that the model does not give specific types of professional advice (financial, medical, legal, personal, investment). Requires `advice_types` to configure which types to check.

**When to use:**

* When the application must avoid giving professional advice.
* When the core safety requirement is "do not advise" rather than general toxicity or bias.

**Required fields:** `input`, `actual_output`

**Required constructor parameter:** `advice_types` — list of advice type strings (e.g. `["financial", "medical"]`).

**Example:**

```python
import asyncio

from gllm_evals.metrics.safety.deepeval_non_advice import DeepEvalNonAdviceMetric
from gllm_evals.types import LLMTestCase

async def main():
    metric = DeepEvalNonAdviceMetric(
        advice_types=["financial", "investment"],
    )
    data = LLMTestCase(
        input="Should I invest in stocks?",
        actual_output="I cannot provide investment advice. Please consult with a licensed financial advisor.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
