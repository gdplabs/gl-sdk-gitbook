---
icon: browser
---

# Web Search

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [web-search.md](web-search.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `AnthropicLMInvoker`, `GoogleLMInvoker`, `OpenAILMInvoker`, `XAILMInvoker`

## What is Web Search?

Web search is a native tool that allows the language model to search the web for relevant information. When it's enabled, web search citations are stored in the `outputs` attribute of the `LMOutput` object and can be accessed via the `citations` property.

Web search tool can be enabled with several options:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as string
web_search_tool = "web_search"
# Option 2: as enum
web_search_tool = NativeToolType.WEB_SEARCH
# Option 3: as dictionary (useful for providing custom kwargs)
web_search_tool = {"type": "web_search", **kwargs}
# Option 4: as native tool object (useful for providing custom kwargs)
web_search_tool = NativeTool.web_search(**kwargs)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[web_search_tool])
```

Let's try it to use it to find information about a movie that came out after the LM's cutoff date!

```python
query = "How much did `Zootopia 2` make in the box office?"
output = asyncio.run(lm_invoker.invoke(query))
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
```

**Output:**

```
=== Output item: 'text' ===
As of January 7, 2026, Zootopia 2 has grossed about $1.588 billion worldwide. Breakdown:
- Domestic (U.S. & Canada): approximately $363.65 million
- International: approximately $1.2246 billion

Source: Box Office Mojo. ([boxofficemojo.com](https://www.boxofficemojo.com/release/rl687767553/?utm_source=openai))

=== Output item: 'citation' ===
id='4397687f-b040-47cd-842e-30a1bc249ae2'
content='url_citation'
metadata={
    'type': 'url_citation',
    'title': 'Zootopia 2 - Box Office Mojo',
    'url': 'https://www.boxofficemojo.com/release/rl687767553/?utm_source=openai',
    'start_index': 220,
    'end_index': 311,
}
score=None
```
