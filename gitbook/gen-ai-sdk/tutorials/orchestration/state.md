---
icon: ballot-check
---

# State

A **State** is the shared data dictionary that flows through your Pipeline. A State is currently defined as a `TypedDict`, so keys and value types are explicit. Each step reads from and writes to the **State** as it executes.

## Default State: `RAGState`

By default, a Pipeline in our SDK is equipped with `RAGState` as it state, which is defined in `gllm_pipeline.pipeline.states`. The state keys are based on the keys that you might find in an Retrieval-Augmented Generation (RAG) pipeline. It is also equipped with a special state key for an `EventEmitter` for streaming purposes.

```python
class RAGState(TypedDict):
    user_query: str
    queries: list[str]
    retrieval_params: dict[str, Any]
    chunks: list
    history: str
    context: str
    response: str
    references: str | list[str]
    event_emitter: EventEmitter
```

{% hint style="warning" %}
During Pipeline definition, you _must_ ensure that your output state belongs to one of the pre-defined state keys.
{% endhint %}

## Defining a Custom State

The default `RAGState` may not be suitable for your purposes. For example, when defining a Subgraph, you may not need all of the keys. In contrast, there may be some additional state keys that you require. In these cases, you can define **your own state structure**.

To do so:

{% stepper %}
{% step %}
**Create state class**

Define a `TypedDict` . This can be in the same file as the Pipeline or in a different module.

{% code title="my_state.py" %}
```python
from typing import TypedDict, Any
from gllm_core.event.event_emitter import EventEmitter

class MyCustomState(TypedDict):
    user_query: str
    chunks: list
    context: str
    response: str
    document_scores: list[float]  # not in RAGState
    debug_info: dict[str, Any]   # not in RAGState
    event_emitter: EventEmitter
```
{% endcode %}
{% endstep %}

{% step %}
**Apply to pipeline**

Pass the `TypedDict` into the `state_type` argument when creating the Pipeline.

```python
from my_state import MyCustomState
from gllm_pipeline.pipeline import Pipeline

pipeline = Pipeline(
    steps=[
        retriever_step,
        response_synthesizer_step
    ],
    state_type=MyCustomState # 👈 custom field
)
```
{% endstep %}
{% endstepper %}

## Using a Pydantic BaseModel as a State

In addition to `TypedDict`, you can also use a **Pydantic `BaseModel`** as your state. This provides runtime validation, default values, and enhanced type safety compared to `TypedDict`. The SDK includes `RAGStateModel` as a Pydantic alternative to `RAGState`.

To use a Pydantic `BaseModel` as your state:

{% stepper %}
{% step %}
**Create state class**

Define a Pydantic `BaseModel`. This can be in the same file as the Pipeline or in a different module.

{% code title="my:state.py" %}
```python
from typing import Any
from pydantic import BaseModel, Field, ConfigDict
from gllm_core.event.event_emitter import EventEmitter

class MyCustomStateModel(BaseModel):
    user_query: str = Field(..., description="The original query from the user")
    chunks: list = Field(default_factory=list, description="Retrieved chunks")
    context: str = Field(default="", description="Context information")
    response: str = Field(default="", description="Generated response")
    document_scores: list[float] = Field(default_factory=list, description="Document relevance scores")
    debug_info: dict[str, Any] = Field(default_factory=dict, description="Debug information")
    event_emitter: EventEmitter | None = Field(default=None, description="Event emitter for logging")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={
            EventEmitter: lambda v: str(v) if v else None,
        },
    )
```
{% endcode %}
{% endstep %}

{% step %}
**Apply to pipeline**

Pass the Pydantic `BaseModel` into the `state_type` argument when creating the Pipeline.

```python
from my_state import MyCustomStateModel
from gllm_pipeline.pipeline import Pipeline

pipeline = Pipeline(
    steps=[
        retriever_step,
        response_synthesizer_step
    ],
    state_type=MyCustomStateModel # 👈 Pydantic BaseModel
)
```
{% endstep %}
{% endstepper %}

Pydantic `BaseModel` comes with the following benefits:

1. **Runtime validation**: Automatic type checking and validation.
2. **Default values**: Use `Field(default=...)` or `Field(default_factory=...)` for defaults.
3. **Enhanced type safety**: Better IDE support and error messages.
4. **Custom validation**: Add validators using `@field_validator` or `@model_validator`.
5. **JSON serialization**: Built-in `model_dump()` and `model_dump_json()` methods.
