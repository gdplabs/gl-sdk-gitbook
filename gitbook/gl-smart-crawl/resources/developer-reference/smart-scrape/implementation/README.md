---
icon: wrench
---

# Implementation

Implementation-focused documentation for GL Smart Crawl **Extraction Layer** internals (`applications/custom-scrapers`, internally referred to as Smart Scrape).

## Documents

* [**Technology Stack**](technology-stack.md) — Major technologies, frameworks, parsing engines, and integrations used by the Extraction Layer.
* [**Appendix: Environment Variables**](appendix-environment-variables.md) — Grouped environment variables for Extraction Layer runtime configuration.
* [**Listing Implementation**](listing-implementation.md) — Detailed implementation flow for `/extract-urls`, extractor routing, pagination handling, and source-specific URL extraction logic.
* [**Domain Scrape Implementation**](domain-scrape-implementation.md) — Detailed implementation flow for `/scrape` on known domains, including source-specific article/property/IDX scraper behavior.
* [**General Scrape Implementation**](general-scrape-implementation.md) — Detailed implementation flow for unknown domains using `GeneralScraper`, schema resolution, Smart Search fallback, and fallback payload behavior.
