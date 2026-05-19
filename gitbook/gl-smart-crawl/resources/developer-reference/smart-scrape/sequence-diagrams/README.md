---
icon: arrow-right-arrow-left
---

# Sequence Diagrams

Step-by-step interaction diagrams for Extraction Layer core operations (module: `custom-scrapers`).

## Diagrams

* [**Domain Scrape**](sequence-domain-scrape.md) — How the Extraction Layer routes a known domain URL to a domain-specific scraper and returns structured content
* [**General Scrape**](sequence-general-scrape.md) — How the Extraction Layer handles unknown URLs using `GeneralScraper` with GL Smart Search fallback
* [**URL Extraction**](sequence-url-extraction.md) — How the Extraction Layer extracts paginated listing URLs from article and property index pages

## Usage

All diagrams use Mermaid `sequenceDiagram` syntax and can be rendered in GitBook, GitHub Markdown, and any Mermaid-compatible viewer.

## Updating Diagrams

Keep diagrams in sync with code changes in:
- `custom_scrapers/app.py` — API routing
- `custom_scrapers/scraper/helper/scraper_router.py` — `ScraperRouter`
- `custom_scrapers/scraper/helper/url_extractor_router.py` — `UrlExtractorRouter`
- `custom_scrapers/scraper/general/general_scraper.py` — `GeneralScraper`
