---
icon: inbox-out
---

# Retriever

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/retriever) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [.](./ "mention") | **Use Case:** [#create-the-retriever](../../../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#create-the-retriever "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/retriever.html)

### What is a Retriever?

A **Retriever** is a fundamental component in Gen AI applications that is responsible for finding and retrieving relevant information from various data sources based on user queries.

#### How Retrievers Work:

1. **Query Input**: Receives a user query (text, structured query, or natural language)
2. **Query Processing**: Transforms the query into a format suitable for the target data source
3. **Data Retrieval**: Searches the connected data store(s) for relevant information
4. **Output**: Returns structured results (typically as `Chunk` objects) with metadata

### What You Can Do with a Retriever

GL SDK provides several retriever types, each designed for specific use cases and data storage requirements:

1. [Vector Retriever](vector-retriever.md): For semantic search over vector embeddings.
2. [Fulltext Retriever](fulltext-retriever.md): For keyword and fulltext search over a data store with fulltext capability.
3. [Hybrid Retriever](hybrid-retriever.md): For combining fulltext and vector search using native data store hybrid capability.
4. [Ensemble Retriever](ensemble-retriever.md): For fusing results from multiple retrievers using weighted Reciprocal Rank Fusion.
5. [Hierarchical Retriever](hierarchical-retriever.md): For N-level coarse-to-fine retrieval across document hierarchies.
6. [Parent Document Retriever](parent-document-retriever.md): For fine-grained search returning parent chunks based on child similarity.
7. [PII-Aware Retriever](pii-aware-retriever.md): For privacy-preserving retrieval with query anonymization and entity filtering.
8. [Smart Search Web Retriever](smart-search-retriever.md): For real-time web search integration via SmartSearch SDK.
9. [Legacy](legacy/): [Vector Retriever (Legacy)](legacy/vector-retriever.md) and [SQL Retriever](legacy/sql-retriever.md).
10. [Graph Retriever](../../knowledge-graph/graph-retriever.md): For traversing and querying graph-structured knowledge.

GL SDK makes it easy to perform common data operations regardless of which retriever type you choose. One of the most powerful features of the GL SDK is its unified approach to data storage. All datastores support storing data in a structured format using the `Chunk` schema.

Think of chunks as standardized containers for your data - they provide a consistent way to represent information across different storage types, making it easy to switch between datastores or combine them in your application.

```python
from gllm_core.schema import Chunk

# Create chunks with structured content
chunks = [
    Chunk(content="AI is the future of technology."),
    Chunk(content="Machine learning enables pattern recognition."),
    Chunk(content="Deep learning powers modern AI applications.")
]
```
