---
icon: house
---

# Property Crawl

This guide explains the simplest way to run **property listing** (URL discovery) and **property scraping** (content extraction) in GL Smart Crawl.

***

## Supported Sources (from Auto Crawl Scheduler)

| Source | Enum Value | Auto-Scheduled | Notes |
|---|---|---|---|
| Rumah123 | `rumah123` | ✅ | Scheduled for `sale` listing type |
| OLX | `olx` | ❌ | Use manual trigger |
| Lamudi | `lamudi` | ❌ | Use manual trigger |
| NineNine | `ninenine` | ❌ | Use manual trigger |

***

## 1) Run Listing (Property URL Discovery)

### Option A: Let scheduler run automatically

For scheduled property jobs, listing runs daily based on scheduler configuration.

### Option B: Trigger listing manually

Use this for immediate crawl or for non-scheduled sources.

```bash
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/listing \
  -H "Content-Type: application/json" \
  -d '{
    "crawl_type": "property",
    "source": "rumah123",
    "query": "sale",
    "property_type": "house",
    "start_date": "2026-04-20",
    "end_date": "2026-04-20"
  }'
```

For property listing:
- `query` = listing type (`sale` or `rent`)
- `property_type` = property category (`house`, `apartment`, etc.)

***

## 2) Run Scraping (Property Content Extraction)

After listing produces `PENDING` property URLs, run scraping:

```bash
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/scraping \
  -H "Content-Type: application/json" \
  -d '{
    "crawl_type": "property",
    "source": "rumah123"
  }'
```

This scrapes pending property URLs and records per-URL success/failure.

***

## 3) Quick Check

Check scheduler jobs:

```bash
curl http://localhost:8000/api/v1/crawl/scheduler/jobs
```

Check crawled data:

```bash
curl "http://localhost:8000/api/v1/data?start_date=2026-04-20&end_date=2026-04-20&domains=rumah123&page=1&page_size=10"
```

***

## Notes

- Listing and scraping endpoints are asynchronous (`202 Accepted`).
- For non-scheduled sources (`olx`, `lamudi`, `ninenine`), use manual trigger.
- Recommended flow: **run listing first**, then **run scraping**.
