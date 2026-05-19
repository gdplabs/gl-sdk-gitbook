# Loader Router

**LoaderRouter** is designed to identify the appropriate [`LoaderType`](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-docproc/gllm_docproc/model/loader_type.py) for a given input by examining its path, extension, metadata, content, or URL.

\
It supports common document, media, and text-based files, returning the matched type in a dictionary keyed by `LoaderType.KEY`, or marking it as `uncategorized` if no match is found.

<details>

<summary>Prerequisites</summary>

If you want to try the snippet code in this page:

* Completion of all setup steps listed on the [Prerequisites](/broken/pages/qFjvrdtREuJTNsHqV6HE) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-interna
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [pdf-example.pdf](https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf).

## Running the Router

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.dpo_router.loader_router import LoaderRouter
from gllm_docproc.model.loader_type import LoaderType

# Example source: local PDF file
source = "./pdf-example.pdf"

# Initialize LoaderRouter
router = LoaderRouter()

# Route the input to get the loader type
result = router.route(source)

# Access the detected loader type
print(f"Detected loader type: {result[LoaderType.KEY]}")

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
Example output:

```json
Detected loader type: pdf_loader
```
{% endstep %}
{% endstepper %}

{% hint style="info" %}
The returned dictionary has:

* **Key:** `LoaderType.KEY` (`"loader_type"`)
* **Value:** one of the values defined in [LoaderType](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-docproc/gllm_docproc/model/loader_type.py), such as `"pdf_loader"`, `"docx_loader"`, `"audio_loader"`, etc.
{% endhint %}
