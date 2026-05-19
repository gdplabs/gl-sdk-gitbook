---
icon: arrows-rotate
---

# Retrieval

Language models (LMs) are powerful, but they inherently have limited context windows, imperfect factual recall, and no direct access to your private or frequently changing data.

_**Retrieval**_ is the process of fetching relevant information from external knowledge sources so an LM can ground its answers—without retraining the model.

In a Retrieval-Augmented Generation (RAG) pipeline, your query may be transformed, used to retrieve candidate documents or chunks (for example, from vector, SQL, or graph stores), and then the most relevant results are passed to the LM. This improves factual accuracy, enables citations, and reduces hallucinations.

Our Retrieval components allow you to:

1. Perform basic retrieval via specialized retrievers for SQL, Vector, and Graph databases.
2. Tune the retrieval process by inferring parameters from the query.
3. Enhance results by manipulating the queries.
4. Improve retrieved context quality by merging or deduplicating retrieved chunks.
5. Upgrade the context relevance by reranking retrieved chunks.<br>
