---
icon: compass
---

# Routing

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [.](./ "mention") | **Use Case:** [Implement Semantic Routing](../../../guides/build-end-to-end-rag-pipeline/implement-semantic-routing.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

## What's a Router?

A router selects which downstream path (tool, retriever, prompt, agent) to use for a given input. This helps ensure that each query is handled by the most suitable component.

Routers are essential for building intelligent pipelines that can dynamically route queries to different components based on their content, complexity, or other criteria. Whether you need simple keyword-based routing or sophisticated semantic understanding, GL SDK provides multiple router implementations to fit your needs.

<details>

<summary>Prerequisites</summary>

This tutorial requires familiarity with these concepts:

1. [em-invoker.md](../../inference/em-invoker.md "mention") - For embedding-based routers
2. [lm-invoker](../../inference/lm-invoker/ "mention") - For LM-based routers
3. [lm-request-processor.md](../../inference/lm-request-processor.md "mention") - For LM request configuration

</details>

## Supported Router Types

GL SDK provides several router types, each designed for specific use cases and routing strategies:

1. [**Similarity-Based Router**](similarity-based-router.md) - Uses embedding similarity with configurable thresholds for simple semantic routing
2. [**Semantic Router**](semantic-router/) - Advanced semantic similarity with pluggable backends (Native, Aurelio) for flexible routing
3. [**LM-Based Router**](lm-based-router.md) - Leverages language models for intelligent, context-aware routing decisions
4. [**Rule-Based Router**](rule-based-router.md) - Deterministic keyword and pattern matching for explicit control over routing logic

All routers share a common interface and support features like route filtering and fallback handling, making it easy to switch between different routing strategies in your application.

## Installation

```bash
pip install gllm-pipeline gllm-inference
```

## Core Concepts

### Routes and Valid Routes

Every router requires:

* **`valid_routes`**: A set of all possible route names the router can select
* **`default_route`**: A fallback route used when no match is found (must be in `valid_routes`)

### Route Filtering

All routers support restricting available routes at runtime:

```python
# Only allow specific routes for this query
route = asyncio.run(
    router.route(query, route_filter={"billing", "faq"})
)
```

The `route_filter` must include the `default_route` and only contain valid routes.

[^1]: This component may involve Language Model (LM). See [lm-request-processor.md](../../inference/lm-request-processor.md "mention") for more information.
