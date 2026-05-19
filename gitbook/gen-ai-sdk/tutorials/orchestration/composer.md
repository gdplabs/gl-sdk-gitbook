---
icon: violin
---

# \[BETA] Composer

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/pipeline/composer) | **Tutorial**: [composer.md](composer.md "mention")| **Use Case**: [build-end-to-end-rag-pipeline](../../guides/build-end-to-end-rag-pipeline/ "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/pipeline/composer.html)

{% hint style="success" %}
New in `gllm-pipeline v0.4.18`
{% endhint %}

{% hint style="warning" %}
This feature is still in Beta.
{% endhint %}

### What's a Composer?

A Composer is a fluent API builder that:

1. Provides a chainable interface for building pipelines step by step.
2. Manages a `Pipeline` instance internally and accumulates steps as you call methods.
3. Offers both direct-style and builder-style patterns for complex operations (branching, conditionals, parallel execution).
4. Returns the composed `Pipeline` via the `.done()` method when you're finished building.

The Composer pattern allows you to build pipelines in a readable, fluent manner:

```python
pipeline = (
    Pipeline()
    .composer
    .step(my_component, {"input": "query"}, "result")
    .log("Processing result: {result}")
    .transform(lambda data: data["result"].upper(), ["result"], "upper_result")
    .terminate()
    .done()
)
```

Learn in greater detail about input maps in [input-mapping.md](steps/input-mapping.md "mention")

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

You should be familiar with these concepts:

1. [state.md](state.md "mention")
2. [steps](steps/ "mention")

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

### Basic Composer Methods

We will first learn the basic composer methods that can be used to create a Pipeline using the fluent API.

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

The `step` method wraps and runs a `Component` with mapped inputs and stores outputs under a state key. This is the composer equivalent of the `step()` function.

```python
from gllm_pipeline.pipeline import Pipeline

pipeline = (
    Pipeline()
    .composer
    .step(
        component=Echo(),
        input_map={"x": "value"},  # Maps argument `x` to the state `value`.
        output_state="answer",
    )
    .done()
)
```

{% hint style="info" %}
When a step calls a `Component`, use `input_map` to map the component's parameter names to keys in your pipeline state. This tells the step where to read each argument.

Learn more about input maps: [input-mapping.md](steps/input-mapping.md "mention").
{% endhint %}

#### transform

The `transform` method applies a callable to selected state keys and writes the result. This is the composer equivalent of the `transform()` function.

```python
from gllm_pipeline.pipeline import Pipeline

def uppercase(data: dict) -> str:
    """Makes a string `UPPERCASE`

    Args:
        data(dict): The state. Must contain `text`.

    Returns:
        str: The uppercase text.
    """
    return data["text"].upper()

pipeline = (
    Pipeline()
    .composer
    .transform(
        operation=uppercase,
        input_map=["text"],
        output_state="upper_text",
    )
    .done()
)
```

#### bundle

The `bundle` method collects multiple state keys into a dictionary without changes to their values. This is the composer equivalent of the `bundle()` function.

```python
from gllm_pipeline.pipeline import Pipeline

pipeline = (
    Pipeline()
    .composer
    .bundle(
        input_states=["user", "query"],
        output_state="payload",  # state payload is now {"user": ..., "query": ...}
    )
    .done()
)
```

#### log

The `log` method emits a message through an event emitter. Can be a plain string or a template with state placeholders. This is the composer equivalent of the `log()` function.

```python
from gllm_pipeline.pipeline import Pipeline

pipeline = (
    Pipeline()
    .composer
    .log("Processing...", is_template=False)
    .log("User: {user_id}, Query: {query}")  # pulls from state keys
    .done()
)
```

#### no\_op

The `no_op` method creates a step that does nothing. This is useful as a placeholder step. This is the composer equivalent of the `no_op()` function.

```python
from gllm_pipeline.pipeline import Pipeline

pipeline = (
    Pipeline()
    .composer
    .no_op()
    .done()
)
```

#### terminate

The `terminate` method explicitly terminates the _current_ Pipeline. This is useful as part of conditional flows. This is the composer equivalent of the `terminate()` function.

```python
from gllm_pipeline.pipeline import Pipeline

pipeline = (
    Pipeline()
    .composer
    .terminate()
    .done()
)
```

### Branching

The Composer provides several methods for conditional execution and branching logic.

#### when / if\_else

The Composer provides two approaches for conditional branching:

1. **Builder-style with `when()`** - for fluent conditional building
2. **Direct-style with `if_else()`** - when you have both branches ready

**Builder-style: when().then().otherwise().end()**

The `when()` method begins a fluent conditional builder that lets you define branches step-by-step:

```python
from gllm_pipeline.pipeline import Pipeline

pipeline = (
    Pipeline()
    .composer
    .when(lambda s: s["flag"])           # condition
        .then(
            Pipeline().composer.log("Feature ON", is_template=False).done()
        )
        .otherwise(
            Pipeline().composer.log("Feature OFF", is_template=False).done()
        )
        .end()  # Returns to the main composer
    .done()
)
```

**Direct-style: if\_else()**

The `if_else()` method creates a conditional step when you already have both branches available:

```python
from gllm_pipeline.pipeline import Pipeline

feature_on_step = Pipeline().composer.log("Feature ON", is_template=False).done()
feature_off_step = Pipeline().composer.log("Feature OFF", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .if_else(
        condition=lambda s: s["flag"],           # truthy -> if_branch
        if_branch=feature_on_step,
        else_branch=feature_off_step,
        output_state="feature_status",           # stores "true"/"false"
    )
    .done()
)
```

As with the functional `if_else()`, the condition could also be a `Component`. In this case, you need to pass an `input_map`:

```python
from gllm_pipeline.pipeline import Pipeline

# Branches: produce constant messages via Val (Echo returns 'x' unchanged)
from gllm_pipeline.types import Val

grant_access = Pipeline().composer.step(Echo(), {"x": Val("Access granted")}, "decision").done()
deny_access = Pipeline().composer.step(Echo(), {"x": Val("Access denied")}, "decision").done()

# Condition: a Component that returns "true" or "false"
# Echo will return the state value at key "is_adult" (must be "true" or "false")
pipeline = (
    Pipeline()
    .composer
    .if_else(
        condition=Echo(),                      # Component condition
        if_branch=grant_access,                # runs when condition returns "true"
        else_branch=deny_access,               # runs when condition returns "false"
        input_map={"x": "is_adult"},           # map state -> component input
        output_state="condition_result",       # optional: persist "true"/"false"
    )
    .done()
)
```

#### switch

The `switch` method selects a branch from a dict of options based on a condition output (string). Supports both builder-style and direct-style patterns.

**Builder-style: switch().case().default().end()**

```python
from gllm_pipeline.pipeline import Pipeline

search_step = Pipeline().composer.log("Searching...", is_template=False).done()
filter_step = Pipeline().composer.log("Filtering...", is_template=False).done()
unknown_step = Pipeline().composer.log("Unknown command", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .switch(lambda s: s["command"])        # e.g., "search", "filter"
        .case("search", search_step)
        .case("filter", filter_step)
        .default(unknown_step)
        .end()
    .done()
)
```

**Direct-style: switch()**

```python
from gllm_pipeline.pipeline import Pipeline

search_step = Pipeline().composer.log("Searching...", is_template=False).done()
filter_step = Pipeline().composer.log("Filtering...", is_template=False).done()
unknown_step = Pipeline().composer.log("Unknown command", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .switch(
        condition=lambda s: s["command"],        # e.g., "search", "filter"
        branches={
            "search": search_step,
            "filter": filter_step,
        },
        default=unknown_step,
        output_state="command_type",
    )
    .done()
)
```

#### toggle

The `toggle` method runs its `if_branch` if condition is true; otherwise behaves like `no_op()`. Condition can be callable, `Component`, or a string key looked up in merged state/config.

This method is useful to enable "optional" steps that are decided at runtime.

**Builder-style: toggle().then().end()**

```python
from gllm_pipeline.pipeline import Pipeline

feature_step = Pipeline().composer.log("Feature executed", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .toggle("feature_enabled")             # truthy in state/config?
        .then(feature_step)
        .end()
    .done()
)
```

**Direct-style: toggle()**

```python
from gllm_pipeline.pipeline import Pipeline

feature_step = Pipeline().composer.log("Feature executed", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .toggle(
        condition="feature_enabled",             # truthy in state/config?
        if_branch=feature_step,
        output_state="feature_status",
    )
    .done()
)
```

#### guard

The `guard` method evaluates a condition. On success runs `success_branch`. On failure runs `failure_branch`, then terminates the _current_ Pipeline.

**Builder-style: guard().on\_success().on\_failure().end()**

```python
from gllm_pipeline.pipeline import Pipeline

welcome_step = Pipeline().composer.log("Welcome!", is_template=False).done()
access_denied_step = Pipeline().composer.log("Access denied!", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .guard(lambda s: s.get("is_authenticated", False))
        .on_success(welcome_step)
        .on_failure(access_denied_step)
        .end()
    .done()
)
```

**Direct-style: guard()**

```python
from gllm_pipeline.pipeline import Pipeline

welcome_step = Pipeline().composer.log("Welcome!", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .guard(
        condition=lambda s: s.get("is_authenticated", False),
        success_branch=welcome_step,
        output_state="auth_result",
    )
    .done()
)
```

### Concurrency

The Composer provides methods for parallel execution and map-reduce operations.

#### parallel

The `parallel` method runs multiple branches in parallel and merges results. Each branch can be a step or a list of steps.

**Builder-style: parallel().fork().end()**

```python
from gllm_pipeline.pipeline import Pipeline

step_a = Pipeline().composer.log("A", is_template=False).done()
step_b = Pipeline().composer.log("B", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .parallel()
        .fork(step_a)
        .fork(step_b)
        .end()
    .done()
)
```

**Direct-style: parallel()**

```python
from gllm_pipeline.pipeline import Pipeline

step_a = Pipeline().composer.log("A", is_template=False).done()
step_b = Pipeline().composer.log("B", is_template=False).done()

pipeline = (
    Pipeline()
    .composer
    .parallel(
        branches=[step_a, step_b],
    )
    .done()
)
```

#### map\_reduce

The `map_reduce` method maps a function (or Component) over multiple items, then reduces results. This is the composer equivalent of the `map_reduce()` function.

By default, iterable values in `input_map` are used for fan-out. To preserve an iterable as a single grouped input in every mapped item, wrap it with `Group(...)`.

{% code lineNumbers="true" expandable="true" %}
```python
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.types import Group

sum_pipeline = (
    Pipeline()
    .composer
    .map_reduce(
        input_map={"n": "numbers"},              # numbers is a list in state
        output_state="total",
        map_func=lambda item: item["n"],         # returns each number
        reduce_func=sum,                         # sums the list of results
    )
    .done()
)

rank_pipeline = (
    Pipeline()
    .composer
    .map_reduce(
        input_map={
            "query": "queries",
            "candidate_pool": Group("candidate_groups"),  # preserve full list per query
        },
        output_state="ranked",
        map_func=lambda item: {
            "query": item["query"],
            "best": item["candidate_pool"][0],
        },
    )
    .done()
)
```
{% endcode %}

### Composition

#### subgraph

The `subgraph` method executes another `Pipeline` as a step, with flexible input/output mapping. This is the composer equivalent of the `subgraph()` function.

```python
from gllm_pipeline.pipeline import Pipeline

# sub_pipeline is a Pipeline you built elsewhere
step_a = Pipeline().composer.log("Step A", is_template=False).done()
step_b = Pipeline().composer.log("Step B", is_template=False).done()
step_c = Pipeline().composer.log("Step C", is_template=False).done()

sub_pipeline = (
    Pipeline()
    .composer
    .step(step_a)
    .step(step_b)
    .step(step_c)
    .done()
)

pipeline = (
    Pipeline()
    .composer
    .subgraph(
        subgraph=sub_pipeline,
        input_map={"query": "user_query"},
        output_state_map={"result": "subgraph_result"},
    )
    .done()
)
```

### Complete Example

Here's a comprehensive example showing how to use the Composer to build a complete RAG pipeline:

```python
from gllm_pipeline.pipeline import Pipeline
from gllm_core.schema.component import Component

# Assume we have these components defined
class Retriever(Component):
    async def _run(self, **kwargs):
        # Retrieval logic here
        return {"documents": ["doc1", "doc2"]}

class Generator(Component):
    async def _run(self, **kwargs):
        # Generation logic here
        return {"response": "Generated response"}

class Validator(Component):
    async def _run(self, **kwargs):
        # Validation logic here
        return kwargs["response"].startswith("Generated")

# Build the pipeline using the Composer
retriever = Retriever()
generator = Generator()
validator = Validator()

def format_context(data: dict) -> str:
    return " ".join(data["documents"])

pipeline = (
    Pipeline()
    .composer
    .log("Starting RAG pipeline for query: {query}")
    .step(
        component=retriever,
        input_map={"query": "query"},
        output_state="retrieval_result"
    )
    .transform(
        operation=format_context,
        input_map=["documents"],
        output_state="context"
    )
    .bundle(
        input_states=["query", "context"],
        output_state="generation_input"
    )
    .step(
        component=generator,
        input_map={"input": "generation_input"},
        output_state="response"
    )
    .when(lambda s: s.get("validate_response", True))
    .then(
        Pipeline()
        .composer
        .step(
            component=validator,
            input_map={"response": "response"},
            output_state="is_valid"
        )
        .guard(lambda s: s["is_valid"])
        .on_success(
            Pipeline().composer.log("Response validated successfully").done()
        )
        .on_failure(
            Pipeline().composer.log("Response validation failed").terminate().done()
        )
        .end()
        .done()
    )
    .end()
    .log("RAG pipeline completed. Response: {response}")
    .done()
)

# Execute the pipeline
result = await pipeline.invoke({"query": "What is machine learning?"})
print(result["response"])
```

This example demonstrates:

* Basic steps (`step`, `log`, `transform`, `bundle`)
* Conditional logic (`when().then().end()`, `guard()`)
* Fluent chaining of multiple operations
* Clean, readable pipeline definition using the Composer API

The Composer provides a powerful and expressive way to build complex pipelines while maintaining readability and flexibility.
