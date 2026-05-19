---
icon: arrow-progress
---

# GLLM Generation v0.5 to v0.6

As you may have noticed, several legacy modules in GLLM Generation v0.5 have been marked as deprecated for a while. If your application is still using them, you should have received warning logs.

Backward compatibility will be **removed** in the upcoming minor version `v0.6.0`. Please review this migration guide to ensure a smooth transition.

{% hint style="info" %}
Note: If you've set the GLLM Generation dependency in your app as `>=0.5.0, <0.6.0`, you don't have to do this migration immediately, as you're locked to `v0.5.x`. You will only migrate to `0.6.0` when you choose to do so by updating your dependency to `^0.6.0`.

However, it's still recommended to do so ASAP to be able to access new features that will be added in the future.
{% endhint %}

## Response Synthesizer

### Deprecated Classes Removed

The following deprecated response synthesizer classes have been **removed**:

1. `StuffResponseSynthesizer`
2. `StaticListResponseSynthesizer`

**Before (v0.5):**

```python
from gllm_generation.response_synthesizer import StuffResponseSynthesizer

synthesizer = StuffResponseSynthesizer(
    lm_request_processor=lm_request_processor,
    streamable=True,
    extractor_func=my_extractor
)
```

**After (v0.6):**

```python
from gllm_generation.response_synthesizer import ResponseSynthesizer

synthesizer = ResponseSynthesizer.stuff(
    lm_request_processor=lm_request_processor,
    streamable=True,
    extractor_func=my_extractor
)
```

### Preset Methods Removed

The following preset factory methods have been **removed** from `ResponseSynthesizer`:

1. `ResponseSynthesizer.stuff_preset()`
2. `ResponseSynthesizer.map_reduce_preset()`
3. `ResponseSynthesizer.refine_preset()`

Use the new `ResponseSynthesizer.preset` factory instead:

**Before (v0.5):**

```python
from gllm_generation.response_synthesizer import ResponseSynthesizer

# Stuff preset
synthesizer = ResponseSynthesizer.stuff_preset(
    model_id="openai/gpt-4",
    credentials="your-api-key",
    system_template="Answer the question based on context: {context}",
    user_template="{query}"
)

# Map-reduce preset
synthesizer = ResponseSynthesizer.map_reduce_preset(
    map_model_id="openai/gpt-4",
    reduce_model_id="openai/gpt-4",
    map_credentials="your-api-key",
    reduce_credentials="your-api-key"
)

# Refine preset
synthesizer = ResponseSynthesizer.refine_preset(
    model_id="openai/gpt-4",
    credentials="your-api-key"
)
```

**After (v0.6):**

```python
from gllm_generation.response_synthesizer import ResponseSynthesizer

# Stuff preset
synthesizer = ResponseSynthesizer.preset.stuff(
    model_id="openai/gpt-4",
    credentials="your-api-key",
    system_template="Answer the question based on context: {context}",
    user_template="{query}"
)

# Map-reduce preset
synthesizer = ResponseSynthesizer.preset.map_reduce(
    map_model_id="openai/gpt-4",
    reduce_model_id="openai/gpt-4",
    map_credentials="your-api-key",
    reduce_credentials="your-api-key"
)

# Refine preset
synthesizer = ResponseSynthesizer.preset.refine(
    model_id="openai/gpt-4",
    credentials="your-api-key"
)
```

### `state_variables` Parameter Removed

The deprecated `state_variables` parameter has been removed from `synthesize_response()` method.

**Before (v0.5):**

```python
result = await synthesizer.synthesize_response(
    query="What is AI?",
    state_variables={"context": context_str, "language": "English"},
    context_list=chunks
)
```

**After (v0.6):**

```python
result = await synthesizer.synthesize_response(
    query="What is AI?",
    context=context_str,  # Pass directly as kwargs
    language="English",   # Pass directly as kwargs
    context_list=chunks
)
```

## Reference Formatter

### Enforced Reference Chunks Simplification for Streaming

When streaming the references in GLLM Generation v0.5, the reference formatter supports two different event schemas:

1. Legacy schema (Kept as default for backward compatibility).

```json
{
    "type": "data",
    "value": '{"data_type": "reference", "value": "{\"id\": \"...\", \"content\": \"...\", \"metadata\": ...}"}',
    ...
}
```

2. New simplified schema (Achieved by setting the `simplify_events` parameter to `True`).

```json
{
    "type": "reference",
    "value": {"id": "...", "content": "...", "metadata": {...}},
    ...
}
```

In GLLM Generation v0.6, the reference formatter now strictly supports only the new simplified format. Thus, both the `simplify_events` parameter and the support for the legacy schema have been **removed**.

## Deep Researcher

### OpenAI Deep Researcher - Deprecated Parameters Removed

The following deprecated parameters have been **removed** from `OpenAIDeepResearcher`:

1. `mcp_servers` - Use `tools` parameter instead
2. `system_template` - Use `prompt_builder` parameter instead
3. `user_template` - Use `prompt_builder` parameter instead

**Migration Path:**

**Before (v0.5):**

```python
from gllm_generation.deep_researcher import OpenAIDeepResearcher
from gllm_inference.schema import NativeTool

researcher = OpenAIDeepResearcher(
    model_name="gpt-4o",
    api_key="your-api-key",
    mcp_servers=[NativeTool.web_search()],  # Deprecated
    system_template="You are a research assistant",  # Deprecated
    user_template="{query}"  # Deprecated
)
```

**After (v0.6):**

```python
from gllm_generation.deep_researcher import OpenAIDeepResearcher
from gllm_inference.schema import NativeTool
from gllm_inference.prompt_builder import PromptBuilder

# Use tools parameter instead of mcp_servers
researcher = OpenAIDeepResearcher(
    model_name="gpt-4o",
    api_key="your-api-key",
    tools=[NativeTool.web_search()],  # Use tools instead
    prompt_builder=PromptBuilder(
        system_template="You are a research assistant",
        user_template="{query}"
    )
)
```

**Note:** `code_interpreter` and `web_search` tools are automatically added if not provided.

## Component Base Classes

### `_run()` Method Removed

The deprecated `_run()` method has been **removed** from the following base classes:

1. `BaseCompressor`
2. `BaseContextEnricher`
3. `BaseRelevanceFilter`
4. `Repacker`

These classes now only use the `@main` decorated public methods.

If you were overriding `_run()` in custom implementations, you should now implement the abstract methods directly:

**Before (v0.5):**

```python
from gllm_generation.context_enricher import BaseContextEnricher

class MyEnricher(BaseContextEnricher):
    async def _run(self, **kwargs):
        chunks = kwargs["chunks"]
        return await self._enrich(chunks)
    
    async def _enrich(self, chunks):
        # Your enrichment logic
        return enriched_chunks
```

**After (v0.6):**

```python
from gllm_generation.context_enricher import BaseContextEnricher

class MyEnricher(BaseContextEnricher):
    async def _enrich(self, chunks):
        # Your enrichment logic
        # _enrich is now abstract and must be implemented
        return enriched_chunks
```

### Abstract Methods Now Enforced

The following methods are now **abstract** and must be implemented in subclasses:

* `BaseCompressor._compress()`
* `BaseContextEnricher._enrich()`
* `BaseRelevanceFilter._filter()`

**Before (v0.5):** These methods are not enforced in subclasses.

**After (v0.6):** These methods are decorated with `@abstractmethod` and will raise `TypeError` if not implemented.
