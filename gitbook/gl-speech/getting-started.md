---
icon: flag-checkered
---

# Getting Started

## GL Speech SDK

A Python library for the GL Speech API: speech-to-text (STT), text-to-speech (TTS), and webhooks.

### Getting Started

**Hello World:**

STT and TTS use different API keys and base URLs, so create two clients:

```python
from gl_speech_sdk import SpeechClient

stt_client = SpeechClient(api_key="your-stt-api-key", base_url="https://api.prosa.ai/v2/speech/")
tts_client = SpeechClient(api_key="your-tts-api-key", base_url="https://api.prosa.ai/v2/speech/")

# List STT models
models = stt_client.stt.list_models()
for m in models:
    print(m["name"], m["label"])

# Synthesize speech
result = tts_client.tts.synthesize(
    text="Hello, world!",
    model="tts-dimas-formal",
    wait=True
)
print(result.result)
```

For configuration, separate STT/TTS keys, transcribe, webhooks, and error handling, see [Cookbook](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gl-speech-sdk/examples).
