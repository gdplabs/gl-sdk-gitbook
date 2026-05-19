---
icon: binary-slash
---

# Error Handling

Error handling in the Pipeline SDK provides robust mechanisms to gracefully handle failures during step execution. Each step can be configured with an **error handling strategy** that determines how errors are processed and what happens to the pipeline state when failures occur.

By default, all steps use the **Raise** strategy, which re-raises exceptions with enhanced context information. This is the strictest approach and ensures that errors immediately stop pipeline execution with detailed error messages.

```python
from gllm_pipeline.steps._func import transform
from gllm_pipeline.steps.step_error_handler import RaiseStepErrorHandler

def may_fail(data: dict) -> str:
    if not data.get("valid"):
        raise ValueError("Invalid input")
    return data["text"].upper()

# By default, errors will be raised with context
step = transform(
    may_fail,
    input_map=["text", "valid"],
    output_state="result",
    # error_handler=RaiseStepErrorHandler()  # 👈 This is the default
)
```

When an error occurs, you'll get enhanced error messages like:

```
Error in Transform 'Transform_may_fail__abc123' during execution.
Error type: ValueError. Original error: Invalid input
```

{% hint style="info" %}
This default behavior is suitable for most production use cases where you want to catch and handle errors explicitly rather than silently continuing with potentially corrupted state.
{% endhint %}

## Error Handling Strategies

The SDK provides four built-in error handling strategies, each designed for different use cases.

### Raise (Default)

Re-raises the exception with enhanced context. The pipeline stops immediately and the error is propagated to the caller.

**When to use:**

1. Production pipelines where data integrity is critical
2. When you want to catch and handle errors explicitly in your application code
3. When you need detailed error information for debugging

**Example:**

```python
from gllm_pipeline.steps.step_error_handler import RaiseStepErrorHandler
from gllm_pipeline.steps._func import transform

def strict_operation(data: dict) -> str:
    result = data["value"] / data["divisor"]  # May raise ZeroDivisionError
    return str(result)

step = transform(
    strict_operation,
    input_map=["value", "divisor"],
    output_state="result",
    error_handler=RaiseStepErrorHandler(),  # Explicitly set (though this is default)
)
```

### Keep

Preserves the current state without modification when an error occurs. The step is skipped and the pipeline continues with the next step.

**When to use:**

1. When a step is optional and failures can be safely ignored
2. When you want to continue processing even if some steps fail
3. For non-critical enrichment steps

**Example:**

```python
from gllm_pipeline.steps.step_error_handler import KeepStepErrorHandler
from gllm_pipeline.steps._func import transform

def optional_enhancement(data: dict) -> str:
    # This might fail, but it's okay - we can continue without it
    return external_api_call(data["text"])

step = transform(
    optional_enhancement,
    input_map=["text"],
    output_state="enhanced_text",
    error_handler=KeepStepErrorHandler(),  # Continue on error
)
```

### Empty

Sets the output state(s) to `None` when an error occurs, then continues execution.

**When to use:**

1. When you want to explicitly mark that a step failed while continuing
2. When downstream steps can handle `None` values gracefully
3. For conditional processing based on whether a step succeeded

**Example:**

```python
from gllm_pipeline.steps.step_error_handler import EmptyStepErrorHandler
from gllm_pipeline.steps._func import transform

def risky_extraction(data: dict) -> str:
    # Extract data from unreliable source
    return parse_complex_format(data["raw_data"])

step = transform(
    risky_extraction,
    input_map=["raw_data"],
    output_state="extracted_data",
    error_handler=EmptyStepErrorHandler(output_state="extracted_data"),
)

# Later step can check if extraction succeeded
def process_if_available(data: dict) -> str:
    if data["extracted_data"] is None:
        return "Extraction failed, using fallback"
    return f"Processed: {data['extracted_data']}"
```

### Fallback

Executes a custom fallback function when an error occurs. This is the most flexible approach, allowing you to define custom recovery logic.

**When to use:**

1. When you have a specific fallback behavior for failures
2. When you want to log errors and provide default values
3. For graceful degradation with alternative processing

**Example:**

```python
from gllm_pipeline.steps.step_error_handler import FallbackStepErrorHandler
from gllm_pipeline.steps._func import transform

def primary_processor(data: dict) -> str:
    # Try to use advanced processing
    return advanced_llm_call(data["query"])

def fallback_logic(error, state, runtime, context):
    # Log the error
    print(f"Primary processor failed: {error}")
    # Return a safe fallback
    return {"response": "I apologize, but I'm having trouble processing your request right now."}

step = transform(
    primary_processor,
    input_map=["query"],
    output_state="response",
    error_handler=FallbackStepErrorHandler(fallback=fallback_logic),
)
```

## Error Context

When an error occurs, the SDK automatically captures detailed context information using the `ErrorContext` model. This context includes:

* **exception**: The original exception that was raised
* **step\_name**: The name of the step where the error occurred
* **step\_type**: The type of step (e.g., "Transform", "Conditional")
* **state**: The pipeline state at the time of the error
* **operation**: Description of the operation being performed
* **additional\_context**: Any additional context information

This context is automatically included in error messages and passed to error handlers, making debugging much easier.

## Best Practices

#### 1. Choose the Right Strategy

* **Use `Raise`** by default for production pipelines
* **Use `Keep`** for truly optional steps that will not affect downstream processing
* **Use `Empty`** when downstream steps need to know a step failed
* **Use `Fallback`** for graceful degradation with alternative logic

#### 2. Handle Errors at the Right Level

```python
# ❌ Bad: Catching errors inside step logic
def bad_step(data: dict) -> str:
    try:
        return risky_operation(data["input"])
    except Exception:
        return "fallback"  # Lost error context

# ✅ Good: Let the error handler manage it
def good_step(data: dict) -> str:
    return risky_operation(data["input"])

# Configure with appropriate error handler
step = transform(
    good_step,
    input_map=["input"],
    output_state="output",
    error_handler=FallbackStepErrorHandler(
        fallback=lambda err, state, rt, ctx: {"output": "fallback"}
    ),
)
```

#### 3. Validate Critical Data Early

```python
# Validate at pipeline entry with strict error handling
validation_step = transform(
    validate_input,
    input_map=["user_input"],
    output_state="validated_input",
    error_handler=RaiseStepErrorHandler(),  # Fail fast
)
```

#### 4. Document Error Behavior

```python
# Clear documentation helps maintainers understand error handling
step = transform(
    unreliable_api_call,
    input_map=["query"],
    output_state="api_result",
    error_handler=KeepStepErrorHandler(),  # API failures are non-critical
    name="optional_api_enhancement",
)
```

{% hint style="warning" %}
**Be cautious with silent error handling**: Using `Keep` or `Empty` can hide problems. Always ensure that downstream steps can handle missing or `None` values gracefully.
{% endhint %}

By choosing the appropriate error handling strategy for each step, you can build resilient pipelines that gracefully handle failures while maintaining data integrity.
