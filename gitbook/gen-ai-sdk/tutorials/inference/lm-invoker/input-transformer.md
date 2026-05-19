---
icon: input-pipe
---

# Input Transformer

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [input-transformer.md](input-transformer.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** All LM invokers

## What is Input Transformer?

Input transformer is a module that transforms the input messages of LM invoker before invocations. This is useful for specific scenarios where certain kind of message transformation is required.&#x20;

By default, LM invokers do not apply any input transformer.

LM invokers support chaining **multiple input transformers** through the `input_transformers` parameter.
Each item in `input_transformers` can be provided as:

- a string (transformer type),
- a dictionary,
- or an `InputTransformerConfig` object.

Let's take a look at the available input transformer options!

## Configure Input Transformers

Here's a quick setup example showing multiple accepted formats:

```python
import asyncio
from gllm_inference.input_transformer import InputTransformerConfig
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

input_transformers = [
    # Option 1: as string
    "identity",
    # Option 2: as dictionary
    {"type": "filter_empty"},
    # Option 3: as config object
    InputTransformerConfig.filter_empty(),
]

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    input_transformers=input_transformers,
)
```

## Identity Input Transformer

This input transformer performs identity transformation, meaning that it essentially performs no transformation to the input messages.

**Example:**

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.input_transformer import InputTransformerConfig

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    input_transformers=[InputTransformerConfig.identity()],
)
```

## Filter Empty Input Transformer

This input transformer filters out any empty strings or whitespace only strings from the message contents. This is useful for models where empty strings are unsupported.

{% hint style="warning" %}
This input transformer will raise error if it detects any message that contains no non-empty contents.
{% endhint %}

**Example:**

```python
import asyncio
from gllm_inference.lm_invoker import AnthropicLMInvoker
from gllm_inference.model import AnthropicLM
from gllm_inference.input_transformer import InputTransformerConfig

lm_invoker = AnthropicLMInvoker(
    AnthropicLM.CLAUDE_SONNET_4_5,
    input_transformers=[InputTransformerConfig.filter_empty()],
)

query = """Name an animal whose name starts with the letter A!"""
output = asyncio.run(lm_invoker.invoke([query, " ", ""]))  # The empty strings will be filtered out!
print(output)
```
