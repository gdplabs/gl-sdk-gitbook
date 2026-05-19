# Parent Document Retriever

## What's a Parent Document Retriever?

**Parent Document Retriever** retrieves parent chunks based on child chunk similarity search. It queries a child data store using vector similarity, then retrieves corresponding parent chunks using parent-child metadata links. This pattern enables fine-grained indexing with context-aware retrieval.

**Best For**:

* Fine-grained indexing with parent-child relationships
* Returning larger context (parent chunks) based on precise matches (child chunks)
* Reducing redundancy in retrieved context
* Splitting documents for better indexing while preserving context
* Hierarchical chunk structures

**Key Features**:

* Dual data store architecture (child + parent)
* Vector similarity on child chunks
* Fulltext retrieval of parent chunks by ID
* Configurable parent-child relationship fields
* Deduplication of parent results
* Flexible parent result capping

**Use Cases**:

* Document chunking with paragraph-level indexing, sentence-level retrieval
* Section-level storage with sentence-level search
* Hierarchical documents where you index fine-grained content but want broad context
* Combining small, searchable chunks with larger, more coherent parent documents

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Chunk](../../data-store/README.md) schema and metadata fields
2. [Data Store](../../data-store/README.md) with vector and fulltext capabilities
3. [EM Invoker](../../inference/em-invoker.md) for embeddings
4. Parent-child relationships encoded in chunk metadata

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

The Parent Document Retriever queries child chunks using vector similarity, extracts parent chunk identifiers from metadata, then retrieves those parent chunks from a separate data store. This gives you the precision of child-level search with the context of parent-level results.

## Basic Usage

Set up two data stores and create a retriever:

```python
from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import ParentDocumentRetriever

# Child store: fine-grained chunks with vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
child_store = ElasticsearchDataStore(
    index_name="child_chunks"
).with_vector(em_invoker=em_invoker)

# Parent store: larger context chunks with fulltext capability
parent_store = ElasticsearchDataStore(
    index_name="parent_chunks"
).with_fulltext()

# Create retriever with custom parent metadata field
retriever = ParentDocumentRetriever(
    child_data_store=child_store,
    parent_data_store=parent_store,
    parent_metadata_field="parent_chunk_id"  # Metadata field linking to parent
)

# Retrieve with similarity search on children, context from parents
results = await retriever.retrieve(
    "What is machine learning?",
    top_k=5
)
```

## Configuring Parent Result Limits

Control the number of parent chunks returned:

```python
retriever = ParentDocumentRetriever(
    child_data_store=child_store,
    parent_data_store=parent_store,
    parent_top_k=10  # Cap parent results to 10
)

# Note: top_k in retrieve() controls child chunks fetched, not parent results
results = await retriever.retrieve(
    "query",
    top_k=20  # Retrieves 20 child chunks, then maps to parents
)
```

## Filtering and Score Thresholds

Apply filters and thresholds:

```python
from gllm_datastore.core.filters import filter as F

retriever = ParentDocumentRetriever(
    child_data_store=child_store,
    parent_data_store=parent_store
)

# Filter on child chunks before parent retrieval
results = await retriever.retrieve(
    "query",
    query_filter=F.eq("metadata.category", "AI"),
    top_k=10,
    threshold=0.75
)
```

{% hint style="info" %}
**Implementation Notes**:
- The `top_k` parameter controls **child** chunks fetched, not final parent results
- Multiple child chunks can map to the same parent (parent deduplication preserves order)
- Use `parent_top_k` to cap final parent chunk count
- Chunks without valid parent metadata are included in results as-is
- The `parent_metadata_field` (default: `"parent_chunk"`) should be consistent with your chunking strategy
{% endhint %}
