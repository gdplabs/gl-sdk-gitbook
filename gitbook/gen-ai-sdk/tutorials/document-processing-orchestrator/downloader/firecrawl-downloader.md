# Firecrawl Downloader

**Firecrawl Downloader** allows you to **download HTML Document from a URL** using [Firecrawl service](https://www.firecrawl.dev/) and save it as a JSON file. You need to have Firecrawl API Key to use this.

This page provides guide to use Firecrawl Downloader in Document Processing Orchestrator (DPO).

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

## **Basic Usage**

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.downloader.html.firecrawl_downloader import HTMLFirecrawlDownloader

source = "https://books.toscrape.com/"
output_path = "downloader/output/download"

# Initialize downloader
downloader = HTMLFirecrawlDownloader(api_key="<YOUR_API_KEY>")

# Download input
downloader.download(source, output_path)
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
The downloader will generate something along:

```
{
    "metadata": {
        "favicon": "https://books.toscrape.com/static/oscar/favicon.ico",
        "viewport": "width=device-width",
        "language": "en-us",
        "title": "\n    All products | Books to Scrape - Sandbox\n",
        "robots": "NOARCHIVE,NOCACHE",
        "description": "",
        "created": "24th Jun 2016 09:29",
        "scrapeId": "4af45949-b185-4690-8938-ca22dcd0409e",
        "sourceURL": "https://books.toscrape.com/",
        "url": "https://books.toscrape.com/",
        "statusCode": 200,
        "contentType": "text/html",
        "proxyUsed": "basic",
        "creditsUsed": 1
    },
    "success": true,
    "element_metadata": {
        "source": "https://books.toscrape.com/",
        "source_type": "html",
        "loaded_datetime": "2025-07-29 18:29:18"
    },
    "content": "<!DOCTYPE html> ..."
}
```
{% endstep %}

{% step %}
You can also access the Firecrawl instance if you need to use Firecrawl method directly:

{% code lineNumbers="true" %}
```python
from gllm_docproc.downloader.html.firecrawl_downloader import HTMLFirecrawlDownloader

source = "https://books.toscrape.com/"

# Initialize downloader
downloader = HTMLFirecrawlDownloader(api_key="<YOUR_API_KEY>")

scrape_result = downloader.firecrawl_instance.scrape_url(source, formats=['markdown', 'html'])
print(scrape_result.markdown)
```
{% endcode %}
{% endstep %}
{% endstepper %}
