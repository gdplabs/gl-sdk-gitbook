---
icon: arrow-right-arrow-left
---

# Routing Blocks

[**`gllm-rag`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-rag/gllm_rag) | **Tutorial**: [routing](routing.md "mention") | **Use Case:** [Build End-to-End RAG Pipeline](../../../guides/build-end-to-end-rag-pipeline/README.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_rag/index.html)

`gllm-rag` includes routing blocks for queries that should be split into multiple sub-queries and sent to different paths.

These blocks help you decompose one request into several smaller requests and send each one to the most suitable branch. They are useful when different parts of the question need different downstream handling.

The main routing block handles decomposition and branch assignment, while the supporting types describe the structure of the routing result.

<details>

<summary>Prerequisites</summary>

This tutorial assumes you are familiar with:

1. [Query Transformer](../../retrieval/query-transformer.md "mention")
2. [Pipeline](../pipeline.md "mention")
3. [Steps](../steps/ "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install gllm-rag gllm-pipeline gllm-retrieval
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install gllm-rag gllm-pipeline gllm-retrieval
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
pip install gllm-rag gllm-pipeline gllm-retrieval
```
{% endtab %}
{% endtabs %}

## Quickstart

We will use the multi-query routing block to split a user query into several sub-queries and route them.

{% stepper %}
{% step %}
**Import the routing block**

```python
from gllm_rag.blocks.routing import MultiQueryRoutingPipeline, PASSTHROUGH
```
{% endstep %}

{% step %}
**Build the router pipeline**

```python
block = MultiQueryRoutingPipeline(
    decomposer=my_query_transformer,
    router=my_router,
    max_sub_queries=4,
    on_empty_decomposition=PASSTHROUGH,
)
```
{% endstep %}

{% step %}
**Invoke the pipeline**

```python
pipeline = block.build()
result = await pipeline.invoke({"query": "Break this question into targeted routes"})
print(result["routing_plan"])
```
{% endstep %}
{% endstepper %}

## Supporting Types

`gllm-rag` exposes a few supporting types for routing:

1. `MultiQueryRoutingState` - the pipeline state used by the routing block.
2. `SubQueryRoute` - a normalized route assignment for one sub-query.
3. `OnEmptyDecompositionPolicy` - controls what happens when decomposition returns no sub-queries.

## Empty-Decomposition Behavior

`OnEmptyDecompositionPolicy` supports two behaviors:

1. `passthrough` - use the original query as a single sub-query.
2. `error` - raise an error instead of continuing.
