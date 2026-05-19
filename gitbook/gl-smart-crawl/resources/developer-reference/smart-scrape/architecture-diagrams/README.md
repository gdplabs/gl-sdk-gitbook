---
icon: diagram-project
---

# Architecture Diagrams

High-level architecture and data flow diagrams for the Extraction Layer (`custom-scrapers` service/module).

## Diagrams

* [**Block Diagram**](block-diagram.md) — Core components of the Extraction Layer: API layer, routing, scraper implementations, and support services
* [**Data Flow Diagram**](data-flow-diagram.md) — Internal lifecycle of a scraping request from acquisition through transformation to serialization

## Usage

All diagrams use [Mermaid](https://mermaid.js.org/) syntax and can be rendered in GitBook, GitHub Markdown, and any Mermaid-compatible viewer.

## Updating Diagrams

Keep diagrams in sync with code changes in:
- `custom_scrapers/app.py` — API entry point
- `custom_scrapers/scraper/helper/` — `ScraperRouter`, `UrlExtractorRouter`
- `custom_scrapers/scraper/article/`, `scraper/property/`, `scraper/general/`
- `custom_scrapers/service/` — `SmartSearchService`, `PlaywrightService`
