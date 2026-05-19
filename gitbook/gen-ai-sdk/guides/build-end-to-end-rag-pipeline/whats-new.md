# What's New

### Changed — September 2025

We refactored the **RAG pipeline architecture** to simplify the way responses are synthesized and remove unnecessary intermediate steps.

#### Key Updates

1. **Repacker removed**\
   The `repacker` is no longer defined as a standalone step in the pipeline. Context is now passed directly without a separate repacking process.
2. **Bundle step removed**\
   The `bundle()` step and `response_synthesis_bundle` state key have been eliminated. State variables (`query`, `context`, toggle flags, etc.) are now passed directly to downstream components.
3. **RAGState streamlined**\
   The `RAGState` no longer references or maintains `response_synthesis_bundle`. This reduces overhead and makes state handling more explicit.
4. **ResponseSynthesizer refactored**\
   The `ResponseSynthesizer` has been reworked to use the **stuff strategy** (other available strategy includes stuff\_preset and static\_list), allowing it to directly consume the necessary inputs (`query`, `context`, and additional flags such as `use_knowledge_base`). This makes the design more transparent and flexible.

#### Tutorials Affected

These changes apply to all tutorials that extend **Your First RAG Pipeline**:

* Your First RAG Pipeline
* Dynamic Step
* Implement Semantic Routing
* Adding Document References
* Simple Guardrail
* Query Transformation
* Multimodal Input Handling
* Caching
* RAG with Dynamic Models
