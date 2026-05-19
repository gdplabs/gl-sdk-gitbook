---
description: >-
  Hierarchy that highlights connections between APIs and how AI Agents can
  utilize them in order to achieve their goals.
hidden: true
icon: sitemap
---

# AI Agent Hierarchy Overview

## Block Diagram

<figure><img src="../../.gitbook/assets/MCP Agent Interaction (1).png" alt=""><figcaption></figcaption></figure>

## Term Definitions

1. **AI Agent / Digital Employee:** LLM-driven agents that perform reasoning and invoke Connectors / Agent Tools to interact with the outside world.
2. **GL Connectors**: Anything that an AI Agent can interact with directly. They are created by GDP Labs and are hosted and maintained within our infrastructure. Can be one of the following:
   1. **MCP (Model Context Protocol)**
   2. **Tools**: Interface that can be consumed by AI Agents to execute certain tasks.
3. **REST API / Local API**: Anything that can interact with the Environment such as external databases, storage, internal filesystems, etc. Cannot be used by AI Agents directly.
