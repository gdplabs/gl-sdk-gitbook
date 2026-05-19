---
description: >-
  The definition of Tools, APIs, MCPs, Connectors, and everything surrounding
  agentic capabilities.
hidden: true
icon: quotes
cover: >-
  https://images.unsplash.com/photo-1426927308491-6380b6a9936f?crop=entropy&cs=srgb&fm=jpg&ixid=M3wxOTcwMjR8MHwxfHNlYXJjaHwyfHxUb29sfGVufDB8fHx8MTc2NDc0MzQzMHww&ixlib=rb-4.1.0&q=85
coverY: 0
coverHeight: 142
---

# GL Connectors

The term "tools" often mean too many things that the meaning tends to get lost. We're going to clarify what "tools" mean, especially when we talk about AI Agents, and what kind of terms we will use in the future.

We split the terminologies into two different sections:

1. [general-hierarchy-overview.md](general-hierarchy-overview.md "mention")\
   This highlights the hierarchy between general clients until it receives data that it needs from external sources.
2. [ai-agent-hierarchy-overview.md](ai-agent-hierarchy-overview.md "mention")\
   This specifically highlights the hierarchy between APIs and how AI Agents can utilize them in order to achieve their goals.

Alongside the terminology, we will also provide how many tools we currently have in our systems that fit this category.

* [connectors-count.md](connectors-count.md "mention")

## Terminology Quick-Terms

For more details, please check the respective pages to see how they correlate. In this page, we will only give a brief explanation of what terms **we will use moving forward for clarity and consistency**.&#x20;

* **AI Agents:** LLM-driven agents that perform reasoning and invoke Connectors / Agent Tools to interact with the outside world.
* **Connectors**: Blanket term for anything that an AI Agent can interact with directly. It can also be called Agent Tools (interchangeable terms), but for consistency, we shall call it Connectors. This includes both MCP and simply Tools.
* **REST API**: Remote API standards for communication between two systems. The target can be external services, data storage (e.g., databases, caches), external file storage (e.g., S3), etc.
* **Local API**: API standards that allow for communication with the internal system. Includes filesystem (i.e., file access, file write, etc.), system time, system level randomizer, code executions, etc.
