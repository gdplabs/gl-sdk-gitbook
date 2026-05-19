---
icon: magnifying-glass
---

# Search Memory

Search memories based on a user query.

## **Parameters**

* **query** _(str, required)_ — Retrieval query string.
* **user\_id** _(str, optional)_ — User identifier for the memory.
* **agent\_id** _(str, optional)_ — Agent identifier for the memory.
* **scopes** _(set\[MemoryScope], optional)_ — Specifies the target for memory management, either for a specific participant or for combined access (USER or ASSISTANT). Default is \[USER].
  * **USER**: Writes and retrieves memories targeting messages from user.
  * **ASSISTANT**: Writes and retrieves memories targeting messages from assistant.
  * **USER, ASSISTANT**: Writes and retrieves memories targeting messages from both the user and assistant.
* **metadata** _(dict\[str, str], optional)_ — Extra metadata linked to the memory, which can be used to store any supplementary details or context related to it. Default is None.
* **threshold** _(float, optional)_ — Minimum similarity threshold for results. Default is 0.3.
* **top\_k** _(int, optional)_ — Maximum number of results to return. Default is 10.
* **include\_important** _(boolean, optional)_ — If True, includes all important memories\
  in addition to query matches. Default is False.
* **rerank** _(boolean, optional)_ — If True, applies re-ranking to search results. Default is False.

**Note:** At least one of `user_id` or `agent_id` must be provided.

## **Returns**

_list\[Chunk]_ — A list of retrieved memory chunks. Each Chunk follows the GL SDK format and includes an id, content, metadata, and score.

## **Example**

```python
import asyncio
from gllm_memory import MemoryManager
from gllm_memory.enums import MemoryScope

# Initialize
memory_manager = MemoryManager()

user_id = "user_123"
agent_id = "agent_general-purpose"

result = asyncio.run(memory_manager.search(
    query="What does the user like to eat?",
    user_id=user_id,
    agent_id=agent_id,
    scopes={MemoryScope.USER},
    threshold=0.3,
    top_k=5,
    include_important=True
))

print(result)
```

### Expected Output

```python
[
    Chunk(
        id=003634aa-c99c-4617-8f8d-e76aca07511b,
        content=User Prefers pizza and Italian food,
        metadata={
            'user_id': '1f2ef5ee8771...',
            'app_id': 'default-project',
            'source': '1f2ef5ee8771...',
            'target': 'agent_general-purpose',
            'categories': None,
            'is_important': True,
            'mark_important_at': '2025-01-01T00:00:00Z',
            'created_at': '2025-11-04T07:51:26-08:00',
            'updated_at': '2025-11-04T07:51:26-08:00',
            'expiration_date': None,
            'structured_attributes': {
                'year': 2025, 'month': 11, 'day': 4, 'hour': 15, 'minute': 51,
                'day_of_week': 'tuesday', 'week_of_year': 45, 'day_of_year': 308,
                'quarter': 4, 'is_weekend': False
            },
            'event': 'RETRIEVE',
        },
        score=0.6258521899073022
    )
]
```
