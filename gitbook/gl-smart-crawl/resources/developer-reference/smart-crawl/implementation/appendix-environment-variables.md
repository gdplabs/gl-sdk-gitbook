# Appendix: Environment Variables (Smart Crawl)

This appendix lists environment variables used by the GL Smart Crawl Orchestration Layer, grouped by purpose.

## 1. Database


| Variable               | Description                                                  | Example / Notes                                                 |
| ---------------------- | ------------------------------------------------------------ | --------------------------------------------------------------- |
| `SMART_CRAWLER_DB_URL` | PostgreSQL connection string for Smart Crawl operational DB. | `postgresql://smartcrawl:password@localhost:5432/smartcrawl_db` |
| `DB_POOL_SIZE`         | SQLAlchemy pool size.                                        | `50`                                                            |
| `DB_MAX_OVERFLOW`      | Extra connections above pool size.                           | `10`                                                            |
| `DB_POOL_TIMEOUT`      | Seconds to wait for a free DB connection.                    | `30`                                                            |
| `DB_POOL_RECYCLE`      | Seconds before recycling DB connections.                     | `3600`                                                          |
| `DB_POOL_PRE_PING`     | Enable connection health-check before use.                   | `true` / `false`                                                |


## 2. Logging and Debug


| Variable               | Description                                    | Example / Notes                     |
| ---------------------- | ---------------------------------------------- | ----------------------------------- |
| `LOG_LEVEL`            | Application log level.                         | `INFO`, `DEBUG`, `WARNING`, `ERROR` |
| `LOG_FORMAT`           | Logger format mode.                            | `default`                           |
| `DEBUG_STATE`          | Enables debug behavior flags in app constants. | `false`                             |
| `SQLALCHEMY_LOG_LEVEL` | SQLAlchemy logger level.                       | `INFO`                              |


## 3. Extraction Layer Integration


| Variable                         | Description                                           | Example / Notes                              |
| -------------------------------- | ----------------------------------------------------- | -------------------------------------------- |
| `CUSTOM_SCRAPER_BASE_URL`        | Base URL for Extraction Layer (Custom Scrapers) service. | `https://custom-scraper-service.gdplabs.id/` |
| `CUSTOM_SCRAPER_API_KEY`         | API key sent to Extraction Layer service when configured. | `your-api-key-here`                          |
| `CUSTOM_SCRAPER_TIMEOUT_SECONDS` | HTTP timeout for Extraction Layer calls from Orchestration Layer. | `60`                                         |


## 4. Search Index / Data API


| Variable            | Description                                 | Example / Notes                                            |
| ------------------- | ------------------------------------------- | ---------------------------------------------------------- |
| `ELASTICSEARCH_URL` | Elasticsearch endpoint for indexing/search. | `http://localhost:9200`; set empty to disable ES features. |


## 5. Listing and Scraping Runtime Controls


| Variable                             | Description                                | Example / Notes                                              |
| ------------------------------------ | ------------------------------------------ | ------------------------------------------------------------ |
| `CRAWL_LISTING_TIMEOUT_SECONDS`      | Timeout (seconds) for listing phase.       | `600` (increase for large property listing validation runs). |
| `CRAWL_LISTING_RETRY_ATTEMPTS`       | Retry attempts for listing operations.     | `3`                                                          |
| `CRAWL_LISTING_RETRY_DELAY_SECONDS`  | Delay between listing retries (seconds).   | `30` in `.env.example`                                       |
| `CRAWL_SCRAPING_TIMEOUT_SECONDS`     | Timeout (seconds) for scraping operations. | `60` in `.env.example`                                       |
| `CRAWL_SCRAPING_RETRY_ATTEMPTS`      | Retry attempts for scraping operations.    | `3` in `.env.example`                                        |
| `CRAWL_SCRAPING_RETRY_DELAY_SECONDS` | Delay between scraping retries (seconds).  | `10` in `.env.example`                                       |


## 6. Scheduler Controls


| Variable                                   | Description                                                     | Example / Notes                                                                   |
| ------------------------------------------ | --------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `CRAWL_SCHEDULER_MAX_INSTANCES_PER_SOURCE` | Max concurrent APScheduler instances per source in one process. | Default `1`. Cross-instance overlap is controlled with PostgreSQL advisory locks. |


### 6.1 Per-source scheduler variables

Pattern:

- `CRAWL_SCHEDULER_{SOURCE}`

Supported value formats:

- `daily` (use default built-in schedule),
- `HH:MM` (UTC),
- cron expression (`min hour day month dow`),
- `disabled` (do not schedule source).

Configured source keys in current template:


| Variable                           | Description                                 | Example / Notes        |
| ---------------------------------- | ------------------------------------------- | ---------------------- |
| `CRAWL_SCHEDULER_CNNINDONESIA`     | Article source scheduler override.          | Example: `*/5 * * * *` |
| `CRAWL_SCHEDULER_CNBCINDONESIA`    | Article source scheduler override.          | Example: `daily`       |
| `CRAWL_SCHEDULER_BLOOMBERGTECHNOZ` | Article source scheduler override.          | Example: `daily`       |
| `CRAWL_SCHEDULER_BISNIS`           | Article source scheduler override.          | Example: `daily`       |
| `CRAWL_SCHEDULER_KONTAN`           | Article source scheduler override.          | Example: `daily`       |
| `CRAWL_SCHEDULER_METROTVNEWS`      | Article source scheduler override.          | Example: `daily`       |
| `CRAWL_SCHEDULER_FOREXFACTORY`     | Optional article source scheduler override. | Example: `disabled`    |
| `CRAWL_SCHEDULER_GOOGLENEWS`       | Optional article source scheduler override. | Example: `disabled`    |
| `CRAWL_SCHEDULER_RUMAH123`         | Property source scheduler override.         | Example: `daily`       |
| `CRAWL_SCHEDULER_OLX`              | Property source scheduler override.         | Example: `disabled`    |
| `CRAWL_SCHEDULER_LAMUDI`           | Property source scheduler override.         | Example: `disabled`    |
| `CRAWL_SCHEDULER_NINENINE`         | Property source scheduler override.         | Example: `disabled`    |


## 7. Quick Notes

- Source scheduler times are evaluated in UTC.
- The Orchestration Layer can run without Elasticsearch, but Data API search/index capabilities will be limited.
- For production, keep secrets (`*_API_KEY`, `*_TOKEN`, `*_SECRET`) in secret manager, not committed `.env` files.
