# Image

**Image Loader** is a component designed for **extracting information from a standalone image file** and **converting it into a standardized JSON format**.

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

You can use the following as a sample file: [image-example.png](https://assets.analytics.glair.ai/generative/image/image-example.png).

## Image Loader

**ImageLoader** is responsible to **extract information from a standalone image**. It uses `magic` to validate the file and `base64` to encode it into a Base64 string.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.image import ImageLoader

source = "./data/source/image-example.png"

# initialize the ImageLoader
loader = ImageLoader()

# load the image source
loaded_elements = loader.load(source)
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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/image/imageloader-output.json).
{% endstep %}
{% endstepper %}
