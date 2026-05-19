# Hybrid Retriever

## What's a Hybrid Retriever?

**Hybrid Retriever** combines vector (semantic) search and fulltext (keyword) search in a single retrieval operation using native data store hybrid capability. This provides both semantic and lexical matches with a single query, leveraging the data store backend to efficiently combine multiple search paradigms.

**Best For**:

* Combining semantic and keyword signals in one operation
* Balanced hybrid search without multiple retrievers
* Backends with native hybrid support (Elasticsearch, etc.)
* Reduced latency over ensemble approaches
* Weighted fusion at the data store level

**Key Features**:

* Native data store hybrid capability
* Configurable weights for vector vs. fulltext
* Support for field-level search configuration
* Metadata filtering and score thresholds
* Single-query or batch-query retrieval
* Efficient backend-level result merging

**Use Cases**:

* Hybrid search combining semantic relevance and keyword precision
* Document retrieval requiring both conceptual and exact matching
* Balanced result ranking from multiple search types
* Improved recall with diverse signal coverage

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Data Store](../../data-store/README.md) and hybrid capability setup
2. [EM Invoker](../../inference/em-invoker.md) for embeddings in hybrid configuration
3. Hybrid search configuration for your chosen data store backend

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

The Hybrid Retriever executes both vector and fulltext search through the data store's native hybrid capability, combining results at the backend level for efficient hybrid retrieval.

## Basic Usage

Set up a data store with hybrid capability and create the retriever:

```python
from gllm_datastore.core.capabilities.hybrid_capability import HybridSearchType, SearchConfig
from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import HybridRetriever

# Create EM invoker for embeddings
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

# Configure hybrid search with vector and fulltext
hybrid_config = [
    SearchConfig(search_type=HybridSearchType.FULLTEXT, field="text", weight=0.3),
    SearchConfig(search_type=HybridSearchType.VECTOR, field="embedding", weight=0.7, em_invoker=em_invoker),
]

# Data store with hybrid capability
data_store = ElasticsearchDataStore(
    index_name="documents",
    url="http://localhost:9200"
).with_hybrid(config=hybrid_config)

# Create retriever
retriever = HybridRetriever(data_store=data_store)

# Retrieve with hybrid search
results = await retriever.retrieve("What is machine learning?", top_k=10)
```

## Filtering and Score Thresholds

Apply metadata filters and result filtering:

```python
from gllm_datastore.core.filters import filter as F

retriever = HybridRetriever(data_store=data_store)

# Single query with filters
results = await retriever.retrieve(
    "search query",
    query_filter=F.eq("metadata.category", "AI"),
    top_k=10,
    threshold=0.8
)

# Batch queries
batch_results = await retriever.retrieve(
    ["query 1", "query 2"],
    top_k=10
)
```

{% hint style="info" %}
**Implementation Notes**:
- Hybrid configuration weights determine the balance between fulltext and vector signals
- The data store backend performs the actual fusion (no separate ranking step needed)
- Field configuration is set at data store initialization, not retriever level
- Score threshold filtering is applied after hybrid fusion
- Batch queries execute multiple hybrid searches efficiently
{% endhint %}

## Alternative: Ensemble Retriever

For data stores without native hybrid capability, use [Ensemble Retriever](./ensemble-retriever.md) to combine separate vector and fulltext retrievers with Reciprocal Rank Fusion.
