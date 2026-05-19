---
icon: gear
---

# Supported Vector Data Store

This page provides instructions for setting up a vector data store to be used in your retrieval pipeline.

## Chroma

1.  **ChromaDB Memory**

    1. Store type: `chroma`
    2. Client type: `memory`
    3. Example:

    ```python
    store = build_data_store(
        store_type="chroma",
        index_name="your_index_name",
        embedding=your_embedding,
        config: {"client_type": "memory"}
    )
    ```
2.  **ChromaDB Persistent**

    1. Store type: `chroma`
    2. Client type: `persistent`
    3. Example:

    ```python
    store = build_data_store(
        store_type="chroma",
        index_name="your_index_name",
        embedding=your_embedding,
        config={"client_type": "persistent", "persist_directory": "/path/to/dir"}
    )
    ```
3.  **ChromaDB HTTP**

    1. Store type: `chroma`
    2. Client type: `http`
    3. Example:

    ```python
    store = build_data_store(
        store_type="chroma",
        index_name="your_index_name",
        embedding=your_embedding,
        host="localhost",
        port=8000,
        config={"client_type": "http"}
    )
    ```

## Elasticsearch

1. Store type: `elasticsearch`
2. Set up a managed Elasticsearch instance with vector search via [Elastic Cloud](https://cloud.elastic.co/login) or [local development setup](https://www.elastic.co/docs/deploy-manage/deploy/self-managed/local-development-installation-quickstart)
3. Example:

```python
store = build_data_store(
    store_type="elasticsearch",
    index_name="your_index_name",
    embedding=your_embedding,
    config={"url": "https://your-elasticsearch-endpoint", "api_key": os.getenv("ELASTIC_API_KEY")}
)
```
