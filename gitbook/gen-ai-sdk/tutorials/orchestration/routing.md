---
icon: compass
---

# Routing

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [routing.md](routing.md "mention") | **Use Case:** [implement-semantic-routing.md](../../guides/build-end-to-end-rag-pipeline/implement-semantic-routing.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

## What's a Router?

A router selects which downstream path (tool, retriever, prompt, agent) to use for a given input. This helps ensure that each query is handled by the most suitable component.

The `gllm-pipeline` library provides multiple router implementations, each suited for different use cases:

- **[LM-Based Router](lm-based-router.md)** - Uses a language model to determine the appropriate route
- **[Rule-Based Router](rule-based-router.md)** - Routes based on keyword matching and pattern rules
- **[Semantic Router](semantic-router.md)** - Uses semantic similarity with embeddings to classify queries
- **[Similarity-Based Router](similarity-based-router.md)** - Uses embedding similarity with configurable thresholds

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

You should be familiar with these concepts:

1. [lm-invoker](../inference/lm-invoker/ "mention")
2. [em-invoker.md](../inference/em-invoker.md "mention")
3. [lm-request-processor.md](../inference/lm-request-processor.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-misc"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-misc"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-misc"
```
{% endtab %}
{% endtabs %}

## Quickstart: Semantic Router (Native Backend)

We'll start with the **Semantic Router** using the native backend, which is the simplest to set up. It uses embeddings to measure semantic similarity between input and route examples:

{% stepper %}
{% step %}
**Set up an embedding model**

Create an EM invoker for generating embeddings:

{% code lineNumbers="true" %}
```python
import asyncio
from gllm_inference.em_invoker import build_em_invoker

# Create an embedding model invoker
em_invoker = build_em_invoker(
    "openai/text-embedding-3-small",
    credentials={"api_key": "<YOUR_OPENAI_API_KEY>"}
)
```
{% endcode %}

The embedding model converts text into vectors for similarity comparison.
{% endstep %}

{% step %}
**Define route examples**

Create a mapping of routes to example queries:

{% code lineNumbers="true" %}
```python
route_examples = {
    "faq": [
        "What are your business hours?",
        "Where can I find the user guide?",
        "How do I reset my password?",
    ],
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
}

default_route = "faq"  # fallback route
```
{% endcode %}

Each route has example queries that define its semantic meaning.
{% endstep %}

{% step %}
**Create the router**

Initialize the similarity-based router:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.router import SemanticRouter

router = SemanticRouter.native(
    em_invoker=em_invoker,
    route_examples=route_examples,
    default_route=default_route,
    valid_routes=set(route_examples.keys()),
    similarity_threshold=0.5,  # Adjust based on your needs
)
```
{% endcode %}

The router will use cosine similarity to match input to the most similar route.
{% endstep %}

{% step %}
**Route a query**

Test the router with a sample query:

{% code lineNumbers="true" %}
```python
user_input = "My credit card expired and billing failed."
route = asyncio.run(router.route(user_input))
print(f"Selected route: {route}")  # Output: "billing"
```
{% endcode %}

The router classifies the input and returns the most appropriate route.
{% endstep %}
{% endstepper %}

## Route Filtering

You can restrict which routes the router can select from using `route_filter`:

{% code lineNumbers="true" %}
```python
# Only allow billing and faq routes
filtered_route = asyncio.run(
    router.route(user_input, route_filter={"billing", "faq"})
)
print(f"Filtered route: {filtered_route}")
```
{% endcode %}

The `route_filter` must include the `default_route` and only contain valid routes.


[^1]: This component may involve Language Model (LM). See tutorial about LM Request Processor or related [here](routing.md#lm-request-processor)
