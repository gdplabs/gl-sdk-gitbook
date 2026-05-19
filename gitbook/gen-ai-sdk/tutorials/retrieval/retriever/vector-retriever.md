# Vector Retriever

## What's a Vector Retriever?

**Vector Retriever** is the most commonly used retriever type for document-based applications. It retrieves documents from a data store with vector capability using semantic similarity search.

**Best For**:

* Document search and retrieval
* Semantic similarity matching
* Large-scale text corpora
* Unstructured data search

**Key Features**:

* Embedding-based similarity search
* Support for data stores with vector capability (Chroma, Elasticsearch, Redis, etc.)
* Metadata filtering and scoring
* Configurable similarity thresholds and batch queries

**Use Cases**:

* Document Q\&A systems
* Content recommendation engines
* Semantic search applications
* Knowledge base retrieval

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

You should be familiar with these concepts:

1. [Data Store](../../data-store/README.md) and the vector capability
2. [EM Invoker](../../inference/em-invoker.md) for embeddings

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

## What it does

The Vector Retriever retrieves relevant documents from a data store with vector capability based on semantic similarity to a query. It provides a standardized interface for document retrieval operations in Gen AI applications.

## Usage

Use `VectorRetriever` with a data store that has vector capability registered:

```python
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker.openai_em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import VectorRetriever

# Data store with vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
data_store = ChromaDataStore(
    collection_name="documents",
    client_type=ChromaClientType.MEMORY,
).with_vector(em_invoker=em_invoker)

retriever = VectorRetriever(data_store=data_store)

# Single query
query = "What is machine learning?"
results = await retriever.retrieve(query, top_k=10)

# Single query with filters and threshold
from gllm_datastore.core.filters import filter as F
results = await retriever.retrieve(
    "What is machine learning?",
    query_filter=F.eq("metadata.category", "AI"),
    top_k=10,
    threshold=0.8
)

# Batch queries
batch_results = await retriever.retrieve(["query 1", "query 2"], top_k=10)
```

{% hint style="info" %}
**Implementation notes**: Filter syntax depends on the data store backend. See [Query filters](../../data-store/query-filter.md) and the backend documentation for supported operators and field names.
{% endhint %}

The previous vector retriever implementation (`BasicVectorRetriever`) is deprecated. See [Vector Retriever (Legacy)](legacy/vector-retriever.md) only if you still use the legacy vector data store API.
