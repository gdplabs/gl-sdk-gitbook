---
icon: bug
---

# Observability and Debugging

[**`gllm-pipeline`**](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/pipeline.html) | **Tutorial**: [observability-and-debugging.md](observability-and-debugging.md "mention") | **Use Case**: [pipeline.md](pipeline.md "mention"), [debug-a-pipeline.md](../../guides/debug-a-pipeline.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/index.html)

The **Pipeline** provides built-in observability and debugging capabilities that let you inspect intermediate step outputs, trace execution in real time, and travel through the history of past pipeline runs. 

For a comprehensive end-to-end walkthrough of these features, check out the [Debugging a Pipeline](../../guides/debug-a-pipeline.md "mention") guide. This page provides a quick reference to the debugging syntax.

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

## Setup Dummy Pipeline

For the snippets below, we assume you have constructed a simple pipeline with a checkpointer attached:

{% code lineNumbers="true" expandable="true" %}
```python
import asyncio
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

class DummyState(TypedDict):
    text: str
    text_upper: str

def to_upper(data: dict) -> str:
    return data["text"].upper()

pipeline = Pipeline(
    steps=[transform(to_upper, input_map=["text"], output_state="text_upper", name="to_upper")],
    state_type=DummyState,
    checkpointer=InMemorySaver(),
)
```
{% endcode %}

## Debug Tracing

Enable per-node console tracing to get a real-time summary of every step executed.

{% code lineNumbers="true" expandable="true" %}
```python
# Enable tracing
pipeline.enable_debug_tracing()

# Subsequent invokes will emit trace logs to stdout
asyncio.run(pipeline.invoke({"text": "hello", "text_upper": ""}, thread_id="t1"))

# To disable tracing:
pipeline.disable_debug_tracing()
```
{% endcode %}

{% hint style="info" %}
**OpenTelemetry Compatibility**: Debug tracing is fully compatible with existing `gl-observability` OpenTelemetry traces. Enabling console tracing does **not** affect, replace, or conflict with any OTel spans already being emitted.
{% endhint %}

## Capturing Step Outputs

Use `include_outputs_from` to capture the individual output produced by specific steps, returning them in the final state under the `__step_outputs__` key.

{% code lineNumbers="true" expandable="true" %}
```python
result = asyncio.run(
    pipeline.invoke(
        {"text": "hello", "text_upper": ""},
        thread_id="t2",
        include_outputs_from={"to_upper"}
    )
)

print(result["__step_outputs__"]["to_upper"])
```
{% endcode %}

## State History

Retrieve the full history of checkpointed states for a given thread to enable time-travel debugging.

{% code lineNumbers="true" expandable="true" %}
```python
async def get_history():
    # Iterate through all checkpointed states (newest first)
    async for snapshot in pipeline.get_state_history("t1"):
        print(snapshot.values)

asyncio.run(get_history())
```
{% endcode %}

{% hint style="danger" %}
**Checkpointer Required**: Calling `get_state_history()` without a checkpointer raises a `ValueError`.
{% endhint %}

## Forking from a Previous State

Fork pipeline execution from a historical checkpoint to create a new branch.

{% code lineNumbers="true" expandable="true" %}
```python
async def fork_pipeline():
    # Get a previous checkpoint ID
    history = [snap async for snap in pipeline.get_state_history("t1")]
    checkpoint_id = history[0].config["configurable"]["checkpoint_id"]

    # Fork with new values
    new_config = pipeline.fork_from(
        thread_id="t1",
        checkpoint_id=checkpoint_id,
        values={"text": "modified input"}
    )

    # Re-invoke from the forked state
    result = await pipeline.invoke(None, config=new_config)
    print(result)

asyncio.run(fork_pipeline())
```
{% endcode %}

{% hint style="info" %}
**Use Cases for Forking**:
- **A/B testing**: Fork from the same checkpoint with different inputs to compare outputs.
- **Debugging**: Replay a failing pipeline from the last known-good state.
- **What-if analysis**: Explore alternative execution paths without re-running earlier steps.
{% endhint %}

{% hint style="danger" %}
**Checkpointer Required**: Calling `fork_from()` without a checkpointer raises a `ValueError`.
{% endhint %}
