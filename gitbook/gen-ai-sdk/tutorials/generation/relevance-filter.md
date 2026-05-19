---
icon: arrow-down-wide-short
---

# Relevance Filter

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/relevance_filter)| <mark style="color:green;background-color:green;">Involves EM</mark> | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | Tutorial: [relevance-filter.md](relevance-filter.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/relevance_filter.html)

## What’s a Relevance Filter?

The **relevance filter** is a utility module designed to filter context chunks based on their relevance with the user query. In this tutorial, you'll learn how to use the `SimilarityBasedRelevanceFilter` .

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [lm-invoker](../inference/lm-invoker/ "mention")
2. [EM Invoker](../inference/em-invoker.md "mention")
3. [lm-request-processor.md](../inference/lm-request-processor.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-generation"
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-generation"
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-generation"
```

{% endtab %}
{% endtabs %}

## Quickstart

Let’s jump into a basic example using `SimilarityBasedRelevanceFilter`. Since it utilizes an embedding model, we can simply pass an EM invoker to build one. We can also set a threshold to control how strictness of the candidate chunks filtering.

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import build_em_invoker
from gllm_generation.relevance_filter import SimilarityBasedRelevanceFilter

candidate_chunks = [
    Chunk(content="Indonesia is a country in Southeast Asia.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="Malaysia is a country in Southeast Asia.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="Singapore is a country in Southeast Asia.", metadata={"file_name": "singapore.txt"}),
    Chunk(content="The capital of Indonesia is Jakarta.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="The capital of Malaysia is Kuala Lumpur.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="The capital of Singapore is Singapore.", metadata={"file_name": "singapore.txt"}),
]
query = "In what part of Asia is Indonesia located? And what's its capital city?"

em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
relevance_filter = SimilarityBasedRelevanceFilter(em_invoker, threshold=0.6)
filtered_chunks = asyncio.run(relevance_filter.filter(chunks=candidate_chunks, query=query))
print(filtered_chunks)
```

**Expected Output**

```
[
    Chunk(
        id='13862359-42d7-4684-bb09-95d03ea74bff',
        content='Indonesia is a country in Southeast Asia.',
        metadata={'file_name': 'indonesia.txt'} score=None),
    ),
    Chunk(
        id='ef4eb6c6-16d0-4318-86c0-cd010b8afb08',
        content='The capital of Indonesia is Jakarta.',
        metadata={'file_name': 'indonesia.txt'},
    ),
]
```

[^1]: This component may involve Language Model (LM). See tutorial about LM Request Processor or related [here](relevance-filter.md#lm-request-processor)
