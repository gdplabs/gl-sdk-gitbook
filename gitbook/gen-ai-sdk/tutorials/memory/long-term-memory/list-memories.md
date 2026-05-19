---
icon: magnifying-glass
---

# List Memories

List all memories for a given identifier, optionally filtering the results by specific keywords.

## **Parameters**

* **user\_id** _(str, optional)_ — User identifier for the memory.
* **agent\_id** _(str, optional)_ — Agent identifier for the memory.
* **scopes** _(set\[MemoryScope], optional)_ — Specifies the target for memory management, either for a specific participant or for combined access (USER or ASSISTANT). Default is \[USER].
  * **USER**: Writes and retrieves memories targeting messages from user.
  * **ASSISTANT**: Writes and retrieves memories targeting messages from assistant.
  * **USER, ASSISTANT**: Writes and retrieves memories targeting messages from both the user and assistant.
* **metadata** _(dict\[str, str], optional)_ — Extra metadata linked to the memory, which can be used to store any supplementary details or context related to it. Default is None.
* **keyword** _(str, optional)_ — Keyword to search for in memory content. If not defined, it will return all memories. The keyword is not case sensitive.
* **page** _(int, optional)_ — Page number for pagination. Defaults to 1.
* **page\_size** _(int, optional)_ — Number of items per page. Defaults to 100.

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

result = asyncio.run(memory_manager.memories(
    user_id=user_id,
    agent_id=agent_id,
    keyword="PyTHon",
    scopes={MemoryScope.USER},
    page=1,
    page_size=10,
))

print(result)
```

### Expected Output

```python
[
    Chunk(
        id=003634aa-c99c-4617-8f8d-e76aca07511b,
        content=User's favorite programming language is Python,
        metadata={
            'agent_id': '1f2ef5ee8771...',
            'app_id': 'default-project',
            'source': 'agent_general-purpose',
            'target': '1f2ef5ee8771...',
            'categories': None,
            'is_important': False,
            'mark_important_at': None,
            'created_at': '2025-11-04T07:51:37-08:00',
            'updated_at': '2025-11-04T07:51:37-08:00',
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
