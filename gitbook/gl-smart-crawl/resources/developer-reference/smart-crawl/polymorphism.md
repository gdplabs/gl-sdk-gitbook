# Polymorphism

Polymorphism in GL Smart Crawl means the system uses stable contracts while allowing different implementations behind those contracts.

## Architecture View

At architecture level, polymorphism appears in three boundaries:

1. The Orchestration Layer interacts with extraction through stable interfaces (`/extract-urls`, `/scrape`), not with source-specific scraper classes.
2. The Extraction Layer routes requests to different implementations (domain-specific handler or general fallback) without changing orchestration flow.
3. Persistence and state operations are abstracted behind repository interfaces so storage implementation can evolve without changing orchestration behavior.

Benefits at this level:

1. New source onboarding with minimal orchestration changes.
2. Stable public/internal contracts while implementation evolves.
3. Cleaner separation between workflow control and extraction logic.

## Design View

At design level, polymorphism is organized by execution axis:

1. **Listing strategy polymorphism**: source-specific listers share common lister contracts.
2. **Scrape strategy polymorphism**: `/scrape` supports domain-specific and general fallback paths behind one endpoint contract.
3. **URL extraction polymorphism**: `/extract-urls` supports multiple extractor implementations behind one endpoint contract.
4. **Persistence polymorphism**: repositories expose consistent lifecycle operations independent of concrete storage classes.

Design rules:

1. Depend on contracts, not concrete source handlers.
2. Add behavior through registration/mapping, not orchestration branching.
3. Keep response contracts backward compatible.

## Implementation View (Detailed)

At implementation level, polymorphism is realized in both layers.

### Orchestration Layer

1. `ListService` dispatches by source using `ARTICLE_LISTER_MAP` and `PROPERTY_LISTER_MAP`.
2. Article listers share `BaseArticleLister`; source implementations override `_customized_operation(...)`.
3. Custom-scraper-backed article listers share `CustomScraperArticleLister` and implement:
   - `_get_custom_date_url(...)`
   - `_get_custom_default_url(...)`
   - `_open_source_list(...)`
4. Property listers share `BasePropertyLister` and implement `_build_listing_url(...)`.
5. `ScrapeService.scrape_url(...)` keeps one orchestration contract while dispatching by domain/content type and preserving common status transitions.

### Extraction Layer

1. `/scrape` uses `ScraperRouter.get_scraper(...)`.
2. `ScraperRouter` dispatches known domains via `URL_SCRAPER_MAP`.
3. Unknown domains are routed to `GeneralScraper` (schema-driven fallback path).
4. `/extract-urls` uses `UrlExtractorRouter.get_extractor(...)`.
5. `UrlExtractorRouter` dispatches via `URL_EXTRACTOR_CONFIGS` (domain + path-aware matching).
6. URL extractors share `BaseUrlExtractorScraper` and implement:
   - `extract_urls(...)`
   - `get_page_number(...)`
   - `get_max_page(...)`
7. Scrapers share `BaseScraper`; concrete scraper classes encapsulate source parsing while preserving contract shape.

### Integration and Persistence Contracts

1. Orchestration-side extraction clients reuse `BaseCustomScraperService` for shared transport/error handling.
2. Repository operations are defined through base repository interfaces (ABC), with concrete SQLAlchemy implementations behind them.

### Why this matters

Polymorphism allows GL Smart Crawl to expand source coverage and extraction quality without destabilizing scheduling, checkpointing, and crawl lifecycle state management in the Orchestration Layer.
