---
icon: diagram-predecessor
---

# Query Transformer

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/query_transformer) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial** : [query-transformer.md](query-transformer.md "mention") | **Use Case**: [query-transformation.md](../../guides/build-end-to-end-rag-pipeline/query-transformation.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/query_transformer.html)

Query transformation is the process of modifying a user's original query using LMs to generate one or more refined or expanded queries, aiming to improve the retrieval of relevant documents by enhancing the search scope and effectiveness.

Query transformation specifically attempts to address three problems when processing user queries for retrieval:

1. **Nuanced user intent**: Users often don't mean what they write. They are prone to assuming that since an LM is an "expert", the LM would have the same knowledge domain as them.
2. **Query-document mismatch**: Queries to a vector store are often based on semantic similarity. However, queries are short; documents are long. Moreover, the vocabulary present in the target document may not be present in the query.
3. **Complexity**: Some queries are not as simple: they may be _multi-part_ (containing multiple points to address) or _multi-hop_ (requiring multiple reasoning steps).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [lm-invoker](../inference/lm-invoker/ "mention")
2. [lm-request-processor.md](../inference/lm-request-processor.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-retrieval"
```

{% endtab %}
{% endtabs %}

## Quickstart

We will use GPT-4.1 nano to initialize the one-to-one query transformation component. The component will transform 1 query into another query.

{% stepper %}
{% step %}
**Imports**

Import the following:

```python
import asyncio

from gllm_inference.request_processor import build_lm_request_processor
from gllm_retrieval.query_transformer.one_to_one_query_transformer import OneToOneQueryTransformer
from gllm_retrieval.query_transformer.query_transformer import BaseQueryTransformer
```

{% endstep %}

{% step %}
**Create an LM request processor**

The LM request processor will assist us in filling in the prompt template and sending our request to the LM.

{% hint style="warning" %}
The query transformer module expects the prompt to have the template `{query}` in either the System or the User template.
{% endhint %}

```python
lmrp = build_lm_request_processor(
    model_id="openai/gpt-4.1-nano",
    credentials="<your-api-key>",     # or use the environment variable OPENAI_API_KEY
    system_template="You are a helpful assistant that rewrites queries for better retrieval. Rewrite the following query. Only output the transformed query.",
    user_template="Query: {query}",          # 'query' will be supplied below (string or dict with matching keys)
)
```

{% endstep %}

{% step %}
**Create a one-to-one query transformer**

Once the LM request processor is created, you can call the one-to-one query transformer and see it get transformed.

```python
transformer = OneToOneQueryTransformer(
    lm_request_processor=lmrp
)

single_input = "Find recent research on diffusion transformers."

result = asyncio.run(transformer.transform(single_input))
print(result[0])  # Result is a string with a single element.
```

{% endstep %}
{% endstepper %}

## Extracting transformation result from structured output

You can control how LM outputs are converted into the final transformed queries by supplying the `extract_func` argument to the transformer.

### Example 1: Extracting from JSON Output

The query transformers have a convenience function `json_extractor` which outputs an extractor function that extracts the output from a specific key, assuming that the LM output is already parsed as a dictionary.

```python
SYSTEM_TEMPLATE = """
You are a helpful assistant that rewrites queries for better retrieval.
Rewrite the following query. Only output the transformed query as JSON with the following format:
{{"query": "<your-result>"}}
"""

lmrp = build_lm_request_processor(
    model_id="openai/gpt-4.1-nano",
    system_template=SYSTEM_TEMPLATE,
    user_template="{query}",
    output_parser_type="json",  # depends on your inference stack configuration
)

transformer = OneToOneQueryTransformer(
    lm_request_processor=lmrp,
    extract_func=OneToOneQueryTransformer.json_extractor("query"),
)

result = asyncio.run(transformer.transform("Rewrite for better retrieval: diffusion transformers"))
print(result[0])
```

### Example 2: Extracting from Structured Output

You can take advantage of our LM Invoker's capability to produce structured output. To do so, define a `response_schema` during the LM request processor building. It is recommended that you use a Pydantic `BaseModel` as the `response_schema`.

```python
from pydantic import BaseModel


class TransformResult(BaseModel):
    query: str | list[str]


SYSTEM_TEMPLATE = """
You are a helpful assistant that rewrites queries for better retrieval.
Rewrite the following query. Only output the transformed query as JSON with the following format:
{{"query": "<your-result>"}}
"""

lmrp = build_lm_request_processor(
    model_id="openai/gpt-4.1-nano",
    config={"response_schema": TransformResult},
    system_template=SYSTEM_TEMPLATE,
    user_template="{query}",
)

transformer = OneToOneQueryTransformer(
    lm_request_processor=lmrp,
    extract_func=lambda lm_output: lm_output.structured_output.query  # The output is an LMOutput object. Access the Pydantic model in the `structured_output` attribute.
)

result = asyncio.run(transformer.transform("Rewrite for better retrieval: diffusion transformers"))
print(result[0])  # ['rewritten text']

```

## Error handling

Sometimes, the query transformation did not go as planned, usually due to malformed responses. To handle this, the Query Transformer has 3 error handling modes available: KEEP, EMPTY, and RAISE.

1. KEEP: Returns the original input, coerced into `list[str]`.
2. EMPTY: Return an empty list.
3. RAISE: Re-raise the exception.

The error handling mode could be set using the `on_error` constructor argument.

```python
from gllm_retrieval.query_transformer.query_transformer import ErrorHandling,

transformer = OneToOneQueryTransformer(
    lm_request_processor=lmrp,
    extract_func=extract,
    on_error=ErrorHandling.RAISE,  # This will raise the original error.
)
```

[^1]: This component may involve Language Model (LM). See tutorial about LM Request Processor or related [here](query-transformer.md#lm-request-processor)
