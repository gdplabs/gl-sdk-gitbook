# XLSX

**XLSX Parser** is responsible for parsing the table structure within XLSX documents. It maps loaded elements from the XLSX Loader into structures such as table, converting raw table data to markdown format and handling sheet names as table captions.

This page provides guide to use XLSX Parser in Document Processing Orchestrator (DPO).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[xlsx]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[xlsx]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[xlsx]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [loaded\_elements.json](https://assets.analytics.glair.ai/generative/xlsx/openpyxlloader-output.json).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json

from gllm_docproc.parser.document import XLSXParser

# loaded_elements (input) that you want to Parse
with open('./data/source/loaded_elements.json', 'r') as file:
    loaded_elements = json.load(file)

# initialize the XLSX Parser
parser = XLSXParser()

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
The parser will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/xlsx/xlsxparser-output.json).
{% endstep %}
{% endstepper %}
