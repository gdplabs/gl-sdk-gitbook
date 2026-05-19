# Vector DB

**Vector DB Indexer** is a component designed for **indexing parsed document elements** into vector databases using vector capability implementations for Retrieval-Augmented Generation (RAG) applications.

<details>

<summary>Prerequisites</summary>

This example specifically requires completion of all setup steps listed on the [Prerequisites](../../../prerequisites.md) page.

You should be familiar with these concepts and components:

1. [Data Store](../../data-store/ "mention")
2. [EM Invoker](../../inference/em-invoker.md "mention")

</details>

## **Installation**

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/ gllm-docproc
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
$token = (gcloud auth print-access-token)
pip install --extra-index-url "https://oauth2accesstoken:$token@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-docproc
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
# you can use a Conda environment
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO SET TOKEN=%T
pip install --extra-index-url "https://oauth2accesstoken:%TOKEN%@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-docproc
```
{% endtab %}
{% endtabs %}

You can use the following as a sample file: [structuredelementchunker-output.json](https://assets.analytics.glair.ai/generative/pdf/structuredelementchunker-output.json).

{% stepper %}
{% step %}
Create a script called `main.py`:

{% code lineNumbers="true" %}
```python
import json

from gllm_docproc.indexer.vector.vector_db_indexer import VectorDBIndexer

# Read elements from JSON file
file_path = "./structuredelementchunker-output.json"

with open(file_path, "r", encoding="utf-8") as f:
    elements = json.load(f)

indexer = VectorDBIndexer()

# Index the elements with required configuration
result = indexer.index(
    elements=elements,
    file_id="file_001",
    vectorizer_kwargs={
        "model": "openai/text-embedding-3-small",  # Format: "provider/model_name"
        "api_key": "<OPENAI_API_KEY>",
    },
    db_engine="elasticsearch",  # Supported: "chroma", "elasticsearch", "opensearch"
    db_config={
        "url": "http://localhost:9200",
        "index_name": "my_index",
    },
)
```
{% endcode %}
{% endstep %}

{% step %}
Run the script:

```bash
python main.py
```
{% endstep %}
{% endstepper %}

{% hint style="info" %}
**Vector Store Support**: The Vector DB Indexer works with any implementation of `VectorCapability`, including Elasticsearch, ChromaDB, Redis, and In-Memory stores. See [supported-vector-data-store.md](../../../resources/supported-vector-data-store.md "mention") for a complete list.
{% endhint %}
