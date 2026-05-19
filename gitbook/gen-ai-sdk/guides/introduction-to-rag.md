---
icon: memo
---

# Introduction to RAG

## What is **Retrieval-Augmented Generation (RAG)** ?

**Retrieval-Augmented Generation (RAG)** is an AI technique that combines the power of large language models with external knowledge sources. Instead of relying solely on the information learned during training, RAG systems can "retrieve" relevant information from databases, documents, or other sources in real-time and use that information to generate more accurate, up-to-date, and contextually relevant responses.

Think of RAG as giving an AI assistant access to a vast library. When you ask a question, the AI doesn't just rely on what it memorized during training - it can quickly search through the library, find relevant books or documents, read the pertinent sections, and then provide an answer based on that current information.<br>

## What does an RAG pipeline entail?

<figure><img src="../../.gitbook/assets/Copy of Diagram Color Guide.png" alt=""><figcaption></figcaption></figure>

The RAG pipeline involves a blend of **retrieval** and **generation**. Here's a breakdown of the steps, as illustrated in the diagram:

{% stepper %}
{% step %}
**Query**

The user submits a question or request.
{% endstep %}

{% step %}
**Embedding**

The query is passed through an **embedding model**, which converts it into a dense vector – a numerical representation that captures the meaning of the text.
{% endstep %}

{% step %}
**Retrieval**

This vector is then used to search a **Vector Database** for similar content. The database returns the most relevant documents or chunks, called **retrieved contexts**.
{% endstep %}

{% step %}
**Augmentation + Generation**

The **retrieved contexts** are combined with the original query and sent to a **Large Language Model (LLM)**. The model uses this enriched input to generate a well-informed response.
{% endstep %}

{% step %}
**Response**

The final answer is returned to the user, grounded in both the model’s knowledge and the external information.
{% endstep %}
{% endstepper %}
