---
icon: magnifying-glass
---

# Level-0 Query Helper

[**`gllm-rag`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-rag/gllm_rag) | **Tutorial**: [query](query.md "mention") | **Use Case:** [Build End-to-End RAG Pipeline](../../../guides/build-end-to-end-rag-pipeline/README.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_rag/index.html)

`query()` is the simplest way to run a RAG flow with `gllm-rag`. It retrieves context from a vector-capable data store, synthesizes a response with an LM, and returns both the answer and the retrieved chunks.

This helper is meant for the most direct retrieve-and-answer workflow. It is a good fit when you want the standard RAG pattern without adding query expansion, routing, or multi-branch orchestration.

Because it is a thin entry point, it is also a useful starting place for understanding how the rest of the reusable blocks fit together.

<details>

<summary>Prerequisites</summary>

This tutorial assumes you are familiar with:

1. [Data Store](../../data-store/README.md "mention")
2. [Retrieval](../../retrieval/README.md "mention")
3. [Inference](../../inference/README.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install gllm-rag gllm-datastore gllm-inference gllm-retrieval gllm-generation
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install gllm-rag gllm-datastore gllm-inference gllm-retrieval gllm-generation
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
pip install gllm-rag gllm-datastore gllm-inference gllm-retrieval gllm-generation
```
{% endtab %}
{% endtabs %}

## Quickstart

We will use `query()` to retrieve context and generate a response in one call.

{% stepper %}
{% step %}
**Import the helper**

```python
from gllm_rag import query
```
{% endstep %}

{% step %}
**Call `query()`**

```python
# `my_datastore` must expose vector capability.
# `my_lm_invoker` is your configured LM invoker.
result = await query(
    question="What is retrieval-augmented generation?",
    datastore=my_datastore,
    lm_invoker=my_lm_invoker,
    top_k=5,
)
```
{% endstep %}

{% step %}
**Use the result**

```python
print(result["response"])
print(result["chunks"])
```
{% endstep %}
{% endstepper %}

## What It Does

1. Validates the inputs.
2. Retrieves chunks from a vector-capable data store.
3. Builds a prompt from the question and the retrieved context.
4. Synthesizes the final answer.
5. Returns the response together with the retrieved chunks.
