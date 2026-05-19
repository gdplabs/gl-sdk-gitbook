---
icon: flag-checkered
---

# Getting Started

This guide runs a browser automation task with GL Browser Use and shows how to consume the final result.

## Prerequisites

Before you begin, complete the [Prerequisites](prerequisites.md) guide. At minimum, you need:

* Python 3.11 or 3.12
* `gl-browser-use` installed
* `OPENAI_API_KEY` configured, or API keys passed directly in code

## Run Your First Browser Task

Create a Python file, for example `browser_task.py`:

```python
from gl_browser_use import BrowserUseClient, BrowserUseClientConfig

client = BrowserUseClient(
    config=BrowserUseClientConfig(
        # Optional when OPENAI_API_KEY is already set.
        llm_openai_api_key="your-openai-api-key",
        page_extraction_llm_openai_api_key="your-openai-api-key",
    )
)

result = client.run_sync("Open Hacker News and list five article titles")

print(result.status)
print(result.final_output)
```

Run the script:

```bash
python browser_task.py
```

`run_sync()` returns a `BrowserUseRunResult` with the final output, status, step count, and any terminal error details.

{% hint style="warning" %}
Do not call `run_sync()` from inside an existing async event loop. Use `await client.run_once(...)` or `async for event in client.run(...)` in async applications.
{% endhint %}

## Stream Progress Events

Use `run()` when your application needs to display progress while the browser task is running:

```python
import asyncio

from gl_browser_use import BrowserUseClient, BrowserUseClientConfig


async def main() -> None:
    client = BrowserUseClient(config=BrowserUseClientConfig())

    async for event in client.run("Open Hacker News and list five article titles"):
        print(event.content)


asyncio.run(main())
```

The stream yields `BrowserUseStreamEvent` objects for progress updates, tool-call summaries, streaming URLs, recording URLs, retries, and final status.

## Use Hosted Browser Sessions

Install the Steel extra and provide a Steel API key when you want GL Browser Use to create a hosted browser session:

```bash
pip install "gl-browser-use[steel]"
export STEEL_API_KEY="your-steel-api-key"
```

```python
from gl_browser_use import BrowserUseClient, BrowserUseClientConfig
from gl_browser_use.infrastructure import SteelBrowserInfrastructure

client = BrowserUseClient(
    config=BrowserUseClientConfig(),
    infrastructure=SteelBrowserInfrastructure(),
)

result = client.run_sync("Open Hacker News and list five article titles")

print(result.session_id)
print(result.streaming_url)
```

With Steel configured, the result can include a `session_id` and `streaming_url`. Streaming mode also emits a `Receive streaming URL` activity event when a URL is available.

## Next Steps

* [Run Browser Automation Tasks](guides/run-browser-automation.md): Learn the streaming, async, and sync run methods.
* [Record Browser Sessions](guides/record-browser-sessions.md): Configure Steel with MinIO or S3-compatible storage.
* [SDK Reference](resources/reference.md): Review configuration, result, event, retry, and error contracts.
