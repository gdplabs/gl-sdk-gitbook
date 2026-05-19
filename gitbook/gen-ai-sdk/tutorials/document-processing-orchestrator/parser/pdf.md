# PDF

**PDF Parser** is responsible for parsing the text structure within PDF documents. It maps loaded elements from the PDF Loader into structures such as header, title, footer, heading, and paragraph, based on their metadata (font size, font family, coordinates, etc.).

This page provides guide to use PDF Parser in Document Processing Orchestrator (DPO).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[pdf]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[pdf]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[pdf]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [loaded\_elements.json](https://assets.analytics.glair.ai/generative/pdf/pymupdfloader-pdfplumberloader-output.json).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json

from gllm_docproc.parser.document import PDFParser

# loaded_elements (input) that you want to Parse
with open('./data/source/loaded_elements.json', 'r') as file:
    loaded_elements = json.load(file)

# initialize the PDF Parser
parser = PDFParser()

# parse loaded elements
parsed_elements = parser.parse(loaded_elements)
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
The parser will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/pdf/pdfparser-output.json).
{% endstep %}
{% endstepper %}
