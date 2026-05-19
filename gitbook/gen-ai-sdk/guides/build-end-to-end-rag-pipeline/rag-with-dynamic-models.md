---
icon: gears
---

# RAG with Dynamic Models

This guide will walk you through the process of creating a Pipeline where the model is not fixed. This is useful for RAG applications where users can freely select their models.

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.
2. An Elastic Search vector data store that is already set up and available for use. Refer to [supported-vector-data-store.md](../../resources/supported-vector-data-store.md "mention") and [index-your-data-with-vector-data-store.md](../index-your-data-with-vector-data-store.md "mention").

You must have already completed the following tutorial:

1. [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```

{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Extend Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the previous tutorial. Add the query transformer component to your existing structure:

You'll extend your existing structure with this new file:

```
rag-with-dynamic-models/
├── data/
│   └── chroma.sqlite3
├── .env
├── .env.example
├── pipeline.py                     # 👈 Updated with dynamic model pipeline
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```

{% endstep %}
{% endstepper %}

{% hint style="warning" %}
Make sure you already set up the API keys for the models that you'd like to try. Refer to [supported-models.md](../../resources/supported-models.md "mention") for the supported models.
{% endhint %}

## 1) Make the response synthesizer dynamic

For the user to be able to utilize different models, we will make the response synthesizer dynamic. To do this, we will wrap the response synthesizer inside a builder function, like so.

{% code title="response_synthesizer.py" %}

```python
from gllm_generation.response_synthesizer import ResponseSynthesizer


def build_response_synthesizer(model_id: str) -> ResponseSynthesizer:
    """Build a response synthesizer for the given model.

    Args:
        model_id (str): The model identifier to use for the LM request processor.

    Returns:
        ResponseSynthesizer: Synthesizer configured with the given model.
    """
    return ResponseSynthesizer.preset.stuff(model_id)

```

{% endcode %}

## 2) Make the pipeline dynamic

Next, we will make the pipeline itself dynamic.

{% stepper %}
{% step %}
**Import the response synthesizer builder**

Since it is the response synthesizer that will handle the calls to the different LMs, we change our import from using the prebuilt component to using the `build_response_synthesizer` function that we created in the previous step.

```python
from modules.response_synthesizer import build_response_synthesizer
```

{% endstep %}

{% step %}
**Wrap the pipeline inside a builder function**

Similarly, we need to make it so that the Pipeline is dynamic by wrapping it inside a builder function, which builds a new pipeline with the selected model.

```python
import asyncio
from gllm_pipeline.steps import step
from gllm_pipeline.pipeline import Pipeline
from modules.response_synthesizer import build_response_synthesizer
from modules.retriever import retriever

def build_pipeline(model_id: str) -> Pipeline:
    """Build the end-to-end pipeline.

    Args:
        model_id (str): Model identifier used to build the response synthesizer.

    Returns:
        Any: A composed pipeline with .invoke(state, config) coroutine method.
    """
    # The following steps stay the same
    retriever_step = step(
        retriever,
        input_map={"query": "user_query", "top_k": "top_k"},
        output_state="chunks",
    )

    response_synthesizer_step = step(
        component=response_synthesizer,
        input_map={
            "query": "user_query",
            "chunks": "chunks",
        },
        output_state="response",
    )
    return retriever_step | response_synthesizer_step

```

{% endstep %}
{% endstepper %}

## 3) Run the pipeline

To run the pipeline, we modify the main block as follows:

```python
if __name__ == "__main__":
    model_id = "openai/gpt-4.1-nano"  # Change this to whatever you want
    e2e_pipeline = build_pipeline(model_id)
    state = {
        "user_query": "Give me nocturnal creature from the dataset",  # Replace with your actual query
    }

    config = {
        "top_k": 5,
        "debug": True,  # Set to True to look at the pipeline execution flow
    }

    result = asyncio.run(e2e_pipeline.invoke(state, config))
    print(f"Response: {result['response']}")

```

You should get a response similar to this:

```
Response: Here are three aquatic animals from the provided context:

1. Aquaflare - A marine creature found near the volcanic isles of Pyronia, with heat-resistant scales and the ability to withstand extreme temperatures.

2. Starburst Lionfish - A solitary fish living in the coral reefs of Celestial Sea, known for its luminescent fins and mild toxin.

3. Aquaglow Jelly - A translucent bioluminescent jellyfish that drifts in the depths of Azure Lake, feeding on microscopic organisms.
```

## 📂 Complete Guide Files

{% file src="../../../.gitbook/assets/dynamic-model-250923.zip" %}

Congratulations! You have created an RAG pipeline with dynamic models!
