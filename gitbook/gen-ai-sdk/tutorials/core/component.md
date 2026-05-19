---
icon: puzzle
---

# Component

## What's a Component?

A `Component` is the **basic executable unit** in GLLM Core. It wraps a piece of async business logic and standardizes how that logic is:

1. **Discovered** via a single async entrypoint (`@main` or fallbacks).
2. **Executed** through a uniform `run(**kwargs)` method.
3. **Observed** via structured input/output events.
4. **Analyzed** so pipelines and orchestrators can understand its input contract.

At a high level:

1. **You implement a subclass** of `Component`.
2. **You mark one async method with `@main`** to declare the entrypoint.
3. **Pipelines never call your method directly**. They call `component.run(**kwargs)`.
4. **Input schemas can be generated** from the `@main` signature, enabling validation and argument construction.

This gives GLLM Core a **uniform abstraction** over heterogeneous logic: pipelines don't need to know whether a component is talking to an LLM, a database, an API, or anything else.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-core"
```
{% endtab %}
{% endtabs %}

## Quickstart

### Define Your First Component

```python
from gllm_core.schema import Component, main


class TextFormatter(Component):
    @main
    async def format(self, text: str, uppercase: bool = False, repeat: int = 1) -> str:
        """Format text with options."""
        result = text.upper() if uppercase else text
        return result * repeat
```

Key points:

1. **Subclass** `Component`.
2. Define a single **async** method (here `format`).
3. Mark it with `@main` to tell the system: _"this is the entrypoint"_.

### Execute the Component Uniformly

```python
formatter = TextFormatter()

result = await formatter.run(text="hello", uppercase=True, repeat=2)
assert result == "HELLOHELLO"
```

You **never** call `await formatter.format(...)` from orchestration code. Instead, you always call `await formatter.run(**kwargs)`:

1. The Component base class emits **start/finish events**.
2. Logging is performed via the component's `_logger`.
3. Pipelines can treat every component the same way.

### Use the Generated Input Schema

The design for Components includes an `input_params` property that exposes a **Pydantic model** mirroring the `@main` signature:

```python
formatter = TextFormatter()
ParamsModel = formatter.input_params  # type: ignore[attr-defined]

params = ParamsModel(text="world", repeat=2)
result = await formatter.run(**params.model_dump())
```

This gives you:

1. Type-checked construction of arguments.
2. Easy validation and error reporting.
3. A single source of truth: the `@main` signature.

## The `@main` Decorator

The `@main` decorator marks **one async method** on a `Component` subclass as the canonical entrypoint. Architecturally, it enables:

1. **Entry-point abstraction**: pipelines don't need to know method names.
2. **Schema generation**: the `@main` signature drives `input_params`.
3. **Future interoperability**: the same entrypoint can later be wrapped as an MCP-compliant `Tool`.

From the docs and specs:

1. `Component.get_main()` resolves the entrypoint by honoring `@main`, `__main_method__`, or falling back to `_run`.
2. `Component.input_params` generates a Pydantic model from the resolved main method.
3. `Component.run(**kwargs)` executes the resolved main coroutine and emits events.

### `@main` Method Resolution

The entrypoint resolution is conceptually:

1. **Prefer an explicitly decorated `@main` method** on the subclass.
2. If none is decorated, look for a class-level `__main_method__` override.
3. As a compatibility fallback, use `_run`.

This resolution is cached (via a resolver such as `MainMethodResolver`) so the cost of introspection is paid once per class.

### Using `@main` with Abstract Classes

The `@main` decorator works seamlessly with abstract base classes, allowing you to define a common entrypoint signature that subclasses can implement. This is particularly useful when building component hierarchies with shared interfaces.

**Example: Abstract Base Component**

```python
from abc import ABC, abstractmethod
from gllm_core.schema import Component, main


class BaseProcessor(Component, ABC):
    """Abstract processor with a defined entrypoint."""

    @main
    @abstractmethod
    async def process(self, data: str) -> str:
        """Process data - must be implemented by subclasses."""
        pass


class UpperCaseProcessor(BaseProcessor):
    """Converts text to uppercase."""

    async def process(self, data: str) -> str:
        return data.upper()


class LowerCaseProcessor(BaseProcessor):
    """Converts text to lowercase."""

    async def process(self, data: str) -> str:
        return data.lower()
```

**Key behaviors:**

1. **The `@main` decorator is inherited**: Both `UpperCaseProcessor` and `LowerCaseProcessor` inherit the `@main` marking from `BaseProcessor.process`.
2. **Subclasses implement the abstract method**: Each subclass provides its own implementation of `process`.
3. **Uniform execution**: All subclasses can be executed via `run(**kwargs)`:

```python
upper = UpperCaseProcessor()
lower = LowerCaseProcessor()

result1 = await upper.run(data="hello")  # Returns "HELLO"
result2 = await lower.run(data="WORLD")  # Returns "world"
```

4. **Shared input schema**: Both subclasses generate the same `input_params` model based on the abstract signature:

```python
# Both have the same parameter structure
assert upper.input_params.model_fields.keys() == lower.input_params.model_fields.keys()
```

#### **Example: Overriding `@main` in Subclasses**

If a subclass needs a different entrypoint, it can define its own `@main` method:

```python
class AdvancedProcessor(BaseProcessor):
    """Processor with additional parameters."""

    async def process(self, data: str) -> str:
        # This implements the abstract method
        return self._transform(data)

    @main
    async def transform(self, data: str, mode: str = "upper") -> str:
        """Transform with configurable mode."""
        if mode == "upper":
            return data.upper()
        elif mode == "lower":
            return data.lower()
        else:
            return data

    def _transform(self, data: str) -> str:
        return data.upper()


# The subclass uses its own @main method
processor = AdvancedProcessor()
result = await processor.run(data="hello", mode="lower")  # Returns "hello"

# The input_params reflects the new signature
ParamsModel = processor.input_params
assert "mode" in ParamsModel.model_fields
```

Important notes:

1. **Most derived `@main` wins**: When a subclass defines its own `@main` method, it takes precedence over inherited `@main` methods.
2. **Abstract methods must still be implemented**: Even if you override `@main`, you must implement all abstract methods from the parent class.
3. **Schema generation uses the resolved main**: The `input_params` property always reflects the signature of the resolved `@main` method, not the abstract one.

## Component Lifecycle and Runtime Behavior

The `Component` base class provides a logger and a standard event flow:

1. `run(**kwargs)`
   1. Formats an **input event** with the component name and arguments.
   2. Logs it via `_logger`.
   3. Optionally emits it through an `EventEmitter` if one is passed in `kwargs`.
2. Calls the resolved main coroutine (or `_run` in the current implementation).
3. Formats and logs an **output event** containing the result.

Binary payloads (e.g., `bytes`) are handled via `binary_handler_factory` so logs show sizes or summaries instead of raw bytes.

## Designing Good Component APIs

### Prefer Clear, Typed Parameters

When defining your `@main` method:

1. Use **explicit type hints** for all parameters.
2. Provide **sensible defaults** where appropriate.
3. Reserve `**kwargs` for truly open-ended options.

Example:

```python
class DataProcessor(Component):
    @main
    async def process(
        self,
        data: list[dict],
        limit: int = 100,
        **options,
    ) -> dict:
        """Process data with optional filters."""
        processed = data[:limit]
        return {
            "count": len(processed),
            "data": processed,
            "options": options,
        }
```

With the planned `input_params` behavior, this will:

1. Generate a `DataProcessorParams` model.
2. Enforce types for `data` and `limit`.
3. Allow extra fields (because of `**options`) via `extra="allow"`.

### When to Use `**kwargs`

Use `**kwargs` when:

1. You truly don't know all the options ahead of time.
2. You want to **forward arbitrary parameters** to downstream systems.

Avoid it when:

1. You can name and type your parameters precisely.
2. You want strict validation and clear API docs.

***

## Backwards Compatibility with Legacy `_run` Components

If you have existing components that only implement `_run`, they continue to work:

```python
class LegacyComponent(Component):
    async def _run(self, message: str, priority: int = 1) -> str:
        """Legacy component using _run."""
        return f"[P{priority}] {message}"
```

See [#migrating-from-the-old-component](migration-guide/gllm-core-v0.3-to-v0.4.md#migrating-from-the-old-component "mention") for a guide to move from the old `_run`-style Components to the newer one.
