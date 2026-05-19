# Domain Scrape Implementation

This page explains how the GL Smart Crawl **Extraction Layer** (Smart Scrape module) implements domain-specific scraping through `POST /scrape` when the URL matches a known source in `URL_SCRAPER_MAP`.

## 1. Scope and Intent

Domain scrape is the high-accuracy path for known sources.

Its responsibilities are:

- detect known source domains,
- route request to the correct scraper class,
- fetch page content with source-appropriate method,
- parse structured fields with source-specific logic,
- return normalized structured output to the Orchestration Layer.

General scrape is not used in this path unless the domain is not mapped.

## 2. Core Components in Domain Scrape Flow

Main implementation entry points:

- `applications/custom-scrapers/custom_scrapers/app.py` (`/scrape`)
- `custom_scrapers/scraper/helper/scraper_router.py` (`ScraperRouter`)
- `custom_scrapers/scraper/base_scraper.py` (`BaseScraper`)
- `custom_scrapers/scraper/article/article_scraper.py` (`ArticleScraper` base)
- source-specific scraper classes under:
  - `custom_scrapers/scraper/article/*.py`
  - `custom_scrapers/scraper/property/*.py`
  - `custom_scrapers/scraper/annual_report/idx_scraper.py`

High-level flow:

1. Client calls `POST /scrape {source, response_type?, schema?, prompt?}`.
2. `ScraperRouter.get_scraper(...)` matches URL against `URL_SCRAPER_MAP`.
3. If matched, domain-specific scraper is instantiated.
4. Scraper fetches content via BaseScraper fetch strategies.
5. Scraper extracts and validates structured output model.
6. API returns `{message: "Success", content: [...]}`.

## 3. Router Behavior (`ScraperRouter`)

Domain map includes:

- article domains: CNN, CNBC, MetroTV, Bisnis, Kontan, Kontan Data, Bloomberg Technoz,
- property domains: OLX, Rumah123, Lamudi, 99.co, 99.co projects,
- annual report domain: IDX.

Behavior notes:

- domain-specific route has priority,
- `response_type`, `schema`, and `prompt` are ignored for matched domain scrapers,
- unknown domains are routed to `GeneralScraper`.

## 4. Shared Fetch and Extraction Patterns

### 4.1 `BaseScraper.get_content(...)` fetch modes

Smart Scrape source handlers use one of:

- `smart_search`: fetch via Smart Search `/v2/web/page` (SELF_HOST then FIRECRAWL fallback),
- `playwright`: browser-rendered HTML for JS-heavy pages,
- `requests`: direct HTTP request for API-like targets.

### 4.2 `ArticleScraper` shared orchestration

Article scrapers share pipeline:

1. fetch `soup`, markdown, and LD+JSON,
2. clean markdown,
3. extract metadata/content/other fields,
4. validate into `Article` model.

Most article scrapers also call Smart Search keypoints to build `summary`.

## 5. Source-by-Source Domain Scrape Implementation (Articles)

### 5.1 CNN Indonesia (`cnnindonesia.com`)

Implementation context:

- scraper: `CNNScraper`
- base: `ArticleScraper` (smart-search content fetch).

Implementation summary:
CNN scraper uses meta-tag centric extraction for metadata, LD+JSON for highlights/video fields, and markdown cleaning rules tailored to CNN page noise patterns.

Behavior:

- metadata from `meta` tags (`originalTitle`, `author`, `publishdate`, etc.),
- quote/image extraction from cleaned markdown,
- infographic detection through CNN-specific category + element lookup.

### 5.2 CNBC Indonesia (`cnbcindonesia.com`)

Implementation context:

- scraper: `CNBCScraper`
- base: `ArticleScraper`.

Implementation summary:
CNBC scraper combines meta/LD+JSON extraction with CNBC-specific content cleaning and optional comment count retrieval.

Behavior:

- metadata from meta tags and page identifiers,
- content summary via Smart Search keypoints,
- comment count enrichment from CNBC-specific identifiers when available.

### 5.3 Bisnis Indonesia (`bisnis.com`)

Implementation context:

- scraper: `BisnisScraper`
- base: `ArticleScraper`.

Implementation summary:
Bisnis scraper uses `og` metadata + LD+JSON timestamps and custom category resolution logic, with dedicated content cleanup for page artifacts.

Behavior:

- date fields parsed from ISO-like LD+JSON values,
- video URL extraction from embed structures,
- infographic is currently non-primary in Bisnis path.

### 5.4 Kontan (`kontan.co.id`)

Implementation context:

- scraper: `KontanScraper`
- base: `ArticleScraper`.

Implementation summary:
Kontan scraper handles Kontan article layout and metadata normalization, including structured extraction of category, date, and media fields.

Behavior:

- content cleaned from page chrome sections,
- metadata assembled from meta tags + LD+JSON fallbacks,
- output validated as `Article`.

### 5.5 Kontan Data (`pusatdata.kontan.co.id`)

Implementation context:

- scraper: `KontanDataScraper` (extends `KontanScraper`).

Implementation summary:
Kontan Data scraper overrides key fields for pusatdata format: fixed author/category assumptions, custom date extraction, and infographic-oriented output.

Behavior:

- author defaulted to `BPS`,
- category set to infographics flavor,
- date parsed from page-specific "Update" format.

### 5.6 MetroTV News (`metrotvnews.com`)

Implementation context:

- scraper: `MetroTVScraper`
- base: `ArticleScraper`.

Implementation summary:
MetroTV scraper emphasizes robust date fallback and media-heavy content extraction for MetroTV page structures.

Behavior:

- dates sourced from LD+JSON with fallback normalization,
- video URL extraction with MetroTV-specific selectors,
- content cleanup removes "Baca Juga" and sharing artifact blocks.

### 5.7 Bloomberg Technoz (`bloombergtechnoz.com`)

Implementation context:

- scraper: `BloombergTechnozScraper`
- base: `ArticleScraper` with pre/post hooks.

Implementation summary:
Bloomberg scraper has a chaining behavior: it can follow `next article` links and merge content into one combined article payload.

Behavior:

- pre-hook stores next article URL,
- post-hook recursively scrapes next article and merges content fields,
- metadata/category parsing is Bloomberg-specific.

## 6. Source-by-Source Domain Scrape Implementation (Properties)

### 6.1 OLX (`olx.co.id`)

Implementation context:

- scraper: `OLXScraper`
- base: `BaseScraper`.

Implementation summary:
OLX scraper is multi-strategy: API search first (by `ad_id`/keyword), then HTML fallback if API cannot find target listing.

Behavior:

- keyword-reduction API search until hit/miss,
- direct transformation from API `parameters/main_info/locations`,
- HTML fallback parsing when API path fails.

### 6.2 Rumah123 (`rumah123.com`)

Implementation context:

- scraper: `Rumah123Scraper`
- base: `BaseScraper` with Playwright fetch.

Implementation summary:
Rumah123 scraper supports both standard listings and perumahan-baru pages, combining LD+JSON graph fields with script metadata extraction.

Behavior:

- dual metadata path (`properti` vs `perumahan-baru`),
- listing type detection from multiple page cues,
- script parsing for bedrooms/bathrooms/electricity/areas and dates.

### 6.3 Lamudi (`lamudi.co.id`)

Implementation context:

- scraper: `LamudiScraper`
- base: `BaseScraper` with Playwright and custom UA.

Implementation summary:
Lamudi scraper parses LD+JSON + runtime script metadata, supports single listing and dual sale/rent decomposition for mixed listing types.

Behavior:

- detects `SALE_AND_RENT` and emits two structured records (sale + rent),
- price-period detection uses listing type + combined title/description/visual price,
- numeric/date normalization with Lamudi-specific parsing helpers.

### 6.4 99.co (`99.co`)

Implementation context:

- scraper: `NineNineScraper`
- base: `BaseScraper`.

Implementation summary:
99.co scraper is Playwright-first with Smart Search fallback if browser path fails, then extracts structured data from JSON-LD and embedded `props.pageProps`.

Behavior:

- fallback chain: Playwright -> Smart Search fetch,
- address and attributes from nested `pageProps` structures,
- update date parsed from Indonesian "Diperbarui" text.

### 6.5 99.co Projects (`99.co/id/projects`)

Implementation context:

- scraper: `NineNineProjectScraper`

Implementation summary:
Project pages use a dedicated scraper that builds listing IDs from slug/unitSlug and maps project/developer/unit fields into property schema.

Behavior:

- project-specific URL/id composition,
- listing type resolved from page key-detail table,
- fields populated from `props.pageProps.data`.

## 7. Source-by-Source Domain Scrape Implementation (Annual Reports)

### 7.1 IDX (`idx.co.id`)

Implementation context:

- scraper: `IDXScraper`
- domain category: annual report data.

Implementation summary:
IDX scraping validates financial-report URL shape and required query params (`year`, `periode`), calls IDX API for report list, then processes attachments (PDF/XLSX) asynchronously.

Behavior:

- fetches report rows from IDX API endpoint,
- AI-assisted PDF selection for best financial report document,
- XLSX extraction pipeline for structured financial output,
- optional upload of selected PDF to LLM Labs integration.

## 8. Reliability and Error Handling Mechanics

Domain scrape reliability characteristics:

- source mismatch never reaches domain scraper (router fallback handles it),
- per-source parser failures are surfaced as API errors,
- each source can choose optimal fetch method (Playwright, Smart Search, requests),
- structured model validation catches schema drift early.

## 9. Practical Summary

Smart Scrape domain scraping is an adapter architecture:

- URL domain determines scraper implementation,
- each scraper owns source-specific parsing quality,
- shared infrastructure standardizes fetching and output shape,
- Smart Crawl receives consistent structured content while extraction complexity stays encapsulated in Smart Scrape.
