---
icon: lightbulb-on
---

# Introduction to GL Observability

Observability is the ability to understand the internal state of a complex system by examining its outputs, primarily through traces, logs, and metrics. While monitoring tells you _that_ something is wrong, observability empowers you to understand _why_.

## Why is it Matters?

In modern distributed systems, complexity often hides the root cause of issues. Observability provides the visibility needed to:

* **Accelerate Debugging**: Pinpoint failures across service boundaries instantly.
* **Optimize Performance**: Identify latency bottlenecks in complex request flows.
* **Build Confidence**: Understand system behavior in real-time, even during peak loads.

## GL Observability Library

Our observability library provides a streamlined way to add observability to a Python code with minimal configuration and easy to use. This library uses [OpenTelemetry](https://opentelemetry.io/) to ensures the telemetry data is standardized and vendor-neutral. Currently, the library supports traces and logs, with more observability components planned for future releases.

### Benefit of using this library:

* **Simplified Setup**: Initialize distributed tracing and logging with just a few lines of code.
* **Backend Flexibility**: Export telemetry data to OTLP-compatible backends (like Jaeger or Tempo) or Sentry.
* **Security First**: Built-in handlers for PII redaction to ensure compliance with GDPR, SOC2, and UU PDP.

## Next Steps

Check out the [getting-started.md](getting-started.md "mention") page if you want to learn how to use GL Observability library or [debugging-guide](guides/debugging-guide/ "mention") guide if you want to learn how to use observability tools for debugging.

{% columns %}
{% column %}
{% content-ref url="getting-started.md" %}
[getting-started.md](getting-started.md)
{% endcontent-ref %}
{% endcolumn %}

{% column %}
{% content-ref url="guides/debugging-guide/" %}
[debugging-guide](guides/debugging-guide/)
{% endcontent-ref %}
{% endcolumn %}
{% endcolumns %}
