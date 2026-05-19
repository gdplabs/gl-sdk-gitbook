---
hidden: true
icon: screwdriver-wrench
---

# Glossary

## A

### APIs

APIs (Application Programming Interface) is a set of functions and procedures allowing the creation of applications that access the features or data of an operating system, application, or other service. We separate it into two types: [#rest-api](glossary.md#rest-api "mention") for remote capabilities (i.e., accessing external services), or [#local-api](glossary.md#local-api "mention") for accessing the local system itself.

**Reference:** [Broken link](/broken/pages/uwTaBgSFKYEUe0Ykv0ci "mention")

### AI Agents

A configured AI worker that executes instructions, invokes tools, processes attached files, and produces responses. In the context of [#gl-connectors](glossary.md#gl-connectors "mention"), these agents utilize GL Connectors to provision their capabilities as a single source of truth. In the context of GL SDK, we provide AI Agents via AI Agent Platform

**Reference:** [AI Agent Platform](https://gdplabs.gitbook.io/gl-aip)

## D

### Digital Employee

Digital Employee is an AI-powered automation platform that enables autonomous workflow execution through intelligent agents. [#gl-connectors](glossary.md#gl-connectors "mention") also provision the capabilities of Digital Employees.

**Reference**: [Digital Employee](https://gdplabs.gitbook.io/catapa/developer-documentation/digital-employee/digital-employee-architecture)

## G

### GL Connectors

GL Connectors is the umbrella project that sits between Clients and the outside world, providing everything agents need to interact with both local systems and external services.

{% hint style="info" %}
In essence: GL Connectors is [#mcp-servers](glossary.md#mcp-servers "mention") + [#skills](glossary.md#skills "mention") + [#apis](glossary.md#apis "mention")
{% endhint %}

### GL Connectors Clients

GL Connectors provisions these services to any compatible clients, however we prioritize the usability for agentic tools, ensuring our tools are capable enough for LLMs to properly utilize. The following are the clients that can utilize GL Connectors:

* [#ai-agents](glossary.md#ai-agents "mention")
* [#digital-employee](glossary.md#digital-employee "mention")
* And other clients that can utilize any component provided by [#gl-connectors](glossary.md#gl-connectors "mention").

## L

### Local API

The communication layer used by GL Connectors to interact with the local system—file access, code execution, system time, etc. Currently accessible through **Agent Skills** and **Agentic Tools** only; HTTP MCP Servers do not support local operations.

## M

### MCP Servers

Model Context Protocol servers hosted by GL Connectors. They expose Third Party Services to any MCP-compatible client, allowing LLMs to discover and invoke operations dynamically without custom code.&#x20;

**Reference:** [agentic-tools-and-model-context-protocol-mcp](sdk/agentic-tools-and-model-context-protocol-mcp/ "mention")

## R

### REST API

The standard HTTP communication layer used by GL Connectors to interact with remote systems—third-party services, external databases, cloud storage, etc. Both Agent Skills and MCP Servers communicate through this layer.

## S

### Skills

Downloadable, reusable agent capabilities sourced from various providers and managed via the GL Connectors SDK. Skills represent higher-level recipes or workflows that extend what an agent can do beyond individual tool calls. Agent Skills can operate over both **REST API** (for remote services) and **Local API** (for filesystem access, code execution, etc.).

**Reference:** [connectors-skills](sdk/connectors-skills/ "mention")

## T

### Tools

Purpose-built interfaces for AI agent development, available through the GL Connectors SDK. Tools are compatible with GL SDK's `BaseTool`, LangChain Tools, and other agent frameworks (LangGraph, CrewAI, etc.), enabling agents to interact with both local capabilities (file uploads, filesystem access, code execution) via [#local-api](glossary.md#local-api "mention") and third-party services via [#rest-api](glossary.md#rest-api "mention") out of the box.

**Reference:** [agentic-tools-and-model-context-protocol-mcp](sdk/agentic-tools-and-model-context-protocol-mcp/ "mention")
