---
icon: arrow-progress
---

# GLLM Core v0.3 to v0.4

## Adding Custom Components

### Overview

The `Component` API now supports an explicit main entrypoint via the `@main` decorator, with a resolver that determines which method to execute when calling `run()`. The legacy `_run` method remains supported as a fallback but is deprecated.

Resolution precedence for the main entrypoint:

1. Most derived method decorated with `@main`.
2. Method named by the `__main_method__` class property.
3. Legacy `_run` method (deprecated fallback).

The input-parameter model (`input_params`) is generated from the resolved main method signature for the class.

### Defining the main method (new)

1. Decorate an async instance method with `@main`.
2. Only one `@main` method per class is allowed.
3. If multiple ancestors define different `@main` methods, a `TypeError` is raised unless the subclass explicitly overrides with its own `@main`.
4. The `__main_method__` class property is still supported but has lower precedence than `@main`. If both are present, a warning is logged and the decorator takes precedence.
5. The main method must be asynchronous.

Example:

```python
import logging
from gllm_core.schema.component import Component, main

class MyComponent(Component):
    _default_log_level = logging.INFO

    @main
    async def execute(self, text: str) -> str:
        return text.upper()
```

### Migrating from the old Component

If your component previously implemented `_run`, you should migrate to the new `@main` decorator pattern.

#### **Recommended: Direct Migration (Remove `_run`)**

Rename `_run` to a meaningful method name and apply `@main`:

```python
from gllm_core.schema.component import Component, main

class MyComponent(Component):
    @main
    async def execute(self, text: str) -> str:
        """Process the input text."""
        return text.upper()
```

**Benefits:**

1. Full compatibility with `as_tool()` for LLM tool conversion
2. Clean, explicit signature for `input_params` validation
3. Future-proof (follows framework intent)

**Breaking Changes:**

1. Any code directly calling `_run()` must be updated to call the new method or use `run()`
2. If used in a `Pipeline`, the `run_profile` may be inconsistent until the framework is updated (see note below)

**Pipeline Note:** As of GLLM Pipeline v0.4.28, the `run_profile` implementation which analyzes `_run` for static input validation is still used. If you rely heavily on `Pipeline` and encounter input routing issues, you may need to temporarily keep `_run` as a stub or override `_analyze_run_method()` until the core framework is updated.

#### **Alternative: Preserve Validation/Adapter Logic**

If your `_run` method contains important validation or acts as an adapter (e.g., extracting specific keys from `**kwargs`), use this pattern:

```python
from gllm_core.schema.component import Component, main
from gllm_core.schema import Chunk

class MyChunkProcessor(Component):
    @main
    async def execute(self, chunks: list[Chunk]) -> list[Chunk]:
        """Execute chunk processing with validation."""
        # Move validation from _run to here
        if not isinstance(chunks, list) or not all(isinstance(c, Chunk) for c in chunks):
            raise ValueError("chunks must be a list[Chunk]")

        return await self.process_chunks(chunks)

    async def process_chunks(self, chunks: list[Chunk]) -> list[Chunk]:
        """Process the chunks (implement in subclass)."""
        raise NotImplementedError

    # Optional: Keep _run temporarily for backwards compatibility
    async def _run(self, **kwargs):
        """Deprecated: Use execute() instead."""
        return await self.execute(**kwargs)
```

**Benefits:**

* Preserves validation logic at the entry point
* Maintains clean separation between validation and business logic
* Full compatibility with `as_tool()` and `input_params`

**Trade-offs:**

* Requires more refactoring than direct migration
* Need to update subclasses if they override `_run`

**Avoid: Decorating `_run` with `@main`**

Do **not** simply add `@main` to your existing `_run` method:

```python
# ❌ DON'T DO THIS
class MyComponent(Component):
    @main
    async def _run(self, text: str) -> str:
        return text.upper()
```

Why this breaks:

* `as_tool()` explicitly rejects `_run` as the main method (raises `RuntimeError`)
* Keeps the deprecated method name, defeating the purpose of migration
* Not future-proof when `_run` is eventually removed

#### Backward compatibility (non-migrated components)

* Components that only implement `_run` continue to work. The resolver falls back to `_run` and logs a deprecation warning recommending the `@main` decorator.
* `input_params` continues to be generated from `_run` in this case, so existing pipelines keep working.
* If both `@main` and `__main_method__` are defined, a warning is emitted and the decorator wins.

#### Multiple inheritance considerations

* If two different ancestors define different `@main` methods and the subclass does not explicitly override them, a `TypeError` is raised at resolution time.
* To resolve, explicitly define a `@main` method in the subclass to choose the desired entrypoint.

Example resolution:

```python
class A(Component):
    @main
    async def a(self): ...

class B(Component):
    @main
    async def b(self): ...

class C(A, B):
    @main
    async def choose(self): ...  # Explicit override resolves the conflict
```

### Troubleshooting

1. TypeError: "Main method '...' must be asynchronous" — ensure the method decorated with `@main` is `async def`.
2. TypeError: "Multiple main methods defined in X" — only one `@main` per class is allowed.
3. TypeError about conflicting main methods across ancestors — add a `@main` method in the subclass to explicitly resolve.

### Notes and best practices

1. Prefer an async instance method for the main entrypoint. Avoid using `@staticmethod` or `@classmethod` with `@main`.
2. Keep the main method signature representative of the inputs you expect; `input_params` will be generated from it.
3. You do not need to document `run_profile` or `input_params` in your component’s docstring; these are derived and consumed by the pipeline.

## Event Handling

A few adjustments have been made to streamline event handling, both to the `EventEmitter` as well as the `Event` schema itself.

### Event Emitter Parameter Update

The `EventEmitter`'s `emit()` method will now only accept actual `Event` objects as arguments. Passing plain strings directly to the `emit()` method is no longer supported.&#x20;

**GLLM Core v0.3:**

```python
text = "Hello, world!"
await event_emitter.emit(value=text)
```

**GLLM Core v0.4:**

```python
text = "Hello, world!"
await event_emitter.emit(Event(value=text))
```

### Event Schema Attributes Update

The `value` attribute of the `Event` schema now supports the following types:

1. `str` for plain texts.
2. `dict[str, Any]` for structured values.
3. `bytes` for multimodal values.

To accommodate this, a new attribute called `value_type` has also been added to help conveying a more specific information about the value type of an `Event`. This attribute is optional. When not defined, it will be derived automatically based on the `value` attribute:

```python
text_event = Event(value="Hi!")  # derived value_type=EventValueType.TEXT
dict_event = Event(value={"key": "value"})  # derived value_type=EventValueType.JSON
bytes_event = Event(value=b"...")  # derived value_type=EventValueType.BYTES
```

We can customize the `value_type` when we want to assign a more specific value type to the event, such as when we want to differentiate the modality type between events with `bytes` values:

```python
audio_event = Event(value=b"...", value_type=EventValueType.AUDIO)
image_event = Event(value=b"...", value_type=EventValueType.IMAGE)
```

### Emitted Event Format Simplification

Native supports for legacy emitted event format that utilizes the `data` event type is removed. As a result, some adjustments are made to the event-related modules:

1. The `data` event type is removed from the `EventType` constant.&#x20;
2. Special handling of the `data` event type across event handlers are removed.&#x20;

For an example of the comparison between the legacy format from GLLM Core v0.3 and the new simplified format, please refer to the `thinking` event below:

**GLLM Core v0.3 (Legacy Format):**

```json
{
    "type": "data",
    "value": '{"data_type": "thinking", "value": "I'm thinking!"}',
    ...
}
```

**GLLM Core v0.4 (Simplified Format):**

```json
{
    "type": "thinking",
    "value": "I'm thinking!",
    ...
}
```

## Disabling Timeout with Retry Config

When defining a `RetryConfig` object, setting the `timeout` attribute to `0.0` will previously cause the timeout to be disabled. Now, setting it to `0.0` will raise an error. Instead, set it to `None` to disable timeout.

**Disabling Timeout Example (v0.3) — Will Raise Error in v0.4**

```python
from gllm_core.utils import RetryConfig

retry_config = RetryConfig(timeout=0.0)
```

**Disabling Timeout Example (v0.4)**

```python
from gllm_core.utils import RetryConfig

retry_config = RetryConfig(timeout=None)
```
