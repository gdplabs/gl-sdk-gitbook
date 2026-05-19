---
icon: diagram-sankey
---

# Execute a Pipeline

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../prerequisites.md "mention") page..

You should be familiar with these concepts and components:

1. [orchestration](../tutorials/orchestration/ "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core gllm-pipeline
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core gllm-pipeline
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-core gllm-pipeline
```
{% endtab %}
{% endtabs %}

## 1) Basic Execution with `.invoke()`

When you have a pre-built pipeline, here is how you can execute it:

```python
# Initialize the pipeline
pipeline = step_1 | step_2 | step_3  # or replace it with your prebuilt pipeline

# Prepare initial state
initial_state = {
    "user_query": "What is machine learning?",
    "history": "",
    "context": ""
}

# Execute the pipeline
final_state = await pipeline.invoke(initial_state)

# Access the results
response = final_state["response"]
references = final_state["references"]
```

### 2) Execution with Configuration

You can also run the pipeline with configuration. Configuration can include debugging, caching, timeouts, retries, and other runtime parameters (`top_k` for retriever, etc). The configuration is passed to the invoke() method and affects how the pipeline executes.

```python
# Execute with custom configuration
config = {
    "debug_state": True,  # Include state logs in output
    "cache_enabled": True,
    "timeout": 30,  # seconds
    "max_retries": 3
    # other configuration
}

final_state = await pipeline.invoke(
    initial_state=initial_state,
    config=config
)
```
