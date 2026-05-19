---
icon: comments-question
---

# Language Model (LM) Invoker

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [.](./ "mention")| **Use Case:** [utilize-language-model-request-processor](../../../guides/utilize-language-model-request-processor/ "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html) | [Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/inference/lm_invoker)

## What’s an LM Invoker? <a href="#whats-an-em-invoker" id="whats-an-em-invoker"></a>

The **LM invoker** is a unified interface designed to help you interact with language models to generate outputs based on the provided inputs. In this tutorial, you'll learn how to invoke a language model using `OpenAILMInvoker` in **just a few lines of code**. You can also explore other types of LM Invokers, available [here](https://api.python.docs.glair.ai/generative-internal/library/gllm_inference/api/lm_invoker.html).

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../../prerequisites.md "mention") page.

</details>

## Available LM Invokers

The LM invoker provides the following built-in implementations:

1. `AnthropicLMInvoker`
2. `AzureOpenAILMInvoker`
3. `BedrockLMInvoker`
4. `DatasaurLMInvoker`
5. `DeepSeekLMInvoker`
6. `GoogleLMInvoker`
7. `LangChainLMInvoker`
8. `LiteLLMLMInvoker`
9. `OpenAIChatCompletionsLMInvoker`
10. `OpenAILMInvoker`
11. `PortkeyLMInvoker`
12. `SeaLionLMInvoker`
13. `XAILMInvoker`

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
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-inference"
```
{% endtab %}
{% endtabs %}

## Quickstart

**Initialization and Invoking**

Let’s jump into a basic example using `OpenAILMInvoker`. We’ll ask the model a simple question and print the output.

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
output = asyncio.run(lm_invoker.invoke("What is the capital city of Indonesia?"))
print(f"output: {output.text}")
```

**Output:**

```
output: Jakarta.
```

## Streaming

To achieve streaming, simply pass an event emitter when invoking the LM invoker. This allows us to process the generated tokens without having to wait for the entire generation process to finish.

```python
import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

event_emitter = EventEmitter.with_print_handler()
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
output = asyncio.run(lm_invoker.invoke("What is the capital city of Indonesia?"))
print(f"output: {output}")
```

In the example above, we're using the `PrintEventHandler` which is intended to print the streamed tokens in a beautified format. For more details about the event emitter, please refer to the [event emitter tutorial page](../../core/event-emitter.md).

***

## Message Roles

Modern LMs understand context better when you structure inputs like a real conversation. That’s where **message roles** come in. You can simulate multi-turn chats, set instructions, or give memory to the model through a structured message format.

**Example 1: Passing a system message**

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Message

messages = [
    Message.system("Talk like a pirate."),
    Message.user("Hi, there! How are you doing?")
]

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
output = asyncio.run(lm_invoker.invoke(messages))
print(f"output: {output.text}")
```

**Output:**

<pre><code><strong>output: Ahoy, matey! I be doin' well, savvy? How be ye farin' on this fine day?
</strong></code></pre>

**Example 2: Simulating a multi-turn conversation**

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Message

messages = [
    Message.system("You are a helpful assistant."),
    Message.user("What is the capital of France?"),
    Message.assistant("The capital of France is Paris."),
    Message.user("What about Indonesia?"),
]

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
output = asyncio.run(lm_invoker.invoke(messages))
print(f"output: {output.text}")

```

**Output:**

```
output: The capital of Indonesia is Jakarta.
```

***

## Multimodal Input

Our LM Invokers support **attachments** (images, documents, etc.). This lets you send rich content and ask the model to analyze or describe them. See [schema.md](../schema.md#attachment "mention") for how to load files into an `Attachment` object.

**Example 1: Describe an image**

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Attachment

image = Attachment.from_path("path/to/dog.jpeg")

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
output = asyncio.run(lm_invoker.invoke(["What is this?", image]))
print(f"output: {output.text}")
```

**Output:**

```
output: A cute golden retriever puppy.
```

***

**Example 2: Analyze a PDF**

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_inference.schema import Attachment

URL = "https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf"
document = Attachment.from_url(URL)

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO)
output = asyncio.run(lm_invoker.invoke(["What is the title of this file?", document]))
print(f"output: {output.text}")
```

**Output:**

```
output: This is the scientific paper titled "Attention Is All You Need".
```

***

**Supported Attachment Types**

Each LM might support different types of inputs. You can find more about supported type for each LM Invoker [here](https://api.python.docs.glair.ai/generative-internal/library/gllm_inference/api/lm_invoker.html).

***

## Structured Output

In many real-world applications, we don't just want natural language outputs — we want **structured data** that our programs can parse and use directly.

You can define your expected output using:

1. A **Pydantic `BaseModel` class** (recommended).
2. A **JSON schema dictionary** compatible with Pydantic's schema format.

When structured output is enabled, structured output results are stored in the outputs attribute of the LMOutput object and can be accessed via the `structured_outputs` property. The output type depends on the input schema:

1. **Pydantic instance** → The output will be a Pydantic BaseModel instance.
2. **JSON schema dict** → The output will be a Python dictionary.

**Using a Pydantic `BaseModel` (Recommended)**

You can define your expected output format as a Pydantic class. This ensures strong type safety and makes the output easier to work with in Python.

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from pydantic import BaseModel

class Animal(BaseModel):
    name: str
    size: str
    diet: str
    color: list[str]
    legs: int

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, response_schema=Animal)
output = asyncio.run(lm_invoker.invoke("Describe a chicken!"))
print(f"output: {output.structured_output}")

```

**Output:**

```
output: Animal(
    name='Chicken',
    size='Medium',
    diet='Omnivore',
    color=['varies by breed'],
    legs=2,
)
```

**Using a JSON Schema Dictionary**

Alternatively, you can define the structure using a JSON schema dictionary.

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

animal_schema = {
    "properties": {
        "color": {
            "items": {"type": "string"},
            "title": "Color",
            "type": "array"
        },
        "diet": {"title": "Diet", "type": "string"},
        "legs": {"title": "Legs", "type": "integer"},
        "name": {"title": "Name", "type": "string"},
        "size": {"title": "Size", "type": "string"}
    },
    "required": ["name", "size", "diet", "color", "legs"],
    "title": "Animal",
    "type": "object",
}

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, response_schema=animal_schema)
output = asyncio.run(lm_invoker.invoke("Describe a chicken!"))
print(f"output: {output.structured_output}")
```

**Output**

```
output: {
    'color': ['reddish-brown feathers', 'white underparts'],
    'diet': 'Omnivore; seeds, grains, insects, greens',
    'legs': 2,
    'name': 'Chicken',
    'size': 'Medium',
}
```

If JSON schema is used, it must still be compatible with Pydantic's JSON schema, especially for complex schemas. For this reason, it is recommended to create the JSON schema using Pydantic's `model_json_schema` method.

```python
animal_schema = Animal.model_json_schema()
```

***

## Tool Calling

**Tool calling** means letting a language model **call external functions** to help it solve a task. It allows the AI to **interact with external functions and APIs** during the conversation, enabling dynamic computation, data retrieval, and complex workflows.

Think of it as:

> The LM is smart at reading and reasoning, but when it needs to calculate or get external data, it picks up the phone and calls your "tool".

For more information about tools definition, please refer to [this guide](../../core/tool.md).

**LM Invocation with Tool**

Let's try to integrate a simple math operation tool to our LM invoker!

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM
from gllm_core.schema.tool import tool

@tool
def get_weather(city: str) -> str:
    """Get the weather of a city.

    Args:
        city (str): The city to get the weather of.

    Returns:
        str: The weather of the city.
    """
    return f"The weather of {city} is sunny."

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, tools=[get_weather])
output = asyncio.run(lm_invoker.invoke("What is the weather of Jakarta?"))
print(f"output: {output.tool_calls}")
```

**Output:**

```
output: [
    ToolCall(
        id='call_BjoVYmFI1CkkSNTzP3LtkGRK',
        name='get_weather',
        args={'city': 'Jakarta'},
        data=None,
    )
]
```

When the LM Invoker is invoked with tool calling capability, the model will return the tool calls. In this case, we still need to execute the tools and feed the result back to the LM invoker ourselves. If you'd like to handle this looping process automatically, please refere to the [LM Request Processor](../lm-request-processor.md) component.

***

## Native Tools

**Native tools** are a specific set tools that allow the language model to execute certain **built-in capabilities** during the invocation, enabling dynamic computation, data retrieval, and complex workflows. Similar to the **user-defined tools**, the **native tools** can be enabled by passing them through the LM invoker's `tools` parameter.

Each type of native tools is only available for certain LM invokers. Please find the available **native tools** below:

1. [**Code interpreter**](image-generation.md) — Writes and runs Python code in a sandboxed environment.
2. [**Data Store**](data-store-management.md) — Performs built-in RAG by utilizing managed data stores as internal knowledge base.
3. [**Image generation**](image-generation.md) — Generates an image based on the provided query.
4. [**MCP Server**](mcp-server.md) — Uses remote MCP servers to give models new capabilities.
5. [**MCP Connector**](mcp-connector.md) — Retrieves data from remote MCP connectors.
6. [**Skill**](skills.md) — Manages custom skills on the provider's server side.
7. [**Web search**](web-search.md) — Searches the web for relevant information.

***

## Thinking

Certain language model providers and models supports thinking. Thinking allows models to produce an internal chain of thought before responding to the user. This enables model to perform advanced tasks such as complex problem solving, coding, scientific reasoning, and multi-step planning for agentic workflows.

When thinking is enabled, thinking results are stored in the `outputs` attribute of the `LMOutput` object and can be accessed via the `thinkings` property.

Let's try to perform thinking by using OpenAI's `gpt-5-nano` model:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, thinking=True)

query = "Solve x^2 + 2x + 1 = 0"
output = asyncio.run(lm_invoker.invoke(query))
for item in output.outputs:
    print(f"=== Output item: {item.type!r} ===\n{item.output}\n")
```

**Output:**

```
=== Output item: 'thinking' ===
id='rs_010dc18bedf628330069688c3967a88194abd178f92ef8acaa'
thinking="""
**Solving quadratic equations**\n\nThe user asks me to solve the equation x^2 + 2x + 1 = 0.
This factors to (x+1)^2 = 0, so the double root is x = -1. I can concisely show the steps.
Additionally, I should note the discriminant calculation, which is b² - 4ac = 0.
If the user wants a step-by-step breakdown, I can explain that recognizing it's a perfect square
helps solve it. Ultimately, the final answer is x = -1 (double root).
"""

=== Output item: 'text' ===
x^2 + 2x + 1 = 0 factors as (x + 1)^2 = 0.
So x = -1 (a double root).
```

For more fine-grained control, you can use `ThinkingConfig` to pass provider-specific thinking parameters. Provider-specific parameters can be found in the provider's documentation.

{% hint style="info" %}
Pass the provider specific parameter in `kwargs`
{% endhint %}

```python
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.schema import ThinkingConfig

thinking_config = ThinkingConfig(enabled=True, kwargs={"effort": "high"})
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, thinking=thinking_config)
```

***

## Output Analytics

**Output analytics** enables you to collect detailed metrics and insights about your language model invocations. When output analytics is enabled, the output includes the following extra attributes:

1. **`token_usage`** : Input and output token counts.
2. **`duration`** : Time taken to generate the output.
3. **`finish_details`**: Additional details about how the generation finished.

To enable output analytics, simply need to set the `output_analytics` parameter to `True`.

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, output_analytics=True)
output = asyncio.run(lm_invoker.invoke("What is the capital of France?"))
print(f"output: {output}")
```

**Output:**

```
output: LMOutput(
    outputs=[LMOutputItem(type='text', output='Paris.')],
    token_usage=TokenUsage(
        input_tokens=13,
        output_tokens=177,
        input_token_details=InputTokenDetails(cached_tokens=0, uncached_tokens=13),
        output_token_details=OutputTokenDetails(thinking_tokens=128, response_tokens=49),
    ),
    duration=4.146970510482788,
    finish_details={'status': 'completed', 'incomplete_details': {'reason': None}}
)
```

***

## Retry & Timeout

**Retry & timeout** functionality provides **robust error handling and reliability** for language model interactions. It allows you to **automatically retry failed requests** and **set time limits** for operations, ensuring your applications remain responsive and resilient to network issues or API failures.

Retry & timeout can be configured via the `RetryConfig` class' parameters:

1. **max\_retries**: Maximum number of retry attempts (defaults to 3 maximum retry attempts).
2. **timeout**: Maximum time in seconds to wait for each request (defaults to 30.0 seconds). To disable timeout, this parameter can be set to `None`.

Let's try to apply it to our LM invoker!

```python
import asyncio
from gllm_core.retry import RetryConfig
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.model import OpenAILM

retry_config = RetryConfig(max_retries=3, timeout=100)
lm_invoker = OpenAILMInvoker(OpenAILM.GPT_5_NANO, retry_config=retry_config)
output = asyncio.run(lm_invoker.invoke("What is the capital of France?"))
print(f"output: {output}")
```

***

## Extra Capabilities

Some LM invokers also provide additional capabities that are useful in certain cases:

1. [**Input Transformer**](input-transformer.md) — To transform the language model messages input before invocation.
2. [**Output Transformer**](output-transformer.md) — To transform the raw output from the language model into a different format or structure.
3. [**Prompt Operations**](prompt-operations.md) — To configure reusable prompt templates and invoke with template variables.
4. [**Batch Invocation**](batch-invocation.md) — To manage batch requests for cheaper but slower invocations.
5. [**File Management**](file-management.md) — To manage uploaded files in their server side. These files can then be used as inputs during invocations.
6. [**Data Store Management**](data-store-management.md) — To manage built-in data stores to be used as internal knowledge base. This allows the LM invoker to perform built-in RAG (Retrieval-Augmented Generation).
7. [**Context Management**](context-management.md) — To estimate request size and check model context limits before invocation.
8. [**[BETA] Custom Processing Hooks**](custom-processing-hooks.md) — To run custom `output_hooks` and `streaming_hooks` in `OpenAILMInvoker` output processing.

## Convenience Builder: `build_lm_invoker`

If you want to instantiate an LM invoker from a model id string without manually selecting a provider-specific class, you can use `build_lm_invoker`.

This helper will detect the provider from `model_id` and return the corresponding LM invoker implementation.

Besides `model_id`, there are two optional parameters:

1. `credentials` - provider credentials (for example an API key string, a credentials dictionary, or a credentials file path for supported providers). If omitted, credentials are loaded from environment variables when supported by the provider.
2. `config` - additional provider-specific runtime options, such as generation settings or provider configuration values.

Example 1 - only `model_id` (credentials from environment variables):

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(model_id="openai/gpt-5-nano")
```

Example 2 - full parameters:

```python
from gllm_inference.lm_invoker import build_lm_invoker

lm_invoker = build_lm_invoker(
    model_id="openai/gpt-5-nano",
    credentials="sk-...",
    config={"thinking": True},
)
```

For complete model id formats and supported providers, refer to [Supported Models](../../../resources/supported-models/README.md#language-models-lms).

{% include "../../../../.gitbook/includes/troubleshooting.md" %}
