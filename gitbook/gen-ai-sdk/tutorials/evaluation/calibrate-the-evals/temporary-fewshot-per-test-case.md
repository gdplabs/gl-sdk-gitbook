# Temporary Fewshot Per Test Case Guide

## Why Temporary Fewshot?

A well-calibrated metric can show high alignment with human judgment on one dataset but degrade on another. For example, a completeness metric tuned on general Q&A expects verbose, explanatory answers. When the same metric evaluates legal-domain responses — which are terse and factual by convention — it may flag correct answers as "incomplete" because the response style differs from what the judge was calibrated to expect.

The obvious fix — forking the metric per domain — creates a maintenance burden. Each fork (`CompletenessMetric_Legal`, `CompletenessMetric_Medical`, `CompletenessMetric_Finance`) requires independent calibration. A change to the base evaluation logic must be propagated across every variant. This is **metric proliferation**: N metrics where one should suffice, each with its own calibration drift risk.

The alternative is to scope fewshot guidance to the evaluation call rather than the metric definition. Instead of embedding domain-specific examples into the metric at creation time, pass them at `evaluate()` time via temporary parameters. After the call completes, the metric is unchanged — ready for the next dataset with different (or no) temporary guidance.

This is what `temp_fewshot`, `temp_info`, and `fewshot_mode` enable:

* **Per-call example injection** — guide the judge for specific domains or edge cases without mutating the base metric
* **Contextual hints** — supply domain rules, compliance standards, or audience expectations as supplementary instructions
* **Configurable merge behavior** — append to the base prompt or replace it entirely
* **No metric proliferation** — a single calibrated metric instance handles multiple evaluation scenarios

{% hint style="info" %}
Runtime parameters are temporary — they do not modify the original metric instance. After `evaluate()` returns, the metric is unchanged and ready for the next call with different (or no) temporary guidance.
{% endhint %}

## Available Parameters

The `evaluate()` method supports three runtime parameters:

| Parameter      | Type                           | Default    | Description                              |
| -------------- | ------------------------------ | ---------- | ---------------------------------------- |
| `temp_fewshot` | `str \| None`                  | `None`     | Few-shot examples to guide the evaluator |
| `temp_info`    | `str \| None`                  | `None`     | Additional context or instructions       |
| `fewshot_mode` | `Literal["append", "replace"]` | `"append"` | How to merge with existing context       |

### Parameter Priority

Runtime parameters follow this priority order:

1. **Runtime parameters** (highest priority) - passed to `evaluate()`
2. **CSV-level prompts** - defined in dataset rows
3. **Initialization parameters** (lowest priority) - set during metric creation

## Fewshot Modes

{% tabs %}
{% tab title="Append Mode (Default)" %}
Adds runtime examples to existing metric context without replacing it.

**Use case:** When you want to supplement the base context with additional examples

```python
result = await metric.evaluate(
    data,
    temp_fewshot="Example: ...",
    fewshot_mode="append"  # Default behavior
)
```
{% endtab %}

{% tab title="Replace Mode" %}
Replaces existing metric context entirely with runtime examples.

**Use case:** When you need completely different evaluation criteria for specific cases

```python
result = await metric.evaluate(
    data,
    temp_fewshot="Example: ...",
    fewshot_mode="replace"  # Override existing context
)
```
{% endtab %}
{% endtabs %}

## Getting Started

{% stepper %}
{% step %}
**Import Required Modules**

```python
import asyncio
import os
from gllm_evals.metrics.generation import GEvalCompletenessMetric
from gllm_evals.types import LLMTestCase
```
{% endstep %}

{% step %}
**Initialize Your Metric**

Create a metric with base configuration. The `additional_context` parameter sets the default context.

```python
metric = GEvalCompletenessMetric(
    model_credentials=os.getenv("GOOGLE_API_KEY"),
)
```
{% endstep %}

{% step %}
**Prepare Your Test Data**

```python
data = LLMTestCase(
    input="What are the benefits of exercise?",
    actual_output="Exercise improves health.",
    expected_output="Exercise improves cardiovascular health, builds muscle, "
    "enhances mental well-being, and helps maintain healthy weight.",
)
```
{% endstep %}

{% step %}
**Run Evaluation with Runtime Parameters**

```python
result = await metric.evaluate(
    data,
    temp_fewshot="""Example:
        Input: What are the benefits of exercise?
        Actual Output: Exercise improves health.
        Expected Output: Exercise improves cardiovascular health, builds muscle,
        enhances mental well-being, and helps maintain healthy weight.
        Score: 1.
        Reason: The response covers all key points from the expected output.
    """,
    fewshot_mode="append"
)
print(f"Score: {result['completeness']}")
```
{% endstep %}
{% endstepper %}

## Usage Examples

### Example 1: Using temp\_fewshot (Append Mode)

Add examples to guide the evaluator while keeping the base context.

```python
async def fewshot_append_mode():
    metric = GEvalCompletenessMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        additional_context="Evaluate how complete the response is.",
    )

    data = LLMTestCase(
        input="What are the benefits of exercise?",
        actual_output="Exercise improves health.",
        expected_output="Exercise improves cardiovascular health, builds muscle, "
        "enhances mental well-being, and helps maintain healthy weight.",
    )

    result = await metric.evaluate(
        data,
        temp_fewshot="""Example:
            Input: What are the benefits of exercise?
            Actual Output: Exercise improves health.
            Expected Output: Exercise improves cardiovascular health, builds muscle,
            enhances mental well-being, and helps maintain healthy weight.
            Score: 1.
            Reason: The response covers all key points from the expected output.
        """,
        fewshot_mode="append"  # Adds to existing context
    )
    print(f"Score: {result['completeness']}")
```

### Example 2: Using temp\_info Only

Add domain-specific context without examples.

```python
async def temp_info_only():
    metric = GEvalCompletenessMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        additional_context="Evaluate how complete the response is.",
    )

    data = LLMTestCase(
        input="What are the benefits of exercise?",
        actual_output="Exercise improves health.",
        expected_output="Exercise improves cardiovascular health, builds muscle, "
        "enhances mental well-being, and helps maintain healthy weight.",
    )

    result = await metric.evaluate(
        data,
        temp_info="Domain: Health & Fitness\nAudience: General public"
    )
    print(f"Score: {result['completeness']}")
```

### Example 3: Combining temp\_fewshot and temp\_info

Provide both examples and contextual information for comprehensive guidance.

```python
async def combined_params():
    metric = GEvalCompletenessMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        additional_context="Evaluate how complete the response is.",
    )

    data = LLMTestCase(
        input="What are the benefits of exercise?",
        actual_output="Exercise improves health.",
        expected_output="Exercise improves cardiovascular health, builds muscle, "
        "enhances mental well-being, and helps maintain healthy weight.",
    )

    result = await metric.evaluate(
        data,
        temp_fewshot="""Example:
            Input: What are the benefits of exercise?
            Actual Output: Exercise improves health.
            Expected Output: Exercise improves cardiovascular health, builds muscle,
            enhances mental well-being, and helps maintain healthy weight.
            Score: 1.
            Reason: The response covers all key points from the expected output.
        """,
        temp_info="Domain: Healthcare\nCompliance: Medical accuracy required",
        fewshot_mode="append"
    )
    print(f"Score: {result['completeness']}")
```

## Complete Example

Here's a complete, runnable example demonstrating all usage patterns:

```python
"""Example: Runtime fewshot parameters usage.


This example demonstrates how to use temp_fewshot, temp_info, and fewshot_mode
parameters in the evaluate() method.
"""


import asyncio
import os


from gllm_evals.metrics.generation import GEvalCompletenessMetric
from gllm_evals.types import LLMTestCase




async def main():
    """Demonstrate runtime fewshot parameters."""
    # Initialize metric with base context
    metric = GEvalCompletenessMetric(
        model_credentials=os.getenv("GOOGLE_API_KEY"),
        additional_context="Evaluate how complete the response is.",
    )


    # Sample data
    data = LLMTestCase(
        input="What are the benefits of exercise?",
        actual_output="Exercise improves health.",
        expected_output="Exercise improves cardiovascular health, builds muscle, "
        "enhances mental well-being, and helps maintain healthy weight.",
    )


    # Example 1: Basic evaluation without runtime params
    print("Example 1: Without runtime parameters")
    result1 = await metric.evaluate(data)
    print(f"Score: {result1['completeness']}\n")


    # Example 2: With temp_fewshot (append mode - default)
    print("Example 2: With temp_fewshot (append mode)")
    result2 = await metric.evaluate(
        data,
        temp_fewshot="""Example:
            Input: What are the benefits of exercise?
            Actual Output: Exercise improves health.
            Expected Output: Exercise improves cardiovascular health, builds muscle,
            enhances mental well-being, and helps maintain healthy weight.
            Score: 1.
            Reason: The response covers all key points from the expected output.
        """,
        fewshot_mode="append",  # Adds to existing context
    )
    print(f"Score: {result2['completeness']}\n")


    # Example 3: With temp_fewshot (replace mode)
    print("Example 3: With temp_fewshot (replace mode)")
    result3 = await metric.evaluate(
        data,
        temp_fewshot="""Example:
            Input: What are the benefits of exercise?
            Actual Output: Exercise improves health.
            Expected Output: Exercise improves cardiovascular health, builds muscle,
            enhances mental well-being, and helps maintain healthy weight.
            Score: 1.
            Reason: The response covers all key points from the expected output.
        """,
        fewshot_mode="replace",  # Replaces existing context
    )
    print(f"Score: {result3['completeness']}\n")


    # Example 4: With temp_info only
    print("Example 4: With temp_info")
    result4 = await metric.evaluate(
        data,
        temp_info="Domain: Health & Fitness\nAudience: General public"
    )
    print(f"Score: {result4['completeness']}\n")


    # Example 5: With both temp_fewshot and temp_info
    print("Example 5: With both temp_fewshot and temp_info")
    result5 = await metric.evaluate(
        data,
        temp_fewshot="""Example:
            Input: What are the benefits of exercise?
            Actual Output: Exercise improves health.
            Expected Output: Exercise improves cardiovascular health, builds muscle,
            enhances mental well-being, and helps maintain healthy weight.
            Score: 1.
            Reason: The response covers all key points from the expected output.
        """,
        temp_info="Domain: Healthcare\nCompliance: Medical accuracy required",
        fewshot_mode="append",
    )
    print(f"Score: {result5['completeness']}\n")


    # Verify original metric unchanged
    print("✓ Original metric context unchanged:", metric.additional_context)




if __name__ == "__main__":
    asyncio.run(main())
```

## Best Practices

### 1. Use Append Mode for Supplemental Examples

When your base metric already has good context, use `append` mode to add scenario-specific examples.

### 2. Use Replace Mode for Different Domains

When evaluating completely different types of content, use `replace` mode.

### 3. Combine temp\_fewshot and temp\_info

Provide both examples and context for optimal results.

### 4. Keep Examples Concise and Relevant

Write clear, focused examples that match your evaluation scenario.

```python
# Good: Clear, concise example
temp_fewshot = """Example:
    Input: Query text
    Actual Output: Response text
    Expected Output: Ideal response
    Score: 3
    Reason: Specific reason for the score
"""
```

## Common Use Cases

### Domain-Specific Evaluation

Adapt metrics for different domains without creating separate metric instances.

```python
# Healthcare domain
healthcare_result = await metric.evaluate(
    healthcare_data,
    temp_info="Domain: Healthcare\nStandard: HIPAA compliant",
    temp_fewshot="Medical response examples..."
)


# Legal domain (same metric, different context)
legal_result = await metric.evaluate(
    legal_data,
    temp_info="Domain: Legal\nStandard: Contract law",
    temp_fewshot="Legal response examples..."
)
```

### A/B Testing Evaluation Criteria

Test different evaluation approaches on the same data.

```python
# Test with stricter criteria
strict_result = await metric.evaluate(
    data,
    temp_fewshot="Strict evaluation examples...",
    fewshot_mode="replace"
)


# Test with lenient criteria
lenient_result = await metric.evaluate(
    data,
    temp_fewshot="Lenient evaluation examples...",
    fewshot_mode="replace"
)
```

### Audience-Specific Evaluation

Adjust evaluation based on target audience.

```python
# Technical audience
tech_result = await metric.evaluate(
    data,
    temp_info="Audience: Technical experts\nExpectation: Detailed technical accuracy"
)


# General audience
general_result = await metric.evaluate(
    data,
    temp_info="Audience: General public\nExpectation: Simple, clear explanations"
)
```
