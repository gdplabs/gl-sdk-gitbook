# Generic Image Modality Transformer

### Introduction

Generic Image Modality Transformer is a version of Image Modality Transformer that only use one converter and doesn't use any router.

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

Initialize the Generic Image Modality Transformer by passing the modality converter into it.

{% hint style="info" %}
This example uses `Attachment` to load a local image file. See [schema.md](../../../inference/schema.md#attachment "mention") for all loading options.
{% endhint %}

{% file src="../../../../../.gitbook/assets/school_backpack.jpg" %}

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption
from gllm_multimodal.modality_transformer.image_modality_transformer.generic_image_modality_transformer import GenericImageModalityTransformer

image = Attachment.from_path("./school_backpack.jpg")

converter = LMBasedImageToCaption.from_preset("default")
transformer = GenericImageModalityTransformer(converter)
result = asyncio.run(transformer.transform(image.data, skip_routing=True))
print(result)
```

**Output:**

```
Ransel hitam serbaguna ini siap menemani petualangan harianmu dengan gaya.
Desain minimalis ransel hitam ini menampilkan tekstur kain yang elegan dan fungsional.
Nikmati kenyamanan dan ruang penyimpanan yang cukup dengan ransel modern berwarna hitam pekat ini.
Ransel klasik berwarna hitam dengan saku depan praktis dan tali bahu yang bisa diatur untuk berbagai kebutuhan.
Sempurnakan penampilanmu dengan ransel hitam stylish ini, pilihan tepat untuk segala aktivitas.
```
