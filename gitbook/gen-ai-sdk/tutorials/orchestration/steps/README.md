---
icon: shoe-prints
---

# Steps

## Steps

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/steps) | **Tutorial**: [.](./ "mention")| **Use Case**: [build-end-to-end-rag-pipeline](../../../guides/build-end-to-end-rag-pipeline/ "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/steps.html)

### What's a Step?

A step is a unit of work (a node) that:

1. Reads specific keys from the pipeline state (and optionally runtime config).
2. Performs an operation (component call, function, branching, etc.).
3. Writes outputs back to the state under specific keys.

You can learn more about composing steps into a pipeline using [#the-pipe-operator](../pipeline.md#the-pipe-operator "mention").

Learn in greater detail about input maps in [input-mapping.md](input-mapping.md "mention").

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [state.md](../state.md "mention")

</details>

### Installation

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

### Basic Steps

We will first learn the basic steps that can be used to create a Pipeline.

Throughout this tutorial page, we will be using the `Echo` component below as a replacement for our SDK components.

{% code title="echo.py" %}
```python
from typing import Any

from gllm_core.schema.component import Component


class Echo(Component):
    """A component that returns the value of 'x' unchanged."""

    def identity(self, x: Any) -> Any:
        """Return the input 'x' unchanged.

        Args:
            x (Any): Any input to be passed to the function.

        Returns:
            Any: The same value provided via 'x'.
        """
        return x

    async def _run(self, **kwargs: Any) -> Any:
        """Returns the value passed under 'x' unchanged.

        Args:
            **kwargs (Any): Must contain key 'x' with the value to return.

        Returns:
            Any: The same value provided via 'x'.

        Raises:
            KeyError: If 'x' is not provided.
        """
        return self.identity(kwargs["x"])
```
{% endcode %}

#### step

A `step` wraps and runs a `Component` of our SDK with mapped inputs and stores outputs under a state key.

```python
from gllm_pipeline.steps import step

echo_step = step(
    component=Echo(),
    input_map={"x": "value"}, # Maps argument `x` to the state `value`.
    output_state="answer",
)
```

{% hint style="info" %}
When a step calls a `Component`, use `input_map` to map the component’s parameter names to keys in your pipeline state. This tells the step where to read each argument.

Learn more about input maps: [input-mapping.md](input-mapping.md "mention").
{% endhint %}

#### transform

A `transform` step applies a callable to selected state keys and writes the result.

```python
from gllm_pipeline.steps import transform

def uppercase(data: dict) -> str:
    """Makes a string `UPPERCASE`

    Args:
        data(dict): The state. Must contain `text`.

    Returns:
        str: The uppercase text.
    """
    return data["text"].upper()

uppercase_step = transform(
    operation=uppercase,
    input_map=["text"],
    output_state="upper_text",
)
```

#### bundle

A `bundle` step collects multiple state keys into a dictionary without changes to their values.

```python
from gllm_pipeline.steps import bundle

make_payload = bundle(
    input_states=["user", "query"],
    output_state="payload",  # state payload is now {"user": ..., "query": ...}
)
```

#### copy

A `copy` step duplicates data from one or more state keys to new keys without transformation.

```python
from gllm_pipeline.steps import copy

# Single to single
copy_one = copy("input_data", "output_data")

# Single to multiple (broadcast)
broadcast = copy("input_data", ["out1", "out2"])

# Multiple to single (pack into list)
pack = copy(["in1", "in2"], "packed_output")
```

### Branching

#### if\_else

An `if_else` step chooses between two branches based on a condition (a callable or a `Component`). The condition result can be saved to state.

```python
from gllm_pipeline.steps import if_else, log

feature_flag_step = if_else(
    condition=lambda s: s["flag"],           # truthy -> if_branch
    if_branch=log("Feature ON", is_template=False),
    else_branch=log("Feature OFF", is_template=False),
    output_state="feature_status",           # stores "true"/"false"
)
```

The condition could also be a `Component`. In this case, you need to pass an `input_map` .

```python
from gllm_pipeline.steps import if_else, step
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.types import Val

# Branches: produce constant messages via input_map (Echo returns 'x' unchanged)
grant_access = step(Echo(), input_map={"x": Val("Access granted")}, output_state="decision")
deny_access = step(Echo(), input_map={"x": Val("Access denied")}, output_state="decision")

# Condition: a Component that returns "true" or "false"
# Echo will return the state value at key "is_adult" (must be "true" or "false")
auth_gate = if_else(
    condition=Echo(),                      # Component condition
    if_branch=grant_access,                # runs when condition returns "true"
    else_branch=deny_access,               # runs when condition returns "false"
    input_map={"x": "is_adult"},           # map state -> component input
    output_state="condition_result",       # optional: persist "true"/"false"
)
```

#### switch

A `switch` step selects a branch from a dict of options based on a condition output (string). Supports default branch.

```python
from gllm_pipeline.steps import switch, log

dispatch_step = switch(
    condition=lambda s: s["command"],        # e.g., "search", "filter"
    branches={
        "search": log("Searching...", is_template=False),
        "filter": log("Filtering...", is_template=False),
    },
    default=log("Unknown command", is_template=False),
    output_state="command_type",
)
```

#### toggle

A `toggle` step runs its `if_branch` if condition is true; otherwise behaves like [no\_op](./#no_op). Condition can be callable, `Component`, or a string key looked up in merged state/config.

This step is useful to enable "optional" steps that are decided at runtime.

```python
from gllm_pipeline.steps import toggle, log

feature_flag_step = toggle(
    condition="feature_enabled",             # truthy in state/config?
    if_branch=log("Feature executed", is_template=False),
    output_state="feature_status",
)
```

### Concurrency

#### parallel

A `parallel` step runs multiple branches in parallel and merges results. Each branch can be a step or a list of steps.

```python
from gllm_pipeline.steps import parallel, log

parallel_step = parallel(
    branches=[
        log("A", is_template=False),
        log("B", is_template=False),
    ],
)
```

#### map\_reduce

A `map_reduce` step maps a function (or Component) over multiple items, then reduces results.

By default, list/tuple inputs in `input_map` drive fan-out. If you need an iterable to stay intact for every mapped item, wrap it with `Group(...)`.

```python
from gllm_pipeline.steps import map_reduce
from gllm_pipeline.types import Group, Val

sum_numbers_step = map_reduce(
    input_map={"n": "numbers"},              # numbers is a list in state
    output_state="total",
    map_func=lambda item: item["n"],         # returns each number
    reduce_func=sum,                         # sums the list of results
)

rank_step = map_reduce(
    input_map={
        "query": "queries",                           # fan-out input (list)
        "candidates": Group("candidate_groups"),      # grouped iterable from state/config
        "labels": Group(Val(["relevant", "neutral"])),  # grouped literal iterable
    },
    output_state="ranked_results",
    map_func=lambda item: {
        "query": item["query"],
        "top_candidate": item["candidates"][0],
        "labels": item["labels"],
    },
)
```

`Group("key")` resolves from state first, then runtime config, and reuses the full value in every map call. If a grouped lookup key is missing from both state and config, `map_reduce` raises a `KeyError`.

### Flow Control

#### goto

A `goto` step allows you to jump to another step in the pipeline, enabling loops and non-linear flows.

```python
from gllm_pipeline.steps import goto
from gllm_pipeline.types import Val

# Jump to a specific step name
jump_step = goto(
    name="jump_to_start",
    target=Val("start_step")
)

# Jump based on state
dynamic_jump = goto(
    name="dynamic_jump",
    target="next_step_name_key", # Reads target from state["next_step_name_key"]
)

# Jump based on function
def compute_next_step(state: dict) -> str:
    return "step_a" if state["value"] > 10 else "step_b"

computed_jump = goto(
    name="computed_jump",
    target=compute_next_step,
    input_map={"value": "state_value"}
)
```

#### no\_op

A `no_op` step is a step that does nothing. This is useful as a placeholder step, or as part of a [toggle](./#toggle).

```python
from gllm_pipeline.steps import no_op

skip_step = no_op()
```

#### terminate

A `terminate` step explicitly terminates the _current_ Pipeline. This is useful as part of a [guard](./#guard) step.

```python
from gllm_pipeline.steps import terminate

stop_now_step = terminate()
```

#### guard

A `guard` step evaluates a condition. On success runs `success_branch`. On failure runs `failure_branch`, then terminates the _current_ Pipeline.

```python
from gllm_pipeline.steps import guard, log, terminate

enforce_auth_step = guard(
    condition=lambda s: s.get("is_authenticated", False),
    success_branch=log("Welcome!", is_template=False),
    output_state="auth_result",
)
```

#### while\_do

A `while_do` step creates a do-while loop in your pipeline. The `body` executes at least once, and a `condition` is evaluated at the end of each iteration to determine whether to repeat the loop.

```python
from gllm_pipeline.steps import while_do, step
from gllm_pipeline.pipeline import Pipeline

# Condition is truthy: continues the loop if the status is not "success"
def check_success(data: dict) -> bool:
    return data.get("status") != "success"

loop_step = while_do(
    body=step(MyProcessingComponent(), input_map={"input": "data"}, output_state="status"),
    condition=check_success
)

```

You can also use a Component to evaluate whether to continue. You can provide an `input_map` when you need explicit field mapping to the component's inputs.

```python
from gllm_pipeline.steps import while_do, step

loop_step = while_do(
    body=step(GenerateAnswer(), input_map={"query": "question"}, output_state="draft"),
    condition=EvaluatorComponent(),
    input_map={"answer": "draft"} # Provide the drafted answer to the Evaluator component
)
```

#### interrupt

An `interrupt` step explicitly halts the pipeline execution at runtime using LangGraph's native `interrupt` functionality. When the pipeline reaches this step, it pauses execution, returns control to the caller along with the current state, and optionally emits a custom message.

Unlike `PauseStep`, which relies on `interrupt_before` or `interrupt_after` targeting at invocation time, an `interrupt` step **unconditionally** halts execution whenever its node runs.

```python
from langgraph.types import Command
from gllm_pipeline.steps import interrupt, step
from gllm_pipeline.pipeline import Pipeline

pipeline = Pipeline(steps=[
    step(FetchData(), output_state="raw_data"),
    # Interrupts and asks for user input, mapping the reply to state
    interrupt(
        name="wait_for_human",
        message="Please review the data before we process it.",
        resume_value_map="user_feedback"
    ),
    step(ProcessData(), input_map={"feedback": "user_feedback"})
])

# 1. Initial run: Halts at the interrupt step
state = await pipeline.invoke(
    initial_state={"topic": "AI algorithms"},
    thread_id="thread-1"
)

# 2. Resumes execution with user feedback mapped to "user_feedback" state variable
result = await pipeline.invoke(
    Command(resume="Looks good, proceed processing!"),
    thread_id="thread-1"
)
```

#### pause

A `pause` step is a specialized marker step that performs no operation (NoOp) but serves as a deterministic breakpoint target. It adds **no runtime behavior** and exists purely to give developers a named node in the pipeline graph that can be targeted by interruptions.

This pattern is highly recommended for **debugging**: you can insert one or more `pause` instances at interesting points in your pipeline, then selectively activate breakpoints at invocation time without needing to recompile or alter the pipeline structure.

<pre class="language-python"><code class="lang-python">from gllm_pipeline.steps import pause, step
from gllm_pipeline.pipeline import Pipeline

# 1. Insert a named pause step into the sequence
bp = pause(name="before_llm")

# 2. Compile your pipeline

pipeline = Pipeline(steps=[preprocess, bp, llm_step, postprocess])
<strong>
</strong><strong># 3. Debug run: the graph will halt execution right before 'before_llm'
</strong>result = await pipeline.invoke( initial_state=state, interrupt_before=["before_llm"] )
</code></pre>

### Observability

#### log

A `log` step emits a message through an event emitter. Can be a plain string or a template with state placeholders.

```python
from gllm_pipeline.steps import log

plain = log("Processing...", is_template=False)
templated = log("User: {user_id}, Query: {query}")  # pulls from state keys
```

### Composition

#### subgraph

A `subgraph` executes another `Pipeline` as a step, with flexible input/output mapping.

```python
from gllm_pipeline.steps import subgraph

# sub_pipeline is a Pipeline you built elsewhere
sub_pipeline = Pipeline(
    steps = [step_a, step_b, step_b]
)

use_subgraph = subgraph(
    subgraph=sub_pipeline,
    input_map={"query": "user_query"},
    output_state_map={"result": "subgraph_result"},
)

```
