# PII-Aware Retriever

## What's a PII-Aware Retriever?

**PII-Aware Retriever** handles Personally Identifiable Information (PII) in queries and retrieved documents with privacy preservation. It performs query anonymization, hybrid search with entity filtering, rank fusion, and automatic de-anonymization of results—keeping PII from being exposed in search operations while retrieving accurate results.

**Best For**:

* Privacy-sensitive applications handling personal data
* Compliance-driven retrieval (GDPR, HIPAA)
* Protecting PII in search queries and results
* Hybrid search with entity-aware filtering
* Applications requiring privacy guarantees

**Key Features**:

* Query anonymization before search
* Entity extraction and PII detection
* Hybrid search combining vector and fulltext with entity filtering
* Weighted Reciprocal Rank Fusion (RRF) result merging
* Automatic de-anonymization of results
* Configurable PII resolver strategies

**Use Cases**:

* Healthcare systems retrieving patient data
* Financial applications with customer information
* Legal document search with client identifiers
* GDPR-compliant document retrieval
* Multi-tenant systems with data isolation requirements

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [Retriever](./README.md) concepts and [Data Store](../../data-store/README.md)
2. [Chunk](../../data-store/README.md) schema and metadata fields
3. Entity extraction and PII handling concepts
4. Basic understanding of query anonymization

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

The PII-Aware Retriever intercepts queries to anonymize sensitive information, performs hybrid search with entity-aware filtering, fuses results from multiple strategies, and finally de-anonymizes retrieved chunks to restore original content. This ensures privacy during the search process while maintaining retrieval accuracy.

## Basic Usage

Create a PII-aware retriever with entity-based privacy:

```python
from gllm_datastore.data_store import ElasticsearchDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker
from gllm_retrieval.retriever import PIIAwareRetriever
from gllm_retrieval.retriever.pii_resolver import MetadataPIIResolver

# Data store with vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
data_store = ElasticsearchDataStore(
    index_name="documents"
).with_vector(em_invoker=em_invoker)

# Create retriever with PII resolver
pii_resolver = MetadataPIIResolver()  # Extracts entities from metadata

retriever = PIIAwareRetriever(
    data_store=data_store,
    pii_resolver=pii_resolver,
    weights=[0.5, 0.5]  # Equal weight on vector and entity-filtered search
)

# Query with PII is automatically anonymized
results = await retriever.retrieve(
    "What are the medical records for John Doe?",
    top_k=10
)
# Results are de-anonymized before returning
```

## Weighted Hybrid Search

Configure weights for combining vector and entity-filtered search:

```python
retriever = PIIAwareRetriever(
    data_store=data_store,
    pii_resolver=pii_resolver,
    weights=[0.7, 0.3]  # 70% vector, 30% entity-filtered
)

results = await retriever.retrieve(
    "Find documents about Alice Smith",
    top_k=10,
    threshold=0.7
)
```

## Filtering and Batch Queries

Apply additional filters and handle batch queries:

```python
from gllm_datastore.core.filters import filter as F

retriever = PIIAwareRetriever(
    data_store=data_store,
    pii_resolver=pii_resolver
)

# Single query with filters
results = await retriever.retrieve(
    "Query with PII",
    query_filter=F.eq("metadata.department", "HR"),
    top_k=10
)

# Batch queries (all will be anonymized)
batch_results = await retriever.retrieve(
    ["Query 1 with PII", "Query 2 with name"],
    top_k=10
)
```

{% hint style="info" %}
**Implementation Notes**:
- Queries are anonymized before any data store access (no PII exposure in logs)
- Entity extraction is configurable via the PII resolver strategy
- Hybrid search combines vector similarity and entity-aware filtering
- Results are de-anonymized using the mapping created during anonymization
- The entities_field metadata stores extracted entities for filtering
- Batch queries process each query independently through anonymization
{% endhint %}

## Privacy Guarantees

The PII-Aware Retriever provides:

1. **Query Privacy**: PII in queries is anonymized before search operations
2. **Entity Filtering**: Metadata-based entity filtering isolates sensitive data
3. **Result Privacy**: Retrieved chunks are de-anonymized only at the final output
4. **Audit Trail**: Entity mappings can be logged separately for compliance

This design ensures that sensitive information is never exposed in intermediate search operations while still retrieving accurate results.
