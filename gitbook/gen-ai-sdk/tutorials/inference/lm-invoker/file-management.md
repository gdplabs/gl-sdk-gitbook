---
icon: files
---

# File Management

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [file-management.md](file-management.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

**Supported by:** `AnthropicLMInvoker`, `GoogleLMInvoker`, `OpenAILMInvoker`

## What is file management?

File management is a feature that allows the language model to **manage uploaded files** in their server side. These files can then be used as inputs during invocations.

File management is only available for certain LM invokers. This feature can be accessed via the `file` attribute of the LM invoker. As an example, let's try to upload a file using `GoogleLMInvoker` and then use it as an input during invocation.

### Init an LM Invoker

First of all, let's create a `GoogleLMInvoker` that we will use to manage the data store:

```python
from dotenv import load_dotenv
load_dotenv()

from gllm_inference.lm_invoker import GoogleLMInvoker

lm_invoker = GoogleLMInvoker("gemini-2.5-flash-lite")
```

### Upload a File

Next, let's upload a file. The `upload()` method will output an `UploadedAttachment` object to be used in later operations.

```python
from gllm_inference.schema import Attachment

file = Attachment.from_path('path/to/file.pdf')
uploaded_file = await lm_invoker.file.upload(attachment)
```

### List the Files

We can verify that the file has been successfully uploaded to the server side by using the `list()` method.

```python
files = await lm_invoker.file.list()

if not files:
    print("No files found.")

for file in files:
    print(f" - {file}")
```

### Invoke LM invoker with Uploaded File

Then, we can use the uploaded file as inputs during invocation.

```python
inputs = [uploaded_file, "Explain this file in a single sentence"]
output = await lm_invoker.invoke(inputs)
print(f"output:\n{output}")
```

### Delete the File

Finally, if the file is no longer used, it can be deleted via the `delete()` method.

```python
await lm_invoker.file.delete(uploaded_file)
```

{% include "../../../../.gitbook/includes/troubleshooting.md" %}
