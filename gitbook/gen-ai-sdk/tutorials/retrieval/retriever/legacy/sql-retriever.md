# SQL Retriever

**BasicSQLRetriever** runs natural-language or SQL queries against a SQL data store and returns results as a `DataFrame`. It uses the legacy `BaseSQLDataStore` interface. You can optionally use an LM to fix failed queries (with retries).

**Best For**:

* Natural-language or SQL queries over a relational database
* Structured, tabular results
* Optional automatic query correction via an LM when execution fails

**Key Features**:

* Single query string (natural language or SQL)
* Returns `pd.DataFrame` or `(executed_query, pd.DataFrame)` when `return_query=True`
* Optional `lm_request_processor` and `max_retries` to fix and re-run failed queries
* Optional `preprocess_query_func` and `extract_func` for custom query handling

<details>

<summary>Prerequisites</summary>

You should be familiar with:

1. [SQL Data Store](../../../data-store/legacy/sql-data-store/)
2. [LM Request Processor](../../../inference/lm-request-processor.md) (optional, for retrying failed queries)

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

The SQL Retriever executes a query (natural language or SQL) against the configured SQL data store. If execution fails and you provided an `lm_request_processor` with `max_retries > 0`, it can ask the LM to correct the query and retry.

## Usage

Basic usage with a SQL data store:

```python
from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from gllm_retrieval.retriever import BasicSQLRetriever

# Assume sql_data_store is an existing BaseSQLDataStore (e.g., SQLAlchemySQLDataStore)
# sql_data_store = SQLAlchemySQLDataStore(engine_or_url="sqlite:///data.db")
retriever = BasicSQLRetriever(sql_data_store=sql_data_store)

# Natural language or SQL query
result = await retriever.retrieve("What is machine learning?")
# result: pd.DataFrame

# Return the executed query along with the result
executed_query, result = await retriever.retrieve(
    "SELECT * FROM users LIMIT 10",
    return_query=True
)
```

With automatic retry on failure (LM fixes the query):

```python
from gllm_inference.request_processor import LMRequestProcessor

# Use a system prompt that instructs the LM to fix the SQL given the query and error message
lm_request_processor = LMRequestProcessor(
    lm_invoker=your_lm_invoker,
    system_prompt="Your system prompt: fix SQL given query and error message.",
)
retriever = BasicSQLRetriever(
    sql_data_store=sql_data_store,
    lm_request_processor=lm_request_processor,
    max_retries=2,
)

# If the first query fails, the LM is asked to fix it and the retriever retries
result = await retriever.retrieve("List all users older than 25")
```

{% hint style="info" %}
**Implementation notes**: `BasicSQLRetriever` uses a default system prompt to ask the LM to correct failed SQL queries. You can pass a custom prompt via `LMRequestProcessor`. The `extract_func` argument controls how the modified query is parsed from the LM output; the default expects a single string. See the [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/retriever.html) for details.
{% endhint %}
