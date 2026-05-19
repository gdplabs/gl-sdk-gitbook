---
icon: megaphone
---

# Event Emitter

## What is EventEmitter?

`EventEmitter` is a small orchestration primitive that sends **typed events** through a configurable chain of **hooks** and **handlers**.

1. It accepts values (text, dicts, or `Event` instances) and wraps them into `Event` objects when needed.
2. It enforces a **minimum severity level** (`event_level`) so only important events flow through.
3. It applies one or more **hooks** that can transform or enrich events.
4. It forwards the final event to a list of **handlers** (console, print, stream, or custom).
5. It optionally supports **streaming consumption** when a `StreamEventHandler` is attached.

In GLLM Core, components like `Component.run()` use `EventEmitter` to emit structured telemetry instead of ad‑hoc `print` or logging calls.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-core
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  "gllm-core"
```
{% endtab %}
{% endtabs %}

## Quickstart

A basic console setup:

```python
import asyncio
from gllm_core.event.event_emitter import EventEmitter
from gllm_core.constants import EventLevel
from gllm_core.schema.event import Event


async def main() -> None:
    emitter = EventEmitter.with_console_handler(event_level=EventLevel.INFO)

    await emitter.emit(Event(value="Hello, world!", level=EventLevel.INFO))
    await emitter.close()


asyncio.run(main())
```

What happens:

1. `with_console_handler` creates an `EventEmitter` with a single `ConsoleEventHandler`.
2. The emitter is configured with a minimum severity of `INFO`.
3. `emit("Hello, world!", event_level=EventLevel.INFO)` constructs an `Event` (if not already one).
4. The event passes the severity check (INFO ≥ INFO) and is forwarded to the handler.
5. `close()` gracefully shuts down all handlers.

## Constructing an EventEmitter

There are two main ways to construct an `EventEmitter`.

1.  **Direct constructor**

    ```python
    from gllm_core.event.event_emitter import EventEmitter
    from gllm_core.event.handler import ConsoleEventHandler
    from gllm_core.constants import EventLevel


    emitter = EventEmitter(
        handlers=[ConsoleEventHandler()],
        event_level=EventLevel.INFO,
        hooks=[],
    )
    ```

    1. `handlers` must be a non-empty list of objects implementing `BaseEventHandler`.
    2. `event_level` defines the minimum `EventLevel` that will be processed.
    3. `hooks` is an optional list of `BaseEventHook` instances applied before handlers.
    4. An empty `handlers` list raises `ValueError`.
2.  **Factory constructors**

    1. `EventEmitter.with_console_handler(event_level=..., hooks=...)`
    2. `EventEmitter.with_print_handler(event_level=..., hooks=...)`
    3. `EventEmitter.with_stream_handler(event_level=..., hooks=...)`

    Each factory:

    1. Creates a single appropriate handler (`ConsoleEventHandler`, `PrintEventHandler`, or `StreamEventHandler`).
    2. Applies the provided `event_level` and `hooks`.
    3. Returns a ready-to-use `EventEmitter` instance.

## Emitting Events

The core method is `emit`:

```python
from gllm_core.schema.event import Event

await emitter.emit(
    Event(
        value="User logged in",
        level=EventLevel.INFO,
        type="status",
        metadata={"user_id": "123"},
        id="login-123",
    ),
    disabled_handlers=["stream"],
)
```

Key behaviors:

1. **Input value forms**
   1. If `value` is already an `Event` instance, it is used directly and the rest of the parameters are ignored (except for the severity check).
   2. Otherwise, `EventEmitter` creates a new `Event(id, value, level, type, metadata, timestamp)`.
2. **Severity filtering**
   1. `event_level` is validated against `EventLevel` using `validate_string_enum`.
   2. If the event’s level is **below** the emitter’s `severity`, the method returns early and nothing is emitted.
3. **Hook application**
   1. Each hook in `self.hooks` is awaited sequentially.
   2. Each hook receives the current `Event` and must return a new or modified `Event`.
   3. The final `Event` instance is what handlers will see.
4. **Handler fan-out**
   1. `disabled_handlers` is an optional list of handler names to skip.
   2. For each handler in `self.handlers`:
      1. If `handler.name` is **not** in `disabled_handlers`, `await handler.emit(event)` is called.
      2. Handlers are responsible for output (printing, logging, streaming, etc.).

## Configuring Severity Thresholds

The `event_level` argument in the constructor or factory methods determines the minimum severity that will be processed.

1. The emitter stores this threshold as `self.severity`.
2. Each call to `emit` compares the event’s level with this threshold.
3. If `event_level < self.severity`, the event is ignored.

Practical usage patterns:

1. Use `EventLevel.DEBUG` during development to see all events.
2. Use `EventLevel.INFO` in staging environments.
3. Use `EventLevel.WARN` or higher in noisy production paths.

## Using Hooks

Hooks are a way to transform events before they reach handlers.

1. Hooks implement the `BaseEventHook` interface and are awaited one by one.
2. Each hook receives an `Event` and returns a (possibly) new `Event`.
3. Examples of what hooks can do:
   1. Serialize complex values into JSON strings.
   2. Redact sensitive fields from `metadata`.
   3. Add correlation IDs or request IDs to `metadata`.

Attach hooks when constructing an emitter:

```python
from gllm_core.event.event_emitter import EventEmitter
from gllm_core.event.handler import ConsoleEventHandler
from gllm_core.event.hook.event_hook import BaseEventHook


class JSONStringifyEventHook(BaseEventHook):
    async def __call__(self, event):  # type: ignore[override]
        # transform event.value or event.metadata here
        return event


emitter = EventEmitter(
    handlers=[ConsoleEventHandler()],
    hooks=[JSONStringifyEventHook()],
)
```

## Choosing Handlers

Handlers are responsible for what **actually happens** when an event is emitted.

1. **ConsoleEventHandler**
   1. Designed to write formatted events to the console.
   2. Useful for local development and rich CLI output.
2. **PrintEventHandler**
   1. Uses simple `print`-style output.
   2. Ideal for environments where you only need plain text logs (e.g., simple scripts, tests).
3. **StreamEventHandler**
   1. Queues events so they can be iterated over via `EventEmitter.stream()`.
   2. Designed for streaming use cases (e.g., yielding events to a client or UI).

You can also implement custom handlers by subclassing `BaseEventHandler` and passing instances via the `handlers` argument.

## Streaming Events

`EventEmitter` supports streaming when configured with a `StreamEventHandler`.

1. `EventEmitter.with_stream_handler()` creates an emitter with exactly one `StreamEventHandler`.
2. `EventEmitter.stream()` locates that handler and returns its async generator.
3. If there is not **exactly one** `StreamEventHandler`, `stream()` raises `ValueError`.

Typical pattern:

```python
import asyncio
from gllm_core.event.event_emitter import EventEmitter


async def producer(emitter: EventEmitter) -> None:
    from gllm_core.schema.event import Event
    await emitter.emit(Event(value="Hello, world!"))


async def main() -> None:
    emitter = EventEmitter.with_stream_handler()

    asyncio.create_task(producer(emitter))

    async for event in emitter.stream():
        print("Received:", event)


asyncio.run(main())
```

What this gives you:

1. A single emitter that both **produces** and **streams** events.
2. A clean async generator interface for consumers.
3. A clear error if your handler configuration is incompatible with streaming.

## Lifecycle and Cleanup

Proper cleanup is important, especially when handlers maintain resources.

1. `close()` should be called when you are done emitting events.
2. It asynchronously iterates over all handlers and calls `await handler.close()`.
3. This allows handlers to release resources (e.g., flush buffers, close streams, stop background tasks).

A typical application lifecycle might look like:

1. Construct an `EventEmitter` at startup (possibly via a factory method).
2. Pass it through pipelines/components that need to emit events.
3. Call `await emitter.close()` at shutdown to clean up resources.

## Best Practices

1. **Use factory constructors in simple cases**
   1. Prefer `with_console_handler`, `with_print_handler`, or `with_stream_handler` whenever they fit your needs.
   2. Fall back to the raw constructor only for advanced multi-handler setups.
2. **Set an appropriate severity threshold**
   1. Start with `EventLevel.INFO` or `EventLevel.WARN` in production.
   2. Switch to `EventLevel.DEBUG` temporarily when diagnosing issues.
3. **Keep hooks side-effect free**
   1. Treat hooks as pure transformations from `Event` → `Event`.
   2. Avoid blocking I/O or heavy computation inside hooks.
4. **Name your handlers meaningfully**
   1. Set handler names so `disabled_handlers` can selectively skip them when needed.
   2. Use this to, for example, suppress streaming while still logging to the console.
5. **Integrate with Components and Pipelines**
   1. Pass a shared `EventEmitter` into components (e.g., via `event_emitter` kwargs) so they can emit start/finish messages.
   2. Use hooks to normalize event structure across heterogeneous components.
