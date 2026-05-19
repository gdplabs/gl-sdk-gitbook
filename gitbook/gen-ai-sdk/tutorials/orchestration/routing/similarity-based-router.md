---
icon: chart-line
---

# Similarity-Based Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [similarity-based-router.md](similarity-based-router.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

The **Similarity-Based Router** uses embedding models to measure semantic similarity between input and predefined route examples. It's the simplest and most straightforward routing approach.

{% hint style="warning" %}
**Deprecated in v0.5**: `SimilarityBasedRouter` is superseded by `SemanticRouter.native()`. While `SimilarityBasedRouter` still works, we recommend migrating to the new API. See [Semantic Router](semantic-router/) and the [migration guide](../migration-guide/gllm-pipeline-v0.4-to-v0.5.md) for details.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This tutorial requires familiarity with these concepts:

1. [em-invoker.md](../../inference/em-invoker.md "mention") - For understanding embedding model invocation

</details>

## Installation

```bash
pip install gllm-pipeline gllm-inference
```

## Basic Usage

### Step 1: Set up an embedding model

```python
import asyncio
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter

# Create an embedding model invoker
em_invoker = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials={"api_key": "<YOUR_OPENAI_API_KEY>"}
)
```

### Step 2: Define route examples

```python
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
    "faq": [
        "What are your business hours?",
        "Where can I find the user guide?",
        "How do I reset my password?",
        "What payment methods do you accept?",
        "How do I contact support?",
    ],
}

default_route = "faq"
```

### Step 3: Create the router

```python
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.5,
)
```

### Step 4: Route queries

```python
# Route a single query
query = "My credit card was charged twice"
route = asyncio.run(router.route(query))
print(f"Selected route: {route}")  # Output: "billing"

# Route with filtering
route = asyncio.run(
    router.route(query, route_filter={"billing", "faq"})
)
print(f"Filtered route: {route}")
```

## Understanding Similarity Threshold

The similarity threshold controls how selective the router is:

```python
# Strict matching (high threshold = only very similar matches)
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.8,  # Only match if very similar
)

# Loose matching (low threshold = more permissive)
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.3,  # Match even with moderate similarity
)

# Balanced (recommended starting point)
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.5,  # Balanced approach
)
```

## Complete Example

```python
import asyncio
from gllm_inference.em_invoker import build_em_invoker
from gllm_pipeline.router import SemanticRouter

async def main():
    # Setup embedding model
    em_invoker = build_em_invoker(
        "openai/text-embedding-3-small",
        credentials={"api_key": "<YOUR_OPENAI_API_KEY>"}
    )

    # Define comprehensive route examples
    route_examples = {
        "billing": [
            "How do I update my payment method?",
            "Invoice not received",
            "Why was I charged twice?",
            "Can I get a refund?",
            "How do I cancel my subscription?",
            "What is my current balance?",
            "When is my payment due?",
        ],
        "tech_support": [
            "App crashes on launch",
            "Connection timeout when uploading",
            "Error code 504 when syncing files",
            "The app is very slow",
            "I can't log in to my account",
            "The app won't open",
            "I'm getting an error message",
        ],
        "sales": [
            "What are your pricing plans?",
            "Do you offer enterprise pricing?",
            "What features are included in the pro plan?",
            "Can I upgrade my plan?",
            "Do you offer discounts for annual billing?",
        ],
        "faq": [
            "What are your business hours?",
            "Where can I find the user guide?",
            "How do I reset my password?",
            "What payment methods do you accept?",
            "How do I contact support?",
        ],
    }

    # Create router
    router = SemanticRouter.native(
        em_invoker=em_invoker,
        route_examples=route_examples,
        default_route="faq",
        valid_routes=set(route_examples.keys()),
        similarity_threshold=0.5,
    )

    # Test with various queries
    test_queries = [
        "My credit card was charged twice",
        "The app keeps crashing when I try to upload files",
        "What are your enterprise pricing options?",
        "What time do you close on weekends?",
        "I forgot my password",
    ]

    print("Routing Results:")
    print("-" * 50)

    for query in test_queries:
        route = await router.route(query)
        print(f"Query: {query}")
        print(f"Route: {route}\n")

asyncio.run(main())
```

## Advanced Configuration

### Using Different Embedding Models

```python
# Small, fast embeddings
em_invoker_small = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials={"api_key": "<YOUR_OPENAI_API_KEY>"}
)

router = SemanticRouter.native(
    em_invoker=em_invoker_small,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.5,
)

# Large, more accurate embeddings
em_invoker_large = build_em_invoker(
    "openai/text-embedding-3-large",
    credentials={"api_key": "<YOUR_OPENAI_API_KEY>"}
)

router = SemanticRouter.native(
    em_invoker=em_invoker_large,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.5,
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

### Dynamic Route Examples

Update route examples after initialization:

```python
# Create router
router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.5,
)

# Add new examples (create new router with updated examples)
updated_examples = {
    **route_examples,
    "new_route": [
        "Example query 1",
        "Example query 2",
    ]
}

router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=updated_examples,
    default_route=default_route,
    valid_routes=set(updated_examples.keys()),
    similarity_threshold=0.5,
)
```

## Best Practices

1. **Quality Examples**: Provide diverse, representative examples for each route
   ```python
   # Good: Diverse examples
   "billing": [
       "How do I update my payment method?",
       "Invoice not received",
       "Why was I charged twice?",
       "Can I get a refund?",
   ]

   # Poor: Similar examples
   "billing": [
       "Payment issue",
       "Payment problem",
       "Payment question",
   ]
   ```

2. **Threshold Tuning**: Start with 0.5 and adjust based on results
   ```python
   # Test different thresholds
   for threshold in [0.3, 0.5, 0.7]:
       router = SemanticRouter.native(
           em_invoker=em_invoker,
           route_examples=route_examples,
           default_route=default_route,
           valid_routes=set(route_examples.keys()),
           similarity_threshold=threshold,
       )
       # Test and evaluate
   ```

3. **Distinct Routes**: Ensure routes are semantically distinct
   ```python
   # Good: Distinct routes
   {
       "billing": ["payment", "invoice", "charge"],
       "tech_support": ["crash", "error", "bug"],
       "sales": ["pricing", "plan", "feature"],
   }
   ```

4. **Monitoring**: Log routing decisions for analysis
   ```python
   route = asyncio.run(router.route(query))
   print(f"Query: {query} -> Route: {route}")
   ```

## Troubleshooting

**Routes not matching correctly?**
- Lower the `similarity_threshold` (e.g., from 0.5 to 0.3)
- Add more diverse examples to routes
- Verify embedding model is appropriate for your domain

**Always falling back to default route?**
- Increase the `similarity_threshold` (e.g., from 0.5 to 0.7)
- Check that route examples are semantically distinct
- Ensure examples are representative of actual queries

**Slow routing?**
- Use smaller embedding model (text-embedding-3-small)
- Cache embeddings if routes are static
- Consider rule-based routing for simple patterns

**Incorrect route selection?**
- Add more examples to the correct route
- Remove ambiguous examples
- Increase threshold to be more selective

## Comparison with Other Routers

| Router | Approach | Speed | Accuracy | Complexity |
|--------|----------|-------|----------|-----------|
| Similarity-Based | Embedding similarity | Fast | Good | Low |
| Semantic | Advanced similarity | Medium | Excellent | Medium |
| LM-Based | Language model reasoning | Slow | Excellent | High |
| Rule-Based | Keyword matching | Very Fast | Fair | Low |

## See Also

- [Semantic Router](semantic-router/) - Advanced embedding-based routing
- [LM-Based Router](lm-based-router.md) - Language model-based routing
- [Rule-Based Router](rule-based-router.md) - Pattern and keyword-based routing
