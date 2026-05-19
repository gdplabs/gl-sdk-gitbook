---
icon: text-size
---

# Prompt Operations

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [prompt-operations.md](prompt-operations.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** All LM invokers

## What are Prompt Operations?

Prompt operations let you configure reusable prompt templates directly from an LM invoker, then invoke the model using template variables.

This is useful when you want to standardize prompt structure (for example, system instructions and user prompt patterns) without rebuilding message lists manually on every call.

You can access prompt operations from the `prompt` attribute on any LM invoker.

## Build a Prompt Template

Start by configuring a template with `lm_invoker.prompt.build(...)`.

```python
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
lm_invoker.prompt.build(
    system_template="You are a helpful coding assistant.",
    user_template="Summarize this bug report in 3 bullets: {report}",
)
```

{% hint style="info" %}
`build(...)` accepts either a prebuilt `PromptBuilder` via `prompt_builder=...`, or template inputs (`system_template`, `user_template`, and `prompt_builder_kwargs`). Do not pass both styles at once.
{% endhint %}

## Invoke with Prompt Template

### No Extra Parameters

Start with the simplest invocation by passing only prompt variables.

```python
import asyncio

output = asyncio.run(
    lm_invoker.prompt.invoke(
        report="Summarize why retries are useful for API calls.",
    )
)
print(output.text)
```

### History

Use `history` to include previous conversation turns.

```python
import asyncio
from gllm_inference.schema import Message

history = [
    Message.user("My name is Rina."),
    Message.assistant("Nice to meet you, Rina."),
]

output = asyncio.run(
    lm_invoker.prompt.invoke(
        history=history,
        report="What is my name?",
    )
)
print(output.text)
```

### Extra Contents

Use `extra_contents` to append extra user contents, such as attachments.

```python
import asyncio
from gllm_inference.schema import Attachment

image = Attachment.from_path("./chart.png")

output = asyncio.run(
    lm_invoker.prompt.invoke(
        extra_contents=[image],
        report="Describe this chart briefly.",
    )
)
print(output.text)
```

### Hyperparameters

Use `hyperparameters` to control generation at invocation time.

```python
import asyncio

output = asyncio.run(
    lm_invoker.prompt.invoke(
        report="Explain event-driven architecture.",
        hyperparameters={"temperature": 0.2, "max_tokens": 300},
    )
)
print(output.text)
```

### Event Emitter

Use `event_emitter` to stream output tokens.

```python
import asyncio
from gllm_core.event import EventEmitter

event_emitter = EventEmitter.with_print_handler()

output = asyncio.run(
    lm_invoker.prompt.invoke(
        report="Give me 5 ideas for naming a chatbot.",
        event_emitter=event_emitter,
    )
)
```

### Max Calls

Use `max_calls` to allow multiple internal LM calls (for example, when tools are involved).

```python
import asyncio

output = asyncio.run(
    lm_invoker.prompt.invoke(
        report="Find the answer and use tools if needed.",
        max_calls=3,
    )
)
print(output.text)
```

### Prompt Variables

Any extra keyword arguments are treated as prompt template variables.

```python
import asyncio

lm_invoker.prompt.build(
    system_template="You are a concise assistant.",
    user_template="Answer this question in one paragraph: {query}",
)

output = asyncio.run(lm_invoker.prompt.invoke(query="What is retrieval-augmented generation?"))
print(output.text)
```

## Clear Prompt Configuration

If you want to remove the configured template, call `clear()`.

```python
lm_invoker.prompt.clear()
```

After clearing, configure a new prompt with `build(...)` before calling `prompt.invoke(...)` again.

## Build with Builder

You can also use fluent chaining from the builder utility:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker("openai/gpt-5-nano").prompt.build(
    system_template="You are a concise assistant.",
    user_template="Answer this question: {query}",
)
```
