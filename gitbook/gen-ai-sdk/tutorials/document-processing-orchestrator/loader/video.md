# Video

**Video Loader** is designed for **extracting information from Video file**.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[video]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[video]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[video]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [video-example.mp4](https://assets.analytics.glair.ai/generative/video/video-example.mp4).

## Video Transcript Loader

**VideoTranscriptLoader** is responsible to **extract information from video file** by utilizing the [GLLM Multimodal Audio to Text](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.video import VideoTranscriptLoader

source = "./data/source/video-example.mp4"

# initialize video transcript loader
loader = VideoTranscriptLoader()

# load video file
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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/video/videotranscriptloader-output.json).
{% endstep %}
{% endstepper %}
