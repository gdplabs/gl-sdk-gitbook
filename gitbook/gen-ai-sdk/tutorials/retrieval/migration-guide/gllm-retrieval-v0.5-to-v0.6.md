# GLLM Retrieval v0.5 to v0.6

As you may have noticed, several legacy modules in GLLM Retrieval v0.5 have been marked as deprecated for a while. If your application is still using them, you should have received warning logs.

Backward compatibility will be **removed** in the upcoming minor version `v0.6.0`. Please review this migration guide to ensure a smooth transition.

{% hint style="info" %}
Note: If you've set the GLLM Retrieval dependency in your app as `>=0.5.0, <0.6.0`, you don't have to do this migration immediately, as you're locked to `v0.5.x`. You will only migrate to `0.6.0` when you choose to do so by updating your dependency to `^0.6.0`.

However, it's still recommended to do so ASAP to be able to access new features that will be added in the future.
{% endhint %}

## Legacy Vector Retriever Module

### Deprecated Classes Removed

The entire `gllm_retrieval.retriever.vector_retriever` module has been **removed**. The following deprecated classes are no longer available:

1. `BasicVectorRetriever` (deprecated in v0.5.20)
2. `BM25Retriever` (deprecated in v0.5.20)
3. `EnsembleRetriever` (deprecated in v0.6.0)
4. `PIIAwareRetriever` (deprecated in v0.6.0)
5. `BaseVectorRetriever` (base class)

All these classes have been replaced with new implementations that support the modern `BaseDataStore` API, batch queries, and improved filtering capabilities.

### 1. BasicVectorRetriever → VectorRetriever

**Before (v0.5):**

```python
from gllm_retrieval.retriever import BasicVectorRetriever
from gllm_datastore.vector_data_store import ElasticsearchVectorDataStore

# Initialize the data store
data_store = ElasticsearchVectorDataStore(
    index_name="my_index",
    url="http://localhost:9200"
)

# Create the retriever
retriever = BasicVectorRetriever(data_store=data_store)

# Retrieve documents
results = await retriever.retrieve(
    query="search query",
    top_k=10,
    retrieval_params={"filter": "category:tech"},
    threshold=0.8
)
```

**After (v0.6):**

```python
from gllm_retrieval.retriever import VectorRetriever
from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_datastore.core.filters import filter as F

# Initialize the data store with vector capability
data_store = ElasticsearchDataStore(
    index_name="my_index",
    url="http://localhost:9200"
).with_vector(em_invoker=embedding_model)

# Create the retriever
retriever = VectorRetriever(data_store=data_store)

# Retrieve documents
results = await retriever.retrieve(
    query="search query",
    top_k=10,
    query_filter=F.eq("metadata.category", "tech"),
    threshold=0.8
)
```

### 2. BM25Retriever → FulltextRetriever

**Before (v0.5):**

```python
from gllm_retrieval.retriever import BM25Retriever
from gllm_datastore.vector_data_store import ElasticsearchVectorDataStore

# Initialize the data store
data_store = ElasticsearchVectorDataStore(
    index_name="my_index",
    url="http://localhost:9200"
)

# Create the BM25 retriever
retriever = BM25Retriever(data_store=data_store)

# Retrieve documents
results = await retriever.retrieve(
    query="search query",
    top_k=10
)
```

**After (v0.6):**

```python
from gllm_retrieval.retriever import FulltextRetriever
from gllm_datastore.data_store import ElasticsearchDataStore

# Initialize the data store with fulltext capability
data_store = ElasticsearchDataStore(
    index_name="my_index",
    url="http://localhost:9200"
).with_fulltext()

# Create the fulltext retriever
retriever = FulltextRetriever(data_store=data_store)

# Retrieve documents
results = await retriever.retrieve(
    query="search query",
    top_k=10
)
```

### 3. EnsembleRetriever (legacy) → EnsembleRetriever (v2)

**Before (v0.5):**

```python
from gllm_retrieval.retriever.vector_retriever import EnsembleRetriever, BasicVectorRetriever
from gllm_datastore.vector_data_store import ElasticsearchVectorDataStore

# Create multiple retrievers
vector_retriever = BasicVectorRetriever(data_store=vector_data_store)
bm25_retriever = BM25Retriever(data_store=bm25_data_store)

# Create ensemble retriever
ensemble = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.7, 0.3]
)

# Retrieve documents
results = await ensemble.retrieve(query="search query", top_k=10)
```

**After (v0.6):**

```python
from gllm_retrieval.retriever import EnsembleRetriever, VectorRetriever, FulltextRetriever
from gllm_datastore.data_store import ElasticsearchDataStore

# Create data store with both capabilities
data_store = ElasticsearchDataStore(
    index_name="my_index",
    url="http://localhost:9200"
)

# Create multiple retrievers
vector_retriever = VectorRetriever(data_store=data_store.with_vector(em_invoker=embedding_model))
fulltext_retriever = FulltextRetriever(data_store=data_store.with_fulltext())

# Create ensemble retriever
ensemble = EnsembleRetriever(
    retrievers=[vector_retriever, fulltext_retriever],
    weights=[0.7, 0.3]
)

# Retrieve documents
results = await ensemble.retrieve(query="search query", top_k=10)
```

### 4. PIIAwareRetriever (legacy) → PIIAwareRetriever (v2)

**Before (v0.5):**

```python
from gllm_retrieval.retriever.vector_retriever import PIIAwareRetriever
from gllm_retrieval.retriever.pii_resolver import MetadataPIIResolver
from gllm_datastore.vector_data_store import ElasticsearchVectorDataStore

# Initialize components
data_store = ElasticsearchVectorDataStore(
    index_name="my_index",
    url="http://localhost:9200"
)
pii_resolver = MetadataPIIResolver()

# Create PII-aware retriever
retriever = PIIAwareRetriever(
    data_store=data_store,
    pii_resolver=pii_resolver,
    weights=[0.7, 0.3]
)

# Retrieve documents
results = await retriever.retrieve(
    query="Find documents about John Doe",
    top_k=10
)
```

**After (v0.6):**

```python
from gllm_retrieval.retriever import PIIAwareRetriever
from gllm_retrieval.retriever.pii_resolver import MetadataPIIResolver
from gllm_datastore.data_store import ElasticsearchDataStore

# Initialize components
data_store = ElasticsearchDataStore(
    index_name="my_index",
    url="http://localhost:9200"
).with_vector(em_invoker=embedding_model).with_fulltext()

pii_resolver = MetadataPIIResolver()

# Create PII-aware retriever
retriever = PIIAwareRetriever(
    data_store=data_store,
    pii_resolver=pii_resolver,
    weights=[0.7, 0.3]
)

# Retrieve documents
results = await retriever.retrieve(
    query="Find documents about John Doe",
    top_k=10
)
```

### Key Differences

1. **Data Store API**: The new `VectorRetriever` uses `BaseDataStore` with vector capability instead of the legacy `BaseVectorDataStore`.

2. **Filtering**: The `retrieval_params` parameter has been replaced with `query_filter`, which uses the new filter API from `gllm_datastore.core.filters`.

3. **Batch Queries**: The new `VectorRetriever` supports batch queries by passing a list of query strings:

```python
# Batch retrieval (v0.6 only)
batch_results = await retriever.retrieve(
    query=["query 1", "query 2", "query 3"],
    top_k=10
)
# Returns: list[list[Chunk]]
```

4. **Vector Capability Registration**: The data store must have vector capability registered using `.with_vector()` method.

### Migration Checklist

- [ ] Replace `BasicVectorRetriever` imports with `VectorRetriever`
- [ ] Replace `BM25Retriever` imports with `FulltextRetriever`
- [ ] Replace `EnsembleRetriever` from `gllm_retrieval.retriever.vector_retriever` with `EnsembleRetriever` from `gllm_retrieval.retriever`
- [ ] Replace `PIIAwareRetriever` from `gllm_retrieval.retriever.vector_retriever` with `PIIAwareRetriever` from `gllm_retrieval.retriever`
- [ ] Update data store initialization to use `BaseDataStore` with capability methods (`.with_vector()`, `.with_fulltext()`)
- [ ] Replace `retrieval_params` with `query_filter` using the new filter API from `gllm_datastore.core.filters`
- [ ] Update any custom implementations that extended `BaseVectorRetriever` or other legacy classes
- [ ] Remove any imports from `gllm_retrieval.retriever.vector_retriever` module
- [ ] Test your retrieval operations to ensure they work as expected

### Import Path Changes Summary

| Old Import Path (v0.5) | New Import Path (v0.6) |
|------------------------|------------------------|
| `from gllm_retrieval.retriever.vector_retriever import BasicVectorRetriever` | `from gllm_retrieval.retriever import VectorRetriever` |
| `from gllm_retrieval.retriever.vector_retriever import BM25Retriever` | `from gllm_retrieval.retriever import FulltextRetriever` |
| `from gllm_retrieval.retriever.vector_retriever import EnsembleRetriever` | `from gllm_retrieval.retriever import EnsembleRetriever` |
| `from gllm_retrieval.retriever.vector_retriever import PIIAwareRetriever` | `from gllm_retrieval.retriever import PIIAwareRetriever` |
| `from gllm_retrieval.retriever import BasicVectorRetriever` | `from gllm_retrieval.retriever import VectorRetriever` |
| `from gllm_retrieval.retriever import BM25Retriever` | `from gllm_retrieval.retriever import FulltextRetriever` |
