---
icon: pickaxe
---

# Retrieval Blocks

[**`gllm-rag`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-rag/gllm_rag) | **Tutorial**: [retrieval.md](retrieval.md "mention") | **Use Case:** [build-end-to-end-rag-pipeline](../../../guides/build-end-to-end-rag-pipeline/ "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_rag/index.html)

`gllm-rag` includes reusable retrieval blocks for cases where a single retrieve step is not enough.

These blocks let you expand a query, retrieve from several angles, and combine the results before generation. They are useful when the best answer depends on broader recall, iterative evidence gathering, or fusion of multiple result sets.

Each block solves a different retrieval problem, so you can choose the one that matches the shape of your query and the depth of evidence you need.

<details>

<summary>Prerequisites</summary>

This tutorial assumes you are familiar with:

1. [query-transformer.md](../../retrieval/query-transformer.md "mention")
2. [retriever](../../retrieval/retriever/ "mention")
3. [pipeline.md](../pipeline.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install gllm-rag gllm-retrieval gllm-pipeline gllm-inference
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install gllm-rag gllm-retrieval gllm-pipeline gllm-inference
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
pip install gllm-rag gllm-retrieval gllm-pipeline gllm-inference
```
{% endtab %}
{% endtabs %}

## Quickstart

We will use the retrieval blocks to expand a query, retrieve several result sets, and combine them into one context list.

{% stepper %}
{% step %}
**Import the retrieval blocks**

```python
from gllm_rag.blocks.retrieval import AgenticRetrievalPipeline, QueryExpansionPipeline, fuse
```
{% endstep %}

{% step %}
**Build a query expansion pipeline**

```python
query_expansion = QueryExpansionPipeline(transformer=my_query_transformer)
pipeline = query_expansion.build(my_retriever)
```
{% endstep %}

{% step %}
**Invoke the pipeline**

```python
result = await pipeline.invoke({"query": "How do the new blocks fit together?"})
print(result["chunks"])
```
{% endstep %}
{% endstepper %}

## Agentic Retrieval Pipeline

The `AgenticRetrievalPipeline` runs retrieval in a bounded loop. It can retrieve, select, evaluate, and retry until it has enough evidence or reaches its limit.

Use it when the system should decide whether the current evidence is good enough before answering.

```python
from gllm_rag.blocks.retrieval import AgenticRetrievalPipeline

pipeline = AgenticRetrievalPipeline(
    retriever=my_retriever,
    selector=my_selector,
    evaluator=my_evaluator,
)
```

## Query Expansion Pipeline

The `QueryExpansionPipeline` expands one user query into multiple sub-queries, retrieves for each of them, and fuses the results back into a single chunk list.

Use it when a question benefits from broader recall, such as when the wording is ambiguous or when the answer may be distributed across several relevant sources.

```python
from gllm_rag.blocks.retrieval import QueryExpansionPipeline

query_expansion = QueryExpansionPipeline(transformer=my_query_transformer)
pipeline = query_expansion.build(my_retriever)
```

## Chunk Fusion

The `fuse()` helper combines multiple ranked chunk lists into one list.

It supports:

1. `rrf` - Reciprocal Rank Fusion.
2. `concat` - Concatenate lists while deduplicating repeated chunks.

Use `fuse()` when you already have multiple retrieval results and want a single ranked context list for generation.

```python
from gllm_rag.blocks.retrieval import fuse

fuse_step = fuse(
    fn="rrf",
    input_state="chunk_lists",
    output_state="chunks",
)
```
