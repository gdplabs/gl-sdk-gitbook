# HTML Downloader

**HTML Downloader** allows you to **download HTML Document from a URL** and save it as a JSON file.

This page provides guide to use HTML Downloader in Document Processing Orchestrator (DPO).

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
from gllm_docproc.downloader.html import HTMLDownloader

source = "https://books.toscrape.com/"
output_path = "downloader/output/download"

# Initialize downloader
downloader = HTMLDownloader()

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
The downloader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/web/html-downloader-output.json).
{% endstep %}
{% endstepper %}

## **Crawl URL**

**HTML Downloader** allows you to **crawl a URL** and save it as JSON files.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.downloader.html import HTMLDownloader

source = "https://quotes.toscrape.com/"
output_path = "downloader/output/crawl"

# Initialize the downloader and set the allowed domains
downloader = HTMLDownloader(allowed_domains=["quotes.toscrape.com"])

# Download input
downloader.download_crawl(source, output_path)
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
The downloader will generate JSON files at the specified output location.
{% endstep %}
{% endstepper %}

## **Download from Sitemap**

**HTML Downloader** allows you to download from **a sitemap link** and save it as JSON files.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.downloader.html import HTMLDownloader

source = "https://indonesiakaya.com/pustaka_cat-sitemap.xml"
output_path = "downloader/output/crawl_sitemap"

# Initialize the downloader and set the allowed domains
downloader = HTMLDownloader(allowed_domains=["indonesiakaya.com"])

# Download input
downloader.download_sitemap(source, output_path)
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
The downloader will generate JSON files at the specified output location.
{% endstep %}
{% endstepper %}
