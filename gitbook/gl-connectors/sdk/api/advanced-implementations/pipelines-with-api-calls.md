---
icon: pipe-valve
---

# Pipelines with API Calls

Using [pipeline.md](../../../../gen-ai-sdk/tutorials/orchestration/pipeline.md "mention") to orchestrate deterministic flows is shown here as one methodology we can achieve optimal token usage. As you can see, given a deterministic flow and you programmatically **control the flow**, it is best we simply use the standard REST API, because we have control over the flow and procedure itself.

## Case Study: Rate Fetcher

{% hint style="info" %}
For this example, we used a public API with no authentication to make it easier to show you a simple way API Calls can be achieved via Pipeline. This API can easily be adjusted to using GL Connectors' API or SDK (see [quickstart.md](../quickstart.md "mention")), provided you have the appropriate [credentials.md](../credentials.md "mention").
{% endhint %}

This project demonstrates how to build a deterministic, AI-enhanced workflow using the **GL SDK**. The goal is to fetch real-time financial data, process it deterministically, and then use an AI Agent to generate a human-readable summary.

The workflow follows a linear pipeline:

1. **Fetch**: Retrieve raw exchange rates from an external API.
2. **Compare**:Filter and format the rates for major currencies against the USD.
3. **Summarize**: Use an LLM Agent to act as a financial analyst and provide a market summary.

### Dependency Installations

```shellscript
uv init --bare
uv add glaip-sdk[local] gllm-core-binary gllm-pipeline-binary httpx
```

### Source Code

Consider the following source code:

<pre class="language-python" data-title="main.py" data-line-numbers><code class="lang-python">import asyncio, httpx
from typing import TypedDict, Any
from glaip_sdk import Agent
from gllm_core.schema import Component
from gllm_pipeline.steps import step

<strong>class RateFetcher(Component):
</strong>    async def _run(self, *args, **kwargs) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://open.er-api.com/v6/latest/USD")
            return {"rates": resp.json().get("rates", {})}

<strong>class RateComparator(Component):
</strong>    async def _run(self, data: dict, *args, **kwargs) -> str:
        rates = data.get("rates", {})
        majors = ["EUR", "GBP", "JPY", "CAD", "AUD"]
        return "\n".join([f"USD to {c}: {rates[c]}" for c in majors if c in rates])

<strong>class AgentComponent(Component):
</strong>    def __init__(self, name: str, instruction: str):
        super().__init__()
        self.agent = Agent(name=name, instruction=instruction)

    async def _run(self, message: str, *args, **kwargs) -> str:
        parts = []
        async for chunk in self.agent.arun(message):
            c = chunk if isinstance(chunk, str) else getattr(chunk, "content", chunk.get("content") if isinstance(chunk, dict) else None)
            if c: parts.append(str(c))
        return "".join(parts)

<strong>class ExchangeState(TypedDict):
</strong>    raw_data: dict[str, Any]
    comparison_text: str
    final_summary: str

async def main():
<strong>    fetch = step(RateFetcher(), name="fetch", output_state="raw_data")
</strong><strong>    compare = step(RateComparator(), name="compare", input_map={"data": "raw_data"}, output_state="comparison_text")
</strong><strong>    agent = step(AgentComponent("Analyst", "Summarize USD strength in 1 sentence."), name="agent", input_map={"message": "comparison_text"}, output_state="final_summary")
</strong>
<strong>    pipeline = fetch | compare | agent
</strong>    pipeline.state_type = ExchangeState

    result = await pipeline.invoke({"raw_data": {}, "comparison_text": "", "final_summary": ""})
    print(result["final_summary"])

asyncio.run(main())
</code></pre>

### Execution

Simply run the following command:

```
uv run main.py
```

The result will go through multiple steps, until it outputs something like this (your mileage may vary as the response itself is LLM)

{% code overflow="wrap" %}
```
USD strength appears mixed: weaker vs EUR and GBP (1 USD = 0.8417 EUR, 0.7330 GBP) but stronger vs JPY, CAD, and AUD (1 USD = 153.32 JPY, 1.3568 CAD, 1.4043 AUD).
```
{% endcode %}

### Delving into the Code

{% stepper %}
{% step %}
#### Component 1: Rate Fetcher

This component deals with handling USD rates using the [Public Exchange Rate API](https://www.exchangerate-api.com/) endpoint: [https://open.er-api.com/v6/latest/USD](https://open.er-api.com/v6/latest/USD)

```python
class RateFetcher(Component):
    async def _run(self, *args, **kwargs) -> dict:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://open.er-api.com/v6/latest/USD")
            return {"rates": resp.json().get("rates", {})}
```

Performs an asynchronous HTTP GET request to `open.er-api.com` to retrieve the latest USD exchange rates.
{% endstep %}

{% step %}
#### Component 2: Rate Comparator

<pre class="language-python"><code class="lang-python"><strong>class RateComparator(Component):
</strong>    async def _run(self, data: dict, *args, **kwargs) -> str:
        rates = data.get("rates", {})
        majors = ["EUR", "GBP", "JPY", "CAD", "AUD"]
        return "\n".join([f"USD to {c}: {rates[c]}" for c in majors if c in rates])
</code></pre>

Takes the raw rate data and filters it for specific major currencies (EUR, GBP, JPY, CAD, AUD). it formats these rates into a clear, text-based list (e.g., "USD to EUR: 0.85").
{% endstep %}

{% step %}
#### Component 3: Agent Component

<pre class="language-python"><code class="lang-python"><strong>class AgentComponent(Component):
</strong>    def __init__(self, name: str, instruction: str):
        super().__init__()
        self.agent = Agent(name=name, instruction=instruction)

    async def _run(self, message: str, *args, **kwargs) -> str:
        parts = []
        async for chunk in self.agent.arun(message):
            c = chunk if isinstance(chunk, str) else getattr(chunk, "content", chunk.get("content") if isinstance(chunk, dict) else None)
            if c: parts.append(str(c))
        return "".join(parts)
</code></pre>

Wraps a `glaip-sdk` `Agent`. It takes the formatted comparison text as a prompt and uses an LLM to generate a natural language summary. It handles the asynchronous streaming response from the agent.
{% endstep %}

{% step %}
#### Pipeline Orchestration

The components are wired together using the `step` wrapper and the pipe `|` operator:

```python
pipeline = fetch | compare | agent
```

This creates a linear flow where data is passed via a shared `ExchangeState` dictionary, ensuring type safety and clear data lineage.
{% endstep %}
{% endstepper %}
