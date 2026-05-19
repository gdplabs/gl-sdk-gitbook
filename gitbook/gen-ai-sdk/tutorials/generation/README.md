---
icon: wand-magic-sparkles
---

# Generation

## What is generation?

Generation is a core subprocess in our SDK that focuses on producing the final output of an RAG (Retrieval-Augmented Generation) pipeline. This output typically consists of two parts:

1. **Response** – the synthesized answer, typically produced by the language model.
2. **References** – the relevant sources used to generate the response.

To support this workflow, the GL SDK provides the following components:

1. [**Compressor**](compressor.md) - For packaging many passages into a single prompt context to reduce token count.
2. [**Context Enricher**](context-enricher.md) - For adding useful context (e.g. metadata) into retrieved chunks before they’re passed to the language model.
3. [**Deep Researcher**](deep-researcher.md) - For performing a deep research operation within an RAG pipeline with ease.
4. [**Reference Formatter**](reference-formatter.md) - For filtering and formatting the references in a clear, standardized format.
5. [**Relevance Filter**](relevance-filter.md) - For filtering context chunks based on their relevance with the user query.
6. [**Repacker**](repacker.md) - For rearranging a list of content chunks into an order that’s more effective for downstream model consumption.
7. [**Response Synthesizer**](response-synthesizer.md) - For synthesizing the response based on the provided inputs and contexts.
