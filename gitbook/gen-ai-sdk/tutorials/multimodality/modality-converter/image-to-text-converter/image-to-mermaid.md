# Image to Mermaid

### Introduction

The Image to Mermaid component converts flowchart and diagram images into [Mermaid](https://mermaid.js.org/intro/syntax-reference.html) syntax using multimodal LLMs. It analyzes visual structures (nodes, shapes, connectors) and generates valid Mermaid code that preserves the diagram's logic and relationships.

### Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-multimodal"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-multimodal"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "gllm-multimodal"
```
{% endtab %}
{% endtabs %}

### Quickstart

The simplest way to initialize Image to Mermaid component is to use the built-in preset.

{% file src="../../../../../.gitbook/assets/flowchart.jpg" %}

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.image_to_text.image_to_mermaid import LMBasedImageToMermaid

image = Attachment.from_path("./flowchart.jpg")
converter = LMBasedImageToMermaid.from_preset("default")
mermaid = asyncio.run(converter.convert(image.data))
print(f"Mermaid Syntax: \n{mermaid.result}")
```

**Output:**

````
Mermaid Syntax:
```mermaid
graph TD
A@{ shape: terminal, label: "Start" } --> B@{ shape: event, label: "Submit expense<br>report" }
B --> C@{ shape: diamond, label: "Is receipt<br>provided?" }
C -- "No" --> D@{ shape: event, label: "Request<br>receipt" }
C -- "Yes" --> G@{ shape: terminal, label: "End" }
D --> E@{ shape: diamond, label: "Is expense<br>approved?" }
E -- "No" --> G
E -- "Yes" --> F@{ shape: lean-right, label: "Issue<br>reimbursement" }
F --> G
```
````

### Customize Model

When using preset, the image-to-mermaid model can be changed by passing `model_id` into the `lm_invoker_kwargs` in `from_preset()` function

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.image_to_text.image_to_mermaid import LMBasedImageToMermaid

image = Attachment.from_path("./flowchart.jpg")
converter = LMBasedImageToMermaid.from_preset("default", lm_invoker_kwargs={"model_id": "openai/gpt-5"})
mermaid = asyncio.run(converter.convert(image.data))
print(f"Mermaid Syntax: \n{mermaid.result}")
```

### Customize Model and Prompt

Using a custom LM Request Processor allows you to customize model and/or prompt.

<pre class="language-python"><code class="lang-python"><strong>import asyncio
</strong>
from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.image_to_text.image_to_mermaid import LMBasedImageToMermaid

lmrp = build_lm_request_processor(
    model_id="google/gemini-2.5-flash",
    credentials="&#x3C;your-api-key>", # or use the environment variable GOOGLE_API_KEY
    system_template="You are a visual structure parser tasked with converting input images into Mermaid.js syntax. Each image contain flowcharts. Your role is to extract the structural meaning and translate it into a valid Mermaid code block.",
    user_template="image(s) attached",
)
image = Attachment.from_path("./flowchart.jpg")

converter = LMBasedImageToMermaid(lm_request_processor=lmrp)
mermaid = asyncio.run(converter.convert(image.data))
print(f"Mermaid Syntax: \n{mermaid.result}")
</code></pre>
