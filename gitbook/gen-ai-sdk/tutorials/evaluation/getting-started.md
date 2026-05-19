# 🚀 Getting Started

## Introduction

This tutorial will guide you step-by-step on how to install the GenAI Evaluator SDK and run your first evaluation.

{% embed url="https://github.com/gdplabs/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/evaluations/getting_started" %}

<details>

<summary>Prerequisites</summary>

Before installing, make sure you have:

1. [Python 3.11+](https://glair.gitbook.io/hello-world/prerequisites#python-v3.11-or-v3.12)
2. [Pip](https://pip.pypa.io/en/stable/installation/)
3. [OpenAI API Key](https://platform.openai.com/api-keys)
4. [gcloud CLI](https://cloud.google.com/sdk/docs/install) - required because `gllm-evals` is a private library hosted in a private Google Cloud repository

After installing, please run

```bash
gcloud auth login
```

to authorize gcloud to access the Cloud Platform with Google user credentials.

{% hint style="info" %}
Our internal `gllm-evals` package is hosted in a secure Google Cloud Artifact Registry.\
You need to authenticate via `gcloud CLI` to access and download the package during installation.
{% endhint %}

</details>

## Installation

{% tabs %}
{% tab title="Linux or Windows WSL" %}
Run the following command to install

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
Run the following command to install

```bash
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-evals[deepeval,langchain,ragas]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
Run the following command to install

```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-evals[deepeval,langchain,ragas]"
```
{% endtab %}
{% endtabs %}

## Environment Setup

Set a valid language model credential as an environment variable. This API Key will be used for evaluators that uses LLM as judge.

* In this example, let's use an Google API Key.

{% hint style="info" %}
**Get an Google API key from** [**Google AI Studio**](https://aistudio.google.com/api-keys)**.**
{% endhint %}

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
export GOOGLE_API_KEY="AIz..."
```
{% endtab %}

{% tab title="Windows Powershell" %}
```bash
$env:GOOGLE_API_KEY = "AIz..."
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
set GOOGLE_API_KEY="AIz..."
```
{% endtab %}
{% endtabs %}

## LLMTestCase

`LLMTestCase` is the canonical input type for all evaluators. It holds your precomputed model outputs and any supporting context needed for evaluation.

| Field                       | Type               | Required | Description                                                                         |
| --------------------------- | ------------------ | -------- | ----------------------------------------------------------------------------------- |
| `input`                     | `str`              | ✓        | The user question or prompt.                                                        |
| `actual_output`             | `str`              | ✓        | The model's generated response to evaluate.                                         |
| `expected_output`           | `str`              | optional | The reference or ground truth answer.                                               |
| `retrieved_context`         | `str \| list[str]` | optional | Supporting context/documents used during generation (e.g., RAG retrieved chunks).   |
| `tools_called`              | `list[dict]`       | optional | Actual tools called by the agent.                                                   |
| `expected_tools`            | `list[dict]`       | optional | Reference tools expected to be called.                                              |
| `agent_trajectory`          | `list[dict]`       | optional | Full agent trajectory (parsed as `tools_called` if `tools_called` is not provided). |
| `expected_agent_trajectory` | `list[dict]`       | optional | Reference trajectory for comparison.                                                |

{% hint style="warning" %}
`actual_output` must be provided by you — the evaluators do **not** run inference. You are responsible for generating model responses beforehand and populating this field before calling `evaluate()`.
{% endhint %}

Not every evaluator uses every field — each evaluator only reads the fields it needs and skips metrics that are missing required data.

**Creating a single data point:**

```python
from gllm_evals import LLMTestCase

data = LLMTestCase(
    input="What is the capital of France?",
    actual_output="Paris",
    expected_output="Paris is the capital of France.",
    retrieved_context="Paris is the capital city of France.",
)
```

**Loading from a dataset:**

```python
from gllm_evals import LLMTestCase, load_simple_qa_dataset
from gllm_evals.utils.demo_utils import your_ai_func_result

data = [
    LLMTestCase(
        input=row["query"],
        actual_output=your_ai_func_result(row["query"])["actual output"],
        expected_output=row["expected_response"],
        retrieved_context=your_ai_func_result(row["query"])["retrieved_context"],
    )
    for row in DictDataset.from_csv("examples/sample_data/simple_qa_data.csv").load()
]
```

## Running Your First Evaluation

In this tutorial, we will evaluate RAG pipeline output.

{% stepper %}
{% step %}
Create a script called `eval.py`. Choose one of the following approaches based on your needs:

{% tabs %}
{% tab title="Using Metric" %}
```python
import asyncio

from gllm_evals import LLMTestCase
from gllm_evals.metrics import GEvalCompletenessMetric

async def main():
    metric = GEvalCompletenessMetric()
    data = LLMTestCase(
        input="What is the capital of France?",
        actual_output="New York",
        expected_output="Paris is the capital of France.",
    )
    result = await metric.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
{% endtab %}

{% tab title="Using Evaluator" %}
```python
import asyncio
import os
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.types import LLMTestCase

async def main():
    model = build_lm_invoker(
        "google/gemini-3-flash-preview",
        os.getenv("GOOGLE_API_KEY"),
    )
    evaluator = GEvalGenerationEvaluator(models=model)

    data = LLMTestCase(
        input="What is the capital of France?",
        expected_output="Paris",
        actual_output="New York",
        retrieved_context="Paris is the capital of France.",
    )

    result = await evaluator.evaluate(data)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```
{% endtab %}
{% endtabs %}

By default, eval uses Gemini 3 Flash from Google as its model. If you want to use your own model, pass a `BaseLMInvoker` via the `models` parameter, or pass `models=[invoker] * N` for multi-judge evaluation.
{% endstep %}

{% step %}
Run the script

```bash
python eval.py
```
{% endstep %}

{% step %}
The evaluator will generate a response for the given input, e.g.:

```python
{
    "generation": {
        "aggregate_explanation": "The following metrics failed to meet expectations:\n1. Completeness is 0 (should be 0.5)\n2. Groundedness is 0 (should be 0.5)",
        "aggregate_success": false,
        "aggregate_score": 0.3333333333333333,
        "completeness": {
            "score": 0.0,
            "explanation": "The minimum key facts are: [Paris]. The Generated Response identifies 'New York' as the capital, which directly contradicts the expected fact [Paris] per Step 5A. Since the single required key fact is contradicted and not matched, the response fails to provide a correct answer per Step 5C Coverage Rule.",
            "rubric_score": 1,
            "success": false,
            "threshold": 0.5,
            "strict_mode": false,
            "higher_is_better": true,
        },
        "redundancy": {
            "score": 0.0,
            "explanation": "The response consists of a single phrase with no repeated words or paraphrased ideas. Each element of the answer is presented only once, maintaining high conciseness without any redundancy.",
            "rubric_score": 1,
            "success": true,
            "threshold": 0.4,
            "strict_mode": false,
            "higher_is_better": false,
        },
        "groundedness": {
            "score": 0.0,
            "explanation": "The output provides 'New York' as the answer, which is a critical factual contradiction of the retrieval context stating that 'Paris is the capital of France.'",
            "rubric_score": 1,
            "success": false,
            "threshold": 0.5,
            "strict_mode": false,
            "higher_is_better": true,
        },
        "is_refusal": false,
    }
}


```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Congratulations! You have successfully run your first evaluation
{% endhint %}

## Recommendation

If you want to run an end-to-end evaluation, use the [evaluate() helper function](evaluate-helper-function.md) instead of the step-by-step commands above.

It will automatically handle experiment tracking (via the [Experiment Tracker](experiment-tracker.md)) and integrates results into your existing [Dataset](dataset.md), so you don’t have to wire these pieces together manually.

## Next Steps

You're now ready to start using our evaluators. We offer several prebuilt evaluators to get you started:

1. [GEvalGenerationEvaluator](evaluator/#gevalgenerationevaluator)
2. [AgentEvaluator](evaluator/#agentevaluator)
3. [QueryTransformerEvaluator](evaluator/#querytransformerevaluator)
4. [ClassicalRetrievalEvaluator](evaluator/#classicalretrievalevaluator)

Looking for something else? [Build your own custom evaluator here.](evaluator/create-custom-evaluator-scorer.md)

<sup>\*All fields are optional and can be adjusted depending on the chosen metric.</sup>
