# Direct File URL

**Direct File URL Downloader** allows you to **download files from a direct file URL** and save them to a specified output directory. A direct file URL is a URL that points directly to a downloadable file (e.g., `https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf`).

<details>

<summary>Prerequisites</summary>

If you want to try the snippet code in this page:

* Completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

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
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc"
```
{% endtab %}
{% endtabs %}

## **Basic Usage**

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.downloader import DirectFileURLDownloader

source = "https://assets.analytics.glair.ai/generative/pdf/pdf-example.pdf"
output_path = "./downloader/output"

# Initialize downloader
downloader = DirectFileURLDownloader()

# Download file
downloaded_files = downloader.download(source, output_path)
print(f"Downloaded files: {downloaded_files}")
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
The downloader will save the file to the specified output directory with an automatically generated filename based on timestamp and UUID. The file extension will be detected from the HTTP response headers or file content.
{% endstep %}
{% endstepper %}
