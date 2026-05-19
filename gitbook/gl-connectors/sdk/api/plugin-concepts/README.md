---
icon: circle-plus
---

# Creating Custom Plugins

GL Connectors is built on a modular plugin architecture using GL SDK's [plugin](../../../../common-modules/tutorials/plugin/ "mention"). Every connector — whether it's GitHub, Google Drive, or a custom integration — is a plugin that plugs into a shared framework for routing, authentication, and service injection. This architecture allows a single plugin to power both REST API endpoints and MCP servers simultaneously, with zero code duplication.

This section covers everything you need to understand and extend the plugin system.

### [creating-custom-plugins](creating-custom-plugins/ "mention")

Learn how to build your own connector plugins using the GL Connectors SDK Plugin Architecture. This page walks you through creating both simple HTTP plugins for basic endpoints and Third Party Integration plugins that handle OAuth2 flows, token storage, and multi-user integration management. You'll also find guidance on registering your plugin into the GL Connectors system.

#### [http-plugin-concepts.md](creating-custom-plugins/http-plugin-concepts.md "mention")

A deep dive into the core building blocks that make the plugin system work. This page covers the HTTP Handler and how it provides framework-agnostic routing, the action-oriented API design pattern (and why we favor it over traditional REST), injected services like authentication and caching, the multi-tenant authentication model (Clients, Users, and Integrations), and how MCP servers are automatically generated from your existing routes.

#### REST and MCP: Dual Exposure

GL Connectors automatically exposes every plugin as both a REST API and an MCP server from a single codebase. This page explains how the [mcp-handler-advanced.md](creating-custom-plugins/plugin-handler/mcp-handler-advanced.md "mention") translates your plugin's HTTP routes into MCP tools, how authentication works consistently across both interfaces, and what limitations exist due to MCP's JSON-RPC specification (such as file operations and callback-based flows).

### [custom-configurations](custom-configurations/ "mention")

Some connectors require setup beyond standard OAuth2 — for example, API keys, workspace IDs, or other provider-specific settings. This page explains how to use the custom configuration system to define and collect these values during plugin activation, giving users a flexible way to configure integrations that don't fit the typical authentication flow.
