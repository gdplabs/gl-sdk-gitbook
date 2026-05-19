---
icon: rotate
---

# Query Transformation

This guide will walk you through **adding a Query Transformer component to your existing RAG pipeline** that automatically rewrites and optimizes user queries for better document retrieval, improving the relevance and accuracy of your search results.

**Query transformation** enhances your RAG pipeline by intelligently reformulating user queries to improve retrieval performance, helping you find more relevant documents and generate better responses.

{% include "../../../.gitbook/includes/extend-first-rag.md" %}

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. **Completion of the** [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") **tutorial** - this builds directly on top of it
2. Completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page
3. A working OpenAI API key configured in your environment variables

You should be familiar with these concepts and components:

1. Components in [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention")- **Required foundation**
2. query-transformer

</details>

{% include "../../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/build_end_to_end_rag_pipeline/006_query_transformation" class="button primary" data-icon="github">View full project code on GitHub</a>

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
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-rag gllm-core gllm-generation gllm-inference gllm-pipeline gllm-retrieval gllm-misc gllm-datastore
```
{% endtab %}
{% endtabs %}

***

{% include "../../../.gitbook/includes/how-to-use-this-guide.md" %}

## Project Setup

{% stepper %}
{% step %}
**Extend Your RAG Pipeline Project**

Start with your completed RAG pipeline project from the [your-first-rag-pipeline.md](your-first-rag-pipeline.md "mention") tutorial. We don't need to add any new file for this tutorial. Therefore, the structure should stay as is:

```
query-transformation/
├── data/
│   └── imaginary_animals.csv
├── .env
├── .env.example
├── indexer.py
├── pipeline.py    # 👈 Will be updated with query transformer
├── pyproject.toml
├── setup.bat
├── setup.sh
└── uv.lock
```
{% endstep %}
{% endstepper %}

***

## 1) Build the Query Transformer Pipeline

{% stepper %}
{% step %}
**Define extended RAG state**

Create a custom state that includes the `query` state:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.pipeline import RAGState

class RAGStateWithQT(RAGState):
    query: str
```
{% endcode %}
{% endstep %}

{% step %}
**Create all pipeline steps**

Define all steps including the new query transformer step:

{% code lineNumbers="true" %}
```python
from gllm_pipeline.steps import step, transform
from gllm_retrieval.query_transformer.one_to_one_query_transformer import OneToOneQueryTransformer

transform_query_step = step(
    component=OneToOneQueryTransformer(
        lm_request_processor=build_lm_request_processor(
            model_id="openai/gpt-4o-mini",
            system_template="You are a helpful assistant that rewrites queries for better retrieval. Rewrite the following query. Only output the transformed query.",
            user_template="Query: {query}",
        )
    ),
    input_map={"query": "user_query"},
    output_state="queries",
)

flatten_query = transform(
    operation=lambda x: "\n".join(x["queries"]),
    input_states=["queries"],
    output_state="query",
)
```
{% endcode %}
{% endstep %}

{% step %}
**Compose the final pipeline**

Chain all steps including the query transformer:

{% code lineNumbers="true" %}
```python
e2e_pipeline = (
    query_transformer_step
    | flatten_query
    | retriever_step
    | response_synthesizer_step
)

e2e_pipeline.state_type = RAGStateWithQT
```
{% endcode %}

This creates a pipeline that **first transforms the user query** before retrieving relevant documents, leading to better search results.

> 🧠 The `RAGStateWithQT` extends the base `RAGState` to include the transformed query field.
{% endstep %}
{% endstepper %}

## 2) Run the Pipeline

{% include "../../../.gitbook/includes/telemetry-notice.md" %}

{% stepper %}
{% step %}
**Configure and invoke the pipeline**

Configure the state and config for direct pipeline invocation:

```python
# Run the pipeline
async def main():
    state = {"user_query": "Give me nocturnal creatures from the dataset"}  # Replace with your actual query
    config = {"top_k": 5}
    result = await e2e_pipeline.invoke(state, config)
    print(f"Pipeline result: {result['response']}")


if __name__ == "__main__":
    asyncio.run(main())
```
{% endstep %}

{% step %}
**Observe output**

If you successfully run all the steps, you will see something like this:

```bash
DEBUG    [OneToOneQueryTransformer] [Start 'OneToOneQueryTransformer'] Processing query:     component.py:130
         'Give me nocturnal creatures from the dataset'
WARNING  [LMRequestProcessor] The `prompt_kwargs` parameter is deprecated and     lm_request_processor.py:160
         will be removed in v0.6. Please pass the prompt kwargs as keyword
         arguments instead.
INFO     [OpenAILMInvoker] Invoking 'OpenAILMInvoker'                                       lm_invoker.py:252
INFO     [LMRequestProcessor] LM invocation result:                               lm_request_processor.py:195
         'List nocturnal animals from the dataset.'
DEBUG    [OneToOneQueryTransformer] [Finished 'OneToOneQueryTransformer'] Successfully       component.py:130
         produced 1 result(s):
         - 'List nocturnal animals from the dataset.'
```
{% endstep %}
{% endstepper %}

## Extending the Query Transformation System

### **Multiple Query Transformation Strategies**

You can extend the system with different transformation approaches:

```python
def multi_strategy_query_transformer():
    """Creates multiple query variations for better retrieval."""
    lmrp = build_lm_request_processor(
        model_id="openai/gpt-4o-mini",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="Generate 3 different variations of the following query for better document retrieval. Output each variation on a new line.",
        user_template="Query: {query}",
    )

    return OneToOneQueryTransformer(lm_request_processor=lmrp)
```

### **Domain-Specific Query Transformers**

Create specialized transformers for different content domains:

```python
def academic_query_transformer():
    """Transforms queries for academic document retrieval."""
    lmrp = build_lm_request_processor(
        model_id="openai/gpt-4o-mini",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="Rewrite the following query using academic terminology for better scholarly document retrieval.",
        user_template="Query: {query}",
    )

    return OneToOneQueryTransformer(lm_request_processor=lmrp)

def technical_query_transformer():
    """Transforms queries for technical documentation retrieval."""
    lmrp = build_lm_request_processor(
        model_id="openai/gpt-4o-mini",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="Rewrite the following query using precise technical terms for better API and documentation retrieval.",
        user_template="Query: {query}",
    )

    return OneToOneQueryTransformer(lm_request_processor=lmrp)
```

### **Custom Query Transformation Logic**

You can implement custom transformation logic:

```python
class CustomRAGState(RAGState):
    original_query: str
    transformed_query: str
    query_intent: str

def intent_aware_query_transformer():
    """Transforms queries based on detected intent."""
    intent_detector = build_lm_request_processor(
        model_id="openai/gpt-4o-mini",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="Classify the intent of this query as: factual, comparative, procedural, or exploratory. Output only the classification.",
        user_template="Query: {query}",
    )

    query_rewriter = build_lm_request_processor(
        model_id="openai/gpt-4o-mini",
        credentials=os.getenv("OPENAI_API_KEY"),
        system_template="Rewrite this {intent} query for optimal document retrieval.",
        user_template="Query: {query}",
    )

    return OneToOneQueryTransformer(lm_request_processor=query_rewriter)
```

## Troubleshooting

**Common Issues**

1. **Poor query transformations**:
   * Review and refine your system template for the query transformer
   * Ensure the transformation model (GPT-4o-mini) is appropriate for your use case
   * Test different system prompts to improve transformation quality
2. **Query transformation taking too long**:
   * Consider using a faster model for query transformation
   * Implement caching for frequently transformed queries
   * Set appropriate timeout configurations in your LM request processor
3. **Transformed queries not improving retrieval**:
   * Analyze the transformed queries to ensure they're more specific
   * Test with different transformation strategies
   * Consider the quality and indexing of your document corpus
4. **Pipeline state management issues**:
   * Ensure your custom RAGState class properly extends the base RAGState
   * Verify that all state field names match between pipeline steps
   * Check that the state\_type is properly assigned to your pipeline

**Debug Tips**

1. **Enable debug mode**: Set `debug: true` in your request to see detailed logs
2. **Log query transformations**: Use the log step to see original vs transformed queries
3. **Test transformations in isolation**: Test your query transformer component separately
4. **Compare retrieval results**: Compare document retrieval with and without query transformation
5. **Monitor transformation quality**: Manually review a sample of transformed queries for quality

***

Congratulations! You've successfully implemented a Query Transformer component in your RAG pipeline. This enhancement improves document retrieval by intelligently rewriting user queries, leading to more relevant search results and better response quality. Your AI system can now understand user intent better and retrieve more appropriate information from your knowledge base.
