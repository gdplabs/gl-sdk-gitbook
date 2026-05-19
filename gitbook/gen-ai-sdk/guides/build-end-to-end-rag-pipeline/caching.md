---
icon: memory
---

# Caching

This guide will walk you through **implementing caching** in your AI pipelines to eliminate redundant computations and improve performance. We'll explore how pipeline caching can transform expensive, repetitive operations into instant responses.

**Caching functionality** gives you control over performance optimization in your pipeline, providing flexibility to cache at different levels based on your specific needs. For example, you can implement step-level caching for expensive operations, pipeline-level caching for complete workflows, or combine both for maximum efficiency.

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") **tutorial** - this builds directly on top of it
2. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page
3. A working OpenAI API key configured in your environment variables

You should be familiar with these concepts and components:

1. Components in [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") - **Required foundation**
2. [data-store](../../tutorials/data-store/ "mention")

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/008_caching" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Extend Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the previous tutorial. The caching functionality works with any pipeline components - we'll demonstrate with your existing RAG pipeline:

Your existing structure is already complete:

```
caching/
├── data/
│   ├── chroma.sqlite3
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── indexer.py
├── pipeline.py                     # 👈 Will be updated with caching
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```
{% endstep %}
{% endstepper %}

***

## Understanding Pipeline Caching

When you deploy pipelines to production, you quickly discover a common pattern: the same inputs get processed over and over again. Users ask similar questions, run identical analyses, or trigger the same computational workflows repeatedly.

GLLM Pipeline framework provides two levels of caching that work seamlessly together: **pipeline-level caching** and **step-level caching**. Pipeline-level caching stores the entire pipeline's output for a given input, while step-level caching stores individual step results within the pipeline execution.

Our caching system uses [data store](../../tutorials/data-store/) as the cache backend, which provides several advantages: semantic similarity matching (so similar inputs can benefit from cached results), scalable storage, and fast retrieval performance.

## 1) Set Up Your Cache Data Store

{% stepper %}
{% step %}
**Create the cache data store**

Before implementing any caching option, you need to set up a cache data store. Add this to your pipeline file:

{% code lineNumbers="true" %}
```python
from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

# Create a data store cache with vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
cache_store = ChromaDataStore(
    collection_name="my_cache",
).with_vector(em_invoker=em_invoker).as_cache()
```
{% endcode %}

You could also configure the matching config (exact match/fuzzy match/semantic match) of the cache store by following the guide in [Vector Data Store](https://gdplabs.gitbook.io/sdk/tutorials/data-store/vector-data-store/using-vector-data-store-as-a-cache) page.
{% endstep %}
{% endstepper %}

## 2) Choose Your Caching Strategy

**Pipeline caching** allows you to optimize performance at different levels based on your specific needs. Each approach can be implemented independently, giving you flexibility to choose the right caching strategy for your use case:

1. **Step-Level Caching**: Caches individual step results within pipeline execution
2. **Pipeline-Level Caching**: Caches complete pipeline outputs for given inputs
3. **Multi-Level Caching**: Combines both approaches for maximum efficiency

You can choose any combination of these options based on your performance requirements and use cases.

### Option 1: Pipeline-Level Caching

**When to use**: Cache complete pipeline results when users frequently run identical workflows with the same inputs.

{% stepper %}
{% step %}
**Enable caching for the entire pipeline**

Create your pipeline with caching enabled:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.pipeline import Pipeline

from gllm_pipeline.types import CacheConfig

e2e_pipeline_with_cache = Pipeline(
    [
        step(
            component=VectorRetriever(data_store=data_store),
            input_map={"query": "user_query", "top_k": "top_k"},
            output_state="chunks",
        ),
        step(
            component=ResponseSynthesizer.stuff_preset(os.getenv("LANGUAGE_MODEL")),
            input_map={"query": "user_query", "chunks": "chunks"},
            output_state="response",
        ),
    ],
    cache=CacheConfig(store=cache_store),  # Enable pipeline-level caching
)
```
{% endcode %}

**Benefits:**

* Maximum performance for repeated identical queries
* Simple implementation - just add `cache` parameter with `CacheConfig`
* Best for production environments with repetitive usage patterns
{% endstep %}
{% endstepper %}

### Option 2: Multi-Level Caching

We could also use step-level caching alongside pipeline caching. If pipeline caching fails, each step with an active cache will check for a cache hit individually.

{% stepper %}
{% step %}
**Enable caching for the step and pipeline level**

Create your step and pipeline with caching enabled:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.pipeline import Pipeline

from gllm_pipeline.types import CacheConfig

e2e_pipeline_with_cache = Pipeline(
    [
        step(
            component=VectorRetriever(data_store=data_store),
            input_map={"query": "user_query", "top_k": "top_k"},
            output_state="chunks",
            cache=CacheConfig(store=cache_store),  # Enable step-level caching
        ),
        step(
            component=ResponseSynthesizer.stuff_preset(os.getenv("LANGUAGE_MODEL")),
            input_map={"query": "user_query", "chunks": "chunks"},
            output_state="response",
        ),
    ],
    cache=CacheConfig(store=cache_store),  # Enable pipeline-level caching
)
```
{% endcode %}
{% endstep %}
{% endstepper %}

## 3) Run the Pipeline

{% include "../../../.gitbook/includes/telemetry-notice.md" %}

{% stepper %}
{% step %}
**Configure the pipeline state for testing**

Set up test cases to demonstrate caching behavior:

{% code lineNumbers="true" %}
```python
# Test state for caching demonstration
test_state = {
    "user_query": "Give me nocturnal creatures",
    "context": "",
}

config = {
    "top_k": 5,
    "debug": True,  # Enable debug to see cache hits/misses
}
```
{% endcode %}
{% endstep %}

{% step %}
**Run the pipeline first time (cache miss)**

```python
import time

start_time = time.time()
result1 = asyncio.run(e2e_pipeline_with_cache.invoke(test_state, config))
first_time = time.time() - start_time
print(f"First execution time: {first_time:.2f} seconds")
print(f"Result: {result1['response'][:100]}...")
```

This execution will populate both step-level and pipeline-level caches.
{% endstep %}

{% step %}
**Run the same pipeline again (cache hit)**

```python
start_time = time.time()
result2 = asyncio.run(e2e_pipeline_with_cache.invoke(test_state, config))
second_time = time.time() - start_time
print(f"Second execution time: {second_time:.2f} seconds")
print(f"Speed improvement: {(first_time/second_time):.1f}x faster")
print(f"Results identical: {result1['response'] == result2['response']}")
```

You should see an improvement on the second run.
{% endstep %}
{% endstepper %}

## Troubleshooting

1. **Cache not providing expected speedup**:
   1. Verify debug logs show cache hits/misses as expected
   2. Ensure your inputs are similar enough to trigger cache hits
2. **General caching issues**:
   1. Verify your cache data store is properly initialized
   2. Check that cache keys are being generated consistently
   3. Monitor cache hit/miss rates to optimize cache configuration
   4. Test cache behavior with various input patterns

***

Congratulations! You've successfully enhanced your RAG pipeline with multi-level caching functionality. Your pipeline can now eliminate redundant computations and provide dramatic performance improvements for repeated or similar requests. This caching system scales with your application and provides intelligent matching for optimal cache utilization.o
