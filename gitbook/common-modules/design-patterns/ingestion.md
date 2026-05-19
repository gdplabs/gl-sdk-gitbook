---
icon: book-sparkles
---

# Ingestion

## Overview

Language models (LMs) are powerful, but they don’t have information about your private documents. **Ingestion** (or Document Processing Orchestrator–DPO) lets you process documents and store them into a retrieval source (e.g., vector database, graph database, SQL database) so they can be used later in the **Retrieval** process.

At a high level, ingestion enables you to:

1. **Extract** data from documents (e.g., PDF, DOCX, HTML, etc.)
2. **Chunk** the data
3. **Enrich** the data with additional metadata
4. **Index** the data into a retrieval source

## Core Design Pattern

### Structure

<figure><img src="../../.gitbook/assets/image (62).png" alt=""><figcaption></figcaption></figure>

At its core, an ingestion pipeline is a staged, modular flow. Each stage has a single responsibility and produces an explicit artifact (usually a JSON-like intermediate), so you can swap components without rewriting everything. Each stage is also optional, you can mix and match based on your needs.

Typical stages:

1. **Router** – chooses the correct sub-pipeline/component variants (e.g., pick Downloader/Loader/Parser based on file type).
2. **Downloader** – downloads resources from a given source and saves them into files.
3. **Loader** – extracts raw elements/text from a file/source into a standardized intermediate format (text + structure + metadata).
4. **Parser** – refines/derives element structures based on Loader output (e.g., classify into header/title/paragraph/table/image, etc.).
5. **Chunker** – splits structured elements into retrieval-friendly chunks.
6. **Data Generator** – enriches data with more information (e.g., metadata augmentation).
7. **Indexer** – indexes processed data into a datastore (e.g., vector DB, graph RAG).

### Capabilities

In typical ingestion implementations, you’ll often need these capabilities:

* **Multi-source ingestion**: DPO can ingest from different upstream sources via Downloaders (e.g., direct URL, Google Drive, HTML crawlers).
* **Standardized intermediate representation**: Loader outputs a consistent schema (`text`, `structure`, `metadata`) to make downstream processing uniform.
* **Structure-aware parsing**: Parser assigns/normalizes structures (header/title/heading/table/image/etc.), improving chunking and indexing quality.
* **Chunking strategies**: Chunker supports different chunking approaches (e.g., structured element chunking, table chunking).
* **Metadata enrichment**: Data Generator enriches extracted/chunked content with more information.
* **Multi-store indexing**: Indexer supports indexing into different data store targets (e.g., Vector DB, Graph RAG).

## Implementation Patterns

Five implementation patterns are provided below, sorted by customization level (low → high). Use these as “reference architectures” for deciding how much to build vs reuse.

### 1. Minimal Ingestion Pipeline (Fastest to ship)

**Goal:** Quick ingestion for a small number of files without indexing.\
**Data sources:** Local files / direct URLs / Google Drive\
**Customization:** Low

**Composition:**

* Downloader (optional) → Loader

**Notes:**

* Best for prototypes, demos, low-volume ingestion, and no need to store into a data store.
* Keep defaults; avoid branching logic.

**Implementation references:**

1. [simple-dpo-pipeline-loader](../../gen-ai-sdk/guides/build-document-processing-pipeline/simple-dpo-pipeline-loader/ "mention")
2. [downloader](../../gen-ai-sdk/tutorials/document-processing-orchestrator/downloader/ "mention")
3. [loader](../../gen-ai-sdk/tutorials/document-processing-orchestrator/loader/ "mention")

### 2. Enriched Ingestion with Metadata

**Goal:** Improve retrieval quality by enriching content (metadata, tags, derived fields).\
**Data sources:** Same as (1)\
**Customization:** Medium–High (Data Generator logic)

**Composition:**

* Loader/Parser produce clean structure → Chunker → **Data Generator enriches** (e.g., additional metadata fields) → Indexer

**When to use:**

* You want to enrich the data (e.g. add image captioning using LLM)
* You want better filtering, grouping, UI facets, or downstream policy enforcement.
* You want consistent “document identity” signals (file\_id/source link mapping) across sources.

**Implementation references:**

1. [advanced-dpo-pipeline.md](../../gen-ai-sdk/guides/build-document-processing-pipeline/advanced-dpo-pipeline.md "mention")
2. [data-generator](../../gen-ai-sdk/tutorials/document-processing-orchestrator/data-generator/ "mention")

### 3. \[DRAFT] Web Ingestion

**Goal:** Ingest a single URL or a list of URLs with optional keywords, crawl/search the web as needed, extract content, and index the results into a data store for retrieval.\
**Data sources:** from end-users / other services\
**Customization:** Medium–High (Data Generator logic)

{% hint style="danger" %}
Web Ingestion pattern is still a draft. This section is shared to give you a preview of the intended approach. The exact design and implementation details are subject to change.
{% endhint %}

**External services:**

* **Smart Search**:
  * Input: search query / seed URLs
  * Output: list of canonical URLs
* **Smart Crawl**:
  * Input: URL(s)
  * Output: fetched pages + metadata (HTML, title, headers, timestamps, source URL, etc.)

**Composition:**

* Create web ingestion record in database → if URL is supported by Smart Crawl (SC), invoke SC → else invoke Smart Search → (optional) Data Generator enriches → Indexer

**When to use:**

* Your users want to "ingest this website / page / docs site into my knowledge base”
* Your users want to “ingest all pages returned by this search query”

**Implementation references:**

1. [GL Smart Search](../../gl-smart-search/introduction.md)
