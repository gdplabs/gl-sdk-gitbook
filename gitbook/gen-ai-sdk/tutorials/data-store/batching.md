---
icon: layer-plus
---

# Batching

## Overview

When dealing with large datasets—such as ingesting thousands of documents—sending everything in a single request can lead to timeouts, rate limits, or memory issues.

The GLLM DataStore library handles this automatically via the **Automated Batching** feature. This ensures that large operations are split into manageable chunks without any extra logic from your side.

## Automated Batching

You can configure batching once during capability registration when the backend supports a `default_batch_size` option. This keeps your CRUD operations clean and readable.

### Configuration During Capability Registration

Specify `default_batch_size` when enabling the capability. All subsequent operations on that capability will respect this limit unless you override it per call.

```python
from gllm_datastore.data_store import MilvusDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    MilvusDataStore(
        collection_name="my_collection",
        uri="http://localhost:19530",
    )
    .with_vector(
        em_invoker=em_invoker,
        default_batch_size=100,
    )
)

await store.vector.create(huge_list_of_chunks)
```

## Environment-specific Examples

Different environments require different batching strategies. Use tabs below to see how to configure for your setup.

{% tabs %}
{% tab title="Local Development" %}
When running locally, you can often afford larger batches for speed since there is less network overhead.

```python
from gllm_datastore.data_store.milvus.data_store import MilvusDataStore

store = (
    MilvusDataStore(
        collection_name="local_dev_store",
        uri="http://localhost:19530",
    )
    .with_fulltext(default_batch_size=500)
)

await store.fulltext.create(huge_list_of_chunks)
```
{% endtab %}

{% tab title="Production Cloud" %}
When using cloud-hosted databases, use smaller batches to avoid payload-size errors and network instability.

```python
from gllm_datastore.data_store import MilvusDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

store = (
    MilvusDataStore(
        collection_name="prod_collection",
        uri="https://my-prod-cluster.cloud",
    )
    .with_vector(
        em_invoker=em_invoker,
        default_batch_size=100,
    )
)

await store.vector.create(huge_list_of_chunks)
```
{% endtab %}
{% endtabs %}

## Per-Call Batching Override

If you need to adjust the batch size for a specific operation (e.g., a one-time migration with a different limit), you can pass the `batch_size` parameter directly to any CRUD method.

```python
from gllm_datastore.core.filters import filter as F

await store.vector.create(chunks, batch_size=50)

await store.fulltext.update(
    filters=F.in_("id", ids),
    update_values=...,
    batch_size=200
)
```

## Best Practices

Choosing the right batch size depends on your environment and the provider's limits.

| Environment             | Recommended Batch Size | Why?                                                                                       |
| ----------------------- | ---------------------- | ------------------------------------------------------------------------------------------ |
| **Local Dev**           | 100 - 500 items        | Faster processing on local machines or local Docker instances.                             |
| **Production Cloud**    | 50 - 100 items         | Avoids common payload size limits and network timeouts in cloud environments.              |
| **High Density Chunks** | 10 - 50 items          | Use smaller batches if your text chunks are very large (e.g., several pages of text each). |

{% hint style="info" %}
**Note**: Exact batching support and defaults vary by backend and capability. If a backend does not expose `default_batch_size`, use the per-call `batch_size` override instead.
{% endhint %}
