# Smart Crawl Downloader

**Smart Crawl Downloader** allows you to retrieve crawled data from the Smart Crawl API using the `GET /api/v1/data` endpoint and save the response as JSON files in a specified output directory.

{% hint style="info" %}
Note: You must have access to the Smart Crawl API endpoint that you provided.
{% endhint %}

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
downloader = SmartCrawlDownloader(endpoint_url="YOUR_SMARTCRAWL_ENDPOINT_URL")

# Download file
downloader_result = downloader.download(
    source="cnnindonesia",
    output="./downloader/output",
    start_date="2026-01-01T00:00:00Z",
    end_date="2026-03-25T23:59:59Z",
)

print(f"Successfully downloaded Smart Crawl data to {downloader_result[0]}")
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
The downloader will fetch data from the Smart Crawl API for the specified domains and date range, saving the response as a JSON file in the output directory with an automatically generated filename.
{% endstep %}

{% step %}
You can also define the specific keywords to retrieve using the `queries` parameter, as well as the output schema using the `schema` parameter.

{% code lineNumbers="true" %}
```python
from gllm_docproc.downloader.smart_crawl_downloader import SmartCrawlDownloader

# Initialize downloader
downloader = SmartCrawlDownloader(endpoint_url="YOUR_SMARTCRAWL_ENDPOINT_URL")

# Download file
downloader_result = downloader.download(
    source="cnnindonesia",
    output="./downloader/output",
    start_date="2026-01-01T00:00:00Z",
    end_date="2026-03-25T23:59:59Z",
    queries="ekonomi,teknologi",
    schema="source_name,source_url,title,subtitle,author,content_text,summary",
)

print(f"Successfully downloaded Smart Crawl data to {downloader_result[0]}")
```
{% endcode %}
{% endstep %}

{% step %}
The downloader will generate something along:

```json
{
  "data": [
      {
        "source_name": "cnnindonesia",
        "source_url": "https://www.cnnindonesia.com/ekonomi/20260316061759-92-1338394/ihsg-diproyeksi-lesu-awali-pekan-ini",
        "title": "IHSG Diproyeksi Lesu Awali Pekan Ini",
        "subtitle": "Indeks Harga Saham Gabungan (IHSG) diproyeksi melemah pada perdagangan Senin (16/3)...",
        "author": "",
        "content_text": ".....",
        "summary": "Indeks Harga Saham Gabungan (IHSG) diproyeksi melemah pada perdagangan Senin, 16 Maret 2026.\nAnalis MNC Sekuritas memperkirakan IHSG... "
      },
      ...
  ],
  "metadata": {
       ...
  }
}
```
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Source Input: The `source` is restricted to a predefined set of supported domains. Refer to the documentation for the list of valid domain values: [GL Smart Crawl Valid Domain Values](https://gdplabs.gitbook.io/sdk/gl-smart-crawl/guides/data-api#valid-domain-values)
{% endhint %}
