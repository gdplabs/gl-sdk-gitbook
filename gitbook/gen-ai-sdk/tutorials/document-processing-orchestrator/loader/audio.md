# Audio

**Audio Loader** is designed for **extracting information from Audio file**.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[audio]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[audio]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[audio]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [sample-audio-1.mp3](https://assets.analytics.glair.ai/generative/audio/sample-audio-1.mp3).

## Audio Loader

**AudioLoader** is responsible to **extract information from audio file** by utilizing the [GLLM Multimodal Audio to Text](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.audio import AudioLoader

source = "https://assets.analytics.glair.ai/generative/audio/sample-audio-1.mp3"

# initialize audio loader
loader = AudioLoader()

# load audio file
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
The loader will generate the following: [output JSON](https://assets.analytics.glair.ai/generative/audio/audioloader-output.json).
{% endstep %}
{% endstepper %}

## Other Audio To Text

You can use other audio-to-text to customize the implementation. In this example, we use `ProsaAudioToText` from [GLLM Multimodal ProsaAudioToText](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
from gllm_docproc.loader.audio import AudioLoader
from gllm_multimodal.modality_converter.audio_to_text import ProsaAudioToText

source = "https://assets.analytics.glair.ai/generative/audio/sample-audio-1.mp3"

# initialize other audio to text (in this case using ProsaAudioToText)
prosa_audio_to_text = ProsaAudioToText(api_key="...", url="...", model="...")

# initialize audio loader
loader = AudioLoader([prosa_audio_to_text])

# load audio file
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
The loader will hit GL Speech service to convert the audio file to text.
{% endstep %}
{% endstepper %}

GLLM Multimodal has the following implementations that you can use:

1. [GeminiAudioToText](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text/gemini_audio_to_text.py)
2. [GoogleCloudAudioToText](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text/google_cloud_audio_to_text.py)
3. [OpenAIWhisperAudioToText](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text/openai_whisper_audio_to_text.py)
4. [ProsaAudioToText](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text/prosa_audio_to_text.py)
5. [YouTubeTranscriptAudioToText](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-multimodal/gllm_multimodal/modality_converter/audio_to_text/youtube_transcript_audio_to_text.py)

## Custom Audio To Text

You can use fully custom audio-to-text to customize the implementation.

{% stepper %}
{% step %}
Create a script called `custom_audio_to_text.py`:

{% code lineNumbers="true" %}
```python
from gllm_multimodal.modality_converter.audio_to_text.audio_to_text import BaseAudioToText
from gllm_multimodal.modality_converter.schema.audio_transcript import AudioTranscript

class CustomAudioToText(BaseAudioToText):
  def __init__(self, ...):
    # your custom initialization

  async def convert(self, audio_source: str) -> list[AudioTranscript]:
    # your custom implementation
```
{% endcode %}
{% endstep %}

{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import CustomAudioToText
from gllm_docproc.loader.audio import AudioLoader

source = "https://assets.analytics.glair.ai/generative/audio/sample-audio-1.mp3"

# initialize custom audio to text (in this case using your own custom implementation)
custom_audio_to_text = CustomAudioToText(...)

# initialize audio loader
loader = AudioLoader([custom_audio_to_text])

# load audio file
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
The loader will use your custom implementation to convert the audio file to text.
{% endstep %}
{% endstepper %}
