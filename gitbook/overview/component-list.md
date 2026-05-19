---
hidden: true
icon: list
---

# Component List

**Last update**: November 17, 2025.

The GL SDK is ✨ **ever-growing**, with ✨ **50+ types of components** available at your disposal. Please find the complete list below:

## AI Agents Package

Useful for building dynamic agents.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/gl-aip/resources/reference/python-sdk">Python SDK</a></td><td>Python client library for building and managing AI agents, tools, and connections with session-aware support aligned to the FastAPI backend.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/gl-aip/resources/reference/cli-commands">CLI Commands</a></td><td>Command-line interface that enables users to manage agents, tools, and MCP connections without writing code.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/gl-aip/resources/reference/rest-api">REST API</a></td><td>Backend interface for managing agents, tools, MCP connections, language models, accounts, and utilities.</td></tr></tbody></table>

## Document Processing

Useful for processing raw documents into a useable knowledge.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/document-processing-orchestrator/downloader">Downloader</a></td><td>Downloads data from a designated source.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/document-processing-orchestrator/loader">Loader</a></td><td>Loads data content.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/document-processing-orchestrator/parser">Parser</a></td><td>Parses data into a structured format.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/document-processing-orchestrator/chunker">Chunker</a></td><td>Chunks data with certain strategy.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/document-processing-orchestrator/data-generator">Data Generator</a></td><td>Generates additional information for the data.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/document-processing-orchestrator/indexer">Indexer</a></td><td>Indexes data into data stores.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/document-processing-orchestrator/dpo-router">DPO Router</a></td><td>Routes data to determines processing paths.</td></tr></tbody></table>

## Evaluator

Useful for performing evaluation of certain modules.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="../gen-ai-sdk/tutorials/evaluation/evaluate-helper-function.md">End-to-End Evaluation</a></td><td>Orchestrates the entire evaluation process, from data loading to result tracking, in a single function call.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/evaluation/evaluator/">Evaluator / Scorer</a></td><td>Evaluates modules using certain metrics.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/evaluation/metric/">Metric</a></td><td>Measures and assesses the performance of language models.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/evaluation/dataset.md">Dataset</a></td><td>It provides a standardized interface to load data, iterate through them, and expose them in a consistent format.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/evaluation/experiment-tracker.md">Experiment Tracker</a></td><td>It logs model inputs/outputs, evaluation scores, configuration parameters, timestamps, and aggregated results to compare runs, reproduce them, and monitor performance changes over time.</td></tr></tbody></table>

## Fine-Tuning

Useful for fine-tuning models.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/fine-tuning/supervised-fine-tuning-sft">SFT Trainer</a></td><td>Manages Supervised Fine-Tuning (SFT) life-cycle.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/fine-tuning/group-relative-policy-optimization-grpo.md">GRPO Trainer</a></td><td>Manages Group Relative Policy Optimization (GRPO) life-cycle.</td></tr></tbody></table>

## i18n/l10n

Useful for implementing i18n (internationalization) & l10n (localization).

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/internationalization/language-detection">Language Detector</a></td><td>Detects the language of a text.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/internationalization/text-normalization">Text Normalizer</a></td><td>Normalizes text into a standard, canonical form.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/internationalization/transliteration">Transliterator</a></td><td>Converts text between writing systems.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/internationalization/translation">Translator</a></td><td>Translates text between languages.</td></tr></tbody></table>

## Model Context Protocol

Useful for working with MCP (Model Context Protocol)s.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="../common-modules/tutorials/tools/mcp-client.md">MCP Client</a></td><td>GDP Labs' in-house MCP Client, framework-agnostic and adaptable to other agentic frameworks.</td></tr><tr><td><a href="/broken/pages/A2YFoQ4N2x1TWWoyHz4e">GL Connector</a></td><td>GDP Labs' maintained Connectors for third party applications.</td></tr></tbody></table>

## Multimodality

Useful for working with multimodal data.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="../gen-ai-sdk/tutorials/multimodality/modality-converter/">Modality Converter</a></td><td>Transform data from one modality to another (e.g., audio → text, image → text, video → text).</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/multimodality/modality-converter/video-to-caption.md">Video to Caption Converter</a></td><td>Converts video files into natural language captions using multimodal language models, suitable for search, RAG, or analytics workflows.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/multimodality/modality-transformer/">Modality Transformer</a></td><td>Wrapper <code>Component</code> that transform an input modality into other modalities using one or more modality converters.</td></tr></tbody></table>

## Retrieval-Augmented Generation

Useful for building dynamic Retrieval-Augmented Generation (RAG) pipelines.

### Core

Useful for managing shared functionality across the RAG components.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="../gen-ai-sdk/tutorials/core/component.md">Component</a></td><td>Basic executable unit; foundation of all Gen AI components.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/core/tool.md">Tool</a></td><td>MCP-style schema to provide functionalities to an AI agent.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/core/logger-manager.md">Logger Manager</a></td><td>Manages logging across Gen AI apps.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/core/event-emitter.md">Event Emitter</a></td><td>Manages event emitting (including streaming) across Gen AI apps.</td></tr></tbody></table>

### Inference

Useful for managing model inferences.

<table><thead><tr><th width="205.4019775390625">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/inference/em-invoker">EM Invoker</a></td><td>Invokes embedding models.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/inference/lm-invoker">LM Invoker</a></td><td>Invokes language models.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/inference/prompt-builder">Prompt Builder</a></td><td>Manages prompts as language models inputs.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/inference/output-parser">Output Parser</a></td><td>Parses language model outputs.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/inference/lm-request-processor">LM Request Processor</a></td><td>Orchestrates language model invocation end-to-end process, which includes prompt building, invocation, and output parsing.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/inference/realtime-chat">[BETA] Realtime Chat</a></td><td>Interacts with language models in realtime.</td></tr></tbody></table>

### Data Store

Useful for managing data stores.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/data-store">Data Store</a></td><td>Stores data for knowledge management.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/data-store/cache-manager">Cache</a></td><td>Enables caching management using data stores.</td></tr></tbody></table>

### Retrieval

Useful for managing knowledge retrieval.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/retrieval/query-transformer">Query Transformer</a></td><td>Transforms query to improve retrieval.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retrieval-parameter-extractor">Retrieval Parameter Extractor</a></td><td>Extracts retrieval parameters from query.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/retrieval/retriever">Retriever</a></td><td>Retrieves knowledge from a designated source.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/retrieval/chunk-processor">Chunk Processor</a></td><td>Transforms retrieved chunks.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/retrieval/reranker">Reranker</a></td><td>Reranks retrieved chunks.</td></tr></tbody></table>

### Generation

Useful for managing response generation.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/generation/context-enricher">Context Enricher</a></td><td>Enriches chunks with additional information.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/generation/relevance-filter">Relevance Filter</a></td><td>Filters chunks based on relevance.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/generation/repacker">Repacker</a></td><td>Repacks chunks as a context.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/generation/compressor">Compressor</a></td><td>Compresses context for compacity.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/generation/response-synthesizer">Response Synthesizer</a></td><td>Synthesizes response based on provided inputs.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/generation/reference-formatter">Reference Formatter</a></td><td>Manages reference formatting based on the response.</td></tr></tbody></table>

### Memory

Useful for managing memory.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/memory/chat-history-manager">Chat History Manager</a></td><td>Manages chat history.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/memory/long-term-memory">Memory Manager</a></td><td>Manages memory.</td></tr></tbody></table>

### Pipeline

Useful for managing pipeline building process.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/orchestration/pipeline">Pipeline</a></td><td>Orchestrates RAG components as pipelines.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/orchestration/steps">Step</a></td><td>Manages various step behavior in a pipeline.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/orchestration/routing">Router</a></td><td>Routes inputs into the most appropriate output.</td></tr><tr><td><a href="https://gdplabs.gitbook.io/sdk/tutorials/orchestration/composer">[BETA] Composer</a></td><td>Builds pipeline with builder patterns.</td></tr></tbody></table>

## Security & Privacy

Useful for managing security & privacy.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="../gen-ai-sdk/tutorials/security-and-privacy/guardrail/">Guardrail</a></td><td>Manages content filtering and safety checks.</td></tr><tr><td><a href="../gen-ai-sdk/tutorials/security-and-privacy/pii-masking.md">PII Anonymizer</a></td><td>Anonymizes PII (Personal Identifiable Information) data.</td></tr></tbody></table>

## Smart Search

Useful for performing smart knowledge retrievals.

<table><thead><tr><th width="209.3819580078125">Component</th><th>Description</th></tr></thead><tbody><tr><td><a href="../gl-smart-search/guides/sdk/web-search.md">Web Search</a></td><td>The <strong>Web Search</strong> module enables you to perform searches across the web, retrieve URLs, fetch page content, and extract structured insights such as snippets or keypoints.</td></tr><tr><td><a href="../gl-smart-search/guides/sdk/connector-search.md">Connector Search</a></td><td>The <strong>Connector</strong> capability lets Smart Search access third-party data sources such as <strong>Google Drive</strong>, <strong>Google Mail</strong>, <strong>Google Calendar</strong>, and <strong>GitHub</strong>.</td></tr></tbody></table>

## Why GL SDK? :question:

Unlock your full potential in the AI era. The GL SDK provides the foundation you need to build groundbreaking applications without compromise.

1. **Low Code:** Achieve complex AI tasks in as few as five lines of code, drastically accelerating development and reducing errors.
2. **Simple, But Flexible:** Offers straightforward solutions without sacrificing the granular control needed for advanced use cases.
3. **Low Maintenance:** We handle all the underlying open-source dependency management, updates, and compatibility, so your applications simply "just work."
4. **One-Stop Shop:** The GL SDK provides a comprehensive, integrated solution for building production-ready AI applications.
5. **Designed with Developer Experience in Mind:** Meticulously crafted for intuitive use, quickly making beginners productive.

{% hint style="success" %}
**Learn more about GL SDK's advantages** [**here**](why-gl-sdk.md)**.**
{% endhint %}
