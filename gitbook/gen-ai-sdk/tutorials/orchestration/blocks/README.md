---
icon: blocks
---

# Reusable Blocks

[**`gllm-rag`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-rag/gllm_rag) | **Tutorial**: [blocks](./ "mention") | **Use Case:** [Build End-to-End RAG Pipeline](../../../guides/build-end-to-end-rag-pipeline/README.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_rag/index.html)

The `gllm-rag` package includes reusable blocks, subpipelines, and strategies that you can compose into your own RAG workflows.

These building blocks let you start from a proven pattern and adapt it to your application without wiring every retrieval, routing, or synthesis step from scratch.

The section below groups the reusable pieces by the kind of orchestration problem they solve. Use the helper when you want a minimal flow, use the retrieval and routing blocks when you want to compose your own pipeline, and use the strategies when you want a higher-level end-to-end pattern.

<details>

<summary>Prerequisites</summary>

This tutorial assumes you are familiar with:

1. [Pipeline](../pipeline.md "mention")
2. [State](../state.md "mention")
3. [Steps](../steps/ "mention")

</details>

## Installation

```bash
pip install gllm-rag
```

## Quickstart

We will first import the reusable blocks that you can compose in your own RAG workflows.

{% stepper %}
{% step %}
**Import the reusable blocks**

```python
from gllm_rag import query
from gllm_rag.blocks.retrieval import AgenticRetrievalPipeline, QueryExpansionPipeline, fuse
from gllm_rag.blocks.routing import MultiQueryRoutingPipeline
from gllm_rag.strategies import CRAG, MapReduceRAG, NaiveRAG, RoutedStrategy
```
{% endstep %}

{% step %}
**Pick the right building block**

Use `query()` when you only need a minimal retrieve-and-answer flow. Use the retrieval and routing blocks when you want to compose your own pipeline. Use the strategy classes when you want a higher-level end-to-end RAG pattern.
{% endstep %}

{% step %}
**Move to a focused page**

Each block type is documented in its own page:

1. [Level-0 Query Helper](query.md)
2. [Retrieval Blocks](retrieval.md)
3. [Routing Blocks](routing.md)
4. [RAG Strategies](strategies.md)
{% endstep %}
{% endstepper %}
