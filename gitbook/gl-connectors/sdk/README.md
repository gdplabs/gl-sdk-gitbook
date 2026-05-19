---
icon: compass
---

# Guides

The GL Connectors Tools SDK provides several ways to extend your agent's capabilities. Choose the approach that best fits your use case:

* [api](api/ "mention") — Reference documentation for the GL Connectors ecosystem, its API capabilities and supplementary libraries on how to access the system.
* [agentic-tools-and-model-context-protocol-mcp](agentic-tools-and-model-context-protocol-mcp/ "mention") — Remote MCP servers expose tools over the network via a standardized protocol. This is the truly modular option: tools are deployed independently, shared across agents, and maintained separately from the agent codebase. Best for **shared, general-purpose capabilities**.
  * **Related Documentations:**
    * [quickstart.md](agentic-tools-and-model-context-protocol-mcp/quickstart.md "mention") to quickly get up to speed.
    * [Curated MCP List](http://connectors.glair.ai/mcps/list)
* [**Tools**](https://claude.ai/chat/tools/README.md) — In-process tools that run alongside the agent. Best for **local API access** and **specific, lightweight use-cases** where the overhead of deploying a remote server isn't justified. The SDK provides a unified BaseTool format so tools work across supported agent frameworks.
* [**Skills**](https://claude.ai/chat/skills/README.md) — Instructions, prompts, and procedures bundled into an agent's configuration. Skills shape _how_ the agent reasons and follows workflows — use them when the capability is about **behavior rather than execution**.
