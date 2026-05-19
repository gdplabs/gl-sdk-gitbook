---
icon: list
---

# Feature Overview

**Last update**: April 23, 2026.

The GL SDK is ✨ **ever-growing**, with ✨ **100+ features** available at your disposal. Find the highlights below, or consult the [detailed feature list](./#detailed-features).

<figure><img src="../../.gitbook/assets/Diagram Color Guide.png" alt=""><figcaption></figcaption></figure>

## Highlights :book:

### ✨ [Anonymized Logging](../../gl-observability/guides/logs.md)

Automatically **detect and mask personally identifiable information (PII)** across operations. This intelligent logging system ensures that **sensitive data such as names, email addresses, phone numbers, and other personal identifiers are automatically redacted** or tokenized before being stored in logs, significantly reducing the risk of data exposure if logging systems are compromised. Maintain detailed **operational visibility** for debugging, monitoring, and analytics while ensuring **compliance with privacy regulations and protecting user data integrity**.

### ✨ [GL AI Agents Package (AIP)](/broken/pages/FHWJhfjGs2w6fEuqwYv9)

Build **tailored agent systems that adapt to your tools, models, execution patterns, and governance requirements**. Configure every part of an agent—from **instructions, memory, and model selection to tool/MCP integrations**, runtime overrides, streaming outputs, and artifact handling—within a unified orchestration layer powered by the REST API, Python SDK, and CLI. This flexibility delivers optimal performance and compliance while keeping development and operations simple and consistent.

### ✨ [Build End-to-End RAG  Pipeline](../../gen-ai-sdk/guides/build-end-to-end-rag-pipeline/)

Craft **customized RAG (Retrieval-Augmented Generation) pipelines** that **adapt to their specific data sources, retrieval strategies, and generation requirements**. Rather than being locked into rigid, one-size-fits-all solutions, you can configure every component of the pipeline—from document chunking and embedding models to retrieval algorithms and LLM integrations. This flexibility ensures optimal performance for your unique use case while maintaining the simplicity of a unified orchestration framework.

### ✨ [GL Deep  Researcher](/broken/pages/7fpxvwBTX0sKcehJtGUI)

**Go beyond quick answers**. Instead of relying on a single search, **explore a question from multiple angles, gather the most relevant information, and bring everything together into a clear, well-supported report**. The reports are designed to be comprehensive, detailed, and grounded in evidence—giving users not just an answer, but a full understanding of their topic.

### ✨ [Knowledge Graph](../../gen-ai-sdk/tutorials/knowledge-graph/)

Build intelligent **graph-based RAG systems that understand relationships between entities rather than treating documents as isolated chunks**. Instead of simple keyword matching, the Knowledge Graph SDK extracts entities, relationships, and hierarchical structures from content, creating interconnected knowledge representations that preserve semantic context and enable sophisticated reasoning across connected information. This approach transforms retrieval from basic similarity search into relationship-aware discovery that follows conceptual pathways through your data.

### ✨ [Realtime Session](../../gen-ai-sdk/tutorials/inference/realtime-session.md)

Experience **seamless, natural conversations**, designed to deliver instant, **human-like spoken responses**. Perfect for voice agents and interactive applications, this low-latency solution transforms how users engage with AI by processing continuous audio streams for a truly dynamic and responsive interaction.

### ✨ [GL Smart Search](../../gl-smart-search/getting-started.md)

Experience **a unified search** that connects results from the web and third-party applications such as Google Drive, Gmail, Google Calendar, and GitHub..

***

## Detailed Features :mag:

The ✨ **100+ features** has been organized into categories for easier viewing.

### ✨ [GL Connectors](/broken/pages/hJFZZ1oCoR3ttkby4Gex)

1. [Skills](https://gdplabs.gitbook.io/sdk/gl-connectors/sdk/connectors-skills)
2. [Tools](https://gdplabs.gitbook.io/sdk/gl-connectors/sdk/tools)

Refer to [agentic-tools-and-model-context-protocol-mcp](../../gl-connectors/sdk/agentic-tools-and-model-context-protocol-mcp/ "mention") for a comprehensive documentation and list!

1. Github
2. Twitter / X
3. Google Docs
4. Gmail
5. Google Calendar
6. Google Meet\*
7. Google Sheets
8. Slack
9. SQL
10. Hackernews
11. Microsoft Calendar
12. Microsoft OneDrive
13. Microsoft Outlook
14. Microsoft Teams
15. Microsoft Sharepoint
16. ...and more!

### ✨[GL Deep Researcher](/broken/pages/7fpxvwBTX0sKcehJtGUI)

1. ✨ [Deep Research](/broken/pages/7fpxvwBTX0sKcehJtGUI)

### ✨[GL Identity and Access Management](/broken/pages/gkfqqoK4pLXoS9eTeu0x)

1. [Pluggable Auth Providers](../../gl-identity-and-access-management/tutorials/traditional-iam/enterprise-protocols/ldap-authentication.md)
2. ✨ [Agent IAM & Delegation](../../gl-identity-and-access-management/tutorials/agent-iam/)
3. [Access Control](../../gl-identity-and-access-management/tutorials/traditional-iam/dpop/)

### ✨[GL Observability](/broken/pages/QzR9EqMk8P0pH5Tb39dc)

1. ✨ [Anonymized Logging](../../gl-observability/guides/logs.md)
2. [Open Telemetry](/broken/pages/QzR9EqMk8P0pH5Tb39dc)

### ✨[GL Smart Crawl](/broken/pages/5T158of17azUCUbD6qbH)

1. [Crawler Article from Multiple Sources](https://gdplabs.gitbook.io/sdk/gl-smart-crawl/resources/developer-reference/smart-scrape/scrapers/article-scrapers)
2. [Crawler Property from Multiple Sources](https://gdplabs.gitbook.io/sdk/gl-smart-crawl/resources/developer-reference/smart-scrape/scrapers/property-scrapers)

### ✨[GL Smart Search](../../gl-smart-search/introduction.md)

1. [Connector Search](../../gl-smart-search/guides/sdk/connector-search.md)
2. [Site Discovery](https://gdplabs.gitbook.io/sdk/gl-smart-search/guides/sdk/web-search#id-4.-map-a-website)
3. [Structured Data Web Content Extraction](https://gdplabs.gitbook.io/sdk/gl-smart-search/guides/sdk/web-search#id-6.1-extract-snippets-with-json-schema)
4. [Web Search](../../gl-smart-search/guides/sdk/web-search.md)

### ✨[Multimodal](../../gen-ai-sdk/tutorials/multimodality/)

1. [Image-to-text Modality Converter](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/multimodality/modality-converter/image-to-text-converter)
2. [Audio-to-text Modality Converter](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/multimodality/modality-converter/audio-to-text-converter)
3. [Video-to-text Modality Converter](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/multimodality/modality-converter/video-to-caption)
4. [Image Modality Transformer](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/multimodality/modality-transformer/image-modality-transformer)

### ✨[GL AI Agents Package (AIP)](/broken/pages/FHWJhfjGs2w6fEuqwYv9)

1. [Audio Interface](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/audio-interface)
2. [Filesystem](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/agent-filesystem)
3. [Human-in-the-loop (HITL)](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/human-in-the-loop-approvals)
4. ✨ [Multi-Agent Execution](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/tutorials/multi-agent-system-patterns)
5. [Programmatic Tool Calling (PTC)](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/programmatic-tool-calling)
6. [Skills](https://gdplabs.gitbook.io/sdk/gl-ai-agent-package/guides/skills)

### ✨[Knowledge Graph](../../gen-ai-sdk/tutorials/knowledge-graph/)

1. ✨ [Text-to-Graph](../../gen-ai-sdk/tutorials/knowledge-graph/text-to-graph.md)
2. [Graph Data Store](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/knowledge-graph/graph-data-store)
3. [GraphRAG Indexer](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/document-processing-orchestrator/indexer/graph-rag)
4. [GraphRAG Retriever](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/knowledge-graph/graph-retriever)

### ✨[GL Meemo](/broken/pages/gsJTdBOACmvLG18UpRI2)

1. [Meeting Bot](../../gl-meemo/tutorials/meetings.md)
2. [Transcription](https://gdplabs.gitbook.io/sdk/gl-meemo/introduction-to-meemo)
3. [Summarization](https://gdplabs.gitbook.io/sdk/gl-meemo/introduction-to-meemo)
4. [Calendar Integration](https://gdplabs.gitbook.io/sdk/gl-meemo/introduction-to-meemo)

### ✨[GL Speech](/broken/pages/VBUHNoySnLzCSiJAGkSv)

1. [Speech-to-Text](../../gl-speech/rest-api-reference/speech-to-text.md)
2. [Text-to-Speech](../../gl-speech/rest-api-reference/text-to-speech.md)

### ✨[Computer Vision](/broken/pages/ICApgCMCCZRveNuTNrlQ)

#### OCR

1. [e-KYC](https://docs.glair.ai/vision#e-kyc)
2. [Paperless/Document Intelligence](https://docs.glair.ai/vision/general-document)

#### Retail Execution & Planogram

1. [Retail Execution & Planogram](https://docs.glair.ai/vision/retail/kpi/osa)

#### Identity Verification & Face Verification

1. [Identity Verification & Face Verification](https://gdplabs.gitbook.io/sdk/computer-vision/introduction-to-computer-vision)

#### Face Biometric

1. [Passive Liveness Detection](https://docs.glair.ai/vision/passive-liveness)
2. [Active Liveness Detection](https://docs.glair.ai/vision/active-liveness)
3. [Deepfake Detection](https://docs.glair.ai/vision/deepfake)
4. [Face Verification](https://docs.glair.ai/vision/identity-face-verification)

### ✨[NLP](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/pii-masking)

1. [Named-Entity Recognition (NER)-based Privacy](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy/pii-masking)

### ✨Security

1. Data at Rest
2. Data in Transit / Data in Motion
3. Key Management
4. Data Classification

### ✨[Common Modules](/broken/pages/YoOdbZ0EF0BPnONp4Ocz)

1. [Plugin](https://gdplabs.gitbook.io/sdk/common-modules/tutorials/plugin)
2. [Internationalization](https://gdplabs.gitbook.io/sdk/common-modules/tutorials/internationalization)
3. [Code Interpreter](https://gdplabs.gitbook.io/sdk/common-modules/guides/code-interpreter-usage-guide)

### ✨[Generative AI](../../gen-ai-sdk/introduction-to-gen-ai-sdk.md)

1. [Core (Component, Event Emitter, Tool, etc.)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/core)
2. [Inference (LLM/SLM, Embedding, & Realtime: OpenAI, Anthropic, Google, xAI, etc.)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/inference)
3. [Data Store (ES, OS, Chroma, Redis, SQL, etc.)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/data-store)
4. [Retrieval (Vector, Hybrid, Hierarchical, etc.)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/retrieval)
5. [Generation (Synthesizer, Citations, Context Enricher, etc.)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/generation)
6. [Orchestration (Routing & Pipeline Orchestration)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/orchestration)
7. [Document Processing (Chunker, Indexer, DPO Router, etc.)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/document-processing-orchestrator)
8. [Evaluation (GEval, RAGAS, DeepEval)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/evaluation)
9. [Security & Privacy (Guardrails, PII Masking)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/security-and-privacy)
10. [Memory (Chat history, memory management)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/memory)
11. [Fine-tuning (SFT, DPO, GRPO)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/fine-tuning)
12. [Cache (Eviction Manager, Eviction Strategy)](https://gdplabs.gitbook.io/sdk/gen-ai-sdk/tutorials/cache)



## Why GL SDK? :question:

Unlock your full potential in the AI era. The GL SDK provides the foundation you need to build groundbreaking applications without compromise.

1. **Low Code:** Achieve complex AI tasks in as few as five lines of code, drastically accelerating development and reducing errors.
2. **Simple, But Flexible:** Offers straightforward solutions without sacrificing the granular control needed for advanced use cases.
3. **Low Maintenance:** We handle all the underlying open-source dependency management, updates, and compatibility, so your applications simply "just work."
4. **One-Stop Shop:** The GL SDK provides a comprehensive, integrated solution for building production-ready AI applications.
5. **Designed with Developer Experience in Mind:** Meticulously crafted for intuitive use, quickly making beginners productive.

{% hint style="success" %}
**Learn more about GL SDK's advantages** [**here**](../why-gl-sdk.md)**.**
{% endhint %}
