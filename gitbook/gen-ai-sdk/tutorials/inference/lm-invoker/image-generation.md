---
icon: image
---

# Image Generation

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [image-generation.md](image-generation.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `GoogleLMInvoker`, `OpenAILMInvoker` , `XAILMInvoker`

## What is Image Generation?

Image generation is a native tool that allows the language model to generate an image based on the provided query. When it's enabled, image results are stored in the `outputs` attribute of the `LMOutput` object and can be accessed via the `attachments` property.

{% hint style="warning" %}
To enable image generation, it's imperative that the used model supports image generation. Using the image generation native tool with a model that doesn't support image generation will cause an error.
{% endhint %}

Image generation tool can be enabled with several options as seen below. Since image generation may take quite some time, it's highly recommended to set a higher timeout via the `RetryConfig`.

```python
import asyncio
from gllm_core.retry import RetryConfig
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import NativeTool, NativeToolType

# Option 1: as string
image_generation_tool = "image_generation"
# Option 2: as enum
image_generation_tool = NativeToolType.IMAGE_GENERATION
# Option 3: as dictionary (useful for providing custom kwargs)
image_generation_tool = {"type": "image_generation", **kwargs}
# Option 4: as native tool object (useful for providing custom kwargs)
image_generation_tool = NativeTool.image_generation(**kwargs)

retry_config = RetryConfig(timeout=60)
lm_invoker = OpenAILMInvoker(
    OpenAILM.GPT_5_NANO, 
    tools=[image_generation_tool], 
    retry_config=retry_config,
)
```

With that all set, let's try it to generate a simple image!

```python
query = "Generate a 2D pixel style of a cute baby polar bear wearing a Santa hat."
output = asyncio.run(lm_invoker.invoke(query))
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
```

**Output:**

```
=== Output item: 'attachment' ===
Attachment(
    data='89504e470d...', 
    filename='3e6739de-ef36-4955-8a2a-c204cd437a2b.png', 
    mime_type='image/png', 
    extension='png', 
    url=None, 
    metadata={},
)
```

Now let's try to save the generated image to our local path:

```python
for attachment in output.attachments:
    attachment.write_to_file("path/to/output.png")
```

**Generated Image:**

<div data-full-width="true"><figure><img src="../../../../.gitbook/assets/image (1) (1).png" alt="" width="188"><figcaption></figcaption></figure></div>
