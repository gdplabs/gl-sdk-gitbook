# Graph RAG

**Graph RAG Indexer** is a component designed for **constructing knowledge graphs** from document chunks and indexing them into graph databases for advanced Retrieval-Augmented Generation (RAG) applications.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-docproc[kg]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[kg]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-docproc[kg]"
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [structuredelementchunker-output.json](https://assets.analytics.glair.ai/generative/pdf/structuredelementchunker-output.json).

## LightRAG Graph RAG Indexer

**LightRAGGraphRAGIndexer** is a lightweight implementation that uses the LightRAG library to create knowledge graphs. It automatically **extracts entities and relationships from text, stores them in a graph database**, and maintains mappings between source files and their chunks.

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json

from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_docproc.indexer.graph.light_rag_graph_rag_indexer import LightRAGGraphRAGIndexer
from gllm_datastore.graph_data_store.light_rag_postgres_data_store import LightRAGPostgresDataStore

# Read elements from JSON file
file_path = "./structuredelementchunker-output.json"

with open(file_path, "r", encoding="utf-8") as f:
    elements = json.load(f)

# Initialize LM and Embedding invokers
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini")
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")

# Create the LightRAG PostgreSQL data store
graph_store = LightRAGPostgresDataStore(
    lm_invoker=lm_invoker,
    em_invoker=em_invoker,
    postgres_db_host="localhost",
    postgres_db_port=5455,
    postgres_db_user="rag",
    postgres_db_password="rag",
    postgres_db_name="rag",
    postgres_db_workspace="default",
)

indexer = LightRAGGraphRAGIndexer(graph_store=graph_store)
indexer.index(elements, file_id="file_001")

```
{% endcode %}
{% endstep %}

{% step %}
Run the script:

```bash
export OPENAI_API_KEY=<OPENAI_API_KEY>
python main.py
```
{% endstep %}
{% endstepper %}

## LlamaIndex Graph RAG Indexer

**LlamaIndexGraphRAGIndexer** is a comprehensive implementation using LlamaIndex's PropertyGraphIndex. It provides advanced knowledge graph construction with customizable entity extractors, vector embeddings for nodes, and support for multiple graph database backends.<br>

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json

from gllm_docproc.indexer.graph.llama_index_graph_rag_indexer import LlamaIndexGraphRAGIndexer
from gllm_datastore.graph_data_store.llama_index_neo4j_graph_rag_data_store import (
    LlamaIndexNeo4jGraphRAGDataStore,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

# Read elements from JSON file
file_path = "./structuredelementchunker-output.json"

with open(file_path, "r", encoding="utf-8") as f:
    elements = json.load(f)

# Initialize LlamaIndex LLM and Embedding models
llm = OpenAI(model="gpt-4o-mini", temperature=0)
embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# Create Neo4j graph store
graph_store = LlamaIndexNeo4jGraphRAGDataStore(
    username="<NEO4J_USERNAME>",
    password="<NEO4J_PASSWORD>",
    url="<NEO4J_URL>",
)

# Create the indexer with default extractors
indexer = LlamaIndexGraphRAGIndexer(
    graph_store=graph_store,
    llama_index_llm=llm,
    embed_model=embed_model,
)

# Index the elements with document metadata
indexer.index(elements, file_id="file_001")

```
{% endcode %}
{% endstep %}

{% step %}
Run the script:

```bash
export OPENAI_API_KEY=<OPENAI_API_KEY>
python main.py
```
{% endstep %}
{% endstepper %}
