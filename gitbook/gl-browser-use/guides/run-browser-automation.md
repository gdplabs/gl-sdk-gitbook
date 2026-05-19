---
icon: arrow-progress
---

# Run Browser Automation Tasks

This guide shows how to run browser automation tasks with GL Browser Use using the three public run methods: `run()`, `run_once()`, and `run_sync()`.

<details>
<summary>Prerequisites</summary>

Complete the setup steps in [Prerequisites](../prerequisites.md "mention"). You need `gl-browser-use` installed and an OpenAI API key available through `OPENAI_API_KEY` or `BrowserUseClientConfig`.
</details>

## 1. Create a Client

Start with `BrowserUseClientConfig`. If `OPENAI_API_KEY` is set, both model API key fields default to that value.

```python
from gl_browser_use import BrowserUseClient, BrowserUseClientConfig

client = BrowserUseClient(
    config=BrowserUseClientConfig(
        llm_openai_model="o3",
        page_extraction_llm_openai_model="gpt-5-mini",
        max_session_retries=2,
        session_retry_delay_in_s=3.0,
    )
)
```

You can also pass `llm_openai_api_key` and `page_extraction_llm_openai_api_key` directly when your application does not use environment variables.

## 2. Choose a Run Method

Use the method that fits your application runtime.

{% tabs %}
{% tab title="Streaming" %}
```python
import asyncio

from gl_browser_use import BrowserUseClient, BrowserUseClientConfig


async def main() -> None:
    client = BrowserUseClient(config=BrowserUseClientConfig())

    async for event in client.run("Compare pricing from two product pages"):
        print(event.content)


asyncio.run(main())
```
{% endtab %}

{% tab title="Async Result" %}
```python
import asyncio

from gl_browser_use import BrowserUseClient, BrowserUseClientConfig


async def main() -> None:
    client = BrowserUseClient(config=BrowserUseClientConfig())
    result = await client.run_once("Compare pricing from two product pages")

    print(result.status)
    print(result.final_output)
    print(len(result.events))


asyncio.run(main())
```
{% endtab %}

{% tab title="Sync Result" %}
```python
from gl_browser_use import BrowserUseClient, BrowserUseClientConfig

client = BrowserUseClient(config=BrowserUseClientConfig())
result = client.run_sync("Compare pricing from two product pages")

print(result.status)
print(result.final_output)
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
`run_sync()` uses `asyncio.run()` internally and must not be called from an already running event loop.
{% endhint %}

## 3. Handle Stream Events

Each streaming item is a `BrowserUseStreamEvent`:

```python
async for event in client.run("Find the latest release notes for a project"):
    if event.content == "Receive streaming URL":
        print("Browser stream:", event.thinking_and_activity_info)
    elif event.is_final:
        print("Finished:", event.content)
    else:
        print("Progress:", event.content)
```

Important event contents include:

1. `Receive streaming URL`: emitted when the hosted browser streaming URL is available.
2. `Receive recording URL`: emitted when a recording URL can be resolved.
3. `Task completed`: emitted for the final successful step.

Activity events encode iframe URLs in `thinking_and_activity_info["data_value"]` as a JSON string:

```json
{"type": "iframe", "message": "<url>"}
```

## 4. Inspect the Result

`BrowserUseRunResult` gives your application a stable result object:

```python
result = await client.run_once("Summarize the homepage of gdplabs.id")

if result.is_success:
    print(result.final_output)
else:
    print(result.error)

print(result.steps)
print(result.session_id)
print(result.streaming_url)
print(result.recording_url)
print(result.metadata)
```

The `events` field is populated by `run_once()`. Streaming consumers receive events as they happen through `run()`.

## 5. Configure Retries

The client retries only classified recoverable browser-session failures, such as browser closure or websocket disconnect messages.

```python
client = BrowserUseClient(
    config=BrowserUseClientConfig(
        max_session_retries=3,
        session_retry_delay_in_s=2.0,
    )
)
```

Total attempts are `max_session_retries + 1`. Non-recoverable task failures return `BrowserUseRunResult(status="error")`. Recoverable session failures that exhaust all attempts raise `BrowserUseRetryExhaustedError`.
