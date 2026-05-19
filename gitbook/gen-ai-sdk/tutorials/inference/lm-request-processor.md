---
icon: head-side-gear
---

# LM Request Processor (LMRP)

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-inference/gllm_inference/request_processor/lm_request_processor.py) | **Tutorial:** [lm-request-processor.md](lm-request-processor.md "mention") | **Use Case:** [utilize-language-model-request-processor](../../guides/utilize-language-model-request-processor/ "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/request_processor.html#gllm_inference.request_processor.LMRequestProcessor) | [Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/inference/lm_request_processor)

{% hint style="warning" %}
**Deprecation Notice:** `LMRequestProcessor` is planned to be deprecated in a future release. For new implementations, please use [LM Invoker Prompt Operations](lm-invoker/prompt-operations.md), which provides a more flexible replacement pattern.
{% endhint %}

## What’s an LMRP?

The **LM Request Processor (LMRP)** is an orchestrator module that wraps a prompt builder and an LM invoker to perform end-to-end LM invocation in a single process. In this tutorial, you'll learn how to use the `LMRequestProcessor` in **just a few lines of code**.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

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

Let’s jump into a basic example using `LMRequestProcessor`. This basic LMRP usage will only utilize a simple `PromptBuilder` and an `OpenAILMInvoker`.

```python
import asyncio
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.request_processor import LMRequestProcessor

prompt_builder = PromptBuilder(
    system_template="Talk like a pirate.",
    user_template="What is the capital city of Indonesia?",
)
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
output = asyncio.run(lm_request_processor.process())
print(f"Response: {output.text}")
```

**Expected Output**

```
Response: Arrr, the capital o' Indonesia be Jakarta.
```

## Using Prompt Variables

The LMRP also supports passing prompt variables to the prompt builder. Let's try it out!

```python
import asyncio
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.request_processor import LMRequestProcessor

role = "pirate"
query = "What is the capital city of Indonesia?"

prompt_builder = PromptBuilder(system_template="Talk like a {role}.", user_template="{query}")
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
output = asyncio.run(lm_request_processor.process(role=role, query=query))
print(f"Response: {output.text}")
```

**Expected Output**

```
Response: Arrr, the cap’n o' Indonesia be Jakarta.
```

## Adding History

The LMRP also supports passing history to the prompt builder. Let's try it out!

```python
import asyncio
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import Message

history = [
    Message.user("What is the capital city of Indonesia?"),
    Message.assistant("Jakarta is the capital city of Indonesia."),
]
prompt_builder = PromptBuilder(user_template="In what island is it located?")
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
output = asyncio.run(lm_request_processor.process(history=history))
print(f"Response: {output.text}")
```

**Expected Output**

```
Response: Java.
```

## Adding Extra Contents

The LMRP also supports passing extra contents to the prompt builder. Let's try it out!

```python
import asyncio
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.request_processor import LMRequestProcessor
from gllm_inference.schema import Attachment

attachment = Attachment.from_path("path/to/tiger.jpg")
prompt_builder = PromptBuilder(user_template="What image is this?")
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
output = asyncio.run(lm_request_processor.process(extra_contents=[attachment]))
print(f"Response: {output.text}")
```

**Expected Output**

```
Response: A tiger (the striped big cat).
```

## Automatic Tool Execution

When tools are provided to the language model, the LMRP has the capability to automatically executes the tools until the desired final response is produced. Let's test it out!

```python
import asyncio
from gllm_core.schema import tool
from gllm_inference.prompt_builder import PromptBuilder
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.request_processor import LMRequestProcessor
​
@tool
def get_weather(city: str) -> str:
    """Get the weather of a city."""
    return f"The weather of {city} is sunny."
​
prompt_builder = PromptBuilder(user_template="What is the weather in Jakarta?"​
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[get_weather])
lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
output = asyncio.run(lm_request_processor.process())
print(f"Response: {output.text}")
```

**Expected Output**

```
Response: Jakarta is sunny right now.
```

In the case that we don't want the LMRP to automatically executes the tool, we can set the `auto_execute_tools` param to `False`. In this case, the LMRP will directly return the `ToolCall` objects produced the language models. Let's try this by changing the following line from the above example:

```python
...
output = asyncio.run(lm_request_processor.process(auto_execute_tools=False))
print(f"Response: {output.tool_calls}")
...
```

**Expected Output**

```
Response: [
    ToolCall(
        id='call_ufT7Ym9IPlWTN66TVcKnFJLA',
        name='get_weather',
        args={'city': 'Jakarta'},
    )
]
```

## Use LM Request Processor Builder (Recommended)

This is a simpler way to initialize an LMRP, in which you can pass the essential parameters directly without manually creating individual components like prompt builders and LM invokers.

The `build_lm_request_processor()` function is a **convenience method** that automatically creates and configures all the necessary components for you:

{% code lineNumbers="true" %}

```python
import os
from gllm_inference.request_processor import build_lm_request_processor

# Simple LMRP creation with essential parameters
lm_request_processor = build_lm_request_processor(
    model_id="openai/gpt-5-nano",
    credentials=os.getenv("OPENAI_API_KEY"),
    system_template="You are a helpful assistant that provides accurate information.",
    user_template="Please answer this question: {question}",
)
```

{% endcode %}

This single function call automatically:

1. Creates a `PromptBuilder` with your templates
2. Sets up the appropriate `LMInvoker` for your model
3. Combines them into a complete `LMRequestProcessor`

---

Congratulations! We've successfully completed the tutorial to use the LMRP!
