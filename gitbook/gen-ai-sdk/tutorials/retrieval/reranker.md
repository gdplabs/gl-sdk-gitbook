---
icon: ranking-star
---

# Reranker

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/reranker) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [reranker.md](reranker.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/reranker.html)

## What's a Reranker?

A **reranker** is a component that reorders retrieved chunks based on their relevance to a query. After initial retrieval returns a set of candidate chunks, the reranker scores and sorts them to ensure the most relevant content appears first. This improves the quality of context provided to language models in RAG pipelines.

Rerankers are particularly useful when:

1. Initial retrieval returns many candidates that need prioritization
2. You want to combine results from multiple retrieval sources
3. The retrieval method does not perfectly capture semantic relevance

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-retrieval"
```
{% endtab %}
{% endtabs %}

## Quickstart

Let's start with a basic example using `SimilarityBasedReranker`, which uses embedding similarity to rerank chunks:

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_retrieval.reranker import SimilarityBasedReranker

em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)

# Create the reranker
reranker = SimilarityBasedReranker(embeddings=em_invoker)

# Sample chunks to rerank
chunks = [
    Chunk(id="1", content="Python is a programming language"),
    Chunk(id="2", content="Machine learning uses algorithms to learn from data"),
    Chunk(id="3", content="Deep learning is a subset of machine learning"),
]

# Rerank based on query relevance
query = "What is machine learning?"
reranked = asyncio.run(reranker.rerank(chunks, query))

for i, chunk in enumerate(reranked, 1):
    print(f"{i}. {chunk.content}")
```

**Expected Output**

The chunks are reordered with the most relevant content first:

```
1. Machine learning uses algorithms to learn from data
2. Deep learning is a subset of machine learning
3. Python is a programming language
```

## Available Rerankers

The SDK provides multiple reranker implementations for different use cases:

| Reranker                  | Description                            | Best For                                  |
| ------------------------- | -------------------------------------- | ----------------------------------------- |
| `CohereBedrockReranker`   | Uses AWS Bedrock Cohere service        | Cloud-based, managed reranking            |
| `FlagEmbeddingReranker`   | Uses FlagEmbedding models              | Multilingual and specialized domains      |
| `JinaReranker`            | Uses Jina AI's reranker API            | Cloud-based reranking via Jina AI         |
| `SimilarityBasedReranker` | Uses embedding similarity scores       | General-purpose semantic reranking        |
| `TEIReranker`             | Uses Text Embedding Inference endpoint | High-performance, self-hosted deployments |

## Similarity-Based Reranking

The `SimilarityBasedReranker` calculates embedding similarity between the query and each chunk, then sorts by score:

```python
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM
from gllm_retrieval.reranker import SimilarityBasedReranker

em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)
reranker = SimilarityBasedReranker(embeddings=em_invoker)

reranked = await reranker.rerank(chunks, query)
```

{% hint style="info" %}
**Custom Similarity Functions**: You can provide a custom similarity function that takes two embedding vectors and returns a float score. Higher scores indicate greater similarity.
{% endhint %}

## TEI Reranking

The `TEIReranker` uses a reranker model hosted on [Text Embedding Inference (TEI)](https://huggingface.github.io/text-embeddings-inference/):

```python
from gllm_retrieval.reranker import TEIReranker

reranker = TEIReranker(
    url="https://your-tei-endpoint.com/rerank",
    timeout=10,
    fallback_to_original=True,
)

reranked = await reranker.rerank(chunks, query)
```

{% hint style="info" %}
**Authentication**: TEIReranker supports both basic auth (username/password) and bearer token (api\_key) authentication methods.
{% endhint %}

## FlagEmbedding Reranking

The `FlagEmbeddingReranker` uses [FlagEmbedding](https://github.com/FlagOpen/FlagEmbedding) models for reranking:

```python
from gllm_retrieval.reranker import FlagEmbeddingReranker

reranker = FlagEmbeddingReranker(
    model_path="BAAI/bge-reranker-base",
    use_fp16=True,
)

reranked = await reranker.rerank(chunks, query)
```

{% hint style="warning" %}
**Installation**: FlagEmbeddingReranker requires the `FlagEmbedding` package. Install with:

```bash
pip install "gllm-retrieval[flag_embedding]"
```
{% endhint %}

## Cohere Bedrock Reranking

The `CohereBedrockReranker` uses Cohere's reranker models hosted on AWS Bedrock:

```python
from gllm_retrieval.reranker import CohereBedrockReranker

reranker = CohereBedrockReranker(
    model_name="cohere.rerank-v3-5:0",
    region_name="us-east-1",
    fallback_to_original=True,
)

reranked = await reranker.rerank(chunks, query)
```

{% hint style="warning" %}
**Installation**: CohereBedrockReranker requires the `cohere` package. Install with:

```bash
pip install "gllm-retrieval[cohere]"
```
{% endhint %}

{% hint style="info" %}
**AWS Credentials**: Ensure your AWS credentials have Bedrock permissions. See [AWS Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/models-supported.html) for supported models.
{% endhint %}

## Jina AI Reranking

The `JinaReranker` uses [Jina AI's reranker API](https://jina.ai/reranker) for cloud-based reranking:

```python
from gllm_retrieval.reranker import JinaReranker

reranker = JinaReranker(
    model="jina-reranker-v3",
    top_n=5,
    fallback_to_original=True,
)

reranked = await reranker.rerank(chunks, query)

# Close the underlying HTTP session when done
await reranker.close()
```

## Using Rerankers in Pipelines

Rerankers integrate seamlessly with the SDK's pipeline system:

```python
from gllm_pipeline import Pipeline, step
from gllm_datastore.data_store import ChromaDataStore
from gllm_retrieval.reranker import SimilarityBasedReranker
from gllm_retrieval.retriever import VectorRetriever
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.model import OpenAIEM

em_invoker = OpenAIEMInvoker(OpenAIEM.TEXT_EMBEDDING_3_SMALL)

# Initialize Chroma data store with vector capability
data_store = ChromaDataStore(
    collection_name="documents",
).with_vector(em_invoker=em_invoker)

# Initialize the vector retriever
retriever = VectorRetriever(data_store=data_store)
pipeline = Pipeline(
    steps=[
        step(retriever, {"query": "query"}, "chunks"),
        step(reranker, {"chunks": "chunks", "query": "query"}, "reranked_chunks"),
    ]
)

result = await pipeline.run(query="What is machine learning?")
```

## API Reference

For detailed API documentation, see the [Reranker API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/reranker.html).
