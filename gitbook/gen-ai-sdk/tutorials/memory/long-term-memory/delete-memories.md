---
icon: trash-can
---

# Delete Memories

Deletes multiple memories based on the provided parameters. You can delete memories by specifying an identifier (`user_id` or `agent_id`) and optionally `memory_ids`.

* If no `memory_ids` are provided, all memories associated with the given `user_id` or `agent_id` will be deleted.
* If `scopes` or `metadata` are included, the deletion will respect these filters — only memories matching the specified `scopes` and `metadata` will be removed.
* When `memory_ids` are provided, any IDs that do not belong to the specified `user_id` or `agent_id` will be ignored; only valid and related memories will be deleted.

## **Parameters**

* **memory\_ids** _(list\[str], optional)_ — List of memory ID.
* **user\_id** _(str, optional)_ — User identifier for the memory.
* **agent\_id** _(str, optional)_ — Agent identifier for the memory.
* **scopes** _(set\[MemoryScope], optional)_ — Specifies the target for memory management, either for a specific participant or for combined access (USER or ASSISTANT). Default is \[USER, ASSISTANT].
  * **USER**: Writes and retrieves memories targeting messages from user.
  * **ASSISTANT**: Writes and retrieves memories targeting messages from assistant.
  * **USER, ASSISTANT**: Writes and retrieves memories targeting messages from both the user and assistant.
* **metadata** _(dict\[str, str], optional)_ — Extra metadata linked to the memory, which can be used to store any supplementary details or context related to it. Default is None.

**Note:** At least one of `user_id` or `agent_id` must be provided.

## **Returns**

_list\[Chunk]_ — A list of deleted memory chunks. Each Chunk follows the GL SDK format and includes an id, content, metadata, and score.

## **Example**

```python
import asyncio
from gllm_memory import MemoryManager

# Initialize
memory_manager = MemoryManager()

memory_ids = [
    "e66f0832-2447-4c5b-ba5f-8fa85957f436",
]
result = asyncio.run(memory_manager.delete(
    memory_ids=memory_ids,
))

print(result)
```

or

```python
import asyncio
from gllm_memory import MemoryManager
from gllm_memory.enums import MemoryScope

# Initialize
memory_manager = MemoryManager()

user_id = "user_123"
agent_id = "agent_general-purpose"

result = asyncio.run(memory_manager.delete(
    user_id=user_id,
    agent_id=agent_id,
    scopes={MemoryScope.USER},
))

print(result)
```

### Expected Output

```python
[
    Chunk(
        id=e66f0832-2447-4c5b-ba5f-8fa85957f436,
        content=User's favorite programming language is Python,
        metadata={
            'message': 'Memory deleted successfully',
            'event': 'DELETE'
        },
        score=None
    )
]
```
