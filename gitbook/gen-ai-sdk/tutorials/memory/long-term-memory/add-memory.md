---
icon: plus
---

# Add Memory

Add new memory items from a list of messages.

## **Parameters**

* **user\_id** _(str, required)_ — User identifier for the memory.
* **agent\_id** _(str, required)_ — Agent identifier for the memory.
* messages (_list\[Message]_, _required_) — List of messages to store in memory. Each Message follows the GL SDK format and contains a role and content.
* **scopes** _(set\[MemoryScope], optional)_ — Specifies the target for memory management, either for a specific participant or for combined access (USER or ASSISTANT). Default is \[USER].
  * **USER**: Writes and retrieves memories targeting messages from user.
  * **ASSISTANT**: Writes and retrieves memories targeting messages from assistant.
  * **USER, ASSISTANT**: Writes and retrieves memories targeting messages from both the user and assistant.
* **metadata** _(dict\[str, str], optional)_ — Extra metadata linked to the memory, which can be used to store any supplementary details or context related to it. Default is None.
* **infer** _(boolean, optional)_ — Whether to infer the memories or directly store the messages. Default is True.

## **Returns**

_list\[Chunk]_ — A list of memory chunks created. Each Chunk follows the GL SDK format and includes an id, content, metadata, and score.

## **Example**

<pre class="language-python"><code class="lang-python">import asyncio
from gllm_inference.schema.message import Message
from gllm_memory import MemoryManager
<strong>from gllm_memory.enums import MemoryScope
</strong>
# Initialize
memory_manager = MemoryManager()

messages = [
    Message.user("I love pizza and Italian food"),
    Message.assistant("I'll remember that you love pizza and Italian food"),
    Message.user("My favorite programming language is Python")
]

user_id = "user_123"
agent_id = "agent_xyz"

result = asyncio.run(memory_manager.add(
    user_id=user_id,
    agent_id=agent_id,
    scopes={MemoryScope.USER},
    messages=messages,
))

print(result)
</code></pre>

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
            'is_important': False,
            'mark_important_at': None,
            'created_at': '2025-11-04T07:51:26-08:00',
            'updated_at': '2025-11-04T07:51:26-08:00',
            'expiration_date': None,
            'structured_attributes': {
                'year': 2025, 'month': 11, 'day': 4, 'hour': 15, 'minute': 51,
                'day_of_week': 'tuesday', 'week_of_year': 45, 'day_of_year': 308,
                'quarter': 4, 'is_weekend': False
            },
            'event': 'ADD',
        },
        score=None
    ),
    Chunk(
        id=e66f0832-2447-4c5b-ba5f-8fa85957f436,
        content=User's favorite programming language is Python,
        metadata={
            'agent_id': '1f2ef5ee8771...',
            'app_id': 'default-project',
            'source': 'agent_general-purpose',
            'target': '1f2ef5ee8771...',
            'categories': None,
            "is_important": False,
            "mark_important_at": "2025-01-01T00:00:00Z",
            'created_at': '2025-11-04T07:51:37-08:00',
            'updated_at': '2025-11-04T07:51:37-08:00',
            'expiration_date': None,
            'structured_attributes': {
                'year': 2025, 'month': 11, 'day': 4, 'hour': 15, 'minute': 51,
                'day_of_week': 'tuesday', 'week_of_year': 45, 'day_of_year': 308,
                'quarter': 4, 'is_weekend': False
            },
            'event': 'ADD',
        },
        score=None
    )
]
```
