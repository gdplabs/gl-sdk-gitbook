---
icon: arrow-right-arrow-left
---

# Sequence Diagrams

Step-by-step interaction diagrams for GL Smart Crawl Orchestration Layer core operations.

## Diagrams

* [**Listing Process**](sequence-listing-process.md) — How the Orchestration Layer triggers listing jobs, calls the Extraction Layer for URL extraction, and stores discovered URLs in the database
* [**Scraping Process**](sequence-scraping-process.md) — How the Orchestration Layer retrieves pending URLs and calls the Extraction Layer to extract page content

## Usage

All diagrams use Mermaid `sequenceDiagram` syntax and can be rendered in GitBook, GitHub Markdown, and any Mermaid-compatible viewer.

## Updating Diagrams

Keep diagrams in sync with code changes in:
- `app/crawl/service.py` — `CrawlService`
- `app/list/service/` — `ListService` implementations
- `app/crawl/scheduler/service.py` — `CrawlSchedulerService`
