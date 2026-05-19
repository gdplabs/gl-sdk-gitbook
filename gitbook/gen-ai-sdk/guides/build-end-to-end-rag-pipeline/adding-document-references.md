---
icon: books
---

# Adding Document References

This guide will walk you through **adding a Reference Formatter component to your existing RAG pipeline** that automatically formats and includes source references in your responses, making your answers more credible and traceable.

**Reference formatting** enhances your RAG responses with automatic source citations, providing transparency and credibility by showing exactly where information came from

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [**Your First RAG Pipeline**](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline) **tutorial** - this builds directly on top of it
2. Completion of all setup steps listed on the [Prerequisites](https://gdplabs.gitbook.io/sdk/overview/prerequisites) page
3. A working OpenAI API key configured in your environment variables

You should be familiar with these concepts and components:

1. Components in [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") - **Required foundation**
2. [reference-formatter.md](../../tutorials/generation/reference-formatter.md "mention")

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/004_adding_document_references" class="button primary" data-icon="github">View full project code on GitHub</a>

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
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

***

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Extend Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") tutorial. We don't need to add any new file for this tutorial. Therefore, the structure should stay as is:

```
adding-document-references/
├── data/
│   ├── chroma.sqlite3
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── indexer.py
├── pipeline.py    # 👈 Will be updated with reference formatter
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```
{% endstep %}
{% endstepper %}

***

## 1) Build the Reference Formatter Pipeline

The `SimilarityBasedReferenceFormatter` analyzes your response against retrieved chunks and automatically creates formatted citations using chunk metadata.

{% stepper %}
{% step %}
**Create the reference formatter step**

Update your `pipeline.py` (or create a new one) with the reference formatter:

{% code lineNumbers="true" %}
```python
from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter
from gllm_pipeline.steps import step

reference_formatter = SimilarityBasedReferenceFormatter(
    em_invoker=em_invoker, threshold=0.5, stringify=False
)

format_reference_step = step(
    component=reference_formatter,
    input_map={"response": "response", "chunks": "chunks"},
    output_state="references",
)
```
{% endcode %}
{% endstep %}

{% step %}
**Compose the final pipeline**

Chain all steps including the reference formatter:

{% code lineNumbers="true" %}
```python
e2e_pipeline = retrieve_step | synthesize_step | format_reference_step
```
{% endcode %}

This creates a pipeline that generates responses **with automatic source citations** from the retrieved chunks.

> 🧠 The `RAGState` input state already contains a `reference` field that gets populated by the reference formatter.
{% endstep %}
{% endstepper %}

## 2) Run the Pipeline

{% include "../../../.gitbook/includes/telemetry-notice.md" %}

{% stepper %}
{% step %}
**Configure and invoke the pipeline**

Configure the state and config for direct pipeline invocation:

```python
async def main():
    state = {"user_query": "Give me nocturnal creatures from the dataset"}  # Replace with your actual query
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")
    print(f"References: {result['references']}")


if __name__ == "__main__":
    asyncio.run(main())
```
{% endstep %}

{% step %}
**Observe output**

If you successfully run all the steps, you will see something like this appended in the end of the result:

{% code overflow="wrap" fullWidth="false" %}
```bash
References: [Chunk(id=ffe9bfbf-6065-480c-bded-276ac9994d72, content=The Luminafox is a nocturnal creature inhabiting t..., metadata={'name': 'Luminafox'}, score=0.4633599574686413), Chunk(id=b91d6dfb-f177-48c9-84dd-a782b785ee0d, content=The Dusk Panther prowls the twilight forests of Sh..., metadata={'name': 'Dusk Panther'}, score=0.4541605560513348), Chunk(id=05429706-c477-4804-a4e5-9da1ddf50632, content=The Gloombat flits through the dark caverns of Dus..., metadata={'name': 'Gloombat'}, score=0.4435190881711845), Chunk(id=4965e21b-4780-4a76-9d6a-b70e4faf1da2, content=The Moonstalker is a nocturnal predator prowling t..., metadata={'name': 'Moonstalker'}, score=0.44225796877897344), Chunk(id=d95382d7-2fdb-41cf-b741-ec0ceaed732d, content=The Glowhopper is an insect-like creature residing..., metadata={'name': 'Glowhopper'}, score=0.42312825178877955)]
```
{% endcode %}
{% endstep %}
{% endstepper %}

## Troubleshooting

**Common Issues**

1. **No references being generated**:
   * Ensure chunks have meaningful metadata
   * Check that the reference formatter step is included in the pipeline
   * Verify the response contains content that matches chunk content
2. **Poor reference quality**:
   * Improve chunk metadata with more descriptive information
   * Ensure chunks are properly indexed with relevant content
   * Check that the response synthesizer generates content that references the chunks
3. **Reference formatting issues**:
   * Verify the SimilarityBasedReferenceFormatter is properly configured
   * Check that chunk metadata is in the expected format
   * Ensure the pipeline state includes the reference field

**Debug Tips**

1. **Enable debug mode**: Set `debug: true` in your request to see detailed logs
2. **Check chunk metadata**: Verify that your chunks have meaningful metadata
3. **Examine response content**: Ensure the response actually references the chunk content
4. **Pipeline step order**: Confirm the reference formatter step comes after response generation

***

Congratulations! You've successfully implemented a Reference Formatter component in your RAG pipeline. This enhancement makes your responses more credible and traceable by automatically including formatted references to the source information, significantly improving the transparency and reliability of your AI-powered answers.
