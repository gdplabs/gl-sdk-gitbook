---
icon: flag-checkered
---

# Getting Started

This guide runs your first desktop automation task with GL Computer Use and demonstrates the three run modes.

## Prerequisites

Before you begin, complete the [Prerequisites](prerequisites.md) guide. At minimum you need:

* Python 3.12 or 3.13
* `gl-computer-use` installed
* `GLCU_E2B_API_KEY` and `GLCU_ANTHROPIC_API_KEY` set (or equivalent for your model provider)

## Run Your First Desktop Task

Create a Python file, for example `desktop_task.py`:

```python
from gl_computer_use import GLComputerUseClient

result = GLComputerUseClient().run_sync("Open a terminal and check Python version")
print(result.status)   # COMPLETED
print(result.output)   # Agent's final answer
```

Run it:

```bash
python desktop_task.py
```

`run_sync()` returns a `TaskResult` with the final output, status, step count, and optional recording URL. No `asyncio.run()` or `await` required — it works in regular scripts and Jupyter notebooks.

{% hint style="warning" %}
Do not call `run_sync()` from inside an already-running async event loop. Use `await client.run_once(...)` or stream via `run()` in async applications.
{% endhint %}

## Stream Live Events

Use `run()` when you want progress updates as the agent works, or when you need the live desktop URL before the task finishes:

```python
import asyncio
from gl_computer_use import GLComputerUseClient


async def main() -> None:
    client = GLComputerUseClient()
    stream = await client.run("Open Firefox and navigate to google.com")

    async for event in stream:
        if event.event_type == "SANDBOX_READY" and event.stream_url:
            print(f"Watch live at: {event.stream_url}")
        elif event.event_type == "STEP_COMPLETED":
            action = event.action.type if event.action else "—"
            print(f"Step {event.step_index}: {action}")
        elif event.event_type == "TASK_COMPLETED":
            print(f"Status: {event.result.status}")
            print(f"Output: {event.result.output}")
        elif event.event_type == "TASK_FAILED":
            print(f"Failed: {event.error}")


asyncio.run(main())
```

## Watch the Live Desktop

The E2B sandbox starts a noVNC HTTP endpoint alongside the desktop. The SDK waits until that endpoint is reachable before surfacing the URL — you can open it in any browser to watch the agent in real time.

```python
# Option A — access before iteration
stream = await client.run("do something")
print(stream.stream_url)

# Option B — from the first SANDBOX_READY event
async for event in stream:
    if event.event_type == "SANDBOX_READY" and event.stream_url:
        import webbrowser
        webbrowser.open(event.stream_url)
```

## Fire-and-Forget Async

`run_once()` returns a `TaskResult` directly when the task finishes. Use it when you only need the final result in an async context and do not need streaming progress:

```python
import asyncio
from gl_computer_use import GLComputerUseClient, TaskFailedError


async def main() -> None:
    client = GLComputerUseClient()
    try:
        result = await client.run_once("Open a terminal and check Python version")
        print(result.status, result.output)
    except TaskFailedError as e:
        print("Agent failed:", e)


asyncio.run(main())
```

`run_once()` raises `TaskFailedError` or `TaskCancelledError` on non-`COMPLETED` outcomes instead of returning a result with a failed status.

## Next Steps

* [Run Desktop Automation](guides/run-desktop-automation.md) — Detailed run methods, event handling, and error handling.
* [Provider Configuration](guides/provider-configuration.md) — Swap agents and sandboxes via config.
* [Human-in-the-Loop Takeover](guides/human-takeover.md) — Pause the agent and hand control to a human.
* [SDK Reference](resources/reference.md) — Complete configuration, event, and result contracts.
