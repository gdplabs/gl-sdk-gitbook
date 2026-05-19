---
icon: subtitles
---

# Embedding Model (EM) Invoker

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/em_invoker) | **Tutorial**: [em-invoker.md](em-invoker.md "mention") | **Use Case:** [#index-your-data](../../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#index-your-data "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/em_invoker.html)

## What’s an EM Invoker?

The **EM invoker** is a unified interface designed to help you to convert inputs into into numerical vector representations. In this tutorial, you'll learn how to invoke an embedding model using `OpenAIEMInvoker` in **just a few lines of code**. You can also explore other types of EM Invokers, available [here](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/em_invoker.html).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Available EM Invokers

The EM invoker provides the following built-in implementations:

1. `AzureOpenAIEMInvoker`
2. `BedrockEMInvoker`
3. `CohereEMInvoker`
4. `GoogleEMInvoker`
5. `JinaEMInvoker`
6. `LangChainEMInvoker`
7. `OpenAIEMInvoker`
8. `TwelveLabsEMInvoker`
9. `VoyageEMInvoker`

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-inference
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-inference
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-inference
```
{% endtab %}
{% endtabs %}

## Quickstart

Let’s jump into a basic example using `OpenAIEMInvoker`. We’ll ask the model a simple question and print the response.

```python
import asyncio
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM

em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)
response = asyncio.run(em_invoker.invoke("Hello world!"))
print(f"Vectorized text:\n{response}")
```

**Expected Output**

```
Vectorized text:
[-0.010044993832707405, ..., 0.0008305096416734159]
```

That’s it! You've just made your first successful embedding model call using `OpenAIEMInvoker`. Fast, clean, and ready to scale into more complex use cases!

***

## Batch Invocation

EM invokers can also be used to vectorize multiple inputs at once. This can be done by providing a list of inputs. When processing a list of inputs, the output will be a list of vectors, where each element corresponds to an element in the input list. Let's try it!

```python
import asyncio
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_inference.model import VoyageEM
from gllm_inference.schema import Attachment

text1 = "Hello world!"
text2 = "The weather is sunny today."
image = Attachment.from_path("path/to/image.png")

em_invoker = VoyageEMInvoker(VoyageEM.VOYAGE_MULTIMODAL_3)
response = asyncio.run(em_invoker.invoke([text1, text2, image]))
print(f"Vectorized texts:\n{response}")
```

**Expected Output**

```
Vectorized texts:
[
    [0.0216064453125, ..., 0.05126953125],  # Result of text1
    [0.023193359375, ..., 0.00653076171875],  # Result of text2
    [0.029541015625, ..., -0.034912109375],  # Result of image
]
```

***

## Multimodal Input

Some embedding model providers, such as [**Voyage**](https://www.voyageai.com/), also have the capability to vectorize **more than just text!** Let's try to embed an image using `VoyageEMInvoker`. To do this, you can get a Voyage [API key](https://docs.voyageai.com/docs/api-key-and-installation) and export it as an environment variable.

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
export VOYAGE_API_KEY="pa-..."
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
$env:VOYAGE_API_KEY = "pa-..."
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```sh
set VOYAGE_API_KEY="pa-..."
```
{% endtab %}
{% endtabs %}

Then, we can embed multimodal inputs such as image by loading them as an `Attachment` object. See [schema.md](schema.md#attachment "mention") for all loading methods.

```python
import asyncio
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_inference.model import VoyageEM
from gllm_inference.schema import Attachment

image = Attachment.from_path("path/to/image.png")

em_invoker = VoyageEMInvoker(VoyageEM.VOYAGE_MULTIMODAL_3)
response = asyncio.run(em_invoker.invoke(image))
print(f"Vectorized text:\n{response}")
```

**Expected Output**

```
Vectorized text:
[0.0296630859375, ..., -0.034912109375]
```

And there it is, you've successfully vectorized an image into its numerical vector representations!

***

## Text Truncation

**Text truncation** allows you to control how text inputs are handled when they exceed the maximum length supported by the embedding model. This is particularly useful when dealing with long documents or when you need to ensure consistent input lengths.

Truncation can be configured using the `TruncationConfig` class (see [schema.md](schema.md#truncationconfig "mention")) with the following parameters:

1. **max\_length**: Maximum number of characters to keep (required)
2. **truncate\_side**: Which side to truncate from (defaults to `TruncateSide.RIGHT`)
   * `TruncateSide.LEFT`: Keep the end of the text, truncate from the beginning
   * `TruncateSide.RIGHT`: Keep the beginning of the text, truncate from the end (default)

```python
import asyncio
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_inference.schema.config import TruncationConfig, TruncateSide

# Configure text truncation
truncation_config = TruncationConfig(
    max_length=1000,
    truncate_side=TruncateSide.RIGHT
)

em_invoker = OpenAIEMInvoker(
    OpenAIEM.TEXT_EMBEDDING_3_SMALL,
    truncation_config=truncation_config
)

long_text = "This is a very long text that exceeds the maximum length..." * 100
response = asyncio.run(em_invoker.invoke(long_text))
print(f"Vectorized text:\n{response}")
```

***

## Vector Fusion

Vector fusion is a feature that enables fusing multiple results into a single vector. This allows the EM invoker to embed mixed modality contents, represented as tuples of contents.

This feature can be enabled by providing a vector fuser to the `vector_fuser` parameter. Two vector fuser strategies are available:

* **`AverageVectorFuser`** — fuses vectors by averaging them element-wise.
* **`SumVectorFuser`** — fuses vectors by summing them element-wise.

**Example using `SumVectorFuser`:**

```python
import asyncio
from gllm_inference.em_invoker import VoyageEMInvoker
from gllm_inference.em_invoker.vector_fuser import SumVectorFuser
from gllm_inference.model import VoyageEM
from gllm_inference.schema import Attachment

text = "Hello world!"
image = Attachment.from_path("path/to/image.png")
mixed_content = (text, image)

em_invoker = VoyageEMInvoker(VoyageEM.VOYAGE_MULTIMODAL_3, vector_fuser=SumVectorFuser())
response = asyncio.run(em_invoker.invoke([text, image, mixed_content]))
print(f"Vectorized texts:\n{response}")
```

**Expected Output**

```
Vectorized texts:
[
    [0.0216064453125, ..., 0.05126953125],  # Result of text
    [0.023193359375, ..., 0.00653076171875],  # Result of image
    [0.029541015625, ..., -0.034912109375],  # Result of the mixed content (text + image, sum-fused)
]
```

{% hint style="info" %}
Some EM invokers, such as the `VoyageEMInvoker`, has a built-in vector fusion capability, essentially allowing it to perform vector fusion without the need of providing any vector fuser.
{% endhint %}

***

## Retry & Timeout

**Retry & timeout** functionality provides **robust error handling and reliability** for embedding model interactions. It allows you to **automatically retry failed requests** and **set time limits** for operations, ensuring your applications remain responsive and resilient to network issues or API failures.

Retry & timeout can be configured via the `RetryConfig` class' parameters:

1. **max\_retries**: Maximum number of retry attempts (defaults to 3 maximum retry attempts).
2. **timeout**: Maximum time in seconds to wait for each request (defaults to 30.0 seconds). To disable timeout, this parameter can be set to `None`.

You can also configure other parameters available [here](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-core/gllm_core/utils/retry.py#L28-L44). Now let's try to apply it to our EM invoker!

```python
import asyncio
from gllm_core.retry import RetryConfig
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM

retry_config = RetryConfig(max_retries=3, timeout=100)
em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL, retry_config=retry_config)
response = asyncio.run(em_invoker.invoke("Hello world!"))
print(f"Vectorized text:\n{response}")
```

***

{% include "../../../.gitbook/includes/troubleshooting.md" %}

***

And there we go! You've successfully completed the tutorial of using EM invokers!
