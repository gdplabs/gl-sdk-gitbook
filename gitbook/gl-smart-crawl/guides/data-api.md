---
icon: database
---

# Data API

The Data API provides a unified interface to retrieve crawled article and property data stored in Elasticsearch (with PostgreSQL fallback). It supports pagination, schema filtering, domain filtering, keyword search, and date range queries.

## Endpoint

```
GET /api/v1/data
```

***

## Query Parameters

### Required Parameters

| Parameter | Type | Format | Description | Example |
|-----------|------|--------|-------------|---------|
| `start_date` | string | YYYY-MM-DD | Start date for filtering | `2026-01-01` |
| `end_date` | string | YYYY-MM-DD | End date for filtering | `2026-01-31` |
| `domains` | string | comma-separated | Source domains to query | `cnnindonesia,cnbcindonesia` |

### Optional Parameters

| Parameter | Type | Default | Description | Example |
|-----------|------|---------|-------------|---------|
| `queries` | string | — | Keyword search (articles only, Elasticsearch) | `ekonomi,teknologi` |
| `schema` | string | — | Fields to return (comma-separated) | `id,title,date_published` |
| `page` | integer | 1 | Page number (1-indexed) | `2` |
| `page_size` | integer | 100 | Items per page (max 1000) | `50` |
| `after_timestamp` | string | — | Cursor-based pagination — return items after this ISO 8601 timestamp | `2026-01-15T10:30:45.123456+00:00` |

***

## Response Format

```json
{
  "data": [...],
  "metadata": {
    "page": 1,
    "page_size": 100,
    "total_items": 1500,
    "total_pages": 15,
    "has_next": true,
    "has_previous": false,
    "last_timestamp": "2026-01-15T18:45:30.123456+00:00",
    "source_integrity": [
      {
        "source_name": "cnnindonesia",
        "last_listed_data_date": "2026-01-31",
        "last_scraped_data_time": "2026-01-31T16:30:00+00:00",
        "first_scraped_data_time": "2025-06-01T08:00:00+00:00",
        "last_list_job_time": "2026-01-31T17:05:00+00:00",
        "last_scrape_job_time": "2026-01-31T17:30:00+00:00",
        "pending_count": 0,
        "failed_count": 0,
        "scraped_window_days": 244
      }
    ]
  }
}
```

### Source Integrity Fields

The `source_integrity` array provides per-source data health metadata included in every response.

| Field | Description |
|-------|-------------|
| `source_name` | Source identifier (e.g., `cnnindonesia`) |
| `last_listed_data_date` | Most recently listed article date — reflects **coverage** |
| `last_scraped_data_time` | Publication time of the most recently scraped article — reflects **freshness** |
| `first_scraped_data_time` | Earliest article publication time scraped — reflects **backward coverage** |
| `last_list_job_time` | When the last listing job completed — reflects **system health** |
| `last_scrape_job_time` | When the last scrape activity occurred — reflects **system activity** |
| `pending_count` | URLs awaiting scraping — indicates **backlog** |
| `failed_count` | URLs that failed scraping — indicates **errors** |
| `scraped_window_days` | Days spanned between first and last scraped times |

***

## Usage Examples

### Basic Query

Retrieve articles from CNN Indonesia for January 2026:

```bash
GET /api/v1/data?start_date=2026-01-01&end_date=2026-01-31&domains=cnnindonesia&page=1&page_size=50
```

### Schema Filtering

Return only specific fields to reduce payload size:

```bash
GET /api/v1/data?start_date=2026-01-01&end_date=2026-01-31&domains=cnnindonesia&schema=id,title,date_published,source_name
```

**Benefits:**
- Reduces payload size by 50–80%
- Faster response times with less serialization overhead
- Lower bandwidth usage, especially beneficial for mobile consumers

### Keyword Search

Find articles mentioning `ekonomi` or `teknologi` (Elasticsearch only):

```bash
GET /api/v1/data?start_date=2026-01-01&end_date=2026-01-31&domains=cnnindonesia,cnbcindonesia&queries=ekonomi,teknologi
```

> ⚠️ **Important:** The `queries` parameter performs full-text search and is only available when Elasticsearch is configured. It applies to article sources only — property sources are not searchable by keyword.

### Multiple Domains

Query articles and properties in a single request:

```bash
GET /api/v1/data?start_date=2026-01-01&end_date=2026-01-31&domains=cnnindonesia,rumah123&page_size=100
```

The response mixes `document_type: "article"` and `document_type: "property"` items.

***

## Pagination

### Offset-Based Pagination (Page Numbers)

Use when building traditional paginated UIs or when users need to jump to specific pages.

```bash
# Page 1
GET /api/v1/data?domains=cnnindonesia&page=1&page_size=50

# Page 2
GET /api/v1/data?domains=cnnindonesia&page=2&page_size=50
```

### Cursor-Based Pagination (Timestamps)

Use for real-time data ingestion to avoid duplicate or skipped records.

```bash
# Initial request
GET /api/v1/data?domains=cnnindonesia&page_size=100

# Continue from last_timestamp in previous response
GET /api/v1/data?domains=cnnindonesia&page_size=100&after_timestamp=2026-01-15T14:30:45.123456+00:00
```

**Benefits of cursor-based pagination:**
- No duplicate data even if new items are added between requests
- No skipped data with concurrent writes
- Deterministic — same timestamp always returns same results

***

## Available Fields

### Article Fields

**Base fields:** `id`, `source_name`, `source_url`, `crawl_date`, `crawl_status`, `document_type`

**Article-specific fields:** `title`, `subtitle`, `author`, `publisher`, `article_url`, `category`, `date_published`, `date_modified`, `tags`, `keywords`, `cover_image_url`, `canonical_url`, `og_title`, `og_image`, `meta_description`, `meta_keywords`, `content_text`, `content_html`, `summary`, `headline_highlight`, `quotes`, `inline_image_urls`, `video_urls`, `infographic_urls`, `schema_org_json`, `comment_count`, `share_count`, `like_count`

### Property Fields

**Base fields:** `id`, `source_name`, `source_url`, `crawl_date`, `crawl_status`, `document_type`

**Property-specific fields:** `property_id`, `title`, `url`, `description`, `property_type`, `listing_type`, `price`, `posting_date`, `update_date`, `longitude`, `latitude`, `address`, `area_name`, `subdistrict`, `district`, `city`, `province`, `agent_contact`, `agent_name`, `bedrooms`, `bathrooms`, `maid_bedrooms`, `maid_bathrooms`, `electricity`, `floor`, `land_area`, `building_area`

***

## Valid Domain Values

### Article Sources

| Domain | Source |
|--------|--------|
| `cnnindonesia` | CNN Indonesia |
| `cnbcindonesia` | CNBC Indonesia |
| `bloombergtechnoz` | Bloomberg Technoz |
| `bisnis` | Bisnis Indonesia |
| `kontan` | Kontan |
| `metrotvnews` | MetroTV News |

### Property Sources

| Domain | Source |
|--------|--------|
| `rumah123` | Rumah123 |
| `lamudi` | Lamudi |
| `olx` | OLX |
| `ninenine` | 99.co |

***

## Error Responses

### Invalid Domain

```json
{
  "detail": "Invalid domain(s): invalid_domain. Valid article sources: bisnis, bloombergtechnoz, cnbcindonesia, cnnindonesia, kontan, metrotvnews. Valid property sources: lamudi, ninenine, olx, rumah123."
}
```

### Invalid Schema Fields

```json
{
  "detail": "Invalid schema field(s): invalid_field. Please check the available fields for ArticleCrawledData and PropertyCrawledData models."
}
```

### Invalid Date Format

```json
{
  "detail": "Invalid date format. Expected YYYY-MM-DD."
}
```

***

## Python Integration Example

```python
import requests
from typing import List, Dict, Any

def get_articles(
    start_date: str,
    end_date: str,
    domains: List[str],
    queries: List[str] | None = None,
    schema: List[str] | None = None,
    page: int = 1,
    page_size: int = 100,
    base_url: str = "http://localhost:8000",
) -> Dict[str, Any]:
    """Fetch crawled articles with pagination."""

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "domains": ",".join(domains),
        "page": page,
        "page_size": page_size,
    }

    if queries:
        params["queries"] = ",".join(queries)

    if schema:
        params["schema"] = ",".join(schema)

    response = requests.get(f"{base_url}/api/v1/data", params=params)
    response.raise_for_status()
    return response.json()


# Retrieve all pages for a source
all_articles = []
page = 1

while True:
    result = get_articles(
        start_date="2026-01-01",
        end_date="2026-01-31",
        domains=["cnnindonesia"],
        schema=["id", "title", "date_published"],
        page=page,
        page_size=100,
    )

    all_articles.extend(result["data"])

    if not result["metadata"]["has_next"]:
        break

    page += 1

print(f"Fetched {len(all_articles)} articles across {page} pages")
```

### Incremental Polling with Source Integrity

```python
def poll_new_data(source: str, last_timestamp: str | None = None) -> str | None:
    """Poll for new scraped data using source integrity info."""

    params = {
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
        "domains": source,
        "page_size": 100,
    }

    if last_timestamp:
        params["after_timestamp"] = last_timestamp

    result = requests.get("http://localhost:8000/api/v1/data", params=params).json()

    for source_info in result["metadata"]["source_integrity"]:
        if source_info["pending_count"] > 0:
            print(f"⚠️  {source_info['pending_count']} articles not yet scraped — wait for completion")

        if source_info["failed_count"] > 0:
            print(f"❌ {source_info['failed_count']} articles failed — alert operations team")

    return result["metadata"].get("last_timestamp")
```

***

## Best Practices

1. **Use schema filtering for lists** — Only fetch fields you need. Returns 50–80% smaller payloads.
2. **Use cursor-based pagination for ingestion** — Prevents skipped or duplicate records when polling continuously.
3. **Check `source_integrity`** — Before processing data, verify `pending_count` is 0 to ensure scraping is complete.
4. **Limit date ranges** — Smaller date ranges return faster. Avoid multi-year ranges in a single query.
5. **Choose appropriate page sizes** — Mobile: 20–50, Desktop: 50–100, API export: 100–500.

> 📚 **Next Steps:** Learn how to configure automated crawling in the [Auto Crawl Scheduler](auto-crawl-scheduler.md) guide.
