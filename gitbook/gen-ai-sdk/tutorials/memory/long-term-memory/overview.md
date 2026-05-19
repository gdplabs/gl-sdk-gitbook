---
icon: clipboard-question
---

# Overview

This SDK provides a provider-agnostic memory layer. Your app talks only to `MemoryManager`, which uses a factory to load a concrete `BaseMemoryClient` (e.g., `Mem0Client`) based on `MemoryConfig`. By keeping a stable interface (`add`, `search`, `memories`, `delete`), you can swap or add providers without changing application code.

## **Class Diagram**

<figure><img src="../../../../.gitbook/assets/Copy of Diagram Color Guide (7).png" alt=""><figcaption></figcaption></figure>

## How It Works

This SDK uses a **Factory + Strategy** design aligned with the diagram: the factory (`memory_client.create_from_env`) reads the environment (e.g., `MEMORY_PROVIDER`, API key), selects a concrete client (e.g., `Mem0Client`), and returns it as a `BaseMemoryClient`. `MemoryManager` is initialized with only the **instruction** and works against the `BaseMemoryClient` interface—providers implement the same methods with different implementations (`add`, `search`, `list_memories`, `delete`, `delete_by_user_query`). This keeps the app layer clean and extensible: you can swap or add providers by changing environment variables (no application code changes), improving testability and separation of concerns. It also guarantees **polymorphism**: calls made by `MemoryManager` behave identically across providers because they share the `BaseMemoryClient` contract.

## How to Add a New Memory Provider

### A. Implement the contract (BaseMemoryClient)

Create a class (e.g., `NewProviderClient`) that **implements all methods** below and returns `list[Chunk]`:

* `add(user_id, agent_id, messages, scopes, metadata, infer)`
* `search(query, user_id, agent_id, scopes, metadata, threshold, top_k)`
* `memories(user_id, agent_id, scopes, metadata, keyword, page, page_size)`
* `delete(memory_ids, user_id, agent_id, scopes, metadata)`
* `delete_by_user_query(query, user_id, agent_id, scopes, metadata, threshold, top_k)`

Scope rules you must support:

* `MemoryScope.USER` → operate on `user_id`
* `MemoryScope.ASSISTANT` → operate on `agent_id`
* `MemoryScope.ALL` → apply to both

```python
class NewProviderClient(BaseMemoryClient):
    def __init__(self, *, api_key: str, timeout_sec: int = 30, **_): ...

    async def add(self, *, user_id=None, agent_id=None, messages=None,
                  scopes=None, metadata=None, infer=True): ...

    async def search(self, *, query, user_id=None, agent_id=None,
                     scopes=None, metadata=None, threshold=0.3, top_k=10): ...

    async def list_memories(self, *, user_id=None, agent_id=None, scopes=None,
                            metadata=None, keyword=None, page=1, page_size=100): ...

    async def delete(self, *, memory_ids=None, user_id=None, agent_id=None,
                     scopes=None, metadata=None): ...

    async def delete_by_user_query(self, *, query, user_id=None, agent_id=None,
                                   scopes=None, metadata=None, threshold=0.3, top_k=10): ...
```

### B. Register the provider (provider\_factory)

Add your class to the **`PROVIDER_REGISTRY`** in `provider_factory`:

```python
# provider_factory.py
PROVIDER_REGISTRY = {
    "mem0": Mem0Client,
    "newprovider": NewProviderClient,   # <-- add this
}
```

### C. Set environment variables

Provide the API key via env variables.

```
NEWPROVIDER_API_KEY=sk-xxxx
```
