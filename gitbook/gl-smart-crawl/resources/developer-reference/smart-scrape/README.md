---
icon: spider
---

# Smart Scrape

This section documents the **Extraction Layer** of GL Smart Crawl (module: `applications/custom-scrapers`, internally referred to as Smart Scrape). It is a domain-specific extraction service that receives a URL and returns structured content by dispatching to the appropriate domain extractor/scraper based on source or URL pattern matching.

## Responsibilities

- **Domain scraping** — Extracts structured article metadata and content from news portals using domain-specific CSS selectors and LD+JSON parsing
- **Property scraping** — Extracts property listing details from real estate sites using multi-strategy approaches (API, LD+JSON, HTML fallback)
- **URL extraction** — Discovers paginated URLs from listing pages for the Orchestration Layer's listing phase
- **General scraping** — Falls back to GL Smart Search (Firecrawl) for unknown or anti-bot protected URLs
- **Financial reports** — Processes IDX annual reports including PDF and XLSX extraction

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/scrape` | Scrape content from a URL and return structured data |
| `POST` | `/extract-urls` | Extract article or property listing URLs from a paginated listing page |
| `GET` | `/health-check` | Service health status |

## Technology Stack

| Component | Technology |
|-----------|-----------|
| API Framework | FastAPI + Uvicorn |
| HTML Parsing | BeautifulSoup4 + lxml |
| Browser Automation | Playwright (with stealth) |
| Content Conversion | markdownify |
| PDF Processing | pdfplumber |
| Data Validation | Pydantic |
| Runtime | Python 3.11–3.12 |

## Documentation

* [**Architecture Diagrams**](architecture-diagrams/) — Block diagram and data flow for the Extraction Layer
* [**Sequence Diagrams**](sequence-diagrams/) — Step-by-step flows for domain scraping, general scraping, and URL extraction
* [**Scrapers**](scrapers/) — Reference for supported article and property scrapers
* [**Implementation**](implementation/) — Implementation-focused documentation for listing extraction, domain scraping, and general scraping internals
