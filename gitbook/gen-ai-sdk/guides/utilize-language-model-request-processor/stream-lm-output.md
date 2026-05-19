---
icon: signal-stream
---

# Stream LM Output

This guide will walk you through creating real-time streaming responses using LM Request Processor (LMRP) with event handling.

**Stream output with LMRP** allows you to receive AI responses **in real-time as tokens are generated**, providing immediate feedback to users while maintaining the full pipeline capabilities of LMRP including prompt formatting and processing.

For example, when asking about Tokyo travel recommendations, instead of waiting for the complete response, you can see each word appearing **progressively**: "Here" → "are" → "some" → "great" → "activities" → "in" → "Tokyo" → "..."

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.
2. A working OpenAI API key configured in your environment variables.

You should be familiar with these concepts and components:

1. [lm-invoker](../../tutorials/inference/lm-invoker/ "mention")
2. [lm-request-processor.md](../../tutorials/inference/lm-request-processor.md "mention")
3. [prompt-builder.md](../../tutorials/inference/prompt-builder.md "mention")

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/inference/lm_request_processor/lm_request_processor_streaming" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference gllm-core
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference gllm-core
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference gllm-core
```

{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Environment Configuration**

Ensure you have a file named `.env` in your project directory with the following content:

```env
OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

{% hint style="info" %}
Replace `<YOUR_OPENAI_API_KEY>` with your actual OpenAI API key.
{% endhint %}
{% endstep %}
{% endstepper %}

---

## Build Your Streaming LMRP System

### 1) Set Up Event Handling Components

The **event system** manages real-time token streaming from the language model:

{% stepper %}
{% step %}
**Import Required Libraries**

Start by importing the necessary dependencies for streaming:

{% code lineNumbers="true" %}

```python
import json
import asyncio
from dotenv import load_dotenv
from gllm_core.event import EventEmitter
from gllm_core.event.handler import StreamEventHandler

load_dotenv()
```

{% endcode %}
{% endstep %}

{% step %}
**Create the Event System**

Set up the streaming components that will handle real-time events:

{% code lineNumbers="true" %}

```python
# Setup event system for streaming
streamer = StreamEventHandler()
event_emitter = EventEmitter([streamer])
```

{% endcode %}

{% hint style="info" %}
The `StreamEventHandler` captures streaming events, while `EventEmitter` manages event distribution to handlers.
{% endhint %}
{% endstep %}
{% endstepper %}

### 2) Configure LMRP Components

The **LMRP components** work together to process prompts and generate streaming responses:

{% stepper %}
{% step %}
**Set up LM Invoker and Prompt Builder**

{% code lineNumbers="true" %}

```python
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.prompt_builder import PromptBuilder

# Initialize LM invoker
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini")

# Create prompt builder
prompt_builder = PromptBuilder(
    system_template="You are a helpful assistant who specializes in recommending activities.",
    user_template="{question}"
)
```

{% endcode %}

The LM invoker handles model communication while the prompt builder formats your templates consistently.
{% endstep %}

{% step %}
**Create the LM Request Processor**

{% code lineNumbers="true" %}

```python
from gllm_inference.request_processor import LMRequestProcessor

lm_request_processor = LMRequestProcessor(
    prompt_builder=prompt_builder,
    lm_invoker=lm_invoker,
)
```

{% endcode %}

This combines your prompt formatting and model invocation into a complete processing pipeline.
{% endstep %}
{% endstepper %}

### 3) Implement Concurrent Streaming

The **concurrent execution** allows you to process the request and stream tokens simultaneously:

{% stepper %}
{% step %}
**Create the Processing Task**

Use `asyncio.create_task()` to run the processor concurrently with streaming:

{% code lineNumbers="true" %}

```python
# Run the processor and stream concurrently
processor_task = asyncio.create_task(
    lm_request_processor.process(
        prompt_kwargs={"question": "I want to go to Tokyo, Japan. What should I do?"},
        event_emitter=event_emitter
    )
)
```

{% endcode %}

{% hint style="info" %}
The `event_emitter` parameter enables streaming - without it, you'd only get the final response.
{% endhint %}
{% endstep %}

{% step %}
**Process Streaming Events**

Iterate through streaming events as they arrive:

{% code lineNumbers="true" %}

```python
async for event in streamer.stream():
    token = json.loads(event)
    print(token)
```

{% endcode %}

Each event contains token information with metadata like timestamp and content type.
{% endstep %}

{% step %}
**Clean Up Resources**

Ensure proper cleanup after streaming completes:

{% code lineNumbers="true" %}

```python
await processor_task
await event_emitter.close()
```

{% endcode %}

This waits for the processor to finish and properly closes the event system.
{% endstep %}
{% endstepper %}

## 📂 Complete Guide Files

Here's the full implementation that brings everything together:

{% code lineNumbers="true" %}

```python
import json
import asyncio
from dotenv import load_dotenv
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_inference.request_processor import LMRequestProcessor
from gllm_core.event import EventEmitter
from gllm_core.event.handler import StreamEventHandler
from gllm_inference.prompt_builder import PromptBuilder

load_dotenv()

async def main():
    # Setup event system for streaming
    streamer = StreamEventHandler()
    event_emitter = EventEmitter([streamer])

    # Initialize LM invoker and processor
    lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini")
    prompt_builder = PromptBuilder(
        system_template="You are a helpful assistant who specializes in recommending activities.",
        user_template="{question}"
    )
    lm_request_processor = LMRequestProcessor(
        prompt_builder=prompt_builder,
        lm_invoker=lm_invoker,
    )

    # Run the processor and stream concurrently
    # If you want real-time tokens → run processor + streamer concurrently.
    # If you only care about the final response → just await process() and parse the result
    processor_task = asyncio.create_task(
        lm_request_processor.process(
            question="I want to go to Tokyo, Japan. What should I do?",
            event_emitter=event_emitter
        )
    )

    async for event in streamer.stream():
        token = json.loads(event)
        print(token)

    await processor_task
    await event_emitter.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{% endcode %}

## Run the Streaming Example

{% stepper %}
{% step %}
**Execute the Script**

Run your streaming LMRP script:

```bash
python stream_lmrp.py
```

{% endstep %}

{% step %}
**Observe Real-time Output**

When running the streaming example, you'll see real-time token output:

```
{'value': 'Here', 'level': 'INFO', 'type': 'response', 'timestamp': '2025-01-19T10:15:30.123456'}
{'value': ' are', 'level': 'INFO', 'type': 'response', 'timestamp': '2025-01-19T10:15:30.134567'}
{'value': ' some', 'level': 'INFO', 'type': 'response', 'timestamp': '2025-01-19T10:15:30.145678'}
{'value': ' great', 'level': 'INFO', 'type': 'response', 'timestamp': '2025-01-19T10:15:30.156789'}
{'value': ' activities', 'level': 'INFO', 'type': 'response', 'timestamp': '2025-01-19T10:15:30.167890'}
...
```

Each token includes:

- **value**: The token or text fragment
- **level**: Log level ('INFO' for response tokens)
- **type**: Event type ('response' for generated content)
- **timestamp**: Precise generation timestamp
  {% endstep %}
  {% endstepper %}

## Tips

### Alternative Implementation Patterns

#### Pattern 1: Real-time Display

{% code lineNumbers="true" %}

```python
async for event in streamer.stream():
    token_data = json.loads(event)
    if token_data['type'] == 'response':
        print(token_data['value'], end='', flush=True)
```

{% endcode %}

#### Pattern 2: Collecting Full Response

{% code lineNumbers="true" %}

```python
full_response = ""
async for event in streamer.stream():
    token_data = json.loads(event)
    if token_data['type'] == 'response':
        full_response += token_data['value']
```

{% endcode %}

#### Pattern 3: Conditional Processing

{% code lineNumbers="true" %}

```python
async for event in streamer.stream():
    token_data = json.loads(event)
    # Only process content tokens, skip metadata
    if token_data['type'] == 'response' and token_data['value'].strip():
        process_token(token_data['value'])
```

{% endcode %}

### When to Use Streaming vs Standard Processing

**Use Streaming When:**

- User experience is priority (immediate feedback)
- Generating long responses (articles, explanations)
- Building interactive applications
- Need to process partial responses

**Use Standard Processing When:**

- Simple, quick responses
- Batch processing scenarios
- When final response structure is needed before proceeding
- Processing structured outputs that require complete validation

---
