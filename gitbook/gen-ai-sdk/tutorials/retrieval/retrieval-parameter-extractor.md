---
icon: sliders
---

# Retrieval Parameter Extractor

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/retrieval_parameter_extractor)| [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [retrieval-parameter-extractor.md](retrieval-parameter-extractor.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/retrieval_parameter_extractor.html)

The retrieval parameter extractor attempts to turn a natural-language query (and optional context) into structured retrieval parameters (e.g., query text, filters, sort). It is useful when you want an LLM to infer filters/sort constraints from user intent before hitting your retriever.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

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

We will use GPT-4.1 nano to extract certain insights from user query.

```python
import asyncio
import json

from gllm_inference.request_processor import build_lm_request_processor
from gllm_retrieval.retrieval_parameter_extractor.lm_based_retrieval_parameter_extractor import (
    LMBasedRetrievalParameterExtractor,
)

def main() -> None:
    SYSTEM_TEMPLATE = """\
        Role: You are an assistant that extracts retrieval parameters from a user query.
        Objective: Infer a structured set of retrieval parameters that a search engine can use.

        AllowedValues (JSON):
        {{
        "department": {allowed_departments_json},
        "content_type": {allowed_content_types_json},
        "sort_fields": {allowed_sort_fields_json},
        "operators": {allowed_operators_json}
        }}

        OutputFormat (JSON):
        {{
        "query": "<string>",
        "filters": [
            {{"field": "<string>", "operator": "<operator_from_allowed_values>", "value": "<string|number|bool>"}}
        ],
        "sort": [
            {{"field": "<sort_field_from_allowed_values>", "order": "asc" | "desc"}}
        ]
        }}

        Instructions:
        - Use only values listed in AllowedValues.
        - Return ONLY a compact JSON object conforming to OutputFormat. No extra text.
    """

    lmrp = build_lm_request_processor(
        model_id="openai/gpt-4.1-nano",
        credentials="<your-api-key>",  # Or use the OPENAI_API_KEY environment variable
        system_template=SYSTEM_TEMPLATE,
        user_template="{query}",
        output_parser_type="json",
    )

    extractor = LMBasedRetrievalParameterExtractor(lm_request_processor=lmrp)

    # Provide JSON-serialized allowed values so they render as JSON in the system template.
    result = asyncio.run(extractor.extract_parameters(
        "Find latest InfoSec security policy documents and prioritize recent updates",
        allowed_departments_json=json.dumps(["InfoSec", "Finance", "HR", "Engineering"]),
        allowed_content_types_json=json.dumps(["security_policies", "standards", "guidelines", "procedures"]),
        allowed_sort_fields_json=json.dumps(["date", "relevance", "title"]),
        allowed_operators_json=json.dumps(["eq", "neq", "gt", "gte", "lt", "lte", "in", "nin", "like"]),
    ))
    print(result)

if __name__ == "__main__":
    main()

```

{% hint style="warning" %}
The system or prompt template must contain the template `{query}`.

The output is expected to be JSON.
{% endhint %}

## Passing a validator

You can optionally pass a validator to validate the result from the LM. You can pass a JSON schema dictionary or a Pydantic `BaseModel`.

The following example uses a validator.

```python
import asyncio
import json
from typing import Literal

from gllm_inference.request_processor import build_lm_request_processor
from gllm_retrieval.retrieval_parameter_extractor.lm_based_retrieval_parameter_extractor import (
    LMBasedRetrievalParameterExtractor,
)
from pydantic import BaseModel, Field


class Filter(BaseModel):
    field: Literal["department", "content_type"]
    operator: Literal["eq", "neq", "gt", "gte", "lt", "lte", "in", "nin", "like"]
    value: str | int | float | bool

class Sort(BaseModel):
    field: Literal["date", "relevance", "title"]
    order: Literal["asc", "desc"]

class RetrievalParams(BaseModel):
    query: str = Field(min_length=1)
    filters: list[Filter] = []
    sort: list[Sort] = []


def main() -> None:
    SYSTEM_TEMPLATE = """\
        Role: You are an assistant that extracts retrieval parameters from a user query.
        Objective: Infer a structured set of retrieval parameters that a search engine can use.

        AllowedValues (JSON):
        {{
        "department": {allowed_departments_json},
        "content_type": {allowed_content_types_json},
        "sort_fields": {allowed_sort_fields_json},
        "operators": {allowed_operators_json}
        }}

        OutputFormat (JSON):
        {{
        "query": "<string>",
        "filters": [
            {{"field": "<string>", "operator": "<operator_from_allowed_values>", "value": "<string|number|bool>"}}
        ],
        "sort": [
            {{"field": "<sort_field_from_allowed_values>", "order": "asc" | "desc"}}
        ]
        }}

        Instructions:
        - Use only values listed in AllowedValues.
        - Return ONLY a compact JSON object conforming to OutputFormat. No extra text.
    """

    lmrp = build_lm_request_processor(
        model_id="openai/gpt-4.1-nano",
        credentials="<your-api-key>",  # Or use the OPENAI_API_KEY environment variable
        system_template=SYSTEM_TEMPLATE,
        user_template="{query}",
        output_parser_type="json",
    )

    extractor = LMBasedRetrievalParameterExtractor(lm_request_processor=lmrp, validator=RetrievalParams)

    # Provide JSON-serialized allowed values so they render as JSON in the system template.
    result = asyncio.run(extractor.extract_parameters(
        "Find latest InfoSec security policy documents and prioritize recent updates",
        allowed_departments_json=json.dumps(["InfoSec", "Finance", "HR", "Engineering"]),
        allowed_content_types_json=json.dumps(["security_policies", "standards", "guidelines", "procedures"]),
        allowed_sort_fields_json=json.dumps(["date", "relevance", "title"]),
        allowed_operators_json=json.dumps(["eq", "neq", "gt", "gte", "lt", "lte", "in", "nin", "like"]),
    ))
    print(result)

if __name__ == "__main__":
    main()

```

[^1]: This component may involve Language Model (LM). See tutorial about LM Request Processor or related [here](retrieval-parameter-extractor.md#lm-request-processor)
