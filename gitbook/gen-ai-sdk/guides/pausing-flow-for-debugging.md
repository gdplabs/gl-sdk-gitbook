---
icon: bug
---

# Interrupting Flow for Debugging

This guide explains how to pause execution of your pipeline at a specific step using `pause()` and the `interrupt_before` / `interrupt_after` parameters to inspect the current state and debug issues.

<details>
<summary>Prerequisites</summary>

This example specifically requires you to complete all setup steps listed on the [prerequisites.md](../../gen-ai-sdk/prerequisites.md "mention").

You should be familiar with these concepts and components:

1. [Pipeline Orchestration](../tutorials/orchestration/pipeline.md)
2. [Steps](../tutorials/orchestration/steps/README.md)
</details>

## 1. Prepare Your Pipeline Setup

To set a static breakpoint for debugging, insert a `pause()` step at the point you want to inspect. A `PauseStep` is a named no-op marker — it does not pause execution by itself, but its name can be targeted by `interrupt_before` or `interrupt_after` at invocation time without recompiling the graph.

{% stepper %}
{% step %}
**Define your pipeline structure**

{% code lineNumbers="true" expandable="true" %}
```python
from typing import TypedDict

from gllm_core.schema import Component, main
from langgraph.checkpoint.memory import MemorySaver

from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import pause, step


class PipelineState(TypedDict, total=False):
    topic: str
    raw_data: str
    result: str


# Simple, self-contained Component classes for demonstration
class FetchDataComponent(Component):
    @main
    async def run(self, topic: str) -> str:
        return f"Fetched data for topic: {topic}"


class ProcessDataComponent(Component):
    @main
    async def run(self, raw_data: str) -> str:
        return f"Processed: {raw_data}"


memory = MemorySaver()

fetch_data = step(FetchDataComponent(), output_state="raw_data", input_map={"topic": "topic"}, name="fetch_data")
process = step(ProcessDataComponent(), output_state="result", input_map={"raw_data": "raw_data"}, name="process")

pipeline = Pipeline(
    steps=[
        fetch_data,
        # Named marker — activate it at invocation time via interrupt_before / interrupt_after
        pause(name="before_processing"),
        process,
    ],
    state_type=PipelineState,
    checkpointer=memory,
)
```
{% endcode %}
{% endstep %}
{% endstepper %}

## 2. Invoke with a Breakpoint

Pass `interrupt_before` or `interrupt_after` when invoking the pipeline to activate the breakpoint at the `PauseStep` you defined. You must also provide a `thread_id` so the pipeline can checkpoint and resume from the same state.

{% stepper %}
{% step %}
**Initialize the execution with a breakpoint**

```python
# Pause right before the "before_processing" marker step
state = await pipeline.invoke(
    initial_state={"topic": "AI Testing"},
    config={"thread_id": "debug-session-1"},
    interrupt_before=["before_processing"],
)

print(f"Pipeline paused. Current state: {state}")
```

{% hint style="info" %}
Use `interrupt_after=["before_processing"]` instead if you want to inspect the state **after** the marker step runs.
{% endhint %}
{% endstep %}
{% endstepper %}

## 3. Resume the Pipeline

Once paused, you can safely inspect variables, dump memory maps, or manually alter state values.

{% stepper %}
{% step %}
**Inspect and Resume**

To continue, invoke the pipeline again with the exact same `thread_id` and no `interrupt_before` / `interrupt_after`.

```python
result = await pipeline.invoke(
    initial_state=None,
    config={"thread_id": "debug-session-1"},
)

print(f"Final output: {result}")
```
{% endstep %}
{% endstepper %}

## Troubleshooting

### Issue: `ValueError: PauseStep is a no-op marker and cannot be cached.`

**Cause**: You attempted to initialize a `pause()` step with a `cache` argument. Since `PauseStep` is a pure marker with no runtime behaviour, it is incompatible with caching.  
**Solution**: Remove the `cache` argument from the `pause()` call.

### Issue: `ValueError: Pipeline caching is inherently incompatible with runtime interrupts.`

**Cause**: You passed `interrupt_before` or `interrupt_after` to `pipeline.invoke()` while the pipeline has caching enabled.  
**Solution**: Disable pipeline-level caching or remove the `interrupt_before` / `interrupt_after` parameters from `invoke()`.

## Next Steps

- Want to see how interruptions power production-grade workflows? Explore [Human-in-the-Loop Orchestration](human-in-the-loop.md).
