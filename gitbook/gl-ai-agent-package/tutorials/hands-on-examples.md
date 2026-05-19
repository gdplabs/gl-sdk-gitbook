---
icon: bolt-lightning
---

Use these examples after [Quick Start](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/quick-start-guide) to explore real scenarios with runnable code and CLI commands.

> **Success**
>
> **When to use this page:** You are ready for richer workflows and want copy-and-run snippets instead of building from scratch.

{% hint style="info" %}
**Audience:** Engineers prototyping orchestration, PMs preparing demos, and data developers running evaluations without coding.
{% endhint %}

{% hint style="info" %}
**TUI Development**: Many examples below demonstrate Textual-based TUI patterns. For comprehensive TUI guidance, refer to the TUI foundation spec in the repository.
{% endhint %}

{% hint style="info" %}
**Note:** Validated example projects are now centralized in the [GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip). This ensures all blueprints remain self-contained, runnable, and maintained with the latest SDK best practices.
{% endhint %}

Each row links to a runnable project. Follow the README for quick start instructions, then inspect code to understand the pattern.

## Validated Example Projects

These projects demonstrate foundational patterns and are maintained in the [GL SDK Cookbook](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip). Each project is self-contained and ready to run.

| Pattern                       | Description                                                                                                                                           | Project Link                                                                                                               |
| :---------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Basic Agent (Hello World)** | A minimal starter demonstrating how to create and run an agent using config-based instantiation.                                                      | [hello-world](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/hello-world)                           |
| **Modular Tool Integration**  | Learn how to organize complex tools with separate helper files and modular structure.                                                                 | [modular-tool-integration](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/modular-tool-integration) |
| **Multi-Agent Coordinator**   | Coordinator with specialized sub-agents (e.g., formal and casual greeting team).                                                                      | [multi-agent](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent)                           |
| **Multi-Agent Patterns**      | Runnable blueprints for Sequential, Parallel, Router, Hierarchical, and Aggregator flows.                                                             | [multi-agent-patterns](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/multi-agent-system-patterns)  |
| **Runtime Configuration**     | How to pass per-request overrides for agents, tools, and MCPs at runtime (e.g., database URLs or planning).                                           | [runtime-config](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/runtime-config)                     |
| **Agent Export & Import**     | Demonstrates how to serialize and deserialize agent configurations for portability.                                                                   | [export-import](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/agent-export-import)                 |
| **Local Execution**           | Run agents locally without deployment (see [Local vs Remote](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/getting-started/local-vs-remote) for feature mapping). | [hello-world-local](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip/examples/hello-world-local)               |

______________________________________________________________________

## Cookbook Examples

For quick copy-and-run recipes, use the dedicated [Cookbook repository](https://github.com/gl-sdk/gen-ai-sdk-cookbook/tree/main/gl-aip).
