---
icon: sliders
---

# [BETA] Custom Processing Hooks

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [custom-processing-hooks.md](custom-processing-hooks.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `OpenAILMInvoker`

## What are custom processing hooks?

Custom processing hooks let you attach your own logic to the LM output lifecycle.

{% hint style="warning" %}
**The custom processing hooks capability is currently in beta and may be subject to changes in future releases. `output_hooks` and `streaming_hooks` are currently available only in `OpenAILMInvoker`.**
{% endhint %}

`OpenAILMInvoker` provides two hook types:

1. `output_hooks`: run for each completed output item in non-streaming and final response processing.
2. `streaming_hooks`: run for each streaming event while tokens and activities are being processed.

## Initialize an LM Invoker with Hooks

```python
from dotenv import load_dotenv
load_dotenv()

from gllm_inference.lm_invoker import OpenAILMInvoker


def capture_output_item(item, output):
    # item: raw OpenAI response output item
    # output: aggregated LMOutput object
    _ = (item, output)


async def observe_stream(event, streamer):
    # event: raw OpenAI stream event
    # streamer: output transformer chain used by LM invoker
    _ = (event, streamer)


lm_invoker = OpenAILMInvoker(
    model_name="gpt-5-nano",
    output_hooks=[capture_output_item],
    streaming_hooks=[observe_stream],
)
```

## Output Hooks

Use `output_hooks` when you want to inspect or augment final parsed outputs.

```python
import asyncio

from gllm_inference.lm_invoker import OpenAILMInvoker


def collect_citations(item, output):
    if not getattr(output, "citations", None):
        return

    print(f"current citations: {len(output.citations)}")


lm_invoker = OpenAILMInvoker(
    model_name="gpt-5-nano",
    output_hooks=[collect_citations],
)

result = asyncio.run(lm_invoker.invoke("Summarize the result and cite sources."))
print(result.text)
```

## Streaming Hooks

Use `streaming_hooks` when you need access to raw streaming events for logging, custom telemetry, or conditional behavior.

```python
import asyncio

from gllm_core.event import EventEmitter
from gllm_inference.lm_invoker import OpenAILMInvoker


async def log_stream_event(event, streamer):
    if event.type.endswith("delta"):
        print(f"stream event: {event.type}")


event_emitter = EventEmitter.with_print_handler()
lm_invoker = OpenAILMInvoker(
    model_name="gpt-5-nano",
    streaming_hooks=[log_stream_event],
)

output = asyncio.run(
    lm_invoker.invoke(
        "Write a short poem about the sea.",
        event_emitter=event_emitter,
    )
)
print(output.text)
```

## When to Use Which Hook

- Use `output_hooks` for post-processing completed output items.
- Use `streaming_hooks` for per-event logic during streaming.
- Use both when you need real-time behavior and final output enrichment.

{% include "../../../../.gitbook/includes/troubleshooting.md" %}
