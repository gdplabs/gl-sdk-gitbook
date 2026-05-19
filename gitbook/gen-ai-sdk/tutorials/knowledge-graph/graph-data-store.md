---
icon: circle-nodes
---

# Graph Data Store

## What's a Graph Data Store?

Graph data stores are specialized databases designed to store and query data in the form of nodes (entities) and edges (relationships). They are essential for applications that need to model and analyze complex relationships between data points. Graph data stores are particularly useful for:

* Knowledge graphs and semantic networks
* Social network analysis and recommendation systems
* Fraud detection and pattern recognition
* Complex relationship modeling and traversal
* Hierarchical data representation

### Available Implementations:

* Neo4j Graph Data Store
* Nebula Graph Data Store
* LlamaIndex Neo4j Graph RAG Data Store
* LightRAG Postgres Graph RAG Data Store

## Installation

{% tabs %}
{% tab title="Linux, MacOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-datastore[kg]"
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$((gcloud auth print-access-token))@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-datastore[kg]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-datastore[kg]"
```
{% endtab %}
{% endtabs %}

## Managing Graph Data with Graph Data Store

{% hint style="info" %}
If you want to try out the following code snippets, you can run a Neo4j server locally with [Docker](https://www.docker.com/).

```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5
```
{% endhint %}

The Graph Data Store provides comprehensive operations for managing graph data. Here's how to use the core operations effectively:

```python
import asyncio
from gllm_datastore.graph_data_store import Neo4jGraphDataStore

async def main():
    # 1) Initialize graph store
    graph_store = Neo4jGraphDataStore(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password",
    )

    # 2) Create nodes
    await graph_store.upsert_node(
        label="Person",
        identifier_key="name",
        identifier_value="John Doe",
        properties={"age": 30, "occupation": "Engineer"},
    )

    await graph_store.upsert_node(
        label="Company",
        identifier_key="name",
        identifier_value="TechCorp",
        properties={"industry": "Technology", "founded": 2010},
    )

    # 3) Create relationship
    await graph_store.upsert_relationship(
        node_source_key="name",
        node_source_value="John Doe",
        relation="WORKS_AT",
        node_target_key="name",
        node_target_value="TechCorp",
        properties={"since": "2018-05-20", "position": "Senior Engineer"},
    )

    # 4) Query to view the output
    query = """
        MATCH (p:Person)-[r:WORKS_AT]->(c:Company)
        RETURN p.name AS person_name, r.position AS position, c.name AS company_name
    """
    results = await graph_store.query(query)

    # 5) Print results
    print("Query results:", results)

if __name__ == "__main__":
    asyncio.run(main())
```

### Node Operations

#### Creating and Updating Nodes

The `upsert_node` method creates a new node if it doesn't exist, or updates an existing node if it does. This is useful for maintaining data consistency.

```python
# Create or update a node
await graph_store.upsert_node(
    label="Person",              # Node label/type
    identifier_key="email",     # Property used as unique identifier
    identifier_value="john@example.com",  # Value of the identifier
    properties={                # Additional properties
        "name": "John Smith",
        "age": 35,
        "skills": ["Python", "Data Science"]
    }
)
```

#### Deleting Nodes

The `delete_node` method removes a node from the graph. Note that in most graph databases, this will also delete all relationships connected to this node.

```python
# Delete a node
await graph_store.delete_node(
    label="Person",
    identifier_key="email",
    identifier_value="john@example.com"
)
```

### Relationship Operations

#### **Creating and Updating Relationships**

The `upsert_relationship` method creates or updates a relationship between two existing nodes.

```python
# Create or update a relationship
await graph_store.upsert_relationship(
    node_source_key="email",
    node_source_value="alice@example.com",
    relation="MANAGES",
    node_target_key="email",
    node_target_value="bob@example.com",
    properties={"since": "2022-01-15", "department": "Engineering"}
)
```

#### **Deleting Relationships**

The `delete_relationship` method removes a specific relationship between two nodes.

```python
# Delete a relationship
await graph_store.delete_relationship(
    node_source_key="email",
    node_source_value="alice@example.com",
    relation="MANAGES",
    node_target_key="email",
    node_target_value="bob@example.com"
)
```

### Querying the Graph

The `query` method allows you to execute native graph query language statements (e.g., Cypher for Neo4j) to retrieve data from the graph.

```python
# Execute a Cypher query (Neo4j)
results = await graph_store.query(
    query="MATCH (p:Person)-[r:WORKS_AT]->(c:Company) WHERE c.industry = $industry RETURN p.name, r.position, c.name",
    parameters={"industry": "Technology"}
)

# Process results
for record in results:
    print(f"{record['p.name']} works as {record['r.position']} at {record['c.name']}")
```

### Graph Traversal

The `traverse_graph` method explores the graph starting from a node that matches a property filter, then follows **all** connected relationships (direction-agnostic) up to a configurable depth. It returns a structured `(nodes, relationships)` tuple — no need to hand-write Cypher/nGQL.

**Parameters**

| Parameter                           | Type                | Description                                                                                                                                                                                                                                                                                                                                 | Example                                                                                                                                                        |
| ----------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `node_properties`                   | `dict[str, Any]`    | Properties used to find the starting node(s). All key/value pairs are AND-ed, so the more keys you pass, the narrower the match. Must not be empty — passing `{}` raises `ValueError`. If no node matches, the method returns `([], [])`.                                                                                                   | `{"name": "John Doe"}` matches any node where `name == "John Doe"`. `{"name": "John Doe", "occupation": "Engineer"}` only matches nodes that satisfy **both**. |
| `extracted_node_properties`         | `list[str] \| None` | Whitelist of node property keys to keep in the returned `nodes`. Use this to keep payloads small and avoid pulling heavy fields (e.g., embeddings, long text). Pass `None` or `[]` to return **all** node properties. A whitelisted key that doesn't exist on a given node appears in the result with value `None` (it is **not** omitted). | `["name", "age"]` returns exactly those two keys for every node, with `None` if the node lacks one. `None` returns every property each node has.               |
| `extracted_relationship_properties` | `list[str] \| None` | Whitelist of relationship property keys to keep in the returned `relationships`. Same semantics as `extracted_node_properties`: missing keys come back as `None`. Pass `None` or `[]` to return **all** relationship properties.                                                                                                            | `["since"]` keeps only `since` (with `None` if the edge lacks it). `None` returns every property each edge has.                                                |
| `depth`                             | `int`               | Maximum number of hops to traverse from the starting node. Must be ≥ 1 — `0` or negative raises `ValueError`. Defaults to `3`. Keep it small (1–2) on dense graphs because reachable nodes can grow exponentially with depth.                                                                                                               | `depth=1` returns only direct neighbors. `depth=2` adds neighbors-of-neighbors.                                                                                |

Traversal is **direction-agnostic** — both incoming and outgoing edges are followed. Returned nodes and relationships are deduplicated by their internal IDs, so each entity appears at most once even if it's reachable through multiple paths.

**Basic Example**

Assume the graph already contains John Doe (`Person`) `WORKS_AT` TechCorp (`Company`), and TechCorp `LOCATED_IN` Jakarta (`City`).

```python
nodes, relationships = await graph_store.traverse_graph(
    node_properties={"name": "John Doe"},
    extracted_node_properties=["name", "age", "occupation"],
    extracted_relationship_properties=["since", "position"],
    depth=2,
)
```

**Example Output**

```python
# Each node: id, labels, properties (only the extracted keys; missing ones become None).
nodes = [
    {
        "id": 8157,
        "labels": ["Person"],
        "properties": {"name": "John Doe", "age": 30, "occupation": "Engineer"},
    },
    {
        "id": 8158,
        "labels": ["Company"],
        # `industry` and `founded` are dropped (not in extracted_node_properties).
        # `age` and `occupation` are kept as None (Company has no such properties).
        "properties": {"name": "TechCorp", "age": None, "occupation": None},
    },
    {
        "id": 8159,
        "labels": ["City"],
        "properties": {"name": "Jakarta", "age": None, "occupation": None},
    },
]

# Each rel: id, type, start_node, end_node, properties.
relationships = [
    {
        "id": 15843,
        "type": "WORKS_AT",
        "start_node": 8157,
        "end_node": 8158,
        "properties": {"since": "2018-05-20", "position": "Senior Engineer"},
    },
    {
        "id": 1571,
        "type": "LOCATED_IN",
        "start_node": 8158,
        "end_node": 8159,
        # `position` is None — LOCATED_IN doesn't have that property.
        "properties": {"since": "2010-01-01", "position": None},
    },
]
```

Node and relationship IDs are Neo4j-internal and will differ from run to run.

## Graph RAG Data Store

The Graph RAG (Retrieval-Augmented Generation) Data Store extends the basic graph data store with capabilities specifically designed for AI applications. It allows you to query the graph using natural language and integrate with LLM workflows. It also helps to link graph components with documents, allowing for a synchronized data between Vector DB and Graph DB.

### LlamaIndex Neo4j Graph RAG Data Store

You can instantiate a LlamaIndex Neo4j Graph RAG Data Store which can then be used for retrieval (see [LlamaIndex Graph RAG Retriever](https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever/graph-retriever#llamaindex-graph-rag-retriever)).

```python
from gllm_datastore.graph_data_store import LlamaIndexNeo4jGraphRAGDataStore

# Initialize the Graph RAG store
graph_rag_store = LlamaIndexNeo4jGraphRAGDataStore(
    url="bolt://localhost:7687",
    username="neo4j",
    password="password",
)
```

### LightRAG Postgres Graph RAG Data Store

The LightRAG Data Store provides a PostgreSQL-backed implementation for graph-based RAG with automatic knowledge graph construction and natural language querying capabilities.

{% hint style="info" %}
If you want to try out the following code snippets, you can run a Neo4j server locally with [Docker](https://www.docker.com/).

```bash
docker run -p 5432:5432 -d --name postgres-rag gzdaniel/postgres-for-rag:16.6 sh -c "service postgresql start && sleep infinity"
```
{% endhint %}

```python
import asyncio
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_core.schema import Chunk
from gllm_datastore.graph_data_store.light_rag_postgres_data_store import LightRAGPostgresDataStore

# Initialize the invokers
os.environ["OPENAI_API_KEY"] = "<YOUR_OPENAI_API_KEY>"
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
lm_invoker = OpenAILMInvoker(model_name="gpt-4o-mini")

async def main():
    # Initialize the LightRAG data store
    data_store = LightRAGPostgresDataStore(
        lm_invoker=lm_invoker,
        em_invoker=em_invoker,
        postgres_db_host="localhost",
        postgres_db_port=5432,
        postgres_db_name="rag",
        postgres_db_user="rag",
        postgres_db_password="rag",
    )


    # Ensure the data store is initialized
    await data_store.ensure_initialized()

    # Insert chunks - LightRAG automatically builds the knowledge graph
    await data_store.insert(
        chunks=[
            Chunk(content="Joko Widodo is the 7th President of Indonesia.", id="joko_widodo"),
            Chunk(content="Prabowo Subianto is the 8th President of Indonesia.", id="prabowo_subianto"),
        ],
    )

    # Query using natural language
    print("Performing query 'Who is Prabowo Subianto?':")
    print(await data_store.query("Who is Prabowo Subianto?"))

    # Delete specific chunks
    await data_store.delete("joko_widodo")
    await data_store.delete("prabowo_subianto")

# Run the async function
asyncio.run(main())
```
