---
icon: bug
---

# Debugging a Pipeline


This guide will show you how to debug a pipeline by inspecting intermediate step outputs, tracing execution in real time, and navigating through the history of past pipeline runs. These built-in observability features are designed for development-time troubleshooting and production monitoring without requiring changes to your pipeline logic.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [basic-concepts.md](basic-concepts.md "mention") of orchestration components
2. [state.md](state.md "mention")
3. [steps](steps/ "mention")
4. [pipeline.md](pipeline.md "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-pipeline"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-pipeline"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "gllm-pipeline"
```
{% endtab %}
{% endtabs %}

## Debug Tracing

You can enable **per-node console tracing** to get a real-time, plain-text summary of every step executed during `invoke()`. Each trace line shows the node name, a truncated state snapshot before and after execution, and the wall-clock duration in milliseconds.

{% stepper %}
{% step %}
**Define state and steps**

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

class DebugState(TypedDict):
    text: str
    text_upper: str
    text_len: int

def to_upper(data: dict) -> str:
    return data["text"].upper()

def count_chars(data: dict) -> int:
    return len(data["text_upper"])
```
{% endcode %}
{% endstep %}

{% step %}
**Build the pipeline and enable tracing**

{% code lineNumbers="true" expandable="true" %}
```python
pipeline = Pipeline(
    steps=[
        transform(to_upper, input_map=["text"], output_state="text_upper", name="to_upper"),
        transform(count_chars, input_map=["text_upper"], output_state="text_len", name="count_chars"),
    ],
    state_type=DebugState,
)

# Enable tracing — all subsequent invoke() calls will emit traces
pipeline.enable_debug_tracing()
```
{% endcode %}
{% endstep %}

{% step %}
**Invoke and observe output**

{% code lineNumbers="true" expandable="true" %}
```python
result = asyncio.run(
    pipeline.invoke({"text": "hello world", "text_upper": "", "text_len": 0})
)
print(result)
```
{% endcode %}
{% endstep %}
{% endstepper %}

After invoking the pipeline, you should see per-node trace output on stdout:

```
[to_upper] state_before={'text': 'hello world', ...} state_after={'text_upper': 'HELLO WORLD'} duration=1ms
[count_chars] state_before={..., 'text_upper': 'HELLO WORLD', ...} state_after={'text_len': 11} duration=0ms
{'text': 'hello world', 'text_upper': 'HELLO WORLD', 'text_len': 11}
```

To disable tracing for subsequent calls, use `disable_debug_tracing()`:

{% code lineNumbers="true" expandable="true" %}
```python
pipeline.disable_debug_tracing()

result = asyncio.run(
    pipeline.invoke({"text": "silent run", "text_upper": "", "text_len": 0})
)
# No trace output this time
```
{% endcode %}

{% hint style="info" %}
**OpenTelemetry Compatibility**: Debug tracing is fully compatible with existing `gl-observability` OpenTelemetry traces. Enabling console tracing does **not** affect, replace, or conflict with any OTel spans already being emitted.
{% endhint %}

### Combining with Debug State

You can use `enable_debug_tracing()` together with the `debug_state` config flag. When combined, you get both real-time console output **and** the full `__state_logs__` in the returned state.

{% code lineNumbers="true" expandable="true" %}
```python
pipeline.enable_debug_tracing()

result = asyncio.run(
    pipeline.invoke(
        {"text": "combined debug", "text_upper": "", "text_len": 0},
        config={"debug_state": True},
    )
)

# Console output: per-node trace lines appear on stdout
# Return value: result["__state_logs__"] contains full debug events
print(result["__state_logs__"])
```
{% endcode %}

## Capturing Step Outputs

By default, `invoke()` returns only the final merged state. Use the `include_outputs_from` parameter to capture the **individual output** produced by specific steps, without modifying the pipeline definition.

{% stepper %}
{% step %}
**Define state and steps**

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

class OutputState(TypedDict):
    text: str
    text_upper: str
    text_len: int

def to_upper(data: dict) -> str:
    return data["text"].upper()

def count_chars(data: dict) -> int:
    return len(data["text_upper"])
```
{% endcode %}
{% endstep %}

{% step %}
**Build the pipeline**

{% code lineNumbers="true" expandable="true" %}
```python
pipeline = Pipeline(
    steps=[
        transform(to_upper, input_map=["text"], output_state="text_upper", name="to_upper"),
        transform(count_chars, input_map=["text_upper"], output_state="text_len", name="count_chars"),
    ],
    state_type=OutputState,
)
```
{% endcode %}
{% endstep %}

{% step %}
**Invoke with `include_outputs_from`**

{% code lineNumbers="true" expandable="true" %}
```python
result = asyncio.run(
    pipeline.invoke(
        {"text": "hello world", "text_upper": "", "text_len": 0},
        include_outputs_from={"to_upper", "count_chars"},
    )
)

# Access individual step outputs under the "__step_outputs__" key
print(result["__step_outputs__"]["to_upper"])    # [{'text_upper': 'HELLO WORLD'}]
print(result["__step_outputs__"]["count_chars"]) # [{'text_len': 11}]
```
{% endcode %}
{% endstep %}
{% endstepper %}

Each entry in `__step_outputs__` is a **list** of state-update dicts produced by that node. For steps that execute once, the list contains a single item. For steps that loop (e.g., via `Command(goto=...)`), the list captures every iteration in order.

{% hint style="warning" %}
**Validation**: Passing an unknown node name to `include_outputs_from` raises a `KeyError`. The reserved key `__step_outputs__` must not appear in the initial state when using this feature.
{% endhint %}


### Extracting Outputs from Subgraphs

You can also capture the aggregated output of a subgraph node:

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio
from typing import TypedDict

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform


class SubState(TypedDict):
    text: str
    text_upper: str
    text_len: int


def to_upper(data: dict) -> str:
    return data["text"].upper()


def count_chars(data: dict) -> int:
    return len(data["text_upper"])


# Build a sub-pipeline (will become a subgraph node named "sub_pipeline")
sub_pipeline = Pipeline(
    steps=[transform(to_upper, input_map=["text"], output_state="text_upper", name="to_upper")],
    state_type=SubState,
    name="sub_pipeline",
)

# Compose: sub_pipeline >> main_step
main_step = transform(count_chars, input_map=["text_upper"], output_state="text_len", name="count_chars")
pipeline = sub_pipeline >> main_step

result = asyncio.run(
    pipeline.invoke(
        {"text": "hello", "text_upper": "", "text_len": 0},
        include_outputs_from={"sub_pipeline"},
    )
)

# Subgraph output is captured as the full state at the subgraph boundary
print(result["__step_outputs__"]["sub_pipeline"])
# [{'text': 'hello', 'text_upper': 'HELLO', 'text_len': 0}]
```
{% endcode %}

## State History

You can retrieve the full history of checkpointed states for a given thread using `get_state_history()`. This enables **time-travel debugging** — iterating backwards through every intermediate state saved during pipeline execution.

{% stepper %}
{% step %}
**Define state and steps**

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

class HistoryState(TypedDict):
    text: str
    text_upper: str

def to_upper(data: dict) -> str:
    return data["text"].upper()
```
{% endcode %}
{% endstep %}

{% step %}
**Build the pipeline with a checkpointer**

{% code lineNumbers="true" expandable="true" %}
```python
pipeline = Pipeline(
    steps=[transform(to_upper, input_map=["text"], output_state="text_upper", name="to_upper")],
    state_type=HistoryState,
    checkpointer=InMemorySaver(),
)
```
{% endcode %}
{% endstep %}

{% step %}
**Run the pipeline and retrieve history**

{% code lineNumbers="true" expandable="true" %}
```python
async def main():
    # Run the pipeline twice on the same thread
    await pipeline.invoke({"text": "hello", "text_upper": ""}, thread_id="thread-1")
    await pipeline.invoke({"text": "world", "text_upper": ""}, thread_id="thread-1")

    # Iterate through all checkpointed states (newest first)
    async for snapshot in pipeline.get_state_history("thread-1"):
        print(snapshot.values)

asyncio.run(main())
```
{% endcode %}
{% endstep %}
{% endstepper %}

The output will look similar to:

```
{'text': 'world', 'text_upper': 'WORLD'}
{'text': 'hello', 'text_upper': 'HELLO'}
...
```

### Filtering History

You can limit the number of results returned, or filter by metadata:

{% code lineNumbers="true" expandable="true" %}
```python
async def main():
    await pipeline.invoke({"text": "hello", "text_upper": ""}, thread_id="thread-2")
    await pipeline.invoke({"text": "world", "text_upper": ""}, thread_id="thread-2")

    # Get only the most recent snapshot
    async for snapshot in pipeline.get_state_history("thread-2", limit=1):
        print(snapshot.values)
        # {'text': 'world', 'text_upper': 'WORLD'}

    # Filter by metadata
    async for snapshot in pipeline.get_state_history(
        "thread-2",
        history_filter={"source": "loop"},
    ):
        print(snapshot.values)
        # {'text': 'world', 'text_upper': 'WORLD'}
        # {'text': 'hello', 'text_upper': 'HELLO'}
        # ...

asyncio.run(main())
```
{% endcode %}


{% hint style="danger" %}
**Checkpointer Required**: Calling `get_state_history()` without a checkpointer raises a `ValueError`. Always provide a checkpointer (e.g., `InMemorySaver()`) when constructing the Pipeline.
{% endhint %}

## Forking from a Previous State

You can **fork** pipeline execution from any historical checkpoint using `fork_from()`. This updates the state at a specific past checkpoint and returns a new configuration that you pass to `invoke()` to re-execute from that point. The original execution history is preserved, the fork creates a new branch.

{% stepper %}
{% step %}
**Define state and steps**

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio
from typing import TypedDict

from langgraph.checkpoint.memory import InMemorySaver

from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

class ForkState(TypedDict):
    text: str
    text_upper: str

def to_upper(data: dict) -> str:
    return data["text"].upper()
```
{% endcode %}
{% endstep %}

{% step %}
**Build the pipeline with a checkpointer**

{% code lineNumbers="true" expandable="true" %}
```python
pipeline = Pipeline(
    steps=[transform(to_upper, input_map=["text"], output_state="text_upper", name="to_upper")],
    state_type=ForkState,
    checkpointer=InMemorySaver(),
)
```
{% endcode %}
{% endstep %}

{% step %}
**Run the pipeline and find a checkpoint to fork from**

{% code lineNumbers="true" expandable="true" %}
```python
async def main():
    # Initial run
    await pipeline.invoke({"text": "original input", "text_upper": ""}, thread_id="t1")

    # Retrieve state history
    history = [snap async for snap in pipeline.get_state_history("t1")]
    checkpoint_id = history[0].config["configurable"]["checkpoint_id"]

    print(f"Checkpoint ID: {checkpoint_id}")
    # Checkpoint ID: 1ef8b9f2-0000-0000-0000-000000000000

    print(f"Values at checkpoint: {history[0].values}")
    # Values at checkpoint: {'text': 'original input', 'text_upper': 'ORIGINAL INPUT'}

asyncio.run(main())
```
{% endcode %}
{% endstep %}

{% step %}
**Fork from the checkpoint and re-invoke**

{% code lineNumbers="true" expandable="true" %}
```python
async def main():
    # Run pipeline to create a checkpoint
    await pipeline.invoke({"text": "original input", "text_upper": ""}, thread_id="t1")

    # Get the checkpoint ID
    history = [snap async for snap in pipeline.get_state_history("t1")]
    checkpoint_id = history[0].config["configurable"]["checkpoint_id"]

    # Fork: update state at that checkpoint and get a new runnable config
    new_config = pipeline.fork_from(
        thread_id="t1",
        checkpoint_id=checkpoint_id,
        values={"text": "modified input"},
    )

    # Resume execution from the forked state
    forked_result = await pipeline.invoke(None, config=new_config)

    print(forked_result)
    # {'text': 'modified input', 'text_upper': 'MODIFIED INPUT'}

asyncio.run(main())
```
{% endcode %}
{% endstep %}
{% endstepper %}

You can optionally pass `as_node` to simulate the update as if it came from a specific node:

{% code lineNumbers="true" expandable="true" %}
```python
new_config = pipeline.fork_from(
    thread_id="t1",
    checkpoint_id=checkpoint_id,
    values={"text": "modified input"},
    as_node="to_upper",  # simulate this update as to_upper's output
)
```
{% endcode %}


{% hint style="info" %}
**Use Cases for Forking**:
- **A/B testing**: Fork from the same checkpoint with different inputs to compare outputs.
- **Debugging**: Replay a failing pipeline from the last known-good state.
- **What-if analysis**: Explore alternative execution paths without re-running earlier steps.
{% endhint %}

{% hint style="danger" %}
**Checkpointer Required**: Calling `fork_from()` without a checkpointer raises a `ValueError`. Always provide a checkpointer (e.g., `InMemorySaver()`) when constructing the Pipeline.
{% endhint %}

