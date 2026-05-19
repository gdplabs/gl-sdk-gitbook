# Hierarchical Retriever

## What's a Hierarchical Retriever?

**Hierarchical Retriever** performs N-level coarse-to-fine retrieval across multiple levels (e.g., corpus → document → chunk). Each level refines results from the previous level, enabling progressive filtering and ranking based on multiple retrieval stages.

**Best For**:

- Multi-level document hierarchies (corpus, document, section, chunk)
- Progressive coarse-to-fine filtering
- Combining different retrieval granularities
- Hierarchical knowledge structures
- Reducing search scope at each level

**Key Features**:

- N-level configurable retrieval pipeline
- Level-specific constraints and filtering
- Independent retriever per level
- Configurable constraint modes (all levels or previous only)
- Score threshold filtering per level
- Flexible output level selection

**Use Cases**:

- Document hierarchies: corpus → doc → section → chunk
- Progressive refinement: broad search → narrow scope → final ranking
- Multi-granularity search combining document and chunk retrieval
- Hierarchical knowledge graphs or organizational structures

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Retriever](./README.md) concepts and [Chunk](../../data-store/README.md) schema
2. [Query Filters](../../data-store/query-filter.md) and metadata filtering
3. Multiple retriever types that will be used at each level

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

## What it does

The Hierarchical Retriever executes a sequence of retrieval levels in order. Each level can optionally constrain its search based on results from previous levels, enabling progressive refinement of the search space.

## Basic Usage

Set up a two-level hierarchy (document → chunk):

```python
from gllm_retrieval.retriever import VectorRetriever
from gllm_retrieval.retriever.hierarchical_retriever import (
    HierarchicalRetriever,
    HierarchicalRetrieverConfig,
    LevelConfig,
    ConstraintMode
)

# Create retrievers for each level
document_retriever = VectorRetriever(data_store=document_store)
chunk_retriever = VectorRetriever(data_store=chunk_store)

# Configure the hierarchy
config = HierarchicalRetrieverConfig(
    levels=[
        LevelConfig(
            name="document",
            retriever=document_retriever,
            top_k=5,
            filter_key="document_id",
            constrain_by=None  # First level has no constraint
        ),
        LevelConfig(
            name="chunk",
            retriever=chunk_retriever,
            top_k=10,
            filter_key="document_id",
            constrain_by=ConstraintMode.PREVIOUS  # Filter by document IDs from previous level
        )
    ],
    output_level="chunk"  # Output from the chunk level
)

retriever = HierarchicalRetriever(config=config)

# Retrieve with progressive refinement
results = await retriever.retrieve("What is machine learning?")
```

## Multi-Level Hierarchies

For deeper hierarchies with more levels:

```python
config = HierarchicalRetrieverConfig(
    levels=[
        LevelConfig(
            name="corpus",
            retriever=corpus_retriever,
            top_k=3,
            filter_key="corpus_id",
            constrain_by=None
        ),
        LevelConfig(
            name="document",
            retriever=document_retriever,
            top_k=5,
            filter_key="corpus_id",
            constrain_by=ConstraintMode.PREVIOUS
        ),
        LevelConfig(
            name="section",
            retriever=section_retriever,
            top_k=8,
            filter_key="document_id",
            constrain_by=ConstraintMode.PREVIOUS
        ),
        LevelConfig(
            name="chunk",
            retriever=chunk_retriever,
            top_k=10,
            filter_key="section_id",
            constrain_by=ConstraintMode.PREVIOUS
        )
    ],
    output_level="chunk",
    final_top_k=10  # Cap final results
)

retriever = HierarchicalRetriever(config=config)
results = await retriever.retrieve("query", top_k=10)
```

## Constraint Modes

Control how each level filters by previous results:

```python
# ConstraintMode.PREVIOUS: Use only IDs from the immediately previous level
LevelConfig(name="chunk", ..., constrain_by=ConstraintMode.PREVIOUS)

# ConstraintMode.ALL: Use IDs from ALL previous levels (logical AND)
LevelConfig(name="chunk", ..., constrain_by=ConstraintMode.ALL)

# None: No constraint (independent search at this level)
LevelConfig(name="document", ..., constrain_by=None)
```

{% hint style="info" %}
**Implementation Notes**:

- Each level's `filter_key` specifies the metadata field for constraint filtering
- `score_threshold` can be set per level to filter low-scoring results
- `output_level` defaults to the last level if not specified
- `final_top_k` caps the final output; if None, all results from output_level are returned
- Hierarchical retrieval is ideal when your data has natural multi-level organization
  {% endhint %}
