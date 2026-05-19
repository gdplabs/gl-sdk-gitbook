---
icon: pen-to-square
---

# Update Memory

Updates an existing memory by providing the memory ID and the new content or metadata. You can modify the memory content, update metadata, or change whether the memory is marked as important.

## **Parameters**

* **memory\_id** _(str, required)_ — Unique identifier of the memory to update.
* **new\_content** _(str, optional)_ — Updated content for the memory. If None, the existing content stays the same. Default is None.
* **metadata** _(dict\[str, str], optional)_ — Updated metadata to merge with existing metadata. If None, metadata stays unchanged. Default is None.
* **user\_id** _(str, optional)_ — User identifier for the memory.
* **agent\_id** _(str, optional)_ — Agent identifier for the memory.
* **scopes** _(set\[MemoryScope], optional)_ — Specifies the target for memory management, either for a specific participant or for combined access (USER or ASSISTANT). Default is \[USER].
  * **USER**: Writes and retrieves memories targeting messages from user.
  * **ASSISTANT**: Writes and retrieves memories targeting messages from assistant.
  * **USER, ASSISTANT**: Writes and retrieves memories targeting messages from both the user and assistant.
* **is\_important** _(boolean, optional)_ — Flag indicating if the memory is important. Default is False.

**Note:** At least one of `user_id` or `agent_id` must be provided.

## **Returns**

_Chunk_ — The updated memory chunk in GL SDK format, or None if the memory was not found or the operation failed.

## **Example**

```python
import asyncio
from gllm_memory import MemoryManager
from gllm_memory.enums import MemoryScope

# Initialize
memory_manager = MemoryManager()

user_id = "user_123"
agent_id = "agent_general-purpose"

result = asyncio.run(memory_manager.memories(
    memory_id="memory_uuid_123",
    new_content="Updated memory content about Python programming",
    user_id=user_id,
    agent_id=agent_id,
    metadata={
        "category": "programming",
    },
    scopes={MemoryScope.USER},
    is_important=True
))

print(result)
```

### Expected Output

```python
Chunk(
    id="memory_uuid_123",
    content="Updated memory content about Python programming",
    metadata={
        'agent_id': '1f2ef5ee8771...',
        'app_id': 'default-project',
        'source': 'agent_general-purpose',
        'target': '1f2ef5ee8771...',
        'categories': None,
        'category': 'programming',
        'is_important': True,
        'mark_important_at': '2025-01-01T00:00:00Z',
        'created_at': '2025-11-04T07:51:37-08:00',
        'updated_at': '2025-11-04T07:51:37-08:00',
        'expiration_date': None,
        'structured_attributes': {
            'year': 2025, 'month': 11, 'day': 4, 'hour': 15, 'minute': 51,
            'day_of_week': 'tuesday', 'week_of_year': 45, 'day_of_year': 308,
            'quarter': 4, 'is_weekend': False
        },
        'event': 'UPDATE',
    },
    score=None
)
```
