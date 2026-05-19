---
icon: object-union
---

# Subgraphs

This guide will walk you through **using pipeline subgraphs to break down complex pipelines** into manageable, maintainable components. We'll transform a monolithic RAG pipeline that has become unwieldy into a well-organized system using focused subgraphs.

**Pipeline subgraphs** solve the complexity problem by providing a way to break down large pipelines into smaller, manageable pieces. Instead of having one massive pipeline with 20+ steps, you can create focused subgraphs, each responsible for a specific part of your workflow with its own clean state schema and testing strategy.

{% hint style="info" %}
This tutorial builds upon fundamental pipeline concepts. Ensure you understand basic pipeline construction before proceeding with subgraph architecture.
{% endhint %}

{% hint style="warning" %}
**Important Note**: The pipeline components used in this tutorial (QueryProcessor, DocumentRetriever, etc.) are simplified examples for demonstration purposes. In practice, you would replace these with your actual component implementations. This guide focuses on subgraph architecture patterns rather than component implementation details.
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of the [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") tutorial - understanding of basic pipeline construction
2. Completion of all setup steps listed on the [#prerequisites](subgraphs.md#prerequisites "mention") page

You should be familiar with these concepts and components:

1. Components in [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") - **Required foundation**
2. [#subgraph](../../tutorials/orchestration/steps/#subgraph "mention")step

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
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-pipeline gllm-rag gllm-core gllm-generation gllm-inference gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

***

## Project Setup

{% stepper %}
{% step %}
**Understanding the Problem**

When you first start building pipelines, everything seems straightforward. You create a few steps, connect them together, and your pipeline works perfectly.

Your pipeline starts simple: take a user query, retrieve some documents, and generate a response. But then you realize you need query preprocessing, document filtering, reranking, context building, prompt engineering, etc. Suddenly, your pipeline has grown from 3 steps to 15 steps.

**Key Pain Points:**

* **Pipeline Bloat**: Simple pipelines grow into 15+ step monsters
* **State Chaos**: Dozens of intermediate variables with unclear purposes
* **Testing Nightmares**: Can't test components in isolation
* **Maintenance Difficulties**: Changes in one area break unrelated functionality
{% endstep %}

{% step %}
**The Subgraph Solution**

Subgraphs solve these problems by providing:

* **Modular Design**: Break complex pipelines into focused, manageable pieces
* **State Isolation**: Each subgraph has its own clean state schema
* **Reusability**: Use the same subgraph in multiple pipelines
* **Clearer Organization**: Logical grouping of related functionality
* **Easier Maintenance**: Modify one subgraph without affecting others
{% endstep %}

{% step %}
**Project Structure**

Create your project structure for the subgraph refactoring:

```
subgraphs/
├── .env.example
├── pipeline_builder.py             # 👈 Single file with all subgraphs
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```

Following real-world patterns, we'll organize all subgraphs within a single pipeline builder class, just like production implementations.
{% endstep %}
{% endstepper %}

***

## Problem: The Monolithic Pipeline with Tons of Steps

Let's first examine a typical complex RAG pipeline that has become unwieldy:

{% stepper %}
{% step %}
**The Monolithic Pipeline State**

{% code lineNumbers="true" %}
```python
from typing import TypedDict
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step

class MonolithicRAGState(TypedDict):
    user_query: str
    processed_query: str
    expanded_query: str
    retrieved_documents: list
    filtered_documents: list
    reranked_documents: list
    selected_documents: list
    context: str
    prompt: str
    generated_response: str
    formatted_response: str
    validated_response: str
    response_metadata: dict
```
{% endcode %}

Notice how this state has **13 different variables** - it's becoming impossible to track what each one does and when it's used.
{% endstep %}

{% step %}
**The Monolithic Pipeline Implementation**

{% code lineNumbers="true" %}
```python
# Example dummy components for demonstration
class QueryProcessor: pass
class QueryExpander: pass
class DocumentRetriever: pass
class DocumentFilter: pass
class RelevanceReranker: pass
class TopKSelector: pass
class ContextBuilder: pass
class PromptBuilder: pass
class LLMGenerator: pass
class ResponseFormatter: pass
class ResponseValidator: pass
class MetadataExtractor: pass

# Monolithic pipeline with many steps
monolithic_rag_pipeline = Pipeline([
    # Query processing
    step(QueryProcessor(), {"query": "user_query"}, "processed_query"),
    step(QueryExpander(), {"query": "processed_query"}, "expanded_query"),

    # Retrieval
    step(DocumentRetriever(), {"query": "expanded_query"}, "retrieved_documents"),
    step(DocumentFilter(), {"documents": "retrieved_documents"}, "filtered_documents"),

    # Reranking
    step(RelevanceReranker(), {"documents": "filtered_documents", "query": "processed_query"}, "reranked_documents"),
    step(TopKSelector(), {"documents": "reranked_documents"}, "selected_documents"),

    # Context preparation
    step(ContextBuilder(), {"documents": "selected_documents"}, "context"),

    # Generation
    step(PromptBuilder(), {"query": "processed_query", "context": "context"}, "prompt"),
    step(LLMGenerator(), {"prompt": "prompt"}, "generated_response"),
    step(ResponseFormatter(), {"response": "generated_response"}, "formatted_response"),
    step(ResponseValidator(), {"response": "formatted_response"}, "validated_response"),

    # Metadata
    step(MetadataExtractor(), {"response": "validated_response"}, "response_metadata"),
], state_type=MonolithicRAGState)
```
{% endcode %}

This pipeline has several problems:

1. **Hard to understand** what each section does
2. **Cluttered state** with intermediate variables
3. **Difficult to test** individual components
4. **Risky changes** - modifying one part can break others
{% endstep %}
{% endstepper %}

***

## Solution: Building with Subgraphs

Now let's refactor this into a clean, modular pipeline builder following real-world patterns:

### 1) Create the Pipeline Builder Class

{% stepper %}
{% step %}
**Create the main pipeline builder**

Create `pipeline_builder.py`:

{% code lineNumbers="true" %}
```python
from typing import TypedDict
import asyncio
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step, subgraph

# Example dummy components - replace with your actual implementations
class QueryProcessor: pass
class QueryExpander: pass
class DocumentRetriever: pass
class DocumentFilter: pass
class RelevanceReranker: pass
class TopKSelector: pass
class ContextBuilder: pass
class PromptBuilder: pass
class LLMGenerator: pass
class ResponseFormatter: pass
class ResponseValidator: pass
class MetadataExtractor: pass

class ModularRAGPipelineBuilder:
    """Modular RAG pipeline builder using subgraphs."""

    def build(self) -> Pipeline:
        """Build the main pipeline using subgraphs."""
        preprocessing_step = self._build_preprocessing_subgraph()
        retrieval_step = self._build_retrieval_subgraph()
        generation_step = self._build_generation_subgraph()

        pipeline = Pipeline(
            steps=[
                preprocessing_step,
                retrieval_step,
                generation_step,
            ],
            state_type=MainRAGState,
            recursion_limit=100,
        )

        return pipeline
```
{% endcode %}

**Benefits:**

* **Clean organization**: Each subgraph is a separate method
* **Real-world pattern**: Matches production implementations
* **Easy to understand**: Clear separation of concerns
{% endstep %}

{% step %}
**Define the clean main state**

{% code lineNumbers="true" %}
```python
# Clean main pipeline state - only essential variables
class MainRAGState(TypedDict):
    user_query: str
    processed_query: str
    expanded_query: str
    context: str
    final_response: str
    metadata: dict
```
{% endcode %}

Notice how the main state only contains **6 essential variables** instead of the original 13!
{% endstep %}
{% endstepper %}

### 2) Build Individual Subgraphs

{% stepper %}
{% step %}
**Create the Query Processing Subgraph**

{% code lineNumbers="true" %}
```python
def _build_preprocessing_subgraph(self):
    """Build the query preprocessing subgraph."""

    # Clean, focused state schema for this subgraph
    class QueryProcessingState(TypedDict):
        user_query: str
        processed_query: str
        expanded_query: str

    # Create the preprocessing pipeline
    preprocessing_pipeline = Pipeline([
        step(QueryProcessor(), {"query": "user_query"}, "processed_query"),
        step(QueryExpander(), {"query": "processed_query"}, "expanded_query"),
    ], state_type=QueryProcessingState)

    # Wrap as subgraph with clean state mapping
    return subgraph(
        subgraph=preprocessing_pipeline,
        input_map={"user_query": "user_query"},
        output_state_map={
            "processed_query": "processed_query",
            "expanded_query": "expanded_query"
        },
        name="preprocessing_step"
    )
```
{% endcode %}

**Benefits:**

* **Clear responsibility**: Only handles query processing
* **Clean state**: Just 3 relevant variables
* **Easy testing**: Can test query processing in isolation
* **Explicit mapping**: Clear input/output contracts
{% endstep %}

{% step %}
**Create the Retrieval Subgraph**

{% code lineNumbers="true" %}
```python
def _build_retrieval_subgraph(self):
    """Build the document retrieval subgraph."""

    class RetrievalState(TypedDict):
        query: str
        retrieved_documents: list
        filtered_documents: list
        reranked_documents: list
        selected_documents: list
        context: str

    # Create the retrieval pipeline
    retrieval_pipeline = Pipeline([
        step(DocumentRetriever(), {"query": "query"}, "retrieved_documents"),
        step(DocumentFilter(), {"documents": "retrieved_documents"}, "filtered_documents"),
        step(RelevanceReranker(), {"documents": "filtered_documents", "query": "query"}, "reranked_documents"),
        step(TopKSelector(), {"documents": "reranked_documents"}, "selected_documents"),
        step(ContextBuilder(), {"documents": "selected_documents"}, "context"),
    ], state_type=RetrievalState)

    return subgraph(
        subgraph=retrieval_pipeline,
        input_map={"query": "expanded_query"},
        output_state_map={"context": "context"},
        name="retrieval_step"
    )
```
{% endcode %}

**Benefits:**

* **Focused functionality**: Only handles document retrieval and context building
* **Isolated state**: Contains only retrieval-related variables
* **Reusable**: Can be used in different types of pipelines
{% endstep %}

{% step %}
**Create the Generation Subgraph**

{% code lineNumbers="true" %}
```python
def _build_generation_subgraph(self):
    """Build the response generation subgraph."""

    class GenerationState(TypedDict):
        query: str
        context: str
        prompt: str
        generated_response: str
        formatted_response: str
        validated_response: str
        response_metadata: dict

    # Create the generation pipeline
    generation_pipeline = Pipeline([
        step(PromptBuilder(), {"query": "query", "context": "context"}, "prompt"),
        step(LLMGenerator(), {"prompt": "prompt"}, "generated_response"),
        step(ResponseFormatter(), {"response": "generated_response"}, "formatted_response"),
        step(ResponseValidator(), {"response": "formatted_response"}, "validated_response"),
        step(MetadataExtractor(), {"response": "validated_response"}, "response_metadata"),
    ], state_type=GenerationState)

    return subgraph(
        subgraph=generation_pipeline,
        input_map={
            "query": "processed_query",
            "context": "context"
        },
        output_state_map={
            "final_response": "validated_response",
            "metadata": "response_metadata"
        },
        name="generation_step"
    )
```
{% endcode %}

**Benefits:**

* **Single responsibility**: Only handles response generation
* **Clear data flow**: Easy to understand prompt → generation → validation flow
* **Independent testing**: Can test generation logic separately
{% endstep %}
{% endstepper %}

### 3) Run the Subgraph Pipeline

{% stepper %}
{% step %}
**Complete the pipeline builder**

Add the complete implementation:

{% code lineNumbers="true" %}
```python
# Complete pipeline_builder.py
from typing import TypedDict
import asyncio
from gllm_pipeline.pipeline import Pipeline
from gllm_pipeline.steps import step, subgraph

# [Include all the dummy component classes and state definitions from above]

class ModularRAGPipelineBuilder:
    """Modular RAG pipeline builder using subgraphs."""

    def build(self) -> Pipeline:
        """Build the main pipeline using subgraphs."""
        preprocessing_step = self._build_preprocessing_subgraph()
        retrieval_step = self._build_retrieval_subgraph()
        generation_step = self._build_generation_subgraph()

        pipeline = Pipeline(
            steps=[
                preprocessing_step,
                retrieval_step,
                generation_step,
            ],
            state_type=MainRAGState,
            recursion_limit=100,
        )

        return pipeline

    # [Include all the _build_*_subgraph methods from above]

# Test the pipeline
async def test_modular_pipeline():
    builder = ModularRAGPipelineBuilder()
    pipeline = builder.build()

    state = {
        "user_query": "What are some forest animals?",
    }

    config = {
        "top_k": 5,
        "debug": True,
    }

    result = await pipeline.invoke(state, config)
    print(f"Pipeline result: {result}")

if __name__ == "__main__":
    asyncio.run(test_modular_pipeline())
```
{% endcode %}
{% endstep %}

{% step %}
**Run the pipeline**

```bash
python pipeline_builder.py
```
{% endstep %}

{% step %}
**Observe the improved output**

You should see much cleaner debug output with clearly separated subgraph execution:

```
Starting pipeline
[Start Subgraph 'preprocessing_step'] Processing user query
[Finished Subgraph 'preprocessing_step'] Query processed and expanded
[Start Subgraph 'retrieval_step'] Retrieving relevant documents
[Finished Subgraph 'retrieval_step'] Context prepared from 5 documents
[Start Subgraph 'generation_step'] Generating response
[Finished Subgraph 'generation_step'] Response generated and validated
Finished pipeline
```

**Benefits of the subgraph output:**

* **Clear boundaries**: Easy to see where each logical unit starts and ends
* **Focused debugging**: Problems can be isolated to specific subgraphs
* **Progress tracking**: Better visibility into pipeline execution progress
{% endstep %}
{% endstepper %}

## Comparison: Before vs After

By transforming the monolithic pipeline into subgraphs, we achieved:

* **Before**: 15 steps in one pipeline → **After**: 3 focused subgraphs
* **Before**: 13 cluttered state variables → **After**: 6 clean state variables
* **Before**: Hard to test individual components → **After**: Easy independent testing
* **Before**: Changes risk breaking other parts → **After**: Isolated modifications
* **Before**: Unclear responsibilities → **After**: Single responsibility per subgraph

***

## Troubleshooting

**Common Issues**

1. **State mapping errors between subgraphs**:
   * Ensure all required input states are properly mapped in `input_map`
   * Verify that output states from one subgraph match input requirements of the next
   * Check that variable names are consistent across subgraph boundaries
2. **Subgraph isolation breaking shared dependencies**:
   * Make sure each subgraph includes all components it needs
   * Avoid assuming components are available from other subgraphs
   * Consider creating shared component factories for reusable dependencies
3. **Complex debugging across multiple subgraphs**:
   * Use meaningful names for each subgraph for easier identification
   * Enable debug mode to see subgraph boundaries in execution logs
   * Test individual subgraphs in isolation before combining them
4. **Component implementation confusion**:
   * Remember that the example components (QueryProcessor, etc.) are placeholders
   * Replace with your actual component implementations
   * Focus on the subgraph structure patterns, not the specific components

**Debug Tips**

1. **Test subgraphs individually**: Each subgraph should work independently with its own state
2. **Use descriptive subgraph names**: This makes debugging much easier
3. **Enable debug logging**: Set `debug: true` to see subgraph execution boundaries
4. **Validate state schemas**: Ensure each subgraph's state schema matches its actual usage
5. **Map states explicitly**: Always use explicit state mapping rather than relying on defaults
6. **Follow production patterns**: Organize subgraphs as methods within a pipeline builder class

***

Congratulations! You've successfully learned how to use pipeline subgraphs to transform complex, monolithic pipelines into clean, maintainable, and testable modular systems. By following production patterns with a single pipeline builder class, your subgraph organization will be both powerful and practical for real-world applications.
