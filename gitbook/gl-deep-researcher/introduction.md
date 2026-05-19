---
icon: lightbulb-on
---

# Introduction to GL Deep Researcher

> This page focuses on using the GL Deep Researcher as a component within an RAG pipeline.
>
> If you’re interested in a centralized, end-to-end **Deep Research service in GL Ecosystem**, see the\
> [**GL Open DeepResearch GitBook**](https://gdplabs.gitbook.io/gl-deepresearch) for a deeper dive.
>
> For documentation specific to the **GL Open DeepResearch service** (API, profiles, deployment), start with the [GL Open DeepResearch Overview](https://gdplabs.gitbook.io/gl-open-deepresearch/gl-open-deepresearch/overview) or [GL Open DeepResearch Documentation](https://github.com/GDP-ADMIN/gl-deep-research/blob/main/applications/gl-deep-research/docs/gl-deepresearch-introduction.md).

## What’s a GL Deep Researcher?

A **GL Deep Researcher** is a specialized component that performs **structured, multi-step research** within a Retrieval-Augmented Generation (RAG) pipeline. Instead of issuing a single retrieval query, it is designed to **plan, execute, and refine research steps** to produce a coherent, high-quality result.

GL Deep Researchers can search across multiple sources, reason over intermediate findings, and iteratively adjust their approach as new information is discovered. This makes them well-suited for tasks that **require depth, comparison, or synthesis**—where a single-pass retrieval would be insufficient.

By encapsulating research logic into a dedicated component, GL Deep Researchers enable RAG pipelines to move beyond basic retrieval and toward **goal-driven, reasoning-aware research workflows**.

## Available Subclasses

The Deep Researcher module provides the following built-in implementations:

1. `GoogleDeepResearcher`
2. `OpenAIDeepResearcher`
3. `ParallelDeepResearcher`
4. `PerplexityDeepResearcher`
5. `GLOpenDeepResearcher`

## Next Steps

1. Begin building by installing prerequisites in [prerequisites.md](prerequisites.md "mention")
2. Get started with Deep Researcher components: [getting-started.md](getting-started.md "mention")
3. Explore more about deep researcher subclasses and features in [API reference page](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/deep_researcher.html)
