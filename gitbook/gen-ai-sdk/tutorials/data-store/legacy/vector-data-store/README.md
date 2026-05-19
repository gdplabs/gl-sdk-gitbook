---
icon: font-case
---

# Vector Data Store

## What's a Vector Data Store?

Vector datastores are specialized for storing and searching high-dimensional vector embeddings. They are essential for:

* **Semantic search** and similarity matching
* **Recommendation systems** based on content similarity
* **Document retrieval** and information retrieval
* **AI/ML applications** requiring embedding storage

**Available Implementations:** [supported-vector-data-store.md](../../../../resources/supported-vector-data-store.md "mention")

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../../../prerequisites.md "mention") page.

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
**Vector Data Store will be deprecated in gllm\_datastore-v0.6.0. A new Data Store is available in gllm\_datastore >=v0.5.32.** please refer to [Data Store page](https://gdplabs.gitbook.io/sdk/~/revisions/beykCxz0UanaEX0sPJJu/tutorials/data-store/data-store).
{% endhint %}

## Save and Retrieve Data

Let's walk through practical example for vector datastore type. This example will show you how to get started quickly and demonstrate common patterns you'll use in your own projects.

```python
from gllm_core.schema import Chunk
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

# Initialize vector store with embedding model
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
vector_store = ChromaVectorDataStore(
    collection_name="documents",
    embedding=em_invoker
)

# Add chunks to the store
chunks = [
    Chunk(content="AI is the future."),
    Chunk(content="Parrot is a bird."),
]
await vector_store.add_chunks(chunks)

# Query by semantic similarity
results = await vector_store.query(query="artificial intelligence")
```

## Metadata Filtering

Instead of relying solely on a string for semantic queries, we can also apply metadata filtering through the `retrieval_params` parameter in the `query()` method. For example, in `ChromaVectorDataStore`, the retrieval parameter can be used as follows:

```python
# Add chunks to the store
chunks = [
    Chunk(content="AI is the future.", metadata={"type": "document"}),
    Chunk(content="Parrot is a bird.", metadata={"type": "document"}),
]
await vector_store.add_chunks(chunks)

retrieval_params = {
    "filter": {
        "$and": [
            {"type": "document"},
        ]
    },
    "where_document": {"$contains": {"text": "AI"}},
}

results = await vector_store.query(query="artificial intelligence")
```

## Use as a Cache

One of the important features of the GL SDK is the ability to use vector datastores as a **cache**. This is perfect for applications that need to cache expensive operations like API calls, database queries, or AI model inferences. The `.as_cache()` method transforms any vector datastore into a sophisticated caching system with three different matching strategies.

### Quick Start with `.as_cache()`

The `.as_cache()` method is your gateway to intelligent caching. It converts a vector datastore into a cache with configurable matching strategies:

```python
from gllm_datastore.vector_data_store import ChromaVectorDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

# Initialize your vector store
vector_store = ChromaVectorDataStore(
    collection_name="my_cache",
    embedding=OpenAIEMInvoker(model_name="text-embedding-3-small")
)

# Convert to cache with exact matching (default)
cache = vector_store.as_cache()
```

### Three Types of Cache Matching

The GL SDK provides three sophisticated matching strategies, each perfect for different use cases:

#### **1) Exact Matching (`"exact"`)**

Perfect for when you need precise key matching. This is the fastest and most reliable option for caching operations where the input must match exactly.

```python
# Use exact matching for API responses
cache = vector_store.as_cache(matching_strategy="exact")

# Store a response
await cache.store("user_query_123", "API response data")

# Retrieve with exact match
result = await cache.retrieve("user_query_123", "exact")
# Returns the exact response if key matches perfectly
```

**Best for**: API responses, database query results, function outputs where exact input matching is required.

#### **2) Fuzzy Matching (`"fuzzy"`)**

Ideal for handling typos, slight variations, or minor differences in input. Uses Levenshtein distance to find close matches.

```python
# Use fuzzy matching for user inputs
cache = vector_store.as_cache(
    matching_strategy="fuzzy",
    matching_config={"max_distance": 2}  # Allow 2 character differences
)

# Store responses
await cache.store("What is artificial intelligence?", "AI explanation...")
await cache.store("How does machine learning work?", "ML explanation...")

# Retrieve with fuzzy matching
result = await cache.retrieve("What is artifical intelligence?", "fuzzy")
# Returns the response even with the typo "artifical" instead of "artificial"
```

**Best for**: User queries, search terms, natural language inputs where minor variations are common.

#### **3) Semantic Matching (`"semantic"`)**

The most intelligent option! Uses vector embeddings to find semantically similar content, even when the exact words don't match.

```python
# Use semantic matching for intelligent caching
cache = vector_store.as_cache(
    matching_strategy="semantic",
    matching_config={"min_similarity": 0.8}  # 80% similarity threshold
)

# Store responses
await cache.store("What is the weather like today?", "Weather forecast data...")
await cache.store("How hot is it outside?", "Temperature information...")

# Retrieve with semantic matching
result = await cache.retrieve("Is it sunny today?", "semantic")
# Returns weather-related response even though the words are different
```
