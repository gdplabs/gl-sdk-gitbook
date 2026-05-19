---
icon: circle-exclamation
---

# Prerequisites

Before you begin using GL Smart Crawl, ensure your environment meets the following requirements.

{% stepper %}
{% step color="blue" %}
#### Python 3.11+

Both the Orchestration Layer (`applications/smart-crawl`) and Extraction Layer (`applications/custom-scrapers`) require [Python](https://www.python.org/) version 3.11 or later. We recommend 3.12.

```bash
python --version
# Python 3.12.x
```

We use [uv](https://github.com/astral-sh/uv) as the package manager and task runner for both services.

```bash
pip install uv
```
{% endstep %}

{% step color="blue" %}
#### PostgreSQL

The Orchestration Layer requires a running PostgreSQL instance for job tracking, crawl state, and article/property storage.

* Minimum version: **PostgreSQL 14**
* The database URL is configured via `SMART_CRAWLER_DB_URL`

Run database migrations before starting the Orchestration Layer:

```bash
uv run alembic upgrade head
```
{% endstep %}

{% step color="blue" %}
#### Elasticsearch (Optional)

Elasticsearch enables full-text search in the Data API and is required for the keyword query (`queries`) parameter. If not configured, the Data API falls back to PostgreSQL-only queries without full-text search.

* Minimum version: **Elasticsearch 8**
* Configure via the `ELASTICSEARCH_URL` environment variable
{% endstep %}

{% step color="blue" %}
#### Extraction Layer Service

The Orchestration Layer calls the Extraction Layer over HTTP for all URL/content extraction. The Extraction Layer must be running and accessible before crawl jobs can scrape URLs.

* Default port: **8001**
* Configure in the Orchestration Layer via:
  * `CUSTOM_SCRAPER_BASE_URL` — Extraction Layer service URL (e.g., `http://localhost:8001`)
  * `CUSTOM_SCRAPER_API_KEY` — API key for authentication
  * `CUSTOM_SCRAPER_TIMEOUT_SECONDS` — HTTP timeout per scrape request (default: `60`)

> 💡 **Tip:** If `CUSTOM_SCRAPER_BASE_URL` is not set, the Orchestration Layer runs in mock mode and returns empty scrape results.
{% endstep %}

{% step color="blue" %}
#### GL Smart Search Credentials (for Extraction Layer)

The Extraction Layer uses GL Smart Search (Firecrawl) for general URL scraping and anti-bot bypass. Configure the Extraction Layer with:

* `SMART_SEARCH_BASE_URL` — GL Smart Search service endpoint
* `SMART_SEARCH_API_TOKEN` — API token for authentication

> 💡 **Tip:** If GL Smart Search is unavailable, the Extraction Layer falls back to open-source Playwright for JavaScript-rendered pages.
{% endstep %}
{% endstepper %}
