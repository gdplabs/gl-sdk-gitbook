# DOCX

**DOCX Loader** is a component designed for **extracting information from a DOCX file** and **converting it into a standardized JSON format**.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

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

You can use the following as a sample file: [docx-example.docx](https://assets.analytics.glair.ai/generative/docx/doc-example.docx).

## Recommendation

We recommend to use [DOCX2Python Loader](docx.md#docx2python-loader).

## DOCX2Python Loader

**DOCX2PythonLoader** is responsible to extract **Text**, **Tables**, and **Images** from within DOCX document by using the `python-docx` library.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.docx import DOCX2PythonLoader

source = "./data/source/docx-example.docx"

# initialize DOCX2Python Loader
loader = DOCX2PythonLoader()

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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/docx/docx2pythonloader-output.json).
{% endstep %}
{% endstepper %}

## Python DOCX Loader

**PythonDOCXLoader** is responsible to extract **Text** and **Tables** from within DOCX document body by using the `docx2python` library.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.docx import PythonDOCXLoader

source = "./data/source/docx-example.docx"

# initialize Python DOCX Loader
loader = PythonDOCXLoader()

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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/docx/pythondocxloader-output.json).
{% endstep %}
{% endstepper %}

## Python DOCX Table Loader

**PythonDOCXTableLoader** is responsible to extract **Tables** from within DOCX document body by using the `python-docx` library.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.docx import PythonDOCXTableLoader

source = "./data/source/docx-example.docx"

# initialize Python DOCX Table Loader
loader = PythonDOCXTableLoader()

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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/docx/pythondocxtableloader-output.json).
{% endstep %}
{% endstepper %}
