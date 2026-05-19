# HTML

**HTML Flat Parser** is responsible for parsing elements loaded from web content. It assigns a structure to each loaded element based on the HTML tags present in its metadata, mapping them into structures such as heading, paragraph, image, video, audio, table, header, footer, and title.

This page provides guide to use HTML Flat Parser in Document Processing Orchestrator (DPO).

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

You can use the following as a sample file: [loaded\_elements.json](https://assets.analytics.glair.ai/generative/web/html-flat-loader-output.json).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json
from gllm_docproc.parser.html import HTMLFlatParser

# read JSON file with content and element_metadata
file_path = "./data/source/loaded_elements.json"
with open(file_path, "r", encoding="utf-8") as f:
    loaded_elements = json.load(f)

# initialize the HTML Flat Parser
parser = HTMLFlatParser()

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
The loader & parser will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/web/html-flat-parser-output.json).
{% endstep %}
{% endstepper %}
