# Image

**Image Data Generator** is a component that processes image elements and generates data derived from their visual content.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[image]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[image]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[image]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [imageloader-output.json](https://assets.analytics.glair.ai/generative/image/imageloader-output.json).

## Image Caption Data Generator

**ImageCaptionDataGenerator** is responsible for processing image elements and generating captions by leveraging `BaseImageToCaption` from `gllm-multimodal`.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json
from gllm_multimodal.modality_converter.image_to_text.image_to_caption import LMBasedImageToCaption
from gllm_docproc.data_generator.image_data_generator import ImageCaptionDataGenerator

# Load the input elements to be processed
with open('./data/source/input_elements.json', 'r') as file:
    elements = json.load(file)

# Initialize the ImageCaptionDataGenerator with a preset image-to-caption model
image_to_caption = LMBasedImageToCaption.from_preset()
image_caption_data_generator = ImageCaptionDataGenerator(image_to_caption)

# Generate captions for image elements
output_elements = image_caption_data_generator.generate(elements)
print(output_elements)
```
{% endcode %}
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}

{% step %}
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/image/imagecaptiondatagenerator-output.json).
{% endstep %}
{% endstepper %}

## Multi Model Image Caption Data Generator

**MultiModelImageCaptionDataGenerator** is responsible for handling image captioning across multiple models with lazy initialization by leveraging `LMBasedImageToCaption` from `gllm-multimodal`.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json
from gllm_docproc.data_generator.image_data_generator import MultiModelImageCaptionDataGenerator

# Load the input elements to be processed
with open('/Users/devita/Desktop/need updated on s3/image/imageloader-output.json', 'r') as file:
    elements = json.load(file)

# Initialize the MultiModelImageCaptionDataGenerator
image_caption_data_generator = MultiModelImageCaptionDataGenerator()

# Generate captions for image elements
output_elements = image_caption_data_generator.generate(elements)
print(output_elements)
```
{% endcode %}
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}

{% step %}
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/image/imagecaptiondatagenerator-output.json).
{% endstep %}
{% endstepper %}
