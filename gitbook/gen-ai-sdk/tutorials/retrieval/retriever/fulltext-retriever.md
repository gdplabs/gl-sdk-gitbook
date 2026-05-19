# Fulltext Retriever

## What's a Fulltext Retriever?

**Fulltext Retriever** uses a data store with fulltext capability to retrieve documents by keyword and fulltext search. Unlike a vector retriever, it matches on lexical and term-based signals (e.g., BM25, by-field, fuzzy) rather than semantic embeddings.

**Best For**:

* Keyword and phrase search.
* Exact or fuzzy term matching.
* Filter-only retrieval (no query text).
* Backends that support fulltext (e.g., Elasticsearch).

**Key Features**:

* Single-query or batch-query retrieval.
* Optional filters (metadata, field conditions).
* Strategy and parameters configurable via kwargs (e.g., BM25 `k1`, `b`).
* Returns `Chunk` lists with relevance scores.

**Use Cases**:

* Product or document search by keywords.
* Filtered retrieval without a search string.
* Combining with vector search in hybrid setups (when hybrid retriever is available).

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Data Store](../../data-store/) and the fulltext capability.
2. A data store backend that supports fulltext (e.g., Elasticsearch with fulltext).

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

The Fulltext Retriever performs retrieval using the data store's fulltext capability. You can pass a single query string, a list of queries (batch), or no query and rely on filters only. Results are returned as `Chunk` objects with scores.

## Basic usage

```python
from gllm_datastore.core.filters import filter as F
from gllm_datastore.data_store.elasticsearch.fulltext import SupportedQueryMethods
from gllm_retrieval.retriever import FulltextRetriever

# Assume data_store is an ElasticsearchDataStore with fulltext capability
# data_store = ElasticsearchDataStore(...).with_fulltext(index_name="my_index")
retriever = FulltextRetriever(data_store=data_store)

# Filter-only (no query text)
results = await retriever.retrieve(
    query_filter=F.eq("metadata.category", "AI"),
    top_k=10
)

# Single query with BM25 strategy and parameters
results = await retriever.retrieve(
    "search query",
    top_k=10,
    strategy=SupportedQueryMethods.BM25,
    k1=1.5,
    b=0.75
)

# Batch queries
batch_results = await retriever.retrieve(
    ["query 1", "query 2"],
    top_k=10,
    strategy="bm25"
)
```
