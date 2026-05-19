---
icon: bars-staggered
---

# Traces

Distributed tracing is the cornerstone of observability in modern applications. It allows you to follow the journey of a request as it travels through various components, services, and databases.

## Why Use Tracing?

* **Root Cause Analysis**: Quickly identify which service in a chain is failing.
* **Latency Bottlenecks**: See exactly how much time is spent in each segment of a request.
* **Service Dependency Mapping**: Visualize how your services interact in real-time.

## Core Concepts

### Traces

A trace represents the full path of a single request, from start to finish, across all connected services in your system, providing a unified view of how they interact to fulfill a user's request. It is constructed from multiple spans.

### Spans

A **Span** is the building block of a trace, representing a single unit of work such as a database query or an API call. Each span contains information such as the start and end timestamps of the operation and attributes—key-value pairs that provide critical context (`user_id`, `http.status_code`, `db.statement`, etc) for debugging and analysis.

### Instrumentation

Instrumentation is the process of adding code to your application that generates telemetry data (traces and spans).

* **Auto-Instrumentation**: Our library can automatically capture telemetry from popular libraries (like FastAPI, LangChain, Requests, or python logging) without requiring manual code changes.
* **Manual Instrumentation**: For custom logic or specific business operations, you can manually create spans to gain deeper insights into your application's behavior.

### Sampling

Sampling is the mechanism used to control the volume of traces sent to your backend. Since recording every single request in a high-traffic system can be expensive and resource-intensive, sampling allows you to collect a representative percentage of traces while maintaining high visibility into system health. This can also be used to filter certain traces from polluting the traces.

### Context Propagation

The magic that links spans together across service boundaries is Context Propagation. When Service A calls Service B, the library automatically "injects" tracing information (like the Trace ID) into the request headers. Service B then "extracts" this info to ensure its own spans are recorded as part of the same trace.

### OpenTelemetry Standard

GL Observability is built entirely on the OpenTelemetry (OTel) framework. This means:

* **Consistency**: Your tracing data follows a globally recognized schema.
* **Portability**: You can export your traces to any OTel-compatible backend without changing your application code.
* **Rich Ecosystem**: Benefit from a wide range of community-maintained instrumentors and tools.

### Next Steps

Start tracing your code by following the [quickstart.md](quickstart.md "mention") .
