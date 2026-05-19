---
icon: puzzle-piece
---

# Custom Handler

Build your own audit handler and combine multiple handlers.

{% hint style="info" %}
**When to use**: When built-in handlers don't fit your needs — send events to Slack, a message queue, external SIEM, or any custom destination.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Console Logging](console-logging.md)

</details>

## 5-Line Core

```python
from gl_iam import AuditHandler

class SlackAuditHandler(AuditHandler):
    def handle(self, event):
        if event.severity in ("error", "critical"):
            send_to_slack(f"[{event.severity}] {event.event_type}: {event.message}")
```

## AuditHandler Protocol

| Method | Required | Default | Description |
| --- | --- | --- | --- |
| `handle(event)` | Yes | — | Process a single audit event (must be fast and non-blocking) |
| `handle_batch(events)` | No | Calls `handle()` per event | Override for efficient bulk processing |
| `close()` | No | No-op | Clean up resources on shutdown |

## Step-by-Step

{% stepper %}
{% step %}
#### Implement AuditHandler

Only `handle()` is required:

```python
from gl_iam import AuditHandler
from gl_iam.core.types.audit import AuditEvent


class SlackAuditHandler(AuditHandler):
    """Send high-severity audit events to Slack."""

    def __init__(self, webhook_url: str):
        self._webhook_url = webhook_url

    def handle(self, event: AuditEvent) -> None:
        # Only alert on errors and critical events
        if event.severity not in ("error", "critical"):
            return
        self._post_to_slack(
            f"*{event.severity.upper()}*: {event.event_type}\n"
            f"User: {event.user_id or 'unknown'}\n"
            f"Message: {event.message or 'N/A'}"
        )

    def _post_to_slack(self, text: str) -> None:
        import requests
        requests.post(self._webhook_url, json={"text": text}, timeout=5)
```
{% endstep %}

{% step %}
#### Build a Queue Handler

For high-throughput systems, buffer events to a message queue:

```python
import json

class RedisAuditHandler(AuditHandler):
    """Push audit events to a Redis stream."""

    def __init__(self, redis_client, stream_name: str = "audit:events"):
        self._redis = redis_client
        self._stream = stream_name

    def handle(self, event: AuditEvent) -> None:
        self._redis.xadd(self._stream, {
            "event_type": event.event_type,
            "severity": event.severity,
            "user_id": event.user_id or "",
            "data": event.model_dump_json(),
        })

    def handle_batch(self, events: list[AuditEvent]) -> None:
        # More efficient: pipeline multiple writes
        pipe = self._redis.pipeline()
        for event in events:
            pipe.xadd(self._stream, {
                "event_type": event.event_type,
                "data": event.model_dump_json(),
            })
        pipe.execute()
```
{% endstep %}

{% step %}
#### Combine with CompositeAuditHandler

Route events to multiple handlers simultaneously:

```python
from gl_iam import CompositeAuditHandler, ConsoleAuditHandler

composite = CompositeAuditHandler([
    ConsoleAuditHandler(),                     # Always log to console
    SlackAuditHandler(webhook_url="https://hooks.slack.com/..."),  # Alert on errors
    db_handler,                                 # Persist to PostgreSQL
])

gateway = IAMGateway(
    auth_provider=provider,
    user_store=provider,
    session_provider=provider,
    audit_handlers=[composite],
)
```

You can also add handlers dynamically:

```python
composite.add_handler(RedisAuditHandler(redis_client))
```
{% endstep %}

{% step %}
#### Error Isolation

`CompositeAuditHandler` catches exceptions per handler — one failure doesn't block the others:

```python
# If SlackAuditHandler raises an exception:
# - The error is logged
# - ConsoleAuditHandler and db_handler still receive the event
# - Your application continues normally
```
{% endstep %}

{% step %}
#### Implement close() for Cleanup

If your handler buffers events or holds connections, implement `close()`:

```python
class BufferedSIEMHandler(AuditHandler):
    def __init__(self, siem_url: str, buffer_size: int = 100):
        self._siem_url = siem_url
        self._buffer: list[AuditEvent] = []
        self._buffer_size = buffer_size

    def handle(self, event: AuditEvent) -> None:
        self._buffer.append(event)
        if len(self._buffer) >= self._buffer_size:
            self._flush()

    def close(self) -> None:
        # Flush remaining events on shutdown
        if self._buffer:
            self._flush()

    def _flush(self) -> None:
        # Send batch to SIEM
        import requests
        requests.post(
            self._siem_url,
            json=[e.model_dump() for e in self._buffer],
            timeout=10,
        )
        self._buffer.clear()
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
You can now route audit events to any destination.
{% endhint %}

## Legacy: CallbackAuditHandler

For simple use cases, pass a callback function directly:

```python
# Via audit_callback parameter (legacy, still supported)
gateway = IAMGateway(
    auth_provider=provider,
    user_store=provider,
    session_provider=provider,
    audit_callback=lambda event: print(f"AUDIT: {event.event_type}"),
)
```

This is wrapped internally as a `CallbackAuditHandler`. For new code, prefer implementing `AuditHandler` directly.

## Complete Example

Create `custom_audit.py`:

```python
"""GL IAM Custom Audit Handler Example."""

import asyncio
import logging

from gl_iam import IAMGateway, AuditHandler, CompositeAuditHandler, ConsoleAuditHandler
from gl_iam.core.types.audit import AuditEvent
from gl_iam.core.types.auth import Credentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"

logging.basicConfig(level=logging.INFO)


class AlertHandler(AuditHandler):
    """Print alerts for high-severity events."""

    def handle(self, event: AuditEvent) -> None:
        if event.severity in ("error", "critical"):
            print(f"ALERT [{event.severity.upper()}]: {event.event_type} - {event.message}")


async def main():
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    provider = PostgreSQLProvider(config)

    # Combine multiple handlers
    composite = CompositeAuditHandler([
        ConsoleAuditHandler(),
        AlertHandler(),
    ])

    gateway = IAMGateway(
        auth_provider=provider,
        user_store=provider,
        session_provider=provider,
        audit_handlers=[composite],
    )

    # This will trigger audit events to both handlers
    result = await gateway.authenticate(
        credentials=Credentials(username="alice", password="wrong_password"),
        organization_id="default",
    )

    if not result.is_ok:
        print(f"Login failed (expected): {result.error.message}")

    await provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run custom_audit.py
```

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| Blocking I/O in `handle()` | Keep `handle()` fast; use internal buffering for network calls |
| Not implementing `close()` | Buffered events may be lost on shutdown |
| Handler exception stops other handlers | Use `CompositeAuditHandler` — it isolates failures per handler |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Faudit-trail%2Fcustom-handler).
{% endhint %}
