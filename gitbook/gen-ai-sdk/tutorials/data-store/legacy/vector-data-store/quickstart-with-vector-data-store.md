---
hidden: true
---

# Quickstart with Vector Data Store

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-datastore"
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-datastore"
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-datastore"
```

{% endtab %}
{% endtabs %}

## Save and Retrieve Data

Let's walk through practical example for vector datastore type. This example will show you how to get started quickly and demonstrate common patterns you'll use in your own projects.

```python
from gllm_core.schema import Chunk
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

# Initialize vector store with embedding model
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
vector_store = ChromaVectorDataStore(
    collection_name="documents",
    embedding=em_invoker
)

# Add chunks to the store
chunks = [
    Chunk(content="AI is the future."),
    Chunk(content="Parrot is a bird."),
]
await vector_store.add_chunks(chunks)

# Query by semantic similarity
results = await vector_store.query(query="artificial intelligence")
```

## Metadata Filtering

Instead of relying solely on a string for semantic queries, we can also apply metadata filtering through the `retrieval_params` parameter in the `query()` method. For example, in `ChromaVectorDataStore`, the retrieval parameter can be used as follows:

```python
# Add chunks to the store
chunks = [
    Chunk(content="AI is the future.", metadata={"type": "document"}),
    Chunk(content="Parrot is a bird.", metadata={"type": "document"}),
]
await vector_store.add_chunks(chunks)

retrieval_params = {
    "filter": {
        "$and": [
            {"type": "document"},
        ]
    },
    "where_document": {"$contains": {"text": "AI"}},
}

results = await vector_store.query(query="artificial intelligence")
```
