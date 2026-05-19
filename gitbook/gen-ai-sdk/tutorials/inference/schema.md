---
icon: shapes
---

# Schema

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/schema) | **Tutorial**: [schema.md](schema.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/schema.html)

## What's a Schema?

The `gllm_inference.schema` module defines the data objects you work with across the SDK — inputs you send to invokers, outputs you receive, and configuration objects that control behavior. Understanding these schemas lets you construct inputs correctly and read outputs reliably.

## Attachment

An `Attachment` wraps a file (image, document, audio, etc.) so it can be passed as input to LM and EM Invokers. Three classes are available:

| Class | Description |
| --- | --- |
| `Attachment` | General-purpose. Downloads and stores the file locally as bytes. |
| `URLAttachment` | For externally-hosted files. The URL is passed directly to the provider — no download. |
| `UploadedAttachment` | Represents a file already uploaded to a provider's file storage. Carries an `id` and `provider`. |

**Loading an Attachment**

```python
from gllm_inference.schema import Attachment

# From a local file path
attachment = Attachment.from_path("path/to/image.jpeg")

# From a remote URL (downloads the file)
attachment = Attachment.from_url("https://example.com/image.png")

# From a data URL
attachment = Attachment.from_data_url("data:image/jpeg;base64,<base64_encoded_image>")

# From raw bytes
attachment = Attachment.from_bytes(b"<file_bytes>")
```

All factory methods auto-detect the MIME type and extension. An optional `filename` and `metadata` dict can be passed to any of them.

**URLAttachment**

Use when the file lives at an external URL and the provider can fetch it directly:

```python
from gllm_inference.schema import URLAttachment

attachment = URLAttachment(url="https://cdn.example.com/video.mp4")
# Or supply mime_type explicitly to skip auto-detection
attachment = URLAttachment(url="https://cdn.example.com/video.mp4", mime_type="video/mp4")
```

{% hint style="info" %}
Use `URLAttachment` when you want to avoid downloading large files. Use `Attachment.from_url` when you need the bytes locally.
{% endhint %}

**UploadedAttachment**

Returned by file-upload APIs rather than constructed directly. See [File Management](lm-invoker/file-management.md "mention") for how to obtain one.

---

## Message

`Message` represents a conversation turn. Use the class methods to construct messages by role:

```python
from gllm_inference.schema import Message

system_msg = Message.system("You are a helpful assistant.")
user_msg = Message.user("What is the capital of Indonesia?")
assistant_msg = Message.assistant("The capital of Indonesia is Jakarta.")
```

A `Message` can hold multiple content items — mix text and `Attachment` objects in the same message:

```python
from gllm_inference.schema import Attachment, Message

image = Attachment.from_path("path/to/chart.png")
user_msg = Message.user(["Describe this chart.", image])
```

---

## LMOutput

`LMOutput` is the object returned by LM Invoker calls. It contains one or more output items of different types (text, structured output, tool calls, attachments, thinking, etc.).

**Common accessors:**

```python
output = asyncio.run(lm_invoker.invoke("Hello!"))

output.text                 # str — first text response
output.texts                # list[str] — all text responses
output.structured_output    # dict | BaseModel | None — first structured output
output.tool_calls           # list[ToolCall]
output.attachments          # list[Attachment]
output.thinkings            # list[Thinking]
output.token_usage          # TokenUsage | None
output.duration             # float | None — invocation time in seconds
```

---

## ToolCall and ToolResult

`ToolCall` is produced by the model when it decides to invoke a tool. `ToolResult` is what you send back.

```python
from gllm_inference.schema import ToolCall, ToolResult

# ToolCall — received from LMOutput
tool_call: ToolCall = output.tool_calls[0]
print(tool_call.id)    # str
print(tool_call.name)  # str — the tool name
print(tool_call.args)  # dict[str, Any] — arguments

# ToolResult — send back to the model
result = ToolResult(id=tool_call.id, output="42")
```

---

## Thinking

`Thinking` represents the extended-thinking text produced by a model when thinking is enabled. Accessed from `LMOutput`:

```python
for t in output.thinkings:
    print(t.thinking)  # str — the raw thinking text
```

---

## TokenUsage

`TokenUsage` provides token consumption analytics for a completed invocation:

```python
usage = output.token_usage

usage.input_tokens   # int
usage.output_tokens  # int
usage.total_tokens   # int

# Detailed breakdowns
usage.input_details.cached_tokens    # int
usage.input_details.uncached_tokens  # int
usage.output_details.thinking_tokens # int
usage.output_details.response_tokens # int
```

---

## Configuration Schemas

### ThinkingConfig

Controls whether extended thinking is enabled for an invocation:

```python
from gllm_inference.schema.config import ThinkingConfig

config = ThinkingConfig(enabled=True)
```

### TruncationConfig

Controls how text inputs are truncated when they exceed the model's maximum length:

```python
from gllm_inference.schema.config import TruncationConfig, TruncateSide

config = TruncationConfig(
    max_length=1000,
    truncate_side=TruncateSide.RIGHT  # keep the start, truncate the end (default)
)
```

`TruncateSide.LEFT` keeps the end of the text; `TruncateSide.RIGHT` keeps the beginning.
