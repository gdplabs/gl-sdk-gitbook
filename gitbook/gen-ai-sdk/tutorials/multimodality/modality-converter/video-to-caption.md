# Video to Caption

## Introduction

The Video to Caption component converts videos into natural language captions using multimodal Language Models. It is built on top of the `LMBasedVideoToCaption` converter, which uses `LMRequestProcessor` and multimodal LM invokers to understand both the visual and temporal aspects of a video and return structured captions.

Typical use cases include:

1. Generating captions for long-form videos to power downstream search or retrieval.
2. Creating short highlight captions for clips in social feeds or internal video libraries.
3. Producing textual context that can be fed into RAG pipelines or evaluation workflows.

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash

# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-multimodal gllm-inference
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell

# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-multimodal gllm-inference
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash

# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-multimodal gllm-inference
```

{% endtab %}
{% endtabs %}

## Quickstart

The simplest way to initialize the Video to Caption component is to use the built-in preset.

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.video_to_text.video_to_caption import LMBasedVideoToCaption

video = Attachment.from_path("./sample_video.mp4")
converter = LMBasedVideoToCaption.from_preset("default")

# The converter expects raw bytes for the video input
result = asyncio.run(converter.convert(video.data))

# The result is a TextResult object
print(f"Video Summary: {result.result}")

# Access detailed segments from metadata
for segment in result.metadata["segments"]:
    print(f"Segment ({segment['start_time']}s - {segment['end_time']}s):")
    for caption in segment.get("segment_caption", []):
        print(f"  - {caption}")
```

### Expected output format

The `LMBasedVideoToCaption` returns a `TextResult` object with the following structure:

- `result` (str): A high-level summary of the entire video.
- `tag` (str): The tag identifying the result type (always `"caption"`).
- `metadata` (dict): Contains detailed captioning information:
  - `video_summary` (str): Same as `result`, the video summary.
  - `segments` (list): List of video segments, each containing:
    - `start_time` (float): Segment start time in seconds.
    - `end_time` (float): Segment end time in seconds.
    - `segment_caption` (list\[str]): Captions for the segment.
    - `keyframes` (list): Keyframe descriptions with `time_offset` and `caption`.
    - `transcripts` (list): Transcript entries with `text`, `start_time`, `end_time`, and `lang_id`.

## Contextual video captioning

Sometimes the raw video alone does not provide enough context. Video to Caption supports passing **additional metadata** to help the model generate more relevant and domain-specific captions.

The supported fields are defined by the `Caption` schema and include:

1. `image_one_liner` (str, optional): Brief one-line summary or title of the video.
2. `image_description` (str, optional): Longer free-form description of what the video is about.
3. `domain_knowledge` (str, optional): Domain-specific hints that are not present in the description.
4. `image_metadata` (dict, optional): Arbitrary metadata, such as duration or frame rate.
5. `number_of_captions` (int, optional): Number of captions to generate.

### Using image one liner and description

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.video_to_text.video_to_caption import LMBasedVideoToCaption

video = Attachment.from_path("./product_demo.mp4")
converter = LMBasedVideoToCaption.from_preset("default")

result = asyncio.run(
    converter.convert(
        video.data,
        image_one_liner="Product demo walkthrough",
        image_description="A short screen recording that walks through the main features of the product dashboard.",
        number_of_captions=3,
    )
)

print(f"Video Summary: {result.result}")
for segment in result.metadata["segments"]:
    for caption in segment.get("segment_caption", []):
        print(f"- {caption}")
```

### Adding domain knowledge and metadata

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.video_to_text.video_to_caption import LMBasedVideoToCaption


video = Attachment.from_path("./conference_talk.mp4")
converter = LMBasedVideoToCaption.from_preset("default")

result = asyncio.run(
    converter.convert(
        video.data,
        image_one_liner="Conference keynote talk",
        image_description="Keynote session about scaling RAG systems in production.",
        domain_knowledge="RAG, vector store, retriever, response synthesizer, production workloads",
        image_metadata={"duration_seconds": 900, "speaker": "Jane Doe"},
        number_of_captions=5,
    )
)

print(f"Video Summary: {result.result}")
for segment in result.metadata["segments"]:
    for caption in segment.get("segment_caption", []):
        print(f"- {caption}")
```

### Using attachment context

Video to Caption also supports **attachment context**, which allows you to pass supporting attachments such as slides, images, or transcripts alongside the main video. These attachments are exposed to the LVLM as additional context to improve caption quality.

```python
import asyncio

from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.video_to_text.video_to_caption import LMBasedVideoToCaption


video = Attachment.from_path("./webinar.mp4")
supporting_attachments = [
    Attachment.from_path("./webinar_slides.pdf"),
    Attachment.from_path("./webinar_outline.txt"),
]

converter = LMBasedVideoToCaption.from_preset("default")

result = asyncio.run(
    converter.convert(
        video.data,
        image_one_liner="Webinar: Introduction to GL SDK",
        image_description="Recorded webinar that introduces GL SDK concepts and shows a live coding demo.",
        attachments_context=supporting_attachments,
        number_of_captions=4,
    )
)

print(f"Video Summary: {result.result}")
for segment in result.metadata["segments"]:
    for caption in segment.get("segment_caption", []):
        print(f"- {caption}")
```

## Customize model and prompt

By default, the preset uses the configured LVLM from the multimodality presets. For advanced use cases, you can provide your own `LMRequestProcessor` configuration to fully control model, prompt, and parsing behavior.

```python
import asyncio
import os

from dotenv import load_dotenv
from gllm_inference.request_processor import build_lm_request_processor
from gllm_inference.schema import Attachment
from gllm_multimodal.modality_converter.video_to_text.video_to_caption import LMBasedVideoToCaption


load_dotenv()

lmrp = build_lm_request_processor(
    model_id=os.getenv("VIDEO_CAPTION_MODEL_ID", "google/gemini-2.5-flash"),
    credentials=os.getenv("GOOGLE_API_KEY"),
    system_template=(
        "Create {number_of_captions} concise captions that describe the provided video. "
        "Your output must be a valid JSON object with 'video_summary' and 'segments' array."
    ),
    user_template=(
        "<INPUT_STRUCTURE>"
        "Title: {image_one_liner}\n"
        "Description: {image_description}\n"
        "Domain knowledge: {domain_knowledge}\n"
        "Filename: {filename}\n"
        "Metadata: {image_metadata}"
        "</INPUT_STRUCTURE>"
    ),
    output_parser_type="json",
)

video = Attachment.from_path("./demo.mp4")

converter = LMBasedVideoToCaption(lm_request_processor=lmrp)
result = asyncio.run(converter.convert(
    video.data,
    image_one_liner="Demo recording",
    image_description="Short demo session that walks through the GL SDK feature overview.",
    number_of_captions=3,
))

print(f"Video Summary: {result.result}")
print(f"Segments: {result.metadata}")
```
