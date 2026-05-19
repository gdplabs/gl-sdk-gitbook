# Instrumentation

Instrumentation is the process of making your code collects telemetry data. This section will explain about what types, where to add, and how to add instrumentation into python code.

## **Instrumentation Level**

There are two level types of instrumentation.

1. **Application-level Instrumentation** — Added inside your application code (e.g., a service, endpoint handler, or business logic function)
2. **Library-level Instrumentation** — OpenTelemetry recommends library developers to add native instrumentation directly into their library components. This ensures deeper, more accurate telemetry data reflecting the library's internal behavior — rather than relying on external wrappers. To add library-level instrumentation, follow [#manual-instrumentation](instrumentation.md#manual-instrumentation "mention") guide. It is possible to use the [#functionsinstrumentor](instrumentation.md#functionsinstrumentor "mention"), though it is not recommended at the library level.

## **How to Add Instrumentation**

### **Auto-Instrumentation**

GL Observability library provides seamless, low code instrumentation for [FastAPI](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html), [Requests](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/requests/requests.html), [HTTPX](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/httpx/httpx.html), [Langchain](https://github.com/traceloop/openllmetry/tree/main/packages/opentelemetry-instrumentation-langchain) and [python logging](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/logging/logging.html) libraries. These are configured directly through the `TelemetryConfig` object.

```python
from gl_observability import init_telemetry, TelemetryConfig, FastAPIConfig

app = FastAPI()
fastapi_config = FastAPIConfig(app=app)

otel_config = TelemetryConfig(
    ...
    fastapi_config=fastapi_config,
    use_langchain=True,
    use_httpx=True,
    use_requests=True,
    log_trace_context=True,
)
init_telemetry(otel_config)
```

#### Logging

To enable logging instrumentation, set the parameter `log_trace_context=True` in `TelemetryConfig`. This does not create a new span but injects trace context into the log statement, linking trace and log data. The following keys are added to log records:

* `otelSpanID: string` - The span ID, default to `"0"` .
* `otelTraceID: string` - The trace ID, default to `"0"` .
* `otelServiceName: string` - The trace resource `service.name`.
* `otelTraceSampled: bool` - `True` if the trace is sampled by trace sampler, otherwise `False`.

{% hint style="info" %}
The [LoggerManager](../../../gen-ai-sdk/tutorials/core/logger-manager.md) JSON format will automatically add the keys into the log.
{% endhint %}

### **Third Party Instrumentor**

You can add more instrumentation by using the third party instrumentor library. For example, if you want to add instrumentation for Redis you can use official OpenTelemetry Redis Instrumentor library. This is the steps to add the instrumentation:

1.  install the OpenTelemetry instrumentation library.<br>

    ```bash
    pip install opentelemetry-instrumentation-redis
    ```
2.  Initiliaze the instrumentation<br>

    ```python
    from opentelemetry.instrumentation.redis import RedisInstrumentor
    import redis

    RedisInstrumentor().instrument()
    ```

This is the list of instrumentation supported by open telemetry SDK: [open telemetry instrumentation list](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation#readme)

### **GL Observability Custom Instrumentors**

GL Observability also provides additional custom instrumentors to help you capture telemetry from parts of your application that standard libraries might not cover.

#### FunctionsInstrumentor

{% hint style="warning" %}
It is possible to use `FunctionsInstrumentor` to create library native instrumentation, but it is not recommended. Use [#manual-instrumentation](instrumentation.md#manual-instrumentation "mention") instead. &#x20;
{% endhint %}

This instrumentor allows you to wrap specific module-level or class-level functions to automatically create spans, capturing their inputs, outputs, and any exceptions. The instrumentor currently support:

* Class functions (CustomClass.function)
* Module functions (module.function)
* Static methods (@staticmethod)
* Class methods (@classmethod)

#### **Example**

This is the example of how to use Custom functions instrumentation. Let's say you have a functions inside `functions.py` file on the `module` folder that you want to instrument.

```python
def sync_function(...):
    ...

async def async_function(...):
    ...
```

You also have this `custom_class.py` on the `module/classes/custom_class` folder that you want to instrument.

```python
class CustomClass:
    def method(self, ...):
        ...

    @classmethod
    def class_method(cls, ...):
        ...

    @staticmethod
    def static_method(...):
        ...

    async def async_method(self, ...):
        ...

    @classmethod
    async def async_class_method(cls, ...):
        ...

    @staticmethod
    async def async_static_method(...):
        ...
```

To instrument those functions:

```python
from module import functions
from module.classes.custom_class import CustomClass
from gl_observability.traces.instrument.functions import FunctionsInstrumentor

# Instrument all functions in the module
FunctionsInstrumentor().instrument(
    methods=[
        functions.sync_function, functions.async_function,
        CustomClass.method, CustomClass.class_method,
        CustomClass.static_method, CustomClass.async_method,
        CustomClass.async_class_method, CustomClass.async_static_method
])

obj = CustomClass()
# Call the methods
obj.method(...)
CustomClass.class_method(...)
CustomClass.static_method(...)

await obj.async_method(...)
await CustomClass.async_class_method(...)
await CustomClass.async_static_method(...)

functions.sync_function(...)
await functions.async_function(...)

# Uninstrument all functions in the module
FunctionsInstrumentor().uninstrument()
```

#### HTTPClientInstrumentor

This instrumentor is to instrument low level `http` library. Right now, the OpenTelemetry SDK only provide instrumentator for high level http library such as `requests`, `aiohttp`, and `httpx`.

```python
from gl_observability.traces.instrument.http import HTTPClientInstrumentor

HTTPClientInstrumentor().instrument()
```

### Manual Instrumentation

You can also add instrumentation to your own Python code by using the OpenTelemetry SDK directly. Manual instrumentation gives you precise control over what gets traced, how spans are named, and what attributes are captured. This section will guide you how to add instrumentation manually, for more detailed information please refer to [official OpenTelemetry documentation](https://opentelemetry.io/docs/languages/python/instrumentation/).

#### Package Dependency

1.  &#x20;`opentelemetry-api` — GL Observability library already include this library. For native instrumentation though, it is recommended to install it without GL Observability library because it will add unnecessary dependencies into your own library. The `opentelemetry-api`  library can be installed via:<br>

    ```bash
    pip install opentelemetry-api
    ```
2.  Semantic convention library (Optional) — This library contains pre-defined attributes that are well-known naming conventions. Using semantic attributes lets you normalize this kind of information across your systems. The library can be installed via:<br>

    ```bash
    pip install opentelemetry-semantic-conventions ## For general semantic conventions
    pip install opentelemetry-semantic-conventions-ai ## For AI semantic conventions
    ```

#### Get Tracer

Before creating spans, obtain a `Tracer` instance from the global `TracerProvider`. Use your module or library name as the tracer name.

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)
```

#### Create a Span&#x20;

{% tabs %}
{% tab title="Using Decorator" %}
```python
@tracer.start_as_current_span(
    "process_order_service",
    attributes={
        "domain.service.name": "order",
    }
)
def process_order_service(order_id: str):
    ...
```

Using a decorator only needs one line to create a span, but setting dynamic attributes requires additional code to get the current span manually.
{% endtab %}

{% tab title="Using Context Manager" %}
```python
def process_order_service(order_id: str):
    with tracer.start_as_current_span(
        name="process_order_service",
        attributes={
            "domain.service.name": "order",
            "order.id": order_id
        }
    ) span:
        ...
```

Using a context manager allows dynamic attributes but requires wrapping existing code inside the context block.
{% endtab %}
{% endtabs %}

#### Add Attributes to a Span

Spans carry attributes — key/value pairs that provide additional context about the operation being tracked, such as user IDs, request parameters, or status codes.

```python
from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.semconv._incubating.attributes import gen_ai_attributes as GenAIAttributes

current_span = trace.get_current_span()

current_span.set_attribute("span.number", 1)
current_span.set_attribute("span.array", [1, 2, 3])
current_span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
current_span.set_attribute(GenAIAttributes.GEN_AI_PROMPT, "What is the capital city of Indonesia?")
```
