---
icon: trash-can
---

# Delete Memory by User Query

Delete memories based on a user query.

## **Parameters**

* **query** _(str, required)_ — user query string to identify memories to delete.
* **user\_id** _(str, optional)_ — User identifier for the memory.
* **agent\_id** _(str, optional)_ — Agent identifier for the memory.
* **scopes** _(set\[MemoryScope], optional)_ — Specifies the target for memory management, either for a specific participant or for combined access (USER or ASSISTANT). Default is \[USER, ASSISTANT].
  * **USER**: Writes and retrieves memories targeting messages from user.
  * **ASSISTANT**: Writes and retrieves memories targeting messages from assistant.
  * **USER, ASSISTANT**: Writes and retrieves memories targeting messages from both the user and assistant.
* **metadata** _(dict\[str, str], optional)_ — Extra metadata linked to the memory, which can be used to store any supplementary details or context related to it. Default is None.
* **threshold** _(float, optional)_ — Minimum similarity threshold for results. Default is 0.3.
* **top\_k** _(int, optional)_ — Maximum number of results to return. Default is 10.

**Note:** At least one of `user_id` or `agent_id` must be provided.

## **Returns**

_list\[Chunk]_ — A list of deleted memory chunks. Each Chunk follows the GL SDK format and includes an id, content, metadata, and score.

## **Example**

```python
import asyncio
from gllm_memory import MemoryManager
from gllm_memory.enums import MemoryScope

# Initialize
memory_manager = MemoryManager()

user_id = "user_123"
agent_id = "agent_general-purpose"

result = asyncio.run(memory_manager.delete_by_user_query(
    user_id="user_123",
    query="food preferences",
    scopes=[MemoryScope.USER],
    threshold=0.5,
    top_k=2,
))

print(result)
```

### Expected Output

<pre class="language-python"><code class="lang-python"><strong>[
</strong>    Chunk(
        id=003634aa-c99c-4617-8f8d-e76aca07511b,
        content=User Prefers pizza and Italian food,
        metadata={
            'message': 'Memory deleted successfully',
            'event': 'DELETE'
        },
        score=None
    )
]
</code></pre>
