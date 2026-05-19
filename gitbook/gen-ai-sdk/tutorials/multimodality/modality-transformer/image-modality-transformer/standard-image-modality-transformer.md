# Standard Image Modality Transformer

### Introduction

The Standard Image Modality Transformer utilizes a router to direct images to the most appropriate converter based on their specific type. For instance, diagram images are routed to an Image-to-Mermaid converter, which yields more accurate results than a standard Image-to-Caption converter.

### Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-multimodal"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
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

Initialize the Standard Image Modality Transformer through the built-in preset, which saves you the hassle of initializing all the required components.

{% file src="../../../../../.gitbook/assets/flowchart.jpg" %}

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_transformer.image_modality_transformer.standard_image_modality_transformer import StandardImageModalityTransformer

image = Attachment.from_path("./flowchart.jpg")
transformer = StandardImageModalityTransformer.from_preset("domain_specific")
result = asyncio.run(transformer.transform(image.data))
print(result)
```

**Output:**

````
```mermaid
graph TD
A@{ shape: terminal, label: "Start" } --> B@{ shape: event, label: "Submit expense<br>report" }
B --> C@{ shape: diamond, label: "Is receipt<br>provided?" }
C -- "No" --> D@{ shape: event, label: "Request<br>receipt" }
C -- "Yes" --> E@{ shape: diamond, label: "Is expense<br>approved?" }
D -- "No" --> E
E -- "Yes" --> F@{ shape: lean-right, label: "Issue<br>reimbursement" }
E -- "No" --> G@{ shape: terminal, label: "End" }
F --> G
```
````

### Custom Router

For more customizable component, image transformer can be initialized with a custom `router` and `route_mapping` . The `route_mapping` is a dictionary defining which converters should handle each route.

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_pipeline.router import LMBasedRouter
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption
from gllm_multimodal.modality_converter.image_to_text.image_to_mermaid import LMBasedImageToMermaid
from gllm_multimodal.modality_transformer.image_modality_transformer.standard_image_modality_transformer import StandardImageModalityTransformer

valid_routes = {"general_image", "diagram"}
router = LMBasedRouter.from_preset(
    modality="image",
    preset_name="domain_specific",
    default_route="general_image",
    valid_routes=valid_routes,
)

caption_converter = LMBasedImageToCaption.from_preset("default")
mermaid_converter = LMBasedImageToMermaid.from_preset("default")
route_mapping = {
    "general_image": caption_converter,
    "diagram": mermaid_converter,
}

transformer = StandardImageModalityTransformer(router=router, route_mapping=route_mapping)
result = asyncio.run(transformer.transform(image.data))
print(result)
```

### Skip Routing

You can also skip the routing process. It will automatically route the image to the router's default route.

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_transformer.image_modality_transformer.standard_image_modality_transformer import StandardImageModalityTransformer

image = Attachment.from_path("./flowchart.jpg")
transformer = StandardImageModalityTransformer.from_preset("domain_specific")
result = asyncio.run(transformer.transform(image.data, skip_routing=True))
print(result)
```
