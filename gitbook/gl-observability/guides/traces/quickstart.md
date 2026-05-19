# Quickstart

This guide will help you on how to setup Tracing mechanism using GL Observability.

{% stepper %}
{% step %}
**Choose your Backend**

A backend is the destination where your traces data is sent for storage, visualization, and analysis. This guide will use Sentry backend. For more details about backend, see [Backend Configuration](configuration.md#backend).

```python
from gl_observability import SentryBackendConfig

backend_config = SentryBackendConfig(
    dsn="<your-sentry-dsn>",
    environment="<project-environment>",
    release="<release-version>",
    send_default_pii=True,
    disable_sentry_distributed_tracing=False
)
```
{% endstep %}

{% step %}
**(Optional) Initialize Sampler**

Sampler can be used to reduce traces collected. See [sampler.md](sampler.md "mention") for more details.

```python
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

trace_sampler = TraceIdRatioBased(1.0)
```
{% endstep %}

{% step %}
**Initialize Telemetry with Instrumentation**

The example code activate instrumentation for FastAPI, Langchain, HTTPX, and Requests library. For more details, see [Initialization Configuration](configuration.md#initialization).

```python
from gl_observability import init_telemetry, TelemetryConfig, FastAPIConfig

app = FastAPI()
fastapi_config = FastAPIConfig(app=app)

otel_config = TelemetryConfig(
    attributes={"service.name": "..."},
    backend_config=backend_config,
    trace_sampler=trace_sampler,
    fastapi_config=fastapi_config,
    use_langchain=True,
    use_httpx=True,
    use_requests=True,
    log_trace_context=True,
)
init_telemetry(otel_config)
```
{% endstep %}

{% step %}
**Next Step**

You can start adding instrumentation into your code. See more details about [instrumentation.md](instrumentation.md "mention").
{% endstep %}
{% endstepper %}

## Full Code Example

The following example demonstrates the complete setup for enabling tracing in your application using GL Observability.

```python
from gl_observability import (
    init_telemetry, 
    TelemetryConfig, 
    SentryBackendConfig, 
    FastAPIConfig,
)
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

app = FastAPI()
fastapi_config = FastAPIConfig(app=app)

backend_config = SentryBackendConfig(
    dsn="<your-sentry-dsn>",
    environment="<project-environment>",
    release="<release-version>",
    send_default_pii=True,
    disable_sentry_distributed_tracing=False
)
trace_sampler = TraceIdRatioBased(0.5) ## Sample only 50% of trace.

otel_config = TelemetryConfig(
    attributes={"service.name": "..."},
    backend_config=backend_config,
    trace_sampler=trace_sampler, ## Optional. Default no sampler will capture all traces.
    fastapi_config=fastapi_config,
    use_langchain=True,
    use_httpx=True,
    use_requests=True,
    log_trace_context=True, ## Enable this to connect log data with trace data.
)
init_telemetry(otel_config)
```
