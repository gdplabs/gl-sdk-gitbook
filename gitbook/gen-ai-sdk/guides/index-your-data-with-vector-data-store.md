---
icon: database
---

# Index Your Data with Vector Data Store

This guide will walk you through setting up a data store and index your local data to a data store.

<details>

<summary>Prerequisites</summary>

This example specifically requires:

1. Completion of all setup steps listed on the [prerequisites.md](../prerequisites.md "mention") page.

You should be familiar with these concepts and components:

1. [data-store](../tutorials/data-store/ "mention")
2. [em-invoker.md](../tutorials/inference/em-invoker.md "mention")

</details>

{% include "../../.gitbook/includes/cookbook.md" %}

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gen-ai/how-to-guides/index_your_data" class="button primary" data-icon="github">View full project code on GitHub</a>

## Installation

{% tabs %}
{% tab title="Linux, macOS, or Windows WSL" %}
```bash
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference gllm-datastore
```
{% endtab %}

{% tab title="Windows Powershell" %}
```powershell
# you can use a Conda environment
pip install --extra-index-url "https://oauth2accesstoken:$(gcloud auth print-access-token)@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-inference gllm-datastore
```
{% endtab %}

{% tab title="Windows Command Prompt" %}
```bash
FOR /F "tokens=*" %T IN ('gcloud auth print-access-token') DO pip install --extra-index-url "https://oauth2accesstoken:%T@glsdk.gdplabs.id/gen-ai-internal/simple/" gllm-datastore
```
{% endtab %}
{% endtabs %}

{% include "../../.gitbook/includes/how-to-use-this-guide.md" %}

## Initialize Vector Data Store

{% hint style="info" %}
When running the pipeline, you may encounter an error like this:

```
[2025-08-26T14:36:10+0700.550 chromadb.telemetry.product.posthog ERROR] Failed to send telemetry event CollectionQueryEvent: capture() takes 1 positional argument but 3 were given
```

Don't worry about this, since we do not use this Chroma feature. Your data store will still work.
{% endhint %}

First, we need to set up a vector data store. In this example, we will use in-memory Chroma Vector Data Store. To initialize the data store, we need two components: EM Invoker and Vector Data Store.

### Option 1: Directly from a Chunk

All data stores support storing data in a structured format using the `Chunk` schema. Think of chunks as standardized containers for your data - they provide a consistent way to represent information across different storage types, making it easy to switch between datastores or combine them in your application.

After that, we can simply use `add_chunks()` method provided by the Vector Data Store.

To load the data, you can run the script below:

```python
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_inference.em_invoker import OpenAIEMInvoker

# Initialize data store with vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
data_store = ChromaDataStore(
    collection_name="documents",
).with_vector(em_invoker=em_invoker)

# Add chunks to the store
chunks = [
    Chunk(content="AI is the future."),
    Chunk(content="Parrot is a bird."),
]
await data_store.add_chunks(chunks)
```

### Option 2: Loading Data from CSV Files

For real-world applications, you'll often need to load data from structured files like CSV. Suppose your project has the following structure:

```
<project-name>/
├── data/
│   └── imaginary_animals.csv
└── indexer.py
```

To load the data, you can run the script below:

{% code lineNumbers="true" %}
```python
import asyncio
import csv
from dotenv import load_dotenv
from gllm_core.schema import Chunk
from gllm_datastore.data_store import ChromaDataStore
from gllm_datastore.data_store.chroma.data_store import ChromaClientType
from gllm_inference.em_invoker import OpenAIEMInvoker

load_dotenv()

# Initialize data store with persistent storage and vector capability
em_invoker = OpenAIEMInvoker(model_name="text-embedding-3-small")
data_store = ChromaDataStore(
    collection_name="documents",
    client_type=ChromaClientType.PERSISTENT,  # use a Persistent Chroma DB
    persist_directory="data",                 # 👈 where the data is located
).with_vector(em_invoker=em_invoker)

# Load documents from CSV file
async def load_csv_data():
    with open("data/imaginary_animals.csv", "r") as f:
        reader = csv.DictReader(f)
        chunks = [
            Chunk(
                content=row["description"],
                metadata={"name": row["name"]}
            )
            for row in reader
        ]

    await data_store.add_chunks(chunks)
    print(f"Successfully indexed {len(chunks)} documents from CSV file")

if __name__ == "__main__":
    asyncio.run(load_csv_data())
```
{% endcode %}

**Key features of this approach:**

* **Persistent Storage**: Uses `ChromaClientType.PERSISTENT` to save data to disk
* **Metadata Support**: Stores additional information (like animal names) in chunk metadata
* **Batch Loading**: Efficiently loads all CSV rows at once
* **Structured Data**: Converts CSV rows into standardized `Chunk` objects

{% hint style="info" %}
After running this script, you’ll see an SQLite database created in your project directory.
{% endhint %}

**CSV File Format Example:**

```csv
name,description
Fire Phoenix,A mythical bird that rises from ashes with brilliant flames
Crystal Unicorn,A magical creature with a horn made of pure crystal
Shadow Wolf,A mysterious wolf that can blend into shadows
```

## Querying Data

To query data using semantic search, we utilize `query()` method. This will return `list[Chunk]`

```python
results: list[Chunk] = await data_store.query(query="artificial intelligence")
```

When querying data loaded from CSV, you can access both content and metadata:

```python
# Query for mythical creatures
results = await data_store.query(query="magical creatures")

for chunk in results:
    print(f"Name: {chunk.metadata.get('name', 'Unknown')}")
    print(f"Description: {chunk.content}")
    print("---")
```

## 📂 Complete Guide Files <a href="#complete-guide-files" id="complete-guide-files"></a>

For the complete code, please visit our [GitHub Cookbook Repository](https://github.com/GDP-ADMIN/gl-sdk-cookbook/tree/main/gen-ai/how-to-guides/index_your_data).
