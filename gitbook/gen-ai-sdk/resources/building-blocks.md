---
hidden: true
icon: block-brick
---

# Building Blocks

Before you begin building your RAG system using our SDK, let us introduce its building blocks.

Tutorials for the items we describe here are available in the [Broken link](/broken/pages/ngmcKzppgjgdGkpKUgLX "mention") section of this documentation. Feel free to come here whenever you get lost!

## Pipeline Diagram

This diagram shows the positioning of each components in the system. The components involved in this diagram are described below:

{% embed url="https://www.figma.com/board/SmYiKYBsLOW6yOsNwkXHNe/Untitled?node-id=1-2&t=veZUNkZtbk6dndfb-1" %}

## ⚙ Guardrail Enforcer

### Guardrail

{% include "../../.gitbook/includes/coming-soon.md" %}

## ⚙ Router

Decides which processing path to take, given user instruction/question. The SDK provides multiple routing strategies to suit different use cases.

### Semantic Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [semantic-router](../tutorials/orchestration/routing/semantic-router/ "mention") | **Use Case:** [implement-semantic-routing.md](../guides/build-end-to-end-rag-pipeline/implement-semantic-routing.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

Uses embedding models to measure semantic similarity between input and predefined route examples. Best for content-based routing decisions.

<details>

<summary>Features</summary>

1. Semantic similarity-based routing using embedding models
2. Supports custom encoders and vector store indexes
3. Configurable similarity thresholds for fine-tuned routing
4. Route filtering and validation

Note:\
Recommended for content-based routing strategy using Aurelio Labs library or embedding models.

</details>

### LM-Based Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [lm-based-router.md](../tutorials/orchestration/routing/lm-based-router.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

Uses language models to intelligently analyze queries and determine the best route. Provides sophisticated reasoning for routing decisions.

<details>

<summary>Features</summary>

1. Language model-based routing with advanced reasoning
2. Natural language understanding for complex routing logic
3. Flexible routing based on query semantics and context
4. Supports custom prompts and instructions

</details>

### Rule-Based Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | **Tutorial**: [rule-based-router.md](../tutorials/orchestration/routing/rule-based-router.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

Routes queries based on keyword matching and pattern rules. Ideal for deterministic routing logic with explicit control.

<details>

<summary>Features</summary>

1. Keyword and pattern-based routing rules
2. Deterministic routing decisions
3. Fast and lightweight routing
4. Easy to understand and maintain

</details>

### Similarity-Based Router

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/router) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [similarity-based-router.md](../tutorials/orchestration/routing/similarity-based-router.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/router.html)

Uses embedding models to measure semantic similarity. Simpler alternative to semantic router with straightforward similarity matching.

<details>

<summary>Features</summary>

1. Simple embedding-based similarity matching
2. Fast routing with minimal overhead
3. Configurable similarity thresholds
4. Lightweight and easy to implement

</details>

## ⚙ Data Ingestion

### Data Store

[**`gllm-datastore`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-datastore/gllm_datastore) | Related tutorials: [index-your-data-with-vector-data-store.md](../guides/index-your-data-with-vector-data-store.md "mention") [#index-your-data](../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#index-your-data "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_datastore/index.html)

Place to store knowledge a.k.a. the knowledge base.

<details>

<summary>Features</summary>

Supported Data Store Types:

1. Traditional SQL DB (see [API Reference](https://api.python.docs.glair.ai/generative-internal/library/gllm_datastore/api/sql_data_store.html)).
2. Vector DB: Stores information as mathematical vectors for semantic search (see [API Reference](https://api.python.docs.glair.ai/generative-internal/library/gllm_datastore/api/vector_data_store.html)).
3. Graph DB: Stores information as connected networks (see [API Reference](https://api.python.docs.glair.ai/generative-internal/library/gllm_datastore/api/graph_data_store.html)).

</details>

### Document Processing Orchestrator

[**`gllm-docproc`**](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-docproc/gllm_docproc) | Related tutorials: [simple-dpo-pipeline-loader](../guides/build-document-processing-pipeline/simple-dpo-pipeline-loader/ "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_docproc/index.html)

Orchestrates the processing of the documents from ingestion until data store.

<details>

<summary>Features</summary>

1. Supported Types
   1. Document: .docx, .pdf, .pptx, .xlsx
   2. Text: .csv, .html, .java, .js, .jsx, .log, .md, .py, .ts, .tsx, .txt
   3. URL: _any public URL that's not behind protection (e.g. IP block, anti-bot)_
   4. Image (_to text_)_:_ .heic, .heif, .jpg, .jpeg, .png, .webp
   5. Audio (_to text_): .flac, .mp3, .ogg, .wav
   6. YouTube URL _(to text; if not blocked by Google)_
2. Chunking Strategies (_based on this_ [_article_](https://ai.gopubby.com/21-chunking-strategies-for-rag-f28e4382d399))
   1. Structured Chunking
   2. Document-Based Chunking
   3. Table-Aware Chunking
   4. Content-Aware Chunking
   5. Recursive Chunking
3. Data Store
   1. Store data into vector database.
   2. Store data into graph database.
4. Miscellaneous
   1. Extract basic math equation from PDF.
   2. Integration with [Datasaur's LLM Labs](https://llm.datasaur.ai/) (including LLM Labs' Dynamic Chunking).
   3. Customizable (_by extending_ [_gllm-docproc_](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-docproc/gllm_docproc) _library_).

**Limitations (plan to be supported)**

1. Can NOT process video yet.
2. Can NOT store data into tabular database yet.
3. Can NOT support transient processing yet.
   1. e.g. just extract data from document, not chunking or storing it into vector database.

**Limitations (no plan to be supported)**

1. PDF
   1. Can NOT extract advanced math equation.
2. DOCX
   1. Can NOT extract math equation.
3. URL
   1. Can NOT bypass URL behind protection (e.g. IP block, anti-bot).
      1. Might be solved using [FirecrawlDownloader](https://gdplabs.gitbook.io/sdk/resources/document-processing-orchestrator/downloader#firecrawl-downloader) (leverages [Firecrawl](https://www.firecrawl.dev/)).
   2. Can NOT access social media (Facebook, Instagram, X, TikTok).
   3. Can NOT get a specific part from HTML (_as the combination will be infinite_)
      1. Specific projects can still customize the result by extending [gllm-docproc](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-docproc/gllm_docproc) library.
4. Can NOT process executable / package file (e.g. .dmg, .exe, .gz, .tar, .zip)
5. Can NOT process files with proprietary extensions (e.g. .ai, .psd, .dll)
6. Can NOT crawl/scrape URL periodically
   1. Specific projects should be responsible to manage their own scheduler / cron.

</details>

## ⚙ Retrieval

### Query Transformer

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/query_transformer) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial** : [Query Transformation](../tutorials/retrieval/query-transformer.md) | **Use Case**: [query-transformation.md](../guides/build-end-to-end-rag-pipeline/query-transformation.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/query_transformer.html)

Converts natural language into better retrieval queries using Language Model.

<details>

<summary>Features</summary>

1. Enhances query for searching by rephrasing unclear questions or adding missing context.
2. Uses language model to improve your query.
3. Supports various error handling strategy.
4. Current supported transformation strategy:
   1. **One-to-one transformation:**\
      Creates one optimized query from input query; suitable for Step-Back Prompting or HyDE (Hypothetical Document Embeddings).
   2. **Many-to-one transformation**:\
      Combines multiple queries into one optimal query; suitable for query expansion or fusion.
   3. **One-to-many transformation**:\
      Expand query into multiple queries; suitable for query expansion or query decomposition.
   4. **Text-to-sql transformation**:\
      Convert text to SQL; suitable for database querying related questions/instructions.

Note: Use cases may vary depending on the specific retrieval requirements and data characteristics.

</details>

### Multimodal Transformer

{% include "../../.gitbook/includes/coming-soon.md" %}

### Retrieval Parameter Extractor

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/retrieval_parameter_extractor)| [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [retrieval-parameter-extractor.md](../tutorials/retrieval/retrieval-parameter-extractor.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/retrieval_parameter_extractor.html)

Determines optimal search parameters for retrieval operations given a query.

<details>

<summary>Features</summary>

1. Uses LLM to analyze queries and extract parameters; suitable for complex, context-aware parameter extraction.
2. Extracts various retrieval parameters:
   1. **Query**: The search query string.
   2. **Filters**: Metadata filters with operators (eq, neq, gt, gte, lt, lte, in, nin, like).
   3. **Sorting**: Sort conditions with order (asc, desc); suitable for result ordering.
3. Provides validation mechanisms for extracted parameters.
4. Supports dynamic parameter adjustment based on query characteristics.

</details>

### Retriever

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/retriever) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [retriever](../tutorials/retrieval/retriever/ "mention") | **Use Case:** [#create-the-retriever](../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#create-the-retriever "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/retriever.html)

Searches through the knowledge base to find relevant information.

<details>

<summary>Features</summary>

1. Searches through the knowledge base.
2. Finds documents, passages, or data points relevant to your question
3. Supports multiple retrieval strategies such as:
   1. **Vector Search**: Semantic similarity using embeddings.
   2. **Entity Relationships**: Leverages structured knowledge graphs to find information through entity relationships and graph traversal patterns.
   3. **SQL Search**: Enables natural language to SQL conversion for querying structured databases.

</details>

### Chunk Processor

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/chunk_processor) | **Tutorial**: [chunk-processor.md](../tutorials/retrieval/chunk-processor.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/chunk_processor.html)

Processes and optimizes retrieved chunks for better context handling.

{% include "../../.gitbook/includes/untitled (2).md" %}

### Reranker

[**`gllm-retrieval`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-retrieval/gllm_retrieval/reranker) | <mark style="color:green;background-color:green;">Involves EM</mark> | **Tutorial**: [reranker.md](../tutorials/retrieval/reranker.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_retrieval/api/reranker.html)

Reorders retrieved results by relevance and importance.

<details>

<summary>Features</summary>

1. Supports multiple reranking methods, including:
   1. **Similarity-based reranking**: Uses embedding similarity scores; suitable for semantic relevance ranking.
   2. **Text Embedding Inference (TEI)**: Uses TEI models for high-performance reranking; suitable for large-scale applications.
   3. **FlagEmbedding-based reranking**: Uses FlagEmbedding models; suitable for multilingual and specialized domains.
   4. **Cohere Bedrock reranking**: Uses AWS Bedrock Cohere service; suitable for cloud-based, managed reranking.
2. Uses embedding models to calculate relevance scores.
3. Provides configurable ranking thresholds and parameters.
4. Supports fallback to original chunks on error.

</details>

## ⚙ Generation

### Compressor

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/compressor) | **Tutorial**: [compressor.md](../tutorials/generation/compressor.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/compressor.html)

Reduces context size while preserving essential information.

<details>

<summary>Features</summary>

1. Supports multiple compression methods, including:
   1. **LLMLingua compression**: Uses LLMLingua models for intelligent compression; suitable for high-quality content reduction.
   2. **Basic compression**: Standard compression without special algorithms; suitable for simple size reduction.
2. Uses language models to identify and preserve important information.
3. Provides configurable compression ratios and quality thresholds.
4. Supports various compression strategies based on content type and requirements.

</details>

### Context Enricher

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/context_enricher) | **Tutorial**: [context-enricher.md](../tutorials/generation/context-enricher.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/context_enricher.html)

Enhances context with additional metadata and information.

<details>

<summary>Features</summary>

1. Supports multiple enrichment strategies, including:
   1. **Basic context enrichment**: Adds fundamental metadata to chunks; suitable for simple context enhancement.
   2. **Metadata-based enrichment**: Enhances context with detailed metadata information; suitable for comprehensive context building.
2. Uses language models to generate contextual information.
3. Provides configurable enrichment parameters and formatting options.
4. Supports metadata information formatting and structuring.

</details>

### Reference Formatter

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/reference_formatter) | <mark style="color:green;background-color:green;">Involves EM</mark> | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [reference-formatter.md](../tutorials/generation/reference-formatter.md "mention") | **Use Case:** [adding-document-references.md](../guides/build-end-to-end-rag-pipeline/adding-document-references.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/relevance_filter.html)

Formats citations and sources in generated responses.

<details>

<summary>Features</summary>

1. Supports multiple formatting strategies, including:
   1. **Language model-based formatting**: Uses LLM to generate contextual citations; suitable for natural, integrated references.
   2. **Similarity-based formatting**: Uses embedding similarity for reference matching; suitable for precise source attribution.
   3. **Basic formatting**: Standard reference formatting; suitable for simple citation requirements.
2. Uses language models or embedding models to enhance reference quality.
3. Provides configurable citation formats and styles.
4. Ensures proper attribution of information sources.

</details>

### Relevance Filter

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/relevance_filter)| <mark style="color:green;background-color:green;">Involves EM</mark> | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | Tutorial: [relevance-filter.md](../tutorials/generation/relevance-filter.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/relevance_filter.html)

Removes irrelevant information from retrieved context.

<details>

<summary>Features</summary>

1. Supports multiple filtering methods, including:
   1. **Semantic similarity filtering**: Filters based on vector similarity scores; suitable for embedding-based relevance assessment.
   2. **Language model-based filtering**: Uses LLM to determine chunk relevance; suitable for context-aware filtering with high accuracy.
2. Uses embedding models or language models to assess relevance.
3. Provides configurable similarity thresholds and filtering criteria.
4. Supports batch processing for improved performance.

</details>

### Repacker

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/repacker) | **Tutorial**: [repacker.md](../tutorials/generation/repacker.md "mention") | **Use Case:** [#create-the-repacker](../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#create-the-repacker "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/repacker.html)

Packages retrieved chunks into formats optimized for LLM understanding.

<details>

<summary>Features</summary>

1. Supports multiple packing strategies, including:
   1. **Forward packing**: Maintains original chunk order; suitable for preserving document flow
   2. **Reverse packing**: Reverses chunk order; suitable for prioritizing recent or important information
   3. **Sides packing**: Alternates chunks from end and start; suitable for balanced context presentation
2. Provides configurable size limits and delimiter options
3. Supports both chunk-based and context-based packing modes
4. Includes size measurement functions for optimal packing

</details>

### Response Synthesizer

[**`gllm-generation`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-generation/gllm_generation/response_synthesizer) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Tutorial**: [response-synthesizer.md](../tutorials/generation/response-synthesizer.md "mention") | **Use Case:** [#create-the-response-synthesizer](../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#create-the-response-synthesizer "mention") | [API Reference](http://api.python.docs.gdplabs.id/gen-ai/library/gllm_generation/api/response_synthesizer.html)

Generates final responses by combining query, context, and history.

<details>

<summary>Features</summary>

1. Supports multiple synthesis strategies, including:
   1. **Stuff synthesis**: Combines all context into single prompt; suitable for comprehensive responses.
   2. **Static list synthesis**: Uses predefined response templates; suitable for structured, consistent outputs.
2. Uses language models to generate coherent and relevant responses.
3. Supports streaming responses for real-time output.
4. Provides configurable hyperparameters and system prompts.
5. Handles multimodal content and attachments.

</details>

## ⚙ Conversation History, Cache, and Memory Manager

### Chat History Manager

[**`gllm-misc`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-misc/gllm_misc/chat_history_manager) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Related tutorials**: [Chat History](#user-content-fn-2)[^2] | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_misc/api/chat_history_manager.html)

Manages conversation history for consistent and contextual responses.

<details>

<summary>Features</summary>

1. Supports multiple history processing methods, including:
   1. **Similarity-based filtering**: Filters message pairs using embedding similarity; suitable for removing redundant conversations.
   2. **Language model-based processing**: Uses LLM to select relevant message pairs; suitable for intelligent history curation.
2. Uses language models or embedding models to process conversation history.
3. Provides configurable data retention and deletion policies.
4. Supports conversation threading and context management.
5. Handles multiple storage backends.

</details>

### Cache Manager

[**`gllm-misc`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-misc/gllm_misc/cache_manager) | [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] | **Related tutorials**: [Caching Implementation](#user-content-fn-2)[^2] | **Use Case:** [caching.md](../guides/build-end-to-end-rag-pipeline/caching.md "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_misc/api/cache_manager.html)

Caches frequently accessed information for improved response speed.

<details>

<summary>Features</summary>

1. Supports multiple cache backends and strategies.
2. Uses language models to generate cache keys and validate cached content.
3. Provides configurable TTL and invalidation policies.
4. Uses Data Store to store cache information.
5. Supports cache warming and intelligent cache management.

</details>

***

## ⚙ **Inference**

Some components may involve language or embedding models—marked with tag [<mark style="background-color:yellow;">Involves LM</mark>](#user-content-fn-1)[^1] or <mark style="color:green;background-color:green;">Involves EM</mark>. These are the key components that enable seamless inference process:

### **LM Request Processor**

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/blob/main/libs/gllm-inference/gllm_inference/request_processor/lm_request_processor.py) | **Tutorial:** [lm-request-processor.md](../tutorials/inference/lm-request-processor.md "mention") | **Use Case:** [utilize-language-model-request-processor](../guides/utilize-language-model-request-processor/ "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/request_processor.html#gllm_inference.request_processor.LMRequestProcessor)

Provides unified interface for LLM interactions.

<details>

<summary>Features</summary>

1. Integrates prompt builder, LM invoker, and output parser into single interface.
2. Provides unified interface for LLM interactions.
3. Supports multiple LLM providers and configurations.
4. Handles request processing and response management.

</details>

### **Catalog**

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial:** [catalog.md](../tutorials/inference/catalog.md "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/catalog.html)

Stores and creates LM request processors or prompt builders from external data sources.

<details>

<summary>Features</summary>

1. Supports multiple data sources, including:
   1. **Record-based creation**: Creates processors from structured records; suitable for predefined configurations.
   2. **Google Sheets integration**: Creates processors from Google Sheets data; suitable for collaborative configurations.
   3. **CSV file processing**: Creates processors from CSV files; suitable for bulk configuration management.
2. Provides automated processor creation from external data.
3. Supports dynamic configuration updates.
4. Enables easy deployment and management of LLM processors.

</details>

### **Prompt Builder**

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [prompt-builder.md](../tutorials/inference/prompt-builder.md "mention")| **Use Case**: [utilize-language-model-request-processor](../guides/utilize-language-model-request-processor/ "mention") | [API Reference](https://api.python.docs.glair.ai/generative-internal/library/gllm_inference/api/catalog.html#gllm_inference.catalog.PromptBuilderCatalog)

Constructs prompts from templates and dynamic content.

<details>

<summary>Features</summary>

1. Supports variable substitution and conditional logic.
2. Handles different prompt formats and structures.
3. Provides template-based prompt construction.
4. Supports dynamic content integration.

</details>

### **LM Invoker**

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/catalog) | **Tutorial**: [lm-invoker](../tutorials/inference/lm-invoker/ "mention")| **Use Case:** [utilize-language-model-request-processor](../guides/utilize-language-model-request-processor/ "mention") | [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/lm_invoker.html)

Provides unified interface for interacting with multiple LM providers.

<details>

<summary>Features</summary>

1. Supports multiple providers: OpenAI, Anthropic, Google, etc.
2. Handles streaming, batching, and error management.
3. Provides unified interface for different LLM services.
4. Supports configurable model parameters and settings.

</details>

### **Output Parser**

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/output_parser) | **Tutorial**: [Broken link](/broken/pages/jxutRrloFx1b9wbYjoDG "mention")| **Use Case:** [produce-consistent-output-from-lm.md](../guides/utilize-language-model-request-processor/produce-consistent-output-from-lm.md "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/output_parser.html)

Extracts structured information from LM responses.

<details>

<summary>Features</summary>

1. Validates response format and content.
2. Handles parsing errors gracefully.
3. Supports structured output extraction.
4. Provides configurable parsing rules and validation.

</details>

### **EM Invoker**

[**`gllm-inference`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-inference/gllm_inference/em_invoker) | **Tutorial**: [em-invoker.md](../tutorials/inference/em-invoker.md "mention") | **Use Case:** [#index-your-data](../guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline.md#index-your-data "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_inference/api/em_invoker.html)

Provides unified interface for interacting with multiple EM providers.

<details>

<summary>Features</summary>

1. Converts text to vector representations.
2. Supports multiple embedding providers and models.
3. Provides unified interface for embedding operations.
4. Handles batch processing and error management.

</details>

## :gear: Orchestration

### Pipeline

[**`gllm-pipeline`**](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/pipeline.html) | **Tutorial**: [pipeline.md](../tutorials/orchestration/pipeline.md "mention")| **Use Case**: [build-end-to-end-rag-pipeline](../guides/build-end-to-end-rag-pipeline/ "mention")[execute-a-pipeline.md](../guides/execute-a-pipeline.md "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/index.html)

Sequences and manages the execution of the components in our SDK.

### Steps

[**`gllm-pipeline`**](https://github.com/GDP-ADMIN/gl-sdk/tree/main/libs/gllm-pipeline/gllm_pipeline/steps) | **Tutorial**: [steps](../tutorials/orchestration/steps/ "mention")| **Use Case**: [build-end-to-end-rag-pipeline](../guides/build-end-to-end-rag-pipeline/ "mention")| [API Reference](https://api.python.docs.gdplabs.id/gen-ai/library/gllm_pipeline/api/steps.html)

The building block of a Pipeline: reads from the state, performs an operation, and writes results back.

[^1]: This component may involve Language Model (LM). See tutorial about LM Request Processor or related [here](building-blocks.md#lm-request-processor)

[^2]: Coming soon!
