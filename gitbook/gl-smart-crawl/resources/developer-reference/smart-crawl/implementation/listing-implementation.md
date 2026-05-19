# Listing Implementation

This page explains how the GL Smart Crawl **Orchestration Layer** implements listing (URL discovery) in the current codebase, including resume behavior and source-specific logic.

> Terminology note: in code and class names, `Smart Crawl` maps to the **Orchestration Layer** and `Smart Scrape` maps to the **Extraction Layer**.

## 1. Scope and Intent

Listing is the first stage of GL Smart Crawl's pipeline at the Orchestration Layer.

Its responsibilities are:

- discover candidate URLs from each source,
- persist those URLs as crawl queue records (`PENDING`) or complete records when metadata is already available,
- maintain deterministic FIFO ordering (`list_order`) for queued records,
- track progress per job/range (`current_page`, `max_pages`, `urls_found`, `urls_stored`),
- support safe resume after timeout, retry, crash, or scheduler restart.

The Orchestration Layer delegates extraction to the Extraction Layer (`/extract-urls`) and focuses on orchestration/state integrity.

## 2. Core Components in Listing Flow

Main implementation entry points:

- `app/crawl/scheduler/service.py` (`CrawlSchedulerService`)
- `app/crawl/service/service.py` (`CrawlService`)
- `app/list/service/service.py` (`ListService`)
- `app/list/service/article/base.py` (`BaseArticleLister`, `CustomScraperArticleLister`)
- `app/list/service/article/*.py` (article source listers)
- `app/list/service/property/base.py` (`BasePropertyLister`)
- `app/list/service/property/*.py` and `app/list/service/property/olx/*.py` (property source listers)

High-level flow:

1. Scheduler triggers listing per source.
2. CrawlService prepares/retrieves listing state (article jobs or property price ranges).
3. CrawlService calls ListService with source/date/query/filter context.
4. ListService routes to the source-specific lister.
5. Lister calls Extraction Layer `/extract-urls` page-by-page.
6. URLs (and metadata when available) are persisted incrementally.
7. Callback updates job/range progress after each page.
8. Job/range is finalized as `COMPLETED` or `FAILED` based on completion criteria.

## 3. Listing State Models

### 3.1 Article state (`ArticleListingJob`)

Important fields:

- `status`: `pending | in_progress | completed | failed | skipped`
- `listing_date`: date key for a listing job (dated sources)
- `current_page`: last successfully processed page
- `max_pages`: source-reported total pages if available
- `urls_found`: total discovered URLs (cumulative per job)
- `urls_stored`: total persisted URLs (derived from DB state)

Operational behavior:

- Processing priority is `IN_PROGRESS` -> `FAILED` -> `PENDING`.
- Progress is persisted per page, not only at the end.
- Timeouts and transient errors mark job `FAILED` with partial progress retained.
- Next run resumes from saved state.

### 3.2 Property state (`PropertyPriceRange`)

Property listing is tracked by range records per `(source, listing_type, property_type, min_price, max_price)`.

Important fields:

- `status`: `pending | in_progress | completed | failed | skipped`
- `last_processed_page`: page checkpoint for resume
- `total_pages`: max page in that range
- `total_urls_found`: discovered URLs in that range
- `total_urls_stored`: persisted URLs in that range

Operational behavior:

- Processing priority is `IN_PROGRESS` -> `FAILED` -> `PENDING`.
- Progress is persisted after each processed page.
- Failed ranges remain resumable; next run continues from `last_processed_page + 1`.

## 4. Listing Modes Implemented

### 4.1 Article date-based listing (default)

Most article sources require `start_date` and `end_date`.

- The Orchestration Layer creates/upserts jobs per date in the requested range.
- Date range is validated to prevent non-consecutive gaps against existing completed coverage.
- Each date is processed with its own listing state.

### 4.2 Article undated descending listing (CNBC)

CNBC uses an undated index and descending pagination.

- `requires_date_range()` returns `False`.
- Crawl starts from higher pages (older content) and moves down to page 1 (newest).
- Completion condition is reaching `current_page <= 1`.
- Cross-day continuation is supported by inheriting prior unfinished state into today's job.

### 4.3 Property price-range listing

Property listing is executed by price range to keep result sets bounded and resumable.

- Ranges are validated/split so each range stays under page limits.
- For each range, listing starts at page 1 or resumes from `last_processed_page + 1`.
- Per-page callback persists URLs directly to `crawled_property` and updates range progress.
- Standard sources store `PENDING` stubs; sources with complete listing metadata (notably OLX) can store `SUCCESS` records immediately.

## 5. Resume, Retry, and Data Integrity Mechanics

### 5.1 Incremental persistence

`CustomScraperArticleLister` and `BasePropertyLister` persist page progress incrementally instead of waiting for full-run completion.

This protects progress when:

- request timeout occurs,
- service restarts mid-run,
- partial source failures happen.

### 5.2 FIFO ordering

`list_order` is maintained so downstream scraping can run oldest-first on queued records.

- URLs can be reordered/reconciled on resume.
- stale rows for the same listing scope can have `list_order` nullified (article).
- deduplication is applied while preserving effective chronological order.

### 5.3 Timeout and retry wrapper

Listing execution is wrapped with `async_with_timeout_and_retry(...)` in CrawlService.

Config defaults (from constants):

- `CRAWL_LISTING_TIMEOUT_SECONDS=600`
- `CRAWL_LISTING_RETRY_ATTEMPTS=3`
- `CRAWL_LISTING_RETRY_DELAY_SECONDS=10`

### 5.4 Shifting pagination recovery (CNBC)

For shifting pagination, Smart Crawl uses anchor-based resume search:

- take recent known URLs from DB as anchors,
- estimate shifted page center using delta between old/new `max_page`,
- spiral-search nearby pages for anchor overlap,
- resume from the page just below matched anchor.

This avoids duplication/omission when new content shifts older items to different pages.

### 5.5 Empty-page retry for anti-bot protected property sources

`BasePropertyLister` supports per-source empty-page retry controls.

- `empty_page_max_retries`
- `empty_page_retry_delay`
- `page_fetch_timeout`

99.co overrides these values to tolerate Cloudflare challenge windows before declaring range failure.

## 6. Source-by-Source Listing Implementation (Articles)

### 6.1 CNN Indonesia (`cnnindonesia`)

Implementation class: `CNNLister`

Implementation summary:
CNN listing uses a date-scoped index URL pattern and runs through the shared custom-scraper-first listing pipeline. It normalizes source output to FIFO order and persists progress per page.

Behavior:

- source-specific date URL format: `...?date=YYYY/MM/DD&page=N`
- `max_pages_per_date = 100`, `max_pages_default = 3`
- URL order is normalized to oldest-first before FIFO storage (`should_reverse_url_order = True`)
- implemented under `CustomScraperArticleLister` (Smart Scrape first)

Fallback notes:

- open-source path exists, but helper functions in `app/list/service/helpers.py`
  (`cnn_fetch_search_page`, `cnn_get_total_pages`, `cnn_extract_article_urls_from_page`) are placeholders/TODO.
- production listing should use Smart Scrape extraction path.

### 6.2 CNBC Indonesia (`cnbcindonesia`)

Implementation class: `CNBCLister`

Implementation summary:
CNBC uses an undated, shifting index. The lister runs in descending pagination mode and relies on resume/anchor logic so new content insertion does not break continuation.

Behavior:

- undated index mode (`requires_date_range = False`)
- descending pagination enabled (`descending_pagination = True`)
- shifting pagination enabled (`has_shifting_pagination = True`)
- default per-run page cap: `max_pages_default = 10`
- URL order normalized to oldest-first before storage

Fallback notes:

- open-source method currently returns empty result (not implemented).
- Smart Scrape extraction path is primary.

### 6.3 Bloomberg Technoz (`bloombergtechnoz`)

Implementation class: `BloombergLister`

Implementation summary:
Bloomberg Technoz listing is date-path based and assumes one index page per date. The implementation bypasses query-param date filtering and uses the source's path convention directly.

Behavior:

- date-specific path format: `/indeks/all/{YYYY-MM-DD}`
- one page per date assumption (`max_pages_per_date = 1`)
- default path-based date listing is used instead of query-param date filtering
- URL order normalized to oldest-first

Fallback notes:

- open-source method currently returns empty result.
- Smart Scrape extraction path is primary.

### 6.4 Bisnis Indonesia (`bisnis`)

Implementation class: `BisnisLister`

Implementation summary:
Bisnis listing follows the common date-and-page query pattern and uses shared custom-scraper pagination plus incremental persistence.

Behavior:

- date URL format: `...?date=YYYY-MM-DD&page=N`
- URL order normalized to oldest-first

Fallback notes:

- open-source method currently returns empty result.
- Smart Scrape extraction path is primary.

### 6.5 Kontan (`kontan`)

Implementation class: `KontanLister`

Implementation summary:
Kontan has a non-standard indeks search format. The lister builds URL parameters explicitly (day/month/year and per-page offset) so each page can be resumed deterministically.

Behavior:

- custom search indeks URL with split date params:
  `.../search/indeks?kanal=&tanggal=DD&bulan=MM&tahun=YYYY&pos=indeks&per_page=OFFSET`
- `per_page` offset increments by 20 per page (`(page_num - 1) * 20`)
- URL order normalized to oldest-first

Fallback notes:

- open-source method currently returns empty result.
- Smart Scrape extraction path is primary.

### 6.6 MetroTV News (`metrotvnews`)

Implementation class: `MetroTVLister`

Implementation summary:
MetroTV listing handles source quirks explicitly: source-side 0-based pages and often missing `max_page`. The lister infers stopping using expected page-size thresholds while still preserving page checkpoints.

Behavior:

- date URL format: `...?date=YYYY-MM-DD&page=N`
- MetroTV page index is 0-based at source; implementation converts from Smart Crawl 1-based page numbering
- source often returns `max_page = null`; stop rule uses page-size heuristic
- listing loop stops when URLs returned on a page are `< expected_urls_per_page (30)`
- URL order normalized to oldest-first

Fallback notes:

- open-source method currently returns empty result.
- Smart Scrape extraction path is primary.

### 6.7 Forex Factory (`forexfactory`)

Implementation class: `ForexFactoryLister`

Implementation summary:
Forex Factory listing uses a source-specific query endpoint and performs direct extraction through Smart Scrape. It is query-driven rather than date-window driven.

Behavior:

- uses custom query-driven API-like endpoint construction
- query is URL-encoded and appended to source-specific search parameters
- listing operation fetches from constructed endpoint via Smart Scrape extraction

Fallback notes:

- no separate open-source listing fallback in this class; on failure it returns empty listing result.

### 6.8 Google News (`googlenews`)

Implementation class: `GoogleNewsLister`

Implementation summary:
Google News listing supports three modes (search, topic, story) and optional structured query operators. It uses repeated extraction loops because Google News does not expose simple page counters consistently.

Behavior:

- supports multiple listing routes:
  - search mode (`query` or structured search fields)
  - topic mode (`topic_id`)
  - story mode (`story_id`)
- structured search fields supported:
  - `exact_phrase`, `has_words`, `exclude_words`, `website`, `when`
- ID format validation is applied for `topic_id` and `story_id`
- default pagination loops up to `max_pages_default = 5` (source does not expose simple `max_page`)

Fallback notes:

- if extraction path is unavailable/fails, method returns empty result.

## 7. Source-by-Source Listing Implementation (Properties)

### 7.1 Rumah123 (`rumah123`)

Implementation class: `Rumah123Lister`

Implementation summary:
Rumah123 uses standard website listing pages and is handled by `BasePropertyLister` flow (first-page max-page detection, subsequent-page traversal, resume support, and per-page persistence via callback in crawl mode).

Behavior:

- URL path converts listing/property labels to local format:
  - `sale -> jual`, `rent -> sewa`
  - `apartment -> apartemen`, `house -> rumah`
- query params include `minPrice`, `maxPrice`, `sort=posted-desc`, and `page` (always present)
- supports resume with `start_page` and known `max_page`
- when used via CrawlService price-range flow, per-page callback stores records and updates range checkpoint

Notes:

- storage at listing stage is usually `PENDING` stubs (content completed in scrape phase).

### 7.2 Lamudi (`lamudi`)

Implementation class: `LamudiLister`

Implementation summary:
Lamudi follows the shared property listing pipeline with Lamudi-specific URL/query formatting. It is primarily range-driven and resumable through property price-range checkpoints.

Behavior:

- URL path converts listing/property labels to local format:
  - `sale -> jual`, `rent -> sewa`
  - `apartment -> apartemen`, `house -> rumah`
- query params include `min-price`, `max-price`, optional `priceCurrency=IDR`, and `page` (only when page > 1)
- uses first-page fetch to determine `max_page`, then traverses remaining pages
- supports resume by starting from `last_processed_page + 1` at range level

Notes:

- storage at listing stage is usually `PENDING` stubs (content completed in scrape phase).

### 7.3 99.co (`ninenine`)

Implementation class: `NineNineLister`

Implementation summary:
99.co uses the shared property listing flow but with anti-bot hardening. The lister increases fetch timeout and enables empty-page retries to reduce false failures from Cloudflare challenge windows.

Behavior:

- URL path converts listing/property labels to local format:
  - `sale -> jual`, `rent -> sewa`
  - `apartment -> apartemen`, `house -> rumah`
- query params include `harga_min`, `harga_maks`, `urut=2`, and `hlmn` for pagination
- anti-bot settings:
  - `page_fetch_timeout = 120`
  - `empty_page_max_retries = 3`
  - `empty_page_retry_delay = 30.0`
- if retries are exhausted, range is marked `FAILED` and resumed on next scheduler run

Notes:

- `_format_price` helper exists, but active listing URL generation uses raw integer price params.

### 7.4 OLX (`olx`)

Implementation class: `OLXLister`

Implementation summary:
OLX is API-style and has a specialized implementation (`olx.py`, `fetcher.py`, `processor.py`, `storage.py`). In addition to URL discovery, OLX can provide listing-time metadata that allows immediate creation of full `SUCCESS` records for some URLs.

Behavior:

- URL built against API endpoint `/relevance/v4/search`
- mapping-driven category selection by `(listing_type, property_type)`
- key query params include `sorting`, `page`, `category`, `price_min`, `price_max`, `type`
- first page fetch determines `max_page` (or uses provided/default fallback)
- supports resume from arbitrary `start_page` when `max_page` is known
- returns both URL list and per-URL metadata map
- post-processing path (`OLXProcessor` + `OLXStorage`) stores:
  - complete `SUCCESS` records when metadata exists,
  - `PENDING` records when metadata is absent

Notes:

- this is the most specialized property lister and differs from other property sources that mostly enqueue `PENDING` stubs during listing.

## 8. Coverage and Scheduler Defaults

Two coverage views are important:

- **Supported in listing service (article)**: CNN, CNBC, Bloomberg, Bisnis, Kontan, MetroTV, ForexFactory, GoogleNews.
- **Supported in listing service (property)**: Rumah123, Lamudi, 99.co, OLX.

Default scheduler coverage:

- **Article daily jobs**: CNN, CNBC, Bloomberg, Bisnis, Kontan, MetroTV.
- **Property daily jobs**: each property source runs four combinations:
  - `sale/apartment`
  - `sale/house`
  - `rent/apartment`
  - `rent/house`

ForexFactory and GoogleNews are currently available via service/API flow but are not included in default daily article scheduler jobs.

## 9. Practical Summary

Current listing implementation is built around three priorities:

- **Resumability**: page-level progress persistence and retry-safe state transitions.
- **Data integrity**: deterministic ordering, deduplication, and reconciliation on resume.
- **Source adaptation**: each source has explicit URL/pagination logic while sharing one orchestration model.

For properties, the price-range model extends this with resumable sub-work units, so long-running crawls can recover precisely without restarting entire source scans.
