---
icon: signal-stream
---

# OpenTelemetry Integration

Correlate audit events with distributed traces.

{% hint style="info" %}
**When to use**: When you use OpenTelemetry for observability and want audit events as span events with trace correlation.
{% endhint %}

<details>

<summary>Prerequisites</summary>

* Completed [Console Logging](console-logging.md)
* OpenTelemetry SDK installed (`pip install opentelemetry-api opentelemetry-sdk`)

</details>

## 5-Line Core

```python
from gl_iam import OpenTelemetryAuditHandler, ConsoleAuditHandler

otel_handler = OpenTelemetryAuditHandler()
gateway = IAMGateway(
    auth_provider=provider, user_store=provider, session_provider=provider,
    audit_handlers=[ConsoleAuditHandler(), otel_handler],
)
# Events now appear as span events with trace_id and span_id
```

## Step-by-Step

{% stepper %}
{% step %}
#### Install OpenTelemetry

```bash
pip install opentelemetry-api opentelemetry-sdk
# Or with GL IAM extras:
pip install "gl-iam[otel]"
```
{% endstep %}

{% step %}
#### Create the Handler

```python
from gl_iam import OpenTelemetryAuditHandler

# Default span event name
otel_handler = OpenTelemetryAuditHandler()

# Custom span event name
otel_handler = OpenTelemetryAuditHandler(event_name="iam.audit")
```
{% endstep %}

{% step %}
#### Wire into Gateway

```python
from gl_iam import IAMGateway, ConsoleAuditHandler

gateway = IAMGateway(
    auth_provider=provider,
    user_store=provider,
    session_provider=provider,
    audit_handlers=[ConsoleAuditHandler(), otel_handler],
)
```

Use both handlers — console for local logging, OTel for distributed trace correlation.
{% endstep %}

{% step %}
#### Trace Context Auto-Population

When an audit event is emitted within an active span, the handler automatically:

1. Populates `event.trace_id` from the current span context
2. Populates `event.span_id` from the current span context
3. Adds the event as a span event with `audit.*` attributes

```python
from opentelemetry import trace

tracer = trace.get_tracer("my-app")

with tracer.start_as_current_span("handle-login"):
    result = await gateway.authenticate(credentials, organization_id="default")
    # AuditEvent now has:
    #   trace_id = "0af7651916cd43dd8448eb211c80319c"
    #   span_id = "b7ad6b7169203331"
```
{% endstep %}

{% step %}
#### Expected Span Event

In your trace viewer (Jaeger, Zipkin, Grafana Tempo), you'll see:

```
Span: handle-login
  └── Event: audit.event
        audit.action = login_success
        audit.severity = info
        audit.actor.id = usr_abc123
        audit.actor.type = user
        audit.actor.ip = 192.168.1.42
        audit.org_id = default
        audit.result = success
        audit.message = User usr_abc123 logged in successfully via postgresql
```
{% endstep %}
{% endstepper %}

{% hint style="success" %}
Audit events are now correlated with your distributed traces.
{% endhint %}

## OTel Attribute Mapping

| AuditEvent Field | OTel Attribute | Example |
| --- | --- | --- |
| `event_type` | `audit.action` | `login_success` |
| `severity` | `audit.severity` | `info` |
| `timestamp` | `audit.timestamp` | `2026-04-06T10:30:00+00:00` |
| (derived) | `audit.result` | `success` or `error` |
| `user_id` | `audit.actor.id` | `usr_abc123` |
| (inferred) | `audit.actor.type` | `user` |
| `ip_address` | `audit.actor.ip` | `192.168.1.42` |
| `organization_id` | `audit.org_id` | `org_456` |
| `resource_id` | `audit.resource.id` | `agent_789` |
| `provider_type` | `audit.resource.type` | `postgresql` |
| `error_code` | `audit.error_code` | `authentication_failed` |
| `message` | `audit.message` | `Login failed: authentication_failed` |

## Graceful Degradation

If `opentelemetry` is not installed, the handler:

1. Logs a warning on first use: `"OpenTelemetry is not installed. OpenTelemetryAuditHandler will be a no-op."`
2. Becomes a silent no-op for all subsequent events
3. Does **not** raise exceptions or affect other handlers

This means you can safely include `OpenTelemetryAuditHandler` in your handler list even in environments where OTel is not available.

## Complete Example

Create `otel_audit.py`:

```python
"""GL IAM OpenTelemetry Audit Trail Example."""

import asyncio
import logging

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from gl_iam import IAMGateway, ConsoleAuditHandler, OpenTelemetryAuditHandler
from gl_iam.core.types.auth import Credentials
from gl_iam.providers.postgresql import PostgreSQLProvider, PostgreSQLConfig

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/gliam"

logging.basicConfig(level=logging.INFO)

# Setup OTel tracer
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("my-app")


async def main():
    config = PostgreSQLConfig(database_url=DATABASE_URL)
    pg_provider = PostgreSQLProvider(config)

    gateway = IAMGateway(
        auth_provider=pg_provider,
        user_store=pg_provider,
        session_provider=pg_provider,
        audit_handlers=[
            ConsoleAuditHandler(),
            OpenTelemetryAuditHandler(),
        ],
    )

    # Wrap auth in a span — audit event will be correlated
    with tracer.start_as_current_span("user-login"):
        result = await gateway.authenticate(
            credentials=Credentials(username="alice", password="secret123"),
            organization_id="default",
        )

    if result.is_ok:
        print(f"Login succeeded for {result.user.id}")
    else:
        print(f"Login failed: {result.error.message}")

    await pg_provider.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
uv run otel_audit.py
```

## Common Pitfalls

| Pitfall | Solution |
| --- | --- |
| No span events appearing | Ensure there's an active span (OTel middleware must be configured) |
| `opentelemetry` not installed | Handler degrades gracefully; install `opentelemetry-api opentelemetry-sdk` |
| Missing `trace_id` on events | Check that the span context is valid and the span is recording |

---

{% hint style="info" %}
**Found an issue on this page?** [Report it on our feedback form](https://docs.google.com/forms/d/e/1FAIpQLScU8uurCRPhWBOBI4BPw05uGaideH70j0-EMiCGUTbpFa7osw/viewform?usp=pp_url&entry.668725353=https%3A%2F%2Fgdplabs.gitbook.io%2Fsdk%2Fgl-identity-and-access-management%2Fidentity-and-access-management%2Faudit-trail%2Fopentelemetry).
{% endhint %}
