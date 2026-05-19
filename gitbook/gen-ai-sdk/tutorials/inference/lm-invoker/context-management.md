---
icon: text-width
---

# Context Management

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [context-management.md](context-management.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

## What is context management?

Context management helps you estimate whether your request fits a model's token limits before invocation. This is useful for preventing context overflow errors, selecting the right model, and managing cost.

LM Invoker provides two context management methods:

1. `get_context_window()`: Retrieve model context limits.
2. `count_input_tokens(messages)`: Count estimated input tokens for a request.

## `get_context_window()`

**Supported by:** `AnthropicLMInvoker`, `GoogleLMInvoker`, `XAILMInvoker`

Use `get_context_window()` to retrieve the model context limits:

```python
import asyncio
from gllm_inference.lm_invoker import AnthropicLMInvoker

lm_invoker = AnthropicLMInvoker("claude-sonnet-4-0")

context_window = asyncio.run(lm_invoker.get_context_window())
print(f"max_input_tokens: {context_window.max_input_tokens}")
print(f"max_output_tokens: {context_window.max_output_tokens}")
```

## `count_input_tokens(messages)`

**Supported by:** `AnthropicLMInvoker`, `GoogleLMInvoker`, `OpenAILMInvoker`

Use `count_input_tokens(messages)` to estimate request size before invoking the model:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Message

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)

messages = [
    Message.system("You are a helpful assistant."),
    Message.user("Summarize this paragraph in one sentence."),
]

input_tokens = asyncio.run(lm_invoker.count_input_tokens(messages))
print(f"input_tokens: {input_tokens}")
```

You can combine both methods to guard invocations:

```python
context_window = asyncio.run(lm_invoker.get_context_window())
input_tokens = asyncio.run(lm_invoker.count_input_tokens(messages))

if context_window.max_input_tokens and input_tokens > context_window.max_input_tokens:
    raise ValueError("Input exceeds model context window")
```

{% hint style="info" %}
If a method is not supported by a provider/model, LM Invoker raises `NotImplementedError`.
{% endhint %}

{% include "../../../../.gitbook/includes/troubleshooting.md" %}
