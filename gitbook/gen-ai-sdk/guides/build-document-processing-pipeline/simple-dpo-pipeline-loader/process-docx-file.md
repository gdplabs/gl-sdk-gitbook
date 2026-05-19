---
hidden: true
---

# Process DOCX File

Let's try to build a simple Document Processing Orchestrator (DPO) pipeline to process a DOCX file.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

* Completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[docx]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[docx]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[docx]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file.

{% file src="../../../../.gitbook/assets/docx-example.docx" %}

## Running the Pipeline

{% stepper %}
{% step %}
Create a script called `main.py`:

```python
import json
from gllm_docproc.loader.docx import PythonDOCXLoader

source = "docx-example.docx"

# initialize DOCX Loader
loader = PythonDOCXLoader()

# load source
loaded_elements = loader.load(source)

print(json.dumps(loaded_elements, indent=4))
```
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}

{% step %}
The loader will generate the following:

```json
[
    {
        "text": "[Header] This is the Header of the Document",
        "structure": "header",
        "metadata": {
            "source": "docx-example.docx",
            "source_type": "docx",
            "loaded_datetime": "2025-07-13 19:22:38",
            "style_name": "Header"
        }
    },
    {
        "text": "[Title] Document Loader Input Example",
        "structure": "uncategorized",
        "metadata": {
            "source": "docx-example.docx",
            "source_type": "docx",
            "loaded_datetime": "2025-07-13 19:22:38",
            "style_name": "Title"
        }
    },
    {
        "text": "[Subtitle] This document serves as a comprehensive example of an input for PDF, and DOCX Loader.",
        "structure": "uncategorized",
        "metadata": {
            "source": "docx-example.docx",
            "source_type": "docx",
            "loaded_datetime": "2025-07-13 19:22:38",
            "style_name": "Subtitle"
        }
    },
    {
        "text": "[Paragraph] To comprehend the functionality of the Loaders available within our internal SDK, it is crucial to furnish comprehensive input and output examples for each Loader. These document serve as essential references that illustrate how each Loader interprets and processes different document elements. To ensure a thorough understanding, the input examples should encompass a wide range of document components, including :",
        "structure": "uncategorized",
        "metadata": {
            "source": "docx-example.docx",
            "source_type": "docx",
            "loaded_datetime": "2025-07-13 19:22:38",
            "style_name": "Normal"
        }
    },
    ...
]
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Congratulations! You have successfully run a DPO pipeline to read a DOCX!
{% endhint %}

You can use use the data extracted (text, font size, font family, font color, coordinates, links, page number, etc) to enrich the data before you embed them into a vector store (typically Elasticsearch).
