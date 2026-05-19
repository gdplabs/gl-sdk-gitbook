---
icon: list-check
---

# Basic CRUD and Methods

## Overview

Data stores expose their operations through capability handlers. After registering a capability, call methods from the matching handler:

* `store.fulltext` for text chunk CRUD, metadata filtering, and fuzzy retrieval.
* `store.vector` for embedding storage and semantic retrieval.
* `store.hybrid` for backends that support fulltext and vector retrieval in one request.

This keeps application code consistent across backends. In most cases, switching from one datastore to another only changes how the store is initialized and which capabilities are registered.

## Common Setup

```python
from gllm_core.schema import Chunk
from gllm_datastore.core.filters import QueryOptions, filter as F

chunk = Chunk(
    id="note-1",
    content="Order 938 is ready for pickup",
    metadata={"store": "jakarta", "status": "ready"},
)
```

## Fulltext Methods

Register fulltext support with `with_fulltext()` and use `store.fulltext` for basic CRUD operations.

```python
store = store.with_fulltext()
```

| Method | Purpose |
| :--- | :--- |
| `create(chunks)` | Insert one chunk or a list of chunks. |
| `retrieve(filters=None, options=None)` | Read chunks using optional filters and query options. |
| `update(update_values, filters=None)` | Update chunks matching the filters. |
| `delete(filters=None, options=None)` | Delete chunks matching the filters. |
| `retrieve_fuzzy(query, ...)` | Retrieve approximate text matches when supported by the backend. |

```python
await store.fulltext.create(chunk)

results = await store.fulltext.retrieve(
    filters=F.eq("metadata.status", "ready"),
    options=QueryOptions(limit=10),
)

await store.fulltext.update(
    update_values={"metadata": {"store": "jakarta", "status": "picked_up"}},
    filters=F.eq("id", "note-1"),
)

await store.fulltext.delete(filters=F.eq("id", "note-1"))
```

## Vector Methods

Register vector support with `with_vector()` and provide an embedding model invoker.

```python
store = store.with_vector(em_invoker=em_invoker)
```

| Method | Purpose |
| :--- | :--- |
| `create(chunks)` | Store chunks and their embeddings. |
| `retrieve(query, filters=None, options=None)` | Retrieve semantically similar chunks from a text query. |
| `retrieve_by_vector(vector, filters=None, options=None)` | Retrieve semantically similar chunks from a precomputed vector when supported. |
| `update(update_values, filters=None)` | Update vector-backed chunk records when supported. |
| `delete(filters=None, options=None)` | Delete vector-backed chunk records. |

```python
await store.vector.create(chunk)

semantic_hits = await store.vector.retrieve(
    query="orders ready for pickup",
    filters=F.eq("metadata.store", "jakarta"),
    options=QueryOptions(limit=5),
)
```

## Hybrid Methods

Register hybrid support with `with_hybrid(config=...)` when a backend supports combined fulltext and vector retrieval.

| Method | Purpose |
| :--- | :--- |
| `create(chunks)` | Store chunks for hybrid retrieval. |
| `retrieve(query, filters=None, options=None)` | Retrieve using a combined fulltext and vector query. |
| `retrieve_by_vector(vector, filters=None, options=None)` | Retrieve using vector input as part of hybrid retrieval when supported. |
| `delete(filters=None, options=None)` | Delete hybrid-backed records. |

```python
await store.hybrid.create(chunk)

hits = await store.hybrid.retrieve(
    query="pickup orders",
    filters=F.eq("metadata.status", "ready"),
    options=QueryOptions(limit=10),
)
```

## Query Filters and Options

Use `filter` helpers for portable metadata filtering across datastore backends.

```python
filters = F.and_(
    F.eq("metadata.store", "jakarta"),
    F.eq("metadata.status", "ready"),
)

options = QueryOptions(limit=20, order_by="metadata.updated_at", order_desc=True)

results = await store.fulltext.retrieve(filters=filters, options=options)
```

See [query-filter.md](query-filter.md "mention") for the full filter syntax.

## Backend-specific Methods

Some datastores expose extra methods for backend-native operations. These methods are useful when you need database-specific functionality, but they are not portable across every datastore.

### SQL `query()`

Unlike most data stores, SQL-backed datastores support read-only native SQL through `query()`. Use this method when you need SQL-specific features that do not fit the portable capability methods, such as projections, joins, aggregates, CTEs, subqueries, or window functions.

```python
df = await store.query(
    "SELECT id, content FROM chunks WHERE id = :chunk_id",
    params={"chunk_id": "chunk-1"},
)
```

`query()` returns a `pandas.DataFrame` and accepts SQLAlchemy-style `:name` bind parameters.

```python
async def query(
    query: str,
    params: dict[str, Any] | None = None,
    max_rows: int | None = 10_000,
) -> pandas.DataFrame
```

{% hint style="warning" %}
`query()` is read-only. It accepts `SELECT`, `WITH`, and `EXPLAIN` statements, and rejects mutating statements such as `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, and `DROP`. Always pass user values through `params` instead of interpolating them into the SQL string.
{% endhint %}
