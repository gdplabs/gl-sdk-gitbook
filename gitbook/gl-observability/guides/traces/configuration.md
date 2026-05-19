# Configuration

This page contains more detailed information about supported Backend and Initialization with their example and API documentation.

## Backend

A backend is the destination where your traces data is sent for storage, visualization, and analysis.

### OTLP Backend

OTLP (OpenTelemetry Protocol) is the industry-standard protocol for OpenTelemetry, widely supported by observability tools such as Jaeger, Tempo, and many others. This is the recommended approach for its flexibility and vendor neutrality. Below is the example code for the backend configuration. For detailed parameters, see the [OpenTelemetryBackendConfig API Reference](configuration.md#class-opentelemetrybackendconfig).

```python
from gl_observability import OpenTelemetryBackendConfig

backend_config = OpenTelemetryBackendConfig(
    endpoint="<OTLP_ENDPOINT>",
    use_grpc=False,
    headers={"Authorization": "Bearer ..."},
)
```

### Sentry Backend

Sentry is an error monitoring and performance tracking service that helps identify and fix issues in applications. For this integration we can use sentry cloud service or using our GDP Labs sentry service in [here](https://sentry.obrol.id/) (you need to contract our DSO team for access it). Below is the example code for the backend configuration. For detailed parameters, see the [SentryBackendConfig API Reference](configuration.md#class-sentrybackendconfig).

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

## Initialization

GL Observability has a single unified function to initialize telemetry through the `init_telemetry` function. Below is the example code for initializing a telemetry. For detailed parameters, see the [TelemetryConfig API Reference](configuration.md#class-telemetryconfig) and [init\_telemetry API Reference](configuration.md#func-init_telemetry).

```python
from gl_observability import init_telemetry, TelemetryConfig

otel_config = TelemetryConfig(
    attributes={"service.name": "..."},
    backend_config=backend_config, ## SentryBackendConfig or OpenTelemetryBackendConfig instance
    ...
)
init_telemetry(otel_config)
```

## Multiple Backend

GL Observability supports multiple backend configurations, which can be added using the `init_telemetry` function. Below is the example code.

{% hint style="warning" %}
The `attributes` and `trace_sampler` parameters on `TelemetryConfig` can be set only once on the first call of `init_telemetry()`. Subsequent calls will ignore changes to this specific parameters.
{% endhint %}

```python
from gl_observability import init_telemetry, TelemetryConfig, SentryBackendConfig, OpenTelemetryBackendConfig

sentry_config = SentryBackendConfig(...)
init_telemetry(TelemetryConfig(
    attributes={"service.name": "..."},
    backend_config=sentry_config,
    ...
))

otlp_config = OpenTelemetryBackendConfig(...)
init_telemetry(TelemetryConfig(
    backend_config=otlp_config
))
```

## API References

### _<mark style="color:blue;">class</mark>_ OpenTelemetryBackendConfig

**parameters:**

* `endpoint: str` — the hostname (include port) of your OTLP-compatible trace exporter (e.g., Jaeger, Tempo).
* `headers: dict[str, str]` — the header sent to connect to OpenTelemetry exporter. Default is `None`.
* `use_grpc: bool` — if `True`, wil connect using GRPC to exporter, otherwise will use HTTP. Default is `True`.
* `**kwargs` — other parameters supported by `OTLPSpanExporter`.

### _<mark style="color:blue;">class</mark>_ SentryBackendConfig

**Parameters:**

* `dsn: str` — your Sentry project DSN.
* `environment: str | None` — deployment environment (e.g., "production"). Default is `None`.
* `release: str | None` — application version tag. Default is `None`.
* `profiles_sample_rate: float | None` — Sentry performance sample rate. Default is `None`.
* `send_default_pii: bool | None` — whether to send PII (e.g., usernames, emails) to Sentry. Default is `None`.
* `disable_sentry_distributed_tracing: bool` — whether to disable Sentry Context Propagation or not. Default is `False`. Sentry have their own context propagation standard, different from the OpenTelemetry standard. On some instance, this can make the trace sampler broken.
* `**kwargs` — other parameters supported by `sentry_sdk.init()`. Note: for trace sampler use OpenTelemetry sampler, the `traces_sample_rate` will always set to `1.0`.

### _<mark style="color:blue;">**class**</mark>_ TelemetryConfig

`TelemetryConfig` is a wrapper configuration object that holds your telemetry setup. Pass this to `init_telemetry()`.

**Parameters:**

* `attributes: dict[str, str] | None` — a dictionary of resource-level tags (e.g., `"service.name": "gen-ai-gllm-backend"`). Can only be set once on the first call of `init_telemetry()`. Default is `None`.
* `trace_sampler: Sampler | None` — OpenTelemetry sampler to sample traces. Default is `None` where there is no sampler and all traces will be collected. Can only be set once on the first call of `init_telemetry()`. For sampler example, see [sampler.md](sampler.md "mention").
* `fastapi_config: FastAPIConfig | None` — Enables automatic FastAPI instrumentation. Default is `None`.
* `use_langchain: bool` — if True, automatically instruments LangChain-based pipelines. Default is `False`.
* `use_httpx: bool = True` — if enabled, automatically instruments HTTPX library.
* `use_requests: bool = True` — if enabled, automatically instruments python Requests library.

### _<mark style="color:orange;">func</mark>_ init\_telemetry

Initializes the appropriate telemetry layers according to the provided `TelemetryConfig`.

**Parameters:**

* `config: TelemetryConfig` — The telemetry configuration.
