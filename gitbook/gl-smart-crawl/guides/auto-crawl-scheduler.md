---
icon: clock
---

# Auto Crawl Scheduler

GL Smart Crawl includes a built-in APScheduler that runs inside the FastAPI process and manages fully automated, per-source crawling. Each source gets an independent daily cron job that runs two phases sequentially: listing (URL discovery) then scraping (content extraction).

***

## Overview

The scheduler runs two phases per source per scheduled tick:

| Phase | Description |
|-------|-------------|
| **Phase 1 – Listing** | Discovers article or property URLs for the next appropriate date and stores them as `PENDING` in the database. |
| **Phase 2 – Scraping** | Fetches content of every `PENDING` URL, processing oldest-first via bi-directional crawl pointers. |

Phases run sequentially inside the same scheduler tick, so newly listed URLs can be scraped on the same day they are discovered.

***

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                  │
│                                                         │
│  ┌─────────────────────┐    ┌──────────────────────┐    │
│  │  CrawlSchedulerService│  │     CrawlService       │    │
│  │  (APScheduler)       │    │                       │    │
│  │                      │    │  resolve_next_        │    │
│  │  daily_listing_<src> │───►│    listing_date()     │    │
│  │  (cron per source)   │    │  run_listing_job()    │    │
│  │                      │    │  run_bidirectional_   │    │
│  └─────────────────────┘    │    scrape()            │    │
│                              └──────────────────────┘    │
│                                        │                 │
│               ┌────────────────────────┘                 │
│               ▼                                          │
│  ┌────────────────────────────────────────┐              │
│  │              PostgreSQL                │              │
│  │                                        │              │
│  │  article_listing_job  (job queue)      │              │
│  │  crawled_article      (PENDING/SUCCESS)│              │
│  │  crawled_property     (PENDING/SUCCESS)│              │
│  │  source_crawl_state   (bi-dir ptrs)    │              │
│  └────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

***

## Supported Sources

### Article Sources

| Source | Enum Value | Daily Schedule (UTC) | Status |
|--------|-----------|---------------------|--------|
| CNN Indonesia | `cnnindonesia` | 02:00 | ✅ Scheduled |
| CNBC Indonesia | `cnbcindonesia` | 02:15 | ✅ Scheduled |
| Bloomberg Technoz | `bloombergtechnoz` | 02:30 | ✅ Scheduled |
| Bisnis Indonesia | `bisnis` | 02:45 | ✅ Scheduled |
| Kontan | `kontan` | 03:00 | ✅ Scheduled |
| MetroTV News | `metrotvnews` | 03:15 | ✅ Scheduled |
| Forex Factory | `forexfactory` | — | ❌ Not scheduled |
| Google News | `googlenews` | — | ❌ Not scheduled |

### Property Sources

| Source | Enum Value | Daily Schedule (UTC) | Status |
|--------|-----------|---------------------|--------|
| Rumah123 | `rumah123` | 03:30 | ✅ Scheduled (sale) |
| OLX | `olx` | — | ❌ Not scheduled |
| Lamudi | `lamudi` | — | ❌ Not scheduled |
| NineNine | `ninenine` | — | ❌ Not scheduled |

***

## Per-Source Schedule Configuration

Override each source's schedule via environment variables:

| Env Variable | Value | Description |
|---|---|---|
| `CRAWL_SCHEDULER_{SOURCE}` | `daily` | **(default)** Use built-in staggered time |
| | `02:00` or `2:0` | Run daily at this UTC time (`HH:MM`) |
| | `0 2 * * *` | Full cron expression |
| | `disabled` | Do not schedule this source |

Source names are **uppercase** in the env key:

```bash
# Override CNN to run at 03:30 UTC
CRAWL_SCHEDULER_CNNINDONESIA=03:30

# Disable CNBC from auto-scheduling
CRAWL_SCHEDULER_CNBCINDONESIA=disabled

# Use a custom cron expression for Kontan
CRAWL_SCHEDULER_KONTAN=0 4 * * *
```

***

## Article Listing — Auto-Advance Logic

The scheduler calls `resolve_next_listing_date()` each tick to determine which date to list:

| Last Job Status | Action |
|----------------|--------|
| No jobs exist | List today (first run) |
| `FAILED` | Retry the same date |
| `COMPLETED` | Advance to `last_date + 1 day` (if ≤ today) |
| `PENDING` / `IN_PROGRESS` | Skip — already queued or running |
| Already up-to-date | Return `None` — skip listing phase |

Each scheduler run lists exactly **one day**. This is intentional:
- A failure affects only a single date, not the whole backlog
- Recovery is fully automatic on the next scheduled run
- The `article_listing_job` table provides a clear audit trail per date

**Example day-by-day behaviour:**

```
Date        Scheduler Fires    Action                  Result
──────────  ─────────────────  ──────────────────────  ─────────────
March 01    02:00 UTC          No jobs → list today    March 01 COMPLETED
March 02    02:00 UTC          Last = March 01 OK      List March 02  COMPLETED
March 03    02:00 UTC          Last = March 02 OK      List March 03  FAILED ❌
March 04    02:00 UTC          Last = March 03 FAILED  Retry March 03 COMPLETED ✅
March 05    02:00 UTC          Last = March 03 OK      List March 04  COMPLETED
```

***

## Article Scraping — Bi-Directional Pointers

After listing, the scheduler runs `run_bidirectional_scrape()`. This uses two datetime pointers per source stored in the `source_crawl_state` table:

| Pointer | Column | Direction | Meaning |
|---------|--------|-----------|---------|
| **Backward** | `first_scraped_data_time` | ← past | Oldest article `date_published` scraped |
| **Forward** | `last_scraped_data_time` | → present | Newest article `date_published` scraped |

On each run:
1. `_forward_scrape`: scrapes `PENDING` articles with `listing_date >= forward_pointer.date + 1`
2. `_backward_scrape`: scrapes `PENDING` articles with `listing_date < backward_pointer.date`

Both directions run concurrently via `asyncio.gather`.

***

## API Reference

### Check Scheduler Status

```bash
GET /api/v1/crawl/scheduler/jobs
```

Returns all scheduled jobs and their next run times.

### Trigger Listing Immediately

Immediately lists a date range (blocking):

```bash
POST /api/v1/crawl/scheduler/listing
{
  "crawl_type": "article",
  "source": "cnnindonesia",
  "start_date": "2026-03-10",
  "end_date": "2026-03-12"
}
```

### Queue Listing Jobs (Non-Blocking)

Creates `PENDING` listing jobs for a date range without processing them immediately. The scheduler picks them up one day per run — recommended for back-filling:

```bash
POST /api/v1/crawl/scheduler/listing/create
{
  "source": "cnnindonesia",
  "start_date": "2026-02-01",
  "end_date": "2026-03-01"
}
```

**Response:**

```json
{
  "source": "cnnindonesia",
  "jobs_created": 28,
  "jobs_skipped": 0,
  "total_dates": 28,
  "message": "Queued 28 new listing jobs for cnnindonesia (2026-02-01 → 2026-03-01)."
}
```

### Trigger Scraping Immediately

```bash
POST /api/v1/crawl/scheduler/scraping
{
  "crawl_type": "article",
  "source": "cnnindonesia"
}
```

### Pause / Resume Scheduler

```bash
# Pause all sources
POST /api/v1/list/scheduler/pause

# Pause a specific source
POST /api/v1/list/scheduler/pause
{"source": "cnnindonesia"}

# Resume
POST /api/v1/list/scheduler/resume
```

***

## Timeout and Retry Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CRAWL_LISTING_TIMEOUT_SECONDS` | `600` | Max seconds per listing attempt. On timeout, job is marked `FAILED`. |
| `CRAWL_LISTING_RETRY_ATTEMPTS` | `3` | Attempts per listing date before failing permanently. |
| `CRAWL_LISTING_RETRY_DELAY_SECONDS` | `10` | Seconds between listing retries. |
| `CRAWL_SCRAPING_TIMEOUT_SECONDS` | `120` | Max seconds per URL scrape attempt. |
| `CRAWL_SCRAPING_RETRY_ATTEMPTS` | `2` | Attempts per URL before skipping. |
| `CRAWL_SCRAPING_RETRY_DELAY_SECONDS` | `5` | Seconds between scrape retries. |
| `CUSTOM_SCRAPER_TIMEOUT_SECONDS` | `60` | HTTP timeout for Extraction Layer service calls. |

***

## Runbook: Operating the Scheduler

### Back-fill Historical Dates (Recommended)

```bash
# 1. Queue 30 days of listing jobs (non-blocking, returns immediately)
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/listing/create \
  -H "Content-Type: application/json" \
  -d '{
    "source": "cnnindonesia",
    "start_date": "2026-02-01",
    "end_date": "2026-03-01"
  }'

# 2. Monitor progress in the database
SELECT listing_date, status, current_page, max_pages, urls_stored, error_message
FROM article_listing_job
WHERE source_name = 'cnnindonesia'
ORDER BY listing_date;
```

### Emergency Re-Run for a Specific Date

```bash
# Force immediate listing (blocking — processes all dates before returning)
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/listing \
  -H "Content-Type: application/json" \
  -d '{
    "crawl_type": "article",
    "source": "cnnindonesia",
    "start_date": "2026-03-10",
    "end_date": "2026-03-10"
  }'
```

### Reset a Failed Job

```sql
UPDATE article_listing_job
SET status = 'pending', error_message = NULL, updated_at = NOW()
WHERE source_name = 'cnnindonesia'
  AND listing_date = '2026-03-10'
  AND status = 'failed';
```

### Monitor Listing Progress

```sql
-- Overall progress per source
SELECT
    source_name,
    COUNT(*) AS total_days,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) AS completed,
    COUNT(CASE WHEN status = 'failed'    THEN 1 END) AS failed,
    COUNT(CASE WHEN status = 'pending'   THEN 1 END) AS pending,
    MAX(CASE WHEN status = 'completed' THEN listing_date END) AS last_completed_date,
    SUM(urls_stored) AS total_urls_stored
FROM article_listing_job
GROUP BY source_name
ORDER BY source_name;
```

### Check Bi-Directional Scrape Pointers

```sql
SELECT
    source_name,
    first_scraped_data_time,
    last_scraped_data_time,
    (last_scraped_data_time::date - first_scraped_data_time::date) AS scraped_window_days
FROM source_crawl_state
ORDER BY source_name;
```

### Add a New Article Source to the Scheduler

Edit `app/crawl/scheduler/service.py`:

```python
sources_config = [
    # ... existing sources ...
    {
        "crawl_type": "article",
        "source": "forexfactory",
        "schedule": {"hour": 3, "minute": 30},
        "description": "Forex Factory - Financial news",
    },
]
```

***

## API Comparison: Listing Endpoints

| Feature | `POST /crawl/scheduler/listing` | `POST /crawl/scheduler/listing/create` |
|---|---|---|
| **Processes immediately** | ✅ Yes (blocking) | ❌ No (returns immediately) |
| **Creates listing jobs** | ✅ Yes | ✅ Yes |
| **Scheduler picks up** | n/a (already done) | ✅ Yes, one day per run |
| **Best for** | Emergency / single date | Back-fill / bulk date ranges |
| **Response** | After processing completes | Immediately after job creation |
| **crawl_type** | `article` or `property` | `article` only |

> 📚 **Next Steps:** See the [Developer Reference](../resources/developer-reference/) for architecture and sequence diagrams of the crawl pipeline.
