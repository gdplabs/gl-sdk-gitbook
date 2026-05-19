---
icon: sitemap
---

# Smart Crawl

This section documents the **Orchestration Layer** of GL Smart Crawl (module: `applications/smart-crawl`). It manages the full crawl lifecycle — scheduling listing and scraping jobs, tracking state in PostgreSQL, migrating data to Elasticsearch, and exposing a Data API to downstream consumers.

## Responsibilities

- **Scheduling** — Per-source APScheduler cron jobs trigger listing and scraping phases daily
- **Listing** — Discovers URLs from sources via the Extraction Layer's `/extract-urls` endpoint and stores them as `PENDING`
- **Scraping** — Fetches content from `PENDING` URLs via the Extraction Layer's `/scrape` endpoint and stores results
- **Data integrity** — FIFO scraping with bi-directional pointers ensures chronological coverage
- **Data API** — Exposes paginated access to crawled data with source integrity metadata
- **Migration** — Batch migrates article data from PostgreSQL to Elasticsearch

## Technology Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI + Uvicorn |
| Database | PostgreSQL (SQLAlchemy, Alembic) |
| Search | Elasticsearch |
| Scheduler | APScheduler (embedded in FastAPI) |
| HTTP Client | httpx (async) |
| Runtime | Python 3.11–3.12 |

## Documentation

* [**Polymorphism**](polymorphism.md) — How GL Smart Crawl uses contract-based polymorphism across architecture, design, and implementation layers.
* [**Architecture Diagrams**](architecture-diagrams/) — Block diagram of Orchestration Layer components and external dependencies
* [**Sequence Diagrams**](sequence-diagrams/) — Step-by-step flows for listing and scraping operations
* [**Implementation**](implementation/) — Implementation-level notes, including source-specific listing behavior
