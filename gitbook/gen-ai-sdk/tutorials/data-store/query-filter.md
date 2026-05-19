---
icon: filter
---

# Query Filter

## Query Filter at a Glance

Query Filter is a tiny DSL that describes **what** you want to retrieve, update, or delete no matter which datastore sits underneath. The API is shared across data stores, so you write the filter once and the implementation translates it for you.

Why we lean on it:

* **Portability**: One filter expression works for `InMemory`, `Chroma`, `Elasticsearch`, and any future capability implementations.
* **Abstraction**: Filters describe intent while each datastore handles its own translation, so you stay focused on the problem instead of backend quirks.
* **User friendly**: The helper DSL mirrors natural language conditions, which makes docs, demos, and code reviews easier to follow.
* **Hidden complexity**: Provider-specific query syntax lives behind the capability layer, so swapping datastores or capabilities does not require rewriting filters.

{% hint style="success" %}
**With QueryFilter, every datastore implementation speaks the same query language!**
{% endhint %}

## WARNING: Encrypted Fields

{% hint style="danger" %}
**DO NOT use encrypted fields for filtering or sorting.**

If you have enabled **Encryption** on your data store, filtering (`F.eq`, `F.lt`, etc.) or sorting (`order_by`) on encrypted fields will fail or yield incorrect results. The database stores randomized ciphertext, so your plaintext query values will never match.

**ALWAYS use plaintext fields (like `id`, `status`, or non-sensitive metadata) for filtering and sorting.**
{% endhint %}

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [prerequisites.md](../../prerequisites.md "mention") page.

</details>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ "gllm-datastore"
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/"  gllm-datastore
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
**QueryFilter is available in gllm\_datastore >=v0.5.32.**
{% endhint %}

## Usage Examples

These snippets spotlight the most common ways to use Query Filters.

### Quick lookups (single clause)

Start with the simplest possible case: pass a lone `FilterClause` to grab an exact match.

```python
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_datastore.core.filters import filter as F
from gllm_inference.em_invoker import OpenAIEMInvoker

em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
store = (
    ChromaDataStore(
        collection_name="customer-notes",
        client_type=ChromaClientType.MEMORY,
    )
    .with_fulltext()
    .with_vector(em_invoker=em_invoker)
)

chunks = [
    Chunk(id="book:1", content="AI is useful for programming", metadata={"topic": "AI", "category": "published"}),
    Chunk(id="book:2", content="Cheesecake is delicious", metadata={"topic": "food", "category": "published"}),
    Chunk(id="book:3", content="Sushi is delicious", metadata={"topic": "food", "category": "unpublished"}),
]
await store.fulltext.create(chunks)

# Query via metadata filter (Ensure "topic" is NOT encrypted)
results = await store.fulltext.retrieve(filters=F.eq("metadata.topic", "food"))
```

### Combining conditions (flat AND)

Stack multiple clauses with `F.and_` when you need every rule to hold true.

```python
from gllm_datastore.core.filters import QueryOptions

published_contents = F.and_(
    F.eq("metadata.category", "AI"),
    F.eq("metadata.status", "published"),
)

results = await store.vector.retrieve(
    query="AI for everyone",
    filters=published_contents,
    options=QueryOptions(limit=5),
)
```

### Nested logic (AND + OR + NOT)

When business logic gets tricky, nest `and_`, `or_`, and `not_` to mirror the requirement exactly.

```python
tech_or_research = F.and_(
    F.or_(
        F.eq("metadata.topic", "AI"),
        F.eq("metadata.topic", "food"),
    ),
    F.not_(F.eq("metadata.category", "published")),
)

await store.fulltext.delete(filters=tech_or_research)
```

### Reusable filter snippets

Extract frequently used clauses into variables so you can compose them on the fly.

```python
is_customer_owned = F.eq("metadata.owner_type", "customer")

async def get_customer_docs(owner_id: str):
    filters = F.and_(is_customer_owned, F.eq("metadata.owner_id", owner_id))
    return await store.fulltext.retrieve(filters=filters, options=QueryOptions(limit=20))
```

### Building filters from dictionaries

Use `QueryFilter.from_dicts()` when your filter rules already arrive as plain dictionaries, such as from config files, request payloads, or UI builders.

```python
from gllm_datastore.core.filters import FilterCondition, QueryFilter

filters = QueryFilter.from_dicts(
    [
        {"key": "metadata.topic", "value": "AI", "operator": "=="},
        {"key": "metadata.status", "value": "published", "operator": "=="},
    ],
    condition=FilterCondition.AND,
)

results = await store.fulltext.retrieve(filters=filters)
```

Each dictionary is validated into a `FilterClause`, then wrapped into a `QueryFilter` using the logical `condition` you provide.

## Supported Filters and Operators

### Filter helpers

Use these builders for field-level comparisons before combining them.

* `eq`, `ne`: equality and inequality.
* `lt`, `lte`, `gt`, `gte`: numeric or timestamp comparisons.
* `in_`, `nin`: membership in a provided list.
* `text_contains`: substring search in text fields.
* `array_contains`: check if array contains a specific value.
* `any_`: check if array contains at least one of the values.
* `all_`: check if array contains all of the values.

### Logical helpers

Reach for these when you need to glue clauses together.

* `and_(*clauses)`: all clauses must be true. Nested ANDs are flattened automatically.
* `or_(*clauses)`: any clause can be true.
* `not_(clause)`: negates the provided clause or QueryFilter.

All helpers live under `gllm_datastore.core.filters.filter` (usually imported as `F`). Mix and match them freely; every datastore implementation speaks the same language.

---

For more detailed informations about the data store query filter, please take a look at our [API Reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_datastore/api/core.html#gllm_datastore.core.FilterClause).
