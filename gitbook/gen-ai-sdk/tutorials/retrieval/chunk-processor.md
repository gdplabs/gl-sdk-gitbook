---
icon: broom-wide
---

# Chunk Processor

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/chunk_processor) | **Tutorial**: [chunk-processor.md](chunk-processor.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/chunk_processor.html)

## What’s a Chunk Processor?

The **chunk processor** is a utility module designed to perform certain transformation on the retrieved chunks, such as deduplication and chunk merging. In this tutorial, you'll learn how to use the `DedupeChunkProcessor` in **just a few lines of code**. You can also explore other types of response synthesizers, available [here](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/chunk_processor.html).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-retrieval"
```
{% endtab %}
{% endtabs %}

## Deduplicating Chunks

Let’s jump into a basic example using `DedupeChunkProcessor`. As the name suggests, this component filters out chunks with duplicate IDs or contents.

1. For chunks with duplicate IDs, they will be considered as the exact same chunks, and therefore the duplicate will be omitted completely.
2. For chunks with duplicate contents, the IDs and metadatas of the duplicate will be stored in a new metadata named `dupes`.

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_retrieval.chunk_processor import DedupeChunkProcessor

chunks = [
    Chunk(id="chunk-1", content="Jakarta, Indonesia", metadata={"source": "source-1"}),
    Chunk(id="chunk-2", content="Kuala Lumpur, Malaysia", metadata={"source": "source-2"}),
    Chunk(id="chunk-3", content="Bangkok, Thailand", metadata={"source": "source-3"}),
    Chunk(id="chunk-1", content="Jakarta, Indonesia", metadata={"source": "source-1"}),  # Duplicate id with chunk-1
    Chunk(id="chunk-4", content="Kuala Lumpur, Malaysia", metadata={"source": "source-2"}), # Duplicate content with chunk-2
]

processor = DedupeChunkProcessor()
result = asyncio.run(processor.process_chunks(chunks))
print(result)
```

**Expected Output**

There should be no repeated or duplicated chunks in the output:

```
[
    Chunk(
        id='chunk-1',
        content='Jakarta, Indonesia',
        metadata={'source': 'source-1'},
    ),
    Chunk(
        id='chunk-2',
        content='Kuala Lumpur, Malaysia',
        metadata={
            'source': 'source-2',
            'dupes': {'chunk-4': {'source': 'source-2'}},
        },
    ),
    Chunk(
        id='chunk-3',
        content='Bangkok, Thailand',
        metadata={'source': 'source-3'},
    ),
]
```

That’s it! You've just successfully used the `DedupeChunkProcessor`!
