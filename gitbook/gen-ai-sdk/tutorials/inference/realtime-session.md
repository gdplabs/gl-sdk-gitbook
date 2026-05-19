---
icon: message
---

# \[BETA] Realtime Session

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/realtime_session) | **Tutorial**: [realtime-session.md](realtime-session.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/realtime_session.html) | [Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/tutorials/inference/realtime_session)

{% hint style="warning" %}
**The realtime session modules are currently in beta and may be subject to changes in the future. They are intended only for quick prototyping in local environments. Please avoid using them in production environments.**
{% endhint %}

## What’s a Realtime Session? <a href="#whats-an-em-invoker" id="whats-an-em-invoker"></a>

The **realtime session** is a unified interface designed to help you interact with language models that supports realtime interactions. In this tutorial, you'll learn how to perform realtime session using the `GoogleRealtimeSession` module in **just a few lines of code**.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [Prerequisites](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/prerequisites) page.
2. Setting a [Gemini API key](https://aistudio.google.com/app/apikey) in the `GOOGLE_API_KEY` environment variable.

</details>

## Available Subclasses

The Realtime Session module provides the following built-in implementations:

1. `GoogleRealtimeSession`
2. `LiveKitRealtimeSession`

Detailed information about each implementation is available at the [API reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/realtime_session.html).

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

Let’s jump into a basic example using `GoogleRealtimeSession`.

```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_inference.realtime_session import GoogleRealtimeSession

realtime_session = GoogleRealtimeSession(model_name="gemini-2.5-flash-native-audio-preview-12-2025")
asyncio.run(realtime_session.start())
```

Notice that after the realtime session starts, the following message appears in the console:

**The conversation starts:**

```log
2026-01-22T20:24:08 INFO      Starting 'GoogleRealtimeSession' with model: 'gemini-2.5-flash-native-audio-preview-12-2025'.
2026-01-22T20:24:08 INFO      Starting 'KeyboardInputStreamer'. Type and press Enter to send a message.
2026-01-22T20:24:08 INFO      Starting 'ConsoleOutputStreamer'. Transcriptions will be printed to the console.
2026-01-22T20:24:08 INFO      Type '/quit' to end the conversation.
```

The realtime session modules utilize a set of input and output streamers to define the input sources and output destinations when interacting with the language model. Notice that by default, it uses the following IO streamers:

1. `KeyboardInputStreamer` : Sending text inputs sent via the keyboard to model.
2. `ConsoleOutputStreamer` : Displaying text outputs from the model to the console.

This means that by default, the `GoogleRealtimeSession` modules support **text inputs** and **text outputs**. Try typing through your keyboard to start interacting with the model!

**Interaction Example:**

```log
Hi there! # Typed by user

╭───────────────────────────────────────╮
│     ASSISTANT TRANSCRIPTION START     │
╰───────────────────────────────────────╯
Hello! How can I help you today?
╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: text_complete

Suggest an activity to do! # Typed by user

╭───────────────────────────────────────╮
│     ASSISTANT TRANSCRIPTION START     │
╰───────────────────────────────────────╯
Sure, but I need a little more information to give you a good suggestion! Are you looking for something indoors or outdoors? Something relaxing or more active?
╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: text_complete
```

When you're done, you can type `/quit` to end the conversation.

**Ending the conversation:**

```log
/quit # Typed by user
2026-01-22T20:24:55 INFO      Conversation ended successfully.
```

## IO Streamer Customization

Now, let's try using other kinds of IO streamers! In the example below, we're going to utilize the `LinuxMicInputStreamer` and `LinuxSpeakerOutputStreamer` to converse with the model via **audio inputs** and **audio outputs**!

{% hint style="warning" %}
**Limitation: As the name suggests, LinuxMicInputStreamer and LinuxSpeakerOutputStreamer are only supported in Linux systems. Similar supports for other operating system, such as Windows and Mac, are not yet available.**
{% endhint %}

```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_inference.realtime_session import GoogleRealtimeSession
from gllm_inference.realtime_session.input_streamer import LinuxMicInputStreamer
from gllm_inference.realtime_session.output_streamer import LinuxSpeakerOutputStreamer

input_streamers = [LinuxMicInputStreamer()]
output_streamers = [LinuxSpeakerOutputStreamer()]

realtime_session = GoogleRealtimeSession(model_name="gemini-2.5-flash-native-audio-preview-12-2025")
asyncio.run(realtime_session.start(input_streamers=input_streamers, output_streamers=output_streamers))
```

**The conversation starts:**

```log
2026-01-22T20:34:55 INFO      Starting 'GoogleRealtimeSession' with model: 'gemini-2.5-flash-native-audio-preview-12-2025'.
2026-01-22T20:34:55 INFO      Starting 'LinuxMicInputStreamer'. Speak to your microphone to send a message.
2026-01-22T20:34:55 INFO      Starting 'LinuxSpeakerOutputStreamer'. Audio will be played through your speakers.
```

Try speaking through your microphone and have fun conversing with the language models in realtime!

After you're done, try combining them with our default IO streamers and see what happens!

```python
...
input_streamers = [KeyboardInputStreamer(), LinuxMicInputStreamer()]
output_streamers = [ConsoleOutputStreamer(), LinuxSpeakerOutputStreamer()]
...
```

## Tool Calling

**Tool calling** means letting a language model **call external functions** to help it solve a task. It allows the model to **interact with external functions and APIs** during the conversation, enabling dynamic computation, data retrieval, and complex workflows.

For more information about tools definition, please refer to [this guide](../core/tool.md).

Now, let's try adding tool calling capabilities to our `GoogleRealtimeSession` module!

{% hint style="warning" %}
**Note: Currently, tool calling capability is only available in GoogleRealtimeSession.**
{% endhint %}

```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.schema import tool
from gllm_inference.realtime_session import GoogleRealtimeSession

@tool
async def get_weather(city: str) -> str:
    """Get the weather of a city.

    Args:
        city (str): The city to get the weather of.

    Returns:
        str: The weather of the city.
    """
    await asyncio.sleep(20)  # Simulate a long-running task
    return f"Cloudy, Temperature: 23°C."

realtime_session = GoogleRealtimeSession(
    model_name="gemini-2.5-flash-native-audio-preview-12-2025",
    tools=[get_weather],
)
asyncio.run(realtime_session.start())
```

**The conversation starts:**

```log
2026-01-22T20:24:08 INFO      Starting 'GoogleRealtimeSession' with model: 'gemini-2.5-flash-native-audio-preview-12-2025'.
2026-01-22T20:24:08 INFO      Starting 'KeyboardInputStreamer'. Type and press Enter to send a message.
2026-01-22T20:24:08 INFO      Starting 'ConsoleOutputStreamer'. Transcriptions will be printed to the console.
2026-01-22T20:24:08 INFO      Type '/quit' to end the conversation.
```

Now try asking a question about the weather of your city!

**Interaction Example:**

```log
What is the weather in Surabaya? # Typed by user

╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: tool_call
>>> id: function-call-16979747789685278717
>>> name: get_weather
>>> args: {'city': 'Surabaya'}
>>> data: None

╭───────────────────────────────────────╮
│     ASSISTANT TRANSCRIPTION START     │
╰───────────────────────────────────────╯
Running get_weather for Surabaya.
╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: text_complete

Let me know when you get the info! # Typed by user

╭───────────────────────────────────────╮
│     ASSISTANT TRANSCRIPTION START     │
╰───────────────────────────────────────╯
Sure, I'll let you know as soon as I have the weather for Surabaya.
╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: text_complete

╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: tool_call_complete
>>> result: {'output': 'Cloudy, Temperature: 23°C.'}

╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: interruption

╭───────────────────────────────────────╮
│     ASSISTANT TRANSCRIPTION START     │
╰───────────────────────────────────────╯
The weather in Surabaya is cloudy, with a temperature of 23°C.
╭──────────────────╮
│     ACTIVITY     │
╰──────────────────╯
>>> type: text_complete
```

Once again, you can type `/quit` to end the conversation.

**Ending the conversation:**

```log
/quit # Typed by user
2026-01-22T20:24:55 INFO      Conversation ended successfully.
```

## Integration with External System

Now that we've successfully tested the realtime session modules locally, let's learn how to integrate it as part of a larger system!

To communicate with external systems, the realtime session modules rely on the following IO streamers:

1. `EventInputStreamer`: Enables external system to push a `RealtimeEvent` object as inputs for the realtime session module.
2. `EventOutputStreamer`: Streams the realtime session modules output events through the [event emitter](../core/event-emitter.md), allowing the system to consumes the output as standard events.

Let's try to simulate a simple integration with an external system using the `GoogleRealtimeSession`:

```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
import json

from gllm_core.event import EventEmitter
from gllm_inference.realtime_session import GoogleRealtimeSession
from gllm_inference.realtime_session.input_streamer import EventInputStreamer
from gllm_inference.realtime_session.output_streamer import EventOutputStreamer
from gllm_inference.realtime_session.schema import RealtimeEvent, RealtimeActivityType

event_emitter = EventEmitter.with_stream_handler()
input_streamer = EventInputStreamer()
output_streamer = EventOutputStreamer(event_emitter)

async def start_realtime_session():
    realtime_session = GoogleRealtimeSession("gemini-2.5-flash-native-audio-preview-12-2025")
    await realtime_session.start(input_streamers=[input_streamer], output_streamers=[output_streamer])

async def stream_output():
    async for event in event_emitter.stream():
        data = json.loads(event)

        if data["type"] == "audio":
            data["value"] = "<audio_bytes>"

        print(f"Event: {json.dumps(data)}")

async def send_text(text: str):
    await asyncio.sleep(5)
    input_streamer.push(RealtimeEvent.input_text(text))

async def terminate():
    await asyncio.sleep(5)
    input_streamer.push(RealtimeEvent.activity(RealtimeActivityType.TERMINATION))

async def main():
    asyncio.create_task(start_realtime_session())
    asyncio.create_task(stream_output())
    await send_text("Hi, how are you?")
    await send_text("Tell me about the history of Indonesia!")
    await send_text("Ok stop! That is enough!")
    await terminate()

if __name__ == "__main__":
    asyncio.run(main())

```

**The conversation starts:**

```log
2026-01-22T20:34:55 INFO      Starting 'GoogleRealtimeSession' with model: 'gemini-2.5-flash-native-audio-preview-12-2025'.
2026-01-22T20:34:55 INFO      Starting 'EventInputStreamer'. Awaiting pushed input events.
2026-01-22T20:34:55 INFO      Starting 'EventOutputStreamer'. Output events will be emitted via the event emitter.
```

Please note that in this example, **you don't need to do anything**, as we've already defined the inputs through the script. Simply observe and wait until the realtime session receives the `termination` activity event and ends the session.

**Output example:**

```log
Event: {"id": null, "value": "", "level": "INFO", "type": "assistant_transcription_start", "timestamp": "2026-01-29T09:03:44.848951", "metadata": {}}
Event: {"id": null, "value": "I'm doing", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:44.850240", "metadata": {}}
Event: {"id": null, "value": " well,", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:45.157201", "metadata": {}}
Event: {"id": null, "value": " thank", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:45.269820", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:45.343184", "metadata": {}}
...
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:45.869419", "metadata": {}}
Event: {"id": null, "value": " you?", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:45.870923", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:45.872261", "metadata": {}}
...
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:46.113085", "metadata": {}}
Event: {"id": null, "value": {"type": "text_complete"}, "level": "INFO", "type": "activity", "timestamp": "2026-01-29T09:03:46.117602", "metadata": {}}
Event: {"id": null, "value": "", "level": "INFO", "type": "assistant_transcription_start", "timestamp": "2026-01-29T09:03:50.227016", "metadata": {}}
Event: {"id": null, "value": "Indonesia's history", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:50.228430", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:50.543661", "metadata": {}}
...
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:51.233951", "metadata": {}}
Event: {"id": null, "value": " diverse.", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:51.235287", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:51.252728", "metadata": {}}
...
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:51.420909", "metadata": {}}
Event: {"id": null, "value": " It spans", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:51.422393", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:51.442239", "metadata": {}}
Event: {"id": null, "value": " from", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:51.444160", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:51.445456", "metadata": {}}
...
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:53.239104", "metadata": {}}
Event: {"id": null, "value": {"type": "interruption"}, "level": "INFO", "type": "activity", "timestamp": "2026-01-29T09:03:53.759238", "metadata": {}}
Event: {"id": null, "value": "", "level": "INFO", "type": "assistant_transcription_start", "timestamp": "2026-01-29T09:03:55.398682", "metadata": {}}
Event: {"id": null, "value": "Understood! Is", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:55.400025", "metadata": {}}
Event: {"id": null, "value": " there", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:55.571325", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:55.584873", "metadata": {}}
...
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:56.375998", "metadata": {}}
Event: {"id": null, "value": " instead?", "level": "INFO", "type": "response", "timestamp": "2026-01-29T09:03:56.377352", "metadata": {}}
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:56.388390", "metadata": {}}
...
Event: {"id": null, "value": "<audio_bytes>", "level": "INFO", "type": "audio", "timestamp": "2026-01-29T09:03:56.556510", "metadata": {}}
Event: {"id": null, "value": {"type": "text_complete"}, "level": "INFO", "type": "activity", "timestamp": "2026-01-29T09:03:56.579371", "metadata": {}}
2026-01-29T09:03:58 INFO      Conversation ended successfully.
```

In this example, we simply print the streamed events streamed by the event emitter regardless of their typing, which causes the text and audio output to be mixed in the console. In an actual system, please handle each type of output events accordingly based on your requirements!

## Future Plans

In the future, more IO streamers can be added to allow for more robust realtime experience, this may include but are not limited to:

1. **Input streamers**
   1. `FileInputStreamer`
   2. `ScreenCaptureInputStreamer`
   3. `CameraInputStreamer`
   4. `WindowsMicInputStreamer`
   5. `MacMicInputStreamer`
2. **Output streamers**
   1. `FileOutputStreamer`
   2. `WindowsSpeakerOutputStreamer`
   3. `MacSpeakerOutputStreamer`
