---
description: >-
  Hierarchy for highlighting the flow from various clients until it receives
  data that it needs from external sources.
hidden: true
icon: sitemap
---

# General Hierarchy Overview

{% hint style="success" %}
This diagram is adapted from [GLChat, AIP, GL SDK - Architecture Block Diagram Slide 6: GL SDK: GDP Labs Software Development Kit](https://docs.google.com/presentation/d/1vV6xMvKZxclBunhFatk__gC2t0xvlDqsYG6x531LSf0/edit?slide=id.g39aef97b903_0_1158#slide=id.g39aef97b903_0_1158)
{% endhint %}

## Block Diagram

<div align="center"><figure><img src="../../.gitbook/assets/Generic Architecture.png" alt=""><figcaption></figcaption></figure></div>

## Term Definitions

1. **GLChat**: Our in-house LLM Chat Client complete with pipeline and inference implementations.
2. **Clients**: The front-end interfaces or autonomous entities that initiate requests to access data or perform actions. This layer aggregates traditional user interfaces (Web, Mobile, Desktop Apps) alongside AI Agents, acting as the consumers of the underlying API layers.
3. **GL Connectors:** Our in-house connectors against third party APIs to provide a synchronized layer for authentication. It can be served over REST API or over MCP for agentic access.
4. **Privacy-First API:** The traditional, standard communication interface used primarily by the Web, Mobile, and Desktop apps. Here, we prioritize API Endpoints that fulfill privacy standards (such as ISO, FIPS, HIPAA, etc.)
5. **Remote Environment:** The backend infrastructure and external systems that serve as the "source of truth" and execution logic. This includes **External Databases, Third-Party Services,** and **External Storage** which are abstracted away from the Clients and accessed strictly through the MCP or REST API layers.
