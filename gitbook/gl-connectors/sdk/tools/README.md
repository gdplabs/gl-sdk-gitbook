---
icon: screwdriver-wrench
---

# Tools

## What Are Tools?

In the context of AI agents, **tools** are functions that a language model can invoke to interact with the outside world. Rather than relying solely on its training data, an agent can call a tool to fetch live information, perform a calculation, query a database, or trigger an action in an external system.

This pattern is central to modern agentic frameworks. LangChain has [Tools](https://docs.langchain.com/oss/python/langchain/tools), CrewAI has [Tools](https://docs.crewai.com/concepts/tools), and the GLLM SDK has its own tool format via the `@tool` decorator — see the [lm-invoker](../../../gen-ai-sdk/tutorials/inference/lm-invoker/ "mention"), [lm-request-processor.md](../../../gen-ai-sdk/tutorials/inference/lm-request-processor.md "mention"), and [tool.md](../../../gen-ai-sdk/tutorials/core/tool.md "mention") to see our version of Tools.

## Beyond In-Process Tools

In-process tools — functions that live alongside the agent in the same codebase — are the most straightforward way to extend an agent. But they aren't the only way, and they come with trade-offs: they're tightly coupled to the agent, harder to share across projects, and can add complexity to the codebase as the number of tools grows.

Depending on what you're trying to achieve, there are three approaches to giving an agent new capabilities:

* **MCP Servers (Remote)** — [Model Context Protocol](https://modelcontextprotocol.io/) servers expose tools over the network via a standardized protocol. This is the truly modular option: tools are deployed independently, shared across agents, and maintained separately from the agent codebase. Best for **shared, general-purpose capabilities** deployed as services.
  * **Reference:** [agentic-tools-and-model-context-protocol-mcp](../agentic-tools-and-model-context-protocol-mcp/ "mention")

{% hint style="warning" %}
We focus on remote (SSE / Streamable HTTP) MCP servers. STDIO-based MCP is omitted because in a typical deployment architecture (`user → server → agent`), the MCP server cannot interact with the user directly — only with the backend that hosts the agent.
{% endhint %}

* **Skills** — Instructions, prompts, and procedures bundled into an agent's configuration. They don't call external functions — instead, they shape _how_ the agent reasons, responds, or follows a workflow. Use skills when the capability is about behavior rather than execution.
  * **Reference:** [connectors-skills](../connectors-skills/ "mention")
* **Unified Tools (GL Connectors Tools SDK)** — Despite the advantages of MCP, in-process tools still have their place. They're the right choice when you need **local API access** (remote MCP servers cannot call internal libraries, local databases, or in-process functions) or have **specific, lightweight use-cases** where the overhead of deploying and maintaining a remote server isn't justified. The GL Connectors Tools SDK provides a unified format for authoring these tools so they work across supported agent frameworks.

### Coming from Other Frameworks

The **GL Connectors Tools SDK** supports converting tools from select frameworks into a unified format, so you can reuse existing tool logic without rewriting it. Conversion is bidirectional and lossless where supported.

<div data-with-frame="true"><figure><img src="../../../.gitbook/assets/image (13).png" alt=""><figcaption><p><a href="https://docs.google.com/presentation/d/1DSqBvM3vfE7-QX5cIGm4aztnZgHVenq-bWo4_fTjNBw/edit?slide=id.g3dd5f5916f1_30_0#slide=id.g3dd5f5916f1_30_0">Diagram Link</a></p></figcaption></figure></div>

{% hint style="info" icon="book-open-lines" %}
For details on converting between tool formats, see [tool-conversion](tool-conversion/ "mention").
{% endhint %}
