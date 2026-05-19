---
icon: chart-scatter-3d
---

# Trace Your Pipeline with OpenTelemetry

This guide shows you how to instrument a `gllm-pipeline` pipeline with [OpenTelemetry](https://opentelemetry.io/) distributed tracing and visualize the resulting spans in a backend such as [Jaeger](https://www.jaegertracing.io/).

`gllm-pipeline` emits OTel spans automatically for every pipeline invocation and every step execution — you only need to configure a `TracerProvider` before your pipeline code runs.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../prerequisites.md "mention") page.
2. [Docker](https://docs.docker.com/get-started/get-docker/) installed and running (to start the Jaeger backend). To install Docker, follow the instructions [here](https://docs.docker.com/engine/install/).

You should be familiar with these concepts and components:

1. [orchestration](../tutorials/orchestration/ "mention")

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-pipeline
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-pipeline
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bat
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline
pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
`gllm-pipeline` already depends on `opentelemetry-api` (the no-op interfaces). The additional packages above provide the SDK and the OTLP exporter needed to actually export spans to a backend.
{% endhint %}

***

## 1) Start a Trace Backend

You need a backend that can receive OTLP spans. This guide uses **Jaeger**, which accepts OTLP over gRPC on port `4317` and provides a web UI on port `16686`.

{% stepper %}
{% step %}
**Start Jaeger with Docker**

```bash
docker run --rm --name jaeger \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 5778:5778 \
  -p 9411:9411 \
  cr.jaegertracing.io/jaegertracing/jaeger:2.17.0
```
{% endstep %}

{% step %}
**Verify Jaeger is running**

Open [http://localhost:16686](http://localhost:16686) in your browser. You should see the Jaeger UI. No traces will appear yet — they will show up after you run the pipeline.
{% endstep %}
{% endstepper %}

{% hint style="info" %}
Any OTLP-compatible backend works here. Replace the exporter endpoint in the next step with your backend's OTLP gRPC address.
{% endhint %}

***

## 2) Configure the TracerProvider

`gllm-pipeline` uses whatever `TracerProvider` is globally registered via `opentelemetry.trace`. You must configure it **before** importing any `gllm_pipeline` module, so the tracer is resolved at import time.

{% stepper %}
{% step %}
**Create `main.py` and configure the provider first**

```python
# -----------------------------------------------------------------------
# Configure the OTel TracerProvider BEFORE any gllm_pipeline import so
# that get_tracer() picks it up on first call.
# -----------------------------------------------------------------------
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider(resource=Resource({SERVICE_NAME: "my-pipeline-service"}))
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    )
)
trace.set_tracer_provider(provider)
```

**Key components:**

* **`TracerProvider`**: The root object that creates and manages tracers.
* **`Resource`**: Metadata attached to all spans — here it sets the service name visible in Jaeger's service list.
* **`BatchSpanProcessor`**: Buffers and exports spans asynchronously in batches for better throughput.
* **`OTLPSpanExporter`**: Sends spans over gRPC to the configured endpoint.
{% endstep %}

{% step %}
**Import `gllm_pipeline` after the provider is set**

Only after the provider is registered should you import your pipeline components:

```python
# gllm_pipeline imports come AFTER trace.set_tracer_provider()
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import if_else, transform
```

{% hint style="warning" %}
Importing `gllm_pipeline` before calling `trace.set_tracer_provider()` will result in the internal tracer being bound to the default no-op provider. Spans will be created but never exported.
{% endhint %}
{% endstep %}
{% endstepper %}

***

## 3) Build Your Pipeline

Define your state and pipeline steps as usual. No tracing-specific code is needed here — the instrumentation is built into `gllm-pipeline` itself.

{% stepper %}
{% step %}
**Define the state type**

```python
from gllm_pipeline.utils.typing_compat import TypedDict


class State(TypedDict):
    text: str
    score: int
    label: str
    result: str
```
{% endstep %}

{% step %}
**Define step functions**

```python
def uppercase(data: dict) -> str:
    return data["text"].upper()


def add_score(data: dict) -> int:
    return len(data["text"])


def tag_long(data: dict) -> str:
    return f"[LONG] {data['text']}"


def tag_short(data: dict) -> str:
    return f"[short] {data['text']}"


def finalize(data: dict) -> str:
    return f"{data['label']} | score={data['score']}"
```
{% endstep %}

{% step %}
**Assemble the pipeline**

```python
pipeline = Pipeline(
    [
        transform(uppercase, input_map=["text"], output_state="text", name="uppercase"),
        transform(add_score, input_map=["text"], output_state="score", name="score"),
        if_else(
            condition=lambda state: state["score"] > 10,
            if_branch=transform(tag_long, input_map=["text"], output_state="label", name="tag_long"),
            else_branch=transform(tag_short, input_map=["text"], output_state="label", name="tag_short"),
            name="length_check",
        ),
        transform(finalize, input_map=["label", "score"], output_state="result", name="finalize"),
    ],
    state_type=State,
)
```

This pipeline demonstrates three span-emitting step types: `transform` steps (`uppercase`, `score`, `finalize`), and an `if_else` conditional step (`length_check`) which additionally emits a condition-evaluation sub-span.
{% endstep %}
{% endstepper %}

***

## 4) Run the Pipeline and View Traces

{% stepper %}
{% step %}
**Invoke the pipeline and flush spans on exit**

```python
import asyncio


async def main() -> None:
    inputs = [
        {"text": "hi",           "score": 0, "label": "", "result": ""},
        {"text": "hello, world!", "score": 0, "label": "", "result": ""},
    ]
    for initial_state in inputs:
        result = await pipeline.invoke(initial_state, thread_id="demo")
        print(result["result"])

    # Flush pending spans before the process exits.
    provider.force_flush()


if __name__ == "__main__":
    asyncio.run(main())
```

{% hint style="info" %}
Always call `provider.force_flush()` at the end of a short-lived script. The `BatchSpanProcessor` buffers spans and flushes them periodically — without an explicit flush, spans buffered at exit time may be lost.
{% endhint %}
{% endstep %}

{% step %}
**Run the script**

```bash
python main.py
```

You should see output like:

```
[short] HI | score=2
[LONG] HELLO, WORLD! | score=13
```
{% endstep %}

{% step %}
**Open the Jaeger UI**

Go to [http://localhost:16686](http://localhost:16686), select **`my-pipeline-service`** from the Service dropdown, and click **Find Traces**. You will see one trace per `pipeline.invoke()` call.

Click any trace to expand it. You will see a span tree like this:

<figure><img src="../../.gitbook/assets/image (4).png" alt=""><figcaption></figcaption></figure>

```
pipeline.invoke.<pipeline-name>               [root span]
  pipeline.step.uppercase                     [child]
  pipeline.step.score                         [child]
  pipeline.step.length_check                  [child]
    pipeline.step.condition_evaluation        [sub-child — if_else only]
  pipeline.step.finalize                      [child]
```
{% endstep %}
{% endstepper %}

***

## Understanding the Span Structure

`gllm-pipeline` emits the following spans on every `pipeline.invoke()` call:

| Span name                            | Type                         | Attributes                                                                                                            |
| ------------------------------------ | ---------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `pipeline.invoke.<name>`             | Root span                    | `gllm.pipeline.name`, `gllm.pipeline.step_count`, `gllm.thread_id`, `gllm.input_state_keys`, `gllm.output_state_keys` |
| `pipeline.step.<name>`               | Child of pipeline span       | `gllm.step.name`, `gllm.step.type`, `gllm.step.has_cache`, `gllm.step.has_retry_policy`, `gllm.thread_id`             |
| `pipeline.step.condition_evaluation` | Child of `if_else` step span | `gllm.condition.result`, `gllm.condition.branches`                                                                    |

All spans have `StatusCode.OK` on success and `StatusCode.ERROR` with a `gllm.step.error` event on failure.

{% hint style="info" %}
State values are never recorded in span attributes — only the key names are, in the form `"text,score,label"`. This avoids serializing large or sensitive state data into your trace backend.
{% endhint %}

***

## Troubleshooting

**No traces appear in Jaeger**

* Verify Jaeger is running:
  * In Linux, macOS, or Windows WSL: `docker ps | grep jaeger`
  * In Windows: `docker ps | Select-String jaeger` (PowerShell) or `docker ps | findstr jaeger` (Command Prompt)
* Check the exporter endpoint matches your Jaeger gRPC port (`4317` by default)
* Confirm `trace.set_tracer_provider(provider)` is called **before** any `gllm_pipeline` import
* Ensure `provider.force_flush()` is called before the process exits

**Spans appear but are missing child steps**

* Each step must have a `name` parameter set — unnamed steps fall back to a generated ID
* Verify all steps are added to the `Pipeline` steps list

**`ImportError` for `OTLPSpanExporter`**

* Install the exporter: `pip install opentelemetry-exporter-otlp-proto-grpc`
* For HTTP export instead of gRPC: `pip install opentelemetry-exporter-otlp-proto-http` and use `OTLPSpanExporter` from `opentelemetry.exporter.otlp.proto.http.trace_exporter`

**Using a different backend (Grafana Tempo, etc.)**

Replace the exporter with your backend's OTLP endpoint. The span structure emitted by `gllm-pipeline` is the same regardless of backend:

```python
OTLPSpanExporter(endpoint="http://<your-backend-host>:<otlp-grpc-port>", insecure=True)
```

***

## Next Steps

* Add [guides](../../gl-observability/guides/ "mention") to your application for a full-stack observability setup with logs and traces together.
* Explore the [debugging-guide](../../gl-observability/guides/debugging-guide/ "mention") to learn how to analyze traces, logs, and metrics in your observability dashboards.
* For production use, configure a [sampler.md](../../gl-observability/guides/traces/sampler.md "mention") to control trace volume.
