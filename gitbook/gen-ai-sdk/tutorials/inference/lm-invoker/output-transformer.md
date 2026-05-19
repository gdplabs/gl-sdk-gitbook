---
icon: square-half-stroke
---

# Output Transformer

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [output-transformer.md](output-transformer.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** All LM invokers

## What is Output Transformer?

**Output transformers** allow you to transform the raw output from the language model into a different format or structure. This is useful when you want to post-process the model's output before returning it to your application.

By default, LM invokers do not apply any output transformer.

LM invokers support chaining **multiple output transformers** through the `output_transformers` parameter.
Each item in `output_transformers` can be provided as:

- a string (transformer type),
- a dictionary,
- or an `OutputTransformerConfig` object.

Let's take a look at the available output transformer options!

## Configure Output Transformers

Here's a quick setup example showing multiple accepted formats:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

output_transformers = [
    # Option 1: as string
    "identity",
    # Option 2: as dictionary
    {"type": "json"},
    # Option 3: as config object
    OutputTransformerConfig.think_tag(),
    # Option 4: as config object with kwargs
    OutputTransformerConfig.event_filter(["thinking"]),
]

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    output_transformers=output_transformers,
)
```

## Identity Output Transformer

This output transformer performs identity transformation, meaning that it essentially performs no transformation to the output.

**Example:**

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    output_transformers=[OutputTransformerConfig.identity()],
)
```

## JSON Output Transformer

This output transformer automatically parses JSON strings contained in text objects into structured outputs. This is useful for language models that don't naturally support structured output.&#x20;

{% hint style="warning" %}
JSON output transformer can only extract a single JSON object from a single text output item.
{% endhint %}

When utilizing this output transformer, we can instruct the model to output a structured JSON:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    output_transformers=[OutputTransformerConfig.json()],
)

query = """Return a JSON object with keys 'name' and 'age' for a person named John who is 30 years old!"""
output = asyncio.run(lm_invoker.invoke(query))
print(output)
```

**Output:**

<pre class="language-python"><code class="lang-python"><strong># Without JSON output transformer (Raw output)
</strong>LMOutput(
    outputs=[
        LMOutputItem(type='text', output='Sure, here you go:\n{"name": "John", "age": 30}')
    ],
)

<strong># With JSON output transformer
</strong>LMOutput(
    outputs=[
        LMOutputItem(type='structured', output={'name': 'John', 'age': 30})
    ],
)
</code></pre>

## Think Tag Output Transformer

Some open source models, such as DeepSeek R1, embed their thinking output as part of the text output by separating them using the `<think>...</think>` special tags. To extract these thinking output gracefully, we can use the think tag output transformer.&#x20;

This output transformer automatically handles these embedded thinking token both in the `LMOutput` object as well as in the streaming events. Feel free to utilize it the next time you try an open source model that utilize this kind of formatting to output their thinking!

Here's an example:&#x20;

```python
import os
import asyncio
from gllm_inference.lm_invoker import OpenAIChatCompletionsLMInvoker
from gllm_inference.output_transformer import OutputTransformerConfig

lm_invoker = OpenAIChatCompletionsLMInvoker(
    model_name="deepseek-ai/DeepSeek-R1",
    base_url="https://api.deepinfra.com/v1",
    api_key=os.getenv("DEEPINFRA_API_KEY"),
    output_transformers=[OutputTransformerConfig.think_tag()],
    output_analytics=True,
)

query = """Solve this equation: 2x + 3 = 11"""
output = asyncio.run(lm_invoker.invoke(query))
print(output)
```

**Output:**

<pre class="language-python"><code class="lang-python"><strong># Without think tag output transformer (Raw output)
</strong>LMOutput(
    outputs=[
        LMOutputItem(type='text', output="""
            &#x3C;think>\nI have this equation: 2x + 3 = 11. I need to solve for x.
            Solving means ...I think I\'m good.\n&#x3C;/think>\n
            To solve the equation...**Solution**: \\(x = 4\\)
        """)
    ],
)

<strong># With think tag output transformer
</strong>LMOutput(
    outputs=[
        LMOutputItem(type='thinking', output=Reasoning(
            reasoning="""
                I have this equation: 2x + 3 = 11. I need to solve for x.
                Solving means ...I think I\'m good.\n
            """, ...)
        ),
        LMOutputItem(type='text', output="""
            \nTo solve the equation...**Solution**: \\(x = 4\\)
        """),
    ],
)
</code></pre>

## Event Filter Output Transformer

This output transformer filters streaming events by event type. It is useful when you only want selected event streams (for example `thinking`) and want to ignore unrelated events.

When you pass base event types, the transformer also keeps their `_start` and `_end` variants automatically.

Here's an example:

```python
import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.output_transformer import OutputTransformerConfig

lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO,
    thinking=True,
    output_transformers=[OutputTransformerConfig.event_filter(["thinking"])],
)

query = """Solve the equation 2x + 4 = 10."""
event_emitter = EventEmitter.with_print_handler()
output = asyncio.run(lm_invoker.invoke(query, event_emitter=event_emitter))
print(output)
```

**Streaming events comparison:**

Without event filter output transformer:

```text
╭────────────────────────╮
│     THINKING START     │
╰────────────────────────╯
**Solving the equation**

The user asked me to solve the equation \(2x + 4 = 10\). This is pretty straightforward! I'll say that first, subtract 4 from both sides, giving me \(2x = 6\). Then, I'll divide by 2, and I find \(x = 3\). I can also mention that the domain is all real numbers. To confirm, substituting back, \(2*3 + 4 = 10\) holds true. Let's keep the final response concise!
╭──────────────────────╮
│     THINKING END     │
╰──────────────────────╯

╭────────────────────────╮
│     RESPONSE START     │
╰────────────────────────╯
x = 3

Reason:
- Subtract 4 from both sides: 2x = 6
- Divide by 2: x = 3
- Check: 2(3) + 4 = 6 + 4 = 10.
╭──────────────────────╮
│     RESPONSE END     │
╰──────────────────────╯
```

With event filter output transformer (`event_filter(["thinking"])`):

```text
╭────────────────────────╮
│     THINKING START     │
╰────────────────────────╯
**Solving the equation**

The user asked me to solve the equation \(2x + 4 = 10\). This is pretty straightforward! I'll say that first, subtract 4 from both sides, giving me \(2x = 6\). Then, I'll divide by 2, and I find \(x = 3\). I can also mention that the domain is all real numbers. To confirm, substituting back, \(2*3 + 4 = 10\) holds true. Let's keep the final response concise!
╭──────────────────────╮
│     THINKING END     │
╰──────────────────────╯
```

{% hint style="info" %}
You can pass either base event types (for example `thinking`) or suffixed types (for example `thinking_start`). Both are normalized to the same filtered group.
{% endhint %}
