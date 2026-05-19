---
icon: books
---

# Terminology

<div data-with-frame="true"><figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p><a href="https://docs.google.com/presentation/d/1DSqBvM3vfE7-QX5cIGm4aztnZgHVenq-bWo4_fTjNBw/edit?slide=id.g3dd4be35086_2_0#slide=id.g3dd4be35086_2_0">Diagram Link</a></p></figcaption></figure></div>

{% hint style="info" %}
GL Connectors = [#agent-skills](terminology.md#agent-skills "mention") + [#mcp-servers](terminology.md#mcp-servers "mention") + [#tools](terminology.md#tools "mention") + [#apis](terminology.md#apis "mention")
{% endhint %}

The umbrella project that sits between Clients and the outside world, providing everything agents need to interact with both local systems and external services.

A **Connector** refers to any third-party service provider (e.g., Gmail, Google Calendar, Microsoft Teams) integrated into the platform. In essence, a Connector here represents a group of Tools exposed by a provider.

Together, these form a single source of truth for agent capabilities, from high-level workflows down to individual API calls.

**Reference**: [gl-connectors](gl-connectors/ "mention")

## GL Connector Components

### Agent Skills

Downloadable, reusable agent capabilities sourced from various providers and managed via the GL Connectors SDK. Skills represent higher-level recipes or workflows that extend what an agent can do beyond individual tool calls. Agent Skills can operate over both **REST API** (for remote services) and **Local API** (for filesystem access, code execution, etc.).

**Reference:** [connectors-skills](sdk/connectors-skills/ "mention")

### MCP Servers

Model Context Protocol servers hosted by or provided by GL Connectors. They expose Third Party Connector to any MCP-compatible client, allowing LLMs to discover and invoke operations dynamically without custom code.

**Reference:** [agentic-tools-and-model-context-protocol-mcp](sdk/agentic-tools-and-model-context-protocol-mcp/ "mention")

### Tools

Tools are the granular capabilities that AI agents use to perform actions. They come in two forms:

* **Connector Tools** — Individual endpoints of a Connector, accessed via [#rest-api](terminology.md#rest-api "mention") (e.g., "Send Email" or "Create Calendar Event").
* **Local Tools** — Built-in capabilities accessed via [#local-api](terminology.md#local-api "mention") (e.g., file uploads, filesystem access, code execution).

All Tools are compatible with GL SDK's `BaseTool`, LangChain Tools, and other agent frameworks (LangGraph, CrewAI, etc.), enabling agents to interact with external services and local capabilities out of the box.

**Reference:** [tools](sdk/tools/ "mention")

### APIs

APIs (Application Programming Interface) is a set of functions and procedures allowing the creation of applications that access the features or data of an operating system, application, or other service. We separate it into two types: **REST API** for remote capabilities (i.e., accessing external services) for every Connector, or **Local API** for accessing the local system itself.

**Reference:** [api](sdk/api/ "mention")

#### REST API

The standard HTTP communication layer used by GL Connectors to interact with remote systems—third-party services, external databases, cloud storage, etc. [#mcp-servers](terminology.md#mcp-servers "mention"), [#agent-skills](terminology.md#agent-skills "mention") and [#tools](terminology.md#tools "mention") typically communicate through this layer.

#### Local API

The communication layer used by GL Connectors to interact with the local system—file access, code execution, system time, etc. Currently accessible through [#agent-skills](terminology.md#agent-skills "mention") and [#tools](terminology.md#tools "mention") only; HTTP MCP Servers do not support local operations.

***

### GL Connectors Clients

GL Connectors provisions these services to any compatible clients, however we prioritize the usability for agentic tools, ensuring our tools are capable enough for LLMs to properly utilize. The following are the clients that can utilize GL Connectors.

#### AI Agents

A configured AI worker that executes instructions, invokes tools, processes attached files, and produces responses. In the context of GL Connectors, these agents utilize GL Connectors to provision their capabilities as a single source of truth. In the context of GL SDK, we provide AI Agents via AI Agent Platform

**Reference:** [AI Agent Platform](https://gdplabs.gitbook.io/sdk/gl-aip)

#### Digital Employee

Digital Employee is an AI-powered automation platform that enables autonomous workflow execution through intelligent agents. GL Connectors also provision the capabilities of Digital Employees.

**Reference**: [Digital Employee](https://gdplabs.gitbook.io/catapa/developer-documentation/digital-employee/digital-employee-architecture)
