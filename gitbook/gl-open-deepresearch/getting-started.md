---
icon: flag-checkered
---

# Getting Started

## GL Open DeepResearch SDK

A Python library for running deep research tasks using the GL Open DeepResearch service.

### Getting Started

#### Hello World

{% tabs %}
{% tab title="Python" %}
```python
from gl_odr_sdk import DeepResearchClient

client = DeepResearchClient(api_key="your-api-key")

task = client.tasks.create(
    query="What are the latest developments in quantum computing?",
    profile="ESSENTIAL",
)

result = client.tasks.get(task.task_id)

if result.data:
    print(result.data.result)
```
{% endtab %}

{% tab title="cURL" %}
```bash
curl --location 'https://open-deepresearch.glair.ai/v1/tasks/your-taskgroup-id'
```
{% endtab %}
{% endtabs %}
