---
icon: shapes
---

# RAG Strategies

[**`gllm-rag`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-rag/gllm_rag) | **Tutorial**: [strategies.md](strategies.md "mention") | **Use Case:** [build-end-to-end-rag-pipeline](../../../guides/build-end-to-end-rag-pipeline/ "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_rag/index.html)

`gllm-rag` provides reusable strategy classes for common RAG patterns. These strategies are useful when you want a higher-level entry point than assembling every step yourself.

The strategy layer gives you a small set of ready-made orchestration patterns that you can adapt to your data and retrieval stack. It is useful when you want to standardize how your RAG system retrieves, filters, reranks, or routes requests.

Each strategy offers a different shape of workflow, from a simple linear path to multi-query fusion and branch routing.

<details>

<summary>Prerequisites</summary>

This tutorial assumes you are familiar with:

1. [pipeline.md](../pipeline.md "mention")
2. [retriever](../../retrieval/retriever/ "mention")
3. [generation](../../generation/ "mention")

</details>

## Available Strategies

`gllm-rag` provides the following built-in strategies:

1. `NaiveRAG` - a simple linear retrieve-and-generate strategy.
2. `MapReduceRAG` - a multi-query strategy that expands the request, retrieves in parallel, and fuses results.
3. `CRAG` - a corrective strategy that branches based on retrieval quality.
4. `RoutedStrategy` - a branch-routing strategy that dispatches to a selected path.

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install gllm-rag gllm-generation gllm-inference gllm-pipeline gllm-retrieval
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install gllm-rag gllm-generation gllm-inference gllm-pipeline gllm-retrieval
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
pip install gllm-rag gllm-generation gllm-inference gllm-pipeline gllm-retrieval
```
{% endtab %}
{% endtabs %}

## Quickstart

We will use the higher-level strategy classes to assemble common RAG patterns.

{% stepper %}
{% step %}
**Import the strategy classes**

```python
from gllm_rag.strategies import CRAG, MapReduceRAG, NaiveRAG, RoutedStrategy
```
{% endstep %}

{% step %}
**Create the strategies**

```python
naive = NaiveRAG(
    retriever=my_retriever,
    response_synthesizer=my_response_synthesizer,
)

map_reduce = MapReduceRAG(
    transformer=my_query_transformer,
    retriever=my_retriever,
    response_synthesizer=my_response_synthesizer,
)

crag = CRAG(
    retriever=my_retriever,
    response_synthesizer=my_response_synthesizer,
)

routed = (
    RoutedStrategy()
    .add_branch("naive", classifier=lambda q: "simple" in q, branch=naive)
    .add_branch("deep", classifier=lambda q: "deep" in q, branch=map_reduce)
)
```
{% endstep %}

{% step %}
**Run the strategy**

```python
result = await naive.arun(question="What is retrieval-augmented generation?")
print(result["response"])
```
{% endstep %}
{% endstepper %}

## Strategy Base Classes

The strategy framework centers on a few core ideas:

1. `Strategy` - the base class for configurable RAG strategies.
2. `uses()` - marks optional strategy slots that can be filled in later.
3. `CompositeStrategy` - the base class for strategies that combine multiple branches or subpipelines.

These are the building blocks that make the higher-level strategies composable and reusable.

## Naive RAG

`NaiveRAG` is the simplest end-to-end strategy. It retrieves context, optionally expands the query, optionally filters or reranks the results, and then generates the response.

Use it when you want a straightforward baseline RAG flow with a small number of optional upgrades.

```python
from gllm_rag.strategies import NaiveRAG

strategy = NaiveRAG(
    retriever=my_retriever,
    response_synthesizer=my_response_synthesizer,
).with_query_expansion(my_query_expansion)

result = await strategy.arun(question="What is retrieval-augmented generation?")
print(result["response"])
```

## Map-Reduce RAG

`MapReduceRAG` expands a query into multiple sub-queries, retrieves context for each one, fuses the results, and then generates the final answer.

Use it when one query should be answered from multiple retrieval angles.

```python
from gllm_rag.strategies import MapReduceRAG

strategy = MapReduceRAG(
    transformer=my_query_transformer,
    retriever=my_retriever,
    response_synthesizer=my_response_synthesizer,
)

result = await strategy.arun(question="Compare the available retrieval blocks")
```

## CRAG

`CRAG` adds a corrective decision step after retrieval.

It can:

1. Continue with the retrieved chunks when they look relevant.
2. Fall back to web retrieval when the main results are irrelevant.
3. Use only the filtered chunks when the results are partially useful.

Use it when you want the system to react differently based on retrieval quality.

```python
from gllm_rag.strategies import CRAG

strategy = CRAG(
    retriever=my_retriever,
    response_synthesizer=my_response_synthesizer,
)

result = await strategy.arun(question="Find the most relevant context and answer")
```

## Routed Strategy

`RoutedStrategy` dispatches a query to one of multiple branches. The routing can be classifier-driven or router-driven, and each branch can itself be a strategy or a pipeline.

Use it when the question should be sent to one of several specialized flows.

```python
from gllm_rag.strategies import RoutedStrategy

routed = (
    RoutedStrategy()
    .add_branch("naive", classifier=lambda q: "simple" in q, branch=my_naive_strategy)
    .add_branch("map_reduce", classifier=lambda q: "compare" in q, branch=my_map_reduce_strategy)
)

result = await routed.arun(question="simple question about RAG")
```

## Example

```python
from gllm_rag.strategies import CRAG, MapReduceRAG, NaiveRAG, RoutedStrategy
```

These strategies are the easiest way to reuse `gllm-rag` in application code because they package common orchestration patterns into a single entry point.
