---
icon: sparkles
---

# Semantic Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [README.md](README.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

The **Semantic Router** uses backend-agnostic semantic similarity to classify queries into predefined routes. It supports multiple backend implementations for flexibility and scalability.

<details>

<summary>Prerequisites</summary>

This tutorial requires familiarity with these concepts:

1. [EM Invoker](../../../inference/em-invoker.md "mention") - For understanding embedding model invocation

</details>

## Overview

The Semantic Router delegates routing logic to pluggable backend implementations, allowing you to switch between different semantic routing algorithms without changing your code.

**Supported Backends:**
- **Native** - Built-in GLLM semantic similarity implementation (via `SemanticRouter.native()`)
- **Aurelio** - Aurelio Labs semantic router (via `SemanticRouter.aurelio()`). More functionalities (encoder, index, etc.) can be found in [aurelio-backend.md](aurelio-backend.md "mention")

## Installation

```bash
pip install gllm-pipeline gllm-inference
```

For Aurelio backend support:
```bash
pip install semantic-router
```

## Quickstart

### Step 1: Set up embeddings

```python
import asyncio
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter

# Create an embedding model invoker
em_invoker = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials="<YOUR_OPENAI_API_KEY>"
)
```

### Step 2: Define routes with examples

```python
routes = {
    "billing": [
        "How do I update my payment method?",
        "Invoice not received",
        "Why was I charged twice?",
    ],
    "tech_support": [
        "App crashes on launch",
        "Connection timeout when uploading",
        "Error code 504 when syncing files",
    ],
    "faq": [
        "What are your business hours?",
        "Where can I find the user guide?",
        "How do I reset my password?",
    ],
}

default_route = "faq"
valid_routes = set(routes.keys())
```

### Step 3: Create the router
#### Option 1: Native Backend

```python
# Create native semantic router
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=routes,
    default_route=default_route,
    valid_routes=valid_routes,
    similarity_threshold=0.5,
)
```

#### Option 2: Aurelio Backend with EM Invoker

```python
from gllm_pipeline.router import SemanticRouter

# Create Aurelio-based semantic router (em_invoker auto-wrapped in v0.5+)
router = SemanticRouter.aurelio(
    encoder=em_invoker,
    route_examples=routes,
    default_route=default_route,
    valid_routes=valid_routes,
    similarity_threshold=0.5,
)
```

#### Option 3: Aurelio Backend with EM Invoker Encoder

```python
from gllm_pipeline.router import SemanticRouter
from gllm_pipeline.router.backend.aurelio.encoders import EMInvokerEncoder

em_encoder = EMInvokerEncoder(em_invoker, name="test-em-invoker")

router = SemanticRouter.aurelio(
    encoder=em_encoder,
    route_examples=routes,
    default_route=default_route,
    valid_routes=valid_routes,
    similarity_threshold=0.5,
)
```

### Step 4: Route queries

```python
# Route a single query
query = "My credit card expired and I can't pay my invoice"
route = asyncio.run(router.route(query))
print(f"Selected route: {route}")  # Output: "billing"

# Route with filtering
route = asyncio.run(
    router.route(query, route_filter={"billing", "faq"})
)
print(f"Filtered route: {route}")
```


### Using Presets

Load predefined route configurations:

```python
from gllm_pipeline.router.schema import BackendType, ModalityType

router = SemanticRouter.from_preset(
    backend=BackendType.AURELIO,
    preset_name="customer_support",
    modality=ModalityType.TEXT,
    default_route="general",
    valid_routes={"billing", "tech_support", "general"},
)
```

### Advanced Configuration

For detailed information on encoders, indexes, and advanced configuration options, see the **[Aurelio Backend Guide](aurelio-backend.md)**:

- **Encoders**: EM Invoker, Langchain, TEI
- **Indexes**: Local, Azure AI Search, Datastore Adapter
- **Sync Modes**: Local, Remote, Async
- **Production Setup**: Complete examples and best practices

## Configuration Options

### Similarity Threshold

Controls the minimum similarity score required to match a route:

```python
# Strict matching (higher threshold)
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=routes,
    default_route=default_route,
    valid_routes=valid_routes,
    similarity_threshold=0.8,  # More selective
)

# Loose matching (lower threshold)
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=routes,
    default_route=default_route,
    valid_routes=valid_routes,
    similarity_threshold=0.3,  # More permissive
)
```

### Route Filtering

Restrict available routes at runtime:

```python
# Only allow specific routes for this query
route = asyncio.run(
    router.route(
        query,
        route_filter={"billing", "faq"}  # Must include default_route
    )
)
```

## Complete Example

```python
import asyncio
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter

async def main():
    # Setup
    em_invoker = build_em_invoker(
        "openai/text-embedding-3-small",
        credentials="<YOUR_OPENAI_API_KEY>"
    )

    routes = {
        "billing": [
            "How do I update my payment method?",
            "Invoice not received",
            "Why was I charged twice?",
        ],
        "tech_support": [
            "App crashes on launch",
            "Connection timeout when uploading",
            "Error code 504 when syncing files",
        ],
        "faq": [
            "What are your business hours?",
            "Where can I find the user guide?",
            "How do I reset my password?",
        ],
    }

    # Create router
    router = SemanticRouter.native(
        em_invoker=em_invoker,
        route_examples=routes,
        default_route="faq",
        valid_routes=set(routes.keys()),
        similarity_threshold=0.5,
    )

    # Route queries
    queries = [
        "My credit card expired and I can't pay my invoice",
        "The app keeps crashing when I try to upload files",
        "What time do you close on weekends?",
    ]

    for query in queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")

# Run
asyncio.run(main())
```

## Best Practices

1. **Route Examples**: Provide diverse, representative examples for each route
2. **Threshold Tuning**: Start with 0.5 and adjust based on your use case
3. **Default Route**: Always set a sensible default for unmatched queries
4. **Validation**: Test with edge cases and ambiguous queries
5. **Monitoring**: Log routing decisions for analysis and improvement

## Troubleshooting

**Routes not matching correctly?**
- Lower the `similarity_threshold`
- Add more diverse examples to routes
- Verify embedding model quality

**Always falling back to default route?**
- Increase the `similarity_threshold`
- Check that route examples are semantically distinct
- Ensure embedding model is appropriate for your domain

## See Also

- [Similarity-Based Router](../similarity-based-router.md) - Simpler alternative with explicit examples
- [LM-Based Router](../lm-based-router.md) - Use language models for routing
- [Rule-Based Router](../rule-based-router.md) - Pattern and keyword-based routing
