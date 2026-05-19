# Vector Retriever (Legacy)

{% hint style="warning" %}
**Deprecated**: This retriever is deprecated and will be removed in 0.6.0. For new applications, use the [Vector Retriever](../vector-retriever.md) with the capability-based data store API.
{% endhint %}

**BasicVectorRetriever** is the previous vector retriever implementation. It works only with the legacy `BaseVectorDataStore` interface (e.g., `ChromaVectorDataStore`).

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Vector Data Store (Legacy)](../../../data-store/legacy/vector-data-store/)
2. [EM Invoker](../../../inference/em-invoker.md) for embeddings

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-retrieval"
```
{% endtab %}
{% endtabs %}

## What it does

The legacy Vector Retriever uses a single `BaseVectorDataStore` (e.g., `ChromaVectorDataStore`) for document retrieval. It accepts a single query string and optional `top_k`, `retrieval_params`, and `threshold`.

## Usage

```python
from gllm_datastore.vector_data_store.chroma_vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever

vector_store = ChromaVectorDataStore(
    collection_name="documents",
    embedding=OpenAIEMInvoker(model_name="text-embedding-3-small")
)
retriever = BasicVectorRetriever(vector_store)

query = "What is machine learning?"
results = await retriever.retrieve(query, top_k=10)
```

With metadata filtering (syntax depends on the data store):

```python
retrieval_params = {
    "filter": {"$and": [{"type": "document"}]},
    "where_document": {"$contains": {"text": "AI"}},
}
results = await retriever.retrieve(query, top_k=10, retrieval_params=retrieval_params)
```

## Migration

Switch to the [Vector Retriever](../vector-retriever.md): use a data store with vector capability (e.g., `ChromaDataStore(...).with_vector(em_invoker=...)`) and `VectorRetriever` from `gllm_retrieval.retriever`.
