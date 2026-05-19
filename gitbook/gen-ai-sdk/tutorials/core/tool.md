---
icon: wrench
---

# Tool

## What is a Tool?

A `Tool` in GLLM Core is a **Model Context Protocol (MCP)–style callable** that an LLM agent can use to interact with the outside world.

Conceptually, a Tool is:

1. **Named**: identified by a `name` and optional `title`.
2. **Described**: has a human-readable `description` and optional `annotations`.
3. **Schema-first**: exposes structured `input_schema` and `output_schema`.
4. **Backed by a function**: optionally wraps a Python callable (`func`) that does the actual work.
5. **Async‑aware**: can wrap both synchronous and asynchronous functions, with a unified `invoke()` API.

In code, Tools live in `gllm_core.schema.tool.Tool` and are typically created via the `@tool` decorator.

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

```python
from gllm_core.schema import Tool, tool


@tool(description="Get weather information")
async def fetch_weather(location: str, units: str = "metric") -> dict:
    """Get weather information for a location.

    Arguments:
        location: City name or query string (e.g. `"Jakarta"`).
        units: Unit system, such as `"metric"` or `"imperial"`.
    """
    # Implementation goes here
    return {"temperature": 22.5, "conditions": "sunny"}


# After decoration, `fetch_weather` is a Tool instance
assert isinstance(fetch_weather, Tool)

# You can call it like a normal function
result = await fetch_weather("New York", "imperial")

# Or use the unified `invoke()` helper
result = await fetch_weather.invoke(location="Tokyo", units="metric")
```

This example shows the core ideas:

1. `@tool` wraps a function and returns a `Tool` instance.
2. The original call semantics are preserved (`fetch_weather(...)`).
3. `invoke()` provides a standard async entrypoint for agents and infrastructure.
4. Input and output schemata are derived from type hints and the docstring.

## The @tool Decorator

The `@tool` decorator converts a regular function into a `Tool`:

```python
from gllm_core.schema import tool


@tool(name="weather", title="Weather Tool")
async def fetch_weather(location: str, units: str = "metric") -> dict:
    ...
```

Key behaviors:

1. **Name resolution**
   * If `name` is passed, it becomes the Tool identifier.
   * Otherwise, the function’s `__name__` is used.
2. **Description resolution**
   * If `description` is passed, it is used directly.
   * Otherwise, the function docstring is cleaned and used.
   * Parameter docs inside a Google‑style `Arguments:` section are parsed and attached to individual fields in the input schema.
3. **Title resolution**
   * `title` is optional display text for UI clients.
   * If omitted, consumers can fall back to the `name` or annotations.

Internally, `@tool`:

1. Inspects the function signature via `inspect.signature`.
2. Collects type hints with `typing.get_type_hints`.
3. Builds a Pydantic input model using `_build_field_definitions`.
4. Builds an optional Pydantic output model from the return type (if not `-> None`).
5. Constructs a `Tool` instance with these schemata and the function implementation.
6. Copies key metadata (`__name__`, `__qualname__`, `__module__`, `__doc__`, `__wrapped__`) onto the Tool instance so it still behaves like a function for introspection and IDEs.

## Input and Output Schemata

Every Tool carries two schema fields:

1. `input_schema`
2. `output_schema`

These fields can be **either**:

1. JSON Schema–style dictionaries, or
2. Pydantic `BaseModel` subclasses.

The `Tool` validators normalize them:

1. If a Pydantic model class is provided, `model_json_schema()` is called and the internal value becomes a **JSON Schema dict**.
2. If a dict is provided, it is used as-is.
3. For `output_schema`, `None` is also allowed to represent “no structured output”.

When you use `@tool`:

1. An input model named `<func_name>_input` is created with one field per parameter (excluding `*args` / `**kwargs`).
2. An output model named `<func_name>_output` is created with a single `result` field if the function has a non-`None` return type.

Example:

```python
@tool
async def add(a: int, b: int) -> int:
    """Add two integers.

    Arguments:
        a: First addend.
        b: Second addend.
    """
    return a + b


add.input_schema   # JSON schema derived from a Pydantic model
add.output_schema  # JSON schema with a `result: int` field
```

These schemata are crucial for MCP clients and LLM agents:

1. They define what arguments are allowed/required.
2. They define what structure the result will have.
3. They enable automatic validation, form building, and documentation.

## Calling a Tool

The `Tool` class supports two primary ways to execute its underlying function.

Direct call:

```python
result = await add(1, 2)
```

1. If the underlying `func` is async, this returns a coroutine and you `await` it.
2. If `func` is sync, it returns the result directly (no coroutine).

Standardized `invoke` call:

```python
result = await add.invoke(a=1, b=2)
```

1. Works uniformly for both sync and async implementations.
2. For async functions, `invoke` simply awaits the function.
3. For sync functions, `invoke` runs the function in a thread executor using the current event loop.
4. Logs both the invocation parameters and the result via the Tool’s logger.

`invoke` is the preferred surface for **agents and orchestration code**, because it:

1. Is always async.
2. Accepts keyword arguments that are expected to match `input_schema`.
3. Provides consistent logging and error handling.

## LangChain and Google ADK Adapters

The `Tool` class provides two constructors for external ecosystems:

1. `Tool.from_langchain(langchain_tool)`
2. `Tool.from_google_adk(function_declaration, func=None)`

These are thin wrappers around adapter functions in `gllm_core.adapters.tool`:

1. `from_langchain_tool()`
2. `from_google_function()`

Typical usage:

```python
from gllm_core.schema import Tool


lc_tool = ...  # Some LangChain tool
mcp_tool = Tool.from_langchain(lc_tool)


google_decl = ...  # Google ADK function declaration
mcp_tool_2 = Tool.from_google_adk(google_decl)
```

The adapters are responsible for:

1. Validating that external definitions have a valid name/description/schema.
2. Translating their argument specifications into JSON Schema.
3. Creating a `Tool` instance that looks the same as those built via `@tool`.

This keeps your internal agent and MCP tooling code **agnostic** to whether a Tool came from:

1. A local Python function via `@tool`.
2. A LangChain Tool object.
3. A Google ADK function declaration.

## Logging and Error Handling

Each `Tool` instance exposes a private `_logger` property:

1. Uses `logging.getLogger` with the fully-qualified class path.
2. Applies a class-level `_log_level` (default `DEBUG`).

`invoke()` uses this logger to:

1. Log debug information before execution (`Invoking tool 'name' with params: ...`).
2. Log the result after successful completion.
3. Log errors if the underlying function raises, then re-raise the exception.

Typical failure modes:

1. **Missing implementation**: if `func` is `None`, both `__call__` and `invoke` raise `ValueError` indicating the Tool has no implementation.
2. **Type mismatches**: upstream validation is expected to be done using the tool’s JSON Schema; incorrect arguments passed directly to `invoke` may result in `TypeError` or domain-specific errors from the function body.

This pattern keeps Tools **transparent to debuggers and logs**, while still letting you treat them as simple callables.

## Designing Good Tools

Some practical guidelines when authoring tools with `@tool`:

1. **Type everything**
   * Add full type hints to all parameters and the return value.
   * This ensures accurate schemata for agents and UIs.
2. **Write Google-style docstrings**
   * Use an `Arguments:` section so `_extract_param_doc` can attach descriptions to individual fields.
   * Keep parameter descriptions concise and action-oriented.
3. **Avoid `*args` and `**kwargs`** in Tool interfaces
   * They are ignored when building the input schema.
   * Prefer explicit, named parameters for clarity.
4. **Return structured data**
   * Use dicts or Pydantic models for results; avoid unstructured strings when possible.
   * This makes it easier for agents to reason about outputs.
5. **Keep side effects clear**
   * Tools are typically small, focused operations with a clear purpose.
   * Document external side effects (e.g., network calls, file writes) in the description.

By following these guidelines, your Tools will be:

1. Easier for LLM agents to understand and call correctly.
2. More interoperable across MCP-compatible runtimes.
3. Simpler to adapt from or into other ecosystems like LangChain or Google ADK.
