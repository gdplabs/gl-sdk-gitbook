# Google Drive

**Google Drive Downloader** allows you to **download files from Google Drive** and save them to a specified output directory. You can download files using a Google Drive file ID or shareable link.

{% hint style="warning" %}
**Important**: The file must be accessible by your GL Connectors account. Make sure the Google Drive file has appropriate sharing permissions for the GL Connectors account associated with your credentials.
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
from gllm_docproc.downloader import GoogleDriveDownloader

source = "https://drive.google.com/file/d/1a2b3c4d5e6f7g8h9i0j/view?usp=sharing"
output_path = "./downloader/output"

# Initialize downloader
downloader = GoogleDriveDownloader(
    api_key="YOUR_GL_CONNECTORS_API_KEY",
    identifier="YOUR_GL_CONNECTORS_IDENTIFIER",
    secret="YOUR_GL_CONNECTORS_SECRET",
)

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
The downloader will automatically extract the file ID from the URL and download the file.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
**Source Input**: The `source` parameter can be either a Google Drive URL or a direct file ID. The downloader automatically extracts the file ID from various Google Drive URL formats:

* `https://drive.google.com/file/d/FILE_ID/view`
* `https://drive.google.com/open?id=FILE_ID`
* `https://drive.google.com/uc?id=FILE_ID`
* `https://docs.google.com/document/d/FILE_ID`
* `https://docs.google.com/spreadsheets/d/FILE_ID`
* `https://docs.google.com/presentation/d/FILE_ID`
* Direct file ID

Make sure your GL Connectors account has access to the file you want to download.
{% endhint %}
