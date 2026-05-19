---
icon: landmark-magnifying-glass
---

# Reference Formatter

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/reference_formatter) | <mark style="color:green;background-color:green;">Involves EM</mark> | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [reference-formatter.md](reference-formatter.md "mention") | **Use Case:** [adding-document-references.md](../../guides/build-end-to-end-rag-pipeline/adding-document-references.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/relevance_filter.html)

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [lm-invoker](../inference/lm-invoker/ "mention")
2. [lm-request-processor.md](../inference/lm-request-processor.md "mention")

</details>

## What’s a Reference Formatter?

The **reference formatter** is a utility module designed to filter and format the references of an RAG pipeline response in a clear, standardized format. In this tutorial, you'll learn how to use the `SimilarityBasedReferenceFormatter` in **just a few lines of code**. You can also explore other types of reference formatters, available [here](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/reference_formatter.html).

## Supported Reference Formatter

| Formatter                           | Filtering method            | Best for                                                      |
| ----------------------------------- | --------------------------- | ------------------------------------------------------------- |
| `LMBasedReferenceFormatter`         | LM judgment                 | Rich semantic filtering; more accurate but slower             |
| `NoOpReferenceFormatter`            | None (pass-through)         | Development, pre-filtered inputs, or always-include-all cases |
| `SimilarityBasedReferenceFormatter` | Embedding cosine similarity | Fast, embedding-based filtering with a score threshold        |

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
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-generation"
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

Let’s jump into a basic example using `SimilarityBasedReferenceFormatter`. Since it utilizes an embedding model, we can simply pass an EM invoker to build one. We can also set a threshold to control how strictness of the candidate chunks filtering.

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import build_em_invoker
from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter

candidate_chunks = [
    Chunk(content="Indonesia is a country in Southeast Asia.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="Malaysia is a country in Southeast Asia.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="Singapore is a country in Southeast Asia.", metadata={"file_name": "singapore.txt"}),
    Chunk(content="The capital of Indonesia is Jakarta.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="The capital of Malaysia is Kuala Lumpur.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="The capital of Singapore is Singapore.", metadata={"file_name": "singapore.txt"}),
]
response = "Indonesia is a country in Southeast Asia. The capital of Indonesia is Jakarta."

em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
ref_formatter = SimilarityBasedReferenceFormatter(em_invoker, threshold=0.7)
references = asyncio.run(ref_formatter.format_reference(response=response, chunks=candidate_chunks))
print(references)
```

**Expected Output**

```
References:
1. indonesia.txt
```

That’s it! You've just successfully used the `StuffResponseSynthesizer`! You can try to play around with the threshold to find a value that works best for your use cases.

## Format Customization

The `SimilarityBasedReferenceFormatter` also supports customizing both the pre chunk display format as well as the entire references display format. These can bet set through the `format_chunk_func` and `format_references_func` parameters, respectively.

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import build_em_invoker
from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter

candidate_chunks = [
    Chunk(content="Indonesia is a country in Southeast Asia.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="Malaysia is a country in Southeast Asia.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="Singapore is a country in Southeast Asia.", metadata={"file_name": "singapore.txt"}),
    Chunk(content="The capital of Indonesia is Jakarta.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="The capital of Malaysia is Kuala Lumpur.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="The capital of Singapore is Singapore.", metadata={"file_name": "singapore.txt"}),
]
response = "Indonesia is a country in Southeast Asia. The capital of Indonesia is Jakarta."

def custom_format_chunk_func(chunk: Chunk) -> str:
    return f"{chunk.metadata['file_name']}: {chunk.content!r}"

def custom_format_references_func(formatted_chunks: list[str]) -> str:
    references = "=== REFERENCES ==="
    for idx, formatted_chunk in enumerate(formatted_chunks):
        references += f"\n[{idx + 1}] {formatted_chunk}"
    return references

em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
ref_formatter = SimilarityBasedReferenceFormatter(
    em_invoker,
    threshold=0.7,
    format_chunk_func=custom_format_chunk_func,
    format_references_func=custom_format_references_func,
)
references = asyncio.run(ref_formatter.format_reference(response=response, chunks=candidate_chunks))
print(references)
```

**Expected Output**

```
=== REFERENCES ===
[1] indonesia.txt: 'The capital of Indonesia is Jakarta.'
[2] indonesia.txt: 'Indonesia is a country in Southeast Asia.'
```

## Returning Raw Chunks

When desired, we can also skip the formatting part altogether by setting the `stringify` param to `False`. In this case, the `SimilarityBasedReferenceFormatter` will simply return the raw relevant chunks.

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import build_em_invoker
from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter

candidate_chunks = [
    Chunk(content="Indonesia is a country in Southeast Asia.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="Malaysia is a country in Southeast Asia.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="Singapore is a country in Southeast Asia.", metadata={"file_name": "singapore.txt"}),
    Chunk(content="The capital of Indonesia is Jakarta.", metadata={"file_name": "indonesia.txt"}),
    Chunk(content="The capital of Malaysia is Kuala Lumpur.", metadata={"file_name": "malaysia.txt"}),
    Chunk(content="The capital of Singapore is Singapore.", metadata={"file_name": "singapore.txt"}),
]
response = "Indonesia is a country in Southeast Asia. The capital of Indonesia is Jakarta."

em_invoker = build_em_invoker(model_id="openai/text-embedding-3-small")
ref_formatter = SimilarityBasedReferenceFormatter(em_invoker, threshold=0.7, stringify=False)
references = asyncio.run(ref_formatter.format_reference(response=response, chunks=candidate_chunks))
print(references)
```

**Expected Output**

<pre><code><strong>[
</strong><strong>    Chunk(
</strong><strong>        id='ef4eb6c6-16d0-4318-86c0-cd010b8afb08',
</strong><strong>        content='The capital of Indonesia is Jakarta.',
</strong><strong>        metadata={'file_name': 'indonesia.txt'},
</strong><strong>    ),
</strong><strong>    Chunk(
</strong><strong>        id='13862359-42d7-4684-bb09-95d03ea74bff',
</strong><strong>        content='Indonesia is a country in Southeast Asia.',
</strong><strong>        metadata={'file_name': 'indonesia.txt'},
</strong><strong>    ),
</strong><strong>]
</strong></code></pre>

Congratulations! You've finished the tutorial to use the `SimilarityBasedReferenceFormatter`!

[^1]: This component may involve Language Model (LM). See tutorial about LM Request Processor or related [here](reference-formatter.md#lm-request-processor)
