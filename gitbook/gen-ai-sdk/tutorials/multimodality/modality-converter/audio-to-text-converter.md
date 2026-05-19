# Audio to Text Converter

### Introduction

The Audio to Text Converter module provides a unified interface for transcribing audio content from multiple sources using different STT providers and VLMs. It supports various input formats including local files, URLs, base64-encoded strings, and YouTube videos.

### Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-multimodal"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-multimodal"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "gllm-multimodal"
```
{% endtab %}
{% endtabs %}

### Quickstart

Here is how to use `GeminiAudioToText` transcription:

```python
from gllm_multimodal.modality_converter.audio_to_text import GeminiAudioToText

converter = GeminiAudioToText(
    api_key="your-gemini-api-key",
    model="gemini-2.5-flash",  # Default model
    max_retries=3,  # Number of retry attempts
    timeout=300,  # Timeout in seconds
)
transcripts = asyncio.run(converter.convert("path/to/audio/file"))

for transcript in transcripts:
    print(
        f"[{transcript.start_time:.2f}s - {transcript.end_time:.2f}s] ({transcript.lang_id or 'unknown'}) {transcript.text}"
    )
```

**Output:**

```
[0.00s - 4.14s] (id) Speaker 1: Ini adalah teks di rentang detik 0 sampai 4.
[4.14s - 9.34s] (id) Speaker 1: Ini adalah teks di rentang detik 4 sampai 9.
[9.34s - 14.00s] (id) Speaker 1: Ini adalah teks di rentang detik 9 sampai 14.
```

## Supported Audio-to-Text Converters

The following converters are available in `gllm-multimodal`:

| Class | Provider | Description |
| ----- | -------- | ----------- |
| `GeminiAudioToText` | Google Gemini | Transcription via Gemini multimodal LLM (shown in Quickstart above). |
| `GoogleCloudAudioToText` | Google Cloud STT | Transcription using Google Cloud Speech-to-Text API. |
| `OpenAIWhisperAudioToText` | OpenAI Whisper | Speech-to-text via OpenAI's Whisper API. |
| `YouTubeTranscriptAudioToText` | YouTube | Retrieves transcripts directly from YouTube videos. |

All converters implement `BaseAudioToText` and expose a consistent `.convert(source)` interface, where `source` is a file path, URL, or YouTube video URL depending on the provider.

### How to Customize Your Prompt

`GeminiAudioToText` uses a default system and user prompt for transcription. Here is how to use a custom prompt:

```python
from gllm_multimodal.modality_converter.audio_to_text import GeminiAudioToText

converter = GeminiAudioToText(
    api_key="your-gemini-api-key",
    model="gemini-2.5-flash",  # Default model
    system_prompt="Custom system prompt",  # Optional
    user_prompt="Custom user prompt",  # Optional
    max_retries=3,  # Number of retry attempts
    timeout=300,  # Timeout in seconds
)
transcripts = asyncio.run(converter.convert("path/to/audio/file"))

for transcript in transcripts:
    print(
        f"[{transcript.start_time:.2f}s - {transcript.end_time:.2f}s] ({transcript.lang_id or 'unknown'}) {transcript.text}"
    )
```
