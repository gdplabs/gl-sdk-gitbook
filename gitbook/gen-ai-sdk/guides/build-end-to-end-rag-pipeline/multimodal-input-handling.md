---
icon: images
---

# Multimodal Input Handling

This guide will walk you through **adding multimodal input handling to your existing RAG pipeline**. This will allow your pipeline to process more than just text inputs, making your application!

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [**Your First RAG Pipeline**](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline) **tutorial** - this builds directly on top of it
2. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page
3. A working OpenAI API key configured in your environment variables

You should be familiar with these concepts and components:

1. [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") - **Required foundation**
2. [Routing](../../tutorials/orchestration/routing/README.md "mention") - Overview of available router types
3. [#switch](../../tutorials/orchestration/steps/#switch "mention")

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/007_multimodal_input_handling" class="button primary" data-icon="github">View full project code on GitHub</a>

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
**Start From Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") tutorial. We don't need to add any new file for this tutorial. Therefore, the structure should stay as is:

```
multimodal-input-handling/
├── data/
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── dog.png
├── indexer.py
├── pipeline.py    # 👈 Will be adjusted for multimodal input handling
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```

{% endstep %}
{% endstepper %}

---

## 1) Adding Multimodal Inputs Handling

### Extending the Pipeline

Let's adjust the pipeline to handle multimodal inputs. In this tutorial, let's assume that the attachment files are passed as local paths through the pipeline state.

{% stepper %}
{% step %}
**Define the extended state**

Create a custom state that includes the attachment files as input as well as the extra contents list to be passed to the response synthesizer:

```python
from gllm_inference.schema import MessageContent

class MultimodalRAGState(RAGState):
    attachments: list[str]
    extra_contents: list[MessageContent]
```

{% endstep %}

{% step %}
**Create a function to create the extra contents**

Our goal is to pass the input attachments as `Attachment` objects to the response synthesizer's `extra_contents` parameter. To do this, lets create a custom function!

```python
from typing import Any
from gllm_inference.schema import MessageContent

def format_extra_contents(inputs: dict[str, Any]) -> list[MessageContent]:
    attachments: list[bytes] = inputs["attachments"]
    return [Attachment.from_path(path) for path in attachments]
```

{% endstep %}

{% step %}
**Update the response synthesizer with a new prompt**

We'll update this with a prompt that can test our multimodal functionality.

```python
import os

from dotenv import load_dotenv
from gllm_generation.response_synthesizer import ResponseSynthesizer
from gllm_inference.request_processor import build_lm_request_processor

load_dotenv()

response_synthesizer = ResponseSynthesizer.stuff(
    lm_request_processor=build_lm_request_processor(
        model_id=os.getenv("LANGUAGE_MODEL"),
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="""Create an imaginary animal that is similar to the animal in the picture. Context: {context}""",
        user_template="Question: {query}",
    )
)
```

{% endstep %}

{% step %}
**Update the pipeline steps**

Define the step to format extra contents and add the extra content param to the response synthesizer.

```python
format_extra_contents_step = transform(  # 👈 New step
    format_extra_contents,
    ["attachments"],
    "extra_contents",
)

response_synthesizer_step = step(
    response_synthesizer,
    {
        "query": "user_query",
        "chunks": "chunks",
        "extra_contents": "extra_contents",  # 👈 New parameter
    },
    "response",
)
```

{% endstep %}

{% step %}
**Compose the final pipeline**

Chain all steps to create the complete guardrail pipeline:

```python
e2e_pipeline = format_extra_contents_step | retrieve_step | synthesize_step
e2e_pipeline.state_type = MultimodalRAGState
```

This creates a pipeline that can handle multimodal input files.
{% endstep %}
{% endstepper %}

## 2) Run the Pipeline

{% include "../../../.gitbook/includes/telemetry-notice.md" %}

Now that the pipeline is all set, let's try it!

{% stepper %}
{% step %}
**Configure the pipeline state for testing**

```python
async def main():
    state = {
        "user_query": "Aquatic animals",
        "attachments": ["dog.png"],
    }
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
```

{% endstep %}
{% endstepper %}

And that's it! Your pipeline should now be able to handle the attached multimodal files!

## Troubleshooting

1. **Attachment loading fails:**
   1. Ensure that the file exists in your local path.
   2. Ensure that the path is valid. Pay attention whether you're using full path or relative path.
2. **LM invocation fails**:
   1. Ensure that the model you're using supports the attachment type and extension.
   2. Ensure that the attachment size does not exceed the model token limit.

---

Congratulations! You've successfully enhanced your RAG pipeline with multimodal input handling, allowing your application to process more than just text inputs!
