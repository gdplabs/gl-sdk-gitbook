# Smart Search Downloader

**Smart Search Downloader** allows you to extract content from a specific web page URL using the Smart Search SDK and save the response data as JSON files in a specified output directory.

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
from gllm_docproc.downloader.smart_crawl_downloader import SmartCrawlDownloader

# Initialize downloader
downloader = SmartSearchDownloader(
    base_url="YOUR_SMARTSEARCH_BASE_URL"), 
    token="YOUR_SMARTSEARCH_TOKEN"),
)

# Download file
downloader_result = downloader.download(
    source="https://docs.python.org/3/tutorial/",
    output="./downloader/output",
)

print(f"Successfully downloaded Smart Search data to {downloader_result[0]}")
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
The downloader will fetch and extract content from a specific web page URL using the Smart Search SDK, saving the processed response as a JSON file in the output directory with an automatically generated filename.
{% endstep %}

{% step %}
You can define a JSON Schema to guide the Smart Search SDK in extracting specific fields and data points from the web page content using the `json_schema` parameter in download method.
{% endstep %}
{% endstepper %}
