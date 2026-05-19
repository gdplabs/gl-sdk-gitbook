# PDF

**PDF Loader** is a component designed for **extracting information from PDF documents**. PDF documents can vary significantly in terms of layout and structure.

This page provides a list of all supported PDF Loader in Document Processing Orchestrator (DPO).

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

You can use the following as a sample file: [pdf-example.pdf](https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf).

## Recommendation

For open-source version, we recommend to use combination of PyMuPDF and PDF Plumber. See [Multi-Loader PDF Extraction](pdf.md#multi-loader-pdf-extraction).

For SaaS version, we recommend to use [Azure AI Document Intelligence Loader](pdf.md#azure-ai-document-intelligence-loader).

## **PyMuPDF Loader**

**PyMuPDFLoader** is responsible to extract **text** and **images** in `base64` format within PDF document. The **text is extracted per paragraph**, based on how the `PyMuPDF` library detects the paragraphs.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.pdf import PyMuPDFLoader

source = "./data/source/pdf-example.pdf"

# initialize the PyMuPDF Loader
loader = PyMuPDFLoader()

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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/pdf/pymupdfloader-output.json).
{% endstep %}
{% endstepper %}

## **PDF Plumber Loader**

**PDFPlumberLoader** is responsible to extract **tables** from PDF documents. It **identifies tables based on clear, well-defined borders**. As a result, tables with missing or incomplete borders won't be detected.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.pdf import PDFPlumberLoader

source = "./data/source/pdf-example.pdf"

# initialize the PDF Plumber Loader
loader = PDFPlumberLoader()

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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/pdf/pymupdfspanloader-output.json).
{% endstep %}
{% endstepper %}

## **Multi-Loader PDF Extraction**

In certain cases, we might need to combine multiple loader to enhance information extraction. Below is a sample implementation to load PDF document using **PyMuPDFLoader** and **PDFPlumberLoader**.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader import PipelineLoader
from gllm_docproc.loader.pdf import PDFPlumberLoader, PyMuPDFLoader

source = "./data/source/pdf-example.pdf"

# initialize pipelineLoader
pipelineLoader = PipelineLoader()

# add Text Loader for PDF document (order matters, add PyMuPDFLoader first)
pipelineLoader.add_loader(PyMuPDFLoader())

# add Table Loader for PDF document
pipelineLoader.add_loader(PDFPlumberLoader())

# load source
loaded_elements = pipelineLoader.load(source)
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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/pdf/pymupdfloader-pdfplumberloader-output.json).
{% endstep %}
{% endstepper %}

## **Azure AI Document Intelligence Loader**

**AzureAIDocumentIntelligenceLoader** extract **text**, **tables**, and **images** from PDF document using the Azure AI Document Intelligence, a cloud-based Azure AI service.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.pdf import AzureAIDocumentIntelligenceLoader

source = "./data/source/pdf-example.pdf"

# initialize the Azure AI Document Intelligence Loader
loader = AzureAIDocumentIntelligenceLoader(
    endpoint="AZURE_AI_ENDPOINT",
    key="AZURE_AI_KEY",
)

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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/pdf/azureaidocumentintelligenceloader-output.json).
{% endstep %}
{% endstepper %}
