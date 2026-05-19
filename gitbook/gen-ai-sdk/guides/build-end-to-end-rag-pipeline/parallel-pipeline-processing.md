---
icon: align-justify
---

# Parallel Pipeline Processing

This guide will walk you through **implementing parallel execution in your AI pipelines** to dramatically improve performance by running independent operations simultaneously. We'll explore how parallel steps can transform sequential bottlenecks into concurrent workflows that maximize resource utilization and minimize total execution time.

**Parallel pipeline processing** allows you to run multiple independent operations simultaneously rather than sequentially. Instead of waiting for each step to complete before starting the next, you can execute compatible operations concurrently, achieving significant performance improvements and better resource utilization.

{% hint style="info" %}
This tutorial builds upon basic pipeline concepts. Ensure you understand sequential pipeline construction before implementing parallel execution patterns.
{% endhint %}

{% hint style="warning" %}
**Important Note**: The pipeline components used in this tutorial (DocumentExtractor, SentimentAnalyzer, etc.) are simplified examples for demonstration purposes. In practice, you would replace these with your actual component implementations. This guide focuses on parallel execution patterns rather than component implementation details.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of the [Your First RAG Pipeline](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline) tutorial - understanding of basic pipeline construction
2. Completion of all setup steps listed on the [Prerequisites](https://gdplabs.gitbook.io/sdk/overview/prerequisites) page

You should be familiar with these concepts and components:

1. Components in [Your First RAG Pipeline prerequisites](https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline#prerequisites) - **Required foundation**
2. [#parallel](../../tutorials/orchestration/steps/#parallel "mention")step

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

***

## Project Setup

{% stepper %}
{% step %}
**Project Structure**

Create your project structure for parallel pipeline implementation:

```
parallel-pipeline-processing/
├── .env.example
├── parallel_pipeline.py
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```
{% endstep %}
{% endstepper %}

***

## The Problem: Sequential Processing Bottleneck

Consider a document analysis service that performs multiple independent analyses on the same text content:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step

# PROBLEM: Sequential execution creates unnecessary bottlenecks
sequential_pipeline = Pipeline([
    step(DocumentExtractor(), {"document": "input_document"}, "extracted_text"),

    # These operations are INDEPENDENT but run sequentially (inefficient!)
    step(SentimentAnalyzer(), {"text": "extracted_text"}, "sentiment_score"),      # 2.5 seconds
    step(TopicDetector(), {"text": "extracted_text"}, "detected_topics"),         # 2.5 seconds
    step(EntityExtractor(), {"text": "extracted_text"}, "named_entities"),        # 2.5 seconds
    step(LanguageDetector(), {"text": "extracted_text"}, "language_info"),        # 1.5 seconds

    step(ReportGenerator(), {
        "sentiment": "sentiment_score",
        "topics": "detected_topics",
        "entities": "named_entities",
        "language": "language_info"
    }, "analysis_report")
])

# Total execution time: ~9.5 seconds (sum of all operations)
# Problem: Each analysis waits for the previous one despite being independent!
```
{% endcode %}

**Key Issues:**

* **Artificial dependencies**: Independent operations wait unnecessarily
* **Resource waste**: Only one analysis runs at a time
* **Poor scalability**: Adding more analyses linearly increases execution time
* **Performance bottleneck**: Sequential execution when parallel is possible

***

## Solution: Implementing Parallel Steps

Create `parallel_pipeline.py` and transform the sequential bottleneck:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step, parallel

# SOLUTION: Parallel execution eliminates the bottleneck
parallel_pipeline = Pipeline([
    step(DocumentExtractor(), {"document": "input_document"}, "extracted_text"),

    # Run independent operations in parallel
    parallel([
        step(SentimentAnalyzer(), {"text": "extracted_text"}, "sentiment_score"),
        step(TopicDetector(), {"text": "extracted_text"}, "detected_topics"),
        step(EntityExtractor(), {"text": "extracted_text"}, "named_entities"),
        step(LanguageDetector(), {"text": "extracted_text"}, "language_info"),
    ], name="content_analysis_parallel"),

    step(ReportGenerator(), {
        "sentiment": "sentiment_score",
        "topics": "detected_topics",
        "entities": "named_entities",
        "language": "language_info"
    }, "analysis_report")
])

# Total execution time: ~3.5 seconds (maximum of parallel operations, not sum)
# Performance improvement: 60-70% faster execution!
```
{% endcode %}

**Key improvements:**

* **Concurrent execution**: All analyses run simultaneously
* **Maximum vs sum**: Total time is the slowest operation (3.5s), not sum (9.5s)
* **Resource efficiency**: Better CPU/GPU utilization
* **Same results**: Identical output with dramatically better performance

***

## Troubleshooting

### **Common Issues**

1. **Dependencies between parallel steps**:
   * Ensure parallel operations don't depend on each other's outputs
   * Verify that each parallel step has independent inputs and outputs
   * Check that no step modifies shared state used by other parallel steps
2. **Resource exhaustion with too many parallel operations**:
   * Limit the number of concurrent operations based on available resources
   * Monitor CPU/memory usage during parallel execution
   * Consider grouping operations or using resource-aware patterns
3. **Incorrect state mapping after parallel execution**:
   * Verify that parallel steps only use inputs available before the parallel block
   * Ensure the step following parallel execution can access all parallel outputs
   * Check that parallel output state names don't conflict
4. **Performance not improving as expected**:
   * Confirm that operations are truly independent and can benefit from parallelism
   * Check if I/O bottlenecks are limiting parallel performance gains
   * Profile individual operations to identify actual bottlenecks

### **Debug Tips**

1. **Start with sequential implementation**: Build and test your pipeline sequentially first
2. **Identify independent operations**: Look for steps that use the same inputs but produce different outputs
3. **Use meaningful names**: Name your parallel blocks for easier debugging and monitoring
4. **Test incrementally**: Add parallelism gradually and verify each step works correctly
5. **Monitor resource usage**: Check CPU, memory, and I/O utilization during parallel execution

### **When to Use Parallel Steps**

✅ **Good candidates for parallelism:**

* Multiple analyses on the same input data (sentiment, topics, entities)
* Independent API calls or database queries
* Different model inferences on the same content
* Multiple format conversions or transformations
* Parallel data processing tasks

❌ **Avoid parallelism when:**

* Operations have dependencies on each other's outputs
* Shared resources could cause conflicts or race conditions
* Operations are already I/O bound (limited by external services)
* The overhead of parallelism exceeds the benefits
* Sequential processing is required for correctness

### **Performance Optimization Guidelines**

{% hint style="warning" %}
Remember that the goal isn't to parallelize everything, but to parallelize strategically where it provides clear benefits in execution time, resource utilization, and overall system throughput.
{% endhint %}

1. **Profile first**: Identify actual bottlenecks before optimizing
2. **Test with realistic workloads**: Use actual data sizes and operation complexity
3. **Consider resource limits**: Don't exceed available CPU, memory, or I/O capacity
4. **Balance complexity**: Ensure the performance gains justify the added complexity
5. **Monitor in production**: Track performance improvements in real-world scenarios

***

Congratulations! You've successfully learned how to implement parallel execution in your AI pipelines. By strategically applying parallel processing to independent operations, you can achieve significant performance improvements while maintaining code clarity and reliability. Your pipelines will now maximize resource utilization and minimize execution time through concurrent processing.
