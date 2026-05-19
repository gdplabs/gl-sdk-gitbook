---
icon: arrows-rotate
---

# Dynamic Component

## What is a Dynamic Component?

A `DynamicComponent` is a runtime wrapper that instantiates an inner `Component` using invocation-time arguments.

Use it when constructor values are only known at runtime, for example:

1. Selecting a model or tenant at request time.
2. Building one component interface that supports multiple runtime configs.
3. Separating constructor config from execution input.

`DynamicComponent` works with `Lazy` bindings to resolve constructor arguments from runtime kwargs or resolver functions.

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
from gllm_core.schema import Component, DynamicComponent, Lazy, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str, tone: str = "casual") -> str:
        return f"{self.prefix} {name}! [model={self.model_id}, tone={tone}]"


dynamic_greeter = DynamicComponent(
    component_class=GreetingComponent,
    init_kwargs={
        "prefix": "Hello",
        "model_id": Lazy.from_runtime("model_id"),
    },
)

result = await dynamic_greeter.run(
    model_id="openai/gpt-4.1-nano",   # consumed by constructor binding
    name="John Doe",                  # passed to @main method
    tone="formal",                    # passed to @main method
)
print(result)
```

## Lazy Binding Modes

`Lazy` supports three binding modes for constructor parameters.

### 1. Runtime Binding (`Lazy.from_runtime`)

Read a constructor value directly from runtime kwargs.

```python
Lazy.from_runtime("model_id")  # reads runtime kwarg "model_id" into constructor param
```

### 2. Sync Resolver (`Lazy.resolver`)

Compute constructor values from runtime kwargs using a sync function.

```python
def resolve_base_url(model_id: str) -> str:
    provider = model_id.split("/", 1)[0]
    return f"https://{provider}.example.com/v1"

base_url_binding = Lazy.resolver(resolve_base_url, arg_name="model_id")
```

### 3. Async Resolver (`Lazy.async_resolver`)

Resolve constructor values with async-capable functions.

```python
async def load_api_key(model_id: str) -> str:
    provider = model_id.split("/", 1)[0]
    return f"key-{provider}"

api_key_binding = Lazy.async_resolver(load_api_key, arg_name="model_id")
```

## Using `Component.to_dynamic()`

You can create the same wrapper directly from your component class:

```python
from gllm_core.schema import Component, Lazy, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str, tone: str = "casual") -> str:
        return f"{self.prefix} {name}! [model={self.model_id}, tone={tone}]"


dynamic_greeter = GreetingComponent.to_dynamic(
    init_kwargs={
        "prefix": "Hi",
        "model_id": Lazy.from_runtime("model_id"),
    },
)

result = await dynamic_greeter.run(
    model_id="openai/gpt-4.1-nano",
    name="Alya",
    tone="friendly",
)
```

## Instance Caching

When `cache_instances=True`, the wrapper reuses inner component instances for identical resolved constructor kwargs.

```python
from gllm_core.schema import DynamicComponent, Lazy
from gllm_core.schema import Component, main


class GreetingComponent(Component):
    def __init__(self, prefix: str, model_id: str) -> None:
        self.prefix = prefix
        self.model_id = model_id

    @main
    async def greet(self, name: str) -> str:
        return f"{self.prefix} {name} [{self.model_id}]"


cached_greeter = DynamicComponent(
    component_class=GreetingComponent,
    init_kwargs={"prefix": "Hello", "model_id": Lazy.from_runtime("model_id")},
    cache_instances=True,
    cache_size=256,
)
```

Notes:

1. Equal resolved init kwargs map to the same cached instance.
2. Different kwargs produce different instances.
3. If kwargs cannot be safely canonicalized, caching is skipped for that call.

## Error Behavior

Common failure cases:

1. Missing required runtime key for `Lazy.from_runtime(...)` or resolver args raises `ValueError`.
2. Invalid `component_class` (not a concrete `Component` subtype) raises `TypeError`.
3. Invalid `Lazy.resolver(...)` or `Lazy.async_resolver(...)` inputs raise `TypeError`.

## When to Use Dynamic Component

Use `DynamicComponent` when:

1. Constructor configuration depends on request context.
2. You want one runtime entrypoint that can build different inner component instances.
3. You need optional reuse of constructed instances via cache.

Use a regular `Component` when constructor values are static for the lifetime of the object.
