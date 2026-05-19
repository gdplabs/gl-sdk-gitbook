---
icon: chart-radar
---

# Text-to-Graph

Text-to-Graph is a transformation process that converts unstructured text into structured graph representations using Large Language Models (LLMs). This process extracts entities (nodes) and their relationships (edges) from natural language text, creating knowledge graphs that can be stored, queried, and visualized.

## Available Implementations:

* **LMBasedGraphTransformer**: General-purpose knowledge graph extraction from text
* **LMBasedMindMapTransformer**: Hierarchical mind map extraction with central themes and sub-ideas

## Installation

{% tabs %}
{% tab title="Linux, MacOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-misc[json_repair]" openai
```
{% endtab %}

{% tab title="Windows Powershell " %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$((gcloud auth print-access-token))@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-misc[json_repair]"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" "gllm-misc[json_repair]"
```
{% endtab %}
{% endtabs %}

Before using the Text-to-Graph, you should be familiar with:

* [LM Invoker](https://gdplabs.gitbook.io/sdk/tutorials/inference/lm-invoker): For converting text into graphs by using generative language models

## Quick Start

Here's a simple example to extract a knowledge graph from text:

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_misc.graph_transformer import LMBasedGraphTransformer
from gllm_core.schema import Chunk

async def main():
    # 1. Initialize the LM invoker
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-4o-mini",
        api_key="<YOUR_OPENAI_API_KEY>"
    )

    # 2. Create the graph transformer
    transformer = LMBasedGraphTransformer(lm_invoker=lm_invoker)

    # 3. Extract graph from text
    text = "Marie Curie discovered radium and won the Nobel Prize twice."
    chunks = [Chunk(content=text)]
    graph_docs = await transformer.convert_to_graph_documents(chunks)

    # 4. Print results
    graph = graph_docs[0]
    print("Nodes:", [node.id for node in graph.nodes])
    print("Relationships:", [(r.source.id, r.type, r.target.id) for r in graph.relationships])

asyncio.run(main())
```

**Output:**

```
Nodes: ['Marie Curie', 'radium', 'Nobel Prize']
Relationships: [('Marie Curie', 'DISCOVERED', 'radium'), ('Marie Curie', 'WON', 'Nobel Prize')]
```

## What it does

The Text-to-Graph transformer analyzes text documents and extracts structured graph representations consisting of nodes (entities) and relationships. It uses LLMs to understand the semantic meaning of text and identify relevant entities and their connections.

### Inputs

* **Documents**: List of `Chunk` objects containing text content to transform
* **LM Invoker**: A language model invoker for entity and relationship extraction
* **Schema Constraints** (optional): Allowed node types and relationship types
* **Configuration**: Structured output mode, strict mode, and custom prompts

### Outputs

The Text-to-Graph transformer returns:

* **GraphDocument**: A structured representation containing:
  * **Nodes**: List of extracted entities with IDs, types, and properties
  * **Relationships**: List of connections between nodes with types and properties
  * **Source**: Reference to the original text chunk

#### Understanding the Output

The `GraphDocument` object contains:

```python
# Access nodes
for node in graph_doc.nodes:
    print(f"ID: {node.id}")
    print(f"Type: {node.type}")
    print(f"Properties: {node.properties}")

# Access relationships
for relationship in graph_doc.relationships:
    print(f"Source: {relationship.source.id}")
    print(f"Target: {relationship.target.id}")
    print(f"Type: {relationship.type}")
    print(f"Properties: {relationship.properties}")

# Access source document
print(f"Original text: {graph_doc.source.content}")
```

## Customizing Graph Extraction

### Constraining Node Types

You can specify which types of entities to extract by providing `allowed_nodes`:

```python
# Extract only specific entity types
transformer = LMBasedGraphTransformer(
    lm_invoker=lm_invoker,
    allowed_nodes=["Person", "Organization", "Location", "Event"],
    strict_mode=True  # Only extract specified node types
)

chunks = [Chunk(content="Elon Musk founded SpaceX in California in 2002.")]
graph_docs = await transformer.convert_to_graph_documents(chunks)

# Result will only contain Person, Organization, Location, and Event nodes
```

### Constraining Relationship Types

You can control which relationships to extract using `allowed_relationships`:

```python
# Option 1: Simple relationship type list
transformer = LMBasedGraphTransformer(
    lm_invoker=lm_invoker,
    allowed_relationships=["WORKS_AT", "FOUNDED", "LOCATED_IN", "MANAGES"]
)

# Option 2: Typed relationships (source_type, relationship, target_type)
transformer = LMBasedGraphTransformer(
    lm_invoker=lm_invoker,
    allowed_nodes=["Person", "Organization", "Location"],
    allowed_relationships=[
        ("Person", "WORKS_AT", "Organization"),
        ("Person", "FOUNDED", "Organization"),
        ("Organization", "LOCATED_IN", "Location"),
        ("Person", "MANAGES", "Person")
    ],
    strict_mode=True
)

chunks = [Chunk(content="Alice works at TechCorp, which is located in San Francisco.")]
graph_docs = await transformer.convert_to_graph_documents(chunks)
```

### Strict Mode vs. Lenient Mode

The `strict_mode` parameter controls how constraints are enforced:

```python
# Strict mode: Only extract specified types
transformer_strict = LMBasedGraphTransformer(
    lm_invoker=lm_invoker,
    allowed_nodes=["Person", "Company"],
    allowed_relationships=["WORKS_AT"],
    strict_mode=True  # Filters out any nodes/relationships not in allowed lists
)

# Lenient mode: Use constraints as guidance but allow other types
transformer_lenient = LMBasedGraphTransformer(
    lm_invoker=lm_invoker,
    allowed_nodes=["Person", "Company"],
    allowed_relationships=["WORKS_AT"],
    strict_mode=False  # May extract additional types beyond the allowed lists
)
```

## Mind Map Extraction

The `LMBasedMindMapTransformer` extends the basic graph transformer to create hierarchical mind map structures. It organizes information into central themes, main ideas, and sub-ideas.

### What's a Mind Map?

A mind map is a hierarchical graph structure that represents information radiating from a central concept. Unlike general knowledge graphs, mind maps:

* Have a **single** root node (Central Theme)
* Follow a strict **hierarchical** structure
* Organize information by levels of detail
* Form a **connected tree structure**

### Basic Mind Map Extraction

```python
import asyncio
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_misc.graph_transformer import LMBasedMindMapTransformer
from gllm_core.schema import Chunk

async def extract_mind_map():
    # Initialize the LM invoker
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-4o-mini",
        api_key="<YOUR_OPENAI_API_KEY>"
    )

    # Create the mind map transformer
    transformer = LMBasedMindMapTransformer(lm_invoker=lm_invoker)

    # Prepare text
    text = """
    Artificial Intelligence is transforming industries through machine learning
    and deep learning. Machine learning includes supervised learning techniques
    like classification and regression, as well as unsupervised learning methods
    like clustering. Deep learning uses neural networks with multiple layers to
    process complex patterns in data.
    """
    chunks = [Chunk(content=text)]

    # Extract mind map
    mind_map_docs = await transformer.convert_to_graph_documents(chunks)

    # Access the mind map structure
    mind_map = mind_map_docs[0]

    print("Mind Map Structure:")
    for node in mind_map.nodes:
        print(f"  [{node.type}] {node.id}")

    print("\nHierarchical Relationships:")
    for rel in mind_map.relationships:
        print(f"  {rel.source.id} --[{rel.type}]--> {rel.target.id}")

    return mind_map_docs

# Run the extraction
asyncio.run(extract_mind_map())
```

### Mind Map Node Types

The mind map transformer uses three default node types:

* **CentralTheme**: The root node representing the main topic (exactly one per mind map)
* **MainIdea**: Primary branches from the central theme (2-5 recommended)
* **SubIdea**: Supporting details branching from main ideas or other sub-ideas

### Mind Map Relationship Types

The mind map uses hierarchical relationships:

* **HAS\_MAIN\_IDEA**: Connects CentralTheme to MainIdea nodes
* **HAS\_SUB\_IDEA**: Connects MainIdea to SubIdea, or SubIdea to SubIdea (for deeper levels)

## End-to-End: From Text to Indexed Graph

In most real applications, extracting a `GraphDocument` is only half of the job — you also want the result to be **persisted into a graph database** so it can be queried, traversed, and reused later. By chaining a Text-to-Graph transformer with a [Graph Data Store](https://gdplabs.gitbook.io/sdk/tutorials/knowledge-graph/graph-data-store), you can build a pipeline whose **input is raw text** and whose **output is an indexed knowledge graph** ready to query.

The integration relies on a simple mapping between the two APIs:

| `GraphDocument` field                               | Graph Data Store API                                                                    |
| --------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `node.type`                                         | `label` in `upsert_node`                                                                |
| `node.id`                                           | `identifier_value` in `upsert_node` (paired with a fixed `identifier_key`, e.g. `"id"`) |
| `node.properties`                                   | `properties` in `upsert_node`                                                           |
| `relationship.source.id` / `relationship.target.id` | `node_source_value` / `node_target_value` in `upsert_relationship`                      |
| `relationship.type`                                 | `relation` in `upsert_relationship`                                                     |
| `relationship.properties`                           | `properties` in `upsert_relationship`                                                   |

{% hint style="info" %}
The example below uses Neo4j as the backing store. The same pattern works for any implementation that exposes `upsert_node` / `upsert_relationship` (e.g., `NebulaGraphDataStore`). To run Neo4j locally:

```bash
docker run -d --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5
```
{% endhint %}

#### Pipeline Example

```python
import asyncio
from gllm_core.schema import Chunk
from gllm_datastore.graph_data_store import Neo4jGraphDataStore
from gllm_inference.lm_invoker import OpenAILMInvoker
from gllm_misc.graph_transformer import LMBasedGraphTransformer
from gllm_misc.graph_transformer.schema import GraphDocument


async def index_graph_document(
    graph_store: Neo4jGraphDataStore,
    graph_doc: GraphDocument,
) -> None:
    """Persist a GraphDocument into a graph data store."""
    # 1. Upsert all nodes first so relationships have valid endpoints.
    for node in graph_doc.nodes:
        await graph_store.upsert_node(
            label=node.type,
            identifier_key="id",
            identifier_value=node.id,
            properties=node.properties,
        )

    # 2. Upsert relationships, referencing nodes by the same identifier key.
    for rel in graph_doc.relationships:
        await graph_store.upsert_relationship(
            node_source_key="id",
            node_source_value=rel.source.id,
            relation=rel.type,
            node_target_key="id",
            node_target_value=rel.target.id,
            properties=rel.properties,
        )


async def main():
    # 1. Initialize the LM invoker and the transformer.
    lm_invoker = OpenAILMInvoker(
        model_name="gpt-5.4-nano",
        api_key="<YOUR_OPENAI_API_KEY>",
    )
    transformer = LMBasedGraphTransformer(
        lm_invoker=lm_invoker,
        allowed_nodes=["Person", "Organization", "Location"],
        allowed_relationships=[
            ("Person", "FOUNDED", "Organization"),
            ("Organization", "LOCATED_IN", "Location"),
        ],
        strict_mode=True,
    )

    # 2. Initialize the graph data store.
    graph_store = Neo4jGraphDataStore(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password",
    )

    # 3. Text in -> GraphDocument out.
    chunks = [
        Chunk(content="Elon Musk founded SpaceX in California in 2002."),
        Chunk(content="Larry Page co-founded Google, which is headquartered in Mountain View."),
    ]
    graph_docs = await transformer.convert_to_graph_documents(chunks)

    # 4. GraphDocument in -> indexed graph in Neo4j.
    for graph_doc in graph_docs:
        await index_graph_document(graph_store, graph_doc)

    # 5. Verify by querying the indexed graph.
    results = await graph_store.query(
        """
        MATCH (p:Person)-[:FOUNDED]->(o:Organization)-[:LOCATED_IN]->(l:Location)
        RETURN p.id AS founder, o.id AS organization, l.id AS location
        """
    )
    print("Indexed graph:", results)


asyncio.run(main())
```

**Output:**

```
Indexed graph: [
    {'founder': 'Elon Musk', 'organization': 'Spacex', 'location': 'California'},
    {'founder': 'Larry Page', 'organization': 'Google', 'location': 'Mountain View'},
]
```

{% hint style="info" %}
**Why is `SpaceX` returned as `Spacex`?** `LMBasedGraphTransformer` runs `str.title()` on every `node.id` before returning the `GraphDocument`. `str.title()` capitalizes the first letter of each word and lowercases the rest, so CamelCase / brand-style names are flattened: `"SpaceX" → "Spacex"`, `"iPhone" → "Iphone"`, `"OpenAI" → "Openai"`. Standard names like `"Elon Musk"` or `"Mountain View"` are unaffected because they are already in title case. This is normalization done by the SDK, not by the LLM — keep it in mind when querying or comparing IDs downstream.
{% endhint %}

#### Practical Notes

* **Upsert order matters.** Always upsert nodes before relationships — `upsert_relationship` expects both endpoints to already exist in the store.
* **Pick a stable identifier key.** Using `"id"` as the `identifier_key` (paired with `node.id` from the `GraphDocument`) makes the same entity converge across re-runs. Re-extracting the same text will update the existing node instead of creating duplicates.
