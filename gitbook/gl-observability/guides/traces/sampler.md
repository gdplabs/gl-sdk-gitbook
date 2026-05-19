# Sampler

GL Observability supports custom trace samplers, allowing you to define your own sampling logic on the traces. You can use an existing sampler implementation provided by the OpenTelemetry SDK or make your own implementation. Example of a custom sampler used to trace FastAPI requests based on their endpoint paths:

```python
from typing import Sequence, Optional

from opentelemetry.context import Context
from opentelemetry.sdk.trace.sampling import (
    ParentBased,
    Sampler,
    SamplingResult,
    TraceIdRatioBased,
)
from opentelemetry.trace import Link, SpanKind
from opentelemetry.trace.span import TraceState
from opentelemetry.util.types import Attributes

NO_SAMPLING_ENDPOINTS: set[str] = {"/health", "not_important"}
IMPORTANT_ENDPOINTS: set[str] = {"/important"}

DEFAULT_SAMPLING_RATE: float = 0.1
IMPORTANT_SAMPLING_RATE: float = 1.0
NO_SAMPLING_RATE: float = 0.0

class OtelSampler(Sampler):

    def should_sample(
        self,
        parent_context: Optional[Context],
        trace_id: int,
        name: str,
        kind: SpanKind = None,
        attributes: Attributes = None,
        links: Sequence[Link] = None,
        trace_state: TraceState = None,
    ) -> SamplingResult:
        trace_sample_rate = DEFAULT_SAMPLING_RATE

        routes = attributes.get("http.route") if attributes else None
        if routes in NO_SAMPLING_ENDPOINTS:
            trace_sample_rate = NO_SAMPLING_RATE
        elif routes in IMPORTANT_ENDPOINTS:
            trace_sample_rate = IMPORTANT_SAMPLING_RATE

        sampler = ParentBased(TraceIdRatioBased(trace_sample_rate))
        return sampler.should_sample(
            parent_context, trace_id, name, kind, attributes, links, trace_state
        )

    def get_description(self) -> str:
        return "OtelSampler"
```

To use the custom sampler, provide an instance of it to `TelemetryConfig`. For more details, see the [TelemetryConfig API Reference](configuration.md#class-telemetryconfig).

{% hint style="warning" %}
The `trace_sampler` parameters on `TelemetryConfig` can be set only once on the first call of `init_telemetry()`. Subsequent calls will ignore changes to this specific parameters.
{% endhint %}

```python
from gl_observability import init_telemetry, TelemetryConfig

otel_config = TelemetryConfig(
    trace_sampler=OtelSampler(),
    ...
)
init_telemetry(otel_config)
```
