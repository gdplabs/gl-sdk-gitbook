# Customization & Capability

## Custom Prompt

We can customize the deep researcher prompts by supplying a custom `PromptBuilder` object. This is useful for adding custom instructions or simply adjusting the tone of the deep research results.

{% code lineNumbers="true" expandable="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.prompt_builder import PromptBuilder
from gllm_generation.deep_researcher import OpenAIDeepResearcher

prompt_builder = PromptBuilder(
    system_template="Provide your deep research results as if you are a journalist writing a news article.",
    user_template="{query}",
)
event_emitter = EventEmitter.with_print_handler()
query = "Create a concise report about why bananas are yellow."

deep_researcher = OpenAIDeepResearcher(prompt_builder=prompt_builder)
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endcode %}

Please note that although we're only using the `OpenAIDeepResearcher` in the example above, the same approach applies to any other deep researcher subclass.

<a href="https://github.com/gl-sdk/gen-ai-sdk-cookbook/blob/main/gen-ai/tutorials/generation/deep_researcher/02_deep_research_custom_prompt.py" class="button primary">See complete code on GitHub</a>



## MCP Integration

{% hint style="warning" %}
Currently, MCP integration is available in **GoogleDeepResearcher, OpenAIDeepResearcher, ParallelDeepResearcher**, and **GLOpenDeepResearcher**.
{% endhint %}

By default, deep researcher components have the capability to access the internet perform web search operations. This enables them to retrieve and utilize latest public information in the deep research process.

However, sometimes we also need to use non-public services as a source of knowledge. We can **provide additional data sources** to deep research by supplying MCP tools at invocation time.

MCP integration allows deep research to access **private or non-public data** (such as enterprise systems or personal data sources) during execution. It does **not** change how deep research performs research or reasoning internally.

Make sure you have:

* MCP server URL or MCP connector credentials
* For MCP connectors (like Google Calendar), get auth token from the provider

{% code lineNumbers="true" expandable="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_inference.schema import NativeTool
from gllm_generation.deep_researcher import OpenAIDeepResearcher

mcp_server = NativeTool.mcp_server(name="...", url="https://...")
mcp_connector = NativeTool.mcp_connector(
    name="google_drive",
    connector_id="connector_googledrive",
    auth="<google_oauth_token>",
)

event_emitter = EventEmitter.with_print_handler()
query = "Create a concise report about my Google Drive structure!"

deep_researcher = OpenAIDeepResearcher(tools=[mcp_server, mcp_connector])
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endcode %}

## API Configuration

{% hint style="warning" %}
Currently, data store integration is only available in **GLOpenDeepResearcher**.
{% endhint %}

This allows you to configure external REST API endpoints used during the deep research process. This is useful when you need the researcher to access specific external services as part of its workflow.

When `api_config` is not provided, the researcher automatically falls back to the profile's default API configuration.

{% code lineNumbers="true" expandable="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import GLOpenDeepResearcher

api_config = {
    "00000000-0000-0000-0000-000000000001": {
        "url": "https://example.com/api",
    }
}

event_emitter = EventEmitter.with_print_handler()
query = "Create a concise report about the latest company announcements."

deep_researcher = GLOpenDeepResearcher(api_config=api_config)
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endcode %}

## Data Store Integration

{% hint style="warning" %}
Currently, data store integration is available in **GoogleDeepResearcher** and **OpenAIDeepResearcher**.
{% endhint %}

Another way to connect to a non-public source of knowledge is by integrating a data store to our deep researcher component. This allows the deep researcher to access files stored in certain provider-managed file stores services. To learn more about these data stores, please refer to the [LM invoker data store management page](../../gen-ai-sdk/tutorials/inference/lm-invoker/data-store-management.md).

Use standardized native tools to pass data stores via the `tools` parameter.

{% code lineNumbers="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_core.event import EventEmitter
from gllm_generation.deep_researcher import GoogleDeepResearcher
from gllm_inference.schema import AttachmentStore, NativeTool

store = AttachmentStore(id="fileSearchStores/<fileSearchStoreId>", provider="google")
data_store_tool = NativeTool.data_store([store])

event_emitter = EventEmitter.with_print_handler()
query = "Analyze the <topic> document and present it as a concise report!"

deep_researcher = GoogleDeepResearcher(tools=[data_store_tool])
asyncio.run(deep_researcher.research(query=query, event_emitter=event_emitter))
```
{% endcode %}

{% hint style="info" %}
`GoogleDeepResearcher(data_stores=[...])` is deprecated and will be removed in a future release. Use `tools=[NativeTool.data_store([...])]` for forward-compatible configuration.
{% endhint %}

## Event Timeout Configuration

{% hint style="warning" %}
Currently, event retry mechanism is only available in **ParallelAIDeepResearcher**.
{% endhint %}

Due to the prolonged process of event streaming, any individual event might momentarily become stuck at some point during the emission phase. To circumvent this potential bottleneck and ensure a smooth flow of events, you can configure an `event_idle_timeout` parameter when initializing the deep researcher.

This timeout mechanism monitors event emission and automatically retries if an event remains idle for longer than the specified duration.

{% code lineNumbers="true" expandable="true" %}
```python
from dotenv import load_dotenv
load_dotenv()

import asyncio
from gllm_generation.deep_researcher import ParallelDeepResearcher
from gllm_core.event import EventEmitter
from gllm_core.utils.retry import RetryConfig
import os

async def research_simple():
    event_emitter = EventEmitter.with_console_handler()
    researcher = ParallelDeepResearcher(
        api_key=os.getenv("PARALLEL_API_KEY"),
        retry_config=RetryConfig(timeout=3600, max_retries=4),
        event_idle_timeout=5
    )
    output = await researcher.research(
        query="Design three differentiated itineraries that competitors rarely deliver as a coherent package and tie them to clear buyer personas",
        event_emitter=event_emitter
    )
    print("\n\n\n")
    print(output)

if __name__ == "__main__":
    asyncio.run(research_simple())
```
{% endcode %}

In this example:

* `retry_config` sets the overall timeout (3600 seconds) and maximum retries (4 attempts)
* `event_idle_timeout=5` ensures that if any event remains idle for more than 5 seconds, it will be retried automatically

## Next Step

1. Explore different [research profiles](https://gdplabs.gitbook.io/gl-open-deepresearch/developers-guide/customization/profiles) for GLOpenDeepResearcher.
2. Explore [guides](../guides/ "mention").
