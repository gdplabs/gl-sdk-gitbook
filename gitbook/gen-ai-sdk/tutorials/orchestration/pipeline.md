---
icon: play
---

# Pipeline

[**`gllm-pipeline`**](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/pipeline.html) | **Tutorial**: [pipeline.md](pipeline.md "mention")| **Use Case**: [build-end-to-end-rag-pipeline](../../guides/build-end-to-end-rag-pipeline/ "mention")[execute-a-pipeline.md](../../guides/execute-a-pipeline.md "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/index.html)

The **Pipeline** is the core orchestration component that sequences and manages the execution of the components in our SDK.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [basic-concepts.md](basic-concepts.md "mention")of orchestration components
2. [state.md](state.md "mention")
3. [steps](steps/ "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-pipeline"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-pipeline"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "gllm-pipeline"
```
{% endtab %}
{% endtabs %}

## Quickstart

We will create a simple general Pipeline to illustrate the general workflow around building Pipelines.

{% stepper %}
{% step %}
**Import the Pipeline and the steps**

```python
from typing import TypedDict  # Optional, only for custom states
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import step, transform, bundle, log, subgraph
```
{% endstep %}

{% step %}
**Define your state**

We will use a simplified state for ths quickstart. Alternatively, if you are dealing with an RAG pipeline, you can use the default [RAGState](state.md#default-state-ragstate) instead.

```python
class MiniState(TypedDict):
    text: str
    text_upper: str
    text_len: int
    summary: dict  # summary bundle
```
{% endstep %}

{% step %}
**Define your steps**

Here we use simple `transform` and `bundle` steps to illustrate how the Pipeline works. You can always use the other [Steps](steps/), or follow the [How-to guide](../../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md) for a comprehensive guide.

```python
def to_upper(data: dict) -> str:
    return data["text"].upper()

def count_chars(data: dict) -> int:
    return len(data["text_upper"])

pipe = Pipeline(
    steps=[
        transform(to_upper, input_map=["text"], output_state="text_upper"),
        transform(count_chars, input_map=["text_upper"], output_state="text_len"),
        bundle(["text", "text_upper", "text_len"], output_state="summary"),
    ],
    state_type=MiniState,
)
```
{% endstep %}

{% step %}
**Invoke the pipeline**

Our pipeline is asynchronous by default. Therefore, to invoke it, you must use `asyncio.run.`

```python
import asyncio

initial: MiniState = {
    "text": "hello world",
    "text_upper": "",
    "text_len": 0,
    "summary": {},
}
final = asyncio.run(pipe.invoke(initial))

print(final)
```

After invoking the pipeline, you should get an output similar to this:

```python
{'text': 'hello world', 'text_upper': 'HELLO WORLD', 'text_len': 11,
 'summary': {'text': 'hello world', 'text_upper': 'HELLO WORLD', 'text_len': 11}}
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
That's it! You have created your first Pipeline! All future Pipelines that you will ever create will follow the above general steps.
{% endhint %}

## The Pipe Operator

You can also utilize the pipe (`|`) operator to compose your Pipeline.

```python
class MiniState2(TypedDict):
    text: str
    text_upper: str
    text_len: int

def to_upper2(data: dict) -> str:
    return data["text"].upper()

def count_chars2(data: dict) -> int:
    return len(data["text_upper"])

pipe2 = (
    transform(to_upper2, input_map=["text"], output_state="text_upper")
    | transform(count_chars2, input_map=["text_upper"], output_state="text_len")
    | log("Upper2: {text_upper} (len={text_len})")
)
pipe2.state_type = MiniState2  # important: set your TypedDict state

initial2: MiniState2 = {"text": "pipeline!", "text_upper": "", "text_len": 0}
final2 = await pipe2.invoke(initial2)
print(final2)
```

{% hint style="warning" %}
When composing using `|` , the Pipeline's state will be `RAGState`. Make sure that you use the `state_type` setter to specify the correct state type before invoking.
{% endhint %}

### Appending a Step

You can use the `|` operator to append a step to a Pipeline.

```python
p1 = Pipeline(
    steps=[transform(to_upper, input_map=["text"], output_state="text_upper")],
    state_type=TextState,
)

# Append step at the end
p1_plus = p1 | transform(count_len, input_map=["text_upper"], output_state="text_len")

final = await p1_plus.invoke({"text": "hello", "text_upper": "", "text_len": 0})
print(final)  # {'text': 'hello', 'text_upper': 'HELLO', 'text_len': 5}
```

### Merge Two Pipelines

You can also use the `|` operator to merge two pipelines **of the same State schema**.

```python
p_left = Pipeline(
    steps=[transform(to_upper, input_map=["text"], output_state="text_upper")],
    state_type=TextState,
)
p_right = Pipeline(
    steps=[transform(count_len, input_map=["text_upper"], output_state="text_len"), log("len={text_len}")],
    state_type=TextState,
)

combined = p_left | p_right  # OK: same state type

final = await combined.invoke({"text": "compose", "text_upper": "", "text_len": 0})
print(final)  # {'text': 'compose', 'text_upper': 'COMPOSE', 'text_len': 7}
```

{% hint style="danger" %}
Merging two pipelines with different State schemata will cause a ValidationError.
{% endhint %}

### Placeholder Pipelines

Finally, you can initialize a Pipeline with an empty step to use as a placeholder, e.g. to set the `state_type`, then use the `|` operator to compose the pipeline with the correct `state_type`.

```python
identity = Pipeline([], state_type=TextState)
p = Pipeline([transform(to_upper, input_map=["text"], output_state="text_upper")],

a = p | identity
b = identity | p  # Same as p, but if constructed via step | identity, set state_type explicitly
```

## Visualizing the Pipeline

Our Pipelines come with the `get_mermaid_diagram()` method, which gives you a Mermaid code. This is useful for docs and reviews.

To obtain the Mermaid diagram of a Pipeline, simply call the method.

```python
diagram = pipe.get_mermaid_diagram()
print(diagram)
```

The output should look something like this:

```mermaid
graph TD
Transform_to_upper__abc123
Transform_count_chars__def456
Log__ghi789
START --> Transform_to_upper__abc123
Transform_to_upper__abc123 --> Transform_count_chars__def456
Transform_count_chars__def456 --> Log__ghi789
Log__ghi789 --> END
```

Which you could then copy and paste to any Mermaid renderer.

## Runtime Configuration

Some steps support dynamic runtime configuration, which allows us to change the step's behavior at runtime.

To use these runtime configurations, during invocation, supply a dictionary using the `config` parameter.

```python
pipe.invoke(state, config={"reverse": False, "uppercase": True})
```

For `step`, `transform`, `parallel`, and `map_reduce`, the Runtime Config is automatically accessible alongside the State when using `input_map`. When you specify a key in `input_map` as a string, the system first tries to resolve it from the State, and if not found, falls back to the Runtime Config.

```python
import asyncio

from typing import TypedDict
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

# State
class CfgState(TypedDict):
    text: str
    result: str

# Operation uses config-driven switches
def format_text(data: dict) -> str:
    s = data["text"]
    if data["reverse"]:
        s = s[::-1]
    if data["uppercase"]:
        s = s.upper()
    return s

pipe = Pipeline(
    steps=[
        transform(
            format_text,
            input_map=["text", "reverse", "uppercase"],
            output_state="result",
        )
    ],
    state_type=CfgState,
)

# Provide all required config keys listed in input_map
state: CfgState = {"text": "Hello", "result": ""}
out = asyncio.run(pipe.invoke(state, config={"reverse": False, "uppercase": True}))
print(out["result"])  # HELLO

out2 = asyncio.run(pipe.invoke({"text": "Hello", "result": ""}, config={"reverse": True, "uppercase": True}))
print(out2["result"])  # OLLEH
```

For conditionals `if_else`, `switch`, `toggle`, and `guard`, the Runtime Config is **always available** and can be accessed using its original keys when using a `Callable`.

```python
from gllm_pipeline.steps._func import if_else, transform

def is_positive(data: dict) -> bool:
    return data["value"] > 0

# Branches write a message
pos = transform(lambda _data: "value is positive", input_map=[], output_state="msg")
neg = transform(lambda _data: "value is non-positive", input_map=[], output_state="msg")

positive_step = if_else(
    condition=is_positive,
    if_branch=pos,
    else_branch=neg,
    output_state="decision",
)
```

However, when using a `Component`, you must explicitly map the inputs using `input_map`.

```python
import asyncio

from gllm_core.schema import Component
from gllm_pipeline.steps._func import if_else, transform

# Minimal Component that returns "true"/"false"
class GreaterThan(Component):
    def decide(self, value: int, threshold: int) -> str:
        """Return 'true' if value > threshold else 'false'."""
        return "true" if value > threshold else "false"

    async def _run(self, **kwargs: Any) -> str:
        """Implements the core logic; called by Component.run(...)."""
        value: int = kwargs["value"]
        threshold: int = kwargs["threshold"]
        return self.decide(value, threshold)


# Branches write a message
higher = transform(lambda _data: "value > threshold", input_map=[], output_state="msg")
lower_eq = transform(lambda _data: "value <= threshold", input_map=[], output_state="msg")

cond_comp = GreaterThan()

greater_than_step = if_else(
    condition=cond_comp,
    if_branch=higher,
    else_branch=lower_eq,
    input_map={"value": "value", "threshold": "threshold"},  # map state and config to args
    output_state="decision",
)
```

## Input and Output Schema

The Pipeline supports defining explicit input and output schemata to validate data entering and leaving the pipeline. This is particularly useful when converting a Pipeline to a tool or when you need strict type checking.

You should define input and output schemata when:

1. Converting a Pipeline to a Tool (for Agent integration)
2. You need validation of data entering/leaving the pipeline
3. You want to document the expected structure of inputs and outputs

Internally, LangGraph uses input and output schemata to **filter** data at the boundaries of your pipeline:

1. **Input Schema Filtering**: When you provide an `input_type`, LangGraph filters the initial state before it enters the graph. Only fields defined in the input schema are passed through to the pipeline's internal state. This ensures your pipeline only receives the exact fields you expect.
2. **Output Schema Filtering**: When you provide an `output_type`, LangGraph filters the final state before returning it. Only fields defined in the output schema are included in the result. This is useful for hiding internal state fields from the caller.

{% hint style="warning" %}
**Important**: Input and output schemas perform **filtering**, not **validation**. If you need to validate inputs (e.g., checking ranges, formats), you must either:

* Use a Pydantic `BaseModel` for your `state_type` (validates during execution)
* Manually validate using your `input_type` schema before calling `invoke()`
{% endhint %}

### Using TypedDict for Simple Schemas

For straightforward use cases, you can use TypedDict to define your schemas:

```python
import asyncio
from typing import TypedDict
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

# Define your state
class TextProcessingState(TypedDict):
    raw_text: str
    processed_text: str
    char_count: int

# Define input schema (subset of state)
class TextInput(TypedDict):
    raw_text: str

# Define output schema (subset of state)
class TextOutput(TypedDict):
    processed_text: str
    char_count: int

def process_text(data: dict) -> str:
    return data["raw_text"].upper()

def count_chars(data: dict) -> int:
    return len(data["processed_text"])

pipe = Pipeline(
    steps=[
        transform(process_text, input_map=["raw_text"], output_state="processed_text"),
        transform(count_chars, input_map=["processed_text"], output_state="char_count"),
    ],
    state_type=TextProcessingState,
    input_type=TextInput,   # Only 'raw_text' is required as input
    output_type=TextOutput,  # Only these fields will be in the output
)

# When invoking, you only need to provide the input schema fields
initial_state = {
    "raw_text": "hello world",
    "processed_text": "",  # Still need to initialize state fields
    "char_count": 0,
}
result = asyncio.run(pipe.invoke(initial_state))
print(result)  # Only contains 'processed_text' and 'char_count' (output schema)
```

### Using Pydantic for Validation

For automatic validation, you must use a Pydantic `BaseModel` as your **state schema**. LangGraph validates the state during pipeline execution based on the state schema.

The input and output schemas may be used to validate the state before and after the pipeline execution.

```python
import asyncio
from pydantic import BaseModel, Field, ValidationError
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

# Define your state as a Pydantic BaseModel for automatic validation
class ScoreState(BaseModel):
    score: int = Field(..., gt=0, description="Score must be positive")
    scaled_score: float = Field(default=0.0)
    message: str = Field(default="")

# Input schema (filter what's passed to the pipeline)
class ScoreInput(BaseModel):
    score: int = Field(..., gt=0, le=100, description="Input score between 1-100")

# Output schema (filters what's returned)
class ScoreOutput(BaseModel):
    scaled_score: float = Field(..., description="The scaled score value")
    message: str = Field(..., description="Notification message")

def scale_score(data: dict) -> float:
    return float(data["score"] * 1.5)

def create_message(data: dict) -> str:
    return f"Processed score: {data['scaled_score']}"

pipe = Pipeline(
    steps=[
        transform(scale_score, input_map=["score"], output_state="scaled_score"),
        transform(create_message, input_map=["scaled_score"], output_state="message"),
    ],
    state_type=ScoreState,    # LangGraph validates THIS during execution
    input_type=ScoreInput,    # Used for manual validation and tool conversion
    output_type=ScoreOutput,  # Filters the returned state
)

# Example 1: Manual validation using input schema before invoking
try:
    user_input = {"score": 10}
    validated_input = ScoreInput(**user_input)  # Validate manually

    # Create initial state from validated input
    initial_state = ScoreState(score=validated_input.score)
    result = asyncio.run(pipe.invoke(initial_state.model_dump()))
    print(result)
    # Only outputs: {'scaled_score': 15.0, 'message': 'Processed score: 15.0'}
except ValidationError as e:
    print(f"Input validation error: {e}")

# Example 2: State validation by LangGraph (score must be > 0)
try:
    # This will fail LangGraph's state validation (score not > 0)
    bad_state = ScoreState(score=-5)  # Pydantic validates immediately
    asyncio.run(pipe.invoke(bad_state.model_dump()))
except ValidationError as e:
    print(f"State validation error: {e}")

# Example 3: Input schema validates stricter constraints (score <= 100)
try:
    user_input = {"score": 150}  # Valid for state, but invalid for input
    validated_input = ScoreInput(**user_input)  # Fails: score > 100
except ValidationError as e:
    print(f"Input validation error: {e}")  # This will catch it
```

### Converting to a Tool

When you define input/output schemas, the Pipeline can be easily converted to a Tool for use with AI Agents:

```python
from gllm_pipeline.pipeline.pipeline import Pipeline
from typing import TypedDict
from pydantic import BaseModel, Field

class QueryInput(BaseModel):
    question: str = Field(..., description="The user's question")

class QueryOutput(BaseModel):
    answer: str = Field(..., description="The generated answer")

class QueryState(TypedDict):
    question: str
    answer: str

# ... define your pipeline steps ...

pipeline = Pipeline(
    steps=[...],  # your steps here
    state_type=QueryState,
    input_type=QueryInput,
    output_type=QueryOutput,
    name="answer_question"
)

# Convert to tool
tool = pipeline.as_tool(description="Answers user questions using RAG")

# Now the tool has proper input/output schemas
print(tool.input_schema)  # Shows Pydantic schema
print(tool.output_schema)  # Shows Pydantic schema
```

## Using the Debug State

Our Pipeline comes with a utility to provide a trace of the Pipeline execution. To do so, pass `config={"debug_state": True}` . The trace is available as `__state_logs__` in the final output.

```python
final_dbg = await pipe.invoke(
    {"text": "debug me", "text_upper": "", "text_len": 0},
    config={"debug_state": True},
)
print(final_dbg["__state_logs__"])
```

## Using a Pipeline as a Subgraph

To use a Pipeline as a Subgraph, one can wrap the Pipeline inside a [subgraph](steps/#subgraph) step and map the input states and configs as necessary.

```python
# Child pipeline with its own state
class ChildState(TypedDict):
    text: str
    text_upper: str

def to_upper_child(data: dict) -> str:
    return data["text"].upper()

child = Pipeline(
    steps=[transform(to_upper_child, input_map=["text"], output_state="text_upper")],
    state_type=ChildState,
    name="child_pipeline",
)

# Parent pipeline with a different state
class ParentState(TypedDict):
    input_text: str
    result_upper: str
    text_len: int

def count_len_parent(data: dict) -> int:
    return len(data["result_upper"])

parent = Pipeline(
    steps=[
        subgraph(
            child,
            input_map={"text": "input_text"},          # parent.input_text -> child.text
            output_state_map={"result_upper": "text_upper"}, # child.text_upper -> parent.result_upper
        ),
        transform(count_len_parent, input_map=["result_upper"], output_state="text_len"),
        log("Parent upper='{result_upper}' (len={text_len})"),
    ],
    state_type=ParentState,
)

initial_parent: ParentState = {"input_text": "SubGraph Rocks!", "result_upper": "", "text_len": 0}
final_parent = await parent.invoke(initial_parent)
print(final_parent)
```

### Using the Leftshift (<<) Operator

Alternatively, you can use the leftshift operator (`<<`) to embed a Pipeline as a subgraph in another Pipeline. Subgraphs created this way will have overlapping State keys automatically mapped.

```python
class Parent2State(TypedDict):
    text: str          # overlaps with ChildState.text
    text_upper: str    # overlaps with ChildState.text_upper
    note: str

# Reuse 'child' from above (ChildState)
parent2 = Pipeline(
    steps=[log("Before: {text}")],
    state_type=Parent2State,
    name="parent2",
)

# Include child as a subgraph within parent2
combined = parent2 << child   # auto-maps overlapping keys

initial_p2: Parent2State = {"text": "Auto-map!", "text_upper": "", "note": ""}
final_p2 = await combined.invoke(initial_p2)
print(final_p2["text"], final_p2["text_upper"])
```
