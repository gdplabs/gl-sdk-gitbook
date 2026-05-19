---
icon: newspaper
---

# Article Crawl

This guide explains the simplest way to run **article listing** (URL discovery) and **article scraping** (content extraction) in GL Smart Crawl.

***

## Supported Sources (from Auto Crawl Scheduler)

| Source | Enum Value | Auto-Scheduled | Notes |
|---|---|---|---|
| CNN Indonesia | `cnnindonesia` | ✅ | Daily scheduler enabled |
| CNBC Indonesia | `cnbcindonesia` | ✅ | Daily scheduler enabled |
| Bloomberg Technoz | `bloombergtechnoz` | ✅ | Daily scheduler enabled |
| Bisnis Indonesia | `bisnis` | ✅ | Daily scheduler enabled |
| Kontan | `kontan` | ✅ | Daily scheduler enabled |
| MetroTV News | `metrotvnews` | ✅ | Daily scheduler enabled |
| Forex Factory | `forexfactory` | ❌ | Use manual trigger |
| Google News | `googlenews` | ❌ | Use manual trigger |

***

## 1) Run Listing (Article URL Discovery)

### Option A: Let scheduler run automatically

For auto-scheduled sources, listing runs daily without manual action.

### Option B: Trigger listing manually

Use this when you want immediate run or when source is not auto-scheduled.

```bash
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/listing \
  -H "Content-Type: application/json" \
  -d '{
    "crawl_type": "article",
    "source": "cnnindonesia",
    "start_date": "2026-04-20",
    "end_date": "2026-04-20"
  }'
```

Response includes a `job_id` (async execution).

***

## 2) Run Scraping (Article Content Extraction)

After listing produces `PENDING` URLs, run scraping:

```bash
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/scraping \
  -H "Content-Type: application/json" \
  -d '{
    "crawl_type": "article",
    "source": "cnnindonesia"
  }'
```

This scrapes pending URLs for that source and updates each URL independently (`SUCCESS` or `FAILED`).

***

## 3) Quick Check

Check scheduler jobs:

```bash
curl http://localhost:8000/api/v1/crawl/scheduler/jobs
```

Check crawled data:

```bash
curl "http://localhost:8000/api/v1/data?start_date=2026-04-20&end_date=2026-04-20&domains=cnnindonesia&page=1&page_size=10"
```

***

## Notes

- Listing and scraping endpoints are asynchronous (`202 Accepted`).
- If a source is not auto-scheduled, manual trigger still works.
- Recommended flow: **run listing first**, then **run scraping**.
