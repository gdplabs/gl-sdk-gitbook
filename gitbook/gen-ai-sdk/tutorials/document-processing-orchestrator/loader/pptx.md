# PPTX

**PPTX Loader** is a component designed for **extracting information from a PPTX file** and **converting it into a standardized JSON format.**

This page provides a list of all supported PPTX Loader in Document Processing Orchestrator (DPO).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[pptx]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[pptx]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[pptx]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [pptx-example.pptx](https://assets.analytics.glair.ai/generative/pptx/pptx-example.pptx).

## **PythonPPTX Loader**

`PythonPPTXLoader` is responsible for extracting text, tables, images, and charts from PPTX documents.\
The text is extracted per shape (paragraphs and runs), tables are normalized into markdown, images are base64 encoded, and charts are converted into minimal structured text with metadata.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.pptx import PythonPPTXLoader

source = "./data/source/pptx-example.pptx"

# initialize the PPTX Loader
loader = PythonPPTXLoader()

# load source
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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/pptx/pythonpptxloader-output.json).
{% endstep %}
{% endstepper %}
