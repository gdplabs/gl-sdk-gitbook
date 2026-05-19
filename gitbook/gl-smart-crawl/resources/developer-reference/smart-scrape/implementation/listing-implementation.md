# Listing Implementation

This page explains how the GL Smart Crawl **Extraction Layer** (Smart Scrape module) implements listing URL extraction through `POST /extract-urls`, including extractor routing, pagination handling, and source-specific behavior.

## 1. Scope and Intent

In GL Smart Crawl architecture, listing discovery is orchestrated by the Orchestration Layer, while the Extraction Layer provides URL extraction as a service.

Extraction Layer listing responsibilities are:

- receive a listing/search/tag URL,
- route to the correct extractor implementation,
- fetch page content using source-specific fetch strategy,
- extract candidate URLs and pagination metadata,
- return normalized response shape to the Orchestration Layer.

## 2. Core Components in Listing Flow

Main implementation entry points:

- `applications/custom-scrapers/custom_scrapers/app.py` (`/extract-urls` endpoint)
- `custom_scrapers/scraper/helper/url_extractor_router.py` (`UrlExtractorRouter`)
- `custom_scrapers/scraper/base_url_extractor_scraper.py` (`BaseUrlExtractorScraper`)
- source-specific extractor classes under:
  - `custom_scrapers/scraper/article/*_url_extractor_scraper.py`
  - `custom_scrapers/scraper/property/*_url_extractor_scraper.py`

High-level flow:

1. Client calls `POST /extract-urls` with `{source}`.
2. `UrlExtractorRouter.get_extractor(source)` selects extractor by domain and path rule.
3. Extractor fetches content via `BaseScraper.get_content(...)`.
4. Extractor runs:
   - `extract_urls(soup)`
   - `get_page_number(source)`
   - `get_max_page(soup)`
5. API returns `UrlExtractorResponse`.

## 3. Listing Response Model

Smart Scrape returns `UrlExtractorResponse`:

- `urls`: extracted candidate URLs,
- `page`: current page number (normalized to `>= 1`),
- `total_urls`: number of URLs in current response,
- `max_page`: optional detected maximum page,
- `metadata`: optional source-specific metadata (used by OLX API extractor).

## 4. Routing Strategy (`UrlExtractorRouter`)

`UrlExtractorRouter` uses `URL_EXTRACTOR_CONFIGS` with:

- domain-level mapping (`cnnindonesia.com`, `lamudi.co.id`, `api.olx.co.id`, etc.),
- optional path-specific extractor override (example: `lamudi.co.id` + `proyek-baru`).

Behavior:

- most specific path config is checked before default `*`,
- if no mapping matches, request fails with `No URL extractor found`.

## 5. Shared Base Behavior (`BaseUrlExtractorScraper`)

Common listing workflow is implemented in `BaseUrlExtractorScraper.scrape(...)`:

1. fetch soup via `get_content(source, options=OPTIONS)`,
2. extract URL list from `extract_urls(soup)`,
3. derive page from `get_page_number(source)`,
4. derive pagination bound from `get_max_page(soup)`,
5. return normalized response.

Helper methods support page extraction from:

- query string (`?page=...`, `?hlmn=...`, etc.),
- path patterns (`/page/{n}`),
- pagination links text.

## 6. Source-by-Source Listing Implementation (Articles)

### 6.1 CNN Indonesia (`cnnindonesia.com`)

Implementation context:

- extractor: `CNNUrlExtractorScraper`
- fetch: Playwright with scroll + `networkidle` wait.

Implementation summary:
CNN listing extraction uses robust multi-selector and generic-link fallback. It filters non-article paths and keeps URLs that contain article-like timestamp/id patterns.

Behavior:

- selectors for list/grid/article layouts,
- strict skip patterns (`/tag/`, `/category/`, `/search`, anchors, js/mail links),
- page from query `page`,
- max page from CNN pagination container.

### 6.2 CNBC Indonesia (`cnbcindonesia.com`)

Implementation context:

- extractor: `CNBCUrlExtractorScraper`

Implementation summary:
CNBC extractor normalizes URLs and keeps only article links with expected path structure (3 path segments), reducing non-content links.

Behavior:

- multi-layout selectors (`group` card/list/grid),
- page from query `page`,
- max page from pagination containers and fallback `href` scanning.

### 6.3 Bisnis Indonesia (`bisnis.com`)

Implementation context:

- extractor: `BisnisUrlExtractorScraper`

Implementation summary:
Bisnis extractor collects article links from `a.artLink.artLinkImg`, normalizes to absolute URL, and deduplicates while preserving order.

Behavior:

- page from query `page`,
- max page from hidden `#total_page`, paging label text, or paging link numbers.

### 6.4 Bloomberg Technoz (`bloombergtechnoz.com`)

Implementation context:

- extractor: `BloombergTechnozUrlExtractorScraper`

Implementation summary:
Bloomberg Technoz extractor supports multiple container layouts and parses both `pagenum` query links and numeric pagination links.

Behavior:

- container-based link extraction (`blockbox` variants),
- page from query `pagenum`,
- max page from `pagenum` link analysis.

### 6.5 MetroTV News (`metrotvnews.com`)

Implementation context:

- extractor: `MetroTVUrlExtractorScraper`
- fetch: Playwright with scroll.

Implementation summary:
MetroTV extractor targets `/read/` and `/play/` links and normalizes MetroTV-relative URLs. Pagination is converted from MetroTV 0-based query to 1-based output.

Behavior:

- selector: `a[href*="/read/"], a[href*="/play/"]`,
- page from query `page` (`0 -> 1`, `1 -> 2`, etc.),
- `max_page` intentionally unavailable (`None`) because only next/prev style navigation exists.

### 6.6 Kontan (`kontan.co.id`)

Implementation context:

- extractor: `KontanUrlExtractorScraper`
- fetch: Playwright with explicit desktop UA.

Implementation summary:
Kontan extractor parses card blocks (`sp-hl linkto-black`) and supports old-style `per_page` pagination semantics.

Behavior:

- keeps HTTPS absolute URLs,
- page derived from `per_page` offset logic (`per_page / 20 + 1`),
- max page from numeric links in `ul.cd-pagination`.

### 6.7 Kontan Data (`pusatdata.kontan.co.id`)

Implementation context:

- extractor: `KontanDataUrlExtractorScraper`
- fetch: custom Playwright loop with repeated "load more" clicks.

Implementation summary:
Kontan Data has no classic paged index. Extractor repeatedly clicks "Selanjutnya" until no-more-data signal appears, then extracts URLs from loaded cards.

Behavior:

- source card selector: `div.title-n a`,
- page fixed as `1`,
- `max_page` unavailable (`None`) due load-more pattern.

### 6.8 Google News (`news.google.com`)

Implementation context:

- extractor: `GoogleNewsUrlExtractorScraper`

Implementation summary:
Google News extractor collects `read/articles` links and normalizes relative links to absolute Google News URLs only.

Behavior:

- accepts `/read/` and `/articles/` patterns,
- rejects external domains,
- page fixed as `1`,
- `max_page` is `None` (infinite-scroll style behavior).

### 6.9 Forex Factory (`forexfactory.com`)

Implementation context:

- extractor: `ForexFactoryUrlExtractorScraper`
- fetch: Smart Search mode.

Implementation summary:
Forex Factory extractor parses feed-style story cards and reads active/last page labels from HTML state.

Behavior:

- URL source: `div.flexposts__storydisplay-info a[href]`,
- current page from active pagination label,
- max page from "last" pagination label.

## 7. Source-by-Source Listing Implementation (Properties)

### 7.1 OLX API (`api.olx.co.id`)

Implementation context:

- extractor: `OLXApiUrlExtractorScraper`
- fetch: direct OLX API (requests mode), not HTML card parsing.

Implementation summary:
OLX listing extractor is API-first and returns both URL list and optional pre-extracted property metadata. This improves downstream speed because Smart Crawl can optionally persist richer listing stubs.

Behavior:

- injects `search` query flag when needed,
- page from query `page`,
- max page computed from API `total_ads`,
- returns `metadata.item` map (`url -> Property`) when transformation succeeds.

### 7.2 Rumah123 (`rumah123.com`)

Implementation context:

- extractor: `Rumah123UrlExtractorScraper`
- fetch: Playwright with `networkidle`.

Implementation summary:
Rumah123 uses dual extraction path: standard property cards and special perumahan-baru cards.

Behavior:

- standard selector: `div[data-test-id^='property-card-'] a[href^='/properti']`,
- perumahan-baru selector uses dedicated class-based links,
- page from query `page`,
- max page from `data-test-id="srp-pagination"`.

### 7.3 Lamudi (`lamudi.co.id`)

Implementation context:

- extractors:
  - `LamudiUrlExtractorScraper` (default)
  - `LamudiProyekUrlExtractorScraper` (path-specific `proyek-baru`)

Implementation summary:
Lamudi default extractor reads LD+JSON list data (`@graph/mainEntity/itemListElement`) while proyek mode uses project card selectors.

Behavior:

- page from query `page`,
- max page inferred using shared Lamudi pagination heuristics:
  - pagination links,
  - text patterns (`halaman X dari Y`),
  - pagination class blocks.

### 7.4 99.co (`99.co`)

Implementation context:

- extractor: `NineNineUrlExtractorScraper`
- fetch: Playwright.

Implementation summary:
99.co extractor reads listing card detail links and handles `hlmn` paging parameter.

Behavior:

- empty search page returns empty URL list,
- page from query `hlmn`,
- max page from highest `hlmn` in pagination links.

## 8. Reliability and Error Handling Mechanics

Listing extraction reliability characteristics:

- unsupported source URL returns explicit 400-level extraction error,
- malformed page parameter falls back to page `1`,
- `max_page` is optional and intentionally `None` when source does not expose deterministic bounds,
- extractor-level exceptions are propagated to API error response.

## 9. Practical Summary

Smart Scrape listing implementation is a router-driven adapter layer:

- each source has dedicated extraction logic,
- all extractors return one normalized response shape,
- pagination metadata is best-effort but consistent,
- Smart Crawl receives deterministic URL discovery output for orchestration and checkpointing.
