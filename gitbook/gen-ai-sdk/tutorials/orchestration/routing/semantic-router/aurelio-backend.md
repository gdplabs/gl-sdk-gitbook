---
icon: layers
---

# Aurelio Backend Guide

The **Aurelio Backend** provides advanced semantic routing capabilities through Aurelio Labs' semantic router library. This guide covers the encoder and index components that power the Aurelio backend.

## Overview

The Aurelio backend consists of three main components:

1. **Encoders** - Convert text/images into embeddings for semantic similarity
2. **Index** - Store and retrieve routes efficiently
3. **Adapter** - Orchestrates encoders and indexes for routing

## Installation

```bash
pip install gllm-pipeline gllm-inference semantic-router
```

<details>

<summary>Prerequisites</summary>

This tutorial requires familiarity with these concepts:

1. [EM Invoker](../../../inference/em-invoker.md "mention") - For understanding embedding model invocation
2. [Semantic Router](../README.md "mention") - For understanding the router interface and basic usage

</details>

## Encoders

Encoders convert input text or images into embeddings for semantic similarity matching. The Aurelio backend supports multiple encoder types.

### EM Invoker Encoder

Use any GLLM embedding model as an encoder. In v0.5+, you can pass a `BaseEMInvoker` directly — it is automatically wrapped:

```python
import asyncio
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter

# Create an embedding model
em_invoker = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials="<YOUR_OPENAI_API_KEY>"
)

# Pass em_invoker directly (auto-wrapped in v0.5+)
router = SemanticRouter.aurelio(
    encoder=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

You can also wrap it manually using `EMInvokerEncoder` for advanced configuration:

```python
from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder

encoder = EMInvokerEncoder(em_invoker, name="my-encoder")
router = SemanticRouter.aurelio(
    encoder=encoder,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

**Advantages:**
- Use any GLLM-supported embedding model
- Consistent with your application's embedding infrastructure
- Supports all EM invoker features (caching, retries, etc.)

### Langchain Encoder

Use Langchain embedding models:

```python
from langchain.embeddings import OpenAIEmbeddings
from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.backend.aurelio.encoders import LangchainEncoder

# Create a Langchain embedding model
langchain_embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key="<YOUR_OPENAI_API_KEY>"
)

# Wrap it as an Aurelio encoder
encoder = LangchainEncoder(langchain_embeddings)

# Use with Aurelio backend
router = SemanticRouter.aurelio(
    encoder=encoder,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

**Advantages:**
- Leverage existing Langchain integrations
- Access to Langchain's embedding ecosystem
- Compatible with Langchain-based applications

### TEI Encoder

Use Text Embeddings Inference (TEI) for local or remote embeddings:

```python
from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.backend.aurelio.encoders import TEIEncoder

# Create a TEI encoder
encoder = TEIEncoder(
    name="tei-encoder",
    base_url="http://localhost:8080",  # Local TEI instance
)

# Use with Aurelio backend
router = SemanticRouter.aurelio(
    encoder=encoder,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

**Advantages:**
- Local embedding inference (privacy-preserving)
- No API costs
- Full control over the embedding model
- Supports various model architectures

## Index Options

Indexes store and retrieve routes efficiently. Choose based on your use case and scale.

### Local Index

In-memory index suitable for development and small deployments:

```python
from semantic_router.index import LocalIndex
from gllm_pipeline.router import SemanticRouter

# Create a local index
index = LocalIndex()

# Use with Aurelio backend
router = SemanticRouter.aurelio(
    encoder=encoder,
    index=index,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

**Characteristics:**
- In-memory storage
- Fast for small datasets
- No persistence
- Single-process only

### Aurelio Index

Base Aurelio index for custom implementations:

```python
from gllm_pipeline.router.backend.aurelio.index import BaseAurelioIndex
from gllm_pipeline.router import SemanticRouter

# Use a custom Aurelio index
index = BaseAurelioIndex()

router = SemanticRouter.aurelio(
    encoder=encoder,
    index=index,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

### Azure AI Search Index

Use Azure AI Search for scalable, cloud-hosted indexing:

```python
from gllm_pipeline.router.backend.aurelio.index import AzureAISearchAurelioIndex
from gllm_pipeline.router import SemanticRouter

# Create Azure AI Search index
index = AzureAISearchAurelioIndex(
    endpoint="https://<your-service>.search.windows.net",
    index_name="routes",
    api_key="<YOUR_AZURE_API_KEY>",
)

# Use with Aurelio backend
router = SemanticRouter.aurelio(
    encoder=encoder,
    index=index,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

**Advantages:**
- Scalable cloud storage
- Full-text and vector search
- High availability
- Enterprise-grade security

### Datastore Adapter Index

Use GLLM datastores (Pinecone, Weaviate, etc.) as indexes:

```python
from gllm_pipeline.router.backend.aurelio.index import DataStoreAdapterIndex
from gllm_retrieval.datastore import build_datastore
from gllm_pipeline.router import SemanticRouter

# Create a GLLM datastore
datastore = build_datastore(
    datastore_type="pinecone",
    config={
        "api_key": "<YOUR_PINECONE_API_KEY>",
        "index_name": "routes",
    }
)

# Create datastore adapter index
index = DataStoreAdapterIndex(datastore=datastore)

# Use with Aurelio backend
router = SemanticRouter.aurelio(
    encoder=encoder,
    index=index,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
)
```

**Advantages:**
- Leverage existing GLLM datastore infrastructure
- Support for multiple vector databases
- Unified interface across datastores
- Reuse datastore configurations

## Advanced Configuration

### Sync Modes

Control how routes are synchronized:

```python
from semantic_router.schema import SyncMode
from gllm_pipeline.router import SemanticRouter

router = SemanticRouter.aurelio(
    encoder=encoder,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
    auto_sync=SyncMode.LOCAL.value,  # "local", "remote", or "async"
)
```

**Sync Modes:**
- **LOCAL** - Synchronous local updates
- **REMOTE** - Synchronous remote updates
- **ASYNC** - Asynchronous updates

### Custom Route Configuration

Define routes with additional metadata:

```python
from semantic_router import Route
from gllm_pipeline.router import SemanticRouter

# Create routes with custom utterances
routes = [
    Route(
        name="billing",
        utterances=[
            "How do I update my payment method?",
            "Invoice not received",
            "Why was I charged twice?",
        ],
    ),
    Route(
        name="tech_support",
        utterances=[
            "App crashes on launch",
            "Connection timeout when uploading",
            "Error code 504 when syncing files",
        ],
    ),
]

router = SemanticRouter.aurelio(
    encoder=encoder,
    route_examples=routes,
    default_route="billing",
    valid_routes={"billing", "tech_support"},
)
```

### Similarity Threshold

Control matching sensitivity:

```python
router = SemanticRouter.aurelio(
    encoder=encoder,
    routes=routes,
    default_route=default_route,
    valid_routes=valid_routes,
    similarity_threshold=0.7,  # Higher = stricter matching
)
```

## Complete Example: Production Setup

```python
import asyncio
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.backend.aurelio.index import AzureAISearchAurelioIndex

async def setup_production_router():
    # Setup embedding model
    em_invoker = build_em_invoker(
        "openai/text-embedding-3-large",  # Larger model for production
        credentials="<YOUR_OPENAI_API_KEY>"
    )

    # Setup Azure AI Search index for scalability
    index = AzureAISearchAurelioIndex(
        endpoint="https://<your-service>.search.windows.net",
        index_name="production-routes",
        api_key="<YOUR_AZURE_API_KEY>",
    )

    # Define route examples
    route_examples = {
        "billing": [
            "How do I update my payment method?",
            "Invoice not received",
            "Why was I charged twice?",
            "Can I get a refund?",
            "How do I cancel my subscription?",
        ],
        "tech_support": [
            "App crashes on launch",
            "Connection timeout when uploading",
            "Error code 504 when syncing files",
            "The app is very slow",
            "I can't log in to my account",
        ],
        "sales": [
            "What are your pricing plans?",
            "Do you offer enterprise pricing?",
            "What features are included in the pro plan?",
            "Can I upgrade my plan?",
        ],
        "general": [
            "What are your business hours?",
            "How do I contact support?",
            "Where can I find the user guide?",
        ],
    }

    # Create router (em_invoker is auto-wrapped in v0.5+)
    router = SemanticRouter.aurelio(
        encoder=em_invoker,
        index=index,
        route_examples=route_examples,
        default_route="general",
        valid_routes=set(route_examples.keys()),
        similarity_threshold=0.6,  # Balanced threshold
    )

    # Test routing
    test_queries = [
        "My credit card was charged twice",
        "The app keeps crashing",
        "What are your enterprise options?",
        "I need help",
    ]

    for query in test_queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")

asyncio.run(setup_production_router())
```

## Best Practices

1. **Encoder Selection**
   - Pass **BaseEMInvoker** directly for simplicity (auto-wrapped in v0.5+)
   - Use **EMInvokerEncoder** for advanced configuration (e.g., custom name)
   - Use **TEIEncoder** for privacy-critical applications
   - Use **LangchainEncoder** if already using Langchain

2. **Index Selection**
   - Use **LocalIndex** for development/testing
   - Use **AzureAISearchAurelioIndex** for production at scale
   - Use **DataStoreAdapterIndex** to leverage existing datastores

3. **Performance Tuning**
   - Adjust `similarity_threshold` based on your accuracy/recall tradeoff
   - Use larger embedding models for better accuracy
   - Cache embeddings when possible

4. **Monitoring**
   - Log routing decisions for analysis
   - Monitor index size and query latency
   - Track fallback to default route frequency

## Troubleshooting

**Encoder initialization fails?**
- Verify API credentials are correct
- Check network connectivity for remote encoders
- Ensure required packages are installed

**Index operations slow?**
- Consider switching to a faster index type
- Optimize similarity threshold
- Check index size and cleanup old routes

**Routes not matching?**
- Lower the similarity threshold
- Add more diverse route examples
- Verify encoder is working correctly

## See Also

- [Semantic Router](semantic-router.md) - Main Semantic Router documentation
- [Similarity-Based Router](similarity-based-router.md) - Simpler alternative
- [LM-Based Router](lm-based-router.md) - Language model-based routing
