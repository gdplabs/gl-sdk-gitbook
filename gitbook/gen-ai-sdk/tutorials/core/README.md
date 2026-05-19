---
icon: block
---

# Core

## What is GLLM Core?

GLLM Core provides utility components to manage shared functionality across RAG components, including:

1. [**Component:**](component.md) Defines reusable runtime units with `@main` as the primary entrypoint and standardized execution via `run(...)`.
2. [**Dynamic Component:**](dynamic-component.md) Builds components dynamically at runtime using `Lazy` constructor bindings.
3. [**Logger Manager:**](logger-manager.md) Manages logging across Gen AI apps.
4. [**Event Emitter:**](event-emitter.md) Manages event emitting (including streaming) across Gen AI apps.
5. [**Tool:**](tool.md) Defines MCP-style callable functions for agent tool use.
