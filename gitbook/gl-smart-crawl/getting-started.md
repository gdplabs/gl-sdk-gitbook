---
icon: flag-checkered
---

# Getting Started

This is the fastest local setup path for GL Smart Crawl.

It starts:
- **Extraction Layer** (`applications/custom-scrapers`)
- **Orchestration Layer** (`applications/smart-crawl`)

Before starting, complete [Prerequisites](prerequisites.md).

***

## Step 1: Start Extraction Layer (Smart Scrape)

```bash
cd applications/custom-scrapers
chmod +x local-start.sh
./local-start.sh
```

Verify:

```bash
curl http://localhost:8001/health-check
# {"message":"I'm alive"}
```

Run this first so Smart Crawl can call extraction endpoints.

If your setup runs **GL Smart Search locally** for general extraction, start it in its own repository with:

```bash
./local-start.sh
```

before starting Smart Crawl.

***

## Step 2: Start Orchestration Layer (Smart Crawl)

```bash
cd applications/smart-crawl
chmod +x local-start.sh
./local-start.sh
```

Verify:

```bash
curl http://localhost:8000/health
# {"status":"healthy"}
```

***

## Step 3: Trigger Your First Listing

Example: list article URLs for one date.

```bash
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/listing \
  -H "Content-Type: application/json" \
  -d '{
    "crawl_type": "article",
    "source": "cnnindonesia",
    "start_date": "2026-04-01",
    "end_date": "2026-04-01"
  }'
```

***

## Step 4: Trigger Your First Scrape

After listing, scrape pending URLs:

```bash
curl -X POST http://localhost:8000/api/v1/crawl/scheduler/scraping \
  -H "Content-Type: application/json" \
  -d '{
    "crawl_type": "article",
    "source": "cnnindonesia"
  }'
```

***

## Step 5: Retrieve Crawled Data

Query crawled results:

```bash
curl "http://localhost:8000/api/v1/data?\
start_date=2026-04-01&\
end_date=2026-04-01&\
domains=cnnindonesia&\
schema=id,title,date_published,source_name&\
page_size=10"
```

***

## Next Steps

* [**Article Crawl**](guides/article-crawl.md) - Step-by-step article listing and scraping
* [**Property Crawl**](guides/property-crawl.md) - Step-by-step property listing and scraping
* [**General Scrape**](guides/general-scrape.md) - One-off URL scraping with `response_type`, `schema`, and `prompt`
* [**Auto Crawl Scheduler**](guides/auto-crawl-scheduler.md) - Automated daily per-source runs
* [**Data API**](guides/data-api.md) - Query crawled results
