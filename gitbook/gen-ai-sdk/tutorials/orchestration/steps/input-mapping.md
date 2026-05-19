---
icon: eye-dropper
---

# Input Mapping

Input mapping in `gllm_pipeline` allows you to control how data flows from the pipeline state and runtime configuration into your components.

## Input sources

When you create some steps, you need to specify how data flows from the pipeline into your component.

There are three main sources of data:

1. **Pipeline State**: Data that flows through the pipeline from step to step. This is **mutable**.
2. **Runtime Configuration**: Settings that can only be changed at runtime. This is **immutable**.
3. **Fixed Values**: Constants that never change. This is also **immutable**.

## Using input\_map


The `input_map` is an argument that can be passed into some steps to define where they get their inputs from. It is the dictionary, where:

* **Keys** are component argument names.
* **Values** can be:
  * **Strings**: State/config keys (tries state first, then config).
  * **Val objects**: Fixed/literal value.

Let's see how `input_map` works when you actually invoke a pipeline. This example shows the complete flow from pipeline creation to execution:

```python
from gllm_pipeline.steps import ComponentStep
from gllm_pipeline.types import Val
from gllm_core.schema.component import Component
from typing import Any

class AdvancedProcessor(Component):
    """A component that processes text with various parameters."""

    async def _run(self, **kwargs: Any) -> Any:
        text = kwargs["text"]
        max_length = kwargs["max_length"]
        prefix = kwargs["prefix"]
        suffix = kwargs["suffix"]

        processed = f"{prefix}{text[:max_length]}{suffix}"
        return {"processed_text": processed, "original_length": len(text)}

# Create step with mixed input_map
processor_step = step(
    AdvancedProcessor(),
    input_map={
        "text": "user_input",           # From state
        "max_length": "config_max_len", # From config
        "prefix": Val(">>> "),          # Fixed value
        "suffix": Val(" <<<")           # Fixed value
    },
    output_state=["processed_text", "original_length"]  # Multiple outputs
)

# Create pipeline
pipeline = Pipeline(steps=[processor_step])

# Invoke with state and config
result = await pipeline.invoke(
    initial_state={"user_input": "This is a very long text that will be truncated"},
    config={"configurable": {"config_max_len": 20}}
)

print(result)
# Output: {
#   "user_input": "This is a very long text that will be truncated",
#   "processed_text": ">>> This is a very long <<<",
#   "original_length": 50
# }
```

For better ergonomics, `input_map` also accepts a list format. This is particularly useful for **Identity Mapping**, where the component argument name matches the state/config key.

```python
# List form with mixed mappings
echo_step = step(
    Echo(),
    input_map=[
        "x",                           # Identity mapping: component `x` gets state/config `x`
        {"y": "user_input"},           # State mapping: component `y` gets state `user_input`
        {"z": Val("Fixed")}            # Fixed value: component `z` gets "Fixed"
    ],
    output_state="echoed_value"
)
```

Identity mapping (passing a string directly in the list) simplifies common cases where your state keys already match your component's parameter names.

{% hint style="info" %}
**Migrated from v0.4**: The legacy parameters `input_state_map`, `runtime_config_map`, and `fixed_args` have been removed in v0.5.0. Use `input_map` with `Val()` for all input mapping needs. See the [migration guide](../migration-guide/gllm-pipeline-v0.4-to-v0.5.md) for details.
{% endhint %}
