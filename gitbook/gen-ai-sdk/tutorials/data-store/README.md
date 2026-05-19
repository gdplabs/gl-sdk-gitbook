---
icon: server
---

# Data Store

## What's a Data Store?

A **Data Store** is a flexible, capability-based abstraction for storing and querying text chunks. It acts as a lightweight shell where you plug in only the features you need—fulltext search, vector search, hybrid search (fulltext + vector in one call), or a combination.

Because all backends inherit from the same base class, the **public API stays consistent**. For example, switching from Chroma to Elasticsearch (or any other backend) means changing only the constructor; your code that interacts with `store.fulltext`, `store.vector`, or `store.hybrid` stays the same.

This design gives you a single entry point — one store, one set of handlers — regardless of how or where your data is persisted. See [supported-datastores.md](supported-datastores.md "mention") for a comprehensive list of backends and their capabilities.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-datastore"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-datastore
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
**This new Data Store interface is available in gllm\_datastore >=v0.5.32.**

For earlier versions, please refer to [Vector Data Store (Legacy)](https://gdplabs.gitbook.io/sdk/~/revisions/w6A7tUKJGDYFXuci5HcW/tutorials/data-store/legacy/vector-data-store)
{% endhint %}

## Quick start

```python
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_datastore.core.filters import filter as F
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
store = (
    ChromaDataStore(
        collection_name="customer-notes",
        client_type=ChromaClientType.MEMORY,
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

Now `store.fulltext` and `store.vector` are ready. Every capability exposes async CRUD helpers, so call them inside an async context:

```python
chunks = [
    Chunk(id="book:1", content="AI is useful for programming", metadata={"topic": "AI"}),
    Chunk(id="book:2", content="Cheesecake is delicious", metadata={"topic": "food"}),
    Chunk(id="book:3", content="Sushi is delicious", metadata={"topic": "food"}),
]
await store.fulltext.create(chunks)

# Query via metadata filter
results = await store.fulltext.retrieve(filters=F.eq("metadata.topic", "food"))

# Query via semantic similarity
results = await store.vector.retrieve(query="pickup orders")
```

## Capability menu

### Fulltext capability

1. Reads and writes plain text chunks plus metadata.
2. Supports exact filters through `QueryFilter` or the helper `filter` API.
3. Offers fuzzy search via `retrieve_fuzzy`.
4. Needed when you want to turn the data store into a cache (`store.as_cache(...)` requires fulltext).

### Vector capability

1. Stores embeddings and enables semantic search.
2. Needs an embedding model invoker (`BaseEMInvoker`) when you register it.
3. Lets you mix semantic and metadata filters.

### Hybrid capability

1. Combines fulltext (e.g. BM25) and vector search in a single query with configurable weights.
2. Configure via a list of `SearchConfig` (FULLTEXT and/or VECTOR); each VECTOR entry requires an embedding model invoker.
3. Use `store.hybrid.create()`, `store.hybrid.retrieve()`, and `store.hybrid.retrieve_by_vector()` for unified indexing and retrieval.

### Encryption capability

1. Provides transparent field-level encryption for chunk content and metadata.
2. Works seamlessly with fulltext and vector capabilities.
3. Encrypts data during write operations and decrypts during read operations.
4. See [encryption.md](encryption.md "mention") for detailed usage and configuration.

## Registering capabilities

Each backend inherits from `BaseDataStore`, so the registration keywords are always the same for datastore capabilities.

| Capability | Register with                    | Required arguments                                           | Common extras                      |
| ---------- | -------------------------------- | ------------------------------------------------------------ | ---------------------------------- |
| Fulltext   | `with_fulltext(**kwargs)`        | Depends on backend (for Chroma: `collection_name`, `client`) | `num_candidates` for fuzzy search  |
| Vector     | `with_vector(em_invoker=...)`    | `em_invoker` is mandatory                                    | `num_candidates`, backend specific |
| Hybrid     | `with_hybrid(config=...)`        | `config` (list of `SearchConfig`) is mandatory               | Backend-specific                   |
| Encryption | `with_encryption(encryptor=...)` | `encryptor` and `fields` are mandatory                       |                                    |

Registration returns the same store, so you can chain calls. Accessing an unregistered capability raises `NotRegisteredException`. Accessing a capability that the backend does not support raises `NotSupportedException`.

## Using the store end to end

#### 1. Prepare chunks

Use `gllm_core.schema.Chunk`. Each chunk must have `id`, `content`, and optional `metadata`.

```python
from gllm_core.schema import Chunk

chunk = Chunk(
    id="note-1",
    content="Order 938 is ready for pickup",
    metadata={"store": "jakarta", "status": "ready"},
)
```

#### 2. Write data

```python
await store.fulltext.create(chunk)
await store.vector.create(chunk)
```

Call both only when you registered both capabilities. Otherwise skip the missing one.

#### 3. Query data

```python
from gllm_datastore.core.filters import filter as F, QueryOptions

filters = F.and_(
    F.eq("metadata.store", "jakarta"),
    F.eq("metadata.status", "ready"),
)
options = QueryOptions(limit=20, order_by="metadata.updated_at", order_desc=True)

hits = await store.fulltext.retrieve(filters=filters, options=options)

semantic_hits = await store.vector.retrieve(
    query="orders ready for pickup",
    filters=filters,
    options=QueryOptions(limit=5),
)
```

#### 4. Using hybrid search

When the backend supports hybrid capability, register it with `with_hybrid(config=...)` and use `store.hybrid` for create and retrieve. Hybrid combines fulltext and vector scores in one call with configurable weights.

```python
from gllm_inference.em_invoker import OpenAIEMInvoker

from gllm_datastore.core.capabilities.hybrid_capability import HybridSearchType, SearchConfig
from gllm_datastore.core.filters import QueryOptions
from gllm_datastore.data_store import ElasticsearchDataStore

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
hybrid_config = [
    SearchConfig(search_type=HybridSearchType.FULLTEXT, field="text", weight=0.3),
    SearchConfig(search_type=HybridSearchType.VECTOR, field="embedding", weight=0.7, em_invoker=em_invoker),
]
store = ElasticsearchDataStore(index_name="my_index", url="http://localhost:9200").with_hybrid(config=hybrid_config)
await store.hybrid.create(chunks)
results = await store.hybrid.retrieve("machine learning", options=QueryOptions(limit=10))
```

## Advanced Features

- [batching.md](batching.md "mention"): Handle large datasets efficiently with automatic or manual batching.
- [query-filter.md](query-filter.md "mention"): Use the unified DSL for portable metadata filtering.

## Takeaways

- Register only the capabilities you plan to use.
- Interact with capabilities through the handler properties (`store.fulltext`, `store.vector`, `store.hybrid` when registered).
- Backends differ in setup but stay compatible at the capability level.

## API Reference

For more information about the data store, please take a look at our [API Reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_datastore/api/data_store.html).
