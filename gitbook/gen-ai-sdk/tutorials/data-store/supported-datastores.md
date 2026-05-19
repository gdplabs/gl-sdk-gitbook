---
icon: database
---

# Supported Datastores

## Overview

The GLLM DataStore library implements the **Single Interface, Multiple Implementations pattern**, meaning you interact with a unified API regardless of the underlying storage engine. Whether you use Chroma for prototyping or Elasticsearch for production, the code to store and retrieve data remains generic:

```python
# The only difference is the initialization
store = ChromaDataStore(...)
# OR
store = ElasticsearchDataStore(...)

# The rest of your code stays the same
await store.vector.retrieve(query="...")
```

## Capability Matrix

| Datastore         | Fulltext | Vector | Hybrid | Best For                                             | Notes                                          |
| :---------------- | :------- | :----- | :----- | :--------------------------------------------------- | :--------------------------------------------- |
| **Chroma**        | ✅       | ✅     | ❌     | Local dev & prototyping                              | Not recommended for production.                |
| **Elasticsearch** | ✅       | ✅     | ✅     | Production-grade hybrid search (semantic + keyword)  | Strongest hybrid + enterprise ops.             |
| **OpenSearch**    | ✅       | ✅     | ✅     | Drop-in open-source alternative to Elasticsearch     | Feature-compatible with ES.                    |
| **Milvus**        | ✅       | ✅     | ✅     | Massive vector scale (100M+ vectors)                 | High-performance vector database.              |
| **PostgreSQL**    | ✅       | ✅     | ❌     | Teams already on Postgres with modest vector scale   | Uses `pgvector`; no hybrid out of the box.     |
| **Redis**         | ✅       | ✅     | ❌     | Ultra-low latency fulltext + vector (no hybrid)      | In-memory speed with persistence.              |
| **SQL**           | ✅       | ❌     | ❌     | Structured / relational data, no AI search needed    | Generic SQL (Postgres, MySQL, SQLite).         |
| **In-Memory**     | ✅       | ✅     | ❌     | Testing and ephemeral / CI workloads                 | Data is lost on restart.                       |

## Initialization Examples

{% tabs %}
{% tab title="Chroma" %}

```python
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

# 1. Initialize Invoker (for vector search)
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

# 2. Initialize Store
store = (
    ChromaDataStore(
        collection_name="my_collection",
        client_type=ChromaClientType.PERSISTENT,
        persist_directory="./chroma-data",
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

{% endtab %}

{% tab title="Elasticsearch" %}

```python
from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    ElasticsearchDataStore(
        index_name="my_index",
        url="http://localhost:9200",
        # api_key="..." or username="user", password="pass"
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

{% endtab %}

{% tab title="OpenSearch" %}

```python
from gllm_datastore.data_store import OpenSearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    OpenSearchDataStore(
        index_name="my_index",
        url="http://localhost:9200",
        # username="user", password="pass"
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

{% endtab %}

{% tab title="Milvus" %}

```python
from gllm_datastore.data_store import MilvusDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    MilvusDataStore(
        collection_name="my_collection",
        uri="http://localhost:19530",
        # token="root:Milvus", # Optional
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker, dimension=1536)
)
```

{% endtab %}

{% tab title="PostgreSQL" %}

```python
from gllm_datastore.data_store.postgresql.data_store import PostgreSQLDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    PostgreSQLDataStore(
        engine_or_url="postgresql+asyncpg://user:password@localhost/dbname",
        table_name="chunks_table",
        embedding_dimension=1536
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

{% endtab %}

{% tab title="Redis" %}

```python
from gllm_datastore.data_store import RedisDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    RedisDataStore(
        index_name="my_index",
        url="redis://localhost:6379",
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

{% endtab %}

{% tab title="SQL" %}

```python
from gllm_datastore.data_store.sql.data_store import SQLDataStore

# Supports SQLite, MySQL, PostgreSQL (without vector)
store = (
    SQLDataStore(
        engine_or_url="sqlite+aiosqlite:///./my_database.db",
        table_name="my_text_chunks"
    )
    .with_fulltext()
)
```

{% endtab %}

{% tab title="In-Memory" %}

```python
from gllm_datastore.data_store import InMemoryDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    InMemoryDataStore()
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
```

{% endtab %}
{% endtabs %}

## Recommendation

Not sure which datastore to pick? The **Best For** column in the Capability Matrix above gives a quick answer. For more detailed guidance, see the scenarios below. Recommendations are based on an internal survey evaluating eight vector databases against RAG-critical capabilities (hybrid search, ANN tuning, metadata filtering, scalability, and enterprise operations).

### By Scenario

{% hint style="success" %}
**General-Purpose RAG — Start Here**

Use **Elasticsearch** (or **OpenSearch** as a drop-in open-source alternative).

- ✅ Best hybrid search: BM25 + dense vector + sparse in a single query
- ✅ Rich metadata filtering with typed fields and boolean expressions
- ✅ Multi-vector support via multiple embedding fields per document
- ✅ Large-k retrieval + rescoring for downstream cross-encoder pipelines
- ✅ Enterprise-grade ops: RBAC, audit logs, TLS, index lifecycle management

**When to upgrade:** If your index grows beyond ~100M vectors and ANN latency becomes a bottleneck, consider integrating Milvus alongside Elasticsearch (see below).
{% endhint %}

{% hint style="info" %}
**High-Scale Vector Retrieval (100M+ vectors)**

Use **Milvus** alongside Elasticsearch.

Milvus provides the most advanced ANN engine available in open source:

- ✅ Purpose-built vector-native architecture
- ✅ Broadest index selection: HNSW, IVF\_PQ, IVF\_SQ8, OPQ, DiskANN, GPU indexes
- ✅ Best large-k throughput (k = 100–1000+) with predictable latency at scale
- ✅ Clean named-vector / multi-vector schema support

**Recommended pattern:**

```
User Query
    ├─► Elasticsearch / OpenSearch  ── Hybrid keyword + metadata filtering
    └─► Milvus                      ── Dense ANN retrieval at scale
                                        + multi-vector ranked fusion
    └─► Re-ranker (cross-encoder / LLM)
```

> **Note on complexity:** Milvus Distributed requires dedicated infrastructure (query nodes, data nodes, etcd, MinIO/S3). Start with **Milvus Standalone** (single-node Docker) before committing to distributed mode.
{% endhint %}

{% hint style="warning" %}
**Already on Postgres?**

Use **PostgreSQL** (pgvector) — but be aware of its limits:

- ✅ No new infrastructure; full SQL expressiveness and ACID guarantees
- ✅ HNSW and IVFFlat index support (pgvector 0.5.0+)
- ❌ No quantization (PQ/SQ8); higher memory cost at scale
- ❌ Hybrid search requires manual SQL composition
- ❌ No native horizontal sharding — not recommended beyond ~5–10M vectors without significant tuning
{% endhint %}
