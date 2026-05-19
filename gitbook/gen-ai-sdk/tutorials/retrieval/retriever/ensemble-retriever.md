# Ensemble Retriever

## What's an Ensemble Retriever?

**Ensemble Retriever** combines multiple retrievers and merges their results using weighted Reciprocal Rank Fusion (RRF). This enables hybrid retrieval by fusing rankings from different retrieval strategies (e.g., vector search and keyword search) into a unified ranked result set.

**Best For**:

* Hybrid retrieval combining semantic and lexical signals
* Combining different retriever types (vector + fulltext)
* Weighted fusion of multiple ranking strategies
* Improving result diversity and coverage

**Key Features**:

* Weighted Reciprocal Rank Fusion (RRF) for result merging
* Support for 2+ retrievers
* Configurable weights for each retriever
* Tunable rank constant and minimum candidate settings
* Single-query or batch-query retrieval

**Use Cases**:

* Hybrid search (semantic + keyword)
* Multi-strategy search combining different data stores
* Ensemble methods for improved search quality
* Combining specialized retrievers for specific domains

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Retriever](./README.md) concepts and types
2. At least two retriever implementations (e.g., Vector Retriever and Fulltext Retriever)
3. Basic understanding of ranking and fusion algorithms

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

The Ensemble Retriever takes a list of base retrievers and executes them in parallel, then fuses their results using weighted Reciprocal Rank Fusion. This combines the strengths of different retrieval strategies into a single ranked output.

## Usage

Combine two or more retrievers with weights:

```python
from gllm_retrieval.retriever import VectorRetriever, FulltextRetriever, EnsembleRetriever

# Create base retrievers
vector_retriever = VectorRetriever(data_store=vector_datastore)
fulltext_retriever = FulltextRetriever(data_store=fulltext_datastore)

# Create ensemble with weighted fusion
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, fulltext_retriever],
    weights=[0.7, 0.3]  # 70% weight on vector, 30% on fulltext
)

# Single query
results = await ensemble_retriever.retrieve(
    "What is machine learning?",
    top_k=10
)

# Batch queries
batch_results = await ensemble_retriever.retrieve(
    ["query 1", "query 2"],
    top_k=10
)
```

## Configuring Weights and Fusion

Adjust the balance between retrievers using weights and tuning parameters:

```python
ensemble_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, fulltext_retriever],
    weights=[0.6, 0.4],          # Custom weights (auto-normalized)
    rank_constant=60,            # Controls balance between high and low-ranked items
    min_candidate=2              # Minimum results per retriever before fusion
)

results = await ensemble_retriever.retrieve(
    "query",
    top_k=10,
    threshold=0.7
)
```

{% hint style="info" %}
**Implementation Notes**:
- Weights are automatically normalized if they don't sum to 1.0
- `rank_constant` (default 60) is added to ranks in RRF, controlling the importance of position
- `min_candidate` ensures each retriever contributes at least a minimum number of candidates
- Threshold filtering is applied after fusion
{% endhint %}
