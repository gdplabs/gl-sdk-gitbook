---
icon: circle-nodes
---

# Graph Retriever

## What's a Graph Retriever?

Graph Retriever is a specialized retrieval component designed to extract information from knowledge graphs and graph databases. Unlike traditional vector retrievers that rely solely on semantic similarity, Graph Retrievers leverage the structured relationships between entities in a graph to provide more contextually relevant and relationally aware results.

### Available Implementations:

- LightRAG Graph RAG Retriever
- LlamaIndex Graph RAG Retriever

## Installation

{% tabs %}
{% tab title="Linux, MacOS, or Windows WSL" %}

```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-retrieval[kg]" openai
```

{% endtab %}

{% tab title="Windows Powershell" %}

```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$((gcloud auth print-access-token))@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-retrieval[kg]"
```

{% endtab %}

{% tab title="Windows Command Prompt" %}

```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-retrieval[kg]"
```

{% endtab %}
{% endtabs %}

Before using the Graph Retriever, you should be familiar with:

- [Graph Data Store](https://gdplabs.gitbook.io/sdk/tutorials/data-store/graph-data-store): Knowledge of graph data stores and their interfaces
- [LM Invoker](https://gdplabs.gitbook.io/sdk/tutorials/inference/lm-invoker): For implementations that use LLMs for query processing
- [EM Invoker](https://gdplabs.gitbook.io/sdk/tutorials/inference/em-invoker): For implementations that use embedding models for query processing

## What it does

The Graph Retriever is a component that retrieves relevant information from a knowledge graph based on a natural language query. It provides a standardized interface for graph-based retrieval operations in Gen AI applications.

### Inputs

- Query: A text string representing the search query
- Data Store: A graph data store instance (e.g., Neo4j, LightRAG)
- Retrieval Parameters: Additional parameters for fine-tuning the search (optional)

### Outputs

The Graph Retriever can return different types of outputs based on the implementation:

- List of Chunks: Document chunks relevant to the query
- Graph Elements: Nodes (entities) and edges (relationships) from the knowledge graph
- Synthesized Response: For implementations that include response generation

## Graph Retriever Types

### LlamaIndex Graph RAG Retriever

The LlamaIndex Graph RAG Retriever leverages LlamaIndex's property graph capabilities to provide advanced graph-based retrieval with multiple retrieval strategies.

```python
import asyncio
import os
from gllm_retrieval.retriever.graph_retriever.llama_index_graph_rag_retriever import (
    LlamaIndexGraphRAGRetriever,
)
from gllm_datastore.graph_data_store.llama_index_neo4j_graph_rag_data_store import (
    LlamaIndexNeo4jGraphRAGDataStore,
)

# Using LlamaIndex LLMs
from gllm_inference.lm_invoker import build_lm_invoker
from gllm_inference.em_invoker import build_em_invoker
from gllm_datastore.graph_data_store.utils import (
    LlamaIndexLMInvokerAdapter,
    LlamaIndexEMInvokerAdapter,
)

os.environ["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>"

async def main():
    # Initialize the components
    lm_invoker = build_lm_invoker("openai/gpt-4o-mini")
    em_invoker = build_em_invoker("openai/text-embedding-3-small")

    # Initialize the graph data store
    graph_store = LlamaIndexNeo4jGraphRAGDataStore(
        url="bolt://localhost:7687",
        username="neo4j",
        password="password",
    )

    try:
        # Initialize the retriever
        retriever = LlamaIndexGraphRAGRetriever(
            data_store=graph_store,
            llama_index_llm=LlamaIndexLMInvokerAdapter(lm_invoker),
            embed_model=LlamaIndexEMInvokerAdapter(em_invoker),
        )

        results = await retriever.retrieve(
            "Who works at TechCorp?",
            retrieval_params={},
        )

        for result in results:
            print(f"Content: {result.content}")

    finally:
        # Close the graph store connection
        graph_store.close()


if __name__ == "__main__":
    asyncio.run(main())
```

### LightRAG Graph RAG Retriever

The LightRAG Graph RAG Retriever is designed to work with LightRAG data stores, providing a comprehensive retrieval solution that combines document retrieval with knowledge graph exploration.

```python
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.lm_invoker import OpenAILMInvoker

from gllm_datastore.graph_data_store.light_rag_postgres_data_store import LightRAGPostgresDataStore
from gllm_retrieval.retriever.graph_retriever.light_rag_retriever import LightRAGRetriever

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini")

data_store = LightRAGPostgresDataStore(
    lm_invoker=lm_invoker,
    em_invoker=em_invoker,
    postgres_db_host="localhost",
    postgres_db_port=5432,
    postgres_db_name="rag",
    postgres_db_user="rag",
    postgres_db_password="rag",
)
await data_store.ensure_initialized()

retriever = LightRAGRetriever(data_store=data_store)
await retriever.retrieve("Who is John Doe?")
```

#### **Advanced Usage #1: Retrieving Graph Elements**

LightRAG Retriever can return not just document chunks but also the knowledge graph elements (nodes and edges) related to the query:

```python
from gllm_retrieval.retriever.graph_retriever.constants import ReturnType

# Retrieve as dictionary with nodes and edges
result_dict = await retriever.retrieve(
    "What is the relationship between TechCorp and John Doe?",
    return_type=ReturnType.DICT
)

# Access the nodes (entities)
for node in result_dict["nodes"]:
    print(f"Entity: {node.entity}, Type: {node.type}")

# Access the edges (relationships)
for edge in result_dict["edges"]:
    print(f"Relationship: {edge.entity_source} -> {edge.description} -> {edge.entity_target}")
```

#### **Advanced Usage #2: Use LightRAG's Response Synthesizer**

LightRAG also comes with its own response synthesizer and prompts:

```python
# Retrieve as final response
response = await retriever.retrieve(
    "What is the relationship between TechCorp and John Doe?",
    only_need_context=False
)
```

###
