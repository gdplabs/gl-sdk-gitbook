---
icon: memory
---

# Cache

## What's a Cache?

Applications often re-run the same expensive operations—database lookups, embeddings generation, fuzzy searches, or API calls. **A cache avoids repeating this work by storing results and serving them instantly on the next request**. Using a cache improves performance, reduces backend load, and keeps response times predictable, especially under heavy traffic.

Cache rides on top of [Data Store](https://gdplabs.gitbook.io/sdk/~/revisions/sDuyGzlPeQbdwjekBfdo/tutorials/data-store/data-store). Once the store has the right capabilities, you get a decorator-based cache that is easy to use, stays readable and short.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../prerequisites.md "mention") page.

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
This page documents the current `BaseDataStore.as_cache()` interface.

If your project still uses the older vector-data-store cache workflow, refer to [Vector Data Store (Legacy)](https://gdplabs.gitbook.io/sdk/~/revisions/w6A7tUKJGDYFXuci5HcW/tutorials/data-store/legacy/vector-data-store).
{% endhint %}

## Quick Start

The cache can be used in two ways: **as a decorator** on your async functions, or through **direct method calls**. The decorator style is best when you want automatic memoization with zero boilerplate—your function stays clean, and the cache handles key generation, storage, and retrieval for you. Direct calls give you full control: you can store arbitrary payloads, manage metadata, or perform manual lookups without decorating a function.

### Simple cache

```python
from gllm_datastore.data_store import ChromaDataStore

store = ChromaDataStore(collection_name="customer-notes").with_fulltext()
cache = store.as_cache()

@cache.cache()
async def get_user(user_id: int) -> User:
    return await repo.fetch(user_id)
```

This basic caching flow keeps everything inside the data store. Call `store.as_cache()` (requires the fulltext capability), take the decorator, and wrap your async function. Every cache hit is stored as a chunk managed by the datastore. If you configure a persistent or remote datastore backend, those entries can survive process restarts. The next time `get_user()` is called with the same `user_id`, the decorator intercepts the call, checks the store, and returns the cached result instantly.

### Semantic cache

Here is the example of a semantic cache by utilizing the vector capability of the data store.

```python
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_datastore.cache import MatchingStrategy
from gllm_datastore.data_store import ChromaDataStore

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
store = (
    ChromaDataStore(collection_name="cache-store")
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)
cache = store.as_cache(matching_strategy=MatchingStrategy.SEMANTIC)

@cache.cache()
async def get_answer(question: str) -> str:
    return await slow_llm_call(question)
```

In this mode, the cache uses the vector capability under the hood for semantic lookup. The EM invoker converts the key (for example, the question text) into an embedding so the cache can find "close enough" keys rather than exact string matches. This is ideal when user queries vary in wording but should map to the same answer—perfect for LLM-powered Q\&A or retrieval-augmented interfaces.

### Direct method call

If you prefer explicit control, you can call the cache methods directly:

```python
import json

cache = store.as_cache(matching_strategy=MatchingStrategy.SEMANTIC)

await cache.store("orders:938", json.dumps(payload), metadata={"channel": "retail"})
result = await cache.retrieve("orders:938")
await cache.delete("orders:938")
await cache.clear()
```

Direct methods behave exactly like the decorator but without wrapping a function:

1. **`store()`** and **`retrieve()`** are async and map directly to the underlying data store handlers. `retrieve()` attempts to deserialize JSON payloads automatically.
2. **`delete()`** accepts a single key or a list of keys and uses metadata filters internally.
3. **`clear()`** removes all cache entries from the collection—very useful during integration tests or environment resets.

{% hint style="success" %}
Use the decorator for convenience; use direct calls when you need flexibility.
{% endhint %}

## Cache Eviction

Some datastores do not ship with TTL or size-based eviction. The SDK adds a pluggable abstraction so you can run consistent policies regardless of backend limits. An eviction manager runs the policy loop, and each policy is implemented as an eviction strategy. When you pass a manager to `as_cache`, the cache asks the strategy to enrich metadata before persisting the chunk.

Use an eviction manager when:

1. Your backend lacks built-in TTL or you want the same policy across multiple backends.
2. You need metadata-driven eviction (for example, "delete anything past 500 hits").
3. You plan to combine eviction with exact, fuzzy, or semantic matching and want uniform behavior.

The cache currently ships with three built-in eviction strategies:

1. **TTL** - expire entries after a fixed duration.
2. **LRU** - evict the least recently used entries when the cache exceeds a maximum size.
3. **LFU** - evict the least frequently used entries when the cache exceeds a maximum size.

### TTL eviction

```python
from gllm_datastore.cache.vector_cache.eviction_strategy.ttl_eviction_strategy import TTLEvictionStrategy
from gllm_datastore.cache.vector_cache.eviction_manager.asyncio_eviction_manager import AsyncIOEvictionManager

ttl_strategy = TTLEvictionStrategy(ttl="10m")
eviction_manager = AsyncIOEvictionManager(
    vector_store=store,
    eviction_strategy=ttl_strategy,
    check_interval=60,
)
cache = store.as_cache(eviction_manager=eviction_manager)
eviction_manager.start()

@cache.cache(eviction_config={"ttl": "10m"})
async def get_fresh_user(user_id: int) -> User:
    return await repo.fetch(user_id)
```

`TTLEvictionStrategy` sets expiration metadata on each cache entry, and `AsyncIOEvictionManager` periodically deletes expired entries from the backing store.

### LRU eviction

Use LRU when you want to keep the cache bounded by size and prefer to retain the entries that were accessed most recently.

```python
from gllm_datastore.cache.vector_cache.eviction_strategy.lru_eviction_strategy import LRUEvictionStrategy
from gllm_datastore.cache.vector_cache.eviction_manager.asyncio_eviction_manager import AsyncIOEvictionManager

lru_strategy = LRUEvictionStrategy(max_entries=1000)
eviction_manager = AsyncIOEvictionManager(
    vector_store=store,
    eviction_strategy=lru_strategy,
    check_interval=60,
)
cache = store.as_cache(eviction_manager=eviction_manager)
eviction_manager.start()
```

LRU relies on the cache metadata field `last_used_at`, which is initialized on write and updated automatically on cache hits. When the cache grows beyond `max_entries`, the oldest entries by recent usage are evicted first.

### LFU eviction

Use LFU when you want to preserve the entries that are reused most often, even if they were not accessed very recently.

```python
from gllm_datastore.cache.vector_cache.eviction_strategy.lfu_eviction_strategy import LFUEvictionStrategy
from gllm_datastore.cache.vector_cache.eviction_manager.asyncio_eviction_manager import AsyncIOEvictionManager

lfu_strategy = LFUEvictionStrategy(max_entries=1000)
eviction_manager = AsyncIOEvictionManager(
    vector_store=store,
    eviction_strategy=lfu_strategy,
    check_interval=60,
)
cache = store.as_cache(eviction_manager=eviction_manager)
eviction_manager.start()
```

LFU relies on the cache metadata field `access_count`, which starts at `0` and is incremented automatically on cache hits. When multiple entries have the same access count, the strategy uses `last_used_at` as the next tie-breaker to keep eviction deterministic.

If you need a different policy beyond TTL, LRU, or LFU, you can implement a custom `BaseEvictionStrategy` and pair it with an eviction manager.

When using `AsyncIOEvictionManager`, start it during application startup and stop it during shutdown so the background eviction task is managed cleanly.

## Takeaways

1. The cache is a thin helper over the data store: all durability, filters, and eviction metadata live in the store.
2. Start with the simple cache, then add an eviction manager when you need TTL or size policies that a backend cannot offer on its own.
3. Built-in eviction strategies available today are TTL, LRU, and LFU.
4. Use the same filters and tooling described in the data store guide to inspect or clean cache entries.

## Eviction Components

### Eviction Strategy

| Name                  | Status    | Notes                                            |
| --------------------- | --------- | ------------------------------------------------ |
| `TTLEvictionStrategy` | Available | Built-in strategy for TTL-based expiration.      |
| `LRUEvictionStrategy` | Available | Evicts the least recently used entries first.    |
| `LFUEvictionStrategy` | Available | Evicts the least frequently used entries first.  |

### Eviction Manager

| Name                     | Status    | Notes                                                        |
| ------------------------ | --------- | ------------------------------------------------------------ |
| `AsyncIOEvictionManager` | Available | Runs background eviction checks in an asyncio task.          |
| `CeleryEvictionManager`  | Backlog   | Planned manager for running eviction through Celery workers. |

## API Reference

For more detailed information about the cache and its correlation with the data store, please refer to the [API Reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_datastore/api/cache.html).
