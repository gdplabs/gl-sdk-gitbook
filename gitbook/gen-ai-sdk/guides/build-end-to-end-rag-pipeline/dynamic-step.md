---
icon: toggle-large-on
---

# Dynamic Step

This guide will walk you through **adding a toggle to your existing RAG pipeline** to allow users to dynamically choose whether to use a component or not.

**Toggle functionality** gives users control over which components to execute in your pipeline, providing flexibility and optimization opportunities. For example, you can toggle knowledge base retrieval, specific processing steps, or any conditional logic based on runtime conditions.

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") **tutorial** - this builds directly on top of it
2. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page
3. A working OpenAI API key configured in your environment variables

You should be familiar with these concepts and components:

1. Components in [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") - **Required foundation**
2. [#toggle](../../tutorials/orchestration/steps/#toggle "mention") step

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/002_dynamic_step" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Extend Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") tutorial. We don't need to add any new file for this tutorial. Therefore, the structure should stay as is:

```
<project-name>/
├── data/
│   ├── chroma.sqlite3
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── indexer.py
├── pipeline.py
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```
{% endstep %}
{% endstepper %}

***

## 1) Build the Toggle Pipeline

### Understanding Toggle Steps

A [**toggle step**](../../tutorials/orchestration/steps/#toggle) allows your pipeline to conditionally execute any components based on a boolean condition. This pattern can be applied to any pipeline step - retrieval, processing, validation, or custom logic. Here's how it works:

1. **Toggle Condition**: Evaluates a boolean condition from the pipeline state
2. **Conditional Execution**: If `True`, executes the specified steps; if `False`, skips them
3. **Pipeline Continuation**: The pipeline continues with subsequent steps regardless

In this example, we'll demonstrate toggling knowledge base retrieval, but the same pattern applies to any pipeline component.

### Create the Enhanced Pipeline

{% stepper %}
{% step %}
**Define the toggle state**

Extend the [RAG state](../../tutorials/orchestration/state.md#default-state-ragstate) to include the toggle condition:

{% code lineNumbers="true" %}
```python
class ToggleState(RAGState):
    use_knowledge_base: bool
```
{% endcode %}

This adds a `use_knowledge_base` field that controls whether retrieval is performed.
{% endstep %}

{% step %}
**Create the** [**toggle step**](../../tutorials/orchestration/steps/#toggle)

This is the core toggle logic that conditionally executes retrieval:

{% code lineNumbers="true" %}
```python
knowledge_base_toggle_step = toggle(
    condition=lambda x: x["use_knowledge_base"],
    if_branch=[retrieve_step],
)
```
{% endcode %}

**How it works:**

* **condition**: Lambda function that checks the `use_knowledge_base` boolean
* **if\_branch**: Steps to execute if condition is `True` (document retrieval)
* **else\_branch**: Not specified, so nothing happens if `False`
{% endstep %}

{% step %}
**Compose the final pipeline**

Chain the toggle step with the synthesis steps:

{% code lineNumbers="true" %}
```python
e2e_pipeline = knowledge_base_toggle_step | synthesize_step
e2e_pipeline.state_type = ToggleState
```
{% endcode %}

This creates a pipeline that:

1. Conditionally retrieves context from knowledge base based on the toggle
2. Synthesizes a response using either retrieved context or just the query

> 🧠 _The response synthesizer can adapt its behavior based on whether context is available or not._
{% endstep %}
{% endstepper %}

## 2) Run the Pipeline

{% include "../../../.gitbook/includes/telemetry-notice.md" %}

{% stepper %}
{% step %}
**Configure the pipeline state for testing**

Set up test cases with different toggle values to see conditional execution in action:

{% code lineNumbers="true" %}
```python
async def main():
    state = {
        "user_query": "Give me nocturnal creatures from the dataset", # Replace with your actual query
        "use_knowledge_base": False, # Set to True to retrieve from knowledge base
        "chunks": [] # Initialize to empty list if knowledge base is disabled
    }
    config = {
        "top_k": 5,
    }
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())

```
{% endcode %}

When you run the pipeline with knowledge base enabled, you should see retrieval happening in the debug logs. Otherwise, you should see no retrieval in the debug logs, and the response should be generated purely from the model's knowledge.
{% endstep %}
{% endstepper %}

## Troubleshooting

1. **Pipeline always executes despite toggle being False**:
   1. Check that you're using the correct state field name in your condition
   2. Verify the lambda condition syntax: `lambda x: x["your_toggle_field"]`
   3. Ensure you're passing the state correctly to `invoke()`
   4. Use debug mode to see which condition is being evaluated
2. **Empty or unexpected responses when toggle is False**:
   1. Check that downstream components can handle missing data from toggled steps
   2. Consider updating your prompts to handle scenarios when certain data is unavailable
3. **Toggle condition not working**:
   1. Verify your state class includes the boolean field: `your_toggle_field: bool`
   2. Check that the boolean value is properly set in your state
   3. Use debug mode to inspect the pipeline execution flow
   4. Test your lambda condition separately to ensure it evaluates correctly
4. **General toggle pattern issues**:
   1. Consider the impact of skipped steps on subsequent pipeline components
   2. Test both True and False conditions to verify expected behavior

***

Congratulations! You've successfully enhanced your RAG pipeline with toggle functionality. You can now conditionally execute any pipeline components based on runtime conditions, providing flexibility and optimization opportunities. This pattern can be applied to knowledge base retrieval, processing steps, validation, or any custom logic in your pipeline.
