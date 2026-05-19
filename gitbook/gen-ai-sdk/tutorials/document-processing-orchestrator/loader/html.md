# HTML

**HTML Loader** is a component designed for **extracting information from HTML Document** and **converting it into a standardized JSON format**.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[html]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[html]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[html]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [html-example.json](https://assets.analytics.glair.ai/generative/web/html-downloader-output.json).

## HTML Flat Loader

**HTMLFlatLoader** is responsible for extracting elements such as **Text**, **Table**, **Hyperlink**, **Image**, **Video**, etc,. from a website.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.html import HTMLFlatLoader

source = "[HTML CONTENT FROM html-example.json FILE]"

# initialize the HTMLFlatLoader
loader = HTMLFlatLoader()

# load the source
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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/web/html-flat-loader-output.json).
{% endstep %}
{% endstepper %}
