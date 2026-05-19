---
icon: list-ol
---

# Connectors Count

## Term Definitions

1. **GL Connector:** Connectors that are written by and maintained by GDP Labs. This can be one of:
   1. **GL Connector Tools and MCP**: The tools and MCP Servers hosted within GDP Labs’ infrastructure.
   2. **GL Connector Tool SDK**: Agentic tools that are provided via code and can be implemented and extended further for AI Agents.
      1. **Predefined Tools**: Tools that are preincluded in the SDK and can be used as-is.
      2. **User-defined Tools:** Tools that are custom-made by people creating their own implementations. Done by extending from the SDK’s Core Tool
2. **Curated External MCP Servers**: External MCP Servers from official sources that can directly be used by a compatible MCP Client. **They are not hosted&#x20;**_**nor**_**&#x20;maintained by GDP Labs.**
3. **Provider**: Denotes the application for which certain tools or functionality are created (for example, Github, Google, etc).

## Connector Counts

For the most up to date information, you can click the following endpoint:

{% embed url="https://connector.gdplabs.id/mcps/list" %}

The following are the general statistics of our current toolsets based on the above terms (only production data is taken into consideration):

| Type                                                                                        | Count                               |
| ------------------------------------------------------------------------------------------- | ----------------------------------- |
| [GL Connector Tools and MCP](connectors-count.md#gl-connector-tools-and-mcp)                | 28 Providers (376 Tools)            |
| [Predefined Tools](connectors-count.md#gl-connector-tools-sdk)                              | 66 Tools                            |
| [User-Defined Tools](connectors-count.md#gl-connector-tools-sdk)                            | 31 Tools                            |
| [Curated External MCP Servers (MCP Only)](connectors-count.md#curated-external-mcp-servers) | 97 Providers (968 Tools)            |
| (Total)                                                                                     | **125 Providers** (**1000+ Tools**) |

## [GL Connector Tools and MCP](#user-content-fn-1)[^1]

**GL Connector** is designed so that every integration **automatically exposes both**:

* a **REST API** (system-to-system interface), and
* an **MCP Server** (LLM-to-system interface),

**with no additional development work required.**

Because of this architectural design, **any API Endpoint that exists in the REST API will typically also exist as an MCP Tool** exposed by the connector’s MCP Server. This makes the connector’s capabilities consistently available to both traditional systems and LLM-based agents.

Currently, we have **26 providers**, and a total of **347 exposed as Tools and MCP**.

The complete list of GL Connector Tools can be accessed by opening these links:

* [Broken link](/broken/pages/uwTaBgSFKYEUe0Ykv0ci "mention")
* [agentic-tools-and-model-context-protocol-mcp](../../gl-connectors/sdk/agentic-tools-and-model-context-protocol-mcp/ "mention")
* [connector-mcp-cookbook.md](../../gl-connectors/sdk/agentic-tools-and-model-context-protocol-mcp/connector-mcp-cookbook.md "mention")

## [GL Connector Tools SDK](#user-content-fn-2)[^2]

{% include "../../.gitbook/includes/glconnector-limitations.md" %}

Our Connector SDK allows for tool provisioning via both predefined tools and user-defined tools. Our latest data based on production is as follows:

| Source                                       | Total  |
| -------------------------------------------- | ------ |
| [Predefined Tools](#user-content-fn-3)[^3]   | 66     |
| [User-Defined Tools](#user-content-fn-4)[^4] | 31     |
| **(Total)**                                  | **97** |

## [Curated External MCP Servers](#user-content-fn-5)[^5]

We have also curated MCP Servers (**Providers**) from various official places as listed in this document: [100+ MCP Servers](https://docs.google.com/spreadsheets/d/1n7ZAzwgA9cMNg7PJozaxA4seX6n3LBq3ZbEjgt_pAHw/edit?gid=805864834#gid=805864834). Currently, there are **106** external MCP Servers that we have curated, and this number is expected to continuously increase.

In general, we have categorized the MCP Servers (excluding the ones we host in GL Connector) as such:

| Read or Write  | Total   |
| -------------- | ------- |
| Readonly       | 48      |
| Read and Write | 58      |
| **(Total)**    | **106** |

Note that on the **Readonly** MCP Servers, a lot of them are from the same services, but for different dataset (such as various Gitbook MCP Servers for our documentation, each having their own MCP Servers, or Cloudflare and OpenZeppelin having multiple MCP Servers catered to specific details).

[^1]: The tools and MCP Servers hosted within GDP Labs’ infrastructure.

[^2]: Agentic tools that are provided via code and can be implemented and extended further for AI Agents.

[^3]: Tools that are preincluded in the SDK and can be used as-is.

[^4]: Tools that are custom-made by people creating their own implementations. Done by extending from the SDK’s Core Tool

[^5]: External MCP Servers from official sources that can directly be used by a compatible MCP Client. **They are not hosted&#x20;**_**nor**_**&#x20;maintained by GDP Labs.**
