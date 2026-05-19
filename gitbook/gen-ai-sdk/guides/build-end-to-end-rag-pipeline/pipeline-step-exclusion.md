---
icon: align-justify
---

# Pipeline Step Exclusion

This guide will walk you through implementing **step exclusion** in your AI pipelines to selectively disable specific steps or branches during execution. We'll explore how step exclusion can help you create flexible, configurable pipelines that can adapt to different scenarios without requiring separate pipeline definitions.

{% hint style="info" %}
This tutorial builds upon basic pipeline concepts. Ensure you understand sequential and parallel pipeline construction before implementing step exclusion patterns.
{% endhint %}

{% hint style="warning" %}
**Important Note:** The pipeline components used in this tutorial (DocumentExtractor, SentimentAnalyzer, etc.) are simplified examples for demonstration purposes. In practice, you would replace these with your actual component implementations. This guide focuses on step exclusion patterns rather than component implementation details.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of the [Your First RAG Pipeline](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline) tutorial - understanding of basic pipeline construction
2. Completion of all setup steps listed on the [Prerequisites](https://gdplabs.gitbook.io/sdk/overview/prerequisites) page

You should be familiar with these concepts and components:

1. Components in [Your First RAG Pipeline prerequisites](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline#prerequisites) - **Required foundation**
2. [#parallel](../../tutorials/orchestration/steps/#parallel "mention")step

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

***

## Project Setup

{% stepper %}
{% step %}
**Project Structure**

Create your project structure for parallel pipeline implementation:

```
pipeline-step-exclusion/
├── .env.example
├── pipeline.py
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```
{% endstep %}
{% endstepper %}

## Understanding Step Exclusion

Step exclusion is a powerful feature that allows you to selectively disable specific steps or branches within your pipeline during execution. This is particularly useful for:

* **A/B Testing**: Compare different processing paths without creating separate pipelines
* **Debugging**: Temporarily disable problematic steps to isolate issues
* **Feature Flags**: Enable/disable features dynamically based on configuration
* **Performance Optimization**: Skip expensive operations when not needed
* **Conditional Processing**: Adapt pipeline behavior based on runtime conditions

The exclusion system uses dot-notation paths to identify specific steps or branches:

* **Simple Steps**: `"step_name"` - Excludes the entire step
* **Parallel Branches**: `"parallel_step.branch_name"` - Excludes a specific parallel branch
* **Conditional Branches**: `"conditional_step.true"` or `"conditional_step.false"` - Excludes a conditional branch
* **Nested Steps**: `"parent_step.child_step"` - Excludes a child step within a composite step

***

## Example

### Basic Use

Let's start with a basic document processing pipeline:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step

# Create a simple document processing pipeline
pipeline = Pipeline([
    step(DocumentExtractor(), {"document": "input_document"}, "extracted_text", name="extract"),
    step(SentimentAnalyzer(), {"text": "extracted_text"}, "sentiment_score", name="sentiment"),
    step(TopicDetector(), {"text": "extracted_text"}, "detected_topics", name="topics"),
    step(ReportGenerator(), {
        "sentiment": "sentiment_score",
        "topics": "detected_topics"
    }, "analysis_report", name="report")
])

# Execute with all steps
result = await pipeline.invoke({"input_document": "Sample document content"})
print("Full pipeline result:", result)

# Exclude the sentiment analysis step
pipeline.exclusions.exclude("sentiment")
result_no_sentiment = await pipeline.invoke({"input_document": "Sample document content"})
print("Without sentiment:", result_no_sentiment)
# Note: sentiment_score will not be present in the result
```
{% endcode %}

### Step Exclusion for Conditional Step

For conditional processing, you can exclude entire branches:

```python
from gllm_pipeline.steps import if_else

# Create a pipeline with conditional processing
pipeline = Pipeline([
    step(DocumentExtractor(), {"document": "input_document"}, "extracted_text", name="extract"),

    if_else(
        condition=lambda state: len(state["extracted_text"]) > 100,
        if_branch=[
            step(DetailedAnalyzer(), {"text": "extracted_text"}, "detailed_analysis", name="detailed"),
            step(SummaryGenerator(), {"analysis": "detailed_analysis"}, "summary", name="summary")
        ],
        else_branch=[
            step(QuickAnalyzer(), {"text": "extracted_text"}, "quick_analysis", name="quick")
        ],
        name="conditional_analysis"
    ),

    step(ReportGenerator(), {
        "analysis": "detailed_analysis",  # or "quick_analysis"
        "summary": "summary"  # may not exist if else branch runs
    }, "final_report", name="report")
])

# Exclude the detailed analysis branch (true branch)
pipeline.exclusions.exclude("conditional_analysis.true")
# Now only the quick analysis will run regardless of text length
```

### Step Exclusion for Complex Pipeline Structures

For complex pipeline structures, you can exclude deeply nested steps:

```python
# Exclude a specific step within a parallel branch
pipeline.exclusions.exclude("analysis_parallel.sentiment.sentiment_step")

# Exclude a step within a conditional branch
pipeline.exclusions.exclude("conditional_analysis.true.detailed")

# Exclude multiple nested steps
pipeline.exclusions.exclude(
    "analysis_parallel.sentiment",
    "conditional_analysis.false.quick",
    "report"
)
```

### Dynamic Pipeline using Step Exclusion

You can dynamically manage exclusions based on runtime conditions:

```python
def create_adaptive_pipeline(user_preferences, debug_mode=False):
    """Create a pipeline with exclusions based on user preferences and debug mode."""

    pipeline = Pipeline([
        step(DocumentExtractor(), {"document": "input_document"}, "extracted_text", name="extract"),
        step(SentimentAnalyzer(), {"text": "extracted_text"}, "sentiment_score", name="sentiment"),
        step(TopicDetector(), {"text": "extracted_text"}, "detected_topics", name="topics"),
        step(EntityExtractor(), {"text": "extracted_text"}, "named_entities", name="entities"),
        step(LanguageDetector(), {"text": "extracted_text"}, "language_info", name="language"),
        step(ReportGenerator(), {
            "sentiment": "sentiment_score",
            "topics": "detected_topics",
            "entities": "named_entities",
            "language": "language_info"
        }, "analysis_report", name="report")
    ])

    # Apply exclusions based on user preferences
    exclusions = []

    if not user_preferences.get("include_sentiment", True):
        exclusions.append("sentiment")

    if not user_preferences.get("include_entities", True):
        exclusions.append("entities")

    if debug_mode:
        # In debug mode, skip expensive operations
        exclusions.extend(["topics", "language"])

    if exclusions:
        pipeline.exclusions.exclude(*exclusions)

    return pipeline

# Usage
user_prefs = {"include_sentiment": False, "include_entities": True}
pipeline = create_adaptive_pipeline(user_prefs, debug_mode=True)
result = await pipeline.invoke({"input_document": "Sample content"})
```

### Step Exclusion Lifecycle

You can manage exclusion state throughout the pipeline lifecycle:

```python
# Start with a full pipeline
pipeline = create_full_pipeline()

# Check current exclusions
print("Current exclusions:", pipeline.exclusions.get_current_exclusions())
print("Excluded steps:", pipeline.exclusions.list_excluded())

# Apply exclusions
pipeline.exclusions.exclude("sentiment", "topics")
print("After exclusion:", pipeline.exclusions.get_current_exclusions())

# Include some steps back (remove from exclusions)
pipeline.exclusions.include("sentiment")
print("After including sentiment:", pipeline.exclusions.get_current_exclusions())

# Clear all exclusions
pipeline.exclusions.clear()
print("After clearing:", pipeline.exclusions.get_current_exclusions())
```

***

Congratulations! You've successfully learned how to implement step exclusion in your AI pipelines. By strategically applying step exclusion, you can create flexible, configurable pipelines that adapt to different scenarios without requiring separate pipeline definitions. Your pipelines will now support dynamic behavior modification, better debugging capabilities, and improved maintainability through selective step execution.
