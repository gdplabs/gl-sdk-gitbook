# Scraping Implementation

This page explains how the GL Smart Crawl **Orchestration Layer** implements scraping (content extraction) in the current codebase, including queue-based scraping, bidirectional article scraping, and source-specific behavior.

> Terminology note: in code and class names, `Smart Crawl` maps to the **Orchestration Layer** and `Smart Scrape` maps to the **Extraction Layer**.

## 1. Scope and Intent

Scraping is the second stage of GL Smart Crawl's pipeline at the Orchestration Layer.

Its responsibilities are:

- consume discovered URLs from crawl storage,
- call the Extraction Layer to extract structured content,
- persist scrape results into article/property records,
- update crawl status (`PENDING`, `SUCCESS`, `FAILED`) per URL,
- preserve listing metadata (`list_order`, `listing_date`) when updating existing records,
- support both standard batch scraping and bidirectional article scraping.

The Orchestration Layer orchestrates scraping and state transitions. The Extraction Layer performs source-level extraction logic.

## 2. Core Components in Scraping Flow

Main implementation entry points:

- `app/crawl/scheduler/service.py` (`CrawlSchedulerService`)
- `app/crawl/service/service.py` (`CrawlService`)
- `app/scrape/service/service.py` (`ScrapeService`)
- `app/engines/custom_scraper/article/service.py` (`ArticleScraperService`)
- `app/engines/custom_scraper/property/service.py` (`PropertyScraperService`)

High-level flow:

1. Scheduler (or API trigger) starts a scrape workflow.
2. CrawlService selects scrape mode (`run_scraping_job` or `run_bidirectional_scrape`).
3. ScrapeService routes each URL by domain to article/property scraping.
4. Orchestration calls Extraction Layer `/scrape` through engine wrappers.
5. Records are created/updated with extracted data and final crawl status.
6. CrawlService aggregates per-run counters (`scraped`, `failed`, `processed`).

## 3. Scraping State Models

### 3.1 Crawl record state (`ArticleCrawledData`, `PropertyCrawledData`)

Important status behavior:

- `PENDING`: URL discovered during listing and queued for scraping.
- `SUCCESS`: scrape completed and structured fields persisted.
- `FAILED`: scrape attempt failed; record remains for retry/inspection.

Update behavior:

- existing records are updated in-place when URL already exists,
- `list_order` and `listing_date` are preserved on update,
- new records are created with generated IDs when URL is new.

### 3.2 Article pointer state (`SourceCrawlState`)

Bidirectional article scraping uses two pointers:

- `first_scraped_data_time`: backward pointer (older frontier)
- `last_scraped_data_time`: forward pointer (newer frontier)

Pointer updates occur only when a contiguous success frontier exists from the boundary side, preventing invalid pointer jumps when boundary records fail.

## 4. Scraping Modes Implemented

### 4.1 Standard queue scraping (`run_scraping_job`)

Used for normal batch scraping.

- CrawlService fetches all `PENDING` URLs (optionally filtered by `crawl_type` and `source`).
- Each URL is scraped independently through `ScrapeService.scrape_url(...)`.
- Failures are isolated per URL; one failure does not stop the batch.
- Returns `urls_scraped`, `urls_failed`, and `total_processed`.

### 4.2 Bidirectional article scraping (`run_bidirectional_scrape`)

Used by article scheduler workflow.

- Initializes source pointers if missing.
- Runs forward and backward scrape tasks (concurrently when both pointers exist).
- Forward path scrapes pending items newer than forward pointer.
- Backward path scrapes pending items older than backward pointer.
- Updates pointers only after contiguous-success frontier validation.

Implementation detail:
Bidirectional scraping is implemented in `CrawlService.run_bidirectional_scrape(...)` and uses `SourceCrawlState` as the per-source crawl frontier state.

#### 4.2.1 State and intent

Each article source keeps two pointers:

- `last_scraped_data_time` (forward pointer, moves to newer data),
- `first_scraped_data_time` (backward pointer, moves to older data).

This allows the Orchestration Layer to continue incremental ingestion in both directions without re-scraping already covered periods.

#### 4.2.2 Initialization path (no state)

When `SourceCrawlState` does not exist:

1. Smart Crawl checks the last completed listing date for the source.
2. If no completed listing exists, Smart Crawl runs listing for today as genesis.
3. Smart Crawl scrapes pending/failed URLs from genesis date.
4. Smart Crawl computes:
   - min `date_published` as `first_scraped_data_time`,
   - max `date_published` as `last_scraped_data_time`.
5. Smart Crawl creates `SourceCrawlState` with both pointers.

Returned action: `initialized`.

#### 4.2.3 Re-initialization path (state exists but pointers are empty)

When state exists but both pointers are `None`:

1. Smart Crawl re-runs the genesis flow (listing if needed, then scraping).
2. Smart Crawl recomputes min/max `date_published`.
3. Smart Crawl updates existing `SourceCrawlState` with refreshed pointers.

Returned action: `initialized`.

#### 4.2.4 Forward path behavior

Forward task runs when `last_scraped_data_time` is available:

1. Determine forward boundary date (`next_date`).
2. Query pending/failed URLs with `listing_date >= next_date` (ascending).
3. Scrape each URL via `scrape_service.scrape_url(url)`.
4. Mark each record `SUCCESS` or `FAILED`.
5. Move forward pointer only when boundary-contiguous success is preserved.

Pointer update rule for forward:

- if boundary record fails, pointer is not updated;
- if boundary succeeds, pointer advances to max `date_published` across the contiguous success zone from the boundary.

#### 4.2.5 Backward path behavior

Backward task runs when `first_scraped_data_time` is available:

1. Determine backward boundary date (`prev_date`).
2. Query pending/failed URLs with `listing_date < current_boundary_date` (descending).
3. Scrape each URL via `scrape_service.scrape_url(url)`.
4. Mark each record `SUCCESS` or `FAILED`.
5. Move backward pointer only when boundary-contiguous success is preserved.

Pointer update rule for backward:

- if boundary record fails, pointer is not updated;
- if boundary succeeds, pointer retreats to min `date_published` across the contiguous success zone from the boundary.

#### 4.2.6 Concurrency and failure isolation

When both pointers exist, forward and backward tasks run concurrently using `asyncio.gather(...)`.

If one directional task fails, the other can still finish and return its own counts. This keeps run-level progress resilient to partial directional errors.

#### 4.2.7 Response shape

Initialization response:

- `source`
- `action: initialized`
- `first_scraped_data_time`
- `last_scraped_data_time`

Normal bidirectional response:

- `source`
- `action: bidirectional`
- `forward_scraped`, `forward_failed`
- `backward_scraped`, `backward_failed`
- `first_scraped_data_time`, `last_scraped_data_time`

### 4.3 Direct scrape API (`POST /scrape`)

Smart Crawl also exposes direct scrape endpoint behavior through `ScrapeService`:

- domain-mapped article scrape,
- domain-mapped property scrape,
- optional general scrape mode (`response_type` + optional `schema`/`prompt`) for unsupported domains.

## 5. Reliability and Error Handling Mechanics

### 5.1 Per-URL failure isolation

In `run_scraping_job`, each URL is wrapped in its own try/except path.

- failed URL increments failure counter,
- loop continues for remaining URLs.

### 5.2 Record-level status integrity

On scrape success:

- record is upserted with `crawl_status=SUCCESS` and fresh `crawl_date`.

On scrape failure:

- existing record (if found) is updated to `crawl_status=FAILED`.

### 5.3 Idempotent update behavior

When URL already exists:

- Smart Crawl updates existing record rather than duplicating rows,
- listing metadata (`list_order`, `listing_date`) is retained.

### 5.4 Pointer safety in bidirectional mode

Pointers are advanced/retreated only when the boundary side is successful and success is contiguous from that boundary.

This avoids over-advancing pointers when partial failures occur mid-batch.

### 5.5 Unsupported domain handling

If URL domain is not mapped to article/property sources:

- default domain-routed scrape returns unsupported URL error,
- caller can use general mode (`response_type="article"` or `"property"`) for schema-driven extraction.

## 6. Source-by-Source Scraping Implementation (Articles)

### 6.1 CNN Indonesia (`cnnindonesia`)

Implementation context:

- source is recognized by domain mapping and routed as article scrape.
- extraction is delegated to Smart Scrape article endpoint via `ArticleScraperService`.

Implementation summary:
CNN scraping follows the standard domain-mapped article path. Smart Crawl updates existing queued records to `SUCCESS` with extracted fields while preserving listing metadata.

Behavior:

- route: `ScrapeService._scrape_article_details(...)`
- extraction call: `article_scraper_service.scrape_article(url)`
- update policy: upsert by URL, preserve `list_order`/`listing_date`
- failure policy: mark existing record `FAILED`

### 6.2 CNBC Indonesia (`cnbcindonesia`)

Implementation context:

- source is recognized by domain mapping and routed as article scrape.
- commonly used in bidirectional scheduler workflow.

Implementation summary:
CNBC scraping uses the same article scrape path but is typically executed through bidirectional crawling to maintain forward/backward time coverage.

Behavior:

- route: `ScrapeService._scrape_article_details(...)`
- extraction call: Smart Scrape article scrape
- update policy: in-place update for existing queued records
- bidirectional note: pointer updates guarded by contiguous-success checks

### 6.3 Bloomberg Technoz (`bloombergtechnoz`)

Implementation context:

- source is recognized by domain mapping and routed as article scrape.

Implementation summary:
Bloomberg Technoz scraping is handled through the standard article route with identical status/update semantics to other mapped article domains.

Behavior:

- route: standard article scrape path
- persistence: update existing or create new record
- status transitions: `PENDING -> SUCCESS` or `FAILED`

### 6.4 Bisnis Indonesia (`bisnis`)

Implementation context:

- source is recognized by domain mapping and routed as article scrape.

Implementation summary:
Bisnis scraping uses the same shared article scrape pipeline and record-upsert strategy.

Behavior:

- route: standard article scrape path
- persistence: upsert by URL
- metadata retention: preserve listing metadata on updates

### 6.5 Kontan (`kontan`)

Implementation context:

- source is recognized by domain mapping and routed as article scrape.

Implementation summary:
Kontan scraping runs through the common article extraction path with per-URL fault isolation and status integrity handling.

Behavior:

- route: standard article scrape path
- batch behavior: one URL failure does not stop others
- status: failed URLs are tracked as `FAILED`

### 6.6 MetroTV News (`metrotvnews`)

Implementation context:

- source is recognized by domain mapping and routed as article scrape.

Implementation summary:
MetroTV scraping is functionally equivalent to other mapped article sources at Smart Crawl layer; source-specific parsing remains inside Smart Scrape.

Behavior:

- route: standard article scrape path
- persistence: update-or-create record strategy
- optional indexing: synced to Elasticsearch when repository is configured

### 6.7 Forex Factory (`forexfactory`)

Implementation context:

- source enum is supported by article model, and domain fallback mapping can route forexfactory URLs.

Implementation summary:
Forex Factory scraping follows the same article scrape pipeline once URL is recognized as article source.

Behavior:

- route: standard article scrape path (domain/enum mapping)
- persistence: upsert with `SUCCESS` on extraction
- failure: mark existing record `FAILED`

### 6.8 Google News (`googlenews`)

Implementation context:

- listing from Google News can produce third-party publisher URLs.
- many publisher domains are outside Smart Crawl's domain-to-article mapping.

Implementation summary:
Google News scraping at Smart Crawl layer is best treated as a general scrape use case when URLs are outside mapped article domains. In default domain-routed mode, unsupported publisher domains will fail.

Behavior:

- mapped-domain URLs: use standard article scrape path
- unmapped-domain URLs: require general mode (`response_type="article"`) if direct API caller wants extraction
- scheduler note: Google News is not included in default daily article scheduler jobs

## 7. Source-by-Source Scraping Implementation (Properties)

### 7.1 Rumah123 (`rumah123`)

Implementation context:

- source is recognized by property domain mapping.
- listing stage typically stores `PENDING` property stubs first.

Implementation summary:
Rumah123 scraping uses standard property scrape flow: pull queued `PENDING` URLs, extract full property fields, and update records to `SUCCESS`.

Behavior:

- route: `ScrapeService._scrape_property_details(...)`
- extraction call: `property_scraper_service.scrape_property(url)`
- update policy: preserve listing metadata on existing rows
- failure policy: mark existing record `FAILED`

### 7.2 Lamudi (`lamudi`)

Implementation context:

- source is recognized by property domain mapping.

Implementation summary:
Lamudi scraping follows the same shared property scrape pipeline and update semantics as Rumah123.

Behavior:

- route: standard property scrape path
- persistence: update existing or create new property row
- status transitions: `PENDING -> SUCCESS` or `FAILED`

### 7.3 99.co (`ninenine`)

Implementation context:

- source is recognized by property domain mapping.
- URL normalization maps `99.co` to `ninenine`.

Implementation summary:
99.co scraping uses the common property scrape path after domain normalization. Any anti-bot complexity is handled on extraction side (Smart Scrape), while Smart Crawl handles retries at workflow level and status transitions.

Behavior:

- route: standard property scrape path
- mapping detail: `99.co` is normalized to `ninenine`
- persistence/status: same update-and-fail semantics as other property sources

### 7.4 OLX (`olx`)

Implementation context:

- source is recognized by property domain mapping.
- OLX listing may already store some records as `SUCCESS` when metadata is available.

Implementation summary:
OLX scraping still uses the standard property scrape pipeline for remaining queued records, but total scrape volume can be lower because listing stage may pre-fill successful records.

Behavior:

- route: standard property scrape path for pending OLX URLs
- listing interaction: URLs with full listing metadata may skip queue-based scrape because already `SUCCESS`
- failure policy: queued failures are marked `FAILED`

## 8. Coverage and Scheduler Defaults

Two coverage views are important:

- **Supported scraping domains (article)**: CNN, CNBC, Bloomberg, Bisnis, Kontan, MetroTV, ForexFactory, Google News (mapped-domain cases), plus general-mode fallback for non-mapped domains.
- **Supported scraping domains (property)**: Rumah123, Lamudi, 99.co, OLX.

Default scheduler behavior:

- **Article sources**: scheduler uses listing + bidirectional scrape workflow per source.
- **Property sources**: scheduler uses listing then `run_scraping_job(crawl_type="property", source=...)`.

## 9. Practical Summary

Current scraping implementation is built around three priorities:

- **Isolation**: per-URL failures do not break whole batches.
- **State integrity**: clear status transitions and metadata-preserving updates.
- **Chronological coverage**: bidirectional pointers for article sources keep forward/backward crawl expansion safe.

At Smart Crawl layer, scraping is intentionally source-agnostic orchestration; source-specific extraction complexity is delegated to Smart Scrape.
