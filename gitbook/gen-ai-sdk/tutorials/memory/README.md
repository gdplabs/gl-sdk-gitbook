---
icon: memo-pad
---

# Memory

## What is memory?

Memory is a core subprocess in our SDK that enables models and applications to retain context across interactions. It ensures that responses can remain coherent, stateful, and efficient by reusing relevant information instead of starting from scratch each time.

The GL SDK currently provides two key components for memory management:

1. [**Chat History Manager**](chat-history-manager.md) – responsible for storing, retrieving, and managing conversation history to maintain contextual continuity.
2. [**Cache Manager** ](/broken/pages/EcGC5XsFAsk5e5uuUhwM)– responsible for caching model outputs or intermediate results to improve performance and reduce redundant computation.
